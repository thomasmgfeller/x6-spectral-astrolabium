# Lorentz: vier n=6-Restpaare und Grenzen der Gradseparatoren

Registerstand: 2026-10-18. MAIN / SOFTWARE. Kein Live-Prüfsiegel.

## Quelle

Branch: main

Commit: e5840afa7c7865a48766d1a5366210508a7b1f05

[Originaldokumentation](https://github.com/thomasmgfeller/x6-spectral-astrolabium/blob/e5840afa7c7865a48766d1a5366210508a7b1f05/research/lorentz_n6_residuals/README.md)

## Dokumentierte Aussage

Alle vier F0-Restpaare des vollständigen n=6-Atlas werden durch gepaarte gerichtete Grade D und bereits durch W_future getrennt. Drei sind Dualpaare. F0+W_future: 318/318 Klassen bei n=6, aber 163/164 für n=7 mit Höhe ≤2; beide Zählgrößen ergeben dort 164. Ein verbundenes n=8-Dualpaar kollidiert sogar für F0+D. Keine allgemeine Vollständigkeit oder physische Validierung.

- [research/lorentz_n6_residuals/evidence/local-results.json](https://github.com/thomasmgfeller/x6-spectral-astrolabium/blob/e5840afa7c7865a48766d1a5366210508a7b1f05/research/lorentz_n6_residuals/evidence/local-results.json): Vollständige Paarwerte, unabhängig nachgerechnete 318 Atlasfälle, Höhe-zwei-n=7-Enumeration, zwei explizite Grenzpaare und 17 Fehlerkontrollen.
- [research/lorentz_n6_residuals/evidence/wolfram-result.json](https://github.com/thomasmgfeller/x6-spectral-astrolabium/blob/e5840afa7c7865a48766d1a5366210508a7b1f05/research/lorentz_n6_residuals/evidence/wolfram-result.json): Wolfram 15.0.1: zwölf Matrizen, 36 exakt übereinstimmende monische Polynome, Grade, Zählgrößen, Isomorphie-/Dualitätsprüfungen. Zwei frühere fehlgeschlagene Versuche bleiben erhalten.
- [research/lorentz_n6_residuals/contract.json](https://github.com/thomasmgfeller/x6-spectral-astrolabium/blob/e5840afa7c7865a48766d1a5366210508a7b1f05/research/lorentz_n6_residuals/contract.json): Fixierte Konventionen und Auswahl, Herkunft des bestehenden Separators, Literaturabgrenzung und Hypothese H7-bidirectional-moments.
- [research/lorentz_n6_residuals/ACCEPTANCE.md](https://github.com/thomasmgfeller/x6-spectral-astrolabium/blob/e5840afa7c7865a48766d1a5366210508a7b1f05/research/lorentz_n6_residuals/ACCEPTANCE.md): Frischer Checkout und Netzwerk-isolierte CI erfolgreich, identisches Neun-Berichte-Bundle; zusätzliche CLI-Manipulationen auch unter Python -O abgelehnt.

## Reproduzieren

Python 3.12, nur Standardbibliothek. Für die gemeinsame Offline-Suite zusätzlich Node.js 24. Kein Wolfram-Zugang oder Netzwerk beim Replay.

Neue Arbeits- und Ausgabeordner verwenden; Voraussetzungen aus der Originaldokumentation beachten.

```sh
git clone --branch main https://github.com/thomasmgfeller/x6-spectral-astrolabium.git x6-lorentz-n6-residuals
cd x6-lorentz-n6-residuals
git checkout --detach e5840afa7c7865a48766d1a5366210508a7b1f05
python3 -S -B research/lorentz_n6_residuals/verify.py --output /tmp/lorentz-residuals.json
python3 -S -B research/lorentz_n6_residuals/verify.py --verify-report /tmp/lorentz-residuals.json
```

Erwartete Ausgabe: Exit 0, PASS_WITH_SCOPE_LIMITS; 4 getrennte / 0 ungelöste Primärpaare, 36 Wolfram-Polynome, 17 abgelehnte Fehlerkontrollen. Fehlende/manipulierte Ausgabe: Exit 1.

## Offene Prüfung

Die vollständige n=7-Abnahme ist im Modul lorentz-n7-complete abgeschlossen: H7-bidirectional-moments ist durch zwei Restpaare widerlegt. Nächster Schritt: strukturelle Erklärung der minimalen Kollisionen und unabhängige externe Replikation; neue Aussagen müssen eigene Voraussetzungen nennen.

Evidenzberichte behalten ihre eigenen Prüfrevisionen. Keine neue Ausführung, externe Begutachtung oder physische Qualifikation durch diese Darstellung.
