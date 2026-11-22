"""Create a per-density index with the direction and meaning of each certified bound."""
import csv
from fractions import Fraction as Q
import io
import json
from pathlib import Path

ROOT=Path(__file__).resolve().parent


def table():
    read=lambda n:json.loads((ROOT/n).read_text())
    base=read('ergebnis.json')['per_type']
    candidates=read('zeugen.json')['rows']
    divided={**read('teilung.json')['rows'],**read('restzeilen.json')}
    stream=io.StringIO(newline='')
    writer=csv.writer(stream,lineterminator='\n')
    writer.writerow(['type','mass','inlet_density_center','status','method',
                     'witness_relative_error_lower','relative_error_upper','upper_bound_applies_to'])
    totals={'UNIFORM_BOUND':0,'COUNTEREXAMPLE':0}
    types={}
    for code in sorted(map(int,base)):
        types[code]=[]
        for center in ('1/8','1/4'):
            row=base[str(code)][center]
            key=f'{code};{center}'
            w=candidates.get(key,{}).get('witness')
            split=divided.get(key,{})
            decisions=[row['angle_joint'],bool(w),bool(split.get('passes'))]
            assert sum(decisions)==1
            if w:
                state,method,low,high,scope='COUNTEREXAMPLE','two_histories',w['relative_error_lower'],w['relative_error_upper'],'witness_only'
                assert Q('1/50')<Q(low)<=Q(high)
            else:
                state,low,scope='UNIFORM_BOUND','','all_admissible_measures'
                method,high=('subdivision',split['relative_upper']) if split else ('sector',row['angle_joint_relative'])
                assert Q(high)<=Q('1/50')
            writer.writerow([code,4,center,state,method,low,high,scope])
            types[code].append(state)
            totals[state]+=1
    assert len(types)==61 and totals=={'UNIFORM_BOUND':94,'COUNTEREXAMPLE':28}
    assert sum(set(v)=={'UNIFORM_BOUND'} for v in types.values())==46
    return stream.getvalue()


if __name__=='__main__':
    print(table(),end='')
