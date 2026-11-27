"""Outward interval constraints for the coupled N23 density and clock equations."""
from intervall import I, Empty, box, point
from ordnungen import COLLAR, EMPTY, POS, LOW, HIGH, Q, coefficients

FREE = (4, 5, 6, *range(11,23))
Z = point(0)

def hull(boxes):
    if not boxes:
        raise Empty("keine kausale Wurzel")
    return I(min(v.l for v in boxes), max(v.h for v in boxes))

def intersect(vector, j, value):
    new = vector[j].cut(value)
    changed = new.l != vector[j].l or new.h != vector[j].h
    vector[j] = new
    return changed

def bounds(pair,side):
    row = pair[side]
    y = {j:box(*row["clock_box"][j]) for j in COLLAR}
    amp = 16 if side == "light" else 1
    w = {j:box(*row["weight_box"][j])*amp for j in COLLAR}
    y[22] = y[3] + box(LOW,HIGH)*(y[7]-y[3])
    for j in FREE:
        if j not in (21,22):
            y[j] = I(y[0].l,y[7].h)
        w[j] = Z if j in EMPTY else box(0,amp)
    return y,w

def ordered(rel,y):
    low, high = {}, {}
    for i,j in rel:
        if i not in y or j not in y:
            continue
        if y[i].l >= y[j].h:
            raise Empty("Kausalordnung")
        low[j] = max(low.get(j,y[j].l), y[i].l)
        high[i] = min(high.get(i,y[i].h), y[j].h)
    for i in y:
        y[i] = I(low.get(i,y[i].l),high.get(i,y[i].h))

def causal_roots(eq, yc, y):
    # Expand about the midpoint for conditioning. A is the exact leading coefficient.
    anchor = I((yc.l+yc.h)//2, (yc.l+yc.h)//2)
    A = sum(r for i,r,k in eq)
    B = 2*sum((k*(anchor-y[i]) for i,r,k in eq),Z)
    C = 19+sum((k*(anchor-y[i]).sq() for i,r,k in eq),Z)
    if A == 0:
        if B.l <= 0 <= B.h:
            return yc
        return yc.cut(anchor-C/B)
    a = point(A)
    disc = (B.sq()-4*a*C).sqrt()
    possible = []
    for numerator in (-B-disc,-B+disc):
        try:
            possible.append(yc.cut(anchor+numerator/(2*a)))
        except Empty:
            continue
    return hull(possible)

def differentiate(eq, j, y):
    # Sum k*(Yj-Yi) by collecting the coefficient of the shared Yj.
    return point(sum(r for i,r,k in eq))*y[j]-sum((k*y[i] for i,r,k in eq),Z)

class Model:
    def __init__(self, rel):
        self.rel = tuple(sorted(rel))
        coeff = coefficients(rel)
        self.inc = {j:[] for j in range(23)}
        self.out = {j:[] for j in range(23)}
        for (i,j),value in sorted(coeff.items()):
            k = point(value)
            self.inc[j].append((i,value,k))
            if j not in EMPTY:
                self.out[i].append((j,value,k))
        assert not self.out[21]
        assert all((0,j) in rel and (j,7) in rel for j in FREE if j not in (21,22))
        eq = self.inc[21]
        self.terminal_sum = sum(r for _,r,_ in eq)
        assert self.terminal_sum != 0

    def terminal(self,y):
        return sum((point(r/self.terminal_sum)*y[i] for i,r,k in self.inc[21]),Z)

    def density(self,j,y):
        eq = self.inc[j]
        y[j] = causal_roots(eq,y[j],y)
        terms = []
        for i,r,k in eq:
            dy = y[j]-y[i]
            if dy.h <= 0:
                raise Empty("Kausalordnung")
            terms.append(k*I(max(0,dy.l),dy.h).sq())
        total = 19+sum(terms,Z)
        if total.l>0 or total.h<0:
            raise Empty("Dichtevariation")
        for idx,(i,r,k) in enumerate(eq):
            if i in COLLAR:
                continue
            # Remove the selected term by its own endpoints (not interval subtraction).
            other = I(total.l-terms[idx].l,total.h-terms[idx].h)
            gap = (-other/k).sqrt()
            intersect(y,i,y[j]-gap)
            intersect(y,j,y[i]+gap)

    def clock(self,j,y,w):
        eq = [(n,k*(y[n]-y[j])) for n,r,k in self.out[j]]
        if j not in EMPTY:
            eq.append((j,-differentiate(self.inc[j],j,y)))
        terms = [v*w[n] for n,v in eq]
        total = sum(terms,Z)
        if total.l>0 or total.h<0:
            raise Empty("Uhrvariation")
        # All nonzero receiver weights are strictly positive, including the collar.
        if eq and (all(v.l>=0 for n,v in eq) and any(v.l>0 for n,v in eq) or
                   all(v.h<=0 for n,v in eq) and any(v.h<0 for n,v in eq)):
            raise Empty("gleichgerichtete Impulse")
        for idx,(n,v) in enumerate(eq):
            if n in COLLAR or v.l<=0<=v.h:
                continue
            other=I(total.l-terms[idx].l,total.h-terms[idx].h)
            intersect(w,n,-other/v)
            if w[n].h<=0:
                raise Empty("positives Gewicht")

    def screen(self,pair,side,iterations=6):
        y,w=bounds(pair,side)
        y[21]=self.terminal(y)
        return self.contract(y,w,iterations)

    def contract(self,y,w,iterations):
        for _ in range(iterations):
            previous=tuple((v.l,v.h) for v in (*y.values(),*w.values()))
            ordered(self.rel,y)
            intersect(y,21,self.terminal(y))
            for j in POS:
                try:
                    self.density(j,y)
                except Empty as e:
                    raise Empty(f"D{j}: {e}") from None
            for j in (22,17,20,15,14,18,19,16,4,5,6,11,12,13,21):
                try:
                    self.clock(j,y,w)
                except Empty as e:
                    raise Empty(f"G{j}: {e}") from None
            if previous==tuple((v.l,v.h) for v in (*y.values(),*w.values())):
                break
        return y,w

def probe_sign(future,coeff,y,w):
    # The collar sum is affine in z. Collect the shared probe clock exactly once.
    a=sum((coeff[j]*w[j]*y[j] for j in future if j in COLLAR),Z)
    b=sum((coeff[j]*w[j] for j in future if j in COLLAR),Z)
    fixed=a-b*y[22]
    active=[coeff[j] for j in future if j in POS and coeff[j]]
    if not active and (fixed.l>0 or fixed.h<0):
        return True
    if active and ((fixed.l>=0 and min(active)>0) or (fixed.h<=0 and max(active)<0)):
        return True
    return False
