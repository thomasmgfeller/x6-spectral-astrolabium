"""Post-freeze diagnosis of the archived witnesses; does not change the test."""
from pathlib import Path
from fractions import Fraction as F
import json
import refined
from intervals import I,precision

ROOT=Path(__file__).resolve().parent


def residuals(cells):
    counts=[]
    for j in range(20):
        f=sum((F(cells[b])*int(refined.C[j,b]) for b in range(20)),F(0))
        counts.append(I(int(f.numerator))/int(f.denominator))
    model=refined.previous.baseline
    s={model.PAIRS[k]:-counts[j].sqrt() for j,k in enumerate(model.PRED)}
    G=[[(s[(0,i)]+s[(0,j)]-(I(0) if i==j else s[tuple(sorted((i,j)))]))/2
         for j in range(1,5)] for i in range(1,5)]
    L=[[I(int(i==j)) for j in range(4)] for i in range(4)];D=[]
    for i in range(4):
        pivot=G[i][i]-sum((L[i][k].square()*D[k] for k in range(i)),I(0))
        assert pivot.hi<0 if i==0 else pivot.lo>0
        D.append(pivot)
        for j in range(i+1,4):
            L[j][i]=(G[j][i]-sum((L[j][k]*L[i][k]*D[k] for k in range(i)),I(0)))/pivot
    out=[]
    for target in [5,6]:
        b=[(s[(0,i)]+s[(0,target)]-s[(i,target)])/2 for i in range(1,5)]
        z=[]
        for i in range(4):z.append(b[i]-sum((L[i][k]*z[k] for k in range(i)),I(0)))
        # b^T G^-1 b = sum_i (L^-1 b)_i^2 / D_i.
        residual=sum((z[i].square()/D[i] for i in range(4)),I(0))-s[(0,target)]
        out.append(residual)
    return out


def main():
    precision(60)
    gs=json.loads((ROOT.parent/'poisson_v0_2/geometries.json').read_text())
    exact_controls=0
    for g in gs:
        a=[F(x) for x in g['atom_ratios']]
        y=[268435456*a[k] for k in refined.previous.KEEP]+[268435456*sum(a[k] for k in refined.previous.MERGED)]
        for r in residuals(y):assert r.lo<=0<=r.hi;exact_controls+=1
    records=[]
    for row in json.loads((ROOT/'REGION_WITNESSES.json').read_text())['records']:
        for i,a in enumerate(row['alternatives']):
            rs=residuals(a['means'])
            excluded=any(not (r.lo<=0<=r.hi) for r in rs)
            assert excluded
            records.append({'geometry':row['geometry'],'alternative':i,
                            'necessary_norm_residuals':[{'lower':str(r.lo),'upper':str(r.hi)} for r in rs],
                            'excluded_from_exact_flat_landmark_model':excluded})
    out={'status':'PASS_NONREALIZABILITY_DIAGNOSIS','stage':'post-freeze diagnostic; no changes to the fresh experiment',
         'exact_geometry_norm_controls':exact_controls,'excluded_witness_means':len(records),'records':records,
         'limit':'Only the ten explicit unrestricted-region witnesses are excluded. No tighter certified estimator is implemented by this diagnosis.'}
    (ROOT/'REALIZABILITY.json').write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps({k:v for k,v in out.items() if k!='records'},indent=2))


if __name__=='__main__':main()
