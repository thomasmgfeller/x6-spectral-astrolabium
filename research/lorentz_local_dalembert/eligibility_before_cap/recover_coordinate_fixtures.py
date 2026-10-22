"""Recover verification coordinates only if old published raw hashes match.
SPDX-License-Identifier: Apache-2.0
"""
import sys,gzip
import numpy as np
from eb_common import HERE,read
from simulation import config,experiment,shell,uniform_diamond,digest

def main(write=False):
    c=read(HERE/'contract.json');_,oc,_,_=config()
    for index in [0,31]:
        record=read(HERE/f'results/cloud-{index:02d}.json.gz');seed=record['seed']
        a,*_=experiment.sprinkle(c['selection_density'],seed)
        for j,(lo,hi) in enumerate(zip(oc['outer_durations'][:-1],oc['outer_durations'][1:]),1):
            zz,*_=shell(c['selection_density'],seed,j,lo,hi,oc);a=np.vstack((a,zz))
        rng=np.random.default_rng(np.random.SeedSequence([seed,c['count_seed_tag'],0]))
        n=int(rng.poisson(c['count_density']*np.pi/12*c['duration']**3));b=uniform_diamond(n,c['duration'],rng)
        expected_b=next(iter(record['replicates'][0]['arms'].values()))['observed']['coordinates_sha256']
        for array,expected in [(a,record['selection']['coordinates_sha256']),(b,expected_b)]:
            assert digest(array)==expected,'Recovery requires reference-compatible numerical dispatch; never replace archived hashes.'
            path=HERE/'coordinate_fixtures'/f'{expected}.bin.gz';raw=array.tobytes()
            if write:
                with path.open('xb') as f:
                    with gzip.GzipFile(filename='',fileobj=f,mode='wb',mtime=0) as g:g.write(raw)
            else:assert gzip.decompress(path.read_bytes())==raw
    print('PASS: all recovered coordinate bytes match their original published hashes')
if __name__=='__main__':main('--write' in sys.argv)
