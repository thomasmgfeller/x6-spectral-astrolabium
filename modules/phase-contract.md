# X6-Phasenfilter: Experimentvertrag

Registerstand: 2026-10-15. MAIN / SOFTWARE. Kein Live-Prüfsiegel.

## Quelle

Branch: main

Commit: a81e62fb077ef5e8fd7774682a400cbef6ed5aa1

[Originaldokumentation](https://github.com/thomasmgfeller/x6-spectral-astrolabium/blob/a81e62fb077ef5e8fd7774682a400cbef6ed5aa1/experiments/x6-phase-filter/README.md)

## Dokumentierte Aussage

Die Vorprüfung trennt einen strukturell gültigen Entwurf von einem ausführungsreifen Versuch; Filterclaim UNVALIDATED.

- [experiments/x6-phase-filter/contract-v0.2.0/validation_report.json](https://github.com/thomasmgfeller/x6-spectral-astrolabium/blob/a81e62fb077ef5e8fd7774682a400cbef6ed5aa1/experiments/x6-phase-filter/contract-v0.2.0/validation_report.json): 42 Softwaretests; keine neuen Filterversuche.

## Reproduzieren

Python 3.12, isolierte venv empfohlen; Abhängigkeiten aus Paket requirements.txt.

Neue Arbeits- und Ausgabeordner verwenden; Voraussetzungen aus der Originaldokumentation beachten.

```sh
git clone --branch main https://github.com/thomasmgfeller/x6-spectral-astrolabium.git x6-phase-contract
cd x6-phase-contract
git checkout --detach a81e62fb077ef5e8fd7774682a400cbef6ed5aa1
cd experiments/x6-phase-filter/contract-v0.2.0
python3 -m pip install -r requirements.txt
python3 preflight.py X6_PF_Experiment_Contract_v0_2_DRAFT.json --mode draft
python3 preflight.py X6_PF_Experiment_Contract_v0_2_DRAFT.json --mode preflight
```

Erwartete Ausgabe: draft: DRAFT_STRUCTURE_VALID/Exit 0; preflight: BLOCKED/Exit 2 ist hier erwartet.

## Offene Prüfung

Offene fachliche Festlegungen und vertrauenswürdigen Freeze schliessen; danach Runner-Review.

Evidenzberichte behalten ihre eigenen Prüfrevisionen. Keine neue Ausführung, externe Begutachtung oder physische Qualifikation durch diese Darstellung.
