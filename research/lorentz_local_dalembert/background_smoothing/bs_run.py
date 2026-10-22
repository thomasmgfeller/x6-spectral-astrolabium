"""Certified common diagonal background and full-law smoothing with residual mass.
SPDX-License-Identifier: Apache-2.0
"""
import sys,json,hashlib
from pathlib import Path
import numpy as np
HERE=Path(__file__).resolve().parent
sys.path.insert(0,str(HERE.parent/'adaptive_surface'))
from as_run import F,read,save,outward,geometry,seed_rectangles,strip,floor,ceil,constant,void_bounds
from as_audit import reconstruct
from sf_run import sqrt_bounds
from ja_run import classify as volume_classify

def ledgers(table):
    inc={};out={}
    for (a,b),(lo,hi) in table.items():
        assert a!=b and 0<=lo<=hi
        for ledger,label in [(out,a),(inc,b)]:
            x,y=ledger.get(label,(F(0),F(0)));ledger[label]=(x+lo,y+hi)
    return inc,out

def original_background(lower,table,residual):
    inc,out=ledgers(table);labels=set(inc)|set(out)
    assert residual>=0 and all(x>=0 for d in lower for x in d.values())
    return {b:max(F(0),lower[0].get(b,F(0))-out.get(b,(0,0))[1]-residual,
                  lower[1].get(b,F(0))-inc.get(b,(0,0))[1]-residual) for b in labels}

def law(background,table,residual):
    assert residual>=0 and all(x>=0 for x in background.values())
    inc,out=ledgers(table);J=F(0);delta_sum=F(0);terms={}
    for b in sorted(set(inc)|set(out)):
        il,iu=inc.get(b,(F(0),F(0)));ol,ou=out.get(b,(F(0),F(0)))
        delta=max(abs(il-ou),abs(iu-ol));delta_sum+=delta;m=background.get(b,F(0))
        denom=(sqrt_bounds(m+ol)[0]+sqrt_bounds(m+il)[0])**2
        term=min(delta,delta*delta/denom) if denom else delta
        # Round every upper contribution outward before summing rational quantities.
        term=F(outward(term, digits=30)[1]);J+=term;terms[b]=str(term)
    D=delta_sum/2
    assert max(D,residual)<=1
    hellinger=sqrt_bounds(void_bounds(J)[1])[1] if J<=1 else F(1)
    coupling=void_bounds(D)[1];known=min(F(1),hellinger,coupling)
    bad=void_bounds(residual)[1]
    combined=bad+(1-bad)*known
    return dict(tv_upper=outward(combined)[1],known_component_tv_upper=outward(known)[1],
        known_hellinger_tv_upper=outward(min(F(1),hellinger))[1],known_coupling_tv_upper=outward(coupling)[1],
        root_distance_squared_upper=outward(J)[1],residual_mean_upper=outward(residual)[1],
        per_label_J_upper=terms)

def local_background(w,z,ends,selected,base,contract):
    data=read(HERE.parent/'adaptive_surface'/'cells.json.gz')
    allcells={r['id']:r for r in data['evaluated_cells']};removed={k for s in data['splits'] for k in s['parents']}
    leaves={k:r for k,r in allcells.items() if k not in removed}
    reps={}
    for key,cell in sorted(leaves.items()):
        if cell['state']!='transfer':continue
        for role,b in enumerate(cell['labels']):
            if base.get(b,F(0))>0:continue
            candidate=(F(cell['mass'][0]),key,role)
            if b not in reps or candidate[0]>reps[b][0]:reps[b]=candidate
    seeds=seed_rectangles(z,selected,64);seed_map={k:(s,r) for k,s,r in seeds}
    node=selected['node'];h=F(selected['step']);v=z[node];unit=contract['coordinate_unit']
    changed=[row[:] for row in z];changed[node][1]+=h
    lower=[];upper=[];metadata=[]
    for label,(_,key,role) in sorted(reps.items()):
        side,rect=reconstruct(seed_map,key);sign,_,_=strip(rect,v[1:],h)
        X=[(a+b)/2 for a,b in rect]
        roots=[sqrt_bounds(sum((a-b)**2 for a,b in zip(X,tip[1:]))) for tip in [v,changed[node]]]
        active=(sign>0) if role==0 else (sign<0)
        for k in contract['offset_multipliers']:
            offset=k*h;half=offset/8
            radius=max(x[1] for x in roots)+offset if active else min(x[0] for x in roots)-offset
            center=[v[0]+side*radius,*X]
            lo=[floor((x-half)*unit) for x in center];hi=[ceil((x+half)*unit) for x in center]
            lower.append(lo);upper.append(hi);metadata.append(dict(label=label,cell=key,role=role,multiplier=k,lower=lo,upper=hi))
    lower=np.array(lower,dtype=np.int64);upper=np.array(upper,dtype=np.int64)
    certified=[];results=[]
    for g in [z,changed]:
        lo=np.array([[floor(x*unit) for x in row] for row in g],dtype=np.int64)
        hi=np.array([[ceil(x*unit) for x in row] for row in g],dtype=np.int64)
        results.append(volume_classify(lower,upper,lo,hi,ends))
    factor=F(w['rho'])*F(w['scale'])**3/unit**3;best=dict(base)
    for i,meta in enumerate(metadata):
        if all(k[i] and bytes(b[i]).hex()==meta['label'] for k,b in results):
            mean=factor*int(np.prod(upper[i]-lower[i]));meta['mean']=str(mean);certified.append(meta)
            best[meta['label']]=max(best.get(meta['label'],F(0)),mean)
    return best,dict(candidate_count=len(metadata),representative_labels=len(reps),certified_boxes=certified,
        original_background={k:str(v) for k,v in sorted(base.items())},background={k:str(v) for k,v in sorted(best.items())})

def run():
    for name,h in read(HERE/'freeze.json')['files'].items():assert hashlib.sha256((HERE/name).read_bytes()).hexdigest()==h,name
    c=read(HERE/'contract.json');w,z,ends,selected=geometry()
    final=read(HERE.parent/'adaptive_surface'/'rounds.json')[-1]
    table={tuple(k.split('>')):tuple(map(F,v)) for k,v in final['transfers'].items()};R=F(final['exact_unknown_upper'])
    previous=read(HERE.parent/'adaptive_surface'/'summary.json')['tv_upper']
    atom=read(HERE.parent/'joint_atoms'/'partitions.json.gz')[-1]['geometries']
    factor=F(w['rho'])*F(w['scale'])**3/65536**3
    lower=[{k:factor*v for k,v in d['atom_integer_volumes'].items()} for d in atom]
    base=original_background(lower,table,R);background,boxes=local_background(w,z,ends,selected,base,c)
    supported={edge:v for edge,v in table.items() if all(background[b]>0 for b in edge)}
    residual=R+sum(v[1] for edge,v in table.items() if edge not in supported)
    methods=dict(inherited_background=law(base,table,R),local_background=law(background,table,R),
                 supported_edges=law(background,supported,residual))
    best=min([F(previous)]+[F(r['tv_upper']) for r in methods.values()])
    local=methods['local_background'];target=F(local['known_coupling_tv_upper'])**2
    diagnostics=dict(sufficient_J_budget_to_match_known_coupling=outward(target)[0],
        current_J_upper=local['root_distance_squared_upper'],
        ratio_to_sufficient_J_budget=outward(F(local['root_distance_squared_upper'])/target)[1],
        smallest_positive_background_lower=outward(min(x for x in background.values() if x>0))[0],
        largest_background_lower=outward(max(background.values()))[0],
        largest_J_contributions=[dict(label=b,J_upper=v,background_lower=str(background[b])) for b,v in
            sorted(local['per_label_J_upper'].items(),key=lambda kv:(-F(kv[1]),kv[0]))[:10]],
        scope='A sufficient sqrt(J) target for this certificate, not a necessary condition, required physical intensity multiplier or actual-TV lower bound.')
    summary=dict(status='SMOOTHING_GAIN_CERTIFIED' if best<F(previous) else 'HOLD_BACKGROUND_SMOOTHING',
        pair_unchanged=True,previous_tv_upper=previous,tv_upper=outward(best)[1],
        involved_labels=len(base),previous_positive_background_labels=sum(x>0 for x in base.values()),
        positive_background_labels=sum(x>0 for x in background.values()),
        certified_common_boxes=len(boxes['certified_boxes']),candidate_boxes=boxes['candidate_count'],
        supported_edges=len(supported),total_edges=len(table),
        unknown_transfer_mean_upper=outward(R)[1],
        method_tv_upper={k:v['tv_upper'] for k,v in methods.items()},
        symmetric_operator_gap=selected['relative'],strong_pair_found=False,
        scope='Common diagonal intensity is derived conservatively, never identified with separate marginal lower volumes. Unknown and excluded transfers remain in a Poisson residual coupling. No actual-TV or reconstruction-accuracy claim.')
    return boxes,methods,diagnostics,summary

if __name__=='__main__':
    for name,data in zip(['background.json.gz','methods.json','diagnostics.json','summary.json'],run()):
        if '--verify' in sys.argv:assert data==read(HERE/name),name
        else:save(HERE/name,data)
        if name=='summary.json':print(json.dumps(data))
