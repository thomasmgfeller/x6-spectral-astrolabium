"""Second scalar calculation: integrate all variables at positive Abel damping.

No stationary elimination, projection of delta rows or symplectic-map formula is
used in this test. The two algorithms share the declared order and boundary data.
"""
import json
from pathlib import Path
import mpmath as mp
import geometry as g

ROOT=Path(__file__).resolve().parent


def numerical_state(name,eps):
    inner,coeffs,_=g.order(name)
    n=len(inner); dim=n+8
    # Use the index order (x, inner fields, two gauge parameters, y).
    vectors={}
    for j in (*g.P,*inner,*g.F):
        v=mp.matrix(dim,1)
        if j in g.P:
            if j>0: v[j-1]=1
            v[3+n]=int(g.BM[j])
        elif j in g.F:
            if j<10: v[dim-3+j-7]=1
            v[4+n]=int(g.BP[j-7])
        else: v[3+inner.index(j)]=1
        vectors[j]=v
    H=mp.matrix(dim)
    for (i,j),b in coeffs.items():
        d=vectors[j]-vectors[i]
        H-=mp.mpf(b)/2*(d*d.T)
    H[3+n,3+n]-=int(g.AM.dot(g.BM)); H[4+n,4+n]+=int(g.AP.dot(g.BP))
    for j in range(3):
        H[3+n,j]-=int(g.AM[j+1]); H[j,3+n]-=int(g.AM[j+1])
        H[4+n,dim-3+j]+=int(g.AP[j]); H[dim-3+j,4+n]+=int(g.AP[j])
    Q=-1j*H
    for j in range(dim-3): Q[j,j]+=1 if j<3 else eps
    h=dim-3; A=Q[:h,:h]
    eff=Q[h:,h:]-Q[h:,:h]*(A**-1)*Q[:h,h:]
    prec=4/mp.sqrt(6)*eff
    pref=1/g.continued_sqrt(A)
    phase=pref/abs(pref)
    return prec,phase


def check():
    mp.mp.dps=80; out={}
    for name in ("chain","one","fork","join","chain_lift"):
        _,state=g.kernel(name,True)
        ref,amp=state
        errors=[]
        for eps in ["1e-12","1e-20","1e-28"]:
            P,phase=numerical_state(name,mp.mpf(eps))
            errors.append({"epsilon":eps,"max_precision_entry_error":float(max(abs(z) for z in P-ref)),
                           "unit_phase_error":float(abs(phase-amp/abs(amp)))})
        assert errors[-1]["max_precision_entry_error"] < 1e-18
        assert errors[-1]["unit_phase_error"] < 1e-18
        out[name]=errors
    return out


if __name__=="__main__":
    import argparse
    parser=argparse.ArgumentParser()
    parser.add_argument("--output",type=Path)
    args=parser.parse_args()
    output=check()
    if args.output: args.output.write_text(json.dumps(output,indent=2)+"\n")
    print(json.dumps({k:v[-1] for k,v in output.items()},indent=2))
