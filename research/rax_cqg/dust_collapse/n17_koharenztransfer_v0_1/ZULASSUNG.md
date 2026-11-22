# Zulassung des zweiten Ordnungstyps 42429

**Entscheid.** Die zwei Vorzeichenpakete auf Typ 42429 sind für den prospektiven N17-Test zugelassen. Beide behalten auf der ganzen Box ihr Stromvorzeichen. Für den Anschluss über die lange Kette und für die abgeschirmte Kontrolle ist die bedingte Ausgangsnorm endlich und strikt positiv. Die Zulassung wurde ohne Auswertung einer Enddichtewahrscheinlichkeit, einer Differenz zwischen den Uhrpräparationen oder eines entsprechenden Vorzeichens bestimmt.

## Auswahl, Ordnung und Prüfumfang

Für diesen Typ existiert ein früherer N15-Zeuge mit identischen äusseren Uhren und zwei entgegengesetzten Anfangsströmen. Er betrifft je eine Feldbelegung. Die Zulassung erweitert diesen Zeugen auf Boxen mit positivem Volumen. Der ursprüngliche Prüfer ist als `basis/zeuge42429.py` beigefügt. [Ursprünglicher N15-Zeuge](https://github.com/thomasmgfeller/x6-spectral-astrolabium/blob/83b8a71bb96f2d794ecc35909f8102c20901f7f6/research/rax_cqg/dust_collapse/n15_sign_record_audit_v0_1/counterexample_42429.py)

Auf den ursprünglichen Labels ist der Eingang die Kette (0,1,2,3), der Zukunftskragen ist die Kette (7,8,9,10). Die maximalen inneren Pfade sind (4,5,11,12), (4,5,14), (4,13), (6,13). Das erste neue Ereignis 15 erhält als Vorgänger den vollständigen Eingang und die eindeutige längste innere Kette. Diese Menge ist ein Ordnungsideal. Im abgeschirmten Vergleich erhält 15 alle 15 alten Ereignisse als Vorgänger. In beiden Fällen liegt Ereignis 16 hinter allen 16 bisherigen Ereignissen. Für jede der beiden Erweiterungen verschwinden alle BD-Koeffizienten vom Eingang zu 15 und 16. Die gemeinsamen Eingangsuhren treten somit weder im ersten noch im zweiten neuen Wirkungsterm auf. Der aus der Gesamtwirkung bestimmte Eingangsstrom jeder alten Feldbelegung ist exakt erhalten. Diese Prüfung berücksichtigt alle vergleichbaren Paare und ihre offenen Intervalle.

## Vollständige Boxen und Einheiten

Alle Uhren tragen dimensionslose Koordinaten \(Y_i=T_i/\Delta\) mit \(\Delta^4=3/722\). Die innere Dichtekoordinate lautet \(W_i=w_i/\Delta\), während die Randdichten direkt in \(w\) angegeben werden. Die markierte Masse \(M=1/4\) stammt aus der gewählten Modellpräparation. Es gelten die folgenden Festlegungen für beide Pakete und beide Ordnungen.

| Grösse | Festlegung |
|---|---|
| Eingangsuhrzentren | \(Y_P=(-5,-4,-3,-7/4)\), also \(e=Y_3+2=1/4\) am Zentrum. |
| Innere Zentren | In Knotenreihenfolge (4,5,6,11,12,13,14) gilt \(u=(1,2,1,3,4,2,3)/5\). Nur \(u_{11}\) wird um \(-1/128\) (positiv) oder \(+1/128\) (negativ) verschoben. Dann \(Y_i=Y_3+(4-e)u_i\). |
| Innere Dichten | Mit \(f_i(u)\) als mittlerem Zellanteil über die vier Pfade gilt am Zentrum \(W_i=M(4-e)f_i=(15/16)f_i\). Auf jedem Pfad bilden die Uhrmittelpunkte zwischen benachbarten inneren Ereignissen die Zellgrenzen. Die äusseren Zellgrenzen liegen bei null und eins. |
| Paketradius | Unabhängig und flach auf jedem der 15 Intervalle in \(Y_3\), sieben \(Y_i\) und sieben \(W_i\), jeweils um den betreffenden Mittelpunkt mit Halbbreite \(2^{-32}\). Die drei übrigen Eingangsuhren sind fest. |
| Bisheriger Zukunftskragen | \(Y_7=2\) ist fix. \(Y_8,Y_9,Y_{10}\) liegen unabhängig und flach um 3, 4, 5 mit Halbbreite \(2^{-20}\). |
| Dichte am alten Eingang | Ein gemeinsamer flacher Wert \(w_P\in[3/32,5/32]\) für alle vier Eingangsknoten. |
| Endliche Randdichten | Alle vier alten Zukunftsdichten und \(w_{15}\) werden in separaten normierten flachen Fenstern \(1/8\pm2^{-20}\) kohärent geschlossen. Die Enddichte \(w_{16}\) bleibt im selben Fenster offen. |
| Neue Uhren | \(Y_{15}=6+x\) mit \(\lvert x\rvert\le h_{\rm Uhr}\le 2^{-18}\) und \(Y_{16}=7\). Die Zulassung gilt sowohl für die fixierte Uhr im gesamten Bereich als auch für die gleichförmig-kohärente Projektion über ein dort enthaltenes zentriertes Fenster und für die entsprechende unaufgelöste Zeitmischung. |

Der Prüfer rechnet mit rationalen Intervallen. Er prüft die strikte innere Uhrordnung, die ursprünglichen Profilfenster \(\lvert u_i-u_i^0\rvert<1/64\), das alte physische Offsetfenster \(1/32<\Delta e<3/32\), die vollständigen 1-%-Dichtebänder und die positiven physischen Dichten der sieben inneren Knoten. Die Kastenzustände besitzen positive Volumina in ihren 15 freien Achsen. Die kleinen unabhängigen Dichteabweichungen sind wie in der ursprünglichen Bandpräparation zugelassen. Der unveränderte Strom in den gewählten Einheiten ist

\[
p=\frac{1}{19}\sum_{j\in I}W_j\sum_{i\in P} b_{ij}(Y_i-Y_j).
\]

| Paket | Exakter Zentrumswert von \(p\) | Nach aussen gerundetes Intervall für das ganze Paket |
|---|---:|---:|
| Positiv | \(1863/622592\) | \([0{,}002992327;\;0{,}002992330]\) |
| Negativ | \(-327/622592\) | \([-0{,}000525225;\;-0{,}000525222]\) |

Die vollständig rationalen Grenzen und alle 15 Zentrumskoordinaten sind in [zulassung.json](zulassung.json) gespeichert.

## Nichtverschwindende bedingte Norm

**Staub.** Jeder Wirkungsterm lautet \(w_j[-1/2-\sum_{i\prec j}b_{ij}(Y_i-Y_j)^2/38]\). Für jedes Paket umfasst ein rationaler Phasenbogen sämtliche zugelassenen Uhren und Dichten, einschliesslich des ganzen Enddichtefensters. In beiden Ordnungen beträgt seine Breite \(L<0{,}27474\). Nach Drehung um den Mittelpunkt ist der Realteil jeder Phase mindestens \(1-L^2/8>0{,}99056\). Sämtliche flachen Amplitudenmittel sind auf ihren jeweiligen Bereich normiert. Über den angegebenen Intervallen folgt eine gleichmässige positive Untergrenze des Staubamplitudenbetrags, auch für jede fixierte frühere Uhr. Für das Zeitgemisch addieren sich die positiven Zweignormen. Diese Schranke bezieht sich auf das normierte Paketmass und die vereinbarte bedingte Randpaarung.

**Skalarfeld.** Übernommen werden der H₃-Rahmen und die zentrierten Gaußformen an den zwei alten dreidimensionalen Skalarenden. Die alten sieben inneren Skalarkoordinaten und die zwei Rahmenrichtungen werden mit derselben regulierten Fresnel-Konvention wie in #349 integriert. Die Determinante des zugehörigen reellen 9×9-Blocks ist beim Kettenanschluss −6 393 181 680 und bei der Abschirmung −216 381 184. Der invertierbare Block definiert einen endlichen, von null verschiedenen Vorfaktor. Die Gaußintegration über die sechs Randkoordinaten enthält das positiv definite \(1+A^2\) einer reell symmetrischen Matrix \(A\). Am Ende bleiben \(q_{15}\) und \(q_{16}\) mit der gedämpften Gaußform \(\exp[-\beta q^T(D-iB)q/2]\), \(D\succeq0\), \(\beta=4/\sqrt6\). Die rationalen Matrizen stehen im Ergebnis. Für \(q_{15}\) und \(q_{16}\) wird jeweils das normierte flache Mass auf \([-1,1]\) verwendet. Der frühere Port wird kohärent geschlossen, der spätere bleibt offen.

Bei \(q_{16}=0\) ist das letzte \(q_{15}\)-Integral bis auf den nichtverschwindenden Vorfaktor gleich \(\int_0^1 e^{(-a+ib)z^2}\,dz\) mit \(a\ge 0\). Für \(b=0\) ist es reell und positiv. Für \(b\ne0\) hat sein Imaginärteil nach der Substitution \(s=|b|z^2\) das Vorzeichen von \(b\). Denn auf \([0,|b|]\) wird \(\sin s\) mit dem streng fallenden positiven Gewicht \(e^{-as/|b|}/\sqrt s\) integriert. Jede negative Halbwelle wird durch die vorhergehende positive Halbwelle strikt überwogen, auch wenn die letzte Halbwelle nur teilweise enthalten ist. Stetigkeit in \(q_{16}\) liefert eine Menge positiven Masses mit nichtverschwindender Amplitude. Kompaktheit der beiden letzten Fenster liefert Endlichkeit. Zusammen mit der Staubschranke ergibt dies bei beiden Ordnungen eine positive endliche Ausgangsnorm. Diese Argumentation behandelt auch den längeren Phasenbogen des Kettenanschlusses.

Der Test ist auf die markierten Pakete und diese Randpaarung bedingt. Er liefert weder eine physikalische Norm des gesamten Historienensembles noch eine Akzeptanzwahrscheinlichkeit pro physischem Eingangsversuch. Die zulassungsrelevante alte Uhr 11 koppelt zusätzlich an die alten Zukunftsknoten 8 und 9. Die spätere Zielauswertung muss deshalb den Fixuhrarm eigenständig behandeln. Der Zulassungsprüfer wertet keinen Dichtedetektor aus.

## Reproduktion

```sh
python3 -B zulassung.py > zulassung.neu.json
diff -u zulassung.json zulassung.neu.json
```

Benötigt wird ausschliesslich die Python-Standardbibliothek (Python 3.9 oder neuer).
