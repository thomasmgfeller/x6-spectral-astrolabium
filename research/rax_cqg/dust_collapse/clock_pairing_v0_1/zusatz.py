"""Independent orbit, reference ODE and phase controls for the finite clock pilot."""
import csv
import json
import math
from collections import Counter
from decimal import Decimal as D, localcontext
from fractions import Fraction as F
from itertools import permutations, product
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parent
REPO = ROOT.parents[3]
SOURCES = json.loads((ROOT / "quellen.json").read_text(encoding="utf8"))["dateien"]
sys.path.insert(0, str((REPO / SOURCES["uhr_quelle/intervals.py"]["pfad"]).parent))
import intervals

def check(ok, message):
    if not ok:
        raise ValueError(message)

def source_path(name):
    return REPO / SOURCES["daten/" + name]["pfad"]


def data(name):
    return json.loads(source_path(name).read_text(encoding="utf8"))

def orbit_columns():
    archived = data("candidates.json")["roots"]["one"]["families"]["rooted_parent_capped_incidence_4"]
    ref = archived["six_order_mask_first"]["pure_orbit_transfer_A_to_B"]
    columns = []
    for rep in ref["representative_codes"]:
        edges = [(i,j) for i,j in product(range(6), repeat=2) if rep & (1 << (6*i+j))]
        # Permute exactly the three inserted events, then delete the last insertion.
        orbit = set()
        for perm in permutations((3,4,5)):
            labels = (0,1,2) + perm
            orbit.add(tuple(sorted((labels[i], labels[j]) for i,j in edges)))
        prefix = Counter(sum(1 << (6*i+j) for i,j in image if i < 5 and j < 5)
                         for image in orbit)
        check(len(orbit) == 3 and all(v == 1 for v in prefix.values()), "three equiprobable paths")
        columns.append({i: F(v,len(orbit)) for i,v in prefix.items()})
    check(columns[0] == columns[1] and sorted(columns[0]) == ref["equal_column_positive_prefixes"],
          "different N13 columns")
    mass_a, mass_b = map(F, ref["witness_orbit_masses"])
    check(mass_a == mass_b == F(1, 49_000_000), "wrong archived witness")
    branch = data("sector.json")["conditional_scalar_branches"]
    fa,fb = (branch[str(i)]["F4"] for i in ref["end_types"])
    rows = []
    for theta in [F(-1,2), F(0), F(1,2)]:
        t = theta * mass_a
        x,y = mass_a-t, mass_b+t
        check(min(x,y) > 0, "positivity")
        for key in columns[0]:
            check(x*columns[0][key]+y*columns[1][key] == (mass_a+mass_b)/3, "N13 marginal")
        shift = x*fa+y*fb-(mass_a*fa+mass_b*fb)
        check(shift == -84*t, "F4 sensitivity")
        rows.append({"theta":theta, "t":t, "A":x, "B":y, "change_in_weighted_F4":shift})
    return {"prefix_column":columns[0], "F4_A_B":[fa,fb], "samples":rows,
            "physical_target_for_F4":None}

def action_controls():
    old=(0,)
    end_orders={"K":(0,1), "A":(0,0)}
    sample=None
    count=changes=0
    max_mod_error=0.0
    import cmath
    for t0,t1,w0,w1 in product([F(-7,8),F(-3,4),F(-5,8)], [F(-3,8),F(-1,8),F(0),F(1,4)],
                               [F(0),F(1,2),F(3,4)], [F(0),F(1,2),F(3,4)]):
        g0,d0=intervals.action((old,(t0,),(w0,)))
        ends={key:intervals.action((order,(t0,t1),(w0,w1))) for key,order in end_orders.items()}
        increments={key:(g-g0,d-d0) for key,(g,d) in ends.items()}
        phases={}
        for key,(g,d) in increments.items():
            arms={"coupled":g+d, "dust_on_reference_antichain":g+increments["A"][1],
                  "no_gravity_phase":d, "no_dust_phase":g, "both_off":F(0)}
            phases[key]=arms
            for exponent in arms.values():
                # Same branch factor for bra and ket. The old packet phase is retained.
                joint_exponent=-exponent+exponent
                check(joint_exponent==0, "phase cancellation")
                phase=cmath.exp(1j*float(exponent))
                max_mod_error=max(max_mod_error, abs(phase.conjugate()*phase-1))
                count+=1
        gap={arm:phases["K"][arm]-phases["A"][arm] for arm in phases["K"]}
        if gap["coupled"]!=gap["dust_on_reference_antichain"]:
            changes+=1
            if sample is None:
                sample={"T":[t0,t1],"density_marks":[w0,w1],"chain_minus_antichain_phase_exponents":gap}
    check(changes>0 and count==1080 and max_mod_error < 1e-14, "inactive intervention")
    return {"marks_and_clock_configurations":108,"orders":2,"arms":5,"branch_comparisons":count,
            "changed_relative_exponents_under_reference_dust":changes,"example":sample,
            "max_float_modulus_squared_error":max_mod_error,
            "scope":"diagonal path effect; no scalar field, no claim of physical backreaction"}

def p3():
    # Fresh fixed-step RK4 for the classical ODE at M=1 on the coarsest numerical grid.
    # The separate radius containment check cubes rational interval endpoints.
    names=("r","rho_over_rho0","H_times_Tend","acceleration_times_Tend_squared")
    with localcontext() as ctx:
        ctx.prec=50
        r,u,h=D(1),-D(1)/6,D(1)/128
        def rhs(radius,velocity):
            return velocity,-1/(72*radius**2)
        samples={}
        for j in range(129):
            if j%32==0:
                samples[F(j,128)] = dict(zip(names, (r,1/r**3,u/r,-1/(72*r**3))))
            if j==128:
                break
            a,b=rhs(r,u)
            c,d=rhs(r+h*a/2,u+h*b/2)
            e,f=rhs(r+h*c/2,u+h*d/2)
            g,k=rhs(r+h*e,u+h*f)
            r+=h*(a+2*c+2*e+g)/6
            u+=h*(b+2*d+2*f+k)/6
        numerics=[]; archive_bounds=[]
        def dec(q):
            return D(q.numerator)/D(q.denominator)
        seen=set()
        with source_path("reference_comparisons.csv").open(newline="") as stream:
            for row in csv.DictReader(stream):
                if F(row["M"])!=1 or int(row["steps"])!=128:
                    continue
                time,name=F(row["x"]),row["observable"]
                check((time,name) not in seen,"duplicate P3 row")
                seen.add((time,name))
                s=1-time/4
                lo,hi=(F(row[key]) for key in ("ODE_enclosure_lo","ODE_enclosure_hi"))
                if name=="r":
                    check(lo**3<=s*s<=hi**3, "radius enclosure")
                    ref=dec(s)**(D(2)/3)
                else:
                    exact={names[1]:1/s**2,names[2]:-1/(6*s),names[3]:-1/(72*s**2)}[name]
                    check(lo<=exact<=hi,"analytical value outside archive")
                    ref=dec(exact)
                y=samples[time][name]
                numerics.append(abs((y-ref)/ref))
                archive_bounds.extend(abs(F(row[key])) for key in ("relative_error_lo","relative_error_hi"))
        check(len(seen)==20 and max(archive_bounds)<=F(1,200), "P3 archive coverage")
        check(max(numerics)<D("1e-10"),"unexpected RK4 discrepancy")
        plan=data("plan.json")
        slots={"dynamics":20,"mass":5,"side_flux":12,"initial_velocity":1}
        check(plan["family"]["total"]==524 and sum(slots.values())==38,"cohort count")
        return {"classical_rows":len(seen),"largest_archived_relative_enclosure_percent":str(dec(max(archive_bounds))*100),
                "RK4_largest_relative_discrepancy":str(max(numerics)),
                "RK4_samples":{str(t):{k:str(x) for k,x in row.items()} for t,row in samples.items()},
                "cohort_slots":slots,"physical_observations":0,"physical_P3":"HOLD_NOT_ELIGIBLE / NOT_RUN"}

def tail_and_records():
    # The known positive-atom laws are diagnostics for the missing physical F(v).
    for n in range(1,21):
        v=F(1,2**n)
        check([v**a / v**2 for a in (1,2,3)]==[1/v,1,v],"tail contribution")
    paths=list(product(range(2), repeat=2))
    def measure(records, use_index):
        weights=[F(0),F(0)]
        for i,(a,b) in enumerate(records):
            key=i%2 if use_index else b
            weights[key]+=F((-1)**(a*b),2)
        return tuple(x*x for x in weights)
    wrong=0
    for order in permutations(paths):
        check(measure(order,False)==(1,0),"permutation changed record")
        wrong+=measure(order,True)!=(1,0)
    check(wrong==12,"injected fault not exposed")
    runs=data("clock_packet_results.json")["finest_grid"]["fixed_clocks"]
    errors=[]
    for run in runs:
        lo,hi=(run[k]["joint_left_middle_right_failure"] for k in ("rho_1_8","rho_1_4"))
        check(len(lo)==len(hi)==4 and math.fsum(lo)==math.fsum(hi)==1,"N11 normalization")
        errors.extend(abs(a-b) for a,b in zip(lo,hi))
    check(len(errors)==12 and max(errors)<1e-14,"N11 control")
    return {"tail_checks":60,"permutations":24,"wrong_index_cases_exposed":wrong,
            "N11_fixed_clock_max_difference":max(errors),"physical_small_volume_tail":None}

if __name__=="__main__":
    print(json.dumps({"orbit":orbit_columns(),"actions":action_controls(),"M1":p3(),
                      "audit":tail_and_records()},indent=2,default=str,sort_keys=True))
