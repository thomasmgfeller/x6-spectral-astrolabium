# Eigenzeit v0.2 — Gültigkeitsbereich und Informationsbedarf

Vorab festgelegte, deterministische Untersuchung: Wann liefern Ereigniszahlen
eine ausreichend präzise Eigenzeitschätzung, und wann verdecken enge Intervalle
eine falsche Modellannahme? Die vorhandene flache Referenz bleibt unverändert.

**Status bei Quellenfixierung: PLANNED.** Noch keine Zielgitter-Auswertung.

[Prüfvertrag](contract.json) · [Herleitung und Grenzen](DERIVATION.md) ·
[Bestehende Eigenzeitreferenz](../lorentz_proper_time_publication/README.md)

Geprüft werden flache Modelle in d=2,3,4, eine bekannte de-Sitter-Familie,
veränderte Dichte, unabhängiges Ausdünnen und konforme Dichtezwillinge.
Zusätzliche konservative Intervalle erlauben vorab begrenzte Dichtefehler
im flachen Modell. Diese Grenzen müssen von aussen begründet sein.

Die Auswertung berechnet endliche Binomialwahrscheinlichkeiten direkt.
Es sind keine neuen Monte-Carlo-Punktwolken oder physischen Messungen.
Alle Budgets sind beobachtete Punktzahlen; fehlende Messungen können den
Akquisitionsaufwand zusätzlich erhöhen. Keine allgemeine Krümmungsdiagnose.

## Ausführen

Python 3.12, POSIX, vom Repository-Stamm:

```sh
python3 -m pip install -r research/lorentz_proper_time_validity/requirements.txt
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 python3 -B research/lorentz_proper_time_validity/verify.py --selftest
```

Der Ziellauf benötigt den öffentlich fixierten Quellencommit und einen neuen
Ausgabeordner. Ergebnisse und vollständiger Replay werden nach dem Lauf ergänzt.
Eine erfolgreiche Softwareprüfung ist keine unabhängige wissenschaftliche
Replikation und bestätigt nicht automatisch die Modellannahmen realer Daten.

English: A prospective deterministic validity map for the existing proper-time
reference, including known geometry, density and observation deviations.
Pointwise fixed-budget confidence only; no universal curvature or physical
clock claim. Code and original documentation: Apache-2.0.
