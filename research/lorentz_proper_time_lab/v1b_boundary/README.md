# V1b: endliche Randwerte und nativer Browser-/Exportnachweis

**Technischer Abschluss: PASS. Gesamtstatus: NOT_PASSED.** Randwertreparatur,
nativer Vergleich und tatsächlicher Chromium-/Exportnachweis sind bestanden.
Die geerbte radiale 4D-Diagnostik bleibt FAIL (p=0,0110616450 bei unveränderter
Einzeltestgrenze 0,05). Ein grüner Softwarejob ist kein V1b-PASS.

Die [Originalberichte und Rohdaten](results/) sind vollständig und unverändert
im Repository eingefroren. [Publikationsnachweis](PUBLICATION.json) und
[SHA-256-Index](results/SHA256SUMS) binden sie an den ursprünglichen CI-Lauf.

## Reparatur und mathematische Grenze

`core.js` Version `x6.proper-time-lab/1.1` verwendet weiterhin denselben
Mulberry32-Stream, dieselbe Normaltransformation, dieselben Exponenten und
denselben strikten Zugehörigkeitstest. Die zusätzliche Regel
`strict-interior-rejection/1` lautet:

1. Ein zeitlicher Uniformwert U_A=0 verwirft den Kandidaten sofort.
2. Andernfalls wird die bisherige Punkttransformation unverändert ausgeführt.
3. Eine ungültige Richtung oder ein nicht endlicher beziehungsweise nicht
   strikt innerer Punkt wird verworfen. Der nächste Kandidat nutzt die nächsten
   PRNG-Werte; bereits verbrauchte Werte werden nicht zurückgesetzt.
4. Nach höchstens 128 Kandidaten für einen Punkt wird ein Fehler ausgelöst.
   `cloud()` gibt dann kein Teilergebnis zurück.

Es wird weder ein Punkt auf eine künstliche Innenposition verschoben noch
`<` zu `<=` gelockert. Der Export enthält Richtlinienversion, Zahl der Versuche
und Verwerfungen nach Ursache. Seed `2463401483` verwirft seinen ersten
zeitlichen Nullwert und liefert anschließend strikt innere Punkte.

Im idealen kontinuierlichen Modell haben U_A=0, die Nullrichtung und der
Rand Wahrscheinlichkeit null. Eine Verwerfung ausschließlich solcher
Nullmengen verändert dessen Volumengesetz nicht. Die Rundungsprüfung ist
hingegen eine Eigenschaft der endlichen Implementierung: Rejection konditioniert
ihre Kandidatenverteilung. Für den deterministischen PRNG wird daraus weder
exakte stetige Gleichverteilung noch Unabhängigkeit abgeleitet. Es gibt hier
keine globale Schranke für die dadurch verursachte endliche Abweichung.

Die feste bisherige Matrix enthält keine Verwerfungen: alle 196.608 Punkte
und ihre Zugehörigkeitsflags bleiben byte-/wertgleich zum nativen Original.
Die mathematische V1-Aussage unter idealen Eingaben bleibt bestehen.

## Kriterien und Provenienz

`protocol.json` wurde vor dem neuen Matrixlauf als lokaler Commit
`5b33a93` festgeschrieben. Bekannte Befunde, insbesondere p≈0,01106, sind darin
offengelegt. Die lokale Testentwicklung korrigierte vor dem Matrixlauf einen
synthetischen Rundungsrandfall von A=1/4 auf A=1/8; es wurden keine statistischen
Seeds, Schwellen, Testfamilien oder Samplerparameter anhand von Ergebnissen
geändert.

Die Ausgangsdokumente vom 20.10.2026 heißen `V1_sampling_geometry.md` und
`V1b_finite_implementation_regression.md`. Der zweite Bericht verwendete den
inzwischen nachgewiesenen fehlerhaften Python-Port; sein CONDITIONAL PASS und
seine PRNG-Sollvektoren sind durch den
[Portkorrektur-Nachweis](../v1b_port_correction/README.md) überholt. Die dort
festgelegten Dimensionen/Seeds, die θ-Reihe 0,10–0,85 in 0,05-Schritten und
die KS-Einzeltestgrenze 0,05 bleiben erhalten. Die korrekten Sollvektoren
stammen aus dem eingefrorenen nativen Original, nicht aus dem fehlerhaften Port.

Der ursprüngliche Bericht gab für räumliche Momente und die erweiterte
Zählmatrix keine vollständige quantitative Regel an. Die jetzigen zusätzlichen
6-Standardfehler-Momentprüfungen und 192 binomialen Prüfungen mit
Bonferroni-Familienniveau 0,05 sind ausdrücklich neue, vor diesem Lauf
festgelegte Diagnostik. Sie ersetzen und lockern die alte KS-Regel nicht.

## Testumfang

- 40.000 PRNG-Ausgaben exakt gegen die eingefrorene native Referenz.
- 12 Wolken mit insgesamt 196.608 Punkten; d=2,3,4 und vier unveränderte Seeds.
- 192 Kombinationen aus Dimension, Seed und θ; Punkte unabhängig von θ,
  Zugehörigkeitsflags und Zählungen exakt geprüft.
- Bekannter Randseed in allen Dimensionen, 15 injizierte Extremfälle,
  strikt innere/äußere Nachbarn der Innergrenze, begrenzter Abbruch.
- Unabhängige Decimal-Prüfung mit 80 Stellen auf den tatsächlichen
  binary64-Koordinaten und Vergleich mit separat repariertem Python-Port.
- Chromium: tatsächliche UI-Eingaben und JSON-Downloads für alle 192 Fälle,
  erneute Generierung und bytegleicher Zweitexport; zusätzlich Randseed,
  Exportblockade nach ungültiger Eingabe und exportierte Einzel-HTML-Datei.
- Zeit-/Radialdiagnostik je Dimension mit 65.536 gepoolten Punkten.

Browser- und Node-Koordinaten dürfen sich innerhalb
`1e-12 + 1e-12*abs(reference)` unterscheiden; PRNG-Werte, Flags und Zählungen
müssen exakt übereinstimmen. Bytegleichheit wird nur für Wiederholung im
gleichen dokumentierten Browser zugesichert, nicht über verschiedene Engines.

## Reproduktion und Gate-Verhalten

Im Repository-Stamm mit den in `protocol.json` angegebenen Versionen:

```sh
python -m pip install -r research/lorentz_proper_time_lab/v1b_boundary/requirements.txt
npm install --no-save --package-lock=false --ignore-scripts playwright@1.62.1
npx playwright install --with-deps chromium
python research/lorentz_proper_time_lab/build.py --check
node research/lorentz_proper_time_lab/v1b_boundary/native.cjs /tmp/v1b-run
node research/lorentz_proper_time_lab/v1b_boundary/browser.cjs /tmp/v1b-run
python research/lorentz_proper_time_lab/v1b_boundary/analyze.py /tmp/v1b-run
python research/lorentz_proper_time_lab/v1b_boundary/analyze.py /tmp/v1b-run --require-overall
```

Der letzte Befehl liefert Exitcode 2, solange V1b insgesamt nicht besteht.
Ohne `--require-overall` führt fehlende/fehlerhafte technische Evidenz zu einem
Fehlercode; statistische Ablehnungen werden vollständig als FAIL im Bericht
gespeichert. `--native-only` kennzeichnet einen unvollständigen lokalen Lauf
mit Browsergate OPEN und darf kein Browser-PASS erzeugen.

`native_raw.json.gz`, `python_raw.json.gz`, zwölf rohe Browser-JSON-Exporte
sowie `native_report.json`, `browser_report.json` und `qualification.json`
bilden die Evidenz. Jeder Bericht bindet Quell- und Testdateien über SHA-256;
der Browserbericht enthält Chromium-, V8- und Playwright-Version sowie die
Hashes beider Downloads aller Fälle. Der CI-Quellstand ist eine konkrete
Git-Commit-ID. Die ursprünglichen Portkorrektur-Dateien bleiben unverändert.

## Eingefrorener Abschlussnachweis vom 20.10.2026

Der erfolgreiche [CI-Lauf 39444754096](https://github.com/thomasmgfeller/x6-spectral-astrolabium/actions/runs/39444754096)
prüfte PR-Head `4719f96e2ea69d8a7d5ec5543f1b02f7f563505c` über den synthetischen
GitHub-Merge-Checkout `8262c6f36698e25073571fc61f56427ea2c475f8`. Dieser Checkout
ist die Quellreferenz der Berichte und nicht die spätere Publikations-Commit-ID.
Alle elf aufgezeichneten Quellhashes stimmen mit den veröffentlichten Dateien
überein; dieser Abschluss ergänzt ausschließlich Evidenz, Dokumentation und
Prüfsummen.

| Prüfung | Ergebnis |
| --- | --- |
| Native Regression und reparierter Python-Port | PASS |
| Strikter Support, unabhängige Decimal-Prüfung | PASS; 0 Verletzungen |
| Tatsächliche Browser-/Exportprüfung | PASS; 192 Matrixfälle, 196 Replay-Paare |
| Zeitmarginalen, zusätzliche Moment- und Zähldiagnostik | PASS |
| Geerbte radiale 4D-Diagnostik | FAIL; p=0,01106164503413279 < 0,05 |
| V1b gesamt | NOT_PASSED |

Runtime: Node v24.21.0, Python 3.12.15, NumPy 2.3.5, SciPy 1.17.0;
Chromium 151.0.7922.34, Browser-V8 15.1.206.8, Playwright 1.62.1.
Der größte Browser-/Node-Koordinatenunterschied beträgt
2,220446049250313e-16; der größte Inferenzunterschied 7,654987754790454e-14.
Beide liegen innerhalb der vorab festgelegten Toleranz.

Das originale GitHub-Artefakt (17.622.165 Bytes) wurde heruntergeladen und
gegen den von GitHub gemeldeten SHA-256-Digest geprüft. Alle 18 enthaltenen
Dateien liegen bytegleich in `results/`, darunter native und Python-Rohdaten,
zwölf komprimierte Browserexporte und die exportierte Einzel-HTML-Datei.
Die dauerhafte Repository-Kopie bleibt unabhängig vom Ablauf des temporären
Actions-Artefakts am 18.01.2027 verfügbar.

Prüfsummenprüfung vom Repository-Stamm:

```sh
(cd research/lorentz_proper_time_lab/v1b_boundary/results && sha256sum -c SHA256SUMS)
```

Die Quelldateien sind in `results/qualification.json` unter
`provenance.source_sha256` festgehalten. Für neue Reproduktionen immer einen
separaten Ausgabeordner verwenden; die eingefrorenen Originaldateien nicht
überschreiben. Der technische Publikationsschritt ist damit abgeschlossen.
Die Ursache des statistischen Befunds bleibt als eigener Forschungsauftrag offen.

## Konsequenz

Der Randfehler erklärt die radiale Auffälligkeit nicht: Die diagnostizierten
Punkte sind unverändert. V1b bleibt deshalb NOT_PASSED. Die nächste
wissenschaftliche Untersuchung muss den bereits sichtbaren radialen Befund
gezielt lokalisieren und einen neuen, vorher festgelegten unabhängigen
Kontrollvergleich planen. Es wird in diesem Reparaturlauf weder ein anderer
Generator gesucht, bis die alten Seeds bestehen, noch nachträglich die
Signifikanzschwelle verändert.

English: The strict-support defect is repaired without altering the frozen
ordinary sample. Native browser/export replay is a separate engineering gate.
The inherited 4D radial screen still rejects at alpha=0.05; overall V1b is not
passed. No physical validation or universal PRNG-quality claim follows.
