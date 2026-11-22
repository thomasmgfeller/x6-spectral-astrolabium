# N17-Kontrollrechnung auf dem bekannten Typ 375841

Die Rechnung betrifft die Zentren der beiden Präparationen auf dem stromerhaltenden Anschluss. Für beide Vorzeichen wird die Wahrscheinlichkeit für dieselbe Enddichtemessung $t>1/8$ ermittelt. Der alte Dichteport bleibt geschlossen. Bei unveränderten Dichtefenstern wird nur die Halbbreite des früheren Uhrfensters verändert.

Für jeden Wert $x$ der früheren Uhrverschiebung summiert das Programm zuerst alle übrigen Amplituden zur bedingten Funktion $A_s(t,x)$. Gauss–Legendre-Knoten und Gewichte der alten Uhr sind in beiden Armen identisch. Die kohärente Auslese benutzt $|\int A_s(t,x)\,d\mu(x)|^2$, die dephasierte Auslese $\int |A_s(t,x)|^2\,d\mu(x)$. Erst danach wird das Integral über die obere Hälfte durch das gesamte Endintegral des jeweiligen Arms und Vorzeichens geteilt. Die ausgegebenen Normen enthalten den gemeinsamen Skalarfaktor nicht.

| Halbbreite der früheren Uhr | Kohärente Differenz, Originalpaar | Kohärente Differenz, halbe Eingangsvariation |
|---|---:|---:|
| $h/2$ | $-8{,}4279873\times 10^{-28}$ | $-4{,}2139936\times 10^{-28}$ |
| $h=2^{-20}$ | $-3{,}3711949\times 10^{-27}$ | $-1{,}6855975\times 10^{-27}$ |
| $2h$ | $-1{,}3484780\times 10^{-26}$ | $-6{,}7423898\times 10^{-27}$ |

Bei 85 Dezimalstellen beträgt der grösste beobachtete Absolutrest der dephasierten Differenz über beide Vorzeichenpaare und alle vier Halbbreiten einschliesslich null weniger als $8{,}05\times 10^{-87}$. Dieser Rest beschreibt eine numerische Gegenprobe. Die tabellierten Quadraturwerte sind Näherungen an den Paketzentren. Eine analytische Einschliessung mit endlichen Paketbreiten ist gesondert auszuweisen.

Die unabhängige Auswertung rekonstruiert die Intervallgewichte aus der Kausalordnung, benutzt die eingefrorene Paketfamilie aus der Vorgängerstudie und integriert die Staubphase direkt. Als Auflösungsprüfung dienen die Quadraturordnungen 3 und 4 pro Achse mit 65 und 85 Dezimalstellen. Die Differenzen beider Auflösungen sind in allen 16 Armvergleichen kleiner als $10^{-48}$. Die dritte Breite bestätigt auf diesen Zentren die vorhergesagte nahezu quadratische Breitenantwort.

```sh
python3 -B quadratur.py > neue_quadratur.json
```

Die Auswertung benötigt mpmath und SymPy. Die Reihenfolge der Zeile in jeder JSON-Liste entspricht der Reihenfolge der Uhrhalbbreiten $0,h/2,h,2h$. Beide Eingangspräparationen, ihre Normen sowie die beiden Rechenstufen lassen sich einzeln vergleichen.
