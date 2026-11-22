"""Exploratory transfer of the dust-amplitude bound across the predetermined intersection."""
from fractions import Fraction as Q
from itertools import product
from hashlib import sha256
import json
import massenquelle as s


def model_bound(code):
    _,order=s.support.geometry(code)
    paths,centers,radius,width,low,high=s.tube.template(code)
    assert width==s.ETA and (1+width)*4*(4*s.support.DELTA[1]+Q(3,32))*max(high)<1
    profile={'clock_center':{str(j):str(centers[j]) for j in s.I},'clock_halfwidth':str(radius),
             'dwell_affine_ranges_per_vertex':{str(j):(str(a),str(b)) for j,a,b in zip(s.I,low,high)}}
    out={}
    for mass,rho in product(s.support.MASSES,(Q(1,8),Q(1,4))):
        phases=[]
        for a,b in s.support.WINDOWS:
            step=(b-a)/8
            for i in range(8):
                phases.append(s.coherence.phase_box(order, (a+i*step,a+(i+1)*step),rho,mass,profile))
        lo=min(p[0] for p in phases); hi=max(p[1] for p in phases)
        floor=max(Q(0),1-(hi-lo)**2/8)
        perturbation=s.G*mass*s.ETA/2
        relative=s.ETA/(floor-perturbation) if floor>perturbation else None
        good=relative is not None and relative<=Q(1,50) and s.G*mass*(1+relative)<3
        out[str(mass)+';'+str(rho)]={'phase_floor':str(floor),'status':'PASS' if good else 'UNRESOLVED',
                                     'error_bound':None if relative is None else str(relative)}
    return out


def run():
    assert sha256((s.ROOT/'katalogplan.txt').read_bytes()).hexdigest()==(s.ROOT/'katalogplan.sha256').read_text().split()[0]
    census=s.json_value('basis/synchronisiert/census.json')['by_type']
    chosen=[]
    for code in s.support.catalogue():
        _,r=s.support.geometry(code)
        if census[str(code)]['full_box'] and all(sum((v,j) in r for v in s.I)<4 for j in s.I):
            chosen.append(code)
    assert len(chosen)==61 and 2324 in chosen
    rows={str(code):model_bound(code) for code in chosen}
    reference=s.json_value('basis/synchronisiert/coherence.json')['rows']
    assert all(row['phase_floor']==reference[key]['conditional_modulus_lower_exact'] for key,row in rows['2324'].items())
    by_mass={str(m):sum(all(rows[str(c)][str(m)+';'+str(rho)]['status']=='PASS'
                                for rho in (Q(1,8),Q(1,4))) for c in chosen) for m in s.support.MASSES}
    all_pass=[c for c in chosen if all(v['status']=='PASS' for v in rows[str(c)].values())]
    return {'scope':'auxiliary positive dust measure on each fixed type; same nonzero scalar channel understood',
            'eligible_types':len(rows),'full_pass_types':all_pass,'pass_types_by_mass_both_densities':by_mass,
            'individual_pass':sum(v['status']=='PASS' for r in rows.values() for v in r.values()),
            'evaluation_rows':rows}


if __name__=='__main__':
    if not __debug__: raise RuntimeError('Run without -O')
    print(json.dumps(run(),indent=2,sort_keys=True))
