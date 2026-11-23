# CST-DUST · Ein Dichtezeiger an Ereignis 11

**23. November 2026 · Endliche Referenzordnung 2097151 · Markierte Dosis 1**

Der vorige Test erhielt die relative Phase $x/304$ unter der Annahme zweier Zugriffe auf dieselbe Feinhistorie, mit $x=w_{11}/D$. Die gewöhnliche zeitliche Verklebung liefert keinen solchen Doppelzugriff. Wir haben einen einfacheren bedingten Eingriff gefunden. Bei der Verarbeitung von Ereignis 11 werden ausschliesslich zwei bereits mitgeführte Uhrargumente für diesen einen Wirkungsschritt verändert. Aus den originalen Paartermen entstehen dabei in den zwei Zeigerarmen exakt die Zusatzphasen $+x/608$ und $-x/608$. Zur Einstellung genügen die vorherigen Uhren 3 und 4 sowie die vorbereitete Dauer. Die Dichte an 11 und die spätere Uhr 12 werden nicht zur Einstellung benutzt.

| Frage | Ergebnis |
|---|---|
| Verdoppelt die gewöhnliche Verklebung eine abgefragte Wirkungsphase? | Jeder der 50 aktiven Paarterme gehört seinem Zielereignis genau einmal. Das stimmt für alle 91 Zerlegungen in drei nichtleere Zeitabschnitte. |
| Funktioniert der lokale Eingriff im ganzen ursprünglichen positiven Fenster? | Ja. Die grössere der beiden Uhrverschiebungen ist in den verwendeten Y-Einheiten kleiner als 0,010744. |
| Lässt sich das Ergebnis nach dem Schliessen der Dichte aus der gewöhnlichen Randamplitude zurückgewinnen? | Für beliebige zulässige komplexe linke Testwellen ist diese Rekonstruktion ausgeschlossen. Der Gegenzeuge gilt gleichzeitig für alle Werte der späteren Uhr 12. |
| Misst der bekannte Skalarsektor die Dichte von sich aus? | Im festen Typ bei faktorisierter Anfangspräparation bleibt der masselose Skalarfaktor unabhängig von der Staubdichte. |
| Welchen Modellwert hat das neue Bit? | Rund 50,02056 % Wahrscheinlichkeit für „+“ im ursprünglichen positiven Referenzmass. Das ist eine Ausgangswahrscheinlichkeit bei Dosis 1. |
| Stand von P3 | Ein physisch steuerbarer Eingriff, der frühe Speicher unter der physikalischen Randpaarung und die unabhängige positive Masseneichung sind offen. Alle 60 Quellzeilen stehen auf `NOT_RUN`. |

## Nachrechnen

Im entpackten Ordner genügen für die Quellen-, Algebra-, Intervall- und Gegenzeugenprüfung Python ab Version 3.10 und die Standardbibliothek. Die zweite Rechnung mit den Originalfenstern benötigt zusätzlich NumPy.

```sh
sha256sum -c SHA256SUMS
python3 -B pruefen.py
OPENBLAS_NUM_THREADS=1 python3 -B zeigerquadratur.py
```

Die technische Herleitung steht in HERLEITUNG.md. exakt.json und quadratur.json enthalten die Rechenergebnisse. quellen/herkunft.json dokumentiert die eingefrorenen Git-Pfade und Prüfsummen. Die drei Prüfpläne dokumentieren die Reihenfolge des lokalen Hauptversuchs und der Ergänzungen. Die Hashes besitzen keinen unabhängigen Zeitstempel.

[Ausgangsstudie zu den vier Uhrstellungen](https://github.com/thomasmgfeller/x6-spectral-astrolabium/pull/361) · [Schnitttransport und offenes Dichtefenster](https://github.com/thomasmgfeller/x6-spectral-astrolabium/pull/360)
