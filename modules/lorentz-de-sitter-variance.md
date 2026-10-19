# Eigenzeit: analytische Wolkenvarianz und Bennett-Intervalle

Registerstand: 2026-10-19. MAIN / SOFTWARE. Kein Live-Prüfsiegel.

## Quelle

Branch: main

Commit: aa2c3dae7bb7afb564cdf4f08b0fe8f2c64c9bfb

[Originaldokumentation](https://github.com/thomasmgfeller/x6-spectral-astrolabium/blob/aa2c3dae7bb7afb564cdf4f08b0fe8f2c64c9bfb/research/lorentz_de_sitter_variance/README.md)

## Dokumentierte Aussage

Analytische Varianzgrenze vollständiger C2-Wolken im bekannten uniformen 4D-de-Sitter-Modell, 0≤h≤0,5. Bennett-Inversion erhält mindestens 95% Überdeckung bei festem Budget; hinreichende Budgets sinken gegenüber KL um Faktor 2,89–4,10. 45.056 neue Wolken: bei h=0,5, M=4.096 qualifizieren fünf von acht Bennett-Intervallen für 20%-Präzision, gegenüber null von acht mit KL. Ein kleines Gruppenintervall ist breiter; keine allgemeine Dominanz oder unbekannte Dichteidentifikation.

- [research/lorentz_de_sitter_variance/DERIVATION.md](https://github.com/thomasmgfeller/x6-spectral-astrolabium/blob/aa2c3dae7bb7afb564cdf4f08b0fe8f2c64c9bfb/research/lorentz_de_sitter_variance/DERIVATION.md): Überlappende Paare, exakte Lorentz-Momente, uniforme Reihenreste und Zellgrenzen sowie vollständiges Bennett-MGF-Argument.
- [research/lorentz_de_sitter_variance/RESULTS.md](https://github.com/thomasmgfeller/x6-spectral-astrolabium/blob/aa2c3dae7bb7afb564cdf4f08b0fe8f2c64c9bfb/research/lorentz_de_sitter_variance/RESULTS.md): Alle drei Budgetgewinne, neue Gruppen, erhaltenes Gegenbeispiel zur Intervall-Dominanz und Geltungsgrenzen.
- [research/lorentz_de_sitter_variance/REVIEW.md](https://github.com/thomasmgfeller/x6-spectral-astrolabium/blob/aa2c3dae7bb7afb564cdf4f08b0fe8f2c64c9bfb/research/lorentz_de_sitter_variance/REVIEW.md): Prüfpaket mit entscheidenden Beweisstellen, Falsifikationsmöglichkeiten und Reproduktionsbefehlen; externe Prüfung offen.
- [research/lorentz_de_sitter_variance/contract.json](https://github.com/thomasmgfeller/x6-spectral-astrolabium/blob/aa2c3dae7bb7afb564cdf4f08b0fe8f2c64c9bfb/research/lorentz_de_sitter_variance/contract.json): Öffentliche Fixierung b519337 vor Zielbudgetvergleich und neuen Punktwolken.
- [research/lorentz_de_sitter_variance/results/mathematics.json](https://github.com/thomasmgfeller/x6-spectral-astrolabium/blob/aa2c3dae7bb7afb564cdf4f08b0fe8f2c64c9bfb/research/lorentz_de_sitter_variance/results/mathematics.json): Exakte Dreipunktkoeffizienten und Varianzobergrenzen auf 64 vollständigen Parameterzellen.
- [research/lorentz_de_sitter_variance/VERIFICATION.json](https://github.com/thomasmgfeller/x6-spectral-astrolabium/blob/aa2c3dae7bb7afb564cdf4f08b0fe8f2c64c9bfb/research/lorentz_de_sitter_variance/VERIFICATION.json): Getrennte Kugelschnitt-Quadratur, 22 Moment-/Profilkontrollen, 200-stellige Bennett-Gegenrechnung und voller Replay.

## Reproduzieren

Python 3.12, gepinnte NumPy-/SciPy-/SymPy-/mpmath-/Matplotlib-Versionen und vollständige Git-Historie. POSIX-Ziellauf: 600 Sekunden und 2 GiB. Vollständiger Replay benötigt mehrere Minuten.

Neue Arbeits- und Ausgabeordner verwenden; Voraussetzungen aus der Originaldokumentation beachten.

```sh
git clone --branch main https://github.com/thomasmgfeller/x6-spectral-astrolabium.git x6-lorentz-de-sitter-variance
cd x6-lorentz-de-sitter-variance
git checkout --detach aa2c3dae7bb7afb564cdf4f08b0fe8f2c64c9bfb
python3 -m pip install -r research/lorentz_de_sitter_variance/requirements.txt
python3 -B research/lorentz_de_sitter_variance/verify.py
```

Erwartete Ausgabe: PASS_FULL_VARIANCE_REPLAY: rationale Varianzgrenze, getrennte Kugelschnitt-Geometrie, symbolische Momente, exakte Negativkontrollen und vollständiger Replay von 45.056 neuen Wolken.

## Offene Prüfung

Externe Prüfung und Replikation anhand des Prüfpakets; anschliessend den Einfluss begrenzter Dichte- und Zeitskalenfehler auf Identifizierbarkeit und Präzisionsfreigabe vorab festgelegt untersuchen. Keine allgemeinen Uhr- oder Stoppzeitbehauptungen.

Evidenzberichte behalten ihre eigenen Prüfrevisionen. Keine neue Ausführung, externe Begutachtung oder physische Qualifikation durch diese Darstellung.
