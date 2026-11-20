"""Independently verify the nine rational deformations with Python's standard library."""
from collections import defaultdict
from fractions import Fraction as Q
from hashlib import sha256
from itertools import combinations, permutations
from pathlib import Path
import json
from zipfile import ZipFile


BASE = Path(__file__).resolve().parent
ARCHIVE = "CST_DUST_Praefix_1564_Selektionsgleichung_v0_1_Pruefpaket.zip"


def require(ok, message):
    if not ok:
        raise ValueError(message)


def permuted(code, labels):
    return sum(1 << (6*labels[i]+labels[j]) for i in range(6) for j in range(6)
               if code & (1 << (6*i+j)))


def end_type(code):
    """Read the minimum bit mask over all topological numberings of the six inner events."""
    pairs = list(combinations(range(6), 2))
    edges = [(i, j) for i in range(6) for j in range(6) if code & (1 << (6*i+j))]
    def masks():
        for order in permutations(range(6)):
            if all(order[i] < order[j] for i, j in edges):
                yield sum(1 << pairs.index((order[i],order[j])) for i, j in edges)
    return min(masks())


def main():
    zpath = BASE / ARCHIVE
    require(sha256(zpath.read_bytes()).hexdigest() ==
            "4a2b985578e9bf41662af0dede7c2054c8406de4f49d077891f505b0fffd917e", "Archive digest")
    with ZipFile(zpath) as z:
        def source(name):
            return json.loads(z.read("prefix_1564_selection_v0_1/inputs/"+name))["one"]
        prior = json.loads(z.read("prefix_1564_selection_v0_1/result.json"))
        catalogue = source("exchange.json")
        residual = source("exchange_certificate.json")["residual_orbit_masses"]
    local = json.loads((BASE/"certificate.json").read_text())["one"]["prefix"]
    law = {}
    for k, value in catalogue["target_pair_marginal"].items():
        pair = {int(k), permuted(int(k), (0, 1, 2, 4, 3, 5))}
        for p in pair:
            law[p] = Q(value)/len(pair)
    mask = sum(1 << (6*i+j) for i in range(5) for j in range(5) if i != j)
    uniform = Q(catalogue["max_uniform_labelled_path_component"])
    paths_count = catalogue["paths_valid_in_all_six_orders"]
    require(law[1564] == Q(1,147) and local["reference_type"] == 1790, "Reference")
    require(set(local["end_types"]) == set(map(int, prior["conditional_weights_at_zero"])),
            "Local end types differ from the archived row")
    require(len(local["moves"]) == 9, "Nine independent targets required")
    require(set(map(int, local["moves"])) == set(local["end_types"]) - {1790}, "Local target list")
    for target, move in local["moves"].items():
        step = Q(move["symmetric_positive_step"])
        require(step > 0, "Positive step required")
        marginal_change, local_change = defaultdict(Q), defaultdict(Q)
        for key, change in move["path_deltas"].items():
            code = int(key)
            orbit = {permuted(code, (0, 1, 2, *s)) for s in permutations((3, 4, 5))}
            require(code == min(orbit), "Noncanonical orbit key")
            end = end_type(code)
            require(end in catalogue["fully_admissible_end_types"], "Unknown end type")
            base = uniform/paths_count + (1-uniform)*Q(residual.get(key, 0))/len(orbit)
            delta = Q(change)
            require(base > step*abs(delta), "Negative or zero perturbed weight")
            for marked in orbit:
                prefix = marked & mask
                require(prefix in law, "Unadmitted marked prefix")
                marginal_change[prefix] += delta
                if prefix == 1564:
                    local_change[end] += delta/law[1564]
        require(all(v == 0 for v in marginal_change.values()), "Changed N13 marginal")
        require({k:v for k,v in local_change.items() if v} == {int(target):1,1790:-1},
                "Incorrect local deformation")
    print("PASS: 9 independent exchanges of conditional amplitude coefficients at prefix 1564")


if __name__ == "__main__":
    main()
