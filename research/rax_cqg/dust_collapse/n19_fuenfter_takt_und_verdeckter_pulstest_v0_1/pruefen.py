"""Replay the staged N19 test using only Python's standard library."""
import argparse
import hashlib
import json
from itertools import product
import subprocess
import sys

from n19_pr395 import ROOT, instrument
from folgetakt import advance, center_radius, classify, projection
from modell import generate, read


def raw(doc):
    return (json.dumps(doc,ensure_ascii=False,indent=2,sort_keys=True)+'\n').encode()


def digest(doc):
    return hashlib.sha256(json.dumps(doc,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode()).hexdigest()


def expect_error(f,*args):
    try:
        f(*args)
    except ValueError:
        return
    raise AssertionError('expected rejection')


def brute(bands,c):
    by_w = {}
    for x,y,z in product(*(range(lo,hi+1) for lo,hi in bands)):
        if abs(z-2*y+x)>c:
            continue
        for w in range(2*z-y-c,2*z-y+c+1):
            for v in range(2*w-z-c,2*w-z+c+1):
                by_w.setdefault(w,{}).setdefault(v,[x,y,z,w,v])
    return by_w


def grid_test():
    from referenzprotokoll import next_envelope
    bands = [(lo,lo+d) for lo in range(-2,2) for d in range(3)]
    count=empty=holes=0
    for comb in product(bands,repeat=3):
        for c in range(3):
            count+=1
            exact=brute(comb,c)
            if not exact:
                empty+=1
                expect_error(next_envelope,comb,c)
                continue
            bounds=next_envelope(comb,c)
            assert bounds==(min(exact),max(exact))
            got=projection(comb,c,bounds)
            assert got=={w:(min(vals),max(vals)) for w,vals in exact.items()}
            holes+=len(exact)<bounds[1]-bounds[0]+1
    case=[[-2,-2],[-2,-1],[-2,0]]
    gap=projection(case,0,next_envelope(case,0))
    assert sorted(gap)==[-2,1]
    return {'cases':count,'empty':empty,'fourth_hulls_with_holes':holes,
            'gap_example':{'bands':case,'C':0,'possible_fourth':sorted(gap)}}


def verify_opening(decisions, opening, binding):
    if digest(opening)!=binding['sha256']:
        raise ValueError('opening disagrees with commitment')
    sources=opening['sources']
    if set(sources)!=set(decisions) or sorted(sources.values())!=['-1/1000000','0','1/1000000']:
        raise ValueError('invalid opening')
    return {s:{'opened':sources[s],'read':d['source_label'],'correct':sources[s]==d['source_label']}
            for s,d in decisions.items()}


def study(docs,model,decisions,opening,binding):
    from referenzprotokoll import forecast
    c=docs['Kontrollen']
    h=docs['Vierte_Null']
    old=forecast(c)
    exam=docs['A_Referenz']
    ref=exam['reference']
    zero_error=advance(c,{**h,'extra_error_codes':0},'Puls-A')['reference']
    bands=[(t['code']-t['extra_error_codes'],t['code']+t['extra_error_codes']) for t in c['controls']]
    truth=brute(bands,c['curvature_codes'])
    cases={}
    for key,w_set,interval in [
        ('unseen_fourth',list(truth),exam['fifth_before_holdout']),
        ('fourth_error_one',range(h['code']-1,h['code']+2),ref['range_codes']),
        ('fourth_exact',[h['code']],zero_error['range_codes'])]:
        possible={i:path for w in w_set for i,path in truth[w].items()}
        lo,hi=min(possible),max(possible)
        assert [lo,hi]==interval
        center,radius=center_radius(interval)
        cases[key]={'interval':[lo,hi],'B':center,'radius':radius,'budget':ref['allowed_error_codes'],
                    'min_witness':possible[lo],'max_witness':possible[hi]}
    assert cases['unseen_fourth']['radius']>ref['allowed_error_codes']
    assert cases['fourth_error_one']['radius']<=ref['allowed_error_codes']
    fifth=model['ticks']['11']
    assert all(v['plateau_budget']>=ref['allowed_error_codes'] for v in fifth['source_intervals'].values())
    assert ref['range_codes'][0]<=fifth['loaded_null'][0]<=fifth['loaded_null'][1]<=ref['range_codes'][1]
    j,k=model['precursor_comparison']
    assert j['intersection'] and j['time_only_label']=='0'
    assert k['intersection'] is None and k['time_only_label']!='0'
    assert j['guarded_label']=='0' and k['guarded_label'] is None and k['guarded_status']=='DISJOINT_REFERENCES'
    scores=verify_opening(decisions,opening,binding)
    assert all(v['correct'] for v in scores.values())
    # Check bit, timing, control and opening failures separately.
    pkt=docs['A_received']
    expect_error(classify,ref,docs['A_receiver'],docs['A_memory'],{**pkt,'bit':1-pkt['bit']})
    expect_error(classify,ref,docs['A_receiver'],docs['A_memory'],docs['B_received'])
    expect_error(advance,c,{**h,'index':11},'Puls-A')
    expect_error(advance,c,{**h,'source_setting':'positive'},'Puls-A')
    expect_error(advance,c,{**h,'reference_id':'other'},'Puls-A')
    expect_error(verify_opening,decisions,{**opening,'nonce':opening['nonce']+'0'},binding)
    low=old['range_codes'][0]
    assert advance(c,{**h,'code':low},'X')['status']=='PARTIAL_HOLDOUT'
    assert advance(c,{**h,'code':low-2},'X')['status']=='INCOMPATIBLE_HOLDOUT'
    no_data=advance({'kind':'no_observations','controls':[]},{},'X')
    assert no_data['status']=='NOT_MEASURED'
    assert all(len(v['min_witness'])==5 and len(v['max_witness'])==5 for v in cases.values())
    return {'kind':'synthetic','old_fourth_reference':old['baseline_code'],
            'minimum_fifth_radii':cases,'blind_comparison':scores,'integer_validation':grid_test(),
            'negative_controls':['flipped_bit','swapped_packet','wrong_tick','source_on_control',
                                 'wrong_reference','wrong_opening','partial_holdout','incompatible_holdout'],
            'empty_physical_input':no_data,'physical_observations':0,'physical_P3':'60 NOT_RUN'}


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--mit-vorgaenger',action='store_true',help='also replay the expensive historical calculation')
    args=p.parse_args()
    if not __debug__:
        raise SystemExit('Python ohne -O starten.')
    data=ROOT/'daten'
    for manifest in ('SHA256SUMS','Pruefplan.sha256'):
        for line in (ROOT/manifest).read_text().splitlines():
            value,name=line.split('  ',1)
            assert hashlib.sha256((ROOT/name).read_bytes()).hexdigest()==value,name
    with instrument() as parent:
        if args.mit_vorgaenger:
            subprocess.run([sys.executable,'-B','pruefen.py'],cwd=parent,check=True)
        from n19_archiv394 import inputs
        binding=read(data,'Bindung')
        # The classification step sees only the public reference and readout files.
        decisions={}
        for slot in ('A','B','C'):
            doc=read(data,slot+'_Referenz')
            decisions[slot]=classify(doc['reference'],*(read(data,slot+'_'+k) for k in ('receiver','memory','received')))
        assert raw(decisions)==(data/'Entscheidungen.json').read_bytes()
        opening=read(data,'Oeffnung')
        verify_opening(decisions,opening,binding)
        with inputs() as (_,previous,early):
            docs,model=generate(parent,previous,early,opening)
            report=study(docs,model,decisions,opening,binding)
        for name,doc in {**docs,'Modellkontrolle':model,'Ergebnisse':report}.items():
            assert (data/(name+'.json')).read_bytes()==raw(doc),name
    print('PASS — fünfter Takt, exakte Grenzen, Blindvergleich, Negativkontrollen und Driftgegenprobe.')
    print('Physische Nullmessungen: 0. P3: 60 NOT_RUN.')


if __name__=='__main__':
    main()
