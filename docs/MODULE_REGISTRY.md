# X6 — zentrales Modul- und Evidenzregister

**Geprüfter Quellenstand: 2026-10-18.** Dieses Register ist der gemeinsame Einstieg in die veröffentlichten Module.

Es beschreibt einen datierten Snapshot, keinen Live-Monitor. Massgeblicher main-Ausgangscommit: [e947dfbdd49890dcb119940548537d1db59272c2](https://github.com/thomasmgfeller/x6-spectral-astrolabium/commit/e947dfbdd49890dcb119940548537d1db59272c2). Dokumentationsänderungen nach diesem Snapshot sind über die Git-Historie nachvollziehbar. Die Quellpins bezeichnen die verfügbare Implementierung; ältere Evidenzberichte behalten ihre eigenen Prüfrevisionen.

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
| X6 Data Agent | [38694613614](https://github.com/thomasmgfeller/x6-spectral-astrolabium/actions/runs/38694613614), `90b74509f2b65de08a77de8a7057204834951fc2` | success: Original-NOAA-Artefakt dauerhaft gesichert, Rohdaten und vollständiges Inventar geprüft; keine neue physische Validierung. |
| X6 Source Agents | [38697674497](https://github.com/thomasmgfeller/x6-spectral-astrolabium/actions/runs/38697674497), `90b74509f2b65de08a77de8a7057204834951fc2` | success: Atlas-Artefakt dieses Laufs dauerhaft gesichert und vollständig inventarisiert; NASA/QuTech nicht Teil dieser Archivauswahl. |
| X6 Bounded Math Agent | [38740481854](https://github.com/thomasmgfeller/x6-spectral-astrolabium/actions/runs/38740481854), `d94f99ca6b49f07e3c7c8d3a79b696fa9bca4d6c` | success: Originalartefakt dauerhaft gesichert, GitHub-Digest und vollständiges Inventar geprüft; keine neue wissenschaftliche Auswertung. |

## Modulübersicht

| Modul | Verfügbarkeit / Art | Branch / Quellcommit |
| --- | --- | --- |
| [Gemeinsamer lokaler Einstieg](#integration) | MAIN / SOFTWARE | `main` / [e947dfbdd498](https://github.com/thomasmgfeller/x6-spectral-astrolabium/commit/e947dfbdd49890dcb119940548537d1db59272c2) |
| [Gemeinsame Offline-Referenzsuite](#offline-reference) | MAIN / SOFTWARE | `main` / [e947dfbdd498](https://github.com/thomasmgfeller/x6-spectral-astrolabium/commit/e947dfbdd49890dcb119940548537d1db59272c2) |
| [Astrolabium und rationale Spektralreferenz](#astrolabium) | MAIN / SOFTWARE | `main` / [e947dfbdd498](https://github.com/thomasmgfeller/x6-spectral-astrolabium/commit/e947dfbdd49890dcb119940548537d1db59272c2) |
| [Signal Validation Lab](#signal-lab) | MAIN / SOFTWARE | `main` / [e947dfbdd498](https://github.com/thomasmgfeller/x6-spectral-astrolabium/commit/e947dfbdd49890dcb119940548537d1db59272c2) |
| [Edge-Referenzadapter](#edge-reference) | MAIN / SOFTWARE | `main` / [e947dfbdd498](https://github.com/thomasmgfeller/x6-spectral-astrolabium/commit/e947dfbdd49890dcb119940548537d1db59272c2) |
| [Evidence & Calibration](#evidence-calibration) | MAIN / SOFTWARE | `main` / [e947dfbdd498](https://github.com/thomasmgfeller/x6-spectral-astrolabium/commit/e947dfbdd49890dcb119940548537d1db59272c2) |
| [X6-Phasenfilter: Experimentvertrag](#phase-contract) | MAIN / SOFTWARE | `main` / [e947dfbdd498](https://github.com/thomasmgfeller/x6-spectral-astrolabium/commit/e947dfbdd49890dcb119940548537d1db59272c2) |
| [Industrielle Entrauschung: Forschungsprogramm v0.2](#industrial-programme) | MAIN / CONCEPT | `main` / [e947dfbdd498](https://github.com/thomasmgfeller/x6-spectral-astrolabium/commit/e947dfbdd49890dcb119940548537d1db59272c2) |
| [Sagnac-Aufnahme und Import](#sagnac-import) | MAIN / SOFTWARE | `main` / [e947dfbdd498](https://github.com/thomasmgfeller/x6-spectral-astrolabium/commit/e947dfbdd49890dcb119940548537d1db59272c2) |
| [Photonischer Zwei-Qubit-Aufbau und Jig](#photonic-design) | MAIN / SOFTWARE | `main` / [e947dfbdd498](https://github.com/thomasmgfeller/x6-spectral-astrolabium/commit/e947dfbdd49890dcb119940548537d1db59272c2) |
| [ACVM: Grundkonzept 0.1](#acvm-concept) | MAIN / CONCEPT | `main` / [e947dfbdd498](https://github.com/thomasmgfeller/x6-spectral-astrolabium/commit/e947dfbdd49890dcb119940548537d1db59272c2) |
| [ACVM C1: Steuerkanal](#acvm-c1) | MAIN / SOFTWARE | `main` / [e947dfbdd498](https://github.com/thomasmgfeller/x6-spectral-astrolabium/commit/e947dfbdd49890dcb119940548537d1db59272c2) |
| [ACVM 0.2: optischer Referenzablauf](#acvm-optical) | MAIN / SOFTWARE | `main` / [e947dfbdd498](https://github.com/thomasmgfeller/x6-spectral-astrolabium/commit/e947dfbdd49890dcb119940548537d1db59272c2) |
| [Sagnac-Komponenten und Ofen](#sagnac-components) | MAIN / CONCEPT | `main` / [e947dfbdd498](https://github.com/thomasmgfeller/x6-spectral-astrolabium/commit/e947dfbdd49890dcb119940548537d1db59272c2) |
| [ACVM Experiment Records](#acvm-records) | MAIN / CONCEPT | `main` / [e947dfbdd498](https://github.com/thomasmgfeller/x6-spectral-astrolabium/commit/e947dfbdd49890dcb119940548537d1db59272c2) |
| [ACVM Electrical & Thermal Test Fixture](#acvm-fixture) | MAIN / CONCEPT | `main` / [e947dfbdd498](https://github.com/thomasmgfeller/x6-spectral-astrolabium/commit/e947dfbdd49890dcb119940548537d1db59272c2) |
| [RAX: relationales Forschungsprogramm](#rax-programme) | MAIN / CONCEPT | `main` / [e947dfbdd498](https://github.com/thomasmgfeller/x6-spectral-astrolabium/commit/e947dfbdd49890dcb119940548537d1db59272c2) |
| [RAX-U1: Reduktionskontrolle](#rax-u1) | MAIN / SOFTWARE | `main` / [e947dfbdd498](https://github.com/thomasmgfeller/x6-spectral-astrolabium/commit/e947dfbdd49890dcb119940548537d1db59272c2) |
| [RAX-B1/M1: Benchmark und Methodenreview](#rax-b1-m1) | MAIN / SOFTWARE | `main` / [e947dfbdd498](https://github.com/thomasmgfeller/x6-spectral-astrolabium/commit/e947dfbdd49890dcb119940548537d1db59272c2) |
| [RAX-W1: exakte Wolfram-Gegenprüfung](#rax-w1) | MAIN / SOFTWARE | `main` / [e947dfbdd498](https://github.com/thomasmgfeller/x6-spectral-astrolabium/commit/e947dfbdd49890dcb119940548537d1db59272c2) |
| [Wolfram Fall 2: Polaritätsumkehr](#wolfram-polarity) | MAIN / SOFTWARE | `main` / [e947dfbdd498](https://github.com/thomasmgfeller/x6-spectral-astrolabium/commit/e947dfbdd49890dcb119940548537d1db59272c2) |
| [Wolfram Fall 4: Nullfehler und Abhängigkeit](#wolfram-dependence) | MAIN / SOFTWARE | `main` / [e947dfbdd498](https://github.com/thomasmgfeller/x6-spectral-astrolabium/commit/e947dfbdd49890dcb119940548537d1db59272c2) |
| [Wolfram Fall 5: Kausalordnung](#wolfram-causal) | MAIN / SOFTWARE | `main` / [e947dfbdd498](https://github.com/thomasmgfeller/x6-spectral-astrolabium/commit/e947dfbdd49890dcb119940548537d1db59272c2) |
| [Öffentliche Datenagenten: NOAA, Atlas, QuTech, NASA](#data-agents) | MAIN / SOFTWARE | `main` / [e947dfbdd498](https://github.com/thomasmgfeller/x6-spectral-astrolabium/commit/e947dfbdd49890dcb119940548537d1db59272c2) |
| [Begrenzter Mathematikagent: Lorentz n=3–5 und Propagator](#lorentz-agent) | MAIN / SOFTWARE | `main` / [e947dfbdd498](https://github.com/thomasmgfeller/x6-spectral-astrolabium/commit/e947dfbdd49890dcb119940548537d1db59272c2) |
| [Lorentz-Kollisionsatlas n=6: vollständiger Forschungsstand](#lorentz-n6) | BRANCH_ONLY / SOFTWARE | `research/lorentz-v1-workpackages` / [f5116b9970a6](https://github.com/thomasmgfeller/x6-spectral-astrolabium/commit/f5116b9970a6b7dc788c18623a8386b4cde33ad4) |
| [Lorentz: vier n=6-Restpaare und Grenzen der Gradseparatoren](#lorentz-n6-residuals) | MAIN / SOFTWARE | `main` / [e947dfbdd498](https://github.com/thomasmgfeller/x6-spectral-astrolabium/commit/e947dfbdd49890dcb119940548537d1db59272c2) |
| [Lorentz: vollständige n=7-Prüfung und Widerlegung von H7](#lorentz-n7-complete) | MAIN / SOFTWARE | `main` / [e947dfbdd498](https://github.com/thomasmgfeller/x6-spectral-astrolabium/commit/e947dfbdd49890dcb119940548537d1db59272c2) |
| [Industrielle Entrauschung: V1-Bewertungsadapter](#industrial-v1) | MAIN / SOFTWARE | `main` / [e947dfbdd498](https://github.com/thomasmgfeller/x6-spectral-astrolabium/commit/e947dfbdd49890dcb119940548537d1db59272c2) |
| [Industrieller Datenvertrag: Paderborn-Machbarkeitspilot](#industrial-pilot) | MAIN / SOFTWARE | `main` / [e947dfbdd498](https://github.com/thomasmgfeller/x6-spectral-astrolabium/commit/e947dfbdd49890dcb119940548537d1db59272c2) |
| [Mehrschichtiger Fingerprint](#fingerprint) | BRANCH_ONLY / SOFTWARE | `research/x6-fingerprint-v1` / [f22030f2dae0](https://github.com/thomasmgfeller/x6-spectral-astrolabium/commit/f22030f2dae0aa670cdbc450c5e881ce250b36b8) |
| [Experiment Fabric](#experiment-fabric) | BRANCH_ONLY / SOFTWARE | `research/x6-experiment-fabric-v1` / [a34c59f2b0e2](https://github.com/thomasmgfeller/x6-spectral-astrolabium/commit/a34c59f2b0e2d30c73936363040669941aa8ce09) |
| [Neutral Discovery](#neutral-discovery) | BRANCH_ONLY / SOFTWARE | `research/x6-neutral-discovery-v1` / [1a02c482d59a](https://github.com/thomasmgfeller/x6-spectral-astrolabium/commit/1a02c482d59a42d554337fb83e0f6d6e6d84b516) |
| [NQK: Forschungsdossier](#nqk) | BRANCH_ONLY / DOSSIER | `research/nqk` / [a8fbc70fae3e](https://github.com/thomasmgfeller/x6-spectral-astrolabium/commit/a8fbc70fae3ecb46bfcd8ceb828ce182e533dd04) |
| [Photonic Link Validation Lab](#photonic-link) | BRANCH_ONLY / SOFTWARE | `research/photonic-link` / [7ff72fcd6a16](https://github.com/thomasmgfeller/x6-spectral-astrolabium/commit/7ff72fcd6a16e9b353d1af277307463f757d3470) |
| [RAX-G1: deklarativer Runner und Fehlerbudget](#rax-guarded) | MAIN / SOFTWARE | `main` / [e947dfbdd498](https://github.com/thomasmgfeller/x6-spectral-astrolabium/commit/e947dfbdd49890dcb119940548537d1db59272c2) |
| [Gemeinsame Referenzedition und Agentenarchiv](#reference-edition) | MAIN / SOFTWARE | `main` / [e947dfbdd498](https://github.com/thomasmgfeller/x6-spectral-astrolabium/commit/e947dfbdd49890dcb119940548537d1db59272c2) |
| [X6-QE: exakte Graphreferenzen und Grenzen spektraler Unterscheidbarkeit](#x6-qe) | MAIN / SOFTWARE | `main` / [e947dfbdd498](https://github.com/thomasmgfeller/x6-spectral-astrolabium/commit/e947dfbdd49890dcb119940548537d1db59272c2) |
| [RAX-CQG: endlicher Causal-Set Benchmark 0.2.0](#rax-cqg-benchmark) | MAIN / SOFTWARE | `main` / [e947dfbdd498](https://github.com/thomasmgfeller/x6-spectral-astrolabium/commit/e947dfbdd49890dcb119940548537d1db59272c2) |
| [RAX-CQG: freies Feld und Entropiereferenz](#free-field-entropy) | MAIN / SOFTWARE | `main` / [e947dfbdd498](https://github.com/thomasmgfeller/x6-spectral-astrolabium/commit/e947dfbdd49890dcb119940548537d1db59272c2) |
| [Eigenzeit: Referenz, Fehlergrenzen und sequenzielle Diagnose](#lorentz-proper-time) | MAIN / SOFTWARE | `main` / [e947dfbdd498](https://github.com/thomasmgfeller/x6-spectral-astrolabium/commit/e947dfbdd49890dcb119940548537d1db59272c2) |
| [Krümmungsbenchmark: Empfindlichkeit und Dichteverwechslung](#lorentz-curvature) | MAIN / SOFTWARE | `main` / [e947dfbdd498](https://github.com/thomasmgfeller/x6-spectral-astrolabium/commit/e947dfbdd49890dcb119940548537d1db59272c2) |
| [RSS bei fester Punktzahl: Formeln, Prüfung und Grenzen](#lorentz-rss-fixed-n) | MAIN / SOFTWARE | `main` / [e947dfbdd498](https://github.com/thomasmgfeller/x6-spectral-astrolabium/commit/e947dfbdd49890dcb119940548537d1db59272c2) |
| [Eigenzeit v0.2: Gültigkeitsbereich und Informationsbedarf](#lorentz-proper-time-validity) | MAIN / SOFTWARE | `main` / [e947dfbdd498](https://github.com/thomasmgfeller/x6-spectral-astrolabium/commit/e947dfbdd49890dcb119940548537d1db59272c2) |
| [Eigenzeit: de-Sitter-Informationsplanung](#lorentz-de-sitter-information) | MAIN / SOFTWARE | `main` / [e947dfbdd498](https://github.com/thomasmgfeller/x6-spectral-astrolabium/commit/e947dfbdd49890dcb119940548537d1db59272c2) |
| [Eigenzeit: konservative C2-Krümmungsintervalle](#lorentz-de-sitter-c2) | MAIN / SOFTWARE | `main` / [e947dfbdd498](https://github.com/thomasmgfeller/x6-spectral-astrolabium/commit/e947dfbdd49890dcb119940548537d1db59272c2) |
| [Eigenzeit: schärfere KL-Krümmungsintervalle](#lorentz-de-sitter-kl) | MAIN / SOFTWARE | `main` / [e947dfbdd498](https://github.com/thomasmgfeller/x6-spectral-astrolabium/commit/e947dfbdd49890dcb119940548537d1db59272c2) |
| [Eigenzeit: analytische Wolkenvarianz und Bennett-Intervalle](#lorentz-de-sitter-variance) | MAIN / SOFTWARE | `main` / [e947dfbdd498](https://github.com/thomasmgfeller/x6-spectral-astrolabium/commit/e947dfbdd49890dcb119940548537d1db59272c2) |
| [Eigenzeit: geglättete BD-Referenz gegen C2](#lorentz-bd-reference) | MAIN / SOFTWARE | `main` / [e947dfbdd498](https://github.com/thomasmgfeller/x6-spectral-astrolabium/commit/e947dfbdd49890dcb119940548537d1db59272c2) |
| [Lokaler d’Alembertian: intrinsischer Phase-1/2-Pilot](#lorentz-local-dalembert) | MAIN / SOFTWARE | `main` / [e947dfbdd498](https://github.com/thomasmgfeller/x6-spectral-astrolabium/commit/e947dfbdd49890dcb119940548537d1db59272c2) |

## Einzelne Module ausführen

Alle Befehle beziehen sich auf den Quellencommit des jeweiligen Moduls. Für einen exakt gepinnten main-Lauf nach dem Klonen `git checkout --detach e947dfbdd49890dcb119940548537d1db59272c2` verwenden. Für Branch-Module folgt jeweils ein eigenes Klonrezept; danach ist der Checkout absichtlich detached. Nicht wahllos zwischen divergierenden Branches wechseln oder deren Versionsinventare mischen.

Archivmodule werden in neue Ordner unter /tmp entpackt. Eine erneute Ausführung benötigt einen neuen Zielnamen. Paketinterne Befehle starten aus dem angegebenen Wurzelordner. Installation externer Abhängigkeiten benötigt Netzwerk oder vorbereitete Wheels; der eigentliche Offline-Replay startet keinen Wolfram-Dienst.

<a id="integration"></a>
### Gemeinsamer lokaler Einstieg

**Stand:** MAIN / SOFTWARE; Branch `main`; Commit `e947dfbdd49890dcb119940548537d1db59272c2`.

**Anleitung:** [aktuelle main-Dokumentation](https://github.com/thomasmgfeller/x6-spectral-astrolabium/blob/main/docs/INTEGRATION.md). **Voraussetzungen:** Linux/POSIX x86-64, Python 3.12, Git, Node >=22; setup installiert gepinntes NumPy/SciPy. Browser für die Oberfläche.

**Geprüfte Aussage:** Installation, Signal/Spektral/RAX-Läufe sowie Export und Replay sind in main integriert. ACVM/C1 besitzen zusätzliche Unterbefehle.

```sh
python3 x6.py setup --profile research
python3 x6.py doctor --profile research
python3 x6.py serve
```

**Erwartung:** doctor: erfolgreich; serve meldet Loopback-URL und bleibt bis Strg+C aktiv.

**Vorhandene Evidenz:**

- [docs/integration-v0.1/evidence/qualification.json](https://github.com/thomasmgfeller/x6-spectral-astrolabium/blob/e947dfbdd49890dcb119940548537d1db59272c2/docs/integration-v0.1/evidence/qualification.json): Historische Abnahme PASS_WITH_BROWSER, 23 Schritte; genaue damalige Revision im Bericht. Kein Nachweis für beliebige spätere Commits.

**Nächste Abnahme:** Frischer Checkout der nächsten Implementierungsrevision: Installation, alle drei Adapter, ZIP-Replay, Negativkontrollen und Browser/CLI-Austausch bestehen.

<a id="offline-reference"></a>
### Gemeinsame Offline-Referenzsuite

**Stand:** MAIN / SOFTWARE; Branch `main`; Commit `e947dfbdd49890dcb119940548537d1db59272c2`.

**Anleitung:** [aktuelle main-Dokumentation](https://github.com/thomasmgfeller/x6-spectral-astrolabium/blob/main/docs/OFFLINE_REFERENCE.md). **Voraussetzungen:** Linux/POSIX x86-64, Python 3.12 und Node.js 24. Nur Standardbibliothek; kein setup, NumPy/SciPy, Netzwerk oder Wolfram-Zugang. Neuer Ausgabeordner.

**Geprüfte Aussage:** Vier unveränderte Wolfram-Archive, fünf rationale Graphfälle, 318 n=6-Ordnungen mit 4.208 exakten Polynomen und aktueller Signal-Lab-Kern gegen die gespeicherte Polaritätsreferenz. Vollständiges quellengebundenes Replay. Frische CI-Checkouts laufen bei relevanten Änderungen mit abgeschaltetem Netzwerk. Endliche Software-/Referenzrechnung, keine physische Abnahme oder externe Begutachtung. Zusätzlich: vier n=6-Restpaare exakt mit Wolfram gegengeprüft; Gradpaar-/Zählseparatoren und n=7/n=8-Grenzfälle lokal reproduzierbar. X6-QE ergänzt drei bekannte exakte Graphreferenzen mit vier Graphen; kein Quanten-, Gedächtnis- oder Arithmetikbefund.

```sh
python3 -S -B x6.py reference qualify --output /tmp/x6-reference-evidence
python3 -S -B x6.py reference verify /tmp/x6-reference-evidence
```

**Erwartung:** Exit 0; PASS_OFFLINE_REFERENCE_REPLAY, 10 Berichte, 27 übergreifende plus 17 Lorentz- und 21 QE-Fehlerkontrollen. Fälschungen einschließlich nachgezogener Hashes scheitern.

**Vorhandene Evidenz:**

- [research/x6_qe/evidence/local-results.json](https://github.com/thomasmgfeller/x6-spectral-astrolabium/blob/e947dfbdd49890dcb119940548537d1db59272c2/research/x6_qe/evidence/local-results.json): X6-QE: lokal ausgeführte exakte Referenzen, vier Graphen, zwölf Umbenennungen, 21 erwartete Zurückweisungen. Quellenhashes im Bericht; keine externe Prüfung.
- [research/lorentz_n6_residuals/ACCEPTANCE.md](https://github.com/thomasmgfeller/x6-spectral-astrolabium/blob/e947dfbdd49890dcb119940548537d1db59272c2/research/lorentz_n6_residuals/ACCEPTANCE.md): Aktuelle Neun-Berichte-Abnahme der Implementierung 5eaffee5a594e2c2c5b86db28a1406dc29168087. Lokal und Netzwerk-isolierte CI PASS, identisches Bundle. Ältere Acht-Berichte-Belege unten gehören zu ihrer historischen Quellenrevision.
- [docs/reference-suite/README.md](https://github.com/thomasmgfeller/x6-spectral-astrolabium/blob/e947dfbdd49890dcb119940548537d1db59272c2/docs/reference-suite/README.md): Ausgeführte Abnahme der Implementierung 7c35b591f77ab1c123ee9795ea6978d1681d59bb. Lokale und Netzwerk-isolierte CI-Abnahme PASS, identische Bundle-Prüfsumme.
- [docs/reference-suite/local/acceptance.json](https://github.com/thomasmgfeller/x6-spectral-astrolabium/blob/e947dfbdd49890dcb119940548537d1db59272c2/docs/reference-suite/local/acceptance.json): Frischer sauberer Checkout ohne .venv/Site-Pakete; elf CLI-Schritte einschließlich zehn erwarteter Zurückweisungen. Historische Prüfrevision explizit gespeichert.
- [docs/reference-suite/local/run/complete.json](https://github.com/thomasmgfeller/x6-spectral-astrolabium/blob/e947dfbdd49890dcb119940548537d1db59272c2/docs/reference-suite/local/run/complete.json): Vollständiges Bundle mit acht Berichten, Quellenhashes und Inventar; durch reference verify erneut berechenbar.
- [docs/reference-suite/ci/acceptance.json](https://github.com/thomasmgfeller/x6-spectral-astrolabium/blob/e947dfbdd49890dcb119940548537d1db59272c2/docs/reference-suite/ci/acceptance.json): GitHub-Lauf 38720405798: network_namespace_isolated=true, alle elf CLI-Schritte wie erwartet.

**Nächste Abnahme:** Bei jeder relevanten Änderung frischen Checkout mit unverändertem Prüfvertrag qualifizieren und neue Evidenzrevision festhalten. Neue Fälle oder größere Korpora benötigen eigene Erwartungen und Fehlerkontrollen; andere Plattformen sind separat zu qualifizieren.

<a id="astrolabium"></a>
### Astrolabium und rationale Spektralreferenz

**Stand:** MAIN / SOFTWARE; Branch `main`; Commit `e947dfbdd49890dcb119940548537d1db59272c2`.

**Anleitung:** [aktuelle main-Dokumentation](https://github.com/thomasmgfeller/x6-spectral-astrolabium/blob/main/docs/SCIENTIFIC_SCOPE.md). **Voraussetzungen:** Python 3.12; gemeinsames setup --profile core. Browser-App: app/index.html.

**Geprüfte Aussage:** Fünf rationale Referenzfälle prüfen strikte Untergrenzen für endliche gerundete Graph-Laplacians, einschliesslich ungültiger Schranken und getrennter Komponenten.

```sh
python3 x6.py run spectral --output runs/register-spectral
python3 x6.py verify runs/register-spectral
```

**Erwartung:** Exit 0; nur die unten genannte Softwareaussage.

**Vorhandene Evidenz:**

- [docs/integration-v0.1/evidence/spectral-run.log](https://github.com/thomasmgfeller/x6-spectral-astrolabium/blob/e947dfbdd49890dcb119940548537d1db59272c2/docs/integration-v0.1/evidence/spectral-run.log): Erhaltene Referenzausführung; keine physische oder allgemeine Raumzeitaussage.
- [evidence/historical_python_results.json](https://github.com/thomasmgfeller/x6-spectral-astrolabium/blob/e947dfbdd49890dcb119940548537d1db59272c2/evidence/historical_python_results.json): Historischer Python-Befund; datierter Prüfstand.

**Nächste Abnahme:** Externe Reproduktion der exakten Zertifikate und separat vollständige Browser-/Julia-Qualifikation.

<a id="signal-lab"></a>
### Signal Validation Lab

**Stand:** MAIN / SOFTWARE; Branch `main`; Commit `e947dfbdd49890dcb119940548537d1db59272c2`.

**Anleitung:** [aktuelle main-Dokumentation](https://github.com/thomasmgfeller/x6-spectral-astrolabium/blob/main/docs/SIGNAL_VALIDATION_LAB.md). **Voraussetzungen:** Python 3.12, Node >=22; setup --profile core. UI: app/signal-lab.html.

**Geprüfte Aussage:** Synthetische Signale werden gegen vier Verfahren verglichen; Roharrays und Qualitätsurteile bleiben im Replay erhalten.

```sh
python3 x6.py run signal --output runs/register-signal
python3 x6.py verify runs/register-signal
```

**Erwartung:** Exit 0; nur die unten genannte Softwareaussage.

**Vorhandene Evidenz:**

- [docs/integration-v0.1/evidence/signal-run.log](https://github.com/thomasmgfeller/x6-spectral-astrolabium/blob/e947dfbdd49890dcb119940548537d1db59272c2/docs/integration-v0.1/evidence/signal-run.log): Erhaltenes Pulsbeispiel: X6-Phasenfilter FAIL ist ein fachliches Ergebnis, kein Laufabbruch.
- [docs/perspectives/edge-platform/evidence/independent-reference.json](https://github.com/thomasmgfeller/x6-spectral-astrolabium/blob/e947dfbdd49890dcb119940548537d1db59272c2/docs/perspectives/edge-platform/evidence/independent-reference.json): Gespeicherte NumPy/SciPy-Gegenprüfung.

**Nächste Abnahme:** Vor Leistungsclaims: starke Baselines, getrennte reale Testdaten, ereigniserhaltende Qualitätsgates und Ressourcenmessung.

<a id="edge-reference"></a>
### Edge-Referenzadapter

**Stand:** MAIN / SOFTWARE; Branch `main`; Commit `e947dfbdd49890dcb119940548537d1db59272c2`.

**Anleitung:** [aktuelle main-Dokumentation](https://github.com/thomasmgfeller/x6-spectral-astrolabium/blob/main/experimental/edge_reference/README.md). **Voraussetzungen:** Node >=22; keine npm-Laufzeitabhängigkeiten.

**Geprüfte Aussage:** Begrenzter lokaler Signalauftrag mit Export und rechnerischem Replay; main enthält den Adapter bereits.

```sh
node experimental/edge_reference/runner.cjs run experimental/edge_reference/examples/synthetic-signal.json runs/register-edge
node experimental/edge_reference/runner.cjs verify runs/register-edge
```

**Erwartung:** Exit 0; nur die unten genannte Softwareaussage.

**Vorhandene Evidenz:**

- [docs/perspectives/edge-platform/evidence/local-validation.json](https://github.com/thomasmgfeller/x6-spectral-astrolabium/blob/e947dfbdd49890dcb119940548537d1db59272c2/docs/perspectives/edge-platform/evidence/local-validation.json): Lokale Softwareprüfung; keine Messung von Geräteeffizienz.

**Nächste Abnahme:** Zweite unabhängige Anwendung, qualifizierter Geräteadapter und ARM64/x86-64-Vergleich nach Roadmap.

<a id="evidence-calibration"></a>
### Evidence & Calibration

**Stand:** MAIN / SOFTWARE; Branch `main`; Commit `e947dfbdd49890dcb119940548537d1db59272c2`.

**Anleitung:** [aktuelle main-Dokumentation](https://github.com/thomasmgfeller/x6-spectral-astrolabium/blob/main/experimental/evidence_calibration/README.md). **Voraussetzungen:** Python 3.12/3.13, Standardbibliothek.

**Geprüfte Aussage:** Datentypen, Evidenzbindung, Bildmetadaten und klassische Referenzmodelle werden softwareseitig geprüft; Hashes authentifizieren keine Messung.

```sh
python3 -m experimental.evidence_calibration.run_qualification --output runs/register-calibration --protect-research
```

**Erwartung:** Exit 0; nur die unten genannte Softwareaussage.

**Vorhandene Evidenz:**

- [experimental/evidence_calibration/REMEDIATION.md](https://github.com/thomasmgfeller/x6-spectral-astrolabium/blob/e947dfbdd49890dcb119940548537d1db59272c2/experimental/evidence_calibration/REMEDIATION.md): Audit-/Fehlerbehandlung und Testzuordnung. Ein erneuter Lauf erzeugt eigene Logs; kein gespeicherter physischer Qualifikationsbefund.

**Nächste Abnahme:** Kontrollierte aufgezeichnete Messdaten, Dunkel-/Sättigungsprüfung, kalibrierter Massstab und vollständiges Unsicherheitsbudget.

<a id="phase-contract"></a>
### X6-Phasenfilter: Experimentvertrag

**Stand:** MAIN / SOFTWARE; Branch `main`; Commit `e947dfbdd49890dcb119940548537d1db59272c2`.

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

- [experiments/x6-phase-filter/contract-v0.2.0/validation_report.json](https://github.com/thomasmgfeller/x6-spectral-astrolabium/blob/e947dfbdd49890dcb119940548537d1db59272c2/experiments/x6-phase-filter/contract-v0.2.0/validation_report.json): 42 Softwaretests; keine neuen Filterversuche.

**Nächste Abnahme:** Offene fachliche Festlegungen und vertrauenswürdigen Freeze schliessen; danach Runner-Review.

<a id="industrial-programme"></a>
### Industrielle Entrauschung: Forschungsprogramm v0.2

**Stand:** MAIN / CONCEPT; Branch `main`; Commit `e947dfbdd49890dcb119940548537d1db59272c2`.

**Anleitung:** [aktuelle main-Dokumentation](https://github.com/thomasmgfeller/x6-spectral-astrolabium/blob/main/docs/industrial-denoising/Astrolabium_Industrial_Denoising_Forschungsprogramm_v0_2.docx). **Voraussetzungen:** DOCX-Leser. In main ausführbar: industrial-v1 (Bestätigungsvertrag) und industrial-pilot (begrenzter nichtkommerzieller Labor-Datenpilot).

**Geprüfte Aussage:** Forschungsplan für Diagnosequalität, Ereigniserhalt und Ressourcenbudgets; keine nachgewiesene neue Filterleistung.

**Erwartung:** Kein ausführbarer Kern in diesem Dokument.

**Vorhandene Evidenz:**

- [docs/industrial-denoising/Astrolabium_Industrial_Denoising_Forschungsprogramm_v0_2.docx](https://github.com/thomasmgfeller/x6-spectral-astrolabium/blob/e947dfbdd49890dcb119940548537d1db59272c2/docs/industrial-denoising/Astrolabium_Industrial_Denoising_Forschungsprogramm_v0_2.docx): Veröffentlichter Forschungsplan; kein abgeschlossener Industrieversuch.

**Nächste Abnahme:** Nach dem abgeschlossenen begrenzten Paderborn-Piloten: konkrete industrielle Zielpopulation und passende Datenrechte, Kalibrierung, unabhängige Referenzlabels, externe Splits und fachlich geprüfte Powerplanung für die Bestätigung. Keine Filterfreigabe allein aus Pilotzählungen.

<a id="sagnac-import"></a>
### Sagnac-Aufnahme und Import

**Stand:** MAIN / SOFTWARE; Branch `main`; Commit `e947dfbdd49890dcb119940548537d1db59272c2`.

**Anleitung:** [aktuelle main-Dokumentation](https://github.com/thomasmgfeller/x6-spectral-astrolabium/blob/main/docs/SAGNAC_INTEGRATION.md). **Voraussetzungen:** Python 3.12, Browser; Standardstart ohne angeschlossenes Gerät.

**Geprüfte Aussage:** SGNCv007-Decoder, synthetischer Import und Loopback-Bridge; optische Stellbefehle gehören zum separaten ACVM-Modul.

```sh
python3 device/sagnac_bridge.py
```

**Erwartung:** http://127.0.0.1:8766/app/; Tab 07 Sagnac, synthetisches Beispiel. Server endet mit Strg+C.

**Vorhandene Evidenz:**

- [evidence/sagnac_integration_validation.json](https://github.com/thomasmgfeller/x6-spectral-astrolabium/blob/e947dfbdd49890dcb119940548537d1db59272c2/evidence/sagnac_integration_validation.json): Gespeicherte Softwarevalidierung des Integrationsstands; keine Hardwaremessung.

**Nächste Abnahme:** Reale serielle Aufnahme und Zähler-/Zeitkalibrierung mit unabhängiger Referenz; optische Claims separat prüfen.

<a id="photonic-design"></a>
### Photonischer Zwei-Qubit-Aufbau und Jig

**Stand:** MAIN / SOFTWARE; Branch `main`; Commit `e947dfbdd49890dcb119940548537d1db59272c2`.

**Anleitung:** [aktuelle main-Dokumentation](https://github.com/thomasmgfeller/x6-spectral-astrolabium/blob/main/experiments/photonic-two-qubit/REPRODUCE.md). **Voraussetzungen:** Python 3.12, GHDL 5.0.1 mcode und CAD-Abhängigkeiten aus requirements; keine Hardware nötig.

**Geprüfte Aussage:** Host-/RTL-Referenz und idealisierte Jig-Geometrie werden geprüft. Ausgelassene optionale Prüfungen sind NOT_EXECUTED.

```sh
python3 -m pip install -r tests/photonics/requirements.txt
python3 tests/photonics/validate_release.py --ghdl --cad --output runs/register-photonic
```

**Erwartung:** Exit 0; nur die unten genannte Softwareaussage.

**Vorhandene Evidenz:**

- [experiments/photonic-two-qubit/SCIENTIFIC_STATUS.md](https://github.com/thomasmgfeller/x6-spectral-astrolabium/blob/e947dfbdd49890dcb119940548537d1db59272c2/experiments/photonic-two-qubit/SCIENTIFIC_STATUS.md): Designstatus und Grenzen; physische Fertigungs-/Verschränkungsnachweise offen.
- [experiments/photonic-two-qubit/reference/sagnac_v0_7/VALIDATION.md](https://github.com/thomasmgfeller/x6-spectral-astrolabium/blob/e947dfbdd49890dcb119940548537d1db59272c2/experiments/photonic-two-qubit/reference/sagnac_v0_7/VALIDATION.md): Erhaltener digitaler Referenzbericht.

**Nächste Abnahme:** Jig fertigen und vermessen; Quelle/Detektoren kalibrieren; vorregistrierte Koinzidenz-/Verschränkungsprüfung nach LAB_PROTOCOL.

<a id="acvm-concept"></a>
### ACVM: Grundkonzept 0.1

**Stand:** MAIN / CONCEPT; Branch `main`; Commit `e947dfbdd49890dcb119940548537d1db59272c2`.

**Anleitung:** [aktuelle main-Dokumentation](https://github.com/thomasmgfeller/x6-spectral-astrolabium/blob/main/docs/acvm/README.md). **Voraussetzungen:** Markdown-/DOCX-Leser; ausführbare C1-/0.2-Module siehe eigene Einträge.

**Geprüfte Aussage:** Historische Gesamtspezifikation. Teilimplementierungen in main ersetzen keine vollständige Geräteabnahme.

**Erwartung:** Dokument lesen; keine eigenständige ausführbare Gesamtspezifikation.

**Vorhandene Evidenz:**

- [docs/acvm/ACVM_CONCEPT_v0_1_DE.md](https://github.com/thomasmgfeller/x6-spectral-astrolabium/blob/e947dfbdd49890dcb119940548537d1db59272c2/docs/acvm/ACVM_CONCEPT_v0_1_DE.md): Ursprünglicher Anforderungstext; spätere Softwarebelege in C1 und optical-v0.2.

**Nächste Abnahme:** Anforderungen mit den Teilimplementierungen verknüpfen und verbleibende elektrische/optische Abnahmen durchführen.

<a id="acvm-c1"></a>
### ACVM C1: Steuerkanal

**Stand:** MAIN / SOFTWARE; Branch `main`; Commit `e947dfbdd49890dcb119940548537d1db59272c2`.

**Anleitung:** [aktuelle main-Dokumentation](https://github.com/thomasmgfeller/x6-spectral-astrolabium/blob/main/docs/acvm/control-channel-v0.1/README.md). **Voraussetzungen:** Softwarequalifikation: Python 3.12, POSIX-PTY, g++/C++17; kein Pico erforderlich. Optionaler Zielbuild: Linux x86-64 und gepinnte Werkzeuge gemäß docs/acvm/c1-e01-target-build/README.md. Physische E01-Abnahme benötigt einen identifizierten Pico/MCP4921-Aufbau und unabhängige kalibrierte Messgeräte.

**Geprüfte Aussage:** Host-Protokoll, Compiler, portabler C++-Sequencer und virtueller serieller Weg sind prüfbar. Unveränderte Firmware wurde für RP2040 gebaut; wiederholte Builds ergeben identische UF2-/BIN-Hashes. Keine physische Ausgabe oder Fehlerreaktion gemessen.

```sh
python3 x6.py control qualify --output runs/register-c1
python3 -B tests/control-channel/test_pico_build.py
```

**Erwartung:** Softwarequalifikation Exit 0; UF2-Kandidat stimmt mit BIN überein, fünf Beschädigungsfälle werden abgelehnt und vorhandene Ergebnisordner bleiben geschützt. Der dokumentierte Zielbuild ergibt TARGET_BUILD_PASS; elektrische Abnahme bleibt NOT_PERFORMED.

**Vorhandene Evidenz:**

- [docs/acvm/control-channel-v0.1/evidence/qualification.json](https://github.com/thomasmgfeller/x6-spectral-astrolabium/blob/e947dfbdd49890dcb119940548537d1db59272c2/docs/acvm/control-channel-v0.1/evidence/qualification.json): Gespeicherte Softwarequalifikation; kein Pico-Build oder elektrischer Messbeleg.
- [docs/acvm/c1-e01-target-build/evidence/build-report.json](https://github.com/thomasmgfeller/x6-spectral-astrolabium/blob/e947dfbdd49890dcb119940548537d1db59272c2/docs/acvm/c1-e01-target-build/evidence/build-report.json): Tatsächlicher RP2040-Zielbuild PASS; Pico SDK 2.3.1/GNU Arm GCC 15.2.1, Firmware-, Werkzeug- und Ausgabehashes. UF2/BIN/ELF und Buildlogs archiviert; kein Flash- oder Messbeleg.
- [docs/acvm/c1-e01-target-build/evidence/readiness.json](https://github.com/thomasmgfeller/x6-spectral-astrolabium/blob/e947dfbdd49890dcb119940548537d1db59272c2/docs/acvm/c1-e01-target-build/evidence/readiness.json): BLOCKED_PHYSICAL_MEASUREMENT: 0/10 Normalläufe und 0/6 Fehlerfälle; reale Geräte, Kalibrierung, vorher fixiertes Messprofil und unabhängige Rohaufnahmen fehlen.

**Nächste Abnahme:** Identifizierten Aufbau flashen; E01-Messprofil vor Datenerhebung fixieren; mindestens zehn Stellfolgen sowie sechs Fehlerfälle unabhängig erfassen. Spannungsfehler plus U95 ≤25 mV, Zeitfehler plus U95 ≤20 ms, Hostverlustreaktion plus U95 ≤550 ms gemäß E01. Vollständige Rohdaten, Kalibrierung und Fehlergrenzen archivieren; anschließend erst elektrische und später optische Abnahme entscheiden.

<a id="acvm-optical"></a>
### ACVM 0.2: optischer Referenzablauf

**Stand:** MAIN / SOFTWARE; Branch `main`; Commit `e947dfbdd49890dcb119940548537d1db59272c2`.

**Anleitung:** [aktuelle main-Dokumentation](https://github.com/thomasmgfeller/x6-spectral-astrolabium/blob/main/docs/acvm/optical-v0.2/README.md). **Voraussetzungen:** Python 3.12, POSIX-PTY, g++; Softwarelauf ohne Geräte.

**Geprüfte Aussage:** V01–V08 MODEL_PASS, synthetische QHQ-/Drift-/Regelkontrollen; ELL14-/PM100D-Adapter sind implementiert, nicht gerätequalifiziert.

```sh
python3 x6.py acvm qualify --output runs/register-acvm
```

**Erwartung:** Exit 0; nur die unten genannte Softwareaussage.

**Vorhandene Evidenz:**

- [docs/acvm/optical-v0.2/evidence/fresh-checkout/fresh-checkout.json](https://github.com/thomasmgfeller/x6-spectral-astrolabium/blob/e947dfbdd49890dcb119940548537d1db59272c2/docs/acvm/optical-v0.2/evidence/fresh-checkout/fresh-checkout.json): 12 Checkout-Schritte; genaue geprüfte lokale Revision und Logs.
- [docs/acvm/optical-v0.2/VALIDATION.md](https://github.com/thomasmgfeller/x6-spectral-astrolabium/blob/e947dfbdd49890dcb119940548537d1db59272c2/docs/acvm/optical-v0.2/VALIDATION.md): V09/V10 physisch NOT_PERFORMED; Regelvorteil nur im angegebenen Modell.

**Nächste Abnahme:** V09/V10 mit unabhängigen Messungen; Geräteidentität/Kalibrierung, reale Hysterese/Laufzeiten und geschlossenen optischen Regelkreis nachweisen.

<a id="sagnac-components"></a>
### Sagnac-Komponenten und Ofen

**Stand:** MAIN / CONCEPT; Branch `main`; Commit `e947dfbdd49890dcb119940548537d1db59272c2`.

**Anleitung:** [aktuelle main-Dokumentation](https://github.com/thomasmgfeller/x6-spectral-astrolabium/blob/main/docs/acvm/sagnac-components-v0.1/README.md). **Voraussetzungen:** Dokument-/PDF-Leser.

**Geprüfte Aussage:** Beschaffungs- und Aufbauprofil für ppKTP, gemeinsamen Dreiecksloop und Temperaturführung.

**Erwartung:** Kein ausführbarer oder gemessener Aufbau.

**Vorhandene Evidenz:**

- [docs/acvm/sagnac-components-v0.1/README.md](https://github.com/thomasmgfeller/x6-spectral-astrolabium/blob/e947dfbdd49890dcb119940548537d1db59272c2/docs/acvm/sagnac-components-v0.1/README.md): Zwölf Abnahmeschritte ungetestet; keine Lieferantenbestätigung.

**Nächste Abnahme:** Lieferantenspezifikation und Fertigungsfreigabe einholen; zwölf Komponenten-/Aufbauprüfungen tatsächlich ausführen.

<a id="acvm-records"></a>
### ACVM Experiment Records

**Stand:** MAIN / CONCEPT; Branch `main`; Commit `e947dfbdd49890dcb119940548537d1db59272c2`.

**Anleitung:** [aktuelle main-Dokumentation](https://github.com/thomasmgfeller/x6-spectral-astrolabium/blob/main/docs/acvm/experiment-records/README.md). **Voraussetzungen:** Markdown-/DOCX-Leser.

**Geprüfte Aussage:** Vorgeschlagenes Run-Archive-Datenmodell mit Provenienz und Abnahmeplan; nicht gleich dem bereits begrenzten CLI-Export.

**Erwartung:** Kein eigenständiger Records-Runner.

**Vorhandene Evidenz:**

- [docs/acvm/experiment-records/README.md](https://github.com/thomasmgfeller/x6-spectral-astrolabium/blob/e947dfbdd49890dcb119940548537d1db59272c2/docs/acvm/experiment-records/README.md): Vierzehn Records-Prüfungen NOT_RUN.

**Nächste Abnahme:** Versionierten Writer/Reader und Adapter implementieren; alle vierzehn Records-Gates mit Manipulations-/Abbruchfällen prüfen.

<a id="acvm-fixture"></a>
### ACVM Electrical & Thermal Test Fixture

**Stand:** MAIN / CONCEPT; Branch `main`; Commit `e947dfbdd49890dcb119940548537d1db59272c2`.

**Anleitung:** [aktuelle main-Dokumentation](https://github.com/thomasmgfeller/x6-spectral-astrolabium/blob/main/docs/acvm/electrical-thermal-fixture/README.md). **Voraussetzungen:** Dokument-/Bildbetrachter.

**Geprüfte Aussage:** Elektrischer/thermischer Prüfstand und QD-01 sind Konzeptdarstellungen; Illustrationen sind keine gefertigten Chips.

**Erwartung:** Kein qualifizierter Prüfstand und kein ausführbarer Chip.

**Vorhandene Evidenz:**

- [docs/acvm/electrical-thermal-fixture/README.md](https://github.com/thomasmgfeller/x6-spectral-astrolabium/blob/e947dfbdd49890dcb119940548537d1db59272c2/docs/acvm/electrical-thermal-fixture/README.md): ETF-T01–ETF-T14 NOT_RUN.

**Nächste Abnahme:** Anforderungen, Bauteile und Messunsicherheit freigeben; Prüfstand aufbauen und ETF-T01–T14 messen.

<a id="rax-programme"></a>
### RAX: relationales Forschungsprogramm

**Stand:** MAIN / CONCEPT; Branch `main`; Commit `e947dfbdd49890dcb119940548537d1db59272c2`.

**Anleitung:** [aktuelle main-Dokumentation](https://github.com/thomasmgfeller/x6-spectral-astrolabium/blob/main/docs/research/rax/README.md). **Voraussetzungen:** DOCX-/Markdown-Leser; ausführbare U1/B1/M1/W1-Pakete separat.

**Geprüfte Aussage:** Gestuftes Programm für prädiktive Reduktionen; U2, Geometrie und Singularitäten bleiben geplant.

**Erwartung:** Kein universeller RAX-Entdeckungsrunner.

**Vorhandene Evidenz:**

- [docs/research/rax/README.md](https://github.com/thomasmgfeller/x6-spectral-astrolabium/blob/e947dfbdd49890dcb119940548537d1db59272c2/docs/research/rax/README.md): Programmbeschreibung und Links zu begrenzten ausgeführten Kontrollen.

**Nächste Abnahme:** U2 mit heterogenen Generatoren, festem Beobachtungsziel, Holdout und eigenem Fehlerbudget vorregistrieren.

<a id="rax-u1"></a>
### RAX-U1: Reduktionskontrolle

**Stand:** MAIN / SOFTWARE; Branch `main`; Commit `e947dfbdd49890dcb119940548537d1db59272c2`.

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

- [docs/research/rax/countercheck-v0.1/RAX_U1_Gegenpruefung_v0_1_Paket.zip](https://github.com/thomasmgfeller/x6-spectral-astrolabium/blob/e947dfbdd49890dcb119940548537d1db59272c2/docs/research/rax/countercheck-v0.1/RAX_U1_Gegenpruefung_v0_1_Paket.zip): Originalquellen, Rohdaten, audit-final und Gegenproben im Paket.

**Nächste Abnahme:** Dauerhafte Speicherung mit Flush/fsync, Reopen/Hashprüfung sowie Abbruch-/Kürzungs-/Neustarttests qualifizieren.

<a id="rax-b1-m1"></a>
### RAX-B1/M1: Benchmark und Methodenreview

**Stand:** MAIN / SOFTWARE; Branch `main`; Commit `e947dfbdd49890dcb119940548537d1db59272c2`.

**Anleitung:** [aktuelle main-Dokumentation](https://github.com/thomasmgfeller/x6-spectral-astrolabium/blob/main/docs/research/rax/method-review-v0.1/README.md). **Voraussetzungen:** setup --profile research; Python 3.12, NumPy/SciPy. Der Replay kann mehrere Minuten dauern.

**Geprüfte Aussage:** 67.584 Benchmarkläufe und Methoden-Gegenbeispiele werden nachgerechnet. Alle acht primären Überlegenheitsentscheidungen bleiben INCONCLUSIVE.

```sh
python3 x6.py run rax --output runs/register-rax
python3 x6.py verify runs/register-rax
```

**Erwartung:** Exit 0; nur die unten genannte Softwareaussage.

**Vorhandene Evidenz:**

- [docs/research/rax/benchmark-v0.1/RAX_B1_Benchmarking_v0_1_Paket.zip](https://github.com/thomasmgfeller/x6-spectral-astrolabium/blob/e947dfbdd49890dcb119940548537d1db59272c2/docs/research/rax/benchmark-v0.1/RAX_B1_Benchmarking_v0_1_Paket.zip): Eingefrorene B1-Daten und Referenzprüfer.
- [docs/research/rax/method-review-v0.1/RAX_M1_Methodenpruefung_v0_1_Paket.zip](https://github.com/thomasmgfeller/x6-spectral-astrolabium/blob/e947dfbdd49890dcb119940548537d1db59272c2/docs/research/rax/method-review-v0.1/RAX_M1_Methodenpruefung_v0_1_Paket.zip): Zwei nachgewiesene Validierungsfehler und Zusatzguards; ursprüngliche Daten bestehen Nachprüfung.

**Nächste Abnahme:** Historische Quellen bleiben unverändert. Neuer deklarativer RAX-G1-Runner mit 33 Angriffskontrollen im Modul rax-guarded; unabhängige personelle Wiederholung und allgemeine Isolation fremden Python-Codes bleiben offen.

<a id="rax-w1"></a>
### RAX-W1: exakte Wolfram-Gegenprüfung

**Stand:** MAIN / SOFTWARE; Branch `main`; Commit `e947dfbdd49890dcb119940548537d1db59272c2`.

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

- [docs/research/rax/wolfram-check-v0.1/RAX_W1_Exakte_Gegenpruefung_v0_1_Paket.zip](https://github.com/thomasmgfeller/x6-spectral-astrolabium/blob/e947dfbdd49890dcb119940548537d1db59272c2/docs/research/rax/wolfram-check-v0.1/RAX_W1_Exakte_Gegenpruefung_v0_1_Paket.zip): Gespeicherte Wolfram-Antworten und unabhängiger Python-Prüfer; interne Post-hoc-Prüfung.

**Nächste Abnahme:** Externe Reproduktion bzw. neuer Wolfram-Lauf mit eigener Umgebung; Aussagebereich nicht auf U2 ausdehnen.

<a id="wolfram-polarity"></a>
### Wolfram Fall 2: Polaritätsumkehr

**Stand:** MAIN / SOFTWARE; Branch `main`; Commit `e947dfbdd49890dcb119940548537d1db59272c2`.

**Anleitung:** [aktuelle main-Dokumentation](https://github.com/thomasmgfeller/x6-spectral-astrolabium/blob/main/docs/signal-lab/wolfram-polarity-v0.1/README.md). **Voraussetzungen:** Python 3.12/Standardbibliothek; Fall 2 mit --rerun zusätzlich Node. Kein frischer Wolfram-Lauf.

**Geprüfte Aussage:** Vier symbolische Identitäten und zwölf numerische Prüfungen; invertiertes Signal wird trotz gleicher PSD/Kohärenz zurückgewiesen.

```sh
python3 -m zipfile -e docs/signal-lab/wolfram-polarity-v0.1/X6_Wolfram_Fall2_v0_1.zip /tmp/x6-register-wolfram-polarity
cd /tmp/x6-register-wolfram-polarity/X6_Wolfram_Fall2_v0_1
python3 verify.py --rerun
```

**Erwartung:** PASS_WITH_SCOPE_LIMITS oder erfolgreicher paketabhängiger Prüfbericht; Exit 0. Wissenschaftliche Aussage bleibt auf den konstruierten Fall begrenzt.

**Vorhandene Evidenz:**

- [docs/signal-lab/wolfram-polarity-v0.1/X6_Wolfram_Fall2_v0_1.zip](https://github.com/thomasmgfeller/x6-spectral-astrolabium/blob/e947dfbdd49890dcb119940548537d1db59272c2/docs/signal-lab/wolfram-polarity-v0.1/X6_Wolfram_Fall2_v0_1.zip): Gespeicherte Erstfehler und korrigierte Wolfram-Antworten, Freeze-Dateien und vollständiges Inventar.

**Nächste Abnahme:** Externe Wiederholung; reale Signale benötigen einen eigenen Messvertrag.

<a id="wolfram-dependence"></a>
### Wolfram Fall 4: Nullfehler und Abhängigkeit

**Stand:** MAIN / SOFTWARE; Branch `main`; Commit `e947dfbdd49890dcb119940548537d1db59272c2`.

**Anleitung:** [aktuelle main-Dokumentation](https://github.com/thomasmgfeller/x6-spectral-astrolabium/blob/main/docs/signal-lab/wolfram-zero-failures-v0.1/README.md). **Voraussetzungen:** Python 3.12/Standardbibliothek; Fall 2 mit --rerun zusätzlich Node. Kein frischer Wolfram-Lauf.

**Geprüfte Aussage:** Zwölf Wolfram-Prüfungen und sieben Python-Vergleiche: unabhängige Versuche und Kopien eines Versuchs haben unterschiedliche Deckung.

```sh
python3 -m zipfile -e docs/signal-lab/wolfram-zero-failures-v0.1/X6_Wolfram_Fall4_v0_1.zip /tmp/x6-register-wolfram-dependence
cd /tmp/x6-register-wolfram-dependence/X6_Wolfram_Fall4_v0_1
python3 verify.py
```

**Erwartung:** PASS_WITH_SCOPE_LIMITS oder erfolgreicher paketabhängiger Prüfbericht; Exit 0. Wissenschaftliche Aussage bleibt auf den konstruierten Fall begrenzt.

**Vorhandene Evidenz:**

- [docs/signal-lab/wolfram-zero-failures-v0.1/X6_Wolfram_Fall4_v0_1.zip](https://github.com/thomasmgfeller/x6-spectral-astrolabium/blob/e947dfbdd49890dcb119940548537d1db59272c2/docs/signal-lab/wolfram-zero-failures-v0.1/X6_Wolfram_Fall4_v0_1.zip): Gespeicherte Erstfehler und korrigierte Wolfram-Antworten, Freeze-Dateien und vollständiges Inventar.

**Nächste Abnahme:** Unabhängigkeit konkreter Datensätze belegen; das konstruktive Gegenbeispiel ist kein Audit aller Projektdaten.

<a id="wolfram-causal"></a>
### Wolfram Fall 5: Kausalordnung

**Stand:** MAIN / SOFTWARE; Branch `main`; Commit `e947dfbdd49890dcb119940548537d1db59272c2`.

**Anleitung:** [aktuelle main-Dokumentation](https://github.com/thomasmgfeller/x6-spectral-astrolabium/blob/main/docs/research/causal-order/wolfram-countercheck-v0.1/README.md). **Voraussetzungen:** Python 3.12/Standardbibliothek; Fall 2 mit --rerun zusätzlich Node. Kein frischer Wolfram-Lauf.

**Geprüfte Aussage:** Sechzehn Wolfram-Assertions und exakte Python-Polynome bestätigen ein Drei-Ereignis-Gegenbeispiel gegen Vollständigkeit dieses Fingerprints.

```sh
python3 -m zipfile -e docs/research/causal-order/wolfram-countercheck-v0.1/X6_Wolfram_Fall5_v0_1.zip /tmp/x6-register-wolfram-causal
cd /tmp/x6-register-wolfram-causal/X6_Wolfram_Fall5_v0_1
python3 verify_release.py
```

**Erwartung:** PASS_WITH_SCOPE_LIMITS oder erfolgreicher paketabhängiger Prüfbericht; Exit 0. Wissenschaftliche Aussage bleibt auf den konstruierten Fall begrenzt.

**Vorhandene Evidenz:**

- [docs/research/causal-order/wolfram-countercheck-v0.1/X6_Wolfram_Fall5_v0_1.zip](https://github.com/thomasmgfeller/x6-spectral-astrolabium/blob/e947dfbdd49890dcb119940548537d1db59272c2/docs/research/causal-order/wolfram-countercheck-v0.1/X6_Wolfram_Fall5_v0_1.zip): Gespeicherte Erstfehler und korrigierte Wolfram-Antworten, Freeze-Dateien und vollständiges Inventar.

**Nächste Abnahme:** Zusätzliche Invarianten an registrierten Korpora prüfen; kein allgemeiner Rekonstruktionssatz.

<a id="data-agents"></a>
### Öffentliche Datenagenten: NOAA, Atlas, QuTech, NASA

**Stand:** MAIN / SOFTWARE; Branch `main`; Commit `e947dfbdd49890dcb119940548537d1db59272c2`.

**Anleitung:** [aktuelle main-Dokumentation](https://github.com/thomasmgfeller/x6-spectral-astrolabium/blob/main/docs/SOURCE_AGENTS.md). **Voraussetzungen:** Lokale Tests: Abhängigkeiten aus agent/requirements.txt und agent/source-requirements.txt; siehe Dokumentation. Produktionsläufe nutzen geschützte GitHub-Workflows und deren Zeitfenster.

**Geprüfte Aussage:** Quellen-/Ablehnungsprüfungen und App-Checks auf öffentlichen Daten. Vier Datenjobs in zwei Workflows; kein Denoising-Nutzenbeleg.

```sh
python3 -m unittest tests/python/test_data_agent.py tests/python/test_source_agents.py -v
```

**Erwartung:** Lokale Softwaretests; kein neuer Datenabruf. Tatsächliche geplante Läufe siehe datierte Workflow-Links im Register.

**Vorhandene Evidenz:**

- [docs/DATA_AGENT.md](https://github.com/thomasmgfeller/x6-spectral-astrolabium/blob/e947dfbdd49890dcb119940548537d1db59272c2/docs/DATA_AGENT.md): NOAA-Lauf, Inputs und Actions-Artefakte 30 Tage.
- [docs/SOURCE_AGENTS.md](https://github.com/thomasmgfeller/x6-spectral-astrolabium/blob/e947dfbdd49890dcb119940548537d1db59272c2/docs/SOURCE_AGENTS.md): Atlas/QuTech/NASA-Artefakte 14 Tage; Archivdaten explizit gekennzeichnet.
- [docs/AGENT_WINDOW_REPAIR_2026_10_13.md](https://github.com/thomasmgfeller/x6-spectral-astrolabium/blob/e947dfbdd49890dcb119940548537d1db59272c2/docs/AGENT_WINDOW_REPAIR_2026_10_13.md): Dokumentierte Fenster- und Schutzprüfungen.
- [docs/agent-archive/2026-10-15/ARCHIVE.json](https://github.com/thomasmgfeller/x6-spectral-astrolabium/blob/e947dfbdd49890dcb119940548537d1db59272c2/docs/agent-archive/2026-10-15/ARCHIVE.json): Drei ausgewählte Originalartefakte dauerhaft in Git: Mathematik/Lorentz, Graphatlas, NOAA; GitHub-Digests, innere Inventare und historische Quellhashes geprüft. Nicht alle Läufe archiviert.

**Nächste Abnahme:** Nach diesem Archiv-Snapshot entstehende oder bislang nicht ausgewählte Belege separat vor Ablauf sichern; unabhängiger Datensatz-/Drift- und Qualitätsvergleich. Nach Frist STOPPED erwarten.

<a id="lorentz-agent"></a>
### Begrenzter Mathematikagent: Lorentz n=3–5 und Propagator

**Stand:** MAIN / SOFTWARE; Branch `main`; Commit `e947dfbdd49890dcb119940548537d1db59272c2`.

**Anleitung:** [aktuelle main-Dokumentation](https://github.com/thomasmgfeller/x6-spectral-astrolabium/blob/main/docs/MATH_AGENT.md). **Voraussetzungen:** Python 3.12, Node >=22 und gepinnte mathematische Abhängigkeiten.

**Geprüfte Aussage:** Endliche Ordnungszählung und 1+1-Diamond-Spektralvergleich; Replikation/Kalibrierung, kein neuer Satz.

```sh
python3 -m pip install -r agent/math-requirements.txt
python3 -m unittest tests/python/test_math_agent.py tests/python/test_lorentz_spectral.py -v
```

**Erwartung:** Exit 0 bei bestandenen Regressionen; startet keinen geplanten Forschungslauf.

**Vorhandene Evidenz:**

- [docs/LORENTZ_RESEARCH.md](https://github.com/thomasmgfeller/x6-spectral-astrolabium/blob/e947dfbdd49890dcb119940548537d1db59272c2/docs/LORENTZ_RESEARCH.md): Definierte Referenzen, n=3/4/5-Zielzählungen und Grenzen.
- [agent/math-agent-config.json](https://github.com/thomasmgfeller/x6-spectral-astrolabium/blob/e947dfbdd49890dcb119940548537d1db59272c2/agent/math-agent-config.json): Konfiguriertes exklusives Ende 2026-10-18T22:00:00Z; 90 Sekunden Rechenbudget.
- [docs/agent-archive/2026-10-15/ARCHIVE.json](https://github.com/thomasmgfeller/x6-spectral-astrolabium/blob/e947dfbdd49890dcb119940548537d1db59272c2/docs/agent-archive/2026-10-15/ARCHIVE.json): Drei ausgewählte Originalartefakte dauerhaft in Git: Mathematik/Lorentz, Graphatlas, NOAA; GitHub-Digests, innere Inventare und historische Quellhashes geprüft. Nicht alle Läufe archiviert.

**Nächste Abnahme:** Unabhängige Replikation; separat registrierte Grössen/Seeds/Ränge und Unsicherheit für Finite-Size-Studie. n=6-Restpaaranalyse in main: Modul lorentz-n6-residuals; vollständiger historischer Atlasgenerator weiter im Branch-Modul.

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

**Nächste Abnahme:** Die vollständige n=7-Abnahme ist im Modul lorentz-n7-complete abgeschlossen: H7-bidirectional-moments ist durch zwei Restpaare widerlegt. Nächster Schritt: strukturelle Erklärung der minimalen Kollisionen und unabhängige externe Replikation; neue Aussagen müssen eigene Voraussetzungen nennen.

<a id="lorentz-n6-residuals"></a>
### Lorentz: vier n=6-Restpaare und Grenzen der Gradseparatoren

**Stand:** MAIN / SOFTWARE; Branch `main`; Commit `e947dfbdd49890dcb119940548537d1db59272c2`.

**Anleitung:** [aktuelle main-Dokumentation](https://github.com/thomasmgfeller/x6-spectral-astrolabium/blob/main/research/lorentz_n6_residuals/README.md). **Voraussetzungen:** Python 3.12, nur Standardbibliothek. Für die gemeinsame Offline-Suite zusätzlich Node.js 24. Kein Wolfram-Zugang oder Netzwerk beim Replay.

**Geprüfte Aussage:** Alle vier F0-Restpaare des vollständigen n=6-Atlas werden durch gepaarte gerichtete Grade D und bereits durch W_future getrennt. Drei sind Dualpaare. F0+W_future: 318/318 Klassen bei n=6, aber 163/164 für n=7 mit Höhe ≤2; beide Zählgrößen ergeben dort 164. Ein verbundenes n=8-Dualpaar kollidiert sogar für F0+D. Keine allgemeine Vollständigkeit oder physische Validierung.

```sh
python3 -S -B research/lorentz_n6_residuals/verify.py --output /tmp/lorentz-residuals.json
python3 -S -B research/lorentz_n6_residuals/verify.py --verify-report /tmp/lorentz-residuals.json
```

**Erwartung:** Exit 0, PASS_WITH_SCOPE_LIMITS; 4 getrennte / 0 ungelöste Primärpaare, 36 Wolfram-Polynome, 17 abgelehnte Fehlerkontrollen. Fehlende/manipulierte Ausgabe: Exit 1.

**Vorhandene Evidenz:**

- [research/lorentz_n6_residuals/evidence/local-results.json](https://github.com/thomasmgfeller/x6-spectral-astrolabium/blob/e947dfbdd49890dcb119940548537d1db59272c2/research/lorentz_n6_residuals/evidence/local-results.json): Vollständige Paarwerte, unabhängig nachgerechnete 318 Atlasfälle, Höhe-zwei-n=7-Enumeration, zwei explizite Grenzpaare und 17 Fehlerkontrollen.
- [research/lorentz_n6_residuals/evidence/wolfram-result.json](https://github.com/thomasmgfeller/x6-spectral-astrolabium/blob/e947dfbdd49890dcb119940548537d1db59272c2/research/lorentz_n6_residuals/evidence/wolfram-result.json): Wolfram 15.0.1: zwölf Matrizen, 36 exakt übereinstimmende monische Polynome, Grade, Zählgrößen, Isomorphie-/Dualitätsprüfungen. Zwei frühere fehlgeschlagene Versuche bleiben erhalten.
- [research/lorentz_n6_residuals/contract.json](https://github.com/thomasmgfeller/x6-spectral-astrolabium/blob/e947dfbdd49890dcb119940548537d1db59272c2/research/lorentz_n6_residuals/contract.json): Fixierte Konventionen und Auswahl, Herkunft des bestehenden Separators, Literaturabgrenzung und Hypothese H7-bidirectional-moments.
- [research/lorentz_n6_residuals/ACCEPTANCE.md](https://github.com/thomasmgfeller/x6-spectral-astrolabium/blob/e947dfbdd49890dcb119940548537d1db59272c2/research/lorentz_n6_residuals/ACCEPTANCE.md): Frischer Checkout und Netzwerk-isolierte CI erfolgreich, identisches Neun-Berichte-Bundle; zusätzliche CLI-Manipulationen auch unter Python -O abgelehnt.

**Nächste Abnahme:** Die vollständige n=7-Abnahme ist im Modul lorentz-n7-complete abgeschlossen: H7-bidirectional-moments ist durch zwei Restpaare widerlegt. Nächster Schritt: strukturelle Erklärung der minimalen Kollisionen und unabhängige externe Replikation; neue Aussagen müssen eigene Voraussetzungen nennen.

<a id="lorentz-n7-complete"></a>
### Lorentz: vollständige n=7-Prüfung und Widerlegung von H7

**Stand:** MAIN / SOFTWARE; Branch `main`; Commit `e947dfbdd49890dcb119940548537d1db59272c2`.

**Anleitung:** [aktuelle main-Dokumentation](https://github.com/thomasmgfeller/x6-spectral-astrolabium/blob/main/research/lorentz_n7_complete/README.md). **Voraussetzungen:** Python 3.12 unter Linux/POSIX, nur Standardbibliothek. Kein Netzwerk oder Wolfram-Zugang für die Rechnung.

**Geprüfte Aussage:** Vollständige exakte Prüfung von F0+W_future+W_past bis n=7. Bei n=7 bleiben zwei nichtisomorphe Paare der Höhe drei; die Hypothese ist widerlegt. Zweiter Enumerator prüft alle 2^21 oberen Binärmatrizen, 96.428 natürliche Beschriftungen und 2.045 Klassen. Insgesamt 2.450 Repräsentanten und 7.350 exakte Polynome. D trennt n≤7, ersetzt aber nicht die skalare Hypothese. Keine physische Validierung oder externe Begutachtung.

```sh
python3 -O research/lorentz_n7_complete/run.py --verify research/lorentz_n7_complete/results
```

**Erwartung:** Exit 0, PASS_REPRODUCED_EXACT_COUNTERCHECK mit REFUTED_BY_COUNTEREXAMPLE. 2.045 n=7-Ordnungen, 2.043 primäre Signaturklassen, zwei vollständig gespeicherte Restpaare. 17 Kontrollgruppen einschließlich 16 Zurückweisungen.

**Vorhandene Evidenz:**

- [research/lorentz_n7_complete/results/RESULTS.json](https://github.com/thomasmgfeller/x6-spectral-astrolabium/blob/e947dfbdd49890dcb119940548537d1db59272c2/research/lorentz_n7_complete/results/RESULTS.json): Vollständiges negatives Ergebnis, Quellbindung und alle Größenklassen.
- [research/lorentz_n7_complete/results/independent-results.json](https://github.com/thomasmgfeller/x6-spectral-astrolabium/blob/e947dfbdd49890dcb119940548537d1db59272c2/research/lorentz_n7_complete/results/independent-results.json): Algorithmisch getrennte Enumeration, Isomorphiesuche, natürliche Multiplizitäten und exakte Determinanteninterpolation.
- [research/lorentz_n7_complete/COUNTEREXAMPLES.md](https://github.com/thomasmgfeller/x6-spectral-astrolabium/blob/e947dfbdd49890dcb119940548537d1db59272c2/research/lorentz_n7_complete/COUNTEREXAMPLES.md): Beide minimalen n=7-Paare mit Matrizen und Polynomen; elementarer Nichtisomorphiebeweis und isolierte Erweiterungen für alle n≥7.
- [research/lorentz_n7_complete/freeze.json](https://github.com/thomasmgfeller/x6-spectral-astrolabium/blob/e947dfbdd49890dcb119940548537d1db59272c2/research/lorentz_n7_complete/freeze.json): Vor dem vollständigen Lauf veröffentlichte Quellhashes; prospektiver Arbeitsablauf, keine externe Präregistrierung.

**Nächste Abnahme:** Externe Replikation und strukturelle Analyse der beiden minimalen Kollisionsklassen. Eine neue begrenzte Aussage vor der nächsten Suche festlegen; der unveränderte skalare Ansatz ist bereits widerlegt.

<a id="industrial-v1"></a>
### Industrielle Entrauschung: V1-Bewertungsadapter

**Stand:** MAIN / SOFTWARE; Branch `main`; Commit `e947dfbdd49890dcb119940548537d1db59272c2`.

**Anleitung:** [aktuelle main-Dokumentation](https://github.com/thomasmgfeller/x6-spectral-astrolabium/blob/main/experiments/industrial-v1/README.md). **Voraussetzungen:** Python 3.12, gepinnte Anforderungen aus requirements; isolierte venv empfohlen.

**Geprüfte Aussage:** Vier Schemata, Vorprüfung, Bewertung und synthetischer Kontrollgenerator; ursprüngliche Quellen unverändert aus f5116b9970a6b7dc788c18623a8386b4cde33ad4 nach main übernommen. Bestätigende AP1-Freigabe bleibt NOT_READY. Der getrennte, tatsächlich ausgeführte Datenpilot steht im Modul industrial-pilot.

```sh
python3 -m pip install -r experiments/industrial-v1/requirements.txt
python3 experiments/industrial-v1/evaluate.py experiments/industrial-v1/V1_PROFILE_DRAFT.json --root experiments/industrial-v1 --output /tmp/register-v1-readiness.json
```

**Erwartung:** NOT_READY, Exit 3 ist beim veröffentlichten Entwurf erwartet.

**Vorhandene Evidenz:**

- [experiments/industrial-v1/examples/draft_readiness.json](https://github.com/thomasmgfeller/x6-spectral-astrolabium/blob/e947dfbdd49890dcb119940548537d1db59272c2/experiments/industrial-v1/examples/draft_readiness.json): Offene Eingabe-/Mess-/Protokollfelder einzeln ausgewiesen.

**Nächste Abnahme:** Für eine benannte industrielle Zielpopulation Rechte, 4-Kanal-Aufnahme/Kalibrierung, unabhängige Labels, Maschinen-/Standortstruktur und genügend unabhängige Lager beschaffen. Fachlich begründete Poweralternativen, Kandidat, starke Baseline und Schwellen vor Zugriff auf Bestätigungsdaten fixieren; ursprüngliche Gates unverändert anwenden.

<a id="industrial-pilot"></a>
### Industrieller Datenvertrag: Paderborn-Machbarkeitspilot

**Stand:** MAIN / SOFTWARE; Branch `main`; Commit `e947dfbdd49890dcb119940548537d1db59272c2`.

**Anleitung:** [aktuelle main-Dokumentation](https://github.com/thomasmgfeller/x6-spectral-astrolabium/blob/main/experiments/industrial-pilot/README.md). **Voraussetzungen:** Python 3.12, gepinnte NumPy/SciPy-Abhängigkeiten; nach Installation offline. Enthaltene fremde Messkanäle: CC BY-NC 4.0, ausschließlich nichtkommerzieller Pilot; eigener Code Apache-2.0. Keine absoluten Kalibrierbelege.

**Geprüfte Aussage:** Status: reproduzierbare Labor-Maschinenreferenz abgeschlossen (Bezeichnung präzisiert am 17.10.2026; Evidenz des Piloten vom 15.10.2026). Tatsächlich ausgeführte, reproduzierbare Sekundärauswertung realer Labormessungen: pro physischem Lager eine vor den Scores nach Metadaten gewählte Aufnahme; 16 Verwerfungen bleiben protokolliert. Drei feste klassische Referenzen. Hüllkurve: 4/4 beschädigte Evaluationslager erkannt, 1/2 gesunde mit Fehlalarm. Keine neue Filterleistung, 1-%-Fehlalarmgarantie oder industrielle Generalisierung.

```sh
python3 -m pip install -r experiments/industrial-v1/requirements.txt
python3 experiments/industrial-pilot/replay.py
python3 experiments/industrial-pilot/test_pilot.py
```

**Erwartung:** REPLAY_PASS, Exit 0; 20 Lager, feste Splits 7/7/6, 13 Tests mit 25 Negativkontrollen. industrial_claim_supported=false und bestätigender V1-Vertrag NOT_READY.

**Vorhandene Evidenz:**

- [experiments/industrial-pilot/evidence/pilot-report.json](https://github.com/thomasmgfeller/x6-spectral-astrolabium/blob/e947dfbdd49890dcb119940548537d1db59272c2/experiments/industrial-pilot/evidence/pilot-report.json): Reproduzierbare Labor-Maschinenreferenz abgeschlossen: vollständige Scores, Schwellen und Entscheidungen für 20 festgelegte Laborlager; industrielle Bestätigung ausdrücklich offen.
- [experiments/industrial-pilot/evidence/replay-portability.json](https://github.com/thomasmgfeller/x6-spectral-astrolabium/blob/e947dfbdd49890dcb119940548537d1db59272c2/experiments/industrial-pilot/evidence/replay-portability.json): Nach anfänglichem CI-Rundungsfehler: unveränderte eingefrorene Quellen und Ergebnisse, separater portabler Replay mit 13 Tests / 25 Negativkontrollen. Unstabile Evaluationsentscheidungen werden abgelehnt.
- [experiments/industrial-pilot/evidence/execution.json](https://github.com/thomasmgfeller/x6-spectral-astrolabium/blob/e947dfbdd49890dcb119940548537d1db59272c2/experiments/industrial-pilot/evidence/execution.json): Historischer Erstlauf: Vertrag/Daten/Code öffentlich vor Scores fixiert; damals elf Pilottests, 23 Negativkontrollen und 25 unveränderte V1-Tests bestanden.
- [experiments/industrial-pilot/data/manifest.json](https://github.com/thomasmgfeller/x6-spectral-astrolabium/blob/e947dfbdd49890dcb119940548537d1db59272c2/experiments/industrial-pilot/data/manifest.json): Originalarchiv-, MAT-, Signal- und NPZ-Hashes; Lager-IDs, Labels, Splits und sämtliche geprüften Wiederholungen.
- [experiments/industrial-pilot/data/LICENSE.txt](https://github.com/thomasmgfeller/x6-spectral-astrolabium/blob/e947dfbdd49890dcb119940548537d1db59272c2/experiments/industrial-pilot/data/LICENSE.txt): Quellenzuordnung und CC-BY-NC-4.0-Bedingungen der Messdaten; kommerzielle Nutzung nicht freigegeben.
- [experiments/industrial-pilot/evidence/power-plan.json](https://github.com/thomasmgfeller/x6-spectral-astrolabium/blob/e947dfbdd49890dcb119940548537d1db59272c2/experiments/industrial-pilot/evidence/power-plan.json): 368-Sonderfall bestätigt; zusätzliche exakte bedingte Powerrechnung mit gepaarten Diskordanzen. Planungsannahmen sind keine Piloteffekt-Schätzungen oder freigegebene Industrie-Fallzahlen.

**Nächste Abnahme:** Benannte industrielle Datenpartnerschaft/Zielpopulation, verwendbare Rechte, unabhängige Labels und ausreichende lager-/maschinenweise getrennte Daten. Vor bestätigendem Leistungsvergleich fachlich geprüften Vertrag samt Kandidat, Baseline, Schwellen, Power und unveränderten V1-Gates einfrieren; bei Clusterung vorab eigenes Design.

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

<a id="rax-guarded"></a>
### RAX-G1: deklarativer Runner und Fehlerbudget

**Stand:** MAIN / SOFTWARE; Branch `main`; Commit `e947dfbdd49890dcb119940548537d1db59272c2`.

**Anleitung:** [aktuelle main-Dokumentation](https://github.com/thomasmgfeller/x6-spectral-astrolabium/blob/main/docs/validation-v1/README.md). **Voraussetzungen:** Python 3.12, Standardbibliothek; neue Ausgabeverzeichnisse. Nur geprüftes deklaratives JSON, kein beliebiger fremder Python-Code.

**Geprüfte Aussage:** Konkrete M1-Zugriffswege im begrenzten Planerformat geschlossen: nur öffentliche Modell-/Präfixdaten, frische Worker, kein Callback, vollständige Index-/Zellprüfung, phasengebundener Holdout und exakter Replay. Historische B1/M1-Archive und Ergebnisse unverändert. Keine allgemeine Python-Sandbox oder externe Blindheit.

```sh
python3 -S -B tests/rax-guarded/qualify.py --output /tmp/register-rax-g1
python3 -S -B experimental/rax_guarded/runner.py verify /tmp/register-rax-g1/run
python3 -S -B tests/rax-guarded/check_budget.py --qualification /tmp/register-rax-g1/qualification.json
```

**Erwartung:** PASS mit 33 erwarteten Zurückweisungen; PASS_GUARDED_REPLAY mit 18 Zellen. Keine angenommene unzulässige Fähigkeit oder Ergebnisfälschung erlaubt.

**Vorhandene Evidenz:**

- [docs/validation-v1/evidence/guarded/qualification.json](https://github.com/thomasmgfeller/x6-spectral-astrolabium/blob/e947dfbdd49890dcb119940548537d1db59272c2/docs/validation-v1/evidence/guarded/qualification.json): Ausgeführte 33 Negativkontrollen, wirksame Datenmutationen und unabhängige exakte Vorhersage 13/24.
- [docs/validation-v1/ERROR_BUDGET.json](https://github.com/thomasmgfeller/x6-spectral-astrolabium/blob/e947dfbdd49890dcb119940548537d1db59272c2/docs/validation-v1/ERROR_BUDGET.json): Nulltoleranz im zugelassenen Profil; menschliche Blindheit, allgemeine Sandbox und externe Wiederholung offen.

**Nächste Abnahme:** Eine außenstehende Person führt den eingefrorenen Umfang aus und dokumentiert Rolle, Runtime, vollständige Ergebnisse und Abweichungen. Fremder ausführbarer Code benötigt eigene Betriebssystem-Isolationsabnahme.

<a id="reference-edition"></a>
### Gemeinsame Referenzedition und Agentenarchiv

**Stand:** MAIN / SOFTWARE; Branch `main`; Commit `e947dfbdd49890dcb119940548537d1db59272c2`.

**Anleitung:** [aktuelle main-Dokumentation](https://github.com/thomasmgfeller/x6-spectral-astrolabium/blob/main/docs/reference-qe-v0.1/EXTERNAL_REPRODUCTION.md). **Voraussetzungen:** Sauberer Git-Checkout; Python 3.12 und Node 24. Standardbibliothek. Die veröffentlichten Release-Assets sind der kürzere externe Einstieg.

**Geprüfte Aussage:** Erweiterte Referenzedition mit zehn Offline-Berichten, exaktem X6-QE-Modul, begrenztem RAX-G1-Runner und ausgewählten archivierten Original-Agentenbelegen. Alte Referenzfreigabe bleibt unverändert; externe personelle Wiederholung NOT_PERFORMED.

```sh
python3 -S -B tools/release/build.py --output /tmp/register-reference-assets
python3 -m zipfile -e /tmp/register-reference-assets/x6-reference-2026.10.15.zip /tmp/register-reference-unpacked
python3 -S -B /tmp/register-reference-unpacked/x6-reference/tools/release/reproduce.py --output /tmp/register-reference-reproduction
```

**Erwartung:** Aus dem entpackten neuen Release: PASS_REFERENCE_REPRODUCTION, zehn eingefrorene Berichte ohne Abweichung, 33 RAX-G1-Zurückweisungen. Anleitung nennt Paket und Runtime.

**Vorhandene Evidenz:**

- [docs/reference-qe-v0.1/expected-reference.json](https://github.com/thomasmgfeller/x6-spectral-astrolabium/blob/e947dfbdd49890dcb119940548537d1db59272c2/docs/reference-qe-v0.1/expected-reference.json): Festgelegte zehn Berichtshashes; acht bestehende fachliche Berichte unverändert. Neu: QE und ergänzter Fehlerkontrollbericht. Ausführungsabnahme steht in X6-QE/ACCEPTANCE.md.
- [docs/validation-v1/expected-reference.json](https://github.com/thomasmgfeller/x6-spectral-astrolabium/blob/e947dfbdd49890dcb119940548537d1db59272c2/docs/validation-v1/expected-reference.json): Feste SHA-256-Erwartungen für alle neun Referenzberichte; ursprünglicher Quellenumfang unverändert.
- [docs/agent-archive/2026-10-15/ARCHIVE.json](https://github.com/thomasmgfeller/x6-spectral-astrolabium/blob/e947dfbdd49890dcb119940548537d1db59272c2/docs/agent-archive/2026-10-15/ARCHIVE.json): Drei Original-ZIPs samt ursprünglichen Ablaufdaten, GitHub-Digests und vollständigen Dateiinventaren.
- [docs/validation-v1/evidence/citation-validation.json](https://github.com/thomasmgfeller/x6-spectral-astrolabium/blob/e947dfbdd49890dcb119940548537d1db59272c2/docs/validation-v1/evidence/citation-validation.json): CFF 1.2.0 gegen offizielles Schema geprüft; keine erfundene DOI oder ORCID.
- [docs/validation-v1/external-report.template.json](https://github.com/thomasmgfeller/x6-spectral-astrolabium/blob/e947dfbdd49890dcb119940548537d1db59272c2/docs/validation-v1/external-report.template.json): Noch nicht eingereichte Erklärung der ausführenden Person; keine externe Bestätigung vorweggenommen.

**Nächste Abnahme:** Tatsächliche unabhängige Wiederholung entgegennehmen, Ergebnisdateien erneut prüfen, Abweichungen und personelle Unabhängigkeit bewerten; EXT-1 erst danach schließen.

<a id="x6-qe"></a>
### X6-QE: exakte Graphreferenzen und Grenzen spektraler Unterscheidbarkeit

**Stand:** MAIN / SOFTWARE; Branch `main`; Commit `e947dfbdd49890dcb119940548537d1db59272c2`.

**Anleitung:** [aktuelle main-Dokumentation](https://github.com/thomasmgfeller/x6-spectral-astrolabium/blob/main/research/x6_qe/README.md). **Voraussetzungen:** Python 3.12, nur Standardbibliothek. Für gemeinsame Suite zusätzlich Node.js 24. Neue Ausgabewege; keine Downloads/Wolfram-Aufrufe.

**Geprüfte Aussage:** Vier Graphen in drei bekannten Referenzen: Stern mit trivialer Ihara-Zeta; primitiver Viererzyklus mit zusammengesetzter Länge; Turmgraph/Shrikhande mit gleichem Spektrum und gleicher globaler Ihara-Zeta, aber K4=8/0. Keine neue Mathematik, Quantengedächtnis- oder Arithmetikbehauptung.

```sh
python3 -S -B research/x6_qe/verify.py --output /tmp/x6-qe.json
python3 -S -B research/x6_qe/verify.py --verify-report /tmp/x6-qe.json
```

**Erwartung:** PASS_WITH_SCOPE_LIMITS; 3 Referenzfälle, 4 Graphen, 12 Umbenennungen, 21 zurückgewiesene Fehlerfälle. Fehler: Exit 1.

**Vorhandene Evidenz:**

- [research/x6_qe/evidence/local-results.json](https://github.com/thomasmgfeller/x6-spectral-astrolabium/blob/e947dfbdd49890dcb119940548537d1db59272c2/research/x6_qe/evidence/local-results.json): Vollständige exakte Polynome, getrennte Determinantenprüfungen und K4-Zählwege, Quellenhashes und Fehlerkontrollen. Interne Rechnung; keine personell unabhängige Wiederholung.

**Nächste Abnahme:** Externe Wiederholung des eingefrorenen Umfangs; vor Spider-/Billiard-Auswertung Originalbild/Erzeugungsregel beschaffen und eigenen Numerikvertrag qualifizieren. Lorentz-n=7 bleibt Priorität.

<a id="rax-cqg-benchmark"></a>
### RAX-CQG: endlicher Causal-Set Benchmark 0.2.0

**Stand:** MAIN / SOFTWARE; Branch `main`; Commit `e947dfbdd49890dcb119940548537d1db59272c2`.

**Anleitung:** [aktuelle main-Dokumentation](https://github.com/thomasmgfeller/x6-spectral-astrolabium/blob/main/docs/research/rax/cqg-benchmark-v0.2.0/README.md). **Voraussetzungen:** Python 3.12, NumPy 2.3.5, SciPy 1.17.0, Node.js 24; Browser für das eigenständige HTML-Labor. Installation der Python-Abhängigkeiten benötigt Netzwerk oder vorbereitete Wheels.

**Geprüfte Aussage:** Explizite endliche Ordnungen, Intervalle, dimensionslose 4D-BDG-Kombination, Graphspektren und induzierte Ausdünnung. Separates klassisches Gaußfeld und vorausgesetzte Zweiqubit-Uhr. Kein Nachweis für Quantengravitation, KR-Unterdrückung oder einen Kontinuumslimes.

```sh
cd research/rax_cqg/benchmark-v0.2.0
python3 -m pip install -r requirements.txt
python3 validate.py
```

**Erwartung:** PASS_WITH_EXPLICIT_SCOPE_LIMITS; 28 Python-Testmethoden, 28 Python/JavaScript-Vergleichsfälle, 16 UI-Logikprüfungen, 240 wiederholte Pilotläufe und 30 Gruppenauswertungen. Fehler: Exit ungleich 0. Der Befehl schreibt einen neuen lokalen Bericht.

**Vorhandene Evidenz:**

- [research/rax_cqg/benchmark-v0.2.0/VALIDATION.json](https://github.com/thomasmgfeller/x6-spectral-astrolabium/blob/e947dfbdd49890dcb119940548537d1db59272c2/research/rax_cqg/benchmark-v0.2.0/VALIDATION.json): Eingefrorener interner Prüflauf mit Quellenhashes und expliziten Grenzen. UI-Logik in Node; keine damalige visuelle Browserprüfung oder personell unabhängige Replikation.
- [docs/research/rax/cqg-benchmark-v0.2.0/PUBLICATION.json](https://github.com/thomasmgfeller/x6-spectral-astrolabium/blob/e947dfbdd49890dcb119940548537d1db59272c2/docs/research/rax/cqg-benchmark-v0.2.0/PUBLICATION.json): Freigegebenes ZIP, 28 bytegleiche Paketdateien und identische Browserkopie; zusätzliche CI getrennt vom ursprünglichen Bericht.

**Nächste Abnahme:** Unabhängige Replikation und fachliche Prüfung. Vor Ensemblevergleichen Beobachtungsgrösse, Dichtekontrollen, Stichprobengrösse und Fehlerbudget festlegen; keine neue physikalische Schlussfolgerung aus dem Pilot allein.

<a id="free-field-entropy"></a>
### RAX-CQG: freies Feld und Entropiereferenz

**Stand:** MAIN / SOFTWARE; Branch `main`; Commit `e947dfbdd49890dcb119940548537d1db59272c2`.

**Anleitung:** [aktuelle main-Dokumentation](https://github.com/thomasmgfeller/x6-spectral-astrolabium/blob/main/research/free_field_entropy/README.md). **Voraussetzungen:** Python 3.12 unter Linux/POSIX; NumPy 2.3.5, SciPy 1.17.0 und threadpoolctl 3.6.0. Vollständiger Referenzlauf: maximal 30 Minuten und 2 GiB; kurze Prüfer ohne neue Zielstichproben.

**Geprüfte Aussage:** Freier masseloser SJ-Gaußzustand auf festen 1+1-kausalen Mengen mit expliziten Nullmoden und Cutoffs. 13 Gegenprüfungen und bekannte Oszillatorentropie bestehen. 64 neue Ordnungen: Steigung 0,358, 95%-Intervall [0,260; 0,458]; vorab verlangte Präzision und Cutoff-Stabilität verfehlt (REFERENCE_NOT_ESTABLISHED). Kein nachgewiesener geometrischer oder industrieller Zusatznutzen.

```sh
python3 -m pip install -r research/free_field_entropy/requirements.txt
OPENBLAS_NUM_THREADS=1 python3 -B research/free_field_entropy/test_core.py -v
OPENBLAS_NUM_THREADS=1 python3 -B research/free_field_entropy/check.py research/free_field_entropy/results
```

**Erwartung:** 13 Gegenprüfungen bestehen; PASS_LEDGER_AND_ANALYSIS prüft Quellen, vollständige Eingaben und Auswertung. Der getrennte wissenschaftliche Status ist im Ergebnisbericht ausgewiesen.

**Vorhandene Evidenz:**

- [research/free_field_entropy/RESULTS.md](https://github.com/thomasmgfeller/x6-spectral-astrolabium/blob/e947dfbdd49890dcb119940548537d1db59272c2/research/free_field_entropy/RESULTS.md): Vollständiger 64-Ordnungen-Befund, vorab fixiertes Kriterium, Cutoff-Empfindlichkeit und Grenzen.
- [research/free_field_entropy/analytic-validation.json](https://github.com/thomasmgfeller/x6-spectral-astrolabium/blob/e947dfbdd49890dcb119940548537d1db59272c2/research/free_field_entropy/analytic-validation.json): Zwei-Oszillator-Referenz und 13 analytische/strukturelle Gegenprüfungen.
- [research/free_field_entropy/independent-audit.json](https://github.com/thomasmgfeller/x6-spectral-astrolabium/blob/e947dfbdd49890dcb119940548537d1db59272c2/research/free_field_entropy/independent-audit.json): Vier Größen mit getrenntem hermiteschem Kovarianz-Rechenweg; interne Prüfung, keine externe Replikation.
- [research/free_field_entropy/freeze.json](https://github.com/thomasmgfeller/x6-spectral-astrolabium/blob/e947dfbdd49890dcb119940548537d1db59272c2/research/free_field_entropy/freeze.json): Öffentlich vor dem Zielversuch fixierte Quellen und Analyse; früherer Pilot separat ausgewiesen.

**Nächste Abnahme:** Endliche Größeneffekte und Cutoff-Empfindlichkeit in einem neuen vorab festgelegten Versuch klären. Geometrieantworten und Zusatznutzen gegenüber bestehenden Merkmalen bei gleichem Budget bleiben separate offene Gates.

<a id="lorentz-proper-time"></a>
### Eigenzeit: Referenz, Fehlergrenzen und sequenzielle Diagnose

**Stand:** MAIN / SOFTWARE; Branch `main`; Commit `e947dfbdd49890dcb119940548537d1db59272c2`.

**Anleitung:** [aktuelle main-Dokumentation](https://github.com/thomasmgfeller/x6-spectral-astrolabium/blob/main/research/lorentz_proper_time_publication/README.md). **Voraussetzungen:** Python 3.12 unter Linux/POSIX; NumPy 2.3.5 und SciPy 1.17.0. Reproduktion in temporären Verzeichnissen; nach Installation kein externer Dienst. Bekannte Dimension, Zeitskala und uniformes unabhängiges Beprobungsgesetz für die statistische Aussage erforderlich.

**Geprüfte Aussage:** Bedingte Eigenzeit-Referenz im bekannten flachen Modell: ursprüngliche 1+1-Qualifikation mit RMSE 0,031614; 49.152 neue Punktwolken prüfen d=2,3,4 und endliche Fehlergrenzen. Zeituniformes Nachbeproben mit expliziter Stoppregel und einmaliger Kettendiagnostik. Kein universeller Zeit-, Krümmungs- oder industrieller Leistungsnachweis; lokale Quellenfixierung vor den neuen Ziehungen, keine öffentliche Präregistrierung.

```sh
python3 -m pip install -r research/lorentz_proper_time_sequential/requirements.txt
OPENBLAS_NUM_THREADS=1 python3 -B research/lorentz_proper_time_publication/replay.py
python3 research/lorentz_proper_time_publication/planning.py
```

**Erwartung:** PASS_PUBLISHED_EVIDENCE_AND_REPLAY nach Prüfung beider neuen Archive, vollständiger Wiederholung, Rohdaten-/Ergebnisvergleich, Quellenfixierung und Reparaturhistorie. Der ursprüngliche 1+1-Versuch hat seinen separat dokumentierten Reproduktionsweg.

**Vorhandene Evidenz:**

- [research/lorentz_proper_time/RESULTS.md](https://github.com/thomasmgfeller/x6-spectral-astrolabium/blob/e947dfbdd49890dcb119940548537d1db59272c2/research/lorentz_proper_time/RESULTS.md): Ursprünglich 6.912 Ordnungen: Hauptvergleich qualifiziert, größte exakt abgeglichene Zusatzkontrolle mit nur 63 statt 128 Paaren offen.
- [research/lorentz_proper_time_domain/results/RESULTS.md](https://github.com/thomasmgfeller/x6-spectral-astrolabium/blob/e947dfbdd49890dcb119940548537d1db59272c2/research/lorentz_proper_time_domain/results/RESULTS.md): CONDITIONAL_FLAT_MODEL_CHECK_PASSED; 24 Zellen, Binomialintervalle und Nullzählungsgrenze.
- [research/lorentz_proper_time_domain/results/verification.json](https://github.com/thomasmgfeller/x6-spectral-astrolabium/blob/e947dfbdd49890dcb119940548537d1db59272c2/research/lorentz_proper_time_domain/results/verification.json): Interne Prüfung aller 49.152 Rohzählungen, Quellenbindung, Quantilinversion und zwölf voller Relationsgegenprüfungen.
- [research/lorentz_proper_time_sequential/results/RESULTS.md](https://github.com/thomasmgfeller/x6-spectral-astrolabium/blob/e947dfbdd49890dcb119940548537d1db59272c2/research/lorentz_proper_time_sequential/results/RESULTS.md): DECLARED_SEQUENTIAL_REFERENCE_CHECK_PASSED; getrennte Zählblock- und Geometriekontrollen, Budgetabbruch und Dichtestörung ausdrücklich ausgewiesen.
- [research/lorentz_proper_time_sequential/results/verification.json](https://github.com/thomasmgfeller/x6-spectral-astrolabium/blob/e947dfbdd49890dcb119940548537d1db59272c2/research/lorentz_proper_time_sequential/results/verification.json): Interne skalare Stream-Replays, 2.048 Rang-p-Werte und geometrische Integration; keine externe Replikation.
- [research/lorentz_proper_time_sequential/EXECUTION_HISTORY.md](https://github.com/thomasmgfeller/x6-spectral-astrolabium/blob/e947dfbdd49890dcb119940548537d1db59272c2/research/lorentz_proper_time_sequential/EXECUTION_HISTORY.md): Erhaltener Erstlauf mit JSON-Serialisierungsfehler; einzige Typkonvertierung und identische Zählblöcke nach Wiederholung.
- [research/lorentz_proper_time_publication/planning.json](https://github.com/thomasmgfeller/x6-spectral-astrolabium/blob/e947dfbdd49890dcb119940548537d1db59272c2/research/lorentz_proper_time_publication/planning.json): Analytische Feststichprobenbeispiele für unter 10% relativen Fehler bei tau/T=0,1 in 4D; getrennt von sequenziellen Budgetmedianen.

**Nächste Abnahme:** Externe Replikation des deklarierten Modells. Für eine Erweiterung zuerst eine bestimmte Geometrie-/Beprobungsklasse, unabhängige Maßstabskalibrierung und Modellfehlergrenze festlegen. Kettenwarnungen erlauben ohne bekannte Beprobung keine eindeutige Krümmungsdiagnose.

<a id="lorentz-curvature"></a>
### Krümmungsbenchmark: Empfindlichkeit und Dichteverwechslung

**Stand:** MAIN / SOFTWARE; Branch `main`; Commit `e947dfbdd49890dcb119940548537d1db59272c2`.

**Anleitung:** [aktuelle main-Dokumentation](https://github.com/thomasmgfeller/x6-spectral-astrolabium/blob/main/research/lorentz_curvature/README.md). **Voraussetzungen:** Python 3.12 unter Linux/POSIX; NumPy 2.3.5, SciPy 1.17.0 und vollständige Git-Historie. Getrennte temporäre Reproduktion; pro Ziellauf 600 Sekunden und 2 GiB. N=64/128 ist fest, also bedingte Poisson-Beprobung.

**Geprüfte Aussage:** 8.702 Ordnungen nach öffentlich fixiertem Prüfvertrag. Im primären de-Sitter-Fall N=128, h=1,25 warnt C2/C3/C4 in 118/512 Fällen, die längste Kette in 5/512; beide verfehlen das Empfindlichkeitsziel. 3.072 konforme Dichtezwillinge bestätigen dieselbe Ordnung trotz verschiedener Krümmung. Keine universelle Krümmungsidentifikation bei unbekannter Beprobungsdichte, keine physische Planck-Uhr und keine fortlaufende Testgarantie.

```sh
python3 -m pip install -r research/lorentz_curvature/requirements.txt
python3 -B research/lorentz_curvature/selftest.py
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 python3 -B research/lorentz_curvature/reproduce_portable.py
```

**Erwartung:** PASS_ARCHIVED_EVIDENCE und PASS_PORTABLE_CURVATURE_REPLAY. Nur Original- oder konkret gegengeprüfte Koordinatenhashes werden akzeptiert; unbekannte Varianten scheitern. Der ursprüngliche strenge Replay bleibt erhalten. Wissenschaftlich weiterhin PRIMARY_SENSITIVITY_NOT_ESTABLISHED für beide Methoden und NOT_IDENTIFIABLE_WITH_UNRESTRICTED_SAMPLING_DENSITY.

**Vorhandene Evidenz:**

- [research/lorentz_curvature/RESULTS.md](https://github.com/thomasmgfeller/x6-spectral-astrolabium/blob/e947dfbdd49890dcb119940548537d1db59272c2/research/lorentz_curvature/RESULTS.md): Alle zwölf Zielzellen, vorab festgelegte Hauptentscheidung, Unsicherheit und exakte Dichteverwechslung.
- [research/lorentz_curvature/contract.json](https://github.com/thomasmgfeller/x6-spectral-astrolabium/blob/e947dfbdd49890dcb119940548537d1db59272c2/research/lorentz_curvature/contract.json): Unveränderter Vertrag aus dem öffentlichen Quellenstand 31cfd8c vor dem ersten Ziellauf.
- [research/lorentz_curvature/results/verification.json](https://github.com/thomasmgfeller/x6-spectral-astrolabium/blob/e947dfbdd49890dcb119940548537d1db59272c2/research/lorentz_curvature/results/verification.json): 8.702 volle Ordnungen, 26.106 unabhängige Kettenzählungen, 12.288 Ränge, 3.072 gekoppelte Zwillinge und 1.024 abgewiesene Relationsfehler.
- [research/lorentz_curvature/results/replay.log](https://github.com/thomasmgfeller/x6-spectral-astrolabium/blob/e947dfbdd49890dcb119940548537d1db59272c2/research/lorentz_curvature/results/replay.log): Vollständiger interner Replay aller Seeds, Relationsbytes, Koordinatenhashes und wissenschaftlichen Ausgaben; keine externe Replikation.
- [research/lorentz_curvature/PORTABILITY.md](https://github.com/thomasmgfeller/x6-spectral-astrolabium/blob/e947dfbdd49890dcb119940548537d1db59272c2/research/lorentz_curvature/PORTABILITY.md): Erster CI-Replay scheiterte am Koordinatenhash. Nachträgliche vollständige NumPy-Gegenprüfung: maximale Abweichung 2,22e-16, alle Relationen identisch. Originalquellen unverändert; zusätzlicher begrenzter Replay separat ausgewiesen.
- [research/lorentz_curvature/results/portable-replay.log](https://github.com/thomasmgfeller/x6-spectral-astrolabium/blob/e947dfbdd49890dcb119940548537d1db59272c2/research/lorentz_curvature/results/portable-replay.log): Ergänzter vollständiger Replay mit 8.696 konkret geprüften Hashvarianten und sechs Originalhashes; unbekannte Varianten abgewiesen.

**Nächste Abnahme:** Externe Replikation. Ein Demonstrator muss Modellabweichungswarnungen und die Dichtezwillinge sichtbar trennen. Vor einer neuen Leistungsstudie unabhängiges Wissen über Beprobung/Volumen und eine identifizierbare geometrische Zielgröße festlegen; kein nachträgliches Retuning dieses Versuchs.

<a id="lorentz-rss-fixed-n"></a>
### RSS bei fester Punktzahl: Formeln, Prüfung und Grenzen

**Stand:** MAIN / SOFTWARE; Branch `main`; Commit `e947dfbdd49890dcb119940548537d1db59272c2`.

**Anleitung:** [aktuelle main-Dokumentation](https://github.com/thomasmgfeller/x6-spectral-astrolabium/blob/main/research/lorentz_rss_fixed_n/README.md). **Voraussetzungen:** Python 3.12, Linux/POSIX, gepinnte NumPy-/SciPy-/Matplotlib-Versionen; vollständiger Git-Checkout. Pro Ziellauf 600 Sekunden und 2 GiB.

**Geprüfte Aussage:** Exakte bedingte Kettenmomente und Kovarianzidentität; 24.576 unabhängige Wolken nach öffentlicher Quellenfixierung. Gemeinsames ±5%-Präzisionsziel nicht erreicht. Unabhängige C2-Quadratur stützt die korrigierte Vorhersage; die untersuchte allgemeine lineare Krümmungsinversion streut bei N=64/128 sehr stark. Keine Auflösung der Dichteverwechslung.

```sh
python3 -m pip install -r research/lorentz_rss_fixed_n/requirements.txt
python3 -B research/lorentz_rss_fixed_n/reproduce.py
```

**Erwartung:** PASS_FULL_RSS_FIXED_N_REPLAY; wissenschaftlich unverändert FORWARD_SLOPE_NOT_RESOLVED. Alle eingefrorenen Quellen bleiben identisch; eine dokumentierte Importhülle behebt den Namenskonflikt des ursprünglichen Prüfers.

**Vorhandene Evidenz:**

- [research/lorentz_rss_fixed_n/DERIVATION.md](https://github.com/thomasmgfeller/x6-spectral-astrolabium/blob/e947dfbdd49890dcb119940548537d1db59272c2/research/lorentz_rss_fixed_n/DERIVATION.md): Bedingte Mittelwerte, Volumenkorrektur, überlappende Teilmengen und Skalenannahmen.
- [research/lorentz_rss_fixed_n/RESULTS.md](https://github.com/thomasmgfeller/x6-spectral-astrolabium/blob/e947dfbdd49890dcb119940548537d1db59272c2/research/lorentz_rss_fixed_n/RESULTS.md): Alle Entscheidungen, Unsicherheit, Kovarianz und große Rekonstruktionsfehler.
- [research/lorentz_rss_fixed_n/contract.json](https://github.com/thomasmgfeller/x6-spectral-astrolabium/blob/e947dfbdd49890dcb119940548537d1db59272c2/research/lorentz_rss_fixed_n/contract.json): Unveränderter Vertrag aus dem öffentlichen Quellenstand 485d866 vor dem ersten Zielversuch.
- [research/lorentz_rss_fixed_n/results/summary.json](https://github.com/thomasmgfeller/x6-spectral-astrolabium/blob/e947dfbdd49890dcb119940548537d1db59272c2/research/lorentz_rss_fixed_n/results/summary.json): Maschinenlesbare Ergebnisse; gemeinsames Präzisionsziel nicht erfüllt.
- [research/lorentz_rss_fixed_n/VERIFICATION.json](https://github.com/thomasmgfeller/x6-spectral-astrolabium/blob/e947dfbdd49890dcb119940548537d1db59272c2/research/lorentz_rss_fixed_n/VERIFICATION.json): Vollständiger interner Replay aller 24.576 Relationshashes und wissenschaftlichen Ausgaben.

**Nächste Abnahme:** Informationsbedarf vor größerem Budget bestimmen. De-Sitter-Modell mit bekannter Ricci-Beziehung und allgemeine Zweiparameter-Rekonstruktion getrennt prüfen; neue Geometriefamilien, Resttermkontrolle und kovarianzbewusste Unsicherheiten vorab festlegen.

<a id="lorentz-proper-time-validity"></a>
### Eigenzeit v0.2: Gültigkeitsbereich und Informationsbedarf

**Stand:** MAIN / SOFTWARE; Branch `main`; Commit `e947dfbdd49890dcb119940548537d1db59272c2`.

**Anleitung:** [aktuelle main-Dokumentation](https://github.com/thomasmgfeller/x6-spectral-astrolabium/blob/main/research/lorentz_proper_time_validity/README.md). **Voraussetzungen:** Python 3.12, Linux/POSIX, gepinnte NumPy-/SciPy-/Matplotlib-Versionen und vollständige Git-Historie. Numerischer Ziellauf: 600 Sekunden und 2 GiB. Drei BLAS/OpenMP-Threadvariablen vor Python auf 1 setzen.

**Geprüfte Aussage:** 1.176 festgelegte Modell-/Budget-/Intervallkombinationen direkt berechnet. Alle 714 Kombinationen innerhalb ihrer Modellklasse erreichen mindestens 95% Überdeckung; 192 erfüllen zusätzlich das Präzisionsziel, 522 bleiben zu unpräzise. 462 Kombinationen liegen ausserhalb der jeweils vorausgesetzten Klasse. Extern begrenzte Dichtefehler erlauben konservative flache Eigenzeitintervalle, können aber eine irreduzible Präzisionsgrenze erzeugen. Keine allgemeine Krümmungsqualifikation.

```sh
python3 -m pip install -r research/lorentz_proper_time_validity/requirements.txt
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 python3 -B research/lorentz_proper_time_validity/reproduce.py
```

**Erwartung:** PASS_FULL_PROPER_TIME_VALIDITY_REPLAY. 1.176 deterministische Kombinationen; vollständige Reproduktion mit unveränderten Forschungsquellen. Keine neuen Punktwolken oder realen Messungen.

**Vorhandene Evidenz:**

- [research/lorentz_proper_time_validity/RESULTS.md](https://github.com/thomasmgfeller/x6-spectral-astrolabium/blob/e947dfbdd49890dcb119940548537d1db59272c2/research/lorentz_proper_time_validity/RESULTS.md): Gültigkeitskarte, Budgettabelle, Fehlpräzision bei selektiv fehlenden Ereignissen und verbleibende Grenzen.
- [research/lorentz_proper_time_validity/DERIVATION.md](https://github.com/thomasmgfeller/x6-spectral-astrolabium/blob/e947dfbdd49890dcb119940548537d1db59272c2/research/lorentz_proper_time_validity/DERIVATION.md): Exakte Binomialmodelle, bekannte de-Sitter-Familie und konservative Transformation für extern begrenzte Intensitätsverhältnisse.
- [research/lorentz_proper_time_validity/contract.json](https://github.com/thomasmgfeller/x6-spectral-astrolabium/blob/e947dfbdd49890dcb119940548537d1db59272c2/research/lorentz_proper_time_validity/contract.json): Öffentlicher Quellenstand 67dc770 vor der ersten Zielgitter-Auswertung.
- [research/lorentz_proper_time_validity/ARCHIVE.json](https://github.com/thomasmgfeller/x6-spectral-astrolabium/blob/e947dfbdd49890dcb119940548537d1db59272c2/research/lorentz_proper_time_validity/ARCHIVE.json): Prüfsumme und Inventar aller unveränderten Originalausgaben im ZIP.
- [research/lorentz_proper_time_validity/VERIFICATION.json](https://github.com/thomasmgfeller/x6-spectral-astrolabium/blob/e947dfbdd49890dcb119940548537d1db59272c2/research/lorentz_proper_time_validity/VERIFICATION.json): Getrennte Integral-/CDF-Gegenprüfung aller 1.176 Zellen und vollständiger Replay.

**Nächste Abnahme:** Externe Replikation und unabhängig begründete Dichte-/Erfassungsgrenzen für eine konkrete Datenquelle. Die getrennten Module lorentz-de-sitter-information und lorentz-de-sitter-c2 enthalten inzwischen Kovarianzplanung und konservative modellbedingte Krümmungsintervalle; präzise gekrümmte Uhr weiterhin offen.

<a id="lorentz-de-sitter-information"></a>
### Eigenzeit: de-Sitter-Informationsplanung

**Stand:** MAIN / SOFTWARE; Branch `main`; Commit `e947dfbdd49890dcb119940548537d1db59272c2`.

**Anleitung:** [aktuelle main-Dokumentation](https://github.com/thomasmgfeller/x6-spectral-astrolabium/blob/main/research/lorentz_de_sitter_information/README.md). **Voraussetzungen:** Python 3.12, gepinnte NumPy-/SciPy-/Matplotlib-Versionen, vollständige Git-Historie. POSIX-Ziellauf begrenzt auf 600 Sekunden und 2 GiB.

**Geprüfte Aussage:** Kovarianzbewusste Einparameter-Planung aus öffentlichen Pilotdaten, danach 16.384 neue unabhängige Wolken nach Quellenfixierung. Im Hauptvergleich senkt GLS234 den RMSE gegenüber C2 um 1,37%; das vorab gesetzte 10%-Ziel wird verfehlt. Bei schwacher Krümmung bleibt der approximative Datenbedarf hoch. Keine Freigabe von Krümmungsintervallen.

```sh
python3 -m pip install -r research/lorentz_de_sitter_information/requirements.txt
python3 -B research/lorentz_de_sitter_information/verify.py
```

**Erwartung:** PASS_FULL_INFORMATION_REPLAY, 16.384 vollständig reproduzierte Punktwolken; interne Softwaregegenprüfung.

**Vorhandene Evidenz:**

- [research/lorentz_de_sitter_information/RESULTS.md](https://github.com/thomasmgfeller/x6-spectral-astrolabium/blob/e947dfbdd49890dcb119940548537d1db59272c2/research/lorentz_de_sitter_information/RESULTS.md): Hauptvergleich, approximative Budgets, negatives 10%-Gate und nächste Entscheidung.
- [research/lorentz_de_sitter_information/contract.json](https://github.com/thomasmgfeller/x6-spectral-astrolabium/blob/e947dfbdd49890dcb119940548537d1db59272c2/research/lorentz_de_sitter_information/contract.json): Öffentlicher Prüfvertrag vor dem frischen Test; Pilotplanung ist deskriptiv.
- [research/lorentz_de_sitter_information/results/summary.json](https://github.com/thomasmgfeller/x6-spectral-astrolabium/blob/e947dfbdd49890dcb119940548537d1db59272c2/research/lorentz_de_sitter_information/results/summary.json): Alle zwölf frischen Ergebniszeilen und gepaarter Bootstrapvergleich.
- [research/lorentz_de_sitter_information/results/hashes.json](https://github.com/thomasmgfeller/x6-spectral-astrolabium/blob/e947dfbdd49890dcb119940548537d1db59272c2/research/lorentz_de_sitter_information/results/hashes.json): Prüfsummen aller Originalausgaben, einschliesslich vollständiger Kettenmerkmale und Relationshashes.
- [research/lorentz_de_sitter_information/VERIFICATION.json](https://github.com/thomasmgfeller/x6-spectral-astrolabium/blob/e947dfbdd49890dcb119940548537d1db59272c2/research/lorentz_de_sitter_information/VERIFICATION.json): Vollständiger interner Replay und getrennte Kausalitäts-, Ketten-, Gewichts- und Momentprüfungen.

**Nächste Abnahme:** Konservative C2-Konfidenzinversion ist im getrennten Modul lorentz-de-sitter-c2 umgesetzt. Nächste Stufe: eine schärfere endlich gültige Schranke unter korrekter Paarabhängigkeit; externe Replikation und Dichtebegründung bleiben offen.

<a id="lorentz-de-sitter-c2"></a>
### Eigenzeit: konservative C2-Krümmungsintervalle

**Stand:** MAIN / SOFTWARE; Branch `main`; Commit `e947dfbdd49890dcb119940548537d1db59272c2`.

**Anleitung:** [aktuelle main-Dokumentation](https://github.com/thomasmgfeller/x6-spectral-astrolabium/blob/main/research/lorentz_de_sitter_c2/README.md). **Voraussetzungen:** Python 3.12, gepinnte NumPy-/SciPy-/SymPy-/Matplotlib-Versionen und vollständige Git-Historie. POSIX-Ziellauf: 600 Sekunden und 2 GiB.

**Geprüfte Aussage:** Rational eingeschlossene C2-Vorwärtsfunktion und strenge Monotonie für bekannte uniforme 4D-de-Sitter-Modelle, 0≤h≤0,5. Eine Hoeffding-U-Statistik-Schranke liefert mindestens 95% Überdeckung bei festem Budget und unabhängigen Wolken. 16.384 neue Wolken: alle geprüften Intervalle enthalten die Modellwerte, keines erreicht 20%-Präzision. Keine allgemeine Uhr oder Identifikation bei unbekannter Dichte.

```sh
python3 -m pip install -r research/lorentz_de_sitter_c2/requirements.txt
python3 -B research/lorentz_de_sitter_c2/verify.py
```

**Erwartung:** PASS_FULL_C2_CONFIDENCE_REPLAY: exakte Integral- und Monotonieprüfungen, 16.384 reproduzierte Punktwolken, alle Intervall- und Budgetentscheide.

**Vorhandene Evidenz:**

- [research/lorentz_de_sitter_c2/DERIVATION.md](https://github.com/thomasmgfeller/x6-spectral-astrolabium/blob/e947dfbdd49890dcb119940548537d1db59272c2/research/lorentz_de_sitter_c2/DERIVATION.md): Vollständige geometrische und statistische Herleitung, uniforme Restfehler, konservative Umkehrung und Geltungsbereich.
- [research/lorentz_de_sitter_c2/RESULTS.md](https://github.com/thomasmgfeller/x6-spectral-astrolabium/blob/e947dfbdd49890dcb119940548537d1db59272c2/research/lorentz_de_sitter_c2/RESULTS.md): Alle Präzisionsverweigerungen, hinreichende Budgetgrenzen und offener Effizienzschritt.
- [research/lorentz_de_sitter_c2/contract.json](https://github.com/thomasmgfeller/x6-spectral-astrolabium/blob/e947dfbdd49890dcb119940548537d1db59272c2/research/lorentz_de_sitter_c2/contract.json): Öffentliche Quellenfixierung c2f1659 vor Zielgitter und frischen Punktwolken.
- [research/lorentz_de_sitter_c2/results/mathematics.json](https://github.com/thomasmgfeller/x6-spectral-astrolabium/blob/e947dfbdd49890dcb119940548537d1db59272c2/research/lorentz_de_sitter_c2/results/mathematics.json): Exakte Bruchzertifikate, Reihenkoeffizienten und getrennte Quadraturkontrolle.
- [research/lorentz_de_sitter_c2/VERIFICATION.json](https://github.com/thomasmgfeller/x6-spectral-astrolabium/blob/e947dfbdd49890dcb119940548537d1db59272c2/research/lorentz_de_sitter_c2/VERIFICATION.json): Symbolische Integralgegenprüfung, abhängiger Paarkern als Negativkontrolle und vollständiger Replay.

**Nächste Abnahme:** Der vorab fixierte KL-Vergleich liegt im Nachfolgemodul lorentz-de-sitter-kl vor: 2,71–2,77-fach kleinere hinreichende Budgets. Diese Hoeffding-Referenz bleibt unverändert; externe Beweisprüfung und Replikation stehen aus.

<a id="lorentz-de-sitter-kl"></a>
### Eigenzeit: schärfere KL-Krümmungsintervalle

**Stand:** MAIN / SOFTWARE; Branch `main`; Commit `e947dfbdd49890dcb119940548537d1db59272c2`.

**Anleitung:** [aktuelle main-Dokumentation](https://github.com/thomasmgfeller/x6-spectral-astrolabium/blob/main/research/lorentz_de_sitter_kl/README.md). **Voraussetzungen:** Python 3.12, gepinnte NumPy-/SciPy-/mpmath-/Matplotlib-Versionen und vollständige Git-Historie. POSIX-Ziellauf: 600 Sekunden und 2 GiB; vollständiger Replay benötigt mehrere Minuten.

**Geprüfte Aussage:** Bernoulli-KL-Schranke für abhängige C2-U-Statistiken: mindestens 95% Überdeckung im bekannten uniformen 4D-de-Sitter-Modell bei festem Budget und 0≤h≤0,5. Hinreichende Budgets sinken gegenüber der Hoeffding-Regel um Faktor 2,71–2,77. 77.824 neue Wolken; bei h=0,5 und M=16.384 qualifizieren vier von vier KL-Intervallen für 20%-Präzision, gegenüber einem von vier mit Hoeffding. Keine präzise Erfolgsratenschätzung, allgemeine Uhr oder Dichteidentifikation.

```sh
python3 -m pip install -r research/lorentz_de_sitter_kl/requirements.txt
python3 -B research/lorentz_de_sitter_kl/verify.py
```

**Erwartung:** PASS_FULL_KL_REPLAY: rationale KL-Gegenprüfung, exakte abhängige Kontrollen, 77.824 reproduzierte Punktwolken, sämtliche Intervall- und Budgetentscheide.

**Vorhandene Evidenz:**

- [research/lorentz_de_sitter_kl/DERIVATION.md](https://github.com/thomasmgfeller/x6-spectral-astrolabium/blob/e947dfbdd49890dcb119940548537d1db59272c2/research/lorentz_de_sitter_kl/DERIVATION.md): Binärer Chernoff-Nachweis mit disjunkter Paarreduktion, rationale KL-Umkehrung und Intervallverschachtelung.
- [research/lorentz_de_sitter_kl/RESULTS.md](https://github.com/thomasmgfeller/x6-spectral-astrolabium/blob/e947dfbdd49890dcb119940548537d1db59272c2/research/lorentz_de_sitter_kl/RESULTS.md): Verfeinerte hinreichende Budgets, alle frischen Gruppen, Präzisionsverweigerungen und Geltungsgrenzen.
- [research/lorentz_de_sitter_kl/contract.json](https://github.com/thomasmgfeller/x6-spectral-astrolabium/blob/e947dfbdd49890dcb119940548537d1db59272c2/research/lorentz_de_sitter_kl/contract.json): Öffentliche Quellenfixierung 09e0cf0 vor Zielbudgetvergleich und 77.824 neuen Wolken.
- [research/lorentz_de_sitter_kl/results/planning.json](https://github.com/thomasmgfeller/x6-spectral-astrolabium/blob/e947dfbdd49890dcb119940548537d1db59272c2/research/lorentz_de_sitter_kl/results/planning.json): Exakte Bruchzertifikate an allen sechs ganzzahligen Budgetgrenzen und unmittelbaren Vorgängerwerten.
- [research/lorentz_de_sitter_kl/VERIFICATION.json](https://github.com/thomasmgfeller/x6-spectral-astrolabium/blob/e947dfbdd49890dcb119940548537d1db59272c2/research/lorentz_de_sitter_kl/VERIFICATION.json): Vollständiger Replay mit getrenntem Kausalitätstest, unabhängiger Hochpräzisionsrechnung und exakten endlichen Kontrollen.

**Nächste Abnahme:** Der vorab fixierte Varianz-/Bennett-Vergleich liegt im Nachfolgemodul lorentz-de-sitter-variance vor: 2,89–4,10-fach kleinere hinreichende Budgets. Diese KL-Referenz bleibt unverändert; externe Prüfung und Dichte-/Zeitskalensensitivität stehen aus.

<a id="lorentz-de-sitter-variance"></a>
### Eigenzeit: analytische Wolkenvarianz und Bennett-Intervalle

**Stand:** MAIN / SOFTWARE; Branch `main`; Commit `e947dfbdd49890dcb119940548537d1db59272c2`.

**Anleitung:** [aktuelle main-Dokumentation](https://github.com/thomasmgfeller/x6-spectral-astrolabium/blob/main/research/lorentz_de_sitter_variance/README.md). **Voraussetzungen:** Python 3.12, gepinnte NumPy-/SciPy-/SymPy-/mpmath-/Matplotlib-Versionen und vollständige Git-Historie. POSIX-Ziellauf: 600 Sekunden und 2 GiB. Vollständiger Replay benötigt mehrere Minuten.

**Geprüfte Aussage:** Analytische Varianzgrenze vollständiger C2-Wolken im bekannten uniformen 4D-de-Sitter-Modell, 0≤h≤0,5. Bennett-Inversion erhält mindestens 95% Überdeckung bei festem Budget; hinreichende Budgets sinken gegenüber KL um Faktor 2,89–4,10. 45.056 neue Wolken: bei h=0,5, M=4.096 qualifizieren fünf von acht Bennett-Intervallen für 20%-Präzision, gegenüber null von acht mit KL. Ein kleines Gruppenintervall ist breiter; keine allgemeine Dominanz oder unbekannte Dichteidentifikation.

```sh
python3 -m pip install -r research/lorentz_de_sitter_variance/requirements.txt
python3 -B research/lorentz_de_sitter_variance/verify.py
```

**Erwartung:** PASS_FULL_VARIANCE_REPLAY: rationale Varianzgrenze, getrennte Kugelschnitt-Geometrie, symbolische Momente, exakte Negativkontrollen und vollständiger Replay von 45.056 neuen Wolken.

**Vorhandene Evidenz:**

- [research/lorentz_de_sitter_variance/DERIVATION.md](https://github.com/thomasmgfeller/x6-spectral-astrolabium/blob/e947dfbdd49890dcb119940548537d1db59272c2/research/lorentz_de_sitter_variance/DERIVATION.md): Überlappende Paare, exakte Lorentz-Momente, uniforme Reihenreste und Zellgrenzen sowie vollständiges Bennett-MGF-Argument.
- [research/lorentz_de_sitter_variance/RESULTS.md](https://github.com/thomasmgfeller/x6-spectral-astrolabium/blob/e947dfbdd49890dcb119940548537d1db59272c2/research/lorentz_de_sitter_variance/RESULTS.md): Alle drei Budgetgewinne, neue Gruppen, erhaltenes Gegenbeispiel zur Intervall-Dominanz und Geltungsgrenzen.
- [research/lorentz_de_sitter_variance/REVIEW.md](https://github.com/thomasmgfeller/x6-spectral-astrolabium/blob/e947dfbdd49890dcb119940548537d1db59272c2/research/lorentz_de_sitter_variance/REVIEW.md): Prüfpaket mit entscheidenden Beweisstellen, Falsifikationsmöglichkeiten und Reproduktionsbefehlen; externe Prüfung offen.
- [research/lorentz_de_sitter_variance/contract.json](https://github.com/thomasmgfeller/x6-spectral-astrolabium/blob/e947dfbdd49890dcb119940548537d1db59272c2/research/lorentz_de_sitter_variance/contract.json): Öffentliche Fixierung b519337 vor Zielbudgetvergleich und neuen Punktwolken.
- [research/lorentz_de_sitter_variance/results/mathematics.json](https://github.com/thomasmgfeller/x6-spectral-astrolabium/blob/e947dfbdd49890dcb119940548537d1db59272c2/research/lorentz_de_sitter_variance/results/mathematics.json): Exakte Dreipunktkoeffizienten und Varianzobergrenzen auf 64 vollständigen Parameterzellen.
- [research/lorentz_de_sitter_variance/VERIFICATION.json](https://github.com/thomasmgfeller/x6-spectral-astrolabium/blob/e947dfbdd49890dcb119940548537d1db59272c2/research/lorentz_de_sitter_variance/VERIFICATION.json): Getrennte Kugelschnitt-Quadratur, 22 Moment-/Profilkontrollen, 200-stellige Bennett-Gegenrechnung und voller Replay.

**Nächste Abnahme:** Externe Prüfung und Replikation anhand des Prüfpakets; anschliessend den Einfluss begrenzter Dichte- und Zeitskalenfehler auf Identifizierbarkeit und Präzisionsfreigabe vorab festgelegt untersuchen. Keine allgemeinen Uhr- oder Stoppzeitbehauptungen.

<a id="lorentz-bd-reference"></a>
### Eigenzeit: geglättete BD-Referenz gegen C2

**Stand:** MAIN / SOFTWARE; Branch `main`; Commit `e947dfbdd49890dcb119940548537d1db59272c2`.

**Anleitung:** [aktuelle main-Dokumentation](https://github.com/thomasmgfeller/x6-spectral-astrolabium/blob/main/research/lorentz_bd_reference/README.md). **Voraussetzungen:** Python 3.12, NumPy 2.3.5, SciPy 1.17.0, C++17-Compiler g++ und vollständige Git-Historie. Der Quellencommit 2d2539123162ddc032b85ba51af56255ca36a906 muss erhalten bleiben. Der gepinnte Originalprüfer fordert bitgleiche Floats und setzt die Original-Rechenumgebung voraus. Die aktuelle README beschreibt zusätzlich den getrennten numerischen Plattformprüfer.

**Geprüfte Aussage:** Geglätteter 4D-Benincasa–Dowker-Operator mit Poisson-Punktzahlen, bekannter physischer Dichte und externer Eigenzeit T=1. 384 Entwicklungs- und 6.144 getrennte Testwolken. Im Hauptfall ist das RMSE-Verhältnis BD/C2 33,34; die vorab lokal fixierten Nutzenkriterien scheitern. C2 nutzt die bekannte de-Sitter-Familie und Modellgrenzen. Nominale Student-Intervalle sind keine garantierten 95%-Intervalle; keine universelle Rangordnung oder allgemeine Krümmungsuhr.

```sh
python3 -m pip install -r research/lorentz_bd_reference/requirements-replay.txt
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 python3 -B research/lorentz_bd_reference/verify.py --archive research/lorentz_bd_reference/results --replay
```

**Erwartung:** Originalumgebung: PASS_FULL_REPLAY für 6.528 Wolken und 102 zusätzliche unabhängige Relationsprüfungen. Für andere Rechner siehe aktuellen README-Einstieg: getrenntes PASS_PORTABLE_NUMERICAL_REPLAY mit offengelegter Gleitkommatoleranz. Fachlicher Entscheid bleibt NO_GO_VARIABLE_CURVATURE_IN_THIS_BUDGET.

**Vorhandene Evidenz:**

- [research/lorentz_bd_reference/RESULTS.md](https://github.com/thomasmgfeller/x6-spectral-astrolabium/blob/e947dfbdd49890dcb119940548537d1db59272c2/research/lorentz_bd_reference/RESULTS.md): Ergebnisse aller zwölf Testzellen, Unsicherheiten, Kosten und Grenzen des NO_GO.
- [research/lorentz_bd_reference/METHODS.md](https://github.com/thomasmgfeller/x6-spectral-astrolabium/blob/e947dfbdd49890dcb119940548537d1db59272c2/research/lorentz_bd_reference/METHODS.md): Operator, Poisson-Sprinkling, Kontinuumsquadratur und vorab lokal festgelegter Vergleich; keine öffentliche Vorregistrierung.
- [research/lorentz_bd_reference/contract.json](https://github.com/thomasmgfeller/x6-spectral-astrolabium/blob/e947dfbdd49890dcb119940548537d1db59272c2/research/lorentz_bd_reference/contract.json): Unveränderter Prüfvertrag mit Budget, Seeds, Entwicklungsauswahl und Abbruchregeln.
- [research/lorentz_bd_reference/VERIFICATION.json](https://github.com/thomasmgfeller/x6-spectral-astrolabium/blob/e947dfbdd49890dcb119940548537d1db59272c2/research/lorentz_bd_reference/VERIFICATION.json): Archivierter vollständiger Nachbau und unabhängige Teilkontrollen.
- [research/lorentz_bd_reference/results/execution.json](https://github.com/thomasmgfeller/x6-spectral-astrolabium/blob/e947dfbdd49890dcb119940548537d1db59272c2/research/lorentz_bd_reference/results/execution.json): Ausführungsumgebung, ursprüngliche Quellenfixierung und gemessener Aufwand.
- [research/lorentz_bd_reference/results/summary.json](https://github.com/thomasmgfeller/x6-spectral-astrolabium/blob/e947dfbdd49890dcb119940548537d1db59272c2/research/lorentz_bd_reference/results/summary.json): Vollständige Kennzahlen und alle Entscheidungen.

**Nächste Abnahme:** Kein Ausbau auf variable Krümmung im geprüften Budget. Externe Replikation bleibt offen. Ein anderer Glättungs-/Skalenplan benötigt einen neuen vorab fixierten Vertrag und frische Testdaten; der lokale d’Alembertian bleibt ein separater Reproduktionszweig.

<a id="lorentz-local-dalembert"></a>
### Lokaler d’Alembertian: intrinsischer Phase-1/2-Pilot

**Stand:** MAIN / SOFTWARE; Branch `main`; Commit `e947dfbdd49890dcb119940548537d1db59272c2`.

**Anleitung:** [aktuelle main-Dokumentation](https://github.com/thomasmgfeller/x6-spectral-astrolabium/blob/main/research/lorentz_local_dalembert/README.md). **Voraussetzungen:** Python 3.12, NumPy 2.3.5, SciPy 1.17.0, C++17-Compiler g++ und vollständige Git-Historie. Quellenfreeze a4ff90306827f6df99048bd2fce61ef96a758f19 muss verfügbar sein.

**Geprüfte Aussage:** Intrinsische längste Ketten und Kausalüberlappungs-Nachbarschaften, BK-Operator und Produktidentitäts-Metriktest in 2+1 Minkowski implementiert. Protokoll und Quellen vor Testdaten öffentlich fixiert. 48 getrennte Testwolken vollständig nachgerechnet. Bei höchster Dichte nur 3/16 verwendbare Nachbarschaften; relative Metrik-RMS-Fehler 3,110 mit glatten und 5,524 mit intrinsischen Feldern (Grenze 0,5). Softwarekontrollen bestehen, fachliche Abnahme scheitert. Keine 3+1-, Konvergenz- oder Krümmungsfreigabe.

```sh
python3 -m pip install -r research/lorentz_bd_reference/requirements-replay.txt
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 python3 -B research/lorentz_local_dalembert/phase12/verify.py
```

**Erwartung:** PASS_NUMERICAL_REPLAY für 48 Testwolken; fachlich HOLD_PHASE3. Koordinatenhashes werden getrennt berichtet. Der historische Vortest bleibt PASS_ASSEMBLY_ONLY.

**Vorhandene Evidenz:**

- [research/lorentz_local_dalembert/PHASE12_RESULTS.md](https://github.com/thomasmgfeller/x6-spectral-astrolabium/blob/e947dfbdd49890dcb119940548537d1db59272c2/research/lorentz_local_dalembert/PHASE12_RESULTS.md): Befund, Verfügbarkeit, Auswahl- und Randfehler sowie Grenzen des HOLD.
- [research/lorentz_local_dalembert/phase12/PROTOCOL.md](https://github.com/thomasmgfeller/x6-spectral-astrolabium/blob/e947dfbdd49890dcb119940548537d1db59272c2/research/lorentz_local_dalembert/phase12/PROTOCOL.md): Vor Entwicklungs- und Testdaten öffentlich fixierter Vertrag.
- [research/lorentz_local_dalembert/phase12/IMPLEMENTATION.md](https://github.com/thomasmgfeller/x6-spectral-astrolabium/blob/e947dfbdd49890dcb119940548537d1db59272c2/research/lorentz_local_dalembert/phase12/IMPLEMENTATION.md): Nach Entwicklungsdaten, vor Testdaten fixierte Umsetzung und Auswertung.
- [research/lorentz_local_dalembert/phase12/results/execution.json](https://github.com/thomasmgfeller/x6-spectral-astrolabium/blob/e947dfbdd49890dcb119940548537d1db59272c2/research/lorentz_local_dalembert/phase12/results/execution.json): Alle Seeds, Rohdatenhashes, Quellenfreeze und gemessene Kosten.
- [research/lorentz_local_dalembert/phase12/results/summary.json](https://github.com/thomasmgfeller/x6-spectral-astrolabium/blob/e947dfbdd49890dcb119940548537d1db59272c2/research/lorentz_local_dalembert/phase12/results/summary.json): Vollständige Kennzahlen, Unsicherheiten und Gates.
- [research/lorentz_local_dalembert/phase12/VERIFICATION.json](https://github.com/thomasmgfeller/x6-spectral-astrolabium/blob/e947dfbdd49890dcb119940548537d1db59272c2/research/lorentz_local_dalembert/phase12/VERIFICATION.json): Vollständiger lokaler numerischer Replay; alle 48 Koordinatenhashes identisch.

**Nächste Abnahme:** Ankersuchabdeckung, Schalenpopulation und Randrobustheit zunächst auf Entwicklungsdaten verbessern. Neuer öffentlicher Vertrag und frische Testseeds für erneute flache Abnahme; keine Phase 3. Früherer BD-C2-NO_GO bleibt unverändert.

## Branch-Inventar und Pflege

Die drei aufeinander aufbauenden Branches Fingerprint → Fabric → Neutral Discovery enthalten auch frühere Module. Zum Snapshot sind die registrierten n=6-, V1-, Fingerprint- und Fabric-Dateien in den jeweiligen späteren Zweigen bytegleich. Die obigen eigenen Modulzweige bleiben die minimalen nachvollziehbaren Einstiege. NQK und Photonic Link bleiben eigenständig.

Ein historischer Branch kann ungemergte Commits haben, obwohl sein Modul bereits via Squash/Cherry-pick in main angekommen ist. Daher sind Commit-Vorsprünge keine Modulreife- oder Integrationsnachweise. Alte Feature-/Publikationsbranches unten sind keine alternativen Empfehlungen zu den main-Einträgen.

| Beobachteter Branch | Tip-Commit | Commits nur dort / nur main | Rolle |
| --- | --- | --- |
| `docs/wolfram-causal-order-v0-1` | [3f8fb920ddef](https://github.com/thomasmgfeller/x6-spectral-astrolabium/commit/3f8fb920ddefd9ede13d0855a14f4bfb1c7b1239) | 0 / 142 | Historischer Entwicklungs-/Publikationszweig |
| `docs/wolfram-zero-failures-v0-1` | [a40a513a9633](https://github.com/thomasmgfeller/x6-spectral-astrolabium/commit/a40a513a9633cbe6aad4ce66132331d9264c0bab) | 0 / 144 | Historischer Entwicklungs-/Publikationszweig |
| `feat/signal-validation-lab` | [33032c23dd0e](https://github.com/thomasmgfeller/x6-spectral-astrolabium/commit/33032c23dd0ef3e035d38c5b9cf7c3db6faf65f0) | 1 / 179 | Historischer Entwicklungs-/Publikationszweig |
| `feature/sagnac-integration-preview-0.1` | [7aaa8e38acc6](https://github.com/thomasmgfeller/x6-spectral-astrolabium/commit/7aaa8e38acc60be556614dd4e4c0ac1697b45815) | 1 / 202 | Historischer Entwicklungs-/Publikationszweig |
| `fix/evidence-audit-20261012` | [680fe6a43e66](https://github.com/thomasmgfeller/x6-spectral-astrolabium/commit/680fe6a43e664164a26dcf1b8cfb6bf52a1b3b56) | 1 / 180 | Historischer Entwicklungs-/Publikationszweig |
| `fix/safe-x6-publish` | [f80225268928](https://github.com/thomasmgfeller/x6-spectral-astrolabium/commit/f802252689284de402a3a322a64a69a07098622f) | 0 / 263 | Historischer Entwicklungs-/Publikationszweig |
| `fix/signal-lab-evidence-archive` | [d43238b4e110](https://github.com/thomasmgfeller/x6-spectral-astrolabium/commit/d43238b4e110ea7338f225334f23c6cde179626e) | 1 / 178 | Historischer Entwicklungs-/Publikationszweig |
| `main` | [e947dfbdd498](https://github.com/thomasmgfeller/x6-spectral-astrolabium/commit/e947dfbdd49890dcb119940548537d1db59272c2) | 0 / 0 | integration, offline-reference, astrolabium, signal-lab, edge-reference, evidence-calibration, phase-contract, industrial-programme, sagnac-import, photonic-design, acvm-concept, acvm-c1, acvm-optical, sagnac-components, acvm-records, acvm-fixture, rax-programme, rax-u1, rax-b1-m1, rax-w1, wolfram-polarity, wolfram-dependence, wolfram-causal, data-agents, lorentz-agent, lorentz-n6-residuals, industrial-v1, industrial-pilot, rax-guarded, reference-edition, x6-qe, rax-cqg-benchmark, lorentz-n7-complete, free-field-entropy, lorentz-proper-time, lorentz-curvature, lorentz-rss-fixed-n, lorentz-proper-time-validity, lorentz-de-sitter-information, lorentz-de-sitter-c2, lorentz-de-sitter-kl, lorentz-de-sitter-variance, lorentz-bd-reference, lorentz-local-dalembert |
| `publication/acvm-c1-v0.1` | [b3def446889b](https://github.com/thomasmgfeller/x6-spectral-astrolabium/commit/b3def446889b34cc25afeb1aad14930199636c22) | 0 / 158 | Historischer Entwicklungs-/Publikationszweig |
| `publication/acvm-optical-v0.2` | [94f08ef30a60](https://github.com/thomasmgfeller/x6-spectral-astrolabium/commit/94f08ef30a60cab4a6534aef9b0d05e1d5b2ff0b) | 0 / 151 | Historischer Entwicklungs-/Publikationszweig |
| `publication/sagnac-components-v0.1-20261015` | [7f0f8b893e5f](https://github.com/thomasmgfeller/x6-spectral-astrolabium/commit/7f0f8b893e5fb91708cb75c1460f880adaf2e519) | 0 / 148 | Historischer Entwicklungs-/Publikationszweig |
| `publication/wolfram-polarity-v0.1-20261015` | [8b6785d55689](https://github.com/thomasmgfeller/x6-spectral-astrolabium/commit/8b6785d556895bcb19856061a681720c3f3ff228) | 0 / 146 | Historischer Entwicklungs-/Publikationszweig |
| `publish/photonic-two-qubit-design` | [8f0cdaad0cd8](https://github.com/thomasmgfeller/x6-spectral-astrolabium/commit/8f0cdaad0cd8823ceb2a3db6f2d9a5815d6134ba) | 1 / 201 | Historischer Entwicklungs-/Publikationszweig |
| `research/lorentz-v1-workpackages` | [f5116b9970a6](https://github.com/thomasmgfeller/x6-spectral-astrolabium/commit/f5116b9970a6b7dc788c18623a8386b4cde33ad4) | 1 / 169 | lorentz-n6 |
| `research/nqk` | [a8fbc70fae3e](https://github.com/thomasmgfeller/x6-spectral-astrolabium/commit/a8fbc70fae3ecb46bfcd8ceb828ce182e533dd04) | 2 / 177 | nqk |
| `research/photonic-link` | [7ff72fcd6a16](https://github.com/thomasmgfeller/x6-spectral-astrolabium/commit/7ff72fcd6a16e9b353d1af277307463f757d3470) | 1 / 176 | photonic-link |
| `research/rax-w1-publication` | [1cd7e4bb7167](https://github.com/thomasmgfeller/x6-spectral-astrolabium/commit/1cd7e4bb71672233058e061d18fae6b249d948ad) | 0 / 162 | Historischer Entwicklungs-/Publikationszweig |
| `research/x6-edge-reference` | [7ac131bcfbab](https://github.com/thomasmgfeller/x6-spectral-astrolabium/commit/7ac131bcfbabd658b38fb1c97686325ac47fa081) | 0 / 169 | Historischer Entwicklungs-/Publikationszweig |
| `research/x6-experiment-fabric-v1` | [a34c59f2b0e2](https://github.com/thomasmgfeller/x6-spectral-astrolabium/commit/a34c59f2b0e2d30c73936363040669941aa8ce09) | 3 / 169 | experiment-fabric |
| `research/x6-fingerprint-v1` | [f22030f2dae0](https://github.com/thomasmgfeller/x6-spectral-astrolabium/commit/f22030f2dae0aa670cdbc450c5e881ce250b36b8) | 2 / 169 | fingerprint |
| `research/x6-integration-v0.1` | [87ca9ad6b12f](https://github.com/thomasmgfeller/x6-spectral-astrolabium/commit/87ca9ad6b12fd87869b393658f2ed6848f876c12) | 0 / 164 | Historischer Entwicklungs-/Publikationszweig |
| `research/x6-neutral-discovery-v1` | [1a02c482d59a](https://github.com/thomasmgfeller/x6-spectral-astrolabium/commit/1a02c482d59a42d554337fb83e0f6d6e6d84b516) | 4 / 169 | neutral-discovery |
| `x6-bounded-math-agent` | [122ba4eb5ac1](https://github.com/thomasmgfeller/x6-spectral-astrolabium/commit/122ba4eb5ac1e7496bf3426b0f3e908d08aa74ff) | 0 / 203 | Historischer Entwicklungs-/Publikationszweig |
| `x6-source-preview` | [24023fd88abd](https://github.com/thomasmgfeller/x6-spectral-astrolabium/commit/24023fd88abd676336098950ea3a08e93eeebfd8) | 0 / 211 | Historischer Entwicklungs-/Publikationszweig |
| `research/lorentz-n6-residuals` | [5eaffee5a594](https://github.com/thomasmgfeller/x6-spectral-astrolabium/commit/5eaffee5a594e2c2c5b86db28a1406dc29168087) | 0 / 133 | Historischer Entwicklungs-/Publikationszweig |
| `hardware/c1-e01-readiness` | [d99b5f8d6d5c](https://github.com/thomasmgfeller/x6-spectral-astrolabium/commit/d99b5f8d6d5cc1294397a7072d136d6209381d57) | 0 / 128 | Historischer Entwicklungs-/Publikationszweig |
| `research/industrial-data-pilot` | [e14eaea1f554](https://github.com/thomasmgfeller/x6-spectral-astrolabium/commit/e14eaea1f55497d397f297d9310e9c6bec1ee6d9) | 0 / 122 | Historischer Entwicklungs-/Publikationszweig |
| `research/validation-reference-release` | [2268fb97f90c](https://github.com/thomasmgfeller/x6-spectral-astrolabium/commit/2268fb97f90cfc09490d0988e4c24e1556c569b5) | 0 / 119 | Historischer Entwicklungs-/Publikationszweig |
| `research/x6-qe-v0.1` | [d81774785916](https://github.com/thomasmgfeller/x6-spectral-astrolabium/commit/d81774785916be76e8642ac9909e61ac5f3743e6) | 0 / 114 | Historischer Entwicklungs-/Publikationszweig |
| `research/curvature-identifiability-v1` | [ced51c97b035](https://github.com/thomasmgfeller/x6-spectral-astrolabium/commit/ced51c97b03525acc5d9ff907e175afce740974a) | 0 / 32 | Historischer Entwicklungs-/Publikationszweig |

Bei einer Modulfreigabe zuerst MODULE_REGISTRY.json aktualisieren: Quellencommit, Einstieg, erwartete Ausgabe, Evidenzrevision und nächste Abnahme. Danach rendern und prüfen:

```sh
python3 tools/module_registry.py --write
python3 tools/module_registry.py --check --git-objects
python3 tests/python/verify_manifest.py
```

Die Prüfung vergleicht JSON und Markdown, vorhandene Hauptzweigpfade, optional alle gepinnten Git-Objekte samt Archiv-Einstiegen sowie UTC/Zürich-Frist und Workflows. Ein Checkout mit vollständiger Git-Historie wird für --git-objects benötigt; bei fehlenden Forschungsobjekten zuerst die im Register genannten Branches fetch-en. Sie führt keine Forschungskommandos, Geräteaktionen oder Agentenläufe aus. Neue wissenschaftliche Befunde benötigen eigene versionierte Evidenz; redaktionelle Registerpflege darf historische Archive und Prüfberichte nicht umschreiben.
