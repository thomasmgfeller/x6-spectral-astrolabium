# CST-DUST · Ist der früheste Uhrimpuls vor dem Senden bestimmbar?

**26. November 2026.** Auf der N19-Ordnung reichen die Staubuhren und Gewichte im strikten kausalen Vorlauf des Senders und auf dem Anfangskragen auch zusammen mit der Summe der vier Anfangsimpulse nicht aus, um den Einzelimpuls G₀ zu bestimmen. Zwei quellfreie stationäre Belegungen mit diesen identischen Daten unterscheiden sich am nominalen Hintergrund in G₀ um rund 0,00149394 in den Einheiten der normierten Wirkung. Bei dieser Gegenprobe dürfen die Gewichte am Zukunftskragen variieren.

Bei festgehaltenem Zukunftskragen ergibt sich ein zweiter Befund. Gibt man zwei bisher feste Freiheitsgrade der Anfangsuhren frei, so lassen sich G₀ und der Gesamtimpuls im stationären Randwertproblem lokal unabhängig vorgeben. Der Beweis benutzt die gesamte endliche Ordnung. Ein vor dem Senden verfügbares physisches Mess- oder Stellverfahren bleibt offen.

## Welche Daten der Uhrimpuls braucht

Für die archivierte Wirkung gilt A = 19 Σⱼ wⱼ + Σᵢ≺ⱼ bᵢⱼ wⱼ(Yⱼ−Yᵢ)², S = F₄ − A/38 und Gᵢ = −(∂A/∂Yᵢ)/2. Die vier Ereignisse 0,1,2,3 bilden den Anfangskragen, die vier Ereignisse 7,8,9,10 den Zukunftskragen. Der materielle Sender z=16 und Empfänger r=18 sind über positive Gewichte und zwei registrierte Zeitfenster bestimmt. Die Uhren der leeren Ereignisse 15 und 17 bleiben frei. Für das früheste Kragenereignis folgt

    G₀ = w₁(Y₁−Y₀) − 9w₂(Y₂−Y₀) + 16w₃(Y₃−Y₀)
         − 8 Σⱼ∈{4,5,6,16} wⱼ(Yⱼ−Y₀).

In der strikten Vergangenheit des Senders liegen nur 0,1,2 und 15. Die direkte Auswertung braucht den Sender selbst sowie unter anderem die Ereignisse 4,5,6, die mit ihm kausal unvergleichbar sind. Aus der transitiven Ordnung lassen sich alle Orte bestimmen, an denen sämtliche Summanden frühestens zusammengeführt werden könnten. Dies sind 7,8,9,10 mit dem einzigen minimalen Ort 7. In der Ordnung gilt 18 ≺ 7. Die Aussage über das Sammeln gilt für diesen direkten Ausleser. Ob andere Formeln dieselben Daten lokal erschliessen können, prüft das folgende Gegenbeispiel.

## Zwei stationäre Lösungen bei identischer lokaler Vergangenheit

Wir fixieren alle 19 Uhren, die vier Anfangsgewichte, die beiden leeren Ereignisse und den Gesamtimpuls ΣG auf ihren Referenzwerten. Wir setzen keine Quelle an Sender oder Empfänger. Die neun freien positiven inneren Gewichte und die vier zukünftigen Gewichte können variieren. Da die neun inneren Dichtegleichungen nur die Uhren enthalten, bleiben sie exakt erfüllt. Die elf freien Uhrgleichungen sind bei festen Uhren linear in den Gewichten. Zusammen mit der Gleichheit von ΣG ergeben sie zwölf unabhängige Bedingungen für dreizehn Gewichte.

Die Normierung δw₇=1 macht das System quadratisch und regulär. Die Lösung v ist eine Richtung im Raum der stationären Belegungen. Im gesamten archivierten Hintergrundintervall e ∈ [1/6 − 2⁻²², 1/6 + 2⁻²²] sind alle dreizehn Komponenten positiv. Entlang dieses Zweigs ist G₀ affin mit einer Steigung zwischen −747,232 und −746,708 pro Einheit w₇. Für die zwei Lösungen verwenden wir w± = w_ref ± 10⁻⁶ v. Alle positiven Gewichte bleiben zwischen null und eins. Uhrordnung, leere Gewichte, Materialfenster und sämtliche zwanzig inneren Gleichungen bleiben erhalten. Kein Feld im kausalen Vorlauf des Senders oder auf dem Anfangskragen unterscheidet sich zwischen den Lösungen.

| Vergleich | Zertifiziertes Ergebnis in Wirkungs­einheiten |
|---|---|
| G₀(w₋) − G₀(w₊) über das Hintergrundintervall | [0,00149341626; 0,00149446328] |
| Dieselbe Differenz bei e=1/6, zweite Elimination | rund 0,001493939807 |
| Untergrenze für den grössten absoluten Fehler jedes Schätzers aus den identischen Eingangsdaten über das Paar | mindestens 0,00074670813 |

Die Fehlergrenze ist die halbe garantierte Trennung. Sie ist eine deterministische Eigenschaft dieses Paars. Ein Beobachter mit Zugriff auf den ganzen globalen frühen Uhrabschnitt hätte in dieser speziellen eindimensionalen Familie mehr Information. Bei bekanntem Uhrprofil und bekannter Referenz bestimmt beispielsweise w₄ den Familienparameter, da v₄ von null getrennt ist. Ereignis 4 liegt ausserhalb des kausalen Vorlaufs von 16. Das archivierte Paket enthält zudem zwei anders getriebene Vergleiche mit gleichen globalen frühen Feldern, gleicher Summe und verschiedenem G₀. Diese Vergleiche testen die zusätzliche Forderung, dass ein Leser auch bei späterer Wahl anderer Senderquellen funktioniert.

## Zwei Impulse als Randvorgabe

Am nominalen Hintergrund e=1/6 verschiebt a die vier Anfangsuhren gemeinsam. b verschiebt zusätzlich Y₀. Die Anfangsgewichte, die Uhren und Gewichte am Zukunftskragen sowie die beiden übrigen relativen Anfangsuhrformen bleiben festgelegt. Die elf inneren Uhren und neun inneren positiven Gewichte relaxieren gemeinsam. Für den Zielvektor p=(ΣG*,G₀*) hat die gemischte Variationsaufgabe die Wirkung A + 2p₁a + 2p₂b. Die beiden zusätzlichen Stationaritätsgleichungen erzwingen genau die zwei gewünschten Impulse mit der angegebenen Vorzeichenkonvention.

Für H=∂²A mit innerem Block I und den beiden Randrichtungen B lautet die lokale Antwortmatrix K=−(H_BB − H_BI H_II⁻¹ H_IB)/2. Im nominalen Referenzzustand liefert sie

| Ableitung | nach a | nach b |
|---|---:|---:|
| ΣG | −0,104141805 | 3,686350145 |
| G₀ | 3,686350145 | −111,841725376 |

Die eingeschlossene Determinante liegt zwischen −1,941779 und −1,941777. Damit lassen sich beide Zielgrössen lokal unabhängig vorgeben. Für drei vorab bestimmte Zielpaare wurde die vollständige nichtlineare Aufgabe nochmals gelöst. Die Zielwerte sind relativ zum **exakten** nominalen Referenzzustand definiert. Eine Intervalleinschliessung der unbekannten Referenzimpulse wird durch die Rechnung mitgeführt. Die Zielgleichungen gelten daher auch ohne Rundung auf die gedruckten Zahlen.

| Vorgegebenes ΔΣG | Vorgegebenes ΔG₀ | Verschiebung a, gerundet | Verschiebung b, gerundet |
|---:|---:|---:|---:|
| 0 | 0 | 0 | 0 |
| 0 | −0,000001 | −1,8984443·10⁻⁶ | −5,36322·10⁻⁸ |
| 0 | +0,000001 | +1,8984363·10⁻⁶ | +5,36321·10⁻⁸ |

Für alle drei Fälle gelten strikte kausale Uhrordnung, dieselben beiden leeren Ereignisse und eindeutig dieselben zwei positiven Materialmarken. Das gilt für die archivierte Fensterkoordinate und für eine mit dem veränderten Anfangskragen neu normierte Fensterkoordinate. Keine Empfangsgrösse ging in die Zielwerte ein. Die beiden von null verschiedenen Fälle ändern die Anfangsuhren. Ihre Vergleichbarkeit als lokale Senderexperimente würde eine zusätzliche physische Präparationsregel erfordern.

## Nachweis und Reproduktion

Nach dem Entpacken genügt Python ab 3.10 mit der Standardbibliothek.

    python3 -B pruefen.py

Der Prüflauf reproduziert zuerst das eingebettete Ausgangspaket aus PR 387 samt seiner Vorstudien. Er verifiziert die Eingabedateien und den lokal vor den Rechnungen festgehaltenen Prüfplan per SHA-256. Die Referenzrechnung verwendet Festkomma-Intervalle mit nach aussen gerundeten Endpunkten. Dezimales Newton-Verfahren und Matrixinversion liefern Vorschläge. Ein unabhängig einschliessender Kontraktionstest zertifiziert für jede Referenz- und Zielbox Existenz und Eindeutigkeit. Die Regularität auf der gesamten archivierten nominalen Referenzhülle identifiziert die Referenzlösung mit dem zuvor nachgewiesenen Zweig. Genaue Koordinaten, Intervallradien, Kontraktionsschranken, Fensterlagen und Ergebnisse stehen in den drei JSON-Dateien.

Die Gegenrechnung rekonstruiert die Schichtkoeffizienten aus der Ordnung. Exakte rationale zentrale Differenzen der ursprünglichen Wirkung kontrollieren alle 22 Ableitungen und die gesamte symmetrische Hesse-Matrix an einem rationalen Testpunkt, einschliesslich der expliziten Formel für G₀. Eine zweite Intervall-Elimination am eingeschlossenen nominalen Zweig liefert die Trennung der beiden quellfreien Lösungen. Ausgeschriebene Knotengleichungen kontrollieren alle fünf Belegungen. Die exakte Stationarität folgt aus der affinen Konstruktion bzw. dem Kontraktionsbeweis. Die blosse Einschliessung von null in nachgerechneten Residuen würde dafür nicht genügen.

**Folgerung für den Staubball.** Für ein frühes Messergebnis braucht es einen vor dem Senden verfügbaren materiellen Freiheitsgrad, dessen Kopplung und Ausleseregel G₀ festlegen oder aufzeichnen. Die vorliegenden Tests zeigen, warum ein zusätzlich gesetzter Zahlenwert im vollständigen Randwertproblem diesen Schritt offenlässt. Die 60 physischen P3-Prüfpunkte bleiben auf `NOT_RUN`.

[Veröffentlichte Ausgangsstudie auf GitHub, PR 387](https://github.com/thomasmgfeller/x6-spectral-astrolabium/pull/387)
