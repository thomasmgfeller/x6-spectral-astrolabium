"""Witness-independent necessary tests for a terminal positive receiver."""
from itertools import combinations
from klassen import S


def certify_terminal(rows):
    result = {}
    for row in rows:
        if row['fo'] or row['weight'] != '+':
            continue
        inc = {i:c for (i,j),c in row['coeff'].items() if j == 21}
        mass = sum(inc.values())
        lower = upper = 19*mass*S*S
        # Expand A sum(c_i Y_i²) - (sum(c_i Y_i))² exactly.
        diag = dict.fromkeys(inc,0)
        for (i,c),(j,d) in combinations(sorted(inc.items()),2):
            diag[i] += c*d
            diag[j] += c*d
            a,b = row['bounds'][i]
            u,v = row['bounds'][j]
            left, right = a-v, b-u
            if (i,j) in row['edges']: right = min(right,0)
            if (j,i) in row['edges']: left = max(left,0)
            assert left <= right
            low = 0 if left<=0<=right else min(left*left,right*right)
            high = max(left*left,right*right)
            lower += min(c*d*low,c*d*high)
            upper += max(c*d*low,c*d*high)
        assert all(diag[i]==c*(mass-c) for i,c in inc.items())
        # Off-diagonal monomial Y_i Y_j has coefficient -2 c_i c_j on both sides.
        result[row['id']] = dict(mass=mass,lower=lower,upper=upper,
                                 excluded=lower>0 or upper<0)
    return result
