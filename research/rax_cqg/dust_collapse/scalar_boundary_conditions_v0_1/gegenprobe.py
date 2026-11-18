"""Gegenprobe aus den Ordnungsbits und Test der Operatoren ohne Import des Hauptprogramms."""
import cmath
import json
import math
from fractions import Fraction as Q
from pathlib import Path

HERE = Path(__file__).resolve().parent
B = 4/math.sqrt(6)


def verify(ok, subject):
    if not ok:
        raise ValueError(subject)


def relation(code, i, j):
    return (code >> (5*i+j)) & 1


def hessian(code):
    m = [[Q(0) for _ in range(5)] for _ in range(5)]
    for i in range(5):
        for j in range(5):
            if relation(code,i,j):
                interior = sum(relation(code,i,k)*relation(code,k,j) for k in range(5))
                w = Q((1,-9,16,-8)[interior],2)
                m[i][i] -= w
                m[j][j] -= w
                m[i][j] += w
                m[j][i] += w
    return m


def relabel(code, p):
    return sum(relation(code,i,j) << (5*p[i]+p[j]) for i in range(5) for j in range(5))


def gaussian_checks(h, ref):
    # Stationary value with a free q_2. Construct by evaluating the
    # five-field bilinear form on four independently continued boundary vectors.
    vectors = []
    for j in (0,1,3,4):
        f = [Q(int(i==j)) for i in range(5)]
        f[2] = -h[2][j]/h[2][2]
        vectors.append(f)
    m = [[sum(f[i]*h[i][j]*g[j] for i in range(5) for j in range(5))
          for g in vectors] for f in vectors]
    x = [r[2:] for r in m[:2]]
    diff = x[0][0]*x[1][1]-x[1][0]*x[0][1]
    verify((2 if diff else int(any(x[0]+x[1])))==ref['rank'], "Kreuzrang")
    if ref['rank']==2:
        return None
    v = ref['null']
    r = [list(map(Q,ref['constraint_row'][:2])),list(map(Q,ref['constraint_row'][2:]))]
    for y in range(4):
        # Momentum for boundary basis vector y from the original five-field action.
        p = [sum(h[i][j]*vectors[y][j] for j in range(5)) for i in (3,4)]
        expected = -(r[0][y-2] if y>=2 else 0)
        verify(sum(z*t for z,t in zip(p,v))==expected, "Impuls aus der vollen Wirkung")
    length = math.hypot(*v)
    e = [-v[1]/length, v[0]/length]
    t = [sum(float(x[i][j])*e[j] for j in range(2)) for i in range(2)]
    a = 1-1j*B*float(m[0][0])
    c = 1-1j*B*float(m[1][1])
    off = -1j*B*float(m[0][1])
    determinant = a*c-off**2
    g = B**2 * (c*t[0]**2-2*off*t[0]*t[1]+a*t[1]**2) / determinant
    verify(abs(g.real-float(Q(ref['gaussian_q']))) < 2e-14, "Transversale Breite")
    alpha = -B*float(h[2][2])
    amp = math.sqrt(2*math.pi/alpha)*2*math.sqrt(math.pi)/cmath.sqrt(determinant)
    # Only |amp| occurs here. The determinant's square-root branch does not affect it.
    width = 10/math.sqrt(g.real)
    n = 800
    step = 2*width/n
    def density(i):
        z = -width+step*i
        return abs(amp*cmath.exp(-g*z*z/2))**2
    total = sum((1 if i in (0,n) else 4 if i%2 else 2)*density(i) for i in range(n+1))*step/3
    target = (8*math.pi**2.5/B)*math.sqrt(float(Q(ref['reduced_squared_norm_factor'])))
    relative = abs(total-target)/target
    verify(relative < 1e-12, "Streifenmittel pro Einheitslänge")
    return relative


def operator(poly, slope):
    # Coefficients in variable sqrt(b) a. Small integer/half-integer
    # coefficients in this polynomial calculation are exactly binary representable.
    result = [0j]*(len(poly)+1)
    for j, coef in enumerate(poly):
        if j:
            result[j-1] -= 1j*j*coef
        result[j+1] -= slope*coef
    return result


def main():
    result = json.loads((HERE/'ergebnis.json').read_bytes())
    records = {r['order']:r for r in result['histories']}
    sources = json.loads((HERE / 'quellen.json').read_bytes())
    path = sources['files']['quellen/aa_hessians.json']['path']
    raw = json.loads((HERE.parent / path).read_bytes())
    errors = []
    for entry in raw['histories']:
        code = entry['order_code']
        h = hessian(code)
        verify(h==[list(map(Q,r)) for r in entry['H0_over_va']], "Ordnungs-Code")
        err = gaussian_checks(h,records[code])
        if err is not None:
            errors.append(err)
        for perm in ((0,1,2,3,4),(1,0,2,3,4),(0,1,2,4,3),(1,0,2,4,3)):
            other = relabel(code, perm)
            other_h = hessian(other)
            verify(other in records and all(h[i][j]==other_h[perm[i]][perm[j]]
                   for i in range(5) for j in range(5)), "Randvertauschung")
            if records[code]['rank']==1:
                verify(records[other]['reduced_squared_norm_factor']==records[code]['reduced_squared_norm_factor'],
                       "Norm und Randvertauschung")
    for degree in range(10):
        poly = [0]*degree+[1]
        a = operator(operator(poly,8.5),3.5)
        b = operator(operator(poly,3.5),8.5)
        verify([i-j for i,j in zip(a,b)]==[5j*x for x in poly]+[0,0], "Kommutator")
    # Widths in units of b after removal of the mean phase. Exact equality only at 5/2.
    delta = Q(5,2)
    for w in (Q(1,4),Q(1),delta,Q(4),Q(9)):
        loss = (w*w+delta*delta)/(2*w)
        verify(loss-delta==(w-delta)**2/(2*w) and loss>=delta, "Schärfe")
    print(f"{len(records)} Hesse-Matrizen aus den Relationen, {len(records)*4} Randvertauschungen, "
          f"{len(errors)} transversale Integrale, 10 Kommutator- und 5 Breitentests bestanden.")
    print(f"Grösste relative Quadraturabweichung: {max(errors):.3g}")


if __name__ == "__main__":
    main()
