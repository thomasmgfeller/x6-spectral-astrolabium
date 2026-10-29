"""Frozen archived-cloud benchmark; all requested terms reach fixed observables."""
import gzip,json,time
import numpy as np
from flint import arb,acb,ctx
from common import HERE,PILOT,old,check,digest,balls,protocol
import geometry,initial_data as data,propagation as prop

def gzwrite(path,obj):path.write_bytes(gzip.compress((json.dumps(obj,ensure_ascii=False,allow_nan=False,separators=(',',':'))+'\n').encode(),mtime=0))
def gzread(path):return json.loads(gzip.decompress(path.read_bytes()))

def probe_reference(bits):
    rows=json.loads((HERE.parent/'certified_budget_v0_3/results/SOURCE.json').read_text())['rows']
    suffix='_192bit' if bits==192 else ''
    rows+=json.loads((HERE.parent/f'massive_reference_v0_5/results/SOURCE{suffix}.json').read_text())['rows']
    result=[[None]*3 for _ in range(28)]
    for r in rows:result[r['probe_index']][r['mass']]=balls.decode(r['value'])
    check(all(v is not None for row in result for v in row),'all 84 existing probe references')
    return result

def source_reference(x,out):
    A=data.source.normalization(ctx.prec)[0];rows=[]
    for i,point in enumerate(x):
        vals=[data.exact_bump(point,m,A) for m in [0,1,2]]
        check(all(z.is_finite() and max(z.real.rad(),z.imag.rad())<=arb(protocol()['reference_component_radius_max']) for z in vals),'compact source reference radius')
        rows.append([balls.encode(z) for z in vals])
        if i%40==0:print('source reference',ctx.prec,i,len(x),flush=True)
    result={'precision_bits':ctx.prec,'cloud':'d0_r00','coordinates_sha256':digest(x),'active_nodes':len(x),'values':rows,
            'normalization_A':balls.encode(A),'scope':'all active nodes including prescribed history on one fixed archived cloud'}
    gzwrite(out/f'SOURCE_NODES_{ctx.prec}.json.gz',result)
    return [[balls.decode(z) for z in row] for row in rows],A

def initial_matrix(x,nh,kind,mass,truth,A=None):
    ks=[0,2,4,8] if kind=='wave' else [mass];nf=len(ks);h=[]
    floats=np.column_stack([data.float_wave_history(x,k,o) if kind=='wave' else data.float_bump_history(x,mass,o,float(A.mid())) for o in [1,3] for k in ks])
    check(np.isfinite(floats).all(),'finite numeric initial adapter')
    for i,point in enumerate(x[:nh]):
        jets=[data.wave(point,k)[1:] if kind=='wave' else data.bump_jets(point,mass,A) for k in ks]
        groups=[truth[i]]+[[data.extension(point,j,o) for j in jets] for o in [1,3]]
        groups += [[acb(complex(z)) for z in floats[i,j*nf:(j+1)*nf]] for j in [0,1]]
        h.append([z for group in groups for z in group])
    return h,floats

def operator_controls(values,truth,truthp,erows,prows,nh,nf):
    """Local normalized defects and their independently accumulated absolute transport."""
    n=len(values);r=[];major=[[acb(0)]*nf for _ in range(nh)]
    for i in range(nh,n):
        predicted=prop.dot_row(erows[i],truth,nf)
        defect=[truth[i][k]-predicted[k] for k in range(nf)];r.append(defect)
        v=prop.dot_row(erows[i],major,nf,True)
        major.append([acb(v[k].real+defect[k].abs_upper()) for k in range(nf)])
    bounds=[];pdef=[]
    err=[[values[i][k]-truth[i][k] for k in range(nf)] for i in range(n)]
    for j,row in enumerate(prows):
        predicted=prop.dot_row(row,truth,nf);rp=[truthp[j][k]-predicted[k] for k in range(nf)]
        transported=prop.dot_row(row,err,nf);out=prop.dot_row(row,values,nf)
        for k in range(nf):check((out[k]-truthp[j][k]-transported[k]+rp[k]).contains(0),'operator-defect transport identity')
        v=prop.dot_row(row,major,nf,True)
        bounds.append([balls.encode(v[k].real+rp[k].abs_upper()) for k in range(nf)]);pdef.append(rp)
    return {'normalized_local_defect_RMS':[prop.enclose_norm([v[k] for v in r]) for k in range(nf)],
            'probe_direct_defect_RMS':[prop.enclose_norm([v[k] for v in pdef]) for k in range(nf)],
            'absolute_transported_defect_upper':bounds,'includes_finite_domain_error':True}

def compute_case(x,p,cc,pc,nu,e,kind,mass,truth,truthp,A=None):
    n=len(truth);nh=int(np.searchsorted(x[:n,0],-1,side='right'));nf=len(truth[0]);h,hfloat=initial_matrix(x,nh,kind,mass,truth,A)
    out,values,gain,erows,prows=prop.solve(cc[:n,:n],pc[:,:n],nu,e,mass,h,nh)
    check(all(z.is_finite() and max(z.real.rad(),z.imag.rad())<=arb(protocol()['solution_component_radius_max']) for row in out for z in row),'solution enclosure radius')
    numeric,backward=prop.float_solve(cc,pc,x,p,nu,arb(e),mass,hfloat)
    check(np.isfinite(numeric).all(),'finite float propagation')
    controls=operator_controls(values,truth,truthp,erows,prows,nh,nf)
    fields=[]
    for order in [1,3]:
        group=1 if order==1 else 2
        for k in range(nf):
            row=prop.field_result(out,truthp,numeric,p,nf,k,order,gain)
            row['field']=f'wave_k{[0,2,4,8][k]}' if kind=='wave' else f'compact_m{mass}'
            hist=max((h[i][group*nf+k]-h[i][k]).abs_upper() for i in range(nh))
            row['initial_history_sup_error_upper']=balls.encode(hist)
            row['initial_error_at_probes_upper']=[balls.encode(hist*g) for g in gain]
            fields.append(row)
    return {'kind':kind,'mass':mass,'nu':nu,'epsilon':e,'precision_bits':ctx.prec,'active_nodes':n,'history_nodes':nh,
            'float_backward_residual':backward,'operator_controls':controls,'fields':fields}

def compute(bits,out,geometry_records=None):
    ctx.prec=bits;p=old.probes()[:28];archive=np.load(PILOT/'results/clouds.npz');records=json.loads((PILOT/'results/RUNS.json').read_text())
    source_x=archive['d0_r00'];source_x=source_x[source_x[:,0]<1]
    source_values,A=source_reference(source_x,out);source_p=probe_reference(bits);rows=[];geom=[]
    for rec in records:
        key=rec['key'];x=archive[key];check(digest(x)==rec['coordinates_sha256'],'canonical cloud identity '+key)
        cc,pc,relations,pr,stats=geometry.inventory(x,old.probes())
        check(digest(cc)==rec['interval_counts_sha256'] and digest(pc)==rec['probe_counts_sha256'],'exact causal counts preserve original graph '+key)
        region,region_stats=geometry.region(x,4);check(np.all(region),'exact archived Omega4 membership')
        geo={'key':key,'N':len(x),'coordinates_sha256':digest(x),'relations_sha256':digest(relations),'probe_relations_sha256':digest(pr),
             'counts_sha256':digest(cc),'probe_counts_sha256':digest(pc),'history_mask_sha256':digest(x[:,0]<=-1),'active_mask_sha256':digest(x[:,0]<1),**stats}
        geo['domain_mask_sha256']=digest(region);geo['domain_relation_stats']=region_stats
        geom.append(geo);n=int(np.searchsorted(x[:,0],1,side='left'))
        truth=[[data.wave(point,k)[0] for k in [0,2,4,8]] for point in x[:n]]
        truthp=[[data.wave(point,k)[0] for k in [0,2,4,8]] for point in p]
        for e in protocol()['epsilon']:
            row=compute_case(x,p,cc,pc[:28],rec['nu'],e,'wave',1,truth,truthp);row['key']=key;rows.append(row)
            if key=='d0_r00':
                for m in [0,1,2]:
                    row=compute_case(x,p,cc,pc[:28],rec['nu'],e,'compact',m,[[v[m]] for v in source_values],[[v[m]] for v in source_p],A)
                    row['key']=key;rows.append(row)
        print('propagation',bits,key,flush=True)
    check(len(rows)==201,'192 wave cells and nine compact-source cells')
    result={'schema':'cspp.scalar-propagation/0.7','precision_bits':bits,'rows':rows,'geometry':geom,'new_random_realizations':0,
            'scientific_status':protocol()['scientific_status']}
    gzwrite(out/f'BENCHMARK_{bits}.json.gz',result)
    return result
