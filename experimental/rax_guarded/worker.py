"""Trusted finite policy interpreter. Input is JSON data, never executable code.
Only public model, validated plan and past observations enter this process.
"""
from fractions import Fraction as F
import json
import math
import sys


def require(ok, reason):
    if not ok: raise ValueError(reason)


def exact_keys(d, names):
    require(type(d) is dict and set(d) == set(names), 'UNEXPECTED_FIELDS')


def integer(x, low, high):
    require(type(x) is int and low <= x <= high, 'INTEGER_RANGE')
    return x


def parse(text):
    require(len(text.encode()) <= 65536, 'INPUT_SIZE')
    def pairs(items):
        d={}
        for k,v in items:
            require(k not in d, 'DUPLICATE_KEY');d[k]=v
        return d
    def reject(_): raise ValueError('NONFINITE')
    return json.loads(text, object_pairs_hook=pairs, parse_constant=reject)


def model(value):
    require(type(value) is list and 1 <= len(value) <= 8, 'MODEL_SIZE')
    require(type(value[0]) is list and 1 <= len(value[0]) <= 8, 'ACTION_SIZE')
    n=len(value[0]);out=[]
    for row in value:
        require(type(row) is list and len(row)==n, 'MODEL_SHAPE')
        converted=[]
        for v in row:
            require(type(v) is str and len(v)<32, 'RATIONAL_REQUIRED')
            p=F(v);require(0<p<1 and p.denominator<=65536, 'PROBABILITY_RANGE')
            # Exact Bernoulli sampling from bits in the broker.
            require(p.denominator & (p.denominator-1)==0,'DYADIC_REQUIRED')
            converted.append(p)
        out.append(tuple(converted))
    return tuple(out)


def expression(expr, step, actions, depth=0, counter=None):
    counter=[0] if counter is None else counter;counter[0]+=1
    require(depth<=8 and counter[0]<=255,'POLICY_COMPLEXITY')
    require(type(expr) is dict,'EXPRESSION_TYPE')
    if set(expr)=={'action'}: integer(expr['action'],0,actions-1)
    elif set(expr)=={'choose'}: require(expr['choose']=='information_gain','UNKNOWN_PRIMITIVE')
    elif set(expr)=={'if_observation','then','else'}:
        integer(expr['if_observation'],0,step-1)
        expression(expr['then'],step,actions,depth+1,counter)
        expression(expr['else'],step,actions,depth+1,counter)
    else: raise ValueError('FORBIDDEN_POLICY_CAPABILITY')


def policy(plan, actions, budget):
    exact_keys(plan,['id','steps'])
    require(type(plan['id']) is str and 1<=len(plan['id'])<=40 and
            all(c in 'abcdefghijklmnopqrstuvwxyz0123456789_-' for c in plan['id']), 'PLAN_ID')
    require(type(plan['steps']) is list and len(plan['steps'])==budget, 'PLAN_BUDGET')
    for i,e in enumerate(plan['steps']):expression(e,i,actions)


def posterior(probabilities, history):
    w=[F(1,len(probabilities))]*len(probabilities)
    for a,y in history:
        w=[v*(r[a] if y else 1-r[a]) for v,r in zip(w,probabilities)]
        s=sum(w);w=[v/s for v in w]
    return w


def decide(expr, probabilities, history):
    if 'action' in expr:return expr['action']
    if 'if_observation' in expr:
        return decide(expr['then'] if history[expr['if_observation']][1] else expr['else'],probabilities,history)
    w=posterior(probabilities,history)
    def h(p):
        p=float(p)
        return -sum(q*math.log2(q) for q in (p,1-p) if q)
    gains=[h(sum(v*r[a] for v,r in zip(w,probabilities)))-sum(float(v)*h(r[a]) for v,r in zip(w,probabilities)) for a in range(len(probabilities[0]))]
    best=max(gains)
    return len(history)%len(gains) if best<=1e-12 else next(a for a,g in enumerate(gains) if best-g<=1e-12)


def respond(request):
    exact_keys(request,['schema','model','plan','history','budget'])
    require(request['schema']=='rax.public-prefix/1','SCHEMA')
    p=model(request['model']);b=integer(request['budget'],1,32);policy(request['plan'],len(p[0]),b)
    hist=request['history'];require(type(hist) is list and len(hist)<b,'HISTORY_LENGTH')
    for row in hist:
        require(type(row) is list and len(row)==2,'HISTORY_SHAPE')
        integer(row[0],0,len(p[0])-1);integer(row[1],0,1)
    return {'action':decide(request['plan']['steps'][len(hist)],p,hist)}


if __name__=='__main__':
    try:
        data=sys.stdin.buffer.read(65537)
        require(len(data)<=65536,'INPUT_SIZE')
        print(json.dumps(respond(parse(data.decode('utf-8'))),sort_keys=True))
    except (ValueError,TypeError,KeyError,IndexError,RecursionError,UnicodeError) as exc:
        print(json.dumps({'status':'REJECTED','reason':str(exc)}));sys.exit(2)
