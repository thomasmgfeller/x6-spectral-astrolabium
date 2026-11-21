"""Offline-Reproduktion der endlichen N15-Studien des Teilartikels."""
import argparse
import hashlib
import json
from decimal import Decimal, localcontext
from fractions import Fraction
from itertools import combinations, permutations, product
from math import isclose, sqrt
from pathlib import Path
import subprocess
import sys
import tempfile
from zipfile import ZipFile


ROOT = Path(__file__).resolve().parent
STUDIES = {
    'n15_birth_covariance_v0_1': [('sources/pruefen.py', 'sources/ergebnis.json')],
    'n15_sector_norm_rest_mass_v0_1': [('pruefen.py', 'ergebnis.json')],
    'n15_quellzeiger_zwischenrand_v0_1': [('nachweis.py', 'nachweis.json')],
    'n15_stromtransport_ward_v0_1': [('strom.py', 'schnitte.json'),
        ('schnittkoordinaten.py', 'schnittkoordinaten.json'), ('gegenprobe.py', 'gegenprobe.json'),
        ('zeigerprodukt.py', 'zeigerprodukt.json')],
    'n15_schnittimpulse_v0_1': [('schnittimpulse.py', 'ergebnis.json'),
        ('rueckrechnung.py', 'rekonstruktion.json'), ('gegenprobe.py', 'gegenprobe.json')],
    'n15_dichtesumme_randquelle_v0_1': [('nachrechnen.py', 'ergebnis.json')],
    'n15_uhrrekonstruktion_v0_1': [('pruefen.py', 'ergebnis.json')],
    'n15_zukunftsdichte_interferenz_v0_1': [('nachrechnen.py', 'ergebnis.json')],
    'n15_dichte_weiterverklebung_v0_1': [('nachrechnen.py', 'ergebnis.json')],
}


def load(path):
    return json.loads(path.read_bytes())


def checked_archives(temp):
    manifest = load(ROOT / 'quellen.json')
    folders = {}
    for record in manifest['originale']:
        name = record['ordner']
        path = ROOT / 'originale' / record['datei']
        data = path.read_bytes()
        assert hashlib.sha256(data).hexdigest() == record['sha256'], path
        assert hashlib.sha1(f'blob {len(data)}\0'.encode() + data).hexdigest() == record['git_blob'], path
        with ZipFile(path) as archive:
            assert all(p.startswith(name + '/') and '..' not in Path(p).parts for p in archive.namelist())
            archive.extractall(temp)
        folder = temp / name
        for line in (folder / 'SHA256SUMS').read_text().splitlines():
            digest, relative_path = line.split(None, 1)
            assert hashlib.sha256((folder / relative_path).read_bytes()).hexdigest() == digest, relative_path
        assert name not in folders
        folders[name] = folder
    assert folders.keys() == STUDIES.keys()
    return folders


def replay(folders):
    verified = []
    for name, programs in STUDIES.items():
        for program, reference in programs:
            folder = folders[name]
            out = subprocess.check_output([sys.executable, '-E', '-B', program], cwd=folder)
            # Whitespace and key order are immaterial. All JSON numbers and strings must agree.
            assert json.loads(out) == load(folder / reference), f'{name}/{program}: {reference}'
            verified.append(f'{name}/{program}')
    return verified


def layer_counts(relation):
    nodes = set(x for pair in relation for x in pair)
    return {(i, j): sum((i, k) in relation and (k, j) in relation for k in nodes)
            for i, j in relation}


def check_labels(folder):
    cfg = load(folder / 'pruefvertrag.json')
    reference = load(folder / 'resultate/ergebnis.json')
    inside = tuple(cfg['reference_inner_order'])
    past, future = (0, 1, 2, 3), (7, 8, 9, 10)
    local_edges = {edge for k, edge in enumerate(combinations(inside, 2)) if cfg['type'] & (1 << k)}
    full = local_edges | set(combinations(past, 2)) | set(combinations(future, 2))
    full |= set(product(past, inside + future)) | set(product(inside, future))
    counts = layer_counts(full)
    factors = (1, -9, 16, -8)
    f4 = 15 - sum(factors[k] for k in counts.values() if k < len(factors))
    assert f4 == reference['F4']
    expected = {tuple(row['old_event_ids_in_birth_order']): row for row in reference['rows']}
    seen = set()
    native_codes = set()
    for order in permutations(inside):
        labels = {v: k for k, v in enumerate(past + order + future)}
        if any(labels[a] >= labels[b] for a, b in local_edges):
            continue
        transported = {(labels[a], labels[b]) for a, b in full}
        recounted = layer_counts(transported)
        assert all(recounted[labels[i], labels[j]] == n for (i, j), n in counts.items())
        code = sum(1 << k for k, edge in enumerate(combinations(order, 2)) if edge in local_edges)
        assert code == expected[order]['native_inner_bit_code']
        assert [labels[j] for j in cfg['ordered_packet_axes']] == expected[order]['ordered_translation_axes_in_birth_labels']
        native_codes.add(code)
        seen.add(order)
    assert seen == expected.keys() and len(native_codes) == len(seen) == cfg['number_of_extensions']
    return {'umbenennungen':len(seen), 'verschiedene_kodierungen':len(native_codes), 'F4':f4}


def check_ensemble(folder):
    """Use row/column contraction of the archived six-bin Gram matrix."""
    source = folder / 'quellen/joint_charge_distribution_v0_1/joint.json'
    matrix_rows = load(source)['rows']
    ref = load(folder / 'ergebnis.json')['sector']['ensemble_overlap_rows']
    overlaps = {}
    for label, row in matrix_rows.items():
        for law in ('1:1', '1:3'):
            stats = row[law]
            raw = stats['decoherence_matrix_scaled_by_record_trace']
            g = [[complex(x, y) for x, y in zip(r, i)] for r, i in zip(raw['re'], raw['im'])]
            assert len(g) == 6 and all(len(line) == 6 for line in g)
            assert all(abs(g[i][j] - g[j][i].conjugate()) < 1e-12 for i, j in product(range(6), repeat=2))
            diagonal = [g[i][i].real for i in range(6)]
            assert isclose(sum(diagonal), 1, abs_tol=1e-12)
            for measured, published in zip(diagonal, stats['bin_probabilities']):
                assert isclose(measured, published, rel_tol=1e-12, abs_tol=1e-15)
            negative = sum(sum(line[:3]) for line in g[:3]).real
            positive = sum(sum(line[3:]) for line in g[3:]).real
            off = sum(sum(line[:3]) for line in g[3:])
            fine = sum(diagonal[3:]) / sum(diagonal)
            coarse = positive / (negative + positive)
            assert isclose(fine, stats['positive_fine_record'], abs_tol=1e-12)
            assert isclose(coarse, stats['positive_sign_record'], abs_tol=1e-12)
            overlap = abs(off) / sqrt(negative * positive)
            overlaps[label, law] = overlap
    assert len(ref) == len(overlaps) == 12
    for line in ref:
        assert isclose(overlaps[line['M/r'], line['A:B']], line['normalized_overlap'], rel_tol=1e-12)
    return {'zeilen':len(overlaps), 'ueberlapp_min':min(overlaps.values()),
            'ueberlapp_max':max(overlaps.values())}


def count_catalog(folder):
    """Count the predecessors of each internal event directly from the order code."""
    table = load(folder / 'katalog/catalog.json')['ranks_pure_free_mixed']
    rows = [int(key) for key, triple in table.items() if triple[0] == 0 == triple[2]]
    complete = set()
    for key in rows:
        predecessor_numbers = [0] * 7
        for bit, (_, j) in enumerate(combinations(range(7), 2)):
            predecessor_numbers[j] += (key >> bit) & 1
        if max(predecessor_numbers) < 4:
            complete.add(str(key))
    laws = load(folder / 'katalog/weights.json')['laws']
    chain = load(folder / 'katalog/chain.json')['law']
    counts = load(folder / 'ergebnis.json')['katalog']
    assert len(rows) == counts['typen'] and len(complete) == counts['vollstaendige_typen']
    for law, coeff in laws.items():
        support = set(chain) | set(coeff)
        weights = [(Fraction(chain.get(key, 0)) + Fraction(coeff.get(key, 0))) / 2 for key in complete & support]
        assert len(weights) == counts['ensemble_vollstaendig']
        assert len(support) == counts['ensemble_traeger']
        assert sum(weights) == Fraction(counts['anteil_des_eingesetzten_typgewichts_auf_vollstaendigen_typen'][law])
    return {'katalog':len(rows), 'katalog_vollstaendig':len(complete),
            'ensemble':len(support), 'ensemble_vollstaendig':len(weights)}


def check_center_port(port, seam):
    """Analytic center values, separately from the original whole-packet bounds."""
    source = load(port / 'ergebnis.json')
    readout = source['optimum_flache_randpaarung']
    bound = load(seam / 'ergebnis.json')['abstieg_und_kontrast']
    def value(q):
        q = Fraction(q)
        return Decimal(q.numerator) / Decimal(q.denominator)
    with localcontext() as ctx:
        ctx.prec = 85
        h = value(source['schritt_der_physischen_zukunftsdichte_w7'])
        a, b = (h * value(source['pakete'][s]['D7_zentrum_minus_referenz']) for s in ('positiv', 'negativ'))
        x = a - b
        assert 0 < x < Decimal('1e-10') and max(abs(a),abs(b)) < Decimal('1e-10')
        # Alternating Taylor remainders below 10^-50 here; retain cancellation accurately.
        sin = lambda t: t - t**3 / 6 + t**5 / 120
        sinc = 1 - x**2 / 6 + x**4 / 120 - x**6 / 5040
        fixed = (sin(a) - sin(b)) / 2
        optimum = (1 - sinc*sinc).sqrt()
        for quantity, interval in [(fixed, readout['P_differenz_fester_port_enger']),
                                   (optimum, readout['maximale_P_differenz_aller_binaeren_effekte']),
                                   (fixed, bound['zwei_moden_P_differenz'])]:
            lo, hi = map(value, interval)
            assert lo < quantity - Decimal('1e-45') < quantity + Decimal('1e-45') < hi
        assert fixed > optimum * Decimal('0.866') and fixed < optimum
        assert value(bound['ein_modus_spurabstand_max']) < Decimal('4.658e-18')
        # For n(w)=sqrt(3)*(w-m)/h, the exact means of the two half bins
        # are opposite. Apply the original two-bin projector before averaging.
        right = Decimal(3).sqrt() / 2
        left = -right
        assert (left + right) / 2 == 0
        alpha = h * value(source['D_referenz'])
        assert abs(alpha) < Decimal('4e-6')
        cos_alpha = 1 - alpha**2 / 2 + alpha**4 / 24 - alpha**6 / 720
        squared = ((left - right) * cos_alpha / 4)**2
        lo, hi = map(value, bound['normierter_glatter_nullzeuge_RE_betragsquadrat'])
        assert Decimal('0.18') < lo < squared < hi
        return {'fester_port_zentren':format(fixed,'.15e'), 'spurabstand_zentren':format(optimum,'.15e'),
                'glatter_nullzeuge_betragsquadrat_nach_port':format(squared,'.15e')}


def main():
    if not __debug__:
        raise RuntimeError('Python ohne -O starten.')
    argparse.ArgumentParser(description=__doc__).parse_args()
    manifest = load(ROOT / 'quellen.json')
    with tempfile.TemporaryDirectory(dir=ROOT, prefix='nachrechnung-') as tmp:
        folders = checked_archives(Path(tmp))
        independent = {
            'geburtslabels':check_labels(folders['n15_birth_covariance_v0_1']),
            'sechsbin_matrix':check_ensemble(folders['n15_sector_norm_rest_mass_v0_1']),
            'sichtbare_dichtesumme':count_catalog(folders['n15_dichtesumme_randquelle_v0_1']),
            'port_und_naht':check_center_port(folders['n15_zukunftsdichte_interferenz_v0_1'],
                                               folders['n15_dichte_weiterverklebung_v0_1']),
        }
        verified = replay(folders)
    print(json.dumps({'status':'PASS','commit':manifest['commit'],
                      'unabhaengige_kontrollen':independent,'originalrechnungen':verified,
                      'sobol':'NICHT_WIEDERHOLT','physikalische_P3_Laeufe':0},indent=2,ensure_ascii=False))


if __name__ == '__main__':
    main()
