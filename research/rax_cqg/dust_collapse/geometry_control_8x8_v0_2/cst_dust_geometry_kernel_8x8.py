#!/usr/bin/env python3
"""Formal geometry/spectator control. No physical clock, Gram or matter kernel."""
from __future__ import annotations
import argparse
import cmath
import hashlib
import io
import json
import math
from pathlib import Path
import sys
import zipfile
import numpy as np

ROOT = Path(__file__).resolve().parent
VERSION = '0.2'
SOURCE_SHA256 = '326c4e016b37154298ea875aa4dfb1828051805a4734a2be925d05e32ce53904'
PERMUTATION = np.array([0, 1, 4, 5, 2, 3, 6, 7], dtype=np.int64)
ORIGINAL_BASIS = [f'{geo}|{sector}|{matter}m' for geo in ('A','K') for sector in ('0','+') for matter in (0,1)]
BASIS = [ORIGINAL_BASIS[i] for i in PERMUTATION]
STRATUM = np.array([0,0,0,0,1,1,1,1], dtype=np.int64)
GEOMETRY = np.array([0,0,1,1,0,0,1,1], dtype=np.int64)
MATTER = np.array([0,1,0,1,0,1,0,1], dtype=np.int64)
PHASES = {'1': 1+0j, '-1': -1+0j, 'i': 1j}
EXPECTED = {'1': [[35,26],[26,20]], '-1': [[3,0],[0,-4]], 'i': [[-13,5-11j],[5-11j,2+8j]]}

class FixtureError(ValueError):
    pass

def require(condition, message):
    if not condition:
        raise FixtureError(message)

def canonical(data):
    return json.dumps(data, ensure_ascii=False, sort_keys=True, indent=2, allow_nan=False)+'\n'

def source_terms():
    data=(ROOT/'inputs/gluing_kernels_2_plus_2.json').read_bytes()
    require(hashlib.sha256(data).hexdigest()==SOURCE_SHA256, 'Polynomial source hash mismatch')
    rows=json.loads(data)['kernels']
    order=[('antichain','antichain'),('antichain','chain'),('chain','chain')]
    return [{x['power']:int(x['coefficient']) for x in next(r for r in rows if (r['A'],r['B'])==pair)['kernel']} for pair in order]

def validate_z(z):
    z=complex(z)
    require(math.isfinite(z.real) and math.isfinite(z.imag), 'z must be finite')
    require(z!=0, 'z must be nonzero (Laurent polynomial)')
    return z

def exact_readout(terms, phase):
    """Gaussian-integer arithmetic at 1,-1,i; no floating power evaluation."""
    result=[0,0]
    for exponent, coefficient in terms.items():
        if phase=='1': real,imag=1,0
        elif phase=='-1': real,imag=(1 if exponent%2==0 else -1),0
        else: real,imag=((1,0),(0,1),(-1,0),(0,-1))[exponent%4]
        result[0]+=coefficient*real;result[1]+=coefficient*imag
    return result

def kernels(z, terms=None):
    z=validate_z(z);terms=source_terms() if terms is None else terms
    phase=next((name for name,value in PHASES.items() if z==value),None)
    try:
        if phase:
            values=[complex(*exact_readout(t,phase)) for t in terms]
        else:
            values=[sum(c*z**p for p,c in t.items()) for t in terms]
    except (OverflowError, ZeroDivisionError) as exc:
        raise FixtureError('Laurent evaluation overflow/underflow') from exc
    result=np.array([[values[0],values[1]],[values[1],values[2]]],dtype=np.complex128)
    require(np.isfinite(result).all(), 'Laurent evaluation is not finite')
    return result

def build8(z):
    kg=kernels(z)
    original=np.kron(kg,np.eye(4,dtype=np.complex128))
    return kg,original[np.ix_(PERMUTATION,PERMUTATION)]

def source_controls():
    outcomes={}
    for phase,z in PHASES.items():
        passed=np.array_equal(kernels(z),np.array(EXPECTED[phase],dtype=np.complex128))
        require(passed, 'Source control failed at z='+phase)
        outcomes[phase]='PASS_EXACT_GAUSSIAN_INTEGER_EVALUATION'
    return outcomes

def diagnostics(kg,k):
    require(kg.shape==(2,2) and k.shape==(8,8),'Wrong matrix shape')
    require(np.isfinite(kg).all() and np.isfinite(k).all(),'Nonfinite matrix')
    stratum_mask=STRATUM[:,None]!=STRATUM[None,:]
    matter_mask=MATTER[:,None]!=MATTER[None,:]
    with np.errstate(over='raise',invalid='raise',divide='raise'):
        try:
            defect=k.conj().T@k-np.eye(8)
            expected=np.kron(np.eye(2),np.kron(kg,np.eye(2)))
            values={
                'tensor_residual_fro':float(np.linalg.norm(k-expected)),
                'stratum_mixing_fro':float(np.linalg.norm(k[stratum_mask])),
                'matter_mixing_fro':float(np.linalg.norm(k[matter_mask])),
                'either_label_mixing_fro':float(np.linalg.norm(k[stratum_mask|matter_mask])),
                'unitarity_defect_diagnostic_I8_fro':float(np.linalg.norm(defect)),
            }
        except FloatingPointError as exc:
            raise FixtureError('Diagnostic overflow/invalid arithmetic') from exc
    require(all(math.isfinite(x) for x in values.values()),'Nonfinite diagnostic')
    return values,defect

def validate_fixture(kg,k):
    values,defect=diagnostics(kg,k)
    # Exact array comparison is intentional: this is a permutation/tensor fixture,
    # not an approximate physical kernel or numerical integration result.
    expected=np.kron(np.eye(2),np.kron(kg,np.eye(2)))
    require(np.array_equal(k,expected),'Tensor/permutation control failed')
    require(values['stratum_mixing_fro']==0 and values['matter_mixing_fro']==0,'Spectator labels mix')
    require(np.array_equal(kg,kg.T),'Geometric transpose-symmetry control failed')
    return values,defect

def cmul(a,b):
    return [a[0]*b[0]-a[1]*b[1],a[0]*b[1]+a[1]*b[0]]

def exact_phase_data(phase):
    a,b,c=[exact_readout(t,phase) for t in source_terms()]
    ac=cmul(a,c);bb=cmul(b,b);det=[ac[0]-bb[0],ac[1]-bb[1]]
    matrix=[[a,b],[b,c]]
    gram=[]
    for i in range(2):
        row=[]
        for j in range(2):
            entries=[cmul([matrix[r][i][0],-matrix[r][i][1]],matrix[r][j]) for r in range(2)]
            row.append([sum(x[0] for x in entries)-int(i==j),sum(x[1] for x in entries)])
        gram.append(row)
    return {'arithmetic':'Gaussian integers','K_geom':matrix,'det_K_geom':det,
            'det_K_geom_abs_squared':sum(x*x for x in det),'defect_geom_I2':gram,
            'defect_8x8_I8_fro_squared':4*sum(x*x for row in gram for pair in row for x in pair)}

def npz_bytes(arrays):
    """Fixed metadata and uncompressed NPY members: deterministic, pickle-free."""
    buffer=io.BytesIO()
    with zipfile.ZipFile(buffer,'w',compression=zipfile.ZIP_STORED) as archive:
        for name,value in sorted(arrays.items()):
            item=io.BytesIO();np.save(item,np.asarray(value),allow_pickle=False)
            info=zipfile.ZipInfo(name+'.npy',(2026,11,11,0,0,0));info.create_system=3;info.external_attr=0o100644<<16
            archive.writestr(info,item.getvalue())
    return buffer.getvalue()

def create_dataset(z,output,invocation=None):
    z=validate_z(z);output=Path(output)
    require(output.suffix=='.npz','Output must have suffix .npz')
    controls=source_controls();kg,k=build8(z);values,defect=validate_fixture(kg,k)
    phase=next((name for name,value in PHASES.items() if z==value),None)
    exact=exact_phase_data(phase) if phase else None
    if exact:
        values['unitarity_defect_diagnostic_I8_fro']=math.sqrt(exact['defect_8x8_I8_fro_squared'])
    arrays={'z':np.array(z),'K_geom':kg,'K':k,'basis':np.array(BASIS),
            'n_channels':np.array(2),'states_per_channel':np.array(4),'n_geometry_states':np.array(2),'n_matter_labels':np.array(2),
            'basis_layout':np.array('stratum_geometry_matter'),'original_to_output_indices':PERMUTATION,
            'stratum_index':STRATUM,'geometry_index':GEOMETRY,'matter_index':MATTER,
            'role':np.array('GEOMETRY_SPECTATOR_CONTROL'),
            'diagnostic_operator_convention':np.array('coefficient_map'),
            'G_in_diagnostic':np.eye(8),'G_out_diagnostic':np.eye(8),'defect_diagnostic_I8':defect}
    blob=npz_bytes(arrays);provenance=json.loads((ROOT/'provenance.json').read_text())
    report={'version':VERSION,'dataset_role':'GEOMETRY_SPECTATOR_CONTROL','physical_kernel':False,
            'z':{'real':z.real,'imag':z.imag},'invocation':invocation,'phase_exact':phase,
            'basis':BASIS,'basis_layout':'stratum_geometry_matter','original_basis':ORIGINAL_BASIS,
            'original_to_output_indices':PERMUTATION.tolist(),'n_channels':2,'states_per_channel':4,
            'n_geometry_states':2,'n_matter_labels':2,'source_controls':controls,
            'K_geom':[[[x.real,x.imag] for x in row] for row in kg], 'exact_source_phase_data':exact,
            'diagnostics':values,'diagnostic_operator_convention':'coefficient_map',
            'diagnostic_gram_origin':'chosen orthonormal formal test basis; not an orbit-derived physical product',
            'identity_on_extra_labels':'explicit additional test assumption, not determined by gravitational polynomials',
            'physical_kernel_convention':None,'physical_gram':None,'physical_clock':None,'delta_chi':None,
            'physical_8x8_matter_matrix':'NOT_CONSTRUCTED','physical_K_0plus':'NOT_COMPUTED',
            'physical_gates':{x:'HOLD' for x in ['MODEL','CURRENT','CORRESPONDENCE','BOUNCE','REGULARITY','BOUNDARY','TRAPPING','EXTENSION']},
            'source_commit':provenance['base_commit'],'source_sha256':SOURCE_SHA256,
            'generator_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
            'npz_sha256':hashlib.sha256(blob).hexdigest(),
            'floating_point_policy':'complex128 for general z; exact Gaussian-integer controls at 1,-1,i; no physical tolerance inferred'}
    text=canonical(report) # strict JSON validation happens before any output is written
    output.parent.mkdir(parents=True,exist_ok=True)
    output.write_bytes(blob);output.with_suffix('.json').write_text(text,encoding='utf-8')
    return report

def main(argv=None):
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--phase',choices=list(PHASES))
    parser.add_argument('--kappa',type=float,help='numerical z=exp(i*kappa); not a physical clock')
    parser.add_argument('--z-real',type=float)
    parser.add_argument('--z-imag',type=float)
    parser.add_argument('--output',default='cst_dust_geometry_kernel_8x8_z1.npz')
    args=parser.parse_args(argv)
    custom=args.z_real is not None or args.z_imag is not None
    if sum([args.phase is not None,args.kappa is not None,custom])>1:parser.error('Choose only one of --phase, --kappa or --z-real/--z-imag')
    try:
        if args.kappa is not None:
            require(math.isfinite(args.kappa),'kappa must be finite');z=cmath.exp(1j*args.kappa);mode={'kappa':args.kappa}
        elif custom:
            z=complex(1 if args.z_real is None else args.z_real,0 if args.z_imag is None else args.z_imag);mode={'z_real':z.real,'z_imag':z.imag}
        else:
            phase=args.phase or '1';z=PHASES[phase];mode={'phase':phase}
        result=create_dataset(z,args.output,mode)
    except (FixtureError,OverflowError,FloatingPointError) as exc:
        print('ERROR: '+str(exc),file=sys.stderr);return 2
    print(f"PASS: source and structure controls; {args.output}; physical gates HOLD")
    return 0

if __name__=='__main__':sys.exit(main())
