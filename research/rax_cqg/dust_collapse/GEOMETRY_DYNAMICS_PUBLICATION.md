# Stationärer Geometriekandidat v0.1

13. November 2026 · Anschluss an die [kohärente Endrandmessung](BOUNDARY_COHERENCE_PUBLICATION.md), PR 290 / `f5ee44d7cb4dc1f924eee580f1eaf0cfcb4a5bc6`.

**Zwei verschiedene Kausalordnungen mit elf Ereignissen besitzen bei identischen äußeren Randdaten positive stationäre innere Staubquellen. Ihre stationäre Wirkungsdifferenz ist exakt ΔS = 8 + 23ρ/19 für 0 < ρ < 1/2. Die gemeinsame gaußsche Skalar-Randpaarung besitzt einen endlichen Abel-Grenzwert. Physikalische Geometriedynamik ist weiterhin nicht hergeleitet.**

[Bericht (PDF)](reports/CST_DUST_Geometriedynamik_Stationaerer_Kandidat_v0_1.pdf) · [Originalprüfpaket (ZIP)](packages/CST_DUST_Geometriedynamik_Stationaerer_Kandidat_v0_1_Pruefpaket.zip) · [Quellen und Reproduktion](geometry_dynamics_v0_1/README.md) · [Neuer Kandidatenvertrag](geometry_dynamics_v0_1/contracts/geometry_candidate.json) · [Publikationsnachweis](geometry_dynamics_publication.json)

## Ergebnis und Anschluss

Der frühere Sechshistorienpilot zeigte eine bedingte, phasenabhängige Materieauslese. Der neue endliche Randwertversuch vergleicht unterschiedliche innere Geometrien nach Lösung ihrer Materiegleichungen: eine vollständige Kette und dieselbe Ordnung ohne die Coverrelationen (4,5) und (5,6), mit erhaltener Relation (4,6). Der feste äußere Kragen ist B={0,1,2,3,7,8,9,10}; sämtliche B–B- und B–I-Relationen bleiben gleich.

| Größe | Kette | Geometrische Alternative |
| --- | --- | --- |
| Innere skalierte Uhr u_I | (4,5,6) | (4,4,5) |
| Innere Dichten r_I/ρ | (1,1,1) | (2,1,1) |
| Stationäre Wirkung | 10−151ρ/38 | 18−105ρ/38 |
| Zahl innerer Relationen | 3 | 1 |

Die bestehende Wirkung bleibt unverändert. Historienfamilie, positive feste Kragenpräparation und Uhrsupport sind ausdrücklich neu; der affine Vergleich benötigt eine größere Uhrbox als der frühere Pilot. ρ bezeichnet den äußeren Dichteparameter, keine bereits kalibrierte Gesamtmasse. Die Skalar-Testpaarung und der klassische Referenzpunkt q_B=0 werden getrennt behandelt.

Ein zusätzlicher regulärer N10-Materiesattel liegt sogar in der früheren Uhrbox. Die wirkungsabgeleitete Vorwärtsrekursion hat jedoch einen wachsenden Störmultiplikator in (−6,−5). Die ursprüngliche kompakte Dichteintegration ist weiterhin kein Constraint-Projektor. Physische Paarung, Historiensummenmaß, Geometriewahrscheinlichkeiten, stabile Evolution und vierdimensionale Staubball-Korrespondenz bleiben offen. Die neue Konstruktion ist explorativ, keine verblindete Vorhersage oder externe Begutachtung.

## Unveränderte Originale und Reproduktion

Alle 37 Dateien des ursprünglichen Pakets einschließlich seines Berichts und Manifests sowie das ursprüngliche ZIP werden unverändert veröffentlicht. Der separate Bericht stimmt bytegleich mit dem eingebetteten PDF überein. Die sechs Fachberichte dokumentieren interne KI-Arbeitsperspektiven und ihre Gegenprüfungen.

```sh
python -m pip install -r research/rax_cqg/dust_collapse/geometry_dynamics_v0_1/requirements.txt
python -B research/rax_cqg/dust_collapse/verify_geometry_dynamics_publication.py
```

Der Publikationsprüfer kontrolliert Größen, SHA-256 und vollständige ZIP/Quellcode-Parität und ruft den ursprünglichen isolierten Replay auf: neun Programme, 13 bytegleich reproduzierte JSON-Dateien. Eine auf diese Veröffentlichung begrenzte CI führt dieselbe Prüfung aus. Die vorhandenen umfangreichen wissenschaftlichen Integrationen werden nicht wiederholt.

Die Angaben über ausbleibende GitHub-Mutationen in den Originaldateien beschreiben die abgeschlossene wissenschaftliche Untersuchung. Diese gesonderte Publikationshülle dokumentiert ihre anschließende Veröffentlichung.

English: two finite causal orders share the same outer boundary and admit positive stationary matter sources. Their on-shell action difference is 8+23ρ/19; a common scalar Gaussian boundary pairing has a finite Abel limit. The action is unchanged, while the finite history family, source preparation and clock support are new. Physical geometry evolution remains NOT_DERIVED. Original artifacts are preserved, and nine isolated programs reproduce thirteen JSON files exactly.
