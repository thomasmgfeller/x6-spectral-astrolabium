# Lorentz-Kollisionsatlas n=6: vollständiger Forschungsstand

Registerstand: 2026-10-18. BRANCH_ONLY / SOFTWARE. Kein Live-Prüfsiegel.

## Quelle

Branch: research/lorentz-v1-workpackages

Commit: f5116b9970a6b7dc788c18623a8386b4cde33ad4

[Originaldokumentation](https://github.com/thomasmgfeller/x6-spectral-astrolabium/blob/f5116b9970a6b7dc788c18623a8386b4cde33ad4/research/lorentz_n6/README.md)

## Dokumentierte Aussage

318 Ordnungen; 286 Spektralklassen, mit Endpunktzahlen 314, Quill-Basis 285, mit maximalen Quills 318. Nur endlicher Korpus. Vollständiger Forschungsstand einschließlich Generator auf diesem Branch; bytegleicher Prüfer und fester Atlas auch in main über die gemeinsame Offline-Referenzsuite.

- [research/lorentz_n6/results/atlas_n6.json](https://github.com/thomasmgfeller/x6-spectral-astrolabium/blob/f5116b9970a6b7dc788c18623a8386b4cde33ad4/research/lorentz_n6/results/atlas_n6.json): Vollständige Repräsentanten, Polynome und Kollisionsgruppen.
- [research/lorentz_n6/results/independent_verification.json](https://github.com/thomasmgfeller/x6-spectral-astrolabium/blob/f5116b9970a6b7dc788c18623a8386b4cde33ad4/research/lorentz_n6/results/independent_verification.json): Separater Rekonstruktions-/Isomorphie-/Determinantenprüfer, 4.208 Polynome.

## Reproduzieren

Python 3.12/Standardbibliothek für diesen unabhängigen Prüfer; vollständiger Atlasgenerator benötigt NumPy 2.3.5.

Neue Arbeits- und Ausgabeordner verwenden; Voraussetzungen aus der Originaldokumentation beachten.

```sh
git clone --branch research/lorentz-v1-workpackages https://github.com/thomasmgfeller/x6-spectral-astrolabium.git x6-lorentz-n6
cd x6-lorentz-n6
git checkout --detach f5116b9970a6b7dc788c18623a8386b4cde33ad4
python3 research/lorentz_n6/verify.py research/lorentz_n6/results/atlas_n6.json --output /tmp/register-atlas-check.json
```

Erwartete Ausgabe: Exit 0; nur die unten genannte Softwareaussage.

## Offene Prüfung

Die vollständige n=7-Abnahme ist im Modul lorentz-n7-complete abgeschlossen: H7-bidirectional-moments ist durch zwei Restpaare widerlegt. Nächster Schritt: strukturelle Erklärung der minimalen Kollisionen und unabhängige externe Replikation; neue Aussagen müssen eigene Voraussetzungen nennen.

Evidenzberichte behalten ihre eigenen Prüfrevisionen. Keine neue Ausführung, externe Begutachtung oder physische Qualifikation durch diese Darstellung.
