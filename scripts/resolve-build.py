#!/usr/bin/env python3
import datetime
import json
import os
from pathlib import Path
import re
import subprocess
import urllib.parse
import urllib.request


def resolve(repository, ref):
    url = f"https://api.github.com/repos/PaNasMs/{repository}/commits/{urllib.parse.quote(ref, safe='')}"
    request = urllib.request.Request(url, headers={
        "Authorization": "Bearer " + os.environ["GH_TOKEN"],
        "Accept": "application/vnd.github+json",
        "X-GitHub-Api-Version": "2022-11-28",
    })
    with urllib.request.urlopen(request, timeout=60) as response:
        commit = json.load(response)
    if not re.fullmatch(r"[0-9a-f]{40}", commit["sha"]):
        raise ValueError("GitHub did not return a full commit SHA")
    return {"repository": f"PaNasMs/{repository}", "commit": commit["sha"],
            "requestedRef": ref, "committedAt": commit["commit"]["committer"]["date"]}


def main():
    tag = os.environ.get("VERSION_TAG", "")
    lock = json.loads(Path("release-lock.json").read_text()) if tag else None
    if tag and (not re.fullmatch(r"v[0-9]+\.[0-9]+\.[0-9]+", tag) or lock["version"] != tag[1:]):
        raise ValueError("Version tag must match release-lock.json")
    if lock and any(not re.fullmatch(r"[0-9a-f]{40}", lock["sources"][name]) for name in ("backend", "frontend", "files", "terminal")):
        raise ValueError("Release sources must be pinned to full commit SHAs")
    sources = {name: resolve(name, lock["sources"][name] if lock else os.environ.get(name.upper() + "_REF") or "main")
               for name in ("backend", "frontend")}
    for name in ("files", "terminal"):
        sources[name] = resolve("module-" + name, lock["sources"][name] if lock else "main")
        sources[name]["role"] = "test-dependency"
    sources["build"] = {
        "repository": "PaNasMs/panasms",
        "commit": subprocess.check_output(["git", "rev-parse", "HEAD"], text=True).strip(),
    }
    request = urllib.request.Request(f"https://api.github.com/repos/{os.environ['GITHUB_REPOSITORY']}/actions/runs/{os.environ['GITHUB_RUN_ID']}", headers={"Authorization": "Bearer " + os.environ["GH_TOKEN"]})
    with urllib.request.urlopen(request, timeout=30) as response:
        created = json.load(response)["created_at"]
    manifest = {
        "channel": "stable" if tag else "testing",
        "releaseVersion": tag.removeprefix("v"),
        "schemaVersion": 1,
        "createdAt": created,
        "sources": sources,
    }
    with Path(os.environ["GITHUB_OUTPUT"]).open("a") as output:
        for name in sources:
            output.write(f"{name}={sources[name]['commit']}\n")
        output.write("manifest=" + json.dumps(manifest, separators=(",", ":")) + "\n")
    print(json.dumps(manifest, indent=2))


if __name__ == "__main__":
    main()
