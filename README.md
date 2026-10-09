# Pavlo's NAS Management System (PaNasMs)

PaNasMs is a web panel for a home NAS that you build yourself. It installs as Debian
packages on an existing Linux system and lets you manage disks, RAID, shared folders,
users, network, files and Docker containers from a browser on a computer or phone.
The interface is available in English, Russian and Ukrainian.

The first stable release, 0.2.15, came out on October 8, 2026. The website at
[panasms.github.io](https://panasms.github.io/) shows every section with real
screenshots and describes the Raspberry Pi 5 build the project runs on.

![PaNasMs desktop with widgets, shortcuts and background tasks](https://panasms.github.io/assets/screenshots/home-desktop-light.png)

## Install

Run this on the NAS, not on your everyday computer:

```sh
curl -fsSL https://panasms.github.io/updates/install.sh | sudo bash
```

The installer checks the system, verifies the signed package, installs the dependencies
(mdadm, Samba, NFS, SMART tools and others) and prints the panel address. Sign in with
your existing Linux administrator account. It does not format disks or create users.
The [installation guide](https://panasms.github.io/docs/setup/install/) covers ports,
HTTPS, updates and removal.

| Operating system | Architecture | How it was tested |
| --- | --- | --- |
| Raspberry Pi OS 13 (64-bit) | ARM64 | Raspberry Pi 5 with a Radxa Penta SATA HAT |
| Debian 13 | ARM64, AMD64 | AMD64 in a Proxmox virtual machine |
| Ubuntu 24.04 LTS | AMD64 | Proxmox virtual machine |
| Armbian 26.8 (Debian 13) | ARM64 | Raspberry Pi 5 with a Radxa Penta SATA HAT |

Other distributions and versions are not supported by the current installer. A test in
a virtual machine does not cover every x64 computer, and hardware features such as fan
control need a compatible board.

## What it does

- Disks, mdadm RAID, partitions, file systems, LUKS encryption with optional unlocking
  at startup, SMART checks, disk sleep and fan control on supported hardware.
- SMB and NFS shared folders with per-user and per-group access, and mounts of remote
  network folders.
- Linux users and groups, SSH keys, sessions, home folder moves, and sign-in with Google
  or GitHub in addition to the Linux password.
- Ethernet and Wi-Fi, connection sharing, a fallback Wi-Fi hotspot, and confirmation with
  rollback for network changes.
- Signed system updates with stable and testing channels, a backup before installation
  and recovery after an interrupted update.
- CPU, memory, disk and network history, and notifications by email, Telegram and
  browser push.

Optional modules are installed from the panel's Modules page and have their own versions:

| Module | What it adds |
| --- | --- |
| [Files](https://github.com/PaNasMs/module-files) | File manager for local storage, network folders, Google Drive and Dropbox |
| [Terminal](https://github.com/PaNasMs/module-terminal) | Shell sessions in the browser as the signed-in Linux user |
| [Cloud Sync](https://github.com/PaNasMs/module-cloud-sync) | Folder synchronization with Google Drive and Dropbox |
| [Containers and applications](https://github.com/PaNasMs/module-containers) | Docker containers, images, networks and volumes (preview) |

## Repositories

This repository holds the project overview, license, public documentation and shared
tools. Each component lives in its own Git repository.

| Repository | Contents |
| --- | --- |
| [backend](https://github.com/PaNasMs/backend) | Go API core, privileged agent, Python system adapters and Debian packaging |
| [frontend](https://github.com/PaNasMs/frontend) | React interface, desktop, system pages, settings and module host |
| [updates](https://github.com/PaNasMs/updates) | Signed stable and testing channels and the installer |
| [module-sdk](https://github.com/PaNasMs/module-sdk) | Go module server and TypeScript contracts for module authors |
| [module-registry](https://github.com/PaNasMs/module-registry) | Signed module catalog and package publication |
| [panasms.github.io](https://github.com/PaNasMs/panasms.github.io) | Project website and setup guides |
| [panasms-oauth-gateway](https://github.com/PaNasMs/panasms-oauth-gateway) | Shared OAuth redirect page for linking cloud accounts |

## Development

Scripts in this workspace expect the components as sibling directories:

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
git clone git@github.com:PaNasMs/module-containers.git modules/containers
```

Each component README lists its build and test commands. CI builds native ARM64 and
AMD64 Debian packages for every change to this repository, the backend or the frontend,
and keeps them as workflow artifacts for 30 days. Successful builds of `main` go to the
signed testing channel. A version tag in this repository produces a stable release.
Modules build their own ARM64 and AMD64 packages, and the registry imports tagged
module releases into the [module catalog](https://panasms.github.io/module-registry/).

The website and the update publisher can be cloned into `website/` and `updates/` when
you work on them. Pushing to the website repository publishes the site and does not
build NAS software.

Write public documentation in English and link to other repositories with full GitHub
URLs. Plans, research notes, machine records and credentials stay out of the public
repositories.

## Documentation

- [Installation](documentation/install.md) and [system update lifecycle](documentation/system-updates.md)
- [Automated builds](documentation/builds.md)
- [API contracts, persistence and recovery](documentation/core-lifecycle.md)
- [External connections](documentation/external-connections.md) and setup guides for
  [Google](https://panasms.github.io/docs/setup/google/),
  [GitHub](https://panasms.github.io/docs/setup/github/) and
  [Dropbox](https://panasms.github.io/docs/setup/dropbox/)
- [Interface design standard](docs/ui-design-guidelines.md), required for interface
  work in the core and in modules by the [project instructions](AGENTS.md). It sets an
  accessibility target. It does not certify that every screen meets it.

## License

Original PaNasMs code uses the [PolyForm Noncommercial 1.0.0](LICENSE) license. You
may use, change and share it for noncommercial purposes. This makes PaNasMs
source-available, not open source in the OSI sense. [NOTICE](NOTICE) explains the scope
and lists third-party components, which keep their own licenses.
