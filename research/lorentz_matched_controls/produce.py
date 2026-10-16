"""Generate every fixed candidate, select without features, then evaluate."""
import json
import math
import resource
import time
from common import (HERE, ledger_entry, matrix, prior_geometry, require, sample, save,
                    savez, select, selected_ids, validate_ledger)
import analysis


def run(directory):
    cfg = json.loads((HERE/'contract.json').read_text())
    begin = time.perf_counter()
    ledger = []
    for n in cfg['generators']['sizes']:
        for family in cfg['generators']['families']:
            for split in cfg['generators']['splits']:
                for draw in range(cfg['generators']['pool_per_family_size_split']):
                    ledger.append(ledger_entry(sample(family, n, split, draw)))
            print(f'pool complete: n={n} family={family}', flush=True)
    validate_ledger(ledger, cfg)
    selection = select(ledger, cfg)
    # Selection is persisted before computing any candidate feature vectors.
    savez(directory/'candidate_ledger.json.gz', ledger)
    savez(directory/'selection.json.gz', selection)
    selection_seconds = time.perf_counter()-begin
    lookup = {r['id']: r for r in ledger}
    records = []
    for name in selected_ids(selection):
        entry = lookup[name]
        r = sample(entry['family'], entry['n'], entry['split'], entry['draw'])
        require(ledger_entry(r) == entry, 'selected raw observation replay')
        r['features'] = prior_geometry.features(matrix(r))
        require(r['features']['height'] == entry['H'] and sum(r['features']['interval_histogram']) == entry['R'], 'selection features agree')
        r['features']['D'] = [entry['R']/math.comb(entry['n'], 2), entry['H']/entry['n']]
        records.append(r)
    report = analysis.evaluate(selection, records, cfg)
    savez(directory/'selected_records.json.gz', records)
    savez(directory/'evaluation.json.gz', report)
    save(directory/'summary.json', analysis.summarize(report))
    save(directory/'support.json', {key: dict(status=cell['status'], n=cell['n'], control=cell['control'],
         train_eligible=cell['train']['eligible'], test_eligible=cell['test']['eligible'],
         train_used=len(cell['train']['pairs']) if cell['status'] == 'EVALUABLE' else 0,
         test_used=len(cell['test']['pairs']) if cell['status'] == 'EVALUABLE' else 0)
         for key, cell in selection.items()})
    save(directory/'costs.json', dict(total_candidates=len(ledger), selected_unique_observations=len(records),
         pool_and_selection_seconds=selection_seconds, total_seconds=time.perf_counter()-begin,
         process_peak_rss_kib=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
         warning='Single Linux run, including interpreter and NumPy; no performance comparison.'))


if __name__ == '__main__':
    from pathlib import Path
    import sys
    run(Path(sys.argv[1]))
