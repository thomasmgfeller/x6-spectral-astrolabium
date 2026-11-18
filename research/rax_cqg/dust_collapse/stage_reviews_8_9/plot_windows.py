"""Render the fixed-window example in review 9. Requires Matplotlib."""
import argparse

import matplotlib as mpl
import matplotlib.pyplot as plt

from verify import LEVELS, HALF_WIDTHS, window_average


def render(output):
    mpl.rcParams.update({
        "font.size": 10, "axes.spines.top": False, "axes.spines.right": False,
        "font.family": "DejaVu Sans", "axes.labelcolor": "#233e48",
        "xtick.color": "#405861", "ytick.color": "#405861", "axes.edgecolor": "#9baeb0",
    })
    fig, ax = plt.subplots(figsize=(7.6, 2.5), layout="constrained")
    ax.plot(LEVELS, LEVELS, color="#153e4a", marker="o", label="Spitzenwert", linewidth=1.8, markersize=4)
    styles = [("Fenster L = 1/8", "#077768", "s"), ("L = 1/4", "#99451d", "^"), ("L = 1/2", "#725795", "D")]
    for width, (label, color, marker) in zip(HALF_WIDTHS, styles):
        averages = [float(window_average(n, width)) for n in LEVELS]
        ax.plot(LEVELS, averages, color=color, marker=marker, label=label, linewidth=1.8, markersize=4)
    ax.set_xscale("log", base=2)
    ax.set_yscale("log", base=2)
    ax.set_xticks(LEVELS, labels=[str(i) for i in LEVELS])
    ax.set_yticks([1/64, 1/8, 1, 8, 64], labels=["1/64", "1/8", "1", "8", "64"])
    ax.set_xlabel("Verfeinerungsindex n")
    ax.set_ylabel("Testsignal")
    ax.grid(axis="y", alpha=.25)
    ax.legend(loc="center left", bbox_to_anchor=(1.02, .5), frameon=False)
    fig.savefig(output, dpi=170)
    plt.close(fig)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("output", help="destination PNG file")
    render(parser.parse_args().output)
