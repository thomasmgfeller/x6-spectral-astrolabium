# Wie breit muss das Ausgangsfenster der beiden inneren Uhren sein?

CST-DUST · N15-Typ 2097151 · 22. November 2026 · [Ausgangspunkt auf GitHub](https://github.com/thomasmgfeller/x6-spectral-astrolabium/pull/356)

Bei Schritt h = 1/8 verwirft ein Ausgangsfilter mit der ursprünglichen Halbbreite 1/64 für jede innere Verschiebung das ganze rechte Randuhrfenster. Ein kohärenter Filter der Halbbreite 7/128 nimmt dagegen jede zugelassene Geschichte auf. Das gilt exakt auf dem vollständigen präparierten Träger. Die numerische Rekonstruktion der markierten Masse 1 bleibt mit diesem breiten Filter bei 0,999855920 bzw. 0,999812474. Ein enges Fenster verändert schon die Eichung. Beim ersten Dichtezentrum sinkt die Rohantwort vom leeren Inneren zur positiven Vierteldosis von 1370,35910 auf 675,21942. Der vereinbarte positive Eichfaktor existiert in dieser numerischen Prüfung nicht.

## Präparation und Quellen

Die Auswertung verwendet die Markierung von Innenbereich und Randkragen, die zwei gleichphasigen äusseren Uhrfenster, die Dichtepräparation und die 15 Phaseneinstellungen von PR #356. Nur die Vorschrift für die Annahme am Ausgang wird variiert. Im eingehenden Mass liegen die sieben normierten Uhrwerte uⱼ = (Tⱼ−T₃)/D um j/8, j = 1,…,7, mit Halbbreite 1/64. Hier ist D = T₇−T₃ = 4Δ−o die vor der Verschiebung bestimmte Dauer, Δ⁴ = 3/722 und o liegt in [−3/32,−1/32] oder [1/32,3/32]. Das Enduhr-Soll ist im betrachteten Modell fest. Eine unbekannte spätere Uhrablesung dürfte für die frühe Ansteuerung nicht vorausgesetzt werden.

Auf der totalen Ordnung werden die beiden inneren Stellen bei drei bzw. fünf strikt früheren inneren Ereignissen angesprochen. Das sind hier die vierte und sechste Uhr. Bei jedem Schritt genügt der bisherige Zählerstand mit der gegebenen Innenmarkierung. Die Adressregel ist unter jeder Umbenennung kovariant, weil strikte Ordnung und Markierung mittransportiert werden. Der Code prüft alle 5040 Permutationen der sieben inneren Namen. Auf verzweigten Ordnungen kann dieselbe Anzahl mehrere Ereignisse auswählen. Diese Studie behandelt die vorliegende Kette.

Für die Quellen a,b = 0 oder ±h werden die skalierten Felder Y = T/Δ wie im Randkern um a/√D bzw. b/√D verschoben. Der Filter prüft die neuen u-Werte beider ausgewählter Uhren gegenüber denselben Zentren im ursprünglichen Bezugssystem. Die äusseren Quellvariationen des Phasenoperators verschieben die Fensterdefinition und die ursprüngliche Dauer dabei nicht. Die Dichten und das Verweilmass werden auf der ursprünglichen Präparation berechnet. Die Messvorschrift behält die komplexe Amplitude auf dem akzeptierten Bereich. Sie schreibt keinen genauen Uhrwert in ein äusseres Register und normiert die Arme nicht einzeln nach.

## Durchlass und Abstand zu anderen Uhren

Für eine verschobene Uhr hat der Betrag des Versatzes in u den Wert q = Δh/D³ᐟ². Auf dem linken äusseren Fenster liegt q zwischen 0,0271628 und 0,0296316, auf dem rechten zwischen 0,0324980 und 0,0358586. Die volle Breite der vorbereiteten inneren Uhr beträgt 1/32 = 0,03125. Beim engen Filter bleibt pro betroffener Uhr ein Längenanteil max(0,1−32q). Rechts ist dieser exakt null. Der breite Filter hat 7/128 = 0,0546875 Halbbreite. Die grösste benötigte Halbbreite beträgt weniger als 0,051484. Sogar ein zusätzlicher Fehler von höchstens 0,003 in der Position der Ausgangsfenster relativ zu den präparierten Zentren erhält den Durchlass. Das ist eine geometrische Toleranz in u, keine Aussage über die Phasengenauigkeit. Selbst zwei breite Nachbarfenster überlappen bei ihrem Mittenabstand 1/8 nicht.

| Strenger Ausgangsfilter | Durchlass im positiven Eingangsreferenzmass, beide äusseren Fenster zusammen |
|---|---:|
| Keine innere Verschiebung | 100 % |
| Eine der beiden inneren Uhren, eine der beiden Richtungen | 8,1026 bis 8,4128 % |
| Beide inneren Uhren, vier Richtungswahlen | 0,8272 bis 0,8644 % |

Die Zahlen sind nach aussen gerundete Prozentgrenzen. Sie messen einen Anteil des positiven Eingangsreferenzmasses. Für exakt leeres Inneres mit atomaren Dichten liegen die entsprechenden Anteile bei rund 6,67053 % und 0,66911 %. Die auswärts gerundeten rationalen Endpunkte für jeden Arm und jedes Fenster stehen in durchlass.json. Diese Anteile sind unabhängig von der positiven Modellmasse, solange die verwendete Dichtebox im zulässigen Bereich liegt. [Herleitung](HERLEITUNG.md)

## Zwei numerische Eichversuche

Nullstandard ist das exakt leere Innere mit positivem Kragen. Der einzige Positivstandard ist die markierte Masse 1/4 bei Dichtezentrum 1/8. Die Eingangspräparationen wurden aus PR #356 übernommen. Alle folgenden Zahlen ausser den geometrischen Grenzen sind deterministische Quadraturwerte.

| Auslese | Leeres Inneres bei 1/8, roh | 1/4 bei 1/8, roh | Masse 1 bei 1/8, roh | Masse 1 bei 1/4, roh |
|---|---:|---:|---:|---:|
| Breiter Ausgang, gemeinsamer Referenzarm | −0,00000786 | 0,25001215 | 0,99992809 | 0,99988464 |
| Enger Ausgang, gemeinsamer Referenzarm | 1370,35910 | 675,21942 | 427,30355 | 1043,73352 |
| Enger Ausgang, Referenz für jeden Arm gleich gefiltert | −0,841638 | −0,869012 | −1,002052 | −1,001822 |

Beim breiten Fenster ergibt die alte Eichung die zwei eingangs genannten Massenschätzungen. Der enge Filter ersetzt das zugelassene Ensemble je nach Phaseneinstellung. Die gewichteten Differenzen der Phasen haben grosse Koeffizienten. Mit der alten Eichung entstehen für Masse 1 die Anzeigen 427,26936 und 1043,64999. Bei einem eigenen Eichversuch liegt der positive Standard unter dem leeren Inneren. Ein bei positivem Standard ansteigender affiner Decoder lässt sich daraus nicht eichen. Die Antwort des vollständig staubfreien Vakuums ist in allen drei primären Fenstermodi roh exakt null, da ausschliesslich positive reelle Integrale verbleiben.

Die dritte Tabellenzeile ist ein gesondert vor ihrer Rechnung festgeschriebener explorativer Vergleich. Für jeden Messarm werden nun exakt dieselben angenommenen Eingangsgeschichten auch in der unverschobenen Referenz verwendet. Dadurch verschwinden die sehr grossen Anzeigen. Der Eichabstand bleibt mit rund −0,027374 negativ. Die Filter im Originalversuch und dieser Vergleich prüfen verschiedene Operationen. Weder Statistik noch Vorzeichen wurden nachträglich zum Erzielen des Zielwerts angepasst.

## Was die Interferenzmessung voraussetzt

Im endlichen Hilfsmodell liefern die normierten Kerne Z₀ und Zₛ bei gemeinsamer kohärenter Endprojektion die gemeinsamen Wahrscheinlichkeiten |Z₀ ± eⁱᶿZₛ|²/4. Aus vier Wahrscheinlichkeiten je Einstellung wurde die ursprüngliche Phasenauslese zurückgerechnet. Bei M = 1 beträgt die kleinste Sichtbarkeit über die 14 Nichtreferenzarme des breiten Filters an beiden Zentren über 99,99998 %. Beim engen Filter sinkt sie auf rund 1,6553 % bzw. 1,6580 %. Ein unterscheidbares orthogonales Armregister löscht beim Ausspuren den Kreuzterm exakt. Das ist eine Kontrolle an einem explizit angenommenen Hilfsraum. Eine physikalische Paarung des gekoppelten Ensembles, Zugriff auf die Quellen und eine von der Markierung unabhängige Ruhemasse-Eichung stehen aus. Alle 60 physischen P3-Prüfpunkte haben den Status `NOT_RUN`.

## Reproduktion

Die Ausgangsdaten in quellen/ stammen bytegleich aus dem Git-Stand 70bad55df756781318fccfd0aec03921a3934fde. herkunft.json nennt alle Pfade und SHA-256-Werte. Der Hauptplan und beide Ergänzungen sind lokal mit getrennten Prüfsummen festgehalten. Die zwei Eichversuche wurden vor ihren jeweiligen Transfers geschrieben. Es gab keine externe Verblindung. Die Null- und Vierteldosiswerte des Vorgängerversuchs waren bekannt.

    python3 -B pruefen.py --nur-exakt
    OPENBLAS_NUM_THREADS=1 python3 -B pruefen.py

Der erste Befehl benötigt Python ab 3.10 und dessen Standardbibliothek. Die Gesamtrechnung verwendet zusätzlich NumPy. Sie reproduziert Geometrie, Durchlass, beide Eichversuche, die 24 Hauptfälle, die gepaarten Referenzen und die Interferenzkontrolle. Die Gitter der Hauptrechnung verwenden 3, 4 und 5 innere sowie 4, 8 und 10 äussere Gauss-Punkte pro Achse. Die Gegenprobe für den engen Filter verwendet Clenshaw-Curtis-Punkte und eine vollständige Tensorkontraktion mit derselben Wirkung. Die scharfen Grenzen werden vor der Quadratur auf die tatsächlich zugelassenen Intervalle abgebildet. Eine validierte Gesamtfehlerschranke für die positiven komplexen Amplituden ist offen.
