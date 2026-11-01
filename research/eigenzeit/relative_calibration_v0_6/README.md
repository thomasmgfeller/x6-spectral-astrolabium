# Eigenzeit v0.6 · Relative Kalibrierung bei mittlerer Nachweisrate

Wie viele markierte Referenzversuche braucht es, um die Krümmungsauswertung aus v0.4 freizugeben? Unter den Voraussetzungen der Studie v0.5 genügen für die relative Kalibrierung **47 Millionen Versuche je Zelle**, insgesamt **752 Millionen**. Das spart gegenüber dem früheren Plan 288 Millionen Versuche oder 27,7 %. Die untere und die obere Grenze gelten für vorab festgelegte Budgets. [Bericht (PDF)](Eigenzeit_Relative_Kalibrierung_v0_6.pdf) · [Vollständiger Beweis](BEWEIS.md) · [Prüfpaket mit Code und Rohzählungen (ZIP)](Eigenzeit_Relative_Kalibrierung_v0_6_Pruefpaket.zip)

| Welches Budget? | Markierte Referenzversuche in 16 Zellen |
|---|---:|
| Nachgewiesene Untergrenze bei beliebigen festen Zellbudgets | 420.800.008 |
| Nachgewiesene Untergrenze bei gleich großen festen Zellbudgets | 420.800.016 |
| Ausführbarer, hinreichender Messplan v0.6 | 752.000.000 |
| Bisheriger hinreichender Messplan v0.5 | 1.040.000.000 |

Der tatsächliche Mindestaufwand innerhalb dieser Spanne ist offen. Der Test prüft einen maximalen Dichtekontrast von 1,002 im vollständigen vierdimensionalen Kausaldiamanten. Für die Erzeugungsdichte, den Referenztransfer einschließlich Drift und die Effizienzschwankung innerhalb jeder Zelle setzt er jeweils eine unabhängig belegte Kontrastgrenze von 1,0001 voraus. Eine Fehlfreigabe bei zu hohem Dichtekontrast hat eine Wahrscheinlichkeit von höchstens 0,989 %. In der günstigen Klasse (kleinstes Zellmittel mindestens 0,49 und Verhältnis der Zellmittel höchstens 1,0002) liegt die Freigabewahrscheinlichkeit bei mindestens 99,737 %. [Numerisches Zertifikat](certificate.json) · [Vorstudie v0.5](../calibration_v0_5/README.md)

**Für eine reale Messung gilt HOLD.** Markierte Referenzzählungen und unabhängige Belege für die externen Grenzen stehen aus. Ohne Freigabe bleiben alle drei Rastermodelle und das volle Krümmungsintervall zulässig. Über alle Wiederholungen einschließlich HOLD bleibt die modellweite Überdeckung bei mindestens 95,15 %. In der günstigen Klasse beträgt die Wahrscheinlichkeit der richtigen Einzelausgabe für jeden Rasterpunkt mindestens 80,11 %. [Leeres Feldprotokoll](field_no_evidence.json)

## Reproduktion

Vom Wurzelverzeichnis des Repositorys aus mit Python 3.12 ausführen.

```sh
python -m pip install -r tools/workflow/requirements-research.txt
python -B research/eigenzeit/relative_calibration_v0_6/publication_check.py --replay
```

Die Prüfung vergleicht den Bericht, alle 48 Archiveinträge, die zwei internen Prüfsummenlisten und die separat verlinkten Dateien. Zusätzlich gleicht sie die 31 übernommenen Eingaben mit dem veröffentlichten v0.5-Archiv ab. Der Wiederholungslauf berechnet die endlichen Budgetschranken, zählt alle 480.000 synthetischen Pilotentscheidungen erneut aus und erzeugt die Rohzählungen aus den festgelegten Seeds. Alle acht Szenarien sind gepaart mit v0.5 ausgewertet. [Pilotergebnisse](pilot.json) · [Prüfprotokoll](verification.json) · [Dateien und Prüfsummen](PUBLICATION.json)
