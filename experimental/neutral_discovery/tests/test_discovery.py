"""Scientific failure controls, neutral decisions, and exact gate size."""
from copy import deepcopy
from fractions import Fraction
from itertools import product
import json
from math import comb
from pathlib import Path
import subprocess
import sys
import unittest

HERE = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(HERE))
import discovery as d


class DiscoveryTests(unittest.TestCase):
    def setUp(self):
        self.c = d.make_contract()
        self.weights = d.initial(self.c)

    def records(self):
        return d.records_for(self.c, "common_cause", 17, "fresh")

    def test_law_search_finds_only_primitive_observational_relation(self):
        found = d.law_candidates([[0, 0], [1, 1]])
        self.assertEqual([r["coefficients_c_x_y"] for r in found], [[0, 1, -1]])
        self.assertEqual(found[0]["status"], "OBSERVATIONAL_RELATION_CANDIDATE")
        self.assertEqual(d.law_candidates([[0, 0], [1, 1], [0, 1]]), [])
        with self.assertRaisesRegex(ValueError, "variation"):
            d.law_candidates([[1, 1], [1, 1]])

    def test_observational_collision_and_interventional_separation(self):
        self.assertAlmostEqual(d.information(self.c, self.weights, ["observe"]), 0)
        self.assertGreater(d.information(self.c, self.weights, ["do_x_1"]), 0)
        self.assertEqual(len(d.explanation_classes(d.generator_candidates())), 3)
        self.assertEqual(d.choose_batch(self.c, self.weights)["interventions"], ["do_x_1", "do_y_1"])

    def test_joint_information_does_not_add_individual_scores(self):
        joint = d.information(self.c, self.weights, ["do_x_1", "do_x_1"])
        naive = 2*d.information(self.c, self.weights, ["do_x_1"])
        self.assertLess(joint, naive)

    def test_representation_duplicates_have_no_extra_prior_mass(self):
        base = d.generator_candidates()
        duplicate = deepcopy(base[0])
        duplicate["mechanism"] = "another_syntax_for_the_same_predictions"
        duplicate["p_one"]["observe"] = "2/2"
        self.assertEqual(d.explanation_classes(base), d.explanation_classes(base+[duplicate]*20))

    def test_aliases_including_lorentz_do_not_enter_computation(self):
        base = d.generator_candidates()
        for names in [("Lorentz", "Galilei", "unknown"), ("unknown", "Lorentz", "Euclidean")]:
            renamed = [{**c, "mechanism": label} for c, label in zip(base, names)]
            c = deepcopy(self.c)
            c["classes"] = d.explanation_classes(renamed)
            self.assertEqual(d.choose_batch(c, d.initial(c)), d.choose_batch(self.c, self.weights))
            self.assertEqual(d.Gate(c, []).evaluate(c, self.records()),
                             d.Gate(self.c, []).evaluate(self.c, self.records()))

    def test_class_order_does_not_change_plan_or_posterior(self):
        c = deepcopy(self.c)
        c["classes"].reverse()
        self.assertEqual(d.choose_batch(c, self.weights), d.choose_batch(self.c, self.weights))
        self.assertEqual(d.posterior(c, self.weights, ["do_y_1"], [0]),
                         d.posterior(self.c, self.weights, ["do_y_1"], [0]))

    def test_contract_rejects_target_fields_and_physical_execution(self):
        from jsonschema import ValidationError
        for location, key, value in [("root", "preferred_geometry", "Lorentz"),
                                     ("class", "target_bonus", 1),
                                     ("root", "evidence_kind", "PHYSICAL")]:
            c = deepcopy(self.c)
            (c if location == "root" else c["classes"][0])[key] = value
            with self.assertRaises(ValidationError):
                d.validate(c)

    def test_semantic_prior_and_identity_guards(self):
        c = deepcopy(self.c)
        c["classes"][0]["prior"] = "1/2"
        with self.assertRaisesRegex(ValueError, "prior"):
            d.validate(c)
        c = deepcopy(self.c)
        c["classes"][0]["p_one"]["do_x_1"] = "2"
        with self.assertRaisesRegex(ValueError, "probability"):
            d.validate(c)

    def test_noncanonical_fraction_cannot_disguise_duplicate_classes(self):
        c = deepcopy(self.c)
        c["classes"][0]["p_one"]["observe"] = "2/2"
        c["classes"][0]["id"] = "C-" + d.digest(c["classes"][0]["p_one"])[:12]
        with self.assertRaisesRegex(ValueError, "canonical"):
            d.validate(c)

    def test_impossible_observation_reports_missing_model(self):
        p, updated = d.posterior(self.c, self.weights, ["observe"], [0])
        self.assertEqual(p, 0)
        self.assertIsNone(updated)

    def test_exact_binomial_size_for_each_null_and_family(self):
        n, alpha = 24, Fraction(1, 20)
        threshold = alpha / 6
        # Exhaust ALL sufficient-statistic outcomes under each registered null.
        for p in (Fraction(1, 2), Fraction(1)):
            size = sum(Fraction(comb(n, k))*p**k*(1-p)**(n-k)
                       for k in range(n+1) if d.binomial_p_value(n, k, p) <= threshold)
            self.assertLessEqual(size, threshold)
            self.assertLessEqual(6*size, alpha)  # union bound; no independence between tests needed
        self.assertEqual(d.binomial_p_value(24, 24, Fraction(1, 2)), Fraction(1, 2**23))

    def test_champion_can_fail_same_gate_as_every_other_class(self):
        # Constructed stress fixture, NOT a randomly selected successful run.
        _, weights = d.posterior(self.c, self.weights, ["do_x_1", "do_x_1"], [1, 1])
        for _ in range(3):
            _, weights = d.posterior(self.c, weights, ["do_x_1", "do_x_1"], [1, 1])
        leader = max(weights, key=weights.get)
        self.assertGreater(weights[leader], Fraction(99, 100))
        records = self.records()
        for e in self.c["falsification"]["interventions"]:
            for i, r in enumerate(r for r in records if r["intervention"] == e):
                r["outcome"] = i % 2
        report = d.Gate(self.c, []).evaluate(self.c, records)
        self.assertEqual(next(r for r in report["classes"] if r["class_id"] == leader)["status"],
                         "REJECTED_WITHIN_REGISTERED_TEST")
        self.assertEqual(sum(r["status"] == "NOT_REJECTED" for r in report["classes"]), 1)
        self.assertEqual(d.challenge_order(self.c, weights)["probes"][0]["intervention"], "do_x_1")

    def test_all_classes_can_fail_without_forced_winner(self):
        records = self.records()
        for r in records:
            r["outcome"] = 1
        report = d.Gate(self.c, []).evaluate(self.c, records)
        self.assertEqual(report["status"], "MODEL_SET_INADEQUATE")
        self.assertEqual(report["theory"], "NOT_ESTABLISHED")

    def test_gate_freeze_reuse_and_fixed_n(self):
        gate = d.Gate(self.c, ["already-used"])
        changed = deepcopy(self.c)
        changed["falsification"]["alpha"] = "1/2"
        with self.assertRaisesRegex(ValueError, "changed"):
            gate.evaluate(changed, self.records())
        records = self.records()
        records[0]["id"] = "already-used"
        with self.assertRaisesRegex(ValueError, "reused"):
            gate.evaluate(self.c, records)
        records = self.records()
        with self.assertRaisesRegex(ValueError, "sample plan"):
            gate.evaluate(self.c, records[:-1])
        gate.evaluate(self.c, records)
        with self.assertRaisesRegex(ValueError, "consumed"):
            gate.evaluate(self.c, records)

    def test_gate_rejects_duplicate_wrong_binding_and_physical_evidence(self):
        for change in (lambda rs: rs[0].update(id=rs[1]["id"]),
                       lambda rs: rs[0].update(contract_sha256="0"*64),
                       lambda rs: rs[0].update(evidence_kind="PHYSICAL"),
                       lambda rs: rs[0].update(outcome=True)):
            records = self.records()
            change(records)
            with self.assertRaises(ValueError):
                d.Gate(self.c, []).evaluate(self.c, records)

    def test_published_controls_replay_without_promoting_geometry(self):
        actual = d.reference()
        self.assertEqual(json.loads((HERE/"examples/control.json").read_text()), actual)
        for run in actual["controls"]:
            self.assertEqual(run["falsification"]["geometry"], "NOT_IDENTIFIED")
            self.assertEqual(run["falsification"]["physical"], "NOT_TESTED")
            self.assertEqual(sum(c["status"] == "NOT_REJECTED" for c in run["falsification"]["classes"]), 1)

    def test_independent_existing_js_planner_matches_all_binary_batches(self):
        # Existing fabric implementation uses floating arithmetic, not this Fraction code.
        payload = d.fabric_campaign(self.c)
        script = """
          import {validateCampaign,information,plan,condition} from './experimental/experiment_fabric/core.mjs';
          let input=''; for await(const chunk of process.stdin) input+=chunk;
          const c=validateCampaign(JSON.parse(input)), w=c.states.map(s=>s.prior);
          const nodes=['A','B'].map(id=>({id,specimen_id:id,available:true,execution_mode:'SIMULATION_ONLY',capabilities:['BINARY_SCM_SIM']}));
          const batches=c.experiments.flatMap(a=>c.experiments.map(b=>({es:[a.id,b.id],eig:information(c,w,[a.id,b.id]),
            updates:[[0,0],[0,1],[1,0],[1,1]].map(ys=>condition(c,w,[a.id,b.id],ys))})));
          console.log(JSON.stringify({plan:plan(c,w,nodes,{budget:2,max_batch:2,cost_weight:0}),batches}));
        """
        result = subprocess.run(["node", "--input-type=module", "-e", script], input=json.dumps(payload),
                                cwd=HERE.parents[1], capture_output=True, text=True, check=True)
        output = json.loads(result.stdout)
        self.assertEqual([a["experiment_id"] for a in output["plan"]["assignments"]],
                         d.choose_batch(self.c, self.weights)["interventions"])
        for batch in output["batches"]:
            self.assertAlmostEqual(batch["eig"], d.information(self.c, self.weights, batch["es"]), places=12)
            for ys, js in zip(product((0, 1), repeat=2), batch["updates"]):
                p, updated = d.posterior(self.c, self.weights, batch["es"], list(ys))
                self.assertAlmostEqual(float(p), js["predictive"], places=12)
                if updated:
                    for c, v in zip(self.c["classes"], js["posterior"]):
                        self.assertAlmostEqual(float(updated[c["id"]]), v, places=12)
                else:
                    self.assertEqual(js["status"], "MODEL_SET_INADEQUATE")


if __name__ == "__main__":
    unittest.main()
