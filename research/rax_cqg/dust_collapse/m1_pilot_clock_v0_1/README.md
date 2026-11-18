# CST-DUST · M=1 auf der ersten Dichtestufe

[Offline-Prüfpaket](../packages/CST_DUST_M1_Pilot_Uhrtest.zip) · [Ergebnisse (JSON)](ergebnis.json) · [Folgeuntersuchung zur ersten Geburtsrate](../first_birth_rate_v0_1/README.md)

Stand 18. November 2026, nach PR #304. Der physikalische Pilot steht bei **HOLD_NOT_ELIGIBLE / NOT_RUN**. Auf der ersten physikalischen Dichtestufe sind 38 Vergleiche vorbereitet. In diesem Paket wurden null dynamische 4D-Staubballhistorien erzeugt.

## Rechnen und Ergebnisse lesen

Python 3.10 oder neuer und die Standardbibliothek genügen. Nach dem Entpacken startet `python3 -B start.py --out nachrechnung.json` die lokale Nachrechnung. Ein byteweiser Vergleich mit `ergebnis.json` prüft die Reproduzierbarkeit. Im Ergebnis enthält `M1.rows` für alle 38 Vergleiche Zeitpunkt bzw. Intervall, Observable, klassische Referenz, Toleranz und Fehlerskala. `physical_value` ist überall null im JSON-Sinn, also fehlend. Der Abschnitt `Uhr` enthält die Ergebnisse des separaten Referenzmodells. Die Eingabedateien sind mit Repository-Pfad und Git-Prüfsumme in [quellen.json](quellen.json) aufgeführt. Vor dem Lauf werden ihre Git-Blob-Prüfsummen kontrolliert.

## 1. Vergleichsplan für den ersten Massenfall

Für M=1, Zähldichte λ/λ₀=1 und die fünf gemeinsamen Uhrwerte x=0, 1/4, 1/2, 3/4, 1 gelten:

| Familie | Anzahl | Prüfung der klassischen Referenz |
| --- | ---: | --- |
| Radius, Dichte, Expansion und Beschleunigung | 20 | Alle analytischen Werte liegen in den veröffentlichten Euler-Intervallen mit 128 Schritten. |
| Gesamtmasse | 5 | Referenz M=1 auf jedem Schnitt. |
| Integrierter Seitenfluss | 12 | Vier Intervalle für die Materialoberfläche, den festen Radius R=4 und das schrumpfende mitbewegte Koordinatenfenster. Alle Beträge und Vorzeichen mit dem archivierten analytischen Fluss verglichen. |
| Anfangsgeschwindigkeit | 1 | dr/dx bei x=0 ist −1/6. |

Die geschlossene Materialoberfläche hat Nullfluss. Beim festen Radius ist der nach aussen positive Fluss negativ, beim schrumpfenden χ-Rohr positiv. Die Fehlerskala ist für alle drei die Anfangsmasse M. Der P3-Vertrag legt für die gesamte Familie von 524 Vergleichen ein Fehlerniveau von 0,05 fest. Auch für diesen Pilot bleibt das Niveau pro Vergleich bei 1/10 480. Die physikalische Basisdichte λ₀ und die Zahl der gezogenen Historien sind weiterhin offen.

## 2. Kann das Aufheben der Ereignisgrenze die Uhrpaarung auswählen?

Die bisher publizierten Paarungen verwenden α=1, den dimensionslosen Uhrwert 0≤s≤1 und beim Start die metrischen Gewichte (1,β,1,1) auf leerer Ordnung, Einzelelement und den beiden Zweierordnungen. Wir prüfen β=5/4 und β=4/3 unter derselben konstruierten Fortsetzung auf alle endlichen Grössen. Der rohe diagonale Ein-Geburts-Koeffizient eines Elternteils mit n Elementen ist für jedes Vergangenheitsideal I gleich 2⁻ⁿ. Die Rechnungen verwenden die inneren Ereignisse ohne den festen Anker, wie im geerbten Uhrintervallkern. Dieser Koeffizient betrifft die Betragsquadrate.

Für eine Ordnung P seien r(P) die Zahl der strikten Ordnungspaare und l(P) die Zahl ihrer Hasse-Kanten. Wir wählen testweise W(P)=2^[r(P)−l(P)]. Fügt man ein neues maximales Ereignis mit Vergangenheit I an, so wächst r um |I| und l um die Zahl maximaler Elemente in I. Frühere Hasse-Kanten bleiben bestehen. Unter den 2ⁿ Teilmengen der alten Ereignisse haben genau 2^[|I|−|max I|] die Abwärtshülle I. Daher gilt für jede endliche Ordnung

    2⁻ⁿ Σ_I W(P+I) = W(P).

Das entspricht der bekannten transitiven Perkolation mit Bindungswahrscheinlichkeit 1/2. Wir benutzen die Konstruktion als positiven Referenzfall. [Rideout und Sorkin, A Classical Sequential Growth Dynamics for Causal Sets](https://arxiv.org/abs/gr-qc/9904062)

**Lösung der Normgleichung.** Für n≥2 setzen wir h(P,s)=exp(−s)W(P). Für die beiden kleineren Stufen folgt aus der gleichen Gleichung h′(P,s)=−2⁻ⁿΣ_I h(P+I,s):

    h₁(s) = β−1+exp(−s)
    h₀(s) = (1−β)s+exp(−s).

Die beiden Zweierordnungen haben W=1. Die Werte bei s=0 stimmen damit für jede Wahl von β mit den zugehörigen vier Anfangsgewichten aus PR #304 überein. h₁ bleibt positiv. h₀ fällt und ist bei s=1 sogar im ungünstigeren Fall exp(−1)−1/3>0. Der Nachweis gilt für das vereinbarte Uhrfenster.

**Norm, Schnitte und Ereigniszahl.** Der Übergang auf eine bestimmte chronologisch beschriftete Erweiterung um k Elemente ist der integrierte Rohkoeffizient (b−a)^k/k! × 2^[−nk−k(k−1)/2], multipliziert mit h(Kind,b)/h(Elternteil,a). Bei einem Zwischenschnitt kürzt sich h. Summation über die am Schnitt mögliche Geburtszahl zerlegt das Uhrsimplex exakt. Für n≥2 ergibt die Summe der Rohkoeffizienten jeder Tiefe k, gewichtet mit W(Kind)/W(Elternteil), genau (b−a)^k/k!. Die normierte Zahl weiterer Ereignisse besitzt daher eine Poisson-Verteilung mit Parameter b−a. Für die Einzel- und die leere Stufe ergibt die Summation mit d=b−a explizit

    h₁(b)+(exp(d)−1)exp(−b) = h₁(a),
    h₀(b)+d h₁(b)+(exp(d)−1−d)exp(−b) = h₀(a).

Alle Zeilen sind damit normiert, und auf diesem Uhrfenster geht keine Wahrscheinlichkeit in unendlich viele Geburten verloren. Die Formel benötigt keinen vorgewählten Enduhrwert. Der Übergang ist ein diagonales Referenzmass. Seine Wahl von W enthält keine gemessene Staubmasse und führt zu keiner Auswahl aus der gekoppelten Wirkung.

**Messbare Unterscheidung im Referenzmodell.** Bei leerem Anfang ist die Wahrscheinlichkeit für keine Geburt bis s=1/2 gleich h₀(1/2). Die Werte sind exp(−1/2)−1/8 ≈ 0,481531 bzw. exp(−1/2)−1/6 ≈ 0,439864. Ihr Abstand 1/24 ist exakt. Die Einzelwerte ändern sich gegenüber dem Modell mit harter Grenze N=2. Der Abstand bleibt erhalten. In dieser Familie entspricht β genau der anfänglichen Rate −h₀′(0). Eine von dieser Familie unabhängige Herleitung jener Rate aus physikalischer Präparation, Randprodukt und gekoppelter Amplitude könnte die beiden Vorschläge trennen. Die dimensionslose Rate ist keine absolute Zähldichte und der Uhrwert s ist noch nicht mit der P3-Staubeigenzeit kalibriert.

**Endlicher Audit.** Für alle natürlich beschrifteten Ordnungen mit bis zu fünf inneren Ereignissen prüfen zwei Zählweisen jeden Übergang bis Grösse sechs. Geprüft wurden 408 Elternordnungen, 5 231 Erweiterungen, 280 rationale Schnittidentitäten und 60 Normhüllen für beide β zusammen. Das Weglassen der Teilmengen-Multiplizität verletzt 402 der 408 Zeilensummen. Für leeren Start ist die gesamte Wahrscheinlichkeit oberhalb N=6 für alle 0≤s≤1 kleiner als 1/12 000: Ab Endgrösse zwei ist die Wahrscheinlichkeit jeder Grösse n gleich exp(−s)sⁿ/n!. Die Schranke gilt für diese Referenzpräparation und dieses Ereignis. Sie liefert kein Fehlerbudget für physikalische P3-Observablen oder inverse Volumenmomente.

## 3. Entscheidung über den 15-Minuten-Piloten

Die zwei expliziten, auch ohne Elementzahlgrenze normierten Lösungen widerlegen die Eindeutigkeit durch Norm- und Schnittkonsistenz in dieser Klasse. Für eine unabhängige Festlegung von β braucht es beispielsweise den Ein-Geburts-Fluss am Anfang bei festem physikalischem Randzustand. Ein Abgleich von β mit der klassischen P3-Kurve würde diese Kurve bereits zur Modellwahl verwenden. Auch bei festgelegtem β benötigt der Pilot den geprüften gekoppelten 4D-Transport, die kalibrierten Messadapter und die im P3-Vertrag verlangten übrigen Eingaben. Der vollständige veröffentlichte Zulassungsbefund liegt im [P3-Zulassungsbefund](../correspondence_v0_1/results/eligibility.json).

Lokal liefen ausschliesslich die deterministischen Kontrollrechnungen. Für die physikalische Laufzeit und den Stichprobenfehler existiert weiterhin kein Messwert. Das vorgeschlagene Limit von 15 Minuten bleibt für einen ersten freigegebenen Ressourcenpilot vorgesehen.

[Repository-Stand](https://github.com/thomasmgfeller/x6-spectral-astrolabium/tree/b595e3c971f4f80ea56c41ea1de0b942d67dce1a/research/rax_cqg/dust_collapse)

## Gemessene Laufzeiten der lokalen Kontrollen

Fünf Wiederholungen der klassischen Referenz für M=1 (128 Schritte und 20 Prüfwerte) dauerten im bereits laufenden Python-Prozess im Median 2,6 ms. Die vollständige M=1-Vorbereitung samt Uhrtest dauerte bei fünf separaten Python-Starts im Median 0,16 s. Beide Messungen stammen aus der lokalen Ausführungsumgebung. Eine gemessene Laufzeit für eine physikalische Staubballhistorie steht aus.
