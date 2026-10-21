"""SPDX-License-Identifier: Apache-2.0"""
import json
import secrets
from gg_common import HERE,BASE,cfg,write,pins
from gg_model import fit

def main():
    assert not (HERE/'seed_schedule.json').exists(),'Never replace target seeds.'
    fitted=fit();write(HERE/'development_model.json',fitted)
    old=json.loads((BASE/'geometry_uncertainty/seed_schedule.json').read_text())
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
    print(json.dumps(dict(status='PREPARED',source_files=len(pins()),development_complete=fitted['development_complete'],new_clouds=2*cfg()['clouds_per_phase'])))

if __name__=='__main__':main()
