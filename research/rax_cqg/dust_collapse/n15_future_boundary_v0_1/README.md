# CST-DUST · Erster Randtest an N15-Typ 375841

**Entscheid.** Die Selektion nach dem Vorzeichen des Wirkungsstroms steigt auf der untersuchten Zweipaketspanne nicht durch die Referenzpaarung des geöffneten Zukunftsrands ab. Zwei Paketbilder stimmen punktweise überein und haben positive Norm. Ihr Differenzvektor hat Norm null, sein positiv selektierter Anteil hat positive Norm. Der Befund gilt für eine konkrete Fortsetzung der bisherigen Rechnung mit drei geöffneten späten Uhren und vier Zukunftsdichten. Die physikalische Paarung, die Wahl des zulässigen Constraint-Sektors und die P3-Massenkalibrierung sind offen.

[Teilartikel als PDF](CST_DUST_N15_Erster_Randtest.pdf) · [Editierbare Manuskriptfassung](Teilartikel.md) · [Ergebnis zum Nachlesen](ergebnis.json)

## Wiederholung ohne Netzverbindung

Python 3.9 oder neuer mit aktiven Assertions genügt. Im entpackten Verzeichnis ausführen:

```sh
sha256sum -c SHA256SUMS
python3 -B pruefen.py > wiederholung.json
cmp ergebnis.json wiederholung.json
```

Der Hauptprüfer vergleicht zwei Berechnungen der zentralen Stromwerte, zertifiziert die Vorzeichen auf offenen Zellen, kontrolliert die Phasenhülle auf der erweiterten Zukunftsbox und überprüft zwei einfache Zukunftsanbauten an die alte Ordnung. Er trägt die analytisch hergeleitete, auf die gemeinsame Norm normierte Gram-Matrix in das Protokoll ein. Die absolute Norm wird nur als strikt positiv eingeschlossen. Die wissenschaftliche Aussage und ihre Voraussetzungen sind im Teilartikel hergeleitet.

- `density_translation_375841.py` rekonstruiert die Ordnung und die Dichtezellen unabhängig von den archivierten Hilfsmodulen. Die drei Dichteverschiebungen erhalten die Wirkung und die Gesamtdichte identisch.
- `randfenster_375841.py` prüft die ganze Präparation des Einzeltyps in der linken und rechten Anfangsuhröffnung. Die beiden Lappen separat aufzuzeichnen ist eine zusätzliche Messannahme. Mit zwei konstanten Zweigkoeffizienten erhält diese Vergleichskonstruktion Rang zwei, lässt aber nichtorthogonale Vorzeichenzustände zurück.
- `studie/inputs/sync/` enthält drei bytegleiche Hilfsmodule aus PR #336. `quellen/` enthält vier Auszüge in Form vollständiger Originaldateien des öffentlichen Stands. Die darin verlinkten früheren Studien stehen im Repository. `herkunft.json` ordnet die Dateien konkreten Git-Blobs und SHA-256-Prüfsummen zu.

Die Zellen wurden bei Kenntnis des Einzeltypbefunds aus dem Vorgängerpaket konstruiert. Das ist eine nachträgliche analytische Untersuchung. Der eingangsseitige Quellkontrast ist ein erster Testwert für eine zukünftige Instrumentkonstruktion. Er zeigt noch keinen am Zukunftsrand gespeicherten physikalischen Strom. Etappe 6 bleibt offen, die 60 P3-Checkpoints stehen auf **NOT_RUN**.

[Forschungsindex am geprüften Commit](https://github.com/thomasmgfeller/x6-spectral-astrolabium/tree/d7de6876f571ece2dca8030f30d8fdda839b8404/research/rax_cqg/dust_collapse)
