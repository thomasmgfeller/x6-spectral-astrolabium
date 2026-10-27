# CSPP: eingeschlossenes Bias-/Varianzbudget v0.3

**Der nächste Schritt ist berechnet. G1 bleibt HOLD.** Ein Gauß-Testfeld
besitzt jetzt einen mit Intervallarithmetik eingeschlossenen Erwartungswert.
Eine hergeleitete Varianzobergrenze berücksichtigt, dass gemeinsame
Sprinkling-Punkte mehrere Intervallzählungen gleichzeitig ändern. Zusätzlich
sind die Normierung der kompakten Quelle und 34 Kontinuumsamplituden
einschließlich Quadratur- und Abschneidefehler eingeschlossen.

## Konkrete Entscheidung aus dem Budget

Für φ=exp[−(t²+r²)/8] am Ursprung gilt □φ=−1/2. Alle Tabellenzahlen sind
gerundete Anzeigen; die maschinenlesbaren Einschließungen stehen in
[BUDGET.json](results/BUDGET.json).

| ℓk | Gewähltes H | Relativer Bias zum unendlichen Gebiet | Erwartete Punkte allein für ε≤1 in diesem D_H |
|---:|---:|---:|---:|
| 0,125 | 20 | 3,9564 % | 85.786.423 |
| 0,1875 | 20 | 7,3043 % | 16.945.466 |
| 0,25 | 20 | 11,0272 % | 5.361.651 |
| 0,5 | 16 | 26,6261 % | 137.258 |
| 1 | 16 | 50,5024 % | 8.579 |
| 1,5 | 16 | 62,5530 % | 1.695 |
| 2 | 16 | 68,2888 % | 536 |

ℓk=0,125 erfüllt als einziger **geprüfter** Wert die festgelegte
5%-Bias-Zuteilung. Die Grenze ε=ℓk⁻⁴/ρ≤1 erfordert dort im gewählten D20
bereits etwa **85,8 Millionen erwartete Punkte**. Das ist eine notwendige
Zulässigkeitsbedingung für diesen Operator und dieses Gebiet, noch keine
Genauigkeitsgarantie. Das Gebiet wurde konservativ aus einer festen Liste
nach einer Randfehlerschranke gewählt; es ist nicht als minimal bewiesen.

Für die fünf geprüften Skalen **ℓk≥0,25** liegt selbst die eingeschlossene
Untergrenze des endlichen Bias über 10 %. Deshalb kann höhere Dichte allein
das 10%-RMS-Ziel für diesen Zeugen in den jeweils gewählten Gebieten nicht
erreichen. Dieser begrenzte Ausschluss gilt nicht für alle möglichen
Operatoren, Randbehandlungen oder Testfelder.

Die konservative Varianzschranke liefert bei ℓk=0,125 eine hinreichende Dichte,
deren Gebiet etwa **2,87×10³⁹ erwartete Punkte** enthalten würde. Damit wäre
das gemeinsame RMS-Ziel mathematisch abgesichert, aber dieses Budget ist
praktisch unbrauchbar. **Dies ist keine notwendige Punktzahl und kein
Unmöglichkeitsbeweis.** Es zeigt, dass die gleichmäßige Varianzhülle stark
verschärft werden muss, bevor sie eine Rechenfreigabe begründen kann.
Ein RMS-Ziel ist zudem keine gleich hohe Wahrscheinlichkeitsschranke.

## Quellenreferenz: ein klar abgegrenzter Teil ist jetzt eingeschlossen

Die ursprüngliche kompakte Quelle, Anfangszeit und Anfangsgeschwindigkeit
bleiben unverändert. Berechnet wurden:

- Die Quellennormierung A=9,1238298263738545666… einschließlich Integralrest.
- Alle **28 masselosen** Referenzproben.
- Weitere **sechs massive** Amplituden: m=1,2 an den drei Zentrumsproben.

Der größte Radius einer gespeicherten Real- oder Imaginärkomponente beträgt
etwa **3,60×10⁻²²**, einschließlich der expliziten abgeschnittenen Quellränder.
Der vorab festgelegte Radius 10⁻¹² wird an allen 34 Werten unterschritten.
Die bisherige feine Ortsraumrechnung weicht dort höchstens etwa 8,53×10⁻¹⁵ ab.
Diese Übereinstimmung ist eine Gegenprüfung; sie begründet die neuen
Einschließungen nicht selbst.

**Offen bleiben die massiven Proben außerhalb des Zentrums**, die übrigen
archivierten Abfragepunkte, eine globale Lösungsnorm und der Fehlertransport
zur Detektor-Dichtematrix. Der volle Referenzstatus bleibt HOLD. Die neuen
Gauß-Ergebnisse ersetzen außerdem keine E4-G1-Testfamilie.

## Prüfung und Reproduktion

Der Audit prüft 260 exakte rationale Gewichtungs- und Kopplungsfälle, drei
Diamantmomente, sechs unabhängige Bessel-Integralidentitäten, 27 exakte
KG-Ebenenwellen, sechs falsche-Vorzeichen-Kontrollen sowie Support,
Anfangsdaten, Symmetrien und unzulässige Eingaben. Alle sieben Budgetzeilen
und 34 Amplituden wurden mit **160 statt 128 Bit** erneut eingeschlossen.
Keine neuen Zufallswolken und kein Bestätigungsseed wurden verwendet.

```sh
python3 -m pip install python-flint==0.8.0 numpy==2.3.5
python3 -O -B research/cspp/certified_budget_v0_3/verify_publication.py
python3 -B research/cspp/certified_budget_v0_3/audit.py --replay
python3 -B research/cspp/certified_budget_v0_3/run.py all --out /tmp/cspp-budget-replay
```

Python 3.12 und das FLINT-3.3.1-Wheel sind festgehalten. Eine reine
Auditkorrektur ist mit Originalfassung und unveränderten Produktionshashes
in [Amendment 01](amendment_01/RECORD.json) dokumentiert.

## Nächster fachlicher Schritt

Die Varianzhülle sollte die Feldabnahme und die tatsächlichen gemeinsamen
Intervallbeiträge ausnutzen. Parallel ist die validierte Referenz auf die
massiven, nichtzentralen E4-Proben zu erweitern. Erst danach lässt sich ein
begründetes Sprinkling-Rechenbudget festlegen. G1 bleibt HOLD, G2/G3 NOT_RUN.

Nachweise: [vollständige Herleitung](METHODS.md), [Protokoll](PROTOCOL.json),
[Quellsperre](FREEZE.json), [Quellen-Einschließungen](results/SOURCE.json),
[Audit](AUDIT.json), [Laufumgebung](results/COMPUTE.json), [Prüfsummen](SHA256SUMS).
