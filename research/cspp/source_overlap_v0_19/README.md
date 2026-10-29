# CSPP v0.19: Quellnormen und geometrisch begrenzter Rest

Die tatsächlichen Ableitungsnormen der unveränderten kompakten KG-Quelle,
eine geometrische Beschränkung der Archivüberlappung und die integrierten
Feld- und Kernhüllen verschärfen die vollständige bedingte L1-Restmajorante.
Die globale Feldobergrenze sinkt auf **weniger als 6,429644**; die oberen
Schranken für den vollständig transportierten Rest liegen nun ungefähr bei
**2,36 bis 3,39 mal 10^14**, gegenüber etwa 10^54 in v0.18.

Das ist eine Verbesserung einer oberen Erwartungswertschranke um rund
40 Größenordnungen, kein gemessener Fehler und keine Fehleruntergrenze.
**METHOD_HOLD und G1 HOLD bleiben bestehen. Individuelle Genauigkeit:
NOT_CERTIFIED.** Das Fehlerziel 0,001 ist weiterhin nicht bestätigt.
Keine neuen Wolken, Seeds, physikalischen Parameter oder statistischen Regeln.

- [Bericht mit vollständiger Herleitung (PDF)](Quellnormen_Intervallgeometrie_v0_19.pdf)
- [Unverändertes vollständiges Prüfpaket (ZIP)](CSPP_Quellnormen_Intervallgeometrie_v0_19.zip)
- [Lesbare Herleitung und Aussagegrenzen](cspp_v019/PROOF.md)
- [Deklarierte Abschätzungsfamilien](cspp_v019/PROTOCOL.json)
- [Ergebnisse bei 512 Bit](cspp_v019/results/BOUNDS_512.json)
- [Kontrollen und Gegenrechnungen](cspp_v019/results/CHECKS.json)
- [Vergleich der Restmajoranten](cspp_v019/results/majorant_comparison.png)

## Reproduktion

```sh
python3 -m pip install python-flint==0.8.0
python3 -B research/cspp/source_overlap_v0_19/publication_check.py --replay
```

Python 3.12. Der Publikationsprüfer kontrolliert PDF, ZIP, alle 25 ursprünglichen
Paketdateien und 24 Paket-Hashes. Die isolierte Neuberechnung bei 384/512 Bit
muss alle drei wissenschaftlichen JSON-Dateien exakt reproduzieren.
960 Präzisionsvergleiche, 35 Quellnormidentitäten, eine validierte direkte
Quadratur, 49 bedingte Kernkontrollen und drei Negativkontrollen bestehen.
Der [GitHub-Workflow](../../../.github/workflows/cspp-source-overlap.yml) prüft
den eingereichten Commit und main. Der archivierte Wolfram-Gegencheck wird
im lokalen Replay nicht erneut als externer Dienst aufgerufen.

Die ursprüngliche Aussage `NOT_PUBLISHED` im Paket beschreibt dessen Stand
vor der Veröffentlichung. Originaldateien, PDF und ZIP bleiben bytegleich;
die Publikationsmetadaten liegen separat in `PUBLICATION.json`.

**Offen:** Die tatsächlichen lokalen Überlappungsvolumina und Punktzahlen
aller beitragenden Archivintervalle sowie die lokalen KG-Feldwerte im
endlichen äußeren Historybereich sind noch nicht gemeinsam ausgewertet.
Die neue geometrische Hülle ersetzt diese Auswertung nicht. Der exakte
bedingte Gewichtskern ist dafür als geprüfter Baustein enthalten.
Algebraische und numerische Kontrollen ersetzen keine unabhängige
wissenschaftliche Begutachtung der Kontur-, Geometrie- und Mecke-Beweise.

Basis: [v0.18 / PR #150](https://github.com/thomasmgfeller/x6-spectral-astrolabium/pull/150),
Merge `995b2184cb5346aee502d8e69089681181c5853e`.
