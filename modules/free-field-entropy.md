# RAX-CQG: freies Feld und Entropiereferenz

Registerstand: 2026-10-19. MAIN / SOFTWARE. Kein Live-Prüfsiegel.

## Quelle

Branch: main

Commit: 6738f129ca31e56a88690a9d17941516ccefb321

[Originaldokumentation](https://github.com/thomasmgfeller/x6-spectral-astrolabium/blob/6738f129ca31e56a88690a9d17941516ccefb321/research/free_field_entropy/README.md)

## Dokumentierte Aussage

Freier masseloser SJ-Gaußzustand auf festen 1+1-kausalen Mengen mit expliziten Nullmoden und Cutoffs. 13 Gegenprüfungen und bekannte Oszillatorentropie bestehen. 64 neue Ordnungen: Steigung 0,358, 95%-Intervall [0,260; 0,458]; vorab verlangte Präzision und Cutoff-Stabilität verfehlt (REFERENCE_NOT_ESTABLISHED). Kein nachgewiesener geometrischer oder industrieller Zusatznutzen.

- [research/free_field_entropy/RESULTS.md](https://github.com/thomasmgfeller/x6-spectral-astrolabium/blob/6738f129ca31e56a88690a9d17941516ccefb321/research/free_field_entropy/RESULTS.md): Vollständiger 64-Ordnungen-Befund, vorab fixiertes Kriterium, Cutoff-Empfindlichkeit und Grenzen.
- [research/free_field_entropy/analytic-validation.json](https://github.com/thomasmgfeller/x6-spectral-astrolabium/blob/6738f129ca31e56a88690a9d17941516ccefb321/research/free_field_entropy/analytic-validation.json): Zwei-Oszillator-Referenz und 13 analytische/strukturelle Gegenprüfungen.
- [research/free_field_entropy/independent-audit.json](https://github.com/thomasmgfeller/x6-spectral-astrolabium/blob/6738f129ca31e56a88690a9d17941516ccefb321/research/free_field_entropy/independent-audit.json): Vier Größen mit getrenntem hermiteschem Kovarianz-Rechenweg; interne Prüfung, keine externe Replikation.
- [research/free_field_entropy/freeze.json](https://github.com/thomasmgfeller/x6-spectral-astrolabium/blob/6738f129ca31e56a88690a9d17941516ccefb321/research/free_field_entropy/freeze.json): Öffentlich vor dem Zielversuch fixierte Quellen und Analyse; früherer Pilot separat ausgewiesen.

## Reproduzieren

Python 3.12 unter Linux/POSIX; NumPy 2.3.5, SciPy 1.17.0 und threadpoolctl 3.6.0. Vollständiger Referenzlauf: maximal 30 Minuten und 2 GiB; kurze Prüfer ohne neue Zielstichproben.

Neue Arbeits- und Ausgabeordner verwenden; Voraussetzungen aus der Originaldokumentation beachten.

```sh
git clone --branch main https://github.com/thomasmgfeller/x6-spectral-astrolabium.git x6-free-field-entropy
cd x6-free-field-entropy
git checkout --detach 6738f129ca31e56a88690a9d17941516ccefb321
python3 -m pip install -r research/free_field_entropy/requirements.txt
OPENBLAS_NUM_THREADS=1 python3 -B research/free_field_entropy/test_core.py -v
OPENBLAS_NUM_THREADS=1 python3 -B research/free_field_entropy/check.py research/free_field_entropy/results
```

Erwartete Ausgabe: 13 Gegenprüfungen bestehen; PASS_LEDGER_AND_ANALYSIS prüft Quellen, vollständige Eingaben und Auswertung. Der getrennte wissenschaftliche Status ist im Ergebnisbericht ausgewiesen.

## Offene Prüfung

Endliche Größeneffekte und Cutoff-Empfindlichkeit in einem neuen vorab festgelegten Versuch klären. Geometrieantworten und Zusatznutzen gegenüber bestehenden Merkmalen bei gleichem Budget bleiben separate offene Gates.

Evidenzberichte behalten ihre eigenen Prüfrevisionen. Keine neue Ausführung, externe Begutachtung oder physische Qualifikation durch diese Darstellung.
