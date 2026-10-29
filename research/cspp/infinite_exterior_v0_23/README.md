# CSPP v0.23: unendlicher Rest und vollständige globale Bilanz

Der gesamte unendliche History-Rest für **t < −6** ist auf dem vollständigen
KG-Träger eingeschlossen und mit der unveränderten endlichen Außenhistory
aus v0.22 verbunden. Über vier feste Archive und beide Detektorfenster
liegen die neuen oberen bedingten Erwartungswertschranken des absoluten
globalen Restes bei rund **3,17 bis 3,75 × 10¹⁰**. Gegenüber der bisherigen
globalen v0.19-Majorante ist das etwa Faktor **6982 bis 9130** enger.

**METHOD und G1 bleiben HOLD.** Das unveränderte Ziel 0,001 ist nicht
bewiesen. Die Zahlen sind keine beobachteten Fehler, keine unteren
Fehlergrenzen und keine realisierungsweisen Genauigkeitsgarantien. Eine
große obere Grenze rechtfertigt kein Verwerfen der Operatorfamilie.
Quelle, Operator, Archive und statistische Regeln bleiben unverändert;
es wurden keine neuen Zufallswolken gezogen.

- [Ergebnisbericht (PDF)](Unendlicher_Rest_Globale_Bilanz_v0_23.pdf)
- [Vollständiges Prüfpaket (ZIP)](CSPP_Unendlicher_Rest_Globale_Bilanz_v0_23_Pruefpaket.zip)
- [Vollständige Herleitung](cspp_v023/PROOF.md)
- [192-Bit-Ergebnisse](cspp_v023/results/GLOBAL_192.json)
- [Kontrollen](cspp_v023/results/CHECKS.json)
- [Nächster wissenschaftlicher Schritt](cspp_v023/NEXT_STEPS.json)
- [Veröffentlichungsmetadaten](PUBLICATION.json)

Die neue Konturabschätzung nutzt dieselben validierten Quellnormen und
liefert engere integrierbare Potenzhüllen nahe dem Lichtkegel. Eine
zusätzliche L²-Abschätzung verkleinert den fernen Teil. Alle unendlichen
Reste sind eingeschlossen. 223 bekannte aktive Endpunkte, 256 vollständige
Detektorzellen und zwei uniforme Fensterhüllen erhalten alle Pfadklassen.
Die endliche Außenhistory wird genau einmal addiert, ohne eine Annahme
unabhängiger Historyintervalle. Dominant bleibt die konservative nahe
Lichtkegelhülle im unendlichen Bereich.

## Reproduktion

```sh
python3 -m pip install numpy==2.3.5 python-flint==0.8.0
python3 -O -B research/cspp/infinite_exterior_v0_23/publication_check.py
python3 -B research/cspp/infinite_exterior_v0_23/publication_check.py --replay
```

Alle 41 ursprünglichen Paketdateien sowie PDF und ZIP werden bytegenau
veröffentlicht. Die Publikationsprüfung kontrolliert 40 Paketprüfsummen,
die Originalartefakte, Ergebnisinventare und Aussagegrenzen. Der Replay
rechnet bei 128 und 192 Bit in einer isolierten Kopie neu und verlangt
fünf byteidentische Ergebnisdateien. Die Kontrollen umfassen 14
Eingabedateien, 35 Quellnormpaare, 34 Gammaidentitäten, 49 unabhängige
Integralgegenrechnungen, 12 direkte Poissonkontrollen, 958 Endpunkt-Audits,
16 globale Zerlegungen und vier Negativkontrollen. Ein unabhängiges
wissenschaftliches Review wird nicht behauptet.
