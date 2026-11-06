# Staubstrom und Messgrößen: bedingte Referenzkalibrierung v0.1

**6. November 2026 · CST-DUST-CURRENT-CAL-001 · Prüfpunkt P2**

Ein konservativer Strom mit expliziten Materiemarken ist definiert. Schnittmasse,
seitlicher Massenfluss, räumliches Volumen und gemittelte Dichte sind an der
endlichen klassischen Referenz des [Modellvertrags](../model_contract_v0_1/PUBLICATION.md)
kalibriert. Oberfläche und ein in den Vakuumaußenraum reichender Detektor sind
enthalten. Die Bewegung, Geometrie, Uhren und Zähldichte werden dabei eingesetzt;
ihre dynamische Erzeugung aus dem gekoppelten CST-Kern bleibt offen.

## Ergebnis und Aussagegrenze

| Prüfung | Ergebnis | Geltungsbereich |
|---|---|---|
| Markierter Strom | 86 Kontrollen; exakte Bilanz- und Coarse-graining-Identitäten | Konservativer kinematischer Fluss, keine Herleitung drucklosen Staubs |
| Masse und Fluss | 420 Massen- und 144 Flussfälle innerhalb analytischer Quadraturgrenzen | Vorgegebene endliche klassische Referenz |
| Zeitfensterkorrektur | Unkorrigierter Volumenbias bis 21,33 %; korrigierter Volumenschätzer unverzerrt | Exakt bekannte Exposition und Poisson-Zählung |
| Dichtepräzision | Bei 4λ₀ gemeinsame Erfolgsuntergrenze 98,1203 % für das ±5-%-Intervallziel | 315 Fälle; deterministische Massengrenzen, ideal kalibrierte Geometrie |
| Physikalischer CST-Strom | **HOLD** | Materiemarken und Messadapter noch nicht aus dem gekoppelten Kern erzeugt |
| Regularität und Singularitätsauflösung | **HOLD**, separat am Prüfpunkt P2 | Keine physikalischen CST-Operatoren, uniformen Momentenschranken oder kontrollierte Fortsetzung |

Bei positiver möglicher Masse und leerer Zählung bleibt die obere Dichtegrenze
unendlich: `HOLD_ZERO_COUNT`. Ein inverser Zählschätzer wird nicht mit einem
physikalischen inversen Volumenoperator gleichgesetzt. Der volle Randdetektor
misst eine andere mittlere Dichte als die materialseitige Maske.

Keine neuen Zufallsstichproben, Punktwolken oder dynamischen CST-Ensembles wurden
erzeugt. Die Wahrscheinlichkeiten sind Gleitkommaauswertungen analytischer
Poissonformeln, keine Intervallzertifikate. Die bisherigen BD-Paarstrom- und
Bounce-Entscheidungen ändern sich nicht. Alle acht physikalischen Vertrags-Gates
bleiben **HOLD**.

## Bericht, Originalpaket und Nachrechnung

- [Bericht als PDF, neun Seiten](../reports/CST_DUST_Staubstrom_Kalibrierung_v0_1.pdf)
- [Unverändertes ursprüngliches Prüf-Paket](../packages/CST_DUST_Staubstrom_Kalibrierung_v0_1_Pruefpaket.zip)
- [Vollständige Herleitung](DERIVATION.md), [eingefrorener Plan](plan.json), [Ergebnisse](results/verification.json)
- [Eigene Regularitätsbewertung und Vertragsprüfung P2](results/checkpoint_P2_audit.json)
- [Getrennte Referenzentscheidungen](results/reference_decisions.json)

Die 38 Originalmitglieder einschließlich PDF und interner Prüfsummen sind hier
bytegleich entpackt. `PUBLICATION.md`, `publication_check.py` und
`publication-requirements.txt` ergänzen den Publikationsrahmen. Der ursprüngliche
Provenienzvermerk „noch nicht publiziert“ dokumentiert den Erstellungszeitpunkt
des unveränderten Pakets; dieses Dokument bezeichnet seine GitHub-Veröffentlichung.

```sh
python3 -m pip install -r research/rax_cqg/dust_collapse/current_calibration_v0_1/publication-requirements.txt
python3 research/rax_cqg/dust_collapse/current_calibration_v0_1/publication_check.py --replay
```

Die Prüfung kontrolliert ZIP, PDF, alle Mitglieder und SHA-256-Werte, die
bytegenauen Elternvertragsquellen, den fixierten Plan und die getrennten
Entscheidungen. Die Nachrechnung erfolgt in einem temporären Verzeichnis und
vergleicht sämtliche Ergebnistabellen und Entscheidungen; die archivierten
Dateien werden nicht überschrieben. Versionsabhängige Laufmetadaten werden
gesondert validiert. Es werden keine zusätzlichen physikalischen Läufe gestartet.

Das nächste offene Bindeglied ist die unabhängige Erzeugung von Strommarken,
Uhr, Oberflächenmaske und Exposition durch den gekoppelten CST-Kandidaten.
Die klassische Randreferenz ersetzt kein dynamisches CST-Anschlussgesetz.
