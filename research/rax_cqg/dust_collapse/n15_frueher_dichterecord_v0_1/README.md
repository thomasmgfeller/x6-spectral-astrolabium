# CST-DUST · Ein früher Dichteeintrag auf der N15-Kette

**Ergebnis vom 23. November 2026.** Eine einmalige Anwendung der vier äusseren Uhrstellungen aus PR #361 liefert auf dem positiven Referenzfenster keinen universellen Einzelrecord der Dichte an Ereignis 11. Selbst bei kohärenter Kontrolle aller vier Stellungen gibt es kein Messergebnis, dessen Wahrscheinlichkeit allein von dieser Dichte abhängt und sich mit ihr ändert. Die Aussage betrifft den modellierten Zugang zu den vier Quellenphasen bei festgehaltener Präparation.

Zwei zulässige Geschichten machen die Grössenordnung sichtbar. Ihre Dichten liegen oberhalb und unterhalb der Schwelle 1/8. Bei gleichen Vorwahrscheinlichkeiten beträgt die beste Trefferwahrscheinlichkeit mit einem Quellenaufruf rund 50,067705 %. Mit zwei Phasenkopplungen an dieselbe ungestörte Geschichte lässt sich dagegen rechnerisch ein Bit mit dichteabhängiger Wahrscheinlichkeit bilden. Seine Kopplung und die Speicherung vor dem Puls sind zusätzliche physikalische Voraussetzungen.

| Prüfung | Ergebnis |
|---|---|
| Frühere vier Wirkungsphasen | Selektiver Mischkoeffizient auf allen 15 Basisdichten bestätigt |
| Störphasen bei festem Zielwert | Zwei unabhängige Variationen innerhalb der ursprünglichen Dichtefenster |
| Einfacher Quellenzugriff | Kein universelles dichteabhängiges Einzelergebnis |
| Zweifacher Zugriff auf dieselbe Geschichte | Bedingte Zeigerphase gleich x/304 |
| Sicherer Nachweis eines Werts ausserhalb des Ursprungsbandes | Für endlich viele reine Phasenabfragen schliesst Analytizität einen solchen Klick ohne Fehlalarm aus |
| Physisches P3-Register | 60 Einträge mit Status NOT_RUN |

Die Entscheidung zwischen festem und bewegtem Dichtefenster sowie die unabhängige Eichung einer positiven Masse bleiben offen. [Ausgangsstudie auf GitHub](https://github.com/thomasmgfeller/x6-spectral-astrolabium/pull/361)

## Nachrechnen

Im entpackten Verzeichnis genügen Python ab Version 3.10 und die Standardbibliothek. Der Prüfer kontrolliert die Herkunft der Eingaben und vergleicht die Neuberechnung mit den archivierten Ergebnissen.

```sh
python3 -B pruefen.py
```

`HERLEITUNG.md` enthält Zugriffsmodell, Beweis, Gegenpaar und Reichweite. `ergebnisse.json` enthält rationale Werte und nach aussen gerundete Intervalle. `quellen/herkunft.json` nennt Commit, Pfade, Git-Objekte und SHA-256 der Eingaben. Der Hauptplan wurde vor der neuen Rechnung lokal gehasht. Die Prüfung zur endlichen Wiederholung und zu den Zeigereffekten ist als spätere Ergänzung datierbar über die dokumentierte Arbeitsreihenfolge. Die lokalen Hashes besitzen keinen unabhängigen Zeitstempel. Für die Paketintegrität steht `sha256sum -c SHA256SUMS` zur Verfügung.
