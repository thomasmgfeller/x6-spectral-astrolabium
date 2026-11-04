# X6-QED C0.1 · Anschluss an den photonischen Zwei-Qubit-Versuchsaufbau

**Status des Nachtrags** Entwurf zur Algorithmusspezifikation v0.2 vom 3. November 2026. Vorschlag vom 4. November 2026 für C0.1. Implementierungsziel C0.2. CAL und C0-VALIDATION stehen auf HOLD. Der Nachtrag setzt die vollständige Spezifikation einschließlich ihrer Originalformeln voraus.

**Geprüfte GitHub-Basis** `thomasmgfeller/x6-spectral-astrolabium` auf `main`, Commit `8f55867de35233b760594fdf6468b729f5706833`. Der [photonische Zwei-Qubit-Versuchsaufbau](../../../experiments/photonic-two-qubit/README.md) verlinkt diesen Nachtrag unter „Einstieg und Unterlagen“.

## 1. Daten und Zuständigkeiten

| Datenpfad | Eingang und vorhandene Auswertung | Aussage und Verwendung in C0 |
|---|---|---|
| Sagnac v0.7 | SGNCv007-Snapshots mit Zählern je Einstellung. Der bestehende Import prüft unter anderem CRC32, Sequenz und Zählerkonsistenz. Das Ergebnis hat das Schema `x6.sagnac.evidence/1`. | Referenz für Rohdatenbindung, Integritätsprüfung und deterministische Wiederholung. Aus aggregierten Zählern lässt sich die Folge einzelner Klicks oder Surface-Code-Syndrome nicht rekonstruieren. |
| Optikplan v0.1 | Vorgesehene Vierkanal-Zeitmarken für A+, A−, B+, B−. `OPTIK-CHSH-0.1` legt ein Koinzidenzfenster von insgesamt 2 ns und eine eindeutige bipartite Paarregel fest. Der vorhandene Statistikprüfer beginnt bei vier Zähltabellen. | Eigenständige Prüfung der Polarisationskorrelation. Rohdatenadapter und Paarbildung sind als offen dokumentiert. Hardware und realer CHSH-Lauf stehen auf NOT_RUN. |
| X6-QED C0.1 | Stim-Detektorbits pro Shot in der Reihenfolge des definierten Schaltkreises, mit validiertem FrozenGraph. Die tatsächlichen logischen Flips stehen nur der Auswertung zur Verfügung. | Vorhersage eines festgelegten logischen Observablenbits oder HOLD. Als erster Entwicklungsfall gelten Rotated Surface Code, Distanz 5, fünf Runden, Radius 2, Clustergröße höchstens 8 und Pfadtiefe höchstens 4. |

## 2. Gemeinsamer Nachweis

Ein Auswertungsindex darf auf Nachweise beider Systeme verweisen. Jeder Eintrag nennt den Datentyp mit Version, die deklarierte Herkunft, die Software-Revision, die zugehörige Konfiguration und den SHA-256 der Originaleingabe. Der Photonik-Eintrag referenziert seinen bestehenden Export. Der C0-Eintrag bindet zusätzlich Schaltkreis, Rauschmodell, DEM, Adapterkonfiguration und FrozenGraph an den Lauf. Beide Ergebnisse behalten ihre Einheit, ihren Nenner und ihren eigenen Status.

Der C0-Eingang akzeptiert ausschließlich einen zum FrozenGraph passenden Detektorvektor. Der Aufrufer prüft Datentyp, Modellidentität, Länge und binäre Werte vor der Inferenz. Ein SGNCv007-Frame, ein Sagnac-Evidence-Export, eine Zeitmarkendatei oder eine CHSH-Zähltabelle am C0-Eingang führt zu einem Eingabefehler außerhalb der Shot-Statistik. Ein gültiges C0-HOLD zählt dagegen als Decoderentscheidung. Der Photonik-Status `physical_quantum_claim` und die vorab festgelegte CHSH-Paarselektion werden unabhängig von C0 geführt.

## 3. Änderungen am Decoderentwurf

1. **Quellereignisse erhalten.** Pro ausgeführter Stim-Fehlerinstruktion eine stabile Identität führen. Separator-Komponenten teilen diese Identität. Detektor- und Observablen-XOR der ausgegebenen Komponenten gegen das Quellereignis prüfen. Bei identischen Endpunkten verschiedene Masken unterscheidbar halten. Unrepräsentierte wirksame Beiträge zählen und vor einer CAL-Freigabe entscheiden.
2. **Kosten festlegen.** Das volle Quell-`p` je Teilkante ist ein Parameter der C0-Näherung. Für überlappende Kandidatenpfade muss die Hauptspezifikation festlegen, ob sie eine Pfadsumme oder die Kosten der XOR-Kantenmenge bewertet. Radius, Nachbarschaft, Kandidatenbudget und Shot-Fusion müssen auch für leeres Syndrom, Budgetabbruch und mehrere Cluster eindeutig sein.
3. **§17 im Entwicklungsmodell ausgezählt.** Unter der syntaktischen Zuordnung erreichen bei 55 von 1.679 verschiedenen nichtleeren Einzelfehler-Syndromen alle Cluster beide Observablenklassen. Werden die Observablenbits je Quelle auf deren erste Komponente gelegt, sind es 979. Die Quellereignisse haben in beiden Fällen dieselbe Gesamtwirkung. Jedes Syndrom zählt einmal. Die PASS-Quote auf zufälligen Shots ist weiterhin offen. [Auswertung und Suchregeln](../../../research/x6_qed/section17_d5_v0_1/README.md) · [Alle Syndrome als CSV](../../../research/x6_qed/section17_d5_v0_1/results/development_syndromes.csv) · [Vollständiges Prüfpaket](../../../research/x6_qed/section17_d5_v0_1/X6_QED_Paragraf17_d5_Pruefpaket.zip).
4. **Leistungsprüfung separat planen.** Schaltkreisvariante, Rauschraten, PyMatching-Version und Vergleichsmodus zuerst festlegen. Auf denselben simulierten Shots Abdeckung, Abdeckung unter nichtleeren Syndromen sowie Fehlerrisiko unter PASS bestimmen. Bei null PASS ist das bedingte Fehlerrisiko undefiniert. Der Vergleich verwendet die simulierten wahren Observablenflips. CAL-A/CAL-B, F1–F3 einschließlich F2, Shotzahl oder Stoppregel, U18-Grenze und Sealing benötigen vor dem Validierungslauf ihre vollständigen Festlegungen.

## 4. Prüffälle für den ersten Softwarebeitrag

| Fall | Erwartung | Stand am 4. November 2026 |
|---|---|---|
| Vorhandenen SGNCv007-Datensatz mit dem vorhandenen Referenzkern auswerten | Vier synthetische Snapshots, Sequenzen 100 bis 103, Einstellungen 0 bis 3. Physikalischer Status NOT_ASSESSED. | Reproduziert. Neun bestehende Kerntests bestanden, darunter der Vergleich mit der Python-Referenz und die Zurückweisung aller 1.952 einzelnen Bitfehler eines 244-Byte-Frames. |
| Dieselbe Binärdatei oder ihren JSON-Export an den geplanten C0-Eingang geben | Abweisung vor der Inferenz. Kein QED-Shot und kein Eintrag im HOLD-Nenner. | Bestanden. Binärdaten und Sagnac-JSON wurden vor dem Aufruf der Inferenz abgewiesen. |
| Synthetischen d=5-Shot mit passender und mit absichtlich falscher Modellidentität einspeisen | Nur der passende Fall erreicht die Inferenz. Der logische Sollwert ist für die Inferenz unzugänglich. | Bestanden. Die Testfunktion erhielt ausschließlich den unveränderten Detektorvektor. Eine fremde Graphkennung wurde vor ihrem Aufruf abgewiesen. |

Der vorhandene Test lässt sich vom Repository-Stamm mit `node tests/sagnac/test_core.cjs` wiederholen. Die benutzte Datei `device/fixtures/synthetic_chsh_capture.bin` hat SHA-256 `cc74c62abdbe1fd38c0960ca98462308a81f94d4d6733c2ba64219c3a5ec900b`.

### Implementierte C0.2-Eingangsprüfung

[`decode_shot`](../../../research/x6_qed/c0_input.py) erhält die SHA-256-Kennung und die Detektoranzahl vom Aufrufer, der die Inferenz an einen bereits validierten FrozenGraph bindet. Das JSON-Objekt enthält genau die Felder `schema` mit Wert `x6.qed.detector-shot/1`, `frozen_graph_sha256` und `detector_bits`. Die Liste enthält für jede Detektor-ID eine Ganzzahl 0 oder 1 in der Reihenfolge des Graphen. Zusätzliche Felder, insbesondere logische Sollwerte, führen zu `ShotInputError`. Die Konfiguration des Aufrufers muss aus vertrauenswürdiger Quelle stammen. Die Schnittstelle implementiert die Eingangsprüfung. Die separate §17-Auswertung ist in Abschnitt 3 dokumentiert. Die gewichtete Inferenz und die vollständige FrozenGraph-Validierung stehen noch aus.

Der [gespeicherte Testfall](../../../tests/sagnac/fixtures/qed_d5_single_fault.json) stammt aus Stim 1.16.0, `surface_code:rotated_memory_x`, Distanz 5, fünf Runden. Ein einzelner möglicher Z-Fehler auf Datenqubit 1 vor der finalen X-Auslese liefert den DEM-Term `error(0.125) D108 L0`. Der ausgewählte synthetische Shot hat genau Bit 108 von 120 gesetzt. Der mitgeführte wahre Observable-Flip ist getrennt unter `evaluation_only` gespeichert. Dieser Graph mit einem Fehlermechanismus dient ausschließlich der Schnittstellenprüfung. Sein Fingerabdruck umfasst die UTF-8-JSON-Darstellung des Objekts `graph` mit sortierten Schlüsseln und ohne Zwischenräume.

Vom Repository-Stamm aus prüft der folgende Befehl den gespeicherten Fall ohne Stim-Installation. Python und Node.js werden benötigt.

```sh
python3 -m unittest discover -s tests/sagnac -p 'test_qed_input.py' -v
```

Mit Stim 1.16.0 lässt sich der Testfall unabhängig neu erzeugen und mit der eingecheckten Fassung vergleichen.

```sh
python3 tests/sagnac/fixtures/rebuild_qed_d5.py
git diff --exit-code -- tests/sagnac/fixtures/qed_d5_single_fault.json
```

## 5. Späterer photonischer Vergleich

Für den geplanten Singulettzustand eignet sich als eigenständige Hardwarefrage, wie häufig bei gleicher Analysatorbasis auf beiden Armen die erwartete Antikorrelation verletzt wird. Dafür werden etwa H/V und D/A in getrennten Serien an frisch präparierten Paaren gemessen. Vorab sind Basiszuordnung, Behandlung von Verlust und Mehrfachklicks, Nenner und Kontrollen festzulegen. Ein solcher Versuch liefert eine beobachtete Paritätsfehlerrate unter seinen Messbedingungen. Eine physische C0-Prüfung erfordert zusätzlich einen kodierten Versuch, bekannte Stabilisatorprüfungen über mehrere Runden und eine auswertbare logische Observable.

## Referenzen

- [Photonischer Zwei-Qubit-Versuchsaufbau](https://github.com/thomasmgfeller/x6-spectral-astrolabium/blob/8f55867de35233b760594fdf6468b729f5706833/experiments/photonic-two-qubit/README.md)
- [Sagnac-Import und Replay](https://github.com/thomasmgfeller/x6-spectral-astrolabium/blob/8f55867de35233b760594fdf6468b729f5706833/docs/SAGNAC_INTEGRATION.md)
- [Optikplan und Implementierungsstand](https://github.com/thomasmgfeller/x6-spectral-astrolabium/blob/8f55867de35233b760594fdf6468b729f5706833/experiments/photonic-two-qubit/optics/optikplan-v0.1/README.md)
- [Synthetischer Referenztest](https://github.com/thomasmgfeller/x6-spectral-astrolabium/blob/8f55867de35233b760594fdf6468b729f5706833/tests/sagnac/test_core.cjs)
- [Stim-Spezifikation des Detector Error Model](https://github.com/quantumlib/Stim/blob/main/doc/file_format_dem_detector_error_model.md)
- [Surface-Code-Detektoren aus wiederholten Paritätsmessungen](https://doi.org/10.1038/s41586-022-05434-1)
- [Polarisations-Antikorrelation des Singuletts](https://doi.org/10.1088/1367-2630/15/2/025033)
