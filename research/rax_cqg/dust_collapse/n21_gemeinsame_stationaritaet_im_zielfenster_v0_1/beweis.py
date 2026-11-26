"""Uniform necessary conditions for all free interior fields at the archived collars."""
from fractions import Fraction as F
from pathlib import Path
import json,sys
from ordnung import orders,audit_action

ROOT=Path(__file__).resolve().parent
sys.path.insert(0,str(ROOT/'basis'))
from quellenpaket import model

def bounds(interval):
    return tuple(map(F,interval.data()))


def proof(Y,W,vel,k,source,windows, *, moment_basis=None):
    from quelle import box,hull
    half=F(1,64)
    def raw(x):
        return Y[3]+x*(Y[7]-Y[3])
    assert all(bounds(Y[j])==(t,t) for j,t in ((0,-5),(1,-4),(2,-3)))
    assert (Y[7]-Y[3]).lo>0
    L=bounds(raw(F(1,2)-half))[0]
    U=bounds(raw(F(1,2)+half))[1]
    gap=U-L
    my,mw = (Y,W) if moment_basis is None else moment_basis
    def collar(t):
        return sum((c*mw[j]*(my[j]-t) for j,c in [(7,-9),(8,16),(9,-8)]),box(0))
    # For every fixed boundary history B is affine. Curve extrema are at an endpoint.
    def deficit(l,u):
        ends=[bounds(-collar(box(x))) for x in (l,u)]
        return min(e[0] for e in ends),max(e[1] for e in ends)
    C_low,C_high=deficit(L,U)
    assert 0<L<U and C_low>0
    L0=bounds(raw(windows[0][0]))[0]
    U0=bounds(raw(windows[1][1]))[1]
    narrow_gap=U0-L0
    C0=deficit(L0,U0)[0]
    # G20 requires w_r(r-z)=-B(z). Positivity, causality and w_r < 1.
    wr=C_low/gap
    required_gap=C_low/bounds(Y[7]-Y[3])[1]
    assert C0>narrow_gap and 0<wr<1
    # In G15 use r-u>r-z, n-u>0, w_n>0. mu=-k, |p_u|<=k*vel.
    assert 0<=k<1
    ws=(8*C_low-k*vel)/((1-k)*(U+3))
    assert 0<ws<1
    load=k*3*vel**2
    # D16 bounds d=s-u. s>0 so s²+6s+6 is increasing across the window.
    ds_lo=(L*L+6*L+6+source-load/ws**2)/(1-k)
    ds_hi=(U*U+6*U+6+source)/(1-k)
    assert 0<ds_lo<=ds_hi
    dmin,dmax=bounds(hull(ds_lo,ds_hi).sqrt())
    # D19 = B19 + a(n-h)^2. n-s, r-s, r-n and r-z all lie in [0,gap].
    b19_lo=35+32*L+8*L**2-9*(dmax+gap)**2
    b19_hi=35+32*U+8*U**2-9*dmin**2+gap**2
    assert b19_lo<=b19_hi<0
    # If a=1 and b=0, the h term in D18 is negative.
    r_only_hi=19-8*dmin**2+(16-k+2)*gap**2+load/wr**2
    # If a=b=1, D19=0 forces (n-h)^2 >= -b19_hi, with h<n<r.
    r_both_lo=19-8*(dmax+gap)**2+(16-k)*(-b19_hi)
    assert r_only_hi<0<r_both_lo
    return {'clock_raw':[L,U],'signed_deficit':[C_low,C_high],
            'old_clock_gap_upper':narrow_gap,'narrow_collar_deficit_lower':C0,
            'narrow_vacuum_residual_upper':narrow_gap-C0,
            'minimum_normalized_gap':required_gap,'weight18_lower':wr,'weight16_lower':ws,
            'sender_minus_precursor':[dmin,dmax],
            'D19_without_17':[b19_lo,b19_hi],'D18_only_17_to_19_upper':r_only_hi,
            'D18_both_lower':r_both_lo}


def study():
    with model() as (_,__,previous,early):
        from gemischt import ORDER,WINDOWS
        from modell import setup
        from referenzwechsel import displaced
        from empfangsbit import K0,STEP,V
        from staubgeraet import solve,verify
        from quelle import box,hull
        from wege import ROUTES
        from driftfamilie import LABELS,LIMIT
        y,w=setup(previous,early)
        order=set(ORDER)
        variants=orders(order)
        out={}
        for (a,b),rel in sorted(variants.items()):
            n=audit_action(rel,ROUTES['positive_bridge'],a,b)
            out[f'{int(a)}{int(b)}']={'relations':len(rel),'finite_difference_checks':n,
                'contradiction':('D19<0' if not a else 'D18>0' if b else 'D18<0')}
        cert=json.loads((ROOT/'basis/Driftzertifikat.json').read_bytes())
        leaves=[tuple(map(F,row['delta'])) for row in cert['leaves']]
        assert len(leaves)==7 and leaves[0][0]==-LIMIT and leaves[-1][1]==LIMIT
        assert all(l<r for l,r in leaves) and all(b==c for (_,b),(c,_) in zip(leaves,leaves[1:]))
        vmax=112*V
        velocities=(hull(-vmax,vmax),)*3
        q=(hull(-1,1),)*3
        # The archived load completion maps arbitrary tail perturbations l and m
        # into Δw8=-l/8, Δw9=-l/4 and ΔM8=-m/8, ΔM9=-m/4; Δw7=ΔM7=0.
        # M_j=w_j*Y_j. This kills both changes in -9*(7)+16*(8)-8*(9).
        assert 16*F(-1,8)-8*F(-1,4)==0
        rows=[];off_rows=[];subrows=[]
        for lo,hi in leaves:
            uy,uw=displaced(y,w,hull(6*STEP+lo,6*STEP+hi))
            for source in LABELS:
                state=solve(uy,uw,source,velocities,K0,box(-K0),'positive_bridge')
                verify(state,source,velocities,K0,box(-K0),'positive_bridge',q)
                # Only the collar is supplied to the N21 proof.
                boundary=(0,1,2,3,7,8,9,10)
                by={n:state['y'][n] for n in boundary}
                bw={n:state['w'][n] for n in boundary}
                entry={'delta':[lo,hi],'source':source,
                       'boundary':{n:[bounds(by[n]),bounds(bw[n])] for n in boundary}}
                for clock in (0,1):
                    b_loaded=sum((c*bw[n]*(by[n]-clock) for n,c in [(7,-9),(8,16),(9,-8)]),box(0))
                    b_native=sum((c*uw[n]*(uy[n]-clock) for n,c in [(7,-9),(8,16),(9,-8)]),box(0))
                    assert (b_loaded-b_native).contains_zero()
                entry.update(proof(by,bw,vmax,K0,source,WINDOWS,moment_basis=(uy,uw)))
                rows.append(entry)
                # Geometry control: remove the remaining device couplings on N21
                # while holding the reference collar for this case fixed.
                off_rows.append(proof(by,bw,0,F(0),source,WINDOWS,moment_basis=(uy,uw)))
            # Independent direct check without cancellation, using narrower drift boxes.
            for sub in range(8):
                left=lo+(hi-lo)*sub/8
                right=lo+(hi-lo)*(sub+1)/8
                sy,sw=displaced(y,w,hull(6*STEP+left,6*STEP+right))
                for source in LABELS:
                    actual=solve(sy,sw,source,velocities,K0,box(-K0),'positive_bridge')
                    check=proof(actual['y'],actual['w'],vmax,K0,source,WINDOWS)
                    subrows.append(check)
        def summary(group):
            keys_low=['minimum_normalized_gap','narrow_collar_deficit_lower','weight18_lower',
                      'weight16_lower','D18_both_lower']
            keys_hi=['narrow_vacuum_residual_upper','old_clock_gap_upper','D18_only_17_to_19_upper']
            s={k:min(x[k] for x in group) for k in keys_low}
            s.update({k:max(x[k] for x in group) for k in keys_hi})
            for k in ['signed_deficit','D19_without_17','sender_minus_precursor','clock_raw']:
                s[k]=[min(x[k][0] for x in group),max(x[k][1] for x in group)]
            return s
        registry=json.loads((ROOT/'basis/P3.json').read_bytes())
        assert len(registry)==60 and all(r['execution']=='NOT_RUN' for r in registry)
        target={(r['checkpoint_context']['M'],r['checkpoint_context']['density_ratio'])
                for r in registry if r['checkpoint_context']['x']=='1/2' and r['checkpoint_context']['M'] in ('1/4','4')}
        assert target=={(m,d) for m in ('1/4','4') for d in (1,2,4,8)}
        return {'variants':out,'cells':rows,'unit_parameters':{'k':K0,'max_abs_velocity':vmax},'active_bounds':summary(rows),
                'device_removed_same_collar_bounds':summary(off_rows),
                'direct_subcells':len(subrows),'direct_bounds':summary(subrows),
                'old_controls':len(rows),'admissible_target_stationary_solutions':0,
                'target_window':'x=1/2 +/- 1/64 for the two anchors and their interval',
                'unrestricted_saddles':'NOT_CLASSIFIED','physical_P3':'60 NOT_RUN'}
