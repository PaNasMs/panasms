#!/usr/bin/env python3
import argparse
import hashlib
import json
import os
from pathlib import Path
import re
import shutil
import struct
import subprocess
import tempfile


def output(*args):
    return subprocess.check_output(args, text=True).strip()


def ci_version(base, created, run, attempt):
    if not re.fullmatch(r"\d+\.\d+\.\d+", base):
        raise ValueError("Expected a three-component stable base version")
    if not run.isdigit() or not attempt.isdigit():
        raise ValueError("Run ID and attempt must be numeric")
    stamp = re.sub(r"[-:TZ]", "", created)
    if not re.fullmatch(r"\d{14}", stamp):
        raise ValueError("Expected an ISO UTC build timestamp")
    return f"{base}~ci.{stamp}.{run}.{attempt}"


def verify_elf(path, arch):
    with path.open("rb") as source:
        header = source.read(20)
    if (len(header) != 20 or header[:6] != b"\x7fELF\x02\x01" or
            struct.unpack("<H", header[18:20])[0] != {"arm64": 183, "amd64": 62}[arch]):
        raise ValueError(f"Wrong binary architecture: {path.name}")
    if "not found" in output("ldd", str(path)):
        raise ValueError(f"Unresolved runtime libraries: {path.name}")


def verify_package(package, name, version, arch):
    actual = output("dpkg-deb", "-f", str(package), "Package", "Version", "Architecture")
    expected = f"Package: {name}\nVersion: {version}\nArchitecture: {arch}"
    if actual != expected:
        raise ValueError(f"Unexpected package metadata: {actual}")
    with tempfile.TemporaryDirectory() as folder:
        root = Path(folder)
        subprocess.run(["dpkg-deb", "-R", str(package), str(root)], check=True)
        for hook in (root / "DEBIAN").iterdir():
            if hook.name in ("preinst", "postinst", "prerm", "postrm"):
                subprocess.run(["sh", "-n", str(hook)], check=True)
        if name == "panasms-prototype":
            for binary in ("panasms-core", "panasms-agent", "panasms-password"):
                verify_elf(root / "usr/lib/panasms" / binary, arch)
            for relative in ("usr/share/panasms/ui/index.html", "etc/pam.d/panasms",
                             "usr/lib/systemd/system/panasms-core.service",
                             "usr/lib/systemd/system/panasms-agent.service",
                             "etc/panasms/module-keys/panasms-ci.pem",
                             "usr/share/doc/panasms-prototype/LICENSE"):
                if not (root / relative).is_file():
                    raise ValueError(f"Missing package file: {relative}")
        for source in root.rglob("*.py"):
            compile(source.read_bytes(), str(source), "exec")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--backend", type=Path, required=True)
    parser.add_argument("--frontend", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    backend, frontend, destination = args.backend.resolve(), args.frontend.resolve(), args.output.resolve()
    metadata = json.loads(os.environ["SOURCE_MANIFEST"])
    for name, path in (("backend", backend), ("frontend", frontend),
                       ("build", Path(__file__).resolve().parents[1])):
        if output("git", "-C", str(path), "rev-parse", "HEAD") != metadata["sources"][name]["commit"]:
            raise ValueError(f"Checkout does not match source manifest: {name}")
    arch = output("dpkg", "--print-architecture")
    if arch not in ("arm64", "amd64"):
        raise ValueError("Supported build architectures: arm64, amd64")
    base = (backend / "VERSION").read_text().strip()
    if json.loads((frontend / "package.json").read_text())["version"] != base:
        raise ValueError("Backend and frontend base versions differ")
    version = ci_version(base, metadata["createdAt"], os.environ["GITHUB_RUN_ID"],
                         os.environ["GITHUB_RUN_ATTEMPT"])
    environment = dict(os.environ, PANASMS_PACKAGE_VERSION=version)
    subprocess.run(["sh", str(backend / "scripts/build-deb.sh"), str(frontend / "dist")],
                   check=True, env=environment)
    destination.mkdir(parents=True, exist_ok=True)
    if any(destination.iterdir()):
        raise ValueError("Artifact output directory must be empty")
    packages = [(backend / f"dist/panasms-prototype_{version}_{arch}.deb",
                 "panasms-prototype", version, arch)]
    if arch == "arm64":
        cooling_version = ci_version("0.2.0", metadata["createdAt"], os.environ["GITHUB_RUN_ID"],
                                     os.environ["GITHUB_RUN_ATTEMPT"])
        subprocess.run(["sh", str(backend / "scripts/build-cooling-deb.sh")], check=True,
                       env=dict(environment, PANASMS_COOLING_VERSION=cooling_version))
        packages.append((backend / f"dist/panasms-cooling_{cooling_version}_all.deb",
                         "panasms-cooling", cooling_version, "all"))
    for package, name, package_version, package_arch in packages:
        verify_package(package, name, package_version, package_arch)
        shutil.copy2(package, destination)
    metadata.update({
        "product": "PaNasMs", "channel": "ci", "version": version, "architecture": arch,
        "target": "Debian 13 / Raspberry Pi OS based on Debian 13",
        "run": f"https://github.com/{os.environ['GITHUB_REPOSITORY']}/actions/runs/{os.environ['GITHUB_RUN_ID']}",
        "attempt": int(os.environ["GITHUB_RUN_ATTEMPT"]),
        "toolchain": {"go": output("go", "version"), "node": output("node", "--version"),
                      "python": output("python3", "--version"),
                      "container": os.environ["BUILD_CONTAINER"]},
        "packages": [{"file": p.name, "sha256": hashlib.sha256(p.read_bytes()).hexdigest()}
                     for p in sorted(destination.glob("*.deb"))],
        "signed": False,
    })
    (destination / "build-manifest.json").write_text(json.dumps(metadata, indent=2) + "\n")
    checksums = "".join(f"{hashlib.sha256(p.read_bytes()).hexdigest()}  {p.name}\n"
                        for p in sorted(destination.iterdir()))
    (destination / "SHA256SUMS").write_text(checksums)
    subprocess.run(["sha256sum", "--check", "SHA256SUMS"], cwd=destination, check=True)
    print(json.dumps(metadata, indent=2))


if __name__ == "__main__":
    main()
