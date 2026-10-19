# RAX-U1: Reduktionskontrolle

Registerstand: 2026-10-19. MAIN / SOFTWARE. Kein Live-Prüfsiegel.

## Quelle

Branch: main

Commit: 6738f129ca31e56a88690a9d17941516ccefb321

[Originaldokumentation](https://github.com/thomasmgfeller/x6-spectral-astrolabium/blob/6738f129ca31e56a88690a9d17941516ccefb321/docs/research/rax/countercheck-v0.1/README.md)

## Dokumentierte Aussage

160 Matrizen/3,2 Mio. Übergänge; Entscheidungen 8 gestützt, 16 verworfen, 16 unentschieden. Archivvorfall bleibt offen.

- [docs/research/rax/countercheck-v0.1/RAX_U1_Gegenpruefung_v0_1_Paket.zip](https://github.com/thomasmgfeller/x6-spectral-astrolabium/blob/6738f129ca31e56a88690a9d17941516ccefb321/docs/research/rax/countercheck-v0.1/RAX_U1_Gegenpruefung_v0_1_Paket.zip): Originalquellen, Rohdaten, audit-final und Gegenproben im Paket.

## Reproduzieren

Linux, Python 3.12, NumPy/SciPy aus enthaltenen requirements.

Neue Arbeits- und Ausgabeordner verwenden; Voraussetzungen aus der Originaldokumentation beachten.

```sh
git clone --branch main https://github.com/thomasmgfeller/x6-spectral-astrolabium.git x6-rax-u1
cd x6-rax-u1
git checkout --detach 6738f129ca31e56a88690a9d17941516ccefb321
python3 -m zipfile -e docs/research/rax/countercheck-v0.1/RAX_U1_Gegenpruefung_v0_1_Paket.zip /tmp/x6-hub-rax-u1
cd /tmp/x6-hub-rax-u1/RAX_U1_Gegenpruefung_v0_1
python3 -m pip install -r research/rax_u1_countercheck/requirements.txt
python3 research/rax_u1_countercheck/audit.py --output audit-reproduced.json
python3 research/rax_u1/reference.py research/rax_u1/evidence/qualification
```

Erwartete Ausgabe: Exit 0; nur die unten genannte Softwareaussage.

## Offene Prüfung

Dauerhafte Speicherung mit Flush/fsync, Reopen/Hashprüfung sowie Abbruch-/Kürzungs-/Neustarttests qualifizieren.

Evidenzberichte behalten ihre eigenen Prüfrevisionen. Keine neue Ausführung, externe Begutachtung oder physische Qualifikation durch diese Darstellung.
