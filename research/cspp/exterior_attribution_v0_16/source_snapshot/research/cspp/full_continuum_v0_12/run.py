"""Reference plus signed four-part error ledger on the original eight clouds."""
import argparse
import hashlib
import json
import sys
import time
from pathlib import Path
import numpy as np
from flint import arb,acb,ctx
import continuum

HERE=Path(__file__).resolve().parent
V10=HERE.parent/'detector_methods_v0_10'
V11=HERE.parent/'nonlocal_initial_v0_11'
sys.path.insert(0,str(V10))
from common10 import previous,pack,unpack,gzread,gzwrite,digest


def encode(v):
    if isinstance(v,(arb,acb)):return pack(v)
    if isinstance(v,dict):return {k:encode(x) for k,x in v.items()}
    if isinstance(v,list):return [encode(x) for x in v]
    return v


def dot(a,b):return sum(x*y for x,y in zip(a,b))


def magnitude(z):
    return {'lower':pack(z.abs_lower()),'upper':pack(z.abs_upper())}


def split_error(q,qhat,T,h_model,h_rounded,h_oracle,v_rounded,numeric,reference):
    """Signed exact identity. All intermediate interval dependence retained safely."""
    adapter=dot(T,[h-g for h,g in zip(h_model,h_oracle)])
    operator_domain=dot(T,h_oracle)-reference
    assembly=dot(T,[h-g for h,g in zip(h_rounded,h_model)])
    detector_integral=dot([a-b for a,b in zip(qhat,q)],v_rounded)
    solution=numeric-dot(qhat,v_rounded)
    pieces={'adapter':adapter,'operator_domain':operator_domain,
            'integration':assembly+detector_integral,'solution':solution}
    total=numeric-reference
    continuum.require((sum(pieces.values())-total).contains(0),'signed decomposition telescopes')
    dominance=[name for name,z in pieces.items() if z.abs_lower()>sum(w.abs_upper() for n,w in pieces.items() if n!=name)]
    return {'components':{name:{'value':pack(z),'magnitude':magnitude(z)} for name,z in pieces.items()},
        'integration_subparts':{'initial_assembly':pack(assembly),'detector_cubature':pack(detector_integral)},
        'total_error':pack(total),'total_magnitude':magnitude(total),
        'dominant_component':dominance[0] if dominance else 'UNRESOLVED',
        'triangle_upper':pack(sum(z.abs_upper() for z in pieces.values()))}


def compute(bits,out):
    p=json.loads((HERE/'PROTOCOL.json').read_text());ctx.prec=bits
    for filename,expected in json.loads((HERE/'FREEZE.json').read_text())['sha256'].items():
        continuum.require(hashlib.sha256((HERE/filename).read_bytes()).hexdigest()==expected,'frozen input '+filename)
    started=time.monotonic();ref=continuum.full_detector(bits,p['bessel_degree'],p['source_hcut'])
    continuum.require(all(max(w['normalized_value'].real.rad(),w['normalized_value'].imag.rad())<=arb(p['reference_radius_goal']) for w in ref['windows']),'full reference accuracy')
    v10=gzread(V10/'results'/f'BENCHMARK_{bits}.json.gz');v11=gzread(V11/'results'/f'BENCHMARK_{bits}.json.gz')
    archive=np.load(HERE.parent/'scalar_pilot_v0_1/results/clouds.npz');rows=[]
    original_scale=unpack(v10['normalization_A']).real/arb(1).exp()
    for key in p['clouds']:
        original=archive[key]
        old=next(r for r in v10['rows'] if r['key']==key)
        pu=next(r for r in v11['rows'] if r['key']==key)
        continuum.require(digest(original)==old['coordinates_sha256']==pu['coordinates_sha256'],'unchanged archive coordinates')
        cc,_,relations,_,_=previous.geometry.inventory(original,np.empty((0,4)))
        continuum.require(digest(cc)==old['counts_sha256'],'unchanged exact causal counts')
        continuum.require(digest(relations)==old['relations_sha256'],'unchanged exact causal relations')
        n=int(np.searchsorted(original[:,0],1.25,side='left'));x=original[:n];nh=int(np.searchsorted(x[:,0],-1,side='right'))
        continuum.require(nh==old['history_nodes']==pu['history_nodes'],'unchanged history')
        history=[];oracle_errors=[]
        for j,point in enumerate(x[:nh]):
            hkg,err=previous.initial_data.reference.off_center(point,1,arb(1).exp())
            continuum.require(hkg.is_finite(),'finite KG history reference')
            # Same normalized original source, not a new source profile.
            local=previous.initial_data.bump_jets(point,1,arb(1).exp())[0]
            projected=unpack(pu['levels'][-1]['coefficient_enclosures'][j][4])
            rounded=[acb(complex(float(z.real.mid()),float(z.imag.mid()))) for z in [local,projected]]
            history.append([hkg,local,projected]+rounded)
            oracle_errors.append({'quadrature_tail_radius_upper':pack((hkg.real.rad()**2+hkg.imag.rad()**2).sqrt())})
        _,values,_,edges,_=previous.propagation.solve(cc[:n,:n],np.empty((0,n),dtype=np.int32),512,'1/16',1,history,nh)
        numeric=np.zeros((n,2),dtype=complex)
        numeric[:nh]=[[complex(float(h[3].real.mid()),float(h[3].imag.mid())),complex(float(h[4].real.mid()),float(h[4].imag.mid()))] for h in history]
        for i in range(nh,n):
            if edges[i]:
                indices=[j for j,w in edges[i]];weights=np.array([float(w.mid()) for j,w in edges[i]])
                numeric[i]=weights@numeric[indices]
        continuum.require(np.isfinite(numeric).all(),'finite float solve')
        windows=[]
        for wi,oldw in enumerate(old['levels'][-1]['windows']):
            q=[unpack(z) for z in oldw['query_coefficients']]
            T=[unpack(z) for z in oldw['history_transfer']]
            qfloat=np.array([float(z.real.mid()) for z in q]);qhat=[acb(float(v)) for v in qfloat]
            actual=qfloat@numeric
            acont=ref['windows'][wi]['normalized_value']
            orac=dot(T,[h[0] for h in history]);models=[]
            continuum.require(orac.overlaps(dot(q,[v[0] for v in values])),'oracle forward/adjoint agreement')
            for index,name in [(1,'local_H1'),(2,'nonlocal_PU_H1')]:
                hmodel=[h[index] for h in history];hrounded=[h[index+2] for h in history]
                vrounded=[v[index+2] for v in values]
                model=dot(T,hmodel)
                continuum.require(model.overlaps(dot(q,[v[index] for v in values])),'model forward/adjoint agreement')
                continuum.require(dot(T,hrounded).overlaps(dot(q,vrounded)),'rounded forward/adjoint agreement')
                legacy=unpack(oldw['values'][4])/original_scale if index==1 else unpack(pu['levels'][-1]['windows'][wi]['responses'][4])
                continuum.require(model.overlaps(legacy),'unchanged previous adapter response')
                observed=acb(complex(actual[index-1]))
                ledger=split_error(q,qhat,T,hmodel,hrounded,[h[0] for h in history],vrounded,observed,acont)
                ledger.update({'adapter':name,'numeric_response':pack(observed),'ideal_adapter_response':pack(model),
                    'continuum_oracle_discrete_response':pack(orac),
                    'operator_reference_uncertainty_upper':pack(dot([t.abs_upper() for t in T],[(h[0].real.rad()**2+h[0].imag.rad()**2).sqrt() for h in history])),
                    'solution_budget_pass':bool(unpack(ledger['components']['solution']['magnitude']['upper']).real<=arb(p['solution_tolerance'])),
                    'history_budget_pass':bool(unpack(ledger['components']['adapter']['magnitude']['upper']).real<=arb(p['adapter_tolerance'])),
                    'total_accuracy_pass':bool((observed-acont).abs_upper()<=arb(p['comparison_tolerance']))})
                if old['source_support_hits']==0 and index==1:
                    continuum.require(observed.is_zero() and model.is_zero(),'original local source erased exactly')
                    continuum.require(all(unpack(ledger['components'][k]['value']).is_zero() for k in ['integration','solution']),'zero-source numerical terms exactly zero')
                models.append(ledger)
            windows.append({'time_window':p['time_windows'][wi],'models':models})
        rows.append({'key':key,'coordinates_sha256':digest(original),'counts_sha256':digest(cc),
            'source_support_hits':old['source_support_hits'],'history_nodes':nh,
            'oracle_history':[pack(h[0]) for h in history],'oracle_error_certificates':oracle_errors,'windows':windows})
        print(key,bits,'history',nh,'complete',flush=True)
    result={'schema':p['schema'],'precision_bits':bits,'reference':encode(ref),'rows':rows,
            'new_random_clouds':0,'new_causal_nodes':0,'reference_status':'FULL_SCALAR_REFERENCE_READY',
            'overall_status':'METHOD_HOLD','G1':'HOLD','elapsed_seconds':time.monotonic()-started}
    gzwrite(out,result);print('completed',bits,result['elapsed_seconds'],flush=True)
    return result


if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('--bits',type=int,choices=[128,192],required=True);ap.add_argument('--out',type=Path,required=True)
    args=ap.parse_args();compute(args.bits,args.out)
