#!/usr/bin/env bash
# Unpack the reviewed micromamba binary into a fresh temporary directory.
set -euo pipefail
prefix=${1:?expected a new installation prefix}
here=$(cd "$(dirname "$0")" && pwd)
tmpdir=$(mktemp -d)
trap 'rm -rf "$tmpdir"' EXIT
curl --fail --location --retry 2 --max-time 120 --silent --show-error \
  https://conda.anaconda.org/conda-forge/linux-64/micromamba-2.10.0-0.tar.bz2 -o "$tmpdir/mamba.tar.bz2"
echo "9a97976244929bbae28fb1fae504e74a3e7e6d1932870e3a03321f01b7fbd07b  $tmpdir/mamba.tar.bz2" | sha256sum --check --status
tar -xjf "$tmpdir/mamba.tar.bz2" -C "$tmpdir" bin/micromamba
MAMBA_ROOT_PREFIX="$tmpdir/root" "$tmpdir/bin/micromamba" create --yes -p "$prefix" --file "$here/tempo2.lock"
