# CST-DUST Randkern-Benchmark

Version 0.1 · Thomas Gfeller / X6 · 11. November 2026

## Ergebnis

Der Benchmark macht vorhandene endliche CST-DUST-Bausteine getrennt nachrechenbar. Er liefert vier geometrische Verklebungskerne, Projektoren und Gram-Matrizen eines Labelquotienten, die ursprüngliche Uhrkern-Negativkontrolle sowie eine stationäre Schurantwort.

41 eng begrenzte Kontrollen sind bestanden. Die Rechnung verwendet nur die Python-Standardbibliothek, exakte rationale Zahlen und zertifizierte rationale Intervalle. Sie benötigt keinen externen Rechendienst.

Alle acht physikalischen CST-DUST-Gates bleiben HOLD: MODEL, CURRENT, CORRESPONDENCE, BOUNCE, REGULARITY, BOUNDARY, TRAPPING und EXTENSION. Die vorgeschlagene gemeinsame 8×8-Materiematrix bleibt NOT_CONSTRUCTED. Das spezifische ältere FAIL des rohen Uhrkerns wird separat reproduziert und erhalten.

## Anschluss an die Reihe

Die Quellen sind die Projektpakete gluing_v0_1, variation_v0_1 und quantum_structure_v0_1. Die neue Ausgabe folgt dem Daten- und Herleitungsvertrag von N0B-2C-MF v0.2. Sie legt fünf unveränderte Originaldateien und fünf neu berechnete Ergebnisdateien bei. provenance.json verankert die Herkunft an einem festen Repository-Commit.

Die Zustandsräume dieser Bausteine sind verschieden. Ein geometrischer Verklebungsindex, eine interne Umbenennungsbahn und ein kinematisches Uhrlabel werden nicht ohne Abbildung miteinander identifiziert. Damit entsteht durch die Zusammenstellung noch kein physikalischer Hamiltonoperator.

## Technische Fassung

DERIVATION.md enthält die vollständigen Formeln und Geltungsbereiche. README.md erschließt Daten, Quellcode und Reproduktion. OFFENE_RANDBASIS.json dokumentiert die noch fehlenden Definitionen. Dieser Bericht ist die kompakte Lesefassung.

# Geometrische Kerne und Quotient

## Vier exakt reproduzierte Verklebungsfälle

Die Enumeration umfasst alle 219 gelabelten Viererordnungen. Bei einer festen Teilung in zwei Zweierblöcke werden die Antiketten-/Kettenfälle getrennt ausgewertet. Die vier Fasergrößen betragen 35, 26, 26 und 20. Alle Laurent-Polynome und die Kontrollphasen 1, -1 und i stimmen mit dem archivierten Ergebnis überein.

Bei z=i lautet die geometrische Matrix zeilenweise (-13, 5-11i) und (5-11i, 2+8i). Die vollständige gewichtete Komposition stimmt koeffizientenweise mit der direkten markierten Summe überein. Kreuzpaare und interne Intervallumklassifizierungen bleiben enthalten.

Diese Indizes bezeichnen induzierte Teilordnungen, keine bereits hergeleiteten Anfangs- und Endzustände. Die Kontrollphase fixiert keinen physikalischen Wert der gravitativen Kopplung. Die Amplitudensummen sind keine Wahrscheinlichkeiten.

## Labelmittelung und positive Norm

Für null, ein und zwei innere Elemente wird die gemeinsame Umbenennung von Geometrie und positiven Dichtemarken vollständig ausgeführt. Die drei Fälle enthalten 1, 2 und 12 markierte Zustände in 1, 2 und 7 Orbits. Projektoreigenschaft, Symmetrie, Orbit-Stabilisator-Identität und Gram-Normen stimmen exakt.

Im betrachteten Unterraum sind Funktionen innerhalb jedes kontinuierlichen Feldstratum konstant. Ein Orbitindikator besitzt die Norm zum Quadrat 1 geteilt durch das Produkt aus 2 hoch m und der Ordnung seines Stabilisators. Die Gram-Matrix ist in dieser Basis diagonal mit den Orbitgewichten. Nach ausdrücklicher Normierung der Orbitvektoren ergibt sich die Einheitsmatrix.

Diese Positivität gehört zum Hilfshistorienraum. Die endliche Gruppe entfernt interne Labels; sie liefert keine gravitativen Constraints und keinen Zeitgenerator. Das isolierte Dichte-Nullatom wird nicht als Eich-Nullrichtung entfernt. Verschiedene positive Markenzahlen werden durch Labelmittelung nicht vermischt; daraus folgt keine dynamische Superselektion.

# Uhrkern und Schurantwort

## Unveränderte Negativkontrolle

Der ältere Kandidat CST-DUST-V1-RAW-K verwendet eine einzige Kausalrelation. Das Anfangs-Dichtegewicht ist null, das Endgewicht wird mit dem deklarierten Atom-/Positivmaß integriert. Die endlichen Eingangs-Uhrlabels (0,1) und Ausgangslabels (2,3) werden durch Translation um zwei identifiziert.

Für diesen unveränderten Kern scheitert bereits eine konstante Normierung im Produkt I2. Der stärkere Test fragt, ob irgendein gemeinsames positives Hermitesches Produkt den Kern nach konstanter Normierung isometrisch machen könnte. Eine notwendige spektrale Bedingung ist verletzt: Der Imaginärteil des Verhältnisses von Spurquadrat zu Determinante liegt zertifiziert zwischen -2.4527328506264341446412621423239 und -2.4527328506264341446412621423238.

Die rationale Taylorrechnung bis Grad 80 reproduziert das ältere Intervallzertifikat. Positive und negative synthetische Kontrollfälle qualifizieren den Test. Das FAIL betrifft genau diesen Kern und diese Identifikation. Es widerlegt weder CST noch unabhängig begründete unterschiedliche Randprodukte, eine Rigging-Map oder vollständige Randräume.

## Stationärer Response bei festem Träger

Das geerbte Beispiel verwendet eine Fünferkette, Dichtegewichte (0,0,1,1,0), feste äußere Uhren 0 und 4 sowie zwei gehaltene innere Uhren. Die Elimination einer weiteren Uhr ergibt den Innenblock -4 und die effektive Matrix mit Zeilen (-55,-17)/16 und (-17,145)/16.

Neun rationale Substitutionen bestätigen die eliminierte Uhrgleichung und die Gleichheit voller und reduzierter Wirkung. Das sind keine Lösungen sämtlicher Staub- und Geometriegleichungen. Der Schur-Hessian definiert ohne kinetische Normierung und Uhrdeutung keine Oszillatorzustände.

Bei überall verschwindender Dichte ist die Staub-Hesse-Matrix null; eine gewöhnliche Schur-Inverse fehlt. Ein einzelnes lokales Nullatom kann dagegen weiterhin an positive Nachbardichten gekoppelt sein. Die kompakte Quantenintegration wird durch die stationäre Substitution nicht ersetzt.

# Offene Randbasis und Reproduktion

## Die 8×8-Matrix ist ein offener Auftrag

Zwei Geometrietypen, zwei Strata und zwei Materielabels sind eine Indexplanung. Vor einer Matrixberechnung müssen acht konkrete Randfunktionen, ihre Träger, Präparation, Gruppenwirkung und Produkte definiert werden. Erst der Rang des Quotient-Gramprodukts zeigt, ob acht unabhängige Zustände vorliegen.

Es fehlen insbesondere die Abbildung zwischen den vorhandenen Hilfsräumen, eine physikalische Uhr einschließlich des Nullatomsektors, die Beziehung möglicher zusätzlicher skalarer Felder zur geerbten Staubwirkung sowie ein kontrollierter Moden- und Integrationsvertrag. Die unbekannten Misch- und stratumbezogenen Schurblöcke bleiben NOT_COMPUTED. Sie werden nicht durch Nullmatrizen ersetzt.

Ein einzelner verschwindender Mischblock beweist keine Superselektion. Der geometrische Kern selbst zeigt Phasenauslöschung: Sein gemischter Eintrag verschwindet bei -1, ist bei i aber 5-11i. Ein nichtverschwindender Randblock wäre zunächst ein Mischbeitrag dieser Amplitude. Ein physikalischer Zeitübergang oder eine bestimmte lineare Feldkopplung benötigt weitere Nachweise.

## Offline nachrechnen

Python 3.10 oder neuer genügt für den Benchmark. Im Paketordner führt python3 -O -B verify_package.py --replay die Rechnung in einem temporären Verzeichnis erneut aus und vergleicht alle fünf Ergebnisdateien bytegleich. Der Prüfer kontrolliert zusätzlich die fünf Original-Blob-Identitäten, das SHA-256-Manifest und die Statuskonsistenz.

Das ZIP ist eigenständig entpackbar und nachrechenbar. Liegt das äußere ZIP zusätzlich im Paketordner, wird es mit einem deterministischen Neuaufbau verglichen. Die PDF entsteht aus REPORT.md mit build_report.py, ReportLab 4.4.9 und DejaVu Sans. Für die reine Nachrechnung sind diese PDF-Abhängigkeiten nicht erforderlich.

Die 41 Kontrollen sind eine Reproduktion bekannter Resultate mit kleinen expliziten Ergänzungen. Sie sind keine unabhängige externe Replikation, keine blinde Vorhersage und kein Produktionslauf. Es werden keine kostenpflichtigen Rechenläufe oder Zeitpläne eingerichtet.
