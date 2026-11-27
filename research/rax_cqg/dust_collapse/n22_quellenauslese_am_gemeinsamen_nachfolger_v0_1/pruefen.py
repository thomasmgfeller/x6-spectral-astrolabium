"""Replay continuous receiver tubes, independent point certificates and the digital reader."""
import argparse,csv,io,json
from fractions import Fraction as F
from hashlib import sha256
from importlib.util import spec_from_file_location,module_from_spec
from leserbasis import model,LIMIT,SOURCES,ROOT,KEY
from leseregel import evaluate,verify_reader,REFERENCE,digits

def encode(v):
    return json.dumps(v,indent=2,sort_keys=True,ensure_ascii=False)+'\n'

def point_checker(base):
    # The archived verifier originally builds the serial order itself. Supply
    # the independently reconstructed common-receiver order as in PR 406.
    code=(base/'zeugnis.py').read_text()
    for old,new in [('def certify(d,proposal):','def certify(d,proposal,edges,coefficients):'),
                    ("rel,c=structure(set(d['order']),row,case[0])","rel,c=set(edges),dict(coefficients)")]:
        assert code.count(old)==1
        code=code.replace(old,new)
    p=base/'leserpunkt.py';p.write_text(code)
    spec=spec_from_file_location('leserpunkt',p)
    mod=module_from_spec(spec);spec.loader.exec_module(mod)
    return mod.certify

def intervals(rows,k):
    return (min(F(r[k][0]) for r in rows),max(F(r[k][1]) for r in rows))

def envelope(lo,hi):
    return list(map(str,(lo,hi)))

def study():
    for name in ('Pruefplan','Vorlaufkontrolle'):
        assert sha256((ROOT/(name+'.md')).read_bytes()).hexdigest()==(ROOT/(name+'.sha256')).read_text().split()[0]
    seeds=json.loads((ROOT/'Startwerte.json').read_text())
    verify_reader()
    with model() as (dirs,y,w,rel,raw,coeff,free):
        from ableitung import lifted_functions
        from feldroehre import solution_line,environment,certify
        from leserkontrolle import action_jacobian,collar_secants
        fun=lifted_functions();old=point_checker(dirs[6])
        jac_entries=secant_entries=0
        past=sorted(i for i,j in rel if j==16)
        assert past==[0,1,2,15]
        central=json.loads((dirs[1]/'Zeugenzentrum.json').read_text())
        out={};points=[];material_ref=None
        for source in SOURCES:
            data=seeds[str(source)];line=solution_line(data)
            for drift,r in data.items():
                assert F(r['source'])==source and F(r['drift'])==F(drift)
                assert (r['cid'],r['past'],r['future'])==KEY and r['row']==central['row'] and r['case']=='B+'
            jac_entries+=action_jacobian(data['0'],coeff,free,source)
            independent_collars=[]
            env=environment(y,w,rel,coeff,free,source,line,fun)
            leaves=[]
            def traverse(a,b,depth):
                cell=certify(env,a,b)
                if cell:
                    cell['codes']=evaluate(cell['receiver'],int(source/LIMIT))
                    leaves.append(cell)
                else:
                    if depth>=10:raise ValueError('Unclosed drift interval')
                    m=(a+b)/2
                    traverse(a,m,depth+1)
                    traverse(m,b,depth+1)
            traverse(-LIMIT,LIMIT,0)
            segments=[tuple(map(F,c['drift'])) for c in leaves]
            assert segments[0][0]==-LIMIT and segments[-1][1]==LIMIT
            assert all(a<b for a,b in segments) and all(b==c for (_,b),(c,_) in zip(segments,segments[1:]))
            receiver=envelope(*intervals(leaves,'receiver'))
            antecedent=envelope(*intervals(leaves,'antecedent'))
            codes=evaluate(receiver,int(source/LIMIT))
            out[str(source)]=dict(leaves=leaves,receiver=receiver,antecedent=antecedent,codes=codes)
            for drift in [-LIMIT,-LIMIT/2,F(0),LIMIT/2,LIMIT]:
                if str(drift) in data:
                    prop=data[str(drift)]
                else:
                    # The half-drift predictions use the same affine line, with no numerical refit.
                    prop=dict(data['0'],drift=str(drift))
                    for k in ('y','w'):
                        prop[k]=[str(c+drift*s) for c,s in line[k]]
                p=old({},prop,rel,raw)
                independent_collars.append((drift,p['collar']))
                material=[p['collar'][str(j)] for j in (0,1,2)]
                assert all(F(a)==F(b) for row in material for a,b in row)
                if material_ref is None:
                    material_ref=material
                assert material==material_ref
                beta,q=map(F,[p['upper_beta'],p['upper_q']])
                assert beta+q<1 and p['equations']==25 and p['strict_relations']==152 and p['positive_weights']==11
                err=beta*F(1,10**7)/(1-q)
                point=dict(drift=str(drift),source=str(source),upper_beta=p['upper_beta'],upper_q=p['upper_q'])
                # The precise point fixed point lies in the affine tube at the same
                # drift: check every free coordinate, not just the receiver's clock.
                for k,indices,radius in [('y',free,F(1,10**7)),('w',(4,5,6,11,12,13,14,16,18,19,21),F(1,10**8))]:
                    for j in indices:
                        c,s=line[k][j]
                        tube_rad=F(1,10**8) if k=='y' and j in (15,21) else radius
                        assert abs(F(prop[k][j])-c-drift*s)+beta*radius/(1-q)<tube_rad
                live=[c for c in leaves if F(c['drift'][0])<=drift<=F(c['drift'][1])]
                assert live
                for j,k in [(15,'antecedent'),(21,'receiver')]:
                    center=F(prop['y'][j]);point[k]=envelope(center-err,center+err)
                    assert all(F(c[k][0])<=center+err and center-err<=F(c[k][1]) for c in live)
                point['codes']=evaluate(point['receiver'],int(source/LIMIT))
                if drift==source==0:
                    assert list(digits(*map(F,point['receiver'])))==[REFERENCE]
                points.append(point)
            secant_entries+=collar_secants(source,independent_collars,y,w,fun)
            print('Quelle',source,'Driftintervalle',len(leaves),'Codes',codes,flush=True)
    gaps={}
    for field in ('receiver','antecedent'):
        ordered=[out[str(s)][field] for s in reversed(SOURCES)]
        distances=[F(b[0])-F(a[1]) for a,b in zip(ordered,ordered[1:])]
        assert min(distances)>0
        gaps[field]=list(map(str,distances))
    return dict(case='216141/229383/0/+',sources=out,point_checks=points,
                adjacent_gaps=gaps,past_of_sender=past,material_past_clocks_and_weights=material_ref,
                exact_jacobian_entries=jac_entries,native_secant_checks=secant_entries,
                p3_not_run=60,physical_readings=0)

def table(result):
    buf=io.StringIO()
    wr=csv.writer(buf,delimiter='\t',lineterminator='\n')
    wr.writerow(['Quelle','Drift_unten','Drift_oben','Y21_unten','Y21_oben','Code_min','Code_max','Y15_unten','Y15_oben','Kontraktion_max','Bildnorm_max'])
    for s in SOURCES:
        for c in result['sources'][str(s)]['leaves']:
            wr.writerow([str(s),*c['drift'],*c['receiver'],*c['codes'],*c['antecedent'],c['upper_contraction'],c['upper_image']])
    return buf.getvalue()

if __name__=='__main__':
    ap=argparse.ArgumentParser()
    ap.add_argument('--ausgabe',action='store_true',help='Ergebnisdateien regenerieren')
    args=ap.parse_args()
    if not __debug__:raise RuntimeError('Assertions required')
    result=study()
    for name,data in [('Ergebnisse.json',encode(result)),('Driftregister.tsv',table(result))]:
        target=ROOT/name
        if args.ausgabe:target.write_text(data)
        else:assert target.read_text()==data
    print('15 Punktkontrollen. Getrennte Klassen am Empfänger und im Sendervorlauf.')
