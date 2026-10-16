"""Fixed losses and whole-order/pair bootstrap, with calibration held fixed."""
import math
import numpy as np
from proper_common import MODELS, NS, Stream
from proper_core import require


def resamples(count, repeats, key):
    rng = Stream(*key)
    return np.fromiter((rng.below(count) for _ in range(count*repeats)), dtype=np.int32).reshape(repeats, count)


def interval(x):
    return np.quantile(x, [0.025, 0.975], method='linear').tolist()


def metrics(records, indices):
    truth = np.asarray([r['theta'] for r in records])
    out, losses = {}, {}
    for model in MODELS:
        error = np.asarray([r['predictions']['clipped'][model] for r in records])-truth
        sq = error*error
        losses[model] = sq
        boot = sq[indices].mean(axis=1)
        out[model] = dict(count=len(records), mse=float(sq.mean()), rmse=math.sqrt(float(sq.mean())),
                          mae=float(np.abs(error).mean()), bias=float(error.mean()),
                          mse_bootstrap_95=interval(boot), rmse_bootstrap_95=interval(np.sqrt(boot)),
                          mae_bootstrap_95=interval(np.abs(error)[indices].mean(axis=1)),
                          bias_bootstrap_95=interval(error[indices].mean(axis=1)))
    a_error = np.asarray([r['features']['K']/r['m']-r['a'] for r in records])
    diff = {base: dict(mse_difference=float((losses['V']-losses[base]).mean()),
                      paired_bootstrap_95=interval((losses['V']-losses[base])[indices].mean(axis=1))) for base in ['D', 'C0']}
    return dict(methods=out, comparisons=diff, zero_K=sum(r['features']['K'] == 0 for r in records),
                squared_time=dict(bias=float(a_error.mean()), mse=float(np.mean(a_error*a_error)),
                                  iid_uniform_analytic_mse=1/(12*records[0]['m'])),
                scope='Fixed calibration; analytic formula applies only to unselected uniform continuum model.')


def primary_decision(cell):
    v = cell['methods']['V']
    gates = dict(rmse_at_most_005=v['rmse'] <= 0.05)
    for base in ['D', 'C0']:
        gates['mse_reduction_'+base] = v['mse'] <= 0.90*cell['methods'][base]['mse']
        gates['bootstrap_upper_negative_'+base] = cell['comparisons'][base]['paired_bootstrap_95'][1] < 0
    return dict(status='QUALIFIED_IN_DECLARED_MODEL' if all(gates.values()) else 'NO_QUALIFICATION_DEMONSTRATED',
                family='uniform', m=256, gates=gates, integrity_required=True)


def evaluate(records, selection, cfg):
    repeats = cfg['evaluation']['bootstrap']['replicates']
    cells = {}
    for m in cfg['sampling']['m_values']:
        for family in cfg['sampling']['families']:
            rr = [r for r in records if r['m'] == m and r['family'] == family and r['split'] == 'test']
            ix = resamples(len(rr), repeats, [NS, 'bootstrap', family, m])
            cells[f'{family}/m{m}'] = metrics(rr, ix)
    matched = {}
    lookup = {r['id']: r for r in records}
    for key, cell in selection.items():
        if cell['status'] != 'EVALUABLE':
            matched[key] = dict(status=cell['status'], eligible=cell['eligible'])
            continue
        pairs = cell['selected_pairs']
        uu, jj = [[lookup[pair['ids'][k]] for pair in pairs] for k in [0, 1]]
        require(all(a['features']['R'] == b['features']['R'] and a['features']['H'] == b['features']['H']
                    and a['predictions']['clipped']['D'] == b['predictions']['clipped']['D'] for a, b in zip(uu, jj)), 'matched nuisance equality')
        ix = resamples(len(pairs), repeats, [NS, 'matched-bootstrap', cell['m']])
        transfer = {}
        for method in MODELS:
            delta = np.asarray([(b['predictions']['clipped'][method]-b['theta'])**2
                                -(a['predictions']['clipped'][method]-a['theta'])**2 for a, b in zip(uu, jj)])
            transfer[method] = dict(jittered_minus_uniform_mse=float(delta.mean()), paired_bootstrap_95=interval(delta[ix].mean(axis=1)))
        matched[key] = dict(status='EVALUABLE', pairs=len(pairs), uniform=metrics(uu, ix), jittered_grid=metrics(jj, ix), transfer=transfer)
    p = cfg['evaluation']['primary']
    return dict(primary=primary_decision(cells[f"{p['family']}/m{p['m']}"]), cells=cells, matched=matched,
                repeats=repeats, caveat='Conditional bootstrap holds calibration fixed; generator transfer is descriptive; no geometry certificate.')
