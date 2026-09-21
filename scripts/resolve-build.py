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
    sources = {name: resolve(name, os.environ.get(name.upper() + "_REF") or "main")
               for name in ("backend", "frontend")}
    sources["build"] = {
        "repository": "PaNasMs/panasms",
        "commit": subprocess.check_output(["git", "rev-parse", "HEAD"], text=True).strip(),
    }
    manifest = {
        "schemaVersion": 1,
        "createdAt": datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "sources": sources,
    }
    with Path(os.environ["GITHUB_OUTPUT"]).open("a") as output:
        for name in ("backend", "frontend", "build"):
            output.write(f"{name}={sources[name]['commit']}\n")
        output.write("manifest=" + json.dumps(manifest, separators=(",", ":")) + "\n")
    print(json.dumps(manifest, indent=2))


if __name__ == "__main__":
    main()
