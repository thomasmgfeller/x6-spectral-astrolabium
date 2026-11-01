# Zwei fest vereinbarte Entscheidungen für die relative Referenzkalibrierung

## 1. Experiment und Ziel

Die externen Modellzusagen von v0.5/v0.6 bleiben Voraussetzung. Die wissenschaftliche Beprobungsdichte ist proportional zu s·e·t_ext pro physischem Vierervolumen. K bezeichnet das Verhältnis zwischen wesentlichem Supremum und wesentlichem Infimum. Für Erzeugungsdichte und Transfer einschließlich Drift braucht es K(s)≤S und K(t_ext)≤D. Innerhalb jeder der 16 vollständigen Messzellen dürfen die Referenzeffizienzen höchstens um Faktor C variieren. Hier ist S=D=C=1,0001. Die relevanten Referenz- und Wissenschaftsmaße sind durch diese Schranken abgedeckt. Der Vergleich der Zellmittel nutzt markierte, innerhalb und zwischen den Zellen unabhängige Referenzversuche mit vollständiger Erfassung auch der Ausfälle. Pro Zelle ist die marginale Trefferwahrscheinlichkeit p_j bei allen potentiellen Versuchen gleich. Die Wissenschaftsordnung und ihre Zufallsgruppierung sind unabhängig von der Kalibrierung.

Ziel ist K(f)≤K*=1,002. Mit L=K*/(SDC²) folgt aus K(f)≤SDC² p_max/p_min, dass bei K(f)>K* ein festes gerichtetes Paar (i,j) mit p_i−L p_j>0 existiert. Die günstige Klasse ist durch m=min_j p_j≥0,49 und p_max/m≤r=1,0002 definiert. Sie setzt vorliegende und gültige externe Nachweise voraus. Aussagen über Fehlfreigabe gelten einheitlich über alle unsicheren Profile im Modell. Aussagen zur Verfügbarkeit gelten nur in der günstigen Klasse.

## 2. Eingefrorener Entscheidungsplan

Schreibe W_n=max_j x_j−L min_j x_j für die empirischen Trefferquoten der 16 Zellen nach n Versuchen je Zelle. In Stufe 1 werden je Zelle n₁=33.000.000 Versuche genommen. Für t₁=0,000333 und h₁=0,000050 gilt

| Bedingung | Entscheidung |
|---|---|
| W₁ ≤ −t₁ | GO, Kalibrierung beenden |
| W₁ ≥ −h₁ | HOLD, Kalibrierung beenden |
| −t₁ < W₁ < −h₁ | Weitere 13.000.000 Versuche je Zelle |

Nur bei Fortsetzung wird W₂ aus den kumulierten n₂=46.000.000 Versuchen je Zelle verglichen. Bei W₂≤−t₂ mit t₂=0,000267 lautet das Ergebnis GO, sonst HOLD. Eingaben der zweiten Stufe sind ausschließlich **zusätzliche** Treffer und Versuche. Die Software bildet die Summe selbst. Am Zwischenstand CONTINUE gibt sie keine Geometrie aus. Bei HOLD gibt sie den ganzen Modellbereich zurück. Für GO darf die separate v0.4-Geometrieauswertung verwendet werden. Nach einem terminalen Zwischenentscheid darf keine zweite Messung in diese Regel eingehen.

Mathematisch kann für jede Zelle vor der ersten Entscheidung eine Folge von n₂ unabhängigen Bernoulli-Beobachtungen konstruiert werden. Nicht erhobene Folgebeobachtungen dienen nur als potentielle Daten für den Beweis und für gepaarte Simulationen. Die beiden aufeinanderfolgenden kumulierten Tests sind abhängig.

## 3. Fehlerbudget und schärfere Schranke für 16 Zellen

U(n,u) ist die in v0.6 zertifizierte obere Wahrscheinlichkeit einer beliebigen einseitigen Abweichung von mindestens u für ein gewichtetes zentriertes Paar der n-Zellmittel. Die Schranke gilt für jede Wahl der beiden Zellwahrscheinlichkeiten und für beide Abweichungsrichtungen. Die unveränderte Implementierung ist previous/budgets.py, die vollständige Herleitung steht in previous/BEWEIS.md. Sie benutzt exponentielle Gewichtung, die allgemeine Berry–Esseen-Ungleichung und 100 Teilintervalle für die unbekannte Varianz. Die Randwerte von U werden rational nach außen gerundet.

Im unsicheren Modell muss das feste ungünstige Paar bei jedem GO die jeweilige Schwelle passieren. Für eine Fehlfreigabe in Stufe 2 genügt die Obergrenze für den **potentiellen** Abschlussvergleich. Aus der Vereinigung der beiden Fehlermöglichkeiten folgt

    P(falsches GO) ≤ U(n₁,t₁) + U(n₂,t₂)
                   ≤ 0,003864429384 + 0,005961782889 = 0,009826212273.

Für die günstige Klasse verbessert sich der Faktor vor den Paarschwänzen. Teile die wahren Zellmittel bei m(1+r)/2 in eine untere und eine obere Hälfte mit k Zellen in der oberen Hälfte. Die Teilung wird nur im Beweis vorgenommen. Schreibe P=0,49, g=P(L−1) und w=P(r−1).

- Zwischen einem hohen i und einem niedrigen j ist L p_j−p_i ≥ m(L−r) ≥ g−w.
- Innerhalb derselben Hälfte ist p_i−p_j ≤ m(r−1)/2. Daher ist L p_j−p_i ≥ m[L−1−(r−1)/2] ≥ g−w/2.
- Zwischen einem niedrigen i und einem hohen j ist p_i≤p_j und L p_j−p_i ≥ g.

Damit sind für jede Schwelle t mit positiven Abständen die Ereignisse W_n≥−t durch

    A(n,t) = min{1, max über k=0,…,16 von
        k(16−k) [U(n,g−w−t)+U(n,g−t)]
        + [240−2k(16−k)] U(n,g−w/2−t)}

nach oben begrenzt. Denn es gibt k(16−k) Paare je Kreuzrichtung und 240−2k(16−k) innerhalb der Hälften. Ein Maximum von W_n wird selbst bei Gleichständen durch ein Paar mit i≠j erreicht. Man setzt die Schranke für die jeweilige Mindestabweichung ein und vereinigt die Ereignisse. Weder eine Unabhängigkeit der 240 Paarabfragen noch eine Festlegung darauf, welche Zellen hoch sind, wird benötigt.

Ein endgültiges HOLD ist im günstigen Modell im frühen HOLD oder im potentiellen finalen HOLD enthalten. Eine verpasste frühe Freigabe ist durch A(n₁,t₁) beschränkt. Daraus folgen

    P(HOLD) ≤ A(n₁,h₁)+A(n₂,t₂)
            ≤ 0,000010025040 + 0,002521651872 = 0,002531676912,
    P(frühes GO) ≥ 1−A(n₁,t₁) ≥ 0,773201871920,
    P(GO insgesamt) ≥ 0,997468323088.

Die gemeinsame obere Fehlfreigabe und die obere günstige HOLD-Rate unterschreiten auch die publizierten v0.6-Schranken 0,009880972695 bzw. 0,002620553280. Nur der neue Abschlussvergleich bei starr eingehaltenen 46 Millionen je Zelle hätte eigene Schranken von 0,005961782889 bzw. 0,002521651872. Dieser Kontrollplan dient dazu, die Wirkung des frühen Stoppens von der verbesserten Paarschätzung zu trennen. Keiner der Pläne darf nach Sichtung der Versuchsdaten gewählt werden.

## 4. Erwarteter Messaufwand und Geometrie

Ohne fehlende externe Zusagen kostet die vorgesehene Kalibrierung 528 Millionen oder 736 Millionen Versuche. Bezeichne mit B die tatsächlich erhobene Gesamtzahl. Für jedes feste Profil gilt exakt

    E[B] = 16 n₁ + 16(n₂−n₁) P(CONTINUE).

Weil CONTINUE eine verpasste frühe Freigabe voraussetzt, ist E[B] in der gesamten günstigen Klasse höchstens **575.174.011** (nach oben gerundet). Das sind mindestens 23,51 % mittlere Einsparung gegenüber den 752 Millionen von v0.6. Allein gegenüber dem festen Vergleich mit n₂ sind es mindestens 21,85 %. Aus dem Klassenmittelwert folgt keine obere Schranke dieser Größe für einen einzelnen Durchlauf oder ein beliebiges Profil außerhalb der Klasse.

Bei mindestens einem Paar mit p_i−L p_j≥0,0002 erhält man P(kein frühes HOLD)≤U(n₁,0,0002+h₁). Somit erfolgt früh HOLD mit mindestens 0,974677055648 Wahrscheinlichkeit und E[B]≤533.267.173. Dies ist ein Kriterium für getrennte Zellmittel. Aus K(f)>K* allein folgt dieser zusätzliche Abstand nicht.

Die Geometrie bleibt der vollständige 4D-Kausaldiamant mit h∈[0,1/2], drei Rasterwerten 0, 1/4, 1/2 und q=RT²=48 atanh(h/2)². Nach GO verwendet man unabhängig 3,2 Millionen wissenschaftliche Ereignisse und die fixierte v0.4-Zählregel mit disjunkten Achtergruppen. Bei HOLD wird das volle h- und q-Intervall zurückgegeben. Für K(f)≤K* kann nur eine ursprüngliche v0.4-Fehlüberdeckung zur Fehlüberdeckung führen. Für K(f)>K* kann nur eine Fehlfreigabe dazu führen. Damit bleibt die unbedingte Überdeckung aller vollständigen Durchläufe einschließlich HOLD bei mindestens 0,951569406. An jedem wahren Rasterpunkt in der günstigen Klasse folgt wegen der Unabhängigkeit P(korrekte Einzelausgabe) ≥ 0,997468323088 · 0,803252245 ≥ 0,801218669836. Diese Garantie ist nicht bedingt auf die Teilmenge der beobachteten GO-Fälle.

## 5. Eigene Untergrenze für Regeln mit frühem Stopp

Die feste Untergrenze von 420.800.008 aus v0.6 bezieht sich auf vorab festgelegte Zellbudgets. Für den erwarteten Verbrauch einer Regel mit Stopp untersuchen wir eine eigene, auch für adaptive Zellwahl gültige Schranke. Sie gilt hier für im Voraus begrenzt viele mögliche Versuche, eine Vorhersagbarkeit der Zellauswahl aus der bisherigen Beobachtung, dieselben unabhängigen Referenzverteilungen innerhalb jeder gewählten Zelle und dieselbe externe Information. Beliebige Vorab- oder Zwischenrandomisierung darf in beiden Anlagen gleich verwendet werden.

Betrachte ein einziges günstiges Profil G mit acht Zellen der konstanten Effizienz a=r/(1+r) und acht der Effizienz 1−a. Ordne die 16 Zellen acht disjunkten Hoch-Niedrig-Paaren zu. Für jedes Paar erzeuge eine eigene ungünstige Alternative. Nur in diesem Paar werden die Basiswerte b, 1−b mit b>L/(1+L) eingesetzt. In einem Gebiet positiver Masse η der hohen Zelle wird dessen Effizienz Cb, ebenso in der niedrigen Zelle (1−b)/C. Wähle s=S und den Transfer D in allen acht hohen Zellen und beide Faktoren eins in den niedrigen Zellen, identisch in allen Anlagen. Die beiden geänderten Zellen bezeugen K(f)≥SDC² b/(1−b)>K*. Alle übrigen Beobachtungen und alle extern verfügbaren Zusagen sind gleich. Die Güteziele gelten also für G und alle acht Alternativen.

Bei höchstens M Versuchen ist die Wahrscheinlichkeit, eines der sehr kleinen Gebiete zu treffen, selbst unter adaptiver Zellauswahl höchstens Mη, wenn die bedingte Positionsziehung innerhalb der gewählten Zelle fest bleibt. Im Grenzübergang η→0, b↓b*=L/(1+L) geht die GO-Wahrscheinlichkeit für jede dieser Alternativen in die des zugehörigen Grenzgesetzes über. Dadurch gilt auch dort die Schranke ≤δ=0,01. Für diesen Schluss genügt, dass die physischen Kontraste der approximierenden Anlagen strikt über K* liegen. Das günstige Gesetz erfordert GO mit Wahrscheinlichkeit ≥g₀=0,997.

Schreibe d(x||y)=x log(x/y)+(1−x)log[(1−x)/(1−y)]. In der schrittweisen Faktorisierung des gestoppten Beobachtungspfades kürzen sich die gemeinsamen Regeln für Zellauswahl und Stopp. Man kann nach dem Stopp bis M mit einem gemeinsamen deterministischen Symbol auffüllen. Unter G hat jeder tatsächlich in einem der beiden geänderten Zellen erhobene Versuch die erwartete Log-Likelihood-Ratio d(a||b*), in der niedrigen Zelle wegen Komplementarität denselben Wert. Alle anderen Versuche tragen null bei. Durch Verdichtung des Pfades auf GO/HOLD kann die relative Entropie nur sinken (Log-Summen-Ungleichung). Da d(g||b) für g>b mit g wächst und mit b fällt, folgt für dieses Paar

    E_G[N_i+N_j] · d(a||b*) ≥ d(g₀||δ).

Die Erwartung ist für alle acht Paare unter **demselben** G. Addieren ergibt E_G[B] ≥ 8 d(0,997||0,01)/d(a||b*) > **149.674.146** Versuche. Dies belegt die Notwendigkeit für mindestens ein günstiges Profil bei jedem solchen Verfahren. Die Zahl ist keine Mindestzahl in jedem einzelnen Lauf und kein Beweis für die Optimalität des vorliegenden Plans. Die Informationsschranke folgt auch aus dem allgemeinen Wechselmaß-Lemma für adaptive Experimente. [Kaufmann, Cappé und Garivier, JMLR 17 (2016), Lemma 1](https://www.jmlr.org/papers/volume17/kaufman16a/kaufman16a.pdf).

Der Code schließt die Logarithmen nach Reduktion auf [1,2] durch die Reihe für 2 atanh((x−1)/(x+1)) mit 30 Gliedern und geometrischer Restschranke ein. Die Zahl wird vor der Ausgabe nach unten abgerundet. Eine getrennte 70-stellige Dezimalrechnung liefert 149.674.146,006913… .

## 6. Modellgrenze und Quellen

Die Protokollprüfung kann Datentypen, Zellkennungen, Stufengrößen, die vorherige Zwischenentscheidung und die angegebenen externen Nachweisverweise prüfen. Dass die Zwischenzählungen unverändert festgehalten wurden und die physischen Zusagen stimmen, ist extern zu sichern. Im Paket sind ausschließlich synthetische Beobachtungen. Für den realen Aufbau gilt weiterhin HOLD.

- Modell, Geometrie und ursprüngliche externe Kalibrierung. [v0.4](https://github.com/thomasmgfeller/x6-spectral-astrolabium/pull/167) · [v0.5](https://github.com/thomasmgfeller/x6-spectral-astrolabium/pull/168).
- Gerichtete Paarschwänze, feste Untergrenze sowie vollständige Herkunft der Referenz. [v0.6, PR 169](https://github.com/thomasmgfeller/x6-spectral-astrolabium/pull/169).
- Konstante für den unabhängigen, nicht identisch verteilten Fall, verwendet im übernommenen v0.6-Zertifikat. [Shevtsova, Informatics and Applications 7 (2013)](https://www.mathnet.ru/eng/ia252).
