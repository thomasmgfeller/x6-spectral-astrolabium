"""Fixed v0.6 input and the extra event with label 14."""
from pathlib import Path
from hashlib import sha256
import sys
from zipfile import ZipFile
from itertools import combinations, product
from functools import cache
import json

ROOT = Path(__file__).resolve().parent
ARCHIVE = ROOT / 'input_v06.zip'
if not ARCHIVE.is_file():
    ARCHIVE = ROOT.parent / 'packages' / 'CST_DUST_N14_Volltraeger_v0_6_Pruefpaket.zip'
DIGEST = '04b2c22bc8867010ffe3ed0c4a27d52314342b8b724c64492d77e3b8d52b3826'
if sha256(ARCHIVE.read_bytes()).hexdigest() != DIGEST:
    raise ValueError('The PR 311 input archive differs.')
# Only materialize the signed-off source and data, then compare existing cached files.
CACHE = ROOT / 'input_v06'
with ZipFile(ARCHIVE) as source:
    for name in source.namelist():
        if not name.startswith(('reference/', 'study/')) or name.endswith('/'):
            continue
        data = source.read(name)
        dest = CACHE / name
        if dest.exists() and dest.read_bytes() != data:
            raise ValueError(f'Input differs: {name}')
        if not dest.exists():
            dest.parent.mkdir(parents=True, exist_ok=True)
            dest.write_bytes(data)
sys.path.insert(0, str(CACHE/'reference'))
import growth
from growth import geometry, orders

@cache
def layout(key):
    n, mask = key
    if n <= 6:
        return growth.layout(key)
    assert n == 7
    inner = (4, 5, 6, 11, 12, 13, 14)
    p, f = geometry.P, geometry.F
    edges = set(combinations(p, 2)) | set(combinations(f, 2))
    edges.update(product(p, inner + f))
    edges.update(product(inner, f))
    edges.update((inner[i], inner[j]) for i,j in orders.bit_edges(n, mask))
    labels = p + inner + f
    coeff = {}
    for i,j in sorted(edges):
        size = sum((i,k) in edges and (k,j) in edges for k in labels)
        coeff[i,j] = (1,-9,16,-8)[size] if size < 4 else 0
    return inner, coeff, len(labels)-sum(coeff.values())

def write(name, obj):
    (ROOT/name).write_text(json.dumps(obj, indent=2, sort_keys=True, allow_nan=False)+'\n')
