"""Replay the publication with Python 3.10+ and its standard library."""
import argparse
from collections import Counter
from fractions import Fraction as F
import gzip
from hashlib import sha256
import json
from pathlib import Path
import subprocess
import sys
from tempfile import TemporaryDirectory
from zipfile import ZipFile
from erweiterung import ROOT, R, OLD, Z, box, Box, extensions, solve, study
from schicht import inside_layer
from schalen import generate, locate, estimate, tracer_faces, transfers
import vorlaeufer

TARGETS=(F(1,4),F(1,2),F(3,4))
OFFSET=Box.hull(F(1,6)-F(1,2**22),F(1,6)+F(1,2**22))
SOURCES={
    'CST_DUST_P3_Arealradius_und_Schalenauslese_N15_Pruefpaket.zip':
        'd58024f86a668f8a786a855b93dcae0c6471dbc8efef4eade16c010b979abdf3',
    'CST_DUST_Materie_Vakuum_und_Masseneichung_Pruefpaket.zip':
        'a4d5e9516e5807a3c564d2c8fde8a2299ca3981f0e5c8654836571b357ee366c'}


def sources():
    assert sha256((ROOT/'Pruefplan.md').read_bytes()).hexdigest()=='ed61d5919bd0575a56625dc8b3ce18503e6914bf662be7169deaf19cec84bc2a'
    assert sha256((ROOT/'Zusatzplan.md').read_bytes()).hexdigest()=='1bcd62a741d4c424d75101ba095d40a044cf89e5421ebdc514fe62e2df000338'
    for i,(name,digest) in enumerate(SOURCES.items()):
        p=ROOT/'quellen'/name
        assert sha256(p.read_bytes()).hexdigest()==digest
        with ZipFile(p) as z, TemporaryDirectory() as tmp:
            z.extractall(tmp)
            if i==0:
                base=Path(tmp)/'oberflaeche'
                assert (ROOT/'basis/auslesen.py').read_bytes()==(base/'quellen/auslesen.py').read_bytes()
                assert (ROOT/'basis/intervall.py').read_bytes()==(base/'basis/intervall.py').read_bytes()
                subprocess.run([sys.executable,'-B','pruefen.py'],cwd=base,check=True,stdout=subprocess.PIPE)
                ledger=json.loads((base/'basis/quellen/inputs/checkpoints.json').read_bytes())
                assert len(ledger)==60 and all(row['execution']=='NOT_RUN' for row in ledger)
                # Rebuild the canonical old relation and interval fields using the pinned original.
                source="""from randdichte import *
import json
r,_,y,w,_=construct(box(F(1,6)),True)
def data(m):
 return {str(j):[str(F(v.lo,SCALE)),str(F(v.hi,SCALE))] for j,v in m.items()}
print(json.dumps({'order':sorted(r),'past':P,'future':FUT,'inner':I,'type':1767356,'positive_fields_midpoint':data(w),'clock_midpoint':data(y)}))"""
                rebuilt=subprocess.check_output([sys.executable,'-B','-c',source],cwd=base/'basis')
                assert json.loads(rebuilt)==json.loads((ROOT/'basis/zweig.json').read_bytes())
            else:
                assert (ROOT/'basis/klassik.py').read_bytes()==z.read('klassik.py')


def window(r,a,b,level=0):
    rows,unknown=solve(r,OFFSET,Box.hull(a,b),False)
    distances=[max(F(row['flux'][0]),-F(row['flux'][1]),F(0)) for row in rows]
    if not unknown and all(distances):
        return [{'x':[str(a),str(b)],'clock_branches_enclosed':len(rows),
                 'min_abs_gradient_lower':str(min(distances)) if distances else None}]
    if level>=12:
        return [{'x':[str(a),str(b)],'unresolved':True}]
    c=(a+b)/2
    return window(r,a,c,level+1)+window(r,c,b,level+1)


def enumerate_independently():
    # Assign the three types incrementally. A chain i<j must respect the
    # order past/incomparable/future. A past+future pair needs an old relation.
    order=sorted(OLD,key=lambda i:sum(v==i for _,v in R))
    result=set()
    def visit(idx,assigned):
        if idx==len(order):
            result.add((tuple(sorted(i for i,v in assigned.items() if v==-1)),
                        tuple(sorted(i for i,v in assigned.items() if v==1))))
            return
        i=order[idx]
        for k in (-1,0,1):
            if any(((u,i) in R and role>k) or ((i,u) in R and k>role)
                   or (role==-1 and k==1 and (u,i) not in R)
                   or (k==-1 and role==1 and (i,u) not in R)
                   for u,role in assigned.items()):continue
            visit(idx+1,{**assigned,i:k})
    visit(0,{})
    return result


def run(save):
    sources()
    ext=list(extensions())
    assert {(tuple(sorted(p)),tuple(sorted(f))) for p,f,r in ext}==enumerate_independently()
    assert len(ext)==227 and sum(bool(p and f) for p,f,r in ext)==182
    midpoint={};windows={}
    for x in TARGETS:
        mid=study(box(F(1,6)),box(x),True)
        assert all(not u['unresolved'] and all(not b['bounds_only'] for b in u['branches']) for u in mid['cases'])
        assert not mid['counts'].get('possibly_zero',0)
        midpoint[str(x)]=mid
        cert=[]
        for p,f,r in ext:
            if not p or not f:continue
            leaves=window(r,x-F(1,64),x+F(1,64))
            assert not any(c.get('unresolved') for c in leaves)
            cert.append({'past':sorted(p),'future':sorted(f),'domains':leaves})
        windows[str(x)]=cert
    layer=inside_layer(OFFSET)
    assert not layer['unresolved'] and layer['old_ideals']==23 and len(layer['candidates'])==9
    distances={str(x):min(max(F(r['relative_time'][0])-x,x-F(r['relative_time'][1]),F(0))
                          for r in layer['candidates']) for x in TARGETS}
    assert all(d>F(1,64) for d in distances.values())
    two=vorlaeufer.run()
    assert not two['open'] and not two['ambiguous'] and 'possibly_zero' not in two['counts']
    frames,radii,flow=generate()
    path=ROOT/'Schalen_und_Tracer.json.gz'
    encoded=json.dumps(frames,sort_keys=True,separators=(',',':')).encode()
    if save:path.write_bytes(gzip.compress(encoded,mtime=0))
    assert gzip.decompress(path.read_bytes())==encoded
    previous=None;fidx=0
    for raw,reference in zip(json.loads(gzip.decompress(path.read_bytes())),radii):
        assert tuple(raw['marks'])==locate(raw['occupied'])
        assert estimate(raw['reading'])['radius']==reference['radius']
        fresh=tracer_faces(raw['tracer'])
        if raw['x']!='0':
            assert transfers(previous,fresh,list(map(F,raw['tracer']['weights'])))==flow[fidx]['inner_outer_fixedR6_in_out']
            fidx+=1
        previous=fresh
    assert fidx==len(flow)==12 and len(radii)==15 and max(r['max_error'] for r in radii)<0.05
    return {'git_base':'d90912e79a2b640549cc184ade4530282b92964b','N16_central':midpoint,'N16_windows':windows,
            'same_slice':layer,'same_slice_distance_lower':{k:str(v) for k,v in distances.items()},
            'N17_predecessor':two,'classical_radii':radii,'classical_flux':flow,
            'raw_sha256':sha256(encoded).hexdigest(),'physical_P3':'HOLD_NOT_ELIGIBLE','physical_not_run':60}


if __name__=='__main__':
    if not __debug__:raise SystemExit('Python ohne -O starten.')
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--erzeugen',action='store_true')
    args=parser.parse_args()
    file=ROOT/'Ergebnisse.json'
    result=run(args.erzeugen)
    data=(json.dumps(result,indent=2,sort_keys=True,ensure_ascii=False)+'\n').encode()
    if args.erzeugen:file.write_bytes(data)
    elif file.read_bytes()!=data:raise SystemExit('Ergebnisse weichen ab.')
    print('PASS: N15-Ursprung, N16-Einfügungen und Uhrfenster, positive Schicht, N17-Vorläufer, 15 klassische Schalen- und 12 Flussvergleiche. Physische P3-Einträge: 60 × NOT_RUN.')
