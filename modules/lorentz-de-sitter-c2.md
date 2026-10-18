# Eigenzeit: konservative C2-Krümmungsintervalle

Registerstand: 2026-10-18. MAIN / SOFTWARE. Kein Live-Prüfsiegel.

## Quelle

Branch: main

Commit: e947dfbdd49890dcb119940548537d1db59272c2

[Originaldokumentation](https://github.com/thomasmgfeller/x6-spectral-astrolabium/blob/e947dfbdd49890dcb119940548537d1db59272c2/research/lorentz_de_sitter_c2/README.md)

## Dokumentierte Aussage

Rational eingeschlossene C2-Vorwärtsfunktion und strenge Monotonie für bekannte uniforme 4D-de-Sitter-Modelle, 0≤h≤0,5. Eine Hoeffding-U-Statistik-Schranke liefert mindestens 95% Überdeckung bei festem Budget und unabhängigen Wolken. 16.384 neue Wolken: alle geprüften Intervalle enthalten die Modellwerte, keines erreicht 20%-Präzision. Keine allgemeine Uhr oder Identifikation bei unbekannter Dichte.

- [research/lorentz_de_sitter_c2/DERIVATION.md](https://github.com/thomasmgfeller/x6-spectral-astrolabium/blob/e947dfbdd49890dcb119940548537d1db59272c2/research/lorentz_de_sitter_c2/DERIVATION.md): Vollständige geometrische und statistische Herleitung, uniforme Restfehler, konservative Umkehrung und Geltungsbereich.
- [research/lorentz_de_sitter_c2/RESULTS.md](https://github.com/thomasmgfeller/x6-spectral-astrolabium/blob/e947dfbdd49890dcb119940548537d1db59272c2/research/lorentz_de_sitter_c2/RESULTS.md): Alle Präzisionsverweigerungen, hinreichende Budgetgrenzen und offener Effizienzschritt.
- [research/lorentz_de_sitter_c2/contract.json](https://github.com/thomasmgfeller/x6-spectral-astrolabium/blob/e947dfbdd49890dcb119940548537d1db59272c2/research/lorentz_de_sitter_c2/contract.json): Öffentliche Quellenfixierung c2f1659 vor Zielgitter und frischen Punktwolken.
- [research/lorentz_de_sitter_c2/results/mathematics.json](https://github.com/thomasmgfeller/x6-spectral-astrolabium/blob/e947dfbdd49890dcb119940548537d1db59272c2/research/lorentz_de_sitter_c2/results/mathematics.json): Exakte Bruchzertifikate, Reihenkoeffizienten und getrennte Quadraturkontrolle.
- [research/lorentz_de_sitter_c2/VERIFICATION.json](https://github.com/thomasmgfeller/x6-spectral-astrolabium/blob/e947dfbdd49890dcb119940548537d1db59272c2/research/lorentz_de_sitter_c2/VERIFICATION.json): Symbolische Integralgegenprüfung, abhängiger Paarkern als Negativkontrolle und vollständiger Replay.

## Reproduzieren

Python 3.12, gepinnte NumPy-/SciPy-/SymPy-/Matplotlib-Versionen und vollständige Git-Historie. POSIX-Ziellauf: 600 Sekunden und 2 GiB.

Neue Arbeits- und Ausgabeordner verwenden; Voraussetzungen aus der Originaldokumentation beachten.

```sh
git clone --branch main https://github.com/thomasmgfeller/x6-spectral-astrolabium.git x6-lorentz-de-sitter-c2
cd x6-lorentz-de-sitter-c2
git checkout --detach e947dfbdd49890dcb119940548537d1db59272c2
python3 -m pip install -r research/lorentz_de_sitter_c2/requirements.txt
python3 -B research/lorentz_de_sitter_c2/verify.py
```

Erwartete Ausgabe: PASS_FULL_C2_CONFIDENCE_REPLAY: exakte Integral- und Monotonieprüfungen, 16.384 reproduzierte Punktwolken, alle Intervall- und Budgetentscheide.

## Offene Prüfung

Der vorab fixierte KL-Vergleich liegt im Nachfolgemodul lorentz-de-sitter-kl vor: 2,71–2,77-fach kleinere hinreichende Budgets. Diese Hoeffding-Referenz bleibt unverändert; externe Beweisprüfung und Replikation stehen aus.

Evidenzberichte behalten ihre eigenen Prüfrevisionen. Keine neue Ausführung, externe Begutachtung oder physische Qualifikation durch diese Darstellung.
