"""Short controls; never runs the n=5 production quadratures."""
from fractions import Fraction as F
from itertools import product
from math import prod, factorial
from pathlib import Path
import copy, hashlib, json, tempfile
import prepare as p
import worker as w
g=p.g;m=p.m;v=p.v;fp=w.fp
require=p.require

def check_arithmetic(exe):
    numbers=list(map(F,['-7/3','-1','-1/7','0','1/3','1','5/2']))
    tests=[(a,b) for a in numbers for b in numbers if b]
    text=['ops',w.line(w.ipair(fp.PI)),str(len(tests))]+[w.line(w.fpair(a)+w.fpair(b)) for a,b in tests]
    rows,_=w.invoke(exe,'\n'.join(text)+'\n');checks=0
    require(len(rows)==len(tests),'Arithmetic control census')
    for (a,b),row in zip(tests,rows):
        for k,target in enumerate([a+b,a-b,a*b,a/b]):
            require(F(row[2*k],w.S)<=target<=F(row[2*k+1],w.S),'Rational arithmetic enclosure');checks+=1
    points=list(map(F,['-50','-20','-7/3','-1','-1/3','-1/1000000','0','1/1000000','1/3','1','7/3','20','50']))
    rows,_=w.invoke(exe,'\n'.join(['points',w.line(w.ipair(fp.PI)),str(len(points))]+[w.line(w.fpair(x)) for x in points])+'\n')
    for x,row in zip(points,rows):
        refs=fp.cis(fp.I.rational(x))+fp.density_characteristic(fp.I.rational(x))
        for k,ref in enumerate(refs):
            require((row[2*k]<<100)<=ref.lo<=ref.hi<=(row[2*k+1]<<100),'160-bit function reference')
    import subprocess
    bad=subprocess.run([str(exe)],input='overflow\n',text=True,capture_output=True,timeout=10)
    require(bad.returncode==2 and 'integer multiply overflow' in bad.stderr,'Overflow rejected')
    return {'rational_checks':checks,'function_enclosures':len(points)*4,'overflow':'REJECTED'}

def direct_points(order,h,mu,qs,begin,end):
    rules=[w.gauss.rule(q) for q in qs];n=len(order);polys=g.action_polynomials(order,h)[0]
    z=(fp.ZERO,fp.ZERO)
    for flat in range(begin,end):
        offset=flat;idx=[0]*n
        for j in reversed(range(n)):idx[j]=offset%qs[j];offset//=qs[j]
        us=[rules[j][0][idx[j]] for j in range(n)]
        weight=fp.I.rational(factorial(n))
        for j in range(n):weight=weight*rules[j][1][idx[j]]*(us[j]**j)
        value=(fp.ONE,fp.ZERO)
        for poly in polys:
            arg=fp.ZERO
            for key,c in poly.items():
                term=fp.I.rational(mu*c)
                for u,k in zip(us,key):term=term*(u**k)
                arg=arg+term
            value=fp.cmul(value,fp.density_characteristic(arg))
        z=fp.cadd(z,fp.cscale(value,weight))
    return z

def run():
    plan=w.read_json(p.ROOT/'plan.json')
    require(plan==p.build(),'Plan reconstructed exactly without integration')
    gaussian_orders=sorted({q for c in plan['configs'] for q in c['q']})
    for q in gaussian_orders:w.gauss.rule(q)
    optimized=0
    for n in (1,2,3):
        for order in m.natural_orders(n):
            require(p.fast_bounds(order,F(1,2))==g.derivative_bounds(order,F(1,2)),
                    'Optimized density-corner bounds equal full tensor Bernstein bounds')
            optimized+=1
    # Include genuinely five-dimensional examples, with distinct interval layers.
    for order in [m.natural_orders(5)[0],m.natural_orders(5)[178],m.natural_orders(5)[-1]]:
        require(p.fast_bounds(order,F(1,2))==g.derivative_bounds(order,F(1,2)),'n=5 Bernstein equality')
        optimized+=1
    actions=moments=0
    for order in m.natural_orders(5):
        for h in [F(1,4),F(1,2)]:
            xs=tuple(F(j,6) for j in range(1,6));ws=tuple(F(j,5) for j in range(1,6))
            T=tuple(-2+4*h*x for x in xs)
            polys,_=g.action_polynomials(order,h,cube=False)
            polynomial=-sum((ww*g.evaluate(a,xs) for ww,a in zip(ws,polys)),F(0))
            state=(order,T,ws)
            require(polynomial==v.action(state)[1]==v.action_by_increments(state)[1],'Full n=5 matter action')
            actions+=1
            require(g.low_moments(order,h,K=1)==g.low_moments(order,h,K=1,cube=False),'Simplex/cube moments')
            moments+=2
    with tempfile.TemporaryDirectory(prefix='n5-controls-') as tmp:
        exe=w.compile_kernel(tmp);arithmetic=check_arithmetic(exe)
        orders=m.natural_orders(3);qs=[4,4,4]
        full,_=w.raw_result(exe,orders,F(1,4),F(1,4),qs,0,64)
        pieces=[w.raw_result(exe,orders,F(1,4),F(1,4),qs,a,b)[0] for a,b in [(0,7),(7,29),(29,64)]]
        require([sum(x['normalization'][j] for x in pieces) for j in range(2)]==full['normalization'],'Exact shard normalization additivity')
        require([[sum(x['values'][k][j] for x in pieces) for j in range(4)] for k in range(7)]==full['values'],'Exact shard amplitude additivity')
        # n=5 phase-free polynomial fixture: q=4 integrates J exactly.
        five=m.natural_orders(5)
        zero,_=w.raw_result(exe,five,F(1,2),F(0),[4]*5,0,1024)
        require(zero['normalization'][0]<=w.S<=zero['normalization'][1],'n=5 normalized Jacobian')
        for lo,hi,li,ui in zero['values']:
            require(lo<=w.S<=hi and li<=0<=ui,'All 357 n=5 phase-free amplitudes')
        # Nonzero n=5 integrand at three selected tensor points, against a
        # separate 160-bit Python evaluation. Not a full field integral.
        chosen=[five[0],five[178],five[-1]];qs=[8]*5;inc=0
        for start in [0,1234,32767]:
            values,_=w.raw_result(exe,chosen,F(1,2),F(1),qs,start,start+1)
            for order,row in zip(chosen,values['values']):
                refs=direct_points(order,F(1,2),F(1),qs,start,start+1)
                for k,ref in enumerate(refs):
                    require((row[2*k]<<100)<=ref.lo<=ref.hi<=(row[2*k+1]<<100),'n=5 nonzero point enclosure');inc+=1
        rejected=0
        for text in [w.request(chosen,F(1,2),F(1),qs,0,1).replace('\n0 1\n','\n-1 1\n',1),
                     w.request(chosen,F(1,2),F(1),qs,0,1).replace('\n0 1\n','\n0 65537\n',1)]:
            import subprocess
            bad=subprocess.run([str(exe)],input=text,text=True,capture_output=True,timeout=10)
            require(bad.returncode==2,'Invalid range rejected');rejected+=1
    # Protocol checks reject wrong source, duplicate and incomplete collections
    # before they can be mistaken for a full result.
    c=plan['configs'][0];start,end=w.job_range(plan,c,0)
    record={'schema':'cst-dust-n5-shard-v1','plan_sha256':p.digest(plan),'source_manifest_sha256':'control',
        'config':c['id'],'fraction_bits':60,'shard':0,'begin':start,'end':end,
        'data':{'normalization':[0,0],'values':[[0,0,0,0] for _ in range(357)]}}
    cases=[([record],'Incomplete'),([record,record],'Duplicate')]
    wrong=copy.deepcopy(record);wrong['plan_sha256']='wrong';cases.append(([wrong],'Plan identity'))
    negative=copy.deepcopy(record);negative['data']['values'][0]=[1,0,0,0];cases.append(([negative],'Endpoint order'))
    for records,message in cases:
        try:w.aggregate(records,plan,c,'control')
        except RuntimeError as e:require(message in str(e),'Expected rejection reason')
        else:raise RuntimeError('Invalid collection accepted')
        rejected+=1
    complete=[]
    for sid in range(c['shards']):
        row=copy.deepcopy(record);row['shard']=sid
        row['begin'],row['end']=w.job_range(plan,c,sid)
        if sid==0:
            row['data']={'normalization':[w.S,w.S],
                         'values':[[w.S,w.S,0,0] for _ in range(357)]}
        complete.append(row)
    combined=w.aggregate(complete,plan,c,'control')
    require(combined==w.aggregate(list(reversed(complete)),plan,c,'control'),'Order independent synthetic reduction')
    require(combined['status'].startswith('PROVISIONAL') and len(combined['channels'])==3,'Complete collection remains provisional')
    require(F(combined['channels'][0]['visibility_interval'][1])==1,'Synthetic phase-free visibility')
    return {'status':'PASS_CONTROLS_ONLY','production_n5_field_integrals_executed':False,
        'plan_sha256':p.digest(plan),'natural_orders':357,'bernstein_equivalence_cases':optimized,
        'action_checks':actions,'simplex_cube_moment_checks':moments,'arithmetic':arithmetic,
        'n3_shard_additivity':'EXACT','n5_analytic_zero_checks':357,'n5_nonzero_point_enclosures':inc,
        'gaussian_orders_checked':gaussian_orders,'synthetic_complete_reduction':'PASS_PROVISIONAL',
        'negative_controls_rejected':rejected,'all_eight_physical_gates':'HOLD'}

if __name__=='__main__':print(json.dumps(run(),indent=2,sort_keys=True))
