# Expansion und Trapping v0.1

**6. November 2026 · CST-DUST-EXPANSION-TRAPPING-001 · Prüfpunkt P4**

Untersucht ist die bereits numerisch geprüfte, eingesetzte klassische
Einstein-Staub-Referenz REF-DUST-FB-01 mit endlichem Ball und Vakuumaußenraum.
**Physikalisches CST-Trapping: HOLD_NOT_ELIGIBLE / NOT_RUN. Regularität:
separat HOLD.** Die Referenzrechnung ersetzt weder den fehlenden gekoppelten
CST-Dynamikkern noch die Rekonstruktion und Kalibrierung physikalischer Nullflächen.

## Ergebnisse und Grenzen

Die Staubexpansion `Theta = 3H` beschreibt Volumenkontraktion. Trapping wird
separat über beide zukünftigen Null-Expansionen jeder ganzen runden Sphäre
geprüft. Mit `R0 = 10`, `G = c = 1` und demselben physikalischen Zeitfenster
`0 <= T <= Tend = 5 sqrt(5)/3` ergibt sich:

| Referenzmasse | Runde Symmetrieflächen im festen Fenster |
|---|---|
| M = 1/4 | Keine gefangenen runden Sphären; maximale Oberflächenkompaktheit < 0,055 |
| M = 1 | Keine gefangenen runden Sphären; maximale Oberflächenkompaktheit < 0,243 |
| M = 4 | Erste marginale Sphäre bei T/Tend = 0,5689164944001346 an Rb = 8 = 2M; danach gefangene runde Sphären zwischen RA = 1/abs(H) und 2M |

Der innere marginale Ast im Staub ist **future inner und zeitartig**, der
äußere im Vakuum **future outer und null**. Am gemeinsamen Anfangspunkt gelten
nur einseitige Ableitungen; es wird keine glatte durchgehende marginale Röhre
behauptet. Der klassische Innen-/Rand-/Außenanschluss erfüllt die Darmois-
Bedingungen ohne dünne Oberflächenschicht. Ein CST-Randgesetz ist damit nicht
abgeleitet. Die Abwesenheit gefangener runder Sphären schließt allgemeine
deformierte gefangene Flächen nicht aus.

420 innere Kugelfälle, 420 gebietsgeprüfte Außenraum-Prüfplätze, 216 unabhängige
Flächenableitungen entlang Nullstrahlen, 12 numerische Ereigniseinschließungen,
15 Randprüfungen und 25 Kontrollen sind dokumentiert. Die feinste Euler-Stufe
hat eine maximale absolute Fehlerhülle von 0,001478 für `e = R theta / 2`,
unter dem vorher festgelegten Cap 0,005. Das ist kein relativer Fehler einer
gegen null gehenden Expansion und keine physikalische CST-Dichteverfeinerung.

Eine hypothetische gemeinsame ±5-%-Fehlerbox für H und R lässt bei neun von
105 inneren Kugelfällen das Vorzeichen unentschieden. Sie beschreibt keine
gemessenen CST-Konfidenzintervalle. Der lokale Plan-Freeze vor der Rechnung
ist keine externe Präregistrierung.

**Alle 72 P4-Datensätze bewahren die getrennten physikalischen Gates auf HOLD.**
Dichte und Krümmung sind im festen klassischen Fenster beschränkt. Die spätere
klassische Singularität wird nicht aufgelöst; ein globaler Ereignishorizont
wird aus diesem endlichen Zeitfenster nicht bestimmt. Neue dynamische CST-
Ensembles, Zufallsstichproben und bezahlte Läufe: jeweils null.

## Bericht und Nachrechnung

- [Bericht (PDF, acht Seiten)](../reports/CST_DUST_Expansion_Trapping_v0_1.pdf)
- [Unverändertes Originalpaket (ZIP)](../packages/CST_DUST_Expansion_Trapping_v0_1_Pruefpaket.zip)
- [Herleitung und Quellen](DERIVATION.md), [fixierter Plan](plan.json), [Ergebnisse](results/verification.json)
- [72 getrennte P4-Entscheidungen](results/checkpoint_P4_audits.json)
- Vorgänger: [Modellvertrag](../model_contract_v0_1/PUBLICATION.md), [Stromkalibrierung](../current_calibration_v0_1/PUBLICATION.md), [Korrespondenzprüfung](../correspondence_v0_1/PUBLICATION.md)

Vom Repository-Stamm mit Python 3.12; keine zusätzlichen Pakete erforderlich:

```sh
python3 -O -B research/rax_cqg/dust_collapse/expansion_trapping_v0_1/publication_check.py
python3 -O -B research/rax_cqg/dust_collapse/expansion_trapping_v0_1/publication_check.py --replay
```

Der Publikationscheck prüft das ursprüngliche ZIP, alle 40 Archivmitglieder,
vollständige SHA-256-Verknüpfungen, PDF, Vorgängereingaben, eingefrorenen Plan
und getrennte physikalische Entscheidungen. `--replay` rechnet in einem
temporären Verzeichnis nach und vergleicht alle 17 Ergebnisdateien exakt.
Nur die tatsächliche Python-Laufzeitversion und die daraus neu berechneten
Manifest-Verknüpfungen dürfen abweichen; deren Integrität wird separat geprüft.
Die GitHub-Aktion führt beide Prüfungen aus. Optimiertes Python (`-O`)
deaktiviert keine Kontrolle.

Das Originalpaket und seine expandierten Dateien sind unverändert.
`PUBLICATION.md` und `publication_check.py` ergänzen sie für das Repository.
