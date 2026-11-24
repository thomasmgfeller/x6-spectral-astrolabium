"""Separate defensiv gewichtete Gegenrechnung zu den Sobol-Integralen."""
import argparse
import csv
import hashlib
import json
from pathlib import Path

import priorlauf as main
from priorlauf import np, lauf, ROOT
from scipy.special import logsumexp
from scipy.stats import multivariate_normal, multivariate_t

COUNTS = np.array([1024, 2048, 5120])
FRACTIONS = COUNTS / COUNTS.sum()
SEED = 936520261124
DIM = 4
DF = 5

def train(archive, target):
    lines = (ROOT/'basis/original_SHA256SUMS').read_text().splitlines()
    expected, = [line.split()[0] for line in lines if line.split()[-1]=='resultate/historien.npz']
    with archive.open('rb') as f:
        digest = hashlib.file_digest(f,'sha256').hexdigest()
    if digest != expected:
        raise ValueError('SHA-256 des Trainingsarchivs weicht ab')
    with np.load(archive) as d:
        coeff = d['coefficients'][:,:DIM]
        ll = lauf.log_like(d['rows'])
    parameters = []
    for col in ll.T:
        mass = np.exp(col-logsumexp(col))
        centre = mass @ coeff
        dev = coeff-centre
        cov = (dev.T * mass) @ dev
        scale = (DF-2)/DF * 1.25**2 * cov + .05**2*np.eye(DIM)
        parameters.append(dict(centre=centre.tolist(),scale=scale.tolist()))
    target.write_text(json.dumps(dict(source_sha256=digest,components=parameters),indent=2)+'\n')

def run(cache, out, proposal):
    files = lauf.ref.inputs(cache)
    bao, sn = lauf.ref.BAO(files), lauf.ref.Pantheon(files)
    log_ref = lauf.reference(bao,sn,32)
    logz = np.log1p(bao.z)
    curve = lauf.Curve(np.r_[bao.z,sn.distance.z])
    design = lauf.basis(-logz)
    pars = json.loads(proposal.read_text())['components']
    values = [multivariate_normal(np.zeros(DIM),np.eye(DIM))]
    for p in pars:
        values.append(multivariate_t(p['centre'],p['scale'],df=DF))
    records = []
    sq_sum = np.zeros((3,2))
    for k, seed in enumerate(np.random.SeedSequence(SEED).spawn(16)):
        rng = np.random.Generator(np.random.PCG64(seed))
        coeff = np.empty((sum(COUNTS),lauf.MODES))
        coeff[:,:DIM] = np.vstack([v.rvs(size=int(n),random_state=rng) for n,v in zip(COUNTS,values)])
        coeff[:,DIM:] = rng.standard_normal((len(coeff),lauf.MODES-DIM))
        log_p = values[0].logpdf(coeff[:,:DIM])
        log_q = logsumexp(np.stack([v.logpdf(coeff[:,:DIM]) for v in values],axis=1),
                          b=FRACTIONS,axis=1)
        w = np.exp(log_p-log_q)
        if np.max(w)>8+1e-12:
            raise ArithmeticError('Verletzte Schranke für das Vorschlagsgewicht')
        ratios = np.empty((len(coeff),3,2))
        for i in range(0,len(coeff),lauf.BATCH):
            sl = slice(i,i+lauf.BATCH)
            c = coeff[sl].T
            dm = curve.comoving(c)
            m = np.exp(lauf.log_matter_fraction(main.ENDPOINT @ c))
            rows = lauf.evaluate(bao,sn,dm[:len(bao.z)],lauf.inv_e(logz,c,design),dm[len(bao.z):],m)
            baseline = np.exp(lauf.log_like(rows)-log_ref)*w[sl,None]
            narrowed, flat = main.endpoint_weights(m)
            for a, multiplier in enumerate([np.ones(len(m)),narrowed,flat]):
                ratios[sl,a] = baseline*multiplier[:,None]
        sq_sum += np.sum(ratios**2,axis=0)
        mean = ratios.mean(axis=0)
        records.append(dict(stream=k,prior_weight_mean=float(w.mean()),
                            **{f'{name}_{survey}':mean[a,b] for a,name in enumerate(('native','restricted','uniform'))
                               for b,survey in enumerate(main.DATA)}))
    out.mkdir(exist_ok=True,parents=True)
    with (out/'importance_stroeme.csv').open('w',newline='') as f:
        wr = csv.DictWriter(f,fieldnames=list(records[0]))
        wr.writeheader()
        wr.writerows(records)

    def stats(x):
        return dict(mean=float(x.mean()),se=float(x.std(ddof=1)/np.sqrt(len(x))))

    cols = {key:np.array([r[key] for r in records]) for key in records[0]}
    n = len(records)*sum(COUNTS)
    summary = {k:stats(x) for k,x in cols.items() if k!='stream'}
    for a,name in enumerate(('native','restricted','uniform')):
        for b,survey in enumerate(main.DATA):
            item = summary[f'{name}_{survey}']
            item['weight_ess'] = float((n*item['mean'])**2/sq_sum[a,b])
    primary = json.loads((ROOT/'resultate/ergebnis.json').read_text())['levels_results']['16384']
    differences = {}
    passed = {}
    for name,key in [('native','native'),('uniform','uniform_direct')]:
        u = summary[name+'_DESI_Pantheon']
        v = primary[key]['DESI_Pantheon']
        z = abs(u['mean']-v['mean'])/np.hypot(u['se'],v['se'])
        differences[name] = float(z)
        passed['sobol_'+name] = bool(z <= 3)
        passed['precision_'+name] = bool(u['se']/u['mean'] < .05)
    passed['mean_prior_weight'] = bool(abs(summary['prior_weight_mean']['mean']-1) < .02)
    paired = {}
    for label, a, b in [('restriction','restricted','native'),('within_interval','uniform','restricted'),
                         ('total','uniform','native')]:
        x,y = [cols[t+'_DESI_Pantheon'] for t in (a,b)]
        ratio = x.mean()/y.mean()
        paired[label] = dict(mean=float(ratio),se=float((x-ratio*y).std(ddof=1)/4/y.mean()))
    result = dict(seed=SEED, count=int(n), streams=16, per_stream=COUNTS.tolist(),
                  estimates=summary, joint_factors=paired,
                  joint_difference_from_sobol_in_standard_errors=differences, gates=passed)
    (out/'importance.json').write_text(json.dumps(result,indent=2,allow_nan=False)+'\n')
    print(json.dumps(result,indent=2))

if __name__ == '__main__':
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--cache',type=Path,default=ROOT/'cache')
    p.add_argument('--out',type=Path,default=ROOT/'resultate')
    p.add_argument('--proposal',type=Path,default=ROOT/'vorschlag.json')
    p.add_argument('--train',type=Path,help='Nur Vorschlag aus dem Originalarchiv neu aufbauen')
    args = p.parse_args()
    if args.train:
        train(args.train,args.proposal)
    else:
        run(args.cache,args.out,args.proposal)
