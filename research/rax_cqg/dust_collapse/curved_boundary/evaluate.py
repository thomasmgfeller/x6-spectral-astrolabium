"""Join held-out reference values to the frozen predictions and apply the gates."""
import csv
import json
from pathlib import Path
import numpy as np
from common import write_rows
def read(path): return list(csv.DictReader(open(path)))
def key(row): return tuple(float(row[k]) for k in ['s','P','F','lam'])
cfg=json.loads(Path('design.json').read_text());spec=cfg['gates']
a={key(r):r for r in read('predictions.csv')}
b={key(r):r for r in read('reference.csv')}
assert set(a)==set(b) and len(a)==24
rows=[]
for key_,r in b.items():
    p=a[key_]
    val=float(r['R']); d=float(p['pred'])
    raw=val-1; cor=val/d-1
    gap=max(float(r['order_gap']),float(r['method_gap']))
    rows.append(dict(s=key_[0],P=key_[1],F=key_[2],lam=int(key_[3]),reference=val,prediction=d,
        raw=raw,corrected=cor,flat_corrected=val/float(p['pred_flat'])-1,no_log_corrected=val/float(p['pred_no_log'])-1,
        numerical_gap=gap,improved=abs(cor)<abs(raw),passed=(gap<=spec['numerical_abs'] and d>0 and abs(cor)<=spec['raw_and_corrected_mass_band'] and abs(cor)<abs(raw))))
write_rows('holdout.csv',rows)
for den in cfg['intensities']:
    part=[r for r in rows if r['lam']==den]
    print(den,'raw',min(r['raw'] for r in part),max(r['raw'] for r in part),
          'corrected', min(r['corrected'] for r in part),max(r['corrected'] for r in part),
          'raw pass',sum(abs(r['raw'])<=.1 for r in part),'pass',sum(r['passed'] for r in part))
print('numeric max',max(r['numerical_gap'] for r in rows))
high=[r for r in rows if r['lam']>=3000000]
print('high maxima / RMS',[(name,max(abs(r[name]) for r in high),float(np.sqrt(np.mean([r[name]**2 for r in high]))))
                          for name in ['raw','flat_corrected','no_log_corrected','corrected']])
