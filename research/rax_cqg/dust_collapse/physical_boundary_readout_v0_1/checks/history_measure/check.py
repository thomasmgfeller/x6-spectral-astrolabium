#!/usr/bin/env python3
"""Exact small-causet checks of covariant positive composed history priors."""
from pathlib import Path
from collections import Counter, defaultdict
from itertools import permutations
from math import comb
import json
import sympy as s

ROOT = Path(__file__).resolve().parent
p = s.Symbol('p', real=True)


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def closure(n, relation):
    relation = set(relation)
    for k in range(n):
        relation |= {(i, j) for i in range(n) for j in range(n)
                     if (i, k) in relation and (k, j) in relation}
    return frozenset(relation)


def covers(n, relation):
    return {(i, j) for i, j in relation
            if not any((i, k) in relation and (k, j) in relation for k in range(n))}


def ideals(n, relation):
    return [frozenset(i for i in range(n) if (mask >> i) & 1)
            for mask in range(1 << n)
            if all(not ((mask >> j) & 1) or ((mask >> i) & 1) for i, j in relation)]


def maximal(relation, subset):
    return {i for i in subset if not any((i, j) in relation for j in subset)}


def normalize_growth(n, relation):
    subsets = ideals(n, relation)
    terms = [(len(maximal(relation, A)), n - len(A)) for A in subsets]
    require(s.expand(sum(p ** m * (1 - p) ** k for m, k in terms)) == 1,
            'Parent transition probabilities do not sum to one')
    comparisons = 0
    for A in subsets:
        for B in subsets:
            union = A | B
            restricted = {(i, j) for i, j in relation if i in union and j in union}
            # Spectator deletion must preserve both exponents in the transition ratio.
            lhs = (len(maximal(relation, A)) - len(maximal(relation, B)),
                   (n - len(A)) - (n - len(B)))
            rhs = (len(maximal(restricted, A)) - len(maximal(restricted, B)),
                   (len(union) - len(A)) - (len(union) - len(B)))
            require(lhs == rhs, 'Classical Bell-causality ratio changes with spectators')
            comparisons += 1
    return comparisons


def classify(n, relation):
    L = len(covers(n, relation))
    R = len(relation)
    incomparable = comb(n, 2) - R
    automorphisms = 0
    extension_count = 0
    canonical = None
    for perm in permutations(range(n)):
        image = frozenset((perm[i], perm[j]) for i, j in relation)
        key = tuple(sorted(image))
        canonical = key if canonical is None else min(canonical, key)
        automorphisms += image == relation
        require(len(image) == R and len(covers(n, image)) == L,
                'Relabeling changes invariant weight exponents')
        position = {element: rank for rank, element in enumerate(perm)}
        if not all(position[i] < position[j] for i, j in relation):
            continue
        extension_count += 1
        total_links = total_incomparables = total_relations = 0
        for rank, element in enumerate(perm):
            past = {i for i, j in relation if j == element}
            require(past <= set(perm[:rank]), 'A natural birth occurs before an ancestor')
            total_relations += len(past)
            total_links += len(maximal(relation, past))
            total_incomparables += rank - len(past)
        require((total_links, total_incomparables, total_relations) == (L, incomparable, R),
                'Prefix multiplication depends on the natural birth order')
    require(extension_count % automorphisms == 0, 'Nonintegral natural-label multiplicity')
    return canonical, extension_count, automorphisms


def finite_checks(n):
    possible = [(i, j) for i in range(n) for j in range(i + 1, n)]
    preimages = defaultdict(Counter)
    for mask in range(1 << len(possible)):
        dag = {e for k, e in enumerate(possible) if (mask >> k) & 1}
        preimages[closure(n, dag)][len(dag)] += 1
    classes = defaultdict(list)
    polynomial = 0
    growth_count = bell_count = extension_checks = 0
    for relation, histogram in preimages.items():
        R = len(relation)
        L = len(covers(n, relation))
        incomparable = len(possible) - R
        # Every cover must have been selected; every redundant relation is arbitrary;
        # every incomparable pair must have been absent before transitive closure.
        expected = {k: comb(R - L, k - L) for k in range(L, R + 1)}
        require(dict(histogram) == expected, 'Percolation closure preimage identity fails')
        polynomial += p ** L * (1 - p) ** incomparable
        canonical, extensions, aut = classify(n, relation)
        extension_checks += extensions
        classes[canonical].append((extensions, aut))
        if n <= 4:
            bell_count += normalize_growth(n, relation)
            growth_count += 1
    require(s.expand(polynomial) == 1, 'Fixed-N normalized law fails')
    for values in classes.values():
        e, aut = values[0]
        require(all(v == (e, aut) for v in values), 'Isomorphic multiplicities disagree')
        require(len(values) == e // aut, 'Forgotten-label pushforward multiplicity wrong')
    return {
        'N': n, 'forward_DAGs_enumerated': 1 << len(possible),
        'distinct_naturally_labeled_posets': len(preimages),
        'unlabeled_isomorphism_classes': len(classes),
        'closure_preimage_histograms_exact': True,
        'symbolic_total_probability': '1 for every p',
        'natural_extension_prefix_checks': extension_checks,
        'normalized_parent_families_checked': growth_count,
        'Bell_spectator_ratio_checks': bell_count,
        'pushforward_multiplicity_e_over_aut_checked': True}


def n11_counts(removed):
    n = 11
    relation = frozenset({(i, j) for i in range(n) for j in range(i + 1, n)} - removed)
    boundary = [0, 1, 2, 3, 7, 8, 9, 10]
    interior = [4, 5, 6]
    extensions = []
    aut_boundary = 0
    all_labeled_orbit = set()
    natural_labeled_orbit = set()
    for inner_perm in permutations(interior):
        seq = [0, 1, 2, 3] + list(inner_perm) + [7, 8, 9, 10]
        position = {v: k for k, v in enumerate(seq)}
        if all(position[i] < position[j] for i, j in relation):
            extensions.append(list(inner_perm))
        mapping = dict(zip(interior, inner_perm)) | {j: j for j in boundary}
        image = frozenset((mapping[i], mapping[j]) for i, j in relation)
        aut_boundary += image == relation
        all_labeled_orbit.add(image)
        if all(i < j for i, j in image):
            natural_labeled_orbit.add(image)
    R = len(relation)
    L = len(covers(n, relation))
    incomparable = comb(n, 2) - R
    require(len(extensions) // aut_boundary == len(natural_labeled_orbit),
            'N11 natural-label multiplicity wrong')
    return {'relations_R': R, 'covers_L': L, 'incomparable_pairs_I': incomparable,
            'natural_linear_extensions_interior': extensions,
            'boundary_preserving_automorphisms': aut_boundary,
            'all_S3_interior_label_images': len(all_labeled_orbit),
            'distinct_natural_label_images': len(natural_labeled_orbit),
            'fixed_natural_representative_probability': str(p ** L * (1 - p) ** incomparable)}


def main():
    audits = [finite_checks(n) for n in range(6)]
    require([r['distinct_naturally_labeled_posets'] for r in audits] == [1, 1, 2, 7, 40, 357],
            'Wrong finite order inventory')
    require([r['unlabeled_isomorphism_classes'] for r in audits] == [1, 1, 2, 5, 16, 63],
            'Wrong finite isomorphism inventory')
    c0 = n11_counts(set())
    c1 = n11_counts({(4, 5), (5, 6)})
    require((c0['relations_R'], c0['covers_L'], c0['incomparable_pairs_I']) == (55, 10, 0),
            'Wrong chain counts')
    require((c1['relations_R'], c1['covers_L'], c1['incomparable_pairs_I']) == (53, 11, 2),
            'Wrong changed-order counts')
    require((c0['distinct_natural_label_images'], c1['distinct_natural_label_images']) == (1, 3),
            'Wrong N11 multiplicities')
    ratio = p * (1 - p) ** 2
    require(ratio.subs(p, s.Rational(1, 2)) == s.Rational(1, 8), 'First prior witness wrong')
    require(ratio.subs(p, s.Rational(3, 4)) == s.Rational(3, 64), 'Second prior witness wrong')
    output = {
        'id': 'CST-DUST-HISTORY-MEASURE-NONUNIQUENESS-0.1',
        'status': 'STRONG_REQUIREMENTS_DO_NOT_SELECT_UNIQUE_PRIOR',
        'raw_covariant_composed_family': {
            'mu_lambda': 'exp(-lambda*R(C)), lambda real, R=#strict comparable pairs',
            'prefix_factor': 'exp(-lambda*|past(newborn)|)',
            'positive': True, 'label_covariant': True, 'exact_prefix_composition': True,
            'stochastic_normalization_claimed': False,
            'N11_fixed_representative_ratio_C1_over_C0': 'exp(2*lambda)',
            'lambda_derived_from_CST_DUST_action': False},
        'normalized_classical_family': {
            'name': 'Transitive percolation', 'parameter_domain': '0<p<1',
            'transition_for_specified_precursor_A': 'p^m*(1-p)^(n-|A|), m=#maximal elements of A',
            'fixed_natural_representative_probability': 'p^L*(1-p)^I',
            'properties': ['internal temporality', 'positive probabilities', 'discrete general covariance', 'exact prefix product', 'Markov normalization', 'classical Bell causality'],
            'N11_chain': c0, 'N11_changed_order': c1,
            'fixed_representative_ratio': 'p*(1-p)^2',
            'unlabeled_growth_pushforward_ratio': '3*p*(1-p)^2',
            'all_label_S3_quotient_rule': 'For a separately declared invariant endpoint weight, sum all six interior-label images then divide by 6: each orbit contributes weight/Aut_B; both Aut_B=1. This is not the stochastic growth law, which uses only natural labels. Extending its formula to nonnatural labels changes conventions.',
            'distinct_parameter_witnesses': [
                {'p': '1/2', 'fixed_representative_ratio': '1/8', 'unlabeled_growth_ratio': '3/8'},
                {'p': '3/4', 'fixed_representative_ratio': '3/64', 'unlabeled_growth_ratio': '9/64'}],
            'p_derived_from_CST_DUST_action': False,
            'classical_probability_is_quantum_amplitude_weight': False},
        'finite_exact_checks': audits,
        'total_natural_extension_checks': sum(a['natural_extension_prefix_checks'] for a in audits),
        'total_normalized_parent_checks': sum(a['normalized_parent_families_checked'] for a in audits),
        'total_Bell_ratio_checks': sum(a['Bell_spectator_ratio_checks'] for a in audits),
        'measure_detector_distinction': 'Prior construction does not select an environmental overlap or detector; changing the detector does not determine the prior parameter.',
        'primary_source': {
            'authors': 'D. P. Rideout and R. D. Sorkin',
            'title': 'A Classical Sequential Growth Dynamics for Causal Sets',
            'doi': '10.1103/PhysRevD.61.024002',
            'url': 'https://arxiv.org/pdf/gr-qc/9904062',
            'locations': 'Sections 2, 3 and 4.2; equation (6); pages 15-16 of the PDF for transitive-percolation transition and invariant finite-causet weight.'},
        'all_checks_passed': True}
    (ROOT / 'results.json').write_text(json.dumps(output, ensure_ascii=False, indent=2) + '\n')
    print('PASS: covariant composed positive family, normalized transitive percolation through N=5, natural-label multiplicities and N11 ratios.')
    print('No unique physical quantum history measure is selected by these requirements.')


if __name__ == '__main__':
    main()
