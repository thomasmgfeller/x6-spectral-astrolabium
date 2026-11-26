"""Rebuild the full labelled register and certified collar from the archived inputs."""
from fractions import Fraction
from hashlib import sha256
from pathlib import Path
from tempfile import TemporaryDirectory
from zipfile import ZipFile
import sys
import json

ROOT = Path(__file__).resolve().parent
PIN = 'c6e266b6a00e25e1e94287fbe6272392a3168c62e518c8821ac9e8219652a5a4'
SCALE = 10**9
MATERIAL = sum(1 << j for j in range(19) if j not in (15, 17))
EARLY = 15
LATE = sum(1 << j for j in (7, 8, 9, 10))
DEVICE = sum(1 << j for j in (15, 16, 17, 18))


def mask(nodes):
    return sum(1 << j for j in nodes)


def enumerate_rows(order, ideals):
    nodes = set(range(19))
    down = ideals(order, nodes)
    up = ideals({(j,i) for i,j in order}, nodes)
    records = sorted((mask(p), mask(f)) for p in down for f in up
                     if p and f and all((i,j) in order for i in p for j in f))
    rows = [(pn,fn,pz,fz) for pn,fn in records for pz,fz in records
            if pn & DEVICE and not ((pn|pz) & LATE or (fn|fz) & EARLY)
            and fz & ~LATE and not (fn & pz or fz & pn)
            and pn & pz & MATERIAL and fn & fz & MATERIAL]
    assert len(rows) == len(set(rows)) == 42716
    return rows


def data():
    archive = ROOT/'basis/Ankerpaket.zip'
    assert sha256(archive.read_bytes()).hexdigest() == PIN
    with TemporaryDirectory() as temp, ZipFile(archive) as z:
        z.extractall(temp)
        p = Path(temp)
        sys.path[:0] = [str(p), str(p/'basis')]
        try:
            from randdaten import collect
            from ordnungen import ideals, two_station_register, coefficients
            from zweipunkt import branch, screen_native_pasts
            from freie_felder import solve_quadratic, COLLAR, DUST
            from auslese import target, affine
            from intervall import I
            order, y, w, _, cells, routes = collect()
            assert cells == 168
            from empfangsbit import K0,V
            from driftfamilie import LABELS
            k=Fraction(1,10**11);vmax=Fraction(112,10**14)
            assert K0==k and 112*V==vmax and max(abs(j) for j in LABELS)==Fraction(1,10**6)
            assert 4*k*(11+vmax)<Fraction(10,SCALE)
            assert 2*121*k+max(LABELS)+3*k*vmax**2/Fraction(1,10**8)**2<Fraction(2001,SCALE)
            assert 19-20*16*11**2 > -100000
            old=json.loads((p/'Ergebnisse.json').read_text())
            assert two_station_register(order)==old['two_point_filter_register']
            used=[(a,b,probe) for track in routes for a,b,probe in track if probe]
            assert used==[(16,16,(15,16)),(18,18,(16,18)),(18,18,(17,18)),(7,7,(18,7))]
            assert all([b for a,b,probe in track]==[1,2,16,18,7] for track in routes)
            rev={(j,i) for i,j in order}
            native,_=branch(order,y)
            past14={i for i,j in order if j==14}
            roots=solve_quadratic(coefficients(rev,past14),native)
            roots=[t for t in roots if t.h>max(native[i].l for i in past14) and t.l<y[7].h]
            assert len(roots)==1
            native[14]=roots[0]
            window=target(y)
            assert all(y[j].h<window.l for j in (0,1,2,3))
            assert all(y[j].l>window.h for j in (7,8,9,10))
            assert all(y[j].l>=-5*10**12 and y[j].h<6*10**12 for j in COLLAR)
            assert all(w[j].l>0 and w[j].h<10**12 for j in COLLAR)
            assert all((0,j) in order and (j,7) in order for j in range(19) if j not in COLLAR)
            past_cases=screen_native_pasts(order,{i:y[i] for i in COLLAR})
            assert len(past_cases)==18 and all(row['reason'] in ('past_outside_window','no_target_root','residual_sign') for row in past_cases)
            collar_checks={}
            for j in (7,8,9,10):
                future=set(range(j,11))
                g=affine(coefficients(order,future),y,w,window)
                assert not g.haszero()
                collar_checks[j]=g.endpoints()
            wide_y=dict(y);wide_w=dict(w)
            for j in (7,8,9,10):wide_w[j]+=I.enclose(Fraction(-1,10**6),Fraction(1,10**6))
            for j in (8,9,10):wide_y[j]+=I.enclose(Fraction(-1,10**4),Fraction(1,10**4))
            wide_checks={}
            for j in (7,8,9,10):
                g=affine(coefficients(order,set(range(j,11))),wide_y,wide_w,window)
                assert not g.haszero() and wide_y[j].l>window.h
                wide_checks[j]=g.endpoints()
            rows=enumerate_rows(order,ideals)
            p3=json.loads((p/'basis/P3.json').read_text())
            assert len(p3)==60 and all(v['execution']=='NOT_RUN' for v in p3)
            def units(x):
                lo,hi=[Fraction(v)*SCALE for v in x.endpoints()]
                return [lo.numerator//lo.denominator,-(-hi.numerator//hi.denominator)]
            return dict(order=sorted(order),collar={i:[*units(y[i]),*units(w[i])] for i in COLLAR},
                        native={i:units(native[i]) for i in DUST},window=units(target(y)),
                        rows=rows, old=old['two_point_filter_register'],routes=routes,
                        wide_collar={i:[*units(wide_y[i]),*units(wide_w[i])] for i in COLLAR},
                        reference={i:[*units(y[i]),*units(w[i])] for i in range(19)},
                        early_proofs={'ancestral_ideals':past_cases,'collar_future_gradients':collar_checks,'wider_collar_gradients':wide_checks})
        finally:
            del sys.path[:2]


def write_input(d, path):
    with path.open('w') as f:
        print(len(d['order']),file=f)
        for edge in d['order']: print(*edge,file=f)
        for j,values in d['collar'].items(): print(j,*values,file=f)
        for j,values in d['native'].items(): print(j,*values,file=f)
        print(*d['window'],file=f)
        print(len(d['rows']),file=f)
        for row in d['rows']: print(*row,file=f)
