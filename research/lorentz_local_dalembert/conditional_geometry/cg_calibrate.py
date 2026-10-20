"""All old PR69 clouds are development now; none counts as new validation."""
import argparse
import hashlib
import json
import zipfile
import numpy as np
from cg_common import HERE, BASE, config, contract, encode, digest, sources
from cg_inference import prepare
from run_calibration import coordinates_only
from cg_run import evaluate


def main():
    p = argparse.ArgumentParser()
    p.add_argument('--output', default='frozen_calibration.json')
    args = p.parse_args()
    destination = HERE/args.output
    if destination.exists():
        raise SystemExit('Refusing to overwrite calibration')
    c = contract()
    _, oc, _, _ = config()
    archive = BASE/'feynman_combiner/independent_clouds.zip'
    rows = []
    with zipfile.ZipFile(archive) as zf:
        for name in sorted(zf.namelist()):
            if not name.endswith('.json') or '/seed-' not in name:
                continue
            raw = zf.read(name)
            row = json.loads(raw)
            z = coordinates_only(row['rho'], row['seed'], oc)
            assert digest(z) == row['coordinates_sha256']
            w = row['selection']['selected']
            if w is None:
                r = np.zeros((0, 0), bool)
            else:
                # Retrospective simulator replay restores the archived observed
                # order. Only this binary matrix enters prepare(), never z.
                ids = [w['root']]+w['support']
                a = z[ids]
                dt = a[None, :, 0]-a[:, None, 0]
                ds = a[None, :, 1:]-a[:, None, 1:]
                r = (dt > 0) & (dt*dt > np.sum(ds*ds, axis=2))
            intrinsic = prepare(w, r, row['joint_pass'])
            evaluation = evaluate(intrinsic, w, z, row['seed'])
            rows.append(dict(seed=row['seed'], source_file=name,
                             source_sha256=hashlib.sha256(raw).hexdigest(),
                             intrinsic=intrinsic, evaluation=evaluation))
    assert len(rows) == 64
    good = [r for r in rows if r['evaluation']['status'] == 'COMPLETE']
    out = dict(status='HOLD', total=len(rows), complete=len(good),
               source_sha256=sources(), development_archive_sha256=hashlib.sha256(archive.read_bytes()).hexdigest(),
               scope='All 64 former PR69 calibration AND test clouds reused as development; clean simulation-assisted calibration.')
    if len(good) >= c['minimum_calibration_complete']:
        errors = np.array([r['evaluation']['clean'] for r in good])+.75
        g = np.cov(errors, rowvar=False)
        out.update(status='FROZEN', bias=errors.mean(axis=0).tolist(), geometry_covariance=g.tolist(),
                   bias_mean_covariance=(g/len(good)).tolist(),
                   mean_noise_covariance=np.mean([r['intrinsic']['conditional_field_covariance'] for r in good], axis=0).tolist())
    destination.write_text(json.dumps(out, indent=2)+'\n')
    (HERE/'development_records.json').write_text(encode(rows))
    print(json.dumps({k:v for k,v in out.items() if k!='source_sha256'}, indent=2))


if __name__ == '__main__':
    main()
