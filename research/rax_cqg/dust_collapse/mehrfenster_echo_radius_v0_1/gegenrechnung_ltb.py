"""Independent nominal LTB time-of-flight control. No radius-estimation code.

Compare two parameterizations of the local null geodesic with fixed comoving
endpoints. This floating-point control does not certify a first arrival or
provide the intervals used to decide the window bits.
"""
import argparse
from fractions import Fraction
from hashlib import sha256
from importlib.util import module_from_spec, spec_from_file_location
from itertools import combinations
import json
from math import sqrt
from pathlib import Path
import sys


ORIGINAL = {
    "ltb.py": "a6901bca9770761bd124210786930a61a01c8e445d84ace44da69689adecae2b",
    "echos.py": "eb451280271dbd86fc6f84053681c65eceb18af5b1585ad37010f8b56e681ff2",
    "netz.py": "16dc88c3718f32d698c8deef990ecc6046f726130858503a360652617145f486",
    "Netzaufnahmen.json": "b14d2b80e679c8c00bafef77783790d3d10008cf0b77464bef20bc0e8291303f",
}


def source_paths(basis):
    paths = {}
    for name, digest in ORIGINAL.items():
        path = Path(basis) / name
        if name == "ltb.py" and not path.exists():
            path = Path(basis) / "basis" / name
        if sha256(path.read_bytes()).hexdigest() != digest:
            raise ValueError(f"Archiv-Prüfsumme abweichend: {name}")
        paths[name] = path
    return paths


def archive_module(path):
    key = f"mehrfenster_original_{path.stem}"
    spec = spec_from_file_location(key, path)
    mod = module_from_spec(spec)
    old = sys.modules.get(key)
    sys.modules[key] = mod
    try:
        spec.loader.exec_module(mod)
    finally:
        if old is None:
            del sys.modules[key]
        else:
            sys.modules[key] = old
    return mod


def in_proper_time(model, a0, mass, theta, start, steps):
    """Integrate in dust proper time; solve for launch angle and duration.

    mu is the radial direction cosine in the dust tetrad. For E=0 the
    spatial radial and angular coefficients are L=R_a and R. The rates
    H_parallel and H_perp follow independently from the archived mass
    and density functions, using (R_T)^2=2m/R and m'=4*pi*rho*R^2*L.
    """
    theta, a0, mass = float(theta), float(a0), float(mass)
    r0, _, l0, _ = model.evolve(a0, start, mass)
    if not (0 < theta < .001 and r0 > 0):
        raise ValueError("Lokaler kurzer Strahl erforderlich")

    def derivatives(t, state):
        da, _, mu = state
        radius, density, radial_scale, velocity = model.evolve(a0 + da, start + t, mass)
        h_perp = velocity / radius
        # m'/L = 4*pi*rho*R^2, m = R*(R_T)^2/2.
        h_parallel = density * radius / velocity - h_perp / 2
        tangential_sq = 1 - mu * mu
        return (mu / radial_scale, sqrt(tangential_sq) / radius,
                tangential_sq * (1 / radius + (h_perp - h_parallel) * mu))

    def advance(y, k, step):
        return tuple(x + step * d for x, d in zip(y, k))

    def residual(mu, duration):
        state = (0., 0., mu)
        h = duration / steps
        for i in range(steps):
            t = i * h
            k1 = derivatives(t, state)
            k2 = derivatives(t + h / 2, advance(state, k1, h / 2))
            k3 = derivatives(t + h / 2, advance(state, k2, h / 2))
            k4 = derivatives(t + h, advance(state, k3, h))
            state = tuple(x + h * (p + 2*q + 2*r + s) / 6
                          for x, p, q, r, s in zip(state, k1, k2, k3, k4))
        return state[0], state[1] - theta

    # First order Newton preconditioner at a short tangential ray:
    # d(a_endpoint)/d(mu) ~ duration/L; d(phi_endpoint)/d(duration) ~ 1/R.
    duration, mu = r0 * theta, -theta / 2
    for _ in range(8):
        radial_error, angle_error = residual(mu, duration)
        if abs(radial_error) <= 1e-17 and abs(angle_error) <= 3e-19:
            return duration
        mu -= radial_error * l0 / duration
        duration -= angle_error * r0
    raise ArithmeticError("Randwerte im Eigenzeit-Schießen nicht erreicht")


def choose_early(ticks, arc, radial_ratio):
    """Only early tick counts and the initial material-grid standard enter."""
    accepted = []
    for pair, count in ticks.items():
        if arc.contained(arc.decode(count, radial_ratio, Fraction(0))):
            accepted.append(pair.split("|"))
    if len(accepted) != 1:
        raise ValueError("Anzahl früh ausgewählter Kanten ungleich eins")
    u, v = accepted[0]
    sums = {x: sum(n for p, n in ticks.items()
                   if x in p.split("|") and set(p.split("|")) != {u, v}) for x in (u, v)}
    if sums[u] == sums[v]:
        raise ValueError("Orientierung durch frühe Echos unbestimmt")
    return (u, v) if sums[u] > sums[v] else (v, u)


def run(basis):
    paths = source_paths(basis)
    arc = archive_module(paths["echos.py"])
    model = archive_module(paths["ltb.py"])
    network = json.loads(paths["Netzaufnahmen.json"].read_text())
    if (model.CELLS, model.INITIAL_EDGE, arc.TARGET, arc.TICK, arc.STAMP) != (
            640, 10, Fraction(1, 9200), Fraction(1, 10**7), Fraction(2, 10**6)):
        raise ValueError("Geometrie- oder Messparameter abweichend")
    if not (model.END / 2 == 5 * sqrt(5) / 6
            and set(network) == {str(m) for m in arc.MASS}):
        raise ValueError("Archivfamilie oder Bezugsepoche abweichend")

    # Recreate the arrangement fixed in the original netz.py from its
    # tag permutation and offsets, entirely before any late propagation.
    codes = sorted(arc.IDS, key=lambda x: sha256(("Kennung|" + x).encode()).digest())
    factors = {"D": Fraction(0), **dict(zip(codes, arc.FACTORS))}
    fixed_angles = {"|".join(sorted((u, v))): abs(factors[u] - factors[v]) * arc.TARGET
                    for u, v in combinations(factors, 2)}
    rows = {}
    for mass in arc.MASS:
        mask = [model.initial_signal(a, mass) > 0 for a in model.GRID]
        j = arc.locate(mask)
        a_inner = model.GRID[j]
        if (j, a_inner, model.initial_signal(Fraction(10), mass)) != (492, Fraction(1599, 160), 0):
            raise ValueError("Positive Station oder Materiegrenze abweichend")
        ticks = network[str(mass)]["ticks"]
        if set(ticks) != set(fixed_angles):
            raise ValueError("Archiv-Echonetz unvollständig")
        for pair, theta in fixed_angles.items():
            outward = in_proper_time(model, a_inner, mass, theta, 0., 8)
            inward = in_proper_time(model, a_inner, mass, theta, outward, 8)
            if round((outward + inward) / float(arc.TICK)) != ticks[pair]:
                raise ValueError(f"Frühes Echotick abweichend: {pair}, {mass}")
        u, v = choose_early(ticks, arc, a_inner / model.INITIAL_EDGE)
        if (u, v) != ("D", "B"):
            raise ValueError("Früh ausgewähltes Materialpaar abweichend")
        pair = "|".join(sorted((u, v)))
        theta = fixed_angles[pair]
        trials = {}
        for label, a in (("material_station", a_inner), ("support_surface", model.INITIAL_EDGE)):
            t0 = model.END / 2
            local = [in_proper_time(model, a, mass, theta, t0, n) for n in (4, 12)]
            legacy = [arc.shoot(float(a), float(mass), float(theta), t0, n) - t0
                      for n in (4, 12)]
            disagreement = max(local + legacy) - min(local + legacy)
            if disagreement > 2e-14:
                raise ArithmeticError("Eigenzeit- und Winkelintegration weichen voneinander ab")
            trials[label] = {"a_initial": str(a), "duration": local[-1],
                             "max_four_way_difference": disagreement}
        rows[str(mass)] = {"angle_rad": str(theta), "selected_early": [u, v],
                           "early_pair_ticks": ticks[pair], "early_edges_reproduced": len(ticks),
                           "forward_control": trials}
    return rows


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("basis", type=Path, help="Verzeichnis der archivierten Eingaben")
    print(json.dumps(run(parser.parse_args().basis), indent=2, sort_keys=True))
