"""Certified finite exterior attribution. No random calls or source changes."""
import argparse, gzip, hashlib, json, sys, time
from fractions import Fraction as F
from pathlib import Path
import numpy as np
from flint import arb, acb, ctx

HERE=Path(__file__).resolve().parent
ROOT=HERE.parent/'source_snapshot/research/cspp'
sys.path.insert(0,str(HERE.parent/'operator_gebiet_v0_15'))
from run import require, pack, unpack, dump, loadgz, digest, sha, geometry
sys.path.insert(0,str(ROOT/'detector_methods_v0_10'))
import time_integral
sys.path.insert(0,str(ROOT/'scalar_propagation_v0_7'))
import propagation, initial_data

def plan(): return json.loads((HERE/'PROTOCOL.json').read_text())
def gzwrite(path,obj):
    with gzip.GzipFile(filename=str(path),mode='wb',mtime=0) as f:
        f.write((json.dumps(obj,sort_keys=True,allow_nan=False)+'\n').encode())
def dot(a,b): return sum((x*y for x,y in zip(a,b)),acb(0))
def enc(z):
    z=acb(z)
    return {'value':pack(z),'abs_lower':pack(z.abs_lower()),'abs_upper':pack(z.abs_upper()),
            'component_radius_upper':pack(max(z.real.rad(),z.imag.rad()))}
def intersect(a,b):
    a,b=acb(a),acb(b)
    require(a.overlaps(b),'intersection of valid certificates')
    return acb(a.real.intersection(b.real),a.imag.intersection(b.imag))
def check_freeze():
    d=json.loads((HERE/'FREEZE.json').read_text())
    for path,expected in d['sha256'].items():
        require(sha(HERE/path)==expected,'frozen input '+path)

def can_reach_detector(p):
    t=F(float(p[0]));dt=F(5,4)-t
    if dt<=0:return False
    r2=sum((F(float(v))-c)**2 for v,c in zip(p[1:],[F(0),F(0),F(3,2)]))
    return r2<(dt+F(1,2))**2

def active_kg_zero(p):
    t=F(float(p[0]));r2=sum(F(float(v))**2 for v in p[1:])
    return t> -1 and r2 >= (t+F(3,2))**2

def inventory(key):
    archive=np.load(ROOT/'scalar_pilot_v0_1/results/clouds.npz')
    x=archive[key];y=archive[key+'_outer'];xmap={tuple(p):i for i,p in enumerate(x)}
    full,_,_,_,stats=geometry.inventory(y,np.empty((0,4)))
    old,_,_,_,_=geometry.inventory(x,np.empty((0,4)))
    all_inner=[i for i,p in enumerate(y) if tuple(p) in xmap]
    require(np.array_equal(full[np.ix_(all_inner,all_inner)],old),'all inner interval counts invariant')
    keep=[i for i,p in enumerate(y) if can_reach_detector(p)]
    z=y[keep];c=full[np.ix_(keep,keep)]
    reduced,_,_,_,_=geometry.inventory(z,np.empty((0,4)))
    require(np.array_equal(c,reduced),'causal-past pruning preserves all interval counts')
    inn=[i for i,p in enumerate(z) if tuple(p) in xmap];ext=[i for i,p in enumerate(z) if tuple(p) not in xmap]
    hist=[i for i,p in enumerate(z) if p[0]<=-1];nh=len(hist)
    require(hist==list(range(nh)),'sorted history block')
    ia=[i for i in inn if i>=nh];ea=[i for i in ext if i>=nh]
    require(all(active_kg_zero(z[i]) for i in ea),'exterior active KG support is zero')
    # A relevant exterior point cannot be causally downstream of any inner node:
    # otherwise convexity with an inner detector endpoint would be violated.
    require(all(c[i,j]<0 for i in ext for j in inn),'no inner-to-relevant-exterior feedback')
    return x,z,c,inn,ext,ia,ea,nh,stats

def coefficients():
    check_freeze();ctx.prec=192;p=plan();start=time.monotonic();rows=[]
    old=loadgz(ROOT/'detector_methods_v0_10/results/BENCHMARK_192.json.gz')
    for key in p['pairs']:
        x,z,c,inn,ext,ia,ea,nh,stats=inventory(key)
        table=propagation.coefficient_table(len(z),512,'1/16',1)
        levels=time_integral.integrate(z,c,table,p['windows'],p['spatial_grids'],
            lambda n:print('coefficients',key,'grid',n,flush=True),deadline=start+p['resource_limit_seconds_per_stage'])
        saved=[];prior=next(r for r in old['rows'] if r['key']==key);xmap={tuple(v):i for i,v in enumerate(x)}
        for level in levels:
            qs=[]
            for wi,q in enumerate(level['q']):
                q=[acb(v) for v in q]
                for j in inn:q[j]=intersect(q[j],unpack(prior['levels'][-1]['windows'][wi]['query_coefficients'][xmap[tuple(z[j])]]))
                qs.append([pack(v) for v in q])
            saved.append({k:v for k,v in level.items() if k!='q'}|{'q':qs})
        row={'key':key,'retained_coordinates_sha256':digest(z),'retained_counts_sha256':digest(c),
             'N4':len(x),'N5':len(np.load(ROOT/'scalar_pilot_v0_1/results/clouds.npz')[key+'_outer']),
             'retained_nodes':len(z),'history_nodes':nh,'inner_active_nodes':len(ia),
             'exterior_history_nodes':sum(j<nh for j in ext),'exterior_active_nodes':len(ea),
             'inner_indices':inn,'exterior_indices':ext,'levels':saved,'geometry_stats':stats}
        rows.append(row);gzwrite(HERE/'results/COEFFICIENTS_192.json.gz',{'rows':rows,'complete':len(rows)==4})
    dump(HERE/'results/COEFFICIENT_RUNTIME.json',{'seconds':time.monotonic()-start,'complete':True})

def forward(c,table,h,nh,allowed=None,clamp=None):
    v=list(h)+[acb(0) for _ in range(len(c)-nh)]
    for i in range(nh,len(c)):
        if allowed is not None and i not in allowed:continue
        if clamp is not None and i in clamp:continue
        v[i]=sum((table[int(c[i,j])]*v[j] for j in range(i) if c[i,j]>=0 and (allowed is None or j in allowed)),acb(0))
    return v

def compute(bits):
    check_freeze();ctx.prec=bits;p=plan();start=time.monotonic();co=loadgz(HERE/'results/COEFFICIENTS_192.json.gz')
    require(co['complete'],'complete geometry stage')
    old=loadgz(ROOT/f'full_continuum_v0_12/results/BENCHMARK_{bits}.json.gz');rows=[]
    for key in p['pairs']:
        x,z,c,inn,ext,ia,ea,nh,stats=inventory(key);table=propagation.coefficient_table(len(z),512,'1/16',1)
        oldrow=next(r for r in old['rows'] if r['key']==key);xmap={tuple(v):i for i,v in enumerate(x)}
        h=[];herr=[]
        for i,point in enumerate(z[:nh]):
            if i in inn:
                value=unpack(oldrow['oracle_history'][xmap[tuple(point)]])
            else:
                value,_=initial_data.reference.off_center(point,1,arb(1).exp())
            require(value.is_finite(),'finite unchanged KG history')
            require(max(value.real.rad(),value.imag.rad())<arb('1e-18'),'history arithmetic radius')
            h.append(value);herr.append(max(value.real.rad(),value.imag.rad()))
        v5=forward(c,table,h,nh)
        h4=[v if j in inn else acb(0) for j,v in enumerate(h)];v4=forward(c,table,h4,nh,set(inn))
        vclamp=forward(c,table,h,nh,clamp=set(ea))
        coef=next(r for r in co['rows'] if r['key']==key)
        require(digest(z)==coef['retained_coordinates_sha256'] and digest(c)==coef['retained_counts_sha256'],'locked geometry reuse')
        windows=[]
        for wi in range(2):
            last=None;levels=[]
            for level in coef['levels']:
                q=list(map(unpack,level['q'][wi]));adj=[q[i] if i in ia else acb(0) for i in range(len(z))]
                for i in reversed(ia):
                    for j in ia:
                        if j<i and c[i,j]>=0:adj[j]+=adj[i]*table[int(c[i,j])]
                L={j:q[j]+sum((adj[i]*table[int(c[i,j])] for i in ia if c[i,j]>=0),acb(0)) for j in ext}
                direct=dot([q[j] for j in ext],[v5[j] for j in ext])
                transported=dot([L[j]-q[j] for j in ext],[v5[j] for j in ext])
                delta=dot([L[j] for j in ext],[v5[j] for j in ext])
                delta_forward=dot([q[j] for j in inn],[v5[j]-v4[j] for j in inn])+direct
                require(delta.overlaps(delta_forward),'outer forcing forward and adjoint agree')
                delta=intersect(delta,delta_forward)
                prescribed=dot([L[j] for j in ext if j<nh],[h[j] for j in ext if j<nh])
                extra=dot([L[j] for j in ea],[v5[j] for j in ea])
                clamp_forward=dot([q[j] for j in inn],[vclamp[j]-v4[j] for j in inn])+dot([q[j] for j in ext],[vclamp[j] for j in ext])
                require(prescribed.overlaps(clamp_forward),'KG-prescribed boundary forward/adjoint')
                require((delta-prescribed-extra).contains(0),'history plus exterior dynamics split')
                original=unpack(oldrow['windows'][wi]['models'][0]['continuum_oracle_discrete_response'])
                original=intersect(original,dot([q[j] for j in inn],[v4[j] for j in inn]))
                extended=intersect(original+delta,dot(q,v5))
                reference=unpack(old['reference']['windows'][wi]['normalized_value'])
                vals={'old_response':original,'extended_response':extended,'shell_change':delta,
                      'direct_exterior':direct,'inner_transport':transported,'KG_prescribed_shell':prescribed,
                      'extra_exterior_dynamics':extra,'old_error':original-reference,
                      'extended_error':extended-reference,'KG_prescribed_error':original+prescribed-reference}
                if last is not None:vals={k:intersect(v,last[k]) for k,v in vals.items()}
                last=vals
                levels.append({'grid':level['n'],'quantities':{k:enc(v) for k,v in vals.items()}})
            q=list(map(unpack,coef['levels'][-1]['q'][wi]));T=q.copy()
            for i in range(len(z)-1,nh-1,-1):
                for j in range(i):
                    if c[i,j]>=0:T[j]+=T[i]*table[int(c[i,j])]
            require(dot(T[:nh],h).overlaps(last['extended_response']),'full history transfer agrees')
            uncertain=sum((T[j].abs_upper()*arb(2).sqrt()*herr[j] for j in range(nh)),arb(0))
            windows.append({'window':p['windows'][wi],'levels':levels,'reference':pack(reference),
                'external_state_transfer':[{'index':j,'coefficient':pack(L[j])} for j in ext],
                'history_uncertainty_effect_upper':pack(uncertain),
                'finite_history_gain_upper':pack(sum(t.abs_upper() for t in T[:nh])),
                'shell_component_radius_pass':bool(max(last['shell_change'].real.rad(),last['shell_change'].imag.rad())<=arb(p['existing_comparison_tolerance'])),
                'extended_accuracy_excluded':bool(last['extended_error'].abs_lower()>arb(p['existing_comparison_tolerance'])),
                'KG_prescribed_accuracy_excluded':bool(last['KG_prescribed_error'].abs_lower()>arb(p['existing_comparison_tolerance']))})
        row={k:coef[k] for k in ['key','N4','N5','retained_nodes','history_nodes','inner_active_nodes','exterior_history_nodes','exterior_active_nodes','retained_coordinates_sha256','retained_counts_sha256']}
        row.update({'history':[pack(v) for v in h],'exterior_active_values':[{'index':j,'KG_value':['0','0'],'discrete_value':pack(v5[j])} for j in ea],
            'windows':windows});rows.append(row)
        gzwrite(HERE/f'results/ATTRIBUTION_{bits}.json.gz',{'precision_bits':bits,'rows':rows,'complete':len(rows)==4,
            'G1':'HOLD','METHOD':'HOLD','infinite_domain_attribution':'NOT_CERTIFIED','new_random_calls':0,'elapsed_seconds':time.monotonic()-start})
        print('attribution',bits,key,'complete',round(time.monotonic()-start,2),flush=True)

if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('stage',choices=['coefficients','solve']);ap.add_argument('--bits',type=int,choices=[128,192],default=128);a=ap.parse_args()
    coefficients() if a.stage=='coefficients' else compute(a.bits)
