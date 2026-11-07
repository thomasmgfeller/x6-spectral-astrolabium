# CST-DUST: Stratumwechsel, Randkopplung und Zustandsauswahl v0.1

Analytischer Folgeschritt nach PR 262. **Alle acht physikalischen Gates
bleiben HOLD.** Kein großer oder kostenpflichtiger Rechenlauf.

Die vorhandene Wirkung qualifiziert noch keine Quantenkopplung zwischen
vollständigen Historien. Die bisherige 1/2-Fehlergrenze wird auf alle
stratumerhaltenden Effekte erweitert: Beliebige Mischung innerhalb des
positiven Dichtebereichs genügt nicht, wenn das Dichte-Nullatom abgetrennt bleibt.

Eine ausdrücklich zusätzliche Randform auf `C + L2(0,1)` wird vollständig
ausgearbeitet: selbstadjungierter Operator, Definitionsbereich,
Wahrscheinlichkeitsfluss, kohärenter Grundzustand und positive Lückenschranke.
Sie ist **mathematisch konsistent, physikalisch nicht ausgewählt**. Zwei
Randvorzeichen wählen bei festem Ziel unterschiedliche Zustände aus.

Weitere Kontrollen zeigen:

- Ein reiner Dichtefilter lässt unendlich viele Uhrmoden offen; sein
  vollständiger Effekt kann vom Ziel in Operatornorm um eins abweichen.
- Die unbeschränkte Randspur fällt nicht ohne Weiteres unter das frühere
  Normbudget für beschränkte Zusatzoperatoren.
- Wird die geerbte Materiewirkung zusätzlich als Potential eingesetzt,
  ist der konstante Zielzustand bei nichtverschwindender Kopplung kein
  Eigenzustand mehr. Das ist ein bedingter Residualtest, keine physikalische
  Identifikation von Wirkung und Hamiltonoperator.

`DERIVATION.md` enthält die vollständigen Beweise und Quellen. Der PDF-Bericht
fasst die Ergebnisse zusammen. `selection_contract.json` trennt den
analytischen Befund, das Zusatzmodell und die offene physikalische Auswahl.

## Reproduktion

Das ZIP vollständig entpacken und im Paketverzeichnis ausführen:

```sh
python3 -B verify_package.py
python3 -B replay.py
```

Nur die Python-Standardbibliothek ist erforderlich. Kein Netzzugriff,
keine Zugangsdaten, kein Cloud-Dienst und keine Fremdrechenleistung.
Der lokal nach dem analytischen Entwurf eingefrorene Plan ist keine externe
Präregistrierung. Sechs Quellen sind mit Git-Blob-Identitäten gepinnt.
`inputs/exact_core.py` wird nur für rationale komplexe Matrixhelfer importiert;
sein geerbter Hauptlauf wird nicht ausgeführt.

36 Blockeffekte, 72 gewichtete Randmatrizen, 72 rationale Cayley-Unitaritäten,
216 Green-Identitäten, 72 Flussbilanzen, sechs Uhrmodenkontrollen,
45 Wirkungspunkte, neun Residualfälle und sieben Negativkontrollen werden
exakt geprüft. Vier wissenschaftliche Dateien werden isoliert bytegleich
reproduziert. Die Cayley-Abbildung ist ein Kontrolloperator, keine exakt
ausgewertete Zeitexponentialfunktion. Die kleinen Gitter sind endliche
Analoga ohne hier zertifizierten kontinuierlichen Konvergenzfehler.

`build_report.py` benötigt optional ReportLab und DejaVu-Schriften.
`package.py` erstellt das Manifest und ein ZIP mit festen Zeitstempeln.
Die Bytegleichheit bezieht sich auf die wissenschaftlichen Resultate;
PDF-Metadaten können beim Neurendern variieren. Die Nachrechnung ist keine
externe wissenschaftliche Replikation oder Beweisassistentenprüfung.

Nächster physikalischer Entscheidungspunkt: Sind kohärente Übergänge zwischen
Dichte-Nullatom und positivem Stratum im physikalischen Raum zulässig und
aus welcher Quantenalgebra/Dynamik folgen sie? Bei einer tatsächlichen
Superselektion muss der Zielvertrag angepasst werden. Das Zusatzmodell
liefert darauf noch keine Antwort. Auch ein Grundzustand allein legt weder
Präparation noch Detektor oder Rückwirkung fest.

Lizenz: Apache-2.0; siehe `LICENSE` und `NOTICE`.
