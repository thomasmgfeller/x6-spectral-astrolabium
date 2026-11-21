"""Independent action oracle, exact rational source acquisition, and counterpair."""
from fractions import Fraction as Q
from hashlib import sha256
from pathlib import Path
from random import Random
import json
import sys

HERE = Path(__file__).resolve().parent
sys.path.insert(0,str(HERE/'vorarbeit'))
import gegenprobe as direct
import randquelle as prior
from rueckrechnung import initial_readout
from inversion import (P,F,SEAM,INNER,BY_DEPTH,BY_SUCCESSORS,from_p,to_f,
                       within_chain,clock_only,clock6_from_seam,clocks_from_future)

HIDDEN = (4,6,12,13,14)


def admissible(y,w):
    e = y[3]+2
    dur = 4-e
    u = {j:(y[j]+2-e)/dur for j in INNER}
    for j in INNER:
        assert abs(u[j]-direct.ref.CENTER[j]) < Q(1,64)
    fractions = dict.fromkeys(INNER,Q(0))
    for chain in direct.CHAINS:
        ends = [0] + [(u[a]+u[b])/2 for a,b in zip(chain,chain[1:])] + [1]
        for j,l,r in zip(chain,ends,ends[1:]):
            fractions[j] += (r-l)/len(direct.CHAINS)
    for j in INNER:
        assert fractions[j]*Q(99,100) < 4*w[j]/dur < fractions[j]*Q(101,100)
    for i,j in direct.REL:
        assert y[i] < y[j]


def read(y,w,h,k):
    """Only entries returned by this function cross the instrument boundary."""
    def clock(axes):
        return direct.response(y,w,axes,h)
    def rho(f):
        a,b = w.copy(),w.copy()
        a[f] += k
        b[f] -= k
        return (direct.action(y,a)-direct.action(y,b))/(2*k)
    def at(yy):
        return direct.action(yy,w)
    seam = {s:clock((s,)) for s in SEAM}
    # mixed_response's wrapper sees all fixed clocks only to evaluate the oracle.
    early = Q(19,8)*prior.mixed_response(at,y,h,k,second=(1,0,0,0))
    total = prior.visible_sum(at,y,h,k)
    return {
        'y':{j:y[j] for j in P+SEAM+F},'w':{j:w[j] for j in SEAM+F},
        'E_F':{j:clock((j,))[0] for j in F[1:]},
        'D_F':{j:rho(j) for j in (7,10)},'seam':seam,
        'total':total,'early':early
    }


def both(data):
    y,w,ef,seam = (data[k] for k in ('y','w','E_F','seam'))
    # Give the future decoder only future data and the two seam coordinates.
    clock_y = {i:y[i] for i in SEAM+F}
    clock_w = {i:w[i] for i in F}
    hidden = clocks_from_future(clock_y,clock_w,ef,data['D_F'])
    complete = y|hidden
    a,_ = initial_readout(complete,w,data['total'],seam[5][0],seam[11][0],curvature11=seam[11][1])
    b,partial,masses = clock_only(y,w,ef,data['total'],data['early'],*seam[5],seam[11][1])
    prediction = partial | {6:clock6_from_seam(y|partial,w|masses,seam[11][0])}
    return (a,hidden),(b,prediction),masses


def score(y,w,h,k):
    admissible(y,w)
    data = read(y,w,h,k)
    a,b,masses = both(data)
    # Targets are evaluated after both predictions, independently via the
    # unexpanded action and direct fields. No incoming slope enters either route.
    target = -direct.response(y,w,P,h)[0]
    assert a==b==(target,{i:y[i] for i in HIDDEN})
    assert masses == {j:w[j] for j in (12,13,14)}
    assert data['early'] == w[4]+w[6] and data['total']==sum(w[j] for j in INNER)
    return target


def equalize_action(y,w,yy,ww):
    def coefficient(j):
        return 1+sum(b*(yy[i]-yy[j])**2 for i,t,b in direct.EDGES if t==j)/19
    difference = coefficient(4)-coefficient(6)
    transfer = 2*(direct.action(yy,ww)-direct.action(y,w))/difference
    ww[4] += transfer
    ww[6] -= transfer
    assert direct.action(yy,ww) == direct.action(y,w)
    return transfer


def polynomial_values(y,w,h,k):
    """Unisolvent evaluations for five clock sources and three density sources."""
    from itertools import combinations
    axes = SEAM + F[1:]
    clock_offsets = [()] + [(a,)*n for a in axes for n in (1,2)] + list(combinations(axes,2))
    values = []
    for f in (None,)+F[1:]:
        densities = w.copy()
        if f is not None:
            densities[f] += k
        for offsets in clock_offsets:
            yy = list(y)
            for a in offsets:
                yy[a] += h
            values.append(direct.action(yy,densities))
    assert len(values) == 84
    return values


def counterpair(h,k,match_action=False):
    y,(wl,wr) = direct.sample(Random(0),'ohne_gesamtinformation',center=True)
    w = [(u+v)/2 for u,v in zip(wl,wr)]
    assert -direct.response(y,w,P)[0] == 0
    q = Q(1,2**24 if match_action else 2**20)
    results,probes = [],[]
    transfers, signatures = [],[]
    for s in (1,-1):
        step = s*q
        yy,ww = list(y),list(w)
        ww[4] -= 10*step
        ww[12] += 9*step
        ww[13] += step
        yy[6] += 9*step*(y[13]-y[12])/w[11]
        if match_action:
            transfers.append(equalize_action(y,w,yy,ww))
            signatures.append(polynomial_values(yy,ww,h,k))
        results.append(score(yy,ww,h,k))
        probes.append(read(yy,ww,h,k))
    a,b = probes
    for key in ('y','w','E_F','seam','total'):
        assert a[key] == b[key]
    assert a['D_F'][10]==b['D_F'][10] and a['D_F'][7]!=b['D_F'][7]
    assert a['early']-b['early']==-20*q
    # Verify the exact coefficient of the observed opposite charges.
    def g(j):
        return sum(from_p(i,j)*(y[i]-y[j]) for i in P)
    slope = (-10*g(4)+9*g(12)+g(13))/19
    assert results == [slope*q,-slope*q] and results[0] != 0
    report = {'q':q,'p_fuer_plus_und_minus_q':results,'p_pro_q':slope,
            'delta_W_frueh':a['early']-b['early'],
            'delta_D7':a['D_F'][7]-b['D_F'][7],
            'delta_D10':a['D_F'][10]-b['D_F'][10],
            'identisch':['sichtbare Felder','E8,E9,E10','E5,H5,E11,H11','W_gesamt']}
    if match_action:
        assert signatures[0] == signatures[1]
        report.update({'transfer_6_nach_4':transfers, 'unisolvente_werte':len(signatures[0]),
                       'gleiche_vollstaendige_wirkungsquellen':{'uhren':SEAM+F[1:],'dichten':F[1:]}})
    return report


def structure():
    edge = {(i,j):b for i,j,b in direct.EDGES}
    for j in INNER:
        assert all(from_p(i,j) == edge.get((i,j),0) for i in P)
        assert all(to_f(j,f) == edge.get((j,f),0) for f in F)
        assert all(within_chain(i,j)==edge.get((i,j),0) for i in INNER)
    assert all((p,f) not in edge for p in P for f in F)
    # Each independent target tube has half width 1/64 in normalized clock time.
    dur_min = 4-Q(3,8)
    gap = dur_min*(Q(1,5)-Q(2,64))
    distance = dur_min*(1-Q(1,5)-Q(1,64))
    prefactor = Q(99,100)*Q(1,4)*dur_min
    min_w14 = prefactor*(Q(1,2)-Q(1,64))/2
    min_w11 = prefactor*(Q(2,5)-Q(2,64))/4
    assert gap == Q(783,1280) and distance > 0
    return {'uhrtrennung_Y13_minus_Y14_mindestens':gap,
            'abstand_Y7_minus_Y6_mindestens':distance,
            'W14_untere_schranke':min_w14,'W11_untere_schranke':min_w11,
            'innere_ziele_nach_vorgaengerzahl':BY_DEPTH,
            'innere_quellen_nach_nachfolgerzahl':BY_SUCCESSORS}


def run():
    contract = (HERE/'pruefvertrag.json').read_bytes()
    assert sha256(contract).hexdigest()==(HERE/'pruefvertrag.sha256').read_text().split()[0]
    plan = json.loads(contract)
    settings = plan['daten']
    h,k = map(Q,plan['schritte'])
    rng = Random(settings['startwert'])
    signs = {'positiv':0,'negativ':0,'null':0}
    cases = []
    for name in direct.NAMES:
        for i in range(settings['paare_pro_familie']):
            y,branches = direct.sample(rng,name,center=i==0)
            cases.extend((y,w) for w in branches)
    for _ in range(settings['weitere_breite_felder']):
        y,(w,_) = direct.sample(rng,'allgemein',broad=True)
        cases.append((y,w))
    for y,w in cases:
        p = score(y,w,h,k)
        signs['positiv' if p>0 else 'negativ' if p<0 else 'null'] += 1
    # Repeat with much narrower probes on the known centers (separate scale control).
    for name in direct.NAMES:
        y,branches = direct.sample(Random(1),name,center=True)
        for w in branches:
            assert read(y,w,h,k)==read(y,w,Q(1,2**26),Q(1,2**27))
    return {'typ':375841,'struktur':structure(),'rationale_belegungen_je_weg':len(cases),
            'einzelne_verborgene_uhrwerte_je_weg':5*len(cases),
            'vorzeichen':signs,'skalenkontrollen':8,'gegenpaar':counterpair(h,k),
            'ergaenzung_gegenpaar_gleicher_wirkung':counterpair(h,k,match_action=True),
            'physikalisches_messinstrument_und_paarung':'HOLD'}

if __name__=='__main__':
    if not __debug__:
        raise RuntimeError('Ohne -O ausführen.')
    print(json.dumps(run(),indent=2,default=str,ensure_ascii=False))
