# CSPP v0.16: Äussere Forcierung des kompakten Detektors

Die vollständige diskrete Erweiterung von Omega4 auf Omega5 und die getrennte
Kontrolle mit vorgeschriebenen äusseren KG-Werten verfehlen das unveränderte
Fehlerziel **0,001 in allen acht Fällen**. Selbst die kleinste zertifizierte
Fehleruntergrenze der vollständigen Erweiterung liegt über **0,006697**.

Der zusätzliche Aussenbeitrag wird direkt und über seinen Transport durch die
innere Dynamik eingeschlossen. Die aktive äussere KG-Referenz ist im relevanten
Zeitraum exakt null. Die diskrete Erweiterung erzeugt dennoch 16 nachweislich
von null verschiedene aktive Aussenwerte; deren zusätzlicher Detektorbeitrag
bleibt überall unter 0,000010.

**Grenzen:** Diese Ergebnisse gelten für vier vorhandene Archivpaare und zwei
vollständige Detektorfenster. In sechs von acht Fällen ist die Einschliessung
der Schalenänderung breiter als die Komponentenradius-Marke 0,001; der
konservative Genauigkeitsausschluss bleibt trotzdem eindeutig. Der Rest
jenseits Omega5 ist **NOT_CERTIFIED**. **METHOD_HOLD und G1 HOLD bleiben bestehen.**
Kein neues Ensemble und kein Ausschluss der ganzen Operatorfamilie.

## Bericht, Prüfpaket und Herleitung

- [Bericht als PDF](output/Aeussere_Forcierung_v0_16.pdf)
- [Vollständiges Prüfpaket als ZIP](Aeussere_Forcierung_v0_16_Pruefpaket.zip)
- [Mathematische Herleitung und konditionales Restlemma](exterior_attribution_v0_16/METHODS.md)
- [Prüfergebnisse und acht Fehlergrenzen](exterior_attribution_v0_16/results/CHECKS.json)
- [Entwicklungsprotokoll](exterior_attribution_v0_16/PROTOCOL.json)
- [Erhaltene erste Auswertung und algebraische Nachbesserung](exterior_attribution_v0_16/AMENDMENT_01.json)

2.003 Intervallvergleiche zwischen 128 und 192 Bit, 64 unabhängige rationale
Kausalzählungen, sechs algebraische Kontrollen und 126 öffentliche
Quelldatei-Identitäten sind bestanden. Die einmalige zertifizierte
192-Bit-Raumquadratur wird von beiden Präzisionsläufen gemeinsam verwendet.

## Vollständige Reproduktion

Aus dem Repositorywurzelverzeichnis, mit Python 3.12 und C++17-Compiler:

```bash
python3 -m pip install -r research/cspp/exterior_attribution_v0_16/exterior_attribution_v0_16/requirements.txt
python3 -B research/cspp/exterior_attribution_v0_16/publication_check.py --replay
```

Der Prüfer kontrolliert PDF, ZIP und alle 167 Originaldateien, entpackt in ein
temporäres Verzeichnis, berechnet alle Detektorkoeffizienten neu, wiederholt
History und Transport bei 128 und 192 Bit und vergleicht die Einschliessungen
mit den archivierten Resultaten. Die veröffentlichten Dateien bleiben unverändert.

Basis: [PR #147](https://github.com/thomasmgfeller/x6-spectral-astrolabium/pull/147),
Commit `61ff6bfae105b14d3dfd69359f11b8f0516872ec`. Dieser Folge-PR führt die
offenen Vorgänger nicht automatisch in `main` zusammen.
