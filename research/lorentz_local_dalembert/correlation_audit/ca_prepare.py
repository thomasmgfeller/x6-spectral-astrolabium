"""SPDX-License-Identifier: Apache-2.0"""
import json
from ca_common import HERE,pins,write

if __name__=='__main__':
    assert not (HERE/'source_pins.json').exists(),'Never replace a freeze.'
    p=pins();write(HERE/'source_pins.json',dict(files=p))
    print(json.dumps(dict(status='PREPARED',source_files=len(p),new_simulations=0)))
