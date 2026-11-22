# Numerische Gegenrechnung am Zentrum von Typ 42429

Die ursprünglichen vier Wege zwischen Eingang und Zukunftsrand erzeugen die Hasse-Kanten. Von jeder Ecke bestimmt eine Erreichbarkeitssuche die transitive Ordnung. Die Einschränkung auf die alten 15 Ereignisse stimmt exakt mit der veröffentlichten Bitkodierung des Typs überein. Ereignis 15 folgt auf den Eingang und die Kette (4,5,11,12). Ereignis 16 ist die gemeinsame Zukunft aller alten Knoten. Die Gewichte der Materiephase folgen durch Zählen aller Zwischenereignisse.

Die beiden Uhrprofile verschieben $u_{11}$ um $-1/128$ beziehungsweise $+1/128$. Ihre Verweilanteile werden entlang aller vier gleich gewichteten Wege aus den Mittelpunktzellen berechnet. Die Kontrolle mit dem ursprünglichen N15-Zeugen ergibt bei der markierten Masse $1/4$ die Ströme $1863/622592$ und $-327/622592$. Die normierten Dichteintegrale bei festgehaltenen Uhren werden analytisch ausgewertet. Die drei alten äusseren Uhren, das neue Uhrfenster und jede Hälfte des letzten Dichtefensters werden direkt per Gauss–Legendre integriert. Der Scharfarm setzt die vorletzte Uhr auf 6. Bei der Zeitmischung werden die unnormierten Intensitäten gemittelt, im kohärenten Arm die Amplituden. In allen drei Armen erfolgt eine einzige Normalisierung nach der jeweiligen Integration.

| Auslese auf den beiden Zentren | Wahrscheinlichkeit für $t>1/8$ beim positiven Paket abzüglich jener beim negativen |
|---|---:|
| Scharfe Uhr | $+3{,}63684506438833\times10^{-21}$ |
| Zeitgemisch | $+3{,}63684506438833\times10^{-21}$ |
| Kohärentes Fenster | $+3{,}61044860827584\times10^{-21}$ |
| **Primärkontrast, kohärent abzüglich gemischt** | **$-2{,}63964561124955\times10^{-23}$** |

Die kohärente Integration verkleinert auf diesen Zentren die bereits bei scharfer Uhr erkennbare Differenz. Der numerisch beobachtete Rest zwischen Scharf- und Mischarm beträgt rund $8{,}1\times10^{-87}$ bei 85 Stellen. Die Resultate für den Primärkontrast stimmen bei den zwei festgelegten Auflösungen (Ordnung 3 bei 65 Stellen und Ordnung 4 bei 85 Stellen) in mehr als 29 signifikanten Stellen überein. Diese Quadratur beurteilt Richtung und Grösse an den Zentren. Über die vollständigen Pakete entscheidet gemäss Prüfvertrag die separate Einschliessung.

```sh
python3 -B transfer_quadratur.py > neue_transfer_quadratur.json
```

Erforderlich ist mpmath. Die JSON-Ausgabe enthält sämtliche sechs bedingten Wahrscheinlichkeiten, die zugehörigen integrierten Staubnormen und die Differenzen für beide Auflösungen. Der gemeinsame Skalarfaktor kürzt sich aus den bedingten Wahrscheinlichkeiten heraus.
