# CST-DUST · Pfadgedächtnis bei N14 · v0.2

Wie viel muss der Rand einer endlichen Staubballhistorie über die letzten Einfügungen wissen? Die Antwort hängt davon ab, was vorhergesagt werden soll. Für die Gewichtsverteilung des nächsten Endtyps gibt es ein exaktes Minimum. Für eine kohärente Randamplitude kommen linear unabhängige skalare Ausgänge hinzu. Das relative physikalische Gewicht zweier solcher Ausgänge bleibt auch nach der geprüften Kompression frei.

**Ausgangsdaten.** N11 bezeichnet elf Ereignisse, darunter die drei inneren Punkte der Anfangsordnung. Drei Einfügungen führen über N12 und N13 nach N14. Die beiden Eltern sind die Dreierkette und eine Ordnung mit einer Relation und einem isolierten Punkt. Die übrigen acht Randereignisse sind fest. Die beiden alten Einfügungen lassen sich vertauschen (S₂), bei N14 sind es sechs Permutationen der drei Einfügungen (S₃). Verwendet wird die archivierte symmetrische N13-Marginale jeder Elternordnung. Strikte Positivität ist nur auf dem vollständig in allen sechs Reihenfolgen zulässigen Träger verlangt. Die Skalarrechnung verwendet das geerbte zentrierte Gaußpaket. Die gerundeten Uhrdaten gehören zu den Dichten 1/8 und 1/4.

Die 77 Ausgangsdateien unter `prior/` entsprechen Byte für Byte dem Forschungsordner in [PR #300](https://github.com/thomasmgfeller/x6-spectral-astrolabium/pull/300), Merge-Commit [bbbe6a9](https://github.com/thomasmgfeller/x6-spectral-astrolabium/tree/bbbe6a934508f5653665a4b667fa672711e90f2c/research/rax_cqg/dust_collapse/history_measure_state_space_v0_1). Die Vergleichswerte der Git-Objekte stehen in `upstream_blobs.json`.

## 1. Vorhersage des nächsten unmarkierten Endtyps

Für einen positiven markierten N13-Präfix p ist μ(p) sein Gewicht. Eine N14-Orbitmasse xₒ verteilt sich gleichmässig auf die |o| verschiedenen markierten Pfade ihres Orbits. Für den nächsten unmarkierten Endtyp j ist die bedingte Kontrollverteilung

    Rₚ(j) = Σ [xₒ / (|o| μ(p))], summiert über alle Pfade mit Präfix p und Endtyp j.

Zwei Präfixe können für diese Aufgabe genau dann gemeinsam kodiert werden, wenn ihre vollständigen R-Zeilen übereinstimmen. Die Anzahl ist eine Zahl unterscheidbarer Zustände in einem endlichen Katalog. Die Koeffizienten sind im Kontrollmodell normalisiert. Sie beschreiben keine gemessenen Häufigkeiten eines Staubkollapses.

| Aufgabe | Kette | Ein-Kanten-Ordnung |
|---|---:|---:|
| Positive markierte N13-Präfixe | 70 | 72 |
| Unmarkierte N13-Typen darunter | 14 | 17 |
| Klassen für die archivierte N14-Fortsetzung | 35 | 38 |
| Kleinste Einteilung, die für **jede** zulässige Fortsetzung funktioniert | 35 | 38 |
| Kleinstmögliche Klassenzahl bei **Wahl** einer einzelnen strikt positiven Fortsetzung | 33 | 38 |

Der Austausch der beiden alten Einfügungen bewahrt die gesamte Endverteilung bei jeder S₃-invarianten Fortsetzung. Die archivierte strikt positive Fortsetzung trennt bereits alle übrigen Präfixpaare. Das beweist sowohl die Hinlänglichkeit als auch die Minimalität der 35 bzw. 38 Klassen für die universelle Aufgabe.

Unter strikter Positivität erzwingen verschiedene Mengen erreichbarer Endtypen verschiedene Zeilen. Es gibt 33 bzw. 38 solche Mengen. Für die Kette konstruiert ein zweites rationales Zeugnis vollständig identische R-Zeilen für die zwei Paare mit gleichen Endtypmengen. Der Prüfer berechnet alle Zeilen neu und kontrolliert jede markierte Marginale. Für die Ein-Kanten-Ordnung erreicht bereits die archivierte Fortsetzung die Untergrenze. Dieses Optimum betrifft alle positiven S₃-Fortsetzungen mit der gegebenen Marginale. Es wurde ohne die zusätzliche Ratenvorschrift des nächsten Abschnitts bestimmt.

In der Kette haben die Präfixe 5834014 und 106430750 beide den unmarkierten Typ 1023. In der archivierten Fortsetzung beträgt das bedingte Gewicht des Endtyps 32187 beim ersten 11/17, beim zweiten null. Die totale Variation ihrer vollständigen Verteilungen beträgt 12/17. Für die Ein-Kanten-Ordnung findet sich beim gemeinsamen Typ 183 ein Abstand von 43/54. Zahlen, Äquivalenzklassen und Verteilungen stehen in `prediction.json`.

## 2. Eine positive Wachstumsregel mit geometrischer Zusatzinformation

Für jede einzelne markierte Einfügung c prüfen wir die Ratenform x(c) = μ(p) q(K(c)). Der Schlüssel K enthält den N13-Präfix mit identifizierbarem N11-Kern und ungeordnetem Paar älterer Einfügungen, den unmarkierten N14-Tochtertyp und min(k,h). Hier zählt h die **gerichteten strikten Ordnungsrelationen** von einem der drei anfänglichen Innenpunkte zu einem der drei ergänzten Punkte im Ziel. Auch transitive Relationen zählen. Die Raten dürfen je N11-Elternordnung verschieden sein.

| Nachweis in dieser Schlüsselfamilie | Kette | Ein-Kanten-Ordnung |
|---|---:|---:|
| Grösste geprüfte unzulässige Kappung | 4 | 3 |
| Erste zulässige Kappung | 5 | 4 |
| Erreichte positive markierte Pfade | 924 von 924 | 1026 von 1026 |
| Freie Komponenten nach Austauschgleichungen, vor Normierung | 137 von 154 vollständigen Orbits | 160 von 191 vollständigen Orbits |

Die Normierungsbedingungen ergeben ein lineares System Aθ = 1 mit θ ≥ 0. Für den jeweils gröberen Schlüssel liefert ein rationaler Vektor y mit Aᵀy ≥ 0 und Σy = −1 einen Widerspruch. Kleinere Kappungen identifizieren weitere Parameter und sind damit ebenfalls ausgeschlossen. Für den nächstfeineren Schlüssel stehen strikt positive rationale Lösungen zur Verfügung. Der Prüfer verfolgt jede Permutation und jede Verlängerung zurück zur ursprünglichen Präfixmasse. Beide Schwellen gelten auch, wenn die Sechsfachzulässigkeit vor Zuweisung der Raten als Maske angewandt wird. Diese Schwellen betreffen diese Form der Übergangsrate. Andere geometrische Kennzahlen können andere Kompressionen erlauben.

Bei k = 4 enthält der positive Ein-Kanten-Zeuge je eine eigene Komponente für die ausgewählten Orbits zu 1790 und 5374. Beide wirken auf dieselben drei Präfixe mit identischen Spalten der Normierungsmatrix. Ihre Orbitmassen betragen beim gewählten Zeugen je 1/49 000 000. Eine Verschiebung t vom ersten zum zweiten erhält alle Gleichungen für |t| < 1/49 000 000 und lässt jeden vollständigen Pfad positiv. Dieser Radius gehört zum konkreten Zeugen. Die Wahl des Zahlenwerts t benötigt eine zusätzliche physikalische Gleichung.

## 3. Dimension des kohärenten Randzustands

C projiziert Orbitmassen auf die N13-Paarmarginale. B addiert Orbitkoeffizienten je unmarkiertem N14-Endtyp. Freie Differenzen bei fester Marginale liegen im Kern von C. Falls S die Endtypen mit von null verschiedenem Präparationsfaktor enthält, beträgt die Zahl zusätzlich erforderlicher linearer Koordinaten

    d(S) = Rang([C; B_S]) − Rang(C).

Die Formel setzt linear unabhängige skalare Endzustände voraus. Für alle 101 Endtypen wird die Gaußpräzision Ω nach Integration der inneren Koordinaten und der gedämpften Eingangsvariablen exakt über den komplexen rationalen Zahlen bestimmt. Der Realteil ist positiv definit. Schon auf der Geraden y = (s,0,0) sind die 101 Werte Ω₁₁ verschieden. Eine stetige Linearkombination, die im L²-Raum verschwindet, ist überall null. Bei u = s² liefert Ableiten der Exponentialfunktionen in u am Ursprung eine Vandermonde-Matrix mit von null verschiedenem Determinantenprodukt. Damit sind die Zustände in der gemeinsamen skalaren Ausgabedarstellung über ℂ linear unabhängig. Individuelle nichtverschwindende Normierungen und Gravitationsphasen erhalten diese Eigenschaft.

| Grösse | Kette | Ein-Kanten-Ordnung |
|---|---:|---:|
| Vollständige Orbits / Endtypen | 154 / 53 | 191 / 72 |
| Rang der Marginale C | 35 | 38 |
| Zusätzliche lineare Koordinaten des reinen Skalarausgangs | 48 | 70 |
| Gesicherter Bereich mit geerbten Uhren auf den beiden gemeinsamen archivierten Gittern | 3 bis 48 | 3 bis 70 |

Die bekannten Uhren auf dem jeweiligen vollen Träger gehören zu {662, 760, 5905} und {926, 1790, 5374}. Bei jeder Elternordnung lassen sich die drei zugehörigen Endkoeffizienten unabhängig verändern. Die rationalen Richtungen in `boundary.json` erhalten die Marginale. Sie erlauben kleine reelle Veränderungen in alle drei Richtungen mit strikt positiven Orbitgewichten. Lineare Dimensionen für kohärente Amplituden sind über ℂ angegeben. Für reelle Gewichtsvariation zählt dieselbe Rangzahl reelle Richtungen. Die untere Schranke erlaubt Änderungen auf dem vollständigen Orbitträger. Werden auch die veränderlichen Orbitkoeffizienten auf die bekannten Uhrtypen beschränkt, sinkt der Zusatzrang auf 0 bzw. 1. Die Ergebnisse gelten vor Normierung und Detektorauslese.

Für die gemeinsame Präparation mit beiden Eltern zu je 1/2 werden die beiden Marginalen getrennt festgehalten. Die Fortsetzungen dürfen unabhängig variieren. Bei 24 von beiden Eltern erreichbaren Endtypen werden die Beiträge vor der Auslese kohärent addiert. Auf 345 Orbitspalten hat die gemeinsame Marginalmatrix Rang 73. Mit den sechs bekannten Endtypen steigt der Rang auf 79, mit allen 101 auf 171. **Damit sind bei fester Marginale genau 98 zusätzliche lineare Koordinaten für den skalaren Ausgang erforderlich. Für den gekoppelten Ausgang liegt der Zusatzrang auf den gemeinsamen Gittern zwischen 6 und 98.** Der Würfel unabhängiger reeller Änderungen der sechs Endkoeffizienten hat für den angegebenen Zeugen Radius 9/52700. Die sechs von null verschiedenen Uhrenfaktoren sind bei beiden Dichten auf den gemeinsamen Gittern 32×6 und 48×8 geprüft. Die Obergrenze wird erreicht, wenn alle zusätzlichen Endkoordinaten einer Rangbasis nichtverschwindende Uhrenfaktoren haben.

## 4. Auswahlversuch mit dem geerbten Detektor

Für das Paar 1790/5374 testen wir einen gemeinsamen eindimensionalen Eingangsteilraum, dessen Zerlegung in Sektor und Komplement an beiden Dichten alle akzeptierten q₇-Fenster ohne Kreuzterme lässt. Bei jeder Dichte allein existieren zwei solche Kanäle. Nach Rücktransport auf dieselben Historienkoeffizienten haben die beiden normierten Mitteleffekte keinen gemeinsamen Eigenvektor. Auf allen vier archivierten Gittern hat ihr gemeinsamer Kommutant die komplexe Dimension eins. Das schliesst eine gemeinsame Rang-eins-Projektion dieser Art aus. Die Originalrechnung, das Positivbeispiel bei fester Dichte und die Empfindlichkeit gegenüber Störungen sind in [Auswahl.md](Auswahl.md) erläutert.

Die algebraischen Aussagen zum Detektor betreffen die gespeicherten Zahlen. Die von der Präparation abhängigen Uhrenwerte haben empirische Gitterkontrollen. Strenge Fehlergrenzen für die exakten Uhrintegrale, eine physikalische Auswahl des Historienmasses und die Konstruktion des vollständigen physikalischen Zustandsraums sind offen. Die vier Auswertungen verwenden die lokale CPU und benötigen keine neue Uhrquadratur.

## Lokale Wiederholung

Getestet mit Python 3.12, NumPy 2.3.5, SciPy 1.17.0, SymPy 1.14.0 und mpmath 1.3.0. In einer Umgebung mit diesen Bibliotheken im entpackten Verzeichnis ausführen.

```sh
python -B verify.py
```

Der Prüfer kontrolliert alle SHA-256-Prüfsummen und die Git-Blob-IDs der Ausgangsdaten. Anschliessend erstellt er die vier neuen Ergebnisdateien in einem temporären Verzeichnis und vergleicht exakte bzw. numerische Resultate. Die rationalen Zertifikate werden direkt in den Gleichungen geprüft. Die optionale Suche in `candidates.py --discover` ist für die Wiederholung entbehrlich. Die Vorgängerrechnung lässt sich zusätzlich unter `prior/` mit ihrem eigenen Prüfer wiederholen.

| Datei | Inhalt |
|---|---|
| prediction.py, prediction.json, prediction_minimum_certificate.json | Vorhersageklassen, bedingte Endverteilungen und Zeuge für das Kettenminimum |
| candidates.py, candidates.json, candidates_certificate.json | Übergangsregeln, positive Fortsetzungen, Unmöglichkeitszeugnisse und A/B-Verschiebung |
| boundary.py, boundary.json | Exakte Gaußpräzisionen, Marginalränge, explizite lineare Variationsrichtungen |
| selection.py, selection.json, Auswahl.md | Dichteabhängige Auswahlprüfung und Störungsintervalle |
| prior/, upstream_blobs.json, SHA256SUMS | Auswertungsgrundlage und Integritätskontrolle |

Die Lizenzangaben stehen in LICENSE, NOTICE und LICENSE_SCOPE.md.
