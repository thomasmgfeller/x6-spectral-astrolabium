"""Apply the published classical shell instruments to the new time width."""
from fractions import Fraction as F
from pathlib import Path
import json
import sys
sys.path.insert(0, str(Path(__file__).resolve().parent/"basis/block"))
from schalenblock import instruments, radius_from_block, radius_bounds, R0, X, roots, surface, ltb, control


def evaluate():
    h = F(1,32)
    calibration = control()
    assert calibration["vacuum_surface"] is None
    end = 5*roots(F(5),2)[1]/3
    results = {}
    for old in calibration["cases"]:
        m = F(old["model_mass"])
        k = roots(F(125,2)*m/R0**3, 2)[1]
        assert R0*roots((1-k*(X+h))**2,3)[0] > 2*m  # Surface speed below one.
        assert F(125,2)*5*m/(2*R0**3)*(X+h)**2 < 1  # Regular ordered stations.
        occupied = [ltb.initial_signal(a,m)>0 for a in ltb.GRID]
        a,b = surface(occupied)
        channels = [instruments(ltb.GRID[i], ltb.GRID[j], m, h) for i,j in [(a-1,a),(b,b+1)]]
        lo,hi = radius_from_block(*channels, h*end)
        target = radius_bounds(R0,m)
        assert lo<=target[0]<=target[1]<=hi
        results[str(m)] = dict(R=list(map(str,(lo,hi))), target=list(map(str,target)),
            max_relative_error=str(max(1-lo/target[1],hi/target[0]-1)),
            within_5_percent=lo>=F(95,100)*target[1] and hi<=F(105,100)*target[0],
            calibrated_mass=old["mass_interval"])
    light,heavy = (tuple(map(F,results[k]["target"])) for k in ("1/4","4"))
    # For common output r the minimax balances 1-r/light and r/heavy-1.
    minimax = [(light[0]-heavy[1])/(light[0]+heavy[1]), (light[1]-heavy[0])/(light[1]+heavy[0])]
    return dict(cases=results, common_output_minimax=list(map(str,minimax)),zero=calibration["vacuum_charge"])


if __name__=="__main__":
    print(json.dumps(evaluate(),sort_keys=True))
