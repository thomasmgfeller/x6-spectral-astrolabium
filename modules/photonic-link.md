# Photonic Link Validation Lab

Registerstand: 2026-10-18. BRANCH_ONLY / SOFTWARE. Kein Live-Prüfsiegel.

## Quelle

Branch: research/photonic-link

Commit: 7ff72fcd6a16e9b353d1af277307463f757d3470

[Originaldokumentation](https://github.com/thomasmgfeller/x6-spectral-astrolabium/blob/7ff72fcd6a16e9b353d1af277307463f757d3470/research/photonic-link/README.md)

## Dokumentierte Aussage

Gemeinsames synthetisches Verlust-, Polarisationsdrift- und Zeitmodell; affine Uhrkalibrierung mit getrennten Modellpulsen.

- [research/photonic-link/evidence/validation.json](https://github.com/thomasmgfeller/x6-spectral-astrolabium/blob/7ff72fcd6a16e9b353d1af277307463f757d3470/research/photonic-link/evidence/validation.json): Gespeicherte Validierung; optionale RTL-Tests separat gekennzeichnet.
- [research/photonic-link/evidence/experiments.json](https://github.com/thomasmgfeller/x6-spectral-astrolabium/blob/7ff72fcd6a16e9b353d1af277307463f757d3470/research/photonic-link/evidence/experiments.json): Synthetische Szenarien mit Fehlfällen; kein gemessener Photonenlink.

## Reproduzieren

Python 3.12/venv und requirements; GHDL optional für zusätzliche RTL-Prüfung.

Neue Arbeits- und Ausgabeordner verwenden; Voraussetzungen aus der Originaldokumentation beachten.

```sh
git clone --branch research/photonic-link https://github.com/thomasmgfeller/x6-spectral-astrolabium.git x6-photonic-link
cd x6-photonic-link
git checkout --detach 7ff72fcd6a16e9b353d1af277307463f757d3470
cd research/photonic-link
python3 -m pip install -r requirements.txt
python3 validate.py --output /tmp/register-plvl-validation.json
python3 experiments.py --output /tmp/register-plvl-experiments.json
```

Erwartete Ausgabe: Exit 0; nur die unten genannte Softwareaussage.

## Offene Prüfung

Modellparameter/Identifizierbarkeit mit realen Zeitstempeln, Verlust- und Driftmessungen prüfen; Fehlerbudget und unabhängige Kalibrierreferenz.

Evidenzberichte behalten ihre eigenen Prüfrevisionen. Keine neue Ausführung, externe Begutachtung oder physische Qualifikation durch diese Darstellung.
