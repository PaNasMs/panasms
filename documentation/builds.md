# Automated PaNasMs builds

The first installation/update pipeline builds the current PaNasMs management
system as Debian packages. It does not produce a bootable SD-card image or
replace the underlying Linux distribution. Target base: Debian 13 (Trixie),
including the ARM64 Raspberry Pi OS based on it. Hardware-dependent functionality
still depends on the host. An AMD64 build passing CI does not certify every PC.

## Triggers and downloads

- Pushes to `main` and pull requests in `panasms`, `backend` and `frontend` run
  **Build PaNasMs**. Component repositories call the same reusable workflow,
  pinned to a reviewed commit in `panasms`; they need no cross-repository write
  token or stored NAS credentials.
- The triggering component is built at that exact commit (the merge commit for
  a pull request), paired with the other component's resolved `main`. Both target
  architectures use the same resolved source commits.
- Manual runs in `panasms` can choose backend/frontend branches, tags or commits.
- Open **Actions → Build PaNasMs → successful run → Artifacts** in the repository
  that triggered the run. Root runs are listed
  [here](https://github.com/PaNasMs/panasms/actions/workflows/build.yml).
- Download `panasms-debian13-arm64-<run>-<attempt>` for Raspberry Pi or the `amd64`
  equivalent for x86-64. Artifacts expire after 30 days and are not stable releases.

Each archive contains the core `.deb`, `build-manifest.json` and `SHA256SUMS`.
The ARM64 archive also contains the optional, hardware-specific cooling `.deb`.
The core package includes the SPA, Go services, PAM integration, Python adapters,
service units and administration tools. Modules remain independently versioned
and distributed through the module registry.

## Versions and verification

The core base version is `backend/VERSION`, and it must match frontend
`package.json`. CI appends `~ci.<UTC timestamp>.<run ID>.<attempt>`, so repeated
builds are distinguishable and sort **below** the corresponding stable version.
The optional cooling package has its own base version. CI versions are not
published to an APT repository and will not automatically replace installed
stable packages.

The manifest records exact workspace/backend/frontend commits, requested refs,
architecture, build run, compiler/runtime versions, Debian container digest and
package SHA-256 hashes. Inspect it before using an artifact. After extracting:

```sh
sha256sum --check SHA256SUMS
dpkg-deb --info ./panasms-prototype_<version>_<architecture>.deb
```

Checksums detect damaged or mismatched files; these artifacts are **not signed**
update manifests. Do not treat them as a trusted automatic-update channel.
The Actions upload additionally provides GitHub's artifact integrity check.

## Build and test boundaries

The native ARM64 and AMD64 runners use a pinned Debian 13 container image.
Actions are pinned by commit; Go is pinned to a patch version, npm uses the
checked-in lockfile, and Go uses its module sums. Node follows the Node 24 line.
Debian build dependencies receive the distribution's current updates. This
captures source provenance but is not a claim of bit-for-bit reproducibility.

Before publishing artifacts, each job runs Go/PAM tests, Go vet, race tests,
Python unit tests, frontend unit tests, TypeScript checks and a production bundle.
Package validation checks Debian metadata, all three Go ELF architectures,
dynamic library resolution, required runtime files, shell-hook syntax, Python
syntax and artifact checksums. APT also simulates installation of every built
package with an empty installed-package status database and recommendations disabled,
checking that core dependencies can be resolved from Debian repositories. ARM64 also
checks core and cooling together with the official Raspberry Pi repository and a
checksum-pinned archive keyring; cooling requires its `raspi-utils` package. A failing job does not upload its packages.

CI does not install packages on a real NAS, run destructive storage/network
integration tests, or validate a physical fan. The existing browser smoke script
is not part of this pipeline; it requires a separate live harness and an updated
scenario. A green build is not hardware or full UI acceptance.

Current backend file-operation tests and frontend translation tests also consume
the Files and Terminal sources. CI resolves and checks out those repositories at
exact commits, recorded as test dependencies in the manifest, and installs Pillow
for thumbnail tests. These module sources are not bundled in the core package.

The `panasms-cooling` package is optional and specific to the verified GPIO27
hardware; do not install it on arbitrary machines. Experimental PWM work is kept
on a separate backend branch and is not included in `main` builds.

## Maintainer workflow

The implementation lives in
[build.yml](../.github/workflows/build.yml),
[resolve-build.py](../scripts/resolve-build.py) and
[build-artifacts.py](../scripts/build-artifacts.py).
Backend and frontend callers pin both the reusable workflow and its `build_ref`
to the same workspace commit. When changing the shared pipeline, test its root
run, then update both caller pins. This prevents a moving build script from being
combined with a different workflow definition.

For local package builds, follow the backend and frontend READMEs. Default
versions are unchanged unless the CI version environment variables are supplied.
Local build orchestration can use the same artifact script with a matching source
manifest and GitHub run metadata; the workflow is the supported CI entry point.

## Next installation and update steps

Future work needs a supported-host installer, release/channel policy, signed
update manifests and durable package hosting, compatibility checks, backups,
state migrations, interruption recovery and tested rollback. A bootable image
would be a separate deliverable. No automatic deployment, reboot, stable release
or update-feed publication is enabled by this initial build pipeline.

GitHub references: [native hosted runners](https://docs.github.com/en/actions/reference/runners/github-hosted-runners),
[reusable workflows](https://docs.github.com/en/actions/how-tos/reuse-automations/reuse-workflows)
and [workflow artifacts](https://docs.github.com/en/actions/how-tos/writing-workflows/choosing-what-your-workflow-does/storing-and-sharing-data-from-a-workflow).

## Installing dependencies

Install a downloaded core package using `sudo apt update` followed by
`sudo apt install ./panasms-prototype_<version>_<architecture>.deb`.
APT downloads its mandatory runtime dependencies, including mdadm, filesystem tools,
NetworkManager/Wi-Fi support and Samba/NFS. Do not use `dpkg -i` as a dependency
installer. This requires accessible distribution repositories; the artifact is not
an offline bundle. Installing the optional cooling package is a separate hardware decision.
