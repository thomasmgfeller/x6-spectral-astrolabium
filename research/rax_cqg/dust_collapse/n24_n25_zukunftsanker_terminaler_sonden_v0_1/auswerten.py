"""Verify the exact certificates and reproduce both output registers offline."""
import argparse
import csv
from collections import Counter
from fractions import Fraction as F
from io import StringIO
import json

from model import ROOT, COLLAR, EMPTY, WINDOW, ideals, inputs, minimal_anchor_orders
from schranken import ACTIVE, Form, constraints, initial_boxes, margin, moment_rows, with_terminal_clock


def tsv(rows):
    stream = StringIO()
    writer = csv.writer(stream, dialect="excel-tab", lineterminator="\n")
    writer.writerows(rows)
    return stream.getvalue()


def label(p):
    return ",".join(map(str, sorted(p))) or "∅"


def n24(pair, rel):
    old = ideals(rel, 22)
    with (ROOT/"input/Terminalregister.tsv").open() as fp:
        terminal = {(r["Vergangenheit"], r["Praeparation"]): r
                    for r in csv.DictReader(fp, delimiter="\t")}
    counts = Counter()
    rows = [["Alte_Vergangenheit_22", "N24_Ordnungen", "Partner18", "Partner19",
             "Mindestens_ein_Partner", "N23_Zeitstatus_schwer", "N23_Zeitstatus_leicht",
             "N24_stationaerer_Kontakt"]]
    for p in old:
        targets = [a for a in old if p <= a]
        complete = [q for q in (18, 19) if q not in p and
                    any((h,q) in rel and h not in EMPTY for h in p)]
        eligible = {q:sum(q in a for a in targets) for q in complete}
        count = sum(any(q in a for q in complete) for a in targets)
        states = [terminal[label(p),side]["Sonde_und_Materie"] for side in ("heavy","light")]
        counts["n24"] += len(targets)
        counts["n24_topology_q18_or_q19"] += count
        for side,state in zip(("heavy","light"), states):
            if state=="ZEUGE":
                counts["terminal_witness_"+side] += 1
                counts["n24_from_witness_"+side] += len(targets)
                counts["n24_topology_from_witness_"+side] += count
        rows.append([label(p),len(targets),eligible.get(18,0),eligible.get(19,0),
                     count,*states,"AUSGESCHLOSSEN"])
    assert len(old)==337 and len(terminal)==674
    return counts,tsv(rows)


def moment_replay(pair, side, q, ext, boxes, cert):
    for batch in cert["tighten"]:
        rows = moment_rows(pair,side,q,ext,boxes)
        next_boxes = boxes.copy()
        seen = set()
        for i, sign, value, weights in batch:
            assert i in boxes and sign in (1,-1) and (i,sign) not in seen
            seen.add((i,sign))
            val = F(value)
            opposite = sign*Form({f"y{i}":1})-val
            assert "opposite" not in weights
            assert margin(dict(rows,opposite=opposite),dict(weights,opposite="1"),boxes)>0
            lo,hi = next_boxes[i]
            next_boxes[i] = (max(lo,val),hi) if sign==1 else (lo,min(hi,-val))
        boxes = next_boxes
        assert all(a <= b for a,b in boxes.values())
    assert set(cert) == {"tighten","no"}
    assert margin(moment_rows(pair,side,q,ext,boxes),cert["no"],boxes)>0



def classify(pair, side, q, ext, cert):
    rows = constraints(pair,side,q,ext)
    if "linear" in cert:
        assert margin(rows,cert["linear"])>0
        return "Uhrgleichungen"
    if "bound" in cert:
        event,upper=cert.get("cap",[24,8])
        assert event in (23,24) and upper>0
        rows[f"y{event}ge{upper}"] = upper-Form({f"y{event}":1})
        assert margin(rows,cert["bound"])>0
        for j in set(ACTIVE)-COLLAR-{22,23,24}:
            assert (0,j) in ext and (j,7) in ext
        assert (22,23) in ext and (23,24) in ext
        boxes=initial_boxes(pair,side,upper,event)
        if cert.get("terminal21"):
            boxes=with_terminal_clock(boxes,ext)
        moment_replay(pair,side,q,ext,boxes,cert["moment"])
        return "Dichte_und_Uhrgleichungen"
    raise ValueError("Unvollständiges Zertifikat")


def verify(write=False):
    pair,rel=inputs()
    counts,table24=n24(pair,rel)
    proofs=json.loads((ROOT/"Zertifikate.json").read_text())
    order_rows=[["Nr","Partner","Alte_Vergangenheit_22","Alte_Vergangenheit_23",
                 "Alte_Vergangenheit_24","Praeparation","Kontakt","Begruendung"]]
    counts["terminal_n23"]=len(ideals(rel,22))
    used=set()
    for idx,(q,p,a,ext) in enumerate(minimal_anchor_orders(rel)):
        counts["n25_orders"]+=1
        counts[f"n25_orders_q{q}"]+=1
        for side in ("heavy","light"):
            key=f"{idx}/{side}"
            used.add(key)
            status=classify(pair,side,q,ext,proofs[key])
            verdict="AUSGESCHLOSSEN"
            counts[f"{side}/{status}"]+=1
            if p=={0}:
                counts[f"pilot/{side}/{verdict}"]+=1
            b={i for i in range(22) if (i,24) in ext}
            order_rows.append([idx,q,label(p),label(a),label(b),side,verdict,status])
    assert used==set(proofs)
    data=dict(sorted(counts.items()))
    data.update(input_commit="fb0631dc289f6f5c582052b7eba0ca9ba9bf0da3",
                physical_pilot_radii=[None]*8,physical_P3="NOT_RUN",physical_P3_count=60)
    output={"N24_Register.tsv":table24,"N25_Register.tsv":tsv(order_rows),
            "Ergebnisse.json":json.dumps(data,indent=2,ensure_ascii=False)+"\n"}
    for filename,content in output.items():
        if write:(ROOT/filename).write_bytes(content.encode())
        else:assert (ROOT/filename).read_bytes()==content.encode(),filename
    return data


if __name__=="__main__":
    if not __debug__:raise RuntimeError("Bitte ohne -O ausführen")
    parser=argparse.ArgumentParser()
    parser.add_argument("--ausgabe",action="store_true")
    print(json.dumps(verify(parser.parse_args().ausgabe),ensure_ascii=False,indent=2))
