"""Apply the fixed two-model decision using observed relation counts."""
from argparse import ArgumentParser
from fractions import Fraction
from pathlib import Path
from math import comb
import json

ROOT=Path(__file__).resolve().parent
DESIGN=json.loads((ROOT/'design.json').read_text())

def thresholds(method):
    if method=='matching':
        opt=DESIGN[method]
        return opt['m'],opt['reject_curved_K_le'],opt['reject_flat_K_ge']
    if method!='full_order':
        raise ValueError('unknown method')
    opt=DESIGN[method]; total=comb(opt['n'],2)
    low=Fraction(opt['reject_curved_U_le'])*total
    high=Fraction(opt['reject_flat_U_ge'])*total
    return total,low.__floor__(),high.__ceil__()

def classify(method,n,count):
    if type(n) is not int or n!=DESIGN[method]['n']:
        raise ValueError('event count differs from certified budget')
    total,low,high=thresholds(method)
    if type(count) is not int or not 0<=count<=total:
        raise ValueError('invalid number of comparable pairs')
    return [name for name,retained in [('Minkowski',count<high),('de Sitter h=1/2',count>low)] if retained]

if __name__=='__main__':
    p=ArgumentParser()
    p.add_argument('method',choices=['full_order','matching'])
    p.add_argument('n',type=int)
    p.add_argument('count',type=int)
    args=p.parse_args()
    print(json.dumps(classify(args.method,args.n,args.count)))
