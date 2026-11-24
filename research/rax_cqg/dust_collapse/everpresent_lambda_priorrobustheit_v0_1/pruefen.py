"""Check inputs, protocol, and reported estimates without rerunning the sky likelihood."""
import csv
import hashlib
import json
from math import atanh, erf, exp, isclose, pi, sqrt
from pathlib import Path
from statistics import mean, stdev

ROOT = Path(__file__).resolve().parent


def check_sums(folder, sums, names=None):
    hashes = {}
    for line in sums.read_text().splitlines():
        digest, name = line.split(None, 1)
        hashes[name.removeprefix('*')] = digest
    pairs = names or {name:name for name in hashes}
    for local, original in pairs.items():
        data = (folder/local).read_bytes()
        if hashlib.sha256(data).hexdigest() != hashes[original]:
            raise ValueError(f'Prüfsummenfehler in {local}')


def near(a,b):
    if not isclose(a,b,rel_tol=2e-11,abs_tol=5e-13):
        raise ValueError(f'{a} und {b} stimmen nicht überein')


def main():
    check_sums(ROOT,ROOT/'protokoll.sha256')
    check_sums(ROOT,ROOT/'zusatzprotokoll.sha256')
    check_sums(ROOT,ROOT/'SHA256SUMS')
    base = ROOT/'basis'
    names = {name:name for name in ('lauf.py','gegenprobe.py','pipeline/ergebnis.json',
             'pipeline/datenpilot.py','pipeline/quelldaten.json','pipeline/LICENSE','pipeline/NOTICE')}
    names['erstlauf.json'] = 'resultate/ergebnis.json'
    check_sums(base,base/'original_SHA256SUMS',names)
    out = ROOT/'resultate'
    results = json.loads((out/'ergebnis.json').read_text())
    old = json.loads((base/'erstlauf.json').read_text())
    with (out/'netze.csv').open() as f:
        rows = list(csv.DictReader(f))
    if len(rows) != 48:
        raise ValueError('Unvollständige Netztabelle')
    for n in (4096,8192,16384):
        group = [r for r in rows if int(r['n'])==n]
        if sorted(int(r['replicate']) for r in group) != list(range(16)):
            raise ValueError('Fehlende oder doppelte Replikate')
        estimates = results['levels_results'][str(n)]
        for name in ('native','uniform_direct','uniform_weighted','restricted'):
            for survey in ('DESI','DESI_Pantheon'):
                sample = [float(r[f'{name}_{survey}']) for r in group]
                near(mean(sample),estimates[name][survey]['mean'])
                near(stdev(sample)/4,estimates[name][survey]['se'])
        for survey in ('DESI','DESI_Pantheon'):
            diffs = [float(r['uniform_direct_'+survey])-float(r['uniform_weighted_'+survey]) for r in group]
            direct_minus = estimates['paired'][survey]['direct_minus_reweighted']
            near(mean(diffs),direct_minus['mean'])
            near(stdev(diffs)/4,direct_minus['se'])
            for label, num, den in (('restriction_factor','restricted','native'),
                                    ('within_interval_factor','uniform_direct','restricted'),
                                    ('uniform_to_native','uniform_direct','native')):
                a = [float(r[num+'_'+survey]) for r in group]
                b = [float(r[den+'_'+survey]) for r in group]
                f = mean(a)/mean(b)
                near(f,estimates['paired'][survey][label]['mean'])
                near(stdev(x-f*y for x,y in zip(a,b))/(4*mean(b)),estimates['paired'][survey][label]['se'])
    # Area under the truncated induced density via its Gaussian antiderivative.
    sigma = results['endpoint_sigma']
    near(sigma,0.8824)
    hi = atanh(0.99)/(sigma*sqrt(2))
    lo = atanh(0.01)/(sigma*sqrt(2))
    mass = (erf(hi)-erf(lo))/2
    near(mass,results['native_interval_mass'])
    # Constant-observable identity via independent midpoint integration over m.
    nint = 100_000
    width = 0.98/nint
    density_sum = 0.
    for i in range(nint):
        m = 0.01+(i+0.5)*width
        g = atanh(1-m)
        density_sum += exp(-0.5*(g/sigma)**2)/(sqrt(2*pi)*sigma*m*(2-m))
    if abs(density_sum*width-mass) > 1e-8:
        raise ValueError('Analytische Intervallmasse stimmt nicht')
    final = results['levels_results']['16384']
    native, flat = [final[k]['DESI_Pantheon'] for k in ('native','uniform_direct')]
    previous = old['ensemble']['BAO_SN']
    z_old = abs(native['mean']-previous['ratio'])/sqrt(native['se']**2+previous['MC_se_iid']**2)
    diff = final['paired']['DESI_Pantheon']['direct_minus_reweighted']
    z_pair = abs(diff['mean']/diff['se'])
    near(z_old,results['prior_replication_z'])
    near(z_pair,results['paired_method_z'])
    err = max(abs(x-old['ensemble'][k]['log_Z_ref']) for x,k in zip(results['log_reference'],('BAO','BAO_SN')))
    near(err,results['reference_error'])
    g = {'reference':err<1e-8,
         'independent_distance':max(r['relative_max'] for r in results['distances'])<1e-7,
         'repeat_native':z_old<=3,'methods_uniform':z_pair<=3}
    for key,value in [('native',native),('uniform',flat)]:
        g['precision_'+key] = value['se']/value['mean'] < 0.10
        g['direction_'+key] = value['mean']+3*value['se'] < 1
    if g != results['gates']:
        raise ValueError('Prüfentscheid stimmt nicht mit Daten überein')
    imp = json.loads((out/'importance.json').read_text())
    with (out/'importance_stroeme.csv').open() as f:
        independent = list(csv.DictReader(f))
    if [int(r['stream']) for r in independent] != list(range(16)):
        raise ValueError('Fehlende unabhängige Kontrollströme')
    for k, info in imp['estimates'].items():
        data = [float(r[k]) for r in independent]
        near(mean(data),info['mean'])
        near(stdev(data)/4,info['se'])
    for name,num,den in [('restriction','restricted','native'),('within_interval','uniform','restricted'),
                         ('total','uniform','native')]:
        a,b = [[float(r[t+'_DESI_Pantheon']) for r in independent] for t in (num,den)]
        ratio = mean(a)/mean(b)
        near(ratio,imp['joint_factors'][name]['mean'])
        near(stdev(x-ratio*y for x,y in zip(a,b))/(4*mean(b)),imp['joint_factors'][name]['se'])
    ig = {'mean_prior_weight':abs(imp['estimates']['prior_weight_mean']['mean']-1) < .02}
    for key, sobol in [('native',native),('uniform',flat)]:
        observed = imp['estimates'][key+'_DESI_Pantheon']
        error = abs(sobol['mean']-observed['mean']) / sqrt(sobol['se']**2+observed['se']**2)
        near(error,imp['joint_difference_from_sobol_in_standard_errors'][key])
        ig['sobol_'+key] = error <= 3
        ig['precision_'+key] = observed['se']/observed['mean'] < .05
    if ig != imp['gates']:
        raise ValueError('Prüfentscheid des Zusatzlaufs stimmt nicht')
    print('Prüfsummen, Originaldateien, Randverteilung, 48 Netzmittel-Zeilen und 16 Zusatzströme verifiziert.')
    for name, passed in ig.items():
        print('Zusatzlauf',name,'PASS' if passed else 'HOLD')
    for name, passed in g.items():
        print(name, 'PASS' if passed else 'HOLD')


if __name__ == '__main__':
    main()
