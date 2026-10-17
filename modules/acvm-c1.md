# ACVM C1: Steuerkanal

Registerstand: 2026-10-17. MAIN / SOFTWARE. Kein Live-Prüfsiegel.

## Quelle

Branch: main

Commit: 389cb3f688dfbc9d90086bb55c1b5d199b7e9c58

[Originaldokumentation](https://github.com/thomasmgfeller/x6-spectral-astrolabium/blob/389cb3f688dfbc9d90086bb55c1b5d199b7e9c58/docs/acvm/control-channel-v0.1/README.md)

## Dokumentierte Aussage

Host-Protokoll, Compiler, portabler C++-Sequencer und virtueller serieller Weg sind prüfbar. Unveränderte Firmware wurde für RP2040 gebaut; wiederholte Builds ergeben identische UF2-/BIN-Hashes. Keine physische Ausgabe oder Fehlerreaktion gemessen.

- [docs/acvm/control-channel-v0.1/evidence/qualification.json](https://github.com/thomasmgfeller/x6-spectral-astrolabium/blob/389cb3f688dfbc9d90086bb55c1b5d199b7e9c58/docs/acvm/control-channel-v0.1/evidence/qualification.json): Gespeicherte Softwarequalifikation; kein Pico-Build oder elektrischer Messbeleg.
- [docs/acvm/c1-e01-target-build/evidence/build-report.json](https://github.com/thomasmgfeller/x6-spectral-astrolabium/blob/389cb3f688dfbc9d90086bb55c1b5d199b7e9c58/docs/acvm/c1-e01-target-build/evidence/build-report.json): Tatsächlicher RP2040-Zielbuild PASS; Pico SDK 2.3.1/GNU Arm GCC 15.2.1, Firmware-, Werkzeug- und Ausgabehashes. UF2/BIN/ELF und Buildlogs archiviert; kein Flash- oder Messbeleg.
- [docs/acvm/c1-e01-target-build/evidence/readiness.json](https://github.com/thomasmgfeller/x6-spectral-astrolabium/blob/389cb3f688dfbc9d90086bb55c1b5d199b7e9c58/docs/acvm/c1-e01-target-build/evidence/readiness.json): BLOCKED_PHYSICAL_MEASUREMENT: 0/10 Normalläufe und 0/6 Fehlerfälle; reale Geräte, Kalibrierung, vorher fixiertes Messprofil und unabhängige Rohaufnahmen fehlen.

## Reproduzieren

Softwarequalifikation: Python 3.12, POSIX-PTY, g++/C++17; kein Pico erforderlich. Optionaler Zielbuild: Linux x86-64 und gepinnte Werkzeuge gemäß docs/acvm/c1-e01-target-build/README.md. Physische E01-Abnahme benötigt einen identifizierten Pico/MCP4921-Aufbau und unabhängige kalibrierte Messgeräte.

Neue Arbeits- und Ausgabeordner verwenden; Voraussetzungen aus der Originaldokumentation beachten.

```sh
git clone --branch main https://github.com/thomasmgfeller/x6-spectral-astrolabium.git x6-acvm-c1
cd x6-acvm-c1
git checkout --detach 389cb3f688dfbc9d90086bb55c1b5d199b7e9c58
python3 x6.py control qualify --output runs/register-c1
python3 -B tests/control-channel/test_pico_build.py
```

Erwartete Ausgabe: Softwarequalifikation Exit 0; UF2-Kandidat stimmt mit BIN überein, fünf Beschädigungsfälle werden abgelehnt und vorhandene Ergebnisordner bleiben geschützt. Der dokumentierte Zielbuild ergibt TARGET_BUILD_PASS; elektrische Abnahme bleibt NOT_PERFORMED.

## Offene Prüfung

Identifizierten Aufbau flashen; E01-Messprofil vor Datenerhebung fixieren; mindestens zehn Stellfolgen sowie sechs Fehlerfälle unabhängig erfassen. Spannungsfehler plus U95 ≤25 mV, Zeitfehler plus U95 ≤20 ms, Hostverlustreaktion plus U95 ≤550 ms gemäß E01. Vollständige Rohdaten, Kalibrierung und Fehlergrenzen archivieren; anschließend erst elektrische und später optische Abnahme entscheiden.

Evidenzberichte behalten ihre eigenen Prüfrevisionen. Keine neue Ausführung, externe Begutachtung oder physische Qualifikation durch diese Darstellung.
