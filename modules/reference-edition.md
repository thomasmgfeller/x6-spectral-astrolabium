# Gemeinsame Referenzedition und Agentenarchiv

Registerstand: 2026-10-19. MAIN / SOFTWARE. Kein Live-Prüfsiegel.

## Quelle

Branch: main

Commit: d6c9f3d9ddf975cdc6f0c2ce055c5becb1f7a2ee

[Originaldokumentation](https://github.com/thomasmgfeller/x6-spectral-astrolabium/blob/d6c9f3d9ddf975cdc6f0c2ce055c5becb1f7a2ee/docs/reference-qe-v0.1/EXTERNAL_REPRODUCTION.md)

## Dokumentierte Aussage

Erweiterte Referenzedition mit zehn Offline-Berichten, exaktem X6-QE-Modul, begrenztem RAX-G1-Runner und ausgewählten archivierten Original-Agentenbelegen. Alte Referenzfreigabe bleibt unverändert; externe personelle Wiederholung NOT_PERFORMED.

- [docs/reference-qe-v0.1/expected-reference.json](https://github.com/thomasmgfeller/x6-spectral-astrolabium/blob/d6c9f3d9ddf975cdc6f0c2ce055c5becb1f7a2ee/docs/reference-qe-v0.1/expected-reference.json): Festgelegte zehn Berichtshashes; acht bestehende fachliche Berichte unverändert. Neu: QE und ergänzter Fehlerkontrollbericht. Ausführungsabnahme steht in X6-QE/ACCEPTANCE.md.
- [docs/validation-v1/expected-reference.json](https://github.com/thomasmgfeller/x6-spectral-astrolabium/blob/d6c9f3d9ddf975cdc6f0c2ce055c5becb1f7a2ee/docs/validation-v1/expected-reference.json): Feste SHA-256-Erwartungen für alle neun Referenzberichte; ursprünglicher Quellenumfang unverändert.
- [docs/agent-archive/2026-10-15/ARCHIVE.json](https://github.com/thomasmgfeller/x6-spectral-astrolabium/blob/d6c9f3d9ddf975cdc6f0c2ce055c5becb1f7a2ee/docs/agent-archive/2026-10-15/ARCHIVE.json): Drei Original-ZIPs samt ursprünglichen Ablaufdaten, GitHub-Digests und vollständigen Dateiinventaren.
- [docs/validation-v1/evidence/citation-validation.json](https://github.com/thomasmgfeller/x6-spectral-astrolabium/blob/d6c9f3d9ddf975cdc6f0c2ce055c5becb1f7a2ee/docs/validation-v1/evidence/citation-validation.json): CFF 1.2.0 gegen offizielles Schema geprüft; keine erfundene DOI oder ORCID.
- [docs/validation-v1/external-report.template.json](https://github.com/thomasmgfeller/x6-spectral-astrolabium/blob/d6c9f3d9ddf975cdc6f0c2ce055c5becb1f7a2ee/docs/validation-v1/external-report.template.json): Noch nicht eingereichte Erklärung der ausführenden Person; keine externe Bestätigung vorweggenommen.

## Reproduzieren

Sauberer Git-Checkout; Python 3.12 und Node 24. Standardbibliothek. Die veröffentlichten Release-Assets sind der kürzere externe Einstieg.

Neue Arbeits- und Ausgabeordner verwenden; Voraussetzungen aus der Originaldokumentation beachten.

```sh
git clone --branch main https://github.com/thomasmgfeller/x6-spectral-astrolabium.git x6-reference-edition
cd x6-reference-edition
git checkout --detach d6c9f3d9ddf975cdc6f0c2ce055c5becb1f7a2ee
python3 -S -B tools/release/build.py --output /tmp/register-reference-assets
python3 -m zipfile -e /tmp/register-reference-assets/x6-reference-2026.10.15.zip /tmp/register-reference-unpacked
python3 -S -B /tmp/register-reference-unpacked/x6-reference/tools/release/reproduce.py --output /tmp/register-reference-reproduction
```

Erwartete Ausgabe: Aus dem entpackten neuen Release: PASS_REFERENCE_REPRODUCTION, zehn eingefrorene Berichte ohne Abweichung, 33 RAX-G1-Zurückweisungen. Anleitung nennt Paket und Runtime.

## Offene Prüfung

Tatsächliche unabhängige Wiederholung entgegennehmen, Ergebnisdateien erneut prüfen, Abweichungen und personelle Unabhängigkeit bewerten; EXT-1 erst danach schließen.

Evidenzberichte behalten ihre eigenen Prüfrevisionen. Keine neue Ausführung, externe Begutachtung oder physische Qualifikation durch diese Darstellung.
