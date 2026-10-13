# X6 Phase Filter – Experiment Contract v0.2.0

**Entwicklungsartefakt. Der Filterclaim bleibt UNVALIDATED.**

Diese Veröffentlichung enthält den maschinenlesbaren Versuchscontract, drei
JSON Schemas, einen Python-Vorprüfer, Prüfsummen und gezielte Softwaretests.
Der mitgelieferte Entwurf ist strukturell gültig; seine Ausführung bleibt wegen
offener fachlicher Festlegungen gesperrt. Es wurden damit keine Filterversuche
oder neuen Agentenläufe gestartet und keine Implementierungen als portabel qualifiziert.

- [Anleitung, Grenzen und offene Entscheidungen](contract-v0.2.0/README_DE.md)
- [Contract v0.2 – DRAFT](contract-v0.2.0/X6_PF_Experiment_Contract_v0_2_DRAFT.json)
- [JSON Schemas](contract-v0.2.0/schema/)
- [Python-Vorprüfer](contract-v0.2.0/preflight.py)
- [Tests](contract-v0.2.0/tests/test_preflight.py)
- [Lokaler Prüfbericht: 42 Softwaretests bestanden](contract-v0.2.0/validation_report.json)
- [Unverändert übernommener Inhalt des ursprünglichen v0.1-Entwurfs](contract-v0.2.0/original/X6_PF_Experiment_Contract_v0_1.json)

Die zwölf Dateien im Versionsordner wurden byteidentisch aus dem freigegebenen
Paket übernommen. Der Prüfbericht dokumentiert lokale Softwaretests, keine
unabhängige wissenschaftliche Begutachtung oder erfolgreiche Entrauschung.
Die vorhandenen Anwendungs- und Agentenquellen werden durch diese Veröffentlichung
nicht verändert.

Für Installation und Tests zuerst in `experiments/x6-phase-filter/contract-v0.2.0`
wechseln und der Anleitung folgen. Als technische Vorprüfung kann dieses Werkzeug
höchstens `READY_FOR_RUNNER_REVIEW` melden; es vergibt keinen wissenschaftlichen PASS.

Es gilt die [Apache-2.0-Lizenz des Projekts](../../LICENSE) im dokumentierten
[Lizenzumfang](../../LICENSE_SCOPE.md). Abhängigkeiten bleiben separat lizenziert
und sind nicht im Paket enthalten.
