# N0B-2C-MF v0.2

Korrigiertes Referenzmodell und offene CST-Brücken

Lesefassung · Thomas Gfeller / X6 · 11. November 2026

## Ergebnis und Reichweite

Das Paket definiert ein reduziertes Modell für Geometrie, zwei Strata und eine skalare Mode. Die mathematischen Annahmen und Bilanzgleichungen sind dokumentiert. 32 kleine algebraische und synthetische Kontrollen wurden ausgeführt. Die Herleitung dieses Modells aus der vollständigen gemeinsamen CST-Amplitude bleibt offen.

Alle acht physikalischen CST-DUST-Gates bleiben HOLD: MODEL, CURRENT, CORRESPONDENCE, BOUNCE, REGULARITY, BOUNDARY, TRAPPING und EXTENSION. Die Vier-Gitter-Studie sowie die A–F-Vergleichsläufe wurden nicht ausgeführt.

## Anschluss an die bestehende Reihe

Die Veröffentlichung ergänzt die Staubball-Reihe im Repository x6-spectral-astrolabium. Die vorherige endliche Stationaritätsprüfung für die Klassen (2,3) und (3,2) bleibt ein eigenständiges Ergebnis. Die nächste offene Klasse (1,4) wird durch das neue Modell nicht erledigt.

Die atomare Komponente des geerbten Maßes, das reduzierte Zweikanalsystem und die neue quadratische Skalarmode sind unterschiedliche Konstruktionen. Eine Identifikation benötigt eine explizite Abbildung von Wirkung, Maß, Zuständen und Randdaten.

## Aufbau des Pakets

MODEL.md und BALANCES.md enthalten die technische Definition. BRIDGE_CONTRACT.md formuliert die offenen Herleitungsschritte. VALIDATION.md und DATA_CONTRACT.md beschreiben die künftigen Prüfungen. CORRECTIONS.md ordnet 29 Korrekturen ihren Gründen und Kontrollen zu. Diese Markdown-Dokumente mit ihren Formeln sind die maßgebliche technische Fassung; dieser Bericht ist eine Zusammenfassung.

# Modell und Erhaltungssätze

## Bedingte Quantendynamik

Die Basiskonstruktion verwendet einen gemeinsamen kontinuierlichen Hilbertraum auf der positiven Geometrie-Halbachse und der reellen Feldachse, ergänzt um zwei Stratumkomponenten. Konstante positive Massen, ein reelles lineares Mischpotential und ein quadratisches Materiepotential sind Modellannahmen.

Die Selbstadjungigkeit folgt unter den in MODEL.md angegebenen zusätzlichen Beschränktheits- und Konfinierungsannahmen aus der geschlossenen, nach unten beschränkten quadratischen Form. Sie folgt nicht bereits aus einer formal hermiteschen Differentialgleichung. Der Impuls auf der Halbachse ist dabei kein selbstadjungierter kanonischer Impulsoperator.

Die relationale Schrödingerdeutung setzt eine ideale kanonische Uhr und einen Constraint voraus, der linear im Uhrimpuls ist. Ein quadratischer Uhrconstraint erfordert getrennte Frequenzzweige und deren physikalische Gewichte. Die Uhrwahl ist Teil der offenen Herleitung.

## Norm, Energie und Wandkraft

Der Mischterm erzeugt entgegengesetzte Transferquellen in den beiden Stratum-Normbilanzen. Ihre Summe verschwindet. Für zeitunabhängige Koeffizienten gilt eine lokale Energieerhaltung mit dem angegebenen Energiefluss.

Eine Dirichletwand kann Norm- und Energiefluss unterbinden und trotzdem Impuls übertragen. Die integrierte Geometriebilanz enthält deshalb eine positive Wandkraft proportional zum Integral des Betragsquadrats der normalen Wellenfunktionsableitung. Im endlichen Rechengebiet sind die Beiträge beider Ränder mit ihrem Vorzeichen zu bilanzieren.

## Erweiterung um eine variable Modenmasse

Eine geometrieabhängige Materiemasse gehört nicht zur geprüften Basiskonstruktion. Bei dieser Erweiterung tritt neben der Ableitung des Materiepotentials auch eine kinetische Kraft auf. Domäne, Ströme und numerische Umsetzung müssen dafür erneut hergeleitet werden. Eine Wandreflexion allein belegt keinen physikalischen Bounce.

# Die ersten drei Herleitungsbrücken

## 1 · Physikalischer Kern und Skalarprodukt

Ein CST-Kern muss mit seiner Bedeutung als kovarianter Matrixelementkern oder als Koeffizientenabbildung geliefert werden. Diese Konventionen benötigen unterschiedliche Gram-Normalisierungen. Das physikalische Maß darf nicht nachträglich so angepasst werden, dass eine gewünschte Unitarität entsteht.

Für eine zeitunabhängige Generatorbeschreibung sind eine stark stetige unitäre Gruppe, ihre Zusammensetzung und eine gemeinsame Domäne erforderlich. Ein nur pro Zeitschritt kleiner Unitaritätsdefekt kann bei Verkleinerung des Schritts eine endliche dissipative Rate behalten.

## 2 · Uhr, Generator und Zweige

Der Logarithmus des vollständigen Kernoperators ist vor einer Kanalzerlegung zu untersuchen. Seine Zweigwahl benötigt zusätzliche spektrale Information. Drei kommensurable Zeiten beseitigen die Mehrdeutigkeit nicht generell. Ein bei einer einzelnen Zeit verschwindender Mischblock kann ein Revival sein und beweist keine verschwindende Generatorkopplung.

Die polare Ersetzung eines Kerns durch einen unitären Operator ist ein diagnostischer Vergleich, keine Herleitung unitärer Physik. Die extrahierte Dynamik muss zudem direkt über Intervalle zusammensetzbar sein; Gedächtnisabhängigkeit darf nicht unbemerkt in einen autonomen Generator gepresst werden.

## 3 · Materiewirkung, Randwirkung und Mode

Eine reelle quadratische Feldwirkung hängt vom symmetrischen Anteil ihrer Matrix ab. Ein retardierter Operator lässt sich deshalb nicht unverändert als reelle quadratische Wirkung einsetzen. Stationäre Elimination liefert ein Schur-Komplement; die vollständige Gaußintegration enthält zusätzlich Determinante und Phase.

Eigenwerte einer Randwirkungs-Hesse-Matrix sind nicht automatisch Modenfrequenzen zum Quadrat. Eine Frequenzzuordnung benötigt die passende dynamische Konstruktion. Die normierte Störungsabschätzung für einen Modenvektor ist keine allgemeine Fehlerobergrenze. Das Paket enthält ein exaktes Gegenbeispiel für einen sonst falschen PASS.

# Kopplung und Quantensignaturen

## 4 · Feldumkehr und Operatorstruktur

Eine feldneutrale Stratumzuordnung und eine vollständig feldumkehrsymmetrische Reduktion erlauben keinen ungeraden linearen Mischterm. Eine kombinierte Symmetrie aus Feldumkehr und Stratumtransformation kann ihn erlauben; ihre Herkunft muss dann aus der CST-Konstruktion gezeigt werden.

Zur Unterscheidung einer Feldkopplung von einer Impulskopplung müssen Aufwärts- und Abwärtsübergänge gemeinsam geprüft werden. Eine einzelne Übergangsrichtung kann eine falsche Kopplungsidentifikation liefern. Die eingereichten Entwürfe enthalten bereits beide Richtungen und einen Impulsterm; die Korrekturfassung präzisiert deren gemeinsame Prüfung.

Ein kleiner linearer Anpassungsrest kontrolliert noch nicht die Geometriekraft. Dafür ist auch die Ableitung des Kopplungsrests nach der Geometrievariable zu begrenzen. Eine geometrieabhängige Phasenwahl kann zusätzliche kinetische Verbindungen erzeugen.

## Kohärenz, Reinheit und Zustandsvergleich

Verschwindende reduzierte Stratumkohärenz schließt kohärenten Transfer im Gesamtsystem nicht aus. Das zeigt ein kleines exaktes Paritätsbeispiel. Die Reinheit eines reduzierten Zustands misst unter einer globalen Reinheitsannahme dessen Verschränkung mit dem gesamten Rest; sie isoliert nicht automatisch allein die Materie.

Eine konditionierte Dichtematrix ist bei leerem oder zu schwach besetztem Kanal nicht definiert. Der klassische Überlappungswert zweier Messverteilungen ist keine allgemeine Gleichheit zur Quantenfidelität. Eine Vergleichsbasis benötigt ihre Quadraturgewichte oder eine explizite Isometrie.

## Zyklen und Historien

Ein verschwindendes zeitliches Integral einer Kopplung beweist keine verschwindende Gesamtübertragung. Echovergleiche brauchen die tatsächlich zeitgeordneten Propagatoren. Historien benötigen klar definierte Klassenoperatoren, vollständige Alternativen und eine Dekohärenzprüfung. Bei operationalen Messungen zählt auch das Messinstrument, nicht nur sein POVM.

# Verfeinerung und ausgeführte Kontrollen

## 5 · Vergleich der Dynamik

Verfeinerungsstufen benötigen kompatible isometrische Einbettungen, gemeinsame Observablen und eine physikalisch begründete Norm. Die Kontrolle eines komprimierten Propagators liefert unter den angegebenen Voraussetzungen auch eine Schranke für die Leckwahrscheinlichkeit. Ein Kontinuumargument braucht darüber hinaus Domänen- oder Resolventenkontrolle.

Die Diskretisierung der reduzierten Differentialgleichung und die Dichte beziehungsweise Regulatoren des CST-Kerns sind getrennte Fehlerquellen. Ein Dreipunktfit allein validiert weder den Kontinuumgrenzwert noch die CST-Herleitung.

## 32 tatsächlich ausgeführte Kontrollen

Die Kontrollen prüfen unter anderem lokale Transfer- und Bilanzidentitäten, Wandimpuls, kombinierte Parität, beide Oszillator-Übergangsrichtungen, Kernrevival, Generator-Aliasing, Uhrzweige, ein Modenfehler-Gegenbeispiel, Gaußfaktoren, variable Masse und Propagatorkompression. Sie laufen ohne externe Messdaten oder Rechendienst. Das kanonische Ergebnis liegt in results/checks.json.

Die Kontrollen sind kleine algebraische und synthetische Beispiele. Ihr PASS bestätigt diese eng begrenzten Aussagen. Er ist kein bestandenes physikalisches CST-DUST-Gate und kein Ergebnis einer Staubballsimulation.

## Vier-Gitter-Studie bleibt offen

Überliefert sind die Tripel (81,91,81), (121,137,121), (161,181,161) und (241,271,241). Die vorgeschlagene Zuordnung zu Geometrie, Feld und Uhr ist eine redaktionelle Arbeitsannahme; die Originalüberschriften fehlen. Die Zuordnung ist vor einem Lauf am Solver zu bestätigen.

Gebiet, Koeffizienten, Anfangszustand, Integrator, tatsächlicher Zeitschritt und Toleranzen sind in study_plan.json bewusst offen. Die Gitterabstände verfeinern sich nicht mit einem einheitlichen Faktor. Ein Konvergenzfit muss dies berücksichtigen.

# Reproduktion und nächster Anschluss

## Nachrechnen und Integrität prüfen

Im Paketordner werden zunächst die Abhängigkeiten aus requirements-checks.txt installiert. Danach führt python3 -O -B verify_package.py --replay die archivierten Kontrollen erneut aus und vergleicht deren kanonisches Ergebnis bytegleich. SHA256SUMS.json erfasst die Paketdateien; der Prüfer kontrolliert zusätzlich das Quellenarchiv. Liegt auch das äußere ZIP im Paketordner, wird dessen deterministischer Neuaufbau bytegleich geprüft.

Die PDF-Lesefassung wird mit python3 -B build_report.py aus REPORT.md erstellt. Dazu werden requirements-report.txt und die DejaVu-Sans-Schriften benötigt. Das Prüfpaket wird mit python3 -B package.py erneuert. Der Offline-Replay benötigt weder GitHub-Zugriff noch einen externen Solver.

## Quellen und Herkunft

provenance.json verankert die relevanten Vorgängerdokumente an einem festen Repository-Commit. source_evidence enthält 111 eingereichte Formelbilder und ihre Prüfsummen. Dieses Archiv dokumentiert die verfügbare Bildbasis; es ist kein vollständiger Originaltext und kein verifizierter historischer Solver.

SOURCES.md enthält die Projektquellen und Primärliteratur zu Operatoren, Uhren, Kausalsets, Oszillatoren, Modenstörungen, Dekohärenz und Historien. Externe Werke werden verlinkt und nicht mitarchiviert. Es wird keine unabhängige externe Replikation behauptet.

## Der nächste prüfbare Beitrag

Zuerst sind gemeinsame CST-Kerne und physikalische Gram-Produkte mit eindeutigem Maß, Uhrzweig, Materiewirkung, Randdaten und Regulatoren zu liefern. DATA_CONTRACT.md beschreibt die erforderlichen Daten. Anschließend lassen sich die Herleitungsbrücken und erst danach die dynamischen Vergleichsläufe prüfen.

Diese Veröffentlichung richtet keine kostenpflichtigen Rechenläufe oder Zeitpläne ein. Ein Beitrag der Community kann anhand dieses Vertrags vorbereitet werden. Die offenen physikalischen Gates bleiben bis zum entsprechenden Nachweis HOLD.
