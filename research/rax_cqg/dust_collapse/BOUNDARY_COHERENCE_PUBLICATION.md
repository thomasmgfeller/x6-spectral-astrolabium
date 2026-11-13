# Kohärente Endrandmessung v0.1

> **Nachfolgende Arbeit:** Der [stationäre Geometriekandidat v0.1](GEOMETRY_DYNAMICS_PUBLICATION.md) führt zu einem expliziten Vergleich zweier geometrischer Ordnungen mit positiven gelösten Quellen und gemeinsamem äußerem Rand. Der hier dokumentierte Endrandversuch und sein Originalpaket bleiben unverändert.

Publikation vom 13. November 2026 · Anschluss an den [konsolidierten Forschungsstand](research_update_2026_11_13/README.md).

**Eine klassenblinde kohärente Auslese macht im erklärten endlichen Hilfsmodell die relative Gravitationsphase in terminalen Skalarmodenwahrscheinlichkeiten sichtbar. Physikalische Geometriedynamik, Rückwirkung und Singularitätsauflösung bleiben offen.**

[Bericht (PDF)](reports/CST_DUST_Kohaerente_Endrandmessung_v0_1.pdf) · [Originalprüfpaket (ZIP)](packages/CST_DUST_Kohaerente_Endrandmessung_v0_1_Pruefpaket.zip) · [Code und Herleitung](boundary_coherence_v0_1/README.md) · [Publikationsnachweis](boundary_coherence_publication.json)

## Anschluss und Aussagegrenzen

Der frühere Sechshistorienpilot unterschied Ordnungsklasse 1 und 2. Seine Klassenrecords waren gegenüber den Phasen mit F4=9 und F4=-7 blind. Der neue bedingte Recordvertrag lässt diese Klassen kohärent zum selben Endrand R={4,5} beitragen; das Innere ist I={3}. Die bestehende P/A-Präparation und Wirkung bleiben erhalten. Das innere Atom-/Positivstratum wird zunächst weiter unterschieden. Bloßes nachträgliches Weglassen eines klassischen Klassenlabels erzeugt keine Interferenz.

Zwei normierte, orthogonale, unter Endknotenvertauschung invariante Skalarmoden liefern tatsächliche terminale Records innerhalb dieses Hilfsmodells. Bei ideal angenommenem Umweltüberlapp gamma=1, ursprünglicher Phase kappa=1 und Gain 1/1024 liegt P(f2|Erfolg,g+)−P(f2|Erfolg,g0) in [2,5194616115; 2,5238895751] × 10⁻⁶. Die Erfolgswahrscheinlichkeiten betragen nur etwa 3,59 × 10⁻¹⁰ beziehungsweise 9,35 × 10⁻¹⁰; Misserfolg ist vollständig bilanziert.

Der dephasierte Vergleich besitzt bereits eine kleine Quellenantwort. Zusätzliche Vergleiche kohärent/dephasiert und mit ausschließlich entfernten F4-Phasen trennen den Interferenzbeitrag. Die Phasenentfernung ist eine kontrafaktische Änderung der Wirkung, kein physischer Gravitationseinsteller. Die Skalarmoden sind keine Radius- oder Krümmungsmessung; die Zahlen sind keine Hardware-Zählraten.

Physische Kohärenz, Constraintpaarung, Quellen-/Uhrkalibrierung und geometrische Observable sind weiterhin nicht abgeleitet. Die Prüfungen der Quellenbedingungen und Uhrreflexion bestätigen begrenzte Hindernisse; sie liefern kein allgemeines CST-No-go. Der physische Zwei-Quellen-Geometrievergleich bleibt **HOLD_NOT_DERIVED**.

## Bewahrte Originale und gezielte Reproduktion

Alle 37 Dateien des Originalprüfpakets, einschließlich seines eingebetteten PDFs und Manifests, sind unverändert veröffentlicht. Das unveränderte Einzel-PDF steht zusätzlich unter `reports/`. Einzel-PDF und eingebettetes PDF haben unterschiedliche Dateibytes; ihr extrahierter Text stimmt überein. Beide Prüfsummen sind dokumentiert.

Die sieben kleinen Prüfprogramme wurden für diese Publikation in einem isolierten Verzeichnis ausgeführt. Alle gespeicherten Dateien blieben bytegleich; 36 ursprüngliche Manifesteinträge und 37 ZIP/Quellcode-Paare stimmen. Die drei geerbten Dateien `pilot.json`, `result_64.json` und `dowker_history_data.json` wurden gegen das zuvor veröffentlichte Quellen-/Ordnungsarchiv abgeglichen. Die geerbten Amplitudeneinschließungen wurden dabei nicht durch erneute Quadratur validiert. Keine neue große Integration oder physikalische Kollapsrechnung wurde gestartet.

```sh
python -m pip install -r research/rax_cqg/dust_collapse/boundary_coherence_v0_1/requirements.txt
python -B research/rax_cqg/dust_collapse/verify_boundary_coherence_publication.py
```

Eine auf dieses Paket begrenzte CI wiederholt Integritätsprüfung und isolierten Replay. Der PDF-Generator und ältere Großpakete sind dafür nicht erforderlich. Hinweise auf ausbleibende GitHub-Mutationen im Originalpaket beschreiben dessen damalige wissenschaftliche Ausführung; diese Publikationshülle dokumentiert die anschließende Veröffentlichung. Die Personennamen in `agents/` bezeichnen historische KI-Prüfperspektiven; die genannten Wissenschaftler waren nicht beteiligt.

English: this unchanged finite auxiliary package demonstrates conditional gravitational-phase sensitivity of terminal scalar records under an assumed coherent boundary pairing. Seven isolated programs reproduce the frozen outputs exactly; inherited quadrature is not rerun. Physical geometry, backreaction and singularity resolution remain unestablished.
