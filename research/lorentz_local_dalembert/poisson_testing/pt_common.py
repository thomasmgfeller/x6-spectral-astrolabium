"""Pinned experiment and exact geometric/sampling error bounds.
SPDX-License-Identifier: Apache-2.0
"""
import sys,ctypes,subprocess,tempfile,hashlib,json,math
from pathlib import Path
import numpy as np
HERE=Path(__file__).resolve().parent
sys.path.insert(0,str(HERE.parent/'witness_overlap_volumes'))
from wv_run import F,read,save,OLD,input_record,boosted,flo,cei,sqrt_bounds,pi_bounds,interval,outward,confidence_bound
UNIT=2**30

def frozen():
    for name,h in read(HERE/'freeze.json')['files'].items():assert hashlib.sha256((HERE/name).read_bytes()).hexdigest()==h,name

def kernel():
    directory=Path(tempfile.mkdtemp(prefix='eigenzeit-poisson-test-'))
    so=directory/'cells.so'
    subprocess.run(['g++','-std=c++17','-O3','-shared','-fPIC',str(HERE/'count_cells.cpp'),'-o',str(so)],check=True)
    lib=ctypes.CDLL(str(so));f=lib.count_cells
    f.argtypes=[ctypes.c_void_p,ctypes.c_int64,ctypes.c_void_p,ctypes.c_void_p,ctypes.c_int,ctypes.c_void_p,ctypes.c_void_p,ctypes.c_void_p]
    f.restype=ctypes.c_int
    return f

def setup(g):
    w=read(OLD/'witness.json');packet,obs,mask=input_record(w['index'])
    lookup={n:i for i,n in enumerate(w['nodes'])};R=w['full_order']
    pairs=[(lookup[a],lookup[b]) for a,b in packet['pairs']]
    ends=[(a,b) if R[a][b] else (b,a) for a,b in pairs]
    assert len(ends)==90 and len(mask)==74 and all(R[a][b] for a,b in ends)
    z=[[F(v) for v in row] for row in w['coordinates'][g]];zz=boosted(z)
    assert F(w['scale'])**2*interval(z,3,0)<F(3,2)**2
    assert all((a==3 or R[3][a]) and (b==0 or R[b][0]) for a,b in ends)
    factor=F(w['rho'])*F(w['scale'])**3;p0,p1=pi_bounds()
    means=[]
    for a,b in ends:
        q=interval(z,a,b);sl,su=sqrt_bounds(q);means.append((factor*p0*q*sl/12,factor*p1*q*su/12))
    a,b=zz[3],zz[0];T=b[0]-a[0];dx=b[1]-a[1];dy=b[2]-a[2]
    rx=sqrt_bounds(T*T-dy*dy)[1]/2;ry=sqrt_bounds(T*T-dx*dx)[1]/2
    low=[flo(a[0]*UNIT),flo(((a[1]+b[1])/2-rx)*UNIT),flo(((a[2]+b[2])/2-ry)*UNIT)]
    high=[cei(b[0]*UNIT),cei(((a[1]+b[1])/2+rx)*UNIT),cei(((a[2]+b[2])/2+ry)*UNIT)]
    lo=np.array([[flo(v*UNIT) for v in row] for row in zz],dtype=np.int64)
    hi=np.array([[cei(v*UNIT) for v in row] for row in zz],dtype=np.int64)
    assert np.max(abs(lo))<10**12 and np.max(abs(hi))<10**12
    exact_mean=factor*F(math.prod(h-l for l,h in zip(low,high)),UNIT**3)
    poisson_mean=float(exact_mean)
    # Every ambiguous cell is within |t-tip_t +/- radius|<=5h of a cone.
    # Each of at most 42 cones contributes <=10h times spatial box area.
    boundary=factor*F(420*(high[1]-low[1])*(high[2]-low[2]),UNIT**3)
    parameter_error=abs(F.from_float(poisson_mean)-exact_mean)
    fbits=np.zeros((21,2),dtype=np.uint64);pbits=fbits.copy()
    for k,(a,b) in enumerate(ends):fbits[a,k//64]|=np.uint64(1)<<np.uint64(k%64);pbits[b,k//64]|=np.uint64(1)<<np.uint64(k%64)
    return dict(means=means,low=low,high=high,lo=lo,hi=hi,fbits=fbits,pbits=pbits,
                poisson_mean=poisson_mean,coupling_upper=boundary+parameter_error,
                boundary_upper=boundary,parameter_error=parameter_error)

def simulate(g,phase,n,f):
    c=read(HERE/'contract.json');s=setup(g);rng=np.random.Generator(np.random.PCG64(c[phase+'_seeds'][g]));rows=[];sizes=[]
    for i in range(n):
        size=int(rng.poisson(s['poisson_mean']));cells=rng.integers(s['low'],s['high'],size=(size,3),dtype=np.int64)
        out=np.zeros(128,dtype=np.int64)
        code=f(cells.ctypes.data,size,s['lo'].ctypes.data,s['hi'].ctypes.data,21,s['fbits'].ctypes.data,s['pbits'].ctypes.data,out.ctypes.data)
        assert code==0 and not any(out[90:])
        rows.append(out[:90].tolist());sizes.append(size)
        if (i+1)%64==0:print(json.dumps(dict(phase=phase,geometry=g,trials=i+1)),flush=True)
    return dict(geometry=g,phase=phase,counts=rows,auxiliary_box_point_counts=sizes,
                coupling_upper=outward(s['coupling_upper'])[1],boundary_upper=outward(s['boundary_upper'])[1],
                poisson_parameter_error_upper=outward(s['parameter_error'])[1],
                seed=c[phase+'_seeds'][g])
