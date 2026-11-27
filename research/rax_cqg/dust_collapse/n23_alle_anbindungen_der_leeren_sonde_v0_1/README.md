# CST-DUST · Alle Anbindungen einer freien leeren N23-Sonde

**Für die N22-Grundordnung 216141/229383/0/+ ist in keiner ihrer 2 657 Ein-Ereignis-Erweiterungen ein beidseitig verankerter Kontakt der neuen leeren Sonde 22 mit Materie im frühen Fenster möglich.** Die Aussage gilt einzeln für die schwere und die leichte Randpräparation. Die alten Innenfelder dürfen sich gemeinsam mit der Sonde neu einstellen. Der Ausschluss bezieht sich auf einen Kontakt des **neuen** Ereignisses unter den unten definierten Bedingungen. Die alte Ordnung besitzt bereits Kontakte zwischen 19 und 17 beziehungsweise 20. [Ausgangsstand auf GitHub · PR 415](https://github.com/thomasmgfeller/x6-spectral-astrolabium/pull/415)

## Messfrage und Geltungsbereich

Die normierte Uhr ist $x_i=(Y_i-Y_3)/(Y_7-Y_3)$. Das geschlossene Fenster ist $W=[15/32,17/32]$. Für den getesteten Kontakt müssen (i) die Sonde 22 und ein Ereignis mit positivem Gewicht beide in W liegen, (ii) beide kausal unvergleichbar sein und (iii) einen gemeinsamen positiven Vorgänger sowie einen gemeinsamen positiven Nachfolger haben. Gleichzeitigkeit im Register bedeutet Zugehörigkeit zum selben Fenster.

Gezählt werden Erweiterungen der einen veröffentlichten, beschrifteten strikten N22-Ordnung um genau ein Ereignis, ohne Änderung der alten Relationen. Die vier frühen und vier späten Kragenereignisse, die Nullquelle und die vier Gerätekorrekturen sind vorgegeben. Die inneren Ereignisse 15,17,20,22 haben Gewicht null. Die übrigen elf inneren Gewichte sind strikt positiv. Alle 15 inneren Uhren bleiben frei. Die veröffentlichten Kragenintervalle sind eingeschlossen. Andere Grundordnungen, eine besetzte neue Sonde, ein äusserer Apparat mit Quelle oder gekoppelte Mehrfacherweiterungen brauchen eigene Nachweise.

| Ordnungen je Präparation | Schwere Präparation | Leichte Präparation |
|---|---:|---:|
| Nichtleere Zukunft der Sonde | 2 320 | 2 320 |
| Sonde im Fenster ausgeschlossen | 2 300 | 2 300 |
| Sonde im Fenster durch stationären Zeugen belegt | 5 | 5 |
| Existenz der Sonde im Fenster offen | 15 | 15 |
| Sonde und positives Ereignis im selben Fenster offen | 8 | 10 |
| Beidseitig verankerter Kontakt der Sonde offen | 0 | 0 |
| Zusätzlich mit leerer Zukunft, daher ohne Zukunftsanker | 337 | 337 |

PR 414 hatte die Existenz in fünf Ordnungen pro Präparation mit je zwei verschiedenen Lösungsboxen nachgewiesen. PR 415 schloss den positiven Fenstertreffer auf sämtlichen stationären Zweigen dieser fünf Ordnungen aus. Vor der jetzigen Prüfung war die Auswahl auf zwei Zukunftsmengen konzentriert. Von den übrigen 29 früher bei festgehaltenen Innenfeldern verworfenen Zukunftsmengen schliesst die Rechnung in **22** die Sonde selbst für jede zulässige Vergangenheit aus. Bei den anderen **sieben** verteilen sich die 15 offenen Anbindungen wie folgt. Alle fünf aus PR 414 zugelassenen Anbindungen gehören zu den zwei früher ausgewählten Familien.

| Zusätzliche Nachfolger neben 7,8,9,10 | Sonde offen, je Präparation | Zeitlicher Fund offen, schwer | Zeitlicher Fund offen, leicht |
|---|---:|---:|---:|
| 18 | 3 | 0 | 2 |
| 21 | 3 | 0 | 0 |
| 19,21 | 1 | 0 | 0 |
| 17,18,19,21 | 2 | 2 | 2 |
| 18,19,20,21 | 2 | 2 | 2 |
| 14,17,18,19,21 | 2 | 2 | 2 |
| 14,18,19,20,21 | 2 | 2 | 2 |

Die frühere Uhrvorauswahl hatte weitere 305 kombinatorisch mögliche nichtleere Zukünfte gar nicht aufgeführt. 29 davon scheitern bereits am frühen Kragen. Für die anderen 276 schliesst die neue Rechnung eine stationäre Sonde im Fenster ebenfalls aus. Die 15 offenen Fälle sind offene Existenzfragen. Vier zusätzlich eingeschlossene stationäre Feldlösungen (zwei Familien unter beiden Präparationen) zeigen, warum die Fensterbedingung nötig ist. Mit Vergangenheit {0} liegt die Sonde bei Zukunft über 18 bei etwa 0,42857140 bzw. 0,42108311, bei Zukunft über 21 bei 0,41038292 bzw. 0,40450877. Alle vier zertifizierten Intervalle enden unter 15/32. Daraus folgt keine Eindeutigkeit dieser Lösungen.

## Vollständige Enumeration

Eine Zukunft F muss nach oben abgeschlossen sein, eine Vergangenheit P nach unten. Es gilt $p\prec f$ für alle $p\in P$, $f\in F$. Diese Bedingungen sind notwendig und hinreichend, um 22 mit Vorgängern P und Nachfolgern F einzufügen und die induzierte alte Ordnung zu erhalten. Jede Zukunft wird aus ihrer minimalen Antikette, jede Vergangenheit aus ihrer maximalen Antikette aufgebaut. Eine zweite Implementierung entscheidet in topologischer Reihenfolge über die Aufnahme jedes Ereignisses in ein Ideal. Beide ergeben 337 Ideale, 336 nichtleere Zukünfte und 2 320 kompatible Paare mit nichtleerer Zukunft. 80 dieser Paare verletzen eine feste Kragenuhr im Fenster. Es bleiben 2 240 Anbindungen aus 307 Zukunftsmengen.

Bei leerer Zukunft gibt es weitere 337 Vergangenheiten. Dann ist $G_{22}=0$ identisch. Das Gewicht null entfernt alle eingehenden Beiträge zu den alten Uhrgleichungen. Ein terminaler Punkt verändert keine alte Intervallschicht. Auf den archivierten N22-Feldlösungen kann deshalb für 279 Vergangenheiten je Präparation eine Sondenuhr in W explizit angegeben werden. Zugleich liegen 18 und 19 mit positiven Gewichten im Fenster. Acht weitere Vergangenheiten verletzen die späten Kragenuhren, für 50 bleibt die zeitliche Realisierbarkeit bei freien Innenfeldern offen. Der gemeinsame positive Zukunftsanker fehlt für alle 337. Diese ergänzende Kontrolle erklärt die Rolle der Ankerbedingung.

## Die überprüften Gleichungen

Die Schichtkoeffizienten auf der Transitivrelation sind $k_{ij}=1,-9,16,-8,0$ für null, eins, zwei, drei bzw. mindestens vier Ereignisse im offenen Intervall. Auf (15,16), (16,18), (17,18), (18,7) kommt die Gerätekorrektur $-10^{-11}$ hinzu. Der Prüfer rekonstruiert sie für jede bearbeitete Ordnung. Es gelten elf Dichtegleichungen und 15 Uhrgleichungen

$$
D_j=19+\sum_i k_{ij}(Y_j-Y_i)^2=0,\qquad
G_i=\sum_j k_{ij}w_j(Y_j-Y_i)-w_i\sum_h k_{hi}(Y_i-Y_h)=0.
$$

Für die leichte Präparation verwendet der Prüfer in den homogenen Uhrgleichungen die gemeinsamen Gewichtseinheiten $16w$. Der frühe Kragen liegt zeitlich vor W, der späte danach. Die inneren Uhren ausser 21 und 22 haben 0 als Vorgänger und 7 als Nachfolger. Die ausgehenden Terme des positiven Ereignisses 21 verschwinden selbst dann, wenn die neue leere Sonde ihm folgt. Daher gilt $A Y_{21}=\sum_i k_{i,21}Y_i$ mit $A=\sum_i k_{i,21}$. Die Rechnung prüft $A\ne0$ überall dort, wo sie diese Schranke verwendet.

1. **Erste Ausschlüsse.** $G_{22}$ enthält eine affine Summe über die festen späten Kragenpaare. Sind deren Vorzeichen und alle möglichen freien Beiträge wegen positiver Gewichte und strikter Kausalordnung unvereinbar mit null, scheidet die ganze Familie aus. Sonst schneiden gerichtete Intervallgrenzen Kausalrelationen, quadratische Dichtewurzeln und lineare Gewichtsschranken. Eine Wurzel wird nur bei leerem Schnitt verworfen. Beim Prüfen eines möglichen positiven Partners erhält dessen Uhr die ganze ursprüngliche Fensterhülle.
2. **Rationale Zertifikate.** Alle auftretenden Produkte zweier Unbekannter werden als zusätzliche Variablen mit äusseren Grenzen geführt. Verwendet werden die vier McCormick-Ungleichungen, Tangenten und Sekanten an Quadrate von Uhrdifferenzen sowie die Positivität der Gewichte. Ein Zertifikat ist eine nichtnegative rationale Linearkombination gültiger Ungleichungen. Die exakt berechnete Untergrenze ihrer linken Seite muss strikt oberhalb der rechten Seite liegen. Eine kleinere Teilbox darf nur den ihr zugewiesenen Bereich ausschliessen. Bei jeder Teilung werden beide geschlossenen Hälften nachgerechnet.
3. **Zusätzliche Momentbedingungen.** Die lineare terminale Uhrgleichung darf mit jeder vorhandenen Uhr und jedem Gewicht multipliziert werden. Für Produkte zweier Uhrdifferenzen gelten ihre rechteckigen Produktgrenzen. Ein ergänzender Schnitt stammt aus dem Quadrat einer reellen affinen Form in $Y_{15},\ldots,Y_{22}$ mit gespeicherten ganzzahligen Koeffizienten. Seine Nichtnegativität gilt auf jeder echten Feldlösung. Der Offline-Prüfer baut den Schnitt aus dem Koeffizientenvektor neu auf.
4. **Gezielte Verfeinerung.** Für einen terminalen Elternwert $Y_i$ mit Koeffizient $k$ und $B=A-k\ne0$ bezeichnet $m$ das signiert gewichtete Mittel der übrigen Eltern. Dann gilt $Y_{21}=m+(k/A)(Y_i-m)$. Die kombinierte Dichtegleichung hat die Form $0=19+\sum_{j\ne i}k_j(Y_j-m)^2+(kB/A)(Y_i-m)^2$. Das Vorzeichen der Wurzel folgt aus $Y_{21}>Y_i$. Differenzen der Uhrgleichungen leerer Ereignisse liefern weitere Intervalle. Keine Division mit unentschiedenem Vorzeichen dient als Ausschluss.
5. **Frühe Uhren.** Nur wenn die tatsächlichen Dichtezeilen exakt die Koeffizienten von PR 415 besitzen, verwendet der Prüfer deren gemeinsame Projektion. Für $a=Y_{16}$ und $u=Y_{15}$ liefert $D_{16}$ die kausale Quadratwurzel. $D_{19}$ ist dann linear mit Steigung $-2h$, $h=-8Y_1+16Y_2-9u+a$. Die ganze zulässige a-Achse wird überdeckt. Unentschiedene Nenner führen zu Teilung oder zu einer weiteren Hülle. Zusätzliche Schranken aus $D_{18},G_{18}$ und der Differenz $G_{17}-G_{20}$ werden erst nach Prüfung der jeweiligen Zeilen, Vorzeichen und kausalen Lücken verwendet.
6. **Übertragung zwischen Ordnungen.** Innerhalb derselben Zukunft dürfen Ausschlüsse auf eine andere Vergangenheit übertragen werden, wenn sämtliche freien Wirkungszeilen identisch sind und alle zusätzlich benötigten strikten Zeitrelationen aus der Zielordnung oder dem festen Kragen folgen. Das Fallregister nennt die Ursprungszeile. Eine Übertragung betrifft den jeweils ausgeschlossenen Partner oder die Sondenexistenz.

Die Intervallrechnung rundet mit Ganzzahlen auf einem Raster von $2^{-64}$ nach aussen. Die Zertifikatsprüfung verwendet exakte rationale Arithmetik. Das Raster approximiert Intervallgrenzen und diskretisiert den Lösungsraum nicht. Numerische Optimierung und Mehrfachstarts dienten zum Auffinden von Vorschlägen. Ein Suchabbruch ohne Zertifikat erzeugt den Status OFFEN. Die vier neuen stationären Kontrolllösungen wurden separat durch eine kontrahierende, vorkonditionierte Abbildung auf rationalen Boxen und durch die direkten Originalgleichungen geprüft. Ausserdem bestehen die vier früheren bekannten Fensterlösungen die neuen Intervallbedingungen und die Kontrolle der erweiterten linearen Hülle.

## Wiederholung und Dateien

Nach dem Entpacken im Studienverzeichnis mit Python ab 3.10 und seiner Standardbibliothek ausführen.

```sh
sha256sum -c SHA256SUMS
python3 -B pruefen.py
python3 -B gegenprobe.py
```

Der Hauptlauf berechnet Ergebnisse.json, Fallregister.tsv (4 640 Zeilen ohne Kopf) und Zukunftsregister.tsv erneut und vergleicht die Ausgaben byteweise. Die Gegenprobe prüft die vollständige Idealmenge unabhängig, reproduziert die älteren stationären Ausgangsfelder und Fensterzeugnisse aus den archivierten Paketen und vergleicht die exakten Kontrollfelder und das Terminalregister. Gesamtregister.tsv führt alle 5 314 Kombinationen aus Ordnung und Präparation zusammen. Die Datei Zertifikate.json enthält die tatsächlich verwendeten rationalen Gewichte, Teilbäume und Quadratbedingungen. Vor der Rechnung wurden Frage, Fenster und Sektor in Pruefplan.md festgehalten. Die terminalen Beispiele und die zusätzlichen stationären Kontrollfelder ergänzen den Primärtest. Es gab keine öffentliche Blindregistrierung.

Der Ausschluss entscheidet die Eignung der **neu eingefügten** Einzelsonde als Partner eines verankerten Randkontakts. Die physische Oberfläche des Staubballs und ihre unabhängige Flächen- und Masseneichung bleiben offen. Acht physische Pilotradien und 60 P3-Prüfpunkte stehen auf NOT_RUN.
