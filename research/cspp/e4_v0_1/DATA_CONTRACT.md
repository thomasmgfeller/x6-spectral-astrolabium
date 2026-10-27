# E4-V0.1: Datenvertrag

Status: Entwurf, keine Mess- oder Simulationsdaten. Das Schema unten ist
verbindlicher Teil des späteren Freeze; es ist kein ausgeführter Datensatz.
Endgültige Containerformate werden mit dem Runner festgelegt. Ein Register
in JSONL und numerische Arrays in NPZ sind vorgesehen.

## Identität und vollständige Nenner

Primärschlüssel: `(phase_id, scenario_id, density_id, realization_id)`.
Alle geplanten Schlüssel werden vor Beginn einer Phase registriert. Jeder
Schlüssel erhält genau einen Endstatus, auch bei Zeitlimit, fehlendem
Detektorsupport oder fehlgeschlagenem Operator. Ersatzläufe dürfen nicht
unbemerkt denselben Schlüssel oder einen neuen Seed erhalten.

| Gruppe | Pflichtfelder |
| --- | --- |
| Provenienz | contract_revision, source_commit, source_sha256_manifest, environment, RNG_bit_generator, RNG_seed_sequence, started_UTC, ended_UTC |
| Geometrie | nu, rho_L0_4, region_parameters, realized_N, cloud_path, cloud_sha256, order_representation_path, order_sha256, label_map |
| Quelle/Detektor | source_parameters, detector_parameters, adapter_id, quadrature_weights, source_norm_interval, detector_support_count, injection_projection_error_bound |
| Operator | scalar_candidate_id, dirac_candidate_id, nonlocality_scale, G1_metrics, G2_metrics, spin_frame_or_transport_provenance, evidence_paths_and_digests |
| Zertifikate | joint_geometry_region_id, alpha_geometry_run, geometry_status, uniform_G3_status, trace_distance_budget_used, all_error_bounds |
| Zustände | complex_state_artifact_path, state_sha256, flavor_basis, spin_basis, reduction_definition, R_detector_real, R_detector_imag, entrywise_enclosures |
| Qualität | hermiticity_residual, minimum_eigenvalue_interval, global_norm_interval, detector_trace_interval, numerical_repair_attempts |
| Observablen | w0_interval, w1_interval, C_det_interval, q_interval, conditional_normalization_status, conditional_outputs_or_null, reference_intervals |
| Entscheidung | final_status, failed_gates, exception_or_resource_reason, primary_inclusion=true, conditional_only=false/true, runtime_seconds, peak_memory |

Eine vorhandene Rohzahl und ihre wissenschaftliche Freigabe sind getrennte
Felder. Diagnostische Zahlen dürfen trotz HOLD erhalten bleiben; sie sind
keine zertifizierten Primäreingaben. Es gibt keine stillen NaN-Filter.

## Komplexe Größen und mathematische Konsistenz

`R_detector_real` und `R_detector_imag` sind 2x2 reelle Arrays mit festen
Indizes f0,f1. Komplexe Zustände bleiben komplex; RGB ist kein Speicherformat.
Re/Im-Einschließungen müssen explizite untere/obere Grenzen enthalten.
Gemeinsame PSD-/Spurbedingungen werden mitgeführt; eine unabhängige Box
aller Einträge darf nur eine konservative äußere Region sein.

Numerische Projektion auf PSD, Abschneiden negativer Eigenwerte oder
Renormierung ist keine unsichtbare Reparatur. Solche Eingriffe werden mit
ihrer Fehlergrenze dokumentiert oder führen zu HOLD. Für sigma ist zusätzlich
der Nichtdetektionsblock 1-q festgelegt. Dessen Bedeutung darf nicht mit
einem dritten Flavor verwechselt werden.

## Ensemblebericht

Für jede Zelle: planned_M, attempted_M, completed_M, computable_M,
certified_M, every_failure_reason_count. Die primären Nenner sind planned_M,
nicht die Zahl erfolgreicher Runs. Nach planmäßigem Kampagnenabschluss
muss attempted_M=planned_M sein; fehlende Versuche verhindern PASS.

Primär gespeichert werden die acht im Vertrag genannten Momentintervalle,
Biasintervalle, Standardabweichungsintervalle, simultanes alpha, tatsächliche
Halbbreiten, Verfügbarkeitsuntergrenzen und Endentscheidungen. Dazu gehören
R-Mittelwert, E[C_det(R)], C_det(E[R]) und explizit getrennte bedingte
Auswertungen. Nur vollständig berechnete Paare dürfen in zusätzliche
gepaarte Diagnosen eingehen; deren eigener Nenner wird immer gezeigt.

Ein HOLD wegen numerischer Unverfügbarkeit bei definiertem Ziel erhält
für die Primäranalyse dessen volle mögliche Spanne. Ein undefiniertes
physikalisches Modell erhält MODEL_HOLD; dafür wird kein fiktiver Mittelwert
gebildet. Eine Verfügbarkeit nur nach einem G2-Filter wird nicht als
unbedingte Eigenschaft des Poisson-Ensembles berichtet.

## Diagnoseansichten

Kausalstruktur, Ausbreitungsgewicht, Flavorzusammensetzung und Kohärenz
benutzen dieselben archivierten Daten. Jeder Frame zeigt seinen Status und
seine Auswerteparametrisierung. Im Benchmark ist das Referenz-t erlaubt.
BD-Schichten dürfen nicht als Zeitslices beschriftet werden. Geometrie- und
Operatorfehler werden als Unsicherheit sichtbar; sie werden nicht durch
Farbglättung entfernt. Keine Dreiflavor-RGB-Aussage in diesem Zweiflavorvertrag.
