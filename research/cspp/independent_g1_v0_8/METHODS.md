# Unabhängige G1-Ablehnungsprüfung v0.8

## Zweck und vorab begrenzte Aussage

v0.1 und v0.7 sind Entwicklungsdaten. Sie zeigen große skalare Fehler,
qualifizieren aber keine unabhängige Freigabe. v0.6 liefert unter dem
bisherigen Budget keinen neuen aussichtsreichen Sprinkling-Kandidaten.
Hier werden auf ausdrücklichen Wunsch **alle zwölf alten Parameterzellen**
mit neuen Daten auf eine notwendige G1-Bedingung geprüft. Das ist ein
bezahlbarer unabhängiger Ablehnungsversuch, keine Wiederaufnahme der in
v0.6 ausgeschlossenen Großsimulation und kein neuer Parameteroptimierer.

Ein nachgewiesenes Scheitern der lokalen skalaren Wirkung genügt, um die
jeweilige Zelle als Voraussetzung für Dirac abzulehnen. Ein Nichtverwerfen
genügt nicht für G1. Insbesondere wird keine Obergrenze des Populations-RMS
aus einer unteren Konfidenzgrenze abgeleitet. Die gesamte neue Kampagne
kann G1 deshalb nicht auf PASS setzen. Sie beantwortet die gegenwärtige
Entscheidung, ob die bisherigen Kandidaten unabhängige Gegenbelege erhalten.

## Festgelegte Daten und Physik

Je 64 neue Realisierungen bei nu=512,1024,2048,4096, insgesamt 256 Wolken.
Die drei epsilon=1,1/4,1/16 werden innerhalb jeder Wolke gepaart; das erzeugt
768 Zellrealisierungen, **keine 768 unabhängigen Wolken**. Jede Wolke wird
genau einmal gezogen. Die SeedSequence-Entropie ist
`[2,8,1,d,i,1,202610280801]`, getrennt von den bisherigen Entwicklungsströmen.
Phase2 ist Methodenvalidierung. Der spätere E4-Bestätigungsseed bleibt unbenutzt.
PCG64DXSM, NumPy2.3.5, der unveränderte Poisson-/Volumensampler, Rohkoordinaten
und Hashes der Zufallsrückgaben werden dokumentiert. Das unabhängige
Wolkenmodell ist die Monte-Carlo-Annahme; Pseudozufallsströme beweisen keine
mathematische Unabhängigkeit, und ihre gerundeten Koordinaten sind nicht
mit einem idealen kontinuierlichen Poissonprozess identisch zertifiziert.

Das Gebiet bleibt Omega4: |t|+r<4, V=512pi/3. rho=nu/V wird aus dem
Poissonmittel, niemals aus der beobachteten Punktzahl, berechnet. Quelle,
Detektor und die physikalischen Wellenzahlen werden nicht verändert.
Die lokale Operatorstufe wertet Quelle und Detektor noch nicht aus.

Die zehn vollständigen bisherigen Felder sind chi mal
1,t,z,t²,z²,tz und exp(i(kz-sqrt(k²+1)t)), k=0,2,4,8.
Der unveränderte glatte Cutoff ist chi=h(|t|)h(r), mit h=1 bis1, h=0 ab3
und h=logistic(1/s-1/(1-s)), s=(q-1)/2 dazwischen. Er wird an jedem
Summenknoten ausgewertet. Alle21 festgelegten inneren Proben liegen strikt
im Plateau. Dort verschwinden sämtliche Cutoff-Ableitungen exakt; die
Kontinuumswerte von Box sind 0,0,0,-2,2,0 und die vier Wellen selbst.
Es wird somit kein Cutoff-Term in der Referenz unterschlagen.

Die Probegewichte sind alle1/21. Es wird keine räumliche Quadratur oder
Detektorintegration behauptet. Der Nenner je Feld ist
D=max(RMS_21(phi),RMS_21(Box phi)), L0=1. Er ist positiv, auch für
Kontinuumsfelder mit verschwindender Box. Die Populationsgröße ist
sqrt(E[R²]), R=RMS_21(B_C phi-Box phi)/D. Die Anforderung bleibt <=0,1
für jedes Feld. Ensemble-Mittelamplituden ersetzen diesen RMS nicht.

## Statistischer Ablehnungsnachweis ohne beschränkte RMS-Annahme

Der einzelne RMS kann unter Poisson-Sampling unbeschränkt sein. Deshalb
werden weder eine ungeprüfte Normal-/t-Näherung noch ein Hoeffding-Intervall
für diesen RMS verwendet. Für tau=1/5 gilt punktweise

    R² >= tau² 1{R>tau},
    E[R²] >= tau² p,  p=P(R>tau).

Unter der Nullhypothese sqrt(E[R²])<=1/10 ist folglich p<=1/4.
Es zählen ausschließlich sicher eingeschlossene Überschreitungen R_lower>tau.
Für S solcher Überschreitungen in M=64 wird der exakte obere Binomialtail

    T(S,p)=sum_{j=S}^64 binom(64,j) p^j(1-p)^(64-j)

bei p=1/4 geprüft. Alle Berechnungen des Tails sind rationale Ganzzahlarithmetik.
Die Familienallokation ist alpha=1/40 über J=12*10=120 Tests, also1/4800
pro Test. Ab S=30 wird verworfen; S=29 genügt nicht. Unter p=0,6 beträgt
die exakte Ablehnungswahrscheinlichkeit mehr als0,98. Dies begründet M=64
als feste Größe für einen Ablehnungsversuch, nicht für eine positive
Genauigkeitsqualifikation. Innerhalb einer Wolke abhängige Felder und
epsilon-Zellen sind zulässig: die Vereinigungsabschätzung benötigt dort
keine Unabhängigkeit. Die Realisierungen innerhalb einer Dichte müssen
dem deklarierten unabhängigen Modell entsprechen.

Zusätzlich wird die einseitige Clopper-Pearson-Untergrenze L(S) durch
T(S,L)=1/4800 eingeschlossen. Für S=0 gilt L=0. Eine rationale Bisektion
liefert ein Intervall der Breite2^-72; ausschließlich sein unteres Ende
wird benutzt. Mit gemeinsamer Überdeckung mindestens97,5% gelten über
alle120 Tests die unteren RMS-Grenzen tau*sqrt(L). Die Begriffe
Konfidenzüberdeckung und posteriorer Wahrheitswahrscheinlichkeit werden
nicht gleichgesetzt. Eine Zelle scheitert, wenn mindestens eines ihrer
zehn Felder verworfen wird. Es gibt keine Auswahl eines Zeugen nach der
Auswertung ohne die vollständige Mehrfachtestkorrektur.

Fehlende Ergebnisse zählen als **null sicher nachgewiesene Überschreitungen**
und behalten ihren Platz im festen Nenner64. Das behauptet nicht, ihr
physikalischer Fehler sei null. Für die unbekannte wahre Anzahl K gilt S<=K;
weil L monoton steigt, bleibt L(S)<=L(K) eine konservative Untergrenze,
auch bei ergebnisabhängig fehlenden Daten. Nicht versuchte Fälle nach
Ressourcenabbruch werden genauso behandelt. Es gibt kein Neuziehen,
kein Ersetzen und keine Auswertung nur erfolgreicher Realisierungen.

## Getrennte Rechenfehler

Der neue Test benutzt die genaue diskrete Wirkung auf den kanonisch
gespeicherten dyadischen Koordinaten. Alle benötigten Kausalrelationen
werden nach v0.7 mit nach außen gerundeten binary64-Filtern und bei
unklaren Vorzeichen mit exakter rationaler Arithmetik berechnet. Exakt
nullartige Beziehungen sind durch die strikte Ordnungsregel ausgeschlossen.
Alle Wolke/Wolke-Relationen, alle Wolke/Probe-Relationen, die daraus
gebildeten Probenintervallzahlen und Omega4-Mitgliedschaften werden geprüft.
Volle Knotenintervallzahlen für eine nicht ausgeführte Propagation werden
nicht als geprüft ausgegeben.

Für jeden Probewert werden drei Beiträge getrennt:

    float(B)(phi_float)-Box(phi)
      = [B(phi)-Box(phi)]
      + [B(phi_float)-B(phi)]
      + [float(B)(phi_float)-B(phi_float)].

Der erste enthält den echten diskreten Operatorfehler einschließlich
Gebiet, Nichtlokalität und Sprinkling. Der zweite umfasst die gerundete
Auswertung des Feldes, der dritte Koeffizienten- und Summationsrundung.
Alle Referenzen, Feldwerte und beide exakten B-Wirkungen werden mit Acb
eingeschlossen. Der maximale Komponentenradius ist1e-12; die beiden
normalisierten numerischen Beiträge haben getrennte Obergrenzen1e-8.
Diese Kontrollen ersetzen oder vergrößern die wissenschaftliche10-%-Grenze
nicht. Es gibt in dieser lokalen Stufe keinen linearen Lösungsschritt und
keinen Anfangsdatenadapter. Deren unabhängige Prüfung wird durch eine
gescheiterte notwendige Operatorbedingung nicht vorgetäuscht.

Alle gespeicherten Werte werden bei128 und192Bit berechnet. Überschneidung
prüft die Implementierung; die Einschließung stammt aus der Ballarithmetik,
nicht aus dem bloßen Vergleich zweier Präzisionen. Einzelwerte, Fehlerbeiträge,
Zählhashes, RNG-Ausgaben und vollständige Versuchsliste werden archiviert.

Beide CPU-Konfigurationen regenerieren alle256 Wolken aus denselben
Streams. RNG-Rückgaben müssen bytegleich sein, Koordinaten höchstens2^-48
abweichen, alle benötigten Relationen/Zahlen/Masken exakt übereinstimmen.
Die eigentliche Wirkung wird auf den kanonischen Archiven erneut berechnet;
atol=1e-10,rtol=1e-11 bleiben unverändert. Eine allgemeine bitweise
Koordinatenportabilität oder exakte kontinuierliche Samplinggeometrie
wird nicht behauptet.

## Zeitfolge, Abbruch und Entscheidungsgrenzen

Code, Testfamilie, Budgets, M und Abbruchregeln werden nach Kontrollen auf
synthetischen/alten Daten, aber **vor dem ersten neuen RNG-Aufruf** eingefroren
und in einem eigenen GitHub-Commit publiziert. REGISTRATION.json hält diesen
Commit und seinen Publikationszeitpunkt fest. Ein späterer Replay zieht
keine weiteren wissenschaftlich unabhängigen Daten. Nachträgliche Änderungen
der eingefrorenen Analyse dürften nicht still dieselben Daten als unberührt
behandeln; sie bräuchten einen dokumentierten Methodenabbruch/Amendment.

Ressourcen: eine CPU-Arbeitseinheit,4GiB,21600s, maximal6000 tatsächliche
Punkte pro Wolke. Vor jeder Wolke wird die globale Zeitgrenze geprüft;
ein einzelner bereits begonnener begrenzter Wolkenschritt darf auslaufen.
Der reale Poissondeckel verursacht keinen bedingten Neuversuch.
Alle256 Identitäten und alle zwölf Zellen bleiben auch nach frühen
negativen Befunden im Plan. Es gibt keine optionale statistische Beendigung.
Quellsperren-, CPU- oder Reproduktionsfehler führen zu METHOD_HOLD und
verhindern eine wissenschaftliche Freigabe.

Sind alle Zellen abgelehnt, lautet die spezifische Schlussfolgerung
ALL_TESTED_CELLS_REJECTED. Das allgemeine G1 bleibt HOLD: andere Konstruktionen
sind damit nicht widerlegt. Bei Überlebenden lautet es INCONCLUSIVE_FOR_SURVIVORS.
In beiden Fällen wird Dirac noch nicht begonnen. Eine spätere positive
G1-Qualifikation braucht eine obere Genauigkeitskontrolle, die vollständige
Anfangsdaten-/Propagationskette, die erforderlichen Geometrie- und
Ressourcenbelege sowie einen neuen vorher festgelegten unabhängigen Plan.
Die bisherige spatial integrierte Detektorunsicherheit bleibt für G3 offen.

## Was vor G2 und Flavor folgen muss

Erst ein vollständig bestandenes unabhängiges G1 erlaubt die Arbeit am
fermionischen Kandidaten. G2 verlangt **beides**: direkte Q_C-Wirkung
gegen Q und Q_C² gegen B_C tensor I4. Eine formale Matrixwurzel von B_C
genügt nicht. Es bleiben die Konventionen eta=(-,+,+,+), gamma0=i beta,
gammaj=i beta alphaj, Q²=Box I4 und (Q-m)(Q+m)=Box-m².

Zusätzlich benötigt G2 unabhängige Prüffelder und neue Prüfwolken,
Spin-/Lorentztests auf gemeinsam transformierten Gebieten und Eingaben,
Umnummerierung, Dispersions-/Zusatzmodendiagnose, Norm/Strom, Kausalität
und eigene numerische Fehlerkontrollen. Die bisherigen notwendigen
Grenzen sind0,10 für direkte Wirkung und Quadratvergleich,1e-8 für globale
Normdrift. Ein späterer G2-Freeze muss Kandidat, Prüfer, weitere Toleranzen,
Ensemble und Abbruchregeln konkretisieren; hier wird kein ausführungsreifes
G2-Protokoll vorgetäuscht.

Flavor- und Kohärenzaussagen verlangen anschließend G3: gemeinsame
Geometrie-/Spinstrukturregion, Quellen-/Detektorabbildung und eine einheitliche
Fehlerkette bis zum endlichen Observablenraum. Eine skalare Punktintensität
oder ein erfolgreiches Quadrat allein ersetzt das nicht. Der E4-Vertragsentwurf
und dessen Risikobudgets bleiben unverändert; die2,5% hier gehören ausschließlich
zur eigenständigen G1-Ablehnungsfamilie.

## Quellen

- Unveränderter [E4-Vertrag](../e4_v0_1/PROTOCOL.md), insbesondere Abschnitte5–8.
- [Skalarpilot](../scalar_pilot_v0_1/METHODS.md), [Budgetplanung](../joint_budget_v0_6/METHODS.md),
  [Anfangsdaten und CPU-Regeln](../scalar_propagation_v0_7/METHODS.md).
- NIST, [Exact Binomial](https://itl.nist.gov/div898/software/dataplot/refman2/auxillar/exacbino.htm):
  ein- und zweiseitige exakte Binomialgrenzen. Die rationale Inversion und
  der RMS-Übergang sind oben vollständig angegeben.
- [python-flint: Arb](https://python-flint.readthedocs.io/en/stable/arb.html):
  nach außen gerundete reelle Einschließungen. Für Reproduktionen ist
  ausschließlich die eingefrorene Version0.8.0 maßgeblich.
