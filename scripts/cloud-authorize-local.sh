#!/bin/sh
set -eu
case "${1:-}" in drive|dropbox) ;; *) echo 'Usage: cloud-authorize-local.sh drive|dropbox' >&2; exit 2;; esac
project=$(CDPATH= cd -- "$(dirname -- "$0")/.." && pwd)
if ! command -v rclone >/dev/null 2>&1; then
  export PATH="/tmp/ostojaos-oauth-tools/runtime/usr/bin:$PATH"
fi
umask 077
mkdir -p "$project/docs/private/cloud-sync"
exec python3 "$project/modules/cloud-sync/tools/authorize.py" "$1" --output "$project/docs/private/cloud-sync/$1-$(date +%Y%m%d-%H%M%S).json"
