"""Evaluate measured charge probabilities and the decoherence matrix on a common H3."""
import json
import numpy as np
from model import BASE,gram,laws,edges,combined_laws
from integrate import MASSES,RHOS

def quadratic(v,G):
    return v.conj().T@(G@v)
def record(D):
    norm=np.diag(D).real
    total=norm.sum()
    assert total>0 and min(norm)>-total*1e-12
    return norm/total,total
def readout(A,G,q):
    V=q[:,None]*A
    D=quadratic(V,G)
    assert np.allclose(D,D.conj().T,rtol=1e-9,atol=1e-17)
    probs,total=record(D)
    S=np.column_stack((V[:,:3].sum(axis=1),V[:,3:].sum(axis=1)))
    signs=quadratic(S,G)
    s,st=record(signs)
    plain=D.sum().real
    assert abs(plain-signs.sum().real)<1e-10*max(total,st)
    dephased=np.sum(abs(V)**2,axis=0)
    return {'bin_probabilities':probs.tolist(),'positive_sign_record':float(s[1]),
            'positive_fine_record':float(probs[3:].sum()),'scaled_denominator':float(total),
            'sign_record_scaled_denominator':float(st),'unrecorded_scaled_norm':float(plain),
            'relative_two_sign_interference':float(2*signs[0,1].real/st),
            'dephased_type_fine_probabilities':(dephased/dephased.sum()).tolist(),
            'decoherence_matrix_scaled_by_record_trace':{'re':(D.real/total).tolist(),'im':(D.imag/total).tolist()}}
def quadratic_coeff(a,b,G):
    x=a.reshape(len(a),-1)
    y=(b-a).reshape(len(a),-1)
    return np.array([np.vdot(x,G@x).real,2*np.vdot(x,G@y).real,np.vdot(y,G@y).real])
def mix_range(A,G,q1,q2):
    V=[q[:,None]*A for q in (q1,q2)]
    neg=quadratic_coeff(V[0][:,:3].sum(axis=1),V[1][:,:3].sum(axis=1),G)
    pos=quadratic_coeff(V[0][:,3:].sum(axis=1),V[1][:,3:].sum(axis=1),G)
    den=pos+neg
    grid=[0.,1.]
    if den[2]>0: grid.append(np.clip(-den[1]/(2*den[2]),0,1))
    value=lambda c,t: float(np.polynomial.polynomial.polyval(t,c))
    dmin=min(value(den,t) for t in grid)
    a,b,c=pos;d,e,f=den
    roots=np.roots([c*e-b*f,2*(c*d-a*f),b*d-a*e])
    grid=[0.,1.]+[float(r.real) for r in roots if abs(r.imag)<1e-10 and 0<r.real<1]
    vals=[value(pos,t)/value(den,t) for t in grid]
    assert dmin>0
    return {'min':min(vals),'max':max(vals),'denominator_min_scaled':dmin,
            'mix_at_min':grid[int(np.argmin(vals))],'mix_at_max':grid[int(np.argmax(vals))]}
def run(combined=False):
    s=np.load(BASE/'scalars.npz'); raw=np.load(BASE/('combined_raw.npz' if combined else 'family_raw.npz')); rawall=np.load(BASE/'all_raw.npz')
    keys,qs=combined_laws() if combined else laws()
    assert keys==raw['keys'].tolist()
    index=np.searchsorted(s['keys'],keys)
    assert np.array_equal(s['keys'][index],keys)
    G=gram(list(zip(s['precision'][index],s['factor'][index])))
    a=raw['amp']; low=rawall['amp'][:,:,:,:,index,:]
    # The two independent runs share the same scramble and nested 1024 points.
    assert np.max(abs(a[:,0]-low[:,1]))<8e-13
    rows={}
    for im,m in enumerate(MASSES):
        for ir,r in enumerate(RHOS):
            A=a[:,-1,im,ir].mean(axis=0)
            row={}
            for iq,label in enumerate(['1:1','1:3']):
                q=qs[iq]
                best=readout(A,G,q)
                convergence={}
                for size,amp in [(256,low[:,0,im,ir]),(1024,a[:,0,im,ir]),(4096,a[:,-1,im,ir])]:
                    av=readout(amp.mean(axis=0),G,q)
                    repeat=[readout(x,G,q) for x in amp]
                    convergence[str(size)]={'sign_positive':av['positive_sign_record'],
                            'positive_fine_record':av['positive_fine_record'],
                            'max_bin_difference_from_finest_mean':float(np.max(np.abs(np.subtract(av['bin_probabilities'],best['bin_probabilities'])))),
                            'four_scramble_positive_sign_range':[min(x['positive_sign_record'] for x in repeat),max(x['positive_sign_record'] for x in repeat)],
                            'max_bin_range_four_scrambles':float(np.ptp([x['bin_probabilities'] for x in repeat],axis=0).max()),
                            'interference_range':[min(x['relative_two_sign_interference'] for x in repeat),max(x['relative_two_sign_interference'] for x in repeat)]}
                if combined:
                    edge_keys,eweights=laws()
                    qedge=np.zeros(len(keys))
                    qedge[np.searchsorted(keys,edge_keys)]=eweights[iq]/2
                    qchain=q-qedge
                    assert qchain.min()>-1e-14
                    VE=qedge[:,None]*A
                    VC=qchain[:,None]*A
                    cross=VE.conj().T@(G@VC)
                    best['parent_interference_over_fine_record_norm']=float(2*np.trace(cross).real/best['scaled_denominator'])
                best['convergence']=convergence
                row[label]=best
            row['convex_line_signed_record']=mix_range(A,G,*qs)
            rows[f'{m:g}/{r:g}']=row
    empty=raw['empty'][:,-1].mean(axis=0)
    vac={}
    for iq,label in enumerate(['1:1','1:3']):
        v=qs[iq]*np.exp(1j*np.array([15-edges(k).sum() for k in keys]))
        vnorm=float(np.vdot(v,G@v).real)
        en=[float(np.vdot(qs[iq]*z,G@(qs[iq]*z)).real) for z in empty]
        assert min(vnorm,*en)>0
        vac[label]={'true_vacuum_norm_excluding_common_clock_volume':vnorm,'matched_empty_norm_scaled_by_density_and_clock_factors':en,'point_mass_at_bare_zero':1}
    return {'scope':'finite four-mark family, H3 and ideal charge register; RQMC results and normalization conditional',
            'bin_edges':['-inf','-1','-1/4','0','1/4','1','inf'],'positive_mass_zero_atom_exact':0,
            'catalog_types':len(s['keys']),'witness_types':len(keys),'two_parents':combined,'vacuum':vac,'rows':rows,
            'physical_unconditional_charge_law':None,'physical_mass_gain':None,'physical_P3':'HOLD_NOT_ELIGIBLE / NOT_RUN'}
if __name__=='__main__':
    import sys
    print(json.dumps(run('--combined' in sys.argv),indent=2))
