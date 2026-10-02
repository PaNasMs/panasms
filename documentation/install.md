# Install PaNasMs

Start with **Debian 13 / Raspberry Pi OS 13 (ARM64 or AMD64), or Ubuntu 24.04 LTS (AMD64)**, a working
internet connection and an existing Linux user with administrator (`sudo`) rights.
PaNasMs is an application installed on this OS, not an SD-card image. ARM64 is the
hardware-tested target; AMD64 packages are experimental.

Open a terminal on the NAS (or connect over SSH) and paste:

```sh
curl -fsSL https://panasms.github.io/updates/install.sh | sudo bash
```

Enter your Linux password if sudo asks. The installer checks compatibility and
free space, verifies the signed release catalog and package, installs dependencies
(including mdadm, filesystem tools, SMART, Samba and NFS), starts the panel and
prints its address. Sign in using your existing Linux administrator account.
It does not format disks, create an administrator or guess your fan wiring.
Hardware cooling remains unconfigured until you select the correct hardware.

The command downloads an administrator-level installer over HTTPS. You can inspect
it first instead of piping it directly to a shell:

```sh
curl -fsSLo panasms-install.sh https://panasms.github.io/updates/install.sh
less panasms-install.sh
sudo bash panasms-install.sh
```

## Stable and testing

The default is **stable**. If no stable release has been published, installation
stops with an explanation; it never silently selects testing. For explicitly
opting into development builds:

```sh
curl -fsSL https://panasms.github.io/updates/install.sh | sudo bash -s -- --channel testing
```

Use `--port 8080` to choose another port; the default remains 80. For encrypted
access with a locally generated certificate, add `--https` (for example,
`--https --port 443`). A local certificate is not automatically trusted by browsers;
install it in your clients' trust stores, or use a certificate issued for your NAS.
HTTP is intended only for a trusted local development network. Do not expose it
to the internet.

On an installed system, enable HTTPS without changing the current port:

```sh
sudo panasms-tls enable
# Or supply a certificate and its matching private key:
sudo panasms-tls enable /path/to/fullchain.pem /path/to/private-key.pem
```

The new address uses `https://` and the same port. Certificate replacement validates
the key pair and expiry, checks panel health, and restores the previous configuration
if activation fails. Certificate renewal is the administrator's responsibility.

## Existing installations and errors

For an existing NAS, use **Settings → System updates**. Re-running the installer
will refuse to replace the running system. The updater supports backups and
recovery; the fresh-install command is not an alternative upgrade path.

If port 80 is busy, rerun with a different port. If the catalog is expired, check
the NAS clock and wait for repository publication. Signature or checksum failure
stops installation. Repair a failed Debian package transaction before retrying.
The command requires `curl` and Python 3 on the base OS.

Installation is complete only after the panel health check succeeds. Packages and
configuration may remain if APT or startup fails; the installer reports failure
rather than claiming an automatic rollback of a fresh OS installation.

For removal, preview the plan with `sudo panasms-uninstall --plan`.

Ubuntu 24.04 AMD64 requires PaNasMs 0.2.13 or newer. A cloud image may have only SSH-key authentication: set a password for your existing sudo user with `sudo passwd "$USER"` before signing in to the panel. SSH password authentication can remain disabled. The installer waits up to 60 seconds for the HTTP listener after starting services.
