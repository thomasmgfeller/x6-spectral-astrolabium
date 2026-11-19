"""Evaluate the independent prefix target and both sensitive boundary equations."""
import os
for var in ('OPENBLAS_NUM_THREADS','OMP_NUM_THREADS','MKL_NUM_THREADS'):
    os.environ[var]='1'
import json
from fractions import Fraction as F
from tempfile import TemporaryDirectory
import mpmath as mp
import numpy as np
import sympy as sp
from prefix import A, B, BASE, PREFIX, read, row
from scalar import geometry, layout, rate, states, overlap
from certify import projection_certificate
from identities import diagnostics
import orders
import quadrature


def pairs(z):
    return [float(mp.re(z)),float(mp.im(z))]


def norm(z):
    return mp.sqrt(mp.re((z.H*z)[0]))


def same_packet(row):
    lobes=np.asarray(row['lobes'])
    return (lobes[...,0]+1j*lobes[...,1]).sum(axis=1)/np.sqrt(2)


def clock_values():
    archival=read('clocks_all.json')['N13_62']
    central=read('response.json')
    assert central['order']==[A,B] and central['densities']==['1/8','1/4']
    archive={tuple(v['grid']):same_packet(v['amplitudes']) for v in archival['grids']}
    pair={tuple(v['grid']):np.array([same_packet(x) for x in v['packets']])
          for v in central['production_grids']}
    assert layout((5,62))==orders.layout((5,62))
    reference=[]
    with TemporaryDirectory() as tmp:
        lib=quadrature.build(tmp)
        for n,m in [(32,6),(48,8),(64,10)]:
            computed=quadrature.packet(62,n,m,lib)[0].sum(axis=1)/np.sqrt(2)
            if (n,m) in archive:
                assert max(abs(computed-archive[n,m]))<1e-14
            reference.append(computed)
    assert np.max(abs(reference[-1]-reference[-2]))<1e-12
    # Also check stability of A and B against the published finer grid.
    assert max(abs(pair[64,10]-pair[80,12]).ravel())<1e-12
    assert min(abs(reference[-1]))>1e-2 and min(abs(pair[64,10]).ravel())>0.005
    return reference, pair


def gram_data(keys, precisions, digits):
    mp.mp.dps=digits
    images=states(keys)
    beta=4/mp.sqrt(6)
    for k in keys:
        assert max(abs(z) for z in images[k][0]-beta*geometry.numeric(precisions[k])) < mp.mpf('1e-46')
    al=keys[1:]
    G=mp.matrix([[overlap(images[x],images[y]) for y in al] for x in al])
    g=mp.matrix([overlap(images[x],images[keys[0]]) for x in al])
    assert max(abs(z) for z in G.H-G)<mp.mpf('1e-45')
    assert max(abs(G[i,i]-1) for i in range(len(al)))<mp.mpf('1e-45')
    assert abs(overlap(images[keys[0]],images[keys[0]])-1)<mp.mpf('1e-45')
    c=mp.lu_solve(G,g)
    residual=1-mp.re((g.H*c)[0])
    assert 0<residual<1 and norm(G*c-g)<mp.mpf('1e-45')
    return G,g,c,residual


def compute():
    paths,bytype=row()
    keys=[(5,62),*[(6,j) for j in sorted(bytype)]]
    precisions={key:rate(key) for key in keys}
    rates={key:x[0,0] for key,x in precisions.items()}
    saved=read('boundary.json')['Omega_11_by_N14_mask']
    for k in keys[1:]:
        assert [sp.re(rates[k]),sp.im(rates[k])]==list(map(sp.Rational,saved[str(k[1])]))
    # A Vandermonde determinant in u=y_1^2 is nonzero over Q(i).
    assert len(set(rates.values()))==len(keys)==11
    assert len({sp.re(v) for v in rates.values()})==11
    parent_arms,pair=clock_values()
    low=gram_data(keys,precisions,55)
    G,g,c,residual=gram_data(keys,precisions,75)
    ix={key[1]:i for i,key in enumerate(keys[1:])}
    sector=read('sector.json')
    assert sector['order']==[A,B]
    assert abs(G[ix[A],ix[B]]-complex(*sector['gram_scalar'][0][1]))<1e-15
    assert abs(residual-low[3])<mp.mpf('1e-44') and norm(c-low[2])<mp.mpf('1e-44')

    def project_equations(d,zparent,zab):
        q=[mp.mpc(zparent)*c[ix[k]]/mp.mpc(zab[i,d]) for i,k in enumerate((A,B))]
        t=[(mp.mpf(1)/18-q[0])/49,(q[1]-mp.mpf(1)/18)/49]
        return q,t
    # Manufactured positive control for the two duals. Other columns carry
    # arbitrary complex nuisance coefficients; their responses must cancel.
    test_t=mp.mpf(1)/3528
    control=mp.matrix([mp.mpc(j+1,1-j)/100 for j in range(len(bytype))])
    for i,(k,sign) in enumerate(((A,-1),(B,1))):
        control[ix[k]]=(mp.mpf(1)/18+sign*49*test_t)*mp.mpc(pair[64,10][i,0])
    recovered=mp.lu_solve(G,G*control)
    control_t=[(recovered[ix[k]]/mp.mpc(pair[64,10][i,0])-mp.mpf(1)/18)/(sign*49)
               for i,(k,sign) in enumerate(((A,-1),(B,1)))]
    assert max(abs(x-test_t) for x in control_t)<mp.mpf('1e-48')
    equations={}
    for d,rho in enumerate(('1/8','1/4')):
        q,t=project_equations(d,parent_arms[2][d],pair[64,10])
        qold,told=project_equations(d,parent_arms[1][d],pair[48,8])
        equations[rho]={'parent_clock':[float(x) for x in pairs(parent_arms[2][d])],
                        'q_required_A_B':[pairs(z) for z in q],'t_implied_A_B':[pairs(z) for z in t],
                        'max_delta_q_48_to_64':float(max(abs(z-w) for z,w in zip(q,qold))),
                        'max_delta_t_48_to_64':float(max(abs(z-w) for z,w in zip(t,told)))}

    assert all(abs(complex(*v['q_required_A_B'][0]).imag)>.02
               and abs(complex(*v['q_required_A_B'][1]).imag)>.003
               and v['max_delta_q_48_to_64']<1e-10 for v in equations.values())

    return {'prefix':PREFIX,'parent_type':62,'prefix_mass':'1/147',
            'action_controls':diagnostics(paths,bytype),
            'rational_projection_certificate':projection_certificate([precisions[k] for k in keys]),
            'paths':[{'end':end,'code':c0,'conditional_weight_at_t0':str(q)} for end,c0,q in paths],
            'conditional_weights_at_zero':{str(j):str(q) for j,q in sorted(bytype.items())},
            'q_slope_per_unit_orbit_t':{str(A):-49,str(B):49},
            'F4_parent_and_daughters':{f'{k[0]+8}_{k[1]}':layout(k)[2] for k in keys},
            'exact_gaussian_rates_axis_one':{f'{k[0]+8}_{k[1]}':[str(sp.re(rates[k])),str(sp.im(rates[k]))] for k in keys},
            'parent_plus_daughters_exact_rank':len(set(rates.values())),
            'daughter_type_order':[j for _,j in keys[1:]],
            'gram_eigenvalue_range':[float(mp.eighe(G,eigvals_only=True)[i]) for i in (0,G.rows-1)],
            'scalar_span_projection_coefficients':{str(k[1]):pairs(c[i]) for i,k in enumerate(keys[1:])},
            'scalar_parent_relative_squared_norm_outside_daughter_span':float(residual),
            'scalar_parent_relative_norm_outside_daughter_span':float(mp.sqrt(residual)),
            'detector_free_dual_equations':equations,
            'manufactured_positive_control_t_recovered_on_both_duals':'1/3528',
            'clock_grids':[[32,6],[48,8],[64,10]],'physical_selection':'UNDETERMINED',
            'bare_parent_identity':'EXCLUDED_ON_FINITE_SECTOR'}


if __name__=='__main__':
    import argparse
    from pathlib import Path
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('output',type=Path)
    args=parser.parse_args()
    if not __debug__:
        raise RuntimeError('Keep assertions enabled')
    args.output.write_text(json.dumps(compute(),indent=2,allow_nan=False)+'\n')
