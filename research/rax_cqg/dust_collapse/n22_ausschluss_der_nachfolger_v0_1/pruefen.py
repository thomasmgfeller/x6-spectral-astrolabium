"""Reconstruct the selected N22 orders and replay the window exclusions offline."""
import argparse
import csv
import io
import json
import subprocess
import sys
from concurrent.futures import ThreadPoolExecutor, as_completed
from hashlib import sha256
from pathlib import Path
from tempfile import TemporaryDirectory
from zipfile import ZipFile
from staubuhren import dust_clocks, DUST_ORDER
from kopplungstest import check as check_couplings
from register import audit

ROOT = Path(__file__).resolve().parent
PARENT = 'bde2befb9dd6f306f596126976fcde4379a4449b351fcc6413c6929c555cf042'
N22 = '7b1e8655d3706ab0980d7843d936912a4914473de7c52033c974d1b4ff261100'
DEVICE = set(range(15, 22))
DUST = {4, 5, 6, 11, 12, 13, 14}


def dump(obj):
    return json.dumps(obj, ensure_ascii=False, indent=2, sort_keys=True) + '\n'


def unpack(path, checksum, target):
    assert sha256(path.read_bytes()).hexdigest() == checksum
    with ZipFile(path) as archive:
        archive.extractall(target)


def run_test(tmp, jobs, budget, previous):
    from fractions import Fraction
    parent, base = tmp / 'parent', tmp / 'n22'
    unpack(ROOT / 'basis/Vorstudie.zip', PARENT, parent)
    unpack(parent / 'basis/N22.zip', N22, base)
    sys.path[:0] = [str(parent), str(base)]
    # Import under a dedicated name to avoid shadowing this verifier.
    from importlib.util import spec_from_file_location, module_from_spec
    spec = spec_from_file_location('vorstudie', parent / 'pruefen.py')
    old = module_from_spec(spec)
    spec.loader.exec_module(old)
    from ordnung22 import structure
    from zeugnis import certify
    ref = json.loads((parent / 'Ergebnisse.json').read_text())
    cfg = old.collect(parent / 'basis/N22.zip', 256)
    assert {str(k): v for k, v in cfg['collar'].items()} == ref['collar']
    order = set(map(tuple, cfg['order']))
    reg = list(csv.DictReader((parent / 'Offene_Faelle.tsv').read_text().splitlines(), delimiter='\t'))
    assert len(reg) == ref['remaining'] == len({(r['Sektor'], r['ID']) for r in reg})
    rows = {}
    groups = {}
    dust_bounds = {}
    coupling = {}
    for r in reg:
        if r['Sektor'] != 'B+':
            continue
        row = [int(r[key]) for key in ('P19', 'F19', 'P20', 'F20')]
        edges, coeff = structure(order, row, 'B')
        coupled = any((i in DUST and j in DEVICE) or (j in DUST and i in DEVICE) for i, j in coeff)
        missing = {(a, b) for j in DEVICE for a, b in ((0, j), (j, 7)) if (a, b) not in edges}
        if not coupled:
            if missing == {(19, 7)}:
                group = 'nur_19'
            else:
                assert missing in ({(20, 7), (21, 7)}, {(19, 7), (20, 7), (21, 7)})
                assert (20, 21) in edges and (21, 8) in edges
                group = 'auch_21'
            assert all((b, a) not in edges for a, b in missing)
            groups[str(r['ID'])] = group
            assert all((0, j) in edges and (j, 7) in edges for j in DUST)
        else:
            group = 'mit_staub'
            groups[r['ID']] = group
            crossing = sorted((i,j,c) for (i,j),c in coeff.items()
                              if (i in DUST and j in DEVICE) or (i in DEVICE and j in DUST))
            assert all(i in DUST and j in (19, 20, 21) for i,j,c in crossing)
            assert (0,21) in edges and ((21,7) in edges or (21,8) in edges)
            assert all((0,j) in edges and (j,7) in edges for j in (15,16,17,18))
            dust_bounds[int(r['ID'])] = dust_clocks(cfg['collar'], edges, coeff)
            coupling[r['ID']] = crossing
        rows[int(r['ID'])] = (row, coeff)
    assert {int(k) for k,v in groups.items() if v == 'nur_19'} == {
        int(k) for k, missing in ref['next_decoupled_B_plus'].items() if missing == [[19, 7]]}
    assert {int(k) for k,v in groups.items() if v != 'mit_staub'} == set(map(int, ref['next_decoupled_B_plus']))
    assert len(dust_bounds) == 9 and len(rows) == ref['positive_follower_remaining'] == 40
    assert list(groups.values()).count('nur_19') == 21 and list(groups.values()).count('auch_21') == 10
    # Reuse the archived solver unchanged up to its old command-line interface.
    kernel = (parent/'zweigtest.cpp').read_text()
    driver = 'int main(int argc,char** argv){'
    assert kernel.count(driver) == 1
    (tmp/'zweigkern.hpp').write_text(kernel.partition(driver)[0])
    binary = tmp/'fenster'
    subprocess.run(['g++', '-std=c++17', '-O2', '-fsanitize=signed-integer-overflow',
                    '-fno-sanitize-recover=all', '-I', str(tmp), '-I', str(base),
                    str(ROOT/'fenster.cpp'), '-o', str(binary)], check=True)

    def header(row, witness=None, bounds=None, algebra=False):
        lines = old.input_text(cfg, row, witness).splitlines()
        start = 1 + int(lines[0]) + 8
        for i, j in enumerate(DUST_ORDER):
            assert int(lines[start + i].split()[0]) == j
            lo, hi = bounds[j]['enclosure'] if bounds else (-old.TICKS*5, old.TICKS*2)
            if algebra:
                lo = hi = 0
            lines[start + i] = f'{j} {lo} {hi}'
        return '\n'.join(lines)+'\n'

    def tree(row, sector, cap, depth=76, witness=None, bounds=None):
        args = [str(binary), str(depth), str(cap), str(sector)]
        if witness is not None:
            args.append('control')
        result = subprocess.run(args, input=header(row, witness, bounds), text=True, capture_output=True, check=True)
        mask, sid, nodes, closed, opened, deepest = map(int, result.stdout.split())
        assert mask == row[1] and sid == sector and nodes == 2 * (closed + opened) - 1
        return dict(nodes=nodes, closed=closed, open=opened, depth=deepest, budget=cap)

    algebra = sum(old.action_check(binary, header(row, algebra=True), coeff, cfg['collar'])
                  for row, coeff in rows.values())
    single_clock_entries = sum(check_couplings(binary, header(rows[k][0], algebra=True), rows[k][1])
                               for k in dust_bounds)
    witness_data = json.loads((base / 'Zeugenzentren.json').read_text())
    controls = {}
    for key in ('Zeuge_Kontrolle', 'Zeuge_Rand_zz'):
        w = witness_data[key]
        cert = certify(cfg, w)
        assert all(not (Fraction(lo) <= Fraction(33,64) and Fraction(31,64) <= Fraction(hi))
                   for lo, hi in cert['normalized_clocks'][:2])
        assert tree(w['row'], 0, 1, depth=0, witness=w)['open'] == 1
        controls[key] = {name: cert[name] for name in ('row', 'upper_sum', 'equations', 'normalized_clocks')}
    trees = {str(k): {} for k in rows}
    with ThreadPoolExecutor(max_workers=jobs) as pool:
        futures = {}
        for k, (row, _) in rows.items():
            for sector in range(4):
                cap = (previous['trees'][str(k)][str(sector)]['budget']
                       if previous and str(k) in previous['trees'] else budget)
                fut = pool.submit(tree, row, sector, cap, bounds=dust_bounds.get(k))
                futures[fut] = k, sector
        for future in as_completed(futures):
            k, sector = futures[future]
            result = future.result()
            trees[str(k)][str(sector)] = result
            print(k, sector, result, flush=True)
    removed = sorted(k for k in rows if all(v['open'] == 0 for v in trees[str(k)].values()))
    keep = [r for r in reg if not (r['Sektor'] == 'B+' and int(r['ID']) in removed)]
    buf = io.StringIO()
    writer = csv.DictWriter(buf, fieldnames=list(reg[0]), delimiter='\t', lineterminator='\n')
    writer.writeheader()
    writer.writerows(keep)
    data = dict(parent_sha256=PARENT, cases=ref['cases'], input_open=len(reg), selected=sorted(rows), groups=groups, dust_clocks=dust_bounds, cross_edges=coupling,
                excluded=removed, remaining=len(keep), now_excluded=ref['cases']-len(keep),
                open_by_sector={s: sum(r['Sektor'] == s for r in keep) for s in ('A0','A+','B0','B+')},
                partitions=cfg['pieces'], sources=cfg['sources'], collar=cfg['collar'], action_entries=algebra, single_clock_entries=single_clock_entries,
                controls=controls, P3=ref['P3'], trees=trees)
    data['register_audit'] = audit(base/'Register.tsv.gz', ref['excluded'], removed, keep)
    assert data['register_audit']['cases'] == ref['cases']
    assert data['remaining'] + len(removed) == len(reg)
    return data, buf.getvalue()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--jobs', type=int, default=2)
    parser.add_argument('--budget', type=int, default=512)
    parser.add_argument('--ausgabe', type=Path)
    parser.add_argument('--profil', type=Path, help='Vorherige Stufe. Offene Bäume erhalten das neue Budget.')
    args = parser.parse_args()
    if not __debug__:
        raise RuntimeError('Verifikation erfordert Python ohne -O.')
    if args.jobs < 1 or args.budget < 1:
        parser.error('Jobs und Budget müssen positiv sein.')
    for name in ('Pruefplan', 'Anschluss', 'Staubuhren'):
        assert sha256((ROOT / (name+'.md')).read_bytes()).hexdigest() == (ROOT / (name+'.sha256')).read_text().split()[0]
    ref = None if args.ausgabe else json.loads((ROOT/'Ergebnisse.json').read_text())
    profile = ref
    if args.profil:
        assert args.ausgabe
        profile = json.loads(args.profil.read_text())
        for sectors in profile['trees'].values():
            for t in sectors.values():
                if t['open']:
                    t['budget'] = args.budget
    with TemporaryDirectory() as td:
        data, table = run_test(Path(td), args.jobs, args.budget, profile)
    if args.ausgabe:
        args.ausgabe.mkdir(exist_ok=True, parents=True)
        (args.ausgabe/'Ergebnisse.json').write_text(dump(data))
        (args.ausgabe/'Offene_Faelle.tsv').write_text(table)
    else:
        actual = json.loads(dump(data))
        assert {k:v for k,v in ref.items() if k!='trees'} == {k:v for k,v in actual.items() if k!='trees'}
        for k, sectors in ref['trees'].items():
            for s, t in sectors.items():
                assert (t['open'] == 0) == (actual['trees'][k][s]['open'] == 0)
        assert (ROOT/'Offene_Faelle.tsv').read_text() == table
    print('Entschiedene B+-Fälle', data['excluded'], 'Offene N22-Fälle', data['remaining'])


if __name__ == '__main__':
    main()
