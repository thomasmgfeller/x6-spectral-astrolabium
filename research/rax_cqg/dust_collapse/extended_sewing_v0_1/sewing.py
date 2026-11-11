"""Reconstruct the joint finite action from serialized cut packets only.

The runtime join does not enumerate histories or query a global causal order.
It returns action coefficients; it does not compose Hilbert-space operators.
"""
from collections import Counter
from fractions import Fraction
from pathlib import Path
import argparse
import cmath
import hashlib
import json
import math

SCHEMA='cst-dust.extended-cut/0.1'
COEFF=(1,-9,16,-8)
MEASURE='boundary_state_space_v0_1: quotient=1/2; clocks=dT/2 on [-1,1]; density=(delta0+dr)/2; scalar=dq'
SCALAR={'mass':0,'beta':'4/sqrt(6)','geometry_coupling':1}

def canonical(obj):
    return json.dumps(obj,sort_keys=True,separators=(',',':'),ensure_ascii=False).encode()

def seal(packet):
    value={k:v for k,v in packet.items() if k!='payload_sha256'}
    return dict(value,payload_sha256=hashlib.sha256(canonical(value)).hexdigest())

def transitive_closure(vertices,relations):
    rel=set(map(tuple,relations))
    for k in vertices:
        rel|={(i,j) for i in vertices for j in vertices if (i,k) in rel and (k,j) in rel}
    if any(i==j for i,j in rel):raise ValueError('cyclic order')
    return rel

def local_action(vertices,relations):
    """Packet preparation/oracle utility; not used to reconstruct cross intervals."""
    v=sorted(vertices);rel=set(map(tuple,relations));terms=[]
    if any(i not in v or j not in v for i,j in rel):raise ValueError('unknown vertex')
    if transitive_closure(v,rel)!=rel:raise ValueError('order is not transitively closed')
    for i,j in sorted(rel):
        n=sum((i,z) in rel and (z,j) in rel for z in v)
        terms.append([i,j,COEFF[n] if n<4 else 0])
    return {'vertices':v,'pair_terms':terms,'F4':len(v)-sum(c for _,_,c in terms)}

def make_packet(side,vertices,relations,seam,outer_boundary,history_weight='1/33'):
    if side not in ('left','right'):raise ValueError('unknown side')
    v=sorted(vertices);rel=set(map(tuple,relations));s=sorted(seam);past=sorted(set(v)-set(s))
    if len(s)!=2 or not set(s).issubset(v):raise ValueError('two-point seam required')
    outer=sorted(outer_boundary)
    if len(outer)!=2 or len(set(outer))!=2 or not set(outer).issubset(past):raise ValueError('two-point external boundary required')
    if any((i,j) in rel for i in s for j in s):raise ValueError('seam must be an antichain')
    if side=='left' and any((i,j) in rel for i in s for j in past):raise ValueError('left cut has backward relation')
    if side=='right' and any((i,j) in rel for i in past for j in s):raise ValueError('right cut has backward relation')
    action=local_action(v,rel)
    def footprint(a):
        return sum(1<<k for k,x in enumerate(s) if ((a,x) if side=='left' else (x,a)) in rel)
    footprints={a:footprint(a) for a in past};profiles=[]
    for a in past:
        hist=Counter(footprints[z] for z in past if ((a,z) if side=='left' else (z,a)) in rel)
        profiles.append({'vertex':a,'footprint':footprints[a],
                         'interval_histogram':{str(mask):min(4,hist[mask]) for mask in range(1,1<<len(s))}})
    packet={'schema':SCHEMA,'side':side,'vertices':v,'seam':s,'outer_boundary':outer,
            'owned_regulator_vertices':sorted(set(past)-set(outer)),
            'measure_id':MEASURE,
            'scalar_parameters':SCALAR.copy(),
            'completion':'minimal_transitive_union_no_bypass_relations',
            'count_cap':4,'history_weight':str(Fraction(history_weight)),
            'profiles':profiles,'local_action':action,
            'field_memory':{str(a):dict({'clock':'t'+str(a),'scalar':'q'+str(a)},
                **({'density':'r'+str(a)} if side=='right' else {})) for a in past},
            'local_auxiliary_fields':{str(a):{'density':'r'+str(a)} for a in past} if side=='left' else {},
            'seam_fields':{str(a):{'clock':'t'+str(a),'density':'r'+str(a),'scalar':'q'+str(a)} for a in s},
            'semantics':'joint conditional amplitude; retained variables are not independently averaged'}
    return seal(packet)

def validate_packet(p):
    if p.get('schema')!=SCHEMA or p.get('count_cap')!=4:raise ValueError('unsupported packet schema')
    if seal(p)['payload_sha256']!=p.get('payload_sha256'):raise ValueError('packet hash mismatch')
    if p.get('completion')!='minimal_transitive_union_no_bypass_relations':raise ValueError('undeclared cross relations')
    if p.get('side') not in ('left','right'):raise ValueError('unsupported side')
    if p.get('measure_id')!=MEASURE or p.get('scalar_parameters')!=SCALAR:raise ValueError('unsupported measure or scalar action')
    v=p['vertices'];s=p['seam']
    if not v or len(v)!=len(set(v)) or any(type(x)!=int for x in v):raise ValueError('invalid vertex labels')
    if len(s)!=2 or s!=sorted(set(s)) or not set(s).issubset(v):raise ValueError('invalid seam labels')
    outer=p['outer_boundary']
    if len(outer)!=2 or len(set(outer))!=2 or not set(outer).issubset(set(v)-set(s)):raise ValueError('invalid external boundary')
    if p['owned_regulator_vertices']!=sorted(set(v)-set(s)-set(outer)):raise ValueError('regulator ownership mismatch')
    if p['local_action']['vertices']!=v:raise ValueError('local action vertex mismatch')
    terms=p['local_action']['pair_terms']
    pairs=[(i,j) for i,j,c in terms]
    if len(pairs)!=len(set(pairs)):raise ValueError('duplicate local pair')
    if any(i==j or i not in v or j not in v or c not in COEFF+(0,) for i,j,c in terms):raise ValueError('invalid local term')
    if any(i in s and j in s for i,j,c in terms):raise ValueError('non-antichain seam')
    if p['side']=='left' and any(i in s for i,j,c in terms):raise ValueError('backward left relation')
    if p['side']=='right' and any(j in s for i,j,c in terms):raise ValueError('backward right relation')
    if p['local_action']['F4']!=len(v)-sum(c for i,j,c in terms):raise ValueError('local gravity mismatch')
    if {x['vertex'] for x in p['profiles']}!=set(v)-set(s) or len(p['profiles'])!=len(v)-len(s):raise ValueError('missing endpoint profiles')
    masks={str(i) for i in range(1,1<<len(s))}
    for x in p['profiles']:
        if type(x['footprint'])!=int or not 0<=x['footprint']<1<<len(s):raise ValueError('invalid footprint')
        if set(x['interval_histogram'])!=masks:raise ValueError('missing histogram mask')
        if any(type(n)!=int or not 0<=n<=4 for n in x['interval_histogram'].values()):raise ValueError('invalid capped count')
    if Fraction(p['history_weight'])<0:raise ValueError('negative control weight')
    if set(p['field_memory'])!={str(x) for x in set(v)-set(s)}:raise ValueError('missing field memory')
    if set(p['seam_fields'])!={str(x) for x in s}:raise ValueError('missing seam fields')
    for x,fields in p['field_memory'].items():
        expected=dict({'clock':'t'+x,'scalar':'q'+x},**({'density':'r'+x} if p['side']=='right' else {}))
        if fields!=expected:raise ValueError('invalid memory binding')
    for x,fields in p['seam_fields'].items():
        if fields!={'clock':'t'+x,'density':'r'+x,'scalar':'q'+x}:raise ValueError('invalid seam binding')
    auxiliary={str(a):{'density':'r'+str(a)} for a in set(v)-set(s)} if p['side']=='left' else {}
    if p.get('local_auxiliary_fields')!=auxiliary:raise ValueError('local auxiliary fields missing')
    # Redundant local order rows permit verification of the cached profiles.
    # This checks each side separately; no global order enters the join.
    expected=make_packet(p['side'],v,pairs,s,outer,p['history_weight'])
    if expected['local_action']!=p['local_action']:raise ValueError('local interval coefficients inconsistent')
    if expected['profiles']!=p['profiles']:raise ValueError('cached interval profiles inconsistent')

def reconstruct_cross(left,right):
    """Use only footprints and capped histograms, never full order data."""
    cross=[]
    for a in left['profiles']:
        for b in right['profiles']:
            u=a['footprint'];v=b['footprint'];intersection=u&v
            if not intersection:continue
            nl=sum(n for mask,n in a['interval_histogram'].items() if int(mask)&v)
            ns=intersection.bit_count()
            nr=sum(n for mask,n in b['interval_histogram'].items() if int(mask)&u)
            n=min(4,nl+ns+nr)
            cross.append({'source':a['vertex'],'target':b['vertex'],
                          'left_count_capped':min(4,nl),'seam_count':ns,'right_count_capped':min(4,nr),
                          'interval_count_capped':n,'coefficient':COEFF[n] if n<4 else 0})
    return sorted(cross,key=lambda x:(x['source'],x['target']))

def sew_packets(left,right):
    validate_packet(left);validate_packet(right)
    if left['side']!='left' or right['side']!='right':raise ValueError('wrong sewing orientation')
    if left['seam']!=right['seam']:raise ValueError('explicit common seam identification required')
    if left['measure_id']!=right['measure_id'] or left['scalar_parameters']!=right['scalar_parameters']:raise ValueError('incompatible measure or scalar action')
    seam=left['seam']
    if set(left['vertices'])&set(right['vertices'])!=set(seam):raise ValueError('overlap exceeds seam')
    cross=reconstruct_cross(left,right)
    vertices=sorted(set(left['vertices'])|set(right['vertices']))
    terms=left['local_action']['pair_terms']+right['local_action']['pair_terms']+[
        [x['source'],x['target'],x['coefficient']] for x in cross]
    if len({(i,j) for i,j,c in terms})!=len(terms):raise ValueError('duplicate reconstructed pair')
    terms=sorted(terms)
    delta_f=-sum(x['coefficient'] for x in cross)
    joint={'vertices':vertices,'pair_terms':terms,'F4':len(vertices)-sum(c for i,j,c in terms)}
    if joint['F4']!=left['local_action']['F4']+right['local_action']['F4']-len(seam)+delta_f:raise ArithmeticError('gravity sewing failed')
    return {'schema':'cst-dust.sewn-action/0.1','completion':left['completion'],
            'left_packet_sha256':left['payload_sha256'],'right_packet_sha256':right['payload_sha256'],
            'history_weight':str(Fraction(left['history_weight'])*Fraction(right['history_weight'])),
            'seam':seam,'cross_intervals':cross,'delta_F4':delta_f,'joint_action':joint,
            'outer_boundary':left['outer_boundary']+right['outer_boundary'],
            'joint_regulator_vertices':sorted(left['owned_regulator_vertices']+seam+right['owned_regulator_vertices']),
            'sewing_measure_factor':2,
            'measure_scope':'two-point seam with dmu_S=(1/2)*labelled measure; other seam sizes require their own measure contract',
            'seam_action':{'F4':len(seam),'dust':'-sum(r_s)/2','scalar':0},
            'regulator':'left/right interiors each once; multiply exp(-epsilon*sum(q_s^2)/2) at seam',
            'influence_phase':'kappa*delta_F4 - beta/4 * sum_cross c_ab*(r_b*(t_b-t_a)^2+(q_b-q_a)^2)',
            'operator_status':'conditional sewing of regulated amplitudes, not Hilbert evolution'}

def doubled_hessian(action):
    v=action['vertices'];index={x:i for i,x in enumerate(v)};h=[[0]*len(v) for _ in v]
    for a,b,c in action['pair_terms']:
        i=index[a];j=index[b];h[i][i]-=c;h[j][j]-=c;h[i][j]+=c;h[j][i]+=c
    return h

def action_components(action,fields):
    """Exact rational coefficients of kappa, 1 and beta; no fitted phases."""
    v=action['vertices']
    f={kind:{i:Fraction(str(fields[kind][str(i)])) for i in v} for kind in ('t','r','q')}
    if any(r<0 or r>1 for r in f['r'].values()):raise ValueError('density outside control support')
    if any(abs(t)>1 for t in f['t'].values()):raise ValueError('clock outside control support')
    dust0=-sum(f['r'].values())/2;dust2=Fraction(0);scalar2=Fraction(0)
    for i,j,c in action['pair_terms']:
        dust2-=Fraction(c,4)*f['r'][j]*(f['t'][j]-f['t'][i])**2
        scalar2-=Fraction(c,4)*(f['q'][j]-f['q'][i])**2
    return {'gravity_over_kappa':str(action['F4']),'dust_constant':str(dust0),
            'dust_over_beta':str(dust2),'scalar_over_beta':str(scalar2)}

def influence_components(joined,fields):
    """Phase of the actual sewing multiplier, Delta S - S_seam, divided by hbar."""
    cross_action={'vertices':joined['joint_action']['vertices'],
                  'pair_terms':[[x['source'],x['target'],x['coefficient']] for x in joined['cross_intervals']],
                  'F4':joined['delta_F4']-len(joined['seam'])}
    result=action_components(cross_action,fields)
    result['dust_constant']=str(sum(Fraction(str(fields['r'][str(x)])) for x in joined['seam'])/2)
    return result

def evaluate_influence(joined,fields,epsilon):
    """Evaluate the sewing multiplier at fixed fields (ordinary float precision).

    The exact phase coefficients remain authoritative. This is not an integral
    over memory variables, and it carries no certified numerical error bound.
    The declared control uses kappa=1.
    """
    eps=float(Fraction(str(epsilon)))
    if not math.isfinite(eps) or eps<0:raise ValueError('finite nonnegative epsilon required')
    p={k:float(Fraction(v)) for k,v in influence_components(joined,fields).items()}
    phase=p['gravity_over_kappa']+p['dust_constant']+(4/math.sqrt(6))*(p['dust_over_beta']+p['scalar_over_beta'])
    q2=sum(float(Fraction(str(fields['q'][str(x)])))**2 for x in joined['seam'])
    return 2*cmath.exp(complex(-eps*q2/2,phase))

def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('left');p.add_argument('right');p.add_argument('--output',required=True)
    p.add_argument('--fields',help='optional JSON binding with t,r,q maps to rational strings')
    p.add_argument('--epsilon',help='optional nonnegative rational regulator for a floating-point influence value; requires --fields')
    args=p.parse_args()
    result=sew_packets(json.loads(Path(args.left).read_text()),json.loads(Path(args.right).read_text()))
    if args.fields:
        fields=json.loads(Path(args.fields).read_text())
        result['bound_action']=action_components(result['joint_action'],fields)
        result['sewing_phase_components']=influence_components(result,fields)
        if args.epsilon is not None:
            z=evaluate_influence(result,fields,args.epsilon)
            result['influence_value']={'real':z.real,'imag':z.imag,'epsilon':args.epsilon,
                                       'arithmetic':'floating-point diagnostic, not an error certificate'}
    elif args.epsilon is not None:p.error('--epsilon requires --fields')
    out=Path(args.output);out.parent.mkdir(parents=True,exist_ok=True)
    out.write_text(json.dumps(result,sort_keys=True,indent=2)+'\n')
    print(json.dumps({'status':'PASS','output':str(out),'cross_terms_nonzero':sum(x['coefficient']!=0 for x in result['cross_intervals']),'delta_F4':result['delta_F4']}))

if __name__=='__main__':main()
