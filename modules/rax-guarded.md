# RAX-G1: deklarativer Runner und Fehlerbudget

Registerstand: 2026-10-17. MAIN / SOFTWARE. Kein Live-Prüfsiegel.

## Quelle

Branch: main

Commit: ced51c97b03525acc5d9ff907e175afce740974a

[Originaldokumentation](https://github.com/thomasmgfeller/x6-spectral-astrolabium/blob/ced51c97b03525acc5d9ff907e175afce740974a/docs/validation-v1/README.md)

## Dokumentierte Aussage

Konkrete M1-Zugriffswege im begrenzten Planerformat geschlossen: nur öffentliche Modell-/Präfixdaten, frische Worker, kein Callback, vollständige Index-/Zellprüfung, phasengebundener Holdout und exakter Replay. Historische B1/M1-Archive und Ergebnisse unverändert. Keine allgemeine Python-Sandbox oder externe Blindheit.

- [docs/validation-v1/evidence/guarded/qualification.json](https://github.com/thomasmgfeller/x6-spectral-astrolabium/blob/ced51c97b03525acc5d9ff907e175afce740974a/docs/validation-v1/evidence/guarded/qualification.json): Ausgeführte 33 Negativkontrollen, wirksame Datenmutationen und unabhängige exakte Vorhersage 13/24.
- [docs/validation-v1/ERROR_BUDGET.json](https://github.com/thomasmgfeller/x6-spectral-astrolabium/blob/ced51c97b03525acc5d9ff907e175afce740974a/docs/validation-v1/ERROR_BUDGET.json): Nulltoleranz im zugelassenen Profil; menschliche Blindheit, allgemeine Sandbox und externe Wiederholung offen.

## Reproduzieren

Python 3.12, Standardbibliothek; neue Ausgabeverzeichnisse. Nur geprüftes deklaratives JSON, kein beliebiger fremder Python-Code.

Neue Arbeits- und Ausgabeordner verwenden; Voraussetzungen aus der Originaldokumentation beachten.

```sh
git clone --branch main https://github.com/thomasmgfeller/x6-spectral-astrolabium.git x6-rax-guarded
cd x6-rax-guarded
git checkout --detach ced51c97b03525acc5d9ff907e175afce740974a
python3 -S -B tests/rax-guarded/qualify.py --output /tmp/register-rax-g1
python3 -S -B experimental/rax_guarded/runner.py verify /tmp/register-rax-g1/run
python3 -S -B tests/rax-guarded/check_budget.py --qualification /tmp/register-rax-g1/qualification.json
```

Erwartete Ausgabe: PASS mit 33 erwarteten Zurückweisungen; PASS_GUARDED_REPLAY mit 18 Zellen. Keine angenommene unzulässige Fähigkeit oder Ergebnisfälschung erlaubt.

## Offene Prüfung

Eine außenstehende Person führt den eingefrorenen Umfang aus und dokumentiert Rolle, Runtime, vollständige Ergebnisse und Abweichungen. Fremder ausführbarer Code benötigt eigene Betriebssystem-Isolationsabnahme.

Evidenzberichte behalten ihre eigenen Prüfrevisionen. Keine neue Ausführung, externe Begutachtung oder physische Qualifikation durch diese Darstellung.
