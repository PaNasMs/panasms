#!/usr/bin/env python3
import argparse
import hashlib
import json
from pathlib import Path
import subprocess
import tempfile
import zipfile

parser = argparse.ArgumentParser(
    description="Build signed OstojaOS module archives from prepared dist payloads"
)
parser.add_argument("--key", required=True, type=Path)
parser.add_argument("--root", default=Path(__file__).resolve().parent, type=Path)
parser.add_argument("--output", type=Path)
parser.add_argument('--module', action='append', help='Module directory ID; repeat to include dependencies')
parser.add_argument('--bundle-root', help='Write one bundle with the selected root and supplied dependencies')
args = parser.parse_args()
output = args.output or args.root / "dist"
output.mkdir(parents=True, exist_ok=True)
modules = {}
for mid in args.module or [p.parent.name for p in args.root.glob("*/manifest.json")]:
    folder = args.root / mid
    m = json.loads((folder / "manifest.json").read_text())
    payload = {
        p.relative_to(folder / "dist").as_posix(): p.read_bytes()
        for p in (folder / "dist").rglob("*")
        if p.is_file()
    }
    for filename in ("LICENSE", "NOTICE"):
        payload[filename] = (folder / filename).read_bytes()
    assert "ui/index.js" in payload, "Build module UI first"
    assert not m.get("service") or m["service"] in payload, "Build native server first"
    m["files"] = {name: hashlib.sha256(raw).hexdigest() for name, raw in payload.items()}
    manifest = json.dumps(m, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode()
    with tempfile.TemporaryDirectory() as tmp:
        source, signature = Path(tmp) / "manifest", Path(tmp) / "signature"
        source.write_bytes(manifest)
        subprocess.run(
            [
                "openssl",
                "pkeyutl",
                "-sign",
                "-inkey",
                str(args.key),
                "-rawin",
                "-in",
                str(source),
                "-out",
                str(signature),
            ],
            check=True,
        )
        payload["manifest.json"] = manifest
        payload["signature"] = signature.read_bytes()
    modules[mid] = payload
for mid in ([args.bundle_root] if args.bundle_root else modules):
    m = json.loads(modules[mid]["manifest.json"])
    dest = output / (mid + "-" + m["version"] + "-" + m["architecture"] + ".ostojaos")
    with zipfile.ZipFile(dest, "w", zipfile.ZIP_DEFLATED) as archive:
        archive.writestr("bundle.json", json.dumps({"root": mid}))
        for included in (modules if args.bundle_root else [mid]):
            for name, raw in modules[included].items():
                archive.writestr("modules/" + included + "/" + name, raw)
    print(dest)
