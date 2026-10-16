# Gemeinsame Offline-Referenzsuite

Registerstand: 2026-10-16. MAIN / SOFTWARE. Kein Live-Prüfsiegel.

## Quelle

Branch: main

Commit: a1f22f6c59f3c5259d12cfb6c0ca2e8b0886f33f

[Originaldokumentation](https://github.com/thomasmgfeller/x6-spectral-astrolabium/blob/a1f22f6c59f3c5259d12cfb6c0ca2e8b0886f33f/docs/OFFLINE_REFERENCE.md)

## Dokumentierte Aussage

Vier unveränderte Wolfram-Archive, fünf rationale Graphfälle, 318 n=6-Ordnungen mit 4.208 exakten Polynomen und aktueller Signal-Lab-Kern gegen die gespeicherte Polaritätsreferenz. Vollständiges quellengebundenes Replay. Frische CI-Checkouts laufen bei relevanten Änderungen mit abgeschaltetem Netzwerk. Endliche Software-/Referenzrechnung, keine physische Abnahme oder externe Begutachtung. Zusätzlich: vier n=6-Restpaare exakt mit Wolfram gegengeprüft; Gradpaar-/Zählseparatoren und n=7/n=8-Grenzfälle lokal reproduzierbar. X6-QE ergänzt drei bekannte exakte Graphreferenzen mit vier Graphen; kein Quanten-, Gedächtnis- oder Arithmetikbefund.

- [research/x6_qe/evidence/local-results.json](https://github.com/thomasmgfeller/x6-spectral-astrolabium/blob/a1f22f6c59f3c5259d12cfb6c0ca2e8b0886f33f/research/x6_qe/evidence/local-results.json): X6-QE: lokal ausgeführte exakte Referenzen, vier Graphen, zwölf Umbenennungen, 21 erwartete Zurückweisungen. Quellenhashes im Bericht; keine externe Prüfung.
- [research/lorentz_n6_residuals/ACCEPTANCE.md](https://github.com/thomasmgfeller/x6-spectral-astrolabium/blob/a1f22f6c59f3c5259d12cfb6c0ca2e8b0886f33f/research/lorentz_n6_residuals/ACCEPTANCE.md): Aktuelle Neun-Berichte-Abnahme der Implementierung 5eaffee5a594e2c2c5b86db28a1406dc29168087. Lokal und Netzwerk-isolierte CI PASS, identisches Bundle. Ältere Acht-Berichte-Belege unten gehören zu ihrer historischen Quellenrevision.
- [docs/reference-suite/README.md](https://github.com/thomasmgfeller/x6-spectral-astrolabium/blob/a1f22f6c59f3c5259d12cfb6c0ca2e8b0886f33f/docs/reference-suite/README.md): Ausgeführte Abnahme der Implementierung 7c35b591f77ab1c123ee9795ea6978d1681d59bb. Lokale und Netzwerk-isolierte CI-Abnahme PASS, identische Bundle-Prüfsumme.
- [docs/reference-suite/local/acceptance.json](https://github.com/thomasmgfeller/x6-spectral-astrolabium/blob/a1f22f6c59f3c5259d12cfb6c0ca2e8b0886f33f/docs/reference-suite/local/acceptance.json): Frischer sauberer Checkout ohne .venv/Site-Pakete; elf CLI-Schritte einschließlich zehn erwarteter Zurückweisungen. Historische Prüfrevision explizit gespeichert.
- [docs/reference-suite/local/run/complete.json](https://github.com/thomasmgfeller/x6-spectral-astrolabium/blob/a1f22f6c59f3c5259d12cfb6c0ca2e8b0886f33f/docs/reference-suite/local/run/complete.json): Vollständiges Bundle mit acht Berichten, Quellenhashes und Inventar; durch reference verify erneut berechenbar.
- [docs/reference-suite/ci/acceptance.json](https://github.com/thomasmgfeller/x6-spectral-astrolabium/blob/a1f22f6c59f3c5259d12cfb6c0ca2e8b0886f33f/docs/reference-suite/ci/acceptance.json): GitHub-Lauf 38720405798: network_namespace_isolated=true, alle elf CLI-Schritte wie erwartet.

## Reproduzieren

Linux/POSIX x86-64, Python 3.12 und Node.js 24. Nur Standardbibliothek; kein setup, NumPy/SciPy, Netzwerk oder Wolfram-Zugang. Neuer Ausgabeordner.

Neue Arbeits- und Ausgabeordner verwenden; Voraussetzungen aus der Originaldokumentation beachten.

```sh
git clone --branch main https://github.com/thomasmgfeller/x6-spectral-astrolabium.git x6-offline-reference
cd x6-offline-reference
git checkout --detach a1f22f6c59f3c5259d12cfb6c0ca2e8b0886f33f
python3 -S -B x6.py reference qualify --output /tmp/x6-reference-evidence
python3 -S -B x6.py reference verify /tmp/x6-reference-evidence
```

Erwartete Ausgabe: Exit 0; PASS_OFFLINE_REFERENCE_REPLAY, 10 Berichte, 27 übergreifende plus 17 Lorentz- und 21 QE-Fehlerkontrollen. Fälschungen einschließlich nachgezogener Hashes scheitern.

## Offene Prüfung

Bei jeder relevanten Änderung frischen Checkout mit unverändertem Prüfvertrag qualifizieren und neue Evidenzrevision festhalten. Neue Fälle oder größere Korpora benötigen eigene Erwartungen und Fehlerkontrollen; andere Plattformen sind separat zu qualifizieren.

Evidenzberichte behalten ihre eigenen Prüfrevisionen. Keine neue Ausführung, externe Begutachtung oder physische Qualifikation durch diese Darstellung.
