"""Exploratory dyadic transfers under the already frozen calibration."""
import json
from concurrent.futures import ProcessPoolExecutor
from rechnung import calc

def run():
    cases = [('positive', rho, 2.0**-k) for rho in (.125, .25) for k in (12, 16, 20)]
    with ProcessPoolExecutor(max_workers=3) as pool:
        return dict(pool.map(calc, cases))

if __name__ == '__main__':
    print(json.dumps(run(), indent=2, sort_keys=True))
