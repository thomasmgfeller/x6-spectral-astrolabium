"""Independent cone-slab, order rejection and SVD controls.
SPDX-License-Identifier: Apache-2.0
"""
from sc_run import *
import numpy as np

def cone(v,sign):
    t=sign*v[0]
    return t>0 and t*t>v[1]*v[1]+v[2]*v[2]

def slab_controls():
    checked=changed=0
    for axis in range(3):
      for direction in [-1,1]:
       d=[0,0,0];d[axis]=direction
       for t in range(-4,5):
        for x in range(-4,5):
         for y in range(-4,5):
          v=[t,x,y];other=[a-b for a,b in zip(v,d)]
          for sign in [-1,1]:
            checked+=1
            if cone(v,sign)!=cone(other,sign):
              changed+=1
              # Exactly |sign*t-sqrt(x²+y²)|<=1, no floating square roots.
              u=sign*t;r=x*x+y*y
              assert u+1>=0 and r<=(u+1)**2
              if u-1>0:assert (u-1)**2<=r
    assert changed>0
    return dict(exact_point_cone_comparisons=checked,changed_memberships_inside_proved_slab=changed)

def audit():
    w,z=inputs();rows=read(HERE/'candidates.json');summary=read(HERE/'summary.json');witness=read(HERE/'witness.json')
    rejected=[]
    for k,r in enumerate(rows):
      if r['status']=='GEOMETRY_OR_RANK_REJECTED':
        zz=deform(z,r['node'],r['axis'],r['sign'],F(r['step']))
        mismatches=[]
        for i in range(len(z)):
          for j in range(i+1,len(z)):
            q=interval(zz,i,j);dt=zz[j][0]-zz[i][0]
            if (q>0 and dt>0)!=w['full_order'][i][j] or (q>0 and dt<0)!=w['full_order'][j][i]:mismatches.append([i,j])
        reason='ORDER_CHANGED' if mismatches else 'MARGIN_ONLY'
        if not mismatches:
            assert min(abs(interval(zz,i,j)) for i in range(21) for j in range(i+1,21))<F(99,10**10)
            exact_weights(zz,F(w['scale']))
        rejected.append(dict(row=k,node=r['node'],changed_order_pairs=mismatches,reason=reason))
    S=summary['selected'];zz=deform(z,S['node'],S['axis'],S['sign'],F(S['step']))
    assert [[str(v) for v in row] for row in zz]==witness['coordinates']
    svd=[]
    for geom,weights in [(z,witness['exact_weight_vectors'][0]),(zz,witness['exact_weight_vectors'][1])]:
        Y=np.array([[float(v-a) for v,a in zip(row,geom[4])] for row in geom[4:]])
        t,x,y=Y.T
        D=np.array([np.ones(len(Y)),t,x,y,t*t,x*x,y*y,t*x,t*y,x*y])
        rhs=np.array([0,0,0,0,-2,2,2,0,0,0],dtype=float)/float(F(w['scale'])**2)
        direct=np.linalg.lstsq(D,rhs,rcond=None)[0];exact=np.array([float(F(v)) for v in weights])
        relative=float(np.linalg.norm(direct-exact)/np.linalg.norm(exact))
        assert relative<1e-9
        svd.append(True)
    C=constant(w);assert F(S['tv_upper'])>=C*F(S['step'])
    assert all(F(r['relative'][1])<F(1,5) for r in rows if 'relative' in r)
    return dict(status='PASS',controls=slab_controls(),independent_svd_weight_checks=svd,
      rejected_candidates=len(rejected),rejections_with_actual_order_changes=sum(bool(r['changed_order_pairs']) for r in rejected),
      rejection_details=rejected,all_certified_grid_candidates_below_strong_gate=True)
if __name__=='__main__':
    r=audit()
    if '--verify' in sys.argv:assert r==read(HERE/'audit.json')
    else:save(HERE/'audit.json',r)
    print(json.dumps({k:v for k,v in r.items() if k!='rejection_details'}))
