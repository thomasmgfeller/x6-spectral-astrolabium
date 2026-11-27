# CST-DUST · Positiver Messpunkt neben der freien N23-Sonde

Für alle 25 vorgegebenen N23-Ordnungen und beide Kragenpräparationen ist ein positiver Messpunkt im frühen Fenster bei gleichzeitig dort liegender leerer Sonde 22 ausgeschlossen. Die Aussage umfasst sämtliche stationären Lösungen in diesem Sektor. Die bekannten stationären Sonden in fünf Ordnungen bleiben als Positivkontrollen erhalten. Die übrigen 20 Ordnungen erlauben schon die Sonde allein nicht im Fenster. Der zugrunde liegende Datensatz und die früheren Nachweise sind im Paket enthalten. [Ausgangsstand PR 414](https://github.com/thomasmgfeller/x6-spectral-astrolabium/pull/414)

Das Koordinatenfenster ist $W=[15/32,17/32]$ für $x_i=(Y_i-Y_3)/(Y_7-Y_3)$. Positiv bedeutet $w_i>0$. Die 23 Ereignisse umfassen acht feste Kragenereignisse, elf positive innere Ereignisse und vier leere innere Ereignisse (15, 17, 20, 22). Alle 15 inneren Uhren sind frei. Beide veröffentlichten Randpräparationen, alle vier Gerätekorrekturen und die Nullquelle gelten im gesamten Nachweis.

## Fünf Ordnungen, vier Gleichungssysteme

| Weitere Zukunft von 22 neben 7,8,9,10,21 | Zulässige Vergangenheiten der Sonde aus PR 414 | Endboxen schwer / leicht für W | Endboxen schwer / leicht für den zusätzlichen Abstandstest |
|---|---|---:|---:|
| 14 | ∅, {0}, {0,1} | 1 373 / 1 661 | 1 451 / 1 796 |
| 18 | ∅, {0} | 127 / 316 | 156 / 770 |

Die fünf Ordnungen ergeben innerhalb jeder Präparation zwei Systeme notwendiger Gleichungen. Die aus der transitiven Ordnung neu gezählten Koeffizienten und die benötigten Kausalrelationen werden für jede der fünf Ordnungen einzeln geprüft. Die Rechnung erfasst die ganzen in PR 414 veröffentlichten Kragenintervalle. Jede Endbox des Hauptlaufs enthält einen geprüften Widerspruch. Im ursprünglichen Fenster ergeben sich 3 477 Endboxen, im ergänzenden Abstandstest 4 173. Alle Läufe endeten mit null offenen Bereichen.

## Wie nahe kommt ein positives Ereignis?

Die Sonde bleibt in $W$. In einer zusätzlichen, nach dem Primärtest gewählten Rechnung werden nur die Zeitgrenzen für positive Ereignisse um $1/1280$ nach beiden Seiten erweitert. Für jedes positive Ereignis auf jedem untersuchten stationären Zweig ist auch das erweiterte geschlossene Intervall ausgeschlossen.

Sei $d_*$ das Infimum von $\operatorname{dist}(x_i,W)$ über alle positiven Ereignisse aller untersuchten stationären Lösungen mit $x_{22}\in W$, über beide Präparationen. Dann gilt

$$
0{,}00078125=1/1280\ \le d_* < 0{,}000786788.
$$

Die obere Schranke liefert der tatsächlich existierende leichte Zweig mit Zukunft über 18. Dort liegt $x_{19}$ in der Nähe von 0,53203678712. Seine gesamte zertifizierte Box liefert die obere Schranke, die in Ergebnisse.json auch als exakter Bruch steht. Die untere Schranke folgt allein aus der Abdeckung. Die Zahlen sind dimensionslose Uhrabstände, gemessen vom nächsten Fensterrand.

## Herleitung der globalen Ausschlussrechnung

Für eine positive innere Dichte gilt $D_j=19+\sum_i k_{ij}(Y_j-Y_i)^2=0$. Für eine freie Uhr gilt $G_i=\sum_j k_{ij}w_j(Y_j-Y_i)-w_i\sum_h k_{hi}(Y_i-Y_h)=0$. Die offenen Intervallschichten tragen die Koeffizienten 1, −9, 16, −8, danach null. Auf den vier Gerätekanten wird $\epsilon=10^{-11}$ subtrahiert. Für die leichte Präparation werden die beteiligten Gewichte für die homogenen Uhrgleichungen einheitlich mit 16 multipliziert. Damit liegen alle besetzten Innengewichte beider Rechnungen im gemeinsamen Hilfsintervall $(0,16]$. Die physische Kalibrierung wird dabei nicht verwendet oder verändert.

**Frühe positive Ereignisse.** Die Dichtezeilen an 4, 5 und 6 stimmen überein und sind linear mit von null getrennter Steigung. Daher gilt $Y_4=Y_5=Y_6$. Bei 11, 12 und 13 haben die beiden Lösungen für den Zuwachs ab einem kausalen Vorläufer entgegengesetzte Vorzeichen. Die positive Wurzel ist jeweils eindeutig. Alle sechs Uhren liegen vor dem erweiterten Fenster. Bei 14 heben sich die drei frühen Beiträge exakt auf. Auf dem ganzen erweiterten Fenster ist bereits $19-9(Y_{14}-Y_{11})^2>0$. Alle weiteren Terme sind nichtnegativ. Auch die Kragenereignisse liegen ausserhalb. Als mögliche positive Messpunkte verbleiben 16, 18, 19 und 21.

**Vorgänger und positive Uhr 19.** Schreibe $u=Y_{15}$, $a=Y_{16}$, $c=Y_{17}$, $b=Y_{18}$, $p=Y_{19}$, $d=Y_{20}$, $t=Y_{21}$ und $z=Y_{22}$. Mit $P(a)=19-8(a-Y_0)^2+16(a-Y_1)^2-9(a-Y_2)^2$ erzwingt $D_{16}=0$ und $u<a$ die Wurzel $u=a-\sqrt{-P(a)/(1-\epsilon)}$. Die vier Koeffizienten von $D_{19}$ an $(Y_1,Y_2,u,a)$ sind $(-8,16,-9,1)$. Ihre Summe verschwindet. Setze $h=-8Y_1+16Y_2-9u+a$. Damit ist $D_{19}(q)=-2h(q-p)$. Eine eindimensionale Abdeckung von $Y_2<a<Y_7$ mit $u>Y_2$ und $a<p<Y_7$ ergibt $a\in[-1{,}071,-0{,}889]$ und $0{,}45\le h\le1{,}93$. Das Programm verwendet für $a$ die engere, nach aussen gerundete dyadische Hülle von $[-1{,}07,-0{,}89]$. 16 scheidet als Messpunkt aus. Die lineare Dichtezeile wird auch vor der Division auf Verträglichkeit geprüft.

**Begrenzung der positiven Uhr 18 und des Abstands der leeren Uhren.** Sei $J=\{c,d\}$ als Liste der beiden Ereignisuhren, bei Zukunft über 18 ergänzt um $z$. Die Dichtegleichung lautet

$$
2h(b-p)=\sum_{s\in J}(b-s)^2-\epsilon\big[(b-a)^2+(b-c)^2\big].
$$

Alle beteiligten kausalen Lücken sind positiv und kleiner als 8. Für $O_{18}(b)$, die ausgehende Impulssumme zum späten Kragen, gilt auf dem ganzen benötigten Uhrbereich $O_{18}<0$. Aus $G_{18}=0$, $w_{18}>0$ und der letzten Gleichung folgen

$$
\sum_{s\in J}(b-s)\le h+16\epsilon,\quad
p\le b+128\epsilon/(2h),\quad
b\le p+(h+16\epsilon)^2/(2h).
$$

Bezeichnet $U$ die obere Rohzeitgrenze für ein positives Ereignis, so erfordert ein Treffer bei 18, 19 oder 21 die Bedingung $p\le U+128\epsilon/(2h)$, denn $p<t$. Selbst beim erweiterten Fenster folgt $b<1{,}18$. Aus $G_{18}$ ergibt sich nun $w_{18}\ge -O_{18}(b)/(1{,}93+16\epsilon)>0{,}0052$. Der späte Koeffizient $L=-9w_7+16w_8-8w_9$ liegt über −0,005. Daher ist $H=L+w_{18}+w_{21}>0$ und $w_{18}/H\le26$. Die Differenz $G_{17}-G_{20}=0$ ergibt $(d-c)H=\epsilon w_{18}(b-c)$. Für $v=(c-d)/2$ folgt $|v|<2\cdot10^{-9}$. Bei Zukunft über 18 haben $G_{20}$ und $G_{22}$ dieselbe affine Form mit Steigung $-H$ und damit $d=z$.

**Terminale Uhr und letzte notwendige Zeilen.** Mit $m=(c+d)/2$, $K=-8Y_2+16u-9a+p+z$ und $B=19-8Y_2^2+16u^2-9a^2+p^2+z^2$ liefern die beiden terminalen Gleichungen $3t=K+2m$ und $0=B+2m^2+2v^2-3t^2$. Wegen $t>c,d$ ist genau das folgende Vorzeichen zulässig.

$$
r=\sqrt{\tfrac32(K^2-B)-3v^2},\qquad m=K-r,\qquad t=K-2r/3.
$$

Bei $D_{18}$ wählt $G_{18}$ die Wurzel mit negativer Ableitung $2O_{18}/w_{18}$. Daraus werden $b$ und $w_{18}$ eingeschlossen. $G_{20}$ begrenzt $w_{21}$. Bei Zukunft über 14 liefern $D_{14},G_{14},G_{22}$ einen zweiten Einschluss desselben Gewichts. $G_{19}$ und $G_{16}$ begrenzen $w_{19}$ und $w_{16}$. Eine notwendige Restgleichung ist $G_{15}=0$. Die betreffenden eingehenden und ausgehenden Zeilen stehen in modellkontrolle.py.

**Abdeckung.** Durchsucht wird das ganze geschlossene Rechteck aus dem zulässigen $a$-Bereich und dem ursprünglichen Sondenfenster für $z$. Die übrigen Variablen werden durch nach aussen gerundete Intervallrechnung eingeschlossen. Beide Hälften jeder Teilung enthalten den gemeinsamen Rand. Ein unentschiedener Nenner führt je nach Zeile zu weiterer Teilung oder zu einer weiteren Gewichtshülle. Ein Ressourcenlimit erzeugt ausdrücklich einen offenen Bereich. Nur ein widersprüchliches notwendiges Intervall, ein unmögliches striktes Vorzeichen oder eine vollständig negative Diskriminante schliesst eine Box aus.

## Reproduktion

Nach dem Entpacken im Paketverzeichnis mit Python ab 3.10 ausführen. Alle Rechnungen verwenden ausschliesslich die Standardbibliothek.

```sh
sha256sum -c SHA256SUMS
python3 -B pruefen.py
python3 -B gegenprobe.py
```

Der Hauptlauf reproduziert Ergebnisse.json und das Register aller 50 Kombinationen byteweise. Die Gegenprobe prüft die arithmetischen Grenzen anhand exakter Brüche, spielt die Zeugen und früheren Ausschlüsse aus dem SHA-256-gebundenen Vorgängerpaket nach und lässt alle vier Lösungsboxen durch die neue Reduktion laufen, wenn die Kontaktforderung entfällt. Für das erweiterte Fenster variiert sie Teilungsverhältnis und Achsenauswahl. Sie bestätigt die Abdeckung mit insgesamt 6 017 anderen Endboxen. Beide Abdeckungen verwenden dieselben notwendigen Gleichungen. Pruefplan.md dokumentiert die ursprüngliche Kontaktfrage. Die zusätzliche Abstandsweite wurde nach dem Primärlauf gewählt. Es gab keine externe Blindregistrierung.

Die 25 Ordnungen gehen auf die Vorauswahl mit festgehaltenen alten N22-Feldern zurück. Für weitere Nachfolgermengen ist deshalb zuerst zu prüfen, welche damaligen Ausschlüsse auch bei freien Innenfeldern gelten. Eine physische Randfläche oder Masseneichung folgt aus dem Zeitabstand nicht. Acht physische Pilotradien und 60 P3-Prüfpunkte stehen weiter auf NOT_RUN. [Archivierter Merge-Commit](https://github.com/thomasmgfeller/x6-spectral-astrolabium/commit/caf68f68454809c9b7e464eb681623f8afff530f)
