#!/usr/bin/env python3
"""Build the dependency-free HTML; --check never writes."""
import argparse
from pathlib import Path

HERE = Path(__file__).resolve().parent
TARGET = HERE.parents[1] / 'app/proper-time.html'

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--check', action='store_true')
    args = parser.parse_args()
    text = (HERE / 'web.html').read_text()
    for marker, file in [('STYLE', 'style.css'), ('CORE', 'core.js'), ('UI', 'ui.js')]:
        text = text.replace(f'/* {marker} */', (HERE / file).read_text())
    if args.check:
        assert TARGET.read_text() == text, 'Generated HTML is stale'
        print('PASS_PROPER_TIME_HTML_BUILD')
    else:
        TARGET.write_text(text)
        print(TARGET)

if __name__ == '__main__':
    main()
