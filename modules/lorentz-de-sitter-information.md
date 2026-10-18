# Eigenzeit: de-Sitter-Informationsplanung

Registerstand: 2026-10-18. MAIN / SOFTWARE. Kein Live-Prüfsiegel.

## Quelle

Branch: main

Commit: e947dfbdd49890dcb119940548537d1db59272c2

[Originaldokumentation](https://github.com/thomasmgfeller/x6-spectral-astrolabium/blob/e947dfbdd49890dcb119940548537d1db59272c2/research/lorentz_de_sitter_information/README.md)

## Dokumentierte Aussage

Kovarianzbewusste Einparameter-Planung aus öffentlichen Pilotdaten, danach 16.384 neue unabhängige Wolken nach Quellenfixierung. Im Hauptvergleich senkt GLS234 den RMSE gegenüber C2 um 1,37%; das vorab gesetzte 10%-Ziel wird verfehlt. Bei schwacher Krümmung bleibt der approximative Datenbedarf hoch. Keine Freigabe von Krümmungsintervallen.

- [research/lorentz_de_sitter_information/RESULTS.md](https://github.com/thomasmgfeller/x6-spectral-astrolabium/blob/e947dfbdd49890dcb119940548537d1db59272c2/research/lorentz_de_sitter_information/RESULTS.md): Hauptvergleich, approximative Budgets, negatives 10%-Gate und nächste Entscheidung.
- [research/lorentz_de_sitter_information/contract.json](https://github.com/thomasmgfeller/x6-spectral-astrolabium/blob/e947dfbdd49890dcb119940548537d1db59272c2/research/lorentz_de_sitter_information/contract.json): Öffentlicher Prüfvertrag vor dem frischen Test; Pilotplanung ist deskriptiv.
- [research/lorentz_de_sitter_information/results/summary.json](https://github.com/thomasmgfeller/x6-spectral-astrolabium/blob/e947dfbdd49890dcb119940548537d1db59272c2/research/lorentz_de_sitter_information/results/summary.json): Alle zwölf frischen Ergebniszeilen und gepaarter Bootstrapvergleich.
- [research/lorentz_de_sitter_information/results/hashes.json](https://github.com/thomasmgfeller/x6-spectral-astrolabium/blob/e947dfbdd49890dcb119940548537d1db59272c2/research/lorentz_de_sitter_information/results/hashes.json): Prüfsummen aller Originalausgaben, einschliesslich vollständiger Kettenmerkmale und Relationshashes.
- [research/lorentz_de_sitter_information/VERIFICATION.json](https://github.com/thomasmgfeller/x6-spectral-astrolabium/blob/e947dfbdd49890dcb119940548537d1db59272c2/research/lorentz_de_sitter_information/VERIFICATION.json): Vollständiger interner Replay und getrennte Kausalitäts-, Ketten-, Gewichts- und Momentprüfungen.

## Reproduzieren

Python 3.12, gepinnte NumPy-/SciPy-/Matplotlib-Versionen, vollständige Git-Historie. POSIX-Ziellauf begrenzt auf 600 Sekunden und 2 GiB.

Neue Arbeits- und Ausgabeordner verwenden; Voraussetzungen aus der Originaldokumentation beachten.

```sh
git clone --branch main https://github.com/thomasmgfeller/x6-spectral-astrolabium.git x6-lorentz-de-sitter-information
cd x6-lorentz-de-sitter-information
git checkout --detach e947dfbdd49890dcb119940548537d1db59272c2
python3 -m pip install -r research/lorentz_de_sitter_information/requirements.txt
python3 -B research/lorentz_de_sitter_information/verify.py
```

Erwartete Ausgabe: PASS_FULL_INFORMATION_REPLAY, 16.384 vollständig reproduzierte Punktwolken; interne Softwaregegenprüfung.

## Offene Prüfung

Konservative C2-Konfidenzinversion ist im getrennten Modul lorentz-de-sitter-c2 umgesetzt. Nächste Stufe: eine schärfere endlich gültige Schranke unter korrekter Paarabhängigkeit; externe Replikation und Dichtebegründung bleiben offen.

Evidenzberichte behalten ihre eigenen Prüfrevisionen. Keine neue Ausführung, externe Begutachtung oder physische Qualifikation durch diese Darstellung.
