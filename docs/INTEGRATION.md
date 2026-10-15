# X6 Integration v0.1 — ein lokaler Arbeitsablauf

Diese Fassung vereinheitlicht Installation, Start, lokale Ausführung, Prüfung
und Export der vorhandenen Softwarewege. Der Einstieg ist `python3 x6.py`.
Die mathematischen Kerne, eingefrorenen RAX-Archive und wissenschaftlichen
Entscheidungen behalten ihre bisherigen Fassungen.

## 1. Einen Checkout dieser Fassung beziehen

Die Integrationsfassung ist seit PR #9 / Merge-Commit
`a4641e00d9f699311e7105d0b5c94b7b356a5ab7` in **main** enthalten.
Der frühere Branch `research/x6-integration-v0.1` ist ein historischer
Entwicklungsstand. Der aktuelle Einstieg ist:

```sh
git clone --branch main https://github.com/thomasmgfeller/x6-spectral-astrolabium.git x6-integration
cd x6-integration
```

Nicht zwischen Forschungsbranches wechseln, um die hier beschriebenen Schritte
auszuführen: alle drei Adapter sind in derselben Fassung enthalten. Das
[zentrale Modulregister](MODULE_REGISTRY.md) nennt die gepinnten Quellstände,
weiteren Module und nächsten Abnahmen. Für den dort dokumentierten Snapshot:
`git checkout --detach 1dd5f65e1046edab6175998552362ad3856f8549`.
Der historische [Abnahmebericht](integration-v0.1/README.md) nennt die genau getestete
Implementierungsrevision und enthält die vollständigen Befehlsprotokolle sowie
die tatsächlich erzeugten Beispiel-Exporte. Seine Entwurfs-/CI-Angaben beschreiben
den damaligen Veröffentlichungszeitpunkt; sie sind kein aktueller Integrationsstatus.

Voraussetzungen für den qualifizierten Ablauf: **Linux/POSIX auf x86-64,
Python 3.12, Git und Node.js ab 22**. Die tatsächlich geprüften Versionen stehen
im beigefügten Qualifikationsbericht. Andere Betriebssysteme und Architekturen
sind mit diesem Lauf nicht qualifiziert. Für die Oberfläche wird zusätzlich
ein Browser benötigt; die Prüfung verwendet Chromium.

Die [gemeinsame Offline-Referenzsuite](OFFLINE_REFERENCE.md) hat einen eigenen,
installationsfreien Prüfweg mit Python 3.12 und Node.js 24:

```sh
python3 -S -B x6.py reference qualify --output /tmp/x6-reference-evidence
```

Dieser Befehl verlangt weder `setup` noch NumPy/SciPy. Er prüft die gespeicherten
Wolfram-Ergebnisse, rationalen Graphfälle, Kausalordnungen und gezielte Fehlerfälle
in einem Ablauf und wiederholt die Rechnung beim Replay.

## 2. Installieren und Umgebung prüfen

Aus dem neuen Checkout:

```sh
python3 x6.py setup --profile research
python3 x6.py doctor --profile research
```

`setup` erstellt `.venv` ohne globale Python-Pakete und installiert NumPy 2.3.5
und SciPy 1.17.0. Dafür wird einmal ein erreichbarer Python-Paketindex benötigt.
`x6.py` verwendet danach automatisch die Python-Umgebung dieses Checkouts;
ein manuelles Aktivieren ist nicht nötig. Git und Node sind Systemvoraussetzungen
und werden nicht automatisch installiert.

Wer zunächst nur Oberfläche, Signal- und rationale Spektralprüfungen benötigt,
kann `--profile core` verwenden. Dafür werden keine zusätzlichen Python-Pakete
installiert. Das spätere `setup --profile research` ergänzt die Abhängigkeiten.

Für einen vorbereiteten Offline-Rechner lassen sich die beiden passenden
Wheels separat beziehen:

```sh
python3 -m pip download --only-binary=:all: --dest ../x6-wheels numpy==2.3.5 scipy==1.17.0
python3 x6.py setup --profile research --wheelhouse ../x6-wheels
```

Wheels müssen zu Python, Betriebssystem und Architektur passen. Die eigentlichen
Versuche und Replays benötigen nach der Installation kein Netzwerk. Verzeichnisse
und ZIP-Zielnamen müssen neu sein. Bestehende Ergebnisse werden nicht ersetzt.

## 3. Oberfläche bedienen

```sh
python3 x6.py serve
```

Die gemeldete Adresse `http://127.0.0.1:8000/` öffnet einen gemeinsamen lokalen
Einstieg für **Spektral-Astrolabium** und **Signal Validation Lab**. Mit
`--port 8001` lässt sich ein belegter Port umgehen, mit Strg+C der Server beenden.
Der Server bindet ausschliesslich an die Loopback-Adresse und dient der lokalen
Bedienung. Er ist kein verteilter Messdienst.

Im Signal Lab:

1. Parameter wählen und **Test ausführen** anklicken.
2. Alle vier Verfahren und ihre getrennten Qualitätsurteile vergleichen.
3. **Prüfbericht JSON** und bei Bedarf **Zeitreihen CSV** herunterladen.
4. Den JSON-Bericht über **JSON-Prüfbericht wiederholen** einlesen und
   **Prüfen & wiederholen** ausführen.

Der unveränderte JSON-Bericht ist auch in das gemeinsame Exportformat überführbar:

```sh
python3 x6.py import-signal /pfad/zum/evidence.json --output runs/browser-001
python3 x6.py export runs/browser-001 --output exports/browser-001.zip
python3 x6.py verify exports/browser-001.zip
```

Der Import prüft und berechnet den nativen Bericht neu. Seine Originalbytes
einschliesslich optionaler Gegenbeispiele bleiben unter
`native/signal/evidence.json` erhalten. Umgekehrt lässt sich die native JSON-Datei
eines CLI-Signallaufs unverändert im vorhandenen Lab importieren. Das ZIP selbst
wird durch die CLI geprüft, nicht in den JSON-Dateidialog des Labs geladen.

## 4. Der dokumentierte vollständige Ablauf

Nach der Installation aus demselben Checkout:

```sh
python3 x6.py run signal --output runs/signal-001
python3 x6.py verify runs/signal-001
python3 x6.py export runs/signal-001 --output exports/signal-001.zip
python3 x6.py verify exports/signal-001.zip

python3 x6.py run spectral --output runs/spectral-001
python3 x6.py verify runs/spectral-001
python3 x6.py export runs/spectral-001 --output exports/spectral-001.zip
python3 x6.py verify exports/spectral-001.zip

python3 x6.py run rax --output runs/rax-001
python3 x6.py verify runs/rax-001
python3 x6.py export runs/rax-001 --output exports/rax-001.zip
python3 x6.py verify exports/rax-001.zip
```

| Adapter | Tatsächliche Ausführung | Erhaltenes wissenschaftliches Urteil |
| --- | --- | --- |
| `signal` | Vorhandener Edge-Runner und Signal-Lab-Kern; gleicher synthetischer Auftrag, JSON-Replay und CSV aus denselben Arrays | Vier getrennte Filterstatus. Im mitgelieferten Pulsbeispiel darf der X6-Phasenfilter FAIL melden, obwohl Ausführung und Export korrekt sind. |
| `spectral` | Unveränderte Python-Referenz mit fünf festen rationalen Graphfällen, einschliesslich ungültiger Schranken und getrennter Komponenten | Erfolg dieser fünf Referenzfälle; keine vollständige Prüfung aller Browserfunktionen und kein physikalischer Nachweis. |
| `rax` | Unverändertes veröffentlichtes RAX-M1-Paket mit vollständiger B1-Nachrechnung, Methoden-Gegenbeispielen und Zusatzprüfungen | Acht primäre B1-Vergleiche bleiben INCONCLUSIVE; die gefundenen Methodenfehler bleiben sichtbar. |

Ein eigener Signalauftrag wird mit `run signal --job job.json --output ...`
übergeben. Das Format ist der bestehende
[`x6.edge-reference.job/0.1`-Vertrag](../experimental/edge_reference/README.md).
Andere Adapter akzeptieren keine frei eingegebenen Programme oder Jobdateien.
Die RAX-Kommandos wiederholen vorhandene Belege; sie starten keine neue
Bestätigungskampagne. Ein RAX-Replay kann je nach Rechner eine Minute oder länger
dauern. Die Zeitgrenze pro Unterprozess beträgt 240 Sekunden und kann bewusst
mit `--timeout` zwischen 1 und 3600 Sekunden gesetzt werden.

## 5. Einheitlicher Exportvertrag

| Datei / Ordner | Bedeutung |
| --- | --- |
| `run.json` | `x6.integration.run/1`: Abschlussvermerk, Adapter, Operation, Laufzeitumgebung, Quellhashes und vollständiges Dateiinventar mit Grössen und SHA-256. Wird zuletzt geschrieben. |
| `summary.json` | `x6.integration.summary/1`: Ausführungsstatus, Backend-Prüfstatus, Evidenzklasse, natives fachliches Ergebnis und Geltungsgrenzen. |
| `native/` | Native Belege ohne Umdeutung; beim Signal vollständige Eingabe, JSON und CSV, bei RAX Originalpaket und sämtliche neu erzeugten Prüf-JSONs. |
| `logs/` | Standardausgabe, Fehlermeldungen und Exitcodes der tatsächlich ausgeführten Unterprozesse. |
| `failure.json` | Nur bei gescheiterten Versuchen. Ein solcher Ordner ist kein abgeschlossener Lauf und kann nicht als gültiger Export bestehen. |

`verify` prüft das exakte Dateiinventar und führt danach das jeweilige Backend
erneut aus. Damit wird eine manipulierte Ergebnisangabe auch dann erkannt,
wenn jemand ihre Prüfsumme passend neu berechnet hat. Native Signal-Replays
verwenden die bestehenden Toleranzen des Signal Labs. RAX-Vergleiche übernehmen
die dokumentierten Ausnahmen für Laufzeitmetadaten sowie relative Toleranz
1e-12 und absolute Toleranz 1e-15 für Gleitkommazahlen. Exakte Werte, IDs,
Status, Hashwerte und Zählungen müssen unverändert übereinstimmen.

`export` prüft Inventar und Hashwerte, kopiert sämtliche Nutzdateien verlustfrei
und veröffentlicht das fertig geschriebene ZIP ohne Überschreiben. Es führt
selbst keine zusätzliche wissenschaftliche Nachrechnung aus; dafür folgt
`verify exports/...zip`. ZIP-Imports weisen Pfadwechsel, doppelte Mitgliedsnamen,
symbolische Links und übergrosse Inhalte zurück. Dies ist eine lokale
Integritätsprüfung, keine qualifizierte Sandbox oder Stromausfallsicherheit.

Quellhashes müssen zum verwendeten Checkout passen. Bei späteren Änderungen
den passenden Quellstand mit den Belegen aufbewahren. Commit, Zeitstempel und
Laufzeitumgebung sind aufgezeichnete Metadaten, keine authentifizierte Herkunft.
Eine kohärent neu erzeugte synthetische Evidenz ist weiterhin kein Messnachweis.

CLI-Exitcode 0 bedeutet erfolgreiches Kommando; Exitcode 1 bezeichnet fehlende
Voraussetzungen, Eingabe-, Lauf- oder Prüfungsfehler. Ungültige Kommandozeilen
liefern den üblichen argparse-Exitcode 2. Ein fachliches `FAIL` oder
`INCONCLUSIVE` kann bei korrekt ausgeführter Software mit Exitcode 0 erscheinen.

## 6. Abnahme aus einem frischen Checkout wiederholen

Der automatische Abnahmelauf verlangt einen sauberen Checkout **ohne `.venv`**
und ein neues Belegverzeichnis ausserhalb des Checkouts:

```sh
python3 tests/integration/qualify_checkout.py --output ../x6-integration-evidence
```

Er installiert die Forschungsumgebung, prüft deren Isolation, führt die
Regressionstests und alle drei oben dokumentierten Abläufe einschliesslich
ZIP-Replay aus, prüft negative Kontrollen und verlangt unveränderte Quellen.
Ohne den optionalen Browsertest lautet das Ergebnis `PASS_CORE_WORKFLOW`;
Browserbedienung ist dann ausdrücklich `NOT_EXECUTED`.

Für die zusätzliche Prüfung der Oberfläche und des tatsächlichen
Browser–CLI-Exportaustauschs benötigt nur der Testtreiber Playwright 1.62.1:

```sh
npm install --prefix ../x6-browser-test --no-save --no-package-lock playwright@1.62.1
node ../x6-browser-test/node_modules/playwright/cli.js install chromium
NODE_PATH=../x6-browser-test/node_modules python3 tests/integration/qualify_checkout.py --output ../x6-integration-evidence --with-browser
```

Ein vorhandenes kompatibles Chromium kann über `X6_CHROMIUM_EXECUTABLE`
angegeben werden. Die tatsächlich getestete Browserversion wird aufgezeichnet.
Der Bericht zählt konkrete Prüfungen und enthält keine behauptete externe
Begutachtung. Ein Fehler beendet die Abnahme mit Status FAIL und erhält Logs.

## Weitere Module und Grenzen

Sagnac-Dateiimport ist über die vorhandene Astrolabium-Oberfläche erreichbar.
Eine UART-Anbindung hat einen eigenen
[Geräteadapter und Prüfbereich](SAGNAC_INTEGRATION.md); sie wird durch diesen
Einstieg nicht gestartet. Zusätzlich zu den drei lokalen Adaptern enthält main
inzwischen getrennte ACVM-Unterbefehle:

```sh
python3 x6.py control qualify --output runs/c1-qualification
python3 x6.py acvm qualify --output runs/acvm-qualification
```

Sie prüfen Software-/Modellpfade; Voraussetzungen und offene Geräteabnahmen
stehen im [Modulregister](MODULE_REGISTRY.md). Hardwarequalifikation,
Julia-Gesamtprüfung, optisch-mechanische CAD-Prüfungen und externe Datenagenten
sind nicht durch die Abnahme der drei lokalen Adapter mitgeprüft.

Zur Entfernung die erzeugte `.venv` und bewusst gewählten Lauf-/Exportordner
löschen; es wurden keine globalen Python-Pakete installiert. Aufzubewahrende
Belege und der dazugehörige Quellstand bleiben bei einer Deinstallation erhalten.
