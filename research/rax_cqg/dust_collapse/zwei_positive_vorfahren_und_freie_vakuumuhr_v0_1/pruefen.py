"""Reproduce all stored results, and check deliberate off-band controls."""
from fractions import Fraction as F
from hashlib import sha256
import json

from kegel import ROOT
from auswerten import integers, scan
from gegenprobe import audit, audit_cone
from uhr import E, Box
from vakuumuhr import scan as scan_mixed


def same(filename, obj):
    expected = (json.dumps(obj, indent=2, sort_keys=True) + '\n').encode()
    assert (ROOT / filename).read_bytes() == expected, filename


def verify():
    for manifest in ('Pruefplan.sha256', 'Quellen.sha256', 'SHA256SUMS'):
        for line in (ROOT / manifest).read_text().splitlines():
            digest, path = line.split('  ', 1)
            assert sha256((ROOT / path).read_bytes()).hexdigest() == digest, path

    main = scan()
    same('Ergebnisse.json', main)
    check = audit()
    same('Gegenprobe.json', check)
    assert not main['unresolved'] and not main['intersections'] and not check['undecided']
    for name, summary in main['two_ancestor_results'].items():
        assert summary['counts']['cones'] == sum(check['counts'][name].values())
        # Re-route the second evaluator to the nearest external enclosures.
        # In these controls it must retain zero as a possible residual.
        for record in summary['neighbours_outside_slab'].values():
            row = record['witness']
            key = (int(name == 'chain'), *(integers(row[field]) for field in
                    ('u_past', 'u_future', 'v_past', 'v_future')))
            x = Box.hull(*map(F, record['interval']))
            target = E - 2 + (4 - E) * x
            assert audit_cone(integers(row['old_past']), key, target) == 'residual_contains_zero'
    mixed = scan_mixed()
    same('Vakuumuhr.json', mixed)
    assert mixed['counts'] == {'outside_open_density_domain': 14, 'nonzero_vacuum_clock_gradient': 1}
    print('PASS — 23 + 1656 reference cones and their enclosures reproduced.')
    print('PASS — 158018 two-ancestor cones, two enumerations, direct density residual, 4 off-band checks.')
    print('PASS — mixed N17 control x=11/23; 15 restricted attachments excluded in target band.')
    print('Physical P3: 60 NOT_RUN.')


if __name__ == '__main__':
    if not __debug__:
        raise SystemExit('Run without -O')
    verify()
