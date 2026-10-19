# Eigenzeit: schärfere KL-Krümmungsintervalle

Registerstand: 2026-10-19. MAIN / SOFTWARE. Kein Live-Prüfsiegel.

## Quelle

Branch: main

Commit: d6c9f3d9ddf975cdc6f0c2ce055c5becb1f7a2ee

[Originaldokumentation](https://github.com/thomasmgfeller/x6-spectral-astrolabium/blob/d6c9f3d9ddf975cdc6f0c2ce055c5becb1f7a2ee/research/lorentz_de_sitter_kl/README.md)

## Dokumentierte Aussage

Bernoulli-KL-Schranke für abhängige C2-U-Statistiken: mindestens 95% Überdeckung im bekannten uniformen 4D-de-Sitter-Modell bei festem Budget und 0≤h≤0,5. Hinreichende Budgets sinken gegenüber der Hoeffding-Regel um Faktor 2,71–2,77. 77.824 neue Wolken; bei h=0,5 und M=16.384 qualifizieren vier von vier KL-Intervallen für 20%-Präzision, gegenüber einem von vier mit Hoeffding. Keine präzise Erfolgsratenschätzung, allgemeine Uhr oder Dichteidentifikation.

- [research/lorentz_de_sitter_kl/DERIVATION.md](https://github.com/thomasmgfeller/x6-spectral-astrolabium/blob/d6c9f3d9ddf975cdc6f0c2ce055c5becb1f7a2ee/research/lorentz_de_sitter_kl/DERIVATION.md): Binärer Chernoff-Nachweis mit disjunkter Paarreduktion, rationale KL-Umkehrung und Intervallverschachtelung.
- [research/lorentz_de_sitter_kl/RESULTS.md](https://github.com/thomasmgfeller/x6-spectral-astrolabium/blob/d6c9f3d9ddf975cdc6f0c2ce055c5becb1f7a2ee/research/lorentz_de_sitter_kl/RESULTS.md): Verfeinerte hinreichende Budgets, alle frischen Gruppen, Präzisionsverweigerungen und Geltungsgrenzen.
- [research/lorentz_de_sitter_kl/contract.json](https://github.com/thomasmgfeller/x6-spectral-astrolabium/blob/d6c9f3d9ddf975cdc6f0c2ce055c5becb1f7a2ee/research/lorentz_de_sitter_kl/contract.json): Öffentliche Quellenfixierung 09e0cf0 vor Zielbudgetvergleich und 77.824 neuen Wolken.
- [research/lorentz_de_sitter_kl/results/planning.json](https://github.com/thomasmgfeller/x6-spectral-astrolabium/blob/d6c9f3d9ddf975cdc6f0c2ce055c5becb1f7a2ee/research/lorentz_de_sitter_kl/results/planning.json): Exakte Bruchzertifikate an allen sechs ganzzahligen Budgetgrenzen und unmittelbaren Vorgängerwerten.
- [research/lorentz_de_sitter_kl/VERIFICATION.json](https://github.com/thomasmgfeller/x6-spectral-astrolabium/blob/d6c9f3d9ddf975cdc6f0c2ce055c5becb1f7a2ee/research/lorentz_de_sitter_kl/VERIFICATION.json): Vollständiger Replay mit getrenntem Kausalitätstest, unabhängiger Hochpräzisionsrechnung und exakten endlichen Kontrollen.

## Reproduzieren

Python 3.12, gepinnte NumPy-/SciPy-/mpmath-/Matplotlib-Versionen und vollständige Git-Historie. POSIX-Ziellauf: 600 Sekunden und 2 GiB; vollständiger Replay benötigt mehrere Minuten.

Neue Arbeits- und Ausgabeordner verwenden; Voraussetzungen aus der Originaldokumentation beachten.

```sh
git clone --branch main https://github.com/thomasmgfeller/x6-spectral-astrolabium.git x6-lorentz-de-sitter-kl
cd x6-lorentz-de-sitter-kl
git checkout --detach d6c9f3d9ddf975cdc6f0c2ce055c5becb1f7a2ee
python3 -m pip install -r research/lorentz_de_sitter_kl/requirements.txt
python3 -B research/lorentz_de_sitter_kl/verify.py
```

Erwartete Ausgabe: PASS_FULL_KL_REPLAY: rationale KL-Gegenprüfung, exakte abhängige Kontrollen, 77.824 reproduzierte Punktwolken, sämtliche Intervall- und Budgetentscheide.

## Offene Prüfung

Der vorab fixierte Varianz-/Bennett-Vergleich liegt im Nachfolgemodul lorentz-de-sitter-variance vor: 2,89–4,10-fach kleinere hinreichende Budgets. Diese KL-Referenz bleibt unverändert; externe Prüfung und Dichte-/Zeitskalensensitivität stehen aus.

Evidenzberichte behalten ihre eigenen Prüfrevisionen. Keine neue Ausführung, externe Begutachtung oder physische Qualifikation durch diese Darstellung.
