import argparse
import json
from pathlib import Path
import subprocess
import sys
ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT/'experimental/rax_guarded'))
import runner as r
import worker as w

p=argparse.ArgumentParser();p.add_argument('--qualification',type=Path,required=True);p.add_argument('--base');a=p.parse_args()
d=r.read(ROOT/'docs/validation-v1/ERROR_BUDGET.json');q=r.read(a.qualification)
w.require(d['limits']=={'accepted_forbidden_access':0,'accepted_output_forgery':0,'unresolved_in_profile':0},'NONZERO_ERROR_BUDGET')
w.require(q['status']=='PASS' and q['source_hashes']==r.source_hashes(),'STALE_QUALIFICATION')
ids=[x['id'] for x in d['findings']];w.require(len(ids)==len(set(ids)),'DUPLICATE_FINDING')
controls={x['id'] for x in q['controls'] if x['result']=='REJECTED_EXPECTED'}
w.require(len(controls)==q['negative_controls']==33 and len(q['controls'])==33,'CONTROL_COUNT')
w.require(q['actual_future_bank_mutation']=='PASS_PREFIX_INVARIANCE_AND_LATER_CHANGE' and q['actual_holdout_mutation']=='PASS_PREDICTIONS_UNCHANGED_SCORES_CHANGED','INEFFECTIVE_ISOLATION_TEST')
for f in d['findings']:
 w.require(f['history'] and set(f['regressions'])<=controls,'MISSING_REGRESSION')
 w.require(f['scope']!='IN_PROFILE' or f['state']=='MITIGATED','UNRESOLVED_BLOCKER')
if a.base:
 b=subprocess.run(['git','show',a.base+':docs/validation-v1/ERROR_BUDGET.json'],cwd=ROOT,capture_output=True)
 if b.returncode==0:
  old=json.loads(b.stdout);current={x['id']:x for x in d['findings']}
  for f in old['findings']:
   w.require(f['id'] in current and current[f['id']]['history'][:len(f['history'])]==f['history'],'FINDING_HISTORY_REMOVED')
print(json.dumps({'status':'PASS_ERROR_BUDGET','in_profile_unresolved':0,'open_outside_profile':[x['id'] for x in d['findings'] if x['state']=='OPEN'],'forbidden_acceptances':0}))
