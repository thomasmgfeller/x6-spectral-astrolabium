"""Conditional bridge from an empty clock prefix to a prepared four-point AA boundary.

Python 3.10+, mpmath 1.3.0. The decisive inequalities use interval arithmetic.
"""
from collections import Counter
from fractions import Fraction as Q
from pathlib import Path
import argparse
import hashlib
import json

from mpmath import iv
from quellen.schranken import dust_mean

ROOT = Path(__file__).resolve().parent
iv.dps = 50
Z = iv.mpc
D = Q(1, 8)
EDGES = (Q(0), Q(1, 24), Q(1, 16), D)
B = iv.sqrt(iv.mpf(8) / 3)


def check(condition, message):
    if not condition:
        raise ValueError(message)


def real(x):
    x = Q(x)
    return iv.mpf(x.numerator) / x.denominator


def conj(z):
    return Z(z.real, -z.imag)


def pair(a, b):
    return sum((conj(x)*y for x, y in zip(a, b, strict=True)), Z(0))


def centre(x):
    return (float(x.a) + float(x.b)) / 2


def approx(z):
    return [round(centre(z.real), 15), round(centre(z.imag), 15)]


def overlap(x, y):
    return x.a <= y.b and y.a <= x.b


def check_equal(z, w, name):
    check(overlap(z.real, w.real) and overlap(z.imag, w.imag), name)


def read_inputs():
    sources = json.loads((ROOT/'quellen.json').read_bytes())
    for name, entry in sources['files'].items():
        data = (ROOT/'quellen'/name).read_bytes()
        prefix = b'blob ' + str(len(data)).encode() + b'\0'
        check(hashlib.sha1(prefix+data).hexdigest() == entry['git_blob'], name)
    def read(name):
        return json.loads((ROOT/'quellen'/name).read_bytes())
    return read('aa_hessians.json')['histories'], read('normen.json'), read('schnitte.json')


def restriction(code):
    return sum(1 << (2*i+j-3) for i in (0,1) for j in (3,4)
               if code & (1 << (5*i+j)))


def zero_action(mask):
    # On two antichains all surviving relations are links. F4=N-number of links.
    h = [[Q(0) for _ in range(4)] for _ in range(4)]
    for i in (0,1):
        for j in (2,3):
            if mask & (1 << (2*i+j-2)):
                h[i][i] -= Q(1,2)
                h[j][j] -= Q(1,2)
                h[i][j] += Q(1,2)
                h[j][i] += Q(1,2)
    return h, 4-mask.bit_count()


def pivot_root(z):
    check(z.real.a > 0, 'ambiguous Gaussian square root')
    r = iv.sqrt((abs(z)+z.real)/2)
    return Z(r, z.imag/(2*r))


def packet_coefficients(h, prefactor):
    # Four Gaussian coordinates in the order two incoming, two outgoing.
    # Simultaneously eliminate the matrix and solve for inverse columns 2 and 3.
    rows = [[Z(int(i==j), -B*real(h[i][j])) for j in range(4)] +
            [Z(int(i==j)) for j in (2,3)] for i in range(4)]
    detroot = Z(1)
    for k in range(4):
        pivot = rows[k][k]
        detroot *= pivot_root(pivot)
        rows[k] = [x/pivot for x in rows[k]]
        for i in range(4):
            if i != k:
                factor = rows[i][k]
                rows[i] = [x-factor*y for x,y in zip(rows[i],rows[k])]
    trace = rows[2][4]+rows[3][5]
    sym = rows[2][5]+rows[3][4]
    unit = prefactor/detroot
    return [unit, unit*(trace+sym-1)/iv.sqrt(2), unit*(trace-sym-1)/iv.sqrt(2)]


def packet_groups(histories):
    counts = Counter(restriction(h['order_code']) for h in histories)
    check(counts == {6:2,7:5,9:2,11:5,13:5,14:5,15:9}, '33 to seven')
    vacuum = [Z(0) for _ in range(3)]
    for mask, multiplicity in sorted(counts.items()):
        kernel, f4 = zero_action(mask)
        prefactor = iv.pi*real(Q(multiplicity,66))*iv.exp(Z(0,f4))
        vector = packet_coefficients(kernel, prefactor)
        vacuum = [x+y for x,y in zip(vacuum,vector)]
    groups = [[Z(0) for _ in range(3)] for _ in range(2)]
    for h in histories:
        m = [[Q(v) for v in row] for row in h['H0_over_va']]
        c = -m[2][2]
        check(c>0, 'interior pivot')
        boundary = (0,1,3,4)
        kernel = [[m[i][j]+m[i][2]*m[2][j]/c for j in boundary] for i in boundary]
        prefactor = iv.pi/66 * iv.sqrt(2*iv.pi/(B*real(c))) * iv.exp(Z(0,h['F4']-iv.pi/4))
        vec = packet_coefficients(kernel,prefactor)
        p = h['p']-1
        groups[p] = [x+y for x,y in zip(groups[p],vec)]
    return counts, vacuum, groups


def primitive(u):
    out = []
    for p in (1,2):
        parts = [iv.mpf([real(lo).a,real(hi).b])*real(u) for lo,hi in dust_mean(p,u)]
        out.append(Z(*parts))
    return out


def length_weights(t):
    base = 2*iv.pi*iv.sqrt(1+B**2)/81
    oblique = iv.sqrt(real(Q(1370,841*t*t+529)))
    return (base*4*iv.sqrt(real(Q(9,12871))),
            base*(iv.sqrt(real(Q(9,1423450))) + 2*oblique*iv.sqrt(real(Q(9,69185)))))


def join(*vectors):
    return [sum(xs,Z(0)) for xs in zip(*vectors, strict=True)]


def response(dust, group_vectors):
    return [sum((coefficient*group[k] for coefficient,group in zip(dust,group_vectors)),Z(0))
            for k in range(len(group_vectors[0]))]


def classify(matrix):
    # Strictly positive pivots prove positive definiteness. After a positive
    # leading block a negative pivot witnesses failure of positive semidefiniteness.
    a = [row[:] for row in matrix]
    for k in range(len(a)):
        pivot = a[k][k].real
        if pivot.b < 0:
            return False
        check(pivot.a > 0, 'intervals do not decide a Schur pivot')
        for i in range(k+1,len(a)):
            for j in range(k+1,len(a)):
                a[i][j] = a[i][j] - a[i][k]*a[k][j]/pivot
    return True


def efficiency_bracket(gram, diag):
    # Bracket the exact threshold on this four-dimensional subspace with two
    # decimal rationals. eta=1 is excluded separately by the vacuum minor.
    scale = 10**8
    low,high = 0,scale
    def feasible(n):
        eta = real(Q(n,scale))
        a = [[Z(diag[i] if i==j else 0)-gram[i][j]*eta for j in range(4)] for i in range(4)]
        return classify(a)
    while high-low>1:
        mid=(low+high)//2
        if feasible(mid):
            low=mid
        else:
            high=mid
    check(feasible(low) and not feasible(high), 'threshold bracket')
    return [f'{n//scale}.{n%scale:08d}' for n in (low,high)]


def run():
    histories, original, cuts = read_inputs()
    counts,vacuum,groups = packet_groups(histories)
    primitives = [primitive(u) for u in EDGES]
    intervals = [[b-a for a,b in zip(x,y)] for x,y in zip(primitives,primitives[1:])]
    w0 = pair(vacuum,vacuum).real
    check(w0.a > 0 and w0.b<1,'three-packet vacuum norm')
    # Cross-check both full-window triples against the rounded published values.
    for v,ref in [(vacuum,original['packet_amplitudes']['0']),
                  (response(primitives[-1],groups),original['packet_amplitudes']['1'])]:
        for z,(re,im) in zip(v,ref):
            check(abs(z-Z(real(re),real(im))).b<real('0.00000000001'),'archived packet')
    result = {'commit':json.loads((ROOT/'quellen.json').read_bytes())['commit'],
              'null_restriction_counts':dict(sorted(counts.items())),
              'edges':[str(x) for x in EDGES],'cases':{}}
    for t in (1,4):
        weights = length_weights(t)
        g0 = vacuum+[Z(iv.sqrt(1-w0)), Z(0), Z(0)]
        group_vectors = [g+[Z(0)]+[Z(iv.sqrt((1-w0)*weights[p])) if j==p else Z(0)
                                    for j in (0,1)] for p,g in enumerate(groups)]
        vectors = [response(dt,group_vectors) for dt in intervals]
        total = response(primitives[-1],group_vectors)
        inner = pair(g0,total)
        check(inner.real.a>real('-0.0100200') and inner.real.b<real('-0.0100199') and
              inner.imag.a>real('0.0014268') and inner.imag.b<real('0.0014269'), 'mixed vacuum/birth')
        q = pair(total,total).real
        check(abs(q-real(original['anchored_products']['00_20_02']['normalized_one_weight'][str(t)])).b <
              real('0.000000000001'),'archived one-birth norm')
        gram = [[pair(a,b) for b in [g0,*vectors]] for a in [g0,*vectors]]
        # For every u, |Z_p(u)|<=1, also for unmeasured density phase marks.
        lbound = sum(iv.sqrt(pair(g,g).real) for g in group_vectors)
        check(real('0.98')*(1+real(D)*lbound**2)<1,'common success effect eta=0.98 on the whole time space')
        lipschitz = B/4 * sum((p+1)*iv.sqrt(pair(g,g).real) for p,g in enumerate(group_vectors))
        widths = [b-a for a,b in zip(EDGES,EDGES[1:])]
        rows={}
        for split in (1,2):
            left,right=join(*vectors[:split]),join(*vectors[split:])
            for x,y in zip(join(left,right),total):
                check_equal(x,y,'direct vs regrouped amplitude')
            cross=pair(left,right)
            check_equal(pair(g0,left)+pair(g0,right),inner,'vacuum mixed cut')
            check_equal(pair(left,left)+pair(right,right)+2*cross.real,pair(total,total),'cut weight')
            # Verify the length-only part independently against the prior rational record.
            length_cross=pair(left[-2:],right[-2:])/(1-w0)
            src=cuts['length_products'][str(t)][str(EDGES[split]/D)]
            for x,key in [(length_cross.real,'real_cross'),(length_cross.imag,'imag_cross')]:
                lo,hi=src[key]
                check(overlap(x,iv.mpf([lo,hi])),'published length product')
            rows[str(EDGES[split])]={'L':approx(pair(left,left))[0],'R':approx(pair(right,right))[0],
                      'LR':approx(cross),'share_2ReLR':centre(2*cross.real/q),
                      '0L':approx(pair(g0,left)), '0R':approx(pair(g0,right))}
        betas={}
        for beta in (Q(5,4),Q(4,3)):
            def h0(u):
                return (1-real(beta))*real(u)+iv.exp(-real(u))
            def h1(u):
                return real(beta)-1+iv.exp(-real(u))
            kappa=h1(D)/h0(D)
            for c in EDGES[1:-1]:
                check_equal(Z(h0(c)*h0(D)/h0(c)),Z(h0(D)),'vacuum propagation')
                check_equal(Z(real(c)*h1(c)*h1(D)/h1(c)),Z(real(c)*h1(D)),'early birth')
                check_equal(Z(h0(c)*real(D-c)*h1(D)/h0(c)),Z(real(D-c)*h1(D)),'late birth')
            source_diag=[iv.mpf(1)]+[kappa*real(b-a) for a,b in zip(EDGES,EDGES[1:])]
            bracket = efficiency_bracket(gram,source_diag)
            # The complementary time modes have covariance bounded by their trace.
            # The within-bin mean-square residual is at most Lip^2 length^3/12.
            defect = lipschitz**2 * real(sum(w**3 for w in widths)/12) / kappa
            lo = 1/(1/real(bracket[0])+defect)
            n = int(centre(lo)*10**8) - 1
            safe = Q(n,10**8)
            check(real(safe)<lo, 'rounded continuum lower certificate')
            example = Q(9994,10000)
            status = 'admissible' if beta==Q(4,3) else 'excluded'
            check((safe>example if status=='admissible' else Q(bracket[1])<example),
                  'efficiency comparison on full time record')
            betas[str(beta)]={'P0':centre(h0(D)),'P1':centre(real(D)*h1(D)),
                              'eta_max_bracket':bracket,
                              'continuum_eta_bracket':[f'{n//10**8}.{n%10**8:08d}',bracket[1]],
                              'eta_0_9994':status,'covariance_defect_approx':centre(defect)}
        result['cases'][str(t)]={'relative_one_weight':centre(q),'vacuum_birth':approx(inner),
            'uniform_L_upper_rounded_up':str((int(centre(lbound)*10000)+1)/10000),
            'cuts':rows,'candidate_clocks':betas}
        check(lbound.b < real(result['cases'][str(t)]['uniform_L_upper_rounded_up']), 'display bound')
    return result


if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--out',type=Path)
    args=parser.parse_args()
    content=json.dumps(run(),ensure_ascii=False,indent=2,sort_keys=True)+'\n'
    if args.out:
        args.out.write_text(content,encoding='utf-8')
    else:
        print(content,end='')
