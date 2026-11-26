"""Current, calibration and shell/radar readout, kept separate by data source."""
from fractions import Fraction as F
import gzip
import json
from math import isqrt

from basis import klassik
from basis.auslesen import estimate
from felder import (COLLAR, INNER, PAST, FUTURE, U, Z, ROOT, OLD, SCALE,
                    Equations, filters, Box, box, serial)

BASIS = ROOT/'basis'


def archived(name):
    p = BASIS/name
    return json.loads(gzip.decompress(p.read_bytes()) if p.suffix == '.gz' else p.read_bytes())


def bounded(interval):
    lo, hi=interval
    assert 0 < lo <= hi
    return {'interval':list(map(str,interval)), 'minimax_estimate':str(2*lo*hi/(hi+lo)),
            'relative_bound':str((hi-lo)/(hi+lo))}


def stationary_current():
    eq=Equations(COLLAR,COLLAR,'shift')
    e=F(1,6)
    x0=F(11,23)
    _,_,branches=eq.cell((e,e),(x0,x0),keep=True)
    assert len(branches)==1
    y,w,gu=branches[0]
    assert all(y[i].hi<y[j].lo for i,j in eq.rel)
    assert all(0<w[j].lo<=w[j].hi<SCALE for j in (*INNER,Z))
    assert gu.lo<=0<=gu.hi and y[Z].lo<=0<=y[Z].hi
    assert y[U].intersection(-box(6).sqrt_nonnegative_part())
    assert w[Z].intersection((3+box(6).sqrt_nonnegative_part())/192)
    cuts={}
    common=None
    ideals=[]
    for x in (F(47,100),F(49,100)):
        t=e-2+(4-e)*x
        past={i for i in y if F(y[i].hi,SCALE)<t}
        assert all((i in past or F(value.lo,SCALE)>t) for i,value in y.items())
        ideals.append(past)
        # Report explicitly the negative-oriented cut flux. This is a dimensionless
        # action-current convention and has no assigned rest-mass scale.
        q=-sum((b*w[j]*(y[j]-y[i]) for i in past for j,b in eq.outgoing[i] if j not in past),box(0))
        common=q if common is None else common.intersection(q)
        assert common is not None and common.lo>0
        cuts[str(x)]={'old_and_new_past':sorted(past),'charge':serial(q)}
    assert ideals[1]-ideals[0]=={Z} and ideals[0]<ideals[1]
    coefficients=set()
    for u,z in filters():
        graph=Equations(u,z,'shift')
        outgoing=graph.outgoing[14]
        assert [i for i,b in outgoing]==list(FUTURE)
        coeffs=tuple(b for _,b in outgoing)
        assert sum(coeffs)==0
        constant=sum(F(b*(j-5),64) for j,b in outgoing)
        assert constant==-F(1,64)
        coefficients.add(coeffs)
    assert coefficients=={(1,-9,16,-8)}
    return {'stationary_x':'11/23','e':'1/6','cuts':cuts,'common_charge':serial(common),
            'empty_interior_G14_all_193':'-1/64'}


def mass_transfer():
    # Only the vacuum and the one positive standard may enter the gain.
    vacuum=klassik.charge_interval(klassik.prepare_charge_samples(F(0)))
    ref=klassik.exterior_standard(F(1,4))
    qlo,qhi=klassik.charge_interval(klassik.prepare_charge_samples(F(1,4)))
    assert vacuum==(0,0) and qlo>0
    gain=(ref/qhi,ref/qlo)
    inferred={}
    for m in (F(1),F(4)):
        q=klassik.charge_interval(klassik.prepare_charge_samples(m))
        output=(q[0]*gain[0],q[1]*gain[1])
        target=klassik.exterior_standard(m)
        assert output[0]<=target<=output[1]
        inferred[str(m)]=list(map(str,output))
    old=archived('massentest.json')['physical']
    ledger=archived('checkpoints.json.gz')
    assert len(ledger)==60 and all(row['execution']=='NOT_RUN' for row in ledger)
    assert sum(row['checkpoint_context']['x']=='0' for row in ledger)==old['initial_cut_records']==12
    assert all(old[k] is None for k in ('physical_vacuum_reading','independent_physical_calibration_pair','physical_gain'))
    return {'classical_reference':str(ref),'classical_vacuum':list(map(str,vacuum)),
            'classical_gain':list(map(str,gain)),'classical_transfers':inferred,
            'physical_vacuum':None,'physical_reference':None,'physical_gain':None,
            'physical_M1':'NOT_RUN','physical_register_rows':len(ledger)}


def tracer_positions(frame):
    positions=frame['positions']
    faces=frame['faces']
    assert len(faces)==3
    result=[]
    for face in faces:
        assert all(v is None or abs(v-face)>2 for v in positions)
        result.append([v is not None and v<face for v in positions])
    return result


def surfaces():
    sh=archived('Schalen_und_Tracer.json.gz')
    echoes=archived('Schaetzungen.json')
    # The published labels just align histories; never select by how close radii are.
    cases={m:v['id'] for m,v in archived('Bewertung.json').items()}
    last={}
    rows=[]
    transfer=[]
    intersected={}
    assert len(sh)==15 and len({(v['case'],v['x']) for v in sh})==15
    for frame in sh:
        case=frame['case']; x=F(frame['x']); m=F(case)
        bounds=tuple(map(F,estimate(frame['reading'])['radius']))
        assert sum(frame['occupied']) and frame['marks']==[492,493]
        got=tracer_positions(frame['tracer'])
        weights=list(map(F,frame['tracer']['weights']))
        assert all(len(b)==len(weights) for b in got)
        if case in last:
            old_x,previous,old_weights=last[case]
            assert x-old_x==F(1,4) and old_weights==weights
            faces=[]
            for p,n in zip(previous,got,strict=True):
                entered=sum((w for w,b,c in zip(weights,p,n,strict=True) if not b and c),F(0))
                exited=sum((w for w,b,c in zip(weights,p,n,strict=True) if b and not c),F(0))
                faces.append([entered,exited])
            assert faces[0]==faces[1]==[0,0] and faces[2][0]>0 and faces[2][1]==0
            transfer.append({'mass':case,'x':str(x),'entered_fixed_R6':str(faces[2][0]),
                             'exited_fixed_R6':'0','inner_and_outer':[['0','0'],['0','0']]})
        last[case]=(x,got,weights)
        rows.append({'mass':case,'x':str(x),'shell':bounded(bounds)})
        if x==F(1,2):
            echo_record=echoes[cases[case]]['all_early']['support']
            echo=(F(echo_record['lower']),F(echo_record['upper']))
            common=(max(echo[0],bounds[0]),min(echo[1],bounds[1]))
            intersected[case]={'case':cases[case],'echo':bounded(echo),'shell':bounded(bounds),'joint':bounded(common)}
        # Separate analytical check of the classical support without numerical ODEs.
        sqrt_m=F(isqrt(m.numerator),isqrt(m.denominator))
        assert sqrt_m**2==m
        true_cube=1000*(1-x*sqrt_m/4)**2
        assert bounds[0]**3<=true_cube<=bounds[1]**3
        if x==F(1,2): assert common[0]**3<=true_cube<=common[1]**3
    assert len(transfer)==12 and len(intersected)==3
    return {'radii':rows,'flux':transfer,'paired_midpoint':intersected,
            'physical_surface':'MISSING_EXPOSURE'}


def run():
    return {'N17_current':stationary_current(),'masses':mass_transfer(),'shell_readout':surfaces()}


if __name__=='__main__':
    print(json.dumps(run(),indent=2,sort_keys=True))
