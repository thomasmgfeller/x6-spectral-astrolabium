"""Bounded tensor quadrature of the original four-inner-clock action."""
import itertools
import numpy as np
from families import scalar, P, F
from clocks import quadrature, STEP, BETA, density_factor, RHO


def point_integral(layout,t,n):
    inner,b,gravity=layout
    x,w=quadrature(n)
    fixed={j:(j-5)*STEP for j in (*P,*F)}
    fixed[3]=t
    def between_fixed(j):
        return 1+BETA/2*sum(v*(fixed[j]-fixed[i])**2 for (i,k),v in b.items()
                              if k==j and i in fixed and v)
    past=sum(between_fixed(j) for j in P)
    future_const=sum(between_fixed(j) for j in F)
    size=len(inner)
    # Separate each future-row term incident on an inner node into its own
    # one-variable phase. Slabs cap the largest temporary even on the fine grid.
    axis=1.5*x
    unary={i:w*np.exp(-1j*BETA/32*sum(b[i,j]*(fixed[j]-axis)**2 for j in F)) for i in inner}
    weight=0j
    chunk=max(1,750000//n**(size-1))
    for first in range(0,n,chunk):
        grids={}; products=1
        for k,j in enumerate(inner):
            sl=slice(first,min(first+chunk,n)) if k==0 else slice(None)
            shp=[1]*size; shp[k]=-1
            grids[j]=axis[sl].reshape(shp)
            products=products*unary[j][sl].reshape(shp)
        for j in inner:
            c=1
            for (i,k),v in b.items():
                if k==j and v:
                    other=fixed[i] if i in fixed else grids[i]
                    c=c+(BETA*v/2)*(grids[j]-other)**2
            products*=density_factor(c)
        weight+=products.sum()
    return past,np.exp(1j*(gravity-future_const/16))*weight


def direct_reference(layout,t,n):
    inner,b,grav=layout;x,w=quadrature(n)
    times={j:(j-5)*STEP for j in (*P,*F)};times[3]=t
    total=0j
    for indices in itertools.product(range(n),repeat=len(inner)):
        times.update({j:1.5*x[k] for j,k in zip(inner,indices)})
        C={j:1+BETA/2*sum(v*(times[j]-times[i])**2 for (i,end),v in b.items() if end==j)
           for j in (*inner,*F)}
        total+=np.prod(w[list(indices)])*np.prod([density_factor(C[j]) for j in inner])*np.exp(-1j*sum(C[j] for j in F)/16)
    return np.exp(1j*grav)*total


def packet(layout,n,m):
    x,w=quadrature(m);norm=np.sqrt(1/48/32);lobe=[];comp=[]
    for side in (-1,1):
        rows=[point_integral(layout,-2*STEP+side/16+v/32,n) for v in x]
        b=np.array([v[0] for v in rows]);a=np.array([v[1] for v in rows])
        lobe.append([norm*((w*np.exp(-0.5j*r*b)*np.sinc(b/(64*np.pi)))@a) for r in RHO])
        comp.append(norm*(w@a))
    return np.array(lobe).T, sum(comp)/np.sqrt(2),point_integral(layout,-2*STEP,n)


def pack_amplitude(value):
    lob,comp,(b,fix)=value
    pair=lambda x:[float(x.real),float(x.imag)]
    return {"lobes":[[pair(x) for x in row] for row in lob],"compensated":pair(comp),"B":float(b),"fixed":pair(fix)}


def decode(row):
    return np.array([[complex(*z) for z in l] for l in row['lobes']]),complex(*row['compensated']),(row['B'],complex(*row['fixed']))


def evaluate_grids(names):
    results={};audit={}
    for nm in names:
        layout=scalar.order(nm)
        low_order=point_integral(layout,-2*STEP+1/16,4)[1]
        independent=direct_reference(layout,-2*STEP+1/16,4)
        assert abs(low_order-independent)<1e-13
        # Relabel all inner events with a nontrivial permutation, keeping collars fixed.
        inner,b,grav=layout
        labels=dict(zip(inner,inner[1:]+inner[:1]))
        alt={ (labels.get(i,i),labels.get(j,j)):v for (i,j),v in b.items()}
        relabel=point_integral((inner,alt,grav),-2*STEP+1/16,7)[1]
        ref=point_integral(layout,-2*STEP+1/16,7)[1]
        assert abs(relabel-ref)<1e-13
        rows=[]
        for n,m in ((32,6),(48,8),(64,10),(80,12)):
            amp=packet(layout,n,m)
            v=np.r_[amp[0].ravel(),amp[1],amp[2][1]]
            rows.append({"grid":[n,m],"amplitudes":pack_amplitude(amp)})
            if len(rows)>1:
                maxdiff=float(np.max(abs(v-old)))
                rows[-1]["change_including_sharp_amplitude"]=maxdiff
                if maxdiff<3e-10:break
            old=v
        if maxdiff>=3e-10:raise ArithmeticError(f"unresolved quadrature for {nm}: {maxdiff}")
        results[nm]=rows
        audit[nm]={"direct_point_check":float(abs(low_order-independent)), "relabelled_clock_check":float(abs(relabel-ref))}
    return results,audit
