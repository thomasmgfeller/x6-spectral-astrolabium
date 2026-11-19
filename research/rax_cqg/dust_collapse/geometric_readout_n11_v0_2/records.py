"""Unconditional four-result probabilities with no separate order tag."""
import importlib.util
import numpy as np
from geometry import SRC, read

spec=importlib.util.spec_from_file_location("clock_packets",SRC/"initial_preparation_v0_1/clock_packets.py")
clock=importlib.util.module_from_spec(spec)
spec.loader.exec_module(clock)
TOL=5e-12


def close(x,y):
    np.testing.assert_allclose(x,y,atol=TOL,rtol=0)


def record(q0,q1,cross,eta):
    # The entire interference of the accepted coherent output is in the inconclusive effect.
    accepted=q0+q1+cross
    outcomes={"one_pair":float(eta*q1),"three_pairs":float(eta*q0),
              "inconclusive":float((1-eta)*(q0+q1)+cross),
              "boundary_failure":float(1-accepted)}
    assert min(outcomes.values())>=0
    close(sum(outcomes.values()),1)
    return {**outcomes,"signed_score":outcomes["one_pair"]-outcomes["three_pairs"],
            "accepted":float(accepted),"cross":float(cross)}


def compute_grid(inner,outer,eta):
    params=clock.CONTRACT
    parent=read(SRC/"parent_geometry.json")["fine_grid"]
    parent_clock=read(SRC/"parent_clock.json")
    overlap=read(SRC/"gaussians.json")["overlap_z_equals_integral_conj_psi0_psi1"]
    overlap=complex(float(overlap["re"]),float(overlap["im"]))
    hr,ht=params["density_half_width"],params["clock_lobe_half_width"]
    z,w=clock.quadrature(outer)
    grid=clock.quadrature(inner)
    t0=-2*clock.ward.DELTA
    phases=np.exp(1j*np.array([0,8]))   # F0=10, F1=18; v already includes gravity
    samples={off:[clock.reduced_weight(t0+off+ht*x,inner,grid) for x in z]
             for off in [0,*params["clock_offsets_from_affine_T3"]]}
    result={}
    density_z,density_w=clock.quadrature(12)
    for shape,offsets in (("narrow",[0]),("split",params["clock_offsets_from_affine_T3"])):
        subtotal=hr*(2*ht/3)*len(offsets)
        B,v=zip(*(sample for off in offsets for sample in samples[off]),strict=True)
        B,v=np.asarray(B),np.asarray(v)
        tw=np.tile(w/len(offsets),len(offsets))
        for label,center in zip(("low","high"),params["density_centers"],strict=True):
            if shape=="narrow" and label=="high": continue
            name=shape+"_"+label
            result[name]={}
            for kernel,values in (("coupled",v),("common_C0_dust",v[:,[0]]*phases)):
                incl=tw @ (np.abs(values)**2/4)
                inclusive_cross=float((overlap*(tw @ (values[:,0].conj()*values[:,1]))/2).real)
                avg_phase=np.exp(-0.5j*center*B)*np.sinc(hr*B/(2*np.pi))
                a=np.sqrt(subtotal)/2 * ((tw*avg_phase) @ values)
                phase_grid=np.exp(-0.5j*(center+hr*density_z[:,None])*B)
                close(a,np.sqrt(subtotal)/2 * ((tw*(density_w @ phase_grid)) @ values))
                cross=float(2*(overlap*a[0].conj()*a[1]).real)
                p_inc=record(*incl,inclusive_cross,eta)
                p_const=record(*np.abs(a)**2,cross,eta)
                for p in (p_inc,p_const):
                    if kernel=="common_C0_dust": close(p["signed_score"],0)
                old=parent_clock[shape][kernel]
                close(incl,[old["three_pairs"],old["one_pair"]])
                if shape=="split":
                    ref=parent["runs"][kernel][label]
                    close(np.abs(a)**2,[ref["three_constant"],ref["one_constant"]])
                    if kernel=="coupled": close(p_const["accepted"],parent["scalar_crosscheck"][label]["native_scalar_success"])
                # Directly integrate the squared norm of the coherent superposition.
                gram=np.array([[1,overlap],[overlap.conjugate(),1]])
                close(p_inc["accepted"],tw @ np.einsum("ti,ij,tj->t",values.conj(),gram,values).real/4)
                close(p_const["accepted"],np.vdot(a,gram@a).real)
                result[name][kernel]={"all_modes":p_inc,"constant_mode":p_const}
    for k in result["split_low"]:
        for field,val in result["split_low"][k]["all_modes"].items():
            close(val,result["split_high"][k]["all_modes"][field])
    contrasts={}
    for intervention,first,last in (("density","split_low","split_high"),("clock","narrow_low","split_low")):
        contrasts[intervention]={}
        for mode in ("all_modes","constant_mode"):
            deltas={}
            for kernel in ("coupled","common_C0_dust"):
                deltas[kernel]=result[last][kernel][mode]["signed_score"]-result[first][kernel][mode]["signed_score"]
            deltas["interaction"]=deltas["coupled"]-deltas["common_C0_dust"]
            contrasts[intervention][mode]=deltas
    close(contrasts["clock"]["all_modes"]["coupled"],eta*parent_clock["score_shift_split_minus_narrow"]["coupled"])
    return {"outcomes":result,"contrasts":contrasts}


def numbers(data):
    if isinstance(data,dict):
        for k in sorted(data): yield from numbers(data[k])
    else: yield float(data)


def compute(eta):
    grids=[[32,6],[64,8],[96,12]]
    runs=[compute_grid(i,o,eta) for i,o in grids]
    changes=[max(abs(x-y) for x,y in zip(numbers(a),numbers(b),strict=True)) for a,b in zip(runs,runs[1:])]
    assert max(changes)<TOL
    return {"grids":grids,"adjacent_grid_max_changes":changes,"finest":runs[-1]}
