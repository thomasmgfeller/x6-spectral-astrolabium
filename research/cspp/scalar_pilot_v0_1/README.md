# CSPP: skalarer Referenzpilot v0.1

**Schritt 2 ausgeführt — wissenschaftlicher Status: HOLD.**
64 unabhängige Poisson-Sprinklings in flacher 3+1-Raumzeit, vier Dichten,
drei gepaarte BD-Glättungen, zehn analytische Operatorfelder,
vier analytisch kontrollierte Propagationsfelder und drei KG-Quellendiagnosen.
Alle 64 Hauptläufe wurden berechnet; keine Wolke wurde nach Ergebnis verworfen.

## Ergebnis

Keine der zwölf Zellen erreicht die vorläufige Operatorgrenze 0,1.
Die Tabelle zeigt pro Zelle den größten normalisierten RMS-Fehler unter
allen zehn Feldern, jeweils über 16 Wolken und 21 feste Proben:

| Erwartete Punktzahl ν | ε=1 | ε=1/4 | ε=1/16 |
|---:|---:|---:|---:|
| 512 | 382.458 | 10.862 | 1.461 |
| 1024 | 680.630 | 17.961 | 2.180 |
| 2048 | 1572.813 | 39.256 | 3.435 |
| 4096 | 2731.881 | 79.332 | 7.586 |

Der kleinste Tabellenwert ist 1,461, also rund 14,6-mal die vorgesehene
Schwelle. Dies ist ein negatives Ergebnis für **diesen begrenzten Pilotbereich**,
kein Ausschluss anderer Dichte-, Glättungs-, Rand- oder Operatorkonstruktionen.
Die Maxima betreffen je nach Zelle verschiedene Felder; die vollständigen
feldweisen Werte einschließlich Bias und Streuung stehen in
[RESULTS.json](results/RESULTS.json).

![Deskriptive Ergebnisse des skalaren Piloten](scalar-pilot.png)

Die analytischen Propagationskontrollen zeigen ebenfalls deutliche Fehler.
Bei ε=1 nimmt die größte gemessene Antwort auf eine Einheitsänderung der
Historie von etwa 491 auf 16.151 zu. Diese eine Testrichtung beweist keine
allgemeine Instabilität, verhindert aber eine ungeprüfte Freigabe.
Der größte algebraische Rückwärtsfehler beträgt nur 3,13×10⁻¹⁶.
Das unterscheidet eine präzise Lösung des diskreten Systems von einer
präzisen Annäherung an die Kontinuumsgleichung.

Weitere getrennte Befunde:

- **Skalen:** ℓ liegt zwischen 0,601 und 1,012 L0, ℓk zwischen 0,601 und
  2,023 L0. Für k=8 liegt kℓk zwischen 4,81 und 16,19; ein langsames
  Variieren auf der Nichtlokalitätsskala ist hier nicht erreicht. Die
  Quellenbreite a=0,5 L0 ist ebenfalls kleiner als ℓ.
- **Rand:** Acht gepaarte Erweiterungen Ω4→Ω5 zeigen relevante Änderungen.
  Auch bei ε=1/16 liegt die maximale feldweise normierte RMS-Änderung
  der inneren Proben bei 0,258 (ν=512) beziehungsweise 1,821 (ν=4096).
- **Quellenreferenz:** 64³ und 128³ unterscheiden sich an den 28
  Propagationsproben relativ um 71,4 %, 69,3 % und 60,8 % RMS für
  m=0,1,2. Die feinere Rechnung ist keine qualifizierte Referenz.
  Die vier analytischen Propagationskontrollen hängen nicht von ihr ab.
- **Statistik:** M=16 ist ein festes Entwicklungsensemble. Es werden
  keine bestätigenden Konfidenzintervalle oder Kontinuumsexponenten behauptet.

## Reproduzierbarkeit und Grenzen

123.083 innere Punkte, alle Rohwolken und komplexen Probeamplituden sind
archiviert. Das Pilotbudget beträgt 4 GiB / sechs Stunden; gemessen wurden
26.5 s für Operator/Propagation, 20.7 s für die Fourier-Referenzen
und 487.0 MiB maximale RSS im Gesamtprozess.

14 algebraische und numerische Kontrollprüfungen sowie ein vollständiger
Replay aller 64 Läufe prüfen Zählungen, Operator, Propagation, Randkontrollen,
Referenzproben und Ergebniszusammenfassung. Das ist interne Softwareprüfung,
keine externe Begutachtung und kein G1-Zertifikat.

Ein beim Review erkannter Auswahlfehler im zusätzlichen äußeren Sprinkling
wurde vor Veröffentlichung korrigiert. Die ursprüngliche Quellsperre und
Änderung sind in [Amendment 01](amendment_01/README.md) dokumentiert.
Der Audit verlangt byteidentische Hauptresultate vor und nach dieser Korrektur.
Die korrigierten Randdiagnosen ersetzen die fehlerhaften ersten Randdiagnosen.

**G1 bleibt HOLD. Dirac, Flavor und Kohärenz werden noch nicht freigegeben.**
Die Propagation verwendet vorgegebene Kontinuumswerte der gesamten
Vergangenheit bis t=−1. Ein intrinsischer Cauchy-Adapter, eine zertifizierte
Kontinuumsreferenz und eine gemeinsame Geometrie-/Operatorfehlergrenze fehlen.
Die sieben Detektorproben ersetzen keine Detektorintegration.
Die früheren Eigenzeit-Zertifikate und wissenschaftlichen HOLDs bleiben unverändert.

## Nächster sinnvoller Arbeitsschritt

Ein eigenes **Skalen- und Randkalibrierungsexperiment** festlegen: zunächst
langsam variierende analytische Felder, ε mit ρ so koppeln, dass zunächst
ℓk fest bleibt und ℓ/ℓk sinkt; anschließend ℓk verkleinern, während Feld-
und Randabstände kontrolliert werden. Der vorliegende Scan mit konstantem
ε prüft diese zweistufige Annäherung nicht. Parallel braucht die kompakte
Quelle eine deutlich feinere, unabhängig abgesicherte Referenz und einen
klaren Anfangsdatenadapter. Erst nach unabhängiger G1-Prüfung ist der
Dirac-Kandidat wissenschaftlich sinnvoll zu bewerten.

## Reproduktion

Python 3.12, g++ mit C++17, numpy==2.3.5, scipy==1.17.0.
Für die optionale Grafik zusätzlich Matplotlib.

```sh
export OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1
python3 -B research/cspp/scalar_pilot_v0_1/verify_publication.py
python3 -B research/cspp/scalar_pilot_v0_1/audit.py --replay
python3 -B research/cspp/scalar_pilot_v0_1/run.py all --out /tmp/cspp-scalar-replay
```

`run.py all` wiederholt denselben Entwicklungslauf; es ist kein neues
unabhängiges Experiment. Archivdateien werden bei `--out /tmp/...` nicht
überschrieben. Die neue Zeitmessung und ZIP-Metadaten müssen nicht bytegleich
sein; maßgeblich sind Roharrays, Zählhashes, Metriken und Statusentscheidungen.
Der Bestätigungs-Seed wurde nicht benutzt.

## Dateien

- [Methode und Primärliteratur](METHODS.md), [festgelegter Pilotplan](PROTOCOL.json), [Quellsperre](FREEZE.json).
- [Rohwolken](results/clouds.npz), [Laufprovenienz](results/RUNS.json), [komplexe Metriken](results/metrics.npz).
- [Numerische Referenzwerte als bytegenaue Teilarchive](results/REFERENCE_ARCHIVE.json), [Datenlayout und Rekonstruktion](DATA.md), [Referenzstatus](results/REFERENCE.json), [Zusatzdiagnosen](results/DIAGNOSTICS.json).
- [Audit](AUDIT.json), [Paketprüfsummen](SHA256SUMS), [exportierbare Vektorgrafik](scalar-pilot.svg).
- [Unveränderter E4-Vertragsentwurf](../e4_v0_1/README.md).
