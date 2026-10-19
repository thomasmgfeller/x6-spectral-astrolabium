# Evidence & Calibration

Registerstand: 2026-10-19. MAIN / SOFTWARE. Kein Live-Prüfsiegel.

## Quelle

Branch: main

Commit: 4a6fe9c383e56b5a26f286fba6aa6d8c9263308a

[Originaldokumentation](https://github.com/thomasmgfeller/x6-spectral-astrolabium/blob/4a6fe9c383e56b5a26f286fba6aa6d8c9263308a/experimental/evidence_calibration/README.md)

## Dokumentierte Aussage

Datentypen, Evidenzbindung, Bildmetadaten und klassische Referenzmodelle werden softwareseitig geprüft; Hashes authentifizieren keine Messung.

- [experimental/evidence_calibration/REMEDIATION.md](https://github.com/thomasmgfeller/x6-spectral-astrolabium/blob/4a6fe9c383e56b5a26f286fba6aa6d8c9263308a/experimental/evidence_calibration/REMEDIATION.md): Audit-/Fehlerbehandlung und Testzuordnung. Ein erneuter Lauf erzeugt eigene Logs; kein gespeicherter physischer Qualifikationsbefund.

## Reproduzieren

Python 3.12/3.13, Standardbibliothek.

Neue Arbeits- und Ausgabeordner verwenden; Voraussetzungen aus der Originaldokumentation beachten.

```sh
git clone --branch main https://github.com/thomasmgfeller/x6-spectral-astrolabium.git x6-evidence-calibration
cd x6-evidence-calibration
git checkout --detach 4a6fe9c383e56b5a26f286fba6aa6d8c9263308a
python3 -m experimental.evidence_calibration.run_qualification --output runs/register-calibration --protect-research
```

Erwartete Ausgabe: Exit 0; nur die unten genannte Softwareaussage.

## Offene Prüfung

Kontrollierte aufgezeichnete Messdaten, Dunkel-/Sättigungsprüfung, kalibrierter Massstab und vollständiges Unsicherheitsbudget.

Evidenzberichte behalten ihre eigenen Prüfrevisionen. Keine neue Ausführung, externe Begutachtung oder physische Qualifikation durch diese Darstellung.
