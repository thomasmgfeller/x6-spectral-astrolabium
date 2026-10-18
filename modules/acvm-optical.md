# ACVM 0.2: optischer Referenzablauf

Registerstand: 2026-10-18. MAIN / SOFTWARE. Kein Live-Prüfsiegel.

## Quelle

Branch: main

Commit: 01430ce5f0a648ad63d611a451f0d0fd7ccb16aa

[Originaldokumentation](https://github.com/thomasmgfeller/x6-spectral-astrolabium/blob/01430ce5f0a648ad63d611a451f0d0fd7ccb16aa/docs/acvm/optical-v0.2/README.md)

## Dokumentierte Aussage

V01–V08 MODEL_PASS, synthetische QHQ-/Drift-/Regelkontrollen; ELL14-/PM100D-Adapter sind implementiert, nicht gerätequalifiziert.

- [docs/acvm/optical-v0.2/evidence/fresh-checkout/fresh-checkout.json](https://github.com/thomasmgfeller/x6-spectral-astrolabium/blob/01430ce5f0a648ad63d611a451f0d0fd7ccb16aa/docs/acvm/optical-v0.2/evidence/fresh-checkout/fresh-checkout.json): 12 Checkout-Schritte; genaue geprüfte lokale Revision und Logs.
- [docs/acvm/optical-v0.2/VALIDATION.md](https://github.com/thomasmgfeller/x6-spectral-astrolabium/blob/01430ce5f0a648ad63d611a451f0d0fd7ccb16aa/docs/acvm/optical-v0.2/VALIDATION.md): V09/V10 physisch NOT_PERFORMED; Regelvorteil nur im angegebenen Modell.

## Reproduzieren

Python 3.12, POSIX-PTY, g++; Softwarelauf ohne Geräte.

Neue Arbeits- und Ausgabeordner verwenden; Voraussetzungen aus der Originaldokumentation beachten.

```sh
git clone --branch main https://github.com/thomasmgfeller/x6-spectral-astrolabium.git x6-acvm-optical
cd x6-acvm-optical
git checkout --detach 01430ce5f0a648ad63d611a451f0d0fd7ccb16aa
python3 x6.py acvm qualify --output runs/register-acvm
```

Erwartete Ausgabe: Exit 0; nur die unten genannte Softwareaussage.

## Offene Prüfung

V09/V10 mit unabhängigen Messungen; Geräteidentität/Kalibrierung, reale Hysterese/Laufzeiten und geschlossenen optischen Regelkreis nachweisen.

Evidenzberichte behalten ihre eigenen Prüfrevisionen. Keine neue Ausführung, externe Begutachtung oder physische Qualifikation durch diese Darstellung.
