# Mehrschichtiger Fingerprint

Registerstand: 2026-10-19. BRANCH_ONLY / SOFTWARE. Kein Live-Prüfsiegel.

## Quelle

Branch: research/x6-fingerprint-v1

Commit: f22030f2dae0aa670cdbc450c5e881ce250b36b8

[Originaldokumentation](https://github.com/thomasmgfeller/x6-spectral-astrolabium/blob/f22030f2dae0aa670cdbc450c5e881ce250b36b8/research/fingerprint_v1/README.md)

## Dokumentierte Aussage

n6-0073 und n6-0181 werden durch gerichtete Gradmultimengen getrennt. Physischer MODAL_2R1F-Pilot ist ungemessen.

- [research/fingerprint_v1/examples/separation-event.json](https://github.com/thomasmgfeller/x6-spectral-astrolabium/blob/f22030f2dae0aa670cdbc450c5e881ce250b36b8/research/fingerprint_v1/examples/separation-event.json): Exakter Vergleich gebundener gespeicherter Werte; Validator berechnet nicht jedes Polynom aus Rohmatrizen neu.
- [research/fingerprint_v1/examples/physical-pilot-plan.json](https://github.com/thomasmgfeller/x6-spectral-astrolabium/blob/f22030f2dae0aa670cdbc450c5e881ce250b36b8/research/fingerprint_v1/examples/physical-pilot-plan.json): Expliziter Messplan ohne erfundene Messwerte.

## Reproduzieren

Python 3.12 und Anforderungen aus industrial-v1; nur validieren, keine Beispielregeneration nötig.

Neue Arbeits- und Ausgabeordner verwenden; Voraussetzungen aus der Originaldokumentation beachten.

```sh
git clone --branch research/x6-fingerprint-v1 https://github.com/thomasmgfeller/x6-spectral-astrolabium.git x6-fingerprint
cd x6-fingerprint
git checkout --detach f22030f2dae0aa670cdbc450c5e881ce250b36b8
python3 -m pip install -r experiments/industrial-v1/requirements.txt
python3 research/fingerprint_v1/validate.py research/fingerprint_v1/examples/n6-0073.json research/fingerprint_v1/examples/n6-0181.json research/fingerprint_v1/examples/separation-event.json research/fingerprint_v1/examples/physical-pilot-plan.json
```

Erwartete Ausgabe: Exit 0; nur die unten genannte Softwareaussage.

## Offene Prüfung

Empirischen Assessor mit Unsicherheit/Bestätigungsdaten implementieren; Pilot kalibrieren und Rohdaten prüfen.

Evidenzberichte behalten ihre eigenen Prüfrevisionen. Keine neue Ausführung, externe Begutachtung oder physische Qualifikation durch diese Darstellung.
