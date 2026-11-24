# Bestimmt der lokale N15-Staubball eine kosmologische Expansionskurve?

CST-DUST · 24. November 2026 · Projektstand d00c2196, anschliessend an den Everpresent-Λ-Distanztest.

**Die geprüfte lokale Information lässt mehrere kosmologische Fortsetzungen zu.** Selbst bei exakt bekannter klassischer Kollapsgeometrie und vorgegebenem heutigem Hubblewert sind zwei homogene Staubhintergründe mit verschiedenen normierten Expansionskurven möglich. Eine zusätzliche äussere Volumenmessung unterscheidet diese beiden Hintergründe im Kontinuum. Der N15-Katalog liefert dafür bislang weder einen kosmologischen Beobachtungsbereich noch eine geeichte räumliche Volumenauslese. Die 60 physischen P3-Einträge tragen den Status NOT_RUN.

[Kurzbericht](Kurzbericht.pdf) · [Typenweise Antiketten](resultate/antiketten.csv) · [Exakter klassischer Anschluss](resultate/anschluss.json) · [Volumenfenster](resultate/volumenfenster.json) · [Lokaler Prüfplan](pruefplan.txt)

## 1 · Was der endliche Katalog liefert

Die 1 048 veröffentlichten Typen werden aus den drei Rangangaben des Katalogs nach derselben Bedingung wie in der Quelldatei support.py ausgewählt. Die 61 Typen der jüngeren Massenauslese sind eine separat ausgewertete Untermenge. Die Typkennzahl codiert die Relation der sieben inneren Ereignisse in den 21 möglichen Paaren. Je vier geordnete Kragenereignisse liegen kausal vor bzw. hinter dem Inneren.

Eine Antikette besteht aus paarweise kausal unvergleichbaren Ereignissen. Sie heisst inklusionsmaximal, wenn sich kein weiteres Ereignis hinzufügen lässt. Die grösste mögliche Kardinalität heisst Breite. Der Prüfer untersucht alle 127 nichtleeren Teilmengen des Inneren. Er kontrolliert Transitivität und Antisymmetrie und berechnet die Breite zusätzlich durch eine minimale Überdeckung mit Ketten.

| Katalog | Breite 1 | Breite 2 | Breite 3 | Breite 4 | Unterschiedlich grosse inklusionsmaximale Antiketten im selben Typ |
|---|---:|---:|---:|---:|---:|
| 1 048 zugelassene Typen | 1 | 188 | 712 | 147 | 883 |
| 61 Typen der Massenauslese | 0 | 0 | 21 | 40 | 50 |

Beispiel Typ 2454. Die Mengen {4, 5, 14} und {5, 6, 13, 14} sind beide inklusionsmaximal. Sie überlappen und stellen keine zwei aufeinanderfolgenden Uhrzeiten dar. Erst eine eigene Schnitt- und Volumenvorschrift könnte solche Mengen einer physikalischen Auslese zuordnen. Eine Regel, die immer die grösste Kardinalität wählt, liefert je Ordnung einen Einzelwert und noch keinen zeitlichen Verlauf.

Der gesondert geprüfte Referenztyp 2097151 ist mit beiden Kragen eine totale Ordnung mit 105 gerichteten Vergleichspaaren. Jede der 15 inklusionsmaximalen Antiketten enthält genau ein Ereignis. Im Inneren sind es sieben Einer-Antiketten. Ein direkt proportional zu dieser Kardinalität gesetztes räumliches Volumen wäre auf dieser Kette konstant. Der Typ gehört zu den 1 048, liegt aber ausserhalb der 61er-Untermenge. Die publizierten Uhr- und Dichtemarken enthalten zusätzliche Informationen. Andere, dynamisch begründete Volumenschätzer bleiben offene Kandidaten.

Bei einer treuen Poisson-Einbettung auf vorgegebener Mannigfaltigkeit entspricht die erwartete Ereigniszahl einer Region ihrer *Raumzeit*-Volumengrösse mal Sprinklingdichte. Ein räumliches Eigenvolumen setzt eine zusätzliche Definition von Region und Zeitfenster voraus. Die endlichen N15-Modellhistorien werden hier als die tatsächlich veröffentlichten Ordnungen behandelt. [CST-Überblick von Surya](https://arxiv.org/abs/1903.11544) · [N15-Quellen mit Git- und SHA-256-Prüfsummen](quellen/herkunft.json)

## 2 · Zwei exakte klassische Anschlusslösungen

Die P3-Referenz verwendet homogenen drucklosen Staub, G=c=1 und marginal gebundenen Kollaps. Wir wählen die veröffentlichte Masse M=1 und den Anfangsradius 10. Im dokumentierten Zeitfenster x=T/T_E von 0 bis 1 sind der Oberflächenradius und die lokale Kontraktionsrate durch R³=1000(1−x/4)² und T_E H_lokal=−1/[6(1−x/4)] gegeben. Ein Schwarzschild-Vakuum der Masse 1 schliesst an die Balloberfläche an.

Als Test für eine zusätzliche kosmologische Fortsetzung lassen wir einen gemeinsamen Teil dieses Vakuums stehen und schliessen weiter aussen einen expandierenden Friedmann-Lemaître-Robertson-Walker-Hintergrund (FLRW) an. Beide Aussenmodelle sind exakte, drucklose Einstein-Lösungen mit Λ=0. Dies variiert die grossräumige Randbedingung. Die veröffentlichte isolierte Vakuumreferenz enthält selbst keinen vorgeschriebenen kosmologischen Hintergrund. Wir synchronisieren den Anfang des lokalen Kollapsfensters mit der gewählten äusseren Vergleichsepoche durch die freie Zeitverschiebung auf jeder Anschlusstrajektorie in Schwarzschild-Koordinaten. Die Balloberfläche fällt von 10 nach innen, während beide äusseren Röhren von mindestens 40 nach aussen laufen. Der Schwarzschild-Bereich dazwischen ist im ganzen geprüften Vorwärtsfenster regulär.

Schreibe b=a/a₀ und R_b=R_b0 b. Am äusseren komovierenden Rand gilt für die Misner-Sharp-Masse M=4πρ R_b³/3, mit der kosmischen Staubdichte ρ. Lege für beide Konstruktionen H₀²=1/32000 fest. Dann gilt

    Ωm0 = 2M / (R_b0³ H₀²),        Ωk0 = 1 − Ωm0,
    H²/H₀² = Ωm0 b⁻³ + Ωk0 b⁻²,    ε = R_b0² H₀² Ωk0,
    Ṙ_b² = 2M/R_b + ε,             R̈_b = −M/R_b².

Die gleiche induzierte Eigenzeit und der gleiche Arealradius sichern die Gleichheit der ersten Fundamentalform. Auf der Schwarzschildseite folgt für den positiven radialen Normalanteil (n·∇R_b)²=1−2M/R_b+Ṙ_b²=1+ε. Auf der FLRW-Seite ist dieser Term 1−kχ²=1+ε in der komovierenden Arealkoordinate χ. Mit derselben, zu zunehmendem Radius gerichteten Normalen stimmen damit die Winkelkomponenten der äusseren Krümmung überein. Beide Randbahnen sind zeitartig geodätisch, also gilt auf beiden Seiten K_ττ=0. Eine dünne Materieschale ist an diesen Anschlüssen entbehrlich. Der Prüfer verifiziert die beiden Koeffizienten der Randbewegung exakt sowie die Eigenzeit, die Winkelkrümmung und die Beschleunigung an drei Skalen. [Mars, Mena und Vera, Abschnitt 2](https://arxiv.org/pdf/1307.4371) · [Lokale Kollaps- und Vakuumreferenz](quellen/klassischer_anschluss.md)

| Äusserer Staubhintergrund | R_b0 | Ωm0 | Ωk0 | E′(0) für E=H/H₀ |
|---|---:|---:|---:|---:|
| Räumlich flach | 40 | 1 | 0 | 3/2 |
| Negativ räumlich gekrümmt | 50 | 64/125 | 61/125 | 157/125 |

Für komovierende Beobachter im homogenen Aussenbereich gilt 1+z=1/b. Folglich unterscheiden sich die Steigungen der beiden Kurven um exakt 61/250. Dieser Befund ist lokal in der kosmologischen Epoche. Eine Lichtausbreitung quer durch den Staubball, eine Extrapolation seiner Vorgeschichte oder einen Distanzfit setzen wir dafür nicht voraus. Die beiden Anschlussradien wurden als rechnerisch einfache Beispiele gewählt. Sie sind keine Parameterbestimmungen. In der Familie R_b0 ≥ 40 gibt es bei festem H₀ kontinuierlich viele flache oder offene Fortsetzungen.

**Kontrolle bei erzwungener räumlicher Flachheit.** Für genau homogenen flachen Staub mit Λ=0 bestimmen die äusseren Feldgleichungen die Form E=(1+z)^(3/2). Für die beiden Radien ergeben sich dann H₀²=1/32000 und 1/62500. Wer zusätzlich H₀ vorgibt, hat innerhalb dieser eingeschränkten Familie die Kurvenform schon durch die äusseren Annahmen festgelegt. Der Vergleich mit dem offenen Fall zeigt die fehlende Auswahl zwischen verschiedenen äusseren Hintergrundgesetzen. Das klassische Gegenbeispiel entscheidet keine Eindeutigkeitsfrage für eine künftige globale quantendynamische Theorie.

## 3 · Welche Zusatzmessung die beiden Hintergründe trennt

In einer komovierenden, homogenen äusseren Zelle gilt für das räumliche Eigenvolumen V/V₀=b³. Mit physikalischer Staubeigenzeit folgt

    H = V̇/(3V),     D = V V̈/V̇² = (2−q)/3 = 2/3−Ωm/6.

Hier ist q=−a(d²a/dt²)/(da/dt)² der Verzögerungsparameter. Die letzte Gleichheit verwendet die Staub-Friedmann-Gleichungen mit Λ=0. Für die Vergleichsepoche ergeben sich D=1/2 und D=218/375. Der Unterschied beträgt 61/750. Innerhalb dieser Modellfamilie bestimmt eine externe Messung von D deshalb Ωm0=4−6D. Im allgemeinen inhomogenen Fall braucht es eine Mittelungsvorschrift und eine gesonderte Abbildung auf beobachtete Rotverschiebungen. [Buchert, Staubmittelung auf komovierenden Gebieten](https://arxiv.org/abs/gr-qc/9906015)

Um diese Zusatzgrösse an einem kontrollierbaren Zähler zu prüfen, setzen wir s=H₀(t−t₀). Für ganzzahlige j=−1, 0, 1 und Breite h heisst W_j das Integral von b(s)³ über das Intervall von (j−1/2)h bis (j+1/2)h. Die physikalischen Vierervolumina haben alle denselben Vorfaktor V₀/H₀. Er kürzt sich im Ausdruck

    D_h = 4 W₀ (W₊ − 2 W₀ + W₋) / (W₊ − W₋)².

Für glattes V mit V̇ ungleich null nähert sich D_h mit Fehler O(h²) dem momentanen Wert. Prüfmethode A integriert die Friedmann-Gleichung in b und invertiert die Eigenzeit mit 60 Dezimalstellen. Prüfmethode B berechnet aus b² b″=−Ωm0/2 eine Ordnung-48-Taylorreihe in s mit rationalen Koeffizienten und integriert deren Kubus bis zur selben Ordnung. Die grösste beobachtete relative Abweichung der ausgewerteten Fensterintegrale bleibt kleiner als 5 × 10⁻³⁸. Dies ist ein Vergleich der Rechenwege. Für den flachen Fall folgt zudem analytisch D_h=1/2+3h²/32.

| Fensterbreite h | D_h flach | D_h offen | Bestmögliche Trefferquote mit insgesamt 15 synthetischen Ereignissen |
|---|---:|---:|---:|
| 1/8 | 0,501465 | 0,579459 | 50,2104 % |
| 1/16 | 0,500366 | 0,580864 | 50,0523 % |
| 1/32 | 0,500092 | 0,581216 | 50,0130 % |
| 1/64 | 0,500023 | 0,581304 | 50,0032 % |

Die Trefferquote gilt ausschliesslich für diese zwei bekannten äusseren Modelle, gleiche Vorchancen, drei beobachtete **Zählwerte** und insgesamt genau 15 Ereignisse in der äusseren Zelle. Unter unabhängigem Poisson-Sprinkling bei gleicher konstanter Intensität sind die drei Zahlen bedingt auf ihre Summe multinomialverteilt mit p_j=W_j/ΣW. Für jedes der 136 möglichen Tripel wählen wir das wahrscheinlichere Modell und summieren die grössere der beiden gemeinsamen Wahrscheinlichkeiten mit Faktor 1/2. Die Auswertung verwendet alle Tripel numerisch. Die hohe Präzision der idealen Fensterintegrale überträgt sich bei wenigen gezählten Ereignissen nicht auf eine Einzelmessung. Die Bedingung auf die Summe entfernt die gemeinsame Ereignisnormierung. Ein Klassifikator mit präzisen Ereigniszeiten, weiteren Beobachtungen oder einer absolut kalibrierten Gesamtzahl hätte andere Daten. Das N15-Ensemble ist kein solches äusseres Poisson-Experiment.

## 4 · Entscheidung und Reproduktion

Die Antiketten- und Anschlussrechnungen klären zwei unterschiedliche Hindernisse. Erstens muss eine N15-Auslese den Zusammenhang einer Uhr und eines räumlichen Volumens begründen. Zweitens muss eine kosmologische Erweiterung einen äusseren Beobachtungsbereich samt Dynamik und Zustandsgewichten festlegen. Die synthetische Volumenmessung bietet einen testbaren Kalibrierfall, sobald ein solcher Bereich vorliegt. Dann lassen sich Uhren, Vierervolumina und Verfeinerung zunächst gegen die zwei hier angegebenen Aussenlösungen blind prüfen. Erst danach hätte ein aus N15 hergeleiteter Vergleich mit DESI oder Pantheon+ eine eigenständige Theorievorhersage. Die vorangegangenen Evidenzwerte gehören zum publizierten Everpresent-Λ-Modell.

Zum Nachrechnen im entpackten Ordner genügen Python und mpmath (hier 1.3.0). Sämtliche Eingaben liegen lokal vor.

```sh
sha256sum -c SHA256SUMS
python -B pruefen.py --out nachrechnung
diff -r resultate nachrechnung
```

Die Originalquellen sind über Git-Objekt-IDs und SHA-256 an einen festen Stand gebunden. Prüfsummen des vor der Auswertung lokal geschriebenen Prüfplans haben keinen externen Zeitstempel. Die Auswertung der realen Katalogdateien und die synthetischen Referenzversuche sind vollständig getrennt nachvollziehbar. [Fester Repository-Stand](https://github.com/thomasmgfeller/x6-spectral-astrolabium/tree/d00c21965fd37f08d4979653ef6e5ad96e5a785a/research/rax_cqg/dust_collapse)
