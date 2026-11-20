# Früher Arealradius bei zwei Staubmassen

**Ergebnis für CST-DUST-C1 · HOLD_NOT_ELIGIBLE / NOT_RUN.** Bei derselben frühen Staubeigenzeit unterscheidet die klassische P3-Referenz die beiden Massen bereits mit getrennten 5-%-Bändern. Für die gekoppelten endlichen Historien fehlt die kalibrierte Zuordnung zur materiellen Oberfläche. Der Radius und seine Streuung über die zulässigen Gewichte sind daher unbestimmt. Es wurden keine neuen dynamischen vierdimensionalen Staubballhistorien erzeugt.

Grundlage ist der Repository-Stand [3c159b6](https://github.com/thomasmgfeller/x6-spectral-astrolabium/tree/3c159b6a2ece918a478496b6727f7f2c782accff/research/rax_cqg/dust_collapse). Die Eingaben enthalten die unveränderten einschlägigen Quellen und das veröffentlichte Vier-Marken-Prüfpaket. Die Auswahlregel in `design.json` wurde lokal vor der Auswertung festgehalten. Eine öffentliche Vorregistrierung dieser neuen Untersuchung liegt nicht vor.

## 1. Zwei Massen bei gleicher Zeit

Wir nehmen die kleinste und die grösste der drei veröffentlichten Massen und denselben Anfangsradius 10 in Einheiten mit G=c=1. Gesucht ist der erste positive Zeitpunkt auf dem bestehenden P3-Gitter, an dem die abgeschlossenen Referenzbänder für den Radius auseinanderliegen. Dieser Zeitpunkt wurde ausschliesslich aus der klassischen Referenz bestimmt. Für beide Massen gilt x=T/T_end mit T_end=5√5/3.

Der klassische Referenzradius ist R=10(1−√M x/4)^(2/3). Bei x=1/4 überlappen die beiden Bänder. Bei x=1/2, also T*=5√5/6, ergibt sich:

| M | Exakter klassischer Radius | R, gerundet | 5-%-Band, gerundet | Physikalischer CST-Radius |
|---:|---|---:|---|---|
| 1/4 | 10(15/16)^(2/3) | 9,578868 | [9,099925, 10,057811] | unbestimmt |
| 4 | 10(3/4)^(2/3) | 8,254818 | [7,842077, 8,667559] | unbestimmt |

Die klassische Differenz R₄−R₁/₄ beträgt rund −1,324050. Zwischen den Toleranzbändern liegen rund 0,432365 Radiuseinheiten. Ein einziger massenunabhängiger Radiuswert kann beide Vorgaben nicht erfüllen. Der schwerere Ball liegt in der Referenz am Testzeitpunkt noch bei R>2M. Die Trennung der Bänder ist eine Eigenschaft des gewählten Tests, keine Abschätzung des physikalischen Gesamtfehlers.

Die analytischen Radien wurden durch exakte rationale Vergleiche nach Kubieren in allen acht archivierten ODE-Einschliessungen geprüft (zwei Massen, 128/256/512/1024 Schritte). Die acht zugehörigen physischen Checkpoint-Einträge auf den vier Dichtestufen 1, 2, 4, 8 tragen alle NOT_RUN. Die Radiuswerte und der Massenkontrast bleiben im Ergebnis-JSON ausdrücklich null im Sinne von „fehlend“. Ein volles P3-PASS würde weitere Observablen, Verfeinerungsstufen und die vereinbarte simultane Unsicherheitskontrolle voraussetzen.

## 2. Was die globale Gewichtung tatsächlich festlegt

Wir verwenden ausschließlich die publizierte markierte Ein-Kanten-Familie mit vier austauschbaren Einfügungen, nichtnegativen feinen Gewichten und sämtlichen 72 älteren N13-Präfixmassen. Die anderen N14-Koeffizienten dürfen sich bewegen. Bedingt auf Präfix 1564 ist p_j=q_j/(Σᵢ qᵢ) der Anteil eines Endtyps. Diese Anteile sind Parameter der endlichen Gewichtskonstruktion. Ihre Verwendung in einer kohärenten Amplitude erfordert eine eigene Ausleseregel.

| Endtyp j | Exaktes Minimum von p_j | Exaktes Maximum von p_j |
|---|---:|---:|
| 766, 926, 2013, 2014, 2015, 5566 | 0 | 1 |
| 990 | 0 | 3/4 |
| 1790 (A), 5374 (B) | 0 | 1/2 |
| 27006 | 0 | 4/5 |

Jede Grenze wird auf der abgeschlossenen nichtnegativen Gewichtsklasse erreicht. Bei strikt positiven Gewichten sind dies Infima und Suprema, denn der publizierte Zeuge mit Gewicht auf jeder Spalte lässt sich beliebig schwach beimischen. Die Grenzen sind komponentenweise scharf. Man kann die zehn Maxima nicht gleichzeitig einsetzen.

Die Rechnung baut die 928 Projektionsspalten vorwärts und rückwärts aus dem publizierten Katalog auf. Schreibe C für die ganzzahlige Löschmatrix mit Spaltensumme 24, b für die 72 normierten Präfixmassen, c_j für die ganzzahlige Zeile des lokalen Endtyps j. Für jedes Maximum enthält `weight_certificates.json` einen nichtnegativen Zeugen w und einen dualen Zeugen y. Der Prüfer kontrolliert mit Brüchen
`Cw = 24b`, `Cᵀy ≥ c_j` und `c_j w = 24 bᵀy`. Division durch 24 b₁₅₆₄ ergibt den Tabellenwert. Für jedes Minimum genügt einer der zertifizierten reinen Vektoren eines anderen Endtyps.

Zehn so gefundene zulässige Vektoren haben neun linear unabhängige Differenzen. Wegen Σ p_j=1 hat der lokale zulässige Bereich daher **exakt affine Dimension neun**. Die vierte Marke schränkt die Form des Bereichs ein. Sie bestimmt weder den lokalen Gewichtsvektor noch das Verhältnis A:B. Der Befund bezieht sich auf diese bedingte endliche Familie. Er bestimmt kein fundamentales Mass auf beliebigen Kausalsets.

## 3. Die Fläche der materiellen Oberfläche

Die geometrische Definition für einen vollständigen Schnitt S der materiellen Weltfläche bei Staubeigenzeit T lautet R_ar(S)=√(A(S)/(4π)). Ein geschlossener, triangulierter Schnitt mit intrinsischen Kantenlängen liefert eine mögliche Auslese. Für eine Dreiecksfläche a und die drei quadrierten Kantenlängen i,j,k gilt 16a²=2(ij+jk+ki)−i²−j². Durch Summieren der Dreiecksflächen folgt der Radius ohne Kenntnis der Masse oder des Sollradius. Die Prüfung verlangt eine zusammenhängende geschlossene triangulierte 2-Sphäre, nichtentartete Dreiecke und genau zwei Flächen an jeder Kante; die Nachbarschaft jedes Eckpunkts muss einen einzelnen Zyklus bilden. Ob eine so gelieferte Oberfläche die physikalische materielle Oberfläche darstellt, ist eine separate Frage.

Zwei separat von den P3-Historien vorgegebene statische Referenzkugeln mit Radien 3 und 7 wurden in jeweils drei Auflösungen trianguliert. Die Auslese erhält nur Dreiecke und intrinsische Längenquadrate. Ein absichtlich geöffneter Schnitt wird zurückgewiesen. Die Abweichungen vom bekannten glatten Radius gehen bei **beiden** Referenzkugeln wie folgt zurück:

| Dreiecke | Relative Radiusabweichung, nach oben gerundet |
|---:|---:|
| 224 | 1,631 % |
| 960 | 0,409 % |
| 3 968 | 0,103 % |

Der Prüfer schliesst den stückweise flachen Radius mit rationalen Schranken ein. Die gemessene Abweichung zur glatten Kugel gilt nur für diese synthetischen Kontrollflächen. Sie darf nicht als physikalischer Diskretisierungsfehler in das P3-Budget eingesetzt werden.

### Wie weit trägt eine direkte Auslese auf N15?

In der geprüften N15-Kragenkonstruktion stehen vier paarweise geordnete Vergangenheitsereignisse vor allen sieben inneren und vier paarweise geordnete Zukunftsereignisse nach allen inneren. Jedes Kragenereignis ist mit jedem anderen Ereignis kausal vergleichbar. Wird ein roher simultaner Oberflächenschnitt durch eine Antikette realer Ereignisse repräsentiert, können somit alle seine verschiedenen Eckpunkte nur im Inneren liegen.

Die Prüfung zählt alle 1 048 skalar zugelassenen N15-Endtypen aus dem benutzten Katalog. Ihre maximalen Antikettengrössen 1, 2, 3 und 4 kommen genau 1-, 188-, 712- und 147-mal vor. Bei 147 Endtypen gibt es also wenigstens eine Vierer-Antikette. Diese allein identifiziert weder eine Materieoberfläche noch Dreiecke oder Längen. Zwei disjunkte 2-Sphären auf zwei verschiedenen Uhrständen, jede als gewöhnliches einfaches Dreiecksnetz mit mindestens vier verschiedenen Eckpunkten, benötigen mindestens acht innere Ereignisse. Keiner der 1 048 Endtypen erfüllt diese Voraussetzung. Das Argument gilt für diese direkte Zwei-Schnitt-Konstruktion. Ein extern kalibrierter Anfangsschnitt, ein rekonstruierter einzelner Schnitt oder eine Auslese über grössere Blöcke haben andere Voraussetzungen.

## 4. Weshalb selbst ein festes Historiengewicht den Radius offen lässt

Eine mögliche kohärente Radiusauslese für dieselbe Präparation in derselben physikalischen Paarung hätte die Form R_M(q,T)=(q†B_M(T)q)/(q†G_M(T)q) für q†Gq>0. Dabei enthält G die Norm der betreffenden konditionierten Zustände, B die Matrixelemente des **Radiusoperators**. Bei gegebener positiver Flächenobservable wäre dies die Erwartung von √(Â/(4π)). Die Wurzel aus der mittleren Fläche definiert bei Fluktuationen eine andere Observable. Eine Reduktion auf die zehn lokalen Komponenten setzt voraus, dass die Auslese wirklich durch diese Projektion faktorisiert. Für einen Massenvergleich ist dieselbe unabhängig definierte Gewichtsregel auf beide Präparationen anzuwenden.

Ein algebraisches Gegenbeispiel isoliert die fehlende Information. Halte alle endlichen strukturellen Gewichte und eine beliebige positive konditionale Gram-Form G fest. Ergänze auf 0≤x≤1/2 rein logisch eine Radiusform B=RₖG mit

Rₖ=10[1−√M x/6−M x²/144−k(4−M)x³], für k=0 oder k=1/3.

Beide Ergänzungen sind positiv, fallen monoton und haben bei x=0 denselben Anfangsradius sowie dieselbe erste und zweite Ableitung wie die jeweilige klassische Referenz. Die erste Ableitung ist auf dem Intervall negativ, und selbst der kleinste der vier Endwerte bleibt positiv. Beide Ergänzungen liefern für jeden Gewichtsvektor mit positiver Norm ihren jeweiligen Wert Rₖ. Dennoch wechselt das Vorzeichen der frühen Massendifferenz:

| k | R₄−R₁/₄ bei x=1/2 |
|---:|---:|
| 0 | −505/384 |
| 1/3 | +95/384 |

Das beweist die Unterbestimmtheit aus den geprüften strukturellen und anfänglichen Bedingungen. Die beiden Radiusformen sind keine aus der gekoppelten Wirkung abgeleiteten Lösungen. Ihre Zahlen sind weder ein physikalisches Vorhersageintervall noch Extremwerte über die Historiengewichte.

## 5. Anschluss an die gekoppelte Dynamik

Der nächste physikalische Gegenstand ist die Abbildung von einer **massenkalibrierten gemeinsamen Historie** auf ihren **materiellen Schnitt bei T\*** und auf dessen Fläche. Sie muss drei schon im Projekt angelegte Teile auf demselben Träger verbinden.

1. Die zwei Anfangspräparationen werden über den Staubstrom und seine Schnittmasse unabhängig festgelegt, bei gemeinsamem Anfangsradius und mit der Anfangsgeschwindigkeit aus dem Zwang. Die Eingabemassen dürfen nicht rückwärts aus dem zu prüfenden Radius bestimmt werden.
2. Die Staubuhr transportiert die materiell identifizierte Oberfläche bis zum gemeinsamen T*. Der Seitenfluss des Staubs prüft die Identifikation als mitbewegte Oberfläche. Gekoppelte Historien müssen die Umgebung beiderseits dieser Fläche enthalten.
3. Eine aus derselben Geometrie hergeleitete intrinsische Flächenauslese liefert zusammen mit der physikalischen Paarung die Radiusmatrixelemente und ihr Fehlerbudget. Erst damit wird die Extremwertaufgabe für den Massenkontrast über alle zulässigen Gewichte definiert. Ein kohärenter Quotient kann seine Extrema im Innern des Gewichtsbereichs haben.

Die veröffentlichte Stromkalibrierung, der N11-Zweigdetektor und die N14/N15-Randkerne liefern verschiedene Teile dieses Vorhabens. Zur gemeinsamen Abbildung fehlen auf diesen Historien die materiell identifizierte Oberfläche und deren intrinsische Flächendaten. Für die zwei frühen Massen bleiben die dynamischen Radien, ihr Vorzeichenvergleich und ihre gewichtsuniformen Intervalle offen. Der Hochdichte-Bounce wurde hier nicht geprüft.

## Offline nachrechnen

Python 3.10 oder neuer mit Standardbibliothek genügt. Nach dem Entpacken im Paketverzeichnis:

```sh
sha256sum -c SHA256SUMS
python3 -B run.py --out nachrechnung.json
cmp results.json nachrechnung.json
```

Der erste Befehl prüft die Dateien, der zweite rekonstruiert die Referenzen, sämtliche rationalen Gewichtsbeweise, die Antikettenzählung, die synthetischen Netze und die Gegenbeispiele. Für eine optionale neue Suche der LP-Zertifikate mit SciPy, NumPy und SymPy steht `weight_domain.py --search` zur Verfügung. Dabei darf ein anderer Optimierer gleichwertige Zeugen wählen. Die Datei `sources.json` führt die publizierten Einzelquellen mit Git-Blob-Prüfsummen. Das originale Vier-Marken-Paket ist separat nach SHA-256 fixiert. Lizenz und Attribution der übernommenen Projektquellen liegen bei.
