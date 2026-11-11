# Kleiner Randzustandsraum A → A v0.1

Schritt 2 nach PR #279. Ein inneres Element, zwei unmarkierte Antichainpunkte
an jedem Rand. Vier explizite normierte kinematische Pakete pro Rand;
Gram-Matrix I₄. Die nach Dichtemasken aufgelöste Produktfamilie hat Rang 6.
Das zusätzliche redundante Aufnehmen des „+“-Pakets liefert acht Vektoren
mit Rang 6. „+“ umfasst 10,01,11; es ist eine kohärente Summe mit Phase null.

**Keine physikalische CST-Übergangsmatrix. Alle physikalischen Gates: HOLD.**

- `CST_DUST_Randzustandsraum_v0_1.pdf`: lesbarer Bericht.
- `DERIVATION.md`: vollständige Herleitung, Maße, Paketfunktionen und Grenzen.
- `boundary_contract.json`: maschinenlesbarer Vertrag mit festen Kontrollwerten.
- `boundary.py`, `test_boundary.py`: exakte Algebra und 20 Prüfungen.
- `results/gram_matrices.json`: exakte Matrizen und Ränge.
- `inputs/`: unveränderte Quellen-Schnappschüsse zur Nachverfolgung;
  sie werden nicht als ausführbares Vorgängerpaket angeboten.
- `provenance.json`, `MANIFEST.sha256.json`: Herkunft und Integrität.

Reproduktion (Python 3.10+, SymPy 1.14.0):

```bash
python verify.py
```

Keine Produktionssimulation und keine kostenpflichtigen Dienste. Die Prüfung
liest nur lokale Dateien und aktualisiert weder Referenzdaten noch Hashes.
Für absichtliche neue Resultate: `python build_evidence.py`. Für das PDF:
`python make_report.py` (ReportLab, Matplotlib und Pillow).
`python package.py` erzeugt nach einer bewussten inhaltlichen Änderung ein
neues Manifest und das ZIP; dies ersetzt nicht die Prüfung eines Empfangspakets.

Die Zustandsauswahl schließt weder physikalische Constraints noch dynamische
Austrittskanäle. Der vollständige Hilbertraum ist unendlichdimensional.
Das Paket ist für den Anschluss unter
`research/rax_cqg/dust_collapse/boundary_state_space_v0_1/` vorbereitet.
