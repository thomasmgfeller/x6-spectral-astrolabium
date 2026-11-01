# Eigenzeit v0.4 · Beprobungsdichte und Krümmung

K bezeichnet das Verhältnis der größten zur kleinsten Beprobungsdichte pro physischem Vierervolumen. Im vollständig beobachteten 4D-Kausaldiamanten darf jede Geometrie ein eigenes unbekanntes positives Dichteprofil haben. Die Ereignisse sind bei fester Anzahl unabhängige Ziehungen. Die positive Garantie setzt eine extern begründete Kontrastobergrenze voraus.

[Dichtekontrast und Ereignisbudget im Browser vergleichen](https://thomasmgfeller.github.io/x6-spectral-astrolabium/app/eigenzeit-dichtevergleich/index.html) · [Forschungsbericht (PDF)](Eigenzeit_Dichte_und_Kruemmung_v0_4.pdf) · [Mathematische Herleitung](BEWEIS.md) · [Vollständiges Prüfpaket mit Code und Daten (ZIP)](Eigenzeit_Dichte_und_Kruemmung_v0_4_Pruefpaket.zip)

| Erlaubter Dichtekontrast | Ergebnis für die untersuchte Modellfamilie |
|---|---|
| K ≤ 1,002 | Bei 3,2 Millionen Ereignissen und 11,2 Millionen Paarabfragen sichert die Achtergruppenregel mindestens 80,32 % richtige Raster-Einzelentscheidungen und mindestens 95,15 % Überdeckung des kontinuierlichen Krümmungsintervalls. |
| K = 1,01 als Obergrenze | Für das Dreifachziel sind mindestens 1.603.478 Ereignisse notwendig. Das frühere Budget von 900.000 reicht damit selbst bei Auswertung der vollständigen Ordnung nicht. |
| K ≥ 64/63 auf beiden Seiten | Ein flaches und ein schwach gekrümmtes Modell (RT² ≈ 0,758) können dasselbe Ordnungsgesetz bei jeder Ereigniszahl erzeugen. Der Faktor ist für das konstruierte gemeinsame Punktgesetz in der ausgerichteten Karte scharf. |

Die drei Rasterkrümmungen aus v0.3 sind RT² ≈ 0, 0,758 und 3,131. Für den kontinuierlichen Teil gilt h ∈ [0, 1/2]. Die 72 gekoppelten Beispielpaare hatten dieselben vollständigen gerichteten Ordnungen. Im gesonderten Stresstest bei K = 1,002 enthielten 31 von 32 Intervallen den wahren Wert. Die Leistungsgarantien stammen aus der analytischen Rechnung. [Rationales Zertifikat](certificate.json) · [Gekoppelte Ordnungen](twins.json) · [Pilotauswertung](pilot_audit.json) · [Vorstudie v0.3](../three_geometries_v0_3/README.md)

Die Folgestudie v0.5 prüft die Kontrastgrenze mit markierten Referenzversuchen und gibt bei fehlender Freigabe den gesamten Modellbereich aus. [Kalibrierung und Feldprotokoll](../calibration_v0_5/README.md)

## Reproduktion

Vom Wurzelverzeichnis des Repositorys aus:

```sh
python3 research/eigenzeit/density_contrast_v0_4/publication_check.py
python3 research/eigenzeit/density_contrast_v0_4/publication_check.py --replay --workers 2
```

Der erste Befehl prüft die drei veröffentlichten Originaldateien, alle 45 ZIP-Einträge, die Prüfsummen des vor dem Pilotlauf fixierten Standes und die separat verlinkten Forschungsdaten. Der zweite Befehl berechnet die Grenzen und Gegenkontrollen erneut, prüft die 72 Zwillingspaare, erzeugt alle 12,8 Millionen Gruppenzählungen und vergleicht die Entscheidungen sowie die interaktive Ansicht. Er verwendet Python 3.12, NumPy, SciPy und Node. [Abhängigkeiten](../../../tools/workflow/requirements-research.txt) · [Veröffentlichungsnachweis](PUBLICATION.json)

Die CI setzt mit `--cpu-baseline` für die Erzeugung der 32 Stressfälle den NumPy-Rechenpfad mit deaktiviertem AVX512F. Für diese Variante sind die Koordinatenprüfsummen separat hinterlegt. Alle Gruppenzahlen, übrigen Fallmetadaten, Entscheidungen und wissenschaftlichen Ergebnisse müssen der archivierten Fassung entsprechen. [Koordinatenprüfsummen](cpu_baseline.json)
