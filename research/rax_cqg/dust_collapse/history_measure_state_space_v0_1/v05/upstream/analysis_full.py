"""Generate the study results from the resolved clock cache and archived contracts."""
import argparse
import json
from pathlib import Path
from readout import (ROOT, reconstruct, allocations, campaigns, radius, weights_array,
                     probabilities, assess, label)
from certify import certify


def main(grids):
    parents,mids,ends,names,stored,path_rows,checks=reconstruct(grids)
    laws=allocations(parents,mids,ends,path_rows)
    previous=json.loads((ROOT/'v03/results.json').read_text())
    witness={}
    for tag,mm in stored.items():
        base=probabilities(mm,weights_array({k:.5 for k in parents},names))
        endpoint=probabilities(mm,weights_array({(5,184):.996,(5,22):.004},names))
        middle=probabilities(mm,weights_array({(4,11):.996,(4,14):.004},names))
        witness[tag]={'at_N12':assess(middle,base),'at_N13':assess(endpoint,base)}
        assert not witness[tag]['at_N12']['pass'] and witness[tag]['at_N13']['pass']
        assert abs(witness[tag]['at_N13']['success_delta']-
                   previous['exploratory_endpoint_checks']['fine']['selected_endpoint']['success_delta'])<5e-12
    return {'source_commit':'cf35adb4ce5d35f6fc79ce05e2db07b8e2a3dd60','branch_order':[label(k) for k in names],
            'full_N13':[label(k) for k in ends],'clock_checks':checks,
            'endpoint_coverage':{'marked_paths':sum(row['paths'] for row in path_rows.values()),
              'valid_forward_paths':sum(row['sequential_paths'] for row in path_rows.values()),
              'valid_in_both_orders':sum(row['reverse_also_admissible_paths'] for row in path_rows.values()),
              'geometries_reached':previous['counts']['all_end_types'],'endpoint_admissible':previous['counts']['admissible_end_types']},
            'campaigns':campaigns(names,stored['fine'],parents,laws),
            'v03_two_type_witness':witness,
            'uniform_bounds':{tag:radius(m['coherent'],names,parents,mids,ends) for tag,m in stored.items()},
            'exact_finite_grid_tests':{tag:certify(m['coherent'],names,parents,mids,ends,laws) for tag,m in stored.items()},
            'coherent_readout_grid_matrices':{tag:m['coherent'].tolist() for tag,m in stored.items()}}


if __name__=='__main__':
    parser=argparse.ArgumentParser()
    parser.add_argument('grids',type=Path);parser.add_argument('output',type=Path)
    args=parser.parse_args()
    args.output.write_text(json.dumps(main(json.loads(args.grids.read_text())),sort_keys=True,indent=2,allow_nan=False)+'\n')
