# CSPP v0.17: Endliche aktive Hülle und Konvergenz der KG-History

Der nächste mathematische Schritt nach dem zusammengeführten v0.16 ist ausgeführt.
Die aktive kausale Vergangenheit des unveränderten Detektors liegt vollständig
in Omega_(21/4). Mit der vorgegebenen glatten kompakten KG-History lässt sich die
absolute Summierbarkeit der History-Forcierung im homogenen Poisson-Modell und
damit die fast sichere Existenz der vollständigen Detektorantwort herleiten.

**Das ist ein analytischer Existenznachweis, keine numerische Restbescheinigung
für die vier Archivfortsetzungen.** Der Rest hinter Omega5, das Fehlerziel 0,001,
METHOD_HOLD und G1 HOLD bleiben offen beziehungsweise unverändert. Keine neue
Wolke, kein neuer Seed, keine neue Testschwelle und keine unabhängige Bestätigung.

Neue Resultate:

- Scharfe aktive Einschlussgrenze: H=21/4=5,25.
- In Omega5 fehlt nur noch ein aktiver Bereich mit -1<t<-7/8 und
  Raumzeitvolumen 29*pi/1536. Seine zusätzliche Poisson-Punktzahl hat Mittelwert
  29/512. Die Modellwahrscheinlichkeit für mindestens einen Punkt ist
  1-exp(-29/512)=0,055066406135...; kein Konfidenztest und kein Leernachweis.
- Eine ungewichtete globale absolute Kernnorm divergiert. Das verhindert
  nicht die Summierbarkeit für die hier festgelegte glatte KG-History.
- Ein Fourierargument für den schnellen Abfall nahe dem Lichtkegel und eine
  Gaußabschätzung im übrigen Gebiet ergeben eine summierbare Ein-Schritt-
  Majorante. Die darin enthaltenen Quellseminormen sind noch nicht numerisch
  eingeschlossen. Sie liefern daher keinen Zahlenwert für den Detektorrest.
- Eine unendliche aktive Volterra-Inverse ist für diesen festgelegten
  Anfangszeitpunkt und diesen kompakten Detektor nicht erforderlich.

## Dateien und Reproduktion

`PROOF.md` enthält die vollständige Herleitung und ihre Reichweite.
`analytic.py` prüft exakte rationale Geometrie, unabhängige axiale
Volumenintegration, Momentidentitäten, Binomialgewichte, Negativkontrollen und
Quellidentitäten. Irrationale Zahlen erhalten Arb-Einschließungen bei 192 Bit.

```sh
python3 analytic.py
python3 verify_package.py
```

Benötigt: Python 3.12, python-flint==0.8.0. Das PDF wird mit
`python3 build_report.py` erstellt; dafür zusätzlich reportlab==4.4.9.
Die Rechenkontrollen beweisen nicht automatisch das analytische Fourier-
oder Poissonargument; diese stehen ausdrücklich als lesbarer Beweis im Text.

`evidence/` enthält unveränderte ausgewählte v0.16-Belege sowie die ursprüngliche
Gewichts- und Quelldefinition. Die früheren großen Replays werden nicht erneut
als neue Validierung ausgegeben. Basis: PR #148, Merge
`5c075bfae81ee6ab5edea72a8ec9aa9ed3583b69`.

## Präziser Anschluss

Für eine numerische Fortsetzung zuerst explizite Quellseminorm-Schranken und
eine **transportierte** Restmajorante einschließen. Ein Erwartungswert der
Forcierung ersetzt weder den konkreten Rest noch die Kontrolle des korrelierten
aktiven Transportes. Die fehlende aktive Realisierung darf nicht ohne
Protokollentscheidung auf leer gesetzt oder neu gezogen werden.
