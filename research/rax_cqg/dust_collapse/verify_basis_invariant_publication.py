"""Portable publication replay, preserving the original package byte for byte.

Only LAPACK-proposed trial vectors and their derived Rayleigh diagnostic may
differ. All other fields, including every amplitude, error enclosure, singular
value, bound endpoint and Sylvester determinant, must match exactly. Both sets
of trial vectors are independently revalidated with interval arithmetic.
"""
import copy
import hashlib
import importlib.util
import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile

ROOT=Path(__file__).resolve().parent/'basis_invariant_coupling_v0_1'
sys.path.insert(0,str(ROOT))
import compute as c
from flint import arb, acb_mat, ctx


def stable_content(data):
    data=copy.deepcopy(data)
    for block in data['blocks'].values():
        for key in ('independent_full6','independent_atom_to_positive'):
            proof=block[key]
            if set(proof)!={'lower','upper','Rayleigh_lower','trial_vector','Sylvester_determinants'}:
                raise AssertionError('Unexpected proof schema')
            del proof['trial_vector']
            del proof['Rayleigh_lower']
    return data


def require_same_science(original,replayed):
    if stable_content(original)!=stable_content(replayed):
        raise AssertionError('Scientific result or fixed certificate differs')


def certify_trial(block,region):
    full=c.matrix_unpack(block['raw_block'])
    if region=='full6':
        b=full;gi=c.repeated_gram(3);go=c.repeated_gram(3)
    else:
        b=acb_mat([[full[i,j] for j in range(2)] for i in range(2,6)])
        gi=c.repeated_gram(1);go=c.repeated_gram(2)
    proof=block['independent_'+region]
    v=c.matrix_unpack(proof['trial_vector'])
    if (v.nrows(),v.ncols())!=(b.ncols(),1):raise AssertionError('Invalid trial dimension')
    h=c.adj(b)*go.inv()*b
    denominator=(c.adj(v)*gi*v)[0,0]
    if not denominator.imag.contains(0) or not denominator.real>0:
        raise AssertionError('Invalid trial norm')
    numerator=(c.adj(v)*h*v)[0,0]
    if not numerator.imag.contains(0):raise AssertionError('Nonreal Rayleigh form')
    ray=(numerator.real/denominator.real).sqrt()
    lower=arb(proof['lower']).upper();upper=arb(proof['upper']).lower()
    if not ray>lower:raise AssertionError('Trial does not prove the lower bound')
    positive=upper*upper*gi-h
    for k in range(1,b.ncols()+1):
        det=acb_mat([[positive[i,j] for j in range(k)] for i in range(k)]).det()
        if not det.imag.contains(0) or not det.real>0:
            raise AssertionError('Upper-bound positive definiteness not certified')
    sig=arb(block[region]['sigma_max'])
    if not (sig>lower and sig<upper):raise AssertionError('Singular interval outside independent bounds')


def negative_controls(data):
    def rejects(fn):
        try:fn()
        except AssertionError:return
        raise AssertionError('Invalid evidence was accepted')
    altered=copy.deepcopy(data)
    altered['blocks']['difference']['raw_block'][0][0]['real']='1'
    rejects(lambda:require_same_science(data,altered))
    altered=copy.deepcopy(data['blocks']['difference'])
    for row in altered['independent_full6']['trial_vector']:
        row[0]={'real':'0','imag':'0'}
    rejects(lambda:certify_trial(altered,'full6'))
    altered=copy.deepcopy(data['blocks']['difference'])
    altered['independent_full6']['upper']='0.000001'
    rejects(lambda:certify_trial(altered,'full6'))


def main():
    ctx.prec=192
    manifest=json.loads((ROOT/'SHA256SUMS.json').read_text())
    for name,digest in manifest.items():
        if hashlib.sha256((ROOT/name).read_bytes()).hexdigest()!=digest:
            raise AssertionError('Package hash mismatch: '+name)
    with tempfile.TemporaryDirectory() as tmp:
        dest=Path(tmp)/'replay';shutil.copytree(ROOT,dest,ignore=shutil.ignore_patterns('__pycache__'))
        subprocess.run([sys.executable,'-B','compute.py'],cwd=dest,check=True)
        subprocess.run([sys.executable,'-B','tests.py'],cwd=dest,check=True,stdout=subprocess.DEVNULL)
        if (dest/'results/quadrature.json').read_bytes()!=(ROOT/'results/quadrature.json').read_bytes():
            raise AssertionError('Quadrature bytes differ')
        varying=[];certificates=0
        for name in ('uniform.json','cancellation_control.json'):
            original=json.loads((ROOT/'results'/name).read_text())
            replayed=json.loads((dest/'results'/name).read_text())
            require_same_science(original,replayed)
            if original!=replayed:varying.append(name)
            for result in (original,replayed):
                for block in result['blocks'].values():
                    for region in ('full6','atom_to_positive'):
                        certify_trial(block,region);certificates+=1
            negative_controls(original)
    print(json.dumps({'status':'PASS','hashes':len(manifest),'quadrature_byte_identical':True,
                      'scientific_blocks_and_fixed_certificates_exact':True,
                      'original_control_groups':13,'original_and_replayed_trial_certificates':certificates,
                      'negative_control_types':3,'platform_trial_variations':varying}))


if __name__=='__main__':main()
