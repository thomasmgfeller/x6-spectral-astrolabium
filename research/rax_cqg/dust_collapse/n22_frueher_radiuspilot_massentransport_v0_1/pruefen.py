"""Replay the two-mass audit with rational certificates and the archived models."""
import argparse
import csv
from fractions import Fraction as F
from hashlib import sha256
from io import StringIO
import json
import subprocess
import sys
from pilotfelder import ROOT, archive, read_box, paths, PAST
from transport import geometry, packing


def operators(y, w, edges):
    density = [F(19) for _ in y]
    impulse = [F(0) for _ in y]
    for (i,j),k in edges.items():
        diff = y[j]-y[i]
        density[j] += F(k)*diff**2
        flux = F(k)*w[j]*diff
        impulse[i] += flux
        impulse[j] -= flux
    return density, impulse


def scales(row, edges, goals, w, free):
    # All tested sources in this control are zero and all device kicks vanish.
    y = [sum(map(F,b))/2 for b in row["y"]]
    midw = [sum(p)/2 for p in w]
    density,current = operators(y,midw,edges)
    q = -sum(goals[1:])
    assert q > 0 and sum(current) == 0
    assert all(0<=lo<=hi<1 for lo,hi in w)
    gain = F(1,4)/(q/16)
    for scale in (F(1,16),F(1)):
        sd,sg = operators(y,[scale*v for v in midw],edges)
        assert sd == density and sg == [scale*v for v in current]
        assert all((lo>0)==(scale*lo>0) for lo,_ in w)
        assert all(0<=scale*lo<=scale*hi<1 for lo,hi in w)
    # With an order ideal as the past collar, changing only its receiver
    # weights affects only edges entirely within the collar. Those cancel in Q.
    early_only=[v/16 if i in PAST else v for i,v in enumerate(midw)]
    sd, sg=operators(y,early_only,edges)
    assert sd==density and all(sg[j]==current[j] for j in range(22) if j not in PAST)
    assert sum(sg[j] for j in PAST)==sum(current[j] for j in PAST)
    assert any(sg[j]!=current[j] for j in PAST)
    # Interval free equation and target checks at both scales.
    from quelle import hull,box
    from impulsfelder import fields
    Y=[hull(*map(F,b)) for b in row["y"]]
    edges_box=[(i,j,box(F(k))) for (i,j),k in sorted(edges.items())]
    for scale in (F(1,16),F(1)):
        W=[hull(scale*l,scale*h) for l,h in w]
        vals,_,_ = fields(Y,W,box(0),edges_box,free,[],
                          list(map(box,[goals[0]]+[scale*t for t in goals[1:]])),box)
        assert len(vals)==30 and all(v.contains_zero() for v in vals)
    return {"Q_normalized_heavy":str(q),"Q_normalized_light":str(q/16),"model_gain":str(gain),
            "calibrated_heavy":str(gain*q),"calibrated_light":str(gain*q/16),"Q_early_weights_only":str(q)}


def run():
    for doc in ("Pruefplan","Ergaenzung"):
        assert sha256((ROOT/(doc+".md")).read_bytes()).hexdigest()==(ROOT/(doc+".sha256")).read_text().split()[0]
    sources=json.loads((ROOT/"Quellen.json").read_text())
    for name,data in sources["files"].items():
        assert sha256((ROOT/name).read_bytes()).hexdigest()==data["sha256"]
    classic=json.loads(subprocess.check_output([sys.executable,"-B",str(ROOT/"schalenkontrolle.py")]))
    proposals=json.loads((ROOT/"Optimierungszeugen.json").read_text())
    reg=json.loads((ROOT/"basis/P3.json").read_text())
    assert len(reg)==60 and all(r["execution"]=="NOT_RUN" for r in reg)
    targets=[r["checkpoint_context"] for r in reg if r["checkpoint_context"]["M"] in ("1/4","4")
             and r["checkpoint_context"]["x"]=="1/2"]
    assert {(c["M"],c["density_ratio"]) for c in targets}=={(m,d) for m in ("1/4","4") for d in (1,2,4,8)}
    assert len(targets)==8
    cases=[]
    scale_cases=0
    with archive() as (rows,rel,edges,free,goals):
        assert all(i in PAST for i,j in rel if j in PAST)
        assert all(i in PAST for (i,j),k in edges.items() if j in PAST and k)
        assert len(rel)==152 and all(i!=j for i,j in rel)
        assert all((a,d) in rel for a,b in rel for c,d in rel if b==c)
        _,_,_,nodes0=read_box(rows[0][2])
        chains=paths(nodes0,rel)
        from quelle import box,hull
        from impulsfelder import fields
        edge_boxes=[(i,j,box(F(k))) for (i,j),k in sorted(edges.items())]
        for idx,(label,choice,row) in enumerate(rows):
            x,w,positive,nodes=read_box(row)
            assert nodes==nodes0
            # Verify the reported exact goals against the inherited box.
            ybox=[hull(*map(F,b)) for b in row["y"]]
            wbox=[hull(l,h) for l,h in w]
            values,_,g=fields(ybox,wbox,box(F(row["source"])),edge_boxes,free,[],list(map(box,goals)),box)
            assert all(v.contains_zero() for v in values)
            assert all((g[i]-box(goals[i+1])).contains_zero() for i in PAST)
            if F(row["source"])==0:
                scaling=scales(row,edges,goals,w,free)
                scale_cases+=1
            fit=packing(chains,nodes,x,w,proposals[str(idx)])
            geo=geometry(rel,nodes,positive,x,w)
            cases.append(dict(case=idx+1,family=label,choice=choice,J=row["source"],geometry=geo,packing=fit))
    fractions=[list(map(F,c["packing"]["fraction"])) for c in cases]
    assert sum(1 for c in cases if c["family"]=="Feld")==63 and len(proposals)==len(cases)==81
    return dict(reference=classic,checkpoints=[dict(**c,R_phys=None,execution="NOT_RUN") for c in targets],
                all_not_run=len(reg),cases=cases,positive_chains=len(chains),scaled_zero_source_cases=scale_cases,
                scale_control=scaling,initial_Q=str(-sum(goals[1:])),
                fraction_envelope=list(map(str,(min(p[0] for p in fractions),max(p[1] for p in fractions)))),
                maximum_gap=str(max(b-a for a,b in fractions)))


def output(data):
    stream=StringIO()
    t=csv.writer(stream,delimiter="\t",lineterminator="\n")
    t.writerow(["Fall","Familie","Fest","J","Ketten_beidseitig","Optimum_unten","Optimum_oben",
                "Positiv_im_Fenster","Leer_im_Fenster","Materielle_Antikettenbreite"])
    for r in data["cases"]:
        packing,geo=r["packing"],r["geometry"]
        t.writerow([r["case"],r["family"],",".join(map(str,r["choice"])),r["J"],packing["crossing"],*packing["fraction"],
                    ",".join(map(str,geo["positive"])),",".join(map(str,geo["zero"])),geo["material_antichain_width"]])
    return {"Ergebnisse.json":json.dumps(data,indent=2,sort_keys=True)+"\n","Fallregister.tsv":stream.getvalue()}


if __name__=="__main__":
    if not __debug__:
        raise RuntimeError("Python ohne -O erforderlich")
    parser=argparse.ArgumentParser()
    parser.add_argument("--ausgabe",action="store_true")
    args=parser.parse_args()
    result=run()
    for name,body in output(result).items():
        path=ROOT/name
        if args.ausgabe:
            path.write_text(body,encoding="utf-8")
        else:
            assert path.read_text(encoding="utf-8")==body,name
    print("N22-Fallvorgaben:",len(result["cases"]),"| Öffentliche P3-Zielzellen:",len(result["checkpoints"]))
    print("Hülle der maximalen beidseitig belegten Massenanteile:",result["fraction_envelope"])
    print("Status der acht physischen Radien: NOT_RUN")
