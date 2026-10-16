"""Targeted regression probes against pinned, unchanged implementation files.

Not a complete requalification of all modules. Python 3.12, numpy, jsonschema,
Node.js >=22 and the pinned Git objects are needed. No network is used.
"""
import argparse
import copy
import hashlib
import importlib.util
import json
from pathlib import Path
import subprocess
import tempfile

ROOT=Path(__file__).resolve().parents[2]
BASE='dc50ffb228e442a230a32e4437e8e452a90b39ad'
FP='f22030f2dae0aa670cdbc450c5e881ce250b36b8'
ND='1a02c482d59a42d554337fb83e0f6d6e6d84b516'


def require(ok,message):
    if not ok:raise ValueError(message)
def digest(data):return hashlib.sha256(data).hexdigest()
def encode(x):return json.dumps(x,sort_keys=True,separators=(',',':'),allow_nan=False).encode()
def load_module(name,path):
    spec=importlib.util.spec_from_file_location(name,path);m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m);return m


def run():
    sources={};checks=[]
    with tempfile.TemporaryDirectory(prefix='x6-h7-audit-') as tmp:
        root=Path(tmp)
        def source(commit,path):
            raw=subprocess.check_output(['git','show',commit+':'+path],cwd=ROOT)
            sources[commit+':'+path]=digest(raw)
            dest=root/commit/path;dest.parent.mkdir(parents=True,exist_ok=True);dest.write_bytes(raw);return dest
        def record(name,detail):checks.append({'name':name,'status':'PASS','detail':detail})
        exact=load_module('h7_exact',source(BASE,'research/lorentz_n7_complete/independent.py'))
        twin=load_module('h7_twin',source(BASE,'research/rax_cqg/benchmark-v0.2.0/rax_cqg_twin.py'))
        js=source(BASE,'research/rax_cqg/benchmark-v0.2.0/web/rax_core.js')
        agent=load_module('h7_agent',source(BASE,'agent/lorentz_spectral.py'))
        witnesses=json.loads(source(BASE,'research/lorentz_n7_complete/results/counterexamples.json').read_text())
        inputs=json.loads(source(BASE,'research/lorentz_n6_residuals/inputs.json').read_text())
        pairs=[]
        for w in witnesses:
            pairs.append([(r['id'],[[int(x) for x in row] for row in r['relation_rows']]) for r in [w['left'],w['right']]])
        pairs.append([(r['id'],r['causal_matrix']) for r in inputs['records'] if r['id'].startswith('n8-degree-')])
        records=[];pair_results=[]
        class Budget:
            def check(self):pass
        for pair in pairs:
            features=[];raw_records=[]
            for name,c in pair:
                obj=twin.CausalSet.from_matrix(c);f=exact.feature(c);features.append(f)
                r={'schema':'RAX-CQG-EXPERIMENT-0.2','relation_rows':obj.rows(),'relation_sha256':obj.digest(),'metrics':{'untrusted':'deliberately not used'}}
                loaded=twin.load_experiment(r)
                require(loaded.rows()==obj.rows(),'Python import changed full relation')
                require(twin.thinning_path(loaded,retention=1,steps=2)['path'][-1]['relation_rows']==obj.rows(),'thinning q=1 changed relation')
                raw_records.append(r);records.append(r)
                if len(c)==7:
                    require(list(map(list,agent.spectral_key(c,Budget())))==f['polynomials_S_A_K'],'agent exact spectrum disagrees')
                    try:agent.canonical_key(c,Budget())
                    except ValueError:pass
                    else:raise ValueError('agent failed to enforce n<=5 canonicalization gate')
            a,b=features
            require(not exact.isomorphic(pair[0][1],pair[1][1]),'counterexample unexpectedly isomorphic')
            signature=lambda f:[f['n'],f['polynomials_S_A_K'],f['minimal_maximal'],f['W_future'],f['W_past']]
            require(signature(a)==signature(b),'H7 signature differs')
            require(raw_records[0]['relation_rows']!=raw_records[1]['relation_rows'],'same relation')
            require(raw_records[0]['relation_sha256']!=raw_records[1]['relation_sha256'],'same byte digest')
            pair_results.append({'ids':[x[0] for x in pair],'n':a['n'],'H7_equal':True,'isomorphic':False,
                                 'same_D':a['degree_pairs']==b['degree_pairs'],
                                 'matrix_hashes':[r['relation_sha256'] for r in raw_records],
                                 'bdg4_brackets':[twin.BDGAction.bracket_4d(twin.CausalSet.from_matrix(c)) for _,c in pair]})
        record('python_raw_relation_roundtrip','All six witnesses retain their complete relation and distinct within-pair byte digests; digests are not isomorphism keys.')
        record('thinning_retention_one','All six full relations survive q=1 induced-suborder processing.')
        record('agent_size_gate','Four n=7 spectra agree exactly; the unchanged n<=5 canonicalizer rejects every n=7 input.')
        payload=root/'records.json';payload.write_bytes(encode(records))
        javascript='''const fs=require('fs');const core=require(process.argv[1]);const records=JSON.parse(fs.readFileSync(process.argv[2]));
const rows=r=>r.map(x=>x.join(''));const result=records.map(record=>{
const r=core.loadExperiment(record);if(JSON.stringify(rows(r))!==JSON.stringify(record.relation_rows))throw Error('JS relation changed');
const path=core.thinning(r,1,2).path;if(JSON.stringify(path[2].relation_rows)!==JSON.stringify(record.relation_rows))throw Error('JS thinning changed');
return {rows:rows(r),bdg4:core.diagnose(r).bdg4_bracket};});process.stdout.write(JSON.stringify(result));'''
        node=json.loads(subprocess.check_output(['node','-e',javascript,str(js),str(payload)],text=True))
        require([x['rows'] for x in node]==[x['relation_rows'] for x in records],'JS roundtrip')
        require([x['bdg4'] for x in node]==[v for p in pair_results for v in p['bdg4_brackets']],'JS/Python action mismatch')
        record('javascript_raw_relation_roundtrip','Unchanged JS core retains all six matrices and agrees on exact integer BDG brackets; browser UI not exercised.')
        # Exercise the full pinned fingerprint schema/validator with a new audit
        # fixture. All fields, sources and comparison scope are explicit.
        fp_path=source(FP,'research/fingerprint_v1/validate.py')
        for name in ['x6-fingerprint.schema.json','comparison-event.schema.json']:
            source(FP,'research/fingerprint_v1/'+name)
        fp=load_module('h7_fingerprint',fp_path)
        from jsonschema.exceptions import ValidationError
        template=json.loads(source(FP,'research/fingerprint_v1/examples/n6-0073.json').read_text())
        event_template=json.loads(source(FP,'research/fingerprint_v1/examples/separation-event.json').read_text())
        fixture=root/'fixture';fixture.mkdir()
        evidence={'protocol':{'definition':'Exact H7 vector and optional D, full transitive relation; audit fixtures only'},
                  'atlas':records,'verification':pair_results,'generator':{'method':'probes.py; exact independent.feature; no physical measurement'}}
        artifacts=[]
        for name,value in evidence.items():
            raw=encode(value);(fixture/(name+'.json')).write_bytes(raw)
            artifacts.append({'id':name,'path':name+'.json','sha256':digest(raw),'media_type':'application/json',
                              'role':{'protocol':'protocol','atlas':'raw','verification':'report','generator':'code'}[name]})
        for index,pair in enumerate(pairs):
            files=[]
            for name,c in pair:
                f=exact.feature(c);r=copy.deepcopy(template)
                r['fingerprint_id']='fp-'+name;r['subject']={'id':name,'kind':'CAUSAL_ORDER','description':'Pinned counterexample used as a dependency-audit fixture'}
                r['context']['comparison_domain']='h7-dependency-audit';r['context']['scale']='finite order; dimensionless'
                r['claim']['scope']='Audit fixture; exact invariants only; no identity or physical equivalence inference'
                r['artifacts']=artifacts;r['provenance']['command']='python probes.py';r['provenance']['method_version']='h7-dependency-audit-1'
                r['layers']={k:{'status':'NOT_APPLICABLE','reason':'Outside the registered audit comparison'} for k in r['layers']}
                values=[f['n'],*f['minimal_maximal'],f['W_future'],f['W_past']]+[v for poly in f['polynomials_S_A_K'] for v in poly]
                feature=copy.deepcopy(template['layers']['sector']['features'][0]);feature.update(id='sector.H7',definition='n, endpoints, directed forks, then monic S/A/K coefficients',depends_on=[])
                feature['value']={'format':'INTEGER_VECTOR','values':list(map(str,values))}
                r['layers']['sector']={'status':'AVAILABLE','features':[feature]}
                if index==2:
                    extra=copy.deepcopy(feature);extra['id']='sector.D';extra['definition']='Sorted full-relation paired degrees';extra['value']['values']=[str(v) for p in f['degree_pairs'] for v in p]
                    r['layers']['sector']['features'].append(extra)
                raw=encode(r);path=name+'.json';(fixture/path).write_bytes(raw);files.append({'id':r['fingerprint_id'],'path':path,'sha256':digest(raw)})
            event=copy.deepcopy(event_template);event['event_id']='audit-pair-'+str(index);event['fingerprints']=files
            event['comparison_domain']='h7-dependency-audit';event['protocol_sha256']=artifacts[0]['sha256'];event['scope']='Registered audit pair only'
            event['steps']=[{'index':0,'feature_ids':['sector.H7']+(['sector.D'] if index==2 else []),'outcome':'EXACT_COLLISION','witness_feature_ids':[],
                             'reason':'Equal tested observables, distinct orders','selection_basis':'Fixed known counterexamples'}]
            event['stop_reason']='NO_ADMISSIBLE_OBSERVABLE'
            require(fp.validate(event,fixture)=='VALID_EXACT_COMPARISON_EVENT','fingerprint rejected legitimate collision')
            bad=copy.deepcopy(event);bad['physical_equivalence']='EQUIVALENT'
            try:fp.validate(bad,fixture)
            except ValidationError:pass
            else:raise ValueError('fingerprint accepted physical equivalence')
            bad=copy.deepcopy(event);bad['stop_reason']='SEPARATED_WITHIN_SCOPE'
            try:fp.validate(bad,fixture)
            except ValueError:pass
            else:raise ValueError('fingerprint accepted unsupported separation')
        record('fingerprint_collision_semantics','Three complete schema-valid collision events accepted, including the known n=8 D collision; all three false equivalence and all three false separation claims rejected. Validator checks stored values, not their raw-matrix derivation.')
        nd=load_module('h7_discovery',source(ND,'experimental/neutral_discovery/discovery.py'))
        candidates=nd.generator_candidates();classes=nd.explanation_classes(candidates)
        require(nd.explanation_classes(candidates+[copy.deepcopy(candidates[0])])==classes,'predictive quotient duplication changed classes')
        require(len(classes)==3,'unexpected predictive classes')
        contract=nd.make_contract();require(contract['claims']['geometry']=='NOT_IDENTIFIED','discovery claims identified geometry')
        record('discovery_predicted_observations_only','The three intervention-prediction classes are unchanged by duplicating a generator representation; geometry remains NOT_IDENTIFIED. This does not certify unseen mechanisms or future observation catalogues.')
        return {'schema':'x6.h7-dependency-probes/1','status':'PASS_WITH_SCOPE_LIMITS','base_commit':BASE,'sources':sources,
                'checks':checks,'pairs':pair_results,'scope':'Targeted imported kernels and comparison semantics; not full module, hardware or physical validation.'}


if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--output',type=Path,required=True);a=parser.parse_args()
    result=run();a.output.parent.mkdir(parents=True,exist_ok=True);a.output.write_text(json.dumps(result,indent=2,ensure_ascii=False)+'\n')
    print(json.dumps({'status':result['status'],'checks':len(result['checks']),'witnesses':2*len(result['pairs'])}))
