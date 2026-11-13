#!/usr/bin/env python3
"""Exact order filtration and accepted-class interference checks; no quadrature."""
from collections import Counter
from decimal import Decimal, localcontext, ROUND_FLOOR, ROUND_CEILING
from fractions import Fraction as F
from itertools import combinations, permutations, product
from pathlib import Path
import hashlib
import json

ROOT = Path(__file__).resolve().parent
SOURCE = ROOT / 'sources'
pilot = json.loads((SOURCE/'pilot.json').read_text())
assert hashlib.sha256((SOURCE/'pilot.json').read_bytes()).hexdigest() == '442cc81227921135ccb046cdc238f8c2d9cae88f2082614490e59cfceba77ba3'
assert hashlib.sha256((SOURCE/'result_64.json').read_bytes()).hexdigest() == '5085b0f3d5bf2d9a70a184853c9d236fc2d41d7d2f7003b9c57ad980bdb34eae'
assert hashlib.sha256((SOURCE/'r_records_results.json').read_bytes()).hexdigest() == 'bcc2ea755f13f7ccebe4303bb05ccefbb8b243167c5246cab746e511d2a21313'
N = tuple(range(6))
G = []
for a,r in product(permutations((1,2)), permutations((4,5))):
    G.append({0:0,1:a[0],2:a[1],3:3,4:r[0],5:r[1]})

def closure(edges):
    e=set(map(tuple,edges))
    while True:
        new=e|{(x,z) for x,y in e for y2,z in e if y==y2}
        if new==e:return frozenset(e)
        e=new

def subsets(nodes):
    return [frozenset(c) for k in range(len(nodes)+1) for c in combinations(nodes,k)]

def profile(e):
    past={x:{y for y in N if (y,x) in e} for x in N}
    future={x:{y for y in N if (x,y) in e} for x in N}
    interval=Counter(len(future[x]&past[y]) for x,y in e)
    height={x:0 for x in N}
    for x in N:
        height[x]=max([height[y]+1 for y in past[x]] or [0])
    antichains=[s for s in subsets(N) if not any((x,y) in e for x in s for y in s)]
    maximal=[s for s in antichains if not any(s<t for t in antichains)]
    ideals=[s for s in subsets(N) if all(past[x]<=s for x in s)]
    filtration=[frozenset(x for x in N if len(past[x])<=k) for k in range(5)]
    for s in filtration:assert s in ideals
    for k in range(5):assert frozenset(x for x in N if len(past[x])==k) in antichains
    lin=sum(all(p.index(x)<p.index(y) for x,y in e) for p in permutations(N))
    return {
      'relation_count':len(e),'interval_histogram':[interval[k] for k in range(4)],
      'F4':6-sum(b*interval[k] for k,b in enumerate((1,-9,16,-8))),
      'height_layers':[sum(h==k for h in height.values()) for k in range(4)],
      'height_in_links':max(height.values()), 'max_antichain_size':max(map(len,antichains)),
      'maximal_antichains':[sorted(s) for s in maximal],
      'ideals_by_size':[sum(len(s)==k for s in ideals) for k in range(7)],
      'past_cardinality_layers':[sum(len(past[x])==k for x in N) for k in range(5)],
      'past_cardinality_filtration_sizes':[len(s) for s in filtration],
      'past_cardinality_filtration_sets':[sorted(s) for s in filtration],
      'inner_A_ancestor_count':len(past[3]&{1,2}),
      'R_past_cardinalities_sorted':sorted(len(past[x]) for x in (4,5)),
      'P_to_R_longest_chain_links_sorted':sorted(height[x] for x in (4,5)),
      'P_to_R_interval_cardinalities_sorted':sorted(len(future[0]&past[x]) for x in (4,5)),
      'linear_extensions':lin,'strictly_order_preserving_clock_box_fraction':str(F(lin,720)),
    }

families=[]
for c in (1,2):
    e=closure(pilot['history_family']['common_generating_relations']+pilot['history_family'][f'class_{c}_added_relations'])
    orbit={frozenset((p[x],p[y]) for x,y in e) for p in G}
    families.append(sorted(orbit,key=lambda x:sorted(x)))
assert list(map(len,families))==[4,2]
assert not set(families[0])&set(families[1])
all_e=[e for f in families for e in f]
for roles in [{4,5},{0,1,2,4,5}]:
    assert len({frozenset((x,y) for x,y in e if x in roles and y in roles) for e in all_e})==1
all_profiles=[]
for c,family in enumerate(families,1):
    for e in family:
        d=profile(e);assert d['inner_A_ancestor_count']==c
        assert d['height_layers']==[1,2,2,1]
        assert d['R_past_cardinalities_sorted']==[3,4]
        assert d['P_to_R_longest_chain_links_sorted']==[2,3]
        assert d['P_to_R_interval_cardinalities_sorted']==[2,3]
        assert d['past_cardinality_filtration_sizes']==([1,3,4,5,6] if c==1 else [1,3,3,5,6])
        assert d['F4']==(9 if c==1 else -7)
        d['class']=c;d['relations']=sorted(e);all_profiles.append(d)

# Rational rectangular interval operations, using only inherited enclosures.
def I(x):return (F(x[0]),F(x[1])) if isinstance(x,list) else (F(x),F(x))
def plus(a,b):return a[0]+b[0],a[1]+b[1]
def minus(a,b):return a[0]-b[1],a[1]-b[0]
def mul(a,b):
    p=[x*y for x in a for y in b];return min(p),max(p)
def cx(d):return I(d['real']),I(d['imag'])
def cplus(a,b):return plus(a[0],b[0]),plus(a[1],b[1])
def conj(a):return a[0],(-a[1][1],-a[1][0])
def cmul(a,b):return minus(mul(a[0],b[0]),mul(a[1],b[1])),plus(mul(a[0],b[1]),mul(a[1],b[0]))
def scale(a,n):return mul(a,I(n))
def dec(x,rounding):
    with localcontext() as c:
        c.prec=35;c.rounding=rounding
        return str(Decimal(x.numerator)/Decimal(x.denominator))
def enc(a):return [dec(a[0],ROUND_FLOOR),dec(a[1],ROUND_CEILING)]
amps=json.loads((SOURCE/'result_64.json').read_text())['analysis']['amplitudes']
mom=json.loads((SOURCE/'r_records_results.json').read_text())['eta_by_class']
eta=[cx(mom[str(c)]) for c in (1,2)]
factor=cplus((I(1),I(0)),cmul(eta[0],conj(eta[1])))
decoherence=[]
for name,row in zip(['g0','gplus'],amps):
    a=list(map(cx,row));s=(I(0),I(0))
    for k in (0,1):s=cplus(s,cmul(a[k],conj(a[k+2])))
    d=cmul(factor,s);d=(scale(d[0],F(1,1024**2)),scale(d[1],F(1,1024**2)))
    assert d[0][1]<0, 'Accepted class branches unexpectedly weakly decoherent'
    decoherence.append({'input':name,'gain':'1/1024','accepted_D12_real':enc(d[0]),'accepted_D12_imag':enc(d[1]),'additivity_defect_2ReD12':enc(scale(d[0],2)),'weakly_decoherent':False,
      'meaning':'K_c is the class-restricted accepted map into (f0/f2) x (atom/positive); this is not a derived physical histories decoherence functional.'})

out={'id':'CST-DUST-GEOMETRIC-FILTRATION-AUDIT-0.1','status':'PASS_EXACT_COMBINATORICS_AND_INHERITED_INTERVAL_ARITHMETIC',
     'history_count':6,'role_preserving_orbits':2,'profiles':all_profiles,
     'pure_order_invariant_algebra_dimension':2,
     'intrinsic_R_order_algebra_dimension_on_family':1,
     'two_history_filtration_sequences_exist':True,
     'terminal_geometry_does_not_distinguish_histories':True,
     'equal_height_profile':True,
     'accepted_class_decoherence':decoherence,
     'clock_box_qualification':'Order-preserving fraction concerns the bare normalized Lebesgue clock box, not an oscillatory physical probability.',
     'new_clock_quadratures':0,'physical_radius_time_or_expansion':'NOT_DERIVED',
     'next_minimal_requirement':'A physical pairing and history instrument for intrinsic causal-volume filtrations; calibrated timelike/spatial geometry for a collapse interpretation. More history labels alone do not supply these.'}
(ROOT/'results.json').write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({'status':out['status'],'profiles':[all_profiles[0],all_profiles[-1]],'accepted_class_decoherence':decoherence},ensure_ascii=False,indent=2))
