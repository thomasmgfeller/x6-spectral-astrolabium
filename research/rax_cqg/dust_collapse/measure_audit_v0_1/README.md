# CST-DUST: Maßabhängigkeit und Zustandstransport v0.1

Analytischer Prüfstand vom 7. November 2026, basierend auf Main nach PR 258
(`3177458a7f8545f845054e235cd3dcd7e829eff3`). Kein n=5-Produktionslauf und
keine kostenpflichtige Rechenleistung. Die wissenschaftliche Rechnung
verwendet ausschließlich exakte rationale Arithmetik der Python-Standardbibliothek.

## Ergebnis und Reichweite

Gleicher Nullanteil, Mittelwert und gleiche Varianz des Materiemaßes legen
die kohärente Auslese mit jeweils konstanten Randvektoren nicht eindeutig
fest. Acht vorher festgelegte Gegenvergleiche im bedingten Ein-Element-Kanal
sind durch rationale Intervalle von null getrennt.

Dies allein belegt keine physikalische Ungleichwertigkeit. Alle untersuchten
Maße sind äquivalent. Werden beide Randvektoren korrekt mit der
Radon-Nikodym-Dichte transportiert, bleiben die betrachteten Matrixelemente
exakt gleich. Im gemeinsamen Hilbertraum entsprechen konstante Vektoren
unter verschiedenen Maßen unterschiedlichen Präparationen und Auslesen.

Der Darstellungssatz ist keine Herleitung unitärer CST-Zeitentwicklung.
Gleiche erste zwei Wirkungs-Momente beweisen weder gleiche klassische
Dynamik noch die physikalische Zulässigkeit dieser Maßfamilie.
MODEL, CURRENT, CORRESPONDENCE, BOUNCE, REGULARITY, BOUNDARY, TRAPPING und
EXTENSION bleiben **HOLD**.

## Lesen

- `CST_DUST_Massabhaengigkeit_Zustandstransport_v0_1.pdf`: sechsseitiger Bericht.
- `DERIVATION.md`: vollständige elementare Beweise, Grenzen und Quellen.
- `plan.json` und `plan.sha256`: vor der endlichen numerischen Auswertung
  eingefrorener Plan; keine externe Präregistrierung.
- `supplement.json`: nach Planfixierung ergänzte Interpretation zum
  Zustandstransport. Parameter und Fehlerordnungen wurden nicht verändert.
- `provenance.json`: vier unverändert übernommene Rechenmodule mit
  Originalpfaden und Git-Blob-Identitäten.
- `results/`: exakte Ergebnisse und Prüfprotokolle. Brüche sind Zeichenketten
  in der Form `Zähler/Nenner`, Dezimalwerte im Bericht nur Lesefassungen.

Die Formulierung „same readout“ im ursprünglichen Plan bedeutet die gleiche
Vorschrift konstanter normierter Randvektoren. Sie identifiziert nicht von
selbst dieselbe physikalische Auslese über verschiedene Maßdarstellungen.
Diese Unterscheidung wird im offengelegten Supplement präzisiert.

## Reproduktion

ZIP vollständig entpacken und in dessen Hauptverzeichnis ausführen:

```sh
python3 -B verify_package.py
python3 -B replay.py
```

Der erste Befehl kontrolliert Paket-Hashes, den eingefrorenen Plan und die
Quellidentitäten. Er beweist keine Urheberschaft. Der zweite berechnet sechs
Ergebnisdateien in einem temporären Verzeichnis erneut und verlangt
Bytegleichheit. Dies ist Reproduzierbarkeit derselben Implementierung,
keine unabhängige externe Replikation oder Beweisassistentenprüfung.

Für die direkte Neuberechnung im Arbeitsverzeichnis:

```sh
python3 -B analyze.py
python3 -B transport_controls.py
```

Es sind keine Netzwerkverbindung, Zugangsdaten, Cloudkonten oder
Python-Pakete erforderlich. Die beiden wissenschaftlichen Skripte
benutzen ausschließlich die Standardbibliothek. Ihre elementaren
Polynom- und Momentrechnungen ersetzen keine große Feldquadratur.

`build_report.py` ist optional und benötigt ReportLab sowie DejaVu-Schriften
unter `/usr/share/fonts/truetype/dejavu/`. Ein neu erzeugtes PDF kann andere
Metadaten erhalten. Nach beabsichtigten Änderungen erzeugt
`python3 -B package.py` ein neues Manifest und ein ZIP mit festen
Archivzeitstempeln. Die Bytegleichheitsforderung gilt den sechs
wissenschaftlichen Ergebnisdateien; ein geändertes Paket ist entsprechend
neu zu versionieren.

## Nächster physikalischer Schritt

Präparation und Messauslese operational und unabhängig von der
Maßdarstellung festlegen. Anschließend prüfen, welche zusätzliche
physikalische Bedingung die offene Zustandswahl einschränkt.

Die bestehende kostenneutrale Community-Anfrage für n=5 betrifft weiterhin
den ursprünglichen Referenzfall und wurde durch diese Analyse nicht geändert:
https://github.com/thomasmgfeller/x6-spectral-astrolabium/issues/259

Lizenz: Apache-2.0, siehe `LICENSE` und `NOTICE`.
