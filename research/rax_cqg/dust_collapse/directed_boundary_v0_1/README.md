# CST-DUST: Gerichteter Randvertrag und bedingte Gaußprojektion v0.1

Fortsetzung der Materieblock-Vorprüfung vom 11. November 2026 nach PR #277.
Das Paket enthält eine explizite **mathematische Kontrollfamilie**, eine
bedingte Gaußprojektion und einen Beweis für singuläre Innenblöcke. Es enthält
keine frei ergänzten physikalischen Materieblöcke.

## Anschluss an die Staubball-Reihe

| Stufe | Bereits geprüft | Anschluss dieses Pakets |
|---|---|---|
| [Randkern-Benchmark](../boundary_kernel_benchmark_v0_1/README.md), PR #275 | Verklebung, Labelquotient, Uhrkern und Schurantwort getrennt | Eine gerichtete Kontrollfamilie mit echtem Innenraum |
| [Geometriekontrollkern v0.2](../geometry_control_8x8_v0_2/README.md), PR #276 | Stratumweise Basis, tatsächliche Mischblock-Masken | Explizite Permutation zum geometrieweisen Schema |
| [Ausgewählte Hilfsbasis](../selected_auxiliary_normalization_v0_1/README.md), PR #277 | Hilfs-Gramstruktur und Darstellungskonventionen | Physikalische Randzustände bleiben gesondert zu begründen |
| [Materieblock-Vorprüfung](../matter_preflight_v0_1/README.md), gemeinsam veröffentlicht | 25 exakte Kontrollen; Träger, Staubuhr/Feld und Parität getrennt | Bedingte volle Gaußprojektion einschließlich Phase und Nullraum |

Die neue Fünferfamilie ersetzt weder die frühere Vierer-Verklebungszählung
noch die physikalische Historienherleitung. Die 25 Kontrollen der Vorprüfung
und die 27 Tests dieses Pakets haben unterschiedliche Prüfgegenstände.
Die frühere Uhrkern-Negativkontrolle bleibt auf ihren ursprünglichen Kern
beschränkt. Es wird kein physikalischer Gate-Status hochgestuft.

## Lesen und nachrechnen

- [Aktualisierter Bericht (PDF, 10 Seiten)](CST_DUST_Randvertrag_Gaussprojektion_v0_1.pdf)
- [Vollständiger mathematischer Quelltext](report.tex)
- [Prüfpaket einschließlich Bericht und Code (ZIP)](CST_DUST_Randvertrag_Gaussprojektion_v0_1_Pruefpaket.zip)
- [Basis-, Index- und Projektionsvertrag](basis_contract.json)
- [Offene physikalische Eingaben und Gates](physical_inputs.json)
- [Gerichtete Träger und Zählergebnisse](results/carriers.json), [27 Kontrollen](results/checks.json)
- [Gaußprojektion](gaussian.py), [Tests](test_contract.py), [Reproduktion](verify.py)
- [Provenienz](provenance.json), [Prüfsummen](SHA256SUMS.json)

Abschnitt 8 des Berichts korrigiert Operator-/Wirkungs- und Modenbegriffe;
Abschnitte 9–10 schließen die Indexkonventionen an die vorhandene Basis an
und prüfen Parität sowie den noch offenen dynamischen Abschluss.

## Ergebnis

- Gerichtete Fünferordnungen mit Randkragen A/K und einem inneren Element:
  49/23/23/12. Mit Anschluss jedes Randelements an die Gegenseite:
  33/14/14/7, jeweils in Reihenfolge AA/AK/KA/KK.
- Für einen reell-symmetrischen Feld-Hessian mit Innenblock A und
  Randkopplung J ist die zentrierte Gaußprojektion im Abel-Grenzwert endlich
  genau dann, wenn `ker(A) ∩ ker(J.T) = {0}`. Die Aussage gilt bei festem
  Hintergrund, positiven Randbreiten, Lebesgue-Feldmaß und ohne Quelle.
- Normierte Gauß-/Hermitepakete, Projektionsformeln für 00/11/20, Paritätsnull
  für 10/01, kontinuierliche Determinantenwurzel und Atommaß sind explizit.
- Die nachgereichten Formeln werden in Abschnitt 8 eingeordnet. Eine
  Projektion der Bilinearform in ihre eigene verallgemeinerte Eigenbasis
  ist diagonal; daraus folgt keine Aussage über Fock-Übergangsamplituden.
- Abschnitte 9–10 prüfen das nachgereichte Achtzustandsschema: die explizite
  Basispermutation, Ausgang/Eingang gegenüber der Trägerorientierung,
  bedingte Paritätsblöcke und den noch fehlenden dynamischen Abschluss.
- Physikalische Matrix `NOT_CONSTRUCTED`, physikalischer Mischblock
  `NOT_COMPUTED`, acht physikalische Gates `HOLD`.

## Dateien

`report.tex` ist die vollständige Herleitung einschließlich Beweisen,
Quellen und Aussagegrenzen. Die PDF-Datei ist ihre gesetzte Lesefassung.
`analyze.py` erzeugt `results/carriers.json` mit allen Ordnungs-IDs,
Orbitgewichten, F4-Polynomen und exakten Auswertungen bei z=1,-1,i.
`gaussian.py` implementiert bedingte numerische Gaußprojektionen; es erfindet
keine physikalische Hesse-Matrix. Seine Kontrollwerte sind nicht als
zertifizierte physikalische Daten zu benutzen.

`physical_inputs.json` enthält die weiterhin fehlenden physikalischen
Eingaben als null. Die bisherige Reihenfolge der acht Planungslabels wird
bewahrt. Die neue Kragenfamilie wird nicht ungeprüft mit jener Hilfsbasis
identifiziert. Insbesondere bleibt die Bedeutung von '+' bei mehreren
Randdichten offen.

`basis_contract.json` hält die beiden Basisreihenfolgen und die Zuordnung
der Matrixblöcke zur umgekehrt beschrifteten Trägerfamilie fest. Unbekannte
physikalische Gram-Matrizen, Einbettungen und Übergänge bleiben null.

## Reproduktion

Python 3 mit NumPy und SymPy (Versionen des Prüflaufs in `environment.json`).

```bash
python analyze.py
python -m unittest discover -s . -p 'test_*.py' -v
python run_checks.py
python verify.py
```

27 Tests umfassen exakte kombinatorische/symbolische Kontrollen und zwei
unabhängige Gauß-Hermite-Quadraturen mit absoluter Toleranz 1e-11.
Der allgemeine Nullraumsatz wird analytisch bewiesen; endliche Testbeispiele
ersetzen diesen Beweis nicht. `verify.py` prüft alle Manifest-Hashes und
reproduziert beide Ergebnisdateien in einem frischen temporären Verzeichnis
bytegleich. Die Paketprüfung ist keine repository-weite GitHub-CI.

Die PDF kann mit einer vollständigen pdfLaTeX-Installation aus `report.tex`
gebaut werden. PDF-Zeitstempel können sich dabei ändern; behauptet wird
Bytegleichheit der beiden JSON-Ergebnisdateien, nicht eines extern neu
gesetzten PDFs. Der mitgelieferte PDF-Hash wird geprüft.

## Grenzen und Herkunft

Die neue Historienfamilie, positive Randpakete und Abel-Feldvorschrift sind
deklarierte Kontrollvoraussetzungen. Kompakte Staubuhrregulatoren bleiben
unverändert. Die Veröffentlichung enthält ausschließlich Dokumentation,
kleine mathematische Kontrollen und deren Ergebnisse. Produktionsläufe und
bezahlte Rechenaufträge wurden nicht gestartet.

Quelle der geerbten Enumerationsfunktionen: Repository
`thomasmgfeller/x6-spectral-astrolabium`, Main-Anschluss
`fdf1deb6ac071056d533a0937e21c238f42b2974`.
Der Git-Blob von `inputs/gluing.py` wurde über GitHub geprüft.
`inputs/SOURCE_PREFLIGHT.md` ist die lokale Vorprüfung; ihr geerbter
Quellennachweis liegt in `inputs/preflight_provenance.json`. Nicht sämtliche
dort aufgeführten älteren Quelldateien werden hier erneut mitgeliefert.

Die freien Kontrollzahlen aus den Tests sind keine vorgeschlagene Auswahl
des tatsächlichen Materie-Hessians oder der physikalischen Randzustände.
