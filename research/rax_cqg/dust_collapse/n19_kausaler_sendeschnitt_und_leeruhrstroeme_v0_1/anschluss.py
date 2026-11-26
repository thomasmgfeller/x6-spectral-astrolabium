"""Necessary first-cut flux for every admissible continuation in the two windows."""
from fractions import Fraction as F


def run():
    from quelle import DATA, box, hull, SCALE
    y,w,order,b,e,windows = DATA
    u,z,h,r = 15,16,17,18
    future = [7,8,9,10]
    rows = {i:[b.get((i,j),0) for j in future] for i in (12,13,h,z)}
    assert all(row == [-9,16,-8,0] for row in rows.values())
    assert not (y[12]-y[13]).contains_zero()
    assert all(not b.get((i,j),0) for i in (12,13) for j in (z,r))
    assert b.get((h,z),0)==0 and b[h,r]==b[z,r]==1
    mz = sum(c*(y[z]-y[i]) for (i,j),c in b.items() if j==z)
    mr = sum(c*(y[r]-y[i]) for (i,j),c in b.items() if j==r)
    assert sum(c for (i,j),c in b.items() if j==z)==0
    assert sum(c for (i,j),c in b.items() if j==r)==1
    assert mz.hi<0 and mr.hi<0
    F0 = sum(c*w[j] for c,j in zip(rows[z],future))
    max_chord = max(4-F(v) for v in e.data())*(windows[1][1]-windows[1][0])
    controls = []
    for source in (-F(1,10**6),F(1,10**6)):
        d = box(source)/(2*mz)
        gap = y[r]-y[z]
        B = mr-d
        C = d*(d-2*gap)
        disc = B*B-C
        assert disc.lo>0 and B.hi<0
        q = C/(-B+disc.sqrt())
        second = -2*B-q
        assert second.lo>max_chord*SCALE
        assert max(abs(F(k)) for k in q.data())<max_chord
        dw_r = -w[r]*q/(y[r]+q-y[h])
        dw_z = (-d*F0 + dw_r*gap + (w[r]+dw_r)*(q-d))/mz
        dflux = (y[z]+d-y[u])*dw_z+w[z]*d
        assert not dflux.contains_zero() and (dflux*source).hi<0
        controls.append({'source_w':str(source),'delta_Yz':d.data(),'delta_Yr':q.data(),
                         'excluded_second_root_delta_Yr':second.data(),'delta_wz':dw_z.data(),
                         'required_delta_G15_inside':dflux.data()})
    assert {(u,z),(h,r)} <= order
    jac = (y[z]-y[u])*(y[r]-y[h])
    assert jac.lo>0
    return {'pure_source_controls':controls,'equal_future_rows':rows[z],
            'max_receiver_window_chord':str(max_chord),'mass_to_two_currents_det':jac.data(),
            'fixed_JY':'0','e':e.data()}


if __name__ == '__main__':
    import json
    from vorstudie import inputs
    with inputs():
        print(json.dumps(run(),indent=2,sort_keys=True))
