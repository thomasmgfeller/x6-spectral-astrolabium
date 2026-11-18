"""Small archive and reference checks accompanying the four CST-DUST reviews."""
import csv
import json
from fractions import Fraction as F
from itertools import combinations, product
from math import hypot, isqrt, pi
from pathlib import Path

DUST = Path(__file__).resolve().parents[1]


def require(condition, message):
    if not condition:
        raise ValueError(message)


def source(path):
    return json.loads((DUST / path).read_text(encoding="utf-8"))


def state_space():
    uniform = source("basis_invariant_coupling_v0_1/results/uniform.json")
    block = uniform["blocks"]["difference"]["full6"]
    require(block["rank"] == "EXACTLY_TWO", "AA archive rank")
    sector = source("history_measure_state_space_v0_1/sector.json")
    overlap4 = F(sector["absolute_overlap_fourth_power_exact"])
    # A normalized Hermitian pair has determinant 1 - |g|^2.
    require(0 < overlap4 < 1, "N14 normalized Gram pair")
    print("4  Archived AA rank 2. N14 scalar pair has positive determinant.")


def preparations():
    # Both N11 orders have this same total order on their four past events.
    layers = (1, -9, 16, -8)
    coefficients = [
        1 + F(sum(layers[j-i-1] * (j-i)**2 for i in range(j)), 19)
        for j in range(4)
    ]
    require(coefficients == [1, F(20, 19), F(-16, 19), F(128, 19)], "past action")
    require(sum(coefficients) / 2 == F(151, 38), "common phase coefficient")
    data = source("initial_preparation_v0_1/clock_packet_results.json")
    packets = data["finest_grid"]["clock_density_packets"]
    ratios = {F(p["rho_center"]): hypot(*p["W1_over_W0_coherent_re_im"]) for p in packets}
    expected = {F(1, 8): "1.59847116", F(1, 4): "1.59591233"}
    require({m: f"{r:.8f}" for m, r in ratios.items()} == expected, "packet ratios")
    print("5  Common phase coefficient 151/38. Packet ratios 1.59847116 and 1.59591233.")


def kernel(h, alpha):
    weight = F(1, 2**alpha)
    pair = weight * h*h / 2
    return [[1, h, pair, pair], [0, 1, weight*h, weight*h],
            [0, 0, 1, 0], [0, 0, 0, 1]]


def transport(a, b, end, alpha):
    before = [sum(row) for row in kernel(end-a, alpha)]
    after = [sum(row) for row in kernel(end-b, alpha)]
    matrix = [[F(entry) * after[j] / before[i] for j, entry in enumerate(row)]
              for i, row in enumerate(kernel(b-a, alpha))]
    require(all(sum(row) == 1 for row in matrix), "row normalization")
    return matrix


def multiply(left, right):
    return [[sum(x*y for x, y in zip(row, column)) for column in zip(*right)]
            for row in left]


def clock_reference():
    times = [F(i, 8) for i in range(5)]
    for alpha, empty in [(1, F(8, 13)), (2, F(16, 25))]:
        counted = total_paths = local_failures = 0
        for first, last in combinations(range(5), 2):
            direct = transport(times[first], times[last], times[-1], alpha)
            for size in range(last-first):
                for cuts in combinations(range(first+1, last), size):
                    route = (first, *cuts, last)
                    common = local = kernel(F(0), alpha)
                    for i, j in zip(route, route[1:]):
                        common = multiply(common, transport(times[i], times[j], times[-1], alpha))
                        local = multiply(local, transport(times[i], times[j], times[j], alpha))
                    require(common == direct, f"clock composition {route}")
                    counted += 1
                    if first == 0 and last == 4:
                        total_paths += 1
                        local_failures += local != direct
                        require(common[0][0] == empty, "empty prefix probability")
        require((counted, total_paths, local_failures) == (26, 8, 7), "clock path coverage")
        print(f"6  alpha={alpha}: 26 paths agree, P(empty)={empty}; 7 local-end controls differ.")


def classical_reference():
    names = ("r", "rho_over_rho0", "H_times_Tend", "acceleration_times_Tend_squared")
    steps = (128, 256, 512, 1024)
    masses = (F(1, 4), F(1), F(4))
    times = [F(i, 4) for i in range(5)]
    expected = set(product(steps, masses, times, names))
    max_errors = {n: F(0) for n in steps}
    path = DUST / "correspondence_v0_1/results/reference_comparisons.csv"
    with path.open(encoding="utf-8", newline="") as stream:
        for row in csv.DictReader(stream):
            n, m, x = int(row["steps"]), F(row["M"]), F(row["x"])
            name = row["observable"]
            expected.remove((n, m, x, name))  # Also rejects duplicate or unknown rows.
            k = F(isqrt(m.numerator), isqrt(m.denominator))
            require(k*k == m, "rational mass root")
            s = 1 - k*x/4
            lo, hi = F(row["ODE_enclosure_lo"]), F(row["ODE_enclosure_hi"])
            if name == "r":
                inside = lo**3 <= s*s <= hi**3
            else:
                values = {names[1]: 1/s**2, names[2]: -k/(6*s), names[3]: -m/(72*s**2)}
                inside = lo <= values[name] <= hi
            require(inside, f"classical enclosure {n, m, x, name}")
            errors = [abs(F(row[key])) for key in ("relative_error_lo", "relative_error_hi")]
            max_errors[n] = max(max_errors[n], *errors)
    require(not expected, "missing classical comparison")
    fine = max_errors[1024]
    require(fine <= F(1, 200) and f"{float(100*fine):.6f}" == "0.130628", "fine error bound")
    # At x=0 the perturbation changes v'' by 32*pi^2/10000 and leaves v,v' fixed.
    relative_shift = (32*pi*pi/10000) / 3 / (1/72)
    require(f"{100*relative_shift:.1f}" == "75.8", "acceleration counterexample")
    print(f"7  All 240 classical enclosures contain the reference; finest bound {100*float(fine):.6f}%.")
    print(f"   Five equal samples of volume and slope allow a {100*relative_shift:.1f}% acceleration shift.")


if __name__ == "__main__":
    state_space()
    preparations()
    clock_reference()
    classical_reference()
