"""Load the pinned N21 publication and enumerate all anchored projections."""
from contextlib import contextmanager
from hashlib import sha256
from pathlib import Path
from tempfile import TemporaryDirectory
from zipfile import ZipFile
import sys

ROOT = Path(__file__).resolve().parent
PIN = '3b5ab2685aa41d00467c36be43832f8f16b82628536946e9c52d480c7929e06a'
EARLY = 15
LATE = sum(1<<j for j in (7,8,9,10))
DEVICE = sum(1<<j for j in (15,16,17,18))
MATERIAL = (1<<19)-1-(1<<15)-(1<<17)


@contextmanager
def source():
    path=ROOT/'basis/N21.zip'
    assert sha256(path.read_bytes()).hexdigest()==PIN
    with TemporaryDirectory() as td, ZipFile(path) as archive:
        archive.extractall(td)
        sys.path.insert(0,td)
        try:
            from eingaben import data
            yield data(),Path(td)
        finally:
            sys.path.remove(td)


def projections(order):
    """Two constructions of ideals; enumeration in lexicographic bitmask order."""
    past=[sum(1<<i for i,k in order if k==j) for j in range(19)]
    def ideals(seq):
        down=[0]
        for j in sorted(range(19), key=lambda i:seq[i].bit_count()):
            down += [s | 1<<j for s in down if not seq[j]&~s]
        return set(down)
    down=ideals(past)
    future=[sum(1<<k for i,k in order if i==j) for j in range(19)]
    up=ideals(future)
    assert {((1<<19)-1)^p for p in down}==up
    candidates=[]
    for p in down-{0}:
        allowed=(1<<19)-1
        for i in range(19):
            if p&(1<<i):allowed &= future[i]
        candidates.extend((p,f) for f in up if f and f&~allowed==0)
    cand=sorted(candidates)
    result=[(p,f,q,g) for p,f in cand for q,g in cand if
            not(p&g or q&f) and p&q&MATERIAL and f&g&MATERIAL]
    assert len(result)==406142
    return result


def prefilter(row,family):
    p,f,q,g=row
    if (p|q)&LATE or (f|g)&EARLY:return 'T'
    if family=='A' and not g&~LATE:return 'G20'
    if family=='B' and not p&DEVICE:return 'D19'
    return ''


def write_input(d,rows,path):
    with path.open('w') as f:
        print(len(d['order']),file=f)
        for edge in d['order']:print(*edge,file=f)
        for j,v in d['collar'].items():print(j,*v,file=f)
        for j,v in d['native'].items():print(j,*v,file=f)
        print(*d['window'],file=f);print(len(rows),file=f)
        for row in rows:print(*row,file=f)
