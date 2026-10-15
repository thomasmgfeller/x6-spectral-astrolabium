# X6 — zentrales Modul- und Evidenzregister

**Geprüfter Quellenstand: 2026-10-15.** Dieses Register ist der gemeinsame Einstieg in die veröffentlichten Module.

Es beschreibt einen datierten Snapshot, keinen Live-Monitor. Massgeblicher main-Ausgangscommit: [dedddc11ed43b14bf872d56b02c92c5b65e695bb](https://github.com/thomasmgfeller/x6-spectral-astrolabium/commit/dedddc11ed43b14bf872d56b02c92c5b65e695bb). Dokumentationsänderungen nach diesem Snapshot sind über die Git-Historie nachvollziehbar. Die Quellpins bezeichnen die verfügbare Implementierung; ältere Evidenzberichte behalten ihre eigenen Prüfrevisionen.

[Maschinenlesbare Quelle](../MODULE_REGISTRY.json) · [Installation und Bedienung](INTEGRATION.md) · [Register-Abnahme](MODULE_REGISTRY_ACCEPTANCE.md) · [Offline-Referenzsuite](OFFLINE_REFERENCE.md)

## Schnellstart aus main

```sh
git clone --branch main https://github.com/thomasmgfeller/x6-spectral-astrolabium.git x6
cd x6
python3 x6.py setup --profile core
python3 x6.py doctor --profile core
python3 x6.py run spectral --output runs/first-spectral
python3 x6.py verify runs/first-spectral
python3 x6.py serve
```

Voraussetzungen: Git, Python 3.12, Node.js >=22; Referenzplattform Linux/POSIX x86-64. Browser für die gemeldete lokale URL. Der Spektrallauf prüft fünf rationale Referenzfälle; er qualifiziert keine Hardware. Für RAX folgt `python3 x6.py setup --profile research`. Server mit Strg+C beenden. Ausgabepfade müssen jeweils neu sein.

## Status richtig lesen

- **MAIN:** im veröffentlichten Hauptzweig verfügbar. **BRANCH_ONLY:** im main-Snapshot nicht enthalten; den unten gepinnten Stand separat auschecken.
- **SOFTWARE:** ausführbarer, begrenzter Prüfweg. **CONCEPT/DOSSIER:** kein eigenständiger ausführbarer Gesamtbaustein; Unterlagen und nächste Abnahme sind benannt.
- Ein erfolgreicher Lauf kann einen fachlichen FAIL, BLOCKED, NOT_READY oder INCONCLUSIVE korrekt reproduzieren. Erwartete Exitcodes stehen beim Modul.
- Gespeicherte interne Prüfungen sind keine externe Begutachtung. Simulation, exakte endliche Rechnung und physische Messung bleiben unterschiedliche Evidenzklassen. Kein Registereintrag behauptet hier eine abgeschlossene physische Gerätequalifikation.

## Agentenfenster

**Exklusives Ende: 19. Oktober 2026, 00:00:00 Europe/Zurich** (`2026-10-18T22:00:00Z`), also einschliesslich Sonntag, 18. Oktober. Vier Datenjobs in zwei Workflows plus ein Mathematikagent teilen dieses Ende. Die drei Workflows und die Mathematikkonfiguration werden auf Übereinstimmung geprüft.

NOAA-/Quellenjobs haben keine Push-/PR-Starts. Der Mathematikworkflow besitzt zusätzlich quellbezogene Push-/PR-Prüfungen, ebenfalls mit Zeitfensterprüfung. Zulassungsreserven: NOAA 15 Minuten, Quellen 25 Minuten, Mathematik 6 Minuten. Der konfigurierte Zeitraum beweist keine tatsächliche Ausführung; verzögerte/ausgelassene GitHub-Starts bleiben möglich. [Betriebsregeln und Reparaturbeleg](AGENT_WINDOW_REPAIR_2026_10_13.md).

| Am Snapshot beobachteter Workflow | Run / geprüfter Quellencommit | Aussage |
| --- | --- | --- |
| X6 Data Agent | [38694613614](https://github.com/thomasmgfeller/x6-spectral-astrolabium/actions/runs/38694613614), `90b74509f2b65de08a77de8a7057204834951fc2` | success: GitHub meldet Workflow-Erfolg; Rohartefakte in dieser Registerpflege nicht erneut ausgewertet. |
| X6 Source Agents | [38697674497](https://github.com/thomasmgfeller/x6-spectral-astrolabium/actions/runs/38697674497), `90b74509f2b65de08a77de8a7057204834951fc2` | success: GitHub meldet Workflow-Erfolg; Rohartefakte in dieser Registerpflege nicht erneut ausgewertet. |
| X6 Bounded Math Agent | [38697085735](https://github.com/thomasmgfeller/x6-spectral-astrolabium/actions/runs/38697085735), `90b74509f2b65de08a77de8a7057204834951fc2` | success: GitHub meldet Workflow-Erfolg; Rohartefakte in dieser Registerpflege nicht erneut ausgewertet. |

## Modulübersicht

| Modul | Verfügbarkeit / Art | Branch / Quellcommit |
| --- | --- | --- |
| [Gemeinsamer lokaler Einstieg](#integration) | MAIN / SOFTWARE | `main` / [dedddc11ed43](https://github.com/thomasmgfeller/x6-spectral-astrolabium/commit/dedddc11ed43b14bf872d56b02c92c5b65e695bb) |
| [Gemeinsame Offline-Referenzsuite](#offline-reference) | MAIN / SOFTWARE | `main` / [dedddc11ed43](https://github.com/thomasmgfeller/x6-spectral-astrolabium/commit/dedddc11ed43b14bf872d56b02c92c5b65e695bb) |
| [Astrolabium und rationale Spektralreferenz](#astrolabium) | MAIN / SOFTWARE | `main` / [dedddc11ed43](https://github.com/thomasmgfeller/x6-spectral-astrolabium/commit/dedddc11ed43b14bf872d56b02c92c5b65e695bb) |
| [Signal Validation Lab](#signal-lab) | MAIN / SOFTWARE | `main` / [dedddc11ed43](https://github.com/thomasmgfeller/x6-spectral-astrolabium/commit/dedddc11ed43b14bf872d56b02c92c5b65e695bb) |
| [Edge-Referenzadapter](#edge-reference) | MAIN / SOFTWARE | `main` / [dedddc11ed43](https://github.com/thomasmgfeller/x6-spectral-astrolabium/commit/dedddc11ed43b14bf872d56b02c92c5b65e695bb) |
| [Evidence & Calibration](#evidence-calibration) | MAIN / SOFTWARE | `main` / [dedddc11ed43](https://github.com/thomasmgfeller/x6-spectral-astrolabium/commit/dedddc11ed43b14bf872d56b02c92c5b65e695bb) |
| [X6-Phasenfilter: Experimentvertrag](#phase-contract) | MAIN / SOFTWARE | `main` / [dedddc11ed43](https://github.com/thomasmgfeller/x6-spectral-astrolabium/commit/dedddc11ed43b14bf872d56b02c92c5b65e695bb) |
| [Industrielle Entrauschung: Forschungsprogramm v0.2](#industrial-programme) | MAIN / CONCEPT | `main` / [dedddc11ed43](https://github.com/thomasmgfeller/x6-spectral-astrolabium/commit/dedddc11ed43b14bf872d56b02c92c5b65e695bb) |
| [Sagnac-Aufnahme und Import](#sagnac-import) | MAIN / SOFTWARE | `main` / [dedddc11ed43](https://github.com/thomasmgfeller/x6-spectral-astrolabium/commit/dedddc11ed43b14bf872d56b02c92c5b65e695bb) |
| [Photonischer Zwei-Qubit-Aufbau und Jig](#photonic-design) | MAIN / SOFTWARE | `main` / [dedddc11ed43](https://github.com/thomasmgfeller/x6-spectral-astrolabium/commit/dedddc11ed43b14bf872d56b02c92c5b65e695bb) |
| [ACVM: Grundkonzept 0.1](#acvm-concept) | MAIN / CONCEPT | `main` / [dedddc11ed43](https://github.com/thomasmgfeller/x6-spectral-astrolabium/commit/dedddc11ed43b14bf872d56b02c92c5b65e695bb) |
| [ACVM C1: Steuerkanal](#acvm-c1) | MAIN / SOFTWARE | `main` / [dedddc11ed43](https://github.com/thomasmgfeller/x6-spectral-astrolabium/commit/dedddc11ed43b14bf872d56b02c92c5b65e695bb) |
| [ACVM 0.2: optischer Referenzablauf](#acvm-optical) | MAIN / SOFTWARE | `main` / [dedddc11ed43](https://github.com/thomasmgfeller/x6-spectral-astrolabium/commit/dedddc11ed43b14bf872d56b02c92c5b65e695bb) |
| [Sagnac-Komponenten und Ofen](#sagnac-components) | MAIN / CONCEPT | `main` / [dedddc11ed43](https://github.com/thomasmgfeller/x6-spectral-astrolabium/commit/dedddc11ed43b14bf872d56b02c92c5b65e695bb) |
| [ACVM Experiment Records](#acvm-records) | MAIN / CONCEPT | `main` / [dedddc11ed43](https://github.com/thomasmgfeller/x6-spectral-astrolabium/commit/dedddc11ed43b14bf872d56b02c92c5b65e695bb) |
| [ACVM Electrical & Thermal Test Fixture](#acvm-fixture) | MAIN / CONCEPT | `main` / [dedddc11ed43](https://github.com/thomasmgfeller/x6-spectral-astrolabium/commit/dedddc11ed43b14bf872d56b02c92c5b65e695bb) |
| [RAX: relationales Forschungsprogramm](#rax-programme) | MAIN / CONCEPT | `main` / [dedddc11ed43](https://github.com/thomasmgfeller/x6-spectral-astrolabium/commit/dedddc11ed43b14bf872d56b02c92c5b65e695bb) |
| [RAX-U1: Reduktionskontrolle](#rax-u1) | MAIN / SOFTWARE | `main` / [dedddc11ed43](https://github.com/thomasmgfeller/x6-spectral-astrolabium/commit/dedddc11ed43b14bf872d56b02c92c5b65e695bb) |
| [RAX-B1/M1: Benchmark und Methodenreview](#rax-b1-m1) | MAIN / SOFTWARE | `main` / [dedddc11ed43](https://github.com/thomasmgfeller/x6-spectral-astrolabium/commit/dedddc11ed43b14bf872d56b02c92c5b65e695bb) |
| [RAX-W1: exakte Wolfram-Gegenprüfung](#rax-w1) | MAIN / SOFTWARE | `main` / [dedddc11ed43](https://github.com/thomasmgfeller/x6-spectral-astrolabium/commit/dedddc11ed43b14bf872d56b02c92c5b65e695bb) |
| [Wolfram Fall 2: Polaritätsumkehr](#wolfram-polarity) | MAIN / SOFTWARE | `main` / [dedddc11ed43](https://github.com/thomasmgfeller/x6-spectral-astrolabium/commit/dedddc11ed43b14bf872d56b02c92c5b65e695bb) |
| [Wolfram Fall 4: Nullfehler und Abhängigkeit](#wolfram-dependence) | MAIN / SOFTWARE | `main` / [dedddc11ed43](https://github.com/thomasmgfeller/x6-spectral-astrolabium/commit/dedddc11ed43b14bf872d56b02c92c5b65e695bb) |
| [Wolfram Fall 5: Kausalordnung](#wolfram-causal) | MAIN / SOFTWARE | `main` / [dedddc11ed43](https://github.com/thomasmgfeller/x6-spectral-astrolabium/commit/dedddc11ed43b14bf872d56b02c92c5b65e695bb) |
| [Öffentliche Datenagenten: NOAA, Atlas, QuTech, NASA](#data-agents) | MAIN / SOFTWARE | `main` / [dedddc11ed43](https://github.com/thomasmgfeller/x6-spectral-astrolabium/commit/dedddc11ed43b14bf872d56b02c92c5b65e695bb) |
| [Begrenzter Mathematikagent: Lorentz n=3–5 und Propagator](#lorentz-agent) | MAIN / SOFTWARE | `main` / [dedddc11ed43](https://github.com/thomasmgfeller/x6-spectral-astrolabium/commit/dedddc11ed43b14bf872d56b02c92c5b65e695bb) |
| [Lorentz-Kollisionsatlas n=6: vollständiger Forschungsstand](#lorentz-n6) | BRANCH_ONLY / SOFTWARE | `research/lorentz-v1-workpackages` / [f5116b9970a6](https://github.com/thomasmgfeller/x6-spectral-astrolabium/commit/f5116b9970a6b7dc788c18623a8386b4cde33ad4) |
| [Industrielle Entrauschung: V1-Bewertungsadapter](#industrial-v1) | BRANCH_ONLY / SOFTWARE | `research/lorentz-v1-workpackages` / [f5116b9970a6](https://github.com/thomasmgfeller/x6-spectral-astrolabium/commit/f5116b9970a6b7dc788c18623a8386b4cde33ad4) |
| [Mehrschichtiger Fingerprint](#fingerprint) | BRANCH_ONLY / SOFTWARE | `research/x6-fingerprint-v1` / [f22030f2dae0](https://github.com/thomasmgfeller/x6-spectral-astrolabium/commit/f22030f2dae0aa670cdbc450c5e881ce250b36b8) |
| [Experiment Fabric](#experiment-fabric) | BRANCH_ONLY / SOFTWARE | `research/x6-experiment-fabric-v1` / [a34c59f2b0e2](https://github.com/thomasmgfeller/x6-spectral-astrolabium/commit/a34c59f2b0e2d30c73936363040669941aa8ce09) |
| [Neutral Discovery](#neutral-discovery) | BRANCH_ONLY / SOFTWARE | `research/x6-neutral-discovery-v1` / [1a02c482d59a](https://github.com/thomasmgfeller/x6-spectral-astrolabium/commit/1a02c482d59a42d554337fb83e0f6d6e6d84b516) |
| [NQK: Forschungsdossier](#nqk) | BRANCH_ONLY / DOSSIER | `research/nqk` / [a8fbc70fae3e](https://github.com/thomasmgfeller/x6-spectral-astrolabium/commit/a8fbc70fae3ecb46bfcd8ceb828ce182e533dd04) |
| [Photonic Link Validation Lab](#photonic-link) | BRANCH_ONLY / SOFTWARE | `research/photonic-link` / [7ff72fcd6a16](https://github.com/thomasmgfeller/x6-spectral-astrolabium/commit/7ff72fcd6a16e9b353d1af277307463f757d3470) |

## Einzelne Module ausführen

Alle Befehle beziehen sich auf den Quellencommit des jeweiligen Moduls. Für einen exakt gepinnten main-Lauf nach dem Klonen `git checkout --detach dedddc11ed43b14bf872d56b02c92c5b65e695bb` verwenden. Für Branch-Module folgt jeweils ein eigenes Klonrezept; danach ist der Checkout absichtlich detached. Nicht wahllos zwischen divergierenden Branches wechseln oder deren Versionsinventare mischen.

Archivmodule werden in neue Ordner unter /tmp entpackt. Eine erneute Ausführung benötigt einen neuen Zielnamen. Paketinterne Befehle starten aus dem angegebenen Wurzelordner. Installation externer Abhängigkeiten benötigt Netzwerk oder vorbereitete Wheels; der eigentliche Offline-Replay startet keinen Wolfram-Dienst.

<a id="integration"></a>
### Gemeinsamer lokaler Einstieg

**Stand:** MAIN / SOFTWARE; Branch `main`; Commit `dedddc11ed43b14bf872d56b02c92c5b65e695bb`.

**Anleitung:** [aktuelle main-Dokumentation](https://github.com/thomasmgfeller/x6-spectral-astrolabium/blob/main/docs/INTEGRATION.md). **Voraussetzungen:** Linux/POSIX x86-64, Python 3.12, Git, Node >=22; setup installiert gepinntes NumPy/SciPy. Browser für die Oberfläche.

**Geprüfte Aussage:** Installation, Signal/Spektral/RAX-Läufe sowie Export und Replay sind in main integriert. ACVM/C1 besitzen zusätzliche Unterbefehle.

```sh
python3 x6.py setup --profile research
python3 x6.py doctor --profile research
python3 x6.py serve
```

**Erwartung:** doctor: erfolgreich; serve meldet Loopback-URL und bleibt bis Strg+C aktiv.

**Vorhandene Evidenz:**

- [docs/integration-v0.1/evidence/qualification.json](https://github.com/thomasmgfeller/x6-spectral-astrolabium/blob/dedddc11ed43b14bf872d56b02c92c5b65e695bb/docs/integration-v0.1/evidence/qualification.json): Historische Abnahme PASS_WITH_BROWSER, 23 Schritte; genaue damalige Revision im Bericht. Kein Nachweis für beliebige spätere Commits.

**Nächste Abnahme:** Frischer Checkout der nächsten Implementierungsrevision: Installation, alle drei Adapter, ZIP-Replay, Negativkontrollen und Browser/CLI-Austausch bestehen.

<a id="offline-reference"></a>
### Gemeinsame Offline-Referenzsuite

**Stand:** MAIN / SOFTWARE; Branch `main`; Commit `dedddc11ed43b14bf872d56b02c92c5b65e695bb`.

**Anleitung:** [aktuelle main-Dokumentation](https://github.com/thomasmgfeller/x6-spectral-astrolabium/blob/main/docs/OFFLINE_REFERENCE.md). **Voraussetzungen:** Linux/POSIX x86-64, Python 3.12 und Node.js 24. Nur Standardbibliothek; kein setup, NumPy/SciPy, Netzwerk oder Wolfram-Zugang. Neuer Ausgabeordner.

**Geprüfte Aussage:** Vier unveränderte Wolfram-Archive, fünf rationale Graphfälle, 318 n=6-Ordnungen mit 4.208 exakten Polynomen und aktueller Signal-Lab-Kern gegen die gespeicherte Polaritätsreferenz. Vollständiges quellengebundenes Replay. Frische CI-Checkouts laufen bei relevanten Änderungen mit abgeschaltetem Netzwerk. Endliche Software-/Referenzrechnung, keine physische Abnahme oder externe Begutachtung.

```sh
python3 -S -B x6.py reference qualify --output /tmp/x6-reference-evidence
python3 -S -B x6.py reference verify /tmp/x6-reference-evidence
```

**Erwartung:** Exit 0; PASS_OFFLINE_REFERENCE_REPLAY, 8 Berichte, 26 zurückgewiesene Fehlerkontrollen. Manipulierte/unvollständige Ausgaben: Exit 1 und FAIL, auch nach neu berechneten Prüfsummen.

**Vorhandene Evidenz:**

- [docs/reference-suite/README.md](https://github.com/thomasmgfeller/x6-spectral-astrolabium/blob/dedddc11ed43b14bf872d56b02c92c5b65e695bb/docs/reference-suite/README.md): Ausgeführte Abnahme der Implementierung 7c35b591f77ab1c123ee9795ea6978d1681d59bb. Lokale und Netzwerk-isolierte CI-Abnahme PASS, identische Bundle-Prüfsumme.
- [docs/reference-suite/local/acceptance.json](https://github.com/thomasmgfeller/x6-spectral-astrolabium/blob/dedddc11ed43b14bf872d56b02c92c5b65e695bb/docs/reference-suite/local/acceptance.json): Frischer sauberer Checkout ohne .venv/Site-Pakete; elf CLI-Schritte einschließlich zehn erwarteter Zurückweisungen. Historische Prüfrevision explizit gespeichert.
- [docs/reference-suite/local/run/complete.json](https://github.com/thomasmgfeller/x6-spectral-astrolabium/blob/dedddc11ed43b14bf872d56b02c92c5b65e695bb/docs/reference-suite/local/run/complete.json): Vollständiges Bundle mit acht Berichten, Quellenhashes und Inventar; durch reference verify erneut berechenbar.
- [docs/reference-suite/ci/acceptance.json](https://github.com/thomasmgfeller/x6-spectral-astrolabium/blob/dedddc11ed43b14bf872d56b02c92c5b65e695bb/docs/reference-suite/ci/acceptance.json): GitHub-Lauf 38720405798: network_namespace_isolated=true, alle elf CLI-Schritte wie erwartet.

**Nächste Abnahme:** Bei jeder relevanten Änderung frischen Checkout mit unverändertem Prüfvertrag qualifizieren und neue Evidenzrevision festhalten. Neue Fälle oder größere Korpora benötigen eigene Erwartungen und Fehlerkontrollen; andere Plattformen sind separat zu qualifizieren.

<a id="astrolabium"></a>
### Astrolabium und rationale Spektralreferenz

**Stand:** MAIN / SOFTWARE; Branch `main`; Commit `dedddc11ed43b14bf872d56b02c92c5b65e695bb`.

**Anleitung:** [aktuelle main-Dokumentation](https://github.com/thomasmgfeller/x6-spectral-astrolabium/blob/main/docs/SCIENTIFIC_SCOPE.md). **Voraussetzungen:** Python 3.12; gemeinsames setup --profile core. Browser-App: app/index.html.

**Geprüfte Aussage:** Fünf rationale Referenzfälle prüfen strikte Untergrenzen für endliche gerundete Graph-Laplacians, einschliesslich ungültiger Schranken und getrennter Komponenten.

```sh
python3 x6.py run spectral --output runs/register-spectral
python3 x6.py verify runs/register-spectral
```

**Erwartung:** Exit 0; nur die unten genannte Softwareaussage.

**Vorhandene Evidenz:**

- [docs/integration-v0.1/evidence/spectral-run.log](https://github.com/thomasmgfeller/x6-spectral-astrolabium/blob/dedddc11ed43b14bf872d56b02c92c5b65e695bb/docs/integration-v0.1/evidence/spectral-run.log): Erhaltene Referenzausführung; keine physische oder allgemeine Raumzeitaussage.
- [evidence/historical_python_results.json](https://github.com/thomasmgfeller/x6-spectral-astrolabium/blob/dedddc11ed43b14bf872d56b02c92c5b65e695bb/evidence/historical_python_results.json): Historischer Python-Befund; datierter Prüfstand.

**Nächste Abnahme:** Externe Reproduktion der exakten Zertifikate und separat vollständige Browser-/Julia-Qualifikation.

<a id="signal-lab"></a>
### Signal Validation Lab

**Stand:** MAIN / SOFTWARE; Branch `main`; Commit `dedddc11ed43b14bf872d56b02c92c5b65e695bb`.

**Anleitung:** [aktuelle main-Dokumentation](https://github.com/thomasmgfeller/x6-spectral-astrolabium/blob/main/docs/SIGNAL_VALIDATION_LAB.md). **Voraussetzungen:** Python 3.12, Node >=22; setup --profile core. UI: app/signal-lab.html.

**Geprüfte Aussage:** Synthetische Signale werden gegen vier Verfahren verglichen; Roharrays und Qualitätsurteile bleiben im Replay erhalten.

```sh
python3 x6.py run signal --output runs/register-signal
python3 x6.py verify runs/register-signal
```

**Erwartung:** Exit 0; nur die unten genannte Softwareaussage.

**Vorhandene Evidenz:**

- [docs/integration-v0.1/evidence/signal-run.log](https://github.com/thomasmgfeller/x6-spectral-astrolabium/blob/dedddc11ed43b14bf872d56b02c92c5b65e695bb/docs/integration-v0.1/evidence/signal-run.log): Erhaltenes Pulsbeispiel: X6-Phasenfilter FAIL ist ein fachliches Ergebnis, kein Laufabbruch.
- [docs/perspectives/edge-platform/evidence/independent-reference.json](https://github.com/thomasmgfeller/x6-spectral-astrolabium/blob/dedddc11ed43b14bf872d56b02c92c5b65e695bb/docs/perspectives/edge-platform/evidence/independent-reference.json): Gespeicherte NumPy/SciPy-Gegenprüfung.

**Nächste Abnahme:** Vor Leistungsclaims: starke Baselines, getrennte reale Testdaten, ereigniserhaltende Qualitätsgates und Ressourcenmessung.

<a id="edge-reference"></a>
### Edge-Referenzadapter

**Stand:** MAIN / SOFTWARE; Branch `main`; Commit `dedddc11ed43b14bf872d56b02c92c5b65e695bb`.

**Anleitung:** [aktuelle main-Dokumentation](https://github.com/thomasmgfeller/x6-spectral-astrolabium/blob/main/experimental/edge_reference/README.md). **Voraussetzungen:** Node >=22; keine npm-Laufzeitabhängigkeiten.

**Geprüfte Aussage:** Begrenzter lokaler Signalauftrag mit Export und rechnerischem Replay; main enthält den Adapter bereits.

```sh
node experimental/edge_reference/runner.cjs run experimental/edge_reference/examples/synthetic-signal.json runs/register-edge
node experimental/edge_reference/runner.cjs verify runs/register-edge
```

**Erwartung:** Exit 0; nur die unten genannte Softwareaussage.

**Vorhandene Evidenz:**

- [docs/perspectives/edge-platform/evidence/local-validation.json](https://github.com/thomasmgfeller/x6-spectral-astrolabium/blob/dedddc11ed43b14bf872d56b02c92c5b65e695bb/docs/perspectives/edge-platform/evidence/local-validation.json): Lokale Softwareprüfung; keine Messung von Geräteeffizienz.

**Nächste Abnahme:** Zweite unabhängige Anwendung, qualifizierter Geräteadapter und ARM64/x86-64-Vergleich nach Roadmap.

<a id="evidence-calibration"></a>
### Evidence & Calibration

**Stand:** MAIN / SOFTWARE; Branch `main`; Commit `dedddc11ed43b14bf872d56b02c92c5b65e695bb`.

**Anleitung:** [aktuelle main-Dokumentation](https://github.com/thomasmgfeller/x6-spectral-astrolabium/blob/main/experimental/evidence_calibration/README.md). **Voraussetzungen:** Python 3.12/3.13, Standardbibliothek.

**Geprüfte Aussage:** Datentypen, Evidenzbindung, Bildmetadaten und klassische Referenzmodelle werden softwareseitig geprüft; Hashes authentifizieren keine Messung.

```sh
python3 -m experimental.evidence_calibration.run_qualification --output runs/register-calibration --protect-research
```

**Erwartung:** Exit 0; nur die unten genannte Softwareaussage.

**Vorhandene Evidenz:**

- [experimental/evidence_calibration/REMEDIATION.md](https://github.com/thomasmgfeller/x6-spectral-astrolabium/blob/dedddc11ed43b14bf872d56b02c92c5b65e695bb/experimental/evidence_calibration/REMEDIATION.md): Audit-/Fehlerbehandlung und Testzuordnung. Ein erneuter Lauf erzeugt eigene Logs; kein gespeicherter physischer Qualifikationsbefund.

**Nächste Abnahme:** Kontrollierte aufgezeichnete Messdaten, Dunkel-/Sättigungsprüfung, kalibrierter Massstab und vollständiges Unsicherheitsbudget.

<a id="phase-contract"></a>
### X6-Phasenfilter: Experimentvertrag

**Stand:** MAIN / SOFTWARE; Branch `main`; Commit `dedddc11ed43b14bf872d56b02c92c5b65e695bb`.

**Anleitung:** [aktuelle main-Dokumentation](https://github.com/thomasmgfeller/x6-spectral-astrolabium/blob/main/experiments/x6-phase-filter/README.md). **Voraussetzungen:** Python 3.12, isolierte venv empfohlen; Abhängigkeiten aus Paket requirements.txt.

**Geprüfte Aussage:** Die Vorprüfung trennt einen strukturell gültigen Entwurf von einem ausführungsreifen Versuch; Filterclaim UNVALIDATED.

```sh
cd experiments/x6-phase-filter/contract-v0.2.0
python3 -m pip install -r requirements.txt
python3 preflight.py X6_PF_Experiment_Contract_v0_2_DRAFT.json --mode draft
python3 preflight.py X6_PF_Experiment_Contract_v0_2_DRAFT.json --mode preflight
```

**Erwartung:** draft: DRAFT_STRUCTURE_VALID/Exit 0; preflight: BLOCKED/Exit 2 ist hier erwartet.

**Vorhandene Evidenz:**

- [experiments/x6-phase-filter/contract-v0.2.0/validation_report.json](https://github.com/thomasmgfeller/x6-spectral-astrolabium/blob/dedddc11ed43b14bf872d56b02c92c5b65e695bb/experiments/x6-phase-filter/contract-v0.2.0/validation_report.json): 42 Softwaretests; keine neuen Filterversuche.

**Nächste Abnahme:** Offene fachliche Festlegungen und vertrauenswürdigen Freeze schliessen; danach Runner-Review.

<a id="industrial-programme"></a>
### Industrielle Entrauschung: Forschungsprogramm v0.2

**Stand:** MAIN / CONCEPT; Branch `main`; Commit `dedddc11ed43b14bf872d56b02c92c5b65e695bb`.

**Anleitung:** [aktuelle main-Dokumentation](https://github.com/thomasmgfeller/x6-spectral-astrolabium/blob/main/docs/industrial-denoising/Astrolabium_Industrial_Denoising_Forschungsprogramm_v0_2.docx). **Voraussetzungen:** DOCX-Leser. Ausführbarer V1-Vertrag: separater Eintrag industrial-v1.

**Geprüfte Aussage:** Forschungsplan für Diagnosequalität, Ereigniserhalt und Ressourcenbudgets; keine nachgewiesene neue Filterleistung.

**Erwartung:** Kein ausführbarer Kern in diesem Dokument.

**Vorhandene Evidenz:**

- [docs/industrial-denoising/Astrolabium_Industrial_Denoising_Forschungsprogramm_v0_2.docx](https://github.com/thomasmgfeller/x6-spectral-astrolabium/blob/dedddc11ed43b14bf872d56b02c92c5b65e695bb/docs/industrial-denoising/Astrolabium_Industrial_Denoising_Forschungsprogramm_v0_2.docx): Veröffentlichter Forschungsplan; kein abgeschlossener Industrieversuch.

**Nächste Abnahme:** AP1: konkrete Maschine/Sensorik, Rechte, Referenzen, unabhängige Splits, Powerplanung und Protokollreview.

<a id="sagnac-import"></a>
### Sagnac-Aufnahme und Import

**Stand:** MAIN / SOFTWARE; Branch `main`; Commit `dedddc11ed43b14bf872d56b02c92c5b65e695bb`.

**Anleitung:** [aktuelle main-Dokumentation](https://github.com/thomasmgfeller/x6-spectral-astrolabium/blob/main/docs/SAGNAC_INTEGRATION.md). **Voraussetzungen:** Python 3.12, Browser; Standardstart ohne angeschlossenes Gerät.

**Geprüfte Aussage:** SGNCv007-Decoder, synthetischer Import und Loopback-Bridge; optische Stellbefehle gehören zum separaten ACVM-Modul.

```sh
python3 device/sagnac_bridge.py
```

**Erwartung:** http://127.0.0.1:8766/app/; Tab 07 Sagnac, synthetisches Beispiel. Server endet mit Strg+C.

**Vorhandene Evidenz:**

- [evidence/sagnac_integration_validation.json](https://github.com/thomasmgfeller/x6-spectral-astrolabium/blob/dedddc11ed43b14bf872d56b02c92c5b65e695bb/evidence/sagnac_integration_validation.json): Gespeicherte Softwarevalidierung des Integrationsstands; keine Hardwaremessung.

**Nächste Abnahme:** Reale serielle Aufnahme und Zähler-/Zeitkalibrierung mit unabhängiger Referenz; optische Claims separat prüfen.

<a id="photonic-design"></a>
### Photonischer Zwei-Qubit-Aufbau und Jig

**Stand:** MAIN / SOFTWARE; Branch `main`; Commit `dedddc11ed43b14bf872d56b02c92c5b65e695bb`.

**Anleitung:** [aktuelle main-Dokumentation](https://github.com/thomasmgfeller/x6-spectral-astrolabium/blob/main/experiments/photonic-two-qubit/REPRODUCE.md). **Voraussetzungen:** Python 3.12, GHDL 5.0.1 mcode und CAD-Abhängigkeiten aus requirements; keine Hardware nötig.

**Geprüfte Aussage:** Host-/RTL-Referenz und idealisierte Jig-Geometrie werden geprüft. Ausgelassene optionale Prüfungen sind NOT_EXECUTED.

```sh
python3 -m pip install -r tests/photonics/requirements.txt
python3 tests/photonics/validate_release.py --ghdl --cad --output runs/register-photonic
```

**Erwartung:** Exit 0; nur die unten genannte Softwareaussage.

**Vorhandene Evidenz:**

- [experiments/photonic-two-qubit/SCIENTIFIC_STATUS.md](https://github.com/thomasmgfeller/x6-spectral-astrolabium/blob/dedddc11ed43b14bf872d56b02c92c5b65e695bb/experiments/photonic-two-qubit/SCIENTIFIC_STATUS.md): Designstatus und Grenzen; physische Fertigungs-/Verschränkungsnachweise offen.
- [experiments/photonic-two-qubit/reference/sagnac_v0_7/VALIDATION.md](https://github.com/thomasmgfeller/x6-spectral-astrolabium/blob/dedddc11ed43b14bf872d56b02c92c5b65e695bb/experiments/photonic-two-qubit/reference/sagnac_v0_7/VALIDATION.md): Erhaltener digitaler Referenzbericht.

**Nächste Abnahme:** Jig fertigen und vermessen; Quelle/Detektoren kalibrieren; vorregistrierte Koinzidenz-/Verschränkungsprüfung nach LAB_PROTOCOL.

<a id="acvm-concept"></a>
### ACVM: Grundkonzept 0.1

**Stand:** MAIN / CONCEPT; Branch `main`; Commit `dedddc11ed43b14bf872d56b02c92c5b65e695bb`.

**Anleitung:** [aktuelle main-Dokumentation](https://github.com/thomasmgfeller/x6-spectral-astrolabium/blob/main/docs/acvm/README.md). **Voraussetzungen:** Markdown-/DOCX-Leser; ausführbare C1-/0.2-Module siehe eigene Einträge.

**Geprüfte Aussage:** Historische Gesamtspezifikation. Teilimplementierungen in main ersetzen keine vollständige Geräteabnahme.

**Erwartung:** Dokument lesen; keine eigenständige ausführbare Gesamtspezifikation.

**Vorhandene Evidenz:**

- [docs/acvm/ACVM_CONCEPT_v0_1_DE.md](https://github.com/thomasmgfeller/x6-spectral-astrolabium/blob/dedddc11ed43b14bf872d56b02c92c5b65e695bb/docs/acvm/ACVM_CONCEPT_v0_1_DE.md): Ursprünglicher Anforderungstext; spätere Softwarebelege in C1 und optical-v0.2.

**Nächste Abnahme:** Anforderungen mit den Teilimplementierungen verknüpfen und verbleibende elektrische/optische Abnahmen durchführen.

<a id="acvm-c1"></a>
### ACVM C1: Steuerkanal

**Stand:** MAIN / SOFTWARE; Branch `main`; Commit `dedddc11ed43b14bf872d56b02c92c5b65e695bb`.

**Anleitung:** [aktuelle main-Dokumentation](https://github.com/thomasmgfeller/x6-spectral-astrolabium/blob/main/docs/acvm/control-channel-v0.1/README.md). **Voraussetzungen:** Python 3.12, POSIX-PTY, g++/C++17; kein Pico erforderlich.

**Geprüfte Aussage:** Host-Protokoll, Compiler, portabler C++-Sequencer und virtueller serieller Weg sind prüfbar.

```sh
python3 x6.py control qualify --output runs/register-c1
```

**Erwartung:** Exit 0; nur die unten genannte Softwareaussage.

**Vorhandene Evidenz:**

- [docs/acvm/control-channel-v0.1/evidence/qualification.json](https://github.com/thomasmgfeller/x6-spectral-astrolabium/blob/dedddc11ed43b14bf872d56b02c92c5b65e695bb/docs/acvm/control-channel-v0.1/evidence/qualification.json): Gespeicherte Softwarequalifikation; kein Pico-Build oder elektrischer Messbeleg.

**Nächste Abnahme:** Pico-Ziel bauen; DAC-Ausgabe, Timing, Fehlerzustände und unabhängige elektrische Messung qualifizieren.

<a id="acvm-optical"></a>
### ACVM 0.2: optischer Referenzablauf

**Stand:** MAIN / SOFTWARE; Branch `main`; Commit `dedddc11ed43b14bf872d56b02c92c5b65e695bb`.

**Anleitung:** [aktuelle main-Dokumentation](https://github.com/thomasmgfeller/x6-spectral-astrolabium/blob/main/docs/acvm/optical-v0.2/README.md). **Voraussetzungen:** Python 3.12, POSIX-PTY, g++; Softwarelauf ohne Geräte.

**Geprüfte Aussage:** V01–V08 MODEL_PASS, synthetische QHQ-/Drift-/Regelkontrollen; ELL14-/PM100D-Adapter sind implementiert, nicht gerätequalifiziert.

```sh
python3 x6.py acvm qualify --output runs/register-acvm
```

**Erwartung:** Exit 0; nur die unten genannte Softwareaussage.

**Vorhandene Evidenz:**

- [docs/acvm/optical-v0.2/evidence/fresh-checkout/fresh-checkout.json](https://github.com/thomasmgfeller/x6-spectral-astrolabium/blob/dedddc11ed43b14bf872d56b02c92c5b65e695bb/docs/acvm/optical-v0.2/evidence/fresh-checkout/fresh-checkout.json): 12 Checkout-Schritte; genaue geprüfte lokale Revision und Logs.
- [docs/acvm/optical-v0.2/VALIDATION.md](https://github.com/thomasmgfeller/x6-spectral-astrolabium/blob/dedddc11ed43b14bf872d56b02c92c5b65e695bb/docs/acvm/optical-v0.2/VALIDATION.md): V09/V10 physisch NOT_PERFORMED; Regelvorteil nur im angegebenen Modell.

**Nächste Abnahme:** V09/V10 mit unabhängigen Messungen; Geräteidentität/Kalibrierung, reale Hysterese/Laufzeiten und geschlossenen optischen Regelkreis nachweisen.

<a id="sagnac-components"></a>
### Sagnac-Komponenten und Ofen

**Stand:** MAIN / CONCEPT; Branch `main`; Commit `dedddc11ed43b14bf872d56b02c92c5b65e695bb`.

**Anleitung:** [aktuelle main-Dokumentation](https://github.com/thomasmgfeller/x6-spectral-astrolabium/blob/main/docs/acvm/sagnac-components-v0.1/README.md). **Voraussetzungen:** Dokument-/PDF-Leser.

**Geprüfte Aussage:** Beschaffungs- und Aufbauprofil für ppKTP, gemeinsamen Dreiecksloop und Temperaturführung.

**Erwartung:** Kein ausführbarer oder gemessener Aufbau.

**Vorhandene Evidenz:**

- [docs/acvm/sagnac-components-v0.1/README.md](https://github.com/thomasmgfeller/x6-spectral-astrolabium/blob/dedddc11ed43b14bf872d56b02c92c5b65e695bb/docs/acvm/sagnac-components-v0.1/README.md): Zwölf Abnahmeschritte ungetestet; keine Lieferantenbestätigung.

**Nächste Abnahme:** Lieferantenspezifikation und Fertigungsfreigabe einholen; zwölf Komponenten-/Aufbauprüfungen tatsächlich ausführen.

<a id="acvm-records"></a>
### ACVM Experiment Records

**Stand:** MAIN / CONCEPT; Branch `main`; Commit `dedddc11ed43b14bf872d56b02c92c5b65e695bb`.

**Anleitung:** [aktuelle main-Dokumentation](https://github.com/thomasmgfeller/x6-spectral-astrolabium/blob/main/docs/acvm/experiment-records/README.md). **Voraussetzungen:** Markdown-/DOCX-Leser.

**Geprüfte Aussage:** Vorgeschlagenes Run-Archive-Datenmodell mit Provenienz und Abnahmeplan; nicht gleich dem bereits begrenzten CLI-Export.

**Erwartung:** Kein eigenständiger Records-Runner.

**Vorhandene Evidenz:**

- [docs/acvm/experiment-records/README.md](https://github.com/thomasmgfeller/x6-spectral-astrolabium/blob/dedddc11ed43b14bf872d56b02c92c5b65e695bb/docs/acvm/experiment-records/README.md): Vierzehn Records-Prüfungen NOT_RUN.

**Nächste Abnahme:** Versionierten Writer/Reader und Adapter implementieren; alle vierzehn Records-Gates mit Manipulations-/Abbruchfällen prüfen.

<a id="acvm-fixture"></a>
### ACVM Electrical & Thermal Test Fixture

**Stand:** MAIN / CONCEPT; Branch `main`; Commit `dedddc11ed43b14bf872d56b02c92c5b65e695bb`.

**Anleitung:** [aktuelle main-Dokumentation](https://github.com/thomasmgfeller/x6-spectral-astrolabium/blob/main/docs/acvm/electrical-thermal-fixture/README.md). **Voraussetzungen:** Dokument-/Bildbetrachter.

**Geprüfte Aussage:** Elektrischer/thermischer Prüfstand und QD-01 sind Konzeptdarstellungen; Illustrationen sind keine gefertigten Chips.

**Erwartung:** Kein qualifizierter Prüfstand und kein ausführbarer Chip.

**Vorhandene Evidenz:**

- [docs/acvm/electrical-thermal-fixture/README.md](https://github.com/thomasmgfeller/x6-spectral-astrolabium/blob/dedddc11ed43b14bf872d56b02c92c5b65e695bb/docs/acvm/electrical-thermal-fixture/README.md): ETF-T01–ETF-T14 NOT_RUN.

**Nächste Abnahme:** Anforderungen, Bauteile und Messunsicherheit freigeben; Prüfstand aufbauen und ETF-T01–T14 messen.

<a id="rax-programme"></a>
### RAX: relationales Forschungsprogramm

**Stand:** MAIN / CONCEPT; Branch `main`; Commit `dedddc11ed43b14bf872d56b02c92c5b65e695bb`.

**Anleitung:** [aktuelle main-Dokumentation](https://github.com/thomasmgfeller/x6-spectral-astrolabium/blob/main/docs/research/rax/README.md). **Voraussetzungen:** DOCX-/Markdown-Leser; ausführbare U1/B1/M1/W1-Pakete separat.

**Geprüfte Aussage:** Gestuftes Programm für prädiktive Reduktionen; U2, Geometrie und Singularitäten bleiben geplant.

**Erwartung:** Kein universeller RAX-Entdeckungsrunner.

**Vorhandene Evidenz:**

- [docs/research/rax/README.md](https://github.com/thomasmgfeller/x6-spectral-astrolabium/blob/dedddc11ed43b14bf872d56b02c92c5b65e695bb/docs/research/rax/README.md): Programmbeschreibung und Links zu begrenzten ausgeführten Kontrollen.

**Nächste Abnahme:** U2 mit heterogenen Generatoren, festem Beobachtungsziel, Holdout und eigenem Fehlerbudget vorregistrieren.

<a id="rax-u1"></a>
### RAX-U1: Reduktionskontrolle

**Stand:** MAIN / SOFTWARE; Branch `main`; Commit `dedddc11ed43b14bf872d56b02c92c5b65e695bb`.

**Anleitung:** [aktuelle main-Dokumentation](https://github.com/thomasmgfeller/x6-spectral-astrolabium/blob/main/docs/research/rax/countercheck-v0.1/README.md). **Voraussetzungen:** Linux, Python 3.12, NumPy/SciPy aus enthaltenen requirements.

**Geprüfte Aussage:** 160 Matrizen/3,2 Mio. Übergänge; Entscheidungen 8 gestützt, 16 verworfen, 16 unentschieden. Archivvorfall bleibt offen.

```sh
python3 -m zipfile -e docs/research/rax/countercheck-v0.1/RAX_U1_Gegenpruefung_v0_1_Paket.zip /tmp/x6-register-rax-u1
cd /tmp/x6-register-rax-u1/RAX_U1_Gegenpruefung_v0_1
python3 -m pip install -r research/rax_u1_countercheck/requirements.txt
python3 research/rax_u1_countercheck/audit.py --output audit-reproduced.json
python3 research/rax_u1/reference.py research/rax_u1/evidence/qualification
```

**Erwartung:** Exit 0; nur die unten genannte Softwareaussage.

**Vorhandene Evidenz:**

- [docs/research/rax/countercheck-v0.1/RAX_U1_Gegenpruefung_v0_1_Paket.zip](https://github.com/thomasmgfeller/x6-spectral-astrolabium/blob/dedddc11ed43b14bf872d56b02c92c5b65e695bb/docs/research/rax/countercheck-v0.1/RAX_U1_Gegenpruefung_v0_1_Paket.zip): Originalquellen, Rohdaten, audit-final und Gegenproben im Paket.

**Nächste Abnahme:** Dauerhafte Speicherung mit Flush/fsync, Reopen/Hashprüfung sowie Abbruch-/Kürzungs-/Neustarttests qualifizieren.

<a id="rax-b1-m1"></a>
### RAX-B1/M1: Benchmark und Methodenreview

**Stand:** MAIN / SOFTWARE; Branch `main`; Commit `dedddc11ed43b14bf872d56b02c92c5b65e695bb`.

**Anleitung:** [aktuelle main-Dokumentation](https://github.com/thomasmgfeller/x6-spectral-astrolabium/blob/main/docs/research/rax/method-review-v0.1/README.md). **Voraussetzungen:** setup --profile research; Python 3.12, NumPy/SciPy. Der Replay kann mehrere Minuten dauern.

**Geprüfte Aussage:** 67.584 Benchmarkläufe und Methoden-Gegenbeispiele werden nachgerechnet. Alle acht primären Überlegenheitsentscheidungen bleiben INCONCLUSIVE.

```sh
python3 x6.py run rax --output runs/register-rax
python3 x6.py verify runs/register-rax
```

**Erwartung:** Exit 0; nur die unten genannte Softwareaussage.

**Vorhandene Evidenz:**

- [docs/research/rax/benchmark-v0.1/RAX_B1_Benchmarking_v0_1_Paket.zip](https://github.com/thomasmgfeller/x6-spectral-astrolabium/blob/dedddc11ed43b14bf872d56b02c92c5b65e695bb/docs/research/rax/benchmark-v0.1/RAX_B1_Benchmarking_v0_1_Paket.zip): Eingefrorene B1-Daten und Referenzprüfer.
- [docs/research/rax/method-review-v0.1/RAX_M1_Methodenpruefung_v0_1_Paket.zip](https://github.com/thomasmgfeller/x6-spectral-astrolabium/blob/dedddc11ed43b14bf872d56b02c92c5b65e695bb/docs/research/rax/method-review-v0.1/RAX_M1_Methodenpruefung_v0_1_Paket.zip): Zwei nachgewiesene Validierungsfehler und Zusatzguards; ursprüngliche Daten bestehen Nachprüfung.

**Nächste Abnahme:** Validierungsfehler in neuer versionierter Runner-Fassung beheben; echten Holdout-Zugriffsschutz und Freeze-Grenzen prüfen, externe Replikation.

<a id="rax-w1"></a>
### RAX-W1: exakte Wolfram-Gegenprüfung

**Stand:** MAIN / SOFTWARE; Branch `main`; Commit `dedddc11ed43b14bf872d56b02c92c5b65e695bb`.

**Anleitung:** [aktuelle main-Dokumentation](https://github.com/thomasmgfeller/x6-spectral-astrolabium/blob/main/docs/research/rax/wolfram-check-v0.1/README.md). **Voraussetzungen:** Python 3.12/Standardbibliothek. Offline-Prüfung startet keinen Wolfram-Kernel.

**Geprüfte Aussage:** 44 ausgewählte U1-Matrizen, zehn gültige Reduktionen und 34 beabsichtigte Verletzungen werden exakt abgeglichen.

```sh
python3 -m zipfile -e docs/research/rax/wolfram-check-v0.1/RAX_W1_Exakte_Gegenpruefung_v0_1_Paket.zip /tmp/x6-register-rax-w1
cd /tmp/x6-register-rax-w1/RAX_W1_Exakte_Gegenpruefung_v0_1
python3 -B verify_package.py
python3 -B verify.py
```

**Erwartung:** Exit 0; nur die unten genannte Softwareaussage.

**Vorhandene Evidenz:**

- [docs/research/rax/wolfram-check-v0.1/RAX_W1_Exakte_Gegenpruefung_v0_1_Paket.zip](https://github.com/thomasmgfeller/x6-spectral-astrolabium/blob/dedddc11ed43b14bf872d56b02c92c5b65e695bb/docs/research/rax/wolfram-check-v0.1/RAX_W1_Exakte_Gegenpruefung_v0_1_Paket.zip): Gespeicherte Wolfram-Antworten und unabhängiger Python-Prüfer; interne Post-hoc-Prüfung.

**Nächste Abnahme:** Externe Reproduktion bzw. neuer Wolfram-Lauf mit eigener Umgebung; Aussagebereich nicht auf U2 ausdehnen.

<a id="wolfram-polarity"></a>
### Wolfram Fall 2: Polaritätsumkehr

**Stand:** MAIN / SOFTWARE; Branch `main`; Commit `dedddc11ed43b14bf872d56b02c92c5b65e695bb`.

**Anleitung:** [aktuelle main-Dokumentation](https://github.com/thomasmgfeller/x6-spectral-astrolabium/blob/main/docs/signal-lab/wolfram-polarity-v0.1/README.md). **Voraussetzungen:** Python 3.12/Standardbibliothek; Fall 2 mit --rerun zusätzlich Node. Kein frischer Wolfram-Lauf.

**Geprüfte Aussage:** Vier symbolische Identitäten und zwölf numerische Prüfungen; invertiertes Signal wird trotz gleicher PSD/Kohärenz zurückgewiesen.

```sh
python3 -m zipfile -e docs/signal-lab/wolfram-polarity-v0.1/X6_Wolfram_Fall2_v0_1.zip /tmp/x6-register-wolfram-polarity
cd /tmp/x6-register-wolfram-polarity/X6_Wolfram_Fall2_v0_1
python3 verify.py --rerun
```

**Erwartung:** PASS_WITH_SCOPE_LIMITS oder erfolgreicher paketabhängiger Prüfbericht; Exit 0. Wissenschaftliche Aussage bleibt auf den konstruierten Fall begrenzt.

**Vorhandene Evidenz:**

- [docs/signal-lab/wolfram-polarity-v0.1/X6_Wolfram_Fall2_v0_1.zip](https://github.com/thomasmgfeller/x6-spectral-astrolabium/blob/dedddc11ed43b14bf872d56b02c92c5b65e695bb/docs/signal-lab/wolfram-polarity-v0.1/X6_Wolfram_Fall2_v0_1.zip): Gespeicherte Erstfehler und korrigierte Wolfram-Antworten, Freeze-Dateien und vollständiges Inventar.

**Nächste Abnahme:** Externe Wiederholung; reale Signale benötigen einen eigenen Messvertrag.

<a id="wolfram-dependence"></a>
### Wolfram Fall 4: Nullfehler und Abhängigkeit

**Stand:** MAIN / SOFTWARE; Branch `main`; Commit `dedddc11ed43b14bf872d56b02c92c5b65e695bb`.

**Anleitung:** [aktuelle main-Dokumentation](https://github.com/thomasmgfeller/x6-spectral-astrolabium/blob/main/docs/signal-lab/wolfram-zero-failures-v0.1/README.md). **Voraussetzungen:** Python 3.12/Standardbibliothek; Fall 2 mit --rerun zusätzlich Node. Kein frischer Wolfram-Lauf.

**Geprüfte Aussage:** Zwölf Wolfram-Prüfungen und sieben Python-Vergleiche: unabhängige Versuche und Kopien eines Versuchs haben unterschiedliche Deckung.

```sh
python3 -m zipfile -e docs/signal-lab/wolfram-zero-failures-v0.1/X6_Wolfram_Fall4_v0_1.zip /tmp/x6-register-wolfram-dependence
cd /tmp/x6-register-wolfram-dependence/X6_Wolfram_Fall4_v0_1
python3 verify.py
```

**Erwartung:** PASS_WITH_SCOPE_LIMITS oder erfolgreicher paketabhängiger Prüfbericht; Exit 0. Wissenschaftliche Aussage bleibt auf den konstruierten Fall begrenzt.

**Vorhandene Evidenz:**

- [docs/signal-lab/wolfram-zero-failures-v0.1/X6_Wolfram_Fall4_v0_1.zip](https://github.com/thomasmgfeller/x6-spectral-astrolabium/blob/dedddc11ed43b14bf872d56b02c92c5b65e695bb/docs/signal-lab/wolfram-zero-failures-v0.1/X6_Wolfram_Fall4_v0_1.zip): Gespeicherte Erstfehler und korrigierte Wolfram-Antworten, Freeze-Dateien und vollständiges Inventar.

**Nächste Abnahme:** Unabhängigkeit konkreter Datensätze belegen; das konstruktive Gegenbeispiel ist kein Audit aller Projektdaten.

<a id="wolfram-causal"></a>
### Wolfram Fall 5: Kausalordnung

**Stand:** MAIN / SOFTWARE; Branch `main`; Commit `dedddc11ed43b14bf872d56b02c92c5b65e695bb`.

**Anleitung:** [aktuelle main-Dokumentation](https://github.com/thomasmgfeller/x6-spectral-astrolabium/blob/main/docs/research/causal-order/wolfram-countercheck-v0.1/README.md). **Voraussetzungen:** Python 3.12/Standardbibliothek; Fall 2 mit --rerun zusätzlich Node. Kein frischer Wolfram-Lauf.

**Geprüfte Aussage:** Sechzehn Wolfram-Assertions und exakte Python-Polynome bestätigen ein Drei-Ereignis-Gegenbeispiel gegen Vollständigkeit dieses Fingerprints.

```sh
python3 -m zipfile -e docs/research/causal-order/wolfram-countercheck-v0.1/X6_Wolfram_Fall5_v0_1.zip /tmp/x6-register-wolfram-causal
cd /tmp/x6-register-wolfram-causal/X6_Wolfram_Fall5_v0_1
python3 verify_release.py
```

**Erwartung:** PASS_WITH_SCOPE_LIMITS oder erfolgreicher paketabhängiger Prüfbericht; Exit 0. Wissenschaftliche Aussage bleibt auf den konstruierten Fall begrenzt.

**Vorhandene Evidenz:**

- [docs/research/causal-order/wolfram-countercheck-v0.1/X6_Wolfram_Fall5_v0_1.zip](https://github.com/thomasmgfeller/x6-spectral-astrolabium/blob/dedddc11ed43b14bf872d56b02c92c5b65e695bb/docs/research/causal-order/wolfram-countercheck-v0.1/X6_Wolfram_Fall5_v0_1.zip): Gespeicherte Erstfehler und korrigierte Wolfram-Antworten, Freeze-Dateien und vollständiges Inventar.

**Nächste Abnahme:** Zusätzliche Invarianten an registrierten Korpora prüfen; kein allgemeiner Rekonstruktionssatz.

<a id="data-agents"></a>
### Öffentliche Datenagenten: NOAA, Atlas, QuTech, NASA

**Stand:** MAIN / SOFTWARE; Branch `main`; Commit `dedddc11ed43b14bf872d56b02c92c5b65e695bb`.

**Anleitung:** [aktuelle main-Dokumentation](https://github.com/thomasmgfeller/x6-spectral-astrolabium/blob/main/docs/SOURCE_AGENTS.md). **Voraussetzungen:** Lokale Tests: Abhängigkeiten aus agent/requirements.txt und agent/source-requirements.txt; siehe Dokumentation. Produktionsläufe nutzen geschützte GitHub-Workflows und deren Zeitfenster.

**Geprüfte Aussage:** Quellen-/Ablehnungsprüfungen und App-Checks auf öffentlichen Daten. Vier Datenjobs in zwei Workflows; kein Denoising-Nutzenbeleg.

```sh
python3 -m unittest tests/python/test_data_agent.py tests/python/test_source_agents.py -v
```

**Erwartung:** Lokale Softwaretests; kein neuer Datenabruf. Tatsächliche geplante Läufe siehe datierte Workflow-Links im Register.

**Vorhandene Evidenz:**

- [docs/DATA_AGENT.md](https://github.com/thomasmgfeller/x6-spectral-astrolabium/blob/dedddc11ed43b14bf872d56b02c92c5b65e695bb/docs/DATA_AGENT.md): NOAA-Lauf, Inputs und Actions-Artefakte 30 Tage.
- [docs/SOURCE_AGENTS.md](https://github.com/thomasmgfeller/x6-spectral-astrolabium/blob/dedddc11ed43b14bf872d56b02c92c5b65e695bb/docs/SOURCE_AGENTS.md): Atlas/QuTech/NASA-Artefakte 14 Tage; Archivdaten explizit gekennzeichnet.
- [docs/AGENT_WINDOW_REPAIR_2026_10_13.md](https://github.com/thomasmgfeller/x6-spectral-astrolabium/blob/dedddc11ed43b14bf872d56b02c92c5b65e695bb/docs/AGENT_WINDOW_REPAIR_2026_10_13.md): Dokumentierte Fenster- und Schutzprüfungen.

**Nächste Abnahme:** Originale und komplette Artefakte vor Ablauf sichern; unabhängiger Datensatz-/Drift- und Qualitätsvergleich. Nach Frist STOPPED erwarten.

<a id="lorentz-agent"></a>
### Begrenzter Mathematikagent: Lorentz n=3–5 und Propagator

**Stand:** MAIN / SOFTWARE; Branch `main`; Commit `dedddc11ed43b14bf872d56b02c92c5b65e695bb`.

**Anleitung:** [aktuelle main-Dokumentation](https://github.com/thomasmgfeller/x6-spectral-astrolabium/blob/main/docs/MATH_AGENT.md). **Voraussetzungen:** Python 3.12, Node >=22 und gepinnte mathematische Abhängigkeiten.

**Geprüfte Aussage:** Endliche Ordnungszählung und 1+1-Diamond-Spektralvergleich; Replikation/Kalibrierung, kein neuer Satz.

```sh
python3 -m pip install -r agent/math-requirements.txt
python3 -m unittest tests/python/test_math_agent.py tests/python/test_lorentz_spectral.py -v
```

**Erwartung:** Exit 0 bei bestandenen Regressionen; startet keinen geplanten Forschungslauf.

**Vorhandene Evidenz:**

- [docs/LORENTZ_RESEARCH.md](https://github.com/thomasmgfeller/x6-spectral-astrolabium/blob/dedddc11ed43b14bf872d56b02c92c5b65e695bb/docs/LORENTZ_RESEARCH.md): Definierte Referenzen, n=3/4/5-Zielzählungen und Grenzen.
- [agent/math-agent-config.json](https://github.com/thomasmgfeller/x6-spectral-astrolabium/blob/dedddc11ed43b14bf872d56b02c92c5b65e695bb/agent/math-agent-config.json): Konfiguriertes exklusives Ende 2026-10-18T22:00:00Z; 90 Sekunden Rechenbudget.

**Nächste Abnahme:** Unabhängige Replikation; separat registrierte Grössen/Seeds/Ränge und Unsicherheit für Finite-Size-Studie. n=6 siehe Branch-Modul.

<a id="lorentz-n6"></a>
### Lorentz-Kollisionsatlas n=6: vollständiger Forschungsstand

**Stand:** BRANCH_ONLY / SOFTWARE; Branch `research/lorentz-v1-workpackages`; Commit `f5116b9970a6b7dc788c18623a8386b4cde33ad4`.

**Anleitung:** [gepinntes Quelldokument](https://github.com/thomasmgfeller/x6-spectral-astrolabium/blob/f5116b9970a6b7dc788c18623a8386b4cde33ad4/research/lorentz_n6/README.md). **Voraussetzungen:** Python 3.12/Standardbibliothek für diesen unabhängigen Prüfer; vollständiger Atlasgenerator benötigt NumPy 2.3.5.

**Geprüfte Aussage:** 318 Ordnungen; 286 Spektralklassen, mit Endpunktzahlen 314, Quill-Basis 285, mit maximalen Quills 318. Nur endlicher Korpus. Vollständiger Forschungsstand einschließlich Generator auf diesem Branch; bytegleicher Prüfer und fester Atlas auch in main über die gemeinsame Offline-Referenzsuite.

```sh
git clone --branch research/lorentz-v1-workpackages https://github.com/thomasmgfeller/x6-spectral-astrolabium.git x6-lorentz-n6
cd x6-lorentz-n6
git checkout --detach f5116b9970a6b7dc788c18623a8386b4cde33ad4
```

```sh
python3 research/lorentz_n6/verify.py research/lorentz_n6/results/atlas_n6.json --output /tmp/register-atlas-check.json
```

**Erwartung:** Exit 0; nur die unten genannte Softwareaussage.

**Vorhandene Evidenz:**

- [research/lorentz_n6/results/atlas_n6.json](https://github.com/thomasmgfeller/x6-spectral-astrolabium/blob/f5116b9970a6b7dc788c18623a8386b4cde33ad4/research/lorentz_n6/results/atlas_n6.json): Vollständige Repräsentanten, Polynome und Kollisionsgruppen.
- [research/lorentz_n6/results/independent_verification.json](https://github.com/thomasmgfeller/x6-spectral-astrolabium/blob/f5116b9970a6b7dc788c18623a8386b4cde33ad4/research/lorentz_n6/results/independent_verification.json): Separater Rekonstruktions-/Isomorphie-/Determinantenprüfer, 4.208 Polynome.

**Nächste Abnahme:** Vier Endpunkt-Kollisionspaare extern prüfen; vor n=7 genaue neue Hypothese, Literaturabgrenzung und Laufzeitbudget festlegen.

<a id="industrial-v1"></a>
### Industrielle Entrauschung: V1-Bewertungsadapter

**Stand:** BRANCH_ONLY / SOFTWARE; Branch `research/lorentz-v1-workpackages`; Commit `f5116b9970a6b7dc788c18623a8386b4cde33ad4`.

**Anleitung:** [gepinntes Quelldokument](https://github.com/thomasmgfeller/x6-spectral-astrolabium/blob/f5116b9970a6b7dc788c18623a8386b4cde33ad4/experiments/industrial-v1/README.md). **Voraussetzungen:** Python 3.12, gepinnte Anforderungen aus requirements; isolierte venv empfohlen.

**Geprüfte Aussage:** Vier Schemata, Vorprüfung, Bewertung und synthetischer Kontrollgenerator. Reale AP1-Freigabe bleibt NOT_READY.

```sh
git clone --branch research/lorentz-v1-workpackages https://github.com/thomasmgfeller/x6-spectral-astrolabium.git x6-industrial-v1
cd x6-industrial-v1
git checkout --detach f5116b9970a6b7dc788c18623a8386b4cde33ad4
```

```sh
python3 -m pip install -r experiments/industrial-v1/requirements.txt
python3 experiments/industrial-v1/evaluate.py experiments/industrial-v1/V1_PROFILE_DRAFT.json --root experiments/industrial-v1 --output /tmp/register-v1-readiness.json
```

**Erwartung:** NOT_READY, Exit 3 ist beim veröffentlichten Entwurf erwartet.

**Vorhandene Evidenz:**

- [experiments/industrial-v1/examples/draft_readiness.json](https://github.com/thomasmgfeller/x6-spectral-astrolabium/blob/f5116b9970a6b7dc788c18623a8386b4cde33ad4/experiments/industrial-v1/examples/draft_readiness.json): Offene Eingabe-/Mess-/Protokollfelder einzeln ausgewiesen.

**Nächste Abnahme:** Reale V1-Daten/Referenzlabels, Powerplanung, Splits und Protokollreview; erst danach Freeze und echte Filter-/Ressourcenmessung.

<a id="fingerprint"></a>
### Mehrschichtiger Fingerprint

**Stand:** BRANCH_ONLY / SOFTWARE; Branch `research/x6-fingerprint-v1`; Commit `f22030f2dae0aa670cdbc450c5e881ce250b36b8`.

**Anleitung:** [gepinntes Quelldokument](https://github.com/thomasmgfeller/x6-spectral-astrolabium/blob/f22030f2dae0aa670cdbc450c5e881ce250b36b8/research/fingerprint_v1/README.md). **Voraussetzungen:** Python 3.12 und Anforderungen aus industrial-v1; nur validieren, keine Beispielregeneration nötig.

**Geprüfte Aussage:** n6-0073 und n6-0181 werden durch gerichtete Gradmultimengen getrennt. Physischer MODAL_2R1F-Pilot ist ungemessen.

```sh
git clone --branch research/x6-fingerprint-v1 https://github.com/thomasmgfeller/x6-spectral-astrolabium.git x6-fingerprint
cd x6-fingerprint
git checkout --detach f22030f2dae0aa670cdbc450c5e881ce250b36b8
```

```sh
python3 -m pip install -r experiments/industrial-v1/requirements.txt
python3 research/fingerprint_v1/validate.py research/fingerprint_v1/examples/n6-0073.json research/fingerprint_v1/examples/n6-0181.json research/fingerprint_v1/examples/separation-event.json research/fingerprint_v1/examples/physical-pilot-plan.json
```

**Erwartung:** Exit 0; nur die unten genannte Softwareaussage.

**Vorhandene Evidenz:**

- [research/fingerprint_v1/examples/separation-event.json](https://github.com/thomasmgfeller/x6-spectral-astrolabium/blob/f22030f2dae0aa670cdbc450c5e881ce250b36b8/research/fingerprint_v1/examples/separation-event.json): Exakter Vergleich gebundener gespeicherter Werte; Validator berechnet nicht jedes Polynom aus Rohmatrizen neu.
- [research/fingerprint_v1/examples/physical-pilot-plan.json](https://github.com/thomasmgfeller/x6-spectral-astrolabium/blob/f22030f2dae0aa670cdbc450c5e881ce250b36b8/research/fingerprint_v1/examples/physical-pilot-plan.json): Expliziter Messplan ohne erfundene Messwerte.

**Nächste Abnahme:** Empirischen Assessor mit Unsicherheit/Bestätigungsdaten implementieren; Pilot kalibrieren und Rohdaten prüfen.

<a id="experiment-fabric"></a>
### Experiment Fabric

**Stand:** BRANCH_ONLY / SOFTWARE; Branch `research/x6-experiment-fabric-v1`; Commit `a34c59f2b0e2d30c73936363040669941aa8ce09`.

**Anleitung:** [gepinntes Quelldokument](https://github.com/thomasmgfeller/x6-spectral-astrolabium/blob/a34c59f2b0e2d30c73936363040669941aa8ce09/experimental/experiment_fabric/README.md). **Voraussetzungen:** Node >=22, Python 3.12 und Anforderungen aus industrial-v1.

**Geprüfte Aussage:** Gemeinsamer EIG-Planer, lokale Simulationsworker und Replay; ein Kontrollfall, kein reales Gerätenetz oder Nutzenvergleich.

```sh
git clone --branch research/x6-experiment-fabric-v1 https://github.com/thomasmgfeller/x6-spectral-astrolabium.git x6-experiment-fabric
cd x6-experiment-fabric
git checkout --detach a34c59f2b0e2d30c73936363040669941aa8ce09
```

```sh
node experimental/experiment_fabric/run.mjs run /tmp/register-fabric
node experimental/experiment_fabric/run.mjs verify /tmp/register-fabric/run.json
python3 -m pip install -r experiments/industrial-v1/requirements.txt
python3 experimental/experiment_fabric/verify_reference.py /tmp/register-fabric/run.json
```

**Erwartung:** Exit 0; nur die unten genannte Softwareaussage.

**Vorhandene Evidenz:**

- [experimental/experiment_fabric/examples/control-run.json](https://github.com/thomasmgfeller/x6-spectral-astrolabium/blob/a34c59f2b0e2d30c73936363040669941aa8ce09/experimental/experiment_fabric/examples/control-run.json): Gespeicherter synthetischer Kontrolllauf.
- [experimental/experiment_fabric/VALIDATION.md](https://github.com/thomasmgfeller/x6-spectral-astrolabium/blob/a34c59f2b0e2d30c73936363040669941aa8ce09/experimental/experiment_fabric/VALIDATION.md): Dokumentierte Referenz- und Browserprüfung, begrenzter Geltungsbereich.

**Nächste Abnahme:** Zwei echte Rechennodes mit persistenten Jobs, Wiederanlauf und Tests für doppelte/verspätete Zustellung; anschliessend gleich budgetierter Nutzenvergleich.

<a id="neutral-discovery"></a>
### Neutral Discovery

**Stand:** BRANCH_ONLY / SOFTWARE; Branch `research/x6-neutral-discovery-v1`; Commit `1a02c482d59a42d554337fb83e0f6d6e6d84b516`.

**Anleitung:** [gepinntes Quelldokument](https://github.com/thomasmgfeller/x6-spectral-astrolabium/blob/1a02c482d59a42d554337fb83e0f6d6e6d84b516/experimental/neutral_discovery/README.md). **Voraussetzungen:** Python 3.12/jsonschema, Node >=22 für die JS-Gegenprüfung.

**Geprüfte Aussage:** Drei synthetische Kontrollen und Challenge-Gates in endlichem Modellraum; hohe vorherige Gewichtung verhindert keine Verwerfung.

```sh
git clone --branch research/x6-neutral-discovery-v1 https://github.com/thomasmgfeller/x6-spectral-astrolabium.git x6-neutral-discovery
cd x6-neutral-discovery
git checkout --detach 1a02c482d59a42d554337fb83e0f6d6e6d84b516
```

```sh
python3 -m pip install -r experiments/industrial-v1/requirements.txt
python3 experimental/neutral_discovery/discovery.py verify experimental/neutral_discovery/examples/control.json
python3 -m unittest discover -s experimental/neutral_discovery/tests -v
```

**Erwartung:** Exit 0; nur die unten genannte Softwareaussage.

**Vorhandene Evidenz:**

- [experimental/neutral_discovery/VALIDATION.md](https://github.com/thomasmgfeller/x6-spectral-astrolabium/blob/1a02c482d59a42d554337fb83e0f6d6e6d84b516/experimental/neutral_discovery/VALIDATION.md): 17 Python-Tests, neun Zweierbatches/36 Ausgangsbelegungen, vollständige endliche Testgrössenprüfung.
- [experimental/neutral_discovery/examples/control.json](https://github.com/thomasmgfeller/x6-spectral-astrolabium/blob/1a02c482d59a42d554337fb83e0f6d6e6d84b516/experimental/neutral_discovery/examples/control.json): Deterministische publizierte Kontrollen.

**Nächste Abnahme:** Persistente Präregistrierung und kampagnenübergreifendes Fehlerbudget; unabhängige Bestätigung unter erweitertem Modellraum.

<a id="nqk"></a>
### NQK: Forschungsdossier

**Stand:** BRANCH_ONLY / DOSSIER; Branch `research/nqk`; Commit `a8fbc70fae3ecb46bfcd8ceb828ce182e533dd04`.

**Anleitung:** [gepinntes Quelldokument](https://github.com/thomasmgfeller/x6-spectral-astrolabium/blob/a8fbc70fae3ecb46bfcd8ceb828ce182e533dd04/research/nqk/README.md). **Voraussetzungen:** PDF-/Markdown-Leser.

**Geprüfte Aussage:** Eigenständige Roadmap und Forschungsfassung; historische Tests 001–013 unbestätigt. Vier vollständige Code-/Datenarchive fehlen in diesem Zweig.

```sh
git clone --branch research/nqk https://github.com/thomasmgfeller/x6-spectral-astrolabium.git x6-nqk
cd x6-nqk
git checkout --detach a8fbc70fae3ecb46bfcd8ceb828ce182e533dd04
```

**Erwartung:** Kein eigenständig ausführbares NQK-Gesamtpaket in diesem Branch. Photonic Link enthält nur ausgewählte numerische Referenzfunktionen.

**Vorhandene Evidenz:**

- [research/nqk/baseline/baseline_summary.json](https://github.com/thomasmgfeller/x6-spectral-astrolabium/blob/a8fbc70fae3ecb46bfcd8ceb828ce182e533dd04/research/nqk/baseline/baseline_summary.json): Zusammenfassung mit Archividentitäten/Prüfsummen, keine öffentlich vollständige Reproduktion.
- [research/nqk/STATUS.md](https://github.com/thomasmgfeller/x6-spectral-astrolabium/blob/a8fbc70fae3ecb46bfcd8ceb828ce182e533dd04/research/nqk/STATUS.md): Begrenzte synthetische Befunde und offene Schritte.

**Nächste Abnahme:** M1: vollständige Archive kontrolliert übernehmen, erwartete Befunde definieren und aus frischem Checkout unabhängig ausführen.

<a id="photonic-link"></a>
### Photonic Link Validation Lab

**Stand:** BRANCH_ONLY / SOFTWARE; Branch `research/photonic-link`; Commit `7ff72fcd6a16e9b353d1af277307463f757d3470`.

**Anleitung:** [gepinntes Quelldokument](https://github.com/thomasmgfeller/x6-spectral-astrolabium/blob/7ff72fcd6a16e9b353d1af277307463f757d3470/research/photonic-link/README.md). **Voraussetzungen:** Python 3.12/venv und requirements; GHDL optional für zusätzliche RTL-Prüfung.

**Geprüfte Aussage:** Gemeinsames synthetisches Verlust-, Polarisationsdrift- und Zeitmodell; affine Uhrkalibrierung mit getrennten Modellpulsen.

```sh
git clone --branch research/photonic-link https://github.com/thomasmgfeller/x6-spectral-astrolabium.git x6-photonic-link
cd x6-photonic-link
git checkout --detach 7ff72fcd6a16e9b353d1af277307463f757d3470
```

```sh
cd research/photonic-link
python3 -m pip install -r requirements.txt
python3 validate.py --output /tmp/register-plvl-validation.json
python3 experiments.py --output /tmp/register-plvl-experiments.json
```

**Erwartung:** Exit 0; nur die unten genannte Softwareaussage.

**Vorhandene Evidenz:**

- [research/photonic-link/evidence/validation.json](https://github.com/thomasmgfeller/x6-spectral-astrolabium/blob/7ff72fcd6a16e9b353d1af277307463f757d3470/research/photonic-link/evidence/validation.json): Gespeicherte Validierung; optionale RTL-Tests separat gekennzeichnet.
- [research/photonic-link/evidence/experiments.json](https://github.com/thomasmgfeller/x6-spectral-astrolabium/blob/7ff72fcd6a16e9b353d1af277307463f757d3470/research/photonic-link/evidence/experiments.json): Synthetische Szenarien mit Fehlfällen; kein gemessener Photonenlink.

**Nächste Abnahme:** Modellparameter/Identifizierbarkeit mit realen Zeitstempeln, Verlust- und Driftmessungen prüfen; Fehlerbudget und unabhängige Kalibrierreferenz.

## Branch-Inventar und Pflege

Die drei aufeinander aufbauenden Branches Fingerprint → Fabric → Neutral Discovery enthalten auch frühere Module. Zum Snapshot sind die registrierten n=6-, V1-, Fingerprint- und Fabric-Dateien in den jeweiligen späteren Zweigen bytegleich. Die obigen eigenen Modulzweige bleiben die minimalen nachvollziehbaren Einstiege. NQK und Photonic Link bleiben eigenständig.

Ein historischer Branch kann ungemergte Commits haben, obwohl sein Modul bereits via Squash/Cherry-pick in main angekommen ist. Daher sind Commit-Vorsprünge keine Modulreife- oder Integrationsnachweise. Alte Feature-/Publikationsbranches unten sind keine alternativen Empfehlungen zu den main-Einträgen.

| Beobachteter Branch | Tip-Commit | Commits nur dort / nur main | Rolle |
| --- | --- | --- |
| `docs/wolfram-causal-order-v0-1` | [3f8fb920ddef](https://github.com/thomasmgfeller/x6-spectral-astrolabium/commit/3f8fb920ddefd9ede13d0855a14f4bfb1c7b1239) | 0 / 6 | Historischer Entwicklungs-/Publikationszweig |
| `docs/wolfram-zero-failures-v0-1` | [a40a513a9633](https://github.com/thomasmgfeller/x6-spectral-astrolabium/commit/a40a513a9633cbe6aad4ce66132331d9264c0bab) | 0 / 8 | Historischer Entwicklungs-/Publikationszweig |
| `feat/signal-validation-lab` | [33032c23dd0e](https://github.com/thomasmgfeller/x6-spectral-astrolabium/commit/33032c23dd0ef3e035d38c5b9cf7c3db6faf65f0) | 1 / 43 | Historischer Entwicklungs-/Publikationszweig |
| `feature/sagnac-integration-preview-0.1` | [7aaa8e38acc6](https://github.com/thomasmgfeller/x6-spectral-astrolabium/commit/7aaa8e38acc60be556614dd4e4c0ac1697b45815) | 1 / 66 | Historischer Entwicklungs-/Publikationszweig |
| `fix/evidence-audit-20261012` | [680fe6a43e66](https://github.com/thomasmgfeller/x6-spectral-astrolabium/commit/680fe6a43e664164a26dcf1b8cfb6bf52a1b3b56) | 1 / 44 | Historischer Entwicklungs-/Publikationszweig |
| `fix/safe-x6-publish` | [f80225268928](https://github.com/thomasmgfeller/x6-spectral-astrolabium/commit/f802252689284de402a3a322a64a69a07098622f) | 0 / 127 | Historischer Entwicklungs-/Publikationszweig |
| `fix/signal-lab-evidence-archive` | [d43238b4e110](https://github.com/thomasmgfeller/x6-spectral-astrolabium/commit/d43238b4e110ea7338f225334f23c6cde179626e) | 1 / 42 | Historischer Entwicklungs-/Publikationszweig |
| `main` | [dedddc11ed43](https://github.com/thomasmgfeller/x6-spectral-astrolabium/commit/dedddc11ed43b14bf872d56b02c92c5b65e695bb) | 0 / 0 | integration, offline-reference, astrolabium, signal-lab, edge-reference, evidence-calibration, phase-contract, industrial-programme, sagnac-import, photonic-design, acvm-concept, acvm-c1, acvm-optical, sagnac-components, acvm-records, acvm-fixture, rax-programme, rax-u1, rax-b1-m1, rax-w1, wolfram-polarity, wolfram-dependence, wolfram-causal, data-agents, lorentz-agent |
| `publication/acvm-c1-v0.1` | [b3def446889b](https://github.com/thomasmgfeller/x6-spectral-astrolabium/commit/b3def446889b34cc25afeb1aad14930199636c22) | 0 / 22 | Historischer Entwicklungs-/Publikationszweig |
| `publication/acvm-optical-v0.2` | [94f08ef30a60](https://github.com/thomasmgfeller/x6-spectral-astrolabium/commit/94f08ef30a60cab4a6534aef9b0d05e1d5b2ff0b) | 0 / 15 | Historischer Entwicklungs-/Publikationszweig |
| `publication/sagnac-components-v0.1-20261015` | [7f0f8b893e5f](https://github.com/thomasmgfeller/x6-spectral-astrolabium/commit/7f0f8b893e5fb91708cb75c1460f880adaf2e519) | 0 / 12 | Historischer Entwicklungs-/Publikationszweig |
| `publication/wolfram-polarity-v0.1-20261015` | [8b6785d55689](https://github.com/thomasmgfeller/x6-spectral-astrolabium/commit/8b6785d556895bcb19856061a681720c3f3ff228) | 0 / 10 | Historischer Entwicklungs-/Publikationszweig |
| `publish/photonic-two-qubit-design` | [8f0cdaad0cd8](https://github.com/thomasmgfeller/x6-spectral-astrolabium/commit/8f0cdaad0cd8823ceb2a3db6f2d9a5815d6134ba) | 1 / 65 | Historischer Entwicklungs-/Publikationszweig |
| `research/lorentz-v1-workpackages` | [f5116b9970a6](https://github.com/thomasmgfeller/x6-spectral-astrolabium/commit/f5116b9970a6b7dc788c18623a8386b4cde33ad4) | 1 / 33 | lorentz-n6, industrial-v1 |
| `research/nqk` | [a8fbc70fae3e](https://github.com/thomasmgfeller/x6-spectral-astrolabium/commit/a8fbc70fae3ecb46bfcd8ceb828ce182e533dd04) | 2 / 41 | nqk |
| `research/photonic-link` | [7ff72fcd6a16](https://github.com/thomasmgfeller/x6-spectral-astrolabium/commit/7ff72fcd6a16e9b353d1af277307463f757d3470) | 1 / 40 | photonic-link |
| `research/rax-w1-publication` | [1cd7e4bb7167](https://github.com/thomasmgfeller/x6-spectral-astrolabium/commit/1cd7e4bb71672233058e061d18fae6b249d948ad) | 0 / 26 | Historischer Entwicklungs-/Publikationszweig |
| `research/x6-edge-reference` | [7ac131bcfbab](https://github.com/thomasmgfeller/x6-spectral-astrolabium/commit/7ac131bcfbabd658b38fb1c97686325ac47fa081) | 0 / 33 | Historischer Entwicklungs-/Publikationszweig |
| `research/x6-experiment-fabric-v1` | [a34c59f2b0e2](https://github.com/thomasmgfeller/x6-spectral-astrolabium/commit/a34c59f2b0e2d30c73936363040669941aa8ce09) | 3 / 33 | experiment-fabric |
| `research/x6-fingerprint-v1` | [f22030f2dae0](https://github.com/thomasmgfeller/x6-spectral-astrolabium/commit/f22030f2dae0aa670cdbc450c5e881ce250b36b8) | 2 / 33 | fingerprint |
| `research/x6-integration-v0.1` | [87ca9ad6b12f](https://github.com/thomasmgfeller/x6-spectral-astrolabium/commit/87ca9ad6b12fd87869b393658f2ed6848f876c12) | 0 / 28 | Historischer Entwicklungs-/Publikationszweig |
| `research/x6-neutral-discovery-v1` | [1a02c482d59a](https://github.com/thomasmgfeller/x6-spectral-astrolabium/commit/1a02c482d59a42d554337fb83e0f6d6e6d84b516) | 4 / 33 | neutral-discovery |
| `x6-bounded-math-agent` | [122ba4eb5ac1](https://github.com/thomasmgfeller/x6-spectral-astrolabium/commit/122ba4eb5ac1e7496bf3426b0f3e908d08aa74ff) | 0 / 67 | Historischer Entwicklungs-/Publikationszweig |
| `x6-source-preview` | [24023fd88abd](https://github.com/thomasmgfeller/x6-spectral-astrolabium/commit/24023fd88abd676336098950ea3a08e93eeebfd8) | 0 / 75 | Historischer Entwicklungs-/Publikationszweig |

Bei einer Modulfreigabe zuerst MODULE_REGISTRY.json aktualisieren: Quellencommit, Einstieg, erwartete Ausgabe, Evidenzrevision und nächste Abnahme. Danach rendern und prüfen:

```sh
python3 tools/module_registry.py --write
python3 tools/module_registry.py --check --git-objects
python3 tests/python/verify_manifest.py
```

Die Prüfung vergleicht JSON und Markdown, vorhandene Hauptzweigpfade, optional alle gepinnten Git-Objekte samt Archiv-Einstiegen sowie UTC/Zürich-Frist und Workflows. Ein Checkout mit vollständiger Git-Historie wird für --git-objects benötigt; bei fehlenden Forschungsobjekten zuerst die im Register genannten Branches fetch-en. Sie führt keine Forschungskommandos, Geräteaktionen oder Agentenläufe aus. Neue wissenschaftliche Befunde benötigen eigene versionierte Evidenz; redaktionelle Registerpflege darf historische Archive und Prüfberichte nicht umschreiben.
