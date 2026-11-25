"""Recompute the interval proof, geometry controls and blinded shell readouts offline."""
from fractions import Fraction as Q
from hashlib import sha256
from itertools import combinations
from pathlib import Path
import argparse
import json
import sys

ROOT = Path(__file__).resolve().parent
sys.path.insert(0,str(ROOT/'quellen'))
from auslesen import estimate, root_bound, PI
sys.path.insert(0,str(ROOT/'basis'))
from intervall import Box, box, SCALE
from randdichte import construct
from pruefung import I
from geometrie import (R0, POSITIONS, CASES, PAST, FUTURE, shape, sphere, volume,
                       deformation, regularity, conserved_profile)

MID = Q(1,2)
TARGETS = (Q(1,4),MID,Q(3,4))
END = 5*box(5).sqrt_nonnegative_part()/3
PLAN = ROOT/'ergebnisse.json'


def ends(interval):
    return [str(Q(interval.lo,SCALE)), str(Q(interval.hi,SCALE))]


def finite_geometry():
    e=Box.hull(Q(1,6)-Q(1,2**22),Q(1,6)+Q(1,2**22))
    rel,edges,y,w,q=construct(e,True)
    width=(4-e)/64
    y={j:(v+Box(-width.hi,width.hi) if j in I else v) for j,v in y.items()}
    # Every field point is covered at the largest tube width.
    relative={j:(v-y[3])/(4-e) for j,v in y.items()}
    relative[3],relative[7]=box(0),box(1)
    time={j:END*v for j,v in relative.items()}
    for target in TARGETS:
        assert all(v.hi < (target-Q(1,64))*SCALE or v.lo > (target+Q(1,64))*SCALE
                   for v in relative.values())
    pairs=[]
    for i,j in combinations(range(15),2):
        d=abs(POSITIONS[i]-POSITIONS[j])
        if (i,j) in rel or (j,i) in rel:
            a,b=(i,j) if (i,j) in rel else (j,i)
            dt= time[b]-time[a]
            gap=Q(dt.lo,SCALE)-d
            kind='timelike'
        else:
            dt=time[j]-time[i]
            gap=d-Q(max(-dt.lo,dt.hi),SCALE)
            kind='spacelike'
        assert gap>0, (i,j,gap)
        pairs.append({'pair':[i,j],'kind':kind,'margin_lower':str(gap)})
    # Independently project causal cones onto the two null coordinates T ± r.
    recovered=set()
    for a in range(15):
        for b in range(15):
            if a==b: continue
            dtime = END*(y[b]-y[a])/(4-e)
            dr=POSITIONS[b]-POSITIONS[a]
            if (dtime+dr).lo>0 and (dtime-dr).lo>0:
                recovered.add((a,b))
            else:
                assert (dtime+dr).hi<0 or (dtime-dr).hi<0
    assert recovered==rel and len(rel)==99
    assert len(set(POSITIONS))==15 and max(POSITIONS)==POSITIONS[6]==R0
    # One realizable off-centre rational field (inside the packet at fixed e=1/6).
    # Central algebraic field itself is covered by the interval proof above.
    base=box(Q(1,6))
    _,_,yc,wc,_=construct(base,True)
    stamps=[Q(yc[j].lo+yc[j].hi,2*SCALE) for j in range(15)]
    stamps[3]=Q(-11,6)
    weights=[Q(1,8) if j in PAST else Q(1,64) if j in FUTURE
             else Q(wc[j].lo+wc[j].hi,2*SCALE) for j in range(15)]
    assert all(Q(y[j].lo,SCALE)<stamps[j]<Q(y[j].hi,SCALE) for j in I)
    for j in I:
        assert wc[j].hi*Q(99,100)<=weights[j]*SCALE<=wc[j].lo*Q(101,100)
    xs=[(v-stamps[3])/(stamps[7]-stamps[3]) for v in stamps]
    masses={str(target):str(conserved_profile(xs,weights,target)) for target in TARGETS}
    return {'type':1767356,'timelike_pairs':len(rel),'spacelike_pairs':105-len(rel),
            'minimum_pair_margin':str(min(Q(p['margin_lower']) for p in pairs)),
            'pairs':pairs,'normalized_clock_intervals':{j:ends(v) for j,v in relative.items()},
            'closest_early_x_upper':str(max(Q(v.hi,SCALE) for v in relative.values() if v.hi<SCALE/2)),
            'closest_late_x_lower':str(min(Q(v.lo,SCALE) for v in relative.values() if v.lo>SCALE/2)),
            'coordinates':list(map(str,POSITIONS)), 'example_mass_divided_by_4pi_per_pair':masses}


def shell_input(d,n,target=MID):
    halfwidth=R0/n
    delay=box(halfwidth)/END
    # Give each timestamp its full independent 1% light-travel-time uncertainty.
    echo=delay*Box.hull(Q(99,100),Q(101,100))
    data={'reflection_x':str(target),'clock_unit':ends(END),'log_L_drift_per_x':'0',
          'verified_assumptions':True}
    for key,a,b in (('inside',1-Q(1,n),Q(1)),('outside',Q(1),1+Q(1,n))):
        scale=4*R0**3*(volume(d,b)-volume(d,a))
        data[key]={'volume':[str(scale*PI[0]*Q(99,100)),str(scale*PI[1]*Q(101,100))],
                   'emission':ends(box(target)-echo),'reception':ends(box(target)+echo)}
    return data


def run():
    info=finite_geometry()
    accuracy=regularity()
    radii={'A':Q(17,2),'B':Q(99,10)}
    ranges={}
    for case,radius in radii.items():
        d=deformation(case,MID)
        assert radius**2==R0**2*sphere(d,Q(1))
        assert R0**2*sphere(deformation(case,Q(0)),Q(1))==100
        for n in (8,16,32,64,128,256):
            data=shell_input(d,n)
            result=estimate(data)
            lo,hi=map(Q,result['radius'])
            assert lo<=radius<=hi
            # Independent area averages with known static radial scale, before sqrt.
            low=R0**2*n*(volume(d,Q(1))-volume(d,1-Q(1,n)))*Q(99,101)
            high=R0**2*n*(volume(d,1+Q(1,n))-volume(d,Q(1)))*Q(101,99)
            assert 0<=low-lo**2<Q(1,10**8) and 0<=hi**2-high<Q(1,10**8)
            ranges.setdefault(n,{})[case]={'radius_bounds':[str(lo),str(hi)],
                                            'five_percent':lo>=Q(95,100)*radius and hi<=Q(105,100)*radius}
    separate=[n for n,d in ranges.items() if Q(d['A']['radius_bounds'][1])<Q(d['B']['radius_bounds'][0])]
    accurate=[n for n,d in ranges.items() if all(q['five_percent'] for q in d.values())]
    assert min(separate)==16 and min(accurate)==32
    minimax=(radii['B']-radii['A'])/sum(radii.values())
    optimum=2*radii['A']*radii['B']/sum(radii.values())
    assert optimum/radii['A']-1==1-optimum/radii['B']==minimax==Q(7,92)
    extra={}
    for target in TARGETS:
        row={}
        for case in CASES:
            d=deformation(case,target,target)
            r2=R0**2*sphere(d,Q(1))
            truth=root_bound(r2,2)
            data=shell_input(d,32,target)
            observed=tuple(map(Q,estimate(data)['radius']))
            assert Q(95,100)*truth[1]<=observed[0]<=truth[0]<=truth[1]<=observed[1]<=Q(105,100)*truth[0]
            row[case]={'radius_squared':str(r2),'radius_enclosure':list(map(str,truth)),
                       'blind_shell_radius_bounds':list(map(str,observed))}
        a=tuple(map(Q,row['A']['radius_enclosure']))
        b=tuple(map(Q,row['B']['radius_enclosure']))
        gap=(b[0]-a[1])/(b[0]+a[1])
        assert gap>Q(74,1000)
        assert Q(row['A']['blind_shell_radius_bounds'][1])<Q(row['B']['blind_shell_radius_bounds'][0])
        row['minimax_relative_lower']=str(gap)
        extra[str(target)]=row
    records=json.loads((ROOT/'basis/quellen/inputs/checkpoints.json').read_text())
    eligibility=json.loads((ROOT/'quellen/zulassung.json').read_text())
    unique={(r['checkpoint_context']['density_ratio'],r['checkpoint_context']['M'],
             r['checkpoint_context']['x']) for r in records if r['checkpoint_id']=='P3' and r['execution']=='NOT_RUN'}
    assert len(unique)==len(records)==60 and eligibility['decision']=='HOLD_NOT_ELIGIBLE'
    return {'geometry':info,'regularity':accuracy,'independent_target_pairs':extra,'radii':{k:str(v) for k,v in radii.items()},
            'minimax_relative':str(minimax),'minimax_estimate':str(optimum),'shells':ranges,
            'first_disjoint_denominator':min(separate),'first_five_percent_denominator':min(accurate),
            'physical_P3':'HOLD_NOT_ELIGIBLE','physical_NOT_RUN':len(unique)}


def main():
    if not __debug__:
        sys.exit('Der Prüfer benötigt aktivierte Assertions. Bitte ohne -O ausführen.')
    parser=argparse.ArgumentParser()
    parser.add_argument('--erzeugen',action='store_true',help='Ergebnisdateien im Arbeitsordner neu erzeugen')
    generate=parser.parse_args().erzeugen
    if not generate:
        for row in (ROOT/'SHA256SUMS').read_text().splitlines():
            digest,name=row.split('  ',1)
            assert sha256((ROOT/name).read_bytes()).hexdigest()==digest,name
    inputs=json.loads((ROOT/'Herkunft.json').read_text())['bundles'].values()
    for bundle in inputs:
        for path,src in bundle['files'].items():
            assert sha256((ROOT/path).read_bytes()).hexdigest()==src['sha256'],path
    result=run()
    files={PLAN:result}
    for case in CASES:
        files[ROOT/('Schale_'+case+'.json')]=shell_input(deformation(case,MID),32)
    for path,value in files.items():
        serial=json.dumps(value,ensure_ascii=False,indent=2)+'\n'
        if generate:
            path.write_text(serial)
        else:
            assert path.read_text()==serial,path
    print('PASS · 105 Ereignispaare · 3 Uhrzeiten mit je 2 Geometrien · 16 verschiedene Schalenablesungen · 60 physische P3-Punkte NOT_RUN')


if __name__=='__main__':
    main()
