"""N11 action symmetry, sector selection, and charge-invariant boundary record."""
import argparse
import hashlib
import json
import math
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

import mpmath as mp
import sympy as s

BASE = Path(__file__).resolve().parent
SRC = BASE/"sources"
Q = s.Rational


def read(path):
    return json.loads(path.read_text(encoding="utf-8"))


def J(n):
    return s.zeros(n).row_join(s.eye(n)).col_join((-s.eye(n)).row_join(s.zeros(n)))


def ratmat(raw):
    return s.Matrix(raw).applyfunc(s.sympify)


def simplify(m):
    return m.applyfunc(s.simplify)


def scalar(m):
    return s.simplify(m[0])


def repo_inputs():
    for name, meta in read(BASE/"provenance.json")["files"].items():
        assert hashlib.sha256((SRC/name).read_bytes()).hexdigest()==meta["sha256"]
    with tempfile.TemporaryDirectory() as tmp:
        script=Path(tmp)/"canonical_check.py"
        shutil.copyfile(SRC/"canonical_check.py",script)
        subprocess.run([sys.executable,"-B",str(script)],stdout=subprocess.DEVNULL,check=True)
        assert read(script.with_name("results.json"))==read(SRC/"canonical.json")


def reduce_shift(d):
    # One unit is a shift of every dimensionless scalar x=sqrt(beta) q by one.
    uniform=s.ones(4,1).col_join(s.zeros(4,1))
    w=[]
    for name,ax,axes,emb in [("A_minus",0,[1,2,3,5,6,7],"input_embedding"),
                             ("A_plus",3,[0,1,2,4,5,6],"output_embedding")]:
        row=ratmat(d["constraints"][name])
        flow=J(4)*row.T
        lift=(s.eye(8)-flow*s.eye(8)[ax,:]/flow[ax]).extract(axes,range(8))
        assert row*uniform==s.zeros(1,1) and lift*flow==s.zeros(6,1)
        v=lift*uniform
        assert v.T*J(3)==uniform.T*J(4)*ratmat(d["common_reduction"][emb])
        w.append(v)
    maps=[ratmat(d["common_reduction"][f"R{j}"]) for j in range(2)]
    for j,r in enumerate(maps):
        H=ratmat(d["legendre"][f"C{j}_Hbar"])
        assert H*s.ones(11,1)==s.zeros(11,1)
        assert r*w[0]==w[1] and w[1].T*J(3)*r==w[0].T*J(3)
    assert (maps[1]-maps[0]).rank()==5
    return maps,*w


def sector_and_pairs(old,maps,wm,wp):
    data={}
    for name,row in old["boundary"]["two_modes"].items():
        gamma=[]
        false_at_tenth=[]
        weight=row["probability_use_test_rejecting_C0"]
        observed=[int(x)-7 for x in name.split(",")]
        omitted,=set(range(3))-set(observed)
        for j,t in enumerate(row["tests_rejecting_C0_C1"]):
            alpha=s.Matrix([t["unnormalized_coefficients_q_then_p"]]).applyfunc(s.sympify)
            N=Q(t["commutator_norm"])
            assert alpha[omitted]==alpha[omitted+3]==0
            assert scalar(s.I*alpha*J(3)*alpha.H)==N
            # Exactly the other oscillator is mixed after tracing the omitted mode:
            # the nontrivial symplectic eigenvalue equals that of the omitted mode.
            rr=maps[j]
            cov=rr*rr.T/2
            aa=observed+[i+3 for i in observed]
            local=cov.extract(aa,aa)
            om=cov.extract([omitted,omitted+3],[omitted,omitted+3]).det()
            tvar=s.Symbol("t")
            assert om>Q(1,4)
            assert s.expand((J(2)*local).charpoly(tvar).as_expr()-(tvar**2+Q(1,4))*(tvar**2+om))==0
            assert simplify((alpha*rr)[:,:3]+s.I*(alpha*rr)[:,3:])==s.zeros(1,3)
            disp=scalar(alpha*wp)
            assert s.simplify(disp-scalar(alpha*rr*wm))==0
            g=s.simplify(s.Abs(disp)**2/N)
            assert g>0
            gamma.append(str(g))
            false_at_tenth.append(float((weight if j==0 else 1-weight)*(-math.expm1(-float(g)/100))))
        data[name]={"opposite_click_displacement_gamma_C0_C1":gamma,
                    "false_click_at_dimensionless_shift_0_1_C0_C1":false_at_tenth,
                    "all_invariant_unambiguous_pair_effects":"zero"}
    return data


def common_state(maps):
    T=maps[0].inv()*maps[1]
    z=s.Symbol("z")
    p=s.factor(T.charpoly(z).as_expr())
    brackets=[(Q(44,1000),Q(45,1000)),(Q(608,1000),Q(609,1000)),
              (Q(1643,1000),Q(1644,1000)),(Q(22252,1000),Q(22253,1000))]
    f=s.Poly(p,z)
    for a,b in brackets: assert f.count_roots(a,b)==1
    assert p.subs(z,1)==s.diff(p,z).subs(z,1)==0 and s.diff(p,z,2).subs(z,1)!=0
    assert (T-s.eye(6)).rank()==5
    return {"relative_characteristic_polynomial":str(p),
            "four_nonunit_real_root_intervals":[[str(a),str(b)] for a,b in brackets],
            "unit_eigenvalue_algebraic_geometric":[2,1],"normal_branch_neutral_state":"excluded"}


def fourth_root_eff_interval(x,places=12):
    scale=10**places
    lo=math.isqrt(math.isqrt(int(x.p)*scale**4//int(x.q)))
    assert Q(lo,scale)**4<=x<Q(lo+1,scale)**4
    return [str(Q(scale-lo-1,scale)),str(Q(scale-lo,scale))]


def fiber_overlap(maps,wp,wm):
    # Use charge as first position of an explicitly canonical output chart.
    ell=wp.T*J(3)
    a,b=ell[:,:3].T,ell[:,3:].T
    unit=s.eye(6)
    chart=ell
    for i in [1,2]: chart=chart.col_join(unit[i,:]-b[i]/b[0]*unit[0,:])
    chart=chart.col_join(-unit[0,:]/b[0])
    for i in [1,2]: chart=chart.col_join(unit[3+i,:]+a[i]/b[0]*unit[0,:])
    assert chart*J(3)*chart.T==J(3)
    axes=[1,2,4,5]
    variance=scalar(wm.T*wm)/2
    cond,slopes=[],[]
    for r in maps:
        V=chart*r*r.T*chart.T/2
        assert V[0,0]==variance
        k=V.extract(axes,[0])/variance
        vc=V.extract(axes,axes)-variance*k*k.T
        assert vc*J(2)*vc==J(2)/4
        cond.append(vc); slopes.append(k)
    tot=cond[0]+cond[1]
    ds=slopes[0]-slopes[1]
    gap=scalar(ds.T*tot.inv()*ds)/2
    zero4=1/tot.det()
    lack4=s.cancel(zero4/(1+variance*gap)**2)
    assert 0<lack4<zero4<1 and gap>0

    # Independent Fourier transform of the complex (unnormalized) cross measure.
    gd=read(SRC/"gaussians.json")
    omega=[ratmat(x["Omega_scaled_exact"]) for x in gd["branches"]]
    def weak_var(x,y):
        v=s.I*a-y*b
        return scalar(b.T*y*b-s.I*a.T*b-v.T*(x.conjugate()+y).inv()*v)
    kappa=s.expand_complex(weak_var(*omega))
    assert s.simplify(weak_var(omega[1],omega[0])-s.conjugate(kappa))==0
    assert all(weak_var(om,om)==variance for om in omega)
    cross4=Q(read(SRC/"record_v02.json")["boundary"]["full_three_modes"]["overlap_fourth_power"])
    assert 0<cross4<lack4
    assert s.simplify(zero4-cross4*variance**2/s.Abs(kappa)**2)==0
    assert s.simplify(gap-(s.re(1/kappa)-1/variance))==0
    assert s.simplify(lack4-cross4*s.Abs(kappa)**2/s.re(kappa)**2)==0
    # Direct charge quadrature, independently of the analytic final Gaussian integral.
    with mp.workdps(45):
        val=lambda x:mp.mpf(str(x.evalf(50)))
        vv,gg,zz=map(val,[variance,gap,zero4])
        overlap_integral=mp.quad(lambda x:zz**mp.mpf("0.25")*mp.exp(-x*x*(1/vv+gg)/2)/
                                mp.sqrt(2*mp.pi*vv),[-mp.inf,0,mp.inf])
        assert abs(overlap_integral**4-val(lack4))<mp.mpf("1e-40")
    # A bounded, positive charge weight preserves transport on each branch.
    # Compare fixed coordinate wavefunctions, normalized in each scalar pairing.
    with mp.workdps(45):
        vv,gg,zz=map(val,[variance,gap,zero4])
        eps=mp.mpf("0.5")
        vw=1/(1/vv+gg)
        norm=1+eps*mp.exp(-mp.mpf("0.5"))
        weighted_loss=overlap_integral*(1+eps*mp.exp(-vw/(2*vv)))/norm
        def weight(q):
            return 1+eps*mp.cos(q/mp.sqrt(vv))
        def dens(q):
            return mp.exp(-q*q/(2*vv))/mp.sqrt(2*mp.pi*vv)
        norm_quad=mp.quad(lambda q:weight(q)*dens(q),[-mp.inf,0,mp.inf])
        loss_quad=mp.quad(lambda q:weight(q)*dens(q)*zz**mp.mpf("0.25")*mp.exp(-gg*q*q/2),
                          [-mp.inf,0,mp.inf])/norm_quad
        assert abs(norm-norm_quad)+abs(weighted_loss-loss_quad)<mp.mpf("1e-40")
        assert 0<overlap_integral<weighted_loss<1
    return {"weighted_pairing_efficiency_same_coordinate_input":float(1-weighted_loss),
            "charge_variance":str(variance),"conditional_overlap_at_zero_fourth_power":str(zero4),
            "conditional_abs_overlap_exp_minus_gap_times_q2_over_two":str(gap),
            "cross_characteristic_weak_variance":[str(s.re(kappa)),str(s.im(kappa))],
            "integrated_inconclusive_fourth_power":str(lack4),
            "optimal_balanced_efficiency_enclosure":fourth_root_eff_interval(lack4),
            "optimal_balanced_efficiency":float(1-lack4**Q(1,4)),
            "conditional_efficiency_at_charge_zero":float(1-zero4**Q(1,4)),
            "unrestricted_three_mode_benchmark":float(1-cross4**Q(1,4))}


def records(old,eta):
    parent=read(SRC/"record_v01.json")["fine_grid"]["runs"]
    clock=read(SRC/"clock_v01.json")
    table={}
    eta0=old["boundary"]["two_modes"]["7,8"]["balanced_efficiency"]
    outcomes=old["records"]["finest"]["outcomes"]
    for prep,kernels in outcomes.items():
        table[prep]={}
        shape,level=prep.split("_")
        for k,modes in kernels.items():
            table[prep][k]={}
            for mode,prev in modes.items():
                one=prev["one_pair"]/eta0;three=prev["three_pairs"]/eta0
                if mode=="all_modes":
                    raw=clock[shape][k]
                    assert abs(one-raw["one_pair"])+abs(three-raw["three_pairs"])<5e-12
                elif shape=="split":
                    raw=parent[k][level]
                    assert abs(one-raw["one_constant"])+abs(three-raw["three_constant"])<5e-12
                hit1,hit3=eta*one,eta*three
                unresolved=prev["accepted"]-hit1-hit3
                fail=1-prev["accepted"]
                assert min(hit1,hit3,unresolved,fail)>=0 and abs(hit1+hit3+unresolved+fail-1)<1e-14
                table[prep][k][mode]={"one_pair":hit1,"three_pairs":hit3,"unresolved":unresolved,
                                      "boundary_failure":fail,"score":hit1-hit3}
    deltas={}
    for name,start,end in [("density","split_low","split_high"),("clock","narrow_low","split_low")]:
        deltas[name]={}
        for mode in ["all_modes","constant_mode"]:
            d={k:table[end][k][mode]["score"]-table[start][k][mode]["score"] for k in table[start]}
            assert abs(d["common_C0_dust"])<1e-14
            if name=="density" and mode=="all_modes":
                assert all(abs(table[end]["coupled"][mode][key]-v)<1e-14 for key,v in table[start]["coupled"][mode].items())
            assert abs(d["coupled"]-eta/eta0*old["records"]["finest"]["contrasts"][name][mode]["coupled"])<1e-14
            deltas[name][mode]=d
    return {"probabilities":table,"changes":deltas,"clock_inputs":"archived PR 317/318 quadratures, no new clock integration"}


def compute():
    repo_inputs()
    d=read(SRC/"canonical.json"); old=read(SRC/"record_v02.json")
    maps,wm,wp=reduce_shift(d)
    pair=sector_and_pairs(old,maps,wm,wp)
    fiber=fiber_overlap(maps,wp,wm)
    return {"shift_in_out":[list(map(str,w)) for w in [wm,wp]],
            "charge_in_out":[list(map(str,w.T*J(3))) for w in [wm,wp]],
            "rank_of_map_difference":5,"pairs":pair,"neutral_state":common_state(maps),
            "three_mode_invariant":fiber,"backreaction":records(old,fiber["optimal_balanced_efficiency"]),
            "physical_stage_5A":"HOLD"}


def check(a,b):
    if isinstance(a,dict):
        assert a.keys()==b.keys()
        for k in a:check(a[k],b[k])
    elif isinstance(a,list):
        assert len(a)==len(b)
        for x,y in zip(a,b):check(x,y)
    elif isinstance(a,float):assert abs(a-b)<5e-13
    else:assert a==b


if __name__=="__main__":
    if not __debug__: raise RuntimeError("Assertions must be active")
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--write",action="store_true")
    arg=parser.parse_args()
    result=compute(); path=BASE/"results.json"
    if arg.write:path.write_text(json.dumps(result,indent=2,allow_nan=False)+"\n")
    else:check(result,read(path))
    print("Passed N11 reconstruction, unique shared charge, pair and common-state obstructions,")
    print("two independent exact fiber calculations, integral, rational enclosure, and probability balances.")
