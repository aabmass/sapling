/*
 * Copyright (c) Facebook, Inc. and its affiliates.
 *
 * This software may be used and distributed according to the terms of the
 * GNU General Public License version 2.
 */

use async_trait::async_trait;
use futures::stream::BoxStream;
use futures::stream::StreamExt;
use futures::task::Context;
use futures::task::Poll;
use futures::Stream;
use std::collections::HashMap;
use std::collections::VecDeque;
use std::fmt::Debug;
use std::hash::Hash;
use std::pin::Pin;

/// Resolve a stream of `I`s (inputs) into a stream of `O`s (outputs).
///
/// The resolution uses a "resolver" that can resolve `I`s in both locally and
/// remotely. `I` is attempted to be resolved locally, if that fails, a batch
/// of `I`s will be sent to remote to resolve.
pub struct HybridStream<I, O, E>(BoxStream<'static, Result<(I, O), E>>);

/// Internal state of the stream.
struct HybridStreamState<I, O, E> {
    /// Remaining inputs to resolve.
    input: BoxStream<'static, Result<I, E>>,

    /// Buffered inputs to resolve (in order).
    /// The 1st item should be unknown locally.
    buffer: VecDeque<ResolveState<I, O>>,

    /// Buffer size before sending a request.
    buffer_size: usize,

    /// Pending remote request. The stream populates `response`.
    request: Option<BoxStream<'static, Result<(I, O), E>>>,

    /// Result from consumed `request` stream.
    response: HashMap<I, O>,

    /// Defines how to resolve I to O.
    resolver: Box<dyn HybridResolver<I, O, E> + Send + Sync + 'static>,
}

/// Defines how to resolve input to output using local data and remote data.
/// The output stream preserves the order of the input stream.
#[async_trait]
pub trait HybridResolver<I, O, E> {
    /// Attempt to resolve I using local data.
    fn resolve_local(&mut self, input: &I) -> Result<Option<O>, E>;

    /// Resolve I using remote data in batch. The output stream can be out-of-order.
    async fn resolve_remote(
        &mut self,
        input: &[I],
    ) -> Result<BoxStream<'static, Result<(I, O), E>>, E>;
}

#[derive(Debug)]
enum ResolveState<I, O> {
    Resolved(I, O),
    NotResolved(I),
}

impl<I, O, E> HybridStream<I, O, E>
where
    I: Eq + Hash + Clone + Send + Sync + Debug + 'static,
    O: Send + Sync + Debug + 'static,
    E: 'static,
{
    /// Create a new `HybridStream`.
    pub fn new(
        stream: BoxStream<'static, Result<I, E>>,
        resolver: impl HybridResolver<I, O, E> + Send + Sync + 'static,
        buffer_size: usize,
    ) -> Self {
        let state = HybridStreamState {
            input: stream,
            buffer: Default::default(),
            response: Default::default(),
            buffer_size: buffer_size.max(1),
            request: Default::default(),
            resolver: Box::new(resolver),
        };
        let stream = futures::stream::unfold(state, |mut state| async {
            let item = state.next_item().await;
            item.transpose().map(|i| (i, state))
        });
        Self(Box::pin(stream.fuse()))
    }
}

impl<I, O, E> Stream for HybridStream<I, O, E>
where
    I: Eq + Hash + Clone + Send + Sync + Debug + 'static,
    O: Send + Sync + Debug + 'static,
    E: 'static,
{
    type Item = Result<(I, O), E>;

    fn poll_next(mut self: Pin<&mut Self>, cx: &mut Context) -> Poll<Option<Self::Item>> {
        Stream::poll_next(self.0.as_mut(), cx)
    }
}

impl<I, O, E> HybridStreamState<I, O, E>
where
    I: Eq + Hash + Clone + Debug,
    O: Debug,
{
    /// A future to produce one `next` item.
    async fn next_item(&mut self) -> Result<Option<(I, O)>, E> {
        loop {
            let item = self.buffer.pop_front();
            match item {
                None => {
                    let count = self.fill_buffer().await?;
                    if count == 0 {
                        // Empty buffer. Input stream has ended.
                        break Ok(None);
                    }
                }
                Some(ResolveState::Resolved(i, o)) => break Ok(Some((i, o))),
                Some(ResolveState::NotResolved(i)) => {
                    if let Some(o) = self.response.remove(&i) {
                        break Ok(Some((i, o)));
                    } else {
                        self.buffer.push_front(ResolveState::NotResolved(i));
                        self.poll_remote().await?;
                    }
                }
            }
        }
    }

    /// Prepare a buffer of inputs. Part of them resolved locally. The remaining
    /// are to be resolved remotely.
    ///
    /// Returns number of items pushed to the buffer.
    ///
    /// Consumes items from `self.input`. Updates `self.buffer`.
    async fn fill_buffer(&mut self) -> Result<usize, E> {
        let mut count = 0;
        while self.buffer.len() < self.buffer_size {
            let next_input = self.input.next().await.transpose()?;
            match next_input {
                Some(input) => {
                    // Attempt to resolve it locally.
                    let state = match self.resolver.resolve_local(&input)? {
                        Some(output) => ResolveState::Resolved(input, output),
                        None => ResolveState::NotResolved(input),
                    };
                    self.buffer.push_back(state);
                    count += 1;
                }
                // Reached the end.
                None => break,
            }
        }
        Ok(count)
    }

    /// Make progress related to the remote request.
    ///
    /// If there is no pending request, send a new one if necessary.
    /// If there is an existing request, read from it (`self.request`),
    /// and updates `self.response`.
    async fn poll_remote(&mut self) -> Result<(), E> {
        // Send a batch request if any input is unresolved and there is no
        // pending request.
        match self.request {
            None => {
                let batch: Vec<I> = self.remote_input();
                if !batch.is_empty() {
                    let request = self.resolver.resolve_remote(&batch).await?;
                    self.request = Some(request);
                }
            }
            Some(ref mut stream) => match stream.next().await {
                None => self.request = None,
                Some(Ok((i, o))) => {
                    self.response.insert(i, o);
                }
                Some(Err(e)) => {
                    self.request = None;
                    return Err(e);
                }
            },
        }
        Ok(())
    }

    /// Input for a remote request.
    fn remote_input(&self) -> Vec<I> {
        self.buffer
            .iter()
            .filter_map(|i| match i {
                ResolveState::NotResolved(i) => {
                    if self.response.contains_key(&i) {
                        // The item was fetched previously.
                        // This can happen when retry requests were sent.
                        None
                    } else {
                        Some(i)
                    }
                }
                ResolveState::Resolved(_, _) => None,
            })
            .cloned()
            .collect()
    }
}

#[cfg(test)]
mod tests {
    use super::*;
    use futures::stream;
    use futures::stream::StreamExt;
    use std::sync::Arc;
    use std::sync::Mutex;
    use tokio::time::{delay_for, Duration};

    #[tokio::test]
    async fn test_hybrid_stream() {
        type I = usize;
        type O = String;
        type E = std::io::Error;

        #[derive(Default)]
        struct Resolver {
            cached: Arc<Mutex<HashMap<usize, String>>>,
        }

        #[async_trait]
        impl HybridResolver<I, O, E> for Resolver {
            fn resolve_local(&mut self, input: &I) -> Result<Option<O>, E> {
                Ok(self.cached.lock().unwrap().get(input).cloned())
            }

            async fn resolve_remote(
                &mut self,
                input: &[I],
            ) -> Result<BoxStream<'static, Result<(I, O), E>>, E> {
                let cached = self.cached.clone();
                // Exercise ".await" in this function.
                delay_for(Duration::from_millis(1)).await;
                let input: Vec<I> = input.iter().cloned().collect();
                let output_iter = input.into_iter().map(move |i| {
                    let o = i.to_string();
                    cached.lock().unwrap().insert(i, o.clone());
                    Ok((i, o))
                });
                Ok(Box::pin(stream::iter(output_iter)))
            }
        }

        for &buffer_size in [0, 1, 2, 10].iter() {
            let input = stream::iter(vec![0, 1, 3, 5, 10].into_iter().map(Ok));
            let resolver = Resolver::default();
            resolver.cached.lock().unwrap().insert(1, "one".to_string());
            let mut stream = HybridStream::new(Box::pin(input), resolver, buffer_size);
            let u = |v: Option<Result<(I, O), E>>| v.unwrap().unwrap();
            assert_eq!(u(stream.next().await), (0, "0".to_string()));
            assert_eq!(u(stream.next().await), (1, "one".to_string()));
            assert_eq!(u(stream.next().await), (3, "3".to_string()));
            assert_eq!(u(stream.next().await), (5, "5".to_string()));
            assert_eq!(u(stream.next().await), (10, "10".to_string()));
            assert!(stream.next().await.is_none());
            assert!(stream.next().await.is_none());
        }
    }
}
