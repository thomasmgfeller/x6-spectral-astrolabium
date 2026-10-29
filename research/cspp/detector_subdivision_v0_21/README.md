# CSPP v0.21: unterteilter Detektor

Die deterministische Detektorunterteilung und eine exakt bewiesene monotone
Schichtkernhülle verkleinern den direkten Beitrag um 54-74 %. Für den bereits
integrierten Historybereich `P=[-6,-5] x [-2,2]^3` sinken die vollständigen
oberen bedingten Erwartungswertschranken um 42-55 % auf etwa 0,00221-0,00312.
Die bekannten und unbekannten aktiven Transportbeiträge bleiben enthalten.

**METHOD_HOLD und G1 HOLD bleiben.** Der übrige äußere Historybereich ist
nicht neu zertifiziert. Die globale v0.19-Majorante bleibt unverändert;
es wird keine obere Patchgrenze von einer oberen Gesamtgrenze abgezogen.
Die Vergleichsgröße 0,001 ist kein neues Teilbudget. Keine neuen Wolken,
Seeds, statistischen Schwellen oder unabhängigen Bestätigungsdaten.

- [Ergebnisbericht (PDF)](Detektor_Unterteilung_v0_21.pdf)
- [Vollständiges Prüfpaket (ZIP)](CSPP_Detektor_Unterteilung_v0_21_Pruefpaket.zip)
- [Herleitung und Grenzen](cspp_v021/PROOF.md)
- [192-Bit-Ergebnisse](cspp_v021/results/DETECTOR_192.json)
- [Prüfresultate](cspp_v021/results/CHECKS.json)
- [Nächste wissenschaftliche Schritte](cspp_v021/NEXT_STEPS.json)

Die ursprünglichen 42 Paketdateien, PDF und ZIP werden bytegenau publiziert.
`NOT_PERFORMED_FOR_V021` in der ursprünglichen Paketmetadaten ist der
festgehaltene Stand vor Veröffentlichung. Die aktuelle Veröffentlichung
wird separat in [PUBLICATION.json](PUBLICATION.json) dokumentiert.

## Reproduktion

```sh
python3 -m pip install numpy==2.3.5 python-flint==0.8.0
python3 -O -B research/cspp/detector_subdivision_v0_21/publication_check.py
python3 -B research/cspp/detector_subdivision_v0_21/publication_check.py --replay
```

Der vollständige Wiederholungslauf berechnet beide Präzisionen in einem
temporären Verzeichnis neu und verlangt sieben byteidentische numerische
Ergebnisdateien. Die ursprünglichen Paketdateien bleiben unverändert.
Die Veröffentlichung prüft außerdem ZIP-Inhalt, 41 Paketprüfsummen,
Quellenidentitäten, alle acht Archiv-/Fensterfälle und die HOLD-Grenzen.
Ein unabhängiges externes Fachreview wird nicht behauptet.
