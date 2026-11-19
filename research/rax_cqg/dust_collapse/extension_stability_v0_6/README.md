# CST-DUST · Erweiterungsstabilität auf dem vollständigen N14-Träger

[Bericht (PDF)](../reports/CST_DUST_N14_Volltraeger_v0_6.pdf) · [Offline-Prüfpaket (ZIP)](../packages/CST_DUST_N14_Volltraeger_v0_6_Pruefpaket.zip) · [Zertifikat beider Gitter](study/result.json) · [Kontrollen und Gegenbeispiel](study/audit.json)

Stand 19. November 2026. Anschluss an die v0.5-Studie aus PR #299, geprüft am Repository-Stand 8b6673c52ce309f203b09da614f17dfb88cea6c2 (PR #310).

## Frage und Entscheidung

Das Paket prüft die ursprüngliche kohärente N11-Zweilobenpräparation mit demselben q7-Detektor und den Anfangsdichten 1/8 und 1/4. Beide N11-Eltern beginnen mit dem reellen Amplitudengewicht 1/2. Jede überträgt denselben Anteil λ ihres eigenen Gewichts, verteilt ihn aber frei und nichtnegativ auf ihre erreichbaren N12-, N13- und N14-Fortsetzungen. Beide Dichten haben dieselbe Aufteilung. Amplituden für gemeinsame Endtypen werden vor der Auslese addiert.

Auf den beiden veröffentlichten Referenzgittern bestehen alle zulässigen Aufteilungen für 0 ≤ λ ≤ 0,050210 die drei ursprünglichen Toleranzen. Bei λ = 0,050211 scheitert mindestens eine zulässige Aufteilung auf beiden Gittern. Die vorherige Klammer für den gesamten Träger reichte von 1,6 % bis 5,0283 %. Die Zahl bezeichnet einen Anteil vom Amplitudengewicht jedes Elternzweigs. Sie bezeichnet weder einen Anteil der Geometrien noch eine Wahrscheinlichkeit.

## Rechnung

Die Basis umfasst 2 Eltern, 5 N12-, 23 N13- und alle 139 zulässigen N14-Endtypen. Für 10 N14-Typen wurden die bisherigen individuellen Uhrintegrale übernommen und für 24 weitere neu ausgewertet. Die übrigen 105 sind durch obere Schranken ihrer Amplituden vertreten. In beiden Auslesestufen bleiben die archivierten Detektorblöcke (jeweils 40 × 40) in der hier verwendeten Referenzumgebung unverändert reproduzierbar. Gemeint ist der Block der 40 bekannten Typen für jede Dichte und jeden Ausleseausgang. Die alte Skalarprüfung schliesst 99 der 238 erreichten Endtypen aus.

Jeder bedingte Skalarzustand ist eine durch die ursprüngliche Wirkung bestimmte normierte Gaußfunktion. Die drei akzeptierten Effekte werden mit der transformierten Gaußkovarianz bei 70 Dezimalstellen aufgebaut. Der vierte Ausgang ist eins minus Gesamterfolg. Die binären Tabellen gram.npy enthalten 169 × 169 komplexe Einträge je Effekt. Der Prüfer bestätigt positive Definitheit der gespeicherten hermiteschen Tabellen durch ganzzahlige Kongruenz. Zwei äussere Effekte stimmen überein.

Für einen unbekannten Uhrenzweig ist jeder innere Dichtefaktor im Betrag höchstens eins. Für jede Zerlegung der sechs inneren Uhren in Gruppen von höchstens drei behalten wir alle vollständig in einer Gruppe enthaltenen Dichtefaktoren; die übrigen werden im Betrag durch eins majorisiert. Die positiven Gewichte der Quadratur erlauben das unabhängige Integrieren der Gruppen. Für jeden äusseren Uhrwert nehmen wir das Minimum der gültigen Schranken und mitteln über beide Loben. Für 27613 ergibt die gemeinsame Auswertung der ersten fünf Dichtefaktoren eine engere Schranke. Jede berechnete Betragshülle erhält einen numerischen Zuschlag von 10⁻¹². Die Referenz v0.5 liefert zusätzlich eine von der Geometrie unabhängige Hülle für den rephasierten Dichtewechsel.

Die 24 direkten Uhrenrechnungen berechnen hochgradige Endknoten mit der C99-Kontraktion der Vorgängerstudie, wenn ihr Ergebnis vom äusseren Uhrwert unabhängig ist. Die übrigen Integrationsvariablen werden durch exakte Summationsumordnung auf den Gauss-Legendre-Gittern eliminiert. Sowohl die neuen direkten komplexen Amplituden als auch der übernommene Typ 760 dürfen sich im Zertifikat je Dichte um 10⁻⁷ verschieben. Die Kontrolle der übrigen, archivierten Amplituden erfolgt am übernommenen Tabellenstand.

## Warum zwei Ungleichungen über alle Mischungen genügen

Sei b der Referenzvektor für eine Dichte, v eine beliebige zulässige Nachkommenmischung und x = (1−λ)b+λv. Das positive Gesamtprodukt S liefert für jeden Prüfvektor q die Stützschranke

    ||x||² ≥ 2 Re〈q,x〉 − ||q||².

Nach Einsetzen der Darstellung von x ist die rechte Seite affin in λ. Für 0 ≤ λ ≤ T genügen die Endpunkte. In jedem der beiden Elternsimplexe liegt das Minimum der linearen Projektion bei einem erreichbaren Endtyp. Unbekannte komplexe Amplituden werden mit ihrem ganzen Betragskreis einbezogen. Der Prüfvektor benutzt die beiden Eltern und die drei Typen 734, 760, 8191; seine Gewichte sind rationale Zahlen. Die Auswahl erfolgte nach einer Suchrechnung. Die nachfolgende Ungleichung verifiziert alle Typen und alle Mischungen unabhängig davon, wie q gefunden wurde.

Für jeden positiven akzeptierten Effekt F wird zugleich aus der quadratischen Auslese geschlossen, dass p_F(x) ≤ p_F(b). Ist C eine obere Schranke für Re〈b,Fv〉 und M eine obere Schranke für 〈v,Fv〉, so gilt

    [p_F(x)−p_F(b)]/λ ≤ (λ−2)p_F(b) + 2(1−λ)C + λM.

Die rechte Seite ist auf beiden Intervallenden negativ. M ist durch Konvexität vom grössten Diagonalbeitrag eines erreichbaren Endtyps beschränkt. Da alle akzeptierten Kanäle abnehmen, ist die halbe L¹-Abweichung aller vier Ausgänge genau der Verlust an Gesamterfolg.

Für den Dichtekontrast ist D die Differenz der Effektmatrizen bei hoher und tiefer Dichte. Am Referenzpunkt ist D₀=b*Db, hier in der Darstellung der Zweiggewichte. Die Änderung ist

    2λ(1−λ)(b*Dv−D₀) + λ²(v*Dv−D₀).

Der erste Term wird über alle erreichbaren linearen Beiträge begrenzt. Für den zweiten genügt die universelle Schranke 2Aη maxᵢ Fᵢᵢ + |D₀| mit A=0,03609 und η=0,001813 (Amplitude und rephasierte Dichtedifferenz). Die Fehlschlagdifferenz ist die negative Summe der drei akzeptierten Differenzen. Ihre halbe L¹-Norm begrenzt die Änderung der signierten Gesamterfolgsdifferenz. Alle Entscheidungen in exact.py verwenden rationale Ungleichungen und nach oben gerundete rationale Moduli. Das Programm protokolliert auch die exakten Brüche der Erfolgsschranken.

## Gegenbeispiel

Jeder Elternzweig gibt vom übertragenen Anteil 21/100 an Typ 734, 70/100 an Typ 760 und 9/100 an Typ 8191 ab. Alle drei kommen von beiden Eltern über zulässige Zwischenordnungen. audit.json enthält die sechs expliziten Wege. Bei 5,0211 % liegt der zentrale Wert des Erfolgsquotienten bei Dichte 1/4 auf beiden Gittern bei rund 0,899998480. Auch einschliesslich der oben genannten Uhrenradien bleibt seine obere Schranke kleiner als 0,9. Damit verletzt die Mischung die Zehnprozent-Niveautoleranz. An der früheren 5,0283-Prozent-Grenze reichte bereits ein einzelner Endtyp.

## Reichweite und Nachrechnung

Die algebraische Zertifizierung gilt für die gespeicherten Skalarmatrizen, Uhrenwerte und Betragshüllen einschliesslich der angegebenen Radien. Die Gauss-Knoten, Integralsummen, Betragsobergrenzen und skalaren Tabellen wurden numerisch erzeugt. Die dritte Quadratur ist eine Konvergenzkontrolle. Eine Intervallrechnung vom mathematisch exakten kontinuierlichen Integral bis zur Grenzstelle bleibt offen. Gleiches gilt für grössere Historienfamilien, ein physikalisch ausgewähltes Historienmass und eine Aussage über den vierdimensionalen Kollaps. Die Auswahlregel der frei verteilten Gewichte unterscheidet sich von der zusätzlichen S3-symmetrischen Pfadgewichtung in der Vorstudie.

Im Verzeichnis dieser Studie oder im entpackten Offline-Paket ausführen.

    python3 -B verify.py

Die schnelle Nachrechnung verifiziert das Dateiinventar, die Positivität, die sechs Wege, beide archivierten Referenzblöcke und die rationalen Zertifikate. Optional baut

    python3 -B verify.py --rebuild

die skalaren Matrizen, alle Betragshüllen, die 24 direkten Uhrenintegrale und die zusätzliche Gitterkontrolle neu auf. Für den Neuaufbau wird ein C99-Compiler benötigt. Die Repository-Fassung liest die geprüften Eingaben aus [v0.5](../extension_stability_v0_5/README.md). Das Offline-Paket enthält dieselben Eingaben unter `reference/`. Geprüft mit Python 3.12.14, NumPy 2.3.5, SymPy 1.14.0 und mpmath 1.3.0 auf einer CPU. Die Reproduzierbarkeit anderer Plattformen ist über numerische Toleranzen zu beurteilen.

[Originalstudie v0.5](https://github.com/thomasmgfeller/x6-spectral-astrolabium/pull/299) · [Quellenstand](https://github.com/thomasmgfeller/x6-spectral-astrolabium/commit/8b6673c52ce309f203b09da614f17dfb88cea6c2)

Die v0.5-Referenz im Offline-Paket entstammt dem veröffentlichten ZIP mit Git-Blob 8298c7edc84b51be373744759b2bf083c27c5c69 und SHA-256 4d69dbe7c3639675d52ae78b7835f38360f5dedc89f7bac842be4acaf767cf09. Die PDF lässt sich zusätzlich mit ReportLab und DejaVu aus study/bericht.py erzeugen.
