#!/usr/bin/env python3
"""Finite, outcome-neutral discovery control. No physical execution or theory claim."""
from __future__ import annotations

from fractions import Fraction
from hashlib import sha256
from itertools import product
import json
from math import comb, gcd, log2
from pathlib import Path
import random
import sys

VERSION = "x6.neutral-discovery/0.1.0"
INTERVENTIONS = ("observe", "do_x_1", "do_y_1")
MECHANISMS = ("x_to_y", "y_to_x", "common_cause")


def require(condition, message):
    if not condition:
        raise ValueError(message)


def digest(value):
    return sha256(json.dumps(value, sort_keys=True, separators=(",", ":"),
                             ensure_ascii=False, allow_nan=False).encode()).hexdigest()


def law_candidates(rows):
    """Enumerate primitive affine relations c + a*x + b*y = 0; exact binary data."""
    require(len(rows) >= 2 and all(len(r) == 2 and all(type(v) is int and v in (0, 1)
            for v in r) for r in rows), "binary observations required")
    require(len(set(map(tuple, rows))) >= 2, "insufficient variation")
    found = set()
    for coefficients in product(range(-1, 2), repeat=3):
        c, a, b = coefficients
        if a == b == 0 or not all(c + a*x + b*y == 0 for x, y in rows):
            continue
        factor = gcd(gcd(abs(c), abs(a)), abs(b))
        primitive = tuple(v // factor for v in coefficients)
        if next(v for v in primitive if v) < 0:
            primitive = tuple(-v for v in primitive)
        found.add(primitive)
    return [{"coefficients_c_x_y": list(c), "status": "OBSERVATIONAL_RELATION_CANDIDATE",
             "domain": "registered binary support only", "units": ["1", "1", "1"]}
            for c in sorted(found)]


def outcome(mechanism, intervention, u):
    """Surgical do sets a variable; outgoing mechanisms remain in force."""
    require(mechanism in MECHANISMS and intervention in INTERVENTIONS and u in (0, 1),
            "unknown generator or intervention")
    if intervention == "observe":
        return 1  # observable: X == Y; all three generators yield X=Y=U.
    if intervention == "do_x_1":
        return 1 if mechanism == "x_to_y" else u  # observable: Y
    return 1 if mechanism == "y_to_x" else u      # observable: X


def generator_candidates():
    # Explicit finite grammar, not a universal generator synthesizer.
    return [{"mechanism": mechanism, "p_one": {
        e: str(Fraction(sum(outcome(mechanism, e, u) for u in (0, 1)), 2))
        for e in INTERVENTIONS}} for mechanism in MECHANISMS]


def explanation_classes(candidates):
    """Quotient by EXACT predictions on the registered intervention catalogue.

    Multiple representations do not gain prior mass. This does not identify
    physical equivalence beyond this finite catalogue and observation channel.
    """
    signatures = {tuple(str(Fraction(c["p_one"][e])) for e in INTERVENTIONS) for c in candidates}
    require(len(signatures) >= 2, "at least two explanation classes required")
    result = []
    for signature in sorted(signatures):
        p = {e: str(Fraction(v)) for e, v in zip(INTERVENTIONS, signature)}
        require(all(0 <= Fraction(v) <= 1 for v in p.values()), "invalid probability")
        result.append({"id": "C-" + digest(p)[:12], "p_one": p,
                       "prior": str(Fraction(1, len(signatures)))})
    return result


def make_contract():
    return {"schema": VERSION, "evidence_kind": "SYNTHETIC_CONTROL",
            "objective": "JOINT_INFORMATION_ABOUT_EXPLANATION_CLASS",
            "class_rule": "EXACT_PREDICTIVE_EQUALITY_ON_REGISTERED_CATALOGUE",
            "prior_rule": "UNIFORM_OVER_DISTINCT_CLASSES",
            "dependence": "INDEPENDENT_REPLICAS_GIVEN_CLASS",
            "classes": explanation_classes(generator_candidates()),
            "interventions": list(INTERVENTIONS),
            "design": {"batch_size": 2, "rounds": 4,
                       "cost_per_observation": 1, "cost_budget_per_batch": 2},
            "falsification": {"rule": "FIXED_N_EXACT_BINOMIAL_BONFERRONI",
                              "alpha": "1/20", "n_per_intervention": 24,
                              "interventions": ["do_x_1", "do_y_1"],
                              "looks": 1},
            "claims": {"geometry": "NOT_IDENTIFIED", "theory": "NOT_ESTABLISHED",
                       "physical": "NOT_TESTED"}}


def validate(contract):
    # Closed, self-contained schema plus semantic checks; no labels/target fields.
    from jsonschema import Draft202012Validator
    schema = json.loads(Path(__file__).with_name("contract.schema.json").read_text())
    Draft202012Validator(schema).validate(contract)
    classes = contract["classes"]
    require(all(str(Fraction(v)) == v for c in classes for v in [c["prior"], *c["p_one"].values()]),
            "probabilities and priors must use canonical reduced fractions")
    require(len({c["id"] for c in classes}) == len(classes), "duplicate class id")
    require(len({digest(c["p_one"]) for c in classes}) == len(classes), "duplicate explanation class")
    require(all(set(c["p_one"]) == set(contract["interventions"]) for c in classes), "prediction coverage")
    require(all(0 <= Fraction(p) <= 1 for c in classes for p in c["p_one"].values()), "probability bounds")
    require(all(Fraction(c["prior"]) == Fraction(1, len(classes)) for c in classes), "class prior rule")
    require(all(c["id"] == "C-" + digest(c["p_one"])[:12] for c in classes), "class identity mismatch")
    require(Fraction(contract["falsification"]["alpha"]) == Fraction(1, 20), "fixed error budget")
    return contract


def initial(contract):
    return {c["id"]: Fraction(c["prior"]) for c in contract["classes"]}


def posterior(contract, weights, experiments, observations):
    require(set(weights) == {c["id"] for c in contract["classes"]} and
            all(w >= 0 for w in weights.values()) and sum(weights.values()) == 1,
            "invalid class weights")
    require(1 <= len(experiments) == len(observations) <= 2 and
            all(e in contract["interventions"] for e in experiments) and
            all(type(y) is int and y in (0, 1) for y in observations), "invalid batch")
    updated = dict(weights)
    for c in contract["classes"]:
        for e, y in zip(experiments, observations):
            p = Fraction(c["p_one"][e])
            updated[c["id"]] *= p if y else 1-p
    predictive = sum(updated.values())
    return (predictive, {k: v/predictive for k, v in updated.items()}) if predictive else (predictive, None)


def entropy(weights):
    return -sum(float(w)*log2(float(w)) for w in weights.values() if w)


def information(contract, weights, experiments):
    expected = 0.0
    for ys in product((0, 1), repeat=len(experiments)):
        p, updated = posterior(contract, weights, experiments, ys)
        if p:
            expected += float(p) * entropy(updated)
    return max(0.0, entropy(weights)-expected)


def choose_batch(contract, weights):
    candidates = [(information(contract, weights, es), es)
                  for es in product(sorted(contract["interventions"]), repeat=2)]
    maximum = max(v for v, _ in candidates)
    # Predeclared neutral tie rule; labels never enter. Repeated interventions allowed.
    tied = sorted(es for value, es in candidates if abs(value-maximum) <= 1e-12)
    return {"interventions": list(tied[0]) if maximum > 1e-12 else [],
            "expected_information_bits": maximum,
            "status": "PLANNED" if maximum > 1e-12 else "NO_DISCRIMINATING_INTERVENTION"}


def binomial_p_value(n, k, p):
    """Exact two-sided probability ordering, Fraction arithmetic including endpoints."""
    masses = [Fraction(comb(n, j))*p**j*(1-p)**(n-j) for j in range(n+1)]
    return sum(m for m in masses if m <= masses[k])


def rejection_power(n, p_null, p_alternative, threshold):
    return sum(Fraction(comb(n, k))*p_alternative**k*(1-p_alternative)**(n-k)
               for k in range(n+1) if binomial_p_value(n, k, p_null) <= threshold)


def challenge_order(contract, weights):
    """Rank registered probes by power against the current leader; no test removed.

    Planning weights affect allocation priority, never the test level or null.
    All predeclared tests are still performed at fixed N.
    """
    leader = sorted(weights, key=lambda k: (-weights[k], k))[0]
    by_id = {c["id"]: c for c in contract["classes"]}
    gate = contract["falsification"]
    threshold = Fraction(gate["alpha"]) / (len(by_id)*len(gate["interventions"]))
    alternatives = sum(w for k, w in weights.items() if k != leader)
    scored = []
    for e in gate["interventions"]:
        p0 = Fraction(by_id[leader]["p_one"][e])
        score = (sum(w * rejection_power(gate["n_per_intervention"], p0,
                    Fraction(by_id[k]["p_one"][e]), threshold)
                    for k, w in weights.items() if k != leader) / alternatives) if alternatives else Fraction(0)
        scored.append({"intervention": e, "expected_rejection_power_against_leader": float(score)})
    return {"leader": leader, "probes": sorted(scored, key=lambda r: (-r["expected_rejection_power_against_leader"], r["intervention"])),
            "status": "RANKED" if alternatives else "NO_WEIGHTED_ALTERNATIVE_EXTERNAL_CHALLENGES_NEEDED"}


class Gate:
    """One fixed-sample look. In-memory lifecycle guard, not durable access control."""
    def __init__(self, contract, used_ids):
        validate(contract)
        self.contract = json.loads(json.dumps(contract))
        self.contract_hash = digest(self.contract)
        self.used_ids = frozenset(used_ids)
        self.consumed = False

    def evaluate(self, contract, records):
        require(not self.consumed, "gate already consumed; no optional second look")
        require(digest(contract) == self.contract_hash, "contract changed after freeze")
        require(all(set(r) == {"id", "contract_sha256", "phase", "evidence_kind", "intervention", "outcome"}
                    for r in records), "unexpected result field")
        identifiers = [r["id"] for r in records]
        require(all(isinstance(v, str) and v for v in identifiers) and
                len(set(identifiers)) == len(identifiers), "duplicate/invalid evidence id")
        require(not self.used_ids.intersection(identifiers), "proposal/selection evidence cannot be reused")
        require(all(r["contract_sha256"] == self.contract_hash and r["phase"] == "SEALED_CHALLENGE" and
                    r["evidence_kind"] == "SYNTHETIC_CONTROL" and type(r["outcome"]) is int and
                    r["outcome"] in (0, 1) for r in records), "invalid evidence binding or kind")
        gate = self.contract["falsification"]
        es, n = gate["interventions"], gate["n_per_intervention"]
        require(len(records) == len(es)*n and all(r["intervention"] in es for r in records) and
                all(sum(r["intervention"] == e for r in records) == n for e in es), "fixed sample plan violated")
        threshold = Fraction(gate["alpha"]) / (len(self.contract["classes"])*len(es))
        results = []
        for c in self.contract["classes"]:
            tests = []
            for e in es:
                k = sum(r["outcome"] for r in records if r["intervention"] == e)
                pv = binomial_p_value(n, k, Fraction(c["p_one"][e]))
                tests.append({"intervention": e, "n": n, "ones": k, "p_value": str(pv),
                              "rejected": pv <= threshold})
            results.append({"class_id": c["id"], "status": "REJECTED_WITHIN_REGISTERED_TEST" if any(
                t["rejected"] for t in tests) else "NOT_REJECTED", "tests": tests})
        self.consumed = True
        return {"contract_sha256": self.contract_hash, "evidence_sha256": digest(records),
                "per_test_threshold": str(threshold), "classes": results,
                "status": "MODEL_SET_INADEQUATE" if all(c["status"] != "NOT_REJECTED" for c in results)
                else "SURVIVORS_REQUIRE_FURTHER_TESTS",
                "geometry": "NOT_IDENTIFIED", "theory": "NOT_ESTABLISHED", "physical": "NOT_TESTED"}


def records_for(contract, mechanism, seed, prefix):
    rng = random.Random(seed)
    return [{"id": f"{prefix}.{e}.{i}", "contract_sha256": digest(contract),
             "phase": "SEALED_CHALLENGE", "evidence_kind": "SYNTHETIC_CONTROL",
             "intervention": e, "outcome": outcome(mechanism, e, rng.randrange(2))}
            for e in contract["falsification"]["interventions"]
            for i in range(contract["falsification"]["n_per_intervention"])]


def fabric_campaign(contract):
    """Adapter to the existing JS class-information planner, not its sensor executor."""
    validate(contract)
    return {"schema": "x6.experiment-fabric/0.1.0", "campaign_id": "neutral-discovery-control",
            "evidence_kind": "SYNTHETIC_CONTROL",
            "dependence": "INDEPENDENT_GIVEN_PERSISTENT_LATENT_STATE",
            "models": [{"id": c["id"]} for c in contract["classes"]],
            "states": [{"id": c["id"], "model_id": c["id"], "prior": float(Fraction(c["prior"]))}
                       for c in contract["classes"]],
            "experiments": [{"id": e, "cost": 1, "capability": "BINARY_SCM_SIM",
                             "p_one": [float(Fraction(c["p_one"][e])) for c in contract["classes"]]}
                            for e in contract["interventions"]]}


def run_control(mechanism, seed):
    contract = validate(make_contract())
    rows = [[0, 0], [1, 1]]  # exhaustive support, not a physical time series
    candidates = law_candidates(rows)
    weights, rng = initial(contract), random.Random(seed)
    ids, events = ["proposal.0", "proposal.1"], []
    for revision in range(contract["design"]["rounds"]):
        plan = choose_batch(contract, weights)
        if not plan["interventions"]:
            break
        ys = [outcome(mechanism, e, rng.randrange(2)) for e in plan["interventions"]]
        evidence_ids = [f"selection.{revision}.{i}" for i in range(len(ys))]
        ids.extend(evidence_ids)
        predictive, updated = posterior(contract, weights, plan["interventions"], ys)
        events.append({"plan": plan, "outcomes": ys, "evidence_ids": evidence_ids,
                       "predictive_probability": str(predictive)})
        if updated is None:
            break
        weights = updated
    gate = Gate(contract, ids)  # freeze before generating the challenge observations
    ranking = challenge_order(contract, weights)
    records = records_for(contract, mechanism, seed+10000, "challenge")
    return {"schema": VERSION, "evidence_kind": "SYNTHETIC_CONTROL", "contract": contract,
            "contract_sha256": digest(contract), "simulation_truth": mechanism, "seed": seed,
            "proposal_rows": rows, "law_candidates": candidates, "selection": events,
            "relative_class_weights": {k: str(v) for k, v in weights.items()},
            "challenge_priority": ranking, "challenge_records": records,
            "falsification": gate.evaluate(contract, records)}


def reference():
    return {"schema": VERSION, "scope": "FINITE_LOGICAL_CONTROL_NOT_PHYSICS_DISCOVERY",
            "controls": [run_control(m, 20261014+i) for i, m in enumerate(MECHANISMS)]}


if __name__ == "__main__":
    require(len(sys.argv) == 3 and sys.argv[1] in ("run", "verify", "fabric"),
            "usage: discovery.py run NEW_JSON | verify JSON | fabric NEW_JSON")
    command, path = sys.argv[1], Path(sys.argv[2])
    if command == "verify":
        require(json.loads(path.read_text()) == reference(), "reference replay differs")
        print("PASS: exact reference replay; no physical or geometric claim")
    else:
        result = reference() if command == "run" else fabric_campaign(make_contract())
        with path.open("x") as handle:
            json.dump(result, handle, indent=2, ensure_ascii=False, allow_nan=False)
            handle.write("\n")
        print(path)
