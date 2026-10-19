"""Complete replay, independent finite controls, and immutable input checks."""
import json
import resource
import signal
import time
import numpy as np
from run_availability import HERE, ROOT, controls, inherited, digest, source_hashes, run_record, summarize


def compare(a, b):
    if isinstance(a, dict):
        assert a.keys() == b.keys()
        for key in a:
            compare(a[key], b[key])
    elif isinstance(a, list):
        assert len(a) == len(b)
        for x, y in zip(a, b):
            compare(x, y)
    elif isinstance(a, float):
        np.testing.assert_allclose(a, b, atol=1e-9, rtol=1e-9)
    else:
        assert a == b, (a, b)


def main():
    start = time.monotonic()
    def timeout(signum, frame):
        raise TimeoutError('1200-second replay budget')
    signal.signal(signal.SIGALRM, timeout)
    signal.alarm(1200)
    folder = HERE / 'results'
    execution = json.loads((folder / 'execution.json').read_text())
    assert execution['status'] == 'COMPLETE' and len(execution['records']) == 48
    assert execution['seconds'] <= 1200 and execution['peak_mib'] <= 2048
    assert source_hashes() == execution['source_sha256']
    check = controls.check(inherited.core)
    assert check == execution['controls']
    inputs = HERE.parent / 'intrinsic_moments/results'
    original_manifest = json.loads((inputs / 'execution.json').read_text())
    original_hashes = {r['file']: r['sha256'] for r in original_manifest['records']}
    assert {r['file'] for r in execution['records']} == set(original_hashes)
    rows, checked = [], set()
    archive_matches = replay_matches = 0
    for entry in execution['records']:
        stored = folder / entry['file']
        original = inputs / entry['file']
        assert digest(stored) == entry['sha256']
        assert digest(original) == entry['input_sha256'] == original_hashes[entry['file']]
        old = json.loads(original.read_text())
        transport = old['rho'] not in checked and old['selection']['status'] == 'ok'
        row = run_record(old, transport)
        if transport:
            checked.add(old['rho'])
        expected = json.loads(stored.read_text())
        assert row['discrete'] == expected['discrete']
        for key in ('rho', 'seed', 'status', 'controls'):
            assert row[key] == expected[key]
        compare(row['continuum_volume_proxy'], expected['continuum_volume_proxy'])
        archive_matches += row['coordinate_bytes_match_archive']
        replay_matches += row['coordinates_sha256'] == expected['coordinates_sha256']
        rows.append(row)
        if resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / 1024 > 2048:
            raise MemoryError('2048-MiB replay budget')
    assert digest(folder / 'summary.json') == execution['summary_sha256']
    assert summarize(rows) == json.loads((folder / 'summary.json').read_text())
    signal.alarm(0)
    print(json.dumps(dict(status='PASS_NUMERICAL_REPLAY', clouds=len(rows), controls=check,
                         transport_densities=sorted(checked), exact_discrete=True,
                         original_coordinate_byte_matches=archive_matches,
                         audit_coordinate_byte_matches=replay_matches,
                         seconds=time.monotonic()-start,
                         peak_mib=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss/1024), indent=2))


if __name__ == '__main__':
    main()
