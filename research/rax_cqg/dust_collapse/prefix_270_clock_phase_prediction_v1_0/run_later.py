"""Call only on a separately authorized post-registration target run."""
import argparse
from pathlib import Path
from packet270 import evaluate
from score import checked_registration,load_json
from study import HERE, write_fresh


def main():
    cli=argparse.ArgumentParser()
    cli.add_argument('output',type=Path)
    args=cli.parse_args()
    if args.output.exists():raise SystemExit('Choose a fresh output path')
    lock=checked_registration()
    ref=load_json(HERE/'reference.json')
    write_fresh(args.output,evaluate(ref,lock))


if __name__=='__main__':
    if not __debug__:raise SystemExit('Keep assertions enabled.')
    main()
