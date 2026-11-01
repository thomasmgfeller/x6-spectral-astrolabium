# Eigenzeit v0.11 · Nachweis der 20-ppm-Bedingung mit gepaarten Referenzversuchen

## 1. Ziel und Geltungsbereich

Die Eingangsbedingung von v0.10 lautet |q(j,h,H) − a_h p_j| ≤ 20·10⁻⁶. Hier sind p_j die wissenschaftlich verankerten Zielmittel von 16 Zellen, q die bedingte Nachweiswahrscheinlichkeit der markierten Gelegenheit h bei bisheriger Geschichte H und a_h die gemeinsame Verstärkung. Für den 4D-Kausaldiamanten gelten weiterhin alle Voraussetzungen der Vorstudie, darunter die äußeren Kontrastgrenzen, vollständige Versuchserfassung, unabhängige Geometriedaten und die im Voraus zugeordnete, exogene Faktorfolge in [0,99; 1,01]. v0.11 prüft einen Eingang dieser Kette. HOLD liefert den vollständigen Modellbereich.

Eine Regimevariable z ∈ [0,1] muss vor dem Versuch physikalisch definiert sein. Die kleinste Entfernung zu den festen Stützstellen c=1/4 und c=3/4 beträgt höchstens 1/4 (gemeint ist das Minimum der beiden Entfernungen pro z). Die gemeinsame Verstärkung hat die Form a_h=a(z_h) für den für alle Zellen gleich zugeordneten, extern fixierten oder von den v0.10-Zufällen unabhängigen Zustandsverlauf. Für die Gerätekonfiguration und denselben Zielzeitraum gelten folgende extern belegte Zusagen, in absoluten Wahrscheinlichkeits-ppm bzw. Faktor-ppm.

| Größe | Annahme über den gesamten zugelassenen Betrieb |
|---|---|
| Gepaarter Standard Y | An jeder Stützstelle gilt für seinen Mittelwert y_jc die Grenze zwischen y_jc und a(c)p_j von höchstens 2 ppm. |
| Prüfling X | Im Referenzversuch ist E[X]=f_j(c). Im Betrieb ist der Abstand zwischen q(j,h,H) und f_j(z_h) für jede zugelassene Vorgeschichte höchstens 1 ppm. |
| Zustandsabhängigkeit | f_j ist mit 8 ppm je z-Einheit Lipschitz-stetig, a mit 4 ppm je z-Einheit. Die Verstärkung liegt in [0,99; 1,01]. |
| Stichproben | Pro Zelle und Stützstelle n unabhängige, gleich verteilte markierte Paare (X,Y) mit demselben Ereignisbezug. Die beiden Antworten innerhalb eines Paares dürfen stark zusammenhängen. |
| Trennung | Bedingungen und wahres System sind für die Analyse fixiert bzw. entsprechend konditioniert. Der Audit ist einmalig vorab festgelegt. Nachmessung v0.10 und Geometrieauswertung verwenden frische, getrennte Daten. |

Die Ankerkalibrierung muss im Fehlernachweis unabhängig vom Prüfling sein. Zwei Kanäle dürfen dieselbe physische Gelegenheit teilen. Weder die Nähe ihrer Zähler noch ein Eintrag im Feldformular beweist die externe Verankerung. Verändert das Ankoppeln des Standards die Prüflingsantwort, muss die ausgewiesene Übertragungsgrenze dies abdecken. Auch ein ungemessener Betriebsparameter kann das Ein-Zustands-Modell ungültig machen.

## 2. Vom Paar zur bedingten Betriebswahrscheinlichkeit

Schreibe m_jc=P(X≠Y). Da |E[X]−E[Y]|≤E|X−Y|=m_jc, folgt für die nächste Stützstelle c und jede zulässige Vorgeschichte

    |q(j,h,H)−a(z_h)p_j|
        ≤ |q−f_j(z_h)| + |f_j(z_h)−f_j(c)| + |E[X]−E[Y]|
          + |y_jc−a(c)p_j| + |a(c)−a(z_h)| p_j
        ≤ [1+(8+4)/4+2] ppm + m_jc = 6 ppm + m_jc.

Dabei genügt p_j≤1. Sind alle 32 Diskordanzwahrscheinlichkeiten höchstens 14 ppm, gilt die geforderte 20-ppm-Schranke über den gesamten zugelassenen Betrieb. Bei einer tatsächlichen Verletzung muss mindestens ein festes m_jc größer als 14 ppm sein. Umgekehrt können viele gegenläufige Diskordanzen trotz korrekter Zellmittel eine Zählfreigabe verhindern.

## 3. Einseitige Zählregel und Kosten

An jedem der 32 Messpunkte werden fest 3.300.000 Paare angesetzt. D=N01+N10 zählt die ungleichen Antworten. Die Zählbedingung ist erfüllt, wenn überall D≤25 gilt. Bei festem m hat D die Verteilung Bin(n,m). Der linke Schwanz fällt mit m, wie man unmittelbar durch dieselben unabhängigen Gleichverteilten für die Bernoulli-Ziehungen sieht.

Ist im Betrieb die 20-ppm-Grenze verletzt, wähle einen der obigen Messpunkte mit m>14 ppm. Die globale Annahme setzt voraus, dass auch sein Zähler ≤25 ist. Die globale Fehlannahmewahrscheinlichkeit ist daher höchstens P[Bin(3.300.000,14·10⁻⁶)≤25] ≤ 0,000477764228. Dafür genügt die Einzelverteilung an diesem Messpunkt. Die simultane GO-Regel ist ein Schnitt lokaler Annahmeereignisse. In der günstigen Auditklasse m≤3 ppm an **allen** Messpunkten gilt umgekehrt mit der Vereinigungsabschätzung P(HOLD) ≤ 32 P[Bin(3.300.000,3·10⁻⁶)>25] ≤ 0,000478810524. Für beide Schranken ist keine Unabhängigkeit zwischen den 32 Zählern nötig. Der 3-ppm-Wert bezeichnet eine günstige Leistungsklasse für den Vergleichsaufbau, keine im Voraus zu bescheinigende Geräteeigenschaft für die Gültigkeit der Fehlannahmeschranke. [Berger und Hsu, Statistical Science 11 (1996), Schnitt-Vereinigungs-Tests](https://www.public.asu.edu/~rlberge1/papers/statsci96.pdf)

Die Grenzen wurden ganzzahlig nach außen gerundet. certificate.py schließt zuerst (1−p)ⁿ mit Intervallpotenzierung ein. Für die folgenden Massen wird mit (n−k)p/[(k+1)(1−p)] multipliziert. Positive Terme erlauben gerichtete Rundung bei jeder Operation. verify.py vergleicht 570 kleine Fälle mit exakten rationalen Binomialsummen und die Hauptwerte mit SciPy. Der Plan ist hinreichend. Eine Optimierung über alle möglichen Vergleichsverfahren wurde nicht vorgenommen.

Ein positiver Lauf kostet 105.600.000 markierte Paargelegenheiten mit zwei binären Ausgängen. Die 26. Diskordanz an einem Messpunkt bewirkt einen unwiderruflichen negativen Abbruch desselben Audits, weil spätere Zähler nur wachsen. Eine Fortführung mit neuen Zählern oder ein Neustart unter derselben Fehlerzuteilung wäre ein anderes Verfahren. Bei seriellem Beginn an einem problematischen Punkt hat der dortige Aufwand Erwartungswert E[min(T₂₆,n)]≤min(26/m,n) für m>0 (negative Binomialwartezeit). Für m=0,5 ergibt das höchstens 52 Paare an diesem Punkt. Frühere Messpunkte und parallel aufgenommene Paare kommen ggf. hinzu.

## 4. Zusammensetzen mit v0.10

Unter belastbaren externen Modellzusagen kann eine falsche physische Freigabe entweder nach einer irrtümlichen Auditannahme oder trotz gültiger 20-ppm-Bedingung im nachgelagerten v0.10-Test auftreten. Konservativ addiert ergeben sich höchstens 0,000477764228+0,009360038055=0,009837802283. In der gemeinsamen günstigen Klasse (v0.10-Zielprofil und alle m≤3 ppm) beträgt die HOLD-Wahrscheinlichkeit höchstens 0,000478810524+0,002175449152=0,002654259676. Für real bereits überprüfte externe Voraussetzungen beziehen sich die Summen allein auf die statistischen Entscheidungen; Ausfall der externen Garantien ist darin nicht eingerechnet. Falls deren gemeinsame Fehlzertifizierungswahrscheinlichkeit τ anderweitig gesichert ist, liefert die einfache Addition weiterhin höchstens 1 % falsches physisches GO, sofern τ≤0,000162197717.

HOLD behält alle Geometrien bei. Die unbedingte Überdeckung beträgt konservativ mindestens 0,951569406−0,000477764228=0,951091641772. In der gemeinsamen günstigen Klasse an einem wahren Rasterpunkt beträgt die richtige Einzelausgabe mindestens 0,801504810584−0,000478810524=0,801026000060. Gedanklich darf ein frischer vollständiger v0.10-Lauf auch bei negativem Audit vorliegen. Das Ersetzen seines Ergebnisses durch den ganzen Bereich bei HOLD kann die Überdeckung nur erhöhen. Bei ungültiger Driftbedingung ist ein Deckungsfehler nur nach fälschlich bestandenem Audit möglich. Das rechtfertigt auch die angegebene konservative Grenze. Budgets für Verfügbarkeit erfordern zusätzlich, dass externe Nachweise vorliegen und die Schutzüberwachung den vorgesehenen Betrieb zulässt. Der Höchstaufwand beider Kalibrierschritte zusammen beträgt 1.081.600.000 markierte Gelegenheiten; externe Metrologie und Wissenschaftsereignisse kommen hinzu. [Vollständiger Nachweis v0.10](https://github.com/thomasmgfeller/x6-spectral-astrolabium/pull/173)

## 5. Grenzen ohne zusätzliche Beobachtungen

**Verdeckter Einzelversuch.** Sei p=1/2, a=1. In Welt A haben die vier geordneten Binärergebnisse eines Zweierblocks die Wahrscheinlichkeiten (1/4,1/4,1/4,1/4), in Welt B (1/4,1/4+d,1/4−d,1/4) für d=30 ppm in der Reihenfolge 00,01,10,11. In B liegt die erste bedingte Trefferwahrscheinlichkeit bei 1/2−d. Dennoch ist das Gesetz der Blocksumme in beiden Welten (1/4,1/2,1/4). Bei unabhängiger Wiederholung der Blöcke gilt die Identität für beliebig viele solche Blockzählungen. Einzelzeitstempel enthalten hier zusätzliche Information. Selbst vollständig geordnete historische Paare können ohne Übertragungsannahmen einen zukünftigen erstmaligen Sprung um 30 ppm nicht ausschließen, da bis zu diesem Sprung beide Welten exakt dieselbe Historie erzeugen können.

**Gemeinsamer Versatz.** Für X=Y bei jeder Gelegenheit und E[X]=1/2+50 ppm, p=1/2, a=1 ergibt sich D=0 mit Wahrscheinlichkeit eins. Die Referenz selbst verletzt die 2-ppm-Forderung. Ein unabhängiger Zielanker ist unverzichtbar. Umgekehrt ergeben gleich große Fehler in beiden Richtungen bei m=30 ppm einen perfekt unverzerrten Mittelwert, aber praktisch immer HOLD im vorliegenden Test. Für zwei bedingt unabhängige Kanäle mit je 50 % Effizienz gilt m=0,5. Bei exakt halben Randmitteln erfordert m≤3 ppm eine Korrelation von mindestens 0,999994, denn m=(1−ρ)/2.

**Aufwand bei getrennten Zählern.** Als ideales Vergleichsexperiment seien alle p_j=1/2 und a=1 exakt bekannt. Pro gewählter Zelle gibt es nur einen unabhängigen Bernoulli-Ausgang. Unter dem guten Basiszustand gilt q_j=1/2. Für die Alternative j steigt nur q_j stationär auf 1/2+δ, mit δ>20 ppm. Eine beliebige, fast sicher endende Regel soll am Basiszustand mit mindestens 0,9995 annehmen und unter jeder Alternative mit höchstens 0,0005. Die Informationsverarbeitung des Log-Likelihood-Verhältnisses des gesamten Protokolls ergibt

    E₀[N_j] · kl(1/2,1/2+δ) ≥ kl(0,9995; 0,0005).

Das gilt auch bei adaptiver Zellwahl und Abbruch. Der Zähler bezeichnet alle Einzelausgänge der jeweiligen Zelle, über beliebige Stützstellen verteilt. Für δ↓20 ppm ist der Nenner −(1/2)log(1−4δ²), der Zähler 0,999 log(1999). Summation über 16 mögliche fehlerhafte Zellen liefert am Basiszustand mehr als 151.847.999.757 Einzelausgänge im Erwartungswert; certificate.py zertifiziert die Abrundung mittels log(1999)>7,6 und −log(1−x)≤x/(1−x). Dies ist eine Untergrenze in diesem eigenen Beobachtungsmodell bei den festgelegten Fehlerzielen. Der Paarplan erhält pro Gelegenheit eine zusätzliche, eng korrelierte Antwort eines separat verankerten Standards. Die Zahlen begründen keine universelle Kostenersparnis und enthalten keine Baukosten des Standards. [Kaufmann, Cappé und Garivier, JMLR 17 (2016), Lemma 1](https://jmlr.csail.mit.edu/papers/volume17/kaufman16a/kaufman16a.pdf)

## 6. Unabhängige Kontrollen

Die im lokalen Freeze festgelegten fünf Profile wurden je 40.000-mal mit separaten Zufallsströmen erzeugt. Simuliert wurden die hinreichenden Binomialzählungen, keine einzelnen physikalischen Trigger. Unter all_3ppm nahmen 39.979 der 40.000 Kampagnen die Zählhürde. Bei genau einem Messpunkt mit 14 ppm waren es 13. Die Einpunktprofile prüfen die Schwellenverteilung und setzen keine bestimmte Vorzeichenstruktur voraus. Bei allseitigen symmetrischen 30 ppm nahmen 0 Kampagnen die Hürde. Beim gemeinsamen 50-ppm-Zielversatz ergaben alle 40.000 digitale Zählannahme; die Ankerkontrolle muss die Weitergabe sperren. Der standardmäßig leere Feldbogen ergibt HOLD_EVIDENCE.

Das Zusatzprogramm controls.py prüft die Abbruchlogik und berechnet die extrem kleinen Wahrscheinlichkeiten getrennt mit 80 Dezimalstellen Rechengenauigkeit. Die in der eingefrorenen SciPy-Auswertung für den symmetrischen 30-ppm-Fall angezeigte 0 ist ein Gleitkomma-Unterlauf. Der Modellwert beträgt ungefähr 3,426·10⁻⁵⁸². Ein zusätzliches zulässiges Gerätemodell mit echtem Zielverstoß hat an beiden Ankern derselben Zelle f_j=0,500021, y_j=0,5 und ausschließlich positive Diskordanzen von 21 ppm. Alle übrigen Zellen haben bei exakt halben Mittelwerten symmetrische Diskordanz von 3 ppm. Unabhängige Messpunkte ergeben eine Audit-Annahmewahrscheinlichkeit von rund 6,92·10⁻¹⁹. Das Zusatzprogramm verwendet keine weiteren Zufallsdaten.
