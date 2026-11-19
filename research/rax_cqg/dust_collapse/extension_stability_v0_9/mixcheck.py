"""Independent floating-point LP on the two parent simplices, checked against exact floors."""
from fractions import Fraction as F
import numpy as np
from scipy.optimize import linprog
from reference import ROOT, SOURCE, full, save_json
from bounds import inputs, GRIDS
from teiltraeger import names_and_reach

def calculate():
    evidence=full.read(ROOT/"planes.json")
    extra=full.read(ROOT/"support_rows.json")
    prior,_=names_and_reach()
    lookup={s:i for i,s in enumerate(prior)}
    rows=[0,1]+[lookup[f"N14_{m}"] for m in (734,760,8191)]
    stored=np.load(SOURCE/"gram.npy").sum(axis=0)
    support=set(evidence["outside_types"])
    reserve=set(evidence["reserve_outside_types"])
    answer={}
    for tag in GRIDS:
        names,reach,_,cols,known,cap,rad=inputs(tag)
        col=np.zeros((5,len(names)),complex)
        for j,s in enumerate(names):
            if s in lookup:
                col[:,j]=stored[rows,lookup[s]]
            else:
                col[:2,j]=np.asarray([[complex(*z) for z in c[:2]] for c in cols[j]]).sum(axis=0)
                col[2:,j]=np.asarray([[complex(*z) for z in r] for r in extra[s]]).sum(axis=1)
        ids=np.array(reach[0]+reach[1])
        nr=len(reach[0])
        eq=np.zeros((2,len(ids)));eq[0,:nr]=1;eq[1,nr:]=1
        for d,weights in enumerate(([.202741,.693388,.103871],[.201682,.691688,.106630])):
            case=evidence["grid_cases"][f"{tag}_{d}"]
            b=np.r_[[complex(*known[k][d])/2 for k in (0,1)],np.zeros(3)]
            q=.95*b
            q[2:]=[.05*w*complex(*known[names.index(prior[k])][d]) for w,k in zip(weights,rows[2:])]
            anchor=stored[np.ix_(rows,rows)]
            p=np.vdot(b,anchor@b).real
            qb=np.vdot(q,anchor@b).real
            qq=np.vdot(q,anchor@q).real
            h=q.conj()@col
            amp=[complex(*a[d]) if a is not None else 0j for a in known]
            radii=[float(r if a is not None else c) for r,a,c in zip(rad,known,cap)]
            lower=((h*np.array(amp)).real-abs(h)*radii)/p
            def lp(bad,allow):
                indicator=np.array([names[i] in bad for i in ids],dtype=float)
                sol=linprog(lower[ids],A_eq=eq,b_eq=[.5,.5],A_ub=indicator[None,:],
                            b_ub=[allow],bounds=(0,None),method="highs")
                if not sol.success or max(abs(eq@sol.x-.5))>1e-9 or indicator@sol.x>allow+1e-9:
                    raise ArithmeticError("Mixture LP")
                return (2*.95*qb-qq)/p+.1*sol.fun
            limits={"all":lp(set(),1.),"safe":lp(support,0.),
                    "safe_plus_outside":lp(support,evidence["outside_transfer_share_per_million_at_five"]/1e6),
                    "reserve_plus_outside":lp(reserve,evidence["reserve_outside_share_per_million_at_five"]/1e6)}
            for k,ref in (("all","all_success_floor_at_five"),("safe","safe_success_floor_at_five")):
                if abs(limits[k]-float(F(case[ref])))>1e-10:
                    raise ArithmeticError(("Independent projection floor",k))
            if min(limits[k] for k in limits if k!="all")<.9-1e-11:
                raise ArithmeticError("Controlled mixture")
            answer[f"{tag}_{d}"]=limits
    return answer

if __name__=="__main__":
    save_json(ROOT/"mixcheck.json",calculate())
