# Ein Materialseitenbit auf einer verlängerten Testbahn

**Ergebnis.** In der flachen geometrischen Kontrolle entscheidet ein einzelnes Innen-/Aussenbit auf der geradlinig über Ereignis 11 hinaus fortgesetzten Bahn 5→11 zwischen den zwei archivalischen Kugelhypothesen. Für jede Ablesung in `[31/64,17/32]` und für beide Feldpräparationen zeigt die kleine Kugel innen und die grosse aussen. Dieselbe Aussage gilt im symmetrischen Fenster `1/2 ± 1979/100000`. Das ursprüngliche ganze Fenster `[15/32,17/32]` ist für keine der drei geprüften Bahnen sicher. An seiner linken Grenze liegen alle drei jeweils in beiden Kugeln. Zwei Hypothesen mit identischen 22 alten Aufzeichnungen benötigen mindestens eine unterscheidende Beobachtung. Das eine Materialseitenbit ist damit für dieses Kontrollpaar minimal. Eine unabhängige Flächenbestimmung für allgemeine Staubränder ist eine andere Aufgabe.

## Messmodell

Kontrollzeit ist die normierte Uhr x, Lichtgeschwindigkeit 1. Für fest vorgegebene alte Ereignisorte uᵢ,u₁₁ und ihre unbekannten wahren Uhren xᵢ,x₁₁ in den archivierten rationalen Intervallen verläuft der Beobachter nach 11 entlang `p(x)=uᵢ+(x−xᵢ)(u₁₁−uᵢ)/(x₁₁−xᵢ)`. Es sind zeitartige inertiale Testbahnen. Die Materialseitenregel ist das Vorzeichen von `g(x)=|p(x)−C|²−[R₀−(x−1/2)/8]²`. Negative Zahlen geben innen an, positive aussen. Es gelten für die kleine Kugel `C=(0,0,−1), R₀=1` und für die grosse `C=(0,0,−5/2), R₀=2`.

| Verlängerte Bahn | Einzige Nullstelle an der grossen Kugel, schwer | Einzige Nullstelle an der grossen Kugel, leicht |
|---|---|---|
| 3→11 | [0,4943653653; 0,4943653654] | [0,4942808559; 0,4942808560] |
| 4→11 | [0,4799419404; 0,4799419405] | [0,4804379040; 0,4804379041] |
| 5→11 | [0,4797082477; 0,4797082478] | [0,4802035621; 0,4802035622] |

Die rechte Grenze des jeweils zitierten Nullstellenintervalls liegt bereits streng auf der Aussenseite. Für alle sechs Fälle ist g der kleinen Kugel auf dem gesamten Fenster strikt negativ. An der grossen Kugel ist die Ableitung überall positiv. Rechts vom Übergang trennt das Seitenbit die Hypothesen. Unter den drei bereits bei der Halbzeit trennenden Bahnen garantiert 5→11 auch bei unbekannter Wahl der schweren oder leichten Präparation den frühesten Übergang. Auf dem rationalen Teilfenster `[31/64,17/32]` beträgt der zertifizierte radiale Abstand der Bahn 5→11 zur kleinen Grenzfläche bei beiden Präparationen mindestens 0,393445 nach innen. Bei der grossen Grenzfläche beträgt er mindestens 0,001251 nach aussen im schweren und 0,001108 nach aussen im leichten Fall. Die Abstände stehen in den festgelegten geometrischen Kontrolleinheiten. Der symmetrische Halbbreitentest prüft das Vorzeichen gesondert und beansprucht diese grössere Abstandsmarge nur auf dem angegebenen rationalen Teilfenster.

Der Prüfer umfasst kontinuierliche Uhren und ganze Zeitintervalle mit exakten Brüchen. Er schliesst die Koeffizienten der quadratischen Funktion g um x=1/2 ein. Für die kleine Kugel schliesst er die Funktionswerte über 64 geschlossene, lückenlos aneinandergrenzende Teilintervalle ein. Für die grosse Kugel zertifiziert er zuerst das Ableitungsvorzeichen und prüft dann beide Vorzeichen am Rand einer rationalen Zelle mit Breite 10⁻¹⁰. Zeitliche Unterteilung dient hier der Intervallrechnung. Die ausgewiesenen Wertebereiche in Ergebnis.json sind nach aussen gerundete Einschliessungen, keine Behauptung exakter Extrema.

Die ursprüngliche Studie hat die unterscheidenden Zielbahnen bei x=1/2 gefunden und die dortigen Anbindungen dynamisch als freie positive oder leere Einzelsonden verworfen. Die neue Rechnung prüft die Zeitrobustheit der **geometrisch vorgegebenen** Testbahnen. Sie leitet weder einen freien stationären Sondenzustand zur Zielzeit her noch entscheidet sie über alle alternativen Positionen oder alle N23-Anbindungen bei anderen Zeiten. Die Bahnbezeichnung nach Ereignisnummer ist eine Laborvorgabe der Kontrollrechnung. Für eine intrinsische CST-Auslese wären eine relabelungsinvariante, im Voraus lokalisierte Messbahn und eine physikalisch hergeleitete, stationär verträgliche Seitenbeobachtung separat erforderlich. Die acht physischen Radien und die 60 P3-Punkte bleiben offen.

## Offline wiederholen

    python3 -B pruefen.py

Der Prüfer nutzt die Standardbibliothek, verifiziert beide Eingabe-Prüfsummen und vergleicht das gesamte Ergebnis byteweise als UTF-8-Text unter LF. Eingaben stammen aus [der publizierten N22-Kugelkontrolle](https://github.com/thomasmgfeller/x6-spectral-astrolabium/tree/2c08c72af7fa7d075f50decc48c9531d64d61c66/research/rax_cqg/dust_collapse/n22_aeussere_materiegrenze_und_n23_sonden_v0_1). Die Auswahl der Bahn mit dem frühesten zugesicherten Übergang ist eine geometrische Optimierung über die drei bekannten Kandidaten.
