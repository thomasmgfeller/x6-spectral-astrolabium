"""Independent Python finite-sum reference: physical response, EIG, optimal plan and posterior.

Does not import/execute the JavaScript implementation. Validates a synthetic run,
not real physics, independent sensor operation or security.
"""
import argparse
import itertools
import json
import math
from pathlib import Path
from jsonschema import Draft202012Validator
from build_contract import build

HERE = Path(__file__).resolve().parent
def near(actual, expected):
    if not math.isfinite(actual) or abs(actual - expected) > 1e-10:
        raise ValueError(f"reference mismatch: {actual} != {expected}")

def model_probabilities(c, p):
    return [math.fsum(x for x, s in zip(p, c["states"]) if s["model_id"] == m["id"]) for m in c["models"]]

def entropy(p):
    return -math.fsum(x * math.log2(x) for x in p if x > 0)

def update(p, experiments, outcomes):
    terms = [weight * math.prod(e["p_one"][s] if outcome else 1 - e["p_one"][s]
                               for e, outcome in zip(experiments, outcomes)) for s, weight in enumerate(p)]
    norm = math.fsum(terms)
    return norm, [x / norm for x in terms] if norm else None

def information(c, p, experiments):
    expected = 0
    for outcomes in itertools.product((0, 1), repeat=len(experiments)):
        probability, posterior = update(p, experiments, outcomes)
        if probability:
            expected += probability * entropy(model_probabilities(c, posterior))
    return entropy(model_probabilities(c, p)) - expected

def verify(record):
    if record["evidence_kind"] != "SYNTHETIC_CONTROL":
        raise ValueError("physical evidence is not accepted by this reference")
    schema = build()
    Draft202012Validator.check_schema(schema)
    if schema != json.loads((HERE / "protocol.schema.json").read_text()):
        raise ValueError("stale protocol schema")
    validator = Draft202012Validator(schema)
    c = record["campaign"]
    p = [s["prior"] for s in c["states"]]
    experiments = {e["id"]: e for e in c["experiments"]}
    # Reconstruct likelihoods from m*x''+c*x'+k*x=F, independently of JS tables.
    for e in c["experiments"]:
        for index, state in enumerate(c["states"]):
            if state["model_id"] == "OTHER":
                expected = 0.5
            else:
                m = next(m for m in c["models"] if m["id"] == state["model_id"])
                w = e["omega_rad_s"]
                amp = w * w / math.sqrt((m["stiffness_n_m"] - m["mass_kg"] * w * w) ** 2 + (m["damping_ns_m"] * w) ** 2)
                expected = 1 / (1 + math.exp(-(state["gain"] * amp - e["threshold"]) / e["noise_scale"]))
            near(e["p_one"][index], expected)
    for entry in record["events"]:
        event = entry["event"]
        for a, b in zip(event["prior"], p):
            near(a, b)
        for message in event["jobs"] + event["results"]:
            validator.validate(message)
        selected = [experiments[j["experiment_id"]] for j in event["jobs"]]
        gain = information(c, p, selected)
        near(event["plan"]["expected_information_bits"], gain)
        # Exhaustive independent admissible assignment enumeration under the runner's registered policy.
        candidates = []
        for assignment in itertools.product(*[
            [None] + [e for e in c["experiments"] if n["available"] and n["execution_mode"] == "SIMULATION_ONLY" and e["capability"] in n["capabilities"]]
            for n in record["nodes"]
        ]):
            chosen = [e for e in assignment if e]
            specimens = [n["specimen_id"] for n, e in zip(record["nodes"], assignment) if e]
            cost = sum(e["cost"] for e in chosen)
            if not chosen or len(chosen) > 2 or len(set(specimens)) != len(specimens) or cost > 2:
                continue
            candidates.append(information(c, p, chosen) - 0.01 * cost)
        near(event["plan"]["utility"], max(candidates))
        probability, p = update(p, selected, [r["outcome"] for r in event["results"]])
        if p is None:
            raise ValueError("unexpected zero predictive probability in supplied mechanical fixture")
        near(event["predictive_probability"], probability)
        for a, b in zip(event["posterior"], p):
            near(a, b)
    for model, probability in zip(c["models"], model_probabilities(c, p)):
        near(record["final_model_probabilities"][model["id"]], probability)
    return {"status": "INDEPENDENT_NUMERICAL_REFERENCE_PASS", "batches": len(record["events"]),
            "likelihood_entries": len(c["experiments"]) * len(c["states"]), "tolerance": 1e-10,
            "physical_evidence": False, "scope": "Registered finite simulation and message schemas; no external scientific review."}

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("run_json", type=Path)
    args = parser.parse_args()
    print(json.dumps(verify(json.loads(args.run_json.read_text())), indent=2))
