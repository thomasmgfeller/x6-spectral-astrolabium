import argparse,json
from pathlib import Path
from families import screen
from integrals import evaluate_grids

if __name__=='__main__':
    parser=argparse.ArgumentParser()
    parser.add_argument('output',type=Path)
    args=parser.parse_args()
    families,audit,states=screen()
    values,checks=evaluate_grids(states)
    result={"families":families,"rank_audit":audit,"grids":values,"direct_clock_checks":checks}
    args.output.write_text(json.dumps(result,indent=2)+"\n")
