"""Unabhängige Gleitkomma-Kontrolle. Rekonstruiert alle 33 komplexen Beiträge ohne Orbitzertifikate."""
import cmath
import json
import math
from fractions import Fraction
from pathlib import Path
from functools import lru_cache

ROOT = Path(__file__).resolve().parent
B = math.sqrt(8/3)


def check(test, message):
    if not test:
        raise ValueError(message)


def eigenvalues(matrix):
    # Orthogonale Jacobi-Rotationen einer reellen symmetrischen 4x4-Matrix.
    a = [row.copy() for row in matrix]
    for _ in range(100):
        p,q = max(((i,j) for i in range(4) for j in range(i+1,4)),key=lambda ij:abs(a[ij[0]][ij[1]]))
        off = a[p][q]
        if abs(off)<1e-14:
            return [a[i][i] for i in range(4)]
        x,y = a[p][p],a[q][q]
        t=.5*math.atan2(2*off,y-x)
        c,s=math.cos(t),math.sin(t)
        for j in range(4):
            if j not in (p,q):
                l,r=a[j][p],a[j][q]
                a[j][p]=a[p][j]=c*l-s*r
                a[j][q]=a[q][j]=s*l+c*r
        a[p][p],a[q][q]=c*c*x-2*c*s*off+s*s*y,s*s*x+2*c*s*off+c*c*y
        a[p][q]=a[q][p]=0.
    raise ValueError("Jacobi-Konvergenz")


def scalar(record):
    h=[[float(Fraction(s)) for s in row] for row in record["H0_over_va"]]
    b=(0,1,3,4)
    c=-h[2][2]
    e=[[h[i][j]+h[i][2]*h[2][j]/c for j in b] for i in b]
    detroot=math.prod(cmath.sqrt(1-1j*B*v) for v in eigenvalues(e))
    return 4*math.pi*cmath.exp(-1j*math.pi/4)*math.sqrt(2*math.pi/(B*c))/detroot


def gauss(n):
    nodes=[]
    for j in range(1,n+1):
        x=math.cos(math.pi*(j-.25)/(n+.5))
        for _ in range(15):
            p,old=x,1.
            for k in range(2,n+1):
                old,p=p,((2*k-1)*x*p-(k-1)*old)/k
            dp=n*(x*p-old)/(x*x-1)
            step=p/dp
            x-=step
            if abs(step)<2e-16:
                break
        nodes.append(((1+x)/2,1/((1-x*x)*dp*dp)))
    check(abs(sum(w for _,w in nodes)-1)<1e-13,"Gewichte")
    return nodes


def chi(x):
    return .5+.5*cmath.exp(-.5j*x)*math.sin(x/2)/(x/2)


def distance(x,box):
    lo,hi=map(float,box)
    return max(0.,lo-x,x-hi)


def main():
    expected=json.loads((ROOT/"ergebnis.json").read_bytes())
    hist=json.loads((ROOT.parent/"amplitude_existence_v0_1"/"inputs"/"aa_hessians.json").read_bytes())["histories"]
    near=gauss(16)
    @lru_cache(maxsize=None)
    def dust(u):
        k=[(B*(u-y)**2,w) for y,w in near]
        return {1:sum(w*chi(.5+x) for x,w in k),
                2:sum(w*v*chi(.5+x+y) for x,w in k for y,v in k)}
    coeff=[(h["p"],scalar(h)/264,cmath.exp(1j*h["F4"])) for h in hist]
    def component(u,gravity=True):
        z=dust(u)
        return [a*z[p]*(phase if gravity else 1) for p,a,phase in coeff]
    @lru_cache(maxsize=None)
    def amp(u):
        return sum(component(u))
    a=amp(0)
    controls=[(a.real,expected["A_real"]),(a.imag,expected["A_imag"]),
              (abs(a)**2,expected["tagged_ground_rate"]),
              (sum(abs(x)**2 for x in component(0)),expected["incoherent_geometry_flag_control"]),
              (abs(sum(component(0,False)))**2,expected["gravity_phase_removed_control"])]
    orbits=json.loads((ROOT.parent/"parity_mixing_v0_1"/"results"/"certified_mixing.json").read_bytes())["orbit_results"]
    representative={k:row["representative"] for row in orbits for k in row["members"]}
    for h,(_,v,_) in zip(hist,coeff):
        cert=next(row for row in expected["records"] if row["code"]==representative[h["order_code"]])
        controls.append((abs(v*dust(0)[h["p"]])**2,cert["per_history_squared"]))
    for row in expected["finite_width_certificates"]:
        d=float(Fraction(row["d"]))
        tagged=sum(w*abs(amp(d*x))**2 for x,w in near)
        controls.append((tagged,row["tagged_weight_over_d"]))
    worst=max(distance(x,box) for x,box in controls)
    check(worst<=2e-12,"Vergleich mit der rationalen Hülle")
    d=1/8
    tagged=d*sum(w*abs(amp(d*x))**2 for x,w in near)
    last=0.
    for row in expected["clock_bins_d_one_eighth"]:
        n=row["bins"]
        width=d/n
        caught=width*sum(abs(sum(w*amp((i+x)*width) for x,w in near))**2 for i in range(n))
        check(last<=caught+1e-14 and -1e-14<=tagged-caught<=float(row["absolute_missing_weight_upper"])+1e-14,"Zeitauflösung")
        last=caught
    print(f"{len(controls)} Werte gegen rationale Hüllen sowie fünf Zeitzellensummen geprüft.")
    print(f"Numerische Kontrolle bei d=1/8: W/d={tagged/d:.12f}, 16 Zellen: {last/d:.12f}.")


if __name__=="__main__":
    main()
