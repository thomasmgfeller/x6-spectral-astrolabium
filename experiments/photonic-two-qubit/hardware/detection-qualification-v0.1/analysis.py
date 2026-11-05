"""Offline detector diagnostics. No device control and no automatic hardware release."""
import argparse
import bisect
import hashlib
import itertools
import json
import math
from pathlib import Path
import statistics

H = 6.62607015e-34
C = 299792458.0

def finite(x):
    if isinstance(x, bool) or not isinstance(x, (int, float)) or not math.isfinite(x):
        raise ValueError('finite number required')
    return x

def integer(x, minimum=0):
    if isinstance(x, bool) or not isinstance(x, int) or x < minimum:
        raise ValueError('integer out of range')
    return x

def poisson_upper(count, exposure_s, alpha=.01):
    """One-sided exact Poisson limit, conditional on the Poisson/stationarity model.

    Invert P(N<=n|lambda)=alpha. Descending recurrence starts at n and is
    stable for the upper-limit domain lambda>n. No Gaussian approximation.
    """
    n=integer(count); t=finite(exposure_s); a=finite(alpha)
    if t<=0 or not 0<a<.5: raise ValueError('positive exposure and 0<alpha<0.5 required')
    if n==0:return -math.log(a)/t
    def cdf(lam):
        term=math.exp(-lam+n*math.log(lam)-math.lgamma(n+1)); total=term
        for k in range(n,0,-1):
            term*=k/lam;total+=term
            if term<total*1e-15:break
        return total
    lo=float(n);hi=n+10*math.sqrt(n+1)+100
    while cdf(hi)>a:hi*=2
    for _ in range(70):
        mid=(lo+hi)/2
        if cdf(mid)>a:lo=mid
        else:hi=mid
    return hi/t

def zero_error_upper(trials, alpha=.01):
    """One-sided binomial upper limit for zero observed failures, per test."""
    n=integer(trials,1);a=finite(alpha)
    if not 0<a<1:raise ValueError('0<alpha<1 required')
    return -math.expm1(math.log(a)/n)

def photon_flux(power_W, wavelength_nm):
    p=finite(power_W);w=finite(wavelength_nm)
    if p<0 or w<=0:raise ValueError('invalid optical power or wavelength')
    return p*w*1e-9/(H*C)

def pulsed_efficiency(clicks, trials, dark_clicks, dark_trials, mu):
    """Point estimate for isolated Poisson optical pulses with independent background.

    Requires reset/recovery and negligible/bounded afterpulses in the prompt
    window. Measures efficiency at the specified optical reference plane.
    Uncertainty, pulse statistics and systematic corrections are not certified.
    """
    n=integer(trials,1);nd=integer(dark_trials,1)
    k=integer(clicks);kd=integer(dark_clicks);m=finite(mu)
    if k>=n or kd>=nd or m<=0:raise ValueError('unsaturated probabilities and positive mu required')
    p=k/n;d=kd/nd
    if p<d:raise ValueError('negative signal estimate: fit a counting model; do not clip')
    eta=(math.log1p(-d)-math.log1p(-p))/m
    return {'eta_point':eta,'prompt_probability':p,'dark_probability':d,
            'model_status':'CONDITIONAL' if eta<=1 else 'INCONSISTENT_WITH_MODEL',
            'uncertainty_status':'NOT_EVALUATED'}

def secondary_excess(k, n, k_background, n_background):
    """Operational excess probability of >=1 secondary in a fixed observed window.

    Matched conditional windows and independent background are assumptions.
    This is not an intrinsic trap-release probability or an all-time afterpulse rate.
    Negative estimates are retained, not clipped.
    """
    n=integer(n,1);nb=integer(n_background,1);k=integer(k);kb=integer(k_background)
    if k>n or kb>=nb:raise ValueError('invalid trial counts')
    p=k/n;b=kb/nb
    return {'raw_secondary_probability':p,'background_probability':b,
            'observed_window_excess_probability':(p-b)/(1-b),
            'uncertainty_status':'NOT_EVALUATED'}

def independent_deconvolution(sigma_measured_ps, sigma_reference_ps, sigma_instrument_ps,
                              independence_verified=False):
    ss=[finite(x) for x in (sigma_measured_ps,sigma_reference_ps,sigma_instrument_ps)]
    if min(ss)<0:raise ValueError('negative standard deviation')
    if not independence_verified:return {'sigma_dut_ps':None,'status':'HOLD_COVARIANCE_MODEL'}
    variance=ss[0]**2-ss[1]**2-ss[2]**2
    return {'sigma_dut_ps':math.sqrt(variance) if variance>0 else None,
            'status':'CONDITIONAL_POINT_ESTIMATE' if variance>0 else 'UNRESOLVED_NOT_ZERO'}

def rate_linearity(flux, observed_rate, dark_rate, frozen_gain):
    f,r,d,g=[finite(x) for x in (flux,observed_rate,dark_rate,frozen_gain)]
    if f<=0 or r<0 or d<0 or g<=0:raise ValueError('invalid linearity input')
    return (r-d)/(g*f)-1

def recovery_ratio(second_clicks, conditioned_firsts, baseline_probability):
    n=integer(conditioned_firsts,1);k=integer(second_clicks);p=finite(baseline_probability)
    if k>n or not 0<p<=1:raise ValueError('invalid recovery data')
    return (k/n)/p

def timing_groups(groups, offsets_ps, full_window_ps=2000):
    """Independent stimulus IDs; signed integer timestamps before float statistics.

    Offsets are frozen before these validation groups, not fitted here.
    Six pair results include all available samples; no coincidence-window crop.
    """
    if len(offsets_ps)!=4 or any(isinstance(x,bool) or not isinstance(x,int) for x in offsets_ps):
        raise ValueError('four frozen integer-ps offsets required')
    integer(full_window_ps,1)
    seen=set();data={pair:[] for pair in itertools.combinations(range(4),2)}
    for row in groups:
        pulse=integer(row['pulse_id'])
        if pulse in seen:raise ValueError('duplicate independent pulse ID')
        seen.add(pulse);ts=row['t_ps']
        if len(ts)!=4:raise ValueError('four channel fields required')
        for t in ts:
            if t is not None:
                integer(t)
                if t>=2**64:raise ValueError('timestamp outside uint64')
        for (i,j),values in data.items():
            if ts[i] is not None and ts[j] is not None:
                values.append((ts[j]-ts[i])-(offsets_ps[j]-offsets_ps[i]))
    if not seen:raise ValueError('no pulse groups')
    result=[]
    for (i,j),dt in data.items():
        result.append({'channels':[i,j],'n_pairs':len(dt),'missing_groups':len(seen)-len(dt),
          'mean_ps':statistics.mean(dt) if dt else None,
          'sigma_ps':statistics.stdev(dt) if len(dt)>1 else None,
          'minimum_ps':min(dt) if dt else None,'maximum_ps':max(dt) if dt else None,
          'fraction_in_fixed_window':sum(2*abs(v)<=full_window_ps for v in dt)/len(dt) if dt else None})
    return {'scope':'ELECTRICAL_OR_OPTICAL_CALIBRATION_DIAGNOSTIC','pairs':result,
            'uncertainty_status':'NOT_EVALUATED','physical_qualification':'NOT_ASSESSED'}

def coincidence_components(events, offsets_ps, full_window_ps=2000, b_shift_ps=0):
    """Small diagnostic records only; exact bipartite connected-component rule.

    Not a streaming converter or a replacement for the full primary CHSH path.
    Channel IDs here are canonical 0..3, not SDK 1..4. Never pair across files.
    """
    if len(events)>100000:raise ValueError('diagnostic size limit; use a qualified streaming path')
    if len(offsets_ps)!=4 or any(isinstance(x,bool) or not isinstance(x,int) for x in offsets_ps):
        raise ValueError('four integer offsets required')
    integer(full_window_ps,1)
    if isinstance(b_shift_ps,bool) or not isinstance(b_shift_ps,int):raise ValueError('integer shift required')
    ts=[];chs=[]
    for e in events:
        ch=integer(e['channel']);t=integer(e['t_ps'])
        if ch>3 or t>=2**64:raise ValueError('invalid channel/time')
        chs.append(ch);ts.append(t-offsets_ps[ch]+(b_shift_ps if ch>=2 else 0))
    parent=list(range(len(ts)));active=set()
    def find(i):
        while parent[i]!=i:parent[i]=parent[parent[i]];i=parent[i]
        return i
    bs=sorted((ts[i],i) for i,ch in enumerate(chs) if ch>=2);bt=[x[0] for x in bs]
    edge_count=0;half=full_window_ps//2
    for i,ch in enumerate(chs):
        if ch>=2:continue
        lo=bisect.bisect_left(bt,ts[i]-half);hi=bisect.bisect_right(bt,ts[i]+half)
        for _,j in bs[lo:hi]:
            if 2*abs(ts[j]-ts[i])>full_window_ps:continue
            parent[find(j)]=find(i);active.update((i,j));edge_count+=1
            if edge_count>500000:raise ValueError('dense diagnostic; ambiguous-event overload')
    components={}
    for i in active:components.setdefault(find(i),[]).append(i)
    counts={f'{a},{b}':0 for a in (0,1) for b in (2,3)};amb=0
    for comp in components.values():
        aa=[i for i in comp if chs[i]<2];bb=[i for i in comp if chs[i]>=2]
        if len(aa)==len(bb)==1:counts[f'{chs[aa[0]]},{chs[bb[0]]}']+=1
        else:amb+=1
    unique=sum(counts.values());den=unique+amb
    return {'unique_pairs':unique,'ambiguous_components':amb,'output_pairs':counts,
            'ambiguous_fraction':amb/den if den else None,'unmatched_singles':len(ts)-len(active),
            'scope':'DIAGNOSTIC_ONLY_NOT_PRIMARY_CHSH_RELEASE'}

def reference_screen(record, contract, evidence_root):
    """Check provided conservative bounds and locally hashed evidence, fail closed.

    A positive result is a numerical/documentary screen, never an instrument
    certificate. An independent reviewer must decide physical qualification.
    """
    missing=[];failures=[];root=Path(evidence_root).resolve()
    if record.get('contract_id')!=contract['contract_id']:raise ValueError('wrong contract')
    origin=record.get('origin')
    if origin not in {'TEMPLATE','SYNTHETIC','MEASURED'}:raise ValueError('explicit data origin required')
    identity=record.get('identity',{})
    for k in contract['required_identity']:
        if not identity.get(k):missing.append('identity:'+k)
    for k, size in contract.get('identity_array_lengths',{}).items():
        v=identity.get(k)
        if v is None:continue
        if not isinstance(v,list) or len(v)!=size or not all(isinstance(x,str) and x.strip() for x in v):
            raise ValueError('invalid identity vector: '+k)
    if identity.get('channel_map') not in (None,contract['channel_map']):failures.append('channel_map')
    for key,required in contract['required_configuration'].items():
        val=record.get('configuration',{}).get(key)
        if val is None:missing.append('configuration:'+key)
        elif val!=required:failures.append('configuration:'+key)
    bounds=record.get('bounds',{})
    for rule in contract['numeric_rules']:
        vals=bounds.get(rule['key'])
        if vals is None:missing.append(rule['key']);continue
        if not isinstance(vals,list) or len(vals)!=rule['count']:raise ValueError('wrong bound vector: '+rule['key'])
        for i,v in enumerate(vals):
            label=f"{rule['key']}[{i}]"
            if v.get('lower') is None or v.get('upper') is None or not v.get('basis'):
                missing.append(label);continue
            lo=finite(v['lower']);hi=finite(v['upper'])
            if rule.get('type')=='integer':integer(lo);integer(hi)
            if lo>hi:raise ValueError('inverted bounds')
            if 'exclusive_lower' in rule and lo<=rule['exclusive_lower']:failures.append(label+':exclusive_lower')
            if 'lower' in rule and lo<rule['lower']:failures.append(label+':lower')
            if 'upper' in rule and hi>rule['upper']:failures.append(label+':upper')
    evidence=record.get('evidence',[]);valid=set();paths=set()
    for e in evidence:
        rel=Path(e['path']);p=(root/rel).resolve()
        if rel.is_absolute() or '..' in rel.parts or not p.is_relative_to(root):raise ValueError('unsafe evidence path')
        if str(rel) in paths:raise ValueError('duplicate evidence path')
        paths.add(str(rel))
        if not p.is_file():missing.append('file:'+str(rel));continue
        with p.open('rb') as f:
            h=hashlib.sha256()
            for block in iter(lambda:f.read(1024*1024),b''):h.update(block)
        if h.hexdigest()!=e.get('sha256'):failures.append('digest:'+str(rel))
        else:valid.add(str(rel))
    for tid in contract['required_tests']:
        t=record.get('tests',{}).get(tid,{})
        if t.get('review')=='REJECTED':failures.append(tid+':review')
        if not (t.get('review')=='ACCEPTED' and t.get('reviewer') and t.get('evidence')
                and all(x in valid for x in t['evidence'])):missing.append(tid+':review/evidence')
    status='FAIL' if failures else 'HOLD' if missing else 'NUMERICAL_SCREEN_PASS'
    if origin!='MEASURED' and status=='NUMERICAL_SCREEN_PASS':status='SYNTHETIC_ONLY'
    return {'screen_status':status,'origin':origin,'missing':missing,'failures':failures,
            'physical_qualification':('REVIEW_REQUIRED' if status=='NUMERICAL_SCREEN_PASS' else 'NOT_QUALIFIED') if origin=='MEASURED' else 'NOT_RUN',
            'bom_freeze':'HOLD','scope':'REFERENCE_ELECTRICAL_ONLY; NO_PDE_OR_CHSH_RELEASE'}

def design_results():
    return {'origin':'DESIGN_CALCULATION','hardware_status':'NOT_RUN',
       'four_module_supply_max_A':4*1.2,'supply_with_25percent_planning_reserve_A':4*1.2*1.25,
       'loop_resistance_limit_ohm_scenario':(5-.05-.05-4.75)/1.2,
       'threshold_high_margin_min_V':1.5-1.,'threshold_low_margin_min_V':1.-.8,
       'nominal_high_headroom_V':3.-(2.2+.4),'pulse_width_margin_ns':10-.5,
       'raw_cmos_3V3_into_50ohm_current_mA':3.3/50*1000,
       'zero_failures_1M_trials_p99_upper':zero_error_upper(1000000),
       'zero_dark_600s_poisson99_upper_Hz':poisson_upper(0,600),
       'canonical_24byte_4x100kHz_2400s_GB':24*4*100000*2400/1e9,
       'photon_flux_1pW_810nm_Hz':photon_flux(1e-12,810)}

if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('mode',choices=['design','reference','timing','coincidences'])
    parser.add_argument('input',type=Path,nargs='?')
    parser.add_argument('--evidence-root',type=Path,default=Path('.'))
    args=parser.parse_args()
    if args.mode=='design':out=design_results()
    else:
        if args.input is None:parser.error('input JSON required')
        d=json.loads(args.input.read_text())
        if args.mode=='reference':
            contract=json.loads((Path(__file__).parent/'Referenzvertrag.json').read_text())
            out=reference_screen(d,contract,args.evidence_root)
        elif args.mode=='timing':out=timing_groups(d['groups'],d['frozen_offsets_ps'])
        else:out=coincidence_components(d['events'],d['frozen_offsets_ps'])
    print(json.dumps(out,indent=2,allow_nan=False))
