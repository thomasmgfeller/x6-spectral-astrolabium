# CST-DUST: Detektorkopplung und notwendige Historienmischung v0.1

Analytischer Prüfschritt nach PR 261. Keine kostenpflichtige Rechenleistung
und kein n=5-Produktionslauf. Alle acht physikalischen Gates bleiben **HOLD**.

## Ergebnis

Eine feste Hilfssystemkopplung, die die erklärten Historienrecords nicht
mischt, erzeugt nur diagonale Messeffekte. Für den balancierten
Rang-eins-Rückkehrprojektor des Referenzmodells ist der universelle
Operatornormfehler daher mindestens **1/2**, und diese Grenze ist scharf.
Pointerpulse, klassische Rückkopplung und Postselektion innerhalb dieser
Klasse beheben das Problem nicht.

Für eine beschränkte zusätzliche Kopplung V(t) liefert
`gamma = integral ||V(t)|| dt / hbar` die notwendige Bedingung
`tau >= max(0, 1/2 - gamma)`. Dies ist keine hinreichende Konstruktion,
kein optimierter Speed-Limit-Satz und keine Aussage über Geldkosten.

Ein zweidimensionaler Mischkontrollfall verlässt die eingeschränkte Klasse
und realisiert den Zielprojektor. Er ist kein physikalischer CST-Detektor.
Ein zusätzlicher dritter Modus zeigt die Einbettungsfalle: Auf dem Testblock
Fehler null, auf dem vollständigen Raum Fehler eins.

**Reichweite:** Keine Gleichsetzung von Ortslokalität und Diagonalität im
Historienraum. Kein allgemeines Verbot lokaler Feldkopplungen oder anderer
Messprotokolle. Der Satz gilt auf dem erklärten Referenzraum mit den
angegebenen Testzuständen; physikalische CST-Constraints sind weiterhin offen.

## Dateien und Reproduktion

- Das PDF ist die kompakte Lesefassung.
- `DERIVATION.md` enthält alle Beweise, Gültigkeitsbedingungen und Quellen.
- `coupling_contract.json` dokumentiert den ausgeschiedenen Kandidaten und
  die Anforderungen an einen physikalisch begründeten Mischterm.
- `plan.json` ist nach dem algebraischen Entwurf und vor den endlichen
  Rechnungen eingefroren; keine externe Präregistrierung.
- `provenance.json` pinnt vier Originalquellen mit Git-Blob-Identitäten.

ZIP vollständig entpacken und im Paketverzeichnis ausführen:

```sh
python3 -B verify_package.py
python3 -B replay.py
```

`analyze.py` erzeugt vier wissenschaftliche Ergebnisdateien mit exakten
rationalen komplexen Zahlen. `replay.py` erzeugt sie isoliert erneut und
verlangt Bytegleichheit. Die Python-Standardbibliothek genügt. Kein
Netzzugriff, keine Zugangsdaten und keine Zusatzpakete sind erforderlich.
Die geerbte `inputs/previous_core.py` wird nur für ihre exakten Matrixhelfer
importiert; ihr früherer Analysehauptlauf wird nicht ausgeführt.

Kontrolliert werden 75 gemeinsame Unitaritäten, 900 reduzierte Effekte,
25 rückgekoppelte Instrumente mit 100 Zweigen, 25 diagonale Effektfälle,
drei gewichtete Darstellungen, sechs rationale Mischrotationen, ein
idealer Mischkontrollfall, ein Einbettungsgegenbeispiel und sieben
Negativkontrollen. Die allgemeinen Sätze beruhen auf den Beweisen;
die kleinen Matrizen sind keine Quadratur kontinuierlicher CST-Historien.

Die Nachrechnung ist keine externe Replikation oder Beweisassistentenprüfung.
`build_report.py` ist optional und benötigt ReportLab sowie DejaVu-Schriften
unter `/usr/share/fonts/truetype/dejavu/`. `package.py` erzeugt Manifest und
ZIP mit festen Archivzeitstempeln. PDF-Metadaten können beim Neurendern
variieren; die Bytegleichheit gilt den wissenschaftlichen Ergebnisdateien.

Nächste physikalische Aufgabe: einen aus der Materie-/Randdynamik
begründeten Mischterm prüfen, einschließlich Zustandsdomäne, Kausalität,
vollständigem Effekt, Ausfallausgang und Rückwirkung. Der abstrakte
Zweimodenoperator ersetzt diese Herleitung nicht.

Lizenz: Apache-2.0, siehe `LICENSE` und `NOTICE`.
