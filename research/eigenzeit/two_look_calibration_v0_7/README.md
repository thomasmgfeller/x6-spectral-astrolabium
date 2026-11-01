# Eigenzeit v0.7 · Wann die relative Kalibrierung früher enden kann

Nach 33 Millionen markierten Referenzversuchen je Zelle kann die relative Kalibrierung mit GO oder HOLD enden. Nur ein unklarer Zwischenstand führt zu 13 Millionen weiteren Versuchen je Zelle. Für diesen vorab festgelegten Plan gelten die beiden Fehlergrenzen von v0.6. [Bericht (PDF)](Eigenzeit_Zweistufige_Kalibrierung_v0_7.pdf) · [Vollständiger Beweis](BEWEIS.md) · [Prüfpaket mit Code, Feldbeispielen und Rohzählungen (ZIP)](Eigenzeit_Zweistufige_Kalibrierung_v0_7_Pruefpaket.zip)

| Messaufwand über alle 16 Zellen | Referenzversuche |
|---|---:|
| Erster möglicher Abschluss | 528.000.000 |
| Obergrenze für den Erwartungswert in der günstigen Klasse | 575.174.011 |
| Höchstaufwand pro Durchlauf mit v0.7 | 736.000.000 |
| Fester Vergleichsplan v0.6 | 752.000.000 |

In der günstigen Klasse hat jede Zelle mindestens 49 % Nachweisrate und das Verhältnis von größtem zu kleinstem Zellmittel beträgt höchstens 1,0002. Für jedes solche Profil spart der Plan im Mittel mindestens 23,5 % gegenüber v0.6. Die Wahrscheinlichkeit einer irrtümlichen Freigabe bei zu großem Dichtekontrast liegt über beide Messstufen zusammen unter 0,983 %. Bei gültigen externen Annahmen beträgt die Überdeckung des anschließenden Krümmungsintervalls über alle Durchläufe einschließlich HOLD mindestens 95,15 %. [Zertifizierte Grenzen](certificate.json) · [Vorstudie v0.6](../relative_calibration_v0_6/README.md)

**Feldstatus HOLD.** Für den realen Aufbau fehlen markierte Referenzzählungen und unabhängige Nachweise für Erzeugungsdichte, Drift und Effizienzschwankung innerhalb der Zellen. Der erste Messstand und seine Entscheidung sind vor einer Fortsetzung festzuhalten. Bei CONTINUE bleibt die Geometrieentscheidung ausstehend. Bei HOLD gibt das Verfahren die vollständige Modellmenge zurück. [Feldprotokoll zum Ausfüllen](field_worksheet.json)

Die Folgestudie v0.8 misst gezielt die Endpunkte noch offener Zellenpaare nach. In der günstigen Klasse liegt der erwartete Gesamtaufwand bei höchstens 480.785.992 Versuchen. [Selektive Nachmessung mit Beweis und Gegenbeispiel](../selective_followup_v0_8/README.md)

## Reproduktion

Vom Wurzelverzeichnis des Repositorys aus mit Python 3.12 ausführen.

```sh
python -m pip install -r tools/workflow/requirements-research.txt
python -B research/eigenzeit/two_look_calibration_v0_7/publication_check.py --replay
```

Die Prüfung vergleicht Bericht, Prüfpaket, die internen Prüfsummenlisten und die separat verlinkten Dateien. Sie gleicht die übernommenen Quellen mit dem veröffentlichten v0.6-Archiv ab. Der Wiederholungslauf berechnet das Zertifikat neu, prüft die Entscheidungslogik und reproduziert die Rohzählungen aus den festgelegten Seeds. Der Pilot umfasst 96.000 gepaarte synthetische Durchläufe mit 384.000 unabhängig nachgezählten Schwellenvergleichen. [Pilotergebnisse](pilot.json) · [Prüfprotokoll](verification.json) · [Veröffentlichungsnachweis](PUBLICATION.json)
