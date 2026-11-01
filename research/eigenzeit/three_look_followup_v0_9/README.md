# Eigenzeit v0.9 · Lohnt sich ein dritter Messstand?

Alle 16 Zellen beginnen mit je 22 Millionen markierten Referenzversuchen. Die Endpunkte noch offener Vergleiche erhalten bei Bedarf 9 Millionen zusätzliche Versuche und nach einem weiteren Entscheid höchstens 15 Millionen weitere. [Bericht (PDF)](Eigenzeit_Dreistufige_Nachmessung_v0_9.pdf) · [Mathematische Herleitung](BEWEIS.md) · [Prüfpaket mit Code und Rohzählungen (ZIP)](Eigenzeit_Dreistufige_Nachmessung_v0_9_Pruefpaket.zip)

| Messaufwand über alle 16 Zellen | Referenzversuche |
|---|---:|
| Erste Stufe v0.9 | 352.000.000 |
| Obergrenze für den Erwartungswert bei jedem günstigen Profil | 418.670.605 |
| Erste Stufe v0.8 | 432.000.000 |
| Höchstaufwand je Durchlauf für beide Pläne | 736.000.000 |

In der günstigen Klasse liegt jede Nachweisrate bei mindestens 49 % und das Verhältnis der Zellmittel bei höchstens 1,0002. Für jedes solche Profil spart v0.9 im Mittel nachweislich mindestens 3,08 % gegenüber v0.8. Mit derselben verbesserten Beweismethode sinkt die obere Kostengrenze schon für den unveränderten v0.8-Plan auf 459.383.912. Die Studie unterscheidet diesen rechnerischen Gewinn von der Einsparung durch den neuen Messplan. [Zertifikat](certificate.json) · [Vorstudie v0.8](../selective_followup_v0_8/README.md)

Im gepaarten Pilot mit acht hohen Zellen am günstigen Rand betrug der mittlere Aufwand 402,29 Millionen Versuche für v0.9 und 451,94 Millionen für v0.8. Bei homogen 10 % Effizienz außerhalb der günstigen Klasse war v0.9 mit 546,21 gegenüber 524,32 Millionen teurer. [Ergebnisse aller acht Profile](pilot.json)

**Für reale Messungen gilt HOLD.** Es fehlen markierte Referenzzählungen und unabhängige Nachweise für Erzeugungsdichte, Drift und Effizienzschwankungen innerhalb der Zellen. Bei gültigen Modellannahmen bleibt die Fehlfreigabe über alle drei Messstände unter 0,973 %, die Überdeckung des Krümmungsintervalls einschließlich HOLD bei mindestens 95,15 %. Zwei vollständige Beispielprotokolle zeigen, wie bei identischem wissenschaftlichem Zähler allein die letzte Nachmessung von C02 den Unterschied zwischen GO und HOLD ausmacht. Beide benötigen 409 Millionen Referenzversuche. [Feldvorlage](field_worksheet.json) · [Beispiel GO](final_go.json) · [Beispiel HOLD](final_hold.json)

## Reproduktion

Im Wurzelverzeichnis des Repositorys mit Python 3.12 ausführen.

```sh
python -m pip install -r tools/workflow/requirements-research.txt
python -B research/eigenzeit/three_look_followup_v0_9/publication_check.py --replay
```

Die Prüfung vergleicht Bericht, Archiv, die internen Prüfsummenlisten, die oben verlinkten Auszüge und die übernommenen Dateien aus dem veröffentlichten v0.8-Archiv. Der Wiederholungslauf berechnet die Schranken neu und reproduziert die Zählungen aller 80.000 gepaarten synthetischen Durchläufe. Die unabhängige Auswertung prüft unter anderem zwölf feste Profile mittels Binomialverteilungen und 46.656 mögliche Datenverläufe in einem kleinen Dreistufenexperiment. [Prüfprotokoll](verification.json) · [Veröffentlichungsnachweis](PUBLICATION.json)

Die Folgestudie untersucht, wie viel Referenzaufwand eine unabhängig belegte Driftreserve von 20 ppm erfordert und ab welcher Restunsicherheit Zählungen allein keine Entscheidung mehr ermöglichen. [Eigenzeit v0.10 · Driftreserve](../drift_reserve_v0_10/README.md)
