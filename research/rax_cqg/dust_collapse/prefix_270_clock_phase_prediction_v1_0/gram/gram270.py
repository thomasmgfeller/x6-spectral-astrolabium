"""Rebuild the scalar Gram certificate at marked prefix 270 from archived inputs."""
import argparse
from fractions import Fraction
from hashlib import sha256
from io import BytesIO
from itertools import combinations, permutations
import json
from pathlib import Path
import sys
from tempfile import TemporaryDirectory
from unittest.mock import patch
from zipfile import ZipFile

import mpmath as mp
import sympy as sp

PREFIX = 270
TYPES = (623, 662, 718, 726, 751, 760, 764, 767, 5295, 5307, 26935)
SOURCE_HASH = '05968e2c6afeb263c66faa15255e1499b7cd6a90a6ff2b6510fd6b48cbc4c1c5'
BOUNDARY_NAME = 'CST_DUST_Randabbildung_1564_v0_1_Pruefpaket.zip'
SELECTION_NAME = 'CST_DUST_Praefix_1564_Selektionsgleichung_v0_1_Pruefpaket.zip'

def check(value, message):
    if not value:
        raise ValueError(message)

def unpack(path, temp):
    raw = path.read_bytes()
    check(sha256(raw).hexdigest() == SOURCE_HASH, 'Input digest mismatch')
    with ZipFile(BytesIO(raw)) as outer:
        boundary = outer.read(BOUNDARY_NAME)
    with ZipFile(BytesIO(boundary)) as middle:
        selection = middle.read(SELECTION_NAME)
    with ZipFile(BytesIO(selection)) as inner:
        inner.extractall(temp)
    return temp/'prefix_1564_selection_v0_1'

def descendants(prefix):
    """Reconstruct the allowed marked continuations using the full parent support."""
    pairs = tuple(combinations(range(6),2))
    data = prefix.read('exchange.json')['chain']
    allowed = set()
    for code in map(int, data['target_pair_marginal']):
        allowed.add(code)
        allowed.add(prefix.encode(prefix.edges(code), (0,1,2,4,3,5)))
    check(PREFIX in allowed, 'Prefix outside the archived chain family')
    by_type = {}
    for end in data['fully_admissible_end_types']:
        edges = [edge for k,edge in enumerate(pairs) if end & (1<<k)]
        marked = {prefix.encode(edges, perm) for perm in permutations(range(6))}
        paths = []
        for c in marked:
            if c & prefix.PAIR_MASK != PREFIX:
                continue
            if all((prefix.encode(prefix.edges(c), p) & prefix.PAIR_MASK) in allowed for p in prefix.MARKS):
                paths.append(c)
        if paths:
            check(prefix.canonical(edges,6) == end, 'Noncanonical end code')
            by_type[end] = sorted(paths)
    return by_type

def exact_complex_matrix(a):
    return [[[str(sp.re(x)),str(sp.im(x))] for x in row] for row in a.tolist()]

def compute(base):
    sys.path.insert(0,str(base))
    import certify
    import prefix
    import scalar
    by_type = descendants(prefix)
    check(sorted(by_type) == list(TYPES), 'Different end type list on archived support')
    mp.mp.dps = 65
    rates = {}
    diagnostics = {}
    states = {}
    with patch.object(scalar.geometry,'order',scalar.layout):
        for j in TYPES:
            key = (6,j)
            details, state = scalar.geometry.kernel(key)
            check(details['status'] == 'ADMISSIBLE' and details['free_directions'] == 0,
                  f'Unqualified scalar quotient for {j}')
            check(details['symplectic_both_directions'], f'Invalid scalar map for {j}')
            rates[j] = scalar.rate(key)
            states[j] = state
            beta = 4/mp.sqrt(6)
            check(mp.norm(state[0] - beta*scalar.geometry.numeric(rates[j])) < mp.mpf('1e-50'),
                  f'Precision reconstruction discrepancy for {j}')
            minor = [rates[j][:k,:k].applyfunc(sp.re).det() for k in (1,2,3)]
            check(min(minor)>0, 'Invalid Gaussian real part')
            diagnostics[str(j)] = {
                'marked_paths':by_type[j], 'integration_rank':details['integration_rank'],
                'delta_rows':details['delta_rows'], 'free_directions':details['free_directions'],
                'pure_bulk_null_vectors':details['pure_bulk_null_vectors'],
                'mixed_legendre_rank':details['legendre_rank'],
                'mixed_legendre_size':details['legendre_size'],
                'real_precision_leading_minors':list(map(str,minor)),
                'precision_over_beta':exact_complex_matrix(rates[j])}
    # Precision scales uniformly by beta, which cancels in the fourth-power formula.
    # The archived half-density factors fix the phases of the separate states.
    row_upper = {j:Fraction(0) for j in TYPES}
    certs = []
    numeric = [[None]*len(TYPES) for j in TYPES]
    for a,i in enumerate(TYPES):
        diag = scalar.overlap(states[i],states[i])
        check(abs(diag-1)<mp.mpf('1e-50'), 'Gaussian normalization')
        numeric[a][a] = ['1','0']
        for b,j in enumerate(TYPES[:a]):
            exact = certify.overlap_fourth(rates[i],rates[j])
            upper = Fraction(certify.upper_fourth_root(exact))
            z = scalar.overlap(states[i],states[j])
            check(abs(abs(z)**4 - mp.mpf(int(exact.p))/int(exact.q)) < mp.mpf('1e-50'),
                  'Exact modulus versus original phased overlap')
            numeric[a][b] = [mp.nstr(z.real,25),mp.nstr(z.imag,25)]
            numeric[b][a] = [mp.nstr(z.real,25),mp.nstr(-z.imag,25)]
            certs.append({'end_types':[i,j],'absolute_fourth':str(exact),'absolute_upper':str(upper)})
            row_upper[i]+=upper
            row_upper[j]+=upper
    worst = max(row_upper.values())
    check(worst<1, 'Gershgorin does not certify strict positivity')
    return {'prefix':PREFIX,'family':'chain','types':list(TYPES),'source_sha256':SOURCE_HASH,
            'domain':'Normalized exterior scalar Gaussians in the published common collar coordinates',
            'gram_lower':str(1-worst),'gram_upper':str(1+worst),
            'max_row_sum_end_types':[j for j in TYPES if row_upper[j]==worst],
            'offdiagonal_row_sum_upper':{str(j):str(x) for j,x in row_upper.items()},
            'end_types':diagnostics,'overlap_certificates':certs,
            'gram_approx_real_imag':numeric}

if __name__ == '__main__':
    if not __debug__:
        raise SystemExit('Use Python without -O for all upstream assertions.')
    cli = argparse.ArgumentParser(description=__doc__)
    cli.add_argument('--source', type=Path, required=True)
    cli.add_argument('--types', help='Optional comma-separated expected types.')
    cli.add_argument('--output', type=Path, required=True)
    args = cli.parse_args()
    if args.types:
        check(tuple(map(int,args.types.split(',')))==TYPES, 'Unexpected choice of end types')
    with TemporaryDirectory() as temp:
        result=compute(unpack(args.source,Path(temp)))
    args.output.write_text(json.dumps(result,indent=2)+'\n')
