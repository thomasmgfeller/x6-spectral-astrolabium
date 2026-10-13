# X6 PF Experiment Contract – Schema und Vorprüfer v0.2.0

Stand: 13. Oktober 2026. Status: **Entwicklungsartefakt; kein validierter Entrauscher.**

Dieses Paket konkretisiert den vom Nutzer vorgelegten Contract v0.1. Es enthält
JSON Schemas nach Draft 2020-12, einen Python-Vorprüfer und gezielte Softwaretests.
Es führt weder X6 noch Referenzfilter aus und verändert keine laufenden Agenten.

## Dateien und Versionsgrenze

- `original/X6_PF_Experiment_Contract_v0_1.json`: strukturgetreue Übertragung des
  geposteten JSON; Einrückung und Zeilenumbrüche wurden vereinheitlicht. Kein
  Anspruch auf Byteidentität mit dem Chattext.
- `X6_PF_Experiment_Contract_v0_2_DRAFT.json`: ausdrücklich nicht freigegebener
  Nachfolgeentwurf. Fachliche Schwellenwerte bleiben offen.
- `schema/X6_PF_Experiment_Contract_v0_2.schema.json`: immutable Versuchsvorgaben.
- `schema/X6_PF_Input_Manifest_v0_2.schema.json`: Fälle und gehashte Eingabearrays.
- `schema/X6_PF_Execution_Request_v0_2.schema.json`: separater Ausführungsauftrag
  mit Zielsystem, Präzisionsprofil, Implementierung und Ressourcenlimits.
- `preflight.py`: Strukturprüfung, semantische Beziehungen und Integritätsprüfung.
- `tests/test_preflight.py`: temporäre Software-Testfixtures; darin verwendete
  Zahlen sind **keine fachlich festgelegten Akzeptanzschwellen**.
- `validation_report.json`: Ergebnis der Paketprüfung; keine Filterergebnisse.
- `build_schemas.py`: reproduzierbarer Erzeuger der drei Schemas und des Entwurfs.
  Nur im Entwicklungskontext verwenden: er überschreibt den enthaltenen Entwurf.

Die Version 0.2.0 ist absichtlich nicht kompatibel zu v0.1. Eine Migration wird
nicht still ausgeführt. Unbekannte Versionen werden abgewiesen. Implementiert
ist zunächst ausschliesslich das Profil für synthetische Chirp-Versuche mit
vollständig materialisierten Eingaben; reale Daten und Domänenübertragung sind
nicht Gegenstand dieses Schemas. Andere Signalmodelle brauchen ein neues Profil.

## Was gegenüber v0.1 korrigiert wurde

1. Offene Werte haben Status `DRAFT`. Ein `locked: true`-Flag ersetzt keine
   definierten Schwellen, Daten, Filterparameter oder Hashes.
2. Contract, Ausführungsauftrag und spätere Ergebnisse sind getrennt. Ergebnisse
   und Runtime-Fingerprints ändern den ursprünglichen Contract nicht.
3. Kein selbstbezüglicher Contract-Hash im Contract: der Hash liegt ausserhalb.
4. Signalerhalt gehört zur beanspruchten Aussage und ist deshalb obligatorisch.
   Jede benannte Preservation-Metrik braucht eine eigene Grenze mit Einheit
   und Vergleichsbasis. Keine Kompensation zerstörter Impulse durch einen guten
   gewichteten Gesamtscore.
5. Genau ein primärer Qualitätsvergleich wird gewählt. Die ursprünglichen drei
   Kandidaten bleiben als Auswahl erhalten; es wurde keiner still bevorzugt.
6. Signalanfangsphase, zyklische Zeitverschiebung und Filtermittelwinkel sind
   getrennte Achsen. `[-180,180)` vermeidet den doppelten Endpunkt.
7. Die Ausführung nutzt gehashte, gemeinsam verwendete Eingabedateien. Der Seed
   allein ist kein sprachübergreifender Datenbezeichner.
8. Baselines benötigen Version, Quelltext, Parameter und ein separat gehashtes
   Parameterschema. Externe Schema-Referenzen sind im lokalen Vorprüfer verboten.
9. Float32 und Float64 besitzen getrennte Profile. Die Toleranzen sind noch
   offen. Native WebGPU-Float64-Ausführung wird in diesem Profil abgewiesen.
10. `ERROR`, `BLOCKED` und wissenschaftliches `FAIL` haben unterschiedliche
    Bedeutungen. Der Vorprüfer kann niemals einen Filterclaim unterstützen.

## Installation und Aufruf

Python 3.12 wurde geprüft. Für andere Versionen liegt hier kein Prüfnachweis vor.

```bash
python -m venv .venv
.venv/bin/python -m pip install -r requirements.txt
.venv/bin/python preflight.py X6_PF_Experiment_Contract_v0_2_DRAFT.json --mode draft
.venv/bin/python preflight.py X6_PF_Experiment_Contract_v0_2_DRAFT.json --mode preflight
.venv/bin/python -m unittest discover -s tests -v
```

Erwartung: `draft` meldet `DRAFT_STRUCTURE_VALID` und listet offene Punkte.
`preflight` meldet beim gelieferten Entwurf `BLOCKED`, Exitcode 2. Das ist das
gewünschte Ergebnis. Es wurde kein gültiger Produktions-Lock hergestellt.

Für einen später vollständig ausgearbeiteten, fachlich geprüften Contract:

```bash
python preflight.py experiment.json --mode preflight \
  --expected-sha256 VERTRAUENSWUERDIG_REGISTRIERTER_64STELLIGER_HASH \
  --request execution-request.json
```

Die Hashangabe ist ein Platzhalter. Sie muss aus einer vorher festgehaltenen,
vertrauenswürdigen Quelle stammen. Den erwarteten Hash aus einem gerade
empfangenen, unbekannten Bundle neu zu berechnen, beweist keine Unverändertheit.
Ein gesonderter verifizierter Commit oder ein vertrauenswürdiges Register kann
als Anker dienen. Ein Hash allein beweist weder Urheberschaft noch Zeitpunkt.

## Zustände und Rückgabewerte

| Status | Bedeutung | Exitcode |
|---|---|---:|
| `DRAFT_STRUCTURE_VALID` | Grundstruktur und semantische Beziehungen gültig; offene Punkte möglich | 0 |
| `BLOCKED` | Vorprüfung angefordert, aber Pflichtentscheidungen/Anker/Auftrag fehlen | 2 |
| `INVALID` | Struktur-, Bereichs-, Integritäts- oder Konsistenzfehler | 2 |
| `READY_FOR_RUNNER_REVIEW` | Technische Vorprüfung der vorhandenen Dateien bestanden | 0 |

Der letzte Status ist **keine Ausführungsautorisierung und kein wissenschaftlicher
PASS**. Ein Aufrufer muss den passenden Modus und den Status prüfen; Exitcode 0
im Entwurfsmodus erlaubt keine Durchführung. Der Claim bleibt immer `UNVALIDATED`.

Das Schema prüft Typen, Pflichtfelder, Bereiche, Enumerationen und ausgewählte
Bedingungen bei `LOCKED`. Der Vorprüfer übernimmt arithmetische Beziehungen,
Eindeutigkeit von IDs, Fallabdeckung, Dateihashes und Systemfähigkeiten. Insbesondere
kann JSON Schema allein weder `duration = N/fs` berechnen noch die Bytes einer
externen Datei prüfen. `format` ist bei Draft 2020-12 nicht automatisch eine
verbindliche Prüfung: UTC-Zeitangaben prüft der Vorprüfer zusätzlich ausdrücklich.
Schaltsekunden sind in diesem engen Timestamp-Profil nicht unterstützt.

## Festlegung der Bytes und Hashes

Die v0.2 verwendet `SHA256_EXACT_FILE_BYTES_V1`, **nicht** eine behauptete
RFC-8785-Kanonisierung. Hash ist SHA-256 über die unveränderten Dateibytes.

- Contract und JSON-Metadaten: UTF-8 ohne BOM. Keine doppelten Schlüsselnamen,
  NaN/Infinity, überlaufenden Zahlen, unpaarigen Unicode-Surrogate oder Integer
  ausserhalb des exakt interoperablen Bereichs `[-(2^53-1),2^53-1]`.
- Nach Registrierung sind auch Änderungen an Leerraum oder Zeilenenden eine
  Änderung des Contracts. Runner müssen zuerst Originalbytes hashen und dürfen
  den Hash nicht über eine sprachabhängige erneute Serialisierung berechnen.
- Eingaben: je Datei genau N fortlaufende IEEE-754 Binary64-Werte, little-endian,
  ohne Header. Fallmanifest bindet Länge, Abtastrate, Fallkoordinaten und Hashes.
- `path` ist relativ zum Verzeichnis des Contracts. Absolute Pfade, `..`,
  Symlink-Ausbrüche und Netzwerkpfade werden abgelehnt.
- Quelltexte und Spezifikationen sind unveränderte Dateien mit separaten Hashes.
  Jede Ausführung bindet sowohl den gemeinsamen mathematischen Contract als auch
  die tatsächlich verwendete Implementierung und deren Abhängigkeiten.

Ein späteres Ergebnisartefakt sollte Contract-Hash, Request-Hash, Eingabe-
Manifest-Hash, Ausgabearray-Hashes, Laufzeiten, Gates und tatsächlichen Fehlerstatus
binden. Sein eigener Hash muss ebenfalls in einem separaten Manifest liegen.
Ein Ergebnisformat samt Gate-Auswerter ist **noch nicht implementiert**.

Die Vorprüfung schützt gegen Abweichungen vom externen Hashanker. Sie schützt
nicht gegen einen Angreifer, der Contract, alle Hashes und den vertrauenswürdigen
Anker gemeinsam ersetzt. Sie beweist auch nicht, dass ein späterer Runner dieselben
Bytes verwendet: dieser muss die geprüften Bytes als unveränderlichen Snapshot
übernehmen beziehungsweise beim Start erneut prüfen. Keine TOCTOU-Garantie.

## Daten, Seeds, Spektren und Signalerhalt

Der Draft übernimmt fs=1000 Hz und N=4096. `duration_s = N/fs = 4.096`; der letzte
Sample liegt bei 4.095 s. Ob die Chirp-Endfrequenz am letzten Sample oder an der
Dauergrenze erreicht wird, bleibt ausdrücklich offen. Generatorformel, PRNG,
Seedableitung, Normalisierung, DC-Anteil, Spektralabschneidung und Definition von
Pink/Red/Blue sowie gemischten Störungen müssen im Generatorprotokoll festliegen.
Eine gemeinsame `phase_offset_deg` hat für alle Rauschmodelle nicht automatisch
eine eindeutige Bedeutung und wurde deshalb nicht übernommen.

Der Datengenerator wird zunächst einmal ausgeführt, die sauberen und verrauschten
Arrays werden materialisiert und gehasht. JS/Python/WASM/WebGPU und der externe
Solver erhalten dieselben Eingabebytes. Float32-Runner müssen eine spezifizierte
Binary64-zu-Binary32-Konversion verwenden; die Rundung zählt zur numerischen
Qualifikation. Dieses Paket qualifiziert keine dieser Implementierungen.

Der spätere Runner muss saubere Referenzsignale vor Kandidaten und Baselines
abschirmen. Der saubere Kanal gehört ausschliesslich zum Evaluator. Zusätzliche
Referenzkanäle etwa für einen LMS-Rauschkompensator sind in diesem Profil nicht
modelliert: eine solche Variante darf hier nicht still als Ein-Kanal-Verfahren
geführt werden. Adaptive Ein-Kanal-Verfahren erfordern eine genaue Spezifikation.

Die aktuelle X6-Phasenmaske besitzt ein bekanntes Gegenbeispiel zur allgemeinen
Zeitverschiebungsinvarianz. Das unveränderte Paarregel-Verhalten des vorhandenen
Kerns muss aus dessen Quelltext übernommen und gehasht werden. Die v0.2 entscheidet
nicht ungeprüft zwischen Paarregeln. Ebenso bleiben DC/Nyquist, Nullkoeffizienten,
DFT-Normierung und Grenzvergleich fachlich festzulegen. `preserve_conjugate_symmetry`
als Boolean wäre dafür nicht ausreichend.

Ein harter Phasenschwellwert ist diskontinuierlich: winzige Rundungsunterschiede
können eine grosse Spektralkomponente anders klassifizieren. Daher braucht das
Portabilitätsprofil neben absoluten/relativen Toleranzen eine Bandgrenze, innerhalb
deren der Vergleich als unentschieden behandelt oder mit höherer Präzision geprüft
wird. Eine pauschale Toleranz 1e-10 wird nicht für Float32 übernommen.

## Aufwand des Entwurfs

Unter der Annahme „1'000 Wiederholungen pro vollständiger Kombination“ besitzt
die ursprüngliche inklusive Winkelachse 37 Einträge und damit
9 × 37 × 6 × 8 × 1'000 = **15'984'000 Kandidatenauswertungen**.

Die v0.2 entfernt den doppelten Winkelendpunkt und trennt Daten- von Filterachsen:

- 8 Rauschmodelle × 9 SNR-Stufen × 1 Signalphase × 1 Verschiebung × 1'000
  Wiederholungen = **72'000 Eingabefälle**;
- 36 Winkel × 6 Breiten = **216 Kandidateneinstellungen**;
- **15'552'000 Kandidatenauswertungen**;
- 8 Baselines einmal je Eingabefall = **576'000 Baseline-Auswertungen**;
- insgesamt **16'128'000 logische Auswertungen**, ohne Generator, Tuning und
  zusätzlichen Referenzsolver. Vollständige Arrays für jede einzelne Ausgabe
  hätten zusätzlich erheblichen Speicherbedarf.

Dies ist eine Planzählung, kein ausgeführter Benchmark und keine Laufzeitprognose.
Zusätzliche Signalphasen/Verschiebungen multiplizieren den Aufwand. Die einzige
derzeit vorgesehene Signalphase/Verschiebung belegt keine allgemeine Robustheit.
Ressourcenbudgets bleiben null und blockieren Ausführung. Der Vorprüfer hat
zusätzlich technische Grenzen von 100'000 Manifestfällen und 64 MiB je JSON-/Array-
Datei. Budgetfelder allein erzwingen keine Ressourcenbegrenzung; der spätere Runner
muss Timeout, Speicherlimit, Abbruch und Ergebnisstatus tatsächlich durchsetzen.

## Noch vor einem bestätigenden Versuch zu entscheiden

1. Betriebsregion und primäre Vergleichsbaseline; faire Abstimmung aller Methoden.
2. Exakte mathematische Spezifikation und unveränderte Quelltexte.
3. Einheiten und Formeln der Metriken; keine günstige nachträgliche Zeit-/Gain-
   Anpassung gegen Ground Truth. Transform-Rekonstruktion prüft DFT/IFFT ohne
   Filtermaske, nicht die Identität eines tatsächlich gefilterten Signals.
4. Mindestnutzen, individuelle Signalerhalt-Grenzen und geeignete Unsicherheits-
   intervalle. q05/q95 der Ergebnisverteilung sind keine Konfidenzintervalle für
   den mittleren oder medianen Vorteil. Bei gleichem Referenzsignal sind RMSE
   und rekonstruktionsbasiertes SNR eng gekoppelt und keine unabhängigen Belege.
5. Analyseeinheit, Stichprobenplanung und Mehrfachvergleichskorrektur. Eine grosse
   Sweep-Suche wird explorativ ausgewertet; ein ausgesuchter Gewinner braucht
   neue unabhängige Bestätigung.
6. Geprüfte Spezifikationen für einzelne Gates. Kein ausgewogener Gesamtscore darf
   einen verletzten Signalerhalt-Grenzwert kompensieren. Fehlende Gate-Ergebnisse
   können keinen Claim freigeben. Nichtsignifikanz beweist keine Nichtunterlegenheit.
7. Holdout-Registry, Sperrzeitpunkt, Unabhängigkeit und Zugriffstrennung. Hashes
   beweisen nicht, dass niemand die Testdaten zuvor angesehen hat. Ein systematisch
   durch Entwicklung beeinflusster Generator ist auch mit neuem Seed kein universell
   unabhängiger Praxistest. Versionswechsel erzeugt ein neues Studienprotokoll.

Die Vorprüfung prüft Existenz, Hash und passende Datentypen dieser referenzierten
Festlegungen. Sie beurteilt deren fachlichen Inhalt nicht automatisch. Ein Text
mit einem korrekten Hash kann wissenschaftlich unzureichend sein. Deshalb heisst
der technische Endstatus `READY_FOR_RUNNER_REVIEW`.

## Referenzen

Primärquellen, aufgerufen am 13.10.2026:

- JSON Schema Draft 2020-12: https://json-schema.org/draft/2020-12
- Format-Annotation und Format-Assertion:
  https://json-schema.org/draft/2020-12/json-schema-validation
- RFC 8785, JSON Canonicalization Scheme (Alternative zur hier gewählten strikten
  Bytebindung, nicht in diesem Paket implementiert):
  https://www.rfc-editor.org/rfc/rfc8785
- W3C WGSL, Skalar- und Gleitkommatypen:
  https://www.w3.org/TR/WGSL/#floating-point-types
- Lakens (2017), Equivalence Tests: A Practical Primer:
  https://pmc.ncbi.nlm.nih.gov/articles/PMC5502906/
- NIST, Mehrfachvergleiche:
  https://itl.nist.gov/div898/handbook/prc/section4/prc47.htm

Projektbeleg zum bereits gefundenen Phasengegenbeispiel:
https://github.com/thomasmgfeller/x6-spectral-astrolabium/actions/runs/38400568957

Keine dieser Quellen ist eine Bestätigung der Leistungsfähigkeit von X6.
