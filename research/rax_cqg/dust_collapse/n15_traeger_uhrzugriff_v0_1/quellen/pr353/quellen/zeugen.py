"""Find and verify interior two-history witnesses for rows left open by the sector bound."""
from bisect import bisect_left
import cmath
from fractions import Fraction as Q
from itertools import product
from math import factorial, pi
from pathlib import Path
import argparse
import json

import pruefen as model
from pruefen import support, tube, coherence as iv

ROOT = Path(__file__).resolve().parent
INSET = Q(1023, 1024)
WEIGHTS = ((7, 4), (3, 2))
GRID = 10**6


def offsets():
    for a,b in support.WINDOWS:
        for sign in (-1, 1):
            yield ((a+b) + sign*INSET*(b-a))/2


def fields(setup, mask):
    paths, center, radius, _, _, _ = setup
    u = {j:center[j]+(1 if mask & (1 << i) else -1)*radius*INSET for i,j in enumerate(support.I)}
    return u, support.fractions_on_paths(paths, u)


def candidates(setup, edges, rho):
    """Floats select coordinates only. The returned witnesses are certified separately."""
    delta = float(sum(support.DELTA)/2)
    buckets = {1:[], -1:[]}
    for mask in range(128):
        exact_u, exact_f = fields(setup, mask)
        u = {j:float(x) for j,x in exact_u.items()}
        fractions = list(map(float, exact_f))
        for oi, offset in enumerate(offsets()):
            e = float(offset)/delta
            y = {j:float(j-5) for j in support.PAST + support.FUTURE}
            y[3] += e
            y.update({j:y[3]+(4-e)*u[j] for j in support.I})
            coeff = [1.0]*15
            for a,b,k in edges:
                coeff[b] += (k/19)*(y[b]-y[a])**2
            past = sum(coeff[j] for j in support.PAST)
            future = sum(coeff[j] for j in support.FUTURE)/8
            inner = sum(coeff[j]*f for j,f in zip(support.I,fractions))*4*(4*delta-float(offset))
            for side,rhosign in product((1,-1),(-1,1)):
                s = -(past*float(rho+rhosign*INSET/32)+future+inner*(1+float(side*INSET/100)))/2
                buckets[side].append((s,(mask,oi,rhosign)))
    return buckets


def select(buckets):
    minus = sorted(buckets[-1])
    phases = [phase for phase,_ in minus]
    best = None
    for x, coord in buckets[1]:
        for target in (x-pi, x+pi):
            pos = bisect_left(phases, target)
            for j in {max(0,min(len(minus)-1,k)) for k in (pos-1,pos)}:
                score = (round(abs(abs(x-minus[j][0])-pi),12), coord, minus[j][1])
                if best is None or score < best:
                    best = score
    return best[1], best[2]


def history(code,rho,side,coords):
    mask, index, rhosign = coords
    assert 0 <= mask < 128 and 0 <= index < 4 and rhosign in (-1,1)
    setup = tube.template(code)
    _,rel = support.geometry(code)
    u, fractions = fields(setup,mask)
    assert min(fractions)>0 and sum(fractions)==1
    assert all(abs(u[j]-setup[1][j]) < setup[2] for j in support.I)
    delta = support.DELTA
    offset = list(offsets())[index]
    assert any(a<offset<b for a,b in support.WINDOWS)
    e = tuple(sorted(offset/x for x in delta))
    d = tuple(4*x-offset for x in delta)
    duration = iv.sub(iv.bounds(4),e)
    y = {j:iv.bounds(Q(j-5)) for j in support.PAST+support.FUTURE}
    y[3] = iv.add(y[3],e)
    y.update({j:iv.add(y[3],iv.mul(duration,iv.bounds(u[j]))) for j in support.I})
    assert all(y[a][1]<y[b][0] for a,b in rel)
    inlet = rho+rhosign*INSET/32
    assert rho-Q(1,32)<inlet<rho+Q(1,32)
    w = dict.fromkeys(support.PAST,iv.bounds(inlet))
    w.update(dict.fromkeys(support.FUTURE,iv.bounds(Q(1,8))))
    marker = model.MASS*(1+side*INSET/100)
    shares = {j:marker*f for j,f in zip(support.I,fractions)}
    w.update({j:iv.mul(d,iv.bounds(shares[j])) for j in support.I})
    assert all(0<lo<=hi<1 for lo,hi in w.values())
    # Four-shift response per unit duration, recalculated from all interval layers.
    response = dict.fromkeys(support.I+support.FUTURE, Q(0))
    total = iv.bounds(Q(0))
    for weight in w.values():
        total = iv.add(total,weight)
    for a,b in sorted(rel):
        interior = sum((a,j) in rel and (j,b) in rel for j in range(15))
        k = (1,-9,16,-8)[interior] if interior<4 else 0
        if a in support.PAST and b in response:
            response[b] -= Q(k*(76,47,24,8)[a],64)
        total = iv.add(total,iv.mul(iv.bounds(Q(k,19)),iv.mul(w[b],iv.sq(iv.sub(y[b],y[a])))))
    assert all(response[j]==0 for j in support.FUTURE)
    assert sum(response[j]*v for j,v in shares.items())==marker
    return iv.mul(iv.bounds(Q(-1,2)),total)


def trig_phase(lo, hi):
    # Cosine at the rational midpoint with absolute Taylor remainder and Lipschitz
    # error <= interval radius. Outward rounding limits integer sizes in later steps.
    scale = 10**12
    lo = Q((lo*scale).__floor__(),scale)
    hi = Q((hi*scale).__ceil__(),scale)
    x = (lo+hi)/2
    poly = sum((-1)**i*x**(2*i)/factorial(2*i) for i in range(11))
    error = abs(x)**21/factorial(21)+(hi-lo)/2
    return max(Q(-1),poly-error), min(Q(1),poly+error)


def certify(code,rho,coords):
    plus,minus = (history(code,rho,side,coord) for side,coord in zip((1,-1),coords))
    delta_s = iv.sub(plus,minus)
    cl,ch = trig_phase(*delta_s)
    h = model.COUPLING*model.MASS*model.ETA*INSET
    for p,n in WEIGHTS:
        re_lo = (p*p+n*n)*(1-h*h/2)+2*p*n*cl
        re_hi = p*p+n*n+2*p*n*ch
        im_lo = (p*p-n*n)*(h-h**3/6)
        im_hi = (p*p-n*n)*h
        assert re_lo>0
        zlo, zhi = im_lo/re_hi, im_hi/re_lo
        assert 0<zlo<=zhi<1 and model.COUPLING*model.MASS+zhi<3
        # atan(z) >= z-z^3/3 is increasing on [0,1].
        lower = (zlo-zlo**3/3)/(model.COUPLING*model.MASS)
        upper = zhi/(model.COUPLING*model.MASS)
        lower = Q((lower*GRID).__floor__(),GRID)
        upper = Q((upper*GRID).__ceil__(),GRID)
        if lower>model.LIMIT:
            # Separate numerical check from the two normalized complex arms.
            samples = [(p, plus, 1), (n, minus, -1)]
            def arm(orientation):
                amplitude = 0j
                for weight, phase, sign in samples:
                    mark = model.MASS * (1 + sign*model.ETA*INSET)
                    argument = sum(phase)/2 + orientation*model.COUPLING*mark/2
                    amplitude += weight*cmath.exp(1j*float(argument))
                return amplitude/(p+n)
            estimate = cmath.phase(arm(1)*arm(-1).conjugate())/float(model.COUPLING)
            observed = abs(estimate/float(model.MASS)-1)
            assert float(lower) <= observed <= float(upper)
            return {'weights':[p,n],'relative_error_lower':str(lower),'relative_error_upper':str(upper),
                    'plus':list(coords[0]),'minus':list(coords[1])}
    return None


def evaluate(reference, search):
    table = json.loads((ROOT/'ergebnis.json').read_text())['per_type']
    result = {}
    for code, rows in sorted((int(c),v) for c,v in table.items()):
        for rho,data in sorted(rows.items()):
            if data['angle_joint']:
                continue
            key = f'{code};{rho}'
            if search:
                _,rel = support.geometry(code)
                coords = select(candidates(tube.template(code),model.coefficients(rel),Q(rho)))
            else:
                entry = reference['rows'][key]
                coords = entry['coordinates']
            result[key] = {'coordinates':[list(c) for c in coords],'witness':certify(code,Q(rho),coords)}
    counter = sorted({int(k.split(';')[0]) for k,v in result.items() if v['witness']})
    unresolved = sorted({int(k.split(';')[0]) for k in result}-set(counter))
    passes = len(table)-len(counter)-len(unresolved)
    return {'rows':result,'types_with_witness':counter,'unresolved_types':unresolved,'certified_types':passes,
            'witness_rows':sum(v['witness'] is not None for v in result.values())}


if __name__=='__main__':
    if not __debug__:
        raise SystemExit('Use Python without -O.')
    cli = argparse.ArgumentParser()
    cli.add_argument('--search',action='store_true',help='repeat the floating-point discovery grid')
    cli.add_argument('--emit',action='store_true')
    args=cli.parse_args()
    for entry in ('zeugenplan','pruefplan'):
        sha,path=(ROOT/(entry+'.sha256')).read_text().split()
        assert model.sha256((ROOT/path).read_bytes()).hexdigest()==sha
    destination = ROOT/'zeugen.json'
    ref = {} if args.emit and args.search else json.loads(destination.read_text())
    result = evaluate(ref,args.search)
    if args.emit:
        print(json.dumps(result,indent=2,sort_keys=True))
    else:
        assert result==ref
        print('PASS',len(result['types_with_witness']),'types with interior witnesses;',
              result['witness_rows'],'witness rows;',len(result['unresolved_types']),'unresolved types')
