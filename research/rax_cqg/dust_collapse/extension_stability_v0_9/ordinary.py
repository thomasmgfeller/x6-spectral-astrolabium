"""Replay the inherited four-parent contraction for the third and fourth ranked masks."""
from reference import ROOT, save_json
from uhrtest import calculate

if __name__ == "__main__":
    save_json(ROOT / "four_parents.json", calculate((45885, 45851)))
