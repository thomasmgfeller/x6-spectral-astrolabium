"""SPDX-License-Identifier: Apache-2.0"""
import json
import secrets
from gu_common import HERE,BASE,cfg,write,pins
from gu_model import fit

def main():
    assert not (HERE/'seed_schedule.json').exists(),'Never replace target seeds.'
    write(HERE/'development_model.json',fit())
    old=json.loads((BASE/'error_calibration/seed_schedule.json').read_text())
    prior=set(old['excluded_prior_seeds'])
    prior.update(r['geometry_seed'] for phase in ['calibration','test'] for r in old[phase])
    schedule={};skipped=[]
    for phase in ['calibration','test']:
        specs=[]
        while len(specs)<cfg()['clouds_per_phase']:
            seed=secrets.randbits(32)
            if seed in prior:skipped.append(seed);continue
            specs.append(dict(index=len(specs),geometry_seed=seed))
        schedule[phase]=specs
    write(HERE/'seed_schedule.json',dict(excluded_prior_seeds=sorted(prior),skipped=skipped,
          eligible_population=2**32-len(prior),**schedule))
    write(HERE/'source_pins.json',dict(files=pins()))
    print(json.dumps(dict(status='PREPARED',source_files=len(pins()),development_complete=58,new_clouds=64)))

if __name__=='__main__':main()
