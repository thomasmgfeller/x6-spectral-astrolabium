# Krümmung: begrenzter Benchmark und exakte Dichteverwechslung

**Ergebnis:** Beide vorab festgelegten Empfindlichkeitskriterien sind verfehlt.
Bei N=128 warnt die gemeinsame C2/C3/C4-Diagnose in 118/512 stark gekrümmten
Fällen (23,05%), die längste Kette in 5/512 (0,98%). Alle 3.072 gekoppelten
Dichtezwillinge bestätigen dieselbe Ordnung bei unterschiedlicher Krümmung.
Ein universeller Krümmungssensor ist bei unbeschränkt unbekannter
Beprobungsdichte aus der Ordnung allein nicht identifizierbar.

[Ergebnisbericht mit allen Zellen](RESULTS.md) · [Vorab fixierter Entwurf](DESIGN.md) ·
[Maschinenlesbarer Vertrag](contract.json) · [Rohdaten und Summen](results/) ·
[Eigenzeit-Vorgeschichte](../lorentz_proper_time_publication/README.md)

Der öffentliche [Quellenstand `31cfd8c`](https://github.com/thomasmgfeller/x6-spectral-astrolabium/commit/31cfd8ca832cffe67942cd198eb2d9d260765f62)
liegt vor dem ersten Zielversuch. 8.702 unabhängige Ordnungen, korrekte
4D-de-Sitter-Volumenbeprobung, bekannte Referenzeigenzeiten, flache Dichte-
und Maskenkontrollen sowie fehlerhafte Relationen sind vollständig erhalten.
N=64/128 ist jeweils fest: bedingte Poisson-Beprobung, keine zufällige
Poisson-Punktzahl. Das Paket schätzt keine unbekannte Krümmung und baut keine
physische Planck-Uhr. Die Ergebnisse stehen zusätzlich im englischen Bericht.

## Reproduzieren

Python 3.12 unter Linux/POSIX, NumPy 2.3.5, SciPy 1.17.0. Ein vollständiger
Git-Checkout mit dem öffentlichen Quellencommit ist erforderlich. Alle
folgenden Befehle werden vom Repository-Stamm ausgeführt:

```sh
python3 -m pip install -r research/lorentz_curvature/requirements.txt
python3 -B research/lorentz_curvature/selftest.py
python3 -B research/lorentz_curvature/verify.py
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 python3 -B research/lorentz_curvature/reproduce.py
```

Erwartet: `PASS_ARCHIVED_EVIDENCE` und `PASS_FULL_CURVATURE_REPLAY`.
Die Wiederholung erzeugt sämtliche Punktwolken in einem neuen temporären
Verzeichnis und vergleicht alle wissenschaftlichen Ausgaben. Pro Ziellauf
gelten 600 Sekunden und 2 GiB; Prüfer und Wiederholung benötigen zusätzliche
Zeit. Die Originaldaten werden dabei nicht überschrieben.

Diese technischen PASS-Status ändern die wissenschaftlichen Status
`PRIMARY_SENSITIVITY_NOT_ESTABLISHED` (beide Methoden) und
`NOT_IDENTIFIABLE_WITH_UNRESTRICTED_SAMPLING_DENSITY` nicht.
Unsicherheitsintervalle gelten bedingt auf das festgehaltene Training und
die gemeinsame Kalibrierungsbank. Kein Nachweis für fortlaufendes Peeking,
keine externe Replikation.

## Nächste begründete Nutzung

Ein Demonstrator darf die Eigenzeit-Referenz im bekannten flachen Modell
und **Warnungen vor Modellabweichungen** zeigen. Der Dichtezwilling gehört
sichtbar dazu. Ein weiterer Leistungsversuch muss zuerst unabhängiges Wissen
über die Beprobung und eine identifizierbare geometrische Zielgröße festlegen;
Schwellen und Stichproben werden für diesen Versuch neu vorab fixiert.
