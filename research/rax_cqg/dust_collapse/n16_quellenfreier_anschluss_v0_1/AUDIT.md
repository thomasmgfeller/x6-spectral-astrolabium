# Unabhängige Prüfung der N16-Anschlüsse

Die zwei vorzeichenreinen Pakete stammen aus N15-Typ 375841. Die neue Uhr ist bei allen Anschlüssen relativ zur festen Uhr am alten Zukunftskragen präpariert, $Y_n=Y_7+4=6$. Das neue Dichtefenster hat dieselbe Mitte $1/8$ und Halbbreite $2^{-20}$ wie das geschlossene alte Fenster. Der Referenzwinkel des Binäreffekts wird je Geometrie aus dem gemeinsamen neutralen Uhrmittelpunkt berechnet.

| Vorgängermenge für das neue Ereignis | Kopplung an die frühere Uhr 6 | Zusatz zum Anfangsstrom am Paketzentrum | Differenz der Ausgangswahrscheinlichkeiten an den Paketzentren |
|---|---:|---:|---:|
| Eingangskette und Ereignis 6 | $1$ | $41v/(76\Delta)$ | $-1{,}5704877205115292\cdot10^{-12}$ |
| Eingangskette und vollständige Viererkette | $-8$ | $0$ | $+1{,}2563901764092233\cdot10^{-11}$ |
| Gesamtes altes Poset | $0$ | $0$ | $0$ |

Der Strom ist die negative Ableitung der Wirkung nach einer gemeinsamen Verschiebung der vier Eingangsuhrwerte in physikalischen Einheiten. Im kurzen Ideal lauten die drei neuen Eingangskoeffizienten an den Ereignissen 1, 2 und 3 der Reihe nach $-8,16,-9$. Am Paketzentrum ist der gemeinsame Zusatz positiv und viel grösser als der Betrag des ursprünglichen Stroms $1099/3187671040$. Beim Anschluss über die ganze Viererkette verschwindet jeder neue Eingangsterm für alle Feldbelegungen. Für diese Geometrie stimmen der alte und der neu aus der Wirkung berechnete Anfangsstrom exakt überein.

Die alte Ordnung wird aus den beiden Ketten und den Kragen neu aufgebaut. Ein Durchlauf über alle $2^{15}$ Teilmengen liefert 28 Ideale. In 16 Idealen trifft die Wirkungsvariation der neuen Dichte die alte Uhr 6. Zehn dieser Ideale haben gleichzeitig keinen neuen Eingangsterm. Die Rechnung transportiert alle markierten Daten durch sämtliche linearen Erweiterungen der drei fertigen Ordnungen. Die Anzahlen sind 364, 196 und 35. In jeder Ordnung gibt es 35 Erweiterungen, in denen das neue Ereignis zuletzt geboren wird.

Die Direktquadratur summiert die vollständige Staubphase kohärent über die gemeinsame Dichte des alten Eingangskragens und über die alte Dichte $w_7$. Am neuen Port werden in den beiden Fensterhälften jeweils die Amplituden für ein zusammengehörendes Wertepaar ausgewertet. Der Ausgang enthält den Kreuzterm $\mathrm{Im}(\bar A_{\mathrm L} e^{-ihD_*} A_{\mathrm H})$. An drei Belegungen der übrigen alten Randfelder werden die direkte N16-Phase und die unabhängig auf N15 berechnete verklebte Amplitude bei 60 und 85 Dezimalstellen verglichen. Die Differenzen liegen an allen geprüften Punkten unter $10^{-48}$. Die Quadratur prüft die Zentren der schmalen Präparationszellen. Die Einschliessung der ganzen Zellen benötigt einen eigenen Fehlernachweis.

Bei den beiden ersten Anschlüssen ist das neue Ereignis zu allen vier Ereignissen des alten Zukunftskragens unvergleichbar. Der gemeinsame markierte Port misst eine lokale Erweiterung mit zwei maximalen Ereignissen. Beim Vollideal liegt der Port über dem gesamten alten Kragen. Die Rechnung verwendet drei feste Ordnungen mit derselben Ausleseregel und eigens bestimmtem neutralem Referenzwinkel je Ordnung.

Zum Nachrechnen erfordert die Quadratur mpmath und Python ab 3.9. Im Studienordner reproduziert `python3 -B gegenprobe.py` die Datei `gegenprobe.json` mit mpmath 1.3.0.
