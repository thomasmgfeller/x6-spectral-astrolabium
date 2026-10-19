# Sagnac-Aufnahme und Import

Registerstand: 2026-10-19. MAIN / SOFTWARE. Kein Live-Prüfsiegel.

## Quelle

Branch: main

Commit: aa2c3dae7bb7afb564cdf4f08b0fe8f2c64c9bfb

[Originaldokumentation](https://github.com/thomasmgfeller/x6-spectral-astrolabium/blob/aa2c3dae7bb7afb564cdf4f08b0fe8f2c64c9bfb/docs/SAGNAC_INTEGRATION.md)

## Dokumentierte Aussage

SGNCv007-Decoder, synthetischer Import und Loopback-Bridge; optische Stellbefehle gehören zum separaten ACVM-Modul.

- [evidence/sagnac_integration_validation.json](https://github.com/thomasmgfeller/x6-spectral-astrolabium/blob/aa2c3dae7bb7afb564cdf4f08b0fe8f2c64c9bfb/evidence/sagnac_integration_validation.json): Gespeicherte Softwarevalidierung des Integrationsstands; keine Hardwaremessung.

## Reproduzieren

Python 3.12, Browser; Standardstart ohne angeschlossenes Gerät.

Neue Arbeits- und Ausgabeordner verwenden; Voraussetzungen aus der Originaldokumentation beachten.

```sh
git clone --branch main https://github.com/thomasmgfeller/x6-spectral-astrolabium.git x6-sagnac-import
cd x6-sagnac-import
git checkout --detach aa2c3dae7bb7afb564cdf4f08b0fe8f2c64c9bfb
python3 device/sagnac_bridge.py
```

Erwartete Ausgabe: http://127.0.0.1:8766/app/; Tab 07 Sagnac, synthetisches Beispiel. Server endet mit Strg+C.

## Offene Prüfung

Reale serielle Aufnahme und Zähler-/Zeitkalibrierung mit unabhängiger Referenz; optische Claims separat prüfen.

Evidenzberichte behalten ihre eigenen Prüfrevisionen. Keine neue Ausführung, externe Begutachtung oder physische Qualifikation durch diese Darstellung.
