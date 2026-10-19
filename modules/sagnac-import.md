# Sagnac-Aufnahme und Import

Registerstand: 2026-10-19. MAIN / SOFTWARE. Kein Live-Prüfsiegel.

## Quelle

Branch: main

Commit: 694dd9ec0409f35c9c6fd3e835ef187ada72c598

[Originaldokumentation](https://github.com/thomasmgfeller/x6-spectral-astrolabium/blob/694dd9ec0409f35c9c6fd3e835ef187ada72c598/docs/SAGNAC_INTEGRATION.md)

## Dokumentierte Aussage

SGNCv007-Decoder, synthetischer Import und Loopback-Bridge; optische Stellbefehle gehören zum separaten ACVM-Modul.

- [evidence/sagnac_integration_validation.json](https://github.com/thomasmgfeller/x6-spectral-astrolabium/blob/694dd9ec0409f35c9c6fd3e835ef187ada72c598/evidence/sagnac_integration_validation.json): Gespeicherte Softwarevalidierung des Integrationsstands; keine Hardwaremessung.

## Reproduzieren

Python 3.12, Browser; Standardstart ohne angeschlossenes Gerät.

Neue Arbeits- und Ausgabeordner verwenden; Voraussetzungen aus der Originaldokumentation beachten.

```sh
git clone --branch main https://github.com/thomasmgfeller/x6-spectral-astrolabium.git x6-sagnac-import
cd x6-sagnac-import
git checkout --detach 694dd9ec0409f35c9c6fd3e835ef187ada72c598
python3 device/sagnac_bridge.py
```

Erwartete Ausgabe: http://127.0.0.1:8766/app/; Tab 07 Sagnac, synthetisches Beispiel. Server endet mit Strg+C.

## Offene Prüfung

Reale serielle Aufnahme und Zähler-/Zeitkalibrierung mit unabhängiger Referenz; optische Claims separat prüfen.

Evidenzberichte behalten ihre eigenen Prüfrevisionen. Keine neue Ausführung, externe Begutachtung oder physische Qualifikation durch diese Darstellung.
