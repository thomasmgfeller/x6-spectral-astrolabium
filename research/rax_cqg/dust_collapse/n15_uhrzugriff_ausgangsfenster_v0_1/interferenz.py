"""Positive auxiliary probabilities for a coherent shared boundary projection."""
from math import atan2,fsum
from geometrie import H
from auslese import settings

def evaluate(kernels,raw):
    z0=complex(*kernels['0']);phases={'0':0};arms={}
    for tag,pair in kernels.items():
        if tag=='0':continue
        z=complex(*pair)
        # Cancel incoherent intensities by taking the difference of output counts.
        probabilities=[]
        for rotation in (1,-1j):
            a=abs(z0+rotation*z)**2/4;b=abs(z0-rotation*z)**2/4
            assert 0<=a<=1 and 0<=b<=1 and a+b<1+1e-12
            probabilities.extend([a,b])
        x=probabilities[0]-probabilities[1];y=probabilities[2]-probabilities[3]
        phases[tag]=atan2(y,x)
        avg=(abs(z0)**2+abs(z)**2)/4
        # Orthogonal path records: amplitudes lie on separate basis vectors.
        for rotation in (1,-1j):
            for sign in (-1,1):
                record=(z0/2,sign*rotation*z/2)
                assert abs(sum(abs(item)**2 for item in record)-avg)<1e-14
        interference=abs(z*z0.conjugate())/2
        arms[tag]={'quadrature_probabilities':probabilities,'visibility':interference/avg,'joint_projection_probability':2*avg,'orthogonal_record_visibility':0}
    reconstructed=fsum(float(w)*phases[tag] for tag,(_,w) in settings().items())
    assert abs(reconstructed-raw)<1e-7
    return {'minimum_visibility':min(v['visibility'] for v in arms.values()),'raw_from_probabilities':reconstructed,'arms':arms}

def run(rows):
    return {k:evaluate(v['fine']['kernels'],v['fine']['raw']) for k,v in rows.items() if '|positive|1|' in k}
if __name__=='__main__':
    import json
    from pathlib import Path
    print(json.dumps(run(json.loads((Path(__file__).resolve().parent/'transfer.json').read_bytes())),indent=2,sort_keys=True))
