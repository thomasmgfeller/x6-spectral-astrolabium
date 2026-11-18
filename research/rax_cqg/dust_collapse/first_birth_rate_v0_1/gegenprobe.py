"""Numerische Gegenprobe der rationalen Einschliessungen mit einem zweiten Rechenweg."""
import cmath
import json
from math import pi, sin, sqrt
from pathlib import Path
from fractions import Fraction

HERE = Path(__file__).resolve().parent


def rule(n):
    if n % 2:
        raise ValueError("Gerade Teilungszahl erforderlich")
    return [(j/n, (1 if j in (0,n) else 2 if j%2==0 else 4)/(3*n)) for j in range(n+1)]


def chi(t):
    if t == 0:
        return 1
    return .5+.5*cmath.exp(-.5j*t)*sin(t/2)/(t/2)


def det5(mat):
    a = [row.copy() for row in mat]
    r = 1+0j
    for k in range(5):
        pivot = max(range(k,5),key=lambda i:abs(a[i][k]))
        if abs(a[pivot][k]) == 0:
            return 0j
        if pivot!=k:
            a[k],a[pivot]=a[pivot],a[k]
            r=-r
        r*=a[k][k]
        for i in range(k+1,5):
            scale=a[i][k]/a[k][k]
            for j in range(k+1,5):
                a[i][j]-=scale*a[k][j]
    return r


def discrepancy(x, interval):
    lo,hi=map(float,interval)
    return max(0.,lo-x,x-hi)


def main():
    expected=json.loads((HERE/"ergebnis.json").read_bytes())
    histories=json.loads((HERE.parent/"amplitude_existence_v0_1"/"inputs"/"aa_hessians.json").read_bytes())["histories"]
    by_code={r["order_code"]:r for r in histories}
    b=sqrt(8/3)
    nodes=rule(192)
    dust={}
    dust[1]=sum(a*chi(.5+b*u*u) for u,a in nodes)
    dust[2]=sum(a*c*chi(.5+b*(u*u+v*v)) for u,a in nodes for v,c in nodes)
    errors=[]
    for row in expected["aa"]["cases"]:
        h=by_code[row["code"]]["H0_over_va"]
        matrix=[[int(i==j and i!=2)-1j*b*float(Fraction(h[i][j]))
                 for j in range(5)] for i in range(5)]
        slope=pi**3*abs(dust[row["p"]])**2/(2*abs(det5(matrix)))
        errors.append(discrepancy(slope,row["squared_amplitude_slope"]))
    for row in expected["clock"]["rows"]:
        from math import exp
        d,beta,mu=(float(Fraction(row[k])) for k in ("d","beta","mu"))
        weight=beta-1+exp(-d)
        v=sum(a*abs(chi(mu*(.5+4*(d*u)**2)))**2 for u,a in nodes)
        for key,val in (("inclusive",weight),("filtered",weight*v),("complement",weight*(1-v))):
            errors.append(discrepancy(val,row[key]))
    if max(errors)>1e-8:
        raise ValueError("Quadratur oder direkte Determinante widerspricht der Einschliessung")
    print(f"{len(errors)} Gegenvergleiche; maximaler Abstand zur rationalen Hülle {max(errors):.3g}")


if __name__=="__main__":
    main()
