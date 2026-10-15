# Industrieller Datenvertrag: begrenzter Paderborn-Machbarkeitspilot

Dieser Pilot schließt einen **begrenzten, nichtkommerziellen Daten- und
Auswertungsweg**. Er entwickelt keinen neuen Filter. Die industrielle
Bestätigung nach [V1](../industrial-v1/README.md) bleibt ein eigener Vertrag.
Die vier Kanäle, 25.600 Hz, 10 s, Ressourcen- und Leistungsgates dieses
ursprünglichen Vertrags werden weder geändert noch durch Labordaten ersetzt.

## Ausgeführtes Ergebnis am 15. Oktober 2026

**PILOT_PIPELINE_PASS; industrielle Bestätigung NOT_READY.** Alle 20 festgelegten
Lager wurden übernommen und ausgewertet; die sechs Evaluationslager sind disjunkt
von Entwicklung und Validierung. Ergebnis und erneute Berechnung stimmen überein.

| Feste Referenz | Erkannte beschädigte Evaluationslager | Fehlalarme bei gesunden Evaluationslagern |
| --- | ---: | ---: |
| AC-RMS | 1 / 4 | 1 / 2 |
| Pearson-Kurtosis | 0 / 4 | 0 / 2 |
| Hüllkurven-Harmonischenverhältnis, primär | 4 / 4 | 1 / 2 |

Diese kleinen Zählungen sind rein beschreibend. Die Hüllkurvenreferenz zeigt einen
Fehlalarm; die Kurtosis zeigt zwar keinen Fehlalarm, erkennt aber auch keinen der
vier Schäden. Daraus folgt weder eine geeignete Betriebsschwelle noch ein
Leistungsvorteil eines neuen Filters. Die Methoden und Schwellen wurden nach
Kenntnis dieser Ergebnisse **nicht geändert**.

- [Vollständiger Bericht mit allen Scores und Entscheidungen](evidence/pilot-report.json)
- [Eingefrorene Validierungsschwellen](evidence/fit.json)
- [Ausführungsbeleg](evidence/execution.json), [elf Tests / 23 Negativkontrollen](evidence/pilot-tests.log)
- [Unveränderte V1-Vorprüfung: NOT_READY](evidence/v1-readiness.json)
- [Bedingte Fallzahl-/Powerrechnung](evidence/power-plan.json)

Vertrag, Messkanäle und Code wurden im öffentlichen Commit
[6f9cd5967cbd](https://github.com/thomasmgfeller/x6-spectral-astrolabium/commit/6f9cd5967cbd28c4322d011108d0b21637623f49)
um 13:18:42 UTC veröffentlicht; Fit und Auswertung folgten danach.
Die Vorstufen 0.1/0.2 waren technische Metadatenversuche, keine gescheiterten
Diagnosevergleiche. Der veröffentlichte Freeze umfasst die endgültige Fassung 0.3.

## Vorab festgelegter Umfang

[contract.json](contract.json) definiert die endgültige Pilotfassung 0.3.
[freeze.json](freeze.json) bindet Quellcode, Vertrag und Eingabemanifest vor
Berechnung der Diagnose-Scores. Das ist eine dokumentierte zeitliche Reihenfolge,
kein Nachweis eines geheimen oder extern beaufsichtigten Holdouts.

| Vertragsfeld | Festlegung / Grenze |
| --- | --- |
| Datenquelle | KAt Bearing DataCenter, Universität Paderborn; originale RAR-Dateien vom Hochschulserver |
| Maschine/Sensor | Modularer elektrischer Antriebsprüfstand; 6203-Lager; PCB 336C04, Kistler 5015A, dSPACE DS1006/DS2004 |
| Betriebsbedingung | Nur `N15_M07_F10`: nominal 1.500 rpm, 0,7 Nm, 1.000 N |
| Aufnahme | Nominal 64 kHz; ein Vibrationskanal; erste 256.000 Samples einer geeigneten Aufnahme, ungefähr 4 s |
| Datenrechte | **CC BY-NC 4.0**, Namensnennung und Quelle in [data/LICENSE.txt](data/LICENSE.txt); kommerzielle Nutzung nicht freigegeben |
| Labels | Sechs gesunde und alle 14 Lager mit Schäden aus Lebensdauerversuchen gemäß Quellentabellen 5/6; keine Labels aus unseren Scores |
| Statistikeinheit | Ein physisches Lager; genau eine Aufnahme je Lager; keine Fenstervermehrung |
| Entwicklung | 7 Lager: 2 gesund, 5 beschädigt |
| Validierung | 7 andere Lager: 2 gesund, 5 beschädigt; nur die beiden gesunden setzen die Schwellen |
| Evaluation | 6 andere Lager: 2 gesund, 4 beschädigt; keine nachträgliche Auswahl der Methode |
| Verfahren | AC-RMS, Pearson-Kurtosis und festgelegtes Hüllkurven-Harmonischenverhältnis; primäre Referenz ist die Hüllkurvenmethode |
| Erlaubte Aussage | Vollständige, wiederholbare Datenübernahme und klassische Auswertung auf genau diesen Laborlagern |
| Nicht abgedeckt | 1-%-Fehlalarmgarantie, Sensitivitätsgewinn eines neuen Filters, Industriepopulation, externe Replikation, Ressourcen-/Energiegewinn |

Die Aufteilung steht vollständig im Vertrag und ist auf Lager-IDs festgelegt.
Ein gemeinsamer Prüfstand und gezielt ausgewählte Schäden sind keine
Zufallsstichprobe einer Flotte. Verschiedene Lager-IDs verhindern Überlappung;
sie beweisen keine Unabhängigkeit von Maschinen-, Standort- oder Chargeneffekten.
Ein späterer Bestätigungsdatensatz darf diese bekannten Pilotdaten nicht als
unberührte externe Bestätigung wiederverwenden.

## Datenqualität und offen protokollierte Pilotrevisionen

Die erste Formatannahme war zu eng. Die Originaldateien haben teilweise einen
zusätzlichen Endpunkt; Host-Zeitstempel sind quantisiert. Außerdem besitzen
mehrere erste Wiederholungen abweichende Längen oder Zeitachsen. Die früheren
Entwürfe und beide fehlgeschlagenen Importversuche sind in [evidence/](evidence/)
aufbewahrt. Diese technischen Revisionen erfolgten **vor jeder Diagnoseauswertung**.

Fassung 0.3 prüft für jedes Lager Wiederholungen 1 bis 20 in fester Reihenfolge:
256.000 oder 256.001 endliche, verlustfrei übernommene Samples; monotone Zeitachse;
maximal eine halbe nominale Sampleperiode kumulative Abweichung vom 64-kHz-Raster;
unverändertes leeres Einheitenfeld. Die erste geeignete Aufnahme wird übernommen.
Fehlt eine geeignete Aufnahme, scheitert der gesamte Pilot. Kein Lager wird
entfernt. Jede geprüfte und verworfene Wiederholung steht mit Hash, Metadaten
und Prüfgründen im [Eingabemanifest](data/manifest.json).

Die tatsächlich ausgewählten Wiederholungen sind: K001–K006 jeweils 1;
KA04: 5, KA15: 4, KA16: 1, KA22: 1, KA30: 2, KB23: 1, KB24: 1, KB27: 1,
KI04: 1, KI14: 2, KI16: 1, KI17: 6, KI18: 1, KI21: 3.
**16 verworfene Aufnahmen bleiben im Auswahlprotokoll.** Diese Auswahl nach
Datenqualität kann die untersuchte Teilmenge beeinflussen; der Pilot macht
keine Aussage über die verworfenen Aufnahmen oder alle Betriebszustände.

Das native Einheitenfeld ist leer und individuelle Kalibrierzertifikate liegen
nicht vor. Deshalb bleibt die Amplitude in gespeicherten nativen Zahlenwerten.
Es wird keine Umrechnung in m/s² erfunden und keine absolute Messgenauigkeit
behauptet. Die Zeitachsenprüfung bescheinigt ebenfalls keine Uhrkalibrierung.

## Feste Referenzverfahren

Alle Parameter stehen vor den Scores im Vertrag. RMS und Pearson-Kurtosis
verwenden das feste Fenster Samples `[6400,249600)`. Die Hüllkurvenreferenz
verwendet Butterworth-Bandpass 4. Ordnung, 2–10 kHz, vorwärts/rückwärts gefiltert,
Hilbert-Betrag und nach Randbeschnitt ein Hann-Fenster. Ihr Score ist das Maximum
der relativen spektralen Energie um die ersten drei Harmonischen von 76,25 bzw.
123,3 Hz, jeweils ±2 Hz, normiert auf die Gesamtenergie von 20–500 Hz.
Diese konkrete Parametrisierung ist eine Pilotfestlegung, kein behauptetes Optimum.

Pro Verfahren wird die Schwelle auf den nächsten darstellbaren Float oberhalb
des höchsten Scores der beiden gesunden Validierungslager gesetzt.
`score >= threshold` bedeutet Alarm. Beschädigte Validierungslager und
Evaluationslager verändern diese Regel nicht. Alle drei Verfahren werden
berichtet; es wird kein Gewinner nachträglich zur Hauptreferenz erklärt.
Die Auswertung ist **offline und nicht kausal**; sie erfüllt damit ausdrücklich
keinen Streaming-/Latenznachweis des V1-Vertrags.

## Reproduzieren

Aus einem frischen Checkout, Python 3.12:

```sh
python3 -m venv .venv-industrial
. .venv-industrial/bin/activate
python3 -m pip install -r experiments/industrial-v1/requirements.txt
python3 experiments/industrial-pilot/pilot.py verify
python3 experiments/industrial-pilot/test_pilot.py
```

Nach einmaliger Installation benötigt die Prüfung kein Netzwerk. Die ausgewählten,
unveränderten Messkanäle sind mit Quelle, Lizenz und Hashes im Checkout enthalten
(insgesamt ungefähr 9,8 MB komprimiert). Original-RAR-Archive werden nicht dupliziert.
Die Daten sind reale fremde Labormessungen, keine eigenen Hardwaremessungen und
keine synthetischen Kontrollsignale.

Ein neuer Lauf schreibt ausschließlich in neue Ausgabedateien:

```sh
python3 experiments/industrial-pilot/pilot.py fit --output /tmp/pu-fit-new.json
python3 experiments/industrial-pilot/pilot.py run --fit /tmp/pu-fit-new.json --output /tmp/pu-run-new.json
python3 experiments/industrial-pilot/pilot.py verify --fit /tmp/pu-fit-new.json --report /tmp/pu-run-new.json
python3 experiments/industrial-pilot/power.py --output /tmp/v1-power-new.json
```

Ein Ergebnis-PASS bedeutet ausschließlich den begrenzten Pilotweg;
`industrial_claim_supported` bleibt immer `false`. Der Prüfer berechnet
Schwellen, Scores, Entscheidungen und vollständige Evaluationszählungen erneut.
Fehlende oder doppelte Lager, vertauschte Labels/Splits, Datenkorruption,
geänderte Schwellen und manipulierte/unvollständige Ergebnisse scheitern.
Numerischer Replay erlaubt nur `rtol=1e-10, atol=1e-12`; Status, Gruppen,
Entscheidungen und Zählungen müssen exakt stimmen. Hashes sind Inhaltsbindungen,
keine digitale Signatur oder unabhängige Echtheitsbescheinigung.

Für einen zusätzlichen Abgleich mit den Originalarchiven (etwa 3,4 GB Download):

```sh
python3 -m pip install -r experiments/industrial-pilot/requirements-import.txt
# prepare.py benötigt zusätzlich die systemweite libarchive-Bibliothek.
python3 experiments/industrial-pilot/download_sources.py --output /tmp/pu-originals-new
python3 experiments/industrial-pilot/prepare.py --archives /tmp/pu-originals-new --output /tmp/pu-extracted-new
```

Archive und ausgewählte MAT-Dateien sind im Manifest mit Hashes fixiert. Bei
veränderten Originaldateien scheitert der Download. Der Reimport muss dieselben
NPZ- und Signalhashes und dieselbe Auswahl ergeben; nur Erstellzeit des neuen
Manifests darf abweichen. Keinen neu erzeugten Import ungeprüft als eingefrorene
Originaleingabe ausgeben.

## Bestätigung bleibt ein eigenes Gate

[power.py](power.py) berechnet den 368-Fall und zusätzliche Fallzahl-/Powerbeispiele
mit den **unveränderten** V1-Gates. Die Annahmen sind explizite Planungsalternativen,
keine aus den wenigen Pilotlagern geschätzten Effekte. Positive gepaarte Fälle
werden über eine bedingte Multinomialsumme behandelt, nicht als unabhängige
Kandidat-/Baseline-Treffer. Für die beiden Ansprüche gilt weiterhin α=0,05/2.

Die genaue Rechnung liefert `n_min=368`: bei 367 liegt die obere Grenze noch
über 1 %, bei 368 darunter. Wenn die wahre Fehlalarmrate beispielsweise 0,2 %
beträgt, beträgt die Wahrscheinlichkeit für null Fehlalarme bei 368 Einheiten
nur etwa **47,9 %**. Die Untergrenze 368 ist daher kein 80-%-Powerplan.

Ein ausdrücklich **bedingtes Rechenbeispiel** mit Kandidat-Sensitivität 90 %,
Baseline-Sensitivität 75 %, gepaarten Wahrscheinlichkeiten W=20 %, L=5 % und
wahrer Fehlalarmrate 0,2 % verwendet **800 beschädigte und 1.164 gesunde
unabhängige Einheiten pro Anspruch**. Unter genau diesen Annahmen liegt die
konservative Untergrenze für das gemeinsame Bestehen der Qualitätsgates beider
Ansprüche bei rund 93,4 %. Die 800 sind der erste passende Wert eines vorgegebenen
Gitters, kein nachgewiesenes Minimum. Ressourcen-/Erhaltungsgates sind dabei als
bestanden vorausgesetzt; Clustereffekte sind nicht abgedeckt. Dieses Beispiel
ist keine bereits fachlich freigegebene Beschaffungs- oder Studienfallzahl.

Vor bestätigender Filterentwicklung/-bewertung fehlen ein benannter Industriepartner
bzw. eine Zielpopulation, verwendbare kommerzielle Rechte, unabhängig erhobene
Referenzlabels, passende Aufnahme-/Kalibrierprotokolle und ausreichende unabhängige
Lager mit dokumentierter Maschinen-/Standortstruktur. Kandidat, starke Baseline,
Schwellen, Powerannahmen, Fallzahlen und Abbruchregeln müssen fachlich geprüft und
vor dem Zugriff auf Bestätigungsdaten eingefroren werden. Bei Clustern ist ein
neuer vorab festgelegter Auswertungsvertrag nötig. Der Pilot ersetzt keine dieser
Freigaben und erzeugt keine V1-PASS-Bescheinigung.

## Quellen

- Christian Lessmeier, James Kuria Kimotho, Detmar Zimmer, Walter Sextro (2016):
  [Originalpublikation und Labeltabellen](https://mb.uni-paderborn.de/fileadmin-mb/kat/PDF/Veroeffentlichungen/20160703_PHME16_CM_bearing.pdf).
- [KAt-Datenquelle und Lizenz](https://mb.uni-paderborn.de/en/kat/research/bearing-datacenter),
  [Messgeräte](https://mb.uni-paderborn.de/en/kat/research/bearing-datacenter/test-rig-and-measurement-equipment),
  [Betriebsbedingungen](https://mb.uni-paderborn.de/en/kat/research/bearing-datacenter/operating-conditions).
- [NIST: exakte Binomialgrenzen](https://www.itl.nist.gov/div898/software/dataplot/refman2/auxillar/exacbici.htm).
- Geprüfte Alternative: Ottawa UORED-VAFCLS, DOI 10.17632/y2px5tg92h.5, CC BY 4.0.
  Deren Rohdatenabruf lieferte hier HTTP 403; sie wurden nicht ausgewertet.
  Lastunterschiede und die quellseitige spektrale Auswahl wären gesondert zu behandeln.

Eigener Code und eigene Dokumentation: Apache-2.0. Die gesondert gekennzeichneten
Paderborner Messdaten behalten **CC BY-NC 4.0**. Es wird keine Zustimmung oder
Mitwirkung der Datenautoren an diesem Pilotprojekt behauptet.
