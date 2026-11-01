# Eigenzeit v0.3 · Drei Geometrien und ein kontinuierliches Krümmungsintervall

Eine einzelne unbeschriftete Kausalordnung liefert eine Auswahl unter drei Krümmungen und ein Intervall für Zwischenwerte. Die Garantien gelten für einen vollständigen 4D-Kausaldiamanten bei fester Ereigniszahl und unabhängiger, gleichmäßiger Beprobung nach physischem Volumen. Die Rasterkrümmungen RT² sind ungefähr 0, 0,758 und 3,131.

[120 Pilotfälle und eigene Paarzahlen im Browser prüfen](https://thomasmgfeller.github.io/x6-spectral-astrolabium/app/eigenzeit-kruemmungsintervalle/index.html) · [Forschungsbericht (PDF)](Eigenzeit_Drei_Geometrien_v0_3.pdf) · [Herleitung](BEWEIS.md) · [Prüfpaket mit Quellcode und Daten (ZIP)](Eigenzeit_Drei_Geometrien_v0_3_Pruefpaket.zip)

[Fortsetzung v0.4 mit begrenzter Beprobungsdichte und exakt ununterscheidbaren Geometrien](../density_contrast_v0_4/README.md).

| Verfahren | Ereignisse | Geprüfte Paare | Richtiger Rasterwert allein, mindestens | Intervallüberdeckung, mindestens |
|---|---:|---:|---:|---:|
| Vollständige Paarzählung | 600.000 | 179.999.700.000 | 81,67 % | 95,14 % |
| Zufällige Achtergruppen | 900.000 | 3.150.000 | 80,40 % | 95,05 % |

Für das Dreifachziel sind **mindestens 217.347 Ereignisse** notwendig. Die Wahrscheinlichkeit der richtigen Einzelentscheidung gilt bei wahrer Rastergeometrie. Die Intervallüberdeckung gilt für jeden festen Wert von h in [0, 1/2]. Im Achtergruppenpilot bei h = 3/8 blieben in allen zwölf Fällen nur Zwischenwerte vereinbar. Alle zwölf kontinuierlichen Intervalle enthielten die wahre Krümmung.

Das Archiv enthält alle 13,5 Millionen Gruppenzählungen, den Quellcode zum Erzeugen und Auswerten der 120 Fälle sowie die lokal vor dem Lauf fixierten Unterlagen. Der Zufallspilot in voller Größe betrifft die Achtergruppen. Für die Vollzählung liegen analytische Schranken und eine strukturierte Testordnung mit 600.000 Ereignissen vor. [Exaktes Zertifikat](certificate.json) · [Pilotauswertung](pilot_audit.json) · [Vorstudie v0.2](../single_order_power_v0_2/README.md)

## Reproduktion

Vom Wurzelverzeichnis des Repositorys aus:

```sh
python3 research/eigenzeit/three_geometries_v0_3/publication_check.py
python3 research/eigenzeit/three_geometries_v0_3/publication_check.py --replay --workers 4
```

Der erste Lauf prüft die veröffentlichten Originaldateien, ihre 37 Archiveinträge und die einzeln verlinkten Fassungen. Der zweite Lauf erzeugt den Pilot aus den archivierten Seeds erneut, berechnet Zertifikat und Gegenkontrollen und prüft die Browserlogik an 11.419 Schwellenfällen sowie allen 120 Beobachtungen. Er benötigt Python 3.12, NumPy, SciPy und Node. Die NumPy- und SciPy-Versionen sind im Repository fixiert. [Abhängigkeiten](../../../tools/workflow/requirements-research.txt) · [Veröffentlichungsnachweis](PUBLICATION.json)

Für die CI setzt `--cpu-baseline` bei der Erzeugung der simulierten Koordinaten den NumPy-Rechenpfad mit deaktiviertem AVX512F. Die zugehörigen SHA-256-Werte sind separat festgelegt. Alle 13,5 Millionen beobachteten Gruppenzahlen, die übrigen Fallmetadaten, die Entscheidungen und das Zertifikat müssen in beiden Varianten exakt der Archivfassung entsprechen. [Koordinatenprüfsummen für diesen Rechenpfad](cpu_baseline.json)
