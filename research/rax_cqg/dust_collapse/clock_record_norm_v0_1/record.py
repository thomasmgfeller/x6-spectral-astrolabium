"""Uhraufgelöste Paarung auf dem AA-Kern. Primärrechnung in rationalen Fehlerscheiben."""
import argparse
import hashlib
import json
from dataclasses import dataclass
from fractions import Fraction as Q
from math import comb, factorial, isqrt
from pathlib import Path

ROOT = Path(__file__).resolve().parent
REPO = ROOT.parents[3]
MANIFEST = json.loads((ROOT / "quellen.json").read_bytes())


def require(condition, message):
    if not condition:
        raise ValueError(message)


def read(name):
    path = REPO / MANIFEST["files"]["quellen/" + name]["path"]
    return json.loads(path.read_bytes())


def sources():
    for name, v in MANIFEST["files"].items():
        data = (REPO / v["path"]).read_bytes()
        digest = hashlib.sha1(b"blob "+str(len(data)).encode()+b"\0"+data).hexdigest()
        require(digest == v["blob"], name)
    return MANIFEST["commit"]


def interval(lo, hi, digits=13):
    require(lo <= hi, "Leeres Intervall")
    den = 10**digits
    def show(k):
        return ("-" if k < 0 else "") + f"{abs(k)//den}.{abs(k)%den:0{digits}d}"
    return [show((lo*den).__floor__()), show((hi*den).__ceil__())]


@dataclass(frozen=True)
class Disk:
    re: Q
    im: Q = Q(0)
    error: Q = Q(0)

    def upper(self):
        return abs(self.re)+abs(self.im)+self.error

    def scale(self, q):
        return Disk(q*self.re,q*self.im,abs(q)*self.error)

    def __add__(self, other):
        return Disk(self.re+other.re,self.im+other.im,self.error+other.error)

    def __mul__(self, other):
        err = self.upper()*other.error+(abs(other.re)+abs(other.im))*self.error
        return Disk(self.re*other.re-self.im*other.im,self.re*other.im+self.im*other.re,err)

    def round(self):
        den = 10**35
        r = Q(int(self.re*den),den)
        i = Q(int(self.im*den),den)
        return Disk(r,i,self.error+abs(r-self.re)+abs(i-self.im))

    def squared(self):
        center = self.re**2 + self.im**2
        delta = (2*(abs(self.re)+abs(self.im))+self.error)*self.error
        return max(Q(0),center-delta), center+delta


def parse_ball(text):
    c, sep, r = text.strip("[]").partition(" +/- ")
    return Q(c), Q(r) if sep else Q(0)


def scalar_factor(orbit):
    re, er = parse_ball(orbit["scalar_factor"]["real"])
    im, ei = parse_ball(orbit["scalar_factor"]["imag"])
    return Disk(re,im,er+ei)


def phase(integer):
    # Teleskopiert keine Wurzelphase; e^(i F4) enthält auch bei F4<0 das Vorzeichen.
    z = Q(integer)
    term = Q(1)
    real, imag = term, Q(0)
    for k in range(1,201):
        term *= z/k
        if k % 2:
            imag += (-1)**(k//2)*term
        else:
            real += (-1)**(k//2)*term
    return Disk(real,imag,abs(z)**201/factorial(201)).round()


def dust_edge(p):
    """Z_p(0) mit allen Dichteatomen, kontinuierlichen Marken und Eingangsuhren."""
    den = 10**23
    b = Q(isqrt(8*den**2//3),den)
    K = 36
    if p == 1:
        sm = [Q(1,2*j+1) for j in range(K+1)]
    else:
        require(p == 2,"Vorgängerzahl")
        sm = [sum(Q(comb(j,i),(2*i+1)*(2*(j-i)+1)) for i in range(j+1)) for j in range(K+1)]
    real, imag = Q(0),Q(0)
    for k in range(K+1):
        moment = sum(comb(k,j)*b**j*Q(1,2)**(k-j)*sm[j] for j in range(k+1))
        density = Q(1,2*(k+1)) if k else Q(1)
        term = density * moment / factorial(k)
        if k % 2:
            imag -= (-1)**(k//2)*term
        else:
            real += (-1)**(k//2)*term
    rem = (Q(1,2)+b*p)**(K+1)/factorial(K+1) + Q(p,4*den)
    return Disk(real,imag,rem).round()


def block_classes(histories, certificate):
    indexed = {r["code"]: r for r in certificate["histories"]}
    out = {}
    null_lines = {}
    for h in histories:
        H = [list(map(Q,row)) for row in h["H0_over_va"]]
        c = -H[2][2]
        B = (0,1,3,4)
        eff = [[H[i][j]+H[i][2]*H[2][j]/c for j in B] for i in B]
        ref = indexed[h["order_code"]]
        require(eff==[list(map(Q,r)) for r in ref["schur_over_beta"]],"Schurblock")
        x,y = [row[2:] for row in eff[:2]]
        rank = 2 if x[0]*y[1]!=x[1]*y[0] else int(any(x+y))
        require(rank==ref["cross_rank"],"Kreuzrang")
        if rank==1:
            first,second = x if any(x) else y
            require(first!=0,"Unerwartete Nullrichtung")
            slope = -second/first
            require(all(row[0]*slope+row[1]==0 for row in (x,y)),"Nullrichtung")
            null_lines[h["order_code"]]=str(slope)
        null_asym = x[0]==x[1] and y[0]==y[1]
        coeff = None
        if null_asym:
            a,off = eff[2][2],eff[2][3]
            require(a==eff[3][3],"Achsen nicht entkoppelt")
            coeff = str((a-off)/2)
        out[h["order_code"]] = (rank,coeff)
    require(len(set(null_lines.values()))==3,"Gemeinsame skalare Nullrichtung")
    return out,null_lines


def run():
    commit = sources()
    data = read("certified_mixing.json")
    hist = {h["order_code"]:h for h in read("aa_hessians.json")["histories"]}
    domain = read("domain_certificate.json")
    classes,lines = block_classes(hist.values(),domain)
    seen = []
    full,without_gravity = Disk(Q(0)),Disk(Q(0))
    diagonal = [Q(0),Q(0)]
    slope_bound = Q(0)
    z = {p:dust_edge(p) for p in (1,2)}
    rows = []
    for row in data["orbit_results"]:
        rep,n = row["representative"],row["multiplicity"]
        members = row["members"]
        p = hist[rep]["p"]
        require(rep==min(members) and n==len(members) and
                all(hist[k]["p"]==p and hist[k]["F4"]==row["F4"] for k in members),"Orbit")
        rel = [(i,j) for i in range(5) for j in range(5) if rep & (1<<(5*i+j))]
        permutations = [(a,1-a,2,3+b,4-b) for a in (0,1) for b in (0,1)]
        orbit = {sum(1<<(5*perm[i]+perm[j]) for i,j in rel) for perm in permutations}
        require(orbit == set(members), "Randvertauschung")
        seen.extend(members)
        factor = scalar_factor(row)
        bare = (factor*z[p]).scale(Q(1,8*33))
        single = phase(row["F4"])*bare
        full += single.scale(n)
        without_gravity += bare.scale(n)
        lo,hi = single.squared()
        diagonal[0] += n*lo
        diagonal[1] += n*hi
        # b=4/sqrt(6)< 49/30, |Z'_p| <= b p/2.
        slope_bound += Q(n,8*33)*factor.upper()*Q(49*p,60)
        rows.append(dict(code=rep,n=n,p=p,per_history_squared=interval(lo,hi)))
    require(sorted(seen)==sorted(hist) and len(seen)==33,"Vollständigkeit")
    lo,hi = full.squared()
    require(lo>0 and (hi<diagonal[0] or lo>diagonal[1]),"Kontrollkontrast")
    finite = []
    for d in (Q(1,16),Q(1,64),Q(1,256),Q(1,1024)):
        # Integriere | |A(u)|²-|A(0)|² | <= 2 |A(0)|L u + L²u².
        residual = full.upper()*slope_bound*d + slope_bound**2*d*d/3
        finite.append(dict(d=str(d),tagged_weight_over_d=interval(max(Q(0),lo-residual),hi+residual)))
    singular = sorted(k for k,(rank,_) in classes.items() if rank==1)
    surviving = {str(k):v for k,(_,v) in classes.items() if v}
    require(surviving=={"25372":"7/4","25496":"7/4","25500":"17/4"},"Quadratische Feldphasen")
    require(len(singular)==5 and len(hist)-len(singular)==28,"Rangverteilung")
    require(Q(49,30)**2 > Q(8,3),"b-Obergrenze")
    # Die frühere untere Schranke nutzte |D| >= 3/16. Dieselbe
    # zertifizierte geometrische Konstante multipliziert nun |Z_p(u)|² >= (1/3)².
    center, radius = parse_ball(domain["tube"]["limit_lower_bound"])
    require(domain["tube"]["Dp_real_lower_bound"]=="3/16" and center-radius>Q(45,10**9),"Referenzschranke")
    density_lower = Q(45,10**9)*(Q(1,3)/Q(3,16))**2
    return dict(commit=commit, records=rows, A_real=interval(full.re-full.error,full.re+full.error),
                A_imag=interval(full.im-full.error,full.im+full.error),tagged_ground_rate=interval(lo,hi),
                incoherent_geometry_flag_control=interval(*diagonal),
                gravity_phase_removed_control=interval(*without_gravity.squared()),
                finite_width_certificates=finite, cross_rank_one=singular,
                rank_two=28, null_directions_q3_over_q4=lines, axial_chirps_over_b=surviving, tube_density_strict_lower=str(density_lower),
                clock_bins_d_one_eighth=[dict(bins=n,absolute_missing_weight_upper=interval(
                    Q(0),slope_bound**2*Q(1,8)**3/(12*n*n))[1]) for n in (1,2,4,8,16)],
                physical_beta=None, physical_P3_comparisons=0, physical_P3=read("eligibility.json")["decision"])


if __name__=="__main__":
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out",type=Path)
    path=parser.parse_args().out
    output=json.dumps(run(),indent=2,ensure_ascii=False)+"\n"
    if path:
        path.write_text(output,encoding="utf8")
    else:
        print(output,end="")
