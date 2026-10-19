# RAX-CQG: endlicher Causal-Set Benchmark 0.2.0

Registerstand: 2026-10-19. MAIN / SOFTWARE. Kein Live-Prüfsiegel.

[Causal-Set-Labor öffnen →](https://thomasmgfeller.github.io/x6-spectral-astrolabium/app/rax-cqg-lab.html)

## Quelle

Branch: main

Commit: ac519f5e4a83de0e570680fe4cfeb2da133db351

[Originaldokumentation](https://github.com/thomasmgfeller/x6-spectral-astrolabium/blob/ac519f5e4a83de0e570680fe4cfeb2da133db351/docs/research/rax/cqg-benchmark-v0.2.0/README.md)

## Dokumentierte Aussage

Explizite endliche Ordnungen, Intervalle, dimensionslose 4D-BDG-Kombination, Graphspektren und induzierte Ausdünnung. Separates klassisches Gaußfeld und vorausgesetzte Zweiqubit-Uhr. Kein Nachweis für Quantengravitation, KR-Unterdrückung oder einen Kontinuumslimes.

- [research/rax_cqg/benchmark-v0.2.0/VALIDATION.json](https://github.com/thomasmgfeller/x6-spectral-astrolabium/blob/ac519f5e4a83de0e570680fe4cfeb2da133db351/research/rax_cqg/benchmark-v0.2.0/VALIDATION.json): Eingefrorener interner Prüflauf mit Quellenhashes und expliziten Grenzen. UI-Logik in Node; keine damalige visuelle Browserprüfung oder personell unabhängige Replikation.
- [docs/research/rax/cqg-benchmark-v0.2.0/PUBLICATION.json](https://github.com/thomasmgfeller/x6-spectral-astrolabium/blob/ac519f5e4a83de0e570680fe4cfeb2da133db351/docs/research/rax/cqg-benchmark-v0.2.0/PUBLICATION.json): Freigegebenes ZIP, 28 bytegleiche Paketdateien und identische Browserkopie; zusätzliche CI getrennt vom ursprünglichen Bericht.

## Reproduzieren

Python 3.12, NumPy 2.3.5, SciPy 1.17.0, Node.js 24; Browser für das eigenständige HTML-Labor. Installation der Python-Abhängigkeiten benötigt Netzwerk oder vorbereitete Wheels.

Neue Arbeits- und Ausgabeordner verwenden; Voraussetzungen aus der Originaldokumentation beachten.

```sh
git clone --branch main https://github.com/thomasmgfeller/x6-spectral-astrolabium.git x6-rax-cqg-benchmark
cd x6-rax-cqg-benchmark
git checkout --detach ac519f5e4a83de0e570680fe4cfeb2da133db351
cd research/rax_cqg/benchmark-v0.2.0
python3 -m pip install -r requirements.txt
python3 validate.py
```

Erwartete Ausgabe: PASS_WITH_EXPLICIT_SCOPE_LIMITS; 28 Python-Testmethoden, 28 Python/JavaScript-Vergleichsfälle, 16 UI-Logikprüfungen, 240 wiederholte Pilotläufe und 30 Gruppenauswertungen. Fehler: Exit ungleich 0. Der Befehl schreibt einen neuen lokalen Bericht.

## Offene Prüfung

Unabhängige Replikation und fachliche Prüfung. Vor Ensemblevergleichen Beobachtungsgrösse, Dichtekontrollen, Stichprobengrösse und Fehlerbudget festlegen; keine neue physikalische Schlussfolgerung aus dem Pilot allein.

Evidenzberichte behalten ihre eigenen Prüfrevisionen. Keine neue Ausführung, externe Begutachtung oder physische Qualifikation durch diese Darstellung.
