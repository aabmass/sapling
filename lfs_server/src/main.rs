// Copyright (c) 2004-present, Facebook, Inc.
// All Rights Reserved.
//
// This software may be used and distributed according to the terms of the
// GNU General Public License version 2 or any later version.

#![recursion_limit = "256"]
#![feature(async_await, async_closure, option_flattening, never_type)]
#![deny(warnings)]

use clap::Arg;
use failure::{err_msg, Error};
use fbinit::FacebookInit;
use futures::{Future, IntoFuture};
use futures_preview::{FutureExt, TryFutureExt};
use futures_util::{compat::Future01CompatExt, try_future::try_join_all};
use gotham::bind_server;
use scuba::ScubaSampleBuilder;
use slog::warn;
use std::collections::HashMap;
use std::net::ToSocketAddrs;
use tokio::net::TcpListener;
use tokio_openssl::SslAcceptorExt;

use blobrepo_factory::open_blobrepo;
use failure_ext::chain::ChainExt;
use metaconfig_parser::RepoConfigs;
use mononoke_types::RepositoryId;

use cmdlib::{args, monitoring::start_fb303_and_stats_agg};

use crate::handler::MononokeLfsHandler;
use crate::lfs_server_context::{LfsServerContext, ServerUris};
use crate::middleware::{
    ClientIdentityMiddleware, LogMiddleware, OdsMiddleware, RequestContextMiddleware,
    ScubaMiddleware, ServerIdentityMiddleware, TimerMiddleware,
};
use crate::router::build_router;

mod batch;
mod download;
mod errors;
mod handler;
mod lfs_server_context;
mod middleware;
mod protocol;
mod router;
mod str_serialized;
mod upload;
#[macro_use]
mod http;

const ARG_SELF_URL: &str = "self-url";
const ARG_UPSTREAM_URL: &str = "upstream-url";
const ARG_LISTEN_HOST: &str = "listen-host";
const ARG_LISTEN_PORT: &str = "listen-port";
const ARG_TLS_CERTIFICATE: &str = "tls-certificate";
const ARG_TLS_PRIVATE_KEY: &str = "tls-private-key";
const ARG_TLS_CA: &str = "tls-ca";
const ARG_TLS_TICKET_SEEDS: &str = "tls-ticket-seeds";
const ARG_SCUBA_DATASET: &str = "scuba-dataset";
const ARG_ALWAYS_WAIT_FOR_UPSTREAM: &str = "always-wait-for-upstream";

const SERVICE_NAME: &str = "mononoke_lfs_server";

#[fbinit::main]
fn main(fb: FacebookInit) -> Result<(), Error> {
    let app = args::MononokeApp {
        hide_advanced_args: true,
    }
    .build("Mononoke LFS Server")
    .arg(
        Arg::with_name(ARG_LISTEN_HOST)
            .long("--listen-host")
            .takes_value(true)
            .default_value("127.0.0.1")
            .help("The host to listen on locally"),
    )
    .arg(
        Arg::with_name(ARG_LISTEN_PORT)
            .long("--listen-port")
            .takes_value(true)
            .default_value("8001")
            .help("The port to listen on locally"),
    )
    .arg(
        Arg::with_name(ARG_TLS_CERTIFICATE)
            .long("--tls-certificate")
            .takes_value(true),
    )
    .arg(
        Arg::with_name(ARG_TLS_PRIVATE_KEY)
            .long("--tls-private-key")
            .takes_value(true),
    )
    .arg(
        Arg::with_name(ARG_TLS_CA)
            .long("--tls-ca")
            .takes_value(true),
    )
    .arg(
        Arg::with_name(ARG_TLS_TICKET_SEEDS)
            .long("--tls-ticket-seeds")
            .takes_value(true),
    )
    .arg(
        Arg::with_name(ARG_SELF_URL)
            .takes_value(true)
            .required(true)
            .help("The base URL for this server"),
    )
    .arg(
        Arg::with_name(ARG_UPSTREAM_URL)
            .takes_value(true)
            .help("The base URL for an upstream server"),
    )
    .arg(
        Arg::with_name(ARG_SCUBA_DATASET)
            .long(ARG_SCUBA_DATASET)
            .takes_value(true)
            .help("The name of the scuba dataset to log to"),
    )
    .arg(
        Arg::with_name(ARG_ALWAYS_WAIT_FOR_UPSTREAM)
            .long(ARG_ALWAYS_WAIT_FOR_UPSTREAM)
            .takes_value(false)
            .help("Whether to always wait for an upstream response (primarily useful in testing)"),
    );

    let app = args::add_fb303_args(app);

    let matches = app.get_matches();

    let caching = args::init_cachelib(fb, &matches);
    let logger = args::init_logging(&matches);
    let myrouter_port = args::parse_myrouter_port(&matches);

    let listen_host = matches.value_of(ARG_LISTEN_HOST).unwrap();
    let listen_port = matches.value_of(ARG_LISTEN_PORT).unwrap();

    let tls_certificate = matches.value_of(ARG_TLS_CERTIFICATE);
    let tls_private_key = matches.value_of(ARG_TLS_PRIVATE_KEY);
    let tls_ca = matches.value_of(ARG_TLS_CA);
    let tls_ticket_seeds = matches.value_of(ARG_TLS_TICKET_SEEDS);

    let mut scuba_logger = if let Some(scuba_dataset) = matches.value_of(ARG_SCUBA_DATASET) {
        ScubaSampleBuilder::new(fb, scuba_dataset)
    } else {
        ScubaSampleBuilder::with_discard()
    };

    scuba_logger.add_common_server_data();

    let server = ServerUris::new(
        matches.value_of(ARG_SELF_URL).unwrap(),
        matches.value_of(ARG_UPSTREAM_URL),
    )?;

    let RepoConfigs {
        metaconfig: _,
        repos,
        common,
    } = args::read_configs(&matches)?;

    let futs = repos
        .into_iter()
        .filter(|(_name, config)| config.enabled)
        .map(|(name, config)| {
            open_blobrepo(
                fb,
                config.storage_config.clone(),
                RepositoryId::new(config.repoid),
                myrouter_port,
                caching,
                config.bookmarks_cache_ttl,
                config.redaction,
                common.scuba_censored_table.clone(),
                config.filestore.clone(),
                logger.clone(),
            )
            .compat()
            .map(|repo| repo.map(|repo| (name, repo)))
        });

    let mut runtime = tokio::runtime::Runtime::new()?;

    start_fb303_and_stats_agg(fb, &mut runtime, SERVICE_NAME, &logger, &matches)?;

    let repos: HashMap<_, _> = runtime
        .block_on(try_join_all(futs).compat())?
        .into_iter()
        .collect();

    let ctx = LfsServerContext::new(
        fb,
        logger.clone(),
        repos,
        server,
        matches.is_present(ARG_ALWAYS_WAIT_FOR_UPSTREAM),
    )?;

    let router = build_router(ctx);

    let root = MononokeLfsHandler::builder()
        .add(ClientIdentityMiddleware::new())
        .add(RequestContextMiddleware::new())
        .add(LogMiddleware::new(logger.clone()))
        .add(ServerIdentityMiddleware::new())
        .add(ScubaMiddleware::new(scuba_logger))
        .add(OdsMiddleware::new())
        .add(TimerMiddleware::new())
        .build(router);

    let addr = format!("{}:{}", listen_host, listen_port);

    let addr = addr
        .to_socket_addrs()
        .chain_err(err_msg("Invalid Listener Address"))?
        .next()
        .ok_or(err_msg("Invalid Socket Address"))?;

    let listener = TcpListener::bind(&addr).chain_err(err_msg("Could not start TCP listener"))?;

    match (tls_certificate, tls_private_key, tls_ca, tls_ticket_seeds) {
        (Some(tls_certificate), Some(tls_private_key), Some(tls_ca), tls_ticket_seeds) => {
            let config = secure_utils::SslConfig {
                cert: tls_certificate.to_string(),
                private_key: tls_private_key.to_string(),
                ca_pem: tls_ca.to_string(),
            };

            let tls_ticket_seeds = tls_ticket_seeds
                .unwrap_or(secure_utils::fb_tls::SEED_PATH)
                .to_string();

            let tls_builder = secure_utils::build_tls_acceptor_builder(config.clone())?;
            let fbs_tls_builder = secure_utils::fb_tls::tls_acceptor_builder(
                logger.clone(),
                config.clone(),
                tls_builder,
                tls_ticket_seeds,
            )?;
            let acceptor = fbs_tls_builder.build();

            let server = bind_server(listener, root, move |socket| {
                acceptor.accept_async(socket).map_err({
                    let logger = logger.clone();
                    move |e| {
                        warn!(&logger, "TLS handshake failed: {:?}", e);
                        ()
                    }
                })
            });

            runtime
                .block_on(server)
                .map_err(|()| err_msg("Server failed"))?;
        }
        (None, None, None, None) => {
            let server = bind_server(listener, root, |socket| Ok(socket).into_future());

            runtime
                .block_on(server)
                .map_err(|()| err_msg("Server failed"))?;
        }
        _ => return Err(err_msg("TLS flags must be passed together")),
    }

    Ok(())
}
