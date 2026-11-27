# CST-DUST · Können kohärente «Quantenpixel» den Arealradius messen?

**Befund.** Eine phasenempfindliche Messung ist ein sinnvoller Forschungsansatz. Die veröffentlichten Gewichtsdaten identifizieren die physische N22-Entropie für keine der drei Präparationen. Für jede festgehaltene Präparation besitzen die zwei kinematischen Kugeln dieselbe archivierte Ordnung, dieselben Felder und dieselben Wirkungswerte. Jede von diesen Eingaben allein abhängige Zustandsregel und jede auf beiden Kugeln identisch implementierte Messung liefert daher denselben Ausgang. Das ist eine Aussage über die vorliegenden Eingaben. Für eine künftig hergeleitete, von der Materialgrenze beeinflusste Quantendynamik ist die Empfindlichkeit offen.

## Ausführen

Nach dem Entpacken im Hauptverzeichnis mit Python ab 3.10 ausführen.

    python3 -B pruefen.py

Für die zusätzliche exakte Routine für beliebige komplexe Amplitudenmatrizen in vollständig vorgegebenen Produktbasen ist SymPy erforderlich (geprüft mit Version 1.14.0).

    python3 -B pruefen.py --mit-sympy

Der Standardlauf umfasst eine unabhängige Implementierung für rational-komplexe Amplituden in orthonormalen Produktbasen. Die Ausgaben werden mit den vollständigen Ergebnisregistern verglichen. Bei der Phasenkontrolle vergleicht der Prüfer sein Rechenergebnis intern. Alle physischen Entropien, der physische Spurabstand und die physische Radius-Fisher-Information sind im Register ausdrücklich unbekannt (null im JSON bedeutet hier fehlender Messwert). Die acht Pilotradien und die 60 P3-Punkte stehen auf NOT_RUN.

## Wie die zwei vorgeschlagenen Tests ausgehen

Unter der **zusätzlichen** Ereignisauswahl p=w18/(w18+w19) lässt sich für schwer und leicht die klassische Streuung 2p(1−p) unterscheiden. Jeweils beide Ereignisse sind in derselben Geschichte besetzt. Aus den Gewichtsboxen folgen rationale Intervalle. In einem explizit angenommenen viermodigen Einteilchenzustand mit Amplitudenbeträgen proportional zur Quadratwurzel der Fenstergewichte verbleibt beim Split {18,19}|{17,20} die ganze Anregung auf Seite 1. Sein reduzierter Zustand ist rein. Vollständiger Nullstaub liefert keine normierte Einteilchenanregung. Man kann im Fockraum zusätzlich den normierten leeren Produktzustand definieren. Andere Quantenfelder können im Vakuum räumlich verschränkt sein.

| Auslese | Schwer | Leicht | Separater Nullstaub |
|---|---:|---:|---|
| Klassische Streuung aus zwei Gewichten, gerundet | 0,388350908 | 0,385538983 | 0/0 |
| Explizite Einteilchenkontrolle, besetzte gegen leere Fenstermoden | 0 | 0 | Zustandsdefinition für den Nullteilchensektor erforderlich |
| Physische Innen-/Aussen-Verschränkung auf N22 | offen | offen | offen |

Alternativ führt der durch uns eingeführte Zustand sqrt(p)|18⟩|r18⟩ + sqrt(1−p)|19⟩|r19⟩ mit normierten Markern zur Entropie 2p(1−p)(1−|⟨r18|r19⟩|²) nach Ausspuren des Markers. Beides sind Ereignislabels im Modellregister. Das zweite Register ist eine hypothetische Aufzeichnung. Für orthogonale Aufzeichnungen ergeben sich die beiden verschiedenen klassischen Zahlen, für identische Aufzeichnungen zweimal null. Der Vergleich Radius 1 gegen 357/200 bei identischer Vorbereitung ergibt für jeden festgehaltenen Marker in beiden Fällen denselben Wert. Ergebnisdateien Radiuspruefung.json und vergleich/Ergebnis.json enthalten die vollen rationalen Grenzen. Das Beispiel zeigt, wie getrennte «Massenwerte» durch Wahl einer Auslese entstehen können und zugleich die Radiusfrage offenlassen.

## Was für eine partielle Spur benötigt wird

Ein Ortsindex auf einer Kausalordnung ist noch kein Hilbertfaktor. Unter der vorgeschlagenen Regel «18,19 und ihre Vorgänger» gehören die beiden als aussen eingeplanten Punkte 17 und 20 bereits zu innen. Die vier Fensterpunkte liegen auf verschiedenen Uhren, einschliesslich der strikten Relationen 17 vor 18 und 20 vor 18. Die vier späten Kragengewichte sind überdies positiv. Die räumliche Aussenalgebra und die Identifikation eines festen Schnitts sind gesondert herzuleiten. Eine begründete Faktorisierung auf dem physikalischen Raum oder eine operational definierte Algebra samt Zustandsrestriktion könnte die benötigte Information liefern.

Für einen *gegebenen* reinen Produktbasiszustand mit Koeffizientenmatrix C und positiv definiten Gram-Matrizen G_I,G_A setzt der Prototyp K=C G_Aᵀ C† G_I und berechnet S_lin=1−tr(K²)/tr(K)². Bei halbdefiniter Paarung erfordert dies zunächst den begründeten physikalischen Quotienten und die darauf definierte Teilstruktur. Abstrakt ist |ψ⟩⟨ψ|/⟨ψ|ψ⟩ korrekt. In den Koordinaten einer nichtorthogonalen Basis operiert der Gesamtdichteoperator als q q†G/(q†Gq). Bei Fluktuationen erfordern zudem erwarteter Arealradius und Wurzel der erwarteten Fläche eine getrennte Definition.

Ein Vierzustandsbeispiel verwendet die Amplitudenmatrix C=(1/2)[[1,1],[1,exp(iθ)]]. Für jedes θ sind alle vier gemeinsamen Messwahrscheinlichkeiten 1/4. Für θ=0 ist S_lin=0, für θ=π ist S_lin=1/2. Bei θ=π/4 entsteht (2−√2)/8. Rationale Messwahrscheinlichkeiten beweisen also auch bei einer festgelegten Produktbasis keine rationale Verschränkungsentropie. Rationale Intervallgrenzen zertifizieren Einschliessungen. Ein einzelner bekannter Flächenoperator hätte einen in der Dichtematrix linearen Erwartungswert. Die Reinheit ist quadratisch. Sie lässt sich im Prinzip an zwei unabhängigen, identisch präparierten Kopien mit einem partiellen SWAP auslesen.

## Vergleich mit der Wirkung und dem N15-Vorbild

Der derzeitige N22-Ausdruck (Quellen und Nachimpulse wie im Archiv) hängt von der Relation, den Schichtkoeffizienten, Uhren und Dichten ab. Der Ordnungsanteil F₄ beträgt 28 auf beiden Kugeln. Die Dirichlet-Kragen sind zeitliche Randvorgaben und liefern keinen zusätzlichen Radius der äusseren materietragenden Fläche. Für alle gemeinsamen Feldvariablen ist die Differenz des belegten Wirkungsfunktionals zwischen den Kugelergänzungen exakt null. Das gilt auch für die Feld-Hesse-Matrix an einem gemeinsamen Feldpunkt. Zufällige oder quantenmechanische Fluktuationskovarianzen erfordern darüber hinaus ein physisches Maß bzw. einen Zustand.

Eine zusätzliche **formale Zeigerkontrolle** macht den Unterschied operational greifbar. Für den ausgewählten Term 17→18 werden bei festen übrigen Feldern die beiden Uhrargumente am Start in den zwei Armen um +h bzw. −h geändert, mit h=1/1024. Die Differenz F₊−F₋ ist dann −4h k₁₇,₁₈ w₁₈(Y₁₈−Y₁₇). Sie ist bei schwer und leicht von null getrennt, in den normierten Wirkungseinheiten ungefähr −5,20150·10⁻⁶ bzw. −3,30443·10⁻⁷. Bei gleichem Feld bleibt sie unter dem Radienwechsel gleich. Verschiebt man Y₁₇ symmetrisch in *allen* Termen bei festen übrigen Variablen, ergibt die quadratische Identität −4h G₁₇, also auf der stationären Lösung genau null. Der Test ist ein Modell für einen zählenden Eingriff. Eine physische Implementation dieses selektiven Zugriffs und eine absolute Wirkungs-/Phasenkalibrierung sind damit nicht nachgewiesen.

Die N15-Rechnung zeigt eine konkrete Methode, um gekoppelte Zeiger und kohärente Endauslesen zu untersuchen. Der dort beschriebene Signaleffekt betrifft eine Dichte bzw. einen Randsektor. Um bei N22 weiterzukommen, braucht es auf derselben Geschichte einen von der Materiegrenze beeinflussten Term, eine Präparation, ein Maß oder einen Messoperator, dessen Festlegung ohne die beiden Sollradien auskommt. Vorab eine erreichbare Messung E festlegen und im gematchten Kugelpaar bei **festgehaltener** Masse P(E|R=1) und P(E|R=1,785) vergleichen. Bei einem Quanteninterferometer kann dieselbe Messung zusätzlich auf eine dephasierte Kontrolle angewendet werden, um den Beitrag relativer Phasen zu isolieren. Zwei unterscheidbare Gegenhypothesen sind noch keine universelle Arealradieneichung. Der positive Massenstandard ist ein separater offener Punkt.

## Unterlagen und Primärliteratur

- [Veröffentlichter Referenzstand PR 419](https://github.com/thomasmgfeller/x6-spectral-astrolabium/pull/419)
- [N15-Gewichtsraum und kubische Operatorergänzung](https://github.com/thomasmgfeller/x6-spectral-astrolabium/tree/e2e2597ce45b9fa1aa5982c99943cde002bda8a0/research/rax_cqg/dust_collapse/early_areal_radius_two_masses_v0_1)
- [N15-Wirkungszeiger mit bedingten Phasen](https://github.com/thomasmgfeller/x6-spectral-astrolabium/tree/e2e2597ce45b9fa1aa5982c99943cde002bda8a0/research/rax_cqg/dust_collapse/n15_zeiger_an_der_verklebung_v0_1)
- [N15-Interferenz unter einer festgelegten Endauslese](https://github.com/thomasmgfeller/x6-spectral-astrolabium/tree/e2e2597ce45b9fa1aa5982c99943cde002bda8a0/research/rax_cqg/dust_collapse/n15_kohaerenz_am_endrand_v0_1)
- [Surya, X und Yazdi, Entanglement Entropy of Causal Set de Sitter Horizons](https://arxiv.org/abs/2008.07697)
- [Tsang, Nair und Lu, Quantum Theory of Superresolution for Two Incoherent Optical Point Sources](https://doi.org/10.1103/PhysRevX.6.031033)
- [Ekert et al., Direct estimations of linear and non-linear functionals of a quantum state](https://arxiv.org/abs/quant-ph/0203016)
- [Paris, Quantum estimation for quantum technology](https://arxiv.org/abs/0804.2981)

Die Statistiken der N15-Endtypen, die N22-Wirkungsprüfung, die algebraischen Kontrollen und der Fenstervergleich sind in den Teilverzeichnissen gewichte, wirkung, info und vergleich dokumentiert. Primäreingaben und feste Quellrevision stehen in eingaben/Herkunft.txt. Alle Ergebnisse sind endliche Modell- oder Kontrollaussagen. Physische Entropiewerte wurden nicht eingesetzt oder als null ausgewiesen.
