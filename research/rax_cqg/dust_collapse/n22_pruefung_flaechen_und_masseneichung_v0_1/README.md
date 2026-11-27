# CST-DUST · Prüfung der Flächen- und Masseneichung

Prüfstand 28. November 2026. Die Eingaben sind unveränderte Dateien aus dem Commit `2c08c72af7fa7d075f50decc48c9531d64d61c66`. Die Zuordnung steht in [input/Herkunft.txt](input/Herkunft.txt). Der Kurzbericht enthält die physikalische Bewertung. Das separat geschriebene Prüfprogramm benötigt Python ab Version 3.10 mit Standardbibliothek.

## Offline nachrechnen

Im entpackten Verzeichnis ausführen.

```sh
sha256sum -c SHA256SUMS
python3 -B pruefen.py > Neuberechnung.json
diff -u Ergebnis.json Neuberechnung.json
```

Die Ergebnisdatei listet auch die Identitäten der kreuzenden Links und aller Ereignisse auf der frühen Seite. Das Programm prüft die Transitivität der strikten Relation, rekonstruiert ihre Überdeckungsrelation und bestimmt für jede Uhrschwelle, dass alle Ereignisse in den rationalen Uhrintervallen eindeutig zugeordnet sind. Bei den Ketten bedeutet ein Schritt eine strikte Vergleichsrelation. Ein Schritt kann mehrere Hasse-Links überspannen. Leere Kettenprofile im Ergebnis bedeuten null Ketten für alle positiven Schrittzahlen.

Die Schwellen 15/32, 1/2 und 17/32 folgen aus den veröffentlichten Fenstergrenzen und ihrem Mittelpunkt. Die Schwelle 129/256 wurde nachträglich gewählt. Sie zeigt, wie ein feldabhängiger Schnitt die Linkzahl verändert. Sie wurde nicht zur Kalibrierung oder als vorregistrierter Test verwendet.

## Zwei Kugeln mit denselben Beobachtungen

Für beide Präparationen prüft das Programm alle 231 ungerichteten Ereignispaare gegen die angegebene Kausalordnung in flachen 3+1 Dimensionen. Grundlage sind die räumlichen Koordinaten und die rational eingeschlossenen normierten Uhrwerte als Zeitkoordinaten dieser Kontrolle. In denselben Koordinaten werden zwei äussere Oberflächen eingesetzt. Sie haben Zentren (0,0,−1) und (0,0,−5/2) und Radien R(t) = r − (t−1/2)/8 mit r = 1 bzw. 2. Jedes positive Feld liegt auf der Innenseite, jedes Nullfeld auf der Aussenseite, auf dem ganzen jeweiligen Zeitintervall. Der Vergleich zweier Grenzen bezieht sich jeweils auf eine festgehaltene Präparation. Eine Lösung der gekoppelten Einstein-Staub-Dynamik oder eine Übertragung der Modelluhr in physische Eigenzeit wird hier nicht vorausgesetzt.

In Einheiten von π sind die beiden Flächen 4 und 16. Ein einziger Schätzwert a, der für beide eine relative Fehlerschranke e einhalten soll, muss insbesondere 16(1−e) ≤ a ≤ 4(1+e) erfüllen. Daraus folgt e ≥ 3/5. Bei a = 32/5 wird die Grenze erreicht. Für die Radien 1 und 2 ergibt sich analog eine Fehlerschranke von mindestens 1/3. Diese Aussagen gelten für die Kontrollklasse, unabhängig von der Rechenpräzision.

## Bedeutung für die vorgeschlagene Kalibrierung

- Eine nominelle Massendifferenz auf einer unveränderten Ordnung erzwingt bei einer festgehaltenen Partition keinen Unterschied in den Kreuzungslinks. Die im Fenster positiven Ereignisse 18 und 19 gehören zu beiden Präparationen. Ein leeres Ereignis ist auch kein Ersatz für eine eigenständig präparierte Vakuumgeschichte.
- Gemeinsame Knoten oder Uhren sind für zwei Messkanäle zulässig. Die physische Bedeutung jedes Kanals muss unabhängig von den zurückgehaltenen P3-Sollwerten geprüft sein. Gemeinsame Unsicherheiten müssen in die Auswertung eingehen. Eine ausschliesslich topologische Masse ist keine Vertragsvoraussetzung.
- Ein positives Referenzpräparat mit bekannter Anfangsmasse samt Unsicherheit und ein Vakuumnullpunkt ermöglichen eine einmalige Eichung einer getrennten Materieladung. Welcher Massenbegriff übertragen wird (Ruhestmasse oder gravitative Masse), ist im gewählten Sektor zu identifizieren. Die klassischen Positivkontrollen beruhen auf einer Lösung mit bekannten Annahmen.
- P3 enthält drei Massen (1/4, 1, 4), fünf Zeiten (0, 1/4, 1/2, 3/4, 1 als Bruchteile derselben Referenzdauer) und vier Zähldichten (1, 2, 4, 8 relativ zur Basis). Die acht Pilotplätze sind darin enthalten. Die 524 geplanten Vergleiche umfassen auch Masse, seitlichen Fluss und Verfeinerung. Die erneute Zählung erzeugt keine physischen Beobachtungen. Die Gründe für HOLD stehen in input/eligibility.json.
