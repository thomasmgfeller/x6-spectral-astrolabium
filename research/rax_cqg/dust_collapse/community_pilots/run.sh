#!/usr/bin/env bash
# Run an explicitly selected local check or a reserved volunteer pilot.
set -euo pipefail
if [[ $# != 3 ]]; then
    echo "Usage: bash run.sh check|A|B ARCHIVE_DIRECTORY NEW_RESULT_DIRECTORY" >&2
    exit 2
fi
mode=$1
case "$mode" in
    check) ;;
    A) window=0; seed=20261102921 ;;
    B) window=1; seed=20261102922 ;;
    *) echo "Select check, A or B." >&2; exit 2 ;;
esac
archives=$(realpath -e -- "$2")
results=$(realpath -m -- "$3")
model=CST_Staubkollaps_Geglaetteter_Massestrom_Pruefpaket.zip
bench=X6_CPU_Optimierung_Pruefpaket.zip
(
    cd "$archives"
    sha256sum --check <<'HASHES'
293abfb2a6854b1a33982d6accc5354838b0573fc2958b9e7212599ba78fe585  CST_Staubkollaps_Geglaetteter_Massestrom_Pruefpaket.zip
47d02094f4c04310af6bbef6b6860b9119735d8b242714ef82fe65d296196bb1  X6_CPU_Optimierung_Pruefpaket.zip
HASHES
)
mkdir -- "$results" # Refuse to overwrite an earlier run.
work=$(mktemp -d)
trap 'rm -rf -- "$work"' EXIT
cd "$work"
unzip -q "$archives/$model"
sha256sum --quiet -c SHA256SUMS
unzip -p "$archives/$bench" parallel_endpoints.patch > parallel_endpoints.patch
patch --batch -o whole_grid_parallel.cpp whole_grid.cpp < parallel_endpoints.patch
g++ -O3 -march=native -fopenmp -ffp-contract=off -std=c++17 -shared -fPIC whole_grid_parallel.cpp -o whole_grid_native.so
export OMP_NUM_THREADS=4 OMP_DYNAMIC=FALSE OPENBLAS_NUM_THREADS=1
unset PYTHONOPTIMIZE
{
    printf 'mode=%s\nOMP_NUM_THREADS=%s\n' "$mode" "$OMP_NUM_THREADS"
    LC_ALL=C lscpu | sed -n '/^Architecture:/p; /^Model name:/p'
    g++ -dumpfullversion
    python3 -c 'import sys,numpy,scipy; print(sys.version); print("NumPy",numpy.__version__,"SciPy",scipy.__version__)'
} > "$results/environment.txt"
# Recreate the control file to ensure that only a freshly generated CSV can be returned.
rm halo_checks.csv
python3 halo_reference.py
cp halo_checks.csv "$results/"
if [[ $mode == check ]]; then
    echo "Controls passed. Results: $results"
    exit 0
fi
echo "Starting pilot $mode, window $window, seed $seed."
SECONDS=0
python3 halo_reference.py --one "$seed" --window "$window" --density 6000000 > "$results/pilot_$mode.json.partial"
printf 'wall_seconds=%s\n' "$SECONDS" >> "$results/environment.txt"
mv -- "$results/pilot_$mode.json.partial" "$results/pilot_$mode.json"
echo "Completed. Results: $results"
