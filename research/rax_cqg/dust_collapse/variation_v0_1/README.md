# CST-DUST: physikalischer Variationskandidat v0.1

Eine regulierte gemeinsame Geometrie-Materie-Amplitude, ihre exakten endlichen
Variationen und eine begrenzte Prüfung ihrer Quantennormierung.

**Ergebnis:** Die Wirkungsvariationen und der daraus definierte Variationsstrom
sind algebraisch geschlossen. Der rohe Amplitudenkern ist mit den ausdrücklich
festgelegten kinematischen Skalarprodukten keine geschlossene Quantenevolution.
Der Nachweis gilt für `CST-DUST-V1-RAW-K`, nicht für CST insgesamt. Ein physikalisches
Junction-Gesetz, die gemeinsame Außenraumgeometrie, Regularität und globaler Bounce
bleiben HOLD. Der bedingte Außenfeld-Response ist nur eine Hilfsuhr-Elimination
bei festgehaltener Geometrie und Dichte.

## Inhalt

- `DERIVATION.md`: Definitionen, Beweise, Gegenbeispiel, Aussagegrenzen und Primärquellen.
- `CST_DUST_Physikalische_Variation_v0_1.pdf`: zehnseitiger Ergebnisbericht.
- `plan.json`, `plan.sha256`: lokaler Plan vor der Rechnung; der analytische
  Ausfallmechanismus war bereits bekannt. Keine externe Präregistrierung.
- `variation.py`: Materiewirkung, Strom, Geometrieantwort und Verklebung.
- `analyze.py`: exakte rationale Kontrollen und zertifizierte Normierungsschranken.
- `results/`: zehn maschinenlesbare Resultate einschließlich begrenztem P1-Audit.
- `inputs/`: unveränderte geerbte Quellen aus Main nach PR 244 und ihre Hashes.
- `build_report.py`, `figures/`: Berichtserstellung; Diagrammwerte dienen nur der Anzeige.
- `REPLAY.json`: Vergleich des isolierten Wiederholungslaufs mit allen zehn Resultaten.
- `MANIFEST.sha256`: Dateiintegrität des Pakets, ohne Selbstreferenz.

## Wiederholung

Aus diesem Verzeichnis:

```bash
python3 -O -B analyze.py
```

Die wissenschaftliche Berechnung benötigt ausschließlich die Python-Standardbibliothek.
Referenzlauf: Python 3.12.14. `-O` deaktiviert keine Prüfungen: Fehlschläge lösen
explizite Ausnahmen aus. Bei anderer Python-Version ändert sich das Versionsfeld
des Manifests und dadurch der zugehörige Audit-Hash; Zahlenresultate werden dadurch
nicht verändert. Keine externen Daten, Zufallszahlen oder kostenpflichtigen Läufe.

Die Berichtserstellung benötigt `reportlab`, `matplotlib` und DejaVu Sans.

```bash
python3 -B build_report.py
```

Sie schreibt den Bericht in `../output/pdf/`. Ein beliebiger Zielpfad kann als
erstes Argument übergeben werden. Zum Integritätsvergleich ist `sha256sum -c
MANIFEST.sha256` geeignet. Ein Neulauf kann reproduzierbare Berechnungsresultate
überschreiben; der PDF-Binärhash enthält Erstellungsmetadaten und wird nicht durch
die wissenschaftlichen Gleichheitstests qualifiziert.

## Prüfstatus

4 473 kleine gelabelte Ordnungen; je 22 095 Produkt-, Uhr-, Dichte- und
Verschiebungsprüfungen; je 130 116 Verklebungs- und Stromschnittprüfungen;
5 377 Labelprüfungen; 1 240 Geometriemoves; neun bedingte Außenfeldantworten;
zehn strukturelle Kontrollen. Alle angegebenen algebraischen Residuen sind exakt null.
Diese Zahlen sind keine 4D-Staubsimulationen.

Die Normierungsprüfung liefert Z[π,π] ≈ 0.01763122254 statt 1 unter einer einmalig
festgelegten Normierung. Der begrenzte P1-Datensatz erhält deshalb MODEL=FAIL;
die sieben weiteren Entscheidungen bleiben HOLD. Frühere Datensätze werden
nicht überschrieben. Nominale Dezimalausgaben, Taylorfehler und nach außen
gerundete zertifizierte Intervalle sind in den Resultaten unterschieden.

Lizenz: Apache-2.0; Herkunft in `NOTICE` und `inputs/provenance.json`.
