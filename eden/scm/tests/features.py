# Copyright (c) Facebook, Inc. and its affiliates.
#
# This software may be used and distributed according to the terms of the
# GNU General Public License version 2.

mutationblacklist = """
    test-commitcloud-backup-all.t
    test-commitcloud-sync-oscillation.t
    test-fb-hgext-hiddenerror.t
    test-fb-hgext-snapshot-show.t
    test-fb-hgext-treemanifest-infinitepush.t
    test-fb-hgext-treemanifest-treeonly-linknodes.t
    test-hggit-incoming.t
    test-infinitepush-forwardfillerqueue.t
    test-infinitepush-replaybookmarksqueue-ignore-backup.t
    test-infinitepush-replaybookmarksqueue-multiple-updates.t
    test-infinitepush-replaybookmarksqueue-one-bookmark.t
    test-inherit-mode.t
    test-mutation-fromobsmarkers.t
    test-rebase-dest.t
    test-revset2.t
    test-obsmarker-template-t.py
""".split()

narrowheadsincompatiblelist = """
    test-bookmarks.t
    test-hgext-perfsuite.t
    test-revset2.t

    test-revset-t.py
"""

segmentedchangelogcompatiblelist = """
    test-abort-checkin-t.py
    test-absorb-edit-lines.t
    test-absorb-phase-t.py
    test-absorb-remotefilelog-segments.t
    test-absorb-strip.t
    test-add.t
    test-adding-invalid-utf8-t.py
    test-addremove-similar.t
    test-alias-circular.t
    test-alias.t
    test-alias2.t
    test-amend-next.t
    test-amend-previous.t
    test-amend-rebase-inmemory.t
    test-amend-restack-auto.t
    test-amend-restack-divergence.t
    test-amend-restack-multidest.t
    test-amend-restack-obsolete.t
    test-amend-split.t
    test-amend-template-t.py
    test-amend-to.t
    test-amend-userestack.t
    test-amend.t
    test-annotate.py
    test-arbitraryfilectx.t
    test-archive-symlinks.t
    test-argspans.py
    test-atomictempfile.py
    test-auth-match.t
    test-autofix.t
    test-bad-extension.t
    test-bad-pull.t
    test-basic.t
    test-batching.py
    test-bdiff.py
    test-bindag-t.py
    test-bisect3.t
    test-bookmarks-current.t
    test-bookmarks-loading-order.t
    test-bookmarks-merge.t
    test-bookmarks-rebase.t
    test-bookmarks-strip.t
    test-bookmarkstore.py
    test-casecollision.t
    test-changelog-exec.t
    test-check-clang-format.t
    test-check-code.t
    test-check-execute.t
    test-check-fix-code.t
    test-check-help.t
    test-check-interfaces.py
    test-check-win32-signature.py
    test-checkoutidentifier-commitinfo.t
    test-checkoutidentifier-dirstateinfo.t
    test-clienttelemetry.t
    test-command-template2-t.py
    test-commit-amend.t
    test-commit-interactive-curses.t
    test-commit-reuse.t
    test-commit-revive.t
    test-commit-size-limits.t
    test-commit-unresolved.t
    test-commitcloud-background-logging-perms.t
    test-commitcloud-backup-compression.t
    test-commitcloud-backup-logging.t
    test-commitcloud-backup-remotenames.t
    test-commitcloud-backup-share.t
    test-commitcloud-checkoutlocations-update.t
    test-commitcloud-list-workspaces-t.py
    test-commitcloud-smartlog-version.t
    test-commitcloud-smartlog.t
    test-commitcloud-sync-rb-enabling.t
    test-commitcloud-sync-workspacenames-t.py
    test-committer.t
    test-completion.t
    test-config-configfile.t
    test-config.t
    test-configparser-t.py
    test-conflict.t
    test-contrib-check-code.t
    test-convert-authormap-t.py
    test-convert.t
    test-copytrace-manual-t.py
    test-crdump-commitcloud.t
    test-ctrl-c.t
    test-custom-filters-t.py
    test-debugbundle-rebase.t
    test-debugbundle.t
    test-debugcauserusterror.t
    test-debugcheckcasecollisions-treemanifest.t
    test-debugcommands.t
    test-debugdifftree-t.py
    test-debugdirs.py
    test-debugdynamicconfig.t
    test-debugexistingcasecollisions-t.py
    test-debugextensions.t
    test-debugignore.t
    test-debugmetalog-t.py
    test-debugrebuilddirstate-corrupt.t
    test-debugshell-args.t
    test-debugsmallcommitmetadata.t
    test-debugthrowrustexception.t
    test-demandimport.py
    test-deprecate.t
    test-devel-warnings.t
    test-diff-antipatience-t.py
    test-diff-binary.t
    test-diff-color.t
    test-diff-copy-depth.t
    test-diff-hashbinary.t
    test-diff-ignore-whitespace.t
    test-diff-indent-heuristic.t
    test-diff-subdir-t.py
    test-diff-unified.t
    test-diff-upgrade.t
    test-diffstat.t
    test-dirstate-backup.t
    test-dirstate-completion-t.py
    test-dirstate-nonnormalset.t
    test-dirstate-rebuild.t
    test-dirstate-symlink-t.py
    test-dirstate.t
    test-disable-bad-features-t.py
    test-disablesymlinks.t
    test-dispatch-debug-prefix-t.py
    test-dispatch.t
    test-doctest.py
    test-dott-quote-t.py
    test-dott-translate.py
    test-duplicateoptions.py
    test-dynamicconfig-unicode.t
    test-edit-tmp.t
    test-editor-filename.t
    test-empty-dir.t
    test-empty-file.t
    test-encode.t
    test-encoding-align.t
    test-encoding-func.py
    test-encoding-textwrap.t
    test-eolfilename.t
    test-execute-bit.t
    test-exitcodemask-t.py
    test-extension-hgext-prefix.t
    test-extension-inline.t
    test-extensions-afterloaded.t
    test-extensions-default.t
    test-extensions-wrapfunction.py
    test-fb-convert-repo.py
    test-fb-hgext-absorb-filefixupstate.py
    test-fb-hgext-arcconfig-t.py
    test-fb-hgext-catnotate.t
    test-fb-hgext-checkmessagehook-t.py
    test-fb-hgext-copytrace-amend.t
    test-fb-hgext-copytrace-mergedriver-t.py
    test-fb-hgext-debugcommitmessage-t.py
    test-fb-hgext-diff-since-last-submit-t.py
    test-fb-hgext-edrecord.t
    test-fb-hgext-errorredirect.t
    test-fb-hgext-extorder.t
    test-fb-hgext-extutil.py
    test-fb-hgext-fastannotate-revmap.py
    test-fb-hgext-fbhistedit-exec-obsolete.t
    test-fb-hgext-fbhistedit-exec.t
    test-fb-hgext-fbhistedit-graft.t
    test-fb-hgext-fbhistedit-json.t
    test-fb-hgext-fbhistedit-show-plan.t
    test-fb-hgext-fbhistedit-stop-obsolete.t
    test-fb-hgext-fbhistedit-stop.t
    test-fb-hgext-generic-bisect.py
    test-fb-hgext-githelp.t
    test-fb-hgext-grepdiff.t
    test-fb-hgext-grpcheck.t
    test-fb-hgext-morestatus.t
    test-fb-hgext-myparent.t
    test-fb-hgext-ownercheck-t.py
    test-fb-hgext-patchrmdir.py
    test-fb-hgext-phabdiff.t
    test-fb-hgext-phabstatus.t
    test-fb-hgext-rage.t
    test-fb-hgext-remotefilelog-bundleloop-t.py
    test-fb-hgext-remotefilelog-commit-repack-t.py
    test-fb-hgext-remotefilelog-datapack.py
    test-fb-hgext-remotefilelog-histpack.py
    test-fb-hgext-remotefilelog-localdatarepack-full.t
    test-fb-hgext-remotefilelog-rust-lfs.t
    test-fb-hgext-remotefilelog-ruststores-lfs-bundle.t
    test-fb-hgext-remotefilelog-ruststores-lfs-duplicated.t
    test-fb-hgext-sampling.t
    test-fb-hgext-scm-prompt-compat.t
    test-fb-hgext-scm-prompt-git.t
    test-fb-hgext-scm-prompt-hg.t
    test-fb-hgext-sigtrace.t
    test-fb-hgext-simplecache.t
    test-fb-hgext-smartlog-smallcommitmetadata.t
    test-fb-hgext-smartlog.t
    test-fb-hgext-snapshot-show.t
    test-fb-hgext-snapshot-sync.t
    test-fb-hgext-sshaskpass.py
    test-fb-hgext-syncstatus-t.py
    test-fb-hgext-template-stat.t
    test-fb-hgext-treemanifest-bad-tree.t
    test-fb-hgext-treemanifest-convertflat.t
    test-fb-hgext-treemanifest-sendtrees.t
    test-fb-hgext-treemanifest-sparse-prefetch.t
    test-fb-hgext-treemanifest-sparse-t.py
    test-fb-hgext-tweakdefaults-bookmarks-t.py
    test-fb-hgext-tweakdefaults-grep.t
    test-fb-hgext-tweakdefaults-opawarecommands.t
    test-fb-hgext-tweakdefaults-ordering-t.py
    test-fb-hgext-tweakdefaults-revsets.t
    test-filecache.py
    test-filelog.py
    test-fileset-generated.t
    test-getbundle.t
    test-git-changelog.t
    test-gitignore-t.py
    test-globalrevs-svnrev.t
    test-help.t
    test-hg-parseurl.py
    test-hgext-logginghelper.t
    test-hggit-clone.t
    test-hggit-conflict-1.t
    test-hggit-conflict-2.t
    test-hggit-convergedmerge.t
    test-hggit-empty-working-tree.t
    test-hggit-encoding.t
    test-hggit-external-sync.t
    test-hggit-extra.t
    test-hggit-file-removal.t
    test-hggit-git-clone.t
    test-hggit-hg-author.t
    test-hggit-illegal-contents.t
    test-hggit-incoming.t
    test-hggit-keywords.t
    test-hggit-merge.t
    test-hggit-nodemap.t
    test-hggit-outgoing.t
    test-hggit-pull-after-strip.t
    test-hggit-push.t
    test-hggit-renames.t
    test-hggit-timezone.t
    test-hggit-tree-decomposition.t
    test-hggit-url-parsing.py
    test-hggit-verify-fail.t
    test-hghave.t
    test-hgrc.t
    test-hint.t
    test-histedit-bookmark-motion.t
    test-histedit-drop.t
    test-histedit-fold-non-commute.t
    test-histedit-fold.t
    test-histedit-non-commute-abort.t
    test-histedit-non-commute.t
    test-histedit-templates.t
    test-hybridencode.py
    test-import-context.t
    test-import-eol.t
    test-import-git.t
    test-include-fail.t
    test-infinitepush-push-to-other.t
    test-install.t
    test-issue1089-t.py
    test-issue1877.t
    test-issue2137-t.py
    test-issue4074.t
    test-known.t
    test-lfs-journal-t.py
    test-lfs-localstore.t
    test-lfs-pointer.py
    test-linelog-edits.py
    test-linerange.py
    test-linkrevcache-linkrevdb.py
    test-lock.py
    test-log-dir-t.py
    test-log-exthook.t
    test-log-simplify-grandparents.t
    test-lrucachedict.py
    test-manifest-insert-before-remove.py
    test-manifest.py
    test-match.py
    test-merge-changedelete.t
    test-merge-conflict-count.t
    test-merge-force.t
    test-merge-halt.t
    test-merge-internal-tools-pattern.t
    test-merge-issue5091.t
    test-merge-local.t
    test-merge-relative-paths.t
    test-merge-update-noconflict.t
    test-merge2.t
    test-mergedriver2.t
    test-metalog-migration-t.py
    test-minirst.py
    test-mkdir-broken-symlink-t.py
    test-mmap-unlink.t
    test-mutation-fromobsmarkers.t
    test-mutation-loops.t
    test-mutation-phases.t
    test-namespaces.t
    test-narrow-heads-migration.t
    test-nested-repo-t.py
    test-origbackup-conflict.t
    test-patch-offset.t
    test-pathconflicts-update.t
    test-pathencode.py
    test-paths.t
    test-patterns.t
    test-perftrace.t
    test-perftweaks.t
    test-profile.t
    test-progress-classicrenderer.t
    test-progress-fancyrenderer.t
    test-progress-rust.t
    test-progressfile.t
    test-purge.t
    test-pushrebase-obsolete.t
    test-rebase-base-flag.t
    test-rebase-copy-relations.t
    test-rebase-inmemory-conflicts.t
    test-rebase-inmemory-mergedriver-exception.t
    test-rebase-missing-cwd.t
    test-rebase-partial.t
    test-rebase-templates.t
    test-rebase-transaction.t
    test-rebuildstate.t
    test-record.t
    test-remotenames-paths.t
    test-remove.t
    test-repo-leak.t
    test-requires-t.py
    test-restack-old-stack-t.py
    test-revert-flags.t
    test-revert-interactive.t
    test-revert-status.t
    test-revlog-packentry.t
    test-revlog-raw.py
    test-revset-dirstate-parents.t
    test-root-t.py
    test-run-tests.py
    test-rust-rmcwd.t
    test-rust-subcommands-t.py
    test-rustthreading.py
    test-seq.t
    test-serve.t
    test-share-requirements-t.py
    test-share-unshare-t.py
    test-show.t
    test-simplekeyvaluefile.py
    test-simplemerge.py
    test-smartlog-collapse-obsolete.t
    test-sortdictfilter.t
    test-sparse-casecollision.t
    test-sparse-clear-t.py
    test-sparse-diff.t
    test-sparse-extensions-t.py
    test-sparse-fetch-t.py
    test-sparse-ignore.t
    test-sparse-import.t
    test-sparse-issues-t.py
    test-sparse-merges.t
    test-sparse-notsparse-t.py
    test-sparse-profiles.t
    test-sparse-rebase.t
    test-sparse-unsafe-sparse-profile.t
    test-sparse-warn-t.py
    test-ssh-hang.t
    test-sshserver.py
    test-status-color.t
    test-status-inprocess.py
    test-status-mlog.t
    test-status-terse-t.py
    test-subcommands.t
    test-template-filestat.t
    test-tools.t
    test-treemanifest-amend.t
    test-treemanifest-diff-t.py
    test-treestate-needcheck.t
    test-treestate-repack.t
    test-treestate-upgrade-t.py
    test-treestate.py
    test-ui-color.py
    test-ui-config.py
    test-ui-verbosity.py
    test-uncommit.t
    test-undo-narrow-heads.t
    test-unicode-inputs-t.py
    test-unified-test.t
    test-update-inactive-t.py
    test-update-issue1456.t
    test-update-merge-state-t.py
    test-update-reverse.t
    test-update-symlink-to-plain.t
    test-url.py
    test-username-newline.t
    test-visibility-reset.t
    test-walk.t
    test-walkrepo.py
    test-wireproto.py
    test-wireproto.t
    test-worker.t
    test-xdg.t
    test-zstdelta.py

    test-addremove-t.py
    test-amend-nextrebase.t
    test-audit-path.t
    test-backout.t
    test-bisect2.t
    test-blackbox.t
    test-bundle2-multiple-changegroups.t
    test-bundle-type.t
    test-commit-amend-reuse-rawfctx.t
    test-commitcloud-backup-all.t
    test-commitcloud-backup-lfs.t
    test-commitcloud-backup-remotenames-public.t
    test-commitcloud-backup-restore-obsolete.t
    test-commitcloud-backup-restore.t
    test-commitcloud-backup-rev.t
    test-commitcloud-backup-status.t
    test-commitcloud-lazypull-phab.t
    test-commitcloud-lazypull.t
    test-commitcloud-rename-workspace.t
    test-commitcloud-sync-migration.t
    test-commitcloud-sync-race.t
    test-commitcloud-sync-rb-deletion.t
    test-commitcloud-sync-rb-enabling2.t
    test-commitcloud-sync.t
    test-commitcloud-update.t
    test-commit-interactive.t
    test-commit.t
    test-copy-move-merge.t
    test-copytrace-heuristics.t
    test-debugsendunbundle.t
    test-double-merge.t
    test-encoding.t
    test-eol-add.t
    test-eol-patch.t
    test-eol.t
    test-fb-hgext-copytrace.t
    test-fb-hgext-crdump.t
    test-fb-hgext-debugdetectissues.t
    test-fb-hgext-dirsync-amend-t.py
    test-fb-hgext-dirsync.t
    test-fb-hgext-git-getmeta.t
    test-fb-hgext-merge-conflictinfo.t
    test-fb-hgext-mergedriver.t
    test-fb-hgext-pull-createmarkers.t
    test-fb-hgext-pushrebase-protection.t
    test-fb-hgext-pushvars-remotenames.t
    test-fb-hgext-remotefilelog-archive.t
    test-fb-hgext-remotefilelog-bad-configs.t
    test-fb-hgext-remotefilelog-bundle2-legacy.t
    test-fb-hgext-remotefilelog-bundle2.t
    test-fb-hgext-remotefilelog-bundles.t
    test-fb-hgext-remotefilelog-getpackv2.t
    test-fb-hgext-remotefilelog-local.t
    test-fb-hgext-remotefilelog-pull-noshallow.t
    test-fb-hgext-remotefilelog-push-pull-query-string.t
    test-fb-hgext-remotefilelog-ruststores-repack.t
    test-fb-hgext-remotefilelog-ruststores-rotatelog-size.t
    test-fb-hgext-remotefilelog-treemanifest-corrupt.t
    test-fb-hgext-remotefilelog-worker.t
    test-fb-hgext-reset-remotenames-t.py
    test-fb-hgext-snapshot.t
    test-fb-hgext-treemanifest-blame.t
    test-fb-hgext-treemanifest-comparetrees.t
    test-fb-hgext-treemanifest-disabled-t.py
    test-fb-hgext-treemanifest-infinitepush.t
    test-fb-hgext-treemanifest-peertopeer.t
    test-fb-hgext-treemanifest-pushrebase.t
    test-fb-hgext-treemanifest-pushrebase-treeonly.t
    test-fb-hgext-treemanifest-remotenames-out-of-sync.t
    test-fb-hgext-treemanifest-treeonly-copyamend.t
    test-fb-hgext-treemanifest-treeonly-fetching.t
    test-fb-hgext-tweakdefaults-remotenames.t
    test-gitlookup-infinitepush.t
    test-globalopts.t
    test-hgext-perfsuite.t
    test-hgext-stablerev.t
    test-hggit-bookmark-workflow.t
    test-hggit-git-workflow.t
    test-hggit-updatemeta.t
    test-histedit-arguments.t
    test-histedit-base.t
    test-histedit-commute.t
    test-histedit-mutation.t
    test-histedit-no-change.t
    test-histedit-outgoing.t
    test-important-remote-names-t.py
    test-import-bypass.t
    test-infinitepush-bundlestore.t
    test-infinitepush-delscratchbookmarks.t
    test-infinitepush-publicscratchbookmarks.t
    test-infinitepush-remotefilelog.t
    test-infinitepush-remotenames.t
    test-infinitepush-scratchbookmark-commands.t
    test-infinitepush-write.t
    test-init.t
    test-issue1502.t
    test-issue522.t
    test-issue586.t
    test-issue672.t
    test-journal-share-t.py
    test-journal.t
    test-lfs-checksum.t
    test-lock-badness.t
    test-log-wireproto-requests-getpack.t
    test-log-wireproto-requests.t
    test-merge1.t
    test-merge6.t
    test-merge8-t.py
    test-merge-criss-cross.t
    test-merge-remove.t
    test-merge-symlinks.t
    test-merge-types.t
    test-mutation-infinitepush.t
    test-mutation-pushrebase.t
    test-mutation.t
    test-narrow-heads.t
    test-pathconflicts-basic.t
    test-pathconflicts-merge.t
    test-pending.t
    test-perftweaks-remotenames.t
    test-pushvars-t.py
    test-rebase-bookmarks.t
    test-rebase-collapse.t
    test-rebase-conflicts.t
    test-rebase-dest.t
    test-rebase-detach.t
    test-rebase-flags.t
    test-rebase-inmemory-mergedriver.t
    test-rebase-inmemory-nochanges-t.py
    test-rebase-inmemory-noconflict.t
    test-rebase-inmemory.t
    test-rebase-interruptions.t
    test-rebase-newancestor.t
    test-rebase-removed.t
    test-rebase-rename.t
    test-remotefilelog-undesired-file-logging.t
    test-remotenames-basic.t
    test-remotenames-convert-t.py
    test-remotenames-fastheaddiscovery-hidden-commits.t
    test-remotenames-journal.t
    test-remotenames-namespaces-t.py
    test-remotenames-on-and-off-t.py
    test-remotenames-pull-rebase.t
    test-remotenames-push.t
    test-remotenames-pushto-pathandname.t
    test-remotenames-pushto.t
    test-remotenames-selective-pull-accessed-bookmarks.t
    test-remotenames-selective-pull.t
    test-remotenames-strip-t.py
    test-remotenames-transition.t
    test-rename-after-merge.t
    test-rename-dir-merge.t
    test-rename-merge1.t
    test-rename.t
    test-resolve.t
    test-revset-outgoing.t
    test-share.t
    test-sparse-clone.t
    test-sparse.t
    test-symlink-os-yes-fs-no.py
    test-symlink-placeholder.t
    test-symlinks.t
    test-unrelated-pull.t
    test-update-dest-t.py
    test-update-names.t
    test-up-local-change.t
    test-url-rev.t
    test-visibility-bundle.t
    test-visibility-cloudsync.t
    test-visibility.t

    test-rebase-abort.t
    test-rebase-brute-force.t
    test-rebase-check-restore-t.py
"""


def setup(testname, hgrcpath):
    # Disable mutation.record to maintain commit hashes.
    with open(hgrcpath, "a") as f:
        f.write("\n[mutation]\nrecord=False\n")
    # Disable mutation and re-enable obsstore on unsupported tests.
    if testname in mutationblacklist:
        with open(hgrcpath, "a") as f:
            f.write("\n[mutation]\nenabled=False\nproxy-obsstore=False\n")
    # Disable narrow-heads if incompatible.
    if testname in narrowheadsincompatiblelist:
        with open(hgrcpath, "a") as f:
            f.write("\n[experimental]\nnarrow-heads=False\n")
    # Enable segmented changelog if compatible.
    if testname in segmentedchangelogcompatiblelist:
        with open(hgrcpath, "a") as f:
            f.write("\n[format]\nuse-segmented-changelog=True\n")
