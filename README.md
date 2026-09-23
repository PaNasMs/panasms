# Pavlo's NAS Management System (PaNasMs)

PaNasMs is a Linux NAS management panel. The current 0.2.x prototype runs on
Raspberry Pi OS ARM64 and manages existing Linux users, storage and network
services. The system identifier used in packages, paths and services is `panasms`.

[Explore PaNasMs](https://panasms.github.io/) — a visual introduction to the
features, with real English-interface screenshots and English, Russian and
Ukrainian descriptions.

## Repositories

This repository contains the workspace overview, licensing and shared tools.
Components are independent Git repositories, not submodules.

[Interface design standard](docs/ui-design-guidelines.md) ·
[Google sign-in setup, step by step](documentation/google-sign-in-setup.md) ·
[Automated builds](documentation/builds.md) ·
[Build runs and downloads](https://github.com/PaNasMs/panasms/actions/workflows/build.yml)

| Repository | Responsibility |
| --- | --- |
| [Project website](https://github.com/PaNasMs/panasms.github.io) | Multilingual feature presentation, screenshots and GitHub Pages publishing |
| [Backend](https://github.com/PaNasMs/backend) | Go API core, privileged agent, Python system adapters and Debian packaging |
| [Frontend](https://github.com/PaNasMs/frontend) | React SPA, desktop, system pages, settings and module host |
| [System updates](https://github.com/PaNasMs/updates) | Signed stable/testing channels and verified package publication |
| [Module SDK](https://github.com/PaNasMs/module-sdk) | Shared Go module server and TypeScript host contracts |
| [Module registry](https://github.com/PaNasMs/module-registry) | Signed catalog, package signing and publication |
| [Files](https://github.com/PaNasMs/module-files) | Installable file manager |
| [Terminal](https://github.com/PaNasMs/module-terminal) | Installable system-user terminal |
| [Cloud Sync](https://github.com/PaNasMs/module-cloud-sync) | Prototype Google Drive and Dropbox synchronization |

Internal plans, research notes and deployment records are maintained locally and
are not published. There is no public `docs` repository.

## Current capabilities

- Linux user/group management, PAM login, profiles, SSH keys, permissions and home-directory relocation.
- Disks, mdadm RAID, partitions, filesystems, mounts, SMART schedules, HDD standby and hardware-dependent cooling.
- Local SMB/NFS shared folders, external network mounts, system services, logs and metric history.
- Signed stable/testing updates with installation policies, progress, backups and recovery.
- Ethernet and Wi-Fi management, access points and connection sharing with rollback confirmation.
- Per-user desktop layout, wallpaper, language and application shortcuts; tasks and notifications.
- Signed module installation from the online catalog or a local `.panasms` archive.

Core and agent run as separate processes with different privileges. Files,
Terminal and Cloud Sync are separately versioned modules. English is the default
and fallback UI language; Russian and Ukrainian are also available.

## Workspace setup

Use the following layout for scripts that refer to sibling repositories:

```sh
git clone git@github.com:PaNasMs/panasms.git
cd panasms
git clone git@github.com:PaNasMs/backend.git backend
git clone git@github.com:PaNasMs/frontend.git frontend
git clone git@github.com:PaNasMs/module-sdk.git module-sdk
git clone git@github.com:PaNasMs/module-registry.git module-registry
git clone git@github.com:PaNasMs/module-files.git modules/files
git clone git@github.com:PaNasMs/module-terminal.git modules/terminal
git clone git@github.com:PaNasMs/module-cloud-sync.git modules/cloud-sync
```

Each component README describes its build and checks. Core CI builds native
ARM64 and AMD64 Debian packages after changes to the workspace, backend or
frontend. Packages, checksums and exact source manifests are retained as workflow
artifacts for 30 days. See [Automated builds](documentation/builds.md) for downloads,
compatibility and the distinction between CI artifacts and stable releases.
Successful main-branch builds are published to the signed testing channel; stable
releases require a version tag. See the [update lifecycle](documentation/system-updates.md)
for publication rules and NAS installation policies.
Modules have ARM64 build workflows and
versioned releases imported by the registry. The official catalog is available at
[panasms.github.io/module-registry](https://panasms.github.io/module-registry/).

The website and update publisher are independent of runtime development. To work
on them locally, optionally clone `git@github.com:PaNasMs/panasms.github.io.git`
into `website/` and `git@github.com:PaNasMs/updates.git` into `updates/`. Website
pushes publish the presentation without building or installing the NAS software.

Local credentials, machine snapshots, session notes, hardware research, CAD,
build outputs and temporary files are excluded from this repository. The local
workspace may also contain historical CasaOS tools; they are not part of the
PaNasMs runtime unless explicitly incorporated into a component.

## Documentation and license

Maintain public project documentation in English. Link across repositories using
GitHub URLs; relative links must resolve inside the repository that contains them.
Do not publish internal documentation or machine-specific records.

The [interface design standard](docs/ui-design-guidelines.md) is the single public
design baseline for the core and modules. It covers layout, visual tokens, tabs,
cards, forms, dialogs, notifications, background work and acceptance checks.
[Project instructions](AGENTS.md) require it for all interface work. The standard
defines an accessibility target, not a claim that every existing screen has passed
acceptance.

Original PaNasMs code uses [PolyForm Noncommercial 1.0.0](LICENSE); see
[NOTICE](NOTICE) for scope and third-party exceptions. This is a source-available
project, not an OSI-approved open-source license. Third-party components retain
their own licenses.

System update publication and NAS recovery are documented in the
[system update lifecycle](documentation/system-updates.md).

Core developers: see [API contracts, persistence and recovery](documentation/core-lifecycle.md).

## External connections

Google account linking and optional panel sign-in use NAS-specific OAuth credentials. See the [architecture, setup and Cloud Sync handoff](https://github.com/PaNasMs/panasms/blob/main/documentation/external-connections.md).
