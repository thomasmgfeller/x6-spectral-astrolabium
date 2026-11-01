# Hanford-Messarchiv im Stabilitätslab

Das Archiv enthält kalibrierte Dehnungsmessungen des LIGO-Interferometers H1. Im Messlauf S6 wurden die Spiegel zu dokumentierten Zeiten mit Testsignalen angeregt. Über „Hanford“ im Stabilitätslab lässt sich jede archivierte Kurve mit ihren Qualitätsmasken und dem dazugehörigen Ergebnis herunterladen. Der Versuch untersucht die Antwort eines festgelegten Filters auf einen historischen Eingriff.

## Importieren und speichern

Voraussetzungen sind Python 3.12 und ein POSIX-Dateisystem mit Dateisperren, z. B. unter Linux oder macOS. Im Hauptverzeichnis des Repositorys:

```sh
python3 -m venv .venv
. .venv/bin/activate
python -m pip install -r agent/hanford-requirements.txt
python -m agent.hanford
python -m agent.hanford --verify
python -m http.server 8000 --bind 127.0.0.1
```

Dann [das lokale Stabilitätslab öffnen](http://localhost:8000/app/causal-stability/#hanford) und „Messarchiv öffnen“ wählen. Die zwei archivierten Pilotfenster sind bereits im Repository enthalten. Für eine unabhängige Neuaufnahme aus dem Archiv dient ein leeres Zielverzeichnis:

```sh
python -m agent.hanford --archive runs/hanford-review --cache runs/hanford-source
python -m agent.hanford --archive runs/hanford-review --verify
```

Der Import liest den öffentlichen H1-Katalog und fragt die GWOSC-API nach den passenden HDF5-Dateien. Die Grundauswahl sind die ersten beiden Katalogzeiten mit Signalform `sinegaussian-235.0-9.0-0.0-0.0` und nominellem hrss von 2,08 × 10⁻²¹. Mit `--count 4` wird dieselbe Auswahl in zeitlicher Reihenfolge auf vier erweitert. Die Auswahl verwendet das publizierte SNR weder als Filter noch als Rangfolge.

Das Standardziel für vollständige Messfenster und Ergebnisindex ist `app/causal-stability/hanford-data/`. Original-HDF5-Dateien und Katalogstand liegen nach einem frischen Abruf unter `runs/hanford-hdf5/`. Jeder erfolgreiche Import schreibt ein JSON pro GPS-Zeit und aktualisiert den Index atomar. Ein Abbruch lässt bereits indexierte Aufnahmen nutzbar. Wiederholte Aufrufe prüfen vorhandene Datensätze und fügen nur fehlende hinzu. Ein späterer Prüffehler beendet den Lauf mit einer Fehlermeldung. Ein Fenster über eine Dateigrenze wird zurückgewiesen. Für die beiden Pilot-Quelldateien prüft der Import feste SHA-256-Werte. Bei später hinzugenommenen Dateien dokumentiert er den beim Abruf berechneten Hash.

Der GitHub-Workflow **Hanford measurement archive** kann nach Aufnahme in den Standardbranch über „Run workflow“ ausgelöst werden. Er ruft bis zu sechs Katalogfenster frisch ab und stellt das Ergebnisarchiv 30 Tage als herunterladbares Artefakt bereit. Die versionierten Pilotdaten sind davon unabhängig dauerhaft über Git verfügbar. Es ist kein periodischer Auftrag eingerichtet.

## Messfenster und Auswertung

Jede JSON-Datei enthält 16.384 unveränderte Strain-Werte bei 4.096 Hz. Der erste Wert gehört zur GPS-Sekunde floor(Katalogzeit) − 2. Das Fenster umfasst vier Sekunden mit exklusivem Ende. Für jede Sekunde speichert der Import die beiden Original-Bitmasken mit den Bezeichnungen aus der jeweiligen HDF5-Datei. DATA und BURST_CAT1 müssen durchgehend gesetzt sein. In S6 muss HW_BURST in der Zielsekunde **gesetzt** sein. Nichtendliche Werte führen zum Abbruch. Die Prüfsumme des Messvektors bezieht sich auf IEEE-Float64 in Little-Endian-Reihenfolge.

Der unabhängige Auswertewert ist die maximale lokale Amplitude bei 235 Hz. Für jedes Fenster aus 256 Samples wird die komplexe Fourierkomponente mit symmetrischem Hann-Fenster berechnet. Die Amplitude beträgt zweimal den Betrag, geteilt durch die Summe der Fenstergewichte. Zugelassen sind Fenstermitten innerhalb ±0,25 s um die veröffentlichte Katalogzeit. Der Betrag ist phasenunabhängig. Es erfolgt keine Rauschgewichtung. Amplitude und Zeitversatz sind diagnostische Grössen. Das von GWOSC publizierte Matched-Filter-SNR ist im JSON separat als Katalogwert gekennzeichnet. Zwei gezielt angeregte Fenster erlauben keine Schätzung einer Fehlalarmrate und keine Aussage über Langzeitstabilität oder einzelne interne Ausbreitungswege.

| H1-Zeitpunkt (GPS) | Eigene Spitzenamplitude (Strain) | Zeitversatz zur Katalogzeit | GWOSC-SNR |
|---|---:|---:|---:|
| 932197539.80 | 3,481 × 10⁻²⁰ | −4,47 ms | 74,90 |
| 932316845.40 | 2,955 × 10⁻²⁰ | −2,42 ms | 58,07 |

## Ergebnisse für Dritte

`hanford-data/index.json` enthält Dateinamen, GPS-Zeit, SHA-256, den eigenen Filterwert, die Katalog-SNR und die Methodenversion. Die referenzierten JSON-Dateien enthalten zusätzlich die Messung, Original-URLs, Quellhashes und Qualitätsmasken. Dieser lesbare Index kann als Ergebnisfeed verwendet werden. Code und geprüfter Index können gemeinsam in einem versionierten GitHub-Release archiviert werden. Nach einer einmaligen Verknüpfung kann Zenodo dafür automatisch einen DOI vergeben. Der Review und eine etwaige Verwendung liegen bei den jeweiligen Forschenden.

GWOSC bietet lesenden Archivzugriff. Für Hinweise zu reproduzierbaren Datenabweichungen veröffentlicht GWOSC ein Community-Forum und einen Kontakt. Vor einem Hinweis sollten Dritte die betreffende Zeit, die Datenqualität und die Verarbeitung unabhängig nachvollziehen können.

- [GWOSC-API](https://gwosc.org/api/)
- [H1-Injektionstabelle](https://gwosc.org/static/injections/s6/burst/H1_s6burst_simple.txt) und [Beschreibung der S6-Burst-Injektionen](https://gwosc.org/s6hwburst/)
- [GWOSC-Kontakt](https://gwosc.org/contact/) und [Zenodo-Anbindung für GitHub](https://help.zenodo.org/docs/github/enable-repository/)

## Herkunft und Lizenz

Die Messdaten stammen vom Gravitational Wave Open Science Center, einem Dienst der LIGO Scientific Collaboration, der Virgo Collaboration und der KAGRA Collaboration. GWOSC veröffentlicht die Daten unter CC BY 4.0. Die hier vorgenommenen Änderungen bestehen aus der zeitlichen Auswahl, der Serialisierung der kalibrierten Werte in JSON und der separaten Filterauswertung. Quellenangaben und vollständige Danksagung für Weiterveröffentlichungen stehen bei GWOSC.

- [S6-Datenfreigabe](https://gwosc.org/S6/)
- [Vollständige Danksagung und Zitierhinweise](https://gwosc.org/acknowledgement/)
- [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/)
- [R. Abbott et al., SoftwareX 13 (2021), 100658](https://doi.org/10.1016/j.softx.2021.100658)
