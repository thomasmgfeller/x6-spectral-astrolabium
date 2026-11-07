# CST-DUST: Randgedächtnis und exakte Fortsetzung v0.1

7. November 2026. Die vollständige Vergangenheit ist eine hinreichende
Zustandsdarstellung der geerbten endlichen Amplitude. Der Wirkungszuwachs beim
Anfügen eines maximalen Elements und die korrekte Zählung natürlicher Labels
sind exakt hergeleitet und geprüft. Das ist eine Umschreibung des bestehenden
festen Elementzahlsektors, keine neue physikalische Wachstumsdynamik.

**Ein fester oberer Ordnungskragen genügt nicht für alle erlaubten zukünftigen
Ideale.** Eine allgemeine Gegenbeispielfamilie behält Ordnung, alte Wirkung und
sichtbaren Kragen bei, verändert aber eine verborgene Vakuumuhr. Eine spätere
Verzweigung unterscheidet die Fälle mit einem exakten Wirkungsunterschied von
1/16. Andere Kompressionen, eingeschränkte Träger und kontrollierte Näherungen
sind dadurch nicht ausgeschlossen.

[Bericht (PDF, sechs Seiten)](../reports/CST_DUST_Randgedaechtnis_Fortsetzung_v0_1.pdf) ·
[Originales Prüfpaket (ZIP)](../packages/CST_DUST_Randgedaechtnis_Fortsetzung_v0_1_Pruefpaket.zip) ·
[Vollständige Herleitung](DERIVATION.md) ·
[Zustandsvertrag](boundary_contract.json) ·
[Ergebnisse und Entscheidungen](results/verification.json)

## Ergebnisse und Grenzen

- Die zwölf Intervallschichtmomente bestimmen den Wirkungszuwachs für ein
  bereits vorgeschlagenes Vergangenheitsideal. Sie ersetzen nicht die zur
  Wahl zukünftiger Ideale nötige Ordnungsinformation.
- Mit e(P) als Zahl linearer Erweiterungen gilt unter dem geerbten invarianten
  Maß die natürliche Labelgewichtung 1/e(P). Die schrittweisen Verhältnisse
  e(Eltern)/e(Kind) teleskopieren zum richtigen festen Endgewicht. Die
  Geburtslabels sind Hilfsmarkierungen, keine physikalische Eigenzeit.
- Der Fortsetzungsoperator erhält die alten Feldvariablen. Sein Kern enthält
  Deltafaktoren in diesen Variablen und fällt nicht unter das frühere Hindernis
  für beschränkte integrierte Kerne. Das erklärt noch kein physikalisches
  Skalarprodukt und keinen physikalischen Quotienten der Geburtslabels.
- Im erklärten Hilfsprodukt lauten die Normfaktoren für Zweierkette und
  Zweierantikette 49/36 und 2. Lokale Normierung macht den Operator formal
  isometrisch, verändert aber die ursprünglichen relativen Amplituden.
- Positive Produkte bei festem Endhorizont lassen sich zurückziehen; sie
  hängen von der Endwahl ab. Kein unendlicher konsistenter physikalischer
  Normpfad ist hergeleitet. Der Hilfsrecord-Vergleich 4/5 gegen 49/67 betrifft
  ausdrücklich kein qualifiziertes kovariantes physikalisches Ereignis.

408 natürliche Ordnungen, 407 Erweiterungen, 2.442 rationale Wirkungsfälle,
268 Austauschdiamanten mit 536 Feldprüfungen, 816 Endanker-Prüfungen, sechs
vollständige Labelsummen, acht Kragenzeugen und 30 endliche Normrückzüge sind
ausgeführt. Fünf exakte Ergebnisdateien werden isoliert bytegleich reproduziert.

**Alle acht physikalischen Gates bleiben HOLD:** MODEL, CURRENT,
CORRESPONDENCE, BOUNCE, REGULARITY, BOUNDARY, TRAPPING und EXTENSION. Keine
neuen dynamischen 4D-Ensembles, kein physikalisches Junction-Gesetz und keine
Singularitätsauflösung. Allgemeine Beweise sind nicht formal maschinengeprüft.
Der vor der Rechnung lokal gehashte Plan ist keine externe Präregistrierung
oder blinde Vorhersage.

## Nachrechnung

Vom Repository-Stamm, Python 3.10+, nur Standardbibliothek:

```bash
python3 -O -B research/rax_cqg/dust_collapse/boundary_memory_v0_1/publication_check.py
python3 -O -B research/rax_cqg/dust_collapse/boundary_memory_v0_1/publication_check.py --replay
```

Die Prüfung pinnt das Original-ZIP, alle 30 Mitglieder, die PDF-Kopie, den
vollständigen Manifestinhalt, den Plan und sieben bytegleiche Vorgängerquellen.
Die isolierte Nachrechnung regeneriert fünf Ergebnisdateien aus Quellen und
vergleicht sämtliche Bytes sowie die Replay-Quittung.
`.github/workflows/cst-dust-boundary-memory.yml` führt diese Kontrollen bei
passenden Pull Requests und Änderungen auf Main aus. Ein Software-PASS hebt
keine physikalische HOLD-Entscheidung auf.

## Unveränderte Veröffentlichung

PDF, ZIP und alle 30 Originalmitglieder bleiben bytegleich. Nur diese
Übersicht und `publication_check.py` ergänzen den entpackten Komponentenordner.

| Artefakt | SHA-256 |
|---|---|
| ZIP | `1181a8f8242f503cb48db4415b0efe06c70d307bc057ebcf00cf7dfaace80fda` |
| PDF | `6113e53f2ecaaa70f2498c41bbb1e64464f6a824d286b698c57c33308b7ef5cd` |
| Plan | `9079923b05523664d420fb1de8505a0117bdd26ee1c615994b0929e9b8ea6e48` |

Basis: Main `886052d8eb9d619da91896d23e0a7ede511ef30f`, nach PR 248.
Nächste Forschungsfrage ist die begründete Auswahl eines positiven Normpfads
mit kontrollierter Horizontabhängigkeit und verträglicher Behandlung
redundanter Geburtslabels bei Erhaltung der ursprünglichen Amplituden.
