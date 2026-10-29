"""Archive adapter audit. Old source files, clouds and detector transfers immutable."""
import argparse
import hashlib
import importlib.util
import json
import sys
import time
from pathlib import Path
import numpy as np
from flint import arb, acb, ctx
import adapter as a

HERE=Path(__file__).resolve().parent
V10=HERE.parent/'detector_methods_v0_10'
sys.path.insert(0,str(V10))
from common10 import pack,unpack,gzread,gzwrite,digest
spec=importlib.util.spec_from_file_location('old_adapter',V10/'adapter.py')
old_adapter=importlib.util.module_from_spec(spec);spec.loader.exec_module(old_adapter)


def realpack(x):return pack(acb(x))


def compute(bits,output):
    ctx.prec=bits;p=json.loads((HERE/'PROTOCOL.json').read_text())
    for name,h in json.loads((HERE/'FREEZE.json').read_text())['sha256'].items():
        a.require(hashlib.sha256((HERE/name).read_bytes()).hexdigest()==h,'method freeze mismatch: '+name)
    archive=np.load(HERE.parent/'scalar_pilot_v0_1/results/clouds.npz')
    prior=gzread(V10/'results'/f'BENCHMARK_{bits}.json.gz')
    A=unpack(prior['normalization_A']).real
    F2=arb(1).exp()**2/(A*A) # ||f/(A/e)||_2^2, original normalized compact source.
    Ctime=old_adapter.constants()[1]
    started=time.monotonic();rows=[]
    for key in p['clouds']:
        original=archive[key];x=original[original[:,0]<=-1];q=x[:,1:]
        previous=next(r for r in prior['rows'] if r['key']==key)
        a.require(digest(original)==previous['coordinates_sha256'],'original archive hash')
        a.require(len(x)==previous['history_nodes'],'same history inventory')
        mesh=a.certify_mesh(q);covered=a.ball_covered(mesh);M=a.mass_matrix(mesh)
        lower,inv=a.gram_min_eigenvalue_bound(M)
        volume=a.ball_fraction(sum(mesh['volumes']))
        sigma=max(inv[i,i].upper().sqrt().upper() for i in range(len(q)))
        mass_condition=max(sum(M[i,j].abs_upper() for j in range(len(q))).upper() for i in range(len(q)))/lower
        waves=a.wave_load(mesh,p['wave_moment_degree'])
        levels=[];last_B=None;last_C=None
        for depth in p['depths']:
            B,leaves=a.integrate_load(mesh,depth,waves)
            if last_B is not None:
                B=[[acb(z.real.intersection(o.real),z.imag.intersection(o.imag)) for z,o in zip(r,s)] for r,s in zip(B,last_B)]
            C=a.project(M,B)
            if last_C is not None:
                C=[[acb(z.real.intersection(o.real),z.imag.intersection(o.imag)) for z,o in zip(r,s)] for r,s in zip(C,last_C)]
            last_B,last_C=B,C
            H=[];errors=[[] for _ in range(5)];spatial=[[] for _ in range(5)]
            for j,point in enumerate(x):
                tau=arb(float(point[0]))+1;z=arb(float(point[3]))
                row=[]
                for kindex,k in enumerate(p['waves']):
                    omega=arb(k*k+1).sqrt();f=acb(0,k*z).exp()
                    h=a.history_polynomial(tau,[C[j][kindex]],[-acb(0,omega)*C[j][kindex]])
                    exact=acb(0,k*z-omega*tau).exp()
                    row.append(h);errors[kindex].append((h-exact).abs_upper())
                    spatial[kindex].append((C[j][kindex]-f).abs_upper())
                rr=sum(arb(float(v))**2 for v in point[1:]);hh=1-4*rr
                f=acb(0) if hh<=0 else (1-1/hh).exp()*acb(0,4*z).exp()
                a.require(hh<=0 or hh>0,'source support decision')
                row.append(C[j][4]);spatial[4].append((C[j][4]-f).abs_upper())
                errors[4].append(spatial[4][-1]+Ctime*tau*tau)
                H.append(row)
            l2=[]
            for f in range(5):
                norm2=volume if f<4 else F2
                e2=a.l2_residual_squared(norm2,B,C,f) if f<4 or covered else None
                if e2 is None:
                    l2.append(None)
                else:
                    ratio=e2/norm2
                    # Orthogonal projection gives the independent bound 0<=ratio<=1.
                    lo=max(arb(0),ratio.lower());hi=min(arb(1),max(arb(0),ratio.upper()))
                    a.require(lo<=hi,'projection contraction consistency')
                    l2.append(lo.sqrt().union(hi.sqrt()))
            windows=[]
            for window in previous['levels'][-1]['windows']:
                T=[unpack(t) for t in window['history_transfer']]
                response=[sum(t*h[f] for t,h in zip(T,H)) for f in range(5)]
                error=[a.transfer_bound(T,errors[f]) for f in range(5)]
                # Stability in product L2(D)xL2(D), fixed time units L0=c=1.
                d=[T,[T[j]*(arb(float(x[j,0]))+1) for j in range(len(x))]]
                stability=arb(0)
                for dd in d:
                    en=sum(dd[i].conjugate()*inv[i,j]*dd[j] for i in range(len(x)) for j in range(len(x)))
                    a.require(en.imag.contains(0),'real dual norm')
                    stability+=max(arb(0),en.real.upper())
                windows.append({'responses':[pack(z) for z in response],
                    'history_error_upper':[realpack(e) for e in error],
                    'history_budget_pass':[bool(e<=arb(p['detector_history_tolerance'])) for e in error],
                    'integration_budget_pass':[bool(max(z.real.rad(),z.imag.rad())<=arb(p['combined_integration_radius_tolerance'])) for z in response],
                    'data_to_detector_L2_norm_upper':realpack(stability.sqrt())})
            levels.append({'depth':depth,'leaf_tetrahedra':leaves,
                'relative_L2_projection_error':[None if v is None else realpack(v) for v in l2],
                'resolution_pass':[v is not None and bool(v<=arb(p['spatial_relative_L2_tolerance'])) for v in l2],
                'nodal_projection_error_upper':[realpack(max(v)) for v in spatial],
                'coefficient_enclosures':[[pack(z) for z in row] for row in C],
                'windows':windows})
            print(key,bits,'depth',depth,'cells',leaves,flush=True)
        rows.append({'key':key,'status':'COMPLETE','coordinates_sha256':digest(original),
            'history_nodes':len(x),'tetrahedra':len(mesh['tetrahedra']),
            'mesh_sha256':hashlib.sha256(json.dumps(mesh['tetrahedra']).encode()).hexdigest(),
            'source_support_hits':old_adapter.support_hits(x),'source_ball_covered':covered,
            'source_not_erased_by_exact_projection':covered,
            'projection_domain_volume':realpack(volume),'lambda_min_lower':realpack(lower),
            'coefficient_condition_upper':realpack(mass_condition),'nodal_L2_evaluation_norm_upper':realpack(sigma),
            'levels':levels})
    result={'schema':p['schema'],'precision_bits':bits,'new_random_clouds':0,'new_causal_nodes':0,
            'normalization':'all fields divided by their original amplitude scale',
            'rows':rows,'decision':'METHOD_HOLD','G1':'HOLD','elapsed_seconds':time.monotonic()-started}
    good=all(r['source_ball_covered'] and all(r['levels'][-1]['resolution_pass']) and all(all(w['history_budget_pass']) and all(w['integration_budget_pass']) for w in r['levels'][-1]['windows']) for r in rows)
    if good:result['decision']='DEVELOPMENT_BUDGETS_ONLY'
    gzwrite(output,result)
    print(json.dumps({k:v for k,v in result.items() if k!='rows'},indent=2))
    return result


if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('--bits',type=int,choices=[128,192],required=True)
    ap.add_argument('--out',type=Path,required=True);args=ap.parse_args()
    compute(args.bits,args.out)
