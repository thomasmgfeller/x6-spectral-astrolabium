# CSPP v0.20 - Lokale äußere History und exakte Überlappung

Fortsetzung von Main `b3e2c41bb32fec02a08432b40cc95acba013952a` (PR #151).
Die Quelle, m=1, rho=3/pi, epsilon=1/16, die beiden Detektorfenster und
die vier archivierten Omega5-Konfigurationen sind unverändert.

## Ergebnis

- Geschlossene tatsächliche Volumenformel für I(y,p) Schnitt Omega5, p in Omega5.
- 223 relevante aktive Archivpunkte; 1.698 kausale feste Prüfintervalle,
  darunter 1.475 echte Linsen. 86 weitere Paare sind nicht kausal.
- Acht neu eingeschlossene lokale KG-Werte mit der unveränderten Referenz.
- Vollständige bedingte obere Erwartungswertschranke für alle Pfade mit
  Historywurzel in P=[-6,-5] x [-2,2]^3, einschließlich unbekannter aktiver
  Außenpunkte: etwa 0,004697 bis 0,005799.
- Der komplementäre Wurzelbereich ist nicht neu integriert. Die globale
  v0.19-Restmajorante bleibt unverändert. Kein Abzug einer oberen Patchgrenze
  von einer oberen Gesamtgrenze.

METHOD_HOLD und G1 HOLD. Frische Bestätigung NOT_RUN. Keine neuen
Zufallsaufrufe, Wolken oder statistischen Regeln. 0,001 bleibt der bisherige
Vergleichsmaßstab und wird nicht zu einem eigenen Patchbudget umdefiniert.

## Inhalt

- `PROOF.md`: vollständige Ableitung, Zellhüllen, Pfadzerlegung und Restbilanz.
- `PROTOCOL.json`: festgelegte geometrische Punkte, Partitionen und Scope.
- `overlap.py`: exakte Kausalentscheidungen und eingeschlossene Volumina.
- `kernel.py`, `kernel_table.py`: bedingte absolute Poisson-Gewichte und
  nach oben geprüfte Majorantentabelle.
- `run.py`: lokale KG-Auswertung, tatsächliche Archivzählung, volle Patchrechnung.
- `verify.py`: unabhängige Integerzählung, Invarianten, Gegenproben und
  Präzisionsvergleich; `reproduce.py`: isolierter vollständiger Wiederholungslauf.
- `legacy/`: bitgenau gepinnte KG-Referenz aus v0.3/v0.5.
- `evidence/`: vier exakte Archivarrays, v0.16-Detektorkoeffizienten,
  v0.19-Restmajoranten, Quellenidentitäten und symbolische Kontrolle.
- `results/`: beide Präzisionsläufe, sämtliche Zellzertifikate und Checks.
- `report/`: lesbarer Bericht; `SHA256SUMS`: Paketintegrität.

## Reproduktion

Python 3.12 und python-flint 0.8.0 werden verwendet. Abhängigkeiten:

```bash
python -m pip install -r requirements.txt
python reproduce.py --quick
python reproduce.py
```

Der vollständige Lauf rechnet in einem temporären Verzeichnis beide
Präzisionen neu und vergleicht die Ergebnisdateien byteweise. Er überschreibt
die archivierten Ergebnisse nicht. Der Bericht wird separat mit
`python build_report.py` gebaut. Ein vollständiger Wiederholungslauf benötigt
auf der verwendeten Umgebung einige Minuten.

Physikalische Werte werden auf Überlappung ihrer Intervalle kontrolliert.
Obere Majoranten können sich bei anderer Präzision geringfügig ändern:
obere Endpunkte und die quantisierten Arb-Radien sind Teil ihrer Konstruktion.
Kleine arithmetische Radien sind keine kleinen physikalischen Fehlerbalken.

Das Paket behauptet kein unabhängiges wissenschaftliches Review und keine
Bestätigung einzelner Realisierungen. Die feste Patchgeometrie ist eine
Integrationszerlegung, kein neuer physikalischer History-Cutoff.
