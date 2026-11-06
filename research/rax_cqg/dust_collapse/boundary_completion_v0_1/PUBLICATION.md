# Innen-/Außenraum-Anschluss v0.1

**6. November 2026 · CST-DUST-BOUNDARY-001 · Prüfpunkt P5**

**Der klassische endliche Referenzanschluss ist geschlossen. Der vollständige
physikalische CST-Anschluss bleibt HOLD_NOT_ELIGIBLE / NOT_RUN; Regularität
und kausale Fortsetzung bleiben unabhängig HOLD.**

Für das flache homogene Einstein-Staubinnere mit mitbewegter zeitartiger
Oberfläche und Schwarzschild-Außenraum konstanter positiver Masse werden
induzierte Metrik, extrinsische Krümmung, Feldgleichungen, Massen- und Flussbilanz
sowie distributionelle Erhaltung gemeinsam nachgewiesen. Der Anschluss ohne
dünne Schicht verlangt `Rdot_b² = 2GM/Rb` und `Rddot_b = -GM/Rb²`.
Der Horizontdurchgang ist im regulären EF-Chart explizit; der klassische
Außenraum reicht bis zur asymptotisch flachen Unendlichkeit.

Unter einer ausdrücklich zusätzlichen klassischen Zukunftswahl lässt sich der
Ereignishorizont bestimmen. Diese Aussage folgt nicht allein aus dem früheren
endlichen Prüfzeitfenster. Die fortgesetzte klassische Lösung bleibt singulär.

Ein Bounce kann unter den angegebenen Voraussetzungen nicht schichtfrei an
Schwarzschild anschließen. Bei oder innerhalb `R = 2GM` kann auch das bloße
Hinzufügen einer Israel-Schicht die zeitartige Bounce-Bahn nicht ermöglichen.
Ein zusätzlich angesetzter statischer Nichtvakuum-Außenraum liefert eine
bedingte Vergleichsgeometrie mit effektivem anisotropem Stress. Er reaktiviert
den verworfenen Bounce-Kandidaten nicht und ist keine CST-Herleitung; globale
Fortsetzung, Horizontstabilität und geodätische Vollständigkeit sind dafür
nicht qualifiziert.

Exakte Kettenkontrollen zeigen, dass isoliertes Abschneiden von Innen- und
Außengebiet übergreifende Beziehungen und BDG-Wirkungsbeiträge verändert.
Diese kleinen Ketten sind kinematische Kontrollen, keine vierdimensionalen
dynamischen Ensembles. Die materielle Oberfläche bleibt ausdrücklich von einer
äußeren Rechengrenze unterschieden.

## Prüfung und Aussagegrenzen

34 exakte Identitäten, 15 klassische Randfälle, 75 Außenraumwerte, neun
EF-Einbettungen, drei bedingte klassische Ereignishorizontfälle, 20 bedingte
Nichtvakuum-Anschlüsse, 27 Kettenschnitte, 24 Labelpermutationen und
19 Entscheidungskontrollen sind dokumentiert. Die größte klassische numerische
Resthülle beträgt etwa `1.06948e-29`, unter dem vorher lokal fixierten
technischen Cap `1e-20`. Dies ist keine physikalische Genauigkeitsangabe oder
externe Präregistrierung.

Alle 60 P5-Datensätze halten sämtliche acht physikalischen Gates auf HOLD.
Die vier Dichtestufen sind geplant; keine physikalische CST-Verfeinerung wurde
ausgeführt. Neue dynamische CST-Ensembles, Zufallsstichproben und bezahlte Läufe:
jeweils null. Es fehlen weiterhin die gemeinsame endliche CST-Wirkung samt
Rand- und Eckbeiträgen, der Außenraumzustand, kalibrierte Randobservablen,
kontrollierte äußere Gebietsfehler und unabhängige Regularitäts-/Fortsetzungsnachweise.

## Bericht und Nachrechnung

- [Bericht (PDF, neun Seiten)](../reports/CST_DUST_Innen_Aussen_Anschluss_v0_1.pdf)
- [Unverändertes Originalpaket (ZIP)](../packages/CST_DUST_Innen_Aussen_Anschluss_v0_1_Pruefpaket.zip)
- [Herleitung und Quellen](DERIVATION.md), [fixierter Plan](plan.json), [Ergebnisse](results/verification.json)
- [Getrennte Abschlussentscheidungen](results/closure_decision.json), [60 P5-Auswertungen](results/checkpoint_P5_audits.json)
- Vorgänger: [Modellvertrag](../model_contract_v0_1/PUBLICATION.md), [Korrespondenz](../correspondence_v0_1/PUBLICATION.md), [Expansion und Trapping](../expansion_trapping_v0_1/PUBLICATION.md), [Regularität](../regularity_v0_2/PUBLICATION.md)

Vom Repository-Stamm mit Python 3.12:

```sh
python3 -O -B research/rax_cqg/dust_collapse/boundary_completion_v0_1/publication_check.py
python3 -m pip install -r research/rax_cqg/dust_collapse/boundary_completion_v0_1/requirements.txt
python3 -O -B research/rax_cqg/dust_collapse/boundary_completion_v0_1/publication_check.py --replay
```

Der Publikationscheck verifiziert das ursprüngliche ZIP, alle 41 Mitglieder,
vollständige SHA-256-Verknüpfungen, den PDF-Bericht, unveränderte Vorgängereingaben,
den fixierten Plan und alle P5-Entscheidungen. Der Replay löscht die temporär
entpackten Ergebnisdateien, rechnet neu und vergleicht alle 15 erzeugten Dateien.
Nur die tatsächliche Python-Laufzeitversion und daraus berechnete
Manifest-Verknüpfungen dürfen abweichen; die Verknüpfungen werden vor diesem
Vergleich gesondert geprüft. SymPy bleibt auf 1.14.0 fixiert. Optimiertes
Python deaktiviert keine Kontrolle. Die GitHub-Aktion führt beide Prüfungen aus.

Originalpaket und expandierte Originaldateien bleiben unverändert.
`PUBLICATION.md` und `publication_check.py` ergänzen die Veröffentlichung.
