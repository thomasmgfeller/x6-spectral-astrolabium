# Photonischer Zwei-Qubit-Aufbau und Jig

Registerstand: 2026-10-19. MAIN / SOFTWARE. Kein Live-Prüfsiegel.

## Quelle

Branch: main

Commit: 26432e3d4cde20adabb510f17d5639891f4ac642

[Originaldokumentation](https://github.com/thomasmgfeller/x6-spectral-astrolabium/blob/26432e3d4cde20adabb510f17d5639891f4ac642/experiments/photonic-two-qubit/REPRODUCE.md)

## Dokumentierte Aussage

Host-/RTL-Referenz und idealisierte Jig-Geometrie werden geprüft. Ausgelassene optionale Prüfungen sind NOT_EXECUTED.

- [experiments/photonic-two-qubit/SCIENTIFIC_STATUS.md](https://github.com/thomasmgfeller/x6-spectral-astrolabium/blob/26432e3d4cde20adabb510f17d5639891f4ac642/experiments/photonic-two-qubit/SCIENTIFIC_STATUS.md): Designstatus und Grenzen; physische Fertigungs-/Verschränkungsnachweise offen.
- [experiments/photonic-two-qubit/reference/sagnac_v0_7/VALIDATION.md](https://github.com/thomasmgfeller/x6-spectral-astrolabium/blob/26432e3d4cde20adabb510f17d5639891f4ac642/experiments/photonic-two-qubit/reference/sagnac_v0_7/VALIDATION.md): Erhaltener digitaler Referenzbericht.

## Reproduzieren

Python 3.12, GHDL 5.0.1 mcode und CAD-Abhängigkeiten aus requirements; keine Hardware nötig.

Neue Arbeits- und Ausgabeordner verwenden; Voraussetzungen aus der Originaldokumentation beachten.

```sh
git clone --branch main https://github.com/thomasmgfeller/x6-spectral-astrolabium.git x6-photonic-design
cd x6-photonic-design
git checkout --detach 26432e3d4cde20adabb510f17d5639891f4ac642
python3 -m pip install -r tests/photonics/requirements.txt
python3 tests/photonics/validate_release.py --ghdl --cad --output runs/register-photonic
```

Erwartete Ausgabe: Exit 0; nur die unten genannte Softwareaussage.

## Offene Prüfung

Jig fertigen und vermessen; Quelle/Detektoren kalibrieren; vorregistrierte Koinzidenz-/Verschränkungsprüfung nach LAB_PROTOCOL.

Evidenzberichte behalten ihre eigenen Prüfrevisionen. Keine neue Ausführung, externe Begutachtung oder physische Qualifikation durch diese Darstellung.
