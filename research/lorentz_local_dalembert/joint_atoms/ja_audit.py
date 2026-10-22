"""Atom-law controls, exact dependence counterexample and cell checks.
SPDX-License-Identifier: Apache-2.0
"""
from ja_run import *
from itertools import product

def audit():
    # Independent closed form for the two-bin Hellinger exponent.
    a={'a':F(100),'b':F(100)};b={'a':F(99),'b':F(101)}
    result=law_bound(a,b,F(200))
    roots=[sqrt_bounds(F(n)) for n in [9900,10100]]
    jlo=400-2*sum(r[1] for r in roots);jhi=400-2*sum(r[0] for r in roots)
    tv=sqrt_bounds(jhi)[1]
    assert F(result['tv_upper'])>=sqrt_bounds(jlo)[0] and F(result['tv_upper'])<F(71,1000)
    assert abs(F(result['tv_upper'])-tv)<F(1,10**19)
    # Alternating exp(-1) bounds: odd truncation lower, even truncation upper.
    even=sum(F((-1)**k,math.factorial(k)) for k in range(81))
    odd=even-F(1,math.factorial(81));coupling=(1-even,1-odd)
    assert coupling[0]>F(63,100)
    missing=law_bound({}, {},F(1));assert missing['tv_upper']=='1.00000000000000000000'
    for args in [({'a':F(-1)},{},F(1)),({'a':F(2)},{},F(1))]:
        try:law_bound(*args)
        except AssertionError:continue
        raise AssertionError('invalid atom lower masses accepted')
    assert law_bound({'x':F(100),'y':F(100)},{'x':F(99),'y':F(101)},F(200))==result
    # Same first and second moments do not identify the full joint count law.
    intensities=[[F(1)+sign*F((-1)**i.bit_count(),4) for i in range(8)] for sign in [1,-1]]
    def intersection(vals,mask):return sum(v for i,v in enumerate(vals) if i&mask==mask)
    assert sum(intensities[0])==sum(intensities[1])==8
    for mask in [1,2,4,3,5,6]:assert intersection(intensities[0],mask)==intersection(intensities[1],mask)
    triple=[intersection(v,7) for v in intensities];assert triple[0]!=triple[1]
    # Independent exact point membership inside cells declared wholly classified.
    tips=np.array([[0,0,0],[16,0,0]],dtype=np.int64);tests=0;known_count=0
    for k in range(256):
        lower=np.array([[k%20-2,(k*7)%21-10,(k*11)%19-9]],dtype=np.int64)
        upper=lower+np.array([[1+k%3,1+(k//3)%3,1+(k//9)%3]])
        known,label=classify(lower,upper,tips,tips,[(0,1)])
        if not known[0]:continue
        known_count+=1
        for fractions in list(product([F(0),F(1)],repeat=3))+[(F(1,2),)*3]:
            p=[F(int(x))+f*int(y-x) for x,y,f in zip(lower[0],upper[0],fractions)]
            t,x,y=p;inside=(t>0 and t*t>x*x+y*y and 16-t>0 and (16-t)**2>x*x+y*y)
            assert bool(label[0,0]&1)==inside
            tests+=1
    # A cell crossing a cone must not receive a definite full pattern.
    known,_=classify(np.array([[0,0,0]]),np.array([[2,2,2]]),tips,tips,[(0,1)])
    assert not known[0]
    records=read(HERE/'partitions.json.gz')
    for old,new in zip(records,records[1:]):
        for a,b in zip(old['geometries'],new['geometries']):
            assert all(b['atom_integer_volumes'].get(k,0)>=v for k,v in a['atom_integer_volumes'].items())
    summary=read(HERE/'summary.json')
    assert summary['status']=='HOLD_VOLUME_RESOLUTION' and summary['best_atom_tv_upper']=='1.00000000000000000000'
    return dict(status='PASS',exact_toy_atom_tv_upper=result['tv_upper'],same_toy_coupling_tv=outward(*coupling),
      omitted_mass_control='retained; no false zero-TV certificate',invalid_lower_mass_controls=2,
      parity_example=dict(total='8',single_and_pair_means_equal=True,triple_means=[str(v) for v in triple]),
      known_cells_checked=known_count,exact_point_membership_checks=tests,crossing_cell_rejected=True,nested_lower_volumes_monotone=True,
      scope='Toy improvement is not a result for the repository geometry pair; cell sampling audits implementation, interval cone bounds supply the proof.')

if __name__=='__main__':
    result=audit()
    if '--verify' in sys.argv:assert result==read(HERE/'audit.json')
    else:save(HERE/'audit.json',result)
    print(json.dumps(result))
