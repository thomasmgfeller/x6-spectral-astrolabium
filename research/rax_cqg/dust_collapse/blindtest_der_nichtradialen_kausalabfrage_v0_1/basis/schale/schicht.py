"""Necessary density equation for any positive new event on an equal-clock layer."""
from fractions import Fraction as F
from erweiterung import OLD, R, B, INNER, PAST, FUTURE, SCALE, Box, box, coeff, serial, strictly_ordered

def inside_layer(e):
    # Enumerate old causal ideals directly by closing each subset; distinct ideals
    # include empty and all-old. An arbitrary common-clock layer is an antichain.
    ideals=set()
    for mask in range(1<<15):
        s={i for i in OLD if mask & (1<<i)}
        ideals.add(tuple(sorted(s | {u for u,v in R if v in s})))
    rows=[];unresolved=[]
    for ideal in sorted(ideals):
        p=set(ideal)
        r={(i,j) for i,j in R if j in p}|{(i,15) for i in p}
        h=coeff(r)
        y={i:box(i-5) for i in PAST+FUTURE if i in p}
        if 3 in p:y[3]=e-2
        variable=[j for j in INNER if j in p]+[15]
        def walk(k,clock):
            if strictly_ordered(clock,r)=='no':return
            if k==len(variable):
                rows.append({'past':list(ideal),'relative_time':serial((clock[15]-(e-2))/(4-e))})
                return
            j=variable[k]
            incoming=[(i,b) for (i,v),b in h.items() if v==j]
            # Absolute-coordinate coefficients for degree*(Y_j)^2 - 2*s*Y_j + c = 0.
            degree=sum(b for _,b in incoming)
            s=sum((b*clock[i] for i,b in incoming),box(0))
            c=19+sum((b*clock[i].square() for i,b in incoming),box(0))
            if degree:
                disc=s.square()-degree*c
                if disc.hi<0:return
                roots=[(s+sgn*disc.sqrt_nonnegative_part())/degree for sgn in (-1,1)]
            elif s.lo>0 or s.hi<0:roots=[c/(2*s)]
            else:
                if s.lo==s.hi==0 and (c.lo>0 or c.hi<0):return
                unresolved.append([list(ideal),j]);return
            for v in roots:walk(k+1,{**clock,j:v})
        walk(0,y)
    return {'old_ideals':len(ideals),'candidates':rows,'unresolved':unresolved}
