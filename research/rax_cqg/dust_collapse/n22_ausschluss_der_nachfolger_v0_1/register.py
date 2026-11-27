"""Join the original four-sector enumeration to both rounds of B+ exclusions."""
import csv
import gzip

SECTORS = ('A0', 'A+', 'B0', 'B+')
MASKS = ('P19', 'F19', 'P20', 'F20')


def key(row):
    return tuple(row[name] for name in MASKS)


def audit(path, previous, removed, keep):
    opened = {}
    count = 0
    with gzip.open(path, 'rt') as file:
        for count, row in enumerate(csv.DictReader(file, delimiter='\t'), start=1):
            assert int(row['ID']) == count
            for sector in SECTORS:
                if row[sector].endswith('/OPEN'):
                    opened[sector, count] = key(row)
    before = len(opened)
    for stage in (previous, removed):
        for case in stage:
            del opened['B+', case]
    assert opened == {(r['Sektor'], int(r['ID'])): key(r) for r in keep}
    return dict(projections=count, cases=count*len(SECTORS), original_open=before,
                previous_exclusions=len(previous), new_exclusions=len(removed),
                paired_A=sorted(k for s,k in opened if s == 'A0' and ('A+',k) in opened))
