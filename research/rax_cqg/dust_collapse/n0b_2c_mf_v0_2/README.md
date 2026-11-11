# N0B-2C-MF v0.2: Referenzmodell und offene CST-Brücken

11. November 2026. Korrigierte Synthese der eingereichten v0.1-Entwürfe.
**Ein reduziertes Geometrie-Stratum-Materie-Modell mit bedingter relationaler
Quantendynamik. Seine Herleitung aus der gemeinsamen CST-Amplitude bleibt HOLD.**

Die Veröffentlichung ergänzt die [bestehende Staubball-Reihe](../README.md).
Die endliche Stationaritätsprüfung [(2,3)](../asymmetric_stationarity_2_3_v0_1/README.md)
und ihre offene Folgeklasse (1,4) behalten ihre Reichweite. Das Referenzmodell
ersetzt weder die geerbte Materiewirkung noch deren Randrelation durch eine
bereits hergeleitete Schrödingerdynamik. Alle acht physikalischen CST-DUST-Gates
bleiben HOLD: MODEL, CURRENT, CORRESPONDENCE, BOUNCE, REGULARITY, BOUNDARY,
TRAPPING, EXTENSION.

## Lesen und einordnen

| Dokument | Inhalt |
|---|---|
| [MODEL.md](MODEL.md) | Modellannahmen, Hilbertraum, Domäne, Uhr und Symmetrien |
| [BALANCES.md](BALANCES.md) | Norm, Energie, Impuls, Wandkraft und variable Masse |
| [BRIDGE_CONTRACT.md](BRIDGE_CONTRACT.md) | Anschluss an den Vorgänger und fünf offene Herleitungsbrücken |
| [VALIDATION.md](VALIDATION.md) | Gitterstudie, Quantensignaturen und Historien |
| [DATA_CONTRACT.md](DATA_CONTRACT.md) | Anforderungen an künftige Matrix- und Trajektoriendaten |
| [CORRECTIONS.md](CORRECTIONS.md) | Korrekturen, Gründe und Kontrollzuordnung |
| [SOURCES.md](SOURCES.md) | Pinned Projektquellen, Literatur und Herkunft der Entwürfe |
| [status.json](status.json) | Getrennte Modell-, Software- und physikalische Statuswerte |
| [Bericht](N0B_2C_MF_v0_2_Bericht.pdf) | Kurze Lesefassung aus [REPORT.md](REPORT.md) |
| [Prüfpaket](N0B_2C_MF_v0_2_Pruefpaket.zip) | Dokumente, Quellen, Kontrollen und archivierte Resultate |

## Tatsächlich ausgeführt

Die kleinen Kontrollen prüfen Transferzeichen, lokale Bilanzidentitäten,
Wandimpuls, kombinierte Parität, kohärenten Transfer bei verschwindender
reduzierter Stratumkohärenz, beide Oszillator-Übergangsrichtungen,
Kernrevival, einen falschen Modenfehler-PASS, die Randwirkungs-/Frequenzverwechslung,
Gaußfaktoren, variable Masse und die Propagatorkompression. Sie stehen in
[checks/run_checks.py](checks/run_checks.py); die Resultate in
[results/checks.json](results/checks.json). Das sind algebraische bzw. kleine
synthetische Kontrollen, keine CST-Kerndaten und keine Staubballsimulation.

```sh
python3 -m pip install -r requirements-checks.txt
python3 -O -B checks/run_checks.py --output /tmp/n0b-checks.json
python3 -O -B verify_package.py --replay
```

Die Befehle werden aus diesem Ordner ausgeführt. Der Replay vergleicht
kanonische Resultate bytegleich; er ruft keine externen Dienste auf.
Installation der Abhängigkeiten ist vom eigentlichen Offline-Replay getrennt.
Es wurden keine kostenpflichtigen Läufe oder Zeitpläne eingerichtet.

## Was offen bleibt

Kein gemeinsamer physikalischer CST-Kern samt Gram-Produkten liegt diesem
Paket als Matrixdatensatz bei. Der historische Solver und die in den Entwürfen
als implementiert bezeichneten Extraktions-/Signaturprogramme sind hier nicht
als verifizierter Originalquellcode wiederhergestellt. Die Vier-Gitter-Studie,
die A-F-Vergleichsläufe und die physikalischen Brückengates sind NOT_RUN/HOLD.
Unlesbare Originalformeln werden nicht als authentisch rekonstruiert ausgegeben.

Vor dem nächsten dynamischen Lauf sind insbesondere Materiewirkung und
Feldumkehrsymmetrie, die gemeinsame Modenidentifikation sowie die Wahl einer
konstanten oder geometrieabhängigen Modenmasse zu klären. Ein positiver
Geometrie-Minimalwert allein belegt weder einen materievermittelten Bounce
noch Singularitätsauflösung oder einen gemeinsamen Außenraum.
