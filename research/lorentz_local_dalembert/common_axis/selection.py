"""Coordinate-blind common-frame reference selector; only scalar time algebra."""
import math

def score(qab,qar,qrb,qax,qxb,qrx,sign):
    values=[qab,qar,qrb,qax,qxb,qrx]
    if any(q is None or not math.isfinite(q) or q<=0 for q in values):
        return dict(status='invalid_time')
    dt=(qax*qax-qxb*qxb-qar*qar+qrb*qrb)/(2*qab)
    h=(dt/qrx)**2-1
    return dict(status='ok' if sign*dt>0 else 'wrong_time_sign',dt=dt,h=h,score=abs(h))

def choose_with_times(g,s,time):
    if 'sides' not in s:return dict(status=s['status'],sides=[])
    r=s['root'];a,b=s['temporal'];common=[(a,b),(a,r),(r,b)]
    counts=[g.interval(u,v) for u,v in common]
    out=dict(status='ok',common_counts=counts,sides=[])
    if min(counts)<=0:return dict(out,status='zero_common_interval')
    common_times=[time(u,v,n) for (u,v),n in zip(common,counts)]
    out['common_times']=common_times
    for side,sign in zip(s['sides'],[1,-1]):
        rows=[]
        for x in sorted(side['shell'],key=lambda x:g.marks[x]):
            row=dict(point=x)
            if not (g.r[a,x] and g.r[x,b]):row['status']='outside_anchor_interval'
            else:
                pairs=[(a,x),(x,b),(r,x) if sign>0 else (x,r)]
                ns=[g.interval(u,v) for u,v in pairs];row['counts']=ns
                if min(ns)<=0:row['status']='zero_candidate_interval'
                else:
                    times=[time(u,v,n) for (u,v),n in zip(pairs,ns)]
                    row.update(times=times,**score(*common_times,*times,sign))
            rows.append(row)
        valid=[row for row in rows if row['status']=='ok']
        winner=min(valid,key=lambda row:(row['score'],g.marks[row['point']])) if valid else None
        out['sides'].append(dict(reference=winner['point'] if winner else None,candidates=rows))
    if any(side['reference'] is None for side in out['sides']):out['status']='no_axis_reference'
    return out

def select(g,s,rho):
    if not math.isfinite(rho) or rho<=0:raise ValueError('rho must be positive and finite')
    return choose_with_times(g,s,lambda u,v,n:(n/(rho*math.pi/12))**(1/3))
