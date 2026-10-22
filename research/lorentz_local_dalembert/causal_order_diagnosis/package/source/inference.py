"""Intrinsic four-landmark inference and full count-covariance propagation.
No simulator, physical coordinates, or evaluation-field inputs.
SPDX-License-Identifier: Apache-2.0
"""
import numpy as np

ETA=np.array([-1.,1.,1.])

def design(z):
    t,x,y=np.asarray(z).T
    return np.array([t,x,y,t*t,x*x,y*y,t*x,t*y,x*y])

def solve(d,target,scale):
    condition=float(np.linalg.cond(d))
    if not np.isfinite(condition) or condition>1e5 or np.linalg.matrix_rank(d)!=9:
        raise ValueError('moment rank or condition')
    n=d.shape[1];h=np.eye(n)+np.ones((n,n))
    kkt=np.block([[h,d.T],[d,np.zeros((9,9))]])
    u=np.linalg.solve(kkt,np.r_[np.zeros(n),target]);a=u[:n]
    residual=float(np.max(abs(kkt@u-np.r_[np.zeros(n),target])))
    if residual>1e-7*(1+np.max(abs(target))):raise ValueError('KKT residual')
    full=np.r_[-a.sum(),a]/scale**2
    return full,kkt,u,dict(condition=condition,kkt_residual=residual)

def normalize(h):
    ev,u=np.linalg.eigh(h)
    condition=float(np.linalg.cond(h))
    if not ev[0]<0<ev[1] or condition>1e5:raise ValueError('Lorentz frame signature or condition')
    return (u/np.sqrt(abs(ev))).T,condition

def strict_order_check(points,observed):
    delta=points[None]-points[:,None]
    r=(delta[:,:,0]>0)&(np.sum(delta*delta*ETA,axis=2)<0)
    observed=np.asarray(observed,bool)
    return dict(passed=bool(np.array_equal(r,observed)),missing=int(np.sum(observed&~r)),extra=int(np.sum(r&~observed)))

def four_geometry(q,packet):
    """q normalized by the inherited, selection-fixed scale squared."""
    n=len(packet['support']);m=len(q)
    lookup={tuple(pair):i for i,pair in enumerate(packet['pairs'])}
    def coeff(a,b):
        v=np.zeros(m)
        if a!=b:v[lookup[tuple(sorted((a,b)))]]=1
        return v
    l=packet['landmarks'];root=packet['root'];s=packet['support']
    hm=np.empty((3,3,m))
    for i in range(3):
        for j in range(3):hm[i,j]=(coeff(l[i+1],l[j+1])-coeff(l[i+1],l[0])-coeff(l[0],l[j+1]))/2
    h=hm@q
    nodes=l+[root]+s
    zm=np.empty((len(nodes),3,m))
    for j,x in enumerate(nodes):
        for i in range(3):zm[j,i]=(coeff(l[i+1],x)-coeff(l[0],x)-coeff(l[i+1],root)+coeff(l[0],root))/2
    z=zm@q
    targetmap=np.vstack((np.zeros((3,m)),2*hm[0,0],2*hm[1,1],2*hm[2,2],2*hm[0,1],2*hm[0,2],2*hm[1,2]))
    return h,z,zm,targetmap

def four(q,packet,covq=None):
    h,z,zm,tm=four_geometry(q,packet)
    transform,hcondition=normalize(h)
    support=z[5:];d=design(support);target=tm@q
    full,kkt,u,certificate=solve(d,target,packet['scale'])
    coordinates=(transform@z.T).T
    future=packet['support'].index(packet['temporal'][1])+5
    if coordinates[future,0]<0:coordinates[:,0]*=-1
    order=strict_order_check(coordinates,packet['full_order'])
    out=dict(status='WEIGHTS_VALID',qualified=order['passed'],order=order,weights=full,
             intrinsic_coordinates=support,coordinates=coordinates,landmark_condition=hcondition,
             certificate=certificate)
    if covq is not None:
        n=len(support);m=len(q);dm=np.zeros((9,n,m));dx=zm[5:]
        dm[:3]=dx.transpose(1,0,2)
        for i in range(3):dm[3+i]=2*support[:,i,None]*dx[:,i]
        for row,(i,j) in enumerate([(0,1),(0,2),(1,2)],6):
            dm[row]=support[:,i,None]*dx[:,j]+support[:,j,None]*dx[:,i]
        rhs=np.vstack((-np.einsum('inm,i->nm',dm,u[n:]),tm-np.einsum('inm,n->im',dm,u[:n])))
        du=np.linalg.solve(kkt,rhs)[:n]
        jac=np.vstack((-du.sum(axis=0),du))/packet['scale']**2
        covariance=jac@covq@jac.T
        covariance=(covariance+covariance.T)/2
        negative_control=(jac*np.diag(covq))@jac.T
        out.update(weight_jacobian=jac,weight_covariance=covariance,
                   independent_counts_negative_control=negative_control)
    return out

def baseline_three(q,packet):
    lookup={tuple(pair):i for i,pair in enumerate(packet['pairs'])}
    def get(a,b):return 0. if a==b else q[lookup[tuple(sorted((a,b)))]]
    l=packet['landmarks'][:3];root=packet['root'];s=packet['support']
    h=np.array([[(-get(a,root)-get(b,root)+get(a,b))/2 for b in l] for a in l])
    transform,hcond=normalize(h)
    vectors=np.array([[(-get(a,root)-get(root,b)+get(a,b))/2 for b in s] for a in l])
    z=(transform@vectors).T
    if z[s.index(packet['temporal'][1]),0]<0:z[:,0]*=-1
    target=np.array([0,0,0,-2,2,2,0,0,0.])
    full,_,_,certificate=solve(design(z),target,packet['scale'])
    order=strict_order_check(np.vstack((np.zeros(3),z)),np.array(packet['full_order'])[4:,4:])
    return dict(status='WEIGHTS_VALID',weights=full,qualified=order['passed'],order=order,
                certificate=certificate,landmark_condition=hcond)

def measurement(packet,counts,overlaps,rho,minimum_count=8):
    counts=np.asarray(counts,float);overlaps=np.asarray(overlaps,float)
    if overlaps.shape!=(len(counts),len(counts)) or not np.array_equal(np.diag(overlaps),counts):
        raise ValueError('count covariance diagonal mismatch')
    if not np.array_equal(overlaps,overlaps.T):raise ValueError('asymmetric intersections')
    fourpairs=np.any(four_geometry(np.ones(len(counts)),packet)[2]!=0,axis=(0,1))
    # Include all anchor Gram inputs, including any cancelling in coordinates.
    anchor=set(packet['landmarks'])
    fourpairs|=np.array([a in anchor and b in anchor for a,b in packet['pairs']])
    q=(counts/(rho*np.pi/12))**(2/3)/packet['scale']**2
    derivative=np.zeros(len(counts));positive=counts>0
    derivative[positive]=(2/3)*q[positive]/counts[positive]
    covq=overlaps*derivative[:,None]*derivative[None,:]
    out=dict(minimum_four_count=float(counts[fourpairs].min()),minimum_all_count=float(counts.min()),
             q=q,count_covariance_min_eigenvalue=float(np.linalg.eigvalsh(overlaps)[0]))
    if counts[fourpairs].min()<minimum_count:
        out['four']=dict(status='COUNT_HOLD')
    else:
        try:out['four']=four(q,packet,covq)
        except (ValueError,np.linalg.LinAlgError) as exc:out['four']=dict(status='UNRESOLVED',reason=str(exc))
    baseline_mask=np.array([packet['landmarks'][3] not in pair for pair in packet['pairs']])
    if counts[baseline_mask].min()<minimum_count:out['baseline']=dict(status='COUNT_HOLD')
    else:
        try:out['baseline']=baseline_three(q,packet)
        except (ValueError,np.linalg.LinAlgError) as exc:out['baseline']=dict(status='UNRESOLVED',reason=str(exc))
    return out
