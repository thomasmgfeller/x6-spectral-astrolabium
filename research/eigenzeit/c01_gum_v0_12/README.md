# Eigenzeit v0.12 · Wie prüft man die 2-ppm-Grenze an C01?

Die Studie definiert die Trefferwahrscheinlichkeit je markiertem Versuch am ersten Referenzpunkt aus v0.11. Für das vorgeschlagene 810-nm-Labormodell dokumentiert sie die acht Arbeitsschritte nach JCGM 100:2008, Abschnitt 8, einschließlich der Prüfung des nichtlinearen Produkts aus Gain und Zielwahrscheinlichkeit nach Amd.1:2026. [Bericht (PDF)](Eigenzeit_C01_GUM_v0_12.pdf) · [Unsicherheitsbilanz](GUM_BILANZ.md) · [Originales Prüfpaket (ZIP)](Eigenzeit_C01_GUM_v0_12_Pruefpaket.zip)

| Größe im synthetischen Beispiel mit 16 Blockpaaren | Ergebnis |
|---|---:|
| Geschätzte Abweichung am ersten Referenzpunkt | +0,19 ppm |
| Kombinierte Standardunsicherheit | 0,124 ppm |
| Erweiterte Unsicherheit bei ungefähr 95 % Überdeckung | 0,26 ppm |
| Erweiterungsfaktor und angesetzte Freiheitsgrade | 2,080 und 21 |

Die beiden Blockmittel für Ziel- und Vergleichszustand sind korreliert. Der Rechner berücksichtigt ihre Kovarianz und weist den zusätzlichen Varianzbeitrag des Produkts gesondert aus. Ob die Abweichung innerhalb von ±2 ppm liegt, wird anhand separat belegter Grenzen und eines vorab festgelegten Risikobudgets geprüft. [Vollständiges Rechenergebnis](records/gum.json) · [Unabhängige Gegenrechnung](records/gum_verification.json) · [Entscheidungsregel](NACHWEIS.md)

**Für die reale Anlage gilt HOLD_GUM_INPUT.** Es fehlen gepaarte Kalibrierblöcke, ein unabhängiger Gain-Nachweis, Daten zum Transfer und Belege für die Modellannahmen. Das bereitgestellte Anforderungsblatt beschreibt, was ein Metrologielabor für die binäre Trefferwahrscheinlichkeit bei 810 nm angeben müsste. [Messdefinition](MESSVERTRAG.md) · [Laboranfrage](LABORANFRAGE.md) · [Feldvorlage](examples/field_gum.json) · [Referenzaudit v0.11](../reference_audit_v0_11/README.md)

## Auswertung und Reproduktion

Im Wurzelverzeichnis des Repositorys mit Python 3.12 ausführen.

```sh
python -m pip install -r tools/workflow/requirements-research.txt
python -B research/eigenzeit/c01_gum_v0_12/publication_check.py --replay
```

Der Prüflauf verifiziert die Originale, alle 43 Archiveinträge und fünf Quellen aus dem veröffentlichten v0.11-Archiv. Anschließend erzeugt er die fünf Ergebnisprotokolle neu und vergleicht sie byteweise mit der Archivfassung. Die Feldentscheidung und das synthetische Beispiel können auch direkt im Studienverzeichnis ausgeführt werden.

```sh
python -B evaluate.py examples/field_gum.json examples/field_anchor.json
python -B evaluate.py examples/gum_synthetic.json examples/qualified_synthetic/anchor.json
```

[Ergebnis für die leere Feldvorlage](records/field.json) · [Synthetische Auswertung](records/synthetic_evaluation.json) · [Veröffentlichungsnachweis](PUBLICATION.json)
