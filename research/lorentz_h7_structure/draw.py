"""Deterministic exact Hasse diagram; edges derived from full input relations."""
import argparse
import json
from math import hypot
from pathlib import Path

HERE = Path(__file__).resolve().parent


def render():
    data = json.loads((HERE/'inputs.json').read_text())
    ids = ['n7-0475', 'n7-0734']
    coordinates = [[(60, 200), (135, 310), (310, 310), (210, 200), (365, 200), (365, 90), (185, 90)],
                   [(60, 310), (365, 310), (220, 310), (310, 200), (150, 200), (320, 90), (100, 90)]]
    parts = ['<svg xmlns="http://www.w3.org/2000/svg" width="920" height="460" viewBox="0 0 920 460" role="img" aria-labelledby="title desc">',
             '<title id="title">Minimal H7 counterexample: two different causal orders</title>',
             '<desc id="desc">Exact Hasse diagrams, future upward. Left order n7-0475 has one isolated element and 154 linear extensions; right order n7-0734 is connected and has 162. Both have the same H7 signature.</desc>',
             '<defs><marker id="arrow" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 Z" fill="#43546b"/></marker></defs>',
             '<rect width="920" height="460" fill="#f7f9fc"/>',
             '<g font-family="sans-serif" fill="#172b47">',
             '<text x="460" y="30" text-anchor="middle" font-size="21" font-weight="bold">Different orders, identical H7 signature</text>']
    for index, (name, points) in enumerate(zip(ids, coordinates)):
        offset = 20+460*index
        parts.append(f'<g transform="translate({offset},40)">')
        parts.append(f'<text x="200" y="22" text-anchor="middle" font-size="18">{name}</text>')
        c = [[int(x) for x in row] for row in data['relations'][name]]
        for i in range(7):
            for j in range(7):
                if not c[i][j] or any(c[i][v] and c[v][j] for v in range(7)):
                    continue
                x, y = points[i]; xx, yy = points[j]; length = hypot(xx-x, yy-y)
                ux, uy = (xx-x)/length, (yy-y)/length
                parts.append(f'<line x1="{x+19*ux:.3f}" y1="{y+19*uy:.3f}" x2="{xx-23*ux:.3f}" y2="{yy-23*uy:.3f}" stroke="#43546b" stroke-width="2" marker-end="url(#arrow)"/>')
        for i, (x, y) in enumerate(points):
            isolated = not any(c[i]) and not any(row[i] for row in c)
            fill = '#ffe3a3' if isolated else '#dbeafa'
            parts.append(f'<circle cx="{x}" cy="{y}" r="18" fill="{fill}" stroke="#244f7c" stroke-width="2"/><text x="{x}" y="{y+5}" text-anchor="middle" font-size="16">{i}</text>')
        parts.append(f'<text x="200" y="360" text-anchor="middle" font-size="15">{[1,0][index]} isolated; {[154,162][index]} linear extensions</text></g>')
    parts += ['<text x="460" y="438" text-anchor="middle" font-size="14">Hasse edges only; the calculation uses the full transitive relation. Future points upward.</text>', '</g></svg>']
    return '\n'.join(parts)+'\n'


if __name__ == '__main__':
    parser = argparse.ArgumentParser(); parser.add_argument('--output', type=Path, required=True)
    parser.parse_args().output.write_text(render())
