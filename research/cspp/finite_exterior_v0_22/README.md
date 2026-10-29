# CSPP v0.22: vollständige endliche Außenhistory

Die gesamte endliche äußere History für **-6 <= t <= -1** ist auf dem
vollständigen exakten KG-Feldträger eingeschlossen, einschließlich aller
räumlichen Flanken und der Wellenfront. Die vollständigen oberen bedingten
Erwartungswertschranken liegen bei etwa **0,477 bis 0,549** über vier
archivierte Konfigurationen und beide ursprünglichen Detektorfenster.
Der alte Patch ist genau einmal enthalten; seine Grenze wird nicht
nochmals addiert.

**METHOD_HOLD und G1 HOLD bleiben.** Der unendliche Wurzelbereich `t < -6`
ist noch nicht kombiniert. Die globale v0.19-Majorante bleibt unverändert,
das unveränderte Ziel 0,001 ist nicht bewiesen. Die Zahlen sind keine
gemessenen Fehler und keine realisierungsweisen Genauigkeitsgarantien.
Quelle, Operator, Wolken und statistische Regeln bleiben unverändert.
Die Rechengrenze schneidet die physikalische History nicht ab.

- [Ergebnisbericht (PDF)](Endliche_Aussenhistory_v0_22.pdf)
- [Vollständiges Prüfpaket (ZIP)](CSPP_Endliche_Aussenhistory_v0_22_Pruefpaket.zip)
- [Vollständige Herleitung und Grenzen](cspp_v022/PROOF.md)
- [192-Bit-Ergebnisse](cspp_v022/results/FINITE_192.json)
- [Prüfergebnisse](cspp_v022/results/CHECKS.json)
- [Nächste wissenschaftliche Schritte](cspp_v022/NEXT_STEPS.json)
- [Veröffentlichungsmetadaten](PUBLICATION.json)

Das exakte Vierervolumen ist `(110567/384) pi`; 688, 2664 und 10480 Zellen
überdecken dasselbe vollständige Gebiet. Der ganze Detektor wird mit exakt
normierten radialen und zeitlichen Teilmassen berücksichtigt. Die erste
Historykante benutzt die konservative punktweise kappa-Hülle. Die
schärferen archivbedingten Zählkerne aus v0.20/v0.21 werden auf diesem
größeren Gebiet noch nicht neu integriert. Die alte Patchgrenze und die
neue Grenze beziehen sich auf unterschiedliche Integrationsgebiete.

## Reproduktion

```sh
python3 -m pip install numpy==2.3.5 python-flint==0.8.0
python3 -O -B research/cspp/finite_exterior_v0_22/publication_check.py
python3 -B research/cspp/finite_exterior_v0_22/publication_check.py --replay
```

Die ursprünglichen 43 Paketdateien, PDF und ZIP werden bytegenau
veröffentlicht. Die Prüfung kontrolliert die 42 Paketprüfsummen,
Originalartefakte, wissenschaftlichen Grenzen und Ergebnisinventare.
Der vollständige Wiederholungslauf berechnet beide Präzisionen in einer
isolierten Kopie und verlangt neun byteidentische numerische Dateien.
Die Selbstkontrollen umfassen 30 feste KG-Punkte je Präzision,
50 unabhängige Moment- und sechs Massenquadraturen, 1332 rationale
Kappenproben, die exakte Gebietsabdeckung und gezielte Negativkontrollen.
Ein unabhängiges wissenschaftliches Review wird nicht behauptet.
