"""Apply the original rational 25-equation certificate to a reconstructed common receiver."""
import json
from importlib.util import module_from_spec, spec_from_file_location
from fractions import Fraction
from pathlib import Path


def verify(tmp, cfg, rows, seed, previous, exe):
    proposal=json.loads((Path(__file__).resolve().parent/'Zeugenzentrum.json').read_text())
    key=f"{proposal['cid']}/{proposal['past']}/{proposal['future']}/+"
    row=next(r for r in rows if r['id']==key)
    assert proposal['row']==seed[row['cid']]['row']
    path=tmp/'base'/'zeugnis.py'
    code=path.read_text()
    signature='def certify(d,proposal):'
    build="rel,c=structure(set(d['order']),row,case[0])"
    assert code.count(signature)==code.count(build)==1
    code=code.replace(signature,'def certify(d,proposal,edges,coefficients):')
    code=code.replace(build,'rel,c=set(edges),dict(coefficients)')
    path=path.with_name('empfangszeugnis.py')
    path.write_text(code)
    spec=spec_from_file_location('empfangszeugnis',path)
    module=module_from_spec(spec)
    spec.loader.exec_module(module)
    proof=module.certify(cfg,proposal,row['edges'],row['coeff'])
    assert proof['equations']==25 and proof['strict_relations']==len(row['edges'])
    assert Fraction(proof['upper_sum'])<1
    assert row['between']==(0,0) and row['fo']==0
    test=previous.invoke(exe,row,previous.inputs(row,cfg['collar'],proposal),0,1,'control')
    assert test.split()==['1','0','1','0']
    return dict(case_id=key,**proof)
