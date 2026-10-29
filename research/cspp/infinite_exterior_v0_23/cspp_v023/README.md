# CSPP v0.23 – unendlicher Rest und vollständige globale Bilanz

Schritt 2, 29. Oktober 2026. Basis ist der verifizierte Main-Commit
`fdf99cd95330eea4151ba32305e9ea8f2f06f2b2` nach PR #154 im Repository
`thomasmgfeller/x6-spectral-astrolabium`.

Der gesamte unendliche History-Rest für t < −6 ist eingeschlossen und mit
der unveränderten endlichen Außenhistory aus v0.22 verbunden. Die Zerlegung
ist disjunkt bis auf Nullränder, umfasst den vollständigen KG-Träger und
enthält direkte Detektorbeiträge, alle bekannten aktiven Pfade sowie
unbekannte aktive Außenpfade. Der frühere lokale Patch wird genau einmal
gezählt. Die physikalische History wird nicht abgeschnitten.

## Ergebnis und Bedeutung

Die obere bedingte Erwartungswertschranke für den absoluten globalen Rest
liegt über die vier festen Archive und zwei Detektorfenster bei rund
3,17 bis 3,75 × 10^10. Gegenüber der bisherigen globalen Schranke aus
v0.19 ist das eine Verbesserung um etwa Faktor 6982 bis 9130.
Die folgenden Werte sind nach oben gerundet:

| Archiv | W0 · obere Grenze / 10^10 | W1 · obere Grenze / 10^10 |
|---|---:|---:|
| d0_r00 | 3,629580 | 3,710231 |
| d0_r01 | 3,384939 | 3,267606 |
| d0_r02 | 3,640491 | 3,744072 |
| d0_r03 | 3,173048 | 3,294028 |

Das unveränderte globale Ziel 0,001 ist **nicht nachgewiesen**.
METHOD und G1 bleiben **HOLD**, eine frische Bestätigung bleibt NOT_RUN.
Die großen oberen Grenzen sind weder gemessene Fehler noch untere
Fehlergrenzen oder eine Garantie für einzelne Realisierungen. Sie liefern
keinen Nachweis gegen die Genauigkeit oder gegen die Operatorfamilie.
Der nahe Lichtkegelteil der unendlichen Majorante ist der verbleibende
Engpass. Quelle, Operator, Archive und statistische Regeln bleiben gleich.

## Neue Abschätzung

Eine einseitige Konturabschätzung liefert für J=1,...,34 und δ=j/16,
j=1,...,15 gültige Potenzhüllen mit Exponenten J−3/4. Ihre positiven
Zeitintegrale werden über [5,8], [8,16], ... und einen analytischen Rest
bis unendlich eingeschlossen. Eine zusätzliche L²-Abschätzung mit
Cauchy-Schwarz in Raum und Zeit verkleinert den fernen Teil. Alle
Kernmomente besitzen analytische Gammafunktionsreste bis unendlich.

223 bekannte Endpunkte und 256 vollständige Detektorzellen werden
individuell behandelt. Zwei uniforme Fensterhüllen erfassen unbekannte
Außenpfade. Bedingte Kernhüllen und der multivariate Mecke-Schritt erhalten
die Abhängigkeiten der Historyintervalle. Die vollständige Herleitung
steht in [PROOF.md](PROOF.md).

## Reproduktion

Geprüfte Laufzeit: Python 3.12.14, python-flint 0.8.0, NumPy 2.3.5.
ReportLab und Matplotlib sind nur für den Bericht erforderlich.

```sh
python3 -m pip install -r requirements.txt
python3 reproduce.py
```

Der Replay prüft zuerst die beigefügten Resultate, rechnet dann in einem
temporären Verzeichnis mit 128 und 192 Bit neu und verlangt Byteidentität
aller fünf Ergebnisdateien. Die Originaldateien bleiben unverändert.

```sh
python3 reproduce.py --quick
```

Der Schnelllauf prüft die mitgelieferten Zahlen, Identitäten,
Gegenquadraturen, Negativkontrollen, Transportzerlegungen, Eingabehashes
und Präzisionsstabilität, ohne die Produktionsläufe zu wiederholen.

Der ausgeführte vollständige Replay war erfolgreich. Die Checks umfassen
14 Eingabedateien, 35 archivierte Quellnormpaare, 34 Gammaidentitäten,
49 unabhängige Integralgegenrechnungen, 12 direkte Poissonkontrollen,
958 Endpunkt-Audits und 16 globale Zerlegungen über beide Präzisionen.
Vier absichtlich falsche Hypothesen werden zurückgewiesen. Diese
Selbstprüfungen sind kein unabhängiges wissenschaftliches Review.

## Dateien

- `report/Unendlicher_Rest_Globale_Bilanz_v0_23.pdf`: deutscher Bericht.
- `PROOF.md`, `PROTOCOL.json`: Herleitung und unveränderte Festlegungen.
- `bounds.py`, `run.py`, `verify.py`, `reproduce.py`: Rechnung und Prüfung.
- `results/`: vollständige Intervalle, Endpunkt-Audits und Kontrollen.
- `PROVENANCE.json`, `evidence/`: unveränderte Eingaben mit SHA256,
  Git-Blob-Identitäten und Herkunftspfaden am Basis-Commit.
- `REPLAY.json`, `REPORT_QA.json`: ausgeführte Reproduktion und Berichtprüfung.
- `STATUS.json`, `NEXT_STEPS.json`: Aussagegrenzen und Anschlussentscheidung.
- `PACKAGE.json`, `SHA256SUMS`: Inventar und Integritätsprüfung.

`python3 build_report.py` erzeugt den Bericht aus den gespeicherten
Ergebnissen; dafür werden DejaVu-Sans-Schriften unter
`/usr/share/fonts/truetype/dejavu` benötigt. `python3 package.py` erzeugt
das deterministische Prüfpaket unter `../output/`. Kein Programm in diesem
Paket zieht neue Zufallswolken oder publiziert Änderungen auf GitHub.

Schritt 3 bleibt offen: die methodischen Gates anhand der vollständigen
Bilanz neu bewerten und die breite nahe Tail-Hülle berücksichtigen.
Eine neue Bestätigungsstichprobe setzt eine tragfähige Begründung voraus.
