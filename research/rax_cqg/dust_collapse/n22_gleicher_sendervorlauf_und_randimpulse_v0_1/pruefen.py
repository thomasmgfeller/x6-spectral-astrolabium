"""Run the crossed comparison, the fixed-past boundary test and endpoint controls."""
import argparse,csv,io,json,subprocess,sys
from fractions import Fraction as F
from hashlib import sha256
from versuchsbasis import ROOT,inputs

def disjoint(a,b):
    return F(a[1])<F(b[0]) or F(b[1])<F(a[0])

def run():
    for k in ('Pruefplan','Ergaenzung','Lesergrenze','Impulsabgleich'):
        assert sha256((ROOT/(k+'.md')).read_bytes()).hexdigest()==(ROOT/(k+'.sha256')).read_text().split()[0]
    with inputs() as (parent,(dirs,y,w,rel,raw,coeff,free),seeds):
        from randversuch import certificate,SOURCES,PAST,POS,FIELDS
        from blockkontrolle import isolate,check_jac
        from leseregel import REFERENCE,ERROR,decode,digits
        # The prior point verifier is loaded under its own name.
        from importlib.util import spec_from_file_location,module_from_spec
        spec=spec_from_file_location('leser_408',parent/'pruefen.py')
        prev=module_from_spec(spec);spec.loader.exec_module(prev)
        verifier=prev.point_checker(dirs[6])
        target=F(seeds['0']['0']['y'][15]);spread=F(1,10**8)
        assert tuple(sorted(i for i,j in rel if j==16))==PAST and (16,8) in rel
        assert all((3,j) not in rel and (j,3) not in rel for j in (15,16,21))
        prior=json.loads((parent/'Ergebnisse.json').read_text())
        assert prior['physical_readings']==0 and prior['p3_not_run']==60
        cases=[];blocks={};jac_tests=0;hashes={}
        collars={}
        for K in SOURCES:
            data=subprocess.check_output([sys.executable,'-B',str(dirs[6]/'eichpunkt.py'),'0',str(K)])
            collars[K]=json.loads(data)
            hashes[str(K)]=sha256(data).hexdigest()
            for J in SOURCES:
                seed=seeds[str(K)]['0']
                z,state=certificate(seed,collars[K],J,coeff,rel,free)
                assert z['decisions']==[int(J*10**6)]
                if J==K:
                    cert=verifier({},seed,rel,raw)
                    # Compare all 25 coordinates with the old, unique solution.
                    beta,q=map(F,(cert['upper_beta'],cert['upper_q']))
                    assert beta+q<1 and cert['collar']==collars[K]
                    for typ,indices,actual,rad in [('y',free,state[0],F(1,10**7)),('w',POS,state[1],F(1,10**8))]:
                        for j in indices:
                            x=F(seed[typ][j])
                            err=rad*beta/(1-q)
                            assert all(abs(F(v)-x)+err<F(1,10**8 if typ=='y' else 10**9) for v in actual[j].data())
                if K==0:blocks[str(J)]=isolate(state,J,coeff,free)
                jac_tests+=check_jac(state,J,coeff,free)
                cases.append(dict(kind='fest',K=str(K),J=str(J),target=None,radius='0',**z))
        assert all(disjoint(blocks[str(a)]['clock15'],blocks[str(b)]['clock15']) for a,b in zip(SOURCES,SOURCES[1:]))
        mixed=[]
        for J in SOURCES:
            for radius in (F(0),spread/2,spread):
                z,state=certificate(seeds['0']['0'],collars[F(0)],J,coeff,rel,free,target,radius)
                assert all(F(v)==target+d for v,d in zip(z['clock']['15'],(-radius,radius)))
                assert all(z['weights_past'][str(j)]==(['0','0'] if j==15 else ['1/8','1/8']) for j in PAST)
                assert all(z['clock'][str(j)]==collars[F(0)][str(j)][0] for j in (0,1,2,3,7))
                if radius==0:jac_tests+=check_jac(state,J,coeff,free)
                if radius<=spread/2:assert z['decisions']==[int(J*10**6)]
                mixed.append(dict(kind='abgleich',K='0',J=str(J),target=str(target),radius=str(radius),**z))
        controls=[]
        for offset in (-spread,spread):
            z,_=certificate(seeds['0']['0'],collars[F(0)],F(0),coeff,rel,free,target+offset)
            bounds=list(map(F,z['clock']['21']))
            for e in (-ERROR,F(0),ERROR):
                ds=list(digits(bounds[0]+e,bounds[1]+e))
                for ref in range(REFERENCE-1,REFERENCE+2):
                    output={decode(n,ref) for n in ds}
                    if len(output)==1 and 0 not in output:
                        controls.append(dict(target_offset=str(offset),read_error=str(e),reference=ref,codes=ds,decision=output.pop()))
                        break
                else:continue
                break
            cases.append(dict(kind='randpunkt',K='0',J='0',target=str(target+offset),radius='0',**z))
        assert {c['target_offset'] for c in controls}=={str(spread),str(-spread)}
        sets=[r for r in mixed if F(r['radius'])==spread]
        for field in ('8','21'):
            assert all(disjoint(a['clock'][field],b['clock'][field]) for a,b in zip(sets,sets[1:]))
        different=[j for j in ('0','1','2','3') if all(disjoint(a['early_currents'][j],b['early_currents'][j]) for a,b in zip(sets,sets[1:]))]
        from impulsabgleich import certify_currents
        null=next(c for c in cases if c['kind']=='fest' and c['J']==c['K']=='0')
        def rounded_center(z):
            return F(round(sum(map(F,z))/2*10**15),10**15)
        goals=[target]+[rounded_center(null['early_currents'][str(i)]) for i in range(4)]
        balanced=[certify_currents(seeds['0']['0'],collars[F(0)],j,coeff,free,rel,goals) for j in SOURCES]
        assert all(r['fixed_past']==balanced[0]['fixed_past'] and r['goals']==balanced[0]['goals'] for r in balanced)
        assert all(v['equations']==30 and v['decisions']==[int(F(v['J'])*10**6)] for v in balanced)
        separation=all(disjoint(a['receiver'],b['receiver']) for i,a in enumerate(balanced) for b in balanced[i+1:])
        assert separation
        return dict(target=str(target),cases=cases+mixed,block=blocks,collar_sha256=hashes,
                    matched_currents=balanced,matched_currents_analog_separation=separation,
                    unequal_boundary_currents_over_full_target_band=different,misclassifications=controls,
                    independent_jacobian_entries=jac_tests+sum(t['jacobian_entries'] for t in balanced),physical_readings=0,P3_NOT_RUN=60)

def table(r):
    s=io.StringIO();w=csv.writer(s,delimiter='\t',lineterminator='\n')
    w.writerow(['Versuch','K','J','Ziel15','Zielradius','Y15_unten','Y15_oben','Y8_unten','Y8_oben','Y21_unten','Y21_oben','Code_min','Code_max','Leserlabels','Bildnorm_max'])
    for v in r['cases']:
        w.writerow([v['kind'],v['K'],v['J'],v['target'],v['radius'],*v['clock']['15'],*v['clock']['8'],*v['clock']['21'],*v['receiver_codes'],','.join(map(str,v['decisions'])),v['upper_image']])
    for v in r['matched_currents']:
        w.writerow(['impulsabgleich','0',v['J'],r['target'],'0',r['target'],r['target'],*v['control_values']['y8'],*v['receiver'],*v['receiver_codes'],','.join(map(str,v['decisions'])),v['upper_image']])
    return s.getvalue()

if __name__=='__main__':
    ap=argparse.ArgumentParser()
    ap.add_argument('--ausgabe',action='store_true')
    args=ap.parse_args()
    if not __debug__:raise ValueError('Run without -O')
    r=run()
    for name,data in [('Ergebnisse.json',json.dumps(r,indent=2,sort_keys=True)+'\n'),('Versuchsregister.tsv',table(r))]:
        path=ROOT/name
        if args.ausgabe:path.write_text(data)
        else:assert path.read_text()==data
    print('Versuche',len(r['cases'])+len(r['matched_currents']),'Jacobi-Einträge',r['independent_jacobian_entries'],
          'sichere Fehlablesungen',len(r['misclassifications']),'getrennte Randimpulse',r['unequal_boundary_currents_over_full_target_band'])
