"""Reproduce v0.19 source, geometric and fully transported L1 bounds."""
import argparse
import hashlib
import json
import math
from pathlib import Path
from flint import arb, ctx
from source_norms import source_data

HERE = Path(__file__).resolve().parent


def enc(x):
    return arb(x).str(55, more=True)


def choose(values):
    key = min(values, key=lambda k: float(values[k].log()))
    for k, value in values.items():
        if k != key and not values[key] < value:
            raise ArithmeticError(f'Unresolved minimum: {key}, {k}')
    return key


def kernel_tail_moment(power, S):
    # Integral_S^infinity s^power exp(-s^2/128) Pbar(s^2/128) ds.
    c = arb(1)/128
    out = arb(0)
    for j, coeff in enumerate([arb(1),arb(9),arb(8),arb(4)/3]):
        a = arb(power+2*j+1)/2
        out += coeff*(c*S*S).gamma_upper(a)/(2*c**(arb(power+1)/2))
    return out


def field_integral(M0, C, N, L):
    # Integral_L^infinity T min(M0,C*T^-N) dT, exact piecewise expression.
    R = (C/M0)**(arb(1)/N)
    if R > L:
        return M0*(R*R-L*L)/2+C*R**(2-N)/(N-2)
    if R < L:
        return C*L**(2-N)/(N-2)
    raise ArithmeticError('Unresolved crossover')


def calculate(bits):
    ctx.prec = bits
    protocol = json.loads((HERE/'PROTOCOL.json').read_text())
    old = json.loads((HERE/'evidence/v18_BOUNDS_192.json').read_text())
    polynomials, norms, Dtilt, M0 = source_data(34,bits)
    a = 1/(2*arb.pi()).sqrt()
    beta = a/(16*(1+a))
    kappa = arb('4976184375/4294967296')
    gamma = beta*kappa
    Nfamily = range(3,33)
    C1 = {N:(arb(21)/8).exp()*math.factorial(N)*(arb(32)/3)**N*Dtilt[N+2]/(8*arb.pi()) for N in Nfamily}
    C2 = {N:(arb(23)/8).exp()*arb(math.factorial(2*N)).sqrt()*(arb(16)/3)**N*(arb(5)/4)**(N+1)*norms[N+1].sqrt()/(8*arb.pi()).sqrt() for N in Nfamily}
    selected = {N:choose({'L1':C1[N],'L2':C2[N]}) for N in Nfamily}
    CN = {N: C1[N] if selected[N]=='L1' else C2[N] for N in Nfamily}
    T0 = arb(9)/2
    pref = 6*beta
    early = gamma*M0*T0**4
    near_old = 21/(1+a)
    far_old = 81*arb(2).sqrt()/(1+a)
    Sgrid = range(8,129,4)
    tails = {(m,S):kernel_tail_moment(m,arb(S)) for S in Sgrid for m in [0,4]}
    archives=[]
    for r in old['archives']:
        n=r['known_active_nodes']
        archives.append({'key':r['key'],'n':n,'G':(1+gamma)**n*(gamma*arb(29)/512).exp()})
    windows=[]
    for window,tmax in [('W0',arb(1)),('W1',arb(5)/4)]:
        smax=(5+tmax)**2-1
        qcap=smax*smax/128
        Dgeom=16*qcap.exp()
        moments={S:{0:kappa*S+Dgeom*tails[0,S],4:kappa*arb(S)**5/5+Dgeom*tails[4,S]} for S in Sgrid}
        candidates={(N,S):early+pref*(moments[S][0]*field_integral(M0,CN[N],N,T0)+M0*moments[S][4]/2) for N in Nfamily for S in Sgrid}
        bestN,bestS=choose(candidates)
        base=candidates[bestN,bestS]
        rows=[]
        simple_best=[]
        for power in range(3,81):
            L=arb(2)**power
            nvals={N:field_integral(M0,CN[N],N,L) for N in Nfamily}
            N=choose(nvals)
            # A positive far-term upper bound, dropping the -L^2 contribution.
            if L < bestS**2:
                far= (kappa*(arb(bestS)**5-L**(arb(5)/2))/5+Dgeom*tails[4,bestS])/2
            else:
                far=Dgeom*kernel_tail_moment(4,L.sqrt())/2
            tail=pref*(moments[bestS][0]*nvals[N]+M0*far)
            one={n:near_old*CN[n]*L**(2-n)/(n-2)+far_old*M0*(-L/256).exp()*(256*L+65536) for n in Nfamily}
            simpleN=choose(one)
            split=gamma*M0*((L+arb(1)/2)**4-arb(6561)/128)+Dgeom*one[simpleN]
            simple_best.append((power,simpleN,split))
            rows.append({'L_power':power,'N':N,'direct_tail':enc(tail),'transported_tail':{r['key']:enc(r['G']*tail) for r in archives}})
        sb=min(simple_best,key=lambda r:float(r[2].log()))
        if not all(sb[2]<r[2] for r in simple_best if r[0]!=sb[0]):raise ArithmeticError('simple L minimum')
        window_result={'window':window,'q_overlap_cap':enc(qcap),'D_geometric':enc(Dgeom),'conditioning_improvement_factor':enc(arb(old['D_conditional'])/Dgeom),
                       'selected_N':bestN,'selected_S':bestS,'early_direct_bound':enc(early),'kernel_I0':enc(moments[bestS][0]),'kernel_I4':enc(moments[bestS][4]),
                       'direct_full_bound':enc(base),'archives':[],'tail_grid':rows}
        for r in archives:
            full=r['G']*base
            first=next(x for x in rows if arb(x['transported_tail'][r['key']])<arb(1)/1000)
            original=next(z for z in old['archives'] if z['key']==r['key'])
            window_result['archives'].append({'key':r['key'],'full_remainder_L1_bound':enc(full),'improvement_over_v18_grid_majorant':enc(arb(original['best_grid_full_beyond5']['bound'])/full),
                'improved_v18_split_bound':enc(r['G']*sb[2]),'improved_split_L_power':sb[0],'improved_split_N':sb[1],
                'first_tail_grid_below_0_001':{'L_power':first['L_power'],'N':first['N'],'bound':first['transported_tail'][r['key']]}})
        windows.append(window_result)
    out={'schema':'cspp.source-overlap/0.19','bits':bits,'source_M0':enc(M0),'source_improvement_factor':enc(arb(old['M0'])/M0),
         'norm_squared':{str(j):enc(x) for j,x in norms.items()},'tilted_L1_D':{str(j):enc(x) for j,x in Dtilt.items()},
         'strip_C':{str(N):{'L1':enc(C1[N]),'L2':enc(C2[N]),'selected':selected[N]} for N in Nfamily},
         'archives':[{'key':r['key'],'known_active_nodes':r['n'],'transport_factor':enc(r['G'])} for r in archives],
         'windows':windows,'status':protocol['status'],'new_random_calls':0,
         'scope':'Conditional expected absolute remainder; no observed error, no individual accuracy certification.'}
    (HERE/f'results/BOUNDS_{bits}.json').write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps({'bits':bits,'M0':out['source_M0'],'windows':[{k:w[k] for k in ['window','D_geometric','selected_N','selected_S','archives']} for w in windows]},indent=2),flush=True)


if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--bits',type=int,default=384)
    calculate(p.parse_args().bits)
