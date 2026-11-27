"""Kontrolliert lokale Radiusintervalle und einen frei spezifizerten Quantenmarker."""
import json
from fractions import Fraction as F
from pathlib import Path
from itertools import pairwise
from eingaben.kugelprobe import endpoint_distance_upper, WINDOW, radius, HYPOTHESES

BASE = Path(__file__).resolve().parent
DATA = BASE / 'eingaben'


def source(file):
    return json.loads((DATA/file).read_bytes())


def marker_probability(weight_a, weight_b):
    # Hypothetische Ereignisauswahl nach relativen klassischen Gewichten.
    (al, ah), (bl, bh) = weight_a, weight_b
    assert al > 0 and bl > 0
    return al / (al + bh), ah / (ah + bl)


def tagged_entropy(p, record_overlap_squared):
    # |Psi> = sqrt(p)|a>|r_a> + sqrt(1-p)|b>|r_b>, <a|b>=0.
    lo, hi = p
    assert 0 <= lo <= hi <= 1 and 0 <= record_overlap_squared <= 1
    def s(x):
        return 2*x*(1-x)*(1-record_overlap_squared)
    samples = [s(lo),s(hi)]
    if lo <= F(1,2) <= hi:
        samples.append(s(F(1,2)))
    return min(samples),max(samples)


def verify_same_record_radius_interval(coords, clocks, weights, center_z, r0, step):
    """Zentrum, Geschwindigkeit, Ortstabelle und Uhrhüllen bleiben fest."""
    assert step > 0
    r_lower, r_upper = r0-step, r0+step
    gaps, radial_parameters = [], []
    for point,(tmin,tmax),(wmin,wmax) in zip(coords,clocks,weights,strict=True):
        d2=sum((v-c)**2 for v,c in zip(point,(0,0,center_z),strict=True))
        lo,hi=radius(r_lower,tmax),radius(r_upper,tmin)
        assert 0 < lo <= hi
        if wmin > 0:
            gaps.append(lo**2-d2)
            radial_parameters.append((d2/hi**2,d2/lo**2))
        else:
            assert wmin==wmax==0
            gaps.append(d2-hi**2)
    assert len(radial_parameters)==19 and len(gaps)==22 and min(gaps)>0
    # Disjunkte radiale Hüllen erlauben auf jeder Kugel ein eigenes glattes
    # mitbewegtes Profil durch alle positiven Stichproben.
    assert all(left[1] < right[0] for left,right in pairwise(sorted(radial_parameters)))
    ray_gaps=[radius(r_lower,t)**2-endpoint_distance_upper(coords,clocks,i,center_z,t)
              for i in (3,4,5) for t in WINDOW]
    assert min(ray_gaps)>0
    return {'r':list(map(str,(r_lower,r_upper))),'center_z':str(center_z),
            'old_squared_clearance_lower':str(min(gaps)),
            'ray_endpoint_squared_clearance_lower':str(min(ray_gaps))}


def main():
    d=source('Vergleichspaar.json')
    pts=[tuple(map(F,p)) for p in source('Ortskoordinaten.json')]
    relation=set(map(tuple,d['relation']))
    assert {(17,18),(20,18)}<=relation
    step=F(1,100000)
    rows={}
    for name in ('heavy','light'):
        case=d[name]
        clocks=[tuple(map(F,v)) for v in case['normalized_clocks']]
        weights=[tuple(map(F,v)) for v in case['weight_box']]
        assert case['positive_in_window']==[18,19] and case['zero_in_window']==[17,20]
        assert all(clocks[i][0]>F(1,2) for i in (17,18,19,20))
        p=marker_probability(weights[18],weights[19])
        rows[name]=dict(p=list(map(str,p)), synthetic_records={},
                        physical_Slin=None, physical_trace_distance=None, physical_Fisher_R=None)
        for overlap in (F(0),F(1,4),F(1)):
            v=tagged_entropy(p,overlap)
            rows[name]['synthetic_records'][str(overlap)]=list(map(str,v))
        rows[name]['identical_kinematic_records']=[
            verify_same_record_radius_interval(pts,clocks,weights,z,r,step) for z,r in HYPOTHESES]
    assert F(rows['heavy']['synthetic_records']['0'][0]) > F(rows['light']['synthetic_records']['0'][1])
    assert all(case['synthetic_records']['1']==['0','0'] for case in rows.values())
    return {'scope':'Die Gewichte sind archiviert. Ereignisauswahl und Hilfsregister sind hypothetisch.',
            'results':rows,'vacuum':{'probability_from_weights':None,'physical_Slin':None,
                                    'separately_postulated_product_state_Slin':'0'},
            'physical_pilot_radii':[None]*8,'physical_P3':{'count':60,'status':'NOT_RUN'}}


if __name__ == '__main__':
    if not __debug__: raise RuntimeError('Ohne -O ausführen.')
    print(json.dumps(main(),indent=2,ensure_ascii=False))
