"""Reconstruct the per-source-box closure inventory from archived rounds.
SPDX-License-Identifier: Apache-2.0
"""
from thc_common import *


def inventory():
    frozen()
    source, parents = original()
    active = {r['path']: r for r in source}
    summary = read(HERE / 'summary.json')
    for rec in summary['rounds']:
        active = replace_round(active, read(HERE / ('round_%02d.json.gz' % rec['level'])))
    final = sorted(active.values(), key=path_key)
    rows = []
    for parent in parents:
        path = parent['path']
        leaves = [r for r in final if r['path'] == path or r['path'].startswith(path + '/')]
        assert leaves and sum(volume(r) for r in leaves) == volume(parent)
        states = Counter(r['status'] for r in leaves)
        rows.append(dict(source_path=path, source_box=parent['box'],
                         source_volume=str(volume(parent)),
                         status='HOLD' if states['HOLD'] else 'CLOSED',
                         terminal_descendants=len(leaves),
                         terminal_paths=[r['path'] for r in leaves],
                         decisions=dict(states)))
    closed = sum(r['status'] == 'CLOSED' for r in rows)
    assert closed == summary['closed_source_hold_cells']
    return dict(source_hold_cells=len(parents), closed_cells=closed,
                unresolved_cells=len(parents)-closed, rows=rows)


if __name__ == '__main__':
    result = inventory()
    if '--verify' in sys.argv:
        assert result == read(HERE / 'closed_cells.json')
    else:
        save(HERE / 'closed_cells.json', result)
    print(json.dumps({k: v for k, v in result.items() if k != 'rows'}))
