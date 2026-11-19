# CST-DUST · N14-Endgewichte und verschobene Staubuhrschnitte

**19. November 2026 · Etappe 6 · Endordnungen A = 1790 und B = 5374.**

Auf dem publizierten N14-Träger scheitert jede Fortsetzung, die allen markierten Pfaden mit demselben unmarkierten Endtyp denselben Amplitudenkoeffizienten zuweist. Das lässt sich mit exakten Zahlen zeigen. Für jede der beiden ausgewählten Ordnungen kann die gekoppelte Amplitude dagegen über zwei verschiedene Staubuhrschnitte ausgewertet werden. Die Wahl des relativen Historiengewichts bleibt dabei frei.

## Welche Gewichtsregeln sind ausgeschlossen?

Der Test verwendet die beiden N11-Eltern, die veröffentlichte N13-Marginale und alle N14-Pfade, die in allen sechs Reihenfolgen der drei Einfügungen zulässig sind. Die zwei alten Einfügungsmarken sind als Paar ungeordnet. Sei Hₚⱼ die Zahl solcher markierten Pfade mit N13-Präfixklasse p und N14-Endtyp j. Eine endtypabhängige Regel ordnet jedem solchen Pfad den Koeffizienten wⱼ zu. Sie muss H w = b erfüllen, wobei b die bereits festgelegten linearen Präfixkoeffizienten bezeichnet. Diese Marginale wird vor Wirkungsphase und Detektor gebildet. Die Werte sind keine Born-Wahrscheinlichkeiten. Die Regel darf für jede der beiden N11-Eltern eigens gewählt werden.

| N11-Elternordnung | Markierte Pfade | N13-Klassen / N14-Endtypen | Rang von H | Kleinster erreichbarer Abstand in Totalvariation |
|---|---:|---:|---:|---:|
| Kette | 924 | 35 / 53 | 28 | 214/3255 ≈ 0,065745 |
| Eine Kante | 1 026 | 38 / 72 | 35 | 109/1568 ≈ 0,069515 |

Bei der Kette erzeugen die Präfixklassen 33566 und 1049374 genau dieselben Anzahlen für jeden der 53 Endtypen. Gefordert sind jedoch 5/217 und 10/217. Bei der Ein-Kanten-Ordnung verschwindet die Zeilenkombination H₅₃₀₈₄₄₄ − H₅₅₇₀₅₈₀ − H₇₂₃₅₁₇₇₂ + H₇₂₆₁₃₉₀₈ für alle 72 Endtypen. Dieselbe Kombination der geforderten Gewichte ist 1/49. Beide Widersprüche gelten auch bei komplex zugelassenen wⱼ unter derselben linearen Marginalbedingung.

Die Mindestabstände in der Tabelle gelten für normierte, nichtnegative Koeffizienten. Dazu wird jede Spalte von H auf Summe eins normiert. Die möglichen Marginalen bilden die konvexe Hülle dieser Spalten. Für jeden Mindestabstand enthält result.json eine erreichende Endtypverteilung und eine Testfunktion 0 ≤ f ≤ 1 auf den Präfixen. Die Differenz zwischen dem Zielmittel von f und dem grössten Spaltenmittel liefert dieselbe Zahl als exakte Untergrenze. Der lineare Optimierer dient zum Finden der Zeugen. Die beiden Schranken werden mit rationaler Arithmetik geprüft. Sowohl gleiches Gewicht je markiertem Pfad als auch Gewichte proportional zu 1/|Aut(j)| sind in dieser Klasse enthalten. Für ein eigenständig abgeleitetes Mass mit anderen Marginalbedingungen wäre die Rechnung neu anzusetzen.

## Was die verschobenen Schnitte prüfen

Der Test übernimmt das kohärente zweiteilige Uhrenpaket, die Dichtezentren 1/8 und 1/4, den Skalar-Gausseingang und den q₇-Detektor. In der dimensionslosen Uhrenamplitude ist exp(i F₄) genau einmal enthalten, mit F₄(A) = 52 und F₄(B) = −32. Die relativen Gewichte wurden für keinen der beiden Schnitte angepasst.

Bei s = 0 und s = 1/4 wird das freigegebene Vergangenheitsideal Dₛ separat berechnet. Es enthält j genau dann, wenn alle Uhren bis einschliesslich j unter der Schwelle liegen. Für ein gegebenes Ideal D wird über ein Rechteck integriert. Die Uhren der enthaltenen Ereignisse liegen unter s, diejenigen der minimalen ausgeschlossenen Ereignisse darüber. Die übrigen Uhren behalten den vollen Integrationsbereich. Jede Ordnung hat an jedem Schnitt 14 solche Ideale. Ihre komplexen Beiträge werden vor der Randpaarung summiert. Das erhält die Kreuzterme sowohl zwischen den unbeobachteten Idealen als auch zwischen A und B. Als unabhängige ungeschnittene Referenz dient die archivierte direkte Randamplitude ohne Zwischenschnitt auf dem 80×12-Gitter.

Zusätzlich werden die drei Fälle «erste Freigabe bis 0», «zwischen 0 und 1/4» und «später als 1/4» auf einem eigenen geteilten Gitter zusammen berechnet und mit beiden Einzelschnitten verglichen. Für den reinen Referenzprozess mit unabhängigen gleichverteilten Uhren wird auf allen 14 Idealzuständen die Zusammensetzung von 0 über 1/4 bis 3/8 in Bruchrechnung geprüft. Diese Zusammensetzung betrifft die Referenzuhr auf jeder festen Endordnung. Die gekoppelte Rechnung vergleicht die Endamplituden bei verschobener Integrationszerlegung. Ein eigenständiger physikalischer Vorwärtskern zwischen wechselnden Ordnungen bleibt offen.

Auf dem 64×10-Gitter ist die grösste absolute Abweichung der komplexen Amplituden von der ungeschnittenen Referenz 3,81 × 10⁻¹⁵. In der vollständigen 2×2-Gram-Matrix einschliesslich des komplexen Kreuzterms beträgt sie 4,96 × 10⁻¹⁷, in den drei q₇-Fenstermatrizen höchstens 1,89 × 10⁻¹⁷. Von 48×8 auf 64×10 ändern sich die einzeln aufgelösten Amplituden um höchstens 4,10 × 10⁻¹². Der direkte sechsdimensionale Kleingittervergleich prüft die Zugehörigkeit zum Ideal anhand aller freigegebenen Ereignisse. Der grösste beobachtete Amplitudenunterschied beträgt dort 1,34 × 10⁻¹⁷. Die Zahlen geben beobachtete Gitterdifferenzen an.

## Was am Schnitt unterscheidbar ist

Im Referenzmass sei p = (s + 3/2)/3. Beide Endordnungen haben zwei minimale Innenereignisse. Die Wahrscheinlichkeiten für null oder ein freigegebenes Ereignis stimmen für alle p überein. Die erste unterscheidende Ereigniszahl ist genau zwei. Für sie beträgt die Differenz A minus B exakt p³(1−p)². Bei s = 0 sind die Werte 3/16 und 5/32. Bei s = 1/4 beträgt die Differenz 8575/248832. Die Herleitung zählt alle 64 möglichen Mengen roher Uhren unter der Schwelle und prüft die zugehörigen Idealrechtecke. Die gekoppelten komplexen Beiträge aus genau diesen Zweier-Idealen stehen separat in result.json. Für das explizite Modell eines orthogonalen Eintrags «genau zwei / sonst» lässt sich die Änderung am Enddetektor berechnen. Bei gleichen A/B-Koeffizienten, Dichte 1/8 und Schnitt 0 ergibt sich mit unbeobachteter Alternative ein q₇-Erfolg von 0,00002323219, mit orthogonal gespeichertem Eintrag 0,00001662627. Die Differenz beträgt 0,00000660592 und stammt aus dem entfernten Kreuzterm. Ein solcher Eintrag ist ein hypothetischer Messeingriff. Ob es in der physikalischen Staubuhr ein entsprechendes Instrument gibt, ist offen.

## Welcher Koeffizient offen bleibt

Die ausgewählten A- und B-Orbits haben in allen sechs Markierungsreihenfolgen dieselbe Präfixspalte mit je 1/3 auf drei markierten N13-Präfixen. In der publizierten positiven Fortsetzung können die Orbitmassen daher gleichzeitig auf 1/882 − t und 1/882 + t gesetzt werden, mit |t| < 1/882. Die anderen Massen bleiben fest. Auf dem gewählten Paar ist der Quotient der komplexen skalaren Vorfaktoren damit (1/882 + t)/(1/882 − t) mal Zᴮ/Zᴬ. Z bezeichnet das integrierte Uhrenpaket einschliesslich der Gravitationsphase. Die normierten skalaren Endfunktionen sind verschieden, ihre Gram-Matrix ist im Prüfer enthalten.

| Dichtezentrum | Zᴮ/Zᴬ bei gleichen Historienkoeffizienten | q₇-Erfolg bei A:B = 1:1 | q₇-Erfolg bei A:B = 1:3 |
|---|---|---:|---:|
| 1/8 | −1,06322 − 0,52028 i | 0,00002323219 | 0,00003285842 |
| 1/4 | −1,06410 − 0,51852 i | 0,00002302212 | 0,00003256169 |

Die beiden Spalten mit Erfolgswahrscheinlichkeiten beziehen sich auf die neu auf das Paar normierte Präparation. Der Wechsel von 1:1 zu 1:3 entspricht t = 1/1764 in der ursprünglichen Fortsetzung. Die frühere direkte Auslese wird damit auf den neuen Schnittgittern reproduziert. Die positive Gram-Matrix betrifft die konditionierten Endzustände. Normerhaltung einer vollständigen Vorwärtsentwicklung mit allen Ausgängen und ein kontinuierlicher Fehlernachweis stehen aus. Der P3-Pilot bleibt auf HOLD.

## Wiederholen

Unter Linux mit Python 3.12, NumPy 2.3.5, SciPy 1.17.0, SymPy 1.14.0 und einem C99-Compiler läuft die Wiederholung im entpackten Ordner mit folgendem Aufruf.

```sh
python -B verify.py
```

Die Wiederholung verwendet eine lokale CPU. Sie prüft die SHA-256-Prüfsummen und die Git-Objekte der mitgelieferten Eingaben, rekonstruiert die exakten Zeugnisse und berechnet alle gekoppelten Gitter erneut. Die Rechenergebnisse stehen in result.json. contract.json dokumentiert Schnitte, Präparation und Vergleichstoleranz. Die Quelldateien und Git-Objektkennungen sind in provenance.json ausgewiesen.

[Publizierte N14-Präparation und Marginale](https://github.com/thomasmgfeller/x6-spectral-astrolabium/tree/2b6574c0fc0f8a2e66680199862e91fe27822027/research/rax_cqg/dust_collapse/history_measure_state_space_v0_1) · [Kausale Definition des Staubuhrschnitts](https://github.com/thomasmgfeller/x6-spectral-astrolabium/tree/2b6574c0fc0f8a2e66680199862e91fe27822027/research/rax_cqg/dust_collapse/relational_transport_n11_v0_2)
