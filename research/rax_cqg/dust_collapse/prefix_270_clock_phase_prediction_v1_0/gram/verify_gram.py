"""Verify the signed rational Gram spectral enclosure from the archived precisions."""
from fractions import Fraction as Q
from itertools import permutations, combinations
import argparse
import json
from pathlib import Path

def check(condition, error):
    if not condition:
        raise ValueError(error)

def det(a):
    """Complex determinant using real-rational pairs."""
    n = len(a)
    re, im = Q(0), Q(0)
    for cols in permutations(range(n)):
        inversions = sum(i > j for i,j in combinations(cols,2))
        x,y = Q((-1)**inversions),Q(0)
        for row,col in enumerate(cols):
            u,v = a[row][col]
            x,y = x*u-y*v, x*v+y*u
        re,im = re+x,im+y
    return re,im

def audit(cert):
    types = cert['types']
    check(len(types)==len(set(types))==11, 'Eleven distinct end types required')
    sizes = {}
    precisions = {}
    for j in types:
        row = cert['end_types'][str(j)]
        a = [[tuple(map(Q,z)) for z in r] for r in row['precision_over_beta']]
        check(len(a)==3 and all(len(r)==3 for r in a), 'Precision dimension')
        check(a==[list(c) for c in zip(*a)], 'Precision symmetry')
        real = [[(x,Q(0)) for x,y in r] for r in a]
        minors = [det([r[:k] for r in real[:k]])[0] for k in (1,2,3)]
        check(min(minors)>0 and list(map(Q,row['real_precision_leading_minors']))==minors,
              'Positive definite real part')
        check(row['free_directions']==0 and not row['pure_bulk_null_vectors']
              and row['mixed_legendre_rank']==row['mixed_legendre_size'],'Domain')
        sizes[j],precisions[j] = minors[-1],a
    used=set()
    budgets={j:Q(0) for j in types}
    for p in cert['overlap_certificates']:
        i,j=p['end_types']
        key=tuple(sorted((i,j)))
        check(i!=j and key not in used, 'Duplicate or diagonal pair')
        used.add(key)
        ai,aj=precisions[i],precisions[j]
        total=[[(ai[r][k][0]+aj[r][k][0],aj[r][k][1]-ai[r][k][1])
                for k in range(3)] for r in range(3)]
        re,im=det(total)
        fourth=64*sizes[i]*sizes[j]/(re**2+im**2)
        bound=Q(p['absolute_upper'])
        check(0<fourth==Q(p['absolute_fourth'])<=1, 'Overlap certificate')
        check(bound>=0 and bound**4>=fourth,'Outward modulus bound')
        budgets[i]+=bound
        budgets[j]+=bound
    check(used==set(combinations(sorted(types),2)), 'Missing pair')
    check(budgets=={int(j):Q(x) for j,x in cert['offdiagonal_row_sum_upper'].items()},'Row sums')
    e=max(budgets.values())
    check(e<1 and Q(cert['gram_lower'])==1-e and Q(cert['gram_upper'])==1+e,'Spectral enclosure')
    return f"{len(used)} pairs, {1-e} I <= G <= {1+e} I"

if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('certificate',type=Path)
    print(audit(json.loads(p.parse_args().certificate.read_text())))
