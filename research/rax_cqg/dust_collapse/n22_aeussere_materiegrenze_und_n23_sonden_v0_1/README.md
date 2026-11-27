# N22 · Äussere Materiegrenze und freie Sonde am frühen Schnitt

Auf dem in [PR 412](https://github.com/thomasmgfeller/x6-spectral-astrolabium/pull/412) publizierten Vergleichspaar bestimmen die abgetasteten Ereignisse den äusseren Kugelradius in der unten definierten flachen Kontrollklasse nicht eindeutig. Zwei kugelsymmetrische, kontrahierende Materieverteilungen mit gleicher Grenzgeschwindigkeit ordnen über die ganze Messzeit sämtliche 19 positiven und drei leeren Ereignisse gleich ein. Sie besitzen am Zielschnitt Radien 1 und 2. Sämtliche Ereigniskoordinaten, Uhren und Feldgewichte können zwischen diesen Alternativen identisch bleiben. Die unterschiedlichen Zentren und die radialen Dichteprofile sind unbeobachtete Grössen.

Im diskreten Modell unterscheiden drei vorgeschlagene Messbahnen die beiden Kontrollränder. Ihre freien Sonden verletzen jedoch notwendige Feldgleichungen. Auch der allgemeine Versuch, bei festgehaltenen N22-Feldern ein leeres Ereignis mit mindestens einem Nachfolger ins frühe Fenster einzufügen, scheitert. Die Aussagen beziehen sich auf die jeweilige endliche Datenauswahl, Kontrollklasse und Wirkungsregel.

## Eingabe und Geltungsbereich

Die [Eingabedatei am Merge-Commit](https://github.com/thomasmgfeller/x6-spectral-astrolabium/blob/2868e40a0a25769c955058f8523189eb7ed1e772/research/rax_cqg/dust_collapse/n22_anfangsladung_zwei_massen_transfer_v0_1/Vergleichspaar.json) ist mit SHA-256 c75c0c97c1b536d0140d77b4f01d8bfa0a2aab487a1b05a2b58f2ebf23159c2f beigefügt. Sie umfasst die Ordnung 216141/229383/0/+, alle 152 strikten Kausalrelationen und die beiden zertifizierten kontinuierlichen Feldboxen. Das Fenster ist [15/32,17/32], der Zielschnitt x=1/2. Darin liegen positive Ereignisse 18,19 und leere Ereignisse 17,20. Die gemischten verankerten Paare sind (19,17) und (19,20). Alle 231 ungeordneten Ereignispaare werden je Präparation geprüft. Die ursprüngliche Massennormierung ist eine Modelleichung.

## Zwei räumliche Kugelränder mit identischen Messdaten

In einer flachen Raumzeit mit Signatur (−,+,+,+), c=1 und gemeinsamer Längeneinheit bekommt jedes Ereignis seine normierte Uhr als Koordinatenzeit t=x und die drei rationalen Raumkoordinaten aus Ortskoordinaten.json. Es gibt nur eine solche Ortstabelle für beide Präparationen und beide Kugeln. Für jede zulässige Zeit in den veröffentlichten Boxen ist jedes geordnete Paar zeitartig orientiert, jedes unvergleichbare Paar raumartig. Eine treue Sprinklingverteilung oder eine metrische Lösung der gekoppelten diskreten Theorie wird hier nicht vorausgesetzt oder nachgewiesen.

| Rand | Zentrum (X,Y,Z) | Radius im Zeitverlauf | Radius bei t=1/2 | Eigenfläche bei t=1/2 |
|---|---|---|---:|---:|
| Kleine Kugel | (0,0,−1) | 1−(t−1/2)/8 | 1 | 4π |
| Grosse Kugel | (0,0,−5/2) | 2−(t−1/2)/8 | 2 | 16π |

Für jeden positiven Punkt gilt streng |p−c|²<R(t)² und für jeden leeren streng |p−c|²>R(t)². Diese Ungleichungen gelten auch für die Uhrboxen. Beide Grenzen sind während der gesamten Beobachtung glatt, zeitartig und radial mit Geschwindigkeit 1/8 einwärts bewegt. Eine gemeinsame Schätzung r aus diesen Daten hat auf dem Kontrollpaar einen maximalen relativen Radiusfehler von mindestens 1/3. Der beste Kompromiss ist r=4/3. Für die Fläche beträgt die entsprechende Untergrenze 3/5. Diese Schranken betreffen die beiden zulässigen Kontrollen je Präparation. Es entsteht kein physischer Radiuswert, keine Fehlerschranke für einen vollständig spezifizierten CST-Operator und keine Lösung des selbstgravitierenden Staubkollapses. Die Wahl t=x ist eine Beobachtungsannahme in der Kontrollraumzeit. Eine gemeinsame Synchronisation auf den bewegten Staubweltlinien wird damit nicht hergeleitet.

### Auch Feldwerte und eine erhaltene Tracerladung sind verträglich

Setze u=(p−c)/R(t), s=|u|². Eine radialsymmetrische Tracerdichte im verwendeten Inertialsystem ist J⁰=R⁻³ f(s), die räumliche Stromdichte ist J=J⁰ R′u. Bei festem u bewegt sich jedes Teilchen geradlinig. Das Raumvolumen erhält den Faktor R³. Die Kontinuitätsgleichung folgt durch Ableiten bei festem u, und |R′u|<1 im Träger. Das Profil sei für s<1 positiv und für s≥1 null. Die 19 positiven Ereignisse haben je Kugel und Präparation nachweislich paarweise getrennte s-Intervalle. Für jede Realisierung der Feldwerte in den Boxen kann man daher ein glattes f mit f(sᵢ)=R(tᵢ)³wᵢ wählen. Konkret multipliziert man b(s)=exp(−1/(1−s)) für s<1 mit exp(P(s)), wobei das Interpolationspolynom P an allen sᵢ die Werte log(R(tᵢ)³wᵢ/b(sᵢ)) annimmt. Ausserhalb setzt man f=0. Dieses Argument betrifft die Existenz glatter Profile für abgetastete Dichten.

Sogar die Gesamttracerladung kann für die beiden Alternativen auf denselben beliebigen positiven Wert gesetzt werden. Die zusätzliche Multiplikation mit exp(λh(s)), h(s)=∏ᵢ(s−sᵢ)², bewahrt alle Stichproben. Das Ladungsintegral über den Einheitsball ist streng monoton und stetig in λ. Für λ→−∞ geht es durch dominierte Konvergenz gegen null, für λ→+∞ wächst es auf jeder inneren Teilregion mit h und f von null getrennt unbegrenzt. Der frei gewählte Profilverlauf und die Gleichsetzung von w mit einer beobachteten Tracerdichte gehören zu dieser Existenzkontrolle. Eine Masseneichung oder eine Ableitung des Profils aus der CST-Wirkung wurde damit nicht durchgeführt.

## Ordnungsschatten und Kontaktfläche

Unter 336 nichtleeren Antiketten sind 37 inklusionsmaximal. Genau sechs maximale Antiketten enthalten 19 und 17. Alle sechs enthalten auch 20. Für jeden beliebigen Schnitt A (jede nichtleere Antikette) werden die strikten Vergangenheits- und Zukunftsschatten einzelner Anker auf A und alle endlichen Durchschnitte dieser Schatten gebildet. Jede Teilfamilie nichttrivialer echter Schatten spannt jeweils die vollen Simplizes auf ihren Ecken auf. Alle Schnittpunkte als einzelne Ecken dürfen immer hinzugenommen werden. Ein Schatten, der ganz A enthält, liefert sofort einen vollen Simplex mit H₂=0. Für **1373** Familien ohne ganzen Schatten ist der zweite Betti-Wert über F₂ ebenfalls null. Berechnet wird β₂=Anzahl der Dreiecke−Rang(∂₂)−Rang(∂₃). Tetraederoberfläche, gefülltes Tetraeder und zwei getrennte Oberflächen dienen als Gegenkontrollen mit β₂=1,0,2. Das Ergebnis gilt für genau diese Rekonstruktion. Es schliesst andere Randoperatoren und gezielt ausgewählte Teilflächen nicht aus.

Selbst die affine Fläche der drei Kontaktpunkte 17,19,20 in der geometrischen Kontrolle hängt von einer unbeobachteten Lage ab. Fixiere 21 der 22 Raumorte und verschiebe nur 20 auf eine kleine Kugel um 17. Sein relativer Ortsvektor ist zunächst (p₁₉−p₁₇)/10000. Anschliessend werden seine drei Komponenten zyklisch vertauscht. Die Länge und das invariante Intervall 17–20 stimmen in beiden Konfigurationen überein. Während der gesamten Drehung bleiben Kausalordnung und Materieseiten gleich. Für a=p₁₉−p₁₇ und q=p₂₀−p₁₇ ergibt sich die Gramdeterminante |a×q|²−|(t₁₉−t₁₇)q−(t₂₀−t₁₇)a|². Ihre eingeschlossenen Werte sind an einem Ende strikt negativ und am anderen strikt positiv, für beide Präparationen. Trotz dreier paarweise raumartiger Ereignisse kann ihre aufgespannte Ebene zeitartig oder raumartig sein. Auf der raumartigen Seite können die Flächen entlang der Drehung beliebig nahe an null liegen.

## Welche Messung unterscheidet die Ränder?

In der flachen Kontrolle lassen sich geodätische Testbeobachter durch je zwei zeitartig geordnete Ereignisse festlegen. An x=1/2 treffen alle 75 Interpolationen zwischen vorhandenen Endpunkten je Präparation dieselbe Materieseite in beiden Kugeln. Unter den 46 in die Zukunft verlängerten Bahnen durch zwei frühere Ereignisse je Präparation trennen genau **3→11, 4→11 und 5→11** die Kugeln. Die vorausgesagte Auslese ist innen bei Radius 1 und aussen bei Radius 2. Die zwei Bahnen 4/5→11 liegen am Ziel mindestens 0,399 innerhalb des kleinen und 0,0052 ausserhalb des grossen Randes, gemessen als räumlicher Abstand vom Rand. Das Sondenregister enthält jede der 46 Fortsetzungen für beide Präparationen. Die N23-Datei führt die drei trennenden Bahnen und ihre geprüften kausalen Anbindungen auf. Der vorhergesagte Besetzungsunterschied ist eine Folge der beiden eigens konstruierten Geometrien.

### Prüfung als freies diskretes Ereignis

Es gilt die bisherige Regel kᵢⱼ=(1,−9,16,−8) für null bis drei offene Intervallereignisse, darüber k=0. Die alten vier kleinen Gerätekorrekturen betreffen keine der benötigten Dichtezeilen oder ausgehenden Kanten von 22. Das neue Ereignis hat keine eigene Gerätequelle. Seine Zukunft ist bei allen drei Bahnen exakt (7,8,9,10). Die Anbindung 3→11 ist in beiden Präparationen dieselbe mit 164 Relationen. Bei 4/5→11 zählt die schwere Präparation 163, die leichte 164.

* Bei w₂₂>0 verlangt die Variation des Gewichts D₂₂=19+Σ kᵢ₂₂(Y₂₂−Yᵢ)²=0 in rohen Uhreinheiten. Die positiven Vorläufer 4,5,6 haben mit festem frühen Kragen eine gemeinsame lineare Dichtegleichung mit nichtverschwindender Steigung. Damit sind ihre Uhren festgelegt. Die Gleichung an 11 ist eine nach oben offene quadratische Gleichung, am spätesten Vorläufer negativ. Die einzig kausal zulässige Nullstelle wird rational von beiden Seiten eingeschlossen. Diese vier Uhren sind daher auch bei erneuter Bestimmung der übrigen Innenfelder fest. Auf dem gesamten frühen Fenster fällt D₂₂ und ist bereits links negativ. Die obere Schranke über alle hier auftretenden Ordnungen und beide Präparationen beträgt **−1,31**.
* Bei w₂₂=0 verlangt die Variation seiner freien Uhr G₂₂=Σ k₂₂ⱼ wⱼ(Yⱼ−Y₂₂)=0. Die vier k betragen 1,−9,16,−8. Diese affine Funktion hat schon auf dem gesamten Bereich 0≤x≤1 strikt negatives Vorzeichen, mit unverändertem späten Kragen. Auch die leere Randlösung eines fest vorgegebenen Gewichts muss diese Uhrgleichung erfüllen. Das Ergebnis gilt unabhängig von den alten Innenfeldern für diese ausgehenden Kanten.

Damit scheitern alle drei freien Sonden in beiden Vorzeichenklassen (positiv oder leer) bei diesen Randfeldern, positiven frühen Vorläufern und gleicher Wirkungsregel. Ein extern geführter Apparat mit eigener Quelle wäre eine andere Dynamik.

## Vollständige Suche nach einer leeren Einzelsonde

Bei festgehaltenen bisherigen Feldboxen hängt G₂₂ für w₂₂=0 nur von der vollständigen Zukunft F ab. Enumeriert wurden alle nichtleeren nach oben abgeschlossenen F, deren Uhren nach dem linken Fensterrand liegen können. Dies ergibt **31 Zukunftsmengen pro Präparation**. Bei jeder ist Σ k₂₂ⱼwⱼ von null getrennt. Deshalb liegt die einzige mögliche rohe Uhr bei Σ k₂₂ⱼwⱼYⱼ / Σ k₂₂ⱼwⱼ. Die gesamte Box dieser Uhr wird gegen das Messfenster und die Uhren ihrer Nachfolger geprüft. Genau am Halbzeitschnitt überlebt keine. Im breiteren Fenster bestehen je zwei die Prüfung der neuen Uhrgleichung.

| Zukunft von 22 | x schwer | x leicht | mitgeprüfte Vergangenheit je Präparation |
|---|---:|---:|---:|
| 7,8,9,10,14,21 | 0,49544436 | 0,48901275 | 4 |
| 7,8,9,10,18,21 | 0,50698408 | 0,50080630 | 21 |

Für jede Zukunft werden sämtliche nach unten abgeschlossenen Vergangenheiten geprüft, die ohne zusätzliche alte Ordnungsrelationen und nach den Uhrboxen möglich sind. Die Enumeration lässt im Zweifelsfall auch eine überlappende Uhrbox zu und bildet dann eine Obermenge. In jeder dieser 25 Anbindungen pro Präparation ändert sich mindestens eine alte stationäre Dichtegleichung an einem positiven Innenereignis um ein von null getrenntes Intervall. Die Daten enthalten für jede Anbindung die betroffenen Zeilen und deren Änderungen. Das schliesst die leere Einzelsonde mit nichtleerer Zukunft bei genau weiterverwendeten alten Feldern im gesamten Fenster aus. Die globale Aussage bei Neulösung der Innenfelder aus dem vorherigen Abschnitt betrifft nur die drei dort angegebenen Sonden. Ein terminales Ereignis besitzt keinen gemeinsamen Zukunftsanker. Dynamische Fortsetzungen mit neu gelösten alten Feldern und anderer Anbindung bleiben offen.

## Wiederholung

Nach dem Entpacken im Verzeichnis mit Python ab 3.10 ausführen. Alle Nachweise verwenden nur die Standardbibliothek und rationale Einschliessungen. Für die Ortskoordinaten wurden numerisch Vorschläge gesucht. Entscheidend sind die eingeschlossenen Vorzeichen für den beigefügten Vorschlag. Der Prüfplan und die im Lauf der Untersuchung ergänzten Kontrollen sind separat mit Prüfsummen versehen. Es gab keine öffentliche Blindregistrierung.

```sh
sha256sum -c SHA256SUMS
python3 -B pruefen.py
```

Ergebnisse.json dokumentiert die Geometrie, die Schattenfamilien, die Fortsetzungen und die ausgeschlossenen Einbettungen leerer Sonden. Sondenregister.tsv enthält die geometrischen Fortsetzungen und Sonden_auf_N23.json die gegenüber den beiden Kontrollrändern empfindlichen N23-Erweiterungen einschliesslich der dynamischen Ausschlüsse. Die unabhängige positive und leere Masseneichung, die materielle Randidentifikation und eine unabhängig kalibrierte Flächenmessung bleiben offen. Alle acht physischen Pilotradien und 60 P3-Prüfpunkte bleiben NOT_RUN.
