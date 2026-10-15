# Ausgewählte Agentenbelege dauerhaft im Git-Stand

Diese drei originalen GitHub-Artefakt-ZIPs wurden am 15. Oktober 2026 vor Ablauf
ihrer Actions-Aufbewahrung heruntergeladen. Die Bytes stimmen mit den von GitHub
angegebenen SHA-256-Digests überein. Auch sämtliche inneren Dateiinventare und die
im Bericht genannten Quellhashes wurden gegen die damaligen Git-Commits geprüft.
[ARCHIVE.json](ARCHIVE.json) nennt Lauf, Commit, Auswahlgrund und ursprüngliches
Ablaufdatum. Die JSON-Berichte daneben sind bytegleiche Leseauszüge.

| Originalarchiv | Aussage des gespeicherten Laufs | Ursprünglicher Ablauf |
| --- | --- | --- |
| [math-lorentz.zip](math-lorentz.zip) | Begrenzte Mathematiksuche; unter anderem exakte Literaturreplikation n=3…5, numerische Propagatorvergleiche und Gegenbeispiele. Keine neue n=6-Replikation und kein Neuheitsnachweis. | 14. November 2026 |
| [graph-atlas.zip](graph-atlas.zip) | 1.253 Graphen: 995 verbundene Zertifikate, 258 erwartete globale Zurückweisungen; kein allgemeiner Satz über beliebige gewichtete Graphen. | 29. Oktober 2026 |
| [noaa.zip](noaa.zip) | Ein gespeichertes NOAA-Fenster samt Rohantwort, Browserlauf und Zertifikaten. Keine eigene physische Messung oder Entrauschungsleistungsbestätigung. | 14. November 2026 |

Prüfung ohne Download:

```sh
python3 -S -B tools/release/verify_archive.py
```

Die Kopien liegen in der Git-Historie und im gemeinsamen Referenzpaket; sie
unterliegen dort keiner Actions-Löschfrist. Das ist keine DOI-Archivierung oder
Garantie gegen spätere Löschung des gesamten Repositorys. Externe Kopien des
Referenzpakets bleiben sinnvoll. Es handelt sich um eine begründete Auswahl,
nicht um die lückenlose Archivierung aller Agentenläufe. NASA-/QuTech-Artefakte
und nach diesem Snapshot entstehende Läufe sind nicht enthalten.

Originale Projektberichte/-prüfungen: Apache-2.0. NOAA-Daten: NOAA/NWS Space
Weather Prediction Center, GOES XRS; Herkunft und Abruf in `noaa-report.json`,
keine institutionelle Unterstützung behauptet. Der Graphatlas stammt aus
NetworkX 3.4.2 (Read/Wilson); die [NetworkX-Lizenz](NETWORKX_LICENSE.txt) bleibt
beigefügt. Quellenhashes und gespeicherte PASS-Status sind keine erneute
wissenschaftliche Analyse oder unabhängige Begutachtung dieser Läufe.
