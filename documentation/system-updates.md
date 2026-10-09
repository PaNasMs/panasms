# System update lifecycle

PaNasMs publishes native ARM64 and AMD64 Debian packages. Linux distribution updates are separate from the panel update transaction. ARM64 releases also carry the optional `panasms-cooling` package, which the updater upgrades together with the core only where it is already installed; it never installs cooling.

## Channels and releases

Pushes to `main` in panasms, backend or frontend produce testing packages with unique versions such as `0.2.6~dev.20260921220000.RUN.ATTEMPT`. Feature branches and pull requests are tested without publication. Bump the backend VERSION and frontend package version together when starting the next release cycle; a testing prerelease sorts below its matching stable version.

For stable publication, run `python3 scripts/prepare-release.py 0.2.6` with GitHub CLI available. Review and commit `release-lock.json`, then create and push tag `v0.2.6` on that commit in PaNasMs/panasms. Both components must declare this version. The lock pins backend, frontend and module test dependencies by full SHA. The shared build-tool commit is the tagged commit itself. No stable release is created without an explicit version tag.

PaNasMs/updates imports successful builds approximately every 15 minutes. GitHub can delay schedules. Both architectures must complete and have identical component provenance. Publication is serialized; an older build cannot replace a newer version. Releases are immutable, signed Pages catalogs retain two recent releases per channel, and old packages remain in Releases. Only updates holds the dedicated signing secret. Public fingerprint: `495D91EE558DA6CA516EA434BC48F33EC04DFC99`.

`backend/packaging/update-policy.json` is reviewed with migrations. Set `rollbackCompatible` to false for changes that cannot safely restore the previous database/configuration snapshot; set `requiresReboot` to true for a release requiring manual reboot maintenance. Such versions cannot use the automatic installation path. Do not claim rollback compatibility without a migration review.

## NAS settings

Settings → System updates provides current/candidate versions, stable/testing selection, notify/download/automatic policies, a daily local-time installation window, manual checks, download, installation, rollback, progress and history. Default: stable, notify only; checks once per day. Conflicting jobs postpone automatic installation. A failed version is not retried automatically.

The updater verifies the detached OpenPGP catalog signature against the packaged key, expiry, catalog age, package checksums and identities. It downloads verified release assets and gives local packages to APT for dependency resolution. It does not add a global APT source automatically, so other unattended-upgrade tools cannot bypass its transaction checks. The signed APT repository is also available for administrators who explicitly configure it.

## Installation and recovery

State lives in `/var/lib/panasms-updates`; preferences in `/etc/panasms/updates.json`. A separate systemd worker uses a saved copy of its code, surviving core/agent replacement. Durable journal writes use fsync and atomic rename. The worker verifies OS/architecture, space, module compatibility, pending network/HTTP changes and active operations. Debian dependency replacements or removals require separate system maintenance. Downloads and dependency resolution finish before services stop.

Open terminal sessions do not block panel updates or rollback. After downloads and initial checks, the updater stops the terminal service and its entire process group, ending all terminal commands. It then obtains the exclusive maintenance lock; other active work still blocks installation. The terminal service returns after a successful update or rollback, but closed sessions and commands are not resumed. A failure before package changes also restarts previously running services.

Core and active module services stop for a consistent backup. Cooling keeps running; only its own package scripts restart it during the package change. Previous versions of every installed PaNasMs package, including cooling, are captured with dpkg-repack; PaNasMs configuration and databases are saved. User data, RAID, mounts, Linux accounts, network connections and the cooling configuration in `/etc/panasms-cooling` are not changed by rollback. The worker installs with APT, restarts services, checks HTTP/UI assets and SQLite integrity, verifies that every updated package has the release version, and requires a previously active cooling service to be active again. Failure after mutation restores previous packages and saved data. A boot recovery unit restores interrupted installations before core startup. If recovery itself fails, the state remains actionable and further mutations are blocked until recovery.

Manual rollback restores PaNasMs settings/database state to the backup point; later settings changes are lost. It is refused if modules have changed since the snapshot or the snapshot does not correspond to the current version. This is not an atomic rollback of the entire operating system. Newly installed distribution dependencies may remain. No automatic reboot occurs.

After an interrupted installation, boot recovery requeues the saved panel and
module services after restoring the package and databases. These starts are
nonblocking because the panel is ordered after the recovery unit. After boot,
verify that the panel is reachable and check the update history; a restored
package alone does not prove that every service is healthy. A persistent external
startup failure must be corrected before recovery can finish. The updater retains
the failed transaction and backup instead of claiming a successful update.

System update progress appears in Tasks and the application bar. Available releases and outcomes appear in notifications. Logs are available in the system journal for `panasms-update.service`; the history remains available after the web interface restarts.

## Removal

Package removal refuses to interrupt an active transaction. Removal disables update scheduling and recovery units. Purge removes the updater's own journal, downloads and rollback copies; user storage and the independent cooling package are retained.

## Exclusive maintenance (0.2.10 and later)

The core API, agent jobs and maintenance-aware module operations hold shared locks
on `/run/lock/panasms-maintenance.lock`. The independent update worker holds the
exclusive lock from the final preflight through backup, installation and health
verification/rollback. New requests cannot enter while it owns the lock. Passive
core event subscriptions and the health endpoint remain exempt.

Running modules must advertise `maintenanceVersion: 1` and report no active work.
Older modules must be updated or explicitly stopped first; an idle snapshot alone
is not sufficient. Cloud Sync background synchronization and Containers background
operations participate for their entire execution. An orderly agent stop cancels
queued work and waits for active mutations, with a 30-minute systemd stop limit.

Manual package replacement must use `sudo panasms-maintenance apt-get install
/path/to/package.deb`; direct upgrades are rejected by the package scripts. This
wrapper is a maintenance guard, not a backup or rollback engine. Prefer the panel
updater. Do not set internal transaction/maintenance environment variables manually.

The first migration from an older version needs a controlled maintenance window:
finish tasks, close terminals, stop module services and back up state before
bootstrapping the new guard. Older running code does not acquire the new lock.
This compatibility limitation cannot be fixed retroactively by the new package.
