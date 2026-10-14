# X6 Integration v0.1 — ausgeführte Abnahme

**Ergebnis: PASS_WITH_BROWSER.** Ein neuer Git-Checkout ohne vorhandene `.venv`
hat die dokumentierte Installation, alle drei lokalen Adapter und den Export-
und Prüfablauf erfolgreich ausgeführt. Die 23 Kommando-Schritte bestanden;
der Checkout blieb sauber und sämtliche getrackten Dateien unverändert.

[Installation und Bedienung](../INTEGRATION.md) ·
[Maschinenlesbarer vollständiger Bericht](evidence/qualification.json)

## Genau geprüfter Stand

- Ausgangsstand des Repositorys: `79eb87e0c20d631197d66f4f516fc22fc4e4b9de`.
- Implementierungsrevision des frischen Checkouts:
  `a7d0fce1f470edb8362ca2e6967d1946b9202ec2`.
- Linux x86-64, Python 3.12.14, Node.js 24.19.0, NumPy 2.3.5, SciPy 1.17.0.
- Browserprüfung: Playwright 1.62.1, Chromium 153.0.8010.0.
- Die anschliessende Ergänzung dieses Berichts verändert keine Implementierung
  der geprüften Adapter. Quellhashes in den Exporten binden die Ausführung an
  ihre tatsächlichen Quellen; der Git-Stand allein ist kein Herkunftsnachweis.

Die lokale Implementierungsrevision ist zusätzlich im
[implementation.bundle](implementation.bundle) erhalten. Ihre Basis ist der
oben genannte bereits veröffentlichte Repository-Commit. In einem separaten
Checkout mit dieser Basis lässt sich der exakt getestete Stand mit
`git fetch /pfad/zu/implementation.bundle HEAD` und `git checkout FETCH_HEAD`
wiederherstellen. Der GitHub-Entwurfscommit kann eine andere Commit-ID haben;
die geprüften Laufzeitquellen bleiben bytegleich.

Die Installation lief mit dem normalen `setup --profile research` in einer
neuen virtuellen Umgebung. Globale Python-Pakete wurden nicht übernommen.
Der Browser kam aus einer separat bereitgestellten lokalen Testumgebung;
er gehört nicht zu den Anwendungsabhängigkeiten oder zu den Exportarchiven.
Ein voriger Playwright-Download lieferte hier eine HTML-Fehlerseite statt eines
Browserarchivs. Die finale Prüfung verwendete deshalb den ausdrücklich
unterstützten Pfad `X6_CHROMIUM_EXECUTABLE`; Details stehen im
[Browserumgebungsnachweis](evidence/browser-environment.json).

## Prüfumfang

| Prüfung | Ausgeführtes Ergebnis |
| --- | --- |
| Installation und Voraussetzungen | Neue `.venv`, gepinnte Forschungspakete, `pip check`, `doctor`: bestanden. |
| Regressionen | Zwölf Tests bestanden; einschliesslich Manipulation mit neu berechneten Hashwerten, fehlerhafter CSV, fehlendem Abschluss, falschem Quellenstand, ZIP-Pfadwechseln und Überschreibschutz. |
| Signal | Ausführen, Verzeichnis-Replay, ZIP-Export und ZIP-Replay bestanden. Die vier nativen Qualitätsurteile bleiben erhalten. |
| Spektralreferenz | Fünf exakte rationale Referenzfälle bestanden; Verzeichnis- und ZIP-Replay bestanden. |
| RAX | Alle neun M1-Prüfblöcke, vollständige B1-Nachrechnung und sechs Zusatztestmethoden reproduziert; Verzeichnis- und ZIP-Replay bestanden. |
| Browser | Einstieg bei Desktop- und Mobilbreite, CLI-JSON im Signal Lab, tatsächliche JSON-/CSV-Downloads und zehn bestehende Astrolabium-Qualifikationsprüfungen bestanden; keine JavaScript-Seitenfehler. |
| Browser zurück zur CLI | Heruntergeladenes JSON bytegleich übernommen, gemeinsam exportiert und aus dem ZIP erfolgreich nachgerechnet. |
| Quellen | Sauberer Checkout vor und nach dem Lauf, alle getrackten Dateien bytegleich; Repository-Inventar ohne Fehler oder unaufgeführte Dateien. |

`REPLAY_PASS` bedeutet die beschriebene Nachrechnung. Es ändert keinen
fachlichen Status: Der X6-Phasenfilter meldet im Signalbeispiel weiterhin FAIL;
die acht primären RAX-B1-Vergleiche bleiben INCONCLUSIVE. Externe Begutachtung,
Hardwarequalifikation und physikalische Validierung wurden nicht durchgeführt.
Die neue GitHub-CI-Konfiguration ist enthalten; dieser Bericht belegt den
lokalen Lauf und behauptet keinen bereits bestandenen GitHub-Actions-Lauf.

## Tatsächlich erzeugte Beispiel-Exporte

| ZIP | Inhalt |
| --- | --- |
| [signal.zip](exports/signal.zip) | Synthetisches Pulsbeispiel, vollständige native JSON-/CSV-Daten und gemeinsame Metadaten. |
| [spectral.zip](exports/spectral.zip) | Fünf rationale Referenzfälle samt unveränderter Referenzquelle. |
| [rax.zip](exports/rax.zip) | Unverändertes freigegebenes M1-Archiv, neu erzeugte Prüfresultate, Protokolle und gemeinsame Metadaten. |
| [browser-import.zip](exports/browser-import.zip) | Tatsächlich im Browser heruntergeladener Signalbericht mit den nativen Originalbytes. |

Mit dem passenden Integrationscheckout:

```sh
python3 x6.py verify docs/integration-v0.1/exports/signal.zip
python3 x6.py verify docs/integration-v0.1/exports/spectral.zip
python3 x6.py verify docs/integration-v0.1/exports/rax.zip
python3 x6.py verify docs/integration-v0.1/exports/browser-import.zip
```

[Dateiinventar und SHA-256](DELIVERY.json) prüfen die bereitgestellten Belege.
Das Inventar ist keine Signatur. Die `*.log`-Dateien unter `evidence/` enthalten
die vollständigen Ausgaben der 23 Schritte; Fehlversuche der Negativkontrollen
werden mit ihrem erwarteten Exitcode 1 dokumentiert.

Copyright 2026 Thomas Gfeller. Originale Projektbeiträge unter
[Apache-2.0](../../LICENSE), gemäss [Lizenzumfang](../../LICENSE_SCOPE.md).
