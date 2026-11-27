"""Re-enumerate the finite family and replay its exact certificates."""
import argparse
from collections import Counter,defaultdict
import csv
from hashlib import sha256
from io import StringIO
import json

from filter import Empty, Model, bounds, intersect, probe_sign
from fruehe_uhren import sharpen
from lineare_huelle import inequalities, margin
from momente import with_cuts
from ordnungen import COLLAR, EMPTY, POS, ROOT, SOURCE, as_relation, closures, compatible, inputs, outgoing
from verfeinerung import refine,split

NO,OPEN,YES="AUSGESCHLOSSEN","OFFEN","ZEUGE"

def dump(data):
    return json.dumps(data,sort_keys=True,indent=2,ensure_ascii=False)+"\n"

def name(values):
    return ",".join(map(str,values)) or "∅"

def replay(model,y,w,cert,stats):
    """Any failed split, missing leaf or nonpositive rational margin aborts the run."""
    try:
        refine(model,y,w)
    except Empty:
        assert cert==0
        stats["Intervall-Endbox"]+=1
        return
    assert isinstance(cert,dict)
    if "split" in cert:
        assert set(cert)=={"split","children"} and len(cert["children"])==2
        for (Y,W),child in zip(split(y,w,cert["split"]),cert["children"],strict=True):
            replay(model,Y,W,child,stats)
    elif "linear" in cert:
        assert margin(*inequalities(model,y,w),cert["linear"])>0
        stats["Lineare Endbox"]+=1
    else:
        c=cert["moment"]
        assert margin(*with_cuts(model,y,w,c["cuts"]),c["dual"])>0
        stats["Moment-Endbox"]+=1

def anchored(rel,p,f,q):
    return (q not in p and q not in f and any((a,q) in rel and a not in EMPTY for a in p)
            and any((q,b) in rel and b not in EMPTY for b in f))

def certify(side,idx,wanted,model,y,w,proofs,stats,used):
    key=str(idx)+"/"+str(wanted)
    if key not in proofs[side]:
        return None
    method,cert=proofs[side][key]
    used[side].add(key)
    if method=="linear":
        assert margin(*inequalities(model,y,w),cert)>0
        stats["Lineare Endbox"]+=1
    else:
        if method=="scharf":
            try:
                sharpen(model,y,w)
            except Empty:
                assert cert=="projection"
                stats["Eingangsprojektion"]+=1
                return method
        else:
            assert method=="tree"
        replay(model,y,w,cert,stats)
    return method

def decide(pair,side,idx,rel,p,f,old,proofs,stats,used):
    previous=old.get((p,f))
    if previous:
        return (YES if previous["status"]=="EXISTS_IN_WINDOW" else NO,NO,NO,"PR415",[])
    baseline,w0=bounds(pair,side)
    if probe_sign(f,outgoing(rel,f),baseline,w0):
        return NO,NO,NO,"G22_Vorzeichen",[]
    model=Model(as_relation(rel,p,f))
    try:
        # The recorded 10-pass polytope starts from fresh collar and sector boxes.
        y,w=model.screen(pair,side,10)
    except Empty as err:
        return NO,NO,NO,"Intervall_"+str(err),[]
    proof=certify(side,idx,"-",model,y.copy(),w.copy(),proofs,stats,used)
    if proof:
        return NO,NO,NO,proof,[]

    pending=[]
    for q in POS:
        Y,W=y.copy(),w.copy()
        try:
            intersect(Y,q,baseline[22])
            model.contract(Y,W,12)
        except Empty:
            continue
        if not certify(side,idx,q,model,Y,W,proofs,stats,used):
            pending.append(q)
    contact=OPEN if any(anchored(rel,p,f,q) for q in pending) else NO
    return OPEN,OPEN if pending else NO,contact,"Einzelereignisse",pending

def tsv(header,rows):
    out=StringIO()
    writer=csv.writer(out,delimiter="\t",lineterminator="\n")
    writer.writerow(header)
    writer.writerows(rows)
    return out.getvalue()

def build():
    digest,filename=(ROOT/"Pruefplan.sha256").read_text().split()
    assert sha256((ROOT/filename).read_bytes()).hexdigest()==digest
    pair,cases,scan=inputs()
    rel=set(map(tuple,pair["relation"]))
    assert len(rel)==152 and all((a,c) in rel and a!=c for a,b in rel for j,c in rel if b==j)
    fs,ps=closures(rel)
    old={(tuple(s["past"]),tuple(s["future"])):s for s in cases}
    prior={tuple(s["future"]):s["allowed"] for s in scan["heavy"]["empty_futures"]}
    assert prior=={tuple(s["future"]):s["allowed"] for s in scan["light"]["empty_futures"]}
    assert len(prior)==31 and sum(prior.values())==2
    assert len(fs)==336 and len(ps)==337 and len(old)==25
    proofs=json.loads((ROOT/"Zertifikate.json").read_text())
    used={s:set() for s in proofs}
    stats=Counter()
    full=[]
    idx=0
    for side in ("heavy","light"):
        clocks,_=bounds(pair,side)
        assert max(clocks[q].h for q in (0,1,2,3))<clocks[22].l
        assert min(clocks[q].l for q in (7,8,9,10))>clocks[22].h
        assert 0 not in EMPTY and 10 not in EMPTY
    for f in fs:
        scope="PR414_Familie" if prior.get(f) else "PR413_verworfen" if f in prior else "weitere_Zukunft"
        for p in ps:
            if not compatible(rel,p,f):continue
            collar=bool(set(f)&{0,1,2,3} or set(p)&{7,8,9,10})
            for side in ("heavy","light"):
                if collar:probe,same,contact,reason,pending=NO,NO,NO,"Kragenzeit",[]
                else:probe,same,contact,reason,pending=decide(pair,side,idx,rel,p,f,old,proofs,stats,used)
                full.append([name(f),name(p),side,scope,probe,same,contact,",".join(map(str,pending)) or "–",reason])
            if not collar:idx+=1
    from uebertrag import propagate
    propagate(full,rel)
    # Tabulate the final decisions after exact transfers between orders.
    aggregates=defaultdict(Counter)
    regroup=defaultdict(Counter)
    for future,past,side,scope,probe,same,contact,pending,reason in full:
        row=regroup[future,side,scope]
        row["orders"]+=1
        row["collar"]+=reason=="Kragenzeit"
        row["probe_"+probe]+=1
        row["same_"+same]+=1
        row["contact_"+contact]+=1
    short=[]
    for (future,side,scope),row in regroup.items():
        aggregates[side].update(row)
        aggregates[side+"/"+scope].update(row)
        short.append([future,side,scope,row["orders"],row["collar"],row["probe_"+NO],row["probe_"+YES],
                      row["probe_"+OPEN],row["same_"+OPEN],row["contact_"+OPEN]])
    assert idx==2240 and len(full)==4640 and len(short)==672
    assert all(aggregates[s]["contact_"+OPEN]==0 for s in ("heavy","light"))
    assert all(used[s]==set(proofs[s]) for s in proofs),{s:sorted(set(proofs[s])-used[s]) for s in proofs}
    info=dict(commit="4409db3c7f92633da49c337ad725e8209e524cbd",input_sha256=SOURCE,orders=2320,
              admissible_after_collar=idx,futures=336,after_collar_futures=307,
              summary={k:dict(v) for k,v in aggregates.items()},certificate_leaves=dict(stats),
              physical_pilot_radii=[None]*8,physical_P3="NOT_RUN",P3_count=60)
    return {"Ergebnisse.json":dump(info),"Fallregister.tsv":tsv(
        ["Zukunft","Vergangenheit","Praeparation","Vorauswahl","Sonde_im_Fenster","Sonde_und_positiv_im_Fenster",
         "Verankerter_Kontakt","Offene_positive_Ereignisse","Nachweis"],full),
        "Zukunftsregister.tsv":tsv(["Zukunft","Praeparation","Vorauswahl","Ordnungen","Kragen_ausschluss","Sonde_ausgeschlossen",
                                   "Sonde_existiert","Sonde_offen","Zeitliche_Koinzidenz_offen","Verankerter_Kontakt_offen"],short)}

if __name__=="__main__":
    if not __debug__:raise RuntimeError("Ohne -O ausführen")
    ap=argparse.ArgumentParser()
    ap.add_argument("--ausgabe",action="store_true")
    write=ap.parse_args().ausgabe
    for filename,content in build().items():
        if write:(ROOT/filename).write_bytes(content.encode())
        else:assert (ROOT/filename).read_bytes()==content.encode(),filename
    print("Alle 2 320 Ordnungen für beide Präparationen geprüft. Verankerter Kontakt in keinem Fall.")
