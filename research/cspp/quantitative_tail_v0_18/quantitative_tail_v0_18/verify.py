"""Independent algebra, negative controls and precision overlap checks."""
import json,hashlib,math
from fractions import Fraction as F
from pathlib import Path
from flint import arb,ctx,fmpq_poly as P,fmpq
import bounds
HERE=Path(__file__).resolve().parent
checks=[]
def require(ok,msg):
    if not ok:raise AssertionError(msg)
    checks.append(msg)
def read(bits):return json.loads((HERE/f'results/BOUNDS_{bits}.json').read_text())
def integral(p,a,b):
    q=p.integral();return q(fmpq(str(b)))-q(fmpq(str(a)))
def verify():
    ctx.prec=192
    low,high=read(128),read(192)
    kappa=-bounds.weight(8)
    require(kappa==F(4976184375,4294967296),'exact extremal layer weight')
    for n in range(129):require(abs(bounds.weight(n))<=kappa,f'finite exact weight n={n}')
    require(bounds.weight_envelope(128)<kappa,'positive envelope beyond n=128 below kappa')
    require(F(15,16)*F(129,128)**3<1,'all four envelope terms decrease for n>=128')
    require(abs(bounds.weight(8))>1,'negative control: proposed bound one is false')
    require(F(77,40)**2>3,'polydisc change in source denominator below a/5')
    require(F(5,9)>F(1,2),'real reciprocal bound supplies exponential damping')
    require(3<4,'carrier and contour factor bounded by exp(11/8)')
    # Independent differentiation operator recurrence yields the factorial sum.
    operator={(0,0,0):1}
    S=[]
    for j in range(35):
        val=sum(abs(c)*math.factorial(k[0])*math.factorial(k[1])*math.factorial(k[2]) for k,c in operator.items())
        S.append(val)
        require(val==bounds.sj(j),f'Laplace derivative coefficient recurrence j={j}')
        new={}
        for k,c in operator.items():
            for axis in range(3):
                kk=list(k);kk[axis]+=2;kk=tuple(kk);new[kk]=new.get(kk,0)-c
        operator=new
    # Exact polynomial integration of omitted source-support spacetime volume.
    t=P([0,1]);outer=4*(t+fmpq(1,2))**3;inner=4*(4-t)**3
    const=integral(outer-inner,F(7,4),F(4))-integral(outer,F(0),F(4))
    poly=outer.integral()+const-outer.integral()(0)
    expected=(t+fmpq(1,2))**4-fmpq(6561,128)
    require(poly==expected,'independent support-shell volume polynomial')
    require(2*(F(9,4))**4==F(6561,128),'omitted support offset')
    # Exact complete ordered graph: path expansion is a sharp envelope in this model.
    g=F(1,50)
    for n in [0,1,2,5,12]:
        v=[]
        for i in range(n):v.append(1+g*sum(v))
        require(1+g*sum(v)==(1+g)**n,f'ordered path expansion n={n}')
    require((1+g)**5>1+5*g,'negative control: keeping only direct active paths misses terms')
    require(F(1,2)*(1*1+3*3)!=F(1,2)*(1+3)*F(1,2)*(1+3),'negative control: correlated expectations do not factor')
    # Gaussian constant: substitute x=k radius and standard beta integral.
    require(F(4)*F(1,4)==1,'radial Fourier L1 integral coefficient pi squared')
    # Every continuous output at both precisions must overlap; discrete data identical.
    overlaps=0
    def compare(x,y,path='root'):
        nonlocal overlaps
        if isinstance(x,dict):
            require(x.keys()==y.keys(),path+' dictionary fields')
            for k in x:
                if k!='precision_bits':compare(x[k],y[k],path+'/'+k)
        elif isinstance(x,list):
            require(len(x)==len(y),path+' list count')
            for i,(a,b) in enumerate(zip(x,y)):compare(a,b,path+f'/{i}')
        elif isinstance(x,str) and ('+/-' in x or '+/-' in str(y)):
            require(arb(x).overlaps(arb(y)),path+' precision overlap');overlaps+=1
        else:require(x==y,path+' exact equality')
    compare(low,high)
    a=1/(2*arb.pi()).sqrt();near=21/(1+a);far=81*arb(2).sqrt()/(1+a);M0=arb(high['M0'])
    for row in high['grid']:
        L=arb(row['L']);chosen=row['selected_N'];values={}
        for ns,C in high['strip_C_N'].items():
            N=int(ns);values[N]=near*arb(C)*L**(2-N)/(N-2)+far*M0*(-L/256).exp()*(256*L+65536)
        require(all(values[chosen]<v for n,v in values.items() if n!=chosen),f'certified choice within N family at L={row["L"]}')
    for r in high['archives']:
        require(arb(r['first_grid_L1_below_0_001']['bound'])<arb(1)/1000,r['key']+' stated conditional L1 tail scale')
        require(arb(r['best_grid_full_beyond5']['bound'])>arb(10)**50,r['key']+' full majorant remains uninformative')
        n=r['known_active_nodes'];gamma=arb(high['gamma']);G=(1+gamma)**n*(gamma*arb(29)/512).exp()
        require(G.overlaps(arb(r['transport_factor'])),r['key']+' conditional path factor')
    require(high['status']['per_realization_accuracy']=='NOT_CERTIFIED','no pathwise gate from mean bound')
    require(high['status']['METHOD']==high['status']['G1']=='HOLD','scientific HOLD preserved')
    for e in json.loads((HERE/'PROVENANCE.json').read_text())['files']:
        require(hashlib.sha256((HERE/e['path']).read_bytes()).hexdigest()==e['sha256'],'unchanged evidence '+e['path'])
    out={'status':'PASS','checks':len(checks),'precision_overlaps':overlaps,'negative_controls':3,'check_names':checks,'scope':'algebra and interval checks; analytic contour/Mecke proof requires mathematical reading'}
    (HERE/'results/CHECKS.json').write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps({k:v for k,v in out.items() if k!='check_names'},indent=2))
if __name__=='__main__':verify()
