"""Replay every training and validation cloud without overwriting evidence.
SPDX-License-Identifier: Apache-2.0
"""
from pt_common import *
from pt_audit import audit
if __name__=='__main__':
    assert audit()==read(HERE/'audit.json')
    c=read(HERE/'contract.json');f=kernel()
    for phase in ['training','validation']:
      for g in range(2):
        assert simulate(g,phase,c[phase+'_trials_per_geometry'],f)==read(HERE/f'{phase}-{g}.json.gz')
    print('PASS: all 1280 shared Poisson clouds, sealed classifier and held-out summary reproduced')
