"""Intensity contrasts from paired histories, with outward integer intervals."""
from fractions import Fraction as F
from pathlib import Path
import json
import sys

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT / 'basis'))
from pruefung import I, S, D, H, K, R, CENTER, Q0, EPS, cell, decimals, hull
from intervalle import widen
from versuch import INNER, ORDER, EDGES, NOISE, coeffs

ZERO = I.of(0)
ONE = I.of(1)


def sin_box(x):
    # Taylor with a uniform absolute remainder. Only used on small intervals.
    assert x.absmax() < S // 4
    return widen(x, F(x.absmax(), S)**3 / 6)


def cos_box(x):
    assert x.absmax() < S // 4
    return widen(ONE - x**2 / 2, F(x.absmax(), S)**4 / 24)


def phase_cell(lobe, left, right):
    y, n, f, x, _, neutral, _, qs, diff = cell(lobe, left, right)
    assert y[3].hi < y[4].lo <= y[4].hi < y[5].lo
    for j, val in x.items():
        displacement = EPS * Q0 * n[j] / qs if j in (12, 13, 14) else ZERO
        for sign in (-1, 1):
            packet = val + sign * displacement
            assert (packet - F(99,100)*f[j]).lo > 0
            assert (F(101,100)*f[j] - packet).lo > 0
            if j == 12:
                assert (sign*(packet-F(1,8))).lo > 0 and (sign*(packet-f[j])).lo > 0
    return neutral, D*EPS*Q0*diff/qs


def paired(left, right):
    # Phasor right times conjugate of left. Differences are high minus low.
    s = right[0]-left[0]
    g = right[1]-left[1]
    return (-2*sin_box(s)*sin_box(g), 2*cos_box(s)*sin_box(g),
            cos_box(s-g), sin_box(s-g))


def average(left, right):
    sums = [I.of(0) for _ in range(4)]
    for a in left:
        for b in right:
            for i, v in enumerate(paired(a, b)):
                sums[i] += v
    return [x/(len(left)*len(right)) for x in sums]


def mean(a, b):
    return [(x+y)/2 for x,y in zip(a,b)]


def record_support(t):
    # x5=(u6-u4)/2+jitter. The earlier model fixes u6=3/8 exactly.
    centers = (I.of(F(1,8)),I.of(F(1,8))-t/(2*K))
    radius = R/(2*K)
    intervals = [(mid-radius-NOISE,mid+radius+NOISE) for mid in centers]
    for shift,(low,high) in zip((ZERO,t),intervals):
        for lobe in (-1,1):
            outer = cell(lobe,shift-R,shift+R)[3][5]
            assert outer.lo <= low.lo and outer.hi >= high.hi
    (left_low,left_high),(right_low,right_high)=intervals
    gap=left_low-right_high
    threshold=(left_low+right_high)/2
    minleft, maxright = centers[0]-radius, centers[1]+radius
    bandgap = F(99,100)*minleft-F(101,100)*maxright
    fraction = (minleft-maxright)/(minleft+maxright)
    assert gap.lo>0 and bandgap.lo>0 and fraction.lo>I.of(F(1,100)).hi
    return {'x5_left':decimals(I(left_low.lo,left_high.hi),13),
            'x5_right':decimals(I(right_low.lo,right_high.hi),13),
            'minimum_gap':decimals(gap,13), 'binary_threshold':decimals(threshold,13),
            'full_one_percent_profile_gap':decimals(bandgap,13),
            'relative_halfwidth_for_contact':decimals(fraction,13)}



def packets():
    t = H/D.sqrt()
    arms = [[phase_cell(lobe,shift-R,shift+R) for lobe in (-1,1)] for shift in (ZERO,t)]
    diag = mean(average(arms[0],arms[0]), average(arms[1],arms[1]))
    cross = average(arms[0],arms[1])
    a, b, c = diag[0], cross[0], -cross[1]
    baseline, real, imag = diag[2], cross[2], -cross[3]
    out = {}
    for key,mu in [('mischung',0),('ein_promille',F(1,1000)),('zehn_prozent',F(1,10)),('kohaerent',1)]:
        out[key] = decimals((a+mu*b)/(baseline+mu*real),20)
    assert a.hi < 0 < b.lo and a.lo+b.lo > 0 and c.lo > 0
    root = -a/b
    assert 0 < root.lo < root.hi < S//1000
    # At unit visibility, bracket a change of sign close to phi=0.
    def delta(phi):
        phi=I.of(phi)
        return a+b*cos_box(phi)+c*sin_box(phi)
    near = -F(925,1000000)
    far = -F(968,1000000)
    angles = I(I.of(far).lo,0)
    assert (c*cos_box(angles)-b*sin_box(angles)).lo>0
    assert delta(near).lo>0 and delta(far).hi<0
    return {'two_windows':out,'real_coherence_zero':decimals(root,12),
            'phase_radian_positive_at':str(near),'phase_radian_negative_at':str(far),
            'absolute_coefficients':{k:decimals(v,21) for k,v in zip(
              ('difference_diagonal','difference_real','difference_imag','low_diagonal','low_real','low_imag'),
              (a,b,c,baseline,real,imag))},'density_record':record_support(t),
            'low_visibility_factor_lower':decimals(real/baseline,14)[0]}


def continuous(parts):
    radius=K/64
    cells=[phase_cell(lobe,-radius+2*radius*k/parts,
                      -radius+2*radius*(k+1)/parts)
           for k in range(parts) for lobe in (-1,1)]
    # For each fixed end, remove one constant phase and accumulate the
    # two moments A=E[exp(iS)cos g], B=E[exp(iS)sin g]. This is linear
    # in the number of slabs. All enclosures hold uniformly in the end.
    central = cells[len(cells)//2][0]
    ref = F(central.lo+central.hi,2*S)
    ar=ai=br=bi=ZERO
    for neutral,odd in cells:
        phase=neutral-ref
        cr,si=cos_box(phase),sin_box(phase)
        co,so=cos_box(odd),sin_box(odd)
        ar+=cr*co
        ai+=si*co
        br+=cr*so
        bi+=si*so
    ar,ai,br,bi=(v/len(cells) for v in (ar,ai,br,bi))
    delta=4*(ai*br-ar*bi)
    low=(ar+bi)**2+(ai-br)**2
    assert low.lo>0
    return decimals(delta/low,16)


def matched_densities():
    # Unique displacement direction preserving all seven Voronoi cell shares:
    # sum of each adjacent displacement pair must vanish at every inner face.
    t=H/D.sqrt()
    signs=dict(zip(INNER,(1,-1,1,-1,1,-1,1)))
    assert len(INNER)==7 and all(signs[i]+signs[j]==0 for i,j in zip(INNER,INNER[1:]))
    branches=[[],[]]
    for lobe in (-1,1):
        v=cell(lobe,-R,R)
        y,n,_,_,w,neutral,_,qs,diff=v
        base_odd=D*EPS*Q0*diff/qs
        branches[0].append(phase_cell(lobe,-R,R))
        moved={i:yi+signs.get(i,0)*t for i,yi in y.items()}
        for k,i in enumerate(INNER,1):
            offset=(moved[i]+F(7,4))/K-F(k,8)
            assert offset.absmax()<I.of(F(1,64)).lo
        assert all(moved[i].hi<moved[j].lo for i,j in zip(ORDER,ORDER[1:]))
        dc={j:ZERO for j in ORDER}
        for (i,j),b in EDGES.items():
            s=(signs.get(j,0)-signs.get(i,0))*t
            dc[j]-=F(b,38)*s*(2*(y[j]-y[i])+s)
        coefficient=coeffs(moved)
        right_mid=sum(w[j]*coefficient[j] for j in w)
        right_odd=base_odd+D*EPS*Q0*sum(dc[j]*n[j] for j in (12,13,14))/qs
        branches[1].append((right_mid,right_odd))
    diag=mean(average(branches[0],branches[0]),average(branches[1],branches[1]))
    cross=average(*branches)
    return {'class_contrast_coherent':decimals((diag[0]+cross[0])/(diag[2]+cross[2]),18),
            'class_contrast_mixed':decimals(diag[0]/diag[2],18),
            'identical_densities_per_paired_history':len(INNER)}


def run():
    result = packets()
    result['continuous_window'] = {'u4_radius':'1/64','subdivisions':1024,
                                   'relative_intensity':continuous(1024)}
    assert F(result['continuous_window']['relative_intensity'][0])>0
    result['moving_profile_exact_contrast']='0'
    result['matched_density_control']=matched_densities()
    return result


if __name__=='__main__':
    print(json.dumps(run(), indent=2, sort_keys=True))
