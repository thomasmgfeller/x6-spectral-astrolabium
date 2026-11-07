"""Manual, bounded, offline volunteer jobs. No network, scheduler or cloud API."""
from fractions import Fraction as F
from functools import lru_cache
from math import prod
from pathlib import Path
import argparse, hashlib, json, platform, subprocess, sys, tempfile, time
import prepare as p
ROOT=p.ROOT
import geometry as g
import gauss
import intervals_fp as fp

S=1<<60
require=p.require

def read_json(path): return json.loads(Path(path).read_text())
def write_new(path,data):
    path=Path(path)
    # Never overwrite an existing result or silently replace partial evidence.
    with path.open('x') as f: json.dump(data,f,indent=2,sort_keys=True); f.write('\n')
def fpair(x):
    x=F(x); return x.numerator*S//x.denominator,-((-x.numerator*S)//x.denominator)
def ipair(x): return x.lo//(1<<100),-((-x.hi)//(1<<100))
def line(x): return ' '.join(map(str,x))

def check_manifest():
    manifest=read_json(ROOT/'manifest.json')
    for name,sha in manifest['sha256'].items():
        require(hashlib.sha256((ROOT/name).read_bytes()).hexdigest()==sha,'Source mismatch: '+name)
    return p.digest(manifest)

def compile_kernel(directory):
    exe=Path(directory)/'kernel'
    subprocess.run(['g++','-std=c++17','-O2','-Wall','-Wextra',str(ROOT/'kernel.cpp'),'-o',str(exe)],
                   capture_output=True,text=True,check=True,timeout=60)
    return exe

def invoke(exe,text,timeout=120):
    require(0<timeout<=120,'Timeout cap is 120 seconds')
    t=time.monotonic()
    result=subprocess.run([str(exe)],input=text,text=True,capture_output=True,check=True,timeout=timeout)
    return [list(map(int,row.split())) for row in result.stdout.splitlines()],time.monotonic()-t

@lru_cache(None)
def prepared_input(orders,h,mu,qs):
    n=len(orders[0]); rules=[gauss.rule(q) for q in qs]
    unique=[]; lookup={}; indices=[]
    for order in orders:
        row=[]
        for poly in g.action_polynomials(order,h)[0]:
            key=tuple(sorted(poly.items()))
            if key not in lookup: lookup[key]=len(unique);unique.append(key)
            row.append(lookup[key])
        indices.append(row)
    keys=sorted({key for poly in unique for key,_ in poly}); key_ids={x:i for i,x in enumerate(keys)}
    prefixes={():0};circuit=[];leaves=[]
    for row in indices:
        prefix=()
        for index in row:
            nxt=prefix+(index,)
            if nxt not in prefixes: circuit.append((prefixes[prefix],index));prefixes[nxt]=len(circuit)
            prefix=nxt
        leaves.append(prefixes[prefix])
    prefix=['integrate',line(ipair(fp.PI)),line([n,len(orders),len(unique),len(keys),len(circuit)])]
    suffix=[line(qs)]
    for nodes,weights,_ in rules: suffix.extend(line(ipair(x)+ipair(w)) for x,w in zip(nodes,weights))
    suffix.extend(line(key) for key in keys)
    for poly in unique:
        suffix.append(str(len(poly)))
        suffix.extend(line((key_ids[key],)+fpair(mu*c)) for key,c in poly)
    suffix.extend(line(x) for x in circuit); suffix.append(line(leaves))
    return prefix,suffix

def request(orders,h,mu,qs,begin,end):
    require(0<=begin<end<=prod(qs) and end-begin<=65536,'Bounded request')
    prefix,suffix=prepared_input(tuple(map(tuple,orders)),F(h),F(mu),tuple(qs))
    return '\n'.join(prefix+[line([begin,end])]+suffix)+'\n'

def config(plan,name):
    found=[c for c in plan['configs'] if c['id']==name]
    require(len(found)==1,'Unknown configuration');return found[0]

def job_range(plan,c,shard):
    require(type(shard) is int and 0<=shard<c['shards'],'Invalid shard ID')
    start=shard*plan['chunk_nodes'];return start,min(start+plan['chunk_nodes'],c['nodes'])

def raw_result(exe,orders,h,mu,qs,begin,end):
    text=request(orders,h,mu,qs,begin,end); rows,elapsed=invoke(exe,text)
    require(len(rows)==len(orders)+1 and len(rows[0])==3 and rows[0][2]==end-begin,'Output census')
    require(all(len(row)==4 for row in rows[1:]),'Complex rectangles')
    require(all(row[k]<=row[k+1] for row in rows for k in range(0,len(row)-1,2)),'Ordered endpoints')
    return {'input_sha256':hashlib.sha256(text.encode()).hexdigest(),
            'normalization':rows[0][:2], 'values':rows[1:]},elapsed

def environment():
    return {'python':platform.python_version(),'os':platform.system(),'machine':platform.machine(),
            'compiler':subprocess.run(['g++','--version'],capture_output=True,text=True,check=True,timeout=10).stdout.splitlines()[0]}

def execute(plan,c,shard,exe,source_hash):
    begin,end=job_range(plan,c,shard)
    data,elapsed=raw_result(exe,plan['natural_orders'],c['h'],c['mu'],c['q'],begin,end)
    return {'schema':'cst-dust-n5-shard-v1','plan_sha256':p.digest(plan),'source_manifest_sha256':source_hash,
        'config':c['id'],'shard':shard,'begin':begin,'end':end,'fraction_bits':60,
        'status':'CANDIDATE_REQUIRES_INDEPENDENT_REPLAY','data':data,
        'environment':environment(),'kernel_seconds':elapsed}

def validate_record(record,plan,c,source_hash):
    require(record['schema']=='cst-dust-n5-shard-v1','Result schema')
    require(record['plan_sha256']==p.digest(plan),'Plan identity')
    require(record['source_manifest_sha256']==source_hash,'Source identity')
    require(record['config']==c['id'] and record['fraction_bits']==60,'Configuration and scale')
    begin,end=job_range(plan,c,record['shard'])
    require((record['begin'],record['end'])==(begin,end),'Exact shard range')
    data=record['data'];require(len(data['normalization'])==2 and len(data['values'])==357,'Result dimensions')
    for row in [data['normalization']]+data['values']:
        require(all(type(x) is int for x in row) and len(row) in (2,4),'Integer endpoints')
        require(all(row[k]<=row[k+1] for k in range(0,len(row),2)),'Endpoint order')
    require(all(len(row)==4 for row in data['values']),'Four endpoints per geometry')

def aggregate(records,plan,c,source_hash):
    seen={}
    for record in records:
        validate_record(record,plan,c,source_hash);sid=record['shard']
        require(sid not in seen,'Duplicate shard; remove duplicate explicitly')
        seen[sid]=record
    require(set(seen)==set(range(c['shards'])),'Incomplete collection; no full amplitude produced')
    norm=[sum(r['data']['normalization'][j] for r in seen.values()) for j in range(2)]
    require(norm[0]<=S<=norm[1],'Full Jacobian normalization')
    values=[[sum(r['data']['values'][k][j] for r in seen.values()) for j in range(4)] for k in range(357)]
    qerror=F(c['quadrature_radius']);max_arith=F(0)
    for lo,hi,li,ui in values:
        error=F(hi-lo+ui-li,2*S);max_arith=max(max_arith,error)
        require(error<=F(plan['arithmetic_budget']),'Arithmetic budget exceeded')
        require(error+qerror<=F(plan['amplitude_tolerance']),'Total amplitude budget exceeded')
    channels=[]
    for coupling in map(F,plan['postprocess_g_over_pi']):
        z=(fp.ZERO,fp.ZERO)
        for order,(lo,hi,li,ui) in zip(plan['natural_orders'],values):
            phase=fp.cis(fp.PI*fp.I.rational(coupling*(p.m.gravity(p.m.with_anchor(tuple(order)))-1)))
            a=(fp.I(lo<<100,hi<<100),fp.I(li<<100,ui<<100))
            z=fp.cadd(z,fp.cmul(phase,a))
        z=(z[0]/357,z[1]/357)
        eps=z[0].radius()+z[1].radius()+qerror
        require(eps<=F(plan['amplitude_tolerance']),'Coherent amplitude budget exceeded')
        center=z[0].midpoint()**2+z[1].midpoint()**2;rad=2*eps+eps*eps
        channels.append({'g_over_pi':str(coupling),'real_interval':list(map(str,z[0].endpoints())),
            'imag_interval':list(map(str,z[1].endpoints())),'amplitude_radius':str(eps),
            'visibility_interval':[str(max(F(0),center-rad)),str(min(F(1),center+rad))]})
    return {'status':'PROVISIONAL_COMPLETE_COLLECTION_REQUIRES_INDEPENDENT_REPLAY',
        'plan_sha256':p.digest(plan),'config':c['id'],'shards':len(seen),'values':values,
        'fraction_bits':60,'quadrature_radius':str(qerror),'max_arithmetic_radius':str(max_arith),
        'channels':channels,'all_eight_physical_gates':'HOLD'}

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    sub=parser.add_subparsers(dest='mode',required=True)
    sub.add_parser('list')
    for name in ['pilot','run','verify','collect']:
        x=sub.add_parser(name);x.add_argument('--out',required=True)
        if name in ('pilot','run'):
            x.add_argument('--config',required=True);x.add_argument('--donated-compute',action='store_true',required=True,
                help='I am authorized to use this resource and cover all costs; no charge to Thomas Gfeller/project')
        if name=='run':x.add_argument('--shard',required=True,type=int)
        if name=='verify':
            x.add_argument('result');x.add_argument('--donated-compute',action='store_true',required=True)
        if name=='collect':x.add_argument('--config',required=True);x.add_argument('directory')
    args=parser.parse_args();source_hash=check_manifest();plan=read_json(ROOT/'plan.json')
    if args.mode=='list':
        print(json.dumps([{k:c[k] for k in ('id','q','nodes','shards')} for c in plan['configs']],indent=2));return
    require(not Path(args.out).exists(),'Output already exists')
    if args.mode=='collect':
        c=config(plan,args.config)
        records=[read_json(path) for path in sorted(Path(args.directory).glob('*.json'))]
        result=aggregate(records,plan,c,source_hash)
    else:
        with tempfile.TemporaryDirectory(prefix='dust-n5-') as tmp:
            exe=compile_kernel(tmp)
            if args.mode=='run':result=execute(plan,config(plan,args.config),args.shard,exe,source_hash)
            elif args.mode=='verify':
                record=read_json(args.result);c=config(plan,record['config'])
                validate_record(record,plan,c,source_hash)
                replay=execute(plan,c,record['shard'],exe,source_hash)
                require(replay['data']==record['data'],'Replay mismatch')
                result={'status':'EXACT_REPLAY_MATCH_NOT_AUTOMATICALLY_INDEPENDENT',
                        'result_sha256':hashlib.sha256(Path(args.result).read_bytes()).hexdigest(),
                        'replay':replay}
            else:
                c=config(plan,args.config);samples=[]
                # Stratify points across the entire grid. This is a timing/control
                # sample, never a complete quadrature or a production shard.
                for start in [0,c['nodes']//2,c['nodes']-64]:
                    data,elapsed=raw_result(exe,plan['natural_orders'],c['h'],c['mu'],c['q'],start,start+64)
                    samples.append({'begin':start,'end':start+64,'kernel_seconds':elapsed,'data':data})
                seconds=sum(s['kernel_seconds'] for s in samples)
                result={'status':'PILOT_ONLY_NOT_AN_INTEGRAL','plan_sha256':p.digest(plan),
                    'source_manifest_sha256':source_hash,'config':c['id'],'samples':samples,
                    'sample_nodes':192,'kernel_seconds':seconds,'environment':environment(),
                    'rough_core_hours':seconds/192*c['nodes']/3600,
                    'estimate_warning':'192 points only; setup and I/O excluded; no runtime guarantee'}
    write_new(args.out,result)
    print(json.dumps({'written':args.out,'status':result['status']}))

if __name__=='__main__':main()
