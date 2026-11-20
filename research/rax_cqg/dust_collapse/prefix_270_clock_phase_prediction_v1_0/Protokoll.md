# Vorregistrierung des Staubuhr-Transfertests am Präfix 270

**Primäre Vorhersage.** Sechs Phasenumkehrungen in jedem der zwei Staubuhrlappen senken das äussere skalare Normquadrat bei den Dichten 1/8 und 1/4 jeweils auf höchstens **1 %** seines Referenzwerts. Die Vorhersage gilt für alle von null verschiedenen komplexen Gewichtsvektoren der elf Endtypen, mit identischem Vektor für Referenz und Ziel. Stand bei Festlegung ist **REGISTERED / NOT_RUN**. Die Vorhersage setzt die seit dem Test am Präfix 1564 publizierte Maske und Entscheidungsschwelle fort.

## Auswahl der Geometrie

Beim bisherigen Ein-Kanten-Präfix 1564 überspannten zehn Endtypen den Testraum. Aus der veröffentlichten Pfadinzidenz wird der kleinste markierte Code aus der N11-Kettenfamilie gewählt, dessen innere Fünferordnung zu 1564 nicht isomorph ist und der mindestens zwei Endtypen mit vollständig disjunktem Träger besitzt. Die Knotenabstände im Binärcode verwenden wie im Rangtest sechs Stellen. Isomorphie wird durch Minimierung über alle 5! Umbenennungen der fünf inneren Ereignisse geprüft. Die Auswahl benötigt weder Referenzamplituden noch modulierte Amplituden.

Unter 70 zulässigen Präfixcodes erfüllt **270** die Auswahlregel als erster. Seine 15 markierten Pfade erreichen 623, 662, 718, 726, 751, 760, 764, 767, 5295, 5307 und 26935. Die kanonischen Präfixcodes lauten 270 und 796. Die tatsächliche Zahl elf bestimmt die Dimension des komplexen Testraums. Es wird kein Ersatzpräfix gewählt.

## Präparation und Prüfgrösse

Randkoordinaten, innere Dichten und Uhren, gravitative Phase, skalare Gauss-Präparation sowie der Verzicht auf Endpostselektion bzw. nachträgliche Normierung entsprechen dem ursprünglichen Test. Die modulierte äussere Uhr ist T₃ = −2Δ + h/16 + u/32 mit h = ±1, Δ = √(2/(19β)), β = 4/√6 und −1 ≤ u ≤ 1. Für beide Lappen gilt s(u) = sgn(64u⁶ − 80u⁴ + 24u² − 1). An den sechs Nullstellen darf s = +1 gesetzt werden. Von links nach rechts lauten die sieben Vorzeichen +, −, +, −, +, −, +. Die punktweise Eingangsintensität und die beiden Lappenbreiten bleiben so erhalten.

Mit der gemeinsamen skalaren Gram-Matrix G und den Uhrfaktoren Dₛ = diag(Zₛⱼ), D₀ = diag(Z₀ⱼ) ist die Prüfgrösse das Maximum über beide Dichten und das Supremum über q ≠ 0 von q†Dₛ†GDₛq/(q†D₀†GD₀q). Die Gravitation wird in jedem Z genau einmal berücksichtigt. Die Referenz ist die kohärente Paarung ohne Modulation.

## Qualifikation vor der Zielrechnung

Das neue Gram-Zertifikat rekonstruiert elf normierte skalare Randzustände. 55 paarweise Betragsabschätzungen und die Zeilensummen liefern exakt gI ≤ G ≤ HI mit g = 8459551/10000000 und H = 11540449/10000000. Die vier Endtypen mit einer Delta-Bedingung werden bei der Randpaarung berücksichtigt. Alle kompletten skalaren Ausgänge sind im verwendeten Testraum zulässig.

Jeder Endtyp wurde ohne Phasenwechsel mit dem vollständigen Gaussgitter berechnet. Alle 22 Referenzfehlerkreise sind von null getrennt. Die kleinsten zertifizierten unteren Betragsgrenzen über die elf Endtypen betragen mehr als 0,0083371 und 0,0082796 bei den beiden Dichten. Ein separat implementierter Archivkontraktor stimmt je Endtyp auf identischem kleinem Uhrgitter für beide Dichten bis 2·10⁻¹⁴ mit dem eingesetzten Integrator überein. Acht Graphen verwenden drei separierbare Endzeiten nach Fixieren der ersten drei Zeiten. Bei den weiteren drei Graphen separieren die übrigen Endzeiten beim Fixieren der Zeit und Dichte eines breiten Endknotens.

Die Begründung der Fehlerkreise steht im eingebetteten Ursprungsarchiv in Numerik.md. Für diese elf Geometrien werden die Voraussetzungen zu Graphzerlegung, Quadraturordnungen, Knoten und Gewichten, Winkelbereich, Termanzahl und ganzzahligen Kopplungen geprüft. Jede der höchstens acht Quadraturkoordinaten trägt im normierten Lappen höchstens 1/32768 bei. Die Auswertung verwendet das gleiche IEEE-binary64-Schema und den absoluten Auswertungszuschlag 1/5000. Der ganze Lappenfaktor ist betragsmässig kleiner als 37/1000 für beide Lappen zusammen. Der Radius der unmodulierten Referenz ist 1/60000.

Die sechs Vorzeichenwechsel werden wie im ursprünglichen Protokoll durch rationale Bisektion lokalisiert. Für alle 77 neuen Teilintervalle gilt mit u=p+hv die unveränderte Schranke h(B+2A|p|) ≤ B für die lineare Phasenrate und Ah² ≤ A für die quadratische. Die Summe der positiven Halbbreiten ist eins. Die Unsicherheit der sechs Vorzeichenwechsel beträgt im normierten Mittel höchstens 6·2⁻⁵¹. Für zusätzliche Produkte und Summen gilt ein Zuschlag 10⁻⁸. Damit bleibt der gemeinsame absolute Ziel- und Kontrollradius unter 1/50000. Der festgelegte Auswerter setzt konservativ genau 1/50000 an.

## Reichweite der Vorhersage

Der Vorzeichenfilter löscht im gleichverteilten Lappenmittel Polynome bis einschliesslich Grad fünf aus. Schon die unmodulierten Referenznenner, die Gram-Schranke und die Phasenableitungen liefern eine Vorausschranke. Mit A und B aus der neuen Referenz ergibt sich pro Endtyp

$$
C_j=\frac1{64}\sum_{k=0}^{3}\frac{A_j^k(2A_j+B_j)^{6-2k}}{k!(6-2k)!},\qquad
\sup_q R_\rho(q)\le\frac H g\max_j \frac{C_j^2}{768\,m_{j\rho}^2}.
$$

Dabei ist m die untere Referenz-Betragsgrenze. Die rationalen Werte in qualification.json liefern nach oben gerundet **0,061613 %** bzw. **0,062473 %**. Dies sind Referenzprognosen vor der neuen Zielintegration. Der registrierte Test wird ausschliesslich anhand der neuen komplexen Zieleinschliessungen gewertet. Diese Art der Replikation prüft den Transfer des endlichen Randmodells und seines Rechenwegs. Eine Trennung der geometrischen Wirkung vom allgemeinen Filtereffekt erfordert ein eigenes Vergleichsdesign.

## Entscheidung im späteren Ziellauf

Bei beiden Dichten sind je elf Zielamplituden erforderlich. Im selben Gitter müssen alle 22 Kontrollen mit positiven Vorzeichen über die sieben Segmente ihren archivierten Referenzfehlerkreis überlappen. Für Zielbetragsgrenzen lⱼ, uⱼ und die alten Referenzgrenzen mⱼ, Mⱼ setzt der Auswerter Lρ = maxⱼ (lⱼ/Mⱼ)² und Uρ = (H/g) maxⱼ (uⱼ/mⱼ)². Die Untergrenze folgt aus den Einheitsvektoren des Testraums. Die obere gilt für den gesamten komplexen Testraum.

| Entscheidung | Kriterium |
| --- | --- |
| PASS | Vollständiger qualifizierter Lauf und Uρ ≤ 1/100 bei beiden Dichten. |
| FAIL | Vollständiger qualifizierter Lauf und Lρ > 1/100 bei mindestens einer Dichte. |
| HOLD | Unvollständige Daten, ungültige Kontrolle, technische oder numerische Verletzung des Fehlerbudgets oder durch die Einschliessungen offenbleibende Entscheidung. |

Bei HOLD wird der Grund dokumentiert. Änderungen der Geometrie, des Fehlerkriteriums, der Maske oder des Auswerters erfordern eine neue Registrierung. Die physikalische Auswahl der Historiengewichte, Etappe 6 und P3 bleiben eigenständige offene Fragen.

[Vorregistrierung am Präfix 1564](https://github.com/thomasmgfeller/x6-spectral-astrolabium/blob/357a3214355ed56dd9e6b887c322278701f15145/research/rax_cqg/dust_collapse/prefix_1564_clock_phase_prediction_v1_0/Protokoll.md) · [Ergebnis am Präfix 1564](https://github.com/thomasmgfeller/x6-spectral-astrolabium/blob/8723cba93224931a6fdffc525c798524ab38bebb/research/rax_cqg/dust_collapse/prefix_1564_clock_phase_run_001/README.md)
