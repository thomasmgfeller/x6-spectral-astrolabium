"""Old clouds only; four transfer probes are not evaluated during fitting."""
import hashlib
import json
import zipfile
import numpy as np
from mb_common import HERE, BASE, contract, config, sources, write_json, digest
from mb_model import ARMS, basis, fit, corrected, prepare
from mb_fields import values, evaluate
from run_calibration import coordinates_only


def archived():
    cfg = contract()
    with zipfile.ZipFile(BASE/'conditional_geometry/development_records.zip') as z:
        intrinsic = {r['seed']:r['intrinsic'] for r in json.loads(z.read('development_records.json'))}
    groups = []
    for path in [cfg['training_archive'], cfg['residual_calibration_archive']]:
        rows = []
        with zipfile.ZipFile(BASE/path) as z:
            for name in sorted(z.namelist()):
                if '/seed-' not in name or not name.endswith('.json'):
                    continue
                row = json.loads(z.read(name))
                if path == cfg['training_archive']:
                    row['intrinsic'] = intrinsic[row['seed']]
                rows.append(row)
        groups.append(sorted(rows, key=lambda r:r['seed']))
    return groups


def main():
    target = HERE/'frozen_model.json'
    if target.exists():
        raise SystemExit('Refusing to overwrite frozen calibration')
    cfg = contract()
    _, oc, _, _ = config()
    training, calibration = archived()
    assert len(training) == 64 and len(calibration) == 32
    assert not ({r['seed'] for r in training} & {r['seed'] for r in calibration})
    good = [r for r in training if r['intrinsic']['status']=='COMPLETE']
    assert len(good) >= cfg['minimum_training_complete']
    samples = [[], []]
    for row in good:
        z = coordinates_only(row['rho'], row['seed'], oc)
        assert digest(z)==row['coordinates_sha256']
        selected = row['selection']['selected']
        delta = z[selected['support']]-z[selected['root']]
        pairs = [values(delta, spec) for spec in cfg['training_fields']]
        contrasts = np.array([p[0] for p in pairs])
        truths = np.array([p[1] for p in pairs])
        for arm in [0, 1]:
            b = basis(row['intrinsic'], arm)
            errors = contrasts@b['a']/b['scale']**2-truths
            samples[arm].append(dict(seed=row['seed'], basis=b, contrasts=contrasts,
                                     errors=errors, truths=truths))
    order = np.random.default_rng(cfg['cv_seed']).permutation(len(good))
    folds = np.array_split(order, cfg['cv_folds'])
    models, scores = {}, {}
    for arm in [0,1]:
        for use_meta in [False, True]:
            name = (['metadata','projected_metadata'] if use_meta else
                    ['constant_ablation','projected_constant_ablation'])[arm]
            scores[name] = []
            for ridge in cfg['ridge_candidates']:
                errors = []
                for held in folds:
                    train = [s for i,s in enumerate(samples[arm]) if i not in held]
                    test = [samples[arm][i] for i in held]
                    assert not ({s['seed'] for s in train} & {s['seed'] for s in test})
                    model = fit(train, ridge, use_meta)
                    for s in test:
                        a, _ = corrected(s['basis'], model)
                        errors.extend(s['contrasts']@a/s['basis']['scale']**2-s['truths'])
                scores[name].append(dict(ridge=ridge, rmse=float(np.sqrt(np.mean(np.array(errors)**2)))))
            best = min(scores[name], key=lambda v:(v['rmse'], -v['ridge']))
            models[name] = fit(samples[arm], best['ridge'], use_meta)
    residuals, records = [], []
    for row in calibration:
        prepared = prepare(row['intrinsic'], models)
        z = coordinates_only(row['rho'], row['seed'], oc)
        assert digest(z)==row['coordinates_sha256']
        evaluation = evaluate(prepared, row['selection']['selected'], z, row['seed'])
        records.append(dict(seed=row['seed'], prepared=prepared, evaluation=evaluation))
        if evaluation['status']=='COMPLETE':
            residuals.append([[v-vv['truth'] for v in vv['clean']] for vv in evaluation['fields']])
    assert len(residuals) >= cfg['minimum_calibration_complete']
    residuals = np.array(residuals)
    pooled = residuals.reshape(-1,len(ARMS))
    mean = pooled.mean(axis=0)
    covariance = (pooled-mean).T@(pooled-mean)/len(pooled)
    second = pooled.T@pooled/len(pooled)
    np.testing.assert_allclose(second, covariance+np.outer(mean,mean), atol=1e-12)
    out = dict(status='FROZEN', scope=cfg['scope'], source_sha256=sources(),
               training_clouds=len(training), training_complete=len(good),
               calibration_clouds=len(calibration), calibration_complete=len(residuals),
               training_seeds=[r['seed'] for r in training], calibration_seeds=[r['seed'] for r in calibration],
               cv_folds=[[good[i]['seed'] for i in fold] for fold in folds], cv_scores=scores, models=models,
               residual_mean=mean.tolist(), residual_covariance=covariance.tolist(),
               residual_second_moment=second.tolist(),
               noise_strata_edges=np.quantile(np.exp([s['basis']['metadata'][0] for s in samples[0]]),[1/3,2/3]).tolist(),
               archive_sha256={p:hashlib.sha256((BASE/p).read_bytes()).hexdigest() for p in
                               [cfg['training_archive'],cfg['residual_calibration_archive'],
                                'conditional_geometry/development_records.zip']})
    with zipfile.ZipFile(HERE/'residual_calibration.zip','w',zipfile.ZIP_DEFLATED) as z:
        z.writestr('records.json', json.dumps(records, allow_nan=False))
    write_json(target, out)
    print(json.dumps(dict(training_complete=len(good), calibration_complete=len(residuals),
                         selected_ridges={k:v['ridge'] for k,v in models.items()}, cv_scores=scores),indent=2))


if __name__=='__main__':
    main()
