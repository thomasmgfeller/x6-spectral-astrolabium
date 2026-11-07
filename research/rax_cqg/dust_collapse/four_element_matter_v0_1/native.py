"""Prepare certified tensor rules, invoke checked integer kernel, retain error bounds."""
from fractions import Fraction as F
from math import prod,factorial
from pathlib import Path
import subprocess
import sys
sys.path.insert(0,str(Path(__file__).resolve().parent/'inputs'))
import geometry as g
import gauss
import intervals_fp as fp

ROOT=Path(__file__).resolve().parent;S=1<<60;EXE=None
require=fp.require


def compile_kernel(directory):
    global EXE
    EXE=str(Path(directory)/'cst_integral')
    subprocess.run(['g++','-std=c++17','-O2','-Wall','-Wextra',str(ROOT/'kernel.cpp'),'-o',EXE],check=True,capture_output=True,text=True)


def rational_pair(x):
    x=F(x);return x.numerator*S//x.denominator,-((-x.numerator*S)//x.denominator)
def pair(x):return x.lo//(1<<100),-((-x.hi)//(1<<100))
def line(x):return ' '.join(map(str,x))
def interval(a,b):return fp.I.rational(F(a,S)) if a==b else fp.I(a<<100,b<<100)
def run(text,timeout=600):
    result=subprocess.run([EXE],input=text,text=True,capture_output=True,check=True,timeout=timeout)
    return [list(map(int,row.split())) for row in result.stdout.splitlines()]


def integrate(orders,h,mu,tolerance=F(1,10**8)):
    n=len(orders[0]);bounds=[g.derivative_bounds(o,h) for o in orders]
    if mu==0:return [(fp.ONE,fp.ZERO) for _ in orders],[F(0) for _ in orders],{
        'orders':[],'evaluations':0,'density_characteristic_calls':0,'derivative_bounds':bounds,
        'quadrature_errors':[F(0) for _ in orders],'normalization_interval':[F(1),F(1)]}
    qs,errors=gauss.select_orders(bounds,mu,tolerance,n);rules=[gauss.rule(q) for q in qs]
    unique=[];indices=[]
    for order in orders:
        row=[]
        for poly in g.action_polynomials(order,h)[0]:
            key=tuple(sorted(poly.items()))
            if key not in unique:unique.append(key)
            row.append(unique.index(key))
        indices.append(row)
    keys=sorted({key for p in unique for key,_ in p});prefixes={():0};circuit=[];leaves=[]
    for row in indices:
        prefix=()
        for index in row:
            nxt=prefix+(index,)
            if nxt not in prefixes:circuit.append((prefixes[prefix],index));prefixes[nxt]=len(circuit)
            prefix=nxt
        leaves.append(prefixes[prefix])
    text=['integrate',line(pair(fp.PI)),line([n,len(orders),len(unique),len(keys),len(circuit)]),line(qs)]
    for nodes,weights,_ in rules:
        text.extend(line(pair(x)+pair(w)) for x,w in zip(nodes,weights))
    text.extend(line(key) for key in keys)
    for poly in unique:
        text.append(str(len(poly)))
        text.extend(line((keys.index(key),)+rational_pair(mu*c)) for key,c in poly)
    text.extend(line(x) for x in circuit);text.append(line(leaves))
    count=prod(qs);require(count<=1200000,'Frozen node budget')
    out=run('\n'.join(text)+'\n');require(len(out)==len(orders)+1 and out[0][2]==count,'Native output census')
    norm=interval(*out[0][:2]);require(norm.contains(1),'Certified Jacobian normalization')
    values=[(interval(*row[:2]),interval(*row[2:])) for row in out[1:]]
    for z,e in zip(values,errors):
        arith=z[0].radius()+z[1].radius();require(arith<=F(1,250000000),'Arithmetic budget')
        require(arith+e<=tolerance,'Total amplitude error budget')
    return values,errors,{'orders':qs,'evaluations':count,'density_characteristic_calls':count*len(unique),
        'unique_density_polynomials':len(unique),'shared_complex_products':len(circuit),
        'derivative_bounds':bounds,'quadrature_errors':errors,'normalization_interval':norm.endpoints()}


def audit():
    numbers=list(map(F,['-7/3','-1','-1/7','0','1/3','1','5/2']))
    tests=[(a,b) for a in numbers for b in numbers if b]
    text=['ops',line(pair(fp.PI)),str(len(tests))]+[line(rational_pair(a)+rational_pair(b)) for a,b in tests]
    out=run('\n'.join(text)+'\n');checks=0
    for (a,b),row in zip(tests,out):
        for k,target in enumerate([a+b,a-b,a*b,a/b]):require(interval(*row[2*k:2*k+2]).contains(target),'Native rational arithmetic');checks+=1
    points=list(map(F,['-50','-20','-7/3','-1','-1/3','-1/1000000','0','1/1000000','1/3','1','7/3','20','50']))
    text=['points',line(pair(fp.PI)),str(len(points))]+[line(rational_pair(x)) for x in points]
    out=run('\n'.join(text)+'\n');inclusions=0
    for x,row in zip(points,out):
        ref=fp.cis(fp.I.rational(x))+fp.density_characteristic(fp.I.rational(x))
        for k,z in enumerate(ref):
            native=interval(*row[2*k:2*k+2]);require(native.lo<=z.lo<=z.hi<=native.hi,'160-bit pointwise inclusion');inclusions+=1
    bad=subprocess.run([EXE],input='overflow\n',text=True,capture_output=True)
    require(bad.returncode==2 and 'integer multiply overflow' in bad.stderr,'Intentional integer overflow rejected')
    return {'rational_arithmetic_checks':checks,'pointwise_160_bit_inclusions':inclusions,
            'intentional_overflow':'REJECTED','native_fraction_bits':60,'floating_point_integral':False}
