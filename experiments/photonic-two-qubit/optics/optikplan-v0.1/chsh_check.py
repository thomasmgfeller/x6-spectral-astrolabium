#!/usr/bin/env python3
"""OPTIK-CHSH-0.1: count-only conditional statistical check, never hardware certification.

Assumes iid Bernoulli parity within each setting conditional on its pair count.
Does not validate raw timestamps, pairing, stationarity or fair sampling.
"""
import argparse
import csv
import json
import math
import re
import sys
from pathlib import Path
from scipy.stats import beta

SETTINGS = ('00', '01', '10', '11')
FIELDS = ('setting', 'pp', 'pm', 'mp', 'mm')
ALPHA = 0.01
MIN_N = 2000

def lower_cp(k, n, alpha=ALPHA/4):
    if type(k) is not int or type(n) is not int or not (0 <= k <= n) or n < 1:
        raise ValueError('Require integers 0 <= k <= n and n >= 1')
    if not (0 < alpha < 1):
        raise ValueError('Require 0 < alpha < 1')
    if k == 0:
        return 0.0
    value = float(beta.ppf(alpha, k, n-k+1))
    if not math.isfinite(value):
        raise ValueError('Non-finite beta quantile')
    return value

def evaluate(counts, data_kind):
    if data_kind not in ('synthetic', 'measurement'):
        raise ValueError('data_kind must be synthetic or measurement')
    if set(counts) != set(SETTINGS):
        raise ValueError('Exactly four settings 00, 01, 10, 11 required')
    rows=[]
    for s in SETTINGS:
        c=counts[s]
        if not isinstance(c, (list, tuple)) or len(c)!=4:
            raise ValueError('Four counts in order pp, pm, mp, mm required')
        if any(type(x) is not int or x<0 for x in c):
            raise ValueError('Counts must be nonnegative integers; bool and float are invalid')
        n=sum(c)
        if n>10**9:
            raise ValueError('Count exceeds declared numerical domain n <= 1e9')
        pp,pm,mp,mm=c
        k=pp+mm if s=='11' else pm+mp
        e=(pp+mm-pm-mp)/n if n else None
        rows.append({'setting':s,'counts_pp_pm_mp_mm':list(c),'n':n,'favourable_k':k,
                     'E':e,'q_hat':k/n if n else None,
                     'one_sided_CP_lower':lower_cp(k,n) if n else None})
    complete=all(r['n']>0 for r in rows)
    sufficient=all(r['n']>=MIN_N for r in rows)
    t=2*sum(r['q_hat'] for r in rows)-4 if complete else None
    lower=2*sum(r['one_sided_CP_lower'] for r in rows)-4 if complete else None
    met=sufficient and lower is not None and lower>2.0
    status=('HOLD_INSUFFICIENT_DATA' if not sufficient else
            'STATISTICAL_CRITERION_MET' if met else 'STATISTICAL_CRITERION_NOT_MET')
    return {'protocol_id':'OPTIK-CHSH-0.1','data_kind':data_kind,
            'scope':'COUNT_ONLY_CONDITIONAL_STATISTICS','alpha':ALPHA,'alpha_each':ALPHA/4,
            'n_min_each':MIN_N,'rows':rows,'T_signed':t,'abs_T_descriptive':abs(t) if t is not None else None,
            'T_lower_99_percent':lower,'statistical_criterion_met':met,'statistical_status':status,
            'hardware_validation':'NOT_ASSESSED','raw_data_integrity':'NOT_ASSESSED',
            'model_assumptions':'NOT_ASSESSED','overall_CHSH_acceptance':'NOT_ASSESSED',
            'warning':'No hardware or entanglement certification. Synthetic data are not experimental evidence.'}

def read_csv(path):
    out={}
    with Path(path).open(newline='',encoding='utf-8') as f:
        reader=csv.DictReader(f)
        if tuple(reader.fieldnames or []) != FIELDS:
            raise ValueError('CSV header must be exactly setting,pp,pm,mp,mm')
        for row in reader:
            if None in row or any(v is None for v in row.values()):
                raise ValueError('Malformed CSV row')
            setting=row['setting']
            if setting not in SETTINGS or setting in out:
                raise ValueError('Unexpected or duplicate setting')
            vals=[]
            for field in FIELDS[1:]:
                raw=row[field]
                if re.fullmatch(r'0|[1-9][0-9]*',raw) is None:
                    raise ValueError('Counts must be decimal nonnegative integers')
                vals.append(int(raw))
            out[setting]=vals
    return out

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('counts_csv')
    parser.add_argument('--data-kind',choices=('synthetic','measurement'),required=True)
    parser.add_argument('--output')
    args=parser.parse_args()
    try:
        result=evaluate(read_csv(args.counts_csv),args.data_kind)
    except (OSError,ValueError) as exc:
        parser.exit(2,str(exc)+'\n')
    text=json.dumps(result,indent=2,ensure_ascii=False,allow_nan=False)+'\n'
    if args.output:
        Path(args.output).write_text(text,encoding='utf-8')
    else:
        sys.stdout.write(text)

if __name__=='__main__':
    main()
