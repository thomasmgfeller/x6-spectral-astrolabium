"""Offline verification of the early two-mass radius audit. Python >= 3.10, standard library."""
import argparse
import ast
from collections import Counter
import csv
from fractions import Fraction as F
from hashlib import sha1, sha256
from itertools import combinations, product
import json
from pathlib import Path
from zipfile import ZipFile
from area_mesh import calibrate
from weight_domain import SOURCE, run as verify_weights

HERE = Path(__file__).resolve().parent
INPUT = HERE / "inputs"
def source(path):
    return INPUT / path.replace("/","__")

def baseline():
    for s in json.loads((HERE/"sources.json").read_text()):
        data = (INPUT/s["name"]).read_bytes()
        assert sha1(b"blob "+str(len(data)).encode()+b"\0"+data).hexdigest()==s["blob"],s["path"]
    plan = json.loads(source("correspondence_v0_1/plan.json").read_text())
    design = json.loads((HERE/"design.json").read_text())
    roots = {F(1,4):F(1,2), F(4):F(2)}
    assert set(roots)==set(map(F,design["masses"]))
    assert plan["reference"]["R0"]==design["R0"]==10 and plan["primary_tolerances"]["R"]==0.05
    grid = list(map(F,plan["reference"]["time_fractions"]))
    assert list(map(F,plan["reference"]["masses"]))==[min(roots),F(1),max(roots)]
    def cube(m,x):
        return (1-roots[m]*x/4)**2
    low,high = F(19,20),F(21,20)
    light,heavy = sorted(roots)
    positive_grid = sorted(x for x in grid if x>0)
    separated = [x for x in positive_grid if low**3*cube(light,x)>high**3*cube(heavy,x)]
    x = min(separated)
    assert x==F(1,2) and F(1,4) not in separated
    radii, bands, diagnostics = {},{},{}
    with source("correspondence_v0_1/results/reference_comparisons.csv").open(newline="") as stream:
        rows = list(csv.DictReader(stream))
    for m in roots:
        relevant = [r for r in rows if F(r["M"])==m and F(r["x"])==x and r["observable"]=="r"]
        assert sorted(int(r["steps"]) for r in relevant)==[128,256,512,1024]
        for row in relevant:
            assert F(row["reference_lo"])**3<=cube(m,x)<=F(row["reference_hi"])**3
            assert F(row["ODE_enclosure_lo"])**3<=cube(m,x)<=F(row["ODE_enclosure_hi"])**3
            assert row["numerical_cap_decision"]=="PASS"
        lo,hi = (10*F(relevant[0][k]) for k in ("reference_lo","reference_hi"))
        radii[m]=(lo,hi)
        bands[m]=(low*lo,high*hi)
        diagnostics[str(m)]={"radius_bounds_exact":list(map(str,(lo,hi))),
                             "radius_approx":float((lo+hi)/2),
                             "tolerance_band_outer_bounds":list(map(str,bands[m])),
                             "tolerance_band_approx":list(map(float,bands[m]))}
    gap = bands[light][0]-bands[heavy][1]
    assert gap>0 and radii[heavy][0]>2*heavy
    records = json.loads(source("correspondence_v0_1/results/checkpoint_P3_records.json").read_text())
    chosen = [r for r in records if F(r["checkpoint_context"]["x"])==x and F(r["checkpoint_context"]["M"]) in roots]
    assert sorted((F(r["checkpoint_context"]["M"]),r["checkpoint_context"]["density_ratio"]) for r in chosen)==list(product(sorted(roots),[1,2,4,8]))
    assert all(r["execution"]=="NOT_RUN" for r in chosen)
    gate = json.loads(source("correspondence_v0_1/results/eligibility.json").read_text())
    assert gate["decision"]=="HOLD_NOT_ELIGIBLE" and not gate["physical_pass"]
    contrast = (radii[heavy][0]-radii[light][1], radii[heavy][1]-radii[light][0])
    return {"x":str(x),"T_star":"5*sqrt(5)/6","reference":diagnostics,
            "heavy_minus_light_bounds_exact":list(map(str,contrast)),
            "heavy_minus_light_approx":float(sum(contrast)/2),
            "gap_lower_bound_exact":str(gap),"band_gap_approx":float(gap),"cross_checked_classical_ODE_rows":8,
            "physical_checkpoint_records_checked":len(chosen),"physical_refinement_ratios":[1,2,4,8]}

def read_order_builder():
    # Use only the order part of the pinned source, before it constructs the scalar Hessian.
    module = ast.parse(source("prefix_1564_two_event_v0_1/two_event.py").read_text())
    keep = []
    for node in module.body:
        if isinstance(node,ast.Assign) and any(isinstance(t,ast.Name) and t.id in {"OLD","INNER","PAST","FUTURE"} for t in ast.walk(node.targets[0])):
            keep.append(node)
        if isinstance(node,ast.FunctionDef) and node.name=="transitive":
            keep.append(node)
        if isinstance(node,ast.FunctionDef) and node.name=="full_geometry":
            cut = next(i for i,stmt in enumerate(node.body) if isinstance(stmt,ast.Assign) and isinstance(stmt.targets[0],ast.Name) and stmt.targets[0].id=="H")
            node.body = node.body[:cut]+[ast.Return(value=ast.Name(id="relations",ctx=ast.Load()))]
            keep.append(node)
    scope = {"product":product,"combinations":combinations}
    exec(compile(ast.fix_missing_locations(ast.Module(body=keep,type_ignores=[])),"order_fragment","exec"),scope)
    return scope["full_geometry"],scope["INNER"],scope["PAST"],scope["FUTURE"]

def geometry():
    order,inner,past,future = read_order_builder()
    assert len(inner)==7 and len(past)==len(future)==4
    with ZipFile(SOURCE) as archive:
        catalog = json.loads(archive.read("catalog.json"))
    pairs = list(combinations(range(7),2))
    histogram = Counter()
    accepted = [int(k) for k,(a,_,b) in catalog["ranks_pure_free_mixed"].items() if a==b==0]
    for key in accepted:
        internal = [pair for i,pair in enumerate(pairs) if key & (1<<i)]
        edges = order(internal)
        for v in past+future:
            assert all((v,w) in edges or (w,v) in edges for w in past+inner+future if w!=v)
        # Every antichain containing a collar vertex is a singleton.
        antichains = [s for size in range(1,8) for s in combinations(inner,size)
                      if all((i,j) not in edges and (j,i) not in edges for i,j in combinations(s,2))]
        width = max(map(len,antichains))
        histogram[width] += 1
        large = [frozenset(s) for s in antichains if len(s)>=4]
        assert all(a & b for a,b in combinations(large,2))
    assert len(accepted)==1048
    return {"scalar_admissible_catalogue_size":len(accepted),"antichain_width_counts":dict(sorted(histogram.items())),
            "one_antichain_at_least_4":sum(v for k,v in histogram.items() if k>=4),
            "two_disjoint_antichains_of_at_least_4":0,
            "scope":"Raw embedded cuts with distinct event vertices and simultaneity interpreted as an antichain. A large antichain does not supply intrinsic lengths or a surface."}

def counterassignments():
    x = F(1,2)
    out = []
    for k in [F(0),F(1,3)]:
        values = {}
        for m,sm in [(F(1,4),F(1,2)),(F(4),F(2))]:
            values[str(m)] = 10*(1-sm*x/6-m*x*x/144-k*(4-m)*x**3)
            assert values[str(m)]>0
        delta = values["4"]-values["1/4"]
        out.append({"k":str(k),"radii":{m:str(v) for m,v in values.items()},"heavy_minus_light":str(delta)})
    assert F(out[0]["heavy_minus_light"])<0<F(out[1]["heavy_minus_light"])
    return out

def main():
    if not __debug__:
        raise SystemExit("Run without -O so verifications are enabled.")
    parser = argparse.ArgumentParser()
    parser.add_argument("--out",type=Path)
    args = parser.parse_args()
    result = {"source_commit":"3c159b6a2ece918a478496b6727f7f2c782accff",
              "design_sha256":sha256((HERE/"design.json").read_bytes()).hexdigest(),
              "p3_reference_check":baseline(),"weights":verify_weights(),"raw_surface_check":geometry(),
              "synthetic_area_controls":calibrate(),"logical_counterassignments":counterassignments(),
              "physical":{"decision":"HOLD_NOT_ELIGIBLE","execution":"NOT_RUN","histories_generated":0,
                          "radius_M_1_4":None,"radius_M_4":None,"weight_uniform_radius_intervals":None,
                          "mass_contrast":None,"bounce":"NOT_TESTED"}}
    encoded = json.dumps(result,indent=2,ensure_ascii=False)+"\n"
    if args.out:
        args.out.write_text(encoded)
    else:
        print(encoded,end="")

if __name__=="__main__":
    main()
