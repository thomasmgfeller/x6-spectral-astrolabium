"""CST-DUST: zwei Auswertungen am gemeinsamen Rand. Python 3.10+, Standardbibliothek."""
import argparse
import cmath
import hashlib
import json
import math
import sys
from collections import Counter
from fractions import Fraction as F
from pathlib import Path


ROOT = Path(__file__).resolve().parent
STUDIES = ROOT.parent
REPO = ROOT.parents[3]
sys.path.insert(0, str(STUDIES / "extended_sewing_v0_1"))
import sewing

B2 = F(8, 3)
B = math.sqrt(B2)
I2 = [[1, 0], [0, 1]]


def require(ok, why):
    if not ok:
        raise ValueError(why)


def load_inputs():
    manifest = json.loads((ROOT / "quellen.json").read_text())
    for name, source in manifest["files"].items():
        data = (REPO / source["path"]).read_bytes()
        git = hashlib.sha1(b"blob " + str(len(data)).encode() + b"\0" + data).hexdigest()
        require(git == source["sha"], "Git-Quellbindung: " + name)
    return json.loads((STUDIES / "amplitude_existence_v0_1/inputs/aa_hessians.json").read_text())["histories"]


def mm(a, b):
    return [[sum(x*y for x, y in zip(row, col)) for col in zip(*b)] for row in a]


def linear(a, b, fa, fb):
    return [[fa*x + fb*y for x, y in zip(ar, br)] for ar, br in zip(a, b)]


def det(a):
    return a[0][0]*a[1][1] - a[0][1]*a[1][0]


def inv(a):
    d = det(a)
    return [[a[1][1]/d, -a[0][1]/d], [-a[1][0]/d, a[0][0]/d]]


def trace(a):
    return a[0][0] + a[1][1]


def relation(code):
    return {(i, j) for i in range(5) for j in range(i+1, 5) if code & (1 << (5*i+j))}


def response(h):
    code = h["order_code"]
    mat = [list(map(F, row)) for row in h["H0_over_va"]]
    action = sewing.local_action(range(5), relation(code))
    require(sewing.doubled_hessian(action) == [[2*x for x in row] for row in mat]
            and action["F4"] == h["F4"], "Rekonstruktion der Einzelwirkung")
    c = -mat[2][2]
    k = [[mat[i][j] + mat[i][2]*mat[2][j]/c for j in (0,1,3,4)] for i in (0,1,3,4)]
    l, x, r = [v[:2] for v in k[:2]], [v[2:] for v in k[:2]], [v[2:] for v in k[2:]]
    m = inv(linear(I2, mm(l, l), 1, B2))
    xt = list(zip(*x))
    q = linear(I2, mm(xt, mm(m, x)), 0, B2)
    p = linear(r, mm(xt, mm(l, mm(m, x))), 1, -B2)
    require(q[0][0] >= 0 and q[1][1] >= 0 and trace(q)>0 and det(q)>=0, "Dämpfung")
    gap = math.hypot(float(l[0][0]-l[1][1]), 2*float(l[0][1]))
    roots = [cmath.sqrt(1-1j*B*(float(trace(l))+s*gap)/2) for s in (-1,1)]
    n = 2*math.sqrt(math.pi)*cmath.exp(-1j*math.pi/4)*math.sqrt(2*math.pi/(B*float(c)))/math.prod(roots)
    return dict(code=code, q=q, p=p, amp=n*cmath.exp(1j*h["F4"])/264, parents=h["p"])


def pair(x, y):
    # det(epsilon I + A + i b T) = epsilon^2 + epsilon tr + det0
    a = linear(x["q"], y["q"], F(1,2), F(1,2))
    t = linear(x["p"], y["p"], F(1,2), F(-1,2))
    re = det(a) - B2*det(t)
    im_b = a[0][0]*t[1][1] + a[1][1]*t[0][0] - 2*a[0][1]*t[0][1]
    if det(a)>0:
        label = "absolute"
    elif re or im_b:
        label = "fresnel"
    else:
        require(t == [[0,0],[0,0]], "Unerwarteter divergenter Paartyp")
        label = "length"
    return (label, complex(float(re), B*float(im_b)), complex(float(trace(a)), B*float(trace(t))))


def quadrature(n):
    nodes = []
    for j in range(n):
        z = math.cos(math.pi*(j+.75)/(n+.5))
        for _ in range(24):
            p, old = z, 1.
            for k in range(2,n+1):
                p, old = ((2*k-1)*z*p - (k-1)*old)/k, p
            derivative = n*(z*p-old)/(z*z-1)
            change = p/derivative
            z -= change
            if abs(change)<2e-16:
                break
        nodes.append(((1+z)/2, 1/((1-z*z)*derivative**2)))
    require(abs(sum(w for _,w in nodes)-1)<1e-13, "Quadraturgewichte")
    return nodes


def dust(u, nodes):
    terms = [(B*(y-u)**2,w) for y,w in nodes]
    def chi(k):
        return .5 + .5*cmath.exp(-.5j*k)*math.sin(.5*k)/(.5*k)
    return {1:sum(w*chi(.5+x) for x,w in terms),
            2:sum(w*v*chi(.5+x+y) for x,w in terms for y,v in terms)}


def time_dust(nodes, d):
    samples = [(w*d,dust(x*d,nodes)) for x,w in nodes]
    return {(p,q):sum(w*z[p].conjugate()*z[q] for w,z in samples)
            for p in (1,2) for q in (1,2)}


def fmt(x):
    return format(x, ".11g")


def complex_fmt(z):
    return [fmt(z.real),fmt(z.imag)]


def folded(rows):
    nodes = quadrature(16)
    weights = time_dust(nodes, 1/8)
    refined = time_dust(quadrature(24), 1/8)
    require(max(abs(z-refined[k]) for k,z in weights.items())<1e-14,"Staubquadratur")
    counts = Counter()
    exceptions = []
    contributions = []
    for x in rows:
        for y in rows:
            label, d0, tr = pair(x, y)
            a = x["amp"].conjugate()*y["amp"]*weights[x["parents"],y["parents"]]*math.pi
            contributions.append((label,d0,tr,a))
            counts[label] += 1
            if label!="absolute":
                exceptions.append({"codes":[x["code"],y["code"]],"type":label})
    require(counts == {"absolute":1078,"fresnel":4,"length":7}, "Paarklassifikation")
    def gram(eps):
        terms = [a/cmath.sqrt(eps*eps + eps*tr + d0) for _,d0,tr,a in contributions]
        result = complex(math.fsum(v.real for v in terms),math.fsum(v.imag for v in terms))
        require(result.real>0 and abs(result.imag)<1e-12, "positive kohärente Norm")
        return result.real
    density = sum((a/cmath.sqrt(math.pi*tr)).real for typ,_,tr,a in contributions if typ=="length")
    finite = sum((a/cmath.sqrt(d0)).real for typ,d0,_,a in contributions if typ!="length")
    require(density>0, "Längendichte")
    sample = []
    for k in (2,4,8,12,16):
        eps = 10.**(-k)
        g = gram(eps)
        sample.append({"epsilon":"1e-"+str(k),"gram":fmt(g),
                       "length_density":fmt(g*math.sqrt(eps/math.pi)),
                       "CS_lower_bound_for_norm_squared":fmt(g*g/gram(2*eps))})
    require(abs(gram(1e-16) - density*math.sqrt(math.pi/1e-16) - finite)<1e-8, "asymptotische Entwicklung")
    by_code = {r["code"]:r for r in rows}
    x,y = by_code[25372],by_code[25500]
    _,d0,_ = pair(x,y)
    cross = math.pi*x["amp"].conjugate()*y["amp"]*weights[1,2]/cmath.sqrt(d0)
    return {"ordered_pairs":dict(counts),"nonabsolute_pairs":exceptions,
            "clock_window":"0 <= u <= 1/8; integrated du",
            "atom_fold_leading_density":fmt(density),"atom_fold_finite_part_on_fixed_sum":fmt(finite),
            "gaussian_cutoffs":sample,"direct_quadrature_controls":{str(e):fmt(gram(e)) for e in (4,8)},
            "finite_part_example_in_clock_window":{"codes":[25372,25500],
            "cross":complex_fmt(cross),"two_by_two_determinant":fmt(-abs(cross)**2)}}


def forward_atom(action, order):
    # Original outer Gaussian packets, inner Abel limit. Use continuous pivot roots.
    h = sewing.doubled_hessian(action)
    exterior = (0,1,6,7)
    m = [[complex(int(i==j and i in exterior), -B*h[i][j]/2) for j in order] for i in order]
    root = 1+0j
    for k in range(8):
        pivot = m[k][k]
        require(abs(pivot)>1e-12 and not (pivot.real < 0 and abs(pivot.imag)<1e-12),
                "unaufgelöster Zweig der Determinantenwurzel")
        root *= cmath.sqrt(pivot)
        for i in range(k+1,8):
            left = m[i][k]/pivot
            for j in range(k+1,8):
                m[i][j] -= left*m[k][j]
    return (math.pi**3/8)*cmath.exp(1j*action["F4"])/root


def forward(rows):
    left, right = [], []
    for h in rows:
        rel = relation(h["code"])
        left.append(sewing.make_packet("left",range(5),rel,[3,4],[0,1]))
        right.append(sewing.make_packet("right",range(3,8),{(i+3,j+3) for i,j in rel},[3,4],[6,7]))
    values = []
    worst = 0.
    for l in left:
        parts = []
        for r in right:
            action = sewing.sew_packets(l,r)["joint_action"]
            a = forward_atom(action,(0,1,6,7,2,3,4,5))
            b = forward_atom(action,(7,6,1,0,2,3,4,5))
            worst = max(worst,abs(a-b))
            parts.append(a/1089)
        values.append(sum(parts))
    total = sum(values)
    control = json.loads((STUDIES/"extended_sewing_v0_1/results/verification.json").read_bytes())["full_1089_sum_all_atom"]["0"]
    tol = float(control["absolute_component_error_bound"])
    require(worst<1e-12 and abs(total.real-float(control["real"]))<tol
            and abs(total.imag-float(control["imag"]))<tol, "publizierter Abel-Wert")
    diag = sum(abs(v)**2 for v in values)
    coherent = abs(total)**2
    cross = sum((x.conjugate()*y).real for i,x in enumerate(values) for j,y in enumerate(values) if i!=j)
    require(abs(coherent-diag-cross)<1e-18 and coherent>0, "Kreuztermbilanz")
    return {"histories_per_half":33,"joint_actions":1089,"folded_record_rank_on_labelled_coefficients":1,
            "total_amplitude":complex_fmt(total),"fixed_record_weight":fmt(coherent),
            "left_diagonal_control":fmt(diag),"left_offdiagonal_total":fmt(cross),
            "reordered_max_difference":fmt(worst),
            "partial_amplitudes":[{"left":r["code"],"complex":complex_fmt(v)} for r,v in zip(rows,values)]}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out", type=Path, required=True)
    args = parser.parse_args()
    rows = [response(h) for h in sorted(load_inputs(),key=lambda a:a["order_code"])]
    require(len(rows)==33 and len({r["code"] for r in rows})==33, "Historienfamilie")
    result = {"commit":json.loads((ROOT/"quellen.json").read_text())["commit"],
              "identity_fold":folded(rows),"extended_sewing_fixed_record":forward(rows),
              "physical_relative_norm":"HOLD","P3_M1_first_density_physical_comparisons":0}
    args.out.write_text(json.dumps(result,ensure_ascii=False,indent=2,sort_keys=True)+"\n")


if __name__ == "__main__":
    main()
