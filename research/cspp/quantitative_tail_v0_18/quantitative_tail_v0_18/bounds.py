"""Explicit KG source constants and correlated causal-path L1 tail bounds."""
import argparse,gzip,hashlib,json,math
from fractions import Fraction as F
from pathlib import Path
from flint import arb,ctx

HERE=Path(__file__).resolve().parent
def enc(x):return arb(x).str(45,more=True)
def weight(n):
    e=F(1,16)
    return sum(F(c*math.comb(n,k))*e**k*(1-e)**(n-k) for k,c in enumerate([1,-9,16,-8]) if k<=n)
def weight_envelope(n):
    u=F(1,15)
    return F(15,16)**n*(1+9*n*u+8*n*n*u*u+F(4,3)*n**3*u**3)
def sj(j):
    return sum(math.factorial(j)//(math.factorial(a)*math.factorial(b)*math.factorial(j-a-b))*math.factorial(2*a)*math.factorial(2*b)*math.factorial(2*(j-a-b)) for a in range(j+1) for b in range(j-a+1))
def source_constant(J):
    total=arb(0)
    for j in range(J+1):
        n=2*j
        m=(-arb(1)/2).exp() if n==0 else (2*n/arb(1).exp())**n
        total+=math.comb(J,j)*40**n*sj(j)*m
    return arb.pi()/6*(arb(11)/8).exp()*total
def read_archives():
    with gzip.open(HERE/'evidence/v16_COEFFICIENTS_192.json.gz','rt') as f:return json.load(f)['rows']
def calculate(bits):
    ctx.prec=bits
    proto=json.loads((HERE/'PROTOCOL.json').read_text())
    kappa=-weight(8);a=1/(2*arb.pi()).sqrt();beta=a/(16*(1+a));gamma=beta*arb(str(kappa))
    M0=source_constant(2)/(8*arb.pi())
    Dcond=16*(arb(625)/8).exp()
    near=21/(1+a);far=81*arb(2).sqrt()/(1+a)
    Du={J:source_constant(J) for J in sorted({2}|{N+2 for N in proto['N_family']})}
    CN={N:(arb(21)/8).exp()*math.factorial(N)*(arb(32)/3)**N*Du[N+2]/(8*arb.pi()) for N in proto['N_family']}
    G0=(gamma*arb(14625)/256).exp()
    rows=[]
    for r in read_archives():
        n=r['inner_active_nodes']+r['exterior_active_nodes']
        assert n==r['retained_nodes']-r['history_nodes']
        rows.append({'key':r['key'],'known_active_nodes':n,'G':(1+gamma)**n*(gamma*arb(29)/512).exp()})
    def one_step(N,L):
        return near*CN[N]*L**(2-N)/(N-2)+far*M0*(-L/256).exp()*(256*L+65536)
    table=[]
    for power in proto['L_grid_powers_of_two']:
        L=arb(2)**power
        bounds={N:one_step(N,L) for N in proto['N_family']}
        N=min(bounds,key=lambda k:float(bounds[k].log()))
        b=bounds[N]
        missing=(L+arb(1)/2)**4-arb(6561)/128
        entry={'L_power':power,'L':str(2**power),'selected_N':N,'one_step':enc(b),'unconditional_transported':enc(G0*b),'archive_tail':[{'key':r['key'],'bound':enc(r['G']*Dcond*b)} for r in rows],
               'archive_full_beyond5':[{'key':r['key'],'bound':enc(r['G']*(gamma*M0*missing+Dcond*b))} for r in rows]}
        table.append(entry)
    scale=arb(1)/1000
    summaries=[]
    for i,r in enumerate(rows):
        first=next(x for x in table if arb(x['archive_tail'][i]['bound'])<scale)
        best=min(table,key=lambda x:float(arb(x['archive_full_beyond5'][i]['bound']).log()))
        L=2**first['L_power'];H=2*L+F(3,2)
        summaries.append({'key':r['key'],'known_active_nodes':r['known_active_nodes'],'transport_factor':enc(r['G']),
                         'first_grid_L1_below_0_001':{'L':str(L),'H_sufficient':str(H),'N':first['selected_N'],'bound':first['archive_tail'][i]['bound'],'expected_support_history_nodes':str((F(L)+F(1,2))**4-F(1,16)),'expected_exterior_history_nodes':str((F(L)+F(1,2))**4-F(6561,128))},
                         'best_grid_full_beyond5':{'L':best['L'],'N':best['selected_N'],'bound':best['archive_full_beyond5'][i]['bound']}})
    result={'schema':'cspp.quantitative-tail/0.18','precision_bits':bits,'exact_kappa':str(kappa),'kappa':enc(arb(str(kappa))),'gamma':enc(gamma),'M0':enc(M0),'D_conditional':enc(Dcond),'unconditional_transport_factor':enc(G0),
            'source_D':{str(J):enc(D) for J,D in Du.items()},'strip_C_N':{str(N):enc(C) for N,C in CN.items()},'archives':summaries,'grid':table,
            'scope':'conditional expectation of absolute fully transported tails; not a pathwise error certificate or new confidence gate','status':{'METHOD':'HOLD','G1':'HOLD','fresh_confirmation':'NOT_RUN','per_realization_accuracy':'NOT_CERTIFIED'},'new_random_calls':0}
    path=HERE/f'results/BOUNDS_{bits}.json';path.write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({k:result[k] for k in ['precision_bits','exact_kappa','kappa','gamma','M0','D_conditional','unconditional_transport_factor','archives','status']},indent=2))

if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('--bits',type=int,default=192);calculate(ap.parse_args().bits)
