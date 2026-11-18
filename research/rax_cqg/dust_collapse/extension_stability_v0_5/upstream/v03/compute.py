"""Generate clock integrals for the selections fixed by study.json and supplement.json."""
import argparse
import json
from pathlib import Path
from orders import daughter_counts, paths, screen, label
from clock_network import scheme, integrate


def select(states):
    parents = sorted(k for k in states if k[0] == 4)
    children = {k: sorted((5, g) for g in daughter_counts(k) if (5, g) in states) for k in parents}
    small = {g for row in children.values() for g in row if scheme(g)[0] <= 3}
    extra = {k:min(g for g in row if scheme(g)[0] == 4) for k,row in children.items() if not small.intersection(row)}
    return children, small, extra


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("out", type=Path)
    args = ap.parse_args()
    families = paths()
    _, states = screen(families)
    _, small, extra = select(states)
    rows = {}
    for k in sorted(small | set(extra.values())):
        rows[label(k)] = integrate(k)
        print(label(k), rows[label(k)]["grids"][-1]["grid"], flush=True)
    args.out.write_text(json.dumps(rows, indent=2, allow_nan=False) + "\n")


if __name__ == "__main__":
    main()
