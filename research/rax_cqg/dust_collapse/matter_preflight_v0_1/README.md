# CST-DUST Materieblock-Vorprüfung v0.1

Die korrigierte nächste Arbeitsstufe lautet **„Materieblöcke: Randvertrag, Schur- und Paritätsprüfung“**. Sie schließt an die ausgewählte Hilfsbasis aus PR #277 an.

**Ergebnis:** 25 exakte endliche Kontrollen bestehen. Die vier ursprünglichen Verklebungsfasern haben 35/26/26/20 Elemente. Eine ausdrücklich zusätzliche Einschränkung auf keine Rückrelationen ergibt 16/9/9/6; das ist noch keine physikalische Randdynamik.

Für eine unter gemeinsamer Feldspiegelung invariante quadratische Theorie mit Randpaketen bestimmter Parität verschwindet der vorgeschlagene Vakuum-zu-Einteilchen-Zeuge bereits aus Symmetrie. Gerade Mischblöcke bleiben dadurch offen. Eigenvektoren eines Schurblocks sind keine automatisch quantisierten Vakuum-/Einteilchenzustände.

- Vollständige Herleitung: [DERIVATION.md](DERIVATION.md)
- Lesefassung: [CST_DUST_Materieblock_Vorpruefung_v0_1.pdf](CST_DUST_Materieblock_Vorpruefung_v0_1.pdf)
- Offene Eingaben: [open_inputs.json](open_inputs.json)
- Exakte Kontrollen: [analyze.py](analyze.py), [algebra_checks.json](results/algebra_checks.json)
- Enumeration mit allen Ordnungs-IDs und Polynomen: [geometry_carrier_audit.json](results/geometry_carrier_audit.json)
- Quellen und Versionen: [provenance.json](provenance.json)

Die algebraische Reproduktion benötigt Python 3.11+ und SymPy 1.14.0. ReportLab und Matplotlib werden nur für die PDF-Erzeugung benötigt.

    python analyze.py
    python verify.py

**PREPARATION_ONLY.** Physikalische Materiematrix NOT_CONSTRUCTED, physikalischer Mischblock NOT_COMPUTED, alle acht physikalischen Gates HOLD. Keine Produktionsrechnung, keine kostenpflichtigen Rechenaufträge und keine erfundenen Materieblöcke.
