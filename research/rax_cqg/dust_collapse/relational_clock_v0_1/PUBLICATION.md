# Relationale Materieuhr und Kandidatenprüfung v0.1

Veröffentlichtes Arbeitspaket vom 7. November 2026. Ausgangspunkt ist
Main `5e08cef8dcac5c7d1214dd2beff1b1533427e856` nach PR 251.

## Ergebnis und Geltungsbereich

Auf dem ausgewählten kausal monotonen Uhrsektor ist der relationale Schnitt
`J_tau = {x: T_x <= tau}` ein labelkovariantes Ordnungsideal. Chronologisches
Sortieren aller Uhr- und Materiemarken hebt die natürliche Multiplizität
exakt auf: Die chronologische Historienamplitude trägt den Koeffizienten
eins, nicht nochmals `1/e(P)`. Die Auswahl des Uhrsektors selbst ist eine
Modellbeschränkung und keine reine Eichwahl. Die Äquivalenz der vollständigen
festen-m-Summen beweist keine unitäre Konjugation der früheren beliebigen
Präfixfortsetzung.

Ein expliziter lokaler L2-Präparationskandidat liefert beim Anhängen genau
eines chronologisch späteren Elements den Normmultiplikator
`r(P,T_max) = |Ideals(P)| (L-T_max)/(2L)`. Zwei normierte positive
Staubpräparationen ergeben Ausgangsnormen zum Quadrat **5/4** und **3/4**.
Der allgemeinere Beweis schließt auf den vollständigen erklärten
Stufenräumen für m >= 1 jede Isometrie mit beschränktem positivem
Kindprodukt und koerzivem positivem Elternprodukt aus, auch bei
nichtdiagonalen feldabhängigen Produkten. Eine Folge normierter Pakete
nahe dem Uhrregulator hat Ausgangsnorm gegen null.

**Der konkrete geschlossene Ein-Geburts-Kandidat ist FAIL.** Das ist kein
allgemeines No-go für CST oder Staubuhren. Eingeschränkte physikalische Räume,
singuläre beziehungsweise nichtkoerzive Produkte, geänderte Amplituden und
variable Elementzahlen sind nicht ausgeschlossen. Der Uhrregulator ist keine
physikalische Singularität. Die neue chronologische Intervallbeschränkung
ändert eine Voraussetzung des Normsatzes im Vorgängerpaket.

Ein Hilfsinstrument mit den Ausgängen „Geburt“ und „keine Geburt“ lässt sich
positiv vervollständigen. Seine freie relative Gewichtung und eine physikalische
Wartezeit sind aber nicht hergeleitet. Ein weiterer exakter Gegenbeleg zeigt:
Eine stationäre alte freie Uhr bleibt beim Anhängen eines neuen Elements
nicht automatisch stationär, selbst wenn dessen Dichtegleichung erfüllt ist.
Das ist keine Aussage über physikalische Akausalität oder bereits hergeleitete
kanonische Quantenconstraints.

**MODEL, CURRENT, CORRESPONDENCE, BOUNCE, REGULARITY, BOUNDARY, TRAPPING und
EXTENSION bleiben jeweils HOLD.** Physikalische Zustands-/Produktauswahl,
globale Vakuumuhr, Quantenmaß-Fortsetzung, Junction-Gesetz und globaler Bounce
bleiben offen. Historische kandidatenspezifische FAILs bleiben erhalten.

## Artefakte

- [Bericht (PDF)](../reports/CST_DUST_Relationale_Uhr_Kandidatenpruefung_v0_1.pdf)
- [Originales Prüfpaket (ZIP)](../packages/CST_DUST_Relationale_Uhr_Kandidatenpruefung_v0_1_Pruefpaket.zip)
- [Vollständige Herleitung und Voraussetzungen](DERIVATION.md)
- [Maschinenlesbarer Kandidatenvertrag](clock_contract.json)
- [Nachrechnung und Nutzung](README.md)
- [Exakte Ergebnisse und Status](results/verification.json)

## Verifikation

88.324 akzeptierte natürliche markierte Darstellungen, 14.704 chronologische
Datensätze, 88.324 offene und geschlossene Wirkungskovarianzprüfungen,
29.440 Uhrschnittprüfungen, 350 Wellenpaketkontrollen und 250 punktweise
Instrumentkontrollen sind exakt nachgerechnet. Die endlichen Uhrgitter und
binären Dichtemarken sind eigenständige Kontrollmaße; sie sind keine
zertifizierte Quadratur des kontinuierlichen Pfadintegrals und keine
physikalischen 4D-Ensembles. Allgemeine Aussagen sind analytisch bewiesen;
es wurde kein formaler Beweisassistent eingesetzt.

Vom Repository-Stamm aus, Python 3.10 oder neuer, keine Zusatzpakete:

```bash
python3 -O -B research/rax_cqg/dust_collapse/relational_clock_v0_1/publication_check.py --replay
```

Der Prüfer kontrolliert das unveränderte Archiv mit allen 30 Mitgliedern,
29 Manifest-Prüfsummen, beide PDF-Kopien, den eingefrorenen Plan, sechs
bytegleiche Repositoryquellen und die abgegrenzten Ergebnisansprüche.
Sechs Ergebnisdateien werden in einem frischen Verzeichnis bytegleich
reproduziert. Wiederholbarkeit ist keine unabhängige wissenschaftliche
Replikation. Der Workflow `cst-dust-relational-clock.yml` führt die Prüfung
auf Pull Requests und Main aus.

| Objekt | SHA-256 |
|---|---|
| Original ZIP | `d7788615b01c9bbb040a8b1834545c981b311b0d19b4c02ecd3bbfe88d9c204d` |
| PDF | `4187a735c9357dfc3e1ee1a0cf1e432f5b6493a16904b760986ab6d8089152d1` |
| Plan | `379d6101c9fb29f8faf5847919e44e83b0292ff30a15446f1160ebb43eccfa0e` |

Die Originaldateien bleiben unverändert. Publikationsnotiz, Repository-Prüfer,
Workflow und Index-/Integritätsdateien werden separat ergänzt.

## Nächster physikalischer Schritt

Eine Zuordnung zwischen festen relationalen Uhrwerten konstruieren, die
variable Elementzahlen und keine, eine oder mehrere Geburten gemeinsam
behandelt. Relative Gewichte, Randzustände, Ereignisse und Komposition müssen
aus einer begründeten Quantendefinition stammen. Ein beliebiger positiver
Instrumentabschluss allein legt diese Physik nicht fest.
