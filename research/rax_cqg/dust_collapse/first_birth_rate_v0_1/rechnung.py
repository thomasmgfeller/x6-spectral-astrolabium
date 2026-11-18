"""Kurzzeitfluss bei leerem Anfang und feste gemeinsame AA-Randpakete."""
import argparse
from collections import Counter
from fractions import Fraction as F
from hashlib import sha1, sha256
from importlib import import_module
from json import dumps, loads
from math import comb, factorial, isqrt
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parent
REPO = ROOT.parents[3]
META = loads((ROOT / "quellen.json").read_bytes())
PREVIOUS = ROOT.parent / "m1_pilot_clock_v0_1" / "uhrtest.py"


def source_path(name):
    return REPO / META["files"][name]["path"]


def check(ok, message):
    if not ok:
        raise ValueError(message)


def sources():
    for name, row in META["files"].items():
        data = source_path(name).read_bytes()
        check(sha1(b"blob "+str(len(data)).encode()+b"\0"+data).hexdigest() == row["git_blob"], name)
    check(sha256(PREVIOUS.read_bytes()).hexdigest()
          == "f8c44eea232984487c27b14a90c6a746bf3e05915454a2151304324265153580", "Vorlauf")
    return META["commit"]


def wmoment(k):
    return F(1) if not k else F(1, 2*(k+1))


def sqrt_bounds(x, digits=16):
    den = 10**digits
    low = isqrt((x.numerator*den**2)//x.denominator)
    return F(low,den), F(low+1,den)


def pi_bounds():
    def atan(q):
        bottom = sum(F((-1)**i, (2*i+1)*q**(2*i+1)) for i in range(16))
        return bottom, bottom+F(1,33*q**33)
    a,b = atan(5)
    c,d = atan(239)
    return 16*a-4*d, 16*b-4*c


def format_interval(lo, hi, digits=12):
    check(lo <= hi, "Leeres Intervall")
    den = 10**digits
    def decimal(k):
        return ("-" if k < 0 else "")+f"{abs(k)//den}.{abs(k)%den:0{digits}d}"
    return [decimal((lo*den).__floor__()), decimal((hi*den).__ceil__())]


def avg_power(d, k):
    # Mittel von (1/2+4u²)^k über 0<u<d, stetig auch bei d=0.
    return sum(comb(k,j)*F(1,2)**(k-j)*(4*d*d)**j/(2*j+1) for j in range(k+1))


def visibility(d, mu):
    # Zwei unabhängig gezogene Dichtemarken, bewertete Differenzphase.
    terms = 10
    z = F(0)
    alternative = F(1,4)
    for j in range(terms+1):
        k = 2*j
        moment = sum((-1)**i*comb(k,i)*wmoment(i)*wmoment(k-i) for i in range(k+1))
        factor = (-1)**j * mu**k * avg_power(d,k)
        z += factor*moment/factorial(k)
        # Direkter Weg über |chi(x)|² = 1/4 + sinc(x)/2 + (1-cos x)/(2x²).
        alternative += factor*(F(1,2*factorial(k+1))+F(1,2*factorial(k+2)))
    check(z == alternative, "Zwei Sichtbarkeitsrechnungen widersprechen sich")
    err = (abs(mu)*(F(1,2)+4*d*d))**(2*terms+1)/factorial(2*terms+1)
    return max(F(0),z-err),min(F(1),z+err)


def clock():
    sys.path.insert(0, str(source_path("memory.py").parent))
    sys.path.insert(0, str(PREVIOUS.parent))
    m = import_module("memory")
    previous = import_module("uhrtest")
    check(previous.run()["beta_contrast"] == "1/24", "Vorlauf")
    betas = (F(5,4),F(4,3))
    ds = [F(1,2**n) for n in range(3,10)]
    action_checks = 0
    for u in [F(0), *ds, F(1,4), F(1)]:
        for w in (F(0), F(1,8), F(1,2), F(1)):
            before, after = m.with_anchor(()), m.with_anchor((0,))
            T = F(-2) + 4*u
            direct = (m.gravity(after)-m.gravity(before),m.matter(after,(-2,T),(0,w)))
            step = m.increment(before,1,(-2,),T,w)
            check(direct == step == (0,-w*(F(1,2)+4*u*u)), "Ein-Geburts-Wirkung")
            action_checks += 1
    rows = []
    for mu in (F(0),F(1,4),F(1)):
        for d in [F(0), *ds]:
            v_min, v_max = visibility(d,mu)
            e_min,e_max = previous.exp_minus_interval(d)
            for beta in betas:
                # P(N_d=1)/d bis an d=0 stetig fortgesetzt.
                l,h = beta-1+e_min,beta-1+e_max
                yes = (l*v_min, h*v_max)
                no = (l*(1-v_max),h*(1-v_min))
                check(yes[0]+no[0] <= l <= h <= yes[1]+no[1], "Ausgangsbilanz")
                if not mu:
                    check(v_min == v_max == 1 and no == (0,0), "Phase-aus-Kontrolle")
                if d:
                    # P(N>=2)=1-e^-d(1+d), d²/2 folgt auch aus dem zweiten Fakultätsmoment.
                    tail_max = 1-(1+d)*e_min
                    check(0 <= tail_max <= d*d/2, "Mehrgeburtenrest")
                rows.append(dict(mu=str(mu),d=str(d),beta=str(beta),inclusive=format_interval(l,h),
                                 filtered=format_interval(*yes),complement=format_interval(*no)))
    return dict(action_checks=action_checks, dyadic_windows=[str(d) for d in ds], rows=rows,
                phase_on_visibility_limit=format_interval(*visibility(F(0),F(1))))


def time_bins():
    """Phasenfreie Kontrollmessung auf einem einheitlichen Detektorraum 0<s<1."""
    rows = []
    for k in range(2, 11):
        d = F(1, 2**k)
        for j in range(2, 11):
            width = F(1,2**j)
            # Norm der Projektion von 1_(0,d) auf normierte Binindikatoren,
            # geteilt durch die Gesamtmasse d.
            bins = range((d/width).__ceil__())
            captured = sum((min(d,(i+1)*width)-i*width)**2/width for i in bins)/d
            check(captured == min(F(1), d/width), "Dyadische Zeitauflösung")
            rows.append(dict(window=str(d), bin_width=str(width), captured_fraction=str(captured)))
    return rows


def det(matrix):
    if len(matrix)==1:
        return matrix[0][0]
    return sum((-1)**j*x*det([r[:j]+r[j+1:] for r in matrix[1:]])
               for j,x in enumerate(matrix[0]) if x)


def dust_at_edge(p):
    # Aus herausintegrierten Randuhren y_i in [0,1] und der normierten inneren Dichtemarke.
    K = 32
    low,high = sqrt_bounds(F(8,3))
    b = low
    def moment_sum(j):
        if p==1:
            return F(1,2*j+1)
        return sum(F(comb(j,i),(2*i+1)*(2*(j-i)+1)) for i in range(j+1))
    segment = [moment_sum(j) for j in range(K+1)]
    real = imag = F(0)
    for k in range(K+1):
        mk = wmoment(k)*sum(comb(k,j)*F(1,2)**(k-j)*b**j*segment[j] for j in range(k+1))
        term = (-1)**((k+1)//2)*mk/factorial(k)
        if k%2:
            imag += term
        else:
            real += term
    # Lipschitz-Fehler im Parameter b und komplexer reeller-Phasen-Taylorrest.
    error = (high-low)*p/4 + (F(1,2)+b*p)**(K+1)/factorial(K+1)
    squared = real*real+imag*imag
    radius = 2*error+error**2
    check(real-error > F(1,3) and squared-radius > 0, "Randamplitude verschwindet")
    return squared-radius, squared+radius


def aa():
    repo = loads(source_path("aa_hessians.json").read_bytes())
    contract = loads(source_path("existence_contract.json").read_bytes())
    cases = repo["histories"]
    check(len({x["order_code"] for x in cases}) == len(cases) == contract["histories"] == 33,
          "AA-Familie")
    pi_lo,pi_hi = pi_bounds()
    b_lo,b_hi = sqrt_bounds(F(8,3))
    weights = {p:dust_at_edge(p) for p in (1,2)}
    outputs = []
    bounds = []
    for case in cases:
        code = int(case["order_code"])
        relations = {(i,j) for i in range(5) for j in range(5) if code & (1<<(5*i+j))}
        H = [[F(0)]*5 for _ in range(5)]
        for i,j in relations:
            depth = sum((i,k) in relations and (k,j) in relations for k in range(5))
            kappa = F((1,-9,16,-8)[depth],2)
            H[i][i] -= kappa
            H[j][j] -= kappa
            H[i][j] += kappa
            H[j][i] += kappa
        check(H == [list(map(F,row)) for row in case["H0_over_va"]], "Hessian")
        p = sum((i,2) in relations for i in (0,1))
        q = sum((2,i) in relations for i in (3,4))
        c = -H[2][2]
        check((p,q) == (case["p"],case["q"]) and c == F(p+q,2) and c >= 1, "Skalarlücke")
        border = (0,1,3,4)
        eff = [[H[i][j]+H[i][2]*H[2][j]/c for j in border] for i in border]
        squared = [[F(i==j)+F(8,3)*sum(eff[i][k]*eff[k][j] for k in range(4))
                    for j in range(4)] for i in range(4)]
        determinant = det(squared)
        check(determinant >= 1, "Gaussnenner")
        low,high = sqrt_bounds(determinant)
        d0,d1 = weights[p]
        bounds.append((pi_lo**3*d0/(2*b_hi*c*high), pi_hi**3*d1/(2*b_lo*c*low)))
        outputs.append(dict(code=code,p=p,q=q,determinant=str(determinant),
                            squared_amplitude_slope=format_interval(*bounds[-1])))
    return dict(packets="atom/skalare Grundmode -> atom/skalare Grundmode; Einheitsbreiten; masselos",
                coefficient="Einheitsbetrag je separat untersuchter Ordnung",
                counts=dict(Counter(f"{r['p']},{r['q']}" for r in outputs)),
                extremal_enclosure=format_interval(min(lo for lo,_ in bounds),max(hi for _,hi in bounds)),
                cases=outputs)


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--out",type=Path)
    args = ap.parse_args()
    commit = sources()
    result = dict(commit=commit,clock=clock(),aa=aa(),time_resolution=time_bins(),
                  physical_eligibility=loads(source_path("eligibility.json").read_bytes())["decision"],
                  physical_birth_rate=None,physical_P3_comparisons=0)
    encoded = dumps(result, indent=2, ensure_ascii=False)+"\n"
    if args.out is None:
        print(encoded,end="")
    else:
        args.out.write_text(encoded,encoding="utf8")


if __name__=="__main__":
    main()
