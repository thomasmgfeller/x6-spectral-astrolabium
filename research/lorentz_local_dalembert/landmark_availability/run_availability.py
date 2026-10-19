"""Replay archived clouds for retrospective, conditional landmark diagnostics."""
import argparse
import hashlib
import json
import resource
import signal
import subprocess
import sys
import time
from pathlib import Path
import numpy as np

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
sys.path.insert(0, str(HERE.parent / 'intrinsic_moments'))
import im_common as inherited
from availability import diagnose
# Avoid the unrelated inherited module also named controls.
import importlib.util
spec = importlib.util.spec_from_file_location('availability_controls', HERE / 'controls.py')
controls = importlib.util.module_from_spec(spec)
spec.loader.exec_module(controls)


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def source_hashes():
    return {**inherited.sources(), **{str(p.relative_to(ROOT)): digest(p)
            for p in sorted(HERE.iterdir()) if p.suffix == '.py' or p.name == 'PROTOCOL.md'}}


def run_record(old, check_transport=False):
    rho, seed = old['rho'], old['seed']
    z, relation, marks, bottom, top = inherited.experiment.sprinkle(rho, seed)
    assert hashlib.sha256(relation.tobytes()).hexdigest() == old['relation_sha256']
    assert hashlib.sha256(marks.tobytes()).hexdigest() == old['marks_sha256']
    g = inherited.core.Poset(relation, marks)
    s = old['selection']
    discrete = diagnose(g, s, [bottom, top])
    if s['status'] == 'ok':
        original = old['inference']['frame']
        assert original['status'] == 'no_admissible_frame'
        full = discrete['views']['full']
        for item in original['candidates']:
            assert full[item['side']]['capped40']['candidates'] == item['count']
        assert sum(v['capped40']['triples']['8'] for v in full.values()) == original['eligible_triples']
        checks = controls.transport(inherited.core, g, s, [bottom, top], discrete, seed) if check_transport else None
        def exact_volume(a, b):
            delta = z[b] - z[a]
            tau2 = max(0., delta[0] ** 2 - float(delta[1:] @ delta[1:]))
            return float(rho * inherited.core.VOLUME * tau2 ** 1.5)
        geometric = diagnose(g, s, [bottom, top], exact_volume)
    else:
        geometric, checks = dict(status=s['status']), None
    return dict(rho=rho, seed=seed, status=s['status'], discrete=discrete,
                continuum_volume_proxy=geometric, controls=checks,
                coordinates_sha256=hashlib.sha256(z.tobytes()).hexdigest(),
                coordinate_bytes_match_archive=hashlib.sha256(z.tobytes()).hexdigest() == old['coordinates_sha256'])


def summarize(rows):
    result = dict(status='DIAGNOSTIC_COMPLETE', scientific_status='HOLD_PHASE3',
                  intrinsic_status='INTRINSIC_MOMENT_HOLD', bd_c2='NO_GO',
                  clouds=len(rows), available=sum(r['status'] == 'ok' for r in rows), densities={})
    for rho in sorted({r['rho'] for r in rows}):
        sample = [r for r in rows if r['rho'] == rho]
        available = [r for r in sample if r['status'] == 'ok']
        out = dict(clouds=len(sample), available=len(available), views={})
        for view in ('full', 'temporal', 'shell', 'root'):
            v = {}
            for kind in ('discrete', 'continuum_volume_proxy'):
                data = [r[kind]['views'][view] for r in available]
                v[kind] = {cap: {str(k): sum(any(s[cap]['triples'][str(k)] > 0 for s in d.values()) for d in data)
                                for k in (0, 1, 2, 4, 8, 16)} for cap in ('all', 'capped40')}
                v[kind]['side_candidate_totals'] = {
                    side: sum(d[side]['all']['candidates'] for d in data) for side in ('past', 'future')}
                if kind == 'discrete':
                    v[kind]['both_sides_packing_impossible'] = sum(all(s['packing_impossible'] for s in d.values()) for d in data)
            out['views'][view] = v
        result['densities'][str(rho)] = out
    return result


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    if args.output.exists():
        raise SystemExit('Refusing to overwrite output')
    inputs = HERE.parent / 'intrinsic_moments/results'
    archive = json.loads((inputs / 'execution.json').read_text())
    assert archive['status'] == 'COMPLETE' and len(archive['records']) == 48
    for p, sha in archive['source_sha256'].items():
        assert digest(ROOT / p) == sha, 'changed inherited source: ' + p
    check = controls.check(inherited.core)
    args.output.mkdir(parents=True)
    start = time.monotonic()
    execution = dict(status='RUNNING', kind='RETROSPECTIVE_CONDITIONAL_DIAGNOSIS',
                     base_commit='760c3c29f15a4d083ff2696351e733d257cfeee1',
                     source_commit=subprocess.check_output(['git', 'rev-parse', 'HEAD'], cwd=ROOT, text=True).strip(),
                     source_sha256=source_hashes(), numpy=np.__version__, controls=check, records=[])
    def save():
        (args.output / 'execution.json').write_text(json.dumps(execution, indent=2) + '\n')
    def timeout(signum, frame):
        raise TimeoutError('1200-second wall budget')
    signal.signal(signal.SIGALRM, timeout)
    signal.alarm(1200)
    rows, checked = [], set()
    try:
        for entry in archive['records']:
            path = inputs / entry['file']
            assert digest(path) == entry['sha256']
            old = json.loads(path.read_text())
            transport = old['rho'] not in checked and old['selection']['status'] == 'ok'
            row = run_record(old, transport)
            if transport:
                checked.add(old['rho'])
            rows.append(row)
            target = args.output / entry['file']
            target.write_text(json.dumps(row, indent=2) + '\n')
            execution['records'].append(dict(file=entry['file'], sha256=digest(target), input_sha256=entry['sha256']))
            save()
            print(json.dumps(dict(rho=row['rho'], seed=row['seed'], status=row['status'])), flush=True)
            if resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / 1024 > 2048:
                raise MemoryError('2048-MiB RSS budget')
        summary = summarize(rows)
        (args.output / 'summary.json').write_text(json.dumps(summary, indent=2) + '\n')
        execution.update(status='COMPLETE', summary_sha256=digest(args.output / 'summary.json'))
    except Exception as exc:
        execution.update(status='ERROR', error=repr(exc))
        raise
    finally:
        signal.alarm(0)
        execution.update(seconds=time.monotonic()-start,
                         peak_mib=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss/1024)
        save()


if __name__ == '__main__':
    main()
