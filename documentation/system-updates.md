# System update lifecycle

PaNasMs publishes native ARM64 and AMD64 Debian packages. Linux distribution updates and hardware cooling are separate from the panel update transaction.

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

Core and active module services stop for a consistent backup. Previous core packages are captured with dpkg-repack; PaNasMs configuration and databases are saved. User data, RAID, mounts, Linux accounts, network connections and independent cooling are not changed by rollback. The worker installs with APT, restarts services, checks HTTP/UI assets and SQLite integrity, and verifies the installed package version. Failure after mutation restores previous packages and saved data. A boot recovery unit restores interrupted installations before core startup. If recovery itself fails, the state remains actionable and further mutations are blocked until recovery.

Manual rollback restores PaNasMs settings/database state to the backup point; later settings changes are lost. It is refused if modules have changed since the snapshot or the snapshot does not correspond to the current version. This is not an atomic rollback of the entire operating system. Newly installed distribution dependencies may remain. No automatic reboot occurs.

System update progress appears in Tasks and the application bar. Available releases and outcomes appear in notifications. Logs are available in the system journal for `panasms-update.service`; the history remains available after the web interface restarts.

## Removal

Package removal refuses to interrupt an active transaction. Removal disables update scheduling and recovery units. Purge removes the updater's own journal, downloads and rollback copies; user storage and the independent cooling package are retained.
