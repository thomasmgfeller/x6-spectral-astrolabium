"""All induced one-helper extensions of the PR 413 midpoint orders. Python 3.10+."""
from pathlib import Path
import csv
from collections import Counter
from fractions import Fraction as F
from hashlib import sha256
from io import StringIO
import argparse
import json
import sys

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT / "basis"))
from intervall import I, S, Empty, Singular, box, point, zero
from ordnungen import COLLAR, EMPTY, POS, DEVICE, LAYERS
from filter import Model, Z, bounds, differentiate, intersect, ordered
from fruehe_uhren import first_projection
from terminal import margin, terms

def source(name, digest):
    raw = (ROOT / "basis" / name).read_bytes()
    assert sha256(raw).hexdigest() == digest
    return json.loads(raw)

def all_ideals(rel):
    order = sorted(range(23), key=lambda i: sum(b == i for a,b in rel))
    ideals = [frozenset()]
    for i in order:
        pred = {a for a,b in rel if b == i}
        ideals += [p | {i} for p in ideals if pred <= p]
    return ideals

def extensions(rel):
    for p in all_ideals(rel):
        if 22 not in p:
            continue
        for start in range(7,12):
            f = tuple(range(start,11))
            if all((i,j) in rel for i in p for j in f):
                yield tuple(sorted(p)), f, rel|{(i,23) for i in p}|{(23,j) for j in f}

class HelperModel(Model):
    def __init__(self, rel):
        self.rel = tuple(sorted(rel))
        self.inc = {i: [] for i in range(24)}
        self.out = {i: [] for i in range(24)}
        for i,j in self.rel:
            length = sum((i,h) in rel and (h,j) in rel for h in range(24))
            k = LAYERS[min(length,4)] - F((i,j) in DEVICE,10**11)
            if k:
                self.inc[j].append((i,k,point(k)))
                if j not in EMPTY:
                    self.out[i].append((j,k,point(k)))
        self.row22 = {j:v for j,v,k in self.out[22]}
        self.tail = tuple(j for i,j in self.rel if i == 23)
        assert all(j in (7,8,9,10) for j in self.tail)

    def force(self, i, time, y, w):
        collar = [(j,k*w[j]) for j,r,k in self.out[i] if j in COLLAR]
        return sum((a*y[j] for j,a in collar),Z) - time*sum((a for j,a in collar),Z)

    def bounded_root(self, j, y):
        """Cauchy's 1+max(|b/a|,|c/a|) bound for Dy=0."""
        inc = self.inc[j]
        a = sum(k for i,k,v in inc)
        if a == 0:
            return None
        m = {i:F(max(abs(y[i].l),abs(y[i].h)),S) for i,_,_ in inc}
        b = 2*sum(abs(k)*m[i] for i,k,v in inc)
        c = 19+sum(abs(k)*m[i]**2 for i,k,v in inc)
        cap = 1+max(b,c)/abs(a)
        return box(-cap,cap)

    def terminal(self, j, y):
        inc = self.inc[j]
        a = sum(r for i,r,k in inc)
        b = sum((k*y[i] for i,r,k in inc),Z)
        if a:
            intersect(y,j,b/point(a))
        else:
            zero(b, f"G{j} terminal")
            # Once H=0 and A=0, the density has no Yj dependence.
            anchor = y[22]
            zero(19+sum((k*(anchor-y[i]).sq() for i,r,k in inc),Z),f"D{j} terminal")

    def interior_projection(self,y):
        # The two matched source rows have common affine dependence on their test clock.
        eps=F(1,10**11)
        d16={0:-8,1:16,2:-9,15:1-eps}
        d19={1:-8,2:16,15:-9,16:1}
        d18={1:-8,2:16,15:-9,16:1-eps,17:1-eps,20:1}
        assert all({i:r for i,r,k in self.inc[j]}==row for j,row in ((16,d16),(18,d18),(19,d19)))
        anchor=point(-1)
        a=y[16]
        core=tuple((i,k) for i,k in d16.items() if i!=15)
        c=19+sum((k*(anchor-y[i]).sq() for i,k in core),Z)
        b=2*sum((k*(anchor-y[i]) for i,k in core),Z)
        t=a-anchor
        intersect(y,15,a-(-(c+t*(b-t))/point(1-eps)).sqrt())
        h=sum((k*y[i] for i,k in d19.items()),Z)
        c=19+sum((k*(anchor-y[i]).sq() for i,k in d19.items()),Z)
        if h.l>0 or h.h<0:
            intersect(y,19,anchor+c/(2*h))
        # D18 - D19(Y18). All three small correction terms are retained.
        slack=point(eps)*(y[18]-y[16]).sq()
        budget=2*h*(y[18]-y[19])+slack
        gaps={}
        for j,k in ((17,1-eps),(20,1)):
            d=y[18]-y[j]
            gaps[j]=point(k)*I(max(0,d.l),d.h).sq()
        for j,k,other in ((17,1-eps,20),(20,1,17)):
            gap=((budget-gaps[other])/point(k)).sqrt()
            intersect(y,j,y[18]-gap)
            intersect(y,18,y[j]+gap)
        if h.l>0:
            intersect(y,18,y[19]+(sum(gaps.values(),Z)-slack)/(2*h))

    def contract_new(self, y, w, rounds):
        for _ in range(rounds):
            before = tuple((a.l,a.h) for a in (*y.values(),*w.values()))
            ordered(self.rel,y)
            for j in (21,23):
                if not self.out[j]:
                    self.terminal(j,y)
            self.interior_projection(y)
            for j in (*POS,23):
                try:
                    self.density(j,y)
                except Empty as exc:
                    raise Empty(f"D{j}") from exc
            # Eliminate w23 between the two free clock equations.
            weight_coeff = self.row22.get(23,0)
            if weight_coeff:
                h = differentiate(self.inc[23],23,y)
                gap = y[23]-y[22]
                force22 = self.force(22,y[22],y,w)
                force23 = self.force(23,y[23],y,w)
                zero(force22*h+point(weight_coeff)*gap*force23, "G22+G23")
            for j in (22,23,17,20,15,14,18,19,16,4,5,6,11,12,13,21):
                try:
                    self.clock(j,y,w)
                except Empty as exc:
                    raise Empty(f"G{j}") from exc
            if before == tuple((a.l,a.h) for a in (*y.values(),*w.values())):
                break

    def prepare(self, pair, side, early):
        y,w = bounds(pair,side)
        y[22] = (y[3]+y[7])/2
        w[23] = box(0,16 if side == "light" else 1)
        force = self.force(22,y[22],y,w)
        c = self.row22.get(23,0)
        if (force.l>0 and c>=0) or (force.h<0 and c<=0):
            raise Empty("G22 Vorzeichen")
        for j,r in early.items():
            intersect(y,j,r)
        y[21] = self.bounded_root(21,y)
        assert y[21] is not None
        if not self.out[21]:
            self.terminal(21,y)
        if self.tail:
            y[23] = I(y[22].l,min(y[i].h for i in self.tail))
        else:
            y[23] = self.bounded_root(23,y)
            if y[23] is None:
                self.terminal(23,y)
                return None
        return y,w

def early_bounds(pair, side, model):
    y,w = bounds(pair, side)
    for j in (4,5,6,11,12,13,14):
        model.density(j,y)
    first_projection(model,y)
    return {j:y[j] for j in (4,5,6,11,12,13,14,15,16,19)}

def refine_terminal(model,y,w,depth):
    model.contract_new(y,w,5)
    if not depth:
        return False
    # Refine actual degrees of freedom in the unbounded-old-field sector.
    # Y16 drives D16 and D19; separate it once Y17 and Y20 have narrowed.
    j=max((16,17,20,18,21),key=lambda i:(y[i].h-y[i].l)*(32 if i==16 else 1))
    for half in y[j].halves():
        child=y.copy()
        child[j]=half
        try:
            if not refine_terminal(model,child,w.copy(),depth-1):
                return False
        except Empty:
            continue
    return True

def projected_boxes(model,pair,side,early,prepared):
    if prepared is not None:
        return prepared
    # H23=0 with A23=0 permits arbitrarily late Y23 in these necessary
    # conditions. The projected polynomial uses no Y23 and no box for it.
    y,w = bounds(pair,side)
    y[22]=(y[3]+y[7])/2
    for j,b in early.items():
        intersect(y,j,b)
    y[21]=model.bounded_root(21,y)
    w[23]=box(0,16 if side=="light" else 1)
    return y,w

def run(depth=6):
    pair = source("Vergleichspaar.json","c75c0c97c1b536d0140d77b4f01d8bfa0a2aab487a1b05a2b58f2ebf23159c2f")
    studies = source("Sonden_auf_N23.json","0e43915b9f8a83491630b3aae99c3b92a03bbf5e6527f256b747d5a5b05a45ae")
    certs=json.loads((ROOT/'Zertifikate.json').read_text())
    used=set()
    base = set(map(tuple,pair['relation']))
    tab = StringIO()
    writer = csv.writer(tab, delimiter='\t', lineterminator='\n')
    writer.writerow(['praeparation','bahnen_von','alte_vergangenheit_23_mit_22','alte_zukunft_23','status','grund'])
    totals = {}
    for side, records in studies.items():
        bypast = {}
        for r in records:
            assert r['order']['future'] == list(range(7,11))
            bypast.setdefault(tuple(r['order']['past']),[]).append(r['start'])
        for past,starts in bypast.items():
            rel = base | {(i,22) for i in past} | {(22,j) for j in range(7,11)}
            early = early_bounds(pair,side,HelperModel(rel))
            previous_model = HelperModel(rel)
            z,_ = bounds(pair,side)
            z.update(early)
            z[22]=(z[3]+z[7])/2
            d22=19+sum((k*(z[22]-z[i]).sq() for i,r,k in previous_model.inc[22]),Z)
            assert d22.h<0
            positive22=[str(F(v,S)) for v in (d22.l,d22.h)]
            positives = Counter()
            terminal_count=0
            margins=[]
            reasons = Counter()
            for p,f,ext in extensions(rel):
                assert all((i,j) in ext for i,k in ext for k2,j in ext if k2==k)
                terminal_count += not f
                model = HelperModel(ext)
                assert all([(i,r) for i,r,k in model.inc[j]]==[(i,r) for i,r,k in previous_model.inc[j]] for j in range(23) if j not in COLLAR)
                try:
                    prepared = model.prepare(pair,side,early)
                    if prepared is None:
                        reason = "terminal, unbeschraenkte Uhr"
                    else:
                        y,w = prepared
                        model.contract_new(y,w,12)
                        if not model.tail and refine_terminal(model,y,w,depth):
                            raise Empty("terminale Intervallueberdeckung")
                        reason = "Intervalle unentschieden"
                    key=side+"_"+str(starts[0])+"_"+",".join(map(str,p))
                    if key in certs:
                        assert not f and key not in used
                        # Subdivision operates on copies. Rebuild the exact
                        # original enclosure on which the certificate was discovered.
                        original=model.prepare(pair,side,early)
                        if original is not None:
                            model.contract_new(*original,12)
                        yy,ww=projected_boxes(model,pair,side,early,original)
                        bx,rows=terms(model,yy,ww)
                        separation=margin(bx,rows,certs[key])
                        assert separation>0,key
                        used.add(key)
                        margins.append(separation)
                        raise Empty("rationales Terminalzertifikat")
                    status = "OFFEN"
                except Empty as exc:
                    status,reason = "AUSGESCHLOSSEN",str(exc)
                positives[status] += 1
                reasons[reason] += 1
                writer.writerow([side,','.join(map(str,starts)),','.join(map(str,p)),','.join(map(str,f)),status,reason])
            totals[side+'_'+','.join(map(str,starts))] = dict(
                cases=dict(positives),rules=dict(reasons),old_past22=past,
                positive_probe_D22=positive22, terminal=terminal_count,
                nonterminal=sum(positives.values())-terminal_count,
                minimum_certificate_margin=str(min(margins)))
    assert used==set(certs) and len(certs)==12
    return tab.getvalue(), json.dumps(totals,ensure_ascii=False,indent=2,sort_keys=True)+'\n'

if __name__ == '__main__':
    if not __debug__:
        raise RuntimeError('Ohne -O ausführen')
    parser = argparse.ArgumentParser()
    parser.add_argument('--ausgabe',action='store_true')
    args=parser.parse_args()
    for name,content in zip(('Fallregister.tsv','Ergebnisse.json'),run()):
        path = ROOT/name
        if args.ausgabe:
            path.write_bytes(content.encode())
        else:
            assert path.read_bytes()==content.encode(),name
    print('Alle induzierten Anbindungen je Halbsondenordnung geprüft.')
