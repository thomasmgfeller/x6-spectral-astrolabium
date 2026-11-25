# Welche Information über den Staubstrom bleibt am Zukunftsrand erhalten?

**CST-DUST · Teilartikel, erster Manuskriptentwurf · 20. November 2026**

## Zusammenfassung

Wir prüfen an einer endlichen Kausalordnung, ob die Vorzeichenauswahl des aus der Wirkung abgeleiteten Staubstroms auf den Zustandsraum eines geöffneten Zukunftsrands übertragen werden kann. Auf dem N15-Typ 375841 konstruieren wir zwei Pakete von Feinhistorien mit positivem Integrationsmass. Sie haben entgegengesetzte Stromvorzeichen, aber punktweise dieselbe Wirkung, dieselbe skalare Ausgangsfunktion und dieselbe Randamplitude für jede zugelassene Zukunftsbelegung. Die Differenz ihrer Indikatorfunktionen besitzt daher Randnorm null. Die Selektion des positiven Stroms gibt ihr positive Randnorm.

Das Ergebnis gilt für die angegebene endliche Wirkung, das geerbte Hilfsmass und einen benannten linearen Testraum. Es stellt ein Hindernis für einen scharfen Vorzeichenrecord auf diesem Rand dar. Die zusätzliche Annahme einer experimentellen Präparierbarkeit der zwei Pakete wird für den mathematischen Test nicht benötigt. Die physikalische Paarung des vollständigen gekoppelten Systems bleibt offen.

## 1. Ausgangslage und untersuchter Rand

In der publizierten N15-Studie tragen 453 Endtypen zum Zwei-Eltern-Ensemble bei. Die skalare Randfunktion eines festen Typs $c$ ist ein von null verschiedener Vektor $\phi_c\in H_3=L^2(\mathbb R^3)$. Jedes vorzeichenselektierte Staubintegral multipliziert dieselbe Funktion $\phi_c$. Die bisherigen Ensemblewahrscheinlichkeiten setzen eine orthogonale Registrierung am Rand voraus. Grundlage für den vorliegenden Test sind die Daten und die Wirkungsdefinition auf dem Stand von PR #337. [Ensemblestudie][ensemble] · [Intervallprüfung][intervalle]

Hier sind $M=1/4$ die markierte Masse und $r=1/8$ das Anfangsdichtezentrum. Ordnung, Skalarpräparation, Eingangspaket und die Enduhr der Synchronisation $Y_7=2$ bleiben fest. Gegenüber der bisherigen Auslese öffnen wir sieben Zukunftsrandkoordinaten: drei spätere Uhren $Y_8,Y_9,Y_{10}$ sowie die positiven Dichten $w_7,\ldots,w_{10}$. Die resultierende positive Paarung ist ein ausdrücklich gewählter endlicher Prüfkandidat. [Wirkung und Verklebung][wirkung] · [Physischer Stand der Constraints][etappen]

| Prüffrage | Ergebnis auf der konstruierten Zweipaketspanne |
|:---|:---|
| Tragen beide Vorzeichen? | Je ein ganzer Bereich positiver Hilfsmasse trägt strikt eines der Vorzeichen. |
| Welche Information erreicht den Rand? | Beide Paketbilder sind identisch und haben positive Norm. |
| Steigt die Vorzeichenselektion ab? | Ein expliziter Nullvektor verletzt die notwendige Abstiegsbedingung. |

<div class="pagebreak"></div>

## 2. Konstruktion der beiden Feinhistorienpakete

Die gerichtete Staubwirkung benutzt am späteren Endpunkt $v$ die Dichte $w_v$. Mit den Uhren $Y=T/\Delta$, $\Delta^4=3/722$, und dem Intervallkoeffizienten $b_{iv}=1,-9,16,-8$ für null bis drei Zwischenereignisse, sonst null, lautet ihr dimensionsloser Beitrag
$$
 S_d=-\tfrac12\sum_v w_v C_v,\qquad
 C_v=1+\tfrac1{19}\sum_{i\prec v} b_{iv}(Y_v-Y_i)^2 .
$$
Die Gravitation ist bei fester Ordnung konstant. Die skalare Wirkung ist unabhängig von den Staubdichten. Für die gemeinsame Verschiebung der vier Anfangsuhren bei festgehaltenen übrigen Feldern ist $p=-\partial_\tau S_d$. Setze $e=\delta/\Delta$, $D_T=\Delta(4-e)$ und $x_v=w_v/(M D_T)$ auf den sieben inneren Ereignissen. Für diese Ordnung verschwinden sämtliche direkten Anfangs-Zukunfts-Koeffizienten. Daraus ergibt sich
$$
 \frac{p}{M}=\sum_{v\in I}k_v x_v,\qquad
 k_v=\frac{4-e}{19}\sum_{i\in P} b_{iv}(Y_i-Y_v).
$$
Die normierten inneren Uhren $u_v$ bestimmen $Y_v=-2+e+(4-e)u_v$. Die positive Verweildichte $f_v(u)$ ist das Mittel der Zellenlängen auf den maximalen Staubpfaden. Die Präparation erlaubt eine relative Halbbreite von 1 % um $f_v$. [Präparation und Stromableitung][ensemble]

Am Prüfpunkt $e=-1/4$ sind die Uhrenzentren, geordnet nach $I=(4,5,6,11,12,13,14)$, gleich $(1,2,1,2,3,4,3)/5$. Wir verschieben nur die drei Dichten auf den Knoten $5,12,13$. In dieser Reihenfolge gilt
$$
 (C_5,C_{12},C_{13})=(-2187,4253,2109)/7600 .
$$
Wähle $d=(7600/8\,000\,000)(C_{12}-C_{13},\,C_{13}-C_5,\,C_5-C_{12})$ auf diesen Knoten und setze die übrigen Komponenten auf null. Dann gelten $\sum_v d_v=0$ und $\sum_v C_vd_v=0$ **für alle** beteiligten Uhrwerte. Im Zentrum ergibt sich $d=(268,537,-805)/10^6$. Die Ladung ändert sich entlang dieser Richtung. Die Determinante der drei Zeilen $(1,1,1)$, $C$ und $k$ auf den drei Achsen beträgt im Zentrum $1217081/180500$.

| Normierte Dichten im Zentrum | $p/M$ exakt | Gesamte zugehörige Testzelle |
|:---|---:|:---|
| $f-d$ | $1429581/190000000$ | $0{,}0074<p/M<0{,}0077$ |
| $f+d$ | $-1004581/190000000$ | $-0{,}0054<p/M<-0{,}0051$ |

Für die zwei Zellen variiert $e$ um $-1/4$, jede der sieben Uhren um ihr Zentrum und jede der sieben Dichtekoordinaten $\xi_v$ um null, jeweils mit Halbbreite $10^{-7}$. Wir setzen $x=f(u)\mp d(e,u)+\xi$. Beide offenen Zellen liegen strikt in den ursprünglichen Präparationsbändern. Die Intervallschranken in der Tabelle gelten auf den ganzen Zellen. Die gemeinsame Eingangsdichte darf ihr ursprüngliches Band $[3/32,5/32]$ durchlaufen.

<div class="pagebreak"></div>

## 3. Der Zukunftsrand und seine Nullrichtung

Seien $P_+,P_-$ die eben konstruierten Zellen und $\chi_+,\chi_-$ ihre reellen Indikatorfunktionen. Die feine Testklasse ist $V=\mathrm{span}_{\mathbb C}\{\chi_+,\chi_-\}$. Als Ausgabekoordinate $z$ variieren wir die sieben Zukunftswerte mit Halbbreite $\eta=2^{-20}$ um $z_0=(3,4,5,1/8,1/8,1/8,1/8)$. Die Eintrittsuhr des Zukunftskragens $Y_7=2$ legt die Verweildauer fest. Die anderen Zukunftsvariablen ändern die Präparationsbänder der alten Dichten nicht.

Der Randoperator $F_Z$ benutzt die geerbte kohärente Integration über die früheren Variablen, mit flachem Dichtemass auf dem positiven Zweig. Die Referenzpaarung entsteht durch Identifikation derselben Zukunftswerte in Amplitude und konjugierter Amplitude:
$$
 (F_Z h)(z)= e^{iF_4(c)}\phi_c\int h\,e^{iS_d(z)}\,d\mu_{\mathrm{alt}},
 \qquad
 D_Z(h,g)=\int_Z\langle F_Z h(z),F_Z g(z)\rangle_{H_3}\,d\nu(z).
$$
Hier ist $\nu$ das normierte flache Mass der Zukunftsbox. Die Konstruktion liefert eine positive semidefinite Form. Die Wahl dieses Randmasses ist eine zusätzliche Annahme. Die Herleitung der physikalischen Constraints und der daraus folgenden Paarung ist ein eigener Schritt. Die Quotientenkonstruktion aus einer positiven Historienpaarung liefert den mathematischen Rahmen. [Dowker, Johnston und Sorkin][history]

**Beweis.** Bei denselben $e,u,\xi$ unterscheiden sich die inneren Dichten der zwei Pakete um $2M D_T d$. Der Unterschied ihrer Staubwirkungen ist bis auf Orientierung $M D_T\, C\!\cdot d=0$. Da alle drei geänderten Dichten an inneren Zielen sitzen, sind ihre $C_v$ unabhängig von sämtlichen späteren Uhren und Dichten. Somit gilt die Identität für jedes $z\in Z$. Bei festem $e,u$ ist der Übergang zwischen den Paketen eine Translation mit Jacobi-Determinante eins. Der gemeinsame Faktor $(M D_T)^7$ der normierten Dichten ist derselbe. Die skalaren und gravitativen Faktoren stimmen ebenfalls überein.

Zum Nachweis des positiven Betrags wird die Staubphase eingeschlossen. Am ursprünglichen Zukunftswert liegt sie zwischen $-0{,}765$ und $-0{,}356$ rad. Auf $Z$ beträgt die zusätzliche Phasenänderung weniger als $0{,}01$ rad. Dies folgt aus höchstens 105 geordneten Paaren, $|b_{iv}|\leq16$, $|Y_i|\leq6$ und $0<w_i<1$. Für jedes Paar gilt $|\Delta(w_v(Y_v-Y_i)^2)|\leq192\eta$. Der Realteil von $\exp(iS_d)$ übersteigt damit auf beiden Zellen $0{,}69$. Beide Zellen haben positives Hilfsmass. Folglich ist $F_Z\chi_+=F_Z\chi_-=v\ne0$ auf der gesamten Zukunftsbox.

Die Gram-Matrix folgt analytisch aus dieser Bildgleichheit. Auf $V$ gilt mit $\gamma=\|v\|^2>0$ die Matrix
$$
 [D_Z]=\gamma\begin{pmatrix}1&1\\1&1\end{pmatrix}.
$$
Die Differenz $n=\chi_+-\chi_-$ liegt im Kern. Der positive Stromselektor erfüllt $S_+ n=\chi_+$ und damit $D_Z(S_+n,S_+n)=\gamma$. Er erhält den Kern nicht und ist auf dem Quotienten dieses Kandidaten nicht wohldefiniert.

<div class="pagebreak"></div>

## 4. Anschluss an die Verklebung und unabhängige Kontrolle

**Reichweite der Wirkungsgleichheit.** Wird der alte Block als nach unten abgeschlossene Teilordnung fortgesetzt, bleiben die alten Intervalle und die $C_v$ an den veränderten Knoten erhalten. Jeder neu hinzukommende Wirkungsterm trägt die Dichte seines neuen Ziels. Alte Uhren und Skalarfelder sind im gepaarten Vergleich gleich. Daher gilt die Wirkungsgleichheit auch für solche Fortsetzungen. Eine auf den gemeinsamen Ausgang wirkende lineare Weiterverarbeitung erhält die Bildgleichheit. Das Hindernis bleibt für jeden solchen Anschluss bestehen, der dem gemeinsamen Bild positive Norm gibt. Eine neue Kopplung an alte Dichten, eine Änderung der inneren Ordnung, andere dichteabhängige Gewichte oder zusätzliche physikalische Constraints benötigen eine eigene Prüfung. Die publizierte Verklebungsidentität auf 1 089 Paaren und die zwei kleinen Fortsetzungsproben hier erfüllen unterschiedliche Zwecke. [Herleitung der Kreuzwirkung][wirkung]

**Was verrät das Anfangsuhrfenster?** Eine zweite Kontrolle behält als zusätzliches Register nur das linke oder rechte ursprüngliche Uhrfenster. Innerhalb jedes Fensters wird kohärent integriert. Auf dem gesamten rechten Fenster gilt für alle inneren Felder $0{,}005175<p/M<0{,}393$. Auf dem linken Fenster tragen zwei innere Uhrprofile durchgehend strikt entgegengesetzte Vorzeichen. Für die ursprüngliche Präparation beträgt die gemeinsame Staubphasenspanne weniger als $0{,}409$ rad. Die drei besetzten Fenster-Vorzeichen-Kanäle sind daher alle ungleich null.

Auf der **anderen** Testklasse mit je einem konstanten Koeffizienten für die beiden ganzen Vorzeichenzweige lautet die Abbildung in die Fensterbasis
$$
 F_{\mathrm{Fenster}}=
 \begin{pmatrix}L_-&L_+\\0&R_+\end{pmatrix}.
$$
Sie hat Rang zwei. Die Vorzeichenselektion ist hier algebraisch wohldefiniert. Bei jeder strikt positiven diagonalen Fensterpaarung gilt jedoch $\operatorname{Re}(\overline{L_-}L_+)>0$ nach Ausklammern gemeinsamer Faktoren. Damit ist der übertragene Selektor kein orthogonaler Projektor. Das rechte Fenster identifiziert ein positives Vorzeichen, während das linke beide zulässt. Eine nichtdiagonale hermitesche Paarung $W$ müsste für einen perfekten Record die prüfbare Gleichung $W_{LL}L_+ + W_{LR}R_+=0$ aus einer unabhängigen Randdynamik erfüllen.

**Der nächste unterscheidende Kanal.** Beide Pakete haben dieselbe Wirkung am unverschobenen Rand. Verschiebt man die *Anfangs*uhren als unabhängige Quelle und hält jede der zwei Feldbelegungen fest, sind die Steigungen verschieden. Die Ladungsdifferenz am Zentrum beträgt exakt $1217081/380000000$. Eine Kopplung an eine solche Quellantwort ist ein konkreter Kandidat für ein Instrument. Um einen physischen Record zu begründen, müsste der minimale gekoppelte Randzustand nach der Verklebung zwei unterscheidbare Ausgänge tragen. Dafür wären das Instrument, ein gemeinsames positives Skalarprodukt und dieselben Eingangsbedingungen vor der Auswertung festzulegen. Eine blosse Wahl zweier Sektornormen kann den hier nachgewiesenen Informationsverlust nicht beheben. [Quellvertrag][quelle]

## Reproduzierbarkeit und Status

Der Prüfer benötigt nur die Python-Standardbibliothek. Er verwendet rationale Arithmetik für die Vorzeichen, die Bandgrenzen und die Wirkungskontrollen. Zwei direkte Wirkungsauswertungen pro Beispiel wurden auf Ordnungen mit 15, 16 und 17 Ereignissen verglichen. Die zwei grösseren Ordnungen prüfen die Wirkung bei Anhängen zukünftiger Ereignisse. Das sind keine neuen dynamischen Kollapsdaten. Die Rechnung wurde nach Kenntnis der N15-Ergebnisse entwickelt. Etappe 6 bleibt offen. Alle 60 physischen P3-Datensätze stehen weiter auf **NOT_RUN**. [P3-Vertrag][p3]

[ensemble]: https://github.com/thomasmgfeller/x6-spectral-astrolabium/blob/d7de6876f571ece2dca8030f30d8fdda839b8404/research/rax_cqg/dust_collapse/joint_charge_distribution_v0_1/README.md
[intervalle]: https://github.com/thomasmgfeller/x6-spectral-astrolabium/blob/d7de6876f571ece2dca8030f30d8fdda839b8404/research/rax_cqg/dust_collapse/n15_charge_interval_record_v0_1/README.md
[wirkung]: https://github.com/thomasmgfeller/x6-spectral-astrolabium/blob/d7de6876f571ece2dca8030f30d8fdda839b8404/research/rax_cqg/dust_collapse/extended_sewing_v0_1/DERIVATION.tex
[etappen]: https://github.com/thomasmgfeller/x6-spectral-astrolabium/blob/d7de6876f571ece2dca8030f30d8fdda839b8404/research/rax_cqg/dust_collapse/stage_reviews_4_7/README.md
[quelle]: https://github.com/thomasmgfeller/x6-spectral-astrolabium/blob/d7de6876f571ece2dca8030f30d8fdda839b8404/research/rax_cqg/dust_collapse/boundary_mass_sector_v0_1/README.md
[history]: https://arxiv.org/abs/1002.0589
[p3]: https://github.com/thomasmgfeller/x6-spectral-astrolabium/blob/d7de6876f571ece2dca8030f30d8fdda839b8404/research/rax_cqg/dust_collapse/correspondence_v0_1/plan.json
