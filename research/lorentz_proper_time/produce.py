"""The one prespecified cohort; coordinates are never passed to inference."""
import json
import resource
import time
from proper_common import HERE, coverage, matching, packet, sample, save, savez
from proper_core import estimates, features, fit_D
from proper_analysis import evaluate


def run(directory):
    cfg = json.loads((HERE/'contract.json').read_text())
    g = cfg['sampling']
    begin = time.perf_counter()
    records = []
    for m in g['m_values']:
        for family in g['families']:
            for split in ['calibration', 'test']:
                count = g['test_per_family_m'] if split == 'test' else g['calibration'][family+'_per_m']
                for draw in range(count):
                    r = sample(family, m, split, draw)
                    r['features'] = features(packet(r))
                    records.append(r)
                print(f'cohort generated: m={m} {family} {split} count={count}', flush=True)
    coverage(records, cfg)
    selection = matching(records, cfg)
    # Matching is persisted before any model fit or prediction/error evaluation.
    savez(directory/'selection.json.gz', selection)
    generation_seconds = time.perf_counter()-begin
    models = {}
    for m in g['m_values']:
        calibration = [r for r in records if r['m'] == m and r['split'] == 'calibration']
        models[str(m)] = fit_D([dict(split='calibration', packet=packet(r), theta=r['theta']) for r in calibration])
        models[str(m)]['calibration_ids'] = [r['id'] for r in calibration]
    for r in records:
        r['predictions'] = estimates(r['features'], models[str(r['m'])])
        r['errors'] = {method: value-r['theta'] for method, value in r['predictions']['clipped'].items()}
    save(directory/'models.json', models)
    savez(directory/'records.json.gz', records)
    report = evaluate(records, selection, cfg)
    save(directory/'summary.json', report)
    save(directory/'costs.json', dict(total_orders=len(records), generation_seconds=generation_seconds,
         total_seconds=time.perf_counter()-begin, process_peak_rss_kib=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
         scope='One Linux run including interpreter; no comparative performance claim.'))


if __name__ == '__main__':
    from pathlib import Path
    import sys
    run(Path(sys.argv[1]))
