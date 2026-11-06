# Korrespondenz vor der Singularität v0.1

**6. November 2026 · CST-DUST-PRE-SINGULARITY-001 · Prüfpunkt P3**

Der physikalische CST-Test bleibt **HOLD_NOT_ELIGIBLE / NOT_RUN**. Der vollständige
gekoppelte Dynamikkern, Messadapter und konkrete physikalische Laufparameter fehlen.
Veröffentlicht werden die vor der Rechnung lokal fixierten Prüfregeln, ausgeführte
klassische Referenzkontrollen und eine bedingte Messbudgetanalyse. Der lokale
Plan-Freeze ist keine externe Präregistrierung.

| Prüfung | Ergebnis | Aussagegrenze |
|---|---|---|
| Toleranz- und Abgleichregeln | 26 Kontrollen bestanden | Metadaten-PASS beweist keine physikalische Gleichwertigkeit |
| Klassische numerische Referenz | 240 Vergleiche, alle analytischen Werte eingeschlossen | Eingesetzte klassische Gleichungen, keine CST-Herleitung |
| Feinste numerische Stufe | Größte relative Fehlerhülle 0,130628 %; Budget 0,5 % | Numerische Zeitschritte, keine physikalischen Dichtestufen |
| Zeitliche Ableitungen aus Volumenzählung | Bisheriges Budget durch die geprüfte konservative Schranke nicht qualifiziert | Hinreichende Hülle, keine notwendige Fehleruntergrenze |
| Physikalische Korrespondenz | **HOLD_NOT_ELIGIBLE / NOT_RUN** | Kein neues dynamisches CST-Ensemble |
| Regularität und Singularitätsauflösung | **HOLD**, eigenständig in allen 60 P3-Datensätzen | Keine uniformen physikalischen Momentenschranken oder kontrollierte Fortsetzung |

## Vorab festgelegte Entscheidungen

Die Toleranzen betragen 5 % für Radius, Dichte, Hubble-Rate und Beschleunigung,
2 % der Gesamtmasse für Masse und integrierten Fluss sowie 2,5 % für die letzten
beiden physikalischen Verfeinerungsstufen. Ein PASS erfordert, dass das vollständige
gemeinsame Unsicherheitsintervall im Toleranzband liegt. Unbekannte Fehleranteile
führen zu HOLD und werden nicht als null eingesetzt. Die geplante Familie umfasst
524 Vergleiche bei gemeinsamem Fehlerrisiko 5 %; sie wurde noch nicht ausgeführt.

Physikalische Zeiten, Messgebiete, Mittelungsskalen und Anfangsdaten müssen über
die geplanten Zähldichteverhältnisse 1, 2, 4 und 8 abgeglichen sein. Eine Änderung
einer fundamentalen Diskretheit ist nicht automatisch ein Regulator-Kontinuumslimes.
Numerische Schrittweite und Ensemblegröße werden separat variiert. Der
[Modellvertrag](../model_contract_v0_1/PUBLICATION.md) und die
[Staubstrom-Kalibrierung](../current_calibration_v0_1/PUBLICATION.md) sind als
unveränderte, mit SHA-256 geprüfte Eingaben enthalten.

## Bericht, Daten und Reproduktion

- [Bericht (PDF, acht Seiten)](../reports/CST_DUST_Korrespondenz_v0_1.pdf)
- [Unverändertes Originalpaket (ZIP)](../packages/CST_DUST_Korrespondenz_v0_1_Pruefpaket.zip)
- [Herleitung und Grenzen](DERIVATION.md), [fixierter Plan](plan.json), [Ergebnisse](results/verification.json)
- [60 getrennte P3-Entscheidungen](results/checkpoint_P3_audits.json)

Vom Repository-Stamm mit Python 3.12:

```sh
python3 -m pip install -r research/rax_cqg/dust_collapse/correspondence_v0_1/requirements.txt
python3 -O -B research/rax_cqg/dust_collapse/correspondence_v0_1/publication_check.py
python3 -B research/rax_cqg/dust_collapse/correspondence_v0_1/publication_check.py --replay
```

Der Publikationscheck prüft Originalarchiv, sämtliche Mitgliedsprüfsummen, PDF,
Vorgängereingaben und alle getrennten physikalischen Entscheidungen. `--replay`
rechnet in einem temporären Verzeichnis nach und vergleicht sämtliche
Ergebnisdateien. Nur tatsächliche Laufzeitversionen und davon abhängige
Manifest-Hashes dürfen sich ändern; die Hash-Verknüpfungen werden neu geprüft.
Gleitkommawerte werden mit enger technischer Reproduktionstoleranz verglichen,
rationale Werte und Entscheidungstexte exakt. Diese technische Toleranz ändert
keinen wissenschaftlichen Grenzwert. Die GitHub-Aktion führt beide Prüfungen aus.

Das Originalpaket und seine expandierten Dateien bleiben unverändert.
`PUBLICATION.md` und `publication_check.py` sind ergänzende Repository-Dateien.
