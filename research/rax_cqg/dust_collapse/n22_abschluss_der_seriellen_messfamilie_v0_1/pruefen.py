"""Offline verification of every remaining N22 predecessor in the fixed measurement window."""
import argparse
import csv
import gzip
import io
import json
import subprocess
import sys
from concurrent.futures import ThreadPoolExecutor, as_completed
from fractions import Fraction as F
from hashlib import sha256
from pathlib import Path
from tempfile import TemporaryDirectory
from zipfile import ZipFile

from paargleichung import check as check_pair_identity
from wirkung import CLOCKS, WEIGHTS, S, check as check_action

ROOT = Path(__file__).resolve().parent
PINS = ('786feda88a47ebab2a117e06bb0b8b8401f05ad311baa1e84d87d27cee5a4a7b',
        'bde2befb9dd6f306f596126976fcde4379a4449b351fcc6413c6929c555cf042',
        '7b1e8655d3706ab0980d7843d936912a4914473de7c52033c974d1b4ff261100')
MASKS = ('P19','F19','P20','F20')
DUST = {4,5,6,11,12,13,14}


def serial(obj):
    return json.dumps(obj, indent=2, sort_keys=True, ensure_ascii=False)+'\n'


def unpack(file, pin, destination):
    assert sha256(file.read_bytes()).hexdigest() == pin
    with ZipFile(file) as package:
        package.extractall(destination)


def calculate(tmp, workers, budgets, budget):
    latest, previous, base = (tmp/s for s in ('follower','branches','n22'))
    unpack(ROOT/'basis/Nachfolger.zip', PINS[0], latest)
    unpack(latest/'basis/Vorstudie.zip', PINS[1], previous)
    unpack(previous/'basis/N22.zip', PINS[2], base)
    sys.path[:0] = [str(previous), str(base)]
    from randhulle import collect
    from ordnung22 import structure
    from zeugnis import certify
    start = json.loads((latest/'Ergebnisse.json').read_text())
    cfg = collect(previous/'basis/N22.zip', 256)
    collar = cfg['collar']
    assert {str(j): b for j,b in collar.items()} == start['collar']
    order = set(map(tuple, cfg['order']))
    left, right = F(31,64), F(33,64)
    lower = (1-left)*collar[3][0] + left*collar[7][0]
    upper = (1-right)*collar[3][1] + right*collar[7][1]
    window = (lower//1,-(-upper//1))
    assert window == (23437499,143229167)
    reg = list(csv.DictReader((latest/'Offene_Faelle.tsv').read_text().splitlines(), delimiter='\t'))
    inputs = {(r['Sektor'],int(r['ID'])):tuple(int(r[n]) for n in MASKS) for r in reg}
    paired = sorted(k for s,k in inputs if s == 'A0' and ('A+',k) in inputs)
    assert paired == start['register_audit']['paired_A'] and len(inputs) == start['remaining'] == 21
    assert all(inputs['A0',k] == inputs['A+',k] for k in paired)

    kernel = (previous/'zweigtest.cpp').read_text()
    marker, driver = 'void combined(', 'int main(int argc,char** argv){'
    assert kernel.count(marker) == kernel.count(driver) == 1
    field, tail = kernel.split(marker)
    (tmp/'gleichungen.hpp').write_text(field)
    (tmp/'suche.hpp').write_text(marker + tail.split(driver)[0])
    program = tmp/'fenster'
    subprocess.run(['g++','-std=c++17','-O2','-fsanitize=signed-integer-overflow',
                    '-fno-sanitize-recover=all','-I',str(tmp),'-I',str(base),
                    str(ROOT/'fenster.cpp'),'-o',str(program)],check=True)

    def run(row, kind, small=0, depth=0, cap=1, mode='tree', boundary=None, centers=()):
        boundary = collar if boundary is None else boundary
        lines = [str(len(order)), *(f'{i} {j}' for i,j in sorted(order))]
        lines.extend(' '.join(map(str,(j,*v))) for j,v in boundary.items())
        lines += [' '.join(map(str,window)), ' '.join(map(str,row))]
        lines.extend(f'{lo} {hi}' for lo,hi in centers)
        result = subprocess.run([str(program),kind,str(small),str(depth),str(cap),mode],
                                input='\n'.join(lines)+'\n',text=True,capture_output=True)
        if result.returncode:
            raise RuntimeError(f'{kind} {row} {mode}: {result.stderr}')
        return result.stdout

    order_counts, action_counts, trees = {}, {}, {}
    pair_coefficients = []
    for (kind, case), row in inputs.items():
        key = f'{kind}/{case}'
        edges, coeff = structure(order,row,'A')
        assert (21,19) in edges and (19,20) not in edges and (20,19) not in edges
        assert all((0,j) in edges for j in (*DUST,*CLOCKS))
        assert all((j,7) in edges for j in (*DUST,15,16,17,18,20))
        assert all(not ((i in DUST and j in CLOCKS) or (j in DUST and i in CLOCKS)) for i,j in coeff)
        independent = {tuple(map(int,s.split())) for s in run(row,kind,mode='order').splitlines()}
        assert independent == {(i,j,coeff.get((i,j),0)) for i,j in edges}
        order_counts[key] = len(edges)
        action_counts[key] = 0
        if kind == 'A+' and case in paired:
            pair_coefficients.append(coeff)
        for small in range(4):
            def algebra_call(boundary, centers):
                return run(row,kind,small,mode='algebra',boundary=boundary,centers=centers)
            action_counts[key] += check_action(algebra_call,coeff,collar,kind,small)
        trees[key] = {}

    def evaluate(kind, case, small, cap):
        result = run(inputs[kind,case],kind,small,76,cap)
        nodes, closed, opened, depth = map(int,result.split())
        assert nodes == 2*(closed+opened)-1
        return dict(nodes=nodes, closed=closed, open=opened, depth=depth, budget=cap)

    # The matched orders are processed before the one-weight cases.
    with ThreadPoolExecutor(max_workers=workers) as pool:
        for ids in (set(paired), set(k for _,k in inputs)-set(paired)):
            futures = {}
            for kind,case in inputs:
                if case not in ids:
                    continue
                key = f'{kind}/{case}'
                for small in range(4):
                    cap = budgets.get(key,{}).get(str(small),budget)
                    futures[pool.submit(evaluate,kind,case,small,cap)] = key,str(small)
            for future in as_completed(futures):
                key,s = futures[future]
                trees[key][s] = future.result()
                print(key,s,trees[key][s],flush=True)

    controls = {}
    witnesses = json.loads((base/'Zeugenzentren.json').read_text())
    witnesses['Vorgaenger_216141'] = json.loads((ROOT/'Zeugenzentrum_216141.json').read_text())
    assert tuple(witnesses['Vorgaenger_216141']['row']) == inputs['A+',216141]
    for name in ('Zeuge_Kontrolle','Zeuge_Rand_zz','Vorgaenger_216141'):
        witness = witnesses[name]
        cert = certify(cfg,witness)
        assert all(F(hi)<left or F(lo)>right for lo,hi in cert['normalized_clocks'][:2])
        if name == 'Vorgaenger_216141':
            assert witness['case'] == 'A+' and cert['inside_window'] == [False,False,True]
        centers = []
        for field, indices, rad in [('y',CLOCKS,F(1,10**7)),('w',WEIGHTS,F(1,10**8))]:
            for j in indices:
                v = F(witness[field][j])
                centers.append(((v-rad)*S//1,-(-(v+rad)*S//1)))
        assert list(map(int,run(witness['row'],witness['case'],mode='control',centers=centers).split())) == [1,0,1,0]
        controls[name] = {k:cert[k] for k in ('row','upper_sum','upper_beta','upper_q','normalized_clocks','equations','inside_window','strict_relations','positive_weights')}
    excluded = {k for k,v in trees.items() if all(t['open']==0 for t in v.values())}
    keep = [r for r in reg if r['Sektor']+'/'+r['ID'] not in excluded]
    out = io.StringIO()
    writer = csv.DictWriter(out,fieldnames=reg[0].keys(),delimiter='\t',lineterminator='\n')
    writer.writeheader()
    writer.writerows(keep)
    # Join the register to the original enumeration with full sector, ID and four masks.
    original = {}
    with gzip.open(base/'Register.tsv.gz','rt') as fp:
        for count,r in enumerate(csv.DictReader(fp,delimiter='\t'),start=1):
            assert int(r['ID']) == count
            for kind in ('A0','A+','B0','B+'):
                if r[kind].endswith('/OPEN'):
                    original[kind,count] = tuple(int(r[k]) for k in MASKS)
    earlier = json.loads((previous/'Ergebnisse.json').read_text())
    for case in earlier['excluded']+start['excluded']:
        del original['B+',case]
    assert original == inputs and count*4 == start['cases']
    result = dict(paired=paired,initial_open=len(inputs),selected=list(sorted(trees)),new_excluded=sorted(excluded),
                  open_by_sector={s:sum(r['Sektor'] == s for r in keep) for s in ('A0','A+','B0','B+')},remaining=len(keep),projections=count,
                  cases=count*4,now_excluded=count*4-len(keep),order_entries=order_counts,action_entries=action_counts,
                  collar=collar,window_ticks=window,partitions=cfg['pieces'],sources=cfg['sources'],
                  pair_density=check_pair_identity(pair_coefficients,collar,window,S),
                  controls=controls,trees=trees,P3=start['P3'])
    comparison = io.StringIO()
    table = csv.writer(comparison,delimiter='\t',lineterminator='\n')
    table.writerow(['ID',*MASKS,'A0','A+'])
    for case in sorted({k for _,k in inputs}):
        row = inputs.get(('A0',case)) or inputs['A+',case]
        state = []
        for kind in ('A0','A+'):
            if (kind,case) not in inputs:
                state.append('BEREITS_AUSGESCHLOSSEN')
            elif f'{kind}/{case}' in excluded:
                state.append('JETZT_AUSGESCHLOSSEN')
            else:
                state.append('OFFEN')
        table.writerow([case,*row,*state])
    return result, out.getvalue(), comparison.getvalue()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--jobs',type=int,default=2)
    parser.add_argument('--budget',type=int,default=10000)
    parser.add_argument('--ausgabe',type=Path)
    parser.add_argument('--stufe',type=Path,help='Für offene Bäume das neue Budget verwenden.')
    args = parser.parse_args()
    if not __debug__:
        raise RuntimeError('Python ohne -O verwenden.')
    if min(args.jobs,args.budget)<1:
        parser.error('Budget und jobs müssen positiv sein.')
    assert sha256((ROOT/'Pruefplan.md').read_bytes()).hexdigest() == (ROOT/'Pruefplan.sha256').read_text().split()[0]
    ref = json.loads((ROOT/'Ergebnisse.json').read_text()) if not args.ausgabe else None
    profile = json.loads(args.stufe.read_text()) if args.stufe else ref
    budgets = {}
    if profile:
        budgets = {k:{s:(args.budget if args.stufe and v['open'] else v['budget']) for s,v in t.items()}
                   for k,t in profile['trees'].items()}
    with TemporaryDirectory() as d:
        result, table, comparison = calculate(Path(d),args.jobs,budgets,args.budget)
    if args.ausgabe:
        args.ausgabe.mkdir(exist_ok=True,parents=True)
        (args.ausgabe/'Ergebnisse.json').write_text(serial(result))
        (args.ausgabe/'Offene_Faelle.tsv').write_text(table)
        (args.ausgabe/'Vorgaengervergleich.tsv').write_text(comparison)
    else:
        got = json.loads(serial(result))
        assert {k:v for k,v in got.items() if k!='trees'} == {k:v for k,v in ref.items() if k!='trees'}
        for k,sectors in ref['trees'].items():
            for s,v in sectors.items():
                assert (v['open']==0) == (got['trees'][k][s]['open']==0)
        assert (ROOT/'Offene_Faelle.tsv').read_text() == table
        assert (ROOT/'Vorgaengervergleich.tsv').read_text() == comparison
    print('Neu ausgeschlossen',len(result['new_excluded']),'restlich offen',result['remaining'])

if __name__ == '__main__':
    main()
