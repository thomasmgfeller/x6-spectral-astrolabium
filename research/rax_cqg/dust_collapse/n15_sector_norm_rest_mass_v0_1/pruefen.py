"""CST-DUST: independently audit sector identifiability and tagged mass transfer."""
import csv
import hashlib
import json
import sys
from collections import Counter
from fractions import Fraction as Q
from itertools import combinations, product
from math import fsum, isqrt, sqrt
from pathlib import Path

ROOT = Path(__file__).resolve().parent
SRC = ROOT / 'quellen'
P, I, F = (0,1,2,3), (4,5,6,11,12,13,14), (7,8,9,10)
NODES = tuple(range(15))
LAYER = (1,-9,16,-8)


def load(name):
    return json.loads((SRC/name).read_bytes())


def source_check():
    manifest = json.loads((ROOT/'quellen.json').read_bytes())
    for item in manifest['files']:
        name = item['path']
        path = ROOT/Path(name).name if Path(name).name in ('LICENSE','NOTICE') else SRC/name
        content = path.read_bytes()
        header = f'blob {len(content)}\0'.encode()
        assert hashlib.sha1(header+content).hexdigest() == item['git_blob'],name
    contract = (ROOT/'pruefvertrag.json').read_bytes()
    digest = hashlib.sha256(contract).hexdigest()
    assert digest == (ROOT/'pruefvertrag.sha256').read_text().split()[0]
    cfg = json.loads(contract)
    assert cfg['source_commit'] == manifest['commit']
    return cfg,digest


def geometry(code):
    rel = set(combinations(P,2)) | set(combinations(F,2))
    rel.update(product(P,I+F))
    rel.update(product(I,F))
    rel.update((a,b) for j,(a,b) in enumerate(combinations(I,2)) if code & (1<<j))
    assert all((a,c) in rel for a,b in rel for u,c in rel if b==u)
    b = {}
    for a,v in rel:
        n = sum((a,t) in rel and (t,v) in rel for t in NODES)
        b[a,v] = LAYER[n] if n<4 else 0
    assert all(b[i,j]==0 for i,j in product(P,F))
    return rel,b


def scalar_overlap(cfg):
    with (SRC/'n15_charge_interval_record_v0_1/ueberlapp.csv').open(newline='') as f:
        reference = {(r['M']+'/'+r['r'],r['A:B']):float(r['normalized_sign_overlap']) for r in csv.DictReader(f)}
    rows = []
    for key,values in load('joint_charge_distribution_v0_1/joint.json')['rows'].items():
        for law in ('1:1','1:3'):
            g = values[law]['decoherence_matrix_scaled_by_record_trace']
            neg, pos = range(3),range(3,6)
            def block(ii,jj):
                return complex(*(fsum(g[part][i][j] for i in ii for j in jj) for part in ('re','im')))
            dn,dp,cross = block(neg,neg).real,block(pos,pos).real,block(neg,pos)
            assert dn>0 and dp>0
            overlap = abs(cross)/sqrt(dn*dp)
            tol = float(cfg['compare_published_overlaps_abs_tol'])
            assert 0 < overlap < 1 and abs(overlap-reference[key,law]) < tol
            for a,b in ((1,1),(2,3),(.001,1000),(1000,.001)):
                scaled = abs(a*b*cross)/sqrt((a*a*dn)*(b*b*dp))
                assert abs(scaled-overlap) < tol
            rows.append({'M/r':key,'A:B':law,'normalized_overlap':overlap})
    assert len(rows) == cfg['six_bin_gram_rows'] == len(reference)
    g = load('n15_future_boundary_v0_1/ergebnis.json')['gram_over_common_squared_norm']
    assert g == [[1,1],[1,1]]
    for a,b in ((Q(1),Q(1)),(Q(2),Q(3)),(Q(1,1000),Q(1000))):
        # In the rescaled packet basis the null vector is (1/a,-1/b).
        def norm(x,y):
            return g[0][0]*(a*x)**2+2*g[0][1]*a*b*x*y+g[1][1]*(b*y)**2
        assert norm(1/a,-1/b) == 0 and norm(1/a,0) == 1
    return {'ensemble_overlap_rows':rows,'min':min(r['normalized_overlap'] for r in rows),
            'max':max(r['normalized_overlap'] for r in rows),'single_type_packet_overlap_exact':'1',
            'normalized_null_norm':'0','normalized_positive_projection_norm':'1',
            'physical_sector_ratio':None,'status':'NOT_IDENTIFIABLE_FROM_THIS_PAIRING'}


def interval_row(x):
    return {'interval':[str(v) for v in x],'midpoint':float(sum(x)/2)}


def mul(a,b):
    values = [x*y for x,y in product(a,b)]
    return min(values),max(values)


def gain(m,charge):
    assert charge[0]>0
    return m/charge[1],m/charge[0]


def dimensionless_current(coeff,y,weights):
    # weights = w/Delta; exterior contributions to this derivative cancel.
    # The complete action is quadratic in the common shift of the four past clocks.
    h = Q(1,7)
    def action(s):
        z = {v:y[v]+s if v in P else y[v] for v in NODES}
        kinetic = sum(c*weights[v]*(z[v]-z[i])**2 for (i,v),c in coeff.items())
        return -sum(weights.values())/2-kinetic/38
    return (action(-h/2)-action(h/2))/h


def read_profile(rel,coeff,path,mass,k,theta,empty=False):
    a,b = path[1:-1]
    assert Q(1,4)<k<Q(1,2)
    # Every traversed edge is a cover. Count the crossing flux independently of p.
    links = tuple(zip(path,path[1:]))
    assert all((i,j) in rel and not any((i,t) in rel and (t,j) in rel for t in NODES)
               for i,j in links)
    cut_mass = sum(mass for i,j in links if i in P and j not in P)
    assert cut_mass == mass
    u = {a:Q(1,2)-k,b:k}
    rest = [v for v in I if v not in u]
    u.update({v:Q(1,2)+Q(j,2*(len(rest)+1)) for j,v in enumerate(rest,1)})
    assert all(u[i]<u[j] for i,j in rel if i in I and j in I)
    half = (u[a]+u[b])/2
    y = {v:Q(v-5) for v in P+F}
    y[3] += theta
    y.update({v:-2+theta+(4-theta)*u[v] for v in I})
    w = dict.fromkeys(NODES,Q(0))
    # Any common exterior density serves in this derivative: P->F has zero
    # layer coefficient, P->P clock differences stay constant. Exercise both vacua.
    if not empty:
        w.update({v:Q(1,8) for v in P+F})
    w[a],w[b] = (mass*(4-theta)*h for h in (half,1-half))
    return dimensionless_current(coeff,y,w)


def polynomial(rel,coeff,path,mass,k):
    def charge(t):
        return read_profile(rel,coeff,path,mass,k,t)
    d=Q(1,4)
    left,center,right = charge(-d),charge(Q(0)),charge(d)
    p0,p1,p2 = center,(right-left)/(2*d),(right+left-2*center)/(2*d*d)
    # Independent closed expression from PR 334, checked as polynomial identity.
    assert (p0,p1,p2) == (mass*4*(1+12*k)/76,
                           mass*(-4*(23+3*k)-(1+12*k))/76,mass*(23+3*k)/76)
    for t in (-Q(1,3),Q(1,3)):
        assert charge(t) == p0+p1*t+p2*t*t
    return p0,p1,p2


def mass_tests(cfg,tol):
    rel,coeff = geometry(cfg['type'])
    path = cfg['path']
    windows = [tuple(map(Q,w)) for w in cfg['clock_windows']]
    width = sum(h-l for l,h in windows)
    moments = [sum((h**(j+1)-l**(j+1))/(j+1) for l,h in windows)/width for j in (1,2)]
    assert moments == [0,Q(13,3072)]
    grid = 10**40
    i = isqrt(3*grid**2//722)
    delta2 = Q(i,grid),Q(i+1,grid)
    assert delta2[0]**2 <= Q(3,722) < delta2[1]**2
    moment_theta2 = moments[1]/delta2[1],moments[1]/delta2[0]
    def mean(m,k):
        c,_,a = polynomial(rel,coeff,path,m,k)
        lo,hi = mul((a,a),moment_theta2)
        return c+lo,c+hi
    assert all(read_profile(rel,coeff,path,Q(0),Q(1,3),Q(1,4),empty) == 0 for empty in (False,True))
    assert mean(Q(0),Q(1,3)) == (0,0)
    m0,k0 = (Q(cfg['calibration'][key]) for key in ('M','k'))
    mu = mean(m0,k0)
    g = gain(m0,mu)
    primary = load('cut_mass_charge_vacuum_v0_1/results.json')['paired_readings']['profiles']
    for key,profile in primary.items():
        measured = mean(m0,Q(key))
        prior = tuple(map(Q,profile['response']['1/4']['auxiliary_mean_p']['exact_bounds']))
        assert prior[0] <= measured[0] <= measured[1] <= prior[1]
    # Full-window physical-density support on this tagged path for both transfers.
    assert Q(13,50)**4 > Q(3,722)
    dmax = 4*Q(13,50)-min(l for l,h in windows)
    assert all(Q(row['M'])*dmax*Q(3,4)<1 for row in cfg['no_refit_transfers'])
    out=[]
    for row in cfg['no_refit_transfers']:
        m,k = Q(row['M']),Q(row['k'])
        p=mean(m,k)
        prediction=mul(g,p)
        if k == k0:
            # Under matched profiles the same polynomial multiplies M.
            assert polynomial(rel,coeff,path,m,k) == tuple(x*m/m0 for x in polynomial(rel,coeff,path,m0,k0))
            assert prediction[0]<=m<=prediction[1]
            prediction=(m,m)
        err=prediction[0]/m-1,prediction[1]/m-1
        status = ('PASS' if -tol<=err[0]<=err[1]<=tol else
                  'FAIL' if err[1]<-tol or err[0]>tol else 'HOLD')
        out.append({**row,'mean_p':interval_row(p),'predicted_M':interval_row(prediction),
                    'relative_error':interval_row(err),'status':status})
    return {'model_only':True,'tagged_cut_mass':str(m0),'clock_profile':str(k0),
            'mean_p_at_calibration':interval_row(mu),'single_frozen_gain':interval_row(g),
            'matched_and_separate_vacua_p':'0','relative_tolerance':str(tol),'transfers':out}


def charge_collision(cfg):
    # All tests are at physical-event coordinates. Delta cancels from p/M.
    sys.path.insert(0,str(SRC/'n15_future_boundary_v0_1'))
    import density_translation_375841 as cell
    rel,coeff = geometry(cfg['type'])
    base_rel,paths,base_coeff = cell.local_geometry()
    assert rel == base_rel and coeff == base_coeff
    e = -Q(1,4)
    assert Q(1,4)**4 < Q(3,722) < Q(13,50)**4
    assert -Q(3,32) < e*Q(13,50) < e*Q(1,4) < -Q(1,32)
    y = {v:Q(v-5) for v in P+F}
    y[3]+=e
    y.update({v:-2+e+(4-e)*cell.CENTER[v] for v in I})
    dwell = dict.fromkeys(I,Q(0))
    for path in paths:
        cuts = [Q(0)]+[(cell.CENTER[a]+cell.CENTER[b])/2 for a,b in zip(path,path[1:])]+[Q(1)]
        for v,lo,hi in zip(path,cuts,cuts[1:]):
            dwell[v]+=(hi-lo)/len(paths)
    C = {v:1+sum(coeff[i,v]*(y[v]-y[i])**2 for i in NODES if (i,v) in rel)/19 for v in I}
    a,b,c=5,12,13
    d = {v:Q(0) for v in I}
    for v,left,right in ((a,b,c),(b,c,a),(c,a,b)):
        d[v]=Q(7600,8000000)*(C[left]-C[right])
    assert sum(dwell.values())==1 and sum(d.values())==0 and sum(C[v]*d[v] for v in I)==0
    def reading(m,t):
        x={v:dwell[v]+(2*t-1)*d[v] for v in I}
        assert 0<=t<=1 and sum(x.values())==1
        assert all(abs(x[v]-dwell[v])<dwell[v]/100 for v in I)
        # 0 < w=M Delta(4-e)x < 1 follows from this rational upper bound.
        assert Q(13,50)**4 > Q(3,722)
        assert all(0<m*Q(13,50)*(4-e)*x[v]<1 for v in I)
        w=dict.fromkeys(NODES,Q(1,8))
        w.update({v:m*(4-e)*x[v] for v in I})
        p=dimensionless_current(coeff,y,w)
        return p
    mref=Q(1,4)
    r0,r1=reading(mref,Q(0))/mref,reading(mref,Q(1))/mref
    archived=load('n15_future_boundary_v0_1/ergebnis.json')
    assert [r0,r1]==list(map(Q,archived['center_p_over_M']))
    boxes = cell.enclose(cell.RADIUS)
    assert Q(boxes['positive'][0]) > 0 > Q(boxes['negative'][1])
    assert r0>0>r1
    mlist=list(map(Q,cfg['normalized_masses']))
    target_positive=min(mlist)*r0/2
    rows=[]
    for target,m in product((Q(0),target_positive),mlist):
        t=(r0-target/m)/(r0-r1)
        assert 0<t<1 and reading(m,t)==target
        rows.append({'M_marked':str(m),'lambda':str(t),'p':str(target)})
    return {'type':cfg['type'],'p_per_M_endpoints':[str(r0),str(r1)],
            'shared_positive_charge':str(target_positive),'witnesses':rows,
            'scope':'Pointwise on the full positive-density preparation band, at fixed central clocks. The interpolated points need not belong to either tiny witness cell.'}


def physical_state():
    records=load('correspondence_v0_1/results/checkpoint_P3_records.json')
    eligibility=load('correspondence_v0_1/results/eligibility.json')
    run_counts=dict(Counter(r['execution'] for r in records))
    contexts=[r['checkpoint_context'] for r in records]
    assert len({(c['M'],c['x'],c['density_ratio']) for c in contexts})==len(records)==60
    zero_time=sum(c['x']=='0' for c in contexts)
    p=load('cut_mass_charge_vacuum_v0_1/results.json')['physical']
    joint=load('joint_charge_distribution_v0_1/joint.json')
    assert run_counts=={'NOT_RUN':60} and zero_time==12
    missing=['independent_positive_cut_mass_same_CST_preparation','measured_physical_charge_for_that_mass',
             'physical_vacuum_readout_same_protocol','physical_gain']
    assert all(p[k] is None for k in missing)
    assert joint['physical_mass_gain'] is None
    assert eligibility['decision']=='HOLD_NOT_ELIGIBLE' and eligibility['execution']=='NOT_RUN'
    return {'source_records':len(records),'initial_cut_records':zero_time,'executions':run_counts,
            'physical_vacuum_reading':None,'independent_physical_calibration_pair':None,
            'physical_gain':None,'physical_rest_mass_from_p':None,'physical_transfer':'NOT_RUN',
            'P3':'HOLD_NOT_ELIGIBLE'}


def main():
    if not __debug__:
        raise RuntimeError('Assertions must be enabled.')
    cfg,digest=source_check()
    plan=load('correspondence_v0_1/plan.json')
    tol=Q(str(plan['primary_tolerances']['mass_or_flux_over_M']))
    assert tol==Q(1,50)
    result={'source_commit':cfg['source_commit'],'contract_sha256':digest,
            'sector':scalar_overlap(cfg['sector']),'tagged_mass':mass_tests(cfg['tagged_model'],tol),
            'signed_charge_witness':charge_collision(cfg['charge_witness']),
            'physical':physical_state()}
    print(json.dumps(result,ensure_ascii=False,indent=2))


if __name__=='__main__':
    main()
