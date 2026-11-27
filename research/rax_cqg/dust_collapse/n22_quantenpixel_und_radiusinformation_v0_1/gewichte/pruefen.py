"""Exakte Diagnose der Endtypgewichte auf dem publizierten N15-Träger."""
from collections import Counter
from fractions import Fraction as F
from hashlib import sha256
import json
from pathlib import Path
import sys
from tempfile import TemporaryDirectory
from zipfile import ZipFile

HERE = Path(__file__).resolve().parent
SOURCE = HERE / 'quellen'
ZIP = SOURCE / 'CST_DUST_Praefix_1564_Vier_Marken_v0_1.zip'
CERTS = SOURCE / 'weight_certificates.json'
PREFIX = 1564


def rank(rows):
    basis = {}
    for row in rows:
        row = list(row)
        for pivot in sorted(basis):
            row = [a-row[pivot]*b for a,b in zip(row,basis[pivot],strict=True)]
        first = next((j for j,v in enumerate(row) if v),None)
        if first is not None:
            basis[first] = [v/row[first] for v in row]
    return len(basis)


def verify():
    assert sha256(ZIP.read_bytes()).hexdigest() == '72c671b458f2d2d0681cfe84b21faf1fbdb1f13fd7b0fdba4e50d7088f2a90f3'
    assert sha256(CERTS.read_bytes()).hexdigest() == '04dd9b3db5e59f28fe585f0ac913a8112cc7fd87a91e9d9e69a0c2d4a2def2da'
    with TemporaryDirectory() as tmp, ZipFile(ZIP) as z:
        for name in ('extension.py','verify.py','catalog.json',
                     'CST_DUST_Praefix_1564_Selektionsgleichung_v0_1_Pruefpaket.zip'):
            z.extract(name,tmp)
        sys.path.insert(0,tmp)
        try:
            from extension import MASK, build_columns, load_inputs, marked_three
            from verify import deletion_catalogue
            data,residual,weights,catalog = load_inputs()
            reps,codes,parents,_ = marked_three(data,residual,weights)
            valid = set(build_columns(reps,codes,catalog))
            assert valid == deletion_catalogue(codes,catalog)
        finally:
            sys.path.pop(0)
    assert len(valid)==928 and len(parents)==72
    coeff = {}
    for key in sorted(valid):
        old,local = Counter(),Counter()
        for rep in key:
            end,orbit = reps[rep]
            assert len(orbit)>0 and 6%len(orbit)==0
            for raw in orbit:
                pr = raw & MASK
                old[pr] += 6//len(orbit)
                if pr==PREFIX:
                    local[end] += 6//len(orbit)
        assert sum(old.values())==24 and sum(local.values())==old[PREFIX]
        coeff[key] = old,local
    ends = sorted({j for old,local in coeff.values() for j in local})
    assert len(ends)==10
    def project(sparse, floor=F(0)):
        extra = {tuple(map(int,key.split(','))):F(v) for key,v in sparse.items()}
        assert set(extra)<=valid and floor>=0
        vec = ({k:floor+extra.get(k,0) for k in valid} if floor else extra)
        assert vec and set(vec)<=valid and min(vec.values())>0 and sum(vec.values())==1
        for p in parents:
            assert sum(w*coeff[key][0][p] for key,w in vec.items())==24*parents[p]
        pvec = [sum(w*coeff[key][1][j] for key,w in vec.items())/(24*parents[PREFIX]) for j in ends]
        assert min(pvec)>=0 and sum(pvec)==1
        return pvec
    published = json.loads(CERTS.read_text())
    assert set(published)=={str(j) for j in ends}
    vertices=[]
    for j in ends:
        doc=published[str(j)]
        pvec=project(doc['primal'])
        dual = {sorted(parents)[int(k)]:F(y) for k,y in doc['dual'].items()}
        assert all(sum(n*dual.get(p,0) for p,n in old.items())>=loc[j] for old,loc in coeff.values())
        assert sum(parents[p]*y for p,y in dual.items())/parents[PREFIX]==pvec[ends.index(j)]
        vertices.append(pvec)
    assert rank([[a-b for a,b in zip(v,vertices[0],strict=True)] for v in vertices[1:]])==9
    uniform = json.loads((HERE/'Gleichverteilung.json').read_text())
    pu = project(uniform)
    full = json.loads((HERE/'Gleichverteilung_strikt.json').read_text())
    floor = F(full['basisgewicht_je_spalte'])
    assert floor==F(1,1000000) and len(full['zusaetzlich'])==47
    assert all(F(v)>0 for v in full['zusaetzlich'].values())
    assert project(full['zusaetzlich'],floor)==pu
    p0 = vertices[ends.index(766)]
    assert pu==[F(1,10)]*10 and p0==[F(1)*(j==766) for j in ends]
    impurity = lambda v:1-sum(x*x for x in v)
    # A polynomial identity in t, checked at three distinct points (degree at most 2).
    for t in (F(0),F(1,3),F(1)):
        mixed=[(1-t)*a+t*b for a,b in zip(p0,pu,strict=True)]
        assert impurity(mixed)==F(9,10)*(2*t-t*t)
    def logically_assigned_radius(m,root_mass,k):
        x=F(1,2)
        return 10*(1-root_mass*x/6-m*x**2/144-k*(4-m)*x**3)
    deltas = [logically_assigned_radius(F(4),F(2),k)-logically_assigned_radius(F(1,4),F(1,2),k)
              for k in (F(0),F(1,3))]
    assert deltas==[F(-505,384),F(95,384)]
    return {'n13_praefix':PREFIX,'n15_endtypen':ends,'affine_dimension':9,'globale_spalten':len(valid),
            'feste_praefixmassen':len(parents),'positive_spalten_des_gleichverteilten_zeugen':len(uniform),
            'strikter_zeuge':{'positive_spalten':len(valid),'basisgewicht_je_spalte':str(floor),'positive_zuschlaege':len(full['zusaetzlich'])},
            'diagonale_endtypgroesse':{'minimum_abgeschlossen':'0','infimum_strikt_positiv':'0','maximum_beider_klassen':'9/10','kurve':'9/10*(2*t-t^2)'},
            'logische_radiusdifferenzen':[str(v) for v in deltas]}


if __name__=='__main__':
    if not __debug__:
        raise RuntimeError('Python ohne -O ausführen')
    print(json.dumps(verify(),indent=2,ensure_ascii=False))
