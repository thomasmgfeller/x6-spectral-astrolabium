# CSPP v0.22 - Vollständige endliche Außenhistory

Schritt 1 der Fortsetzung von v0.21 ist ausgeführt. Die gesamte endliche
Außenhistory für -6<=t<=-1 ist auf dem vollständigen exakten KG-Feldträger
einschließlich der räumlichen Flanken und der Wellenfront eingeschlossen.
Für -11/4<=t<=-1 ist ihr Beitrag exakt null. Der alte Patch P ist genau
einmal enthalten; seine alte Grenze wird nicht zusätzlich addiert.

Die feinsten oberen bedingten Erwartungswertschranken, nach oben gerundet:

| Archiv | W0 | W1 |
| --- | ---: | ---: |
| d0_r00 | 0,498358 | 0,535630 |
| d0_r01 | 0,494252 | 0,517072 |
| d0_r02 | 0,508123 | 0,548527 |
| d0_r03 | 0,476913 | 0,511382 |

Diese Grenzen umfassen direkten Detektorbeitrag, bekannte aktive Pfade
und Pfade über unbekannte aktive Außenpunkte. Sie sind keine gemessenen
Fehler, keine unteren Fehlerschranken und keine realisierungsweise Garantie.
Das unveränderte globale Ziel 0,001 ist nicht nachgewiesen.
METHOD_HOLD und G1 HOLD bleiben; eine frische Bestätigung ist NOT_RUN.

Die erste Historykante verwendet die konservative punktweise kappa-Hülle.
Die schärferen archivbedingten Zählkerne aus v0.20/v0.21 werden nicht neu
auf das ganze Gebiet integriert. Der unendliche Wurzelbereich t<-6 wird
in dieser Version noch nicht kombiniert. Die globale v0.19-Majorante
bleibt unverändert. Weder Quelle, Operator, Wolken noch Statistik ändern
sich. Die Rechengrenze ist keine physikalische Historytrunkierung.

## Reproduktion

Getestet: Python 3.12.14, python-flint 0.8.0, NumPy 2.3.5.
Die vollständigen benötigten Eingabedateien liegen bei.

```bash
python3 -m pip install -r requirements.txt
python3 reproduce.py --quick
python3 reproduce.py
```

Der volle Lauf erzeugt die Ergebnisse bei 128 und 192 Bit in einer
isolierten Kopie erneut, prüft sämtliche Kontrollen und verlangt
Byteidentität aller neun numerischen Ergebnisdateien. Die Originaldateien
bleiben unverändert. `verify.py` schreibt seine deterministische
CHECKS.json am Ausgangsort neu. Das ist eine Selbstprüfung, kein externes
wissenschaftliches Review.

Die Produktionsläufe können auch einzeln wiederholt werden:

```bash
python3 run.py --bits 128
python3 run.py --bits 192
python3 verify.py
python3 build_report.py
python3 package.py
```

`build_report.py` erzeugt Bericht und Geometriegrafik neu. Die Anforderungen
für ReportLab/Matplotlib sind für diese Darstellungen, nicht für die
numerische Rechnung erforderlich; DejaVuSans wird unter dem üblichen
Linux-Schriftpfad erwartet. `package.py` erstellt einen deterministischen
ZIP-Abzug einschließlich Manifest, ohne Logdateien oder Python-Caches.

## Inhalt

- `PROOF.md`: vollständige neue Herleitung und Geltungsgrenzen.
- `PROTOCOL.json`: unveränderter physikalischer Ansatz und feste Rechengeometrie.
- `PROVENANCE.json`, `evidence/MAIN_TREE.json`: elf Eingabeidentitäten
  gegenüber Main `ff990b1ffe04259f963525e51aa106925b23cf6f`.
- `domains.py`, `fields.py`, `run.py`: exakte Gebiete, Feldhüllen, Transport.
- `verify.py`: unabhängige Moment-/Massenquadraturen, Geometrie-, Kappen-,
  Präzisions-, Transport- und Negativkontrollen.
- `results/`: sechs vollständige Zellaudits, zwei Präzisionsberichte und CHECKS.
- `REPLAY.json`: beobachteter isolierter Replay und Ergebnisdatei-Hashes.
- `report/`: vierseitiger deutscher Bericht, Geometrie als PNG und SVG.
- `STATUS.json`, `NEXT_STEPS.json`: Grenzen und noch offener unendlicher Rest.

Die exakte Abdeckung ist |D5|=(110567/384)pi. Alle 10480 Zellen des feinsten
Gitters werden integriert. Auf dem vollständigen Detektor summieren sich
die positiven rationalen Teilmassen exakt zu eins. Alle 30 festen KG-
Kontrollpunkte pro Präzision liegen in ihren Feldhüllen. Es gibt keine
zusätzlichen Poissonpunkte oder Zufallsaufrufe.

## Nächster fachlicher Schritt

Den disjunkten Rest t<-6 mit kompatibler Konditionierung und Pfadzerlegung
begrenzen und dann die globale Bilanz bilden. Auch ein kleiner Rest würde
die derzeitigen endlichen Majoranten allein noch nicht unter 0,001 bringen.
Eine Freigabe braucht entsprechend schärfere Abschätzungen. Die fachliche
Arbeit dieses Pakets ist auf Schritt 1 beschränkt.
