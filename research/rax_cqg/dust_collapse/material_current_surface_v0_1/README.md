# Zwei Staubmassen vom Anfangsschnitt bis zur materiellen Oberfläche

**P3 auf dem gekoppelten CST-Träger · HOLD_NOT_ELIGIBLE / NOT_RUN.** Die bisherige Randpräparation legt keine der beiden gewünschten positiven Massen als scharfen Wert des direkten Wirkungsstroms fest. Das lässt sich für jeden der 1 048 untersuchten N15-Endtypen an zwei inneren Dichtebelegungen mit denselben Anfangsdaten zeigen. Ein positiv präparierter Markerstrom transportiert dagegen beide Massen exakt über alle untersuchten Ideale. Seine Strommarken enthalten keine Flächenmetrik.

Für die marginal gebundene klassische Einstein-Staub-Referenz ist die gesamte Messung ausführbar. Dort stammen Gesamtmasse, Weltrohr und Fläche aus derselben Lösung. In geometrisierten Einheiten gilt bei der gemeinsamen Staubeigenzeit T*=5√5/6:

| Anfangsmasse aus dem Strom | Transportierte Masse bei T* | Seitlich übergetretene Masse | Fläche bei T* | Arealradius bei T* |
|---:|---:|---:|---:|---:|
| 1/4 | 1/4 | 0 | 1 153,023696 | 9,578868 |
| 4 | 4 | 0 | 856,297906 | 8,254818 |

Die Differenzen „schwer minus leicht“ betragen rund −296,725790 Flächeneinheiten und −1,324050 Längeneinheiten. Die gekoppelten CST-Flächen und ihr Kontrast stehen in `results.json` gesondert als fehlende Werte.

## 1. Direkter Versuch mit dem Strom der gekoppelten Wirkung

Der endliche Kandidat enthält die Staubuhr T, die integrierte Dichte w und die auf derselben Ordnung C bestimmte Matrix B. Mit der Projektvorzeichenkonvention lautet der durch Uhrvariation definierte Kantenstrom

`j(y→v) = (β/2) w_v b(y,v) (T_v−T_y)`, mit `b(k) = (1,−9,16,−8,0,…)` und β>0.

Hier ist k die Zahl der strikt zwischen y und v liegenden Ereignisse. Dies ist der dimensionslose Strom in der verwendeten Projektnormierung. Die gekoppelte minimale Skalarwirkung hängt bei festem C nicht direkt von T oder w ab. Den Strom berechnet der beigefügte Originalcode der Variation, der β als Einheit ausklammert. Im endlichen Pfadintegral sind die einzelnen Feldbelegungen im Allgemeinen nicht stationär. Schnittkonstanz des Variationsstroms würde im überstrichenen Inneren die entsprechende Uhr-Eulergleichung erfordern.

Sei P der vollständige Vergangenheitskragen aus den Ereignissen 0,1,2,3. Alle sieben inneren Ereignisse liegen strikt zwischen P und dem Zukunftskragen. Jede direkte Kante von P zum Zukunftskragen hat daher b=0. Die Schnittladung Q(P) hängt ausschließlich von den **Empfängerdichten hinter P** und von den beteiligten Uhren ab. Wir testen zwei zulässige Feldbelegungen mit identischer Randpräparation, identischen Uhren und identischer Ordnung:

1. Alle sieben inneren Dichten liegen auf ihrem Nullatom. Dann ist Q(P)=0.
2. Genau ein im Inneren minimales Ereignis v hat 0<w_v<1. Seine Koeffizienten von den vier Vorgängern sind der Reihe nach (−8,16,−9,1). Mit den geerbten Kragenuhren (−5Δ,−4Δ,−3Δ,t) ergibt sich exakt
   **Q(P)=−β w_v(3Δ+t)/2**. Die Uhr T_v kürzt sich heraus. Für beide veröffentlichten Uhrfenster gilt t=−2Δ+δ mit |δ|≤3/32. Aus Δ²=2/(19β), β=4/√6<2 folgt Δ>3/32, also Q(P)<0.

Die Formel wurde für alle 2 438 minimalen inneren Zeilen der 1 048 Endtypen überprüft. Für jeden Endtyp kontrolliert der ursprüngliche Variationscode die vollständige Schnittladung und ihre Gleichheit mit der Summe der Randgradienten an rationalen Testdaten. Das Vorzeichen auf den ganzen tatsächlichen Uhrfenstern folgt analytisch. Beide Belegungsarten haben Träger im deklarierten Produktmass aus Nullatom und positiver Dichte. Aus diesem Trägerargument folgt keine Born-Wahrscheinlichkeit.

Ein Vorzeichenwechsel oder eine konstante Umrechnung in Masseneinheiten lässt die erste Belegung bei null. Auch ein positives Umverteilen von Kantenströmen, das **diese** Schnittladung auf jeder Belegung unverändert erhalten soll, kann daraus keine fest vorgegebene positive Anfangsmasse machen. Beide Randdichtezentren 1/8 und 1/4 führen zu derselben Unterscheidung. Das Ergebnis schliesst die direkte Identifikation mit der scharf präparierten P3-Ruhemasse aus. Eine aus der Theorie abgeleitete Projektion auf einen Massensektor oder eine anders definierte grobe Stromobservable bleibt offen. Die Rechnung behandelt die zugelassenen endlichen Ordnungstypen mit dem erklärten Feldmass. Eine neue kohärente Zielintegration für alle Typen wurde nicht durchgeführt.

## 2. Zwei explizite positive Anfangsströme auf denselben Ordnungen

Als getrennten Versuch benutzen wir auf denselben Ordnungen den publizierten Vertrag für einen konservativen, markierten Staubstrom. Quelle ist das letzte Ereignis des Vergangenheitskragens, Senke das erste des Zukunftskragens. Wir schicken M entlang der maximalen, aus Überdeckungsrelationen bestehenden Ketten zwischen beiden. Jede vollständige Kette erhält denselben Anteil. Diese zusätzliche, umbenennungsinvariante Routingregel wird vor beiden Massen gleich gewählt.

Für die Kante u→v ist ihr Transportgewicht M mal der Zahl der maximalen Pfade durch die Kante, geteilt durch die Zahl aller maximalen Pfade. Der Zähler ist das Produkt der Wegzahl von der Quelle bis u und von v bis zur Senke. An jedem inneren Knoten stimmen dadurch Zu- und Abfluss überein. Das archivierte Modul `current.py` kontrolliert Vorwärtsrichtung, Positivität, Bilanz und Schnittmasse mit exakten Brüchen.

| Geprüfte Grösse | Ergebnis |
|---|---:|
| Skalar zugelassene kanonische N15-Endtypen | 1 048 |
| Schnitte aus P und einem inneren Ordnungsideal, über alle Typen, je Masse | 21 792 |
| Direkte Massenvergleiche für beide Präparationen | 43 584 |
| Endtypen mit mehr als einem maximalen Transportpfad | 1 047 |
| Endtypen ohne inneres Ereignis, das auf jedem solchen Pfad liegt | 786 |

Alle geprüften Schnitte tragen genau die eingespeiste Masse 1/4 beziehungsweise 4. Bei mehr als einem Pfad kann man ihre Anteile auch zwischen zwei Wegen verschieben und dieselbe Randmasse behalten. Die Bilanz gilt somit auch auf jedem über eine Uhr ausgewählten solchen Ideal. Es fehlt die physikalische Identifikation eines dieser Ideale mit T* des Staubballs. Ein innerer Transportpfad beschreibt zudem keine zweidimensionale materielle Grenze. Dieser Versuch konstruiert einen markierten positiven Strom auf den gegebenen Ordnungen. Die Kantenmarken wurden nicht aus der gekoppelten Amplitude gewonnen.

## 3. Anfangspräparation, Transport und Fläche im klassischen Vergleich

Für den P3-Vergleich gelten G=c=1, R₀=10 sowie homogener, druckloser und marginal gebundener Einstein-Staub. Materiallabels sind die radiale Koordinate u und die beiden Winkel. Auf der Anfangsscheibe mit R(0,u)=10u wird die Dichte durch die geforderte Schnittmasse normiert. Das Stromintegral innerhalb von u ergibt m(u)=Mu³. Der Staub endet bei u=1 und der Aussenraum ist Vakuum. Die materielle Oberfläche ist die Grenze des positiven Staubsupports. Ein inneres mitbewegtes Rohr hätte ebenfalls Nullfluss; bei u=1/2 enthält es nur M/8.

Auf dem marginal gebundenen Zweig ist die radiale Eigenlänge R′du. Dadurch stimmen die über den Staubstrom gemessene eingeschlossene Ruhemasse und die in der klassischen Einsteingleichung auftretende Massenfunktion überein. Mit der kollabierenden Anfangsrichtung gilt Ṙ=−√(2m(u)/R). Die materielle Markierung u=1 wird bis T* propagiert. Im Solver wird die Gleichung für R^(3/2) integriert. Ein zweiter Integrator löst unabhängig die untransformierte Gleichung in der Eigenzeit mit 32, 64 und 128 Schritten. Der bekannte Endradius dient erst nach der Rechnung zum Vergleich.

Die anfänglichen Stromanteile werden auf 8, 16 und 32 radiale Schalen und je 128 Winkelbereiche aufgeteilt. Zu drei Uhrständen sind die geschachtelten Schalen geordnet, die gesamte Masse stimmt, und die Aussenfläche behält ihre Materiallabels. Die Rechnung verfolgt mitbewegte Massenmarker und zählt Ein- und Austritte gesondert. Über die mitbewegte Fläche tritt in keiner Richtung Staub. Durch den festen Kontrollradius 9 strömt in beiden Massenfällen auf allen drei Schalenauflösungen eine positive Markermasse nach innen. Für dieselbe entwickelte Metrik lauten die Komponenten der induzierten Winkelmetrik R² und R²sin²θ. Die Integration ihrer Flächendichte über die 128 Winkelbereiche liefert die oben angegebenen Flächen. Rationale Einschlüsse für Radius, Fläche und beide Differenzen stehen im Ergebnis-JSON.

Die verwendeten Feldgleichungen sind die sphärischen Einstein-Staub-Gleichungen mit Energieparameter E=0; die Wahl des negativen Geschwindigkeitszweigs beschreibt Kollaps. [Klassische Gleichungen (6) und (7)](https://pure.mpg.de/pubman/item/item_52863_2/component/file_52864/jcap8_10_003.pdf) · [P3-Vertrag im geprüften Repository-Stand](https://github.com/thomasmgfeller/x6-spectral-astrolabium/blob/024a3de4ee7e616789c0103fc4e563becaf125b5/research/rax_cqg/dust_collapse/correspondence_v0_1/DERIVATION.md)

## 4. Warum eine transportierte Masse noch kein gewichtsuniformes Flächensignal liefert

Eine geometrische Kontrolle hält sogar alle mitbewegten Eigenvolumina fest. Sei B(T) der klassische Oberflächenradius der jeweiligen Masse, x=T/T_end, h(M)=(8M−17)/15, k=0 oder 1. Betrachte allein als Prüfung der Identifizierbarkeit die synchronen Innenmetriken

`ds²=−dT²+L²du²+S²dΩ²`, mit `s=1+k h x³u²`, `S=B u s` und `L=B/s²`.

Auf 0≤x≤1/2, 0≤u≤1 sind s positiv und ∂S/∂u>0. Das Zentrum ist regulär. Die Zeit einer mitbewegten Linie ist in beiden Fällen T. Ihr Einheitsgeschwindigkeitsfeld ist geodätisch, weil g_TT=−1 und g_Tu=0. Die Identität LS²=B³u² erhält die räumliche Volumenform **punktweise**. Mit derselben Dichte 3M/(4πB³) gilt die Kontinuitätsgleichung, und jede materielle Zelle hat dieselbe Masse und denselben seitlichen Nullfluss. Anfängliche Form, Geschwindigkeit und zweite Zeitableitung stimmen ebenfalls überein. Die Oberfläche bleibt u=1. Ihre induzierte Fläche beträgt jetzt 4πS(T,1)².

| Ergänzte Geometrie | R₄−R₁/₄ bei T* |
|---|---:|
| k=0, klassische Einstein-Staub-Lösung | −1,324050 |
| k=1, geometrische Gegenkontrolle | +0,905161 |

Die zweite Metrik wird weder als zweite Einstein-Staub-Lösung noch als Lösung der gekoppelten CST-Wirkung behauptet. Diese Gegenkontrolle isoliert, welche Information selbst bei korrekter Massenerhaltung, mitbewegter Oberfläche, Staubeigenzeit und gleichem Volumen noch durch Geometriedynamik geliefert werden muss. Sie ist kein Intervall über Historiengewichte.

Für den physikalischen Vergleich müssten zwei mit derselben Regel präparierte Massensektoren, ihre Uhrentwicklung, die Flächenobservable der materiellen Grenze und ihre Paarung auf denselben Historien vorliegen. Eine kohärente Auslese benötigt dabei auch die Kreuzterme zwischen Historien. Ohne diese Zuordnung ist die Prüfung des Vorzeichens über die zulässigen globalen Gewichte *undefiniert*. Weitere Gewichtsscans auf der vorhandenen skalaren Gram-Matrix würden eine andere Observable auswerten.

## Offline wiederholen

Im entpackten Verzeichnis mit Python 3.10 oder neuer und der Standardbibliothek:

```sh
sha256sum -c SHA256SUMS
python3 -B run.py --out wiederholung.json
cmp results.json wiederholung.json
```

`design.json` hält die lokalen Entscheidungen vor der Auswertung fest. `sources.json` enthält den Git-Stand und die Blob-Prüfsummen aller übernommenen Eingaben; der Prüfer kontrolliert jede davon vor der Rechnung. Die Ausführung benötigt weder eine Netzverbindung noch externe Rechenressourcen.
