"""Offline-Nachrechnung. Optionales Ziel enthält ausschliesslich neu erzeugtes JSON."""
import argparse
import json
from pathlib import Path
import pilot
import uhrtest


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--out', type=Path)
    args = parser.parse_args()
    result = {'M1': pilot.run(), 'Uhr': uhrtest.run()}
    data = json.dumps(result, indent=2, ensure_ascii=False) + '\n'
    if args.out:
        args.out.write_text(data, encoding='utf-8')
    else:
        print(data, end='')


if __name__ == '__main__':
    main()
