"""Enumerate exact one-event extensions of the fixed 22-event strict order."""
from fractions import Fraction as Q
from hashlib import sha256
from io import BytesIO
from pathlib import Path
from zipfile import ZipFile
import json

ROOT = Path(__file__).resolve().parent
SOURCE = "6322d4784ded4dd443a78471e17087f82918c360d682de962e79f6b9ec14a711"
LAYERS = (1, -9, 16, -8, 0)
COLLAR = (0, 1, 2, 3, 7, 8, 9, 10)
EMPTY = (15, 17, 20, 22)
POS = (4, 5, 6, 11, 12, 13, 14, 16, 18, 19, 21)
DEVICE = ((15,16),(16,18),(17,18),(18,7))
LOW, HIGH = Q(15,32), Q(17,32)

def inputs():
    data = (ROOT/"basis/Fensterabstand.zip").read_bytes()
    assert sha256(data).hexdigest() == SOURCE
    with ZipFile(BytesIO(data)) as latest:
        previous = json.loads(latest.read("Ergebnisse.json"))
        with ZipFile(BytesIO(latest.read("basis/Innenfelder.zip"))) as coupled:
            cases = json.loads(coupled.read("Ergebnisse.json"))["cases"]
            with ZipFile(BytesIO(coupled.read("basis/Randgeometrie.zip"))) as geo:
                pair = json.loads(geo.read("basis/Vergleichspaar.json"))
                scan = json.loads(geo.read("Ergebnisse.json"))["comparison"]
    assert previous["mixed_contacts_excluded"] == 50
    return pair, cases, scan

def closures(rel):
    nodes = range(22)
    antichains = {()}
    for i in nodes:
        antichains |= {group+(i,) for group in antichains
                       if all((i,j) not in rel and (j,i) not in rel for j in group)}
    futures = {tuple(sorted(set(g)|{b for a,b in rel if a in g})) for g in antichains}
    pasts = {tuple(sorted(set(g)|{a for a,b in rel if b in g})) for g in antichains}
    return sorted(futures-{()},key=lambda f:(len(f),f)), sorted(pasts,key=lambda p:(len(p),p))

def compatible(rel, past, future):
    return all((i,j) in rel for i in past for j in future)

def coefficient(n):
    return LAYERS[min(n,4)]

def outgoing(rel, future):
    return {j:coefficient(sum((i,j) in rel for i in future)) for j in future}

def as_relation(rel, past, future):
    return rel|{(i,22) for i in past}|{(22,j) for j in future}

def coefficients(rel):
    rows = {}
    for i,j in rel:
        k = coefficient(sum((i,h) in rel and (h,j) in rel for h in range(23)))
        k -= Q((i,j) in DEVICE,10**11)
        if k:
            rows[i,j] = k
    return rows
