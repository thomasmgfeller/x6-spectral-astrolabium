"""Zwei Paarungen auf Ordnungen beliebiger endlicher Grösse, exakter endlicher Audit."""
from collections import Counter
from fractions import Fraction as Q
from itertools import combinations
from math import factorial, comb


def require(condition, message):
    if not condition:
        raise ValueError(message)


def metric_weight(order):
    """2^(Anzahl Beziehungen minus Anzahl Hasse-Kanten), aus der ganzen Ordnung."""
    transitive = 0
    for past in order:
        indirect = 0
        for j, previous in enumerate(order):
            if past & (1 << j):
                indirect |= previous
        transitive += indirect.bit_count()
    return 1 << transitive


def closed_extensions(order):
    """Alle Teilmengen mit ihrer Abwärtshülle gruppieren (p=1/2)."""
    counts = Counter()
    for subset in range(1 << len(order)):
        past = subset
        for j, previous in enumerate(order):
            if subset & (1 << j):
                past |= previous
        counts[past] += 1
    return counts


def ideal_masks(order):
    """Unabhängiger Test der Ideale über die Implikation x in I => past(x) in I."""
    return [mask for mask in range(1 << len(order))
            if all(not (mask & (1 << j)) or past & mask == past
                   for j, past in enumerate(order))]


def exp_minus_interval(s):
    """Alternierende Taylorhülle für 0 <= s <= 1."""
    require(0 <= s <= 1, "Uhrwert ausserhalb des untersuchten Fensters")
    upper = sum(((-s)**i / factorial(i) for i in range(21)), Q(0))
    return upper - s**21 / factorial(21), upper


def raw(a, n, d):
    return d**(n-a) / (factorial(n-a) * (1 << sum(range(a, n))))


def row_norm_checks(grid):
    """Summiert über die Geburtszahlen, mit rationaler Hülle für den unendlichen Rest."""
    tests = 0
    for beta in (Q(5,4), Q(4,3)):
        for a,b in combinations(grid, 2):
            d = b-a
            for m in (0,1,2):
                # Nach Division durch das geometrische Elterngewicht ist der
                # Grundterm jeder Endstufe e^-b d^k/k!. Die beiden kleinen
                # Endstufen tragen die unten separat summierten Korrekturen.
                cutoff = 6-m
                partial = sum(d**k/factorial(k) for k in range(cutoff+1))
                first_omitted = d**(cutoff+1)/factorial(cutoff+1)
                max_tail = first_omitted/(1-d/(cutoff+2))
                lo_b, hi_b = exp_minus_interval(b)
                lo_a, hi_a = exp_minus_interval(a)
                if m == 0:
                    correction = (1-beta)*b + d*(beta-1)
                    parent = (1-beta)*a
                elif m == 1:
                    correction = parent = beta-1
                else:
                    correction = parent = 0
                lo = lo_b*partial + correction
                hi = hi_b*(partial+max_tail) + correction
                require(lo <= lo_a+parent and hi >= hi_a+parent,
                        "Unabhängige Summenhülle für die Elternnorm")
                tests += 1
    return tests


def run():
    order_level = [()]
    levels = [1]
    checked_rows = 0
    bad_rows = 0
    edges = 0
    for n in range(6):
        next_level = []
        for order in order_level:
            counts = closed_extensions(order)
            ideals = ideal_masks(order)
            require(set(counts) == set(ideals), "Ideale und Abwärtshüllen")
            weight = metric_weight(order)
            total = 0
            for ideal in ideals:
                child = order + (ideal,)
                new_weight = metric_weight(child)
                require(new_weight == weight * counts[ideal], "Orbit-/Teilmengenmultiplikität")
                total += new_weight
                next_level.append(child)
            require(total == (1 << n) * weight, "harmonische Zeilensumme")
            bad_rows += len(ideals) != 1 << n
            checked_rows += 1
            edges += len(ideals)
        order_level = next_level
        levels.append(len(order_level))
        require(len(set(order_level)) == len(order_level), "doppelte Ordnung")
        # Bei Start aus dem leeren Präfix ist die geometrische Gewichtssumme eins.
        require(sum(map(metric_weight, order_level)) == 1 << comb(n+1, 2), "Gesamtgewicht")
    require(levels == [1, 1, 2, 7, 40, 357, 4824] and bad_rows > 0, "Kontrollzählung")

    # Direkte Simplex-Integration gegen alle möglichen Geburtszahlen am Zwischenschnitt.
    cut_checks = 0
    grid = [Q(k, 4) for k in range(5)]
    for start, middle, end in combinations(grid, 3):
        for i in range(7):
            for n in range(i, 7):
                sewn = sum(raw(i,j,middle-start)*raw(j,n,end-middle) for j in range(i,n+1))
                require(sewn == raw(i,n,end-start), "Schnittkomposition")
                cut_checks += 1
    bounds = {}
    for beta in (Q(5,4), Q(4,3)):
        at_one = exp_minus_interval(Q(1))[0] + 1 - beta
        require(at_one > 0, "Positivität am rechten Rand")
        lo, hi = exp_minus_interval(Q(1,2))
        bounds[str(beta)] = [str(x-(beta-1)/2) for x in (lo,hi)]
    first = list(map(Q, bounds['5/4']))
    second = list(map(Q, bounds['4/3']))
    require(all(i-j == Q(1,24) for i,j in zip(first,second)), "Betakontrast")
    require(first[0] > second[1], "Intervalle überlappen")
    # n>=2 hat bei leerem Anfang Poisson(s)-Gewichte. Der Tail wächst mit s.
    lo,hi = exp_minus_interval(Q(1))
    partial = sum(Q(1, factorial(j)) for j in range(7))
    tail = (1 - hi*partial, 1 - lo*partial)
    require(0 < tail[0] < tail[1] < Q(1,12000), "Cutoff-Hülle")
    return dict(order_counts=levels, parent_rows=checked_rows, checked_edges=edges,
                rows_detecting_missing_multiplicity=bad_rows,
                sewn_raw_coefficients=cut_checks, interval_norm_checks=row_norm_checks(grid),
                empty_half_intervals=bounds,
                beta_contrast="1/24", empty_start_tail_N_gt_6_at_s1=list(map(str,tail)),
                uniform_upper_tail_probability="1/12000", physical_histories=0)
