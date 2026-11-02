# NICER-Archiv im kausalen Stabilitätslabor

Wie stark unterschätzt man die Röntgenzählrate, wenn man Beobachtungspausen als Messzeit zählt? Der Vergleich verwendet bereinigte XTI-Ereignisse auf der Sichtlinie zum Millisekundenpulsar PSR J0030+0451. Quelle, Detektor und Hintergrund tragen zur beobachteten Rate bei. Aus diesem Vergleich lässt sich weder das Gravitationsfeld noch die Pulsform bestimmen. Das Labor verwendet die Daten als Kontrolle für Verfahren, die mit Messlücken umgehen müssen.

## Eine Aufnahme nachrechnen

Am 24. Juli 2017 registrierte NICER im ausgewählten Energieband 1 003 Ereignisse innerhalb von 15 gültigen Zeitintervallen. Vom Anfang des ersten bis zum Ende des letzten Intervalls verstrichen 12 037 s. Davon entfallen 1 162 s auf gültige Messzeit.

| Mittelwert | Rechnung | Ereignisse/s |
|---|---|---:|
| Pro Sekunde gültiger Messzeit | 1 003 / 1 162 | 0,86317 |
| Pro Sekunde verstrichener Zeit | 1 003 / 12 037 | 0,08333 |

Beide Zahlen verwenden dieselben Ereignisse. Die verstrichene Zeit im Nenner senkt den Wert um den Faktor 10,36. Die lokal mitgelieferte Aufnahme hat die ObsID `1060020101`. Bei der zweiten Aufnahme oder einem anderen Ziel muss der Faktor neu berechnet werden.

## Datenweg und Wiederholung

Der schlüssellose HEASARC-TAP-Dienst liefert den Beobachtungskatalog als VOTable. Der Import wählt nach ObsID aufsteigend die ersten 52 validierten und bereits freigegebenen Beobachtungen mit positiver Exposition und exaktem Zielnamen `PSR_J0030+0451`. Diese begrenzte historische Auswahl dient dem Methodenvergleich. [Katalog und Felddefinitionen](https://heasarc.gsfc.nasa.gov/W3Browse/nicer/nicermastr.html) · [Archivzugang](https://heasarc.gsfc.nasa.gov/docs/nicer/analysis_threads/access-data/)

Am 2. November 2026 endete der Import nach zwei archivierten Pulsarbeobachtungen. Der Wochenzeitplan und die Startmöglichkeiten für weitere Abrufe über GitHub Actions sind aufgehoben. Das Labor liest die gespeicherten Lichtkurven. [Messarchiv](https://github.com/thomasmgfeller/x6-spectral-astrolabium/tree/nicer-data) · [Frühere Importläufe](https://github.com/thomasmgfeller/x6-spectral-astrolabium/actions/workflows/nicer-archive.yml)

Der Browser prüft den SHA-256 der ausgewählten JSON-Datei. Wenn das Online-Verzeichnis nicht erreichbar ist, kennzeichnet er die mitgelieferte Referenzaufnahme. Jeder Datensatz nennt die FITS-Adresse, den SHA-256 der heruntergeladenen komprimierten Originaldatei, den Abrufzeitpunkt und die Verarbeitungs- und Kalibrationsversion. Das Original liegt bei HEASARC. Bei einem unvollständigen Abruf bleibt das veröffentlichte Verzeichnis gültig.

Für die lokale Wiederholung unter Linux ab Repository-Wurzel mit Python 3.12:

```sh
python3.12 -m venv .venv-nicer
.venv-nicer/bin/pip install -r agent/nicer-requirements.txt
.venv-nicer/bin/python -m unittest discover -s tests/python -p test_nicer.py -v
.venv-nicer/bin/python -m agent.nicer runs/nicer
```

## Was die Werte bedeuten

1. Ausgangspunkt ist die bereinigte, über die sieben MPUs zusammengefasste Level-2-Ereignisdatei. Der Import prüft Instrument, Beobachtung, Ziel, Zeitbasis sowie die FITS-Prüfsummen der verwendeten Tabellen.
2. In das Band fallen kalibrierte PI-Kanäle 30 bis einschliesslich 299 (0,30 bis unter 3,00 keV). Die gemeinsame GTI-Tabelle gibt die gültigen Messzeiten vor. Ereignis- und GTI-Zeiten werden mit ihren jeweiligen TIMEZERO-Offsets auf lokale TT-Missionssekunden bezogen. Die Zeitachse der Grafik beginnt am Anfang des ersten gültigen Intervalls.
3. Die 64-s-Fenster sind links geschlossen und rechts offen. Für jedes Fenster wird die Schnittdauer mit allen GTIs aufsummiert. Die Höhe eines Punktes ist die Zahl akzeptierter Ereignisse geteilt durch die gültigen Sekunden des Fensters. Auch ein teilweise belegtes Fenster erscheint in seiner nominellen Mitte. Null Ereignisse bei positiver Messzeit ergeben eine echte Null. Fenster ohne Messzeit fehlen.
4. Im JSON hat jedes Element von `bins` die Form `[Fensterindex, Ereignisse, gültige Sekunden]`. Für ein gröberes Mittel summiert man zunächst Ereignisse und gültige Sekunden jeder Gruppe und dividiert erst am Ende. Die Analyse verwendet keine zusätzliche Totzeit-, Hintergrund- oder baryzentrische Korrektur. Die archivierte Kalibration ist im Datensatz angegeben.

[Mission Guide](https://heasarc.gsfc.nasa.gov/docs/nicer/mission_guide/) · [Verarbeitungsstufen](https://heasarc.gsfc.nasa.gov/docs/nicer/analysis_threads/level-0-1-2-3/)

## Nachweis und Weiterverwendung

Die Messdaten stammen von der NASA-Mission NICER und wurden vom High Energy Astrophysics Science Archive Research Center (HEASARC) der Astrophysics Science Division am NASA Goddard Space Flight Center bereitgestellt. Das X6-Projekt verantwortet die Auswahl, zeitliche Gruppierung und Darstellung. Die Quellenangabe gehört zur Auswertung. Bei einer Publikation, zu der das Archiv wesentlich beiträgt, bittet HEASARC um die dort angegebene Danksagung. Die Bedingungen externer Daten sind im Lizenzumfang des Projekts getrennt ausgewiesen. [HEASARC-Nutzungsbedingungen und Danksagung](https://heasarc.gsfc.nasa.gov/docs/heasarc/data_policy.html) · [Lizenzumfang des Projekts](../../../../LICENSE_SCOPE.md)

Instrumentreferenz: K. C. Gendreau et al. (2016), *The Neutron star Interior Composition Explorer (NICER): design and development*, Proc. SPIE 9905, 99051H. [DOI](https://doi.org/10.1117/12.2231304)
