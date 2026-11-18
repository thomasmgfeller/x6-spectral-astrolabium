# CST-DUST · Prüfberichte zu den Etappen 4 bis 7

**18. November 2026.** Die vier internen Prüfberichte untersuchen, welche Aussagen die veröffentlichten CST-DUST-Rechnungen über einen kollabierenden Staubball tragen. Gemeinsamer Ausgangspunkt ist der [Stand nach PR #301](https://github.com/thomasmgfeller/x6-spectral-astrolabium/commit/95e2e4d1e6caf8f3fbabf701aa551ace47c32be4). Jede PDF enthält den Prüfvertrag, den Befund, dessen Geltungsbereich und Verweise auf die zugehörigen Rechnungen.

| Etappe und Bericht | Geprüfter Befund | Physikalischer Status |
| --- | --- | --- |
| [4 · Physikalischer Zustandsraum](../reports/CST_DUST_Etappe_4_Artefaktpruefung.pdf) | Der Differenzblock für 33 AA-Historien hat bei Gleichgewichtung Rang zwei. In einer anderen Familie sind die bedingten Skalarausgänge der N14-Endtypen 1790 und 5374 linear unabhängig. | **HOLD.** Für den gemeinsamen Geometrie-Staub-Skalar-Sektor fehlen die hergeleitete physikalische Paarung und der Kopplungsnachweis nach Projektion. |
| [5 · Gemeinsame Geometrie-Materie-Rückwirkung](../reports/CST_DUST_Etappe_5_Artefaktpruefung.pdf) | Bei affinen festen N11-Randuhren erzeugt die Anfangsdichte eine gemeinsame Phase. Beim kohärenten Uhrpaket ändert sich der Betrag des Zweigverhältnisses von 1,59847116 auf 1,59591233. | **5A–5C HOLD.** Die Paketdaten betreffen ein Skalarinstrument. Der feste geometrische Effekt und die vollständige Entkopplungskontrolle für die Staubpräparation sind offen. |
| [6 · Relationale Dynamik entlang der Staubuhr](../reports/CST_DUST_Etappe_6_Artefaktpruefung.pdf) | In der diagonalen Referenz mit höchstens zwei Ereignissen stimmen für jedes der zwei Zahlgewichte alle 26 Unterteilungen über zehn Endpunktpaare bei festem Enduhrwert überein. Die Gewichte ergeben verschiedene Wahrscheinlichkeiten für ausbleibende Geburt. | **6A–6C HOLD.** Kohärenter Transport, physikalische Norm und kontrollierter Grenzwert des gekoppelten Systems bleiben offen. |
| [7 · Klassische Korrespondenz vor der Singularität](../reports/CST_DUST_Etappe_7_Artefaktpruefung.pdf) | Alle 240 archivierten klassischen Einschliessungen enthalten die analytische Einstein-Staub-Referenz. Auf dem feinsten numerischen Gitter beträgt die grösste relative Fehlerhülle 0,130628 % bei einem Budget von 0,5 %. | **HOLD_NOT_ELIGIBLE / NOT_RUN.** Die 524 geplanten physikalischen P3-Vergleiche stehen aus. Eine fünfte Ereignisdichte und die Konzentrationsprüfung sind Erweiterungsvorschläge. |

## Nachrechnung

Aus dem Stammverzeichnis des Repositorys mit Python 3 und dessen Standardbibliothek ausführen.

```sh
python3 research/rax_cqg/dust_collapse/stage_reviews_4_7/verify.py
```

Das Skript liest die archivierte Rangangabe und prüft den rationalen N14-Überlapp, den N11-Phasenkoeffizienten und die beiden Paketverhältnisse. Für Etappe 6 vergleicht es alle Einträge der Transportmatrizen auf fünf Uhrwerten exakt. In der Gegenprobe mit einem eigenen Endwert je Teilstück weichen alle sieben unterteilten Wege der Gesamtstrecke vom Direktweg ab. Für Etappe 7 prüft es jede Kombination aus drei Massen, fünf Uhrwerten, vier Observablen und vier numerischen Gittern. Ein glatter Gegenversuch zeigt zudem, wie bei identischen Volumen- und Steigungswerten auf allen fünf Stützstellen die Anfangsbeschleunigung um 75,8 % abweichen kann.

### Eingangsdaten und Herleitungen

- Etappe 4 · [AA-Differenzblock](../basis_invariant_coupling_v0_1/results/uniform.json), [bedingtes N14-Gramprodukt](../history_measure_state_space_v0_1/sector.json) und [Pfadgedächtnis bei N14](../history_measure_state_space_v0_2/README.md).
- Etappe 5 · [Wirkung und Uhridentität](../physical_boundary_readout_v0_1/checks/ward_clock/check.py) und [archivierter Lauf der Präparationspakete](../initial_preparation_v0_1/clock_packet_results.json).
- Etappe 6 · [Intervalltransport, Zahlgewichte und Endrand](../clock_intervals_v0_1/DERIVATION.md).
- Etappe 7 · [P3-Prüfvertrag](../correspondence_v0_1/README.md) und [240 klassische Referenzintervalle](../correspondence_v0_1/results/reference_comparisons.csv).
