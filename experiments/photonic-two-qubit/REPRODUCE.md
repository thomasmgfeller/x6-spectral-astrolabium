# Software und Modelle reproduzieren

Alle Ergebnisse dieser Prüfung betreffen synthetische Daten, digitale Logik oder idealisierte mechanische Modelle. Ein PASS ist keine physische Qualifizierung. Originalberichte in den ZIPs behalten ihren ursprünglichen Stand; frische CI-Ergebnisse sind beim jeweiligen Commit sichtbar.

## Einheitlicher Lauf

Vom Wurzelverzeichnis des Repositorys, empfohlen Python 3.12 unter Linux:

```bash
python -m venv .venv
. .venv/bin/activate
python -m pip install -r tests/photonics/requirements.txt
python tests/python/verify_manifest.py
python tests/photonics/validate_release.py --cad --output /tmp/photonic-evidence
```

Mit installiertem GHDL 5.0.1 (mcode):

```bash
python tests/photonics/validate_release.py --ghdl --cad --output /tmp/photonic-full-evidence
```

Der Runner prüft Herkunftshashes, Archiv-Prüfsummen, Identität der lesbaren v0.7-Quellen und der bereits integrierten X6-Decoder sowie die unveränderte Jig-Geometrie. Anschließend führt er vorhandene Python-Testreihen und Jig-Modellrechnungen in temporären Kopien aus. `--cad` regeneriert die Geometrie samt Gültigkeits-/Kollisionsprüfungen. `--ghdl` verlangt zusätzlich 28 v0.7-RTL-Szenarien und generische Synthese von vier Modulen. Ein fehlendes angefordertes Werkzeug führt zum Fehlschlag. Ausgelassene optionale Prüfungen stehen ausdrücklich unter `not_run` im Bericht.

Die vollständige Kombination läuft im [Workflow Photonic Reference](../../.github/workflows/photonic-reference.yml). Zusammenfassung, Werkzeugversionen und Logs werden als kurzlebiges CI-Artefakt bereitgestellt (7 Tage). Der öffentliche Workflow-Log und der zugehörige Commit erlauben die Zuordnung; die Tests bleiben erneut ausführbar. Das bestehende **X6 Validation** prüft zusätzlich App, Python-/Julia-Referenzen, Bridge und Browser.

## Prüfumfang und Grenzen

| Prüffamilie | Zweck | Nicht geprüft |
|---|---|---|
| v0.7 Host | Striktes Frameformat/CRC, Auswertung, simulierte serielle Übertragung | Elektrische UART-Verbindung |
| v0.7 RTL | Grenzen, Fehlerflags, Zähler, Watermarks, Sättigung, UART-TX und Vergleich mit Batchreferenz | Board, TDC, CDC und FPGA-Timing |
| Ältere Python-Suiten | Regression der v0.6-/Herald-/Einkanal-Referenzen | Alte RTL erneut synthetisiert oder Hardware rückwirkend validiert |
| Jig analytisch | Rang 6, 64 Ecklagen, 16 Lastfälle im definierten Modell | Reibung, Drift, Fertigung, reale Klebung |
| Jig CAD | Volumenkörper, nominale Kollisionen, diskret abgetasteter Rückzug | Toleranzketten und reale Belastung |

Die bereits gelieferten Archive können zusätzliche historische Tests enthalten. Nur tatsächlich neu ausgeführte Prüfungen werden als aktuelles Ergebnis berichtet. Testmethodenzahlen sind kein Maß für die wissenschaftliche Beweiskraft.

## PDF und CAD

Im Jig-ZIP stehen Generatoren unter `src/`, Geometrie unter `cad/` und Fertigungsformate in den dort dokumentierten Verzeichnissen. Für den PDF-Generator werden ReportLab und DejaVu Sans benötigt; die Veröffentlichungsfassung nutzte ReportLab 4.4.9. Dokumentation v0.1.1 trennt die zuvor überlappenden P02/P03-Druckseiten; Geometrie und Maßstab sind unverändert. Alle 14 Seiten der erzeugten PDF wurden visuell kontrolliert. Vor Verwendung einer 1:1-Schablone immer den ausgedruckten 100-mm-Balken messen.
