# Referenzdetektion und Eigenfrontend: Prüfstand v0.1

**Prüfvorbereitung und Offline-Auswertung · 05.11.2026 · Hardware `NOT_RUN` · BOM-Freeze `HOLD`**

Die Referenzkette aus vier SPCM-AQRH-14-FC und Time Tagger Ultra erhält einen eigenen elektrischen Prüfvertrag. Der Kaskodenentwurf wird zunächst ausschließlich mit Niedervoltpulsen charakterisiert. Erst ein vollständiges, separat freigegebenes APD-/Quench-Modul darf in den optischen Detektorbenchmark gehen.

| Prüfpfad | Umfang | Aussagegrenze |
|---|---|---|
| Referenz R00–R14 | 15 Prüfungen: Identität, Versorgung, Pegel, Zählverluste, Timing, Drift, Archiv und Review | Keine reale Hardwarequalifikation ausgeführt |
| Eigenfrontend F00–F09 | 10 elektrische Prüfungen und Übergabebedingungen | APD/HV/Quench und ein qualifizierter Leitungstreiber bleiben offen |
| Benchmark B01–B07 | PDE/Systemeffizienz, Dunkelrate, Recovery, Afterpulsing, Jitter, Linearität, Koinzidenzen | Optische Messungen am vollständigen Modul erforderlich |

## Dateien und Laborstart

- [Bericht als PDF](X6_Detektionsqualifikation_v0_1.pdf) · [unverändertes vollständiges Prüfpaket](X6_Detektionsqualifikation_v0_1_Pruefpaket.zip)
- [Referenzvertrag](Referenzvertrag.json) · [leere Referenzmessung](Referenzmessung.template.json) · [Schnittstellenbudget](Schnittstellenbudget.json)
- [Eigenfrontend-Prüfmatrix](Eigenfrontend_Pruefmatrix.json) · [leere Benchmarkmessung](Benchmarkmessung.template.json)
- [Zeitmarken-Vorlage](Zeitmarken.template.json) · [Koinzidenz-Vorlage](Koinzidenzen.template.json)
- [Rechenergebnisse](Rechenergebnisse.json) · [Validierung](Validierung.json) · [Testprotokoll](Tests_Protokoll.txt) · [Primärquellen](Quellen.json)

Zuerst die gelieferten Geräte, Kabel, Lizenz und Versorgungen aufnehmen und R00–R03 an realer Hardware durchführen. Die Messfelder bleiben bis dahin leer. Die bisherigen Systemziele bleiben erhalten: elektrischer Paarjitter ≤200 ps, Restoffset ≤100 ps und keine nachgewiesenen Zählverluste. Neue technische Reserven und Entwicklungsziele sind ausdrücklich gekennzeichnet.

Der CML-Pfad des Eigenfrontends darf nicht direkt an den 50-Ohm-Ultra-Eingang angeschlossen werden. Auch `J404` ist kein nachgewiesener 50-Ohm-Leitungstreiber. Der spätere APD-/Quench-Pfad benötigt eine eigene Freigabe; elektrische Ersatzpulse belegen weder PDE noch optische Totzeit.

## Offline reproduzieren

Python ab 3.10; Auswertung und Tests verwenden ausschließlich die Standardbibliothek. Im Verzeichnis dieses Dokuments:

```sh
python -m unittest -v test_analysis
python verify_package.py
python publication_check.py
python analysis.py design
python analysis.py reference Referenzmessung.template.json --evidence-root .
```

Die 47 synthetischen Tests prüfen Statistik, große ganzzahlige Zeitstempel, feste Offsets, mehrdeutige Koinzidenzen, fehlende Daten, vertauschte Kanäle und veränderte Belegdateien. Ein leerer Datensatz ergibt `HOLD`; vollständige synthetische Daten ergeben höchstens `SYNTHETIC_ONLY`. Auch ein `NUMERICAL_SCREEN_PASS` realer Daten verlangt unabhängige Prüfung und lässt die BOM auf `HOLD`.

Die Auswertung extrahiert keine Oszillogramme, berechnet keine vollständige Messunsicherheit und steuert keine Geräte. Die Koinzidenzfunktion ist auf kleine Diagnosedatensätze begrenzt. Ein fertiger, unabhängig validierter `.ttbin`-Konverter und eine freigegebene Streaming-CHSH-Pipeline sind nicht Bestandteil dieses Pakets. Die bestehenden [Gerätetreiber](../../laborbetrieb-v0.1/README.md) bleiben unverändert.

## Herkunft und Status

Die 20 ursprünglichen ZIP-Mitglieder und das ZIP selbst sind bytegleich übernommen. `README.md` und `publication_check.py` sind zusätzliche Veröffentlichungshilfen. `SHA256.json` prüft die ursprünglichen 19 Nutzdateien; der Repository-Verlauf und die Quellinventare erfassen die Veröffentlichung. Ein Hash belegt Dateiintegrität, keine Messwahrheit.

Projektbasis: `11bd0f067775080d36e5f9c650788a868d72a3c9`. Verknüpfte Vorarbeiten: [Systemziele](../../optics/pump-input-v0.1/README.md), [RFQs/BOM](../../optics/rfq-bom-v0.1/README.md), [Polarisation/Filter/Spektrum](../../optics/polarisation-filter-spektral-v0.1/README.md) und [Kaskoden-Schaltplan](../cascode-schematic-v0.1/README.md).

Projektbeiträge gemäß [Lizenzumfang des Repositorys](../../../../LICENSE_SCOPE.md); Herstellerunterlagen sind verlinkt, nicht mitgeliefert. Keine reale Geräteabnahme, Bestellung oder automatische BOM-/CHSH-Freigabe.
