"""Regenerate the isolated d=5 interface control with Stim 1.16.0."""
import hashlib
import json
import math
from pathlib import Path

import stim


def digest(data):
    return hashlib.sha256(data).hexdigest()


def main():
    if stim.__version__ != "1.16.0":
        raise SystemExit("Use Stim 1.16.0 for this frozen development control")
    task = "surface_code:rotated_memory_x"
    ideal = stim.Circuit.generated(task, distance=5, rounds=5)
    final_mx, = [i for i, instruction in enumerate(ideal) if instruction.name == "MX"]
    circuit = ideal[:final_mx] + stim.Circuit("Z_ERROR(0.125) 1") + ideal[final_mx:]
    dem = circuit.detector_error_model(decompose_errors=True)
    errors = [str(term) for term in dem.flattened() if term.type == "error"]
    assert errors == ["error(0.125) D108 L0"] and circuit.num_detectors == 120
    graph = {
        "scope": "synthetic_single_fault_input_control",
        "task": task, "distance": 5, "rounds": 5,
        "detector_count": circuit.num_detectors, "detector_order": "ascending Stim detector ID",
        "circuit_sha256": digest(str(circuit).encode()), "dem_sha256": digest(str(dem).encode()),
        "edges": [{"edge_id": 0, "endpoints": [108, "boundary"], "error_probability": 0.125,
                   "weight": math.log(7), "observable_mask": 1,
                   "adapter_provenance": {"source_event_id": 0, "source_component_index": 0}}],
    }
    graph_hash = digest(json.dumps(graph, sort_keys=True, separators=(",", ":")).encode())
    shots, labels = circuit.compile_detector_sampler(seed=1).sample(shots=1024, separate_observables=True)
    i = next(i for i, bits in enumerate(shots) if bits.any())
    assert shots[i].nonzero()[0].tolist() == [108] and labels[i].tolist() == [True]
    fixture = {
        "graph": graph,
        "shot": {"schema": "x6.qed.detector-shot/1", "frozen_graph_sha256": graph_hash,
                 "detector_bits": shots[i].astype(int).tolist()},
        "evaluation_only": {"observable_flips": labels[i].astype(int).tolist()},
    }
    output = Path(__file__).with_name("qed_d5_single_fault.json")
    output.write_text(json.dumps(fixture, indent=2) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
