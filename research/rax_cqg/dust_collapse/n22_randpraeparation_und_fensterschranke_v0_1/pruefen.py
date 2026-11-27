"""Rebuild the prepared collars, both comparison windows and independent stationary controls."""
import argparse
import json
from fractions import Fraction as F
from hashlib import sha256
from pathlib import Path
from tempfile import TemporaryDirectory
from rechnung import ROOT,H1,H2,header_and_rows,primary,secondary,fine_cover,assemble,witnesses


def encode(value):
    return json.dumps(value,ensure_ascii=False,indent=2,sort_keys=True)+'\n'


def compute(tmp,jobs):
    state,rows1,rows2=header_and_rows(tmp)
    study,prev,exe,special,seeds,old,cfg,coarse,original=state
    assert len(rows1)==len(rows2)==len({r['id'] for r in rows2})==1342
    a=primary(tmp/'nachfolger',prev,special,rows1,cfg,jobs,3500)
    controls=witnesses(tmp,study,prev,exe,special,seeds,cfg,rows2,coarse)
    if not a['excluded']:
        raise RuntimeError('Der Primärfall ist offen. Der Folgetest erfordert den Ausschluss.')
    trees,audit,cuts=secondary(study,prev,exe,special,rows2,cfg,tmp/'nachfolger',jobs)
    finer,refinement=fine_cover(tmp,prev,special,rows2,cfg,coarse,cuts,jobs)
    tally,register=assemble(rows2,trees,cuts,refinement)
    upper=F(controls['tighter_upper_bound'])
    lower=H2 if tally['open']==0 else H1
    assert lower<upper and a['excluded'] and old['P3']=={'NOT_RUN':60,'radius':None}
    return (dict(primary=a,secondary=dict(summary=tally,trees=trees,coarse_target=cuts,
                                          fine_target=refinement,algebra=audit),
                 controls=controls,bounds=dict(lower=str(lower),upper=str(upper),width=str(upper-lower)),
                 previous_collar=original,P3=old['P3']),
            {'coarse':coarse,'fine':finer},register)


def compare(reference,actual,register,table):
    assert actual['controls']==reference['controls'] and actual['bounds']==reference['bounds']
    assert actual['P3']==reference['P3'] and actual['previous_collar']==reference['previous_collar']
    core=('previous_case_count','previously_excluded','target','sector','excluded','inherited_open_slabs')
    assert all(actual['primary'][k]==reference['primary'][k] for k in core)
    assert all(x['open']==0 for x in actual['primary']['slabs'])
    got,ref=actual['secondary'],reference['secondary']
    assert got['algebra']==ref['algebra'] and got['trees'].keys()==ref['trees'].keys()
    for key,sectors in got['trees'].items():
        assert sectors.keys()==ref['trees'][key].keys()
        assert all((x['open']==0)==(ref['trees'][key][s]['open']==0) for s,x in sectors.items())
    assert all(got['summary'][k]==ref['summary'][k] for k in ('open','excluded','cases','initial_exclusions','open_leaves'))
    # A different sound preconditioner may give different tree sizes.
    def classes(text):
        return [line.split('\t')[:8] for line in text.splitlines()]
    assert classes(register)==classes(table)


def main():
    p=argparse.ArgumentParser()
    p.add_argument('--jobs',type=int,default=4)
    p.add_argument('--ausgabe',type=Path)
    args=p.parse_args()
    if not __debug__ or args.jobs<1:raise ValueError('Python ohne -O und positive Parallelität erforderlich.')
    assert sha256((ROOT/'Pruefplan.md').read_bytes()).hexdigest()==(ROOT/'Pruefplan.sha256').read_text().split()[0]
    with TemporaryDirectory() as td:
        result,prep,register=compute(Path(td),args.jobs)
    if args.ausgabe:
        args.ausgabe.mkdir(parents=True,exist_ok=True)
        for name,data in [('Ergebnisse.json',result),('Randzellen.json',prep)]:
            (args.ausgabe/name).write_text(encode(data))
        (args.ausgabe/'Fallregister_55_2048.tsv').write_text(register)
    else:
        assert encode(prep)==(ROOT/'Randzellen.json').read_text()
        compare(json.loads((ROOT/'Ergebnisse.json').read_text()),json.loads(encode(result)),register,
                (ROOT/'Fallregister_55_2048.tsv').read_text())
    print('27/1024:',result['primary']['excluded'],'55/2048:',result['secondary']['summary'])
    print('Schranken',result['bounds'])

if __name__=='__main__':main()
