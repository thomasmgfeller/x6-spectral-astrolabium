# Physikalischer Rand- und Auslesevertrag v0.1

Veröffentlicht am 13. November 2026. Anschluss an [PR #292](https://github.com/thomasmgfeller/x6-spectral-astrolabium/pull/292), Ausgangscommit `06ca1444d582f2c3563e0be015b5ae7c3dbc9c49`.

Für beide N11-Geometrien ist ein gemeinsamer positiver, bedingter skalarer Drei-Moden-Vertrag konstruiert. Berechnete Normierungen und fortgesetzte Fresnelphasen liefern mit einem lokalen Gaußdetektor kohärente Auslesewahrscheinlichkeiten und einen vollständigen Fehlschlagseffekt. Die ursprüngliche Wirkung wählt die gemeinsame Projektion, Kontrollpräparation und physikalische Uhr-/Dichtepaarung nicht eindeutig. **Physikalische Geometriedynamik bleibt NOT_DERIVED.**

Die neue Quellenprüfung präzisiert den Vorgänger: Bei festen vergangenen Randuhren ist eine isolierte Änderung der Anfangsdichte für alle Record- und Fehlschlagwahrscheinlichkeiten wirkungslos. Der frühere diagonale Dichtekontrast ist in diesem Vertrag eine Zukunftsrandantwort. Integrierte Anfangs-Uhrpakete und andere physikalische Präparationen sind davon nicht ausgeschlossen.

## Artefakte

- [Bericht](reports/CST_DUST_Physikalischer_Rand_Auslesevertrag_v0_1.pdf)
- [Ursprüngliches Prüfpaket](packages/CST_DUST_Physikalischer_Rand_Auslesevertrag_v0_1_Pruefpaket.zip)
- [Unveränderte Quellen und wissenschaftliche Einordnung](physical_boundary_readout_v0_1/README.md)
- [Vertrag und offene Auswahlannahmen](physical_boundary_readout_v0_1/contracts/boundary_readout_contract.json)
- [Veröffentlichungsnachweis mit SHA-256-Hashes](physical_boundary_readout_publication.json)

Alle 40 Archiveinträge wurden bytegleich übernommen; die 39 Einträge des ursprünglichen Manifests bleiben unverändert. Der separat bereitgestellte PDF-Bericht und die im ZIP enthaltene PDF haben unterschiedliche Bytes, aber identischen mit Poppler extrahierten Text. Beide Originaldateien bleiben erhalten und werden separat gehasht; Bytegleichheit der PDFs wird nicht behauptet.

## Prüfung und Reproduktion

Zehn Prüfprogramme wurden in einer isolierten Kopie ausgeführt und zehn JSON-Ausgaben reproduziert. Exakte algebraische Felder werden identisch verglichen; numerische Felder mit absoluter und relativer Toleranz von jeweils `5e-12`. Laufzeiten sind ausgenommen, Abhängigkeitshashes werden gegen die tatsächlichen Quelldateien geprüft. Beide Elternquellen stimmen bytegleich mit dem veröffentlichten Ausgangscommit überein.

```bash
python -m pip install -r research/rax_cqg/dust_collapse/physical_boundary_readout_v0_1/requirements.txt
python -B research/rax_cqg/dust_collapse/verify_physical_boundary_readout_publication.py
```

Ein eigener GitHub-Actions-Lauf prüft Archiv, Manifest und dieselbe endliche Regression. Es wird kein externer Rechendienst und kein großer historischer Integrationslauf gestartet. Die Float64-Auswertungen sind nicht vollständig intervallzertifiziert. Die vorhandenen Fachagentenberichte dokumentieren interne KI-Prüfungen, keine externe Begutachtung.

English: A conditional positive common three-mode scalar contract and normalized local readout are constructed for the N11 pair. The original action does not uniquely select the added quotient, boundary pairing or preparation. The isolated past-density variation is exactly invisible with fixed past clocks. Physical geometric evolution and singularity resolution remain unestablished.
