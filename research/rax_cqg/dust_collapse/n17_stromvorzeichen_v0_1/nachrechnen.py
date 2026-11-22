"""Certified conditional N17 comparison. Python 3.9+, standard library."""
from fractions import Fraction as Q
from hashlib import sha256
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parent
sys.path.insert(0,str(ROOT/'basis'))
import pakettest as n16
import skalar

old = n16.old
M, H = n16.MID, n16.H
BAND = old.box(M,H)
Y16 = n16.YN + 1
NODES = tuple(range(17))


def weights(relation):
    out = {}
    for a,b in relation:
        depth = sum((a,c) in relation and (c,b) in relation for c in NODES)
        if depth < 4:
            out[a,b] = n16.LAYERS[depth]
    return out


def geometry(ideal):
    past = old.ORDER | {(i,15) for i in ideal}
    total = past | {(i,16) for i in range(16)}
    full = weights(total)
    previous = dict(old.B)
    previous = {edge:w for edge,w in previous.items() if w}
    previous.update({(i,15):w for i,w in n16.new_edges(ideal).items()})
    assert previous == {edge:w for edge,w in full.items() if edge[1]<16}
    incoming = {i:w for (i,j),w in full.items() if j==16}
    # The four earlier future-collar events shield all old inner and input clocks.
    assert set(incoming) <= set(old.F) | {15}
    assert incoming[15] == 1
    return past, full, incoming


def slope_range(incoming, clock, uncertainties, target):
    terms = [old.sc(w,old.square(old.box(clock[i]-target,uncertainties.get(i,0))))
             for i,w in incoming.items()]
    return old.add(old.box(-Q(1,2)), old.sc(-Q(1,38),old.total(terms)))


def relative_slope_span(incoming, clock, target):
    # Only Y8,Y9,Y10 vary in z. This is |D(z)-D(z0)|, not a diameter.
    return sum(abs(w)*(2*abs(clock[i]-target)*H+H*H)/38
               for i,w in incoming.items() if i in old.F[1:])


def schur_scalar(ideal, incoming):
    old_n, old_weights = skalar.geometry(ideal)
    assert old_n == 16
    previous = skalar.framed_hessian(old_n,old_weights)
    g = [row+[Q(0)] for row in previous] + [[Q(0)]*17]
    # Convert differences q_i-q16 to the frozen H3-frame. Only the old F and
    # q15 can contribute, including the old future-frame direction at column 14.
    for i,b in incoming.items():
        u = [Q(0)]*17
        u[16] = -1
        if i == 15:
            u[15] = 1
        else:
            j = old.F.index(i)
            if j < 3:
                u[3+j] = 1
            u[14] = (0,16,32,46)[j]
        for a in range(17):
            for c in range(17):
                g[a][c] -= Q(b,2)*u[a]*u[c]
    inside = list(range(6,15))
    outside = list(range(6))+[15,16]
    det, inv = skalar.det_inverse(skalar.block(g,inside,inside))
    links = skalar.block(g,outside,inside)
    def sandwich(l,m,r):
        return skalar.multiply(skalar.multiply(l,m),r)
    part = sandwich(links, inv, skalar.transpose(links))
    k = [[g[i][j]-part[a][c] for c,j in enumerate(outside)] for a,i in enumerate(outside)]
    both = range(6)
    a = skalar.block(k,both,both)
    c = skalar.block(k,both,[6,7])
    d = skalar.block(k,[6,7],[6,7])
    # Real Gaussian damping on input and coherently projected old output.
    a2 = skalar.multiply(a,a)
    real_det, inv = skalar.det_inverse([[v+int(i==j) for j,v in enumerate(row)]
                                        for i,row in enumerate(a2)])
    real = sandwich(skalar.transpose(c),inv,c)
    correction = sandwich(skalar.transpose(c),skalar.multiply(a,inv),c)
    phase = [[d[i][j]-correction[i][j] for j in range(2)] for i in range(2)]
    assert det and real_det > 0 and real[0][0] >= 0 and real[1][1] >= 0
    assert real[0][0]*real[1][1] >= real[0][1]**2
    # At final scalar q16=0 integrate exp[-beta*(a-i b)*q15^2/2] on [-1,1].
    # Rotating by the middle of the phase arc makes its real part positive.
    assert abs(phase[0][0]) < Q(5,2)  # beta/2 < 1; half-arc below 5/4 radians.
    return dict(hidden_det=det, old_gaussian_det_I_plus_A2=real_det,
                real_quadratic_over_beta=real, phase_quadratic_over_beta=phase,
                nonzero_at_final_scalar_zero=True)


def packets(name, ideal, incoming, deformation):
    neutral, family = n16.packet_family(deformation)
    neutral[15] = n16.YN
    first = n16.new_edges(ideal)
    reference = n16.slope(first,neutral)
    old_ref = -n16.old_coefficient(neutral)[7]/2
    widths = {i:H for i in old.F[1:]}
    final_range = slope_range(incoming,neutral,widths,Y16)
    eta = H*relative_slope_span(incoming,neutral,Y16)
    assert 0 <= eta < 1
    info, all_effects, retained_error = {}, Q(0), Q(0)
    slopes = {}
    for sign,center in family.items():
        y = dict(center[0]); y[15] = n16.YN
        region = old.whole_cell(center,old_ref)
        e = n16.budget(first,center,region)['amplitudenfehler_je_paketmass']
        # No final phase uses a narrow hidden axis. The old pointwise error
        # bound therefore survives all the new normalized coherent integrals.
        first_range = slope_range(first,y,widths,n16.YN)
        enclosure = old.total([region['staubphase'],old.mul(BAND,first_range),
                               old.mul(BAND,final_range)])
        length = enclosure[1]-enclosure[0]
        c = 1-length**2/8
        assert Q(99,100) < c <= 1 and e<c
        # Divide the exact and centered output by their midpoint amplitudes.
        # They agree at the midpoint; their modulation error is O(eta*e).
        ratio_error = eta*e*(1+1/c)/(c-e)
        centered_ratio_norm = 1-eta/c
        distance = 2*ratio_error/centered_ratio_norm
        all_effects += distance
        retained_error += 2*e/c
        slopes[sign] = n16.slope(first,y)
        current16 = old.add(region['p'],n16.input_correction(first,y))
        info[sign] = dict(pointwise_packet_error=e,center_modulus_lower=c,
                          anchored_error=ratio_error,trace_distance_bound=distance,
                          input_current_N17=current16)
    yp,wp=family['positiv']; yn,wn=family['negativ']
    assert [i for i in yp if yp[i]!=yn[i]] == [6]
    assert all(wp[i]==wn[i] for i in old.P+old.F)
    assert all(old.B.get((6,i),0)==0 for i in old.F[1:])
    # The only old z-dependent relative phase before closure is on w7.
    # w7's centered slope is independent of the others. At the first birth
    # the two slopes are constants (unshielded) or an identical function (full ideal).
    if set(first)&set(old.F):
        assert set(first)==set(old.F) and slopes['positiv']==slopes['negativ']
        kept = old.box(0,retained_error)
    else:
        delta = slopes['positiv']-slopes['negativ']
        cubic = sum(abs(H*(value-reference))**3 for value in slopes.values())/12
        kept = old.box(H*delta/2,retained_error+cubic)
        assert kept[0]*kept[1]>0
    return dict(branches=info,eta=eta,final_slope_range=final_range,
                closed_all_binary_effects_upper=all_effects,
                retained_N16_detector_signed_interval=kept,
                retained_N16_current_signs=[1 if info[s]['input_current_N17'][0]>0 else
                                            -1 if info[s]['input_current_N17'][1]<0 else 0
                                            for s in ('positiv','negativ')])


def run():
    entry = json.loads((ROOT/'quellen.json').read_text())
    for name,digest in entry['sha256'].items():
        assert sha256((ROOT/'basis'/name).read_bytes()).hexdigest()==digest, name
    assert sha256((ROOT/'pruefvertrag.json').read_bytes()).hexdigest()==(
        ROOT/'pruefvertrag.sha256').read_text().split()[0]
    # Reproduce the frozen N16 whole-packet results before the new comparison.
    legacy=json.loads(json.dumps(n16.run(),default=str))
    assert legacy==json.loads((ROOT/'basis/ergebnis.json').read_text())
    result={}
    for name,ideal in n16.CASES.items():
        past, full, incoming=geometry(ideal)
        assert all((i,16) not in full for i in old.P)
        result[name]=dict(incoming_weights=incoming, link_maxima_before_cap=[
            i for i in range(16) if all((i,j) not in past for j in range(16))],
            input_current_change_N17_minus_N16=0, scalar=schur_scalar(ideal,incoming),
            original=packets(name,ideal,incoming,old.STEP),
            transfer=packets(name,ideal,incoming,old.STEP/2))
    return result


if __name__=='__main__':
    if not __debug__: raise RuntimeError('Run without -O')
    print(json.dumps(run(),indent=2,default=str,sort_keys=True))
