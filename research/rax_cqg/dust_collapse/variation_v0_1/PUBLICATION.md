# CST-DUST-Variationskandidat v0.1 · Veröffentlichung

Eine regulierte gemeinsame Geometrie-Materie-Amplitude ist als Kandidat definiert.
Ihre endlichen Uhr-, Dichte- und Geometrievariationen, der Variationsstrom und
eine bedingte Außenfeldantwort sind ausgerechnet. Die Variation der vollständigen
endlichen Amplitude enthält bei zweiter Ableitung zusätzlich eine verbundene
Zweipunktinsertion. Maß, Regulatoren und kinematische Zustandsräume sind explizite
Modellannahmen und noch nicht physikalisch hergeleitet.

**Die direkte Interpretation des rohen Kerns als geschlossene Quantenevolution
mit den deklarierten I₂-Skalarprodukten scheitert.** Dieses FAIL betrifft
`CST-DUST-V1-RAW-K` in den angegebenen endlichen kinematischen Randräumen. Es ist
kein No-go-Satz für CST, andere physikalische Skalarprodukte, eine Constraint- oder
Rigging-Map-Interpretation beziehungsweise kontrollierte Grenzwertfamilien.

**Physikalisches Junction-Gesetz: HOLD_NOT_DERIVED. Gemeinsame Außenraumgeometrie:
HOLD_NOT_SOLVED. Globaler Bounce: HOLD_NOT_RUN. Regularität: separat HOLD.**
Der neue abgegrenzte P1-Datensatz ergibt MODEL=FAIL und sieben HOLD-Entscheidungen;
frühere Datensätze bleiben unverändert.

[Bericht (PDF, zehn Seiten)](../reports/CST_DUST_Physikalische_Variation_v0_1.pdf) ·
[Originales Prüfpaket (ZIP)](../packages/CST_DUST_Physikalische_Variation_v0_1_Pruefpaket.zip) ·
[Definitionen und Beweise](DERIVATION.md) · [Exakte Ergebnisse](results/verification.json)

## Geprüfte Ergebnisse

- 4 473 gelabelte endliche Ordnungen; je 22 095 Produkt-, Uhr-, Dichte- und
  Verschiebungsprüfungen. Alle angegebenen algebraischen Residuen sind exakt null.
- Je 130 116 Materieverklebungen und Variationsstrom-Schnittbilanzen,
  5 377 Labelpermutationen und 1 240 zulässige Geometriemoves.
- Neun exakte Schurantworten bei festem C und w. Diese eliminieren eine Hilfsuhr;
  sie lösen keine Vakuummetrik, Staubtrajektorie oder Dichte-Normierungsbedingung.
- Analytisch Re(K†K)₀₁ > 1/2. Daher ist K†K für kein konstantes c>0 gleich cI₂.
  Die feste In-in-Normierung liefert Z[π,π] ≈ 0,01763122254 statt 1.
- Rationale Taylorrechnung bis Grad 80 mit Restschranke und nach außen gerundeten
  Intervallen; zehn strukturelle Positiv-/Negativkontrollen.

Die algebraische Testklasse ist breiter als der Amplitudenträger und keine
vierdimensionale Staubball-Dynamik. Der Variationsstrom ist noch nicht als
physikalischer positiver Massestrom kalibriert. Der analytische Ausfallmechanismus
war vor der Rechnung bekannt und im lokalen Plan offengelegt; keine blinde
Vorhersage oder externe Präregistrierung. Keine neuen 4D-Ensembles, Sprinklings,
Zufallsdaten oder bezahlten Läufe.

## Reproduzieren

Vom Repository-Stamm aus, mit Python 3.10 oder neuer:

```bash
python3 -O -B research/rax_cqg/dust_collapse/variation_v0_1/publication_check.py
python3 -O -B research/rax_cqg/dust_collapse/variation_v0_1/publication_check.py --replay
```

Die Prüfung benötigt nur die Standardbibliothek. Sie kontrolliert Originalbytes
von ZIP, PDF und allen 29 Archivmitgliedern, das vollständige SHA-256-Manifest,
Vorgängereingaben, den fixierten Plan und die Quellen des ausgeführten Codes.
Der neue P1-Datensatz wird mit dem unveränderten geerbten Gate erneut auditiert.

Der Replay entpackt isoliert, löscht die archivierten Ergebnisse und erzeugt alle
zehn Ergebnisdateien neu. Nur die Python-Version im Manifest und ihr unabhängig
geprüfter abhängiger Datensatzhash dürfen zwischen Laufzeiten abweichen.
Wissenschaftliche Resultate und Entscheidungen müssen unverändert bleiben.

`.github/workflows/cst-dust-variation.yml` führt die Prüfung auf Pull Requests
und bei Änderungen auf Main aus. Ein erfolgreicher Softwarecheck bestätigt die
korrekte Reproduktion des begrenzten negativen Ergebnisses und stuft keine
physikalische Entscheidung hoch.

Das ursprüngliche Prüfpaket und alle enthaltenen Dateien bleiben bytegleich.
`PUBLICATION.md` und `publication_check.py` ergänzen die Repository-Einbindung.
Die optionale Berichtserstellung ist in der originalen README beschrieben.

| Artefakt | SHA-256 |
|---|---|
| Original-ZIP | `655e760e46c2b676ba6dc0499271293feabb12acda97d291433f416ea2fbe848` |
| Bericht | `091b2eb54ecf342caaa5376227ffe56f5660780673d29c01564f1408f01342f9` |
| Fixierter Plan | `65ea55b1f64e7f0e577927922e502bd97f16b017335042eb33d6d35e318db743` |

Projektbasis: Main-Commit `9fa170dfd604be3847004ea2bdbe8587ada5d068` nach PR 244.

## Nächster physikalischer Engpass

Eine begründete Definition von Zustandsraum, physikalischem Skalarprodukt,
Constraints beziehungsweise Evolution, Anfangszustand und zulässigen Quellen.
Erst darauf können die gemeinsame kausale effektive Variation, der Außenraum
und eine kontrollierte erste-Variations-/Verfeinerungsbrücke aufgebaut werden.
Regularität behält eigene Operator-, Moment-, Tail- und Verfeinerungsprüfungen.
