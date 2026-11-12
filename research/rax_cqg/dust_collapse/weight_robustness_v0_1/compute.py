"""Certify global weight-simplex minima. Solvers supply no proof assumptions."""
import argparse, hashlib, json
from pathlib import Path
from flint import arb, acb, acb_mat, ctx
import basis as b

ROOT=Path(__file__).resolve().parent

def read(name):return json.loads((ROOT/name).read_text())
def write(name,data):(ROOT/name).write_text(json.dumps(data,indent=2,sort_keys=True)+'\n')
def rs(x):return x.str(40,more=True)
def adj(a):return a.conjugate().transpose()
def vec(data):return acb_mat([[acb(arb(z['real']),arb(z['imag']))] for z in data])
def norm(v):return (adj(v)*v)[0,0].real.sqrt()
def inner(u,a,v):return (adj(u)*a*v)[0,0]
def interval_matrix_pack(a):return b.matrix_pack(a)

def orbit_data(data):
    rows=data['rows'];t=b.gram_transform();ref=b.scalar(b.pc.reference_h0())
    r=b.density_input();rn=sum(abs(z)**2 for z in r).sqrt();out=[]
    for row in rows:
        d,e=b.dust(row);s=b.scalar(b.pc.h0(row['code']));phase=acb(0,row['F4']).exp()
        dw=[b.pc.widen(z,err) for z,err in zip(d,e)]
        def block(field):
            c=acb_mat(6,2)
            for k in range(3):
                a=adj(t)*(field*dw[k]*phase)*t
                for i in range(2):
                    for j in range(2):c[2*k+i,j]=a[i,j]
            return c
        coupled=block(s);decoupled=block(ref)
        # Direct difference retains the common quadrature error cancellation.
        delta=block(s-ref)
        out.append({'code':row['code'],'members':row['members'],'multiplicity':len(row['members']),
                    'F4':row['F4'],'phase':phase,'dust':dw,'scalar':s,
                    'coupled':coupled,'decoupled':decoupled,'difference':delta})
    return out,ref,r,rn

def choose(o,key,rn):
    c=o['difference']
    return c*rn if key=='full6' else acb_mat([[c[i,j] for j in range(2)] for i in range(2,6)])

def sigma(c):
    h=adj(c)*c;a=h[0,0].real;d=h[1,1].real;z=h[0,1]
    gap=((a-d)**2+4*abs(z)**2).sqrt()
    return ((a+d+gap)/2).sqrt()

def combine(blocks,w):
    return sum((a*x for a,x in zip(blocks,w)),acb_mat(blocks[0].nrows(),2))

def certify(orbits,rn,key):
    candidate=read('inputs/'+key+'_candidate.json');den=candidate['weight_denominator'];nums=candidate['weight_numerators']
    if len(nums)!=len(orbits) or any(n<0 for n in nums) or sum(nums)!=den:raise ArithmeticError('inadmissible primal weights')
    w=[arb(n)/den for n in nums];u=vec(candidate['left_vector']);v=vec(candidate['right_vector'])
    nu=norm(u);nv=norm(v)
    if not nu>0 or not nv>0:raise ArithmeticError('zero dual vector')
    blocks=[choose(o,key,rn) for o in orbits]
    scores=[inner(u,a,v).real/(nu*nv) for a in blocks]
    lower=min(x.lower() for x in scores);upper=sigma(combine(blocks,w)).upper()
    # These outward decimal endpoints are part of the checked certificate.
    endpoints={'full6':('0.0022939794998','0.0022939795002'),
               'positive':('0.0003502439596','0.0003502439599')}
    lo,hi=map(arb,endpoints[key])
    if not lower>lo or not upper<hi:raise ArithmeticError('fixed enclosure not certified')
    epsilon=arb(1)/10**12
    wp=[(1-epsilon)*x+epsilon*arb(o['multiplicity'])/33 for o,x in zip(orbits,w)]
    if not all(x>0 for x in wp):raise ArithmeticError('full-support witness not positive')
    positive_upper=sigma(combine(blocks,wp)).upper()
    if not positive_upper<hi:raise ArithmeticError('full-support upper endpoint unresolved')
    test_coefficients=u/nu
    incoming=v/nv
    if key=='full6':
        density=b.density_input()
        incoming=acb_mat([[density[i//2].conjugate()/rn*incoming[i%2,0]] for i in range(6)])
    return {'status':'POSITIVE_GLOBAL_LOWER_BOUND','objective':key,'lower_endpoint':str(endpoints[key][0]),
            'upper_endpoint':str(endpoints[key][1]),'certified_dual_lower':rs(lower),'certified_primal_upper':rs(upper),
            'positive_witness_epsilon':'1/1000000000000','positive_witness_upper':rs(positive_upper),
            'positive_witness_weights':{str(o['code']):rs(x) for o,x in zip(orbits,wp)},
            'universal_test_coefficients_V_orthonormal':interval_matrix_pack(test_coefficients),
            'universal_input_coefficients_V_orthonormal':interval_matrix_pack(incoming),
            'dual_vector_norm_product':rs(nu*nv),'dual_scores':{str(o['code']):rs(x) for o,x in zip(orbits,scores)},
            'primal_weight_denominator':den,'primal_weight_numerators':nums,
            'primal_orbit_weights':{str(o['code']):rs(x) for o,x in zip(orbits,w)},
            'proof':'For all simplex w: ||sum w A||2 >= Re(u* sum w A v)/(||u||||v||) >= min_o score_o. Upper from an exact rational feasible w; no solver assumptions.',
            'primal_compressed_block':interval_matrix_pack(combine(blocks,w))}

def diagnostics(orbits,ref,r,rn,weights):
    z=sum(w*o['phase'] for w,o in zip(weights,orbits))
    if not z.abs_lower()>0:raise ArithmeticError('diagnostic Z unresolved; never exclude such weights from optimization')
    average=sum((w*o['phase']*o['scalar'] for w,o in zip(weights,orbits)),acb_mat(2,2))/z
    t=b.gram_transform();matrices={name:acb_mat(6,2) for name in ('coupled','decoupled','difference','connected','mean_response')}
    for o,w in zip(orbits,weights):
        for name in ('coupled','decoupled','difference'):matrices[name]+=o[name]*w
        for k in range(3):
            for name,field in [('connected',o['scalar']-average),('mean_response',average-ref)]:
                a=adj(t)*(field*o['dust'][k]*o['phase']*w)*t
                for i in range(2):
                    for j in range(2):matrices[name][2*k+i,j]+=a[i,j]
    residual=matrices['difference']-matrices['connected']-matrices['mean_response']
    if not all(residual[i,j].contains(0) for i in range(6) for j in range(2)):raise ArithmeticError('decomposition failure')
    packed={}
    for name,c in matrices.items():
        full=acb_mat([[c[i,j%2]*r[j//2] for j in range(6)] for i in range(6)])
        positive=acb_mat([[c[i,j] for j in range(2)] for i in range(2,6)])
        packed[name]={'V_normalized_block':interval_matrix_pack(full),'full6_sigma':rs(sigma(c*rn)),'positive_sigma':rs(sigma(positive))}
    return {'gravity_sum':b.pc.pack(z,40),'blocks':packed,'decomposition':'difference = connected + mean_response, checked by interval overlap'}

def main():
    p=argparse.ArgumentParser();p.add_argument('--recompute-quadrature',action='store_true');args=p.parse_args();ctx.prec=192
    if hashlib.sha256((ROOT/'contract.json').read_bytes()).hexdigest()!=(ROOT/'contract.sha256').read_text().strip():raise ArithmeticError('changed contract')
    stored=read('inputs/quadrature.json')
    if args.recompute_quadrature:
        fresh=b.quadrature(40)
        if fresh!=stored:raise ArithmeticError('quadrature replay mismatch')
        print('PASS: all ten 40-node/192-bit orbit quadratures exactly reproduced',flush=True)
    orbits,ref,r,rn=orbit_data(stored)
    for key in ('full6','positive'):
        cert=certify(orbits,rn,key);write('results/'+key+'_certificate.json',cert)
        print(key,cert['lower_endpoint'],cert['upper_endpoint'], 'dual',cert['certified_dual_lower'],'primal',cert['certified_primal_upper'],flush=True)
    sets={'uniform':[arb(o['multiplicity'])/33 for o in orbits]}
    for key in ('full6','positive'):
        candidate=read('inputs/'+key+'_candidate.json');sets[key+'_near_minimizer']=[arb(n)/candidate['weight_denominator'] for n in candidate['weight_numerators']]
    scalars={o['code']:o['scalar'] for o in orbits};alt=b.cancellation_weights(stored['rows'],scalars,ref)
    sets['prior_channel_cancellation']=[alt[o['code']] for o in orbits]
    result={name:diagnostics(orbits,ref,r,rn,w) for name,w in sets.items()}
    # At each orbit vertex the scalar response is constant on its orbit:
    # connected=0 exactly, while the difference is nonzero.
    result['vertices']=[{'code':o['code'],'full6_difference_sigma':rs(sigma(o['difference']*rn)),
                        'connected':'EXACT_ZERO','mean_response':'EXACTLY_DIFFERENCE',
                        'gravity_sum_abs':'EXACTLY_ONE'} for o in orbits]
    write('results/diagnostics.json',result)
    write('results/orbit_blocks.json',{'incoming_density_norm':rs(rn),'orbits':[
        {'code':o['code'],'members':o['members'],'multiplicity':o['multiplicity'],'F4':o['F4'],
         'V_normalized_compressed_difference':interval_matrix_pack(o['difference'])} for o in orbits]})

if __name__=='__main__':main()
