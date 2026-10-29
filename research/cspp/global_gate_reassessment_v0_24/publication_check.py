"""Check immutable v0.24 publication, method scope and exact replay."""
import argparse, hashlib, json, subprocess, sys, zipfile
from pathlib import Path, PurePosixPath

HERE = Path(__file__).resolve().parent

def require(ok, message):
    if not ok:
        raise RuntimeError(message)

def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def safe(name, package=None):
    p = PurePosixPath(name)
    require(bool(p.parts) and not p.is_absolute() and '..' not in p.parts and (package is None or p.parts[0] == package), 'safe publication path')

def read(path):
    return json.loads(path.read_text())

def run(replay=False):
    meta = read(HERE/'PUBLICATION.json')
    package = HERE/'cspp_v024'
    for name, digest in meta['artifact_sha256'].items():
        safe(name)
        require(sha(HERE/name) == digest, 'artifact SHA256: '+name)
    with zipfile.ZipFile(HERE/'CSPP_Gate_Neubewertung_v0_24_Pruefpaket.zip') as z:
        require(z.testzip() is None, 'ZIP CRC')
        names = z.namelist()
        require(len(names) == len(set(names)) == meta['package_file_count'] == 58, 'original package inventory')
        for name in names:
            safe(name, package.name)
            require((HERE/name).read_bytes() == z.read(name), 'original package bytes: '+name)
        before = {name:sha(HERE/name) for name in names}
    manifest = (package/'SHA256SUMS').read_text().splitlines()
    require(len(manifest) == meta['package_manifest_entries'] == 57, 'manifest inventory')
    checked = set()
    for line in manifest:
        digest, name = line.split('  ',1)
        safe(name)
        require(name not in checked, 'unique manifest path')
        checked.add(name)
        require(sha(package/name) == digest, 'package SHA256: '+name)
    require(checked|{'SHA256SUMS'} == {str(PurePosixPath(n).relative_to(package.name)) for n in names}, 'complete manifest coverage')
    pdf = 'Gate_Neubewertung_Globale_Bilanz_v0_24.pdf'
    require((package/'report'/pdf).read_bytes() == (HERE/pdf).read_bytes(), 'same PDF')
    checks = read(package/'results/CHECKS.json')
    require(checks['status'] == 'PASS', 'scientific checks')
    require(checks['counts'] == {
        'cross_precision_comparisons':40, 'exact_counterexample_identities':60,
        'exact_geometry_identities':4, 'global_decompositions':16,
        'independent_Poisson_PGF_sums':12, 'inherited_H_cover_nodes':258,
        'legacy_method_entries':24, 'paired_covariance_sign_controls':2,
        'source_files':34, 'v023_replay_files':5}, 'declared check scope')
    require(len(checks['negative_controls']) == 6 and all(v.startswith('REJECTED_') for v in checks['negative_controls'].values()), 'six excluded invalid inferences')
    receipt = read(package/'REPLAY.json')
    require(receipt['isolated_replay'] == 'PASS' and receipt['byte_identical_result_files'] == 4 and receipt['precisions_bits'] == [128,192], 'replay receipt')
    require(len(receipt['files']) == 4, 'numerical result inventory')
    for name, digest in receipt['files'].items():
        safe(name)
        require(sha(package/'results'/name) == digest, 'replayed result identity')
    protocol = read(package/'PROTOCOL.json')
    status = read(package/'STATUS.json')
    require(protocol['base_commit'] == meta['base_commit'] == status['base_commit'], 'fixed research basis')
    require(protocol['completed_step'] == 3 and status['step_3'] == 'COMPLETED', 'reassessment complete')
    require(protocol['new_clouds'] == protocol['new_random_calls'] == 0, 'no new data')
    require(protocol['physical_parameters_changed'] is False and protocol['statistical_rules_changed'] is False, 'fixed physical and statistical scope')
    require(protocol['unchanged_global_accuracy_target'] == '1/1000' and protocol['unchanged_operator_necessary_relative_RMS_target'] == '1/10', 'distinct unchanged targets')
    require(status['METHOD'] == status['G1'] == checks['METHOD'] == checks['G1'] == 'HOLD', 'scientific gates')
    require(status['fresh_confirmation'] == checks['fresh_confirmation'] == 'NOT_RUN' and status['new_candidate'] == 'NOT_SELECTED', 'no premature candidate or confirmation')
    require(status['whole_operator_family'] == 'NOT_REJECTED' and status['accuracy_release'] == 'NOT_CERTIFIED', 'claim boundary')
    require(status['independent_scientific_review'] == checks['independent_scientific_review'] == 'NOT_PERFORMED', 'review boundary')
    for bits in [128,192]:
        d = read(package/f'results/DECISION_{bits}.json')
        require(d['precision_bits'] == bits and d['completed_step'] == 3, 'precision and step')
        require(d['decision'] == 'NO_ACCURACY_RELEASE_NO_FRESH_ENSEMBLE', 'decision')
        require(d['METHOD'] == d['G1'] == 'HOLD' and d['new_random_calls'] == d['new_clouds'] == 0, 'fixed scope')
        require(d['global_coverage'] == 'COMPLETE_FINITE_PLUS_INFINITE', 'whole exterior budget')
        require([w['window'] for w in d['budget_windows']] == [0,1], 'both windows')
        for w in d['budget_windows']:
            require([r['archive'] for r in w['archives']] == ['d0_r00','d0_r01','d0_r02','d0_r03'], 'four inherited archives')
            require(w['ensemble_L1_status'] == 'FINITE_UNDER_IDEAL_POISSON_LAW' and w['covariance_prediction'] == 'NOT_EVALUATED', 'L1 scope')
            for r in w['archives']:
                require(r['Markov_failure_probability_upper_at_target'] == '1' and r['actual_error_lower_bound_from_this_budget'] == '0', 'upper bound is not observed error')
        require(all(c['decision'] == 'REJECTED_FOR_CONFIRMATORY_RUN' for c in d['legacy_candidates'].values()), 'inherited method admission')
        require(d['operator_witness']['fixed_cell_domain_only_repair'] == 'REJECTED_BY_INHERITED_NECESSARY_WITNESS' and d['operator_witness']['whole_operator_family'] == 'NOT_REJECTED', 'restricted Gaussian witness')
        require(all(v is None for v in d['new_confirmatory_design'].values()), 'no fresh design')
    if replay:
        subprocess.run([sys.executable,'-B',str(package/'reproduce.py')],check=True)
    for name,digest in before.items():
        require(sha(HERE/name) == digest, 'publication unchanged: '+name)
    print('Publication integrity PASS: original PDF, ZIP, 58 files, 57 hashes; step 3 complete; METHOD and G1 HOLD; no fresh confirmation',flush=True)

if __name__ == '__main__':
    p = argparse.ArgumentParser()
    p.add_argument('--replay',action='store_true')
    run(p.parse_args().replay)
