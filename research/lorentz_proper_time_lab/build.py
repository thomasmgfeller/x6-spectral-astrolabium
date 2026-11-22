#!/usr/bin/env python3
"""Build the dependency-free HTML; --check never writes."""
import argparse
import ast
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
TARGET = HERE.parents[1] / 'app/proper-time.html'


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--check', action='store_true')
    args = parser.parse_args()
    text = (HERE / 'web.html').read_text()
    order = HERE / 'order_geometry'
    text = text.replace('<!-- ORDER_PANEL -->', (order/'panel.html').read_text())
    files = {'STYLE': HERE/'style.css', 'CORE': HERE/'core.js', 'UI': HERE/'ui.js',
             'ORDER_STYLE': order/'style.css', 'ORDER_BANK': order/'reference.json',
             'ORDER_CORE': order/'order.js', 'ORDER_UI': order/'ui.js'}
    for marker, file in files.items():
        text = text.replace(f'/* {marker} */', file.read_text())
    source = (order/'reference.py').read_text()
    function = next(node for node in ast.parse(source).body
                    if isinstance(node, ast.FunctionDef) and node.name == 'analyse')
    text = text.replace('/* NOTEBOOK_ANALYSE */', json.dumps(ast.get_source_segment(source, function)))
    if args.check:
        assert TARGET.read_text() == text, 'Generated HTML is stale'
        print('PASS_PROPER_TIME_HTML_BUILD')
    else:
        TARGET.write_text(text)
        print(TARGET)


if __name__ == '__main__':
    main()
