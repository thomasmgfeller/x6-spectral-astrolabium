"""Verify the supplied defect and corrected port against frozen native JS evidence."""
from datetime import datetime, timezone
import gzip
import hashlib
import json
import math
from pathlib import Path
import platform
import struct
import sys

from port import RNG, MissingXorRNG, cloud, imul, normal, urshift, MASK

ROOT = Path(__file__).resolve().parent
OUT = Path(sys.argv[1]).resolve() if len(sys.argv)>1 else ROOT/'results'
protocol = json.loads((ROOT/'protocol.json').read_text())
native = json.loads(gzip.decompress((OUT/'native_reference.json.gz').read_bytes()))
supplied = json.loads((ROOT/'supplied_vectors.json').read_text())
sha = lambda b: hashlib.sha256(b).hexdigest()
assert native['source_sha256'] == sha((ROOT/'source/core.js').read_bytes())
assert native['test_sha256'] == sha((ROOT/'native_reference.cjs').read_bytes())
assert native['protocol_sha256'] == sha((ROOT/'protocol.json').read_bytes())
old_counts = {2:[4073,4125,4158,4146],3:[2032,2041,2011,2077],4:[973,1065,1033,1029]}
atol = protocol['float_tolerance']['absolute']
rtol = protocol['float_tolerance']['relative']

def floats(values, reference):
    pairs=list(zip(values,reference,strict=True))
    errors=[abs(a-b) for a,b in pairs]
    return {'values':len(pairs), 'max_absolute_error':max(errors,default=0),
        'different_binary64':sum(struct.pack('>d',a)!=struct.pack('>d',b) for a,b in pairs),
        'tolerance_failures':sum(not (math.isfinite(a) and math.isfinite(b) and abs(a-b)<=atol+rtol*abs(b)) for a,b in pairs)}

vector_results=[]
normal_results=[]
for stream in native['streams']:
    seed=stream['seed'];old=MissingXorRNG(seed);fixed=RNG(seed)
    old_values=[old() for _ in range(10)]
    assert old_values==supplied[str(seed)]
    actual=[fixed() for _ in range(protocol['prng_values_per_seed'])]
    mismatches=sum(a!=b for a,b in zip(actual,stream['uniforms'],strict=True))
    vector_results.append({'seed':seed,'old_values_reproduced':10,'corrected_values_checked':len(actual),
        'corrected_mismatches':mismatches,'first_ten_corrected':actual[:10]})
    fixed=RNG(seed)
    normal_results.append({'seed':seed,**floats([normal(fixed) for _ in range(protocol['normal_values_per_seed'])],stream['normals'])})

cloud_results=[]
corrected_raw=[]
for row in native['clouds']:
    p=row['parameters']
    old_pts,old_inside=cloud(**p,rng_type=MissingXorRNG)
    expected_old=old_counts[p['d']][protocol['seeds'].index(p['seed'])]
    assert sum(old_inside)==expected_old
    pts,inside=cloud(**p)
    comparison=floats((x for point in pts for x in point),(x for point in row['points'] for x in point))
    flags=sum(a!=b for a,b in zip(inside,row['inside'],strict=True))
    corrected_raw.append({'parameters':p,'points':pts,'inside':inside})
    cloud_results.append({**p,'old_count':sum(old_inside),'old_report_count_reproduced':True,
        'corrected_count':sum(inside),'native_count':row['k'],'inside_mismatches':flags,**comparison})

fixture_results={}
for name,rng_type in [('missing_xor',MissingXorRNG),('corrected',RNG)]:
    pts,inside=cloud(64,4,.5,20261017,rng_type=rng_type)
    payload=json.dumps({'points':pts,'inside':inside},separators=(',',':'),allow_nan=False).encode('utf-8')
    (OUT/(name+'_python_fixture.json')).write_bytes(payload)
    fixture_results[name]={'sha256':sha(payload),'bytes':len(payload)}
assert fixture_results['missing_xor']['sha256']=='f1869f9749d3f1f2c8f6c2e9e677a1e657177a6f169dcdf2213ec4e543348781'
fixture_results['native_points_inside_only']=native['fixture']['sha256']
fixture_results['corrected_vs_native_bytes_equal']=(OUT/'corrected_python_fixture.json').read_bytes()==(OUT/'native_fixture.json').read_bytes()

seed=20261017
state=(seed+0x6D2B79F5)&MASK
left=imul(state^urshift(state,15),1|state)
product=imul(left^urshift(left,7),61|left)
summed=left+product
mixed=(left^(summed&MASK))&MASK
trace={'seed':seed,'advanced_state_uint32':state,'left_x_signed':left,'second_imul_signed':product,
    'sum_before_outer_xor':summed,'correct_outer_xor_uint32':mixed,
    'missing_xor_final_uint32':int(MissingXorRNG(seed)()*4294967296),
    'corrected_final_uint32':int(RNG(seed)()*4294967296)}

boundary=[]
for row in native['boundary']:
    pts,_=cloud(1,row['d'],.5,protocol['boundary_seed'])
    assert pts[0]==row['point']
    value=abs(pts[0][0])+math.hypot(*pts[0][1:])
    boundary.append({'d':row['d'],'point':pts[0],'support':value,'strict_support_pass':value<.5})

passed=all(x['corrected_mismatches']==0 for x in vector_results) and all(x['tolerance_failures']==0 for x in normal_results) and all(x['tolerance_failures']==0 and x['inside_mismatches']==0 and x['corrected_count']==x['native_count'] for x in cloud_results)
report={'validation_id':protocol['validation_id'],'timestamp_utc':datetime.now(timezone.utc).isoformat(),
    'git_commit':native['git_commit'],'source_sha256':native['source_sha256'],
    'runtimes':{'native':native['runtime'],'python':platform.python_version(),'os':platform.platform()},
    'script_sha256':{name:sha((ROOT/name).read_bytes()) for name in ['port.py','verify_port.py','native_reference.cjs','protocol.json']},
    'formatting_assumptions':['232 and 231 interpreted as 2**32 and 2**31','init and call interpreted as __init__ and __call__','No historical temporary script or tool log was available; this is a reconstruction from the newly supplied text.'],
    'first_step_trace':trace,'vector_results':vector_results,'normal_results':normal_results,
    'cloud_results':cloud_results,'fixtures':fixture_results,'boundary_cases':boundary,
    'gates':{'old_result_provenance':'REPRODUCED_MISSING_XOR_VARIANT',
        'old_port_equivalence':'FAIL',
        'corrected_port_matrix':'PASS' if passed else 'FAIL',
        'native_strict_support':'FAIL_KNOWN_ZERO_INPUT',
        'browser_and_export_freeze':'OPEN',
        'overall_V1b':'NOT_PASSED'},
    'scope_limits':['Corrected port matches declared inputs and numeric tolerances, not all seeds and all floating paths.',
        'Integer streams are exact; Python and JS transcendental arithmetic is only checked numerically.',
        'The original JavaScript sampler has not been modified; the boundary defect remains.',
        'No statistical acceptance thresholds or seeds were changed. Existing native statistical diagnostics are not overwritten by this port correction.']}
(OUT/'port_verification.json').write_text(json.dumps(report,indent=2)+'\n')
(OUT/'corrected_python_clouds.json.gz').write_bytes(gzip.compress(json.dumps(corrected_raw,separators=(',',':')).encode(),compresslevel=9,mtime=0))
print(json.dumps({'gates':report['gates'],'trace':trace,'normal_max_abs_error':max(x['max_absolute_error'] for x in normal_results),
    'cloud_max_abs_error':max(x['max_absolute_error'] for x in cloud_results),
    'cloud_different_binary64':sum(x['different_binary64'] for x in cloud_results),
    'inside_mismatches':sum(x['inside_mismatches'] for x in cloud_results),'fixtures':fixture_results,
    'counts':[(x['d'],x['seed'],x['old_count'],x['corrected_count']) for x in cloud_results]},indent=2))
if not passed: sys.exit(1)
