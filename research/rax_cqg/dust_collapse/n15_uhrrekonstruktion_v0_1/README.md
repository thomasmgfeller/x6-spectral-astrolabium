# Lassen sich die inneren Uhren und der Anfangsstrom aus Rand- und Schnittantworten rekonstruieren?

**CST-DUST · N15, Typ 375841 · 21. November 2026**

Die Rückrechnung des Anfangsstroms benötigt auf dieser Ordnung kein vorgegebenes inneres Uhrprofil mehr. Drei Uhrantworten und zwei Dichteantworten am geöffneten Zukunftsrand bestimmen zusammen mit den beiden Schnittuhren alle fünf verborgenen Uhrwerte. Ein zweiter Weg gewinnt den Strom ausschliesslich aus Uhrvariationen an Eingang, Schnitt und Zukunft. Dabei entfallen sowohl die Rekonstruktion von $Y_6$ als auch der erste Schnittimpuls bei Ereignis 11. Beide Verfahren lieferten bei 216 rationalen Feldbelegungen exakt die verdeckte Anfangsladung.

Ein neues Gegenpaar zeigt die Grenze. Seine Anfangsströme haben entgegengesetzte Vorzeichen, obwohl die sichtbaren Felder, die innere Dichtesumme und eine ganze Familie endlicher Quellenänderungen dieselbe Antwort ergeben. Jeder der beiden Wege enthält eine zusätzliche Quelle, die dieses Paar unterscheidet. Der Befund betrifft die Wirkung einzelner Feinhistorien in der publizierten endlichen Präparation. [Ausgangspunkt, PR #343](https://github.com/thomasmgfeller/x6-spectral-astrolabium/pull/343) · [Bisherige Schnittinversion, PR #342](https://github.com/thomasmgfeller/x6-spectral-astrolabium/pull/342)

## Welche Informationen in die Rekonstruktion eingehen

Wir verwenden $Y=T/\Delta$, $W=w/\Delta$, $\Delta^4=3/722$ und die Staubwirkung $\widehat S=S_d/\Delta$. Ihre Uhrantworten sind $E_j=\partial_{Y_j}\widehat S$, $H_j=\partial_{Y_j}^2\widehat S$. Eine Dichteantwort ist $D_j=\partial_{W_j}\widehat S$. Wie in den Vorarbeiten werden nur die Quellenargumente der Wirkung variiert. Alle übrigen Felder, Gewichte und Integrationsfenster sind fest. Die erste gemeinsame Verschiebung der Eingangskette definiert $p_P$ und wird erst zur Bewertung der Vorhersage ausgewertet.

Sichtbar sind die vier Eingangsuhren, die Uhren und Dichten bei 5 und 11 auf dem Zwischenschnitt sowie die Uhren und Dichten des Zukunftsrands $F=(7,8,9,10)$. $Y_7=2$ bleibt als Synchronisationsuhr fest. Eine Variation von $W_7$ ist im ursprünglichen geöffneten Zukunftsrand zugelassen. Die fünf verborgenen Uhren sind $Y_4,Y_6,Y_{12},Y_{13},Y_{14}$. [Veröffentlichte Definition des Zukunftsrands](https://github.com/thomasmgfeller/x6-spectral-astrolabium/blob/44674654c4dc8a8f10f8a1f2d2186e3b49758776/research/rax_cqg/dust_collapse/n15_future_boundary_v0_1/Teilartikel.md)

| Benötigte Quellenantwort | Weg A für den Strom | Weg B für den Strom |
|---|---|---|
| Drei freie Zukunftsuhren | $E_8,E_9,E_{10}$ | $E_8,E_9,E_{10}$ |
| Zukunftsdichten | $D_7,D_{10}$ | keine |
| Schnittuhren | $E_5,E_{11},H_{11}$ | $E_5,H_5,H_{11}$ |
| Eingangskrümmungen | tatsächliche innere Dichtesumme aus PR #343 | dieselbe Summe und die Summe $W_4+W_6$ |

### Weg A. Fünf verborgene Uhren aus Zukunftsantworten bestimmen

Die inneren Ketten sind $4\prec5\prec14$ und $6\prec11\prec12\prec13$. Gruppiert man die inneren Ereignisse nach der Anzahl $s$ ihrer inneren Nachfolger, erhält man

| $s$ | Ereignisse | Summe der Uhren $U_s$ |
|---:|---|---|
| 0 | 13, 14 | $Y_{13}+Y_{14}$ |
| 1 | 5, 12 | $Y_5+Y_{12}$ |
| 2 | 4, 11 | $Y_4+Y_{11}$ |
| 3 | 6 | $Y_6$ |

Liegt ein Zukunftsereignis $f$ auf Rang $r=f-7$, hat die Beziehung vom inneren Ereignis der Gruppe $s$ zu $f$ genau $s+r$ Zwischenereignisse. Die Wirkungsgewichte lauten $b(0),\ldots,b(3)=(1,-9,16,-8)$ und verschwinden ab vier Zwischenereignissen. Schreibe $n_s$ für die Zahl der Elemente der Gruppe $s$ und setze $b_{ij}=0$ ausserhalb vorwärts gerichteter Beziehungen. Die korrigierte Uhrantwort

$$
L_f=\frac{19E_f+\sum_{g\in F} b_{fg}W_g(Y_f-Y_g)}{W_f}
-\sum_{g\in F} b_{gf}(Y_g-Y_f)
+Y_f\sum_s b(r+s)n_s
=\sum_s b(r+s) U_s
$$

enthält nur bekannte Randdaten auf der linken Seite. Für $f=10,9,8$ entstehen nacheinander die Zeilen $(-8,0,0)$, $(16,-8,0)$ und $(-9,16,-8)$ für $(U_0,U_1,U_2)$. Das ergibt unmittelbar $Y_{12}=U_1-Y_5$ und $Y_4=U_2-Y_{11}$.

Die Dichte sitzt in der Wirkung jeweils am Ziel der Beziehung. Deshalb liefert eine einzelne Dichteableitung die zweite Uhrpotenz

$$
K_f=-38D_f-19-\sum_{g\in F}b_{gf}(Y_g-Y_f)^2
=\sum_{j\in I} b_{jf}(Y_j-Y_f)^2 .
$$

Bei 10 tragen nur die beiden Endereignisse bei. Setze $d=\sqrt{2K_{10}/(-8)-(U_0-2Y_{10})^2}$. Dann gelten $Y_{13}=(U_0+d)/2$ und $Y_{14}=(U_0-d)/2$. Die Zuordnung folgt aus den getrennten Uhrfenstern um $u_{13}=4/5$ und $u_{14}=3/5$ der ursprünglichen Präparation. Die Ordnung allein vergleicht diese zwei Ereignisse nicht. Für $Y_6$ verbleibt in $K_7$ nach Abzug aller bekannten Beiträge nur $-8(Y_6-Y_7)^2$. Die kausale Uhrordnung legt hier den kleineren Wurzelzweig fest. Im ganzen Uhrfenster gelten $Y_{13}-Y_{14}\ge783/1280$ und $Y_7-Y_6\ge7279/2560$.

Damit rekonstruiert dieser Teil des Verfahrens die fünf inneren Uhren bereits aus den beiden Schnittuhren und dem Zukunftsrand. Für den Strom werden anschliessend die Eingangs- und Schnittquellen der ersten Tabellenspalte eingesetzt. [Ausführbare Inversion](inversion.py)

### Weg B. Den Strom mit reinen Uhrquellen bestimmen

Die Summe $W_{\mathrm{ges}}$ kommt wie in PR #343 aus der gemischten Eingangskrümmung. Dieselbe gleichförmige Verschiebung $u$ der Eingangskette kann mit einer Verschiebung $e_0$ nur des ersten Eingangsereignisses kombiniert werden. Von dort erreicht der Wirkungskoeffizient $-8$ nur die zwei inneren Ziele ohne inneren Vorgänger. Alle Beiträge innerhalb des Eingangs fallen durch die konstante erste Richtung heraus. Folglich gilt

$$
W_{\rm früh}=W_4+W_6=\frac{19}{8}\,\partial_u\partial_{e_0}\widehat S.
$$

Nach Abzug der bekannten Eingangs- und Zukunftsterme liefern die Schnittkrümmungen $H_5$ und $H_{11}$ die Grössen $W_{14}$ und $L=W_{12}-9W_{13}$. Mit $s=W_{\rm ges}-W_{\rm früh}-W_5-W_{11}-W_{14}$ folgt $W_{13}=(s-L)/10$ und $W_{12}=s-W_{13}$. Die drei Zukunftsuhrantworten ergeben wie oben $U_0,Y_4,Y_{12}$. Damit sind am Ereignis 5 alle ankommenden Terme der ersten Uhrableitung und die Beiträge vom Zukunftsrand bekannt. Der verbleibende ausgehende Term ist $J_5=W_{14}(Y_5-Y_{14})$. So erhält man $Y_{14}=Y_5-J_5/W_{14}$ und $Y_{13}=U_0-Y_{14}$. Die positive Dichte im Nenner hat auf dem ursprünglichen Fenster bei $M=1/4$ die Untergrenze $89001/409600$.

Für die Eingangsladung sei $g_j=\sum_{i\in P}b_{ij}(Y_i-Y_j)$. Die beiden frühesten inneren Ziele haben identische Eingangskoeffizienten mit Zeilensumme null. Deshalb ist $g_4=g_6$ unabhängig von beiden Zieluhren, und es gilt

$$
19p_P=g_4W_{\rm früh}+g_5W_5+g_{11}W_{11}+g_{12}W_{12}+g_{13}W_{13}+g_{14}W_{14}.
$$

Die Stromvorhersage kann jetzt abgegeben werden. Erst wenn auch die fünfte verborgene Uhr verlangt ist, wird $E_{11}$ eingesetzt. Ihr einziger noch unbekannter Term ist $W_{11}(Y_6-Y_{11})$, wobei $W_{11}\ge169389/2048000$ im genannten Fenster. Diese Auslese benötigt sowohl am Eingang als auch am Schnitt und am Ausgang ausschliesslich Uhrvariationen.

## Gegenprobe mit entgegengesetztem Strom und gleicher Wirkung

Am neutralen Mittelpunkt der beiden Dichtezweige des Zusatzpaars aus PR #342 sei $q$ eine kleine rationale Verschiebung. Ändere $W_4,W_{12},W_{13}$ um $-10q,9q,q$ und $Y_6$ um $9q(Y_{13}-Y_{12})/W_{11}$. Die sichtbaren Felder und $W_{\rm ges}$ bleiben gleich. In den Schnittantworten kompensiert die Änderung von $Y_6$ bei 11 den geänderten ausgehenden Beitrag. Die frei variierbaren Zukunftsuhren 8, 9 und 10 sind von Ereignis 6 durch mindestens vier Zwischenereignisse getrennt. Ihre Antworten bleiben ebenfalls gleich. Die beiden Vorzeichen von $q$ führen jedoch zu $p_P(q)=-(1099/190)q$. Dieser erste Test benutzt $|q|=2^{-20}$.

Für eine stärkere Kontrolle wurde zusätzlich die unverschobene Wirkung exakt angeglichen. Bei $|q|=2^{-24}$ kann eine weitere Dichtemenge zwischen 6 und 4 übertragen werden, während beide Dichten innerhalb ihrer ursprünglichen 1-%-Bänder bleiben. Schreibe $C_j=1+\sum_{i\prec j} b_{ij}(Y_i-Y_j)^2/19$. Der erforderliche Übertrag auf 4 ist $2(\widehat S_{\rm verschoben}-\widehat S_{\rm neutral})/(C_4-C_6)$ bei den verschobenen Uhren. Er ändert weder $W_{\rm früh}$ noch $p_P$. Die beiden Historien haben jetzt entgegengesetzte Ströme von Betrag $1099/3187671040$ und exakt dieselbe Wirkung.

Mehr noch, die Wirkung bleibt für **beliebige gemeinsame endliche Verschiebungen** der fünf Uhren $(5,11,8,9,10)$ und der drei Dichten $(8,9,10)$ bei beiden Historien identisch. Bei festen Dichten hat die Quellenwirkung in den fünf Uhrverschiebungen Grad höchstens zwei. Ihr Wert an 21 geeignet gewählten Punkten legt alle Koeffizienten fest. Die affine Abhängigkeit von drei Dichteverschiebungen benötigt vier Dichtebelegungen. Alle $21\times4=84$ bestimmenden Werte stimmen in exakter Arithmetik überein. Auch die frühere Summenquelle liefert denselben Wert.

Beide neuen Wege brechen diese Gleichheit. Für $+q$ minus $-q$ ist die Differenz der Dichteantwort $D_7$ exakt $-8789/722206720$. Die zusätzliche Uhrquelle nach Weg B liefert $\delta W_{\rm früh}=-5/4194304$. Auf den zwei einzelnen, gleichphasigen Historien ist damit auch die erste Ableitung ihrer Phasenfaktor-Differenz nach $W_7$ ungleich null, mit Betrag $\Delta|\delta D_7|$. Die Gleichheit des gesamten Quellenpolynoms bezeichnet die fünf genannten Uhr- und drei Dichtevariationen. Die beiden neuen Quellen und Dichtevariationen an den Schnittpunkten gehören nicht zu dieser Gleichheit. [Exakte Gegenproben](pruefen.py) · [Werte und rationale Zertifikate](ergebnis.json)

## Reichweite und Reproduktion

Der vorab lokal festgelegte Test umfasst je 18 Paare aus vier bekannten Paketfamilien und 72 weitere Belegungen der breiteren Präparation. Der Zufallsstartwert ist neu. Beide Verfahren treffen in allen 216 Belegungen den Anfangsstrom exakt, darunter 123 positive und 93 negative. Je Weg ergeben sich mit dem ergänzenden Schritt für $Y_6$ bei Weg B auch alle 1 080 einzelnen verdeckten Uhrwerte exakt. Für acht Zentrumsbelegungen wurden sämtliche Quellenantworten bei erheblich verkleinerten Schrittweiten wiederholt. Erzeugung und Bewertung verwenden die unmittelbar aus den offenen Intervallen aufgebaute Wirkung. Der Vorhersagecode erhält nur die ausgewiesenen sichtbaren Daten und Quellenantworten.

Die Formeln rekonstruieren auf einer festgehaltenen Feinhistorie. Eine kohärente Amplitude summiert die Phasenfaktoren vor der Auswertung. Wurzelziehen, Dividieren und die Klassifikation des Vorzeichens lassen sich im Allgemeinen nicht durch diese Summation hindurchziehen. Für einen physikalischen Vorzeichenrecord bleibt zu prüfen, welcher gemeinsame Randdetektor die voneinander getrennten Quellenantworten auf ganzen Paketen in unterscheidbare Ausgänge überträgt und welche positive Paarung dabei gilt. Das vorliegende Ergebnis trägt zur endlichen Vorzeichenfrage auf Typ 375841 bei. Der 1 048-Typen-Zählwert in PR #343 bezog sich auf die Dichtesumme. Ein Katalogtransfer der Uhrrekonstruktion und die physikalische P3-Korrespondenz bleiben offen.

Im entpackten Studienordner mit Python 3.9 oder neuer ausführen. Es genügt die Standardbibliothek.

```sh
sha256sum -c SHA256SUMS
python3 -B pruefen.py > nachrechnung.json
cmp ergebnis.json nachrechnung.json
```

Die stärkere Gegenprobe mit gleicher Wirkung, die acht Schrittweitenvergleiche und die expliziten Untergrenzen ergänzen den [ursprünglichen Prüfvertrag](pruefvertrag.json). Die zehn übernommenen Quelldateien sind mit den Git-Blob-IDs des veröffentlichten Standes verknüpft. [Quellenstand](quellen.json) · [Lizenz](LICENSE) · [NOTICE](NOTICE)
