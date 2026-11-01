# Eigenzeit v0.8 · Welche Zellen brauchen eine zweite Messung?

Der erste Messblock umfasst 27 Millionen markierte Referenzversuche pro Zelle. Bleiben einzelne gerichtete Vergleiche offen, erhalten nur deren Endpunkte je 19 Millionen zusätzliche Versuche. Jede ausgewählte Zelle wird einmal nachgemessen, auch wenn sie in mehreren Paaren vorkommt. [Bericht (PDF)](Eigenzeit_Selektive_Nachmessung_v0_8.pdf) · [Mathematische Herleitung](BEWEIS.md) · [Vollständiges Prüfpaket mit Code und Rohzählungen (ZIP)](Eigenzeit_Selektive_Nachmessung_v0_8_Pruefpaket.zip)

| Messaufwand über 16 Zellen | Referenzversuche |
|---|---:|
| Erste Stufe | 432.000.000 |
| Obergrenze für den Erwartungswert bei jedem günstigen Profil | 480.785.992 |
| Höchstaufwand pro Durchlauf bei Nachmessung aller Zellen | 736.000.000 |

Die günstige Klasse verlangt mindestens 49 % Nachweisrate in jeder Zelle und ein Verhältnis der Zellmittel von höchstens 1,0002. Im Mittel über alle Durchläufe eines solchen Profils werden höchstens 2,57 Zellen nachgemessen. Da v0.7 bereits für seine erste Stufe 528 Millionen Versuche benötigt, beträgt die mittlere Einsparung für jedes günstige Profil mindestens 8,94 %. Die garantierte obere Grenze des Erwartungswerts sinkt gegenüber v0.7 um 16,41 %. Einzelne Durchläufe können teurer sein als ihr v0.7-Gegenstück. [Numerisches Zertifikat](certificate.json) · [Vorstudie v0.7](../two_look_calibration_v0_7/README.md)

## Warum die dritte Zelle zählt

In zwei Beispielen stimmen sowohl die ersten Zählungen als auch die Nachmessungen der Extremzellen C01 und C02 überein. Allein die Nachmessung von C03 unterscheidet sich um 20.000 Treffer. Bei identischem wissenschaftlichem Zähler von 1.157.840 führt das erste Protokoll zur Freigabe mit dem Rasterkandidaten h=1/2. Im zweiten bleiben alle drei Modelle zulässig. [Eingabe für GO](sparse_go.json) · [Eingabe für HOLD](sparse_hold.json)

Unter den nachgewiesenen Modellannahmen bleibt die Wahrscheinlichkeit einer Fehlfreigabe bei zu hohem Dichtekontrast unter 0,976 %. Das anschließende Krümmungsintervall behält einschließlich der HOLD-Fälle mindestens 95,15 % Überdeckung. **Für die reale Messung gilt HOLD.** Es fehlen markierte Referenzzählungen und unabhängige Nachweise für Erzeugungsdichte, Drift und Effizienzschwankungen innerhalb der Zellen. [Feldprotokoll](field_worksheet.json)

Die Folgestudie v0.9 prüft die aktiven Zellen nach kumuliert 22, 31 und 46 Millionen Versuchen. Bei günstigen Profilen liegt der erwartete Verbrauch bei höchstens 418.670.605 Versuchen. [Dreistufiger Messplan, Vergleich und Reproduktion](../three_look_followup_v0_9/README.md)

## Reproduktion

Im Wurzelverzeichnis des Repositorys mit Python 3.12 ausführen.

```sh
python -m pip install -r tools/workflow/requirements-research.txt
python -B research/eigenzeit/selective_followup_v0_8/publication_check.py --replay
```

Die Prüfung gleicht die beiden Originaldateien, alle 60 Archiveinträge, die internen Prüfsummenlisten und die öffentlich verlinkten Auszüge ab. Die 39 übernommenen Eingaben werden mit dem veröffentlichten v0.7-Archiv verglichen. Der Wiederholungslauf berechnet die analytischen Schranken erneut, prüft die Gegenbeispiele und reproduziert die Rohzählungen für 80.000 gepaarte synthetische Durchläufe. [Pilotergebnisse](pilot.json) · [Prüfprotokoll](verification.json) · [Veröffentlichungsnachweis](PUBLICATION.json)
