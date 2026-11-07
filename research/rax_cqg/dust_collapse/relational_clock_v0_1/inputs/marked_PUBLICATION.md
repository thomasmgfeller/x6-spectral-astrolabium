# Markierte Zustände, Ereignisse und Endauslese v0.1

Veröffentlichtes Arbeitspaket vom 7. November 2026. Ausgangspunkt ist
Main `57aea796ac1f35c31ca3fabce45e0a27c518a5bf` nach PR 250.

Der kohärente Quotient wird bei festem endlichem Regulator auf die
vollständigen kontinuierlichen Uhr- und Materiefelder erweitert. Die
geerbte Fortsetzung steigt auf ihn ab; eine beschränkte Linksinverse
liefert positive koerzive Produkte und transportierte Präparationsprojektoren.
Diese mathematische Existenz wählt den physikalischen CST-Zustandsraum
und das physikalische Skalarprodukt noch nicht aus.

Ein exaktes binäres Referenzbeispiel zeigt zwei zusätzliche Bedingungen:

- Eine labelinvariante aktuelle Staubaussage ist nicht automatisch ein
  selbstadjungierter Messprojektor im konstruierten Produkt. Die naive
  Messzuordnung liefert für einen Hilfsraum-Testzustand **−1/149**.
- Die ursprüngliche Summenauslese ist im phasenfreien Referenzfall nicht
  mit einem zusätzlichen Fortsetzungsschritt proportional kompatibel:
  Antiketten und Ketten erhalten die verschiedenen Faktoren **8/3** und
  **11/6**. Eine transportierte Auslese ist kompatibel, verändert jedoch
  die ursprüngliche Endkontraktion.

Die binären Kontrollen sind ein diskreter Maß-Ersatz, keine nachgewiesene
Quadratur des kontinuierlichen Feldintegrals und keine Staubballsimulation.
Der allgemeine kontinuierliche Satz wird analytisch bewiesen.

**MODEL, CURRENT, CORRESPONDENCE, BOUNCE, REGULARITY, BOUNDARY, TRAPPING und
EXTENSION bleiben jeweils HOLD.** Physikalische Constraints, relationaler
Uhrschnitt, Produkt- und Ereignisauswahl, unendliche Quantenmaß-Fortsetzung,
Junction-Gesetz und globaler Bounce bleiben offen. Historische
kandidatenspezifische FAILs werden nicht aufgehoben.

## Artefakte

- [Bericht (PDF)](../reports/CST_DUST_Markierte_Zustaende_Ereignisse_v0_1.pdf)
- [Originales Prüfpaket (ZIP)](../packages/CST_DUST_Markierte_Zustaende_Ereignisse_v0_1_Pruefpaket.zip)
- [Vollständige Ableitung und Geltungsbereich](DERIVATION.md)
- [Maschinenlesbarer Ereignisvertrag](event_contract.json)
- [Nachrechnung und Nutzung](README.md)
- [Exakte Ergebnisse](results/verification.json)

## Verifikation

707 natürliche markierte Zustände, 234 markierte Isomorphietypen,
6.384 unabhängige Maximal-Löschungs-Einträge, 15.715 Permutationen mit
offener und geschlossener Wirkungsprüfung sowie 706 Wirkungsinkremente
sind exakt geprüft. Vier positive Produkte und vier transportierte
Projektorzerlegungen erfüllen die Matrixidentitäten. Sechs Ergebnisdateien
werden in einem frischen Verzeichnis bytegleich reproduziert.

Vom Repository-Stamm aus, Python 3.10 oder neuer, keine Zusatzpakete:

```bash
python3 -O -B research/rax_cqg/dust_collapse/marked_events_v0_1/publication_check.py --replay
```

Die Publikationsprüfung kontrolliert das unveränderte Archiv, alle 31
Mitglieder, beide PDF-Kopien, den eingefrorenen Plan, sieben bytegleiche
Repositoryquellen und die acht physikalischen HOLDs. Der dazugehörige
Workflow `cst-dust-marked-events.yml` führt diese Prüfung auf Pull Requests
und `main` aus. Wiederholbarkeit ist keine unabhängige wissenschaftliche
Replikation; allgemeine Beweise wurden nicht formal maschinell zertifiziert.

| Objekt | SHA-256 |
|---|---|
| Original ZIP | `6df972fb1e4b53eec4c693ff61ecc6afe83ef4d755206d103fb6a7c9facc6e1e` |
| PDF | `167decf4a0c64b2358d2ca8dfba60669466b4bd169374f95ceff45bb3b2deae3` |
| Plan | `6eea1d379814c77dfe50e02ae6946da030dfea3eb1074ad181447abe27c8a0c2` |

Die Originaldateien aus dem Prüfpaket bleiben unverändert. Nur diese
Publikationsnotiz, der Repository-Prüfer, CI und Index-/Integritätsdateien
werden ergänzt. Der historische Normvertrag des Vorgängers bleibt als
Quelle erhalten; die formale Erweiterung ist im neuen Ereignisvertrag
mit ihren Voraussetzungen abgegrenzt.

## Nächste physikalische Entscheidung

Einen konkreten Kandidaten aus Präparation, relationalem Uhrschnitt,
begründetem Skalarprodukt und Ausleseinstrument gemeinsam festlegen.
Danach die tatsächliche Randphase, Normierung und erforderliche
Schnittkompatibilität prüfen. Freie Hilfsprodukte bestimmen die Physik
nicht allein.
