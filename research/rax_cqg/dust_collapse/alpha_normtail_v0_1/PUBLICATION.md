# α-abhängige Normrestschranke v0.1

Arbeitspaket vom 7. November 2026. Ausgangsbasis ist Main nach PR 257,
Commit `0067da907da4ea8df5b625ea9f8f99ce1527e9ed`.

## Ergebnis und Geltungsbereich

Die bisherige Normrestschranke des Vier-Element-Referenzmodells nutzte weder
die zusätzliche Unterdrückung durch α>1 noch die exakt gezählten Ordnungen.
Ein kombinatorischer Beweis verbindet nun die Schranke auf Vergangenheitideale
mit der geerbten Zahlgewichtung. Die 4824 Sechs-Element-Ordnungen liefern
zusätzlich den exakten Faktor `603/4096` gegenüber der universellen α-Grenze.

Die obere Gewichtsschranke für die gesamten unbekannten Phasensektoren sinkt
um weitere **81,85–94,91 % bei α=2** und **0,37–1,47 % bei α=1**.
Alle bisherigen Feldamplituden und Fehler bleiben unverändert; es werden
keine neuen Feldintegrale berechnet. Die viel stärkere Reduktion der reinen
Normrestschranke bei α=2 darf nicht mit diesem gesamten Phasenrest verwechselt
werden: Die unbekannten Feldphasen n=5,6 bleiben enthalten.

Alle 36 Zahlkanal- und kohärenten Erfolgsintervalle liegen innerhalb ihrer
Vorgänger. Auch 180 bedingte Ausleseintervalle bleiben eingeschlossen.
Rohintervall und Schnitt mit der gültigen Vorgängergrenze werden für den
kohärenten Kanal getrennt gespeichert. Der phasenfreie Fall bleibt exakt eins.

Der Satz gilt für reelle α≥1 und einen geometrischen Restquotienten kleiner
als eins. Die Implementierung verwendet ganzzahlige α≥1 und exakte rationale
Arithmetik. Eine Schlussfolgerung über alle α<1 wird nicht behauptet.
Die vollständige Enumeration bis n=7 dient nur der Validierung; die
Produktionsnormierung bleibt bei n≤6, die Feldintegration bei n≤4.
Unbegrenzt ist die Elementzahlsumme bei festem endlichem Uhrhorizont, nicht die Zeit.

**MODEL, CURRENT, CORRESPONDENCE, BOUNCE, REGULARITY, BOUNDARY, TRAPPING und
EXTENSION bleiben HOLD.** Die physikalische Begründung von α, Dichtemaß,
kohärentem Historienzugriff und Randwahl bleibt offen. Keine vollständige
vierdimensionale CST-Dynamik, Rückwirkung, Singularitätsauflösung, Bounce
oder Junction werden hergeleitet.

## Artefakte

- [Bericht (PDF)](../reports/CST_DUST_Alpha_Abhaengige_Normrestschranke_v0_1.pdf)
- [Originales Prüfpaket (ZIP)](../packages/CST_DUST_Alpha_Abhaengige_Normrestschranke_v0_1_Pruefpaket.zip)
- [Vollständiger Beweis und Ergebnisinterpretation](DERIVATION.md)
- [Maschinenlesbarer Vertrag](alpha_normtail_contract.json)
- [Nachrechnung](README.md)
- [Ergebnisstatus](results/verification.json)
- [Vergleich der Schranken](results/improvement_summary.json)
- [Alle 36 verfeinerten Parameterfälle](results/refined_results.json)

## Verifikation

Zwei vollständige Enumerationswege liefern dieselben natürlichen Ordnungen
für n=0,...,7. Die endlichen Kontrollen bestätigen 157 gültige rationale
Parameter-/Cutoff-Fälle; elf ungültige Restquotienten werden zurückgewiesen.
7536 Majorantenschritte kontrollieren Rekurrenz, monotone Quotienten und
geometrische Domination. Der unendliche Beweis beruht auf der Präfix-Ideal-
Bijektion und der geometrischen Reihe, nicht auf einer Extrapolation dieser Tests.

Falsche Varianten mit α statt α-1 im Fortsetzungsquotienten oder fehlendem
N6-Faktor unterschreiten bereits die exakt gezählte n=7-Masse und werden
zurückgewiesen. Weitere Negativkontrollen betreffen ungültige Domänen.
Fünf neue Ergebnisdateien werden in einem frischen Verzeichnis bytegleich
reproduziert. Das ist interne Wiederholbarkeit, keine externe Replikation
oder formale Beweisassistenzprüfung.

Vom Repository-Stamm, mit Python 3.12 und Standardbibliothek:

```bash
python3 -B research/rax_cqg/dust_collapse/alpha_normtail_v0_1/publication_check.py --replay
```

Der Prüfer kontrolliert das unveränderte Originalarchiv, 31 Mitglieder,
30 Manifest-Prüfsummen, beide PDF-Kopien, den eingefrorenen Plan, acht
bytegleiche Repositoryquellen sowie Ergebnis- und Aussageumfang.
Der Workflow `cst-dust-alpha-normtail.yml` führt Integrität und Replay auf
Pull Requests und Main aus. Die Nachrechnung benötigt keinen C++-Compiler
und startet keine neuen Feldintegrale. Ihr Prozesszeitlimit beträgt 180 Sekunden.
ReportLab und DejaVu Sans sind nur zum optionalen Neubau des Berichts nötig.

| Objekt | SHA-256 |
|---|---|
| Original ZIP | `30f519f3db1197933f32ca5cbf5eef908231f7000e08879ddbb9da250c716835` |
| PDF | `b18c24053a8a0eefe7b4f3cd4310c6c89a37360dd276c73296b9b83ac2f5f1ef` |
| Plan | `3e02c09940c35349fbf64374bb22466e2e1189355c0c632c911007b6303eba78` |

Alle Originaldateien bleiben unverändert. Publikationsnotiz, Repository-Prüfer,
CI und Index-/Integritätsdateien ergänzen das Paket. Der Plan wurde nach
symbolischer Beweisplanung und vor neuen Zahlenwerten und Implementierung
lokal eingefroren; keine externe Präregistrierung wird behauptet.

## Nächste wissenschaftliche Grenze

Jetzt entfallen etwa 96,35–99,95 % der verbleibenden oberen Restmasse auf
den n=5-Sektor. Dies betrifft die konservative Unsicherheitsbilanz und ist
keine gemessene Elementzahlverteilung. Der nächste quantitative Kandidat ist
eine Kosten- und Fehlerentscheidung für die n=5-Feldintegration. Die
physikalische Begründung des Modells bleibt davon getrennt offen.
