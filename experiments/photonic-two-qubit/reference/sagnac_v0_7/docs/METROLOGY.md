# Messmodell und Auswertung

## Vor der Messung festlegen

Zielzustand: Psi-minus = (HV−VH)/sqrt(2). Gemeinsame Definition von +/−,
Detektorkanälen, Zeitkalibrierung, Fensterbreite, Fensterepoche, Messdauer,
Analysatorwinkeln, Wiederholungszahl und Entscheidungskriterium.
Kalibrierung und Abnahme erhalten getrennte Daten. Keine Optimierung des
Fensters oder der Kanalauswahl anhand des späteren Bell-Wertes.

Die Auswertung erwartet lineare Analysatorwinkel
a0=0°, a1=45°, b0=22.5°, b1=−22.5°. Das sind **Messachsen**, keine direkt
übertragbaren Wellenplatten-Skalenwerte. Die optische Abbildung und Nullpunkte
werden separat kalibriert. Idealer Singulettwert: S=−2sqrt(2).

Die aktuell implementierte Messplanung hält eine Einstellung je Lauf konstant.
Sie ist für eine Laborcharakterisierung geeignet, schließt jedoch weder
Setting-Abhängigkeit der Quelle noch Zeitdrift noch die Lokalitätslücke.
Eine randomisierte, schnelle Einstellungsauswahl pro Trial ist nicht implementiert.

## Zwei getrennte Resultate

1. Bedingte Koinzidenzkorrelation: genau ein belegter Port pro Seite. Die Masken
   5 (++), 9 (+−), 6 (−+), 10 (−−) ergeben
   E=(n5+n10−n9−n6)/(n5+n10+n9+n6).
   Wiederholungen desselben Kanals bleiben enthalten; sie werden berichtet.
   Leere, einseitige und Doppelport-Trials sind hier nicht im Nenner.
   Die Übertragung auf einen Zwei-Qubit-Zustand benötigt insbesondere eine
   geeignete Detektionsbeschreibung und Fair Sampling. Ein Gate-PASS ist nur
   eine Aussage unter diesen Annahmen, kein schlupflochfreier Nachweis.
2. Alle Trials: lokale feste Zuordnung eines ±1-Ergebnisses je Seite.
   Nur Minus-Port belegt → −1. Plus allein, kein Klick oder beide Ports → +1.
   Alle 16 Masken und sämtliche leeren Zeitfenster bleiben im Nenner. Diese
   vorab definierte Zuordnung beseitigt die Koinzidenz-Postselektion aus dieser
   Statistik. Sie beseitigt nicht automatisch die übrigen Bell-Test-Lücken.

Rohzähler bleiben unverändert. Kein Effizienzgewicht, keine Untergrundsubtraktion,
kein Löschen vermeintlicher Nachpulse und kein pauschaler 5-%-Filter.
Ein qualifiziertes Störquoten-Gate wäre ein eigenes, vorab festgelegtes Verfahren
mit explizitem Zähler/Nenner, Unsicherheit und Behandlung kompletter Messblöcke.
Die beobachtete Wiederholungsquote wird hier ausschließlich berichtet.

## Unsicherheit

S=E00+E01+E10−E11. Der Singulett-Test verwendet vorab T=−S, nicht ein nach
Sichtung gewähltes Vorzeichen. Pro Einstellung sind Produkte ±1.

Unter unabhängigen identisch verteilten Trials innerhalb jeder Einstellung
liefert Hoeffdings Ungleichung für die jeweilige Erwartung eine einseitige
Fehlerwahrscheinlichkeit höchstens alpha/4 bei Abstand

epsilon_j = sqrt(2 log(4/alpha)/N_j).

Mit der Vereinigungsabschätzung ist

T_lower = T_hat − Summe_j epsilon_j

eine konservative untere Schranke mit Abdeckung mindestens 1−alpha für die
vorab definierte Kombination der vier Erwartungswerte. Unabhängigkeit zwischen
den vier Schätzern wird für diese Vereinigungsabschätzung nicht benötigt;
Unabhängigkeit innerhalb der jeweiligen Stichprobe bleibt Voraussetzung.
Für den bedingten Zweig kommt die repräsentative Auswahl der Koinzidenzen hinzu.
Fehlende Koinzidenzen erzeugen INSUFFICIENT_DATA, keine Division durch null.

Default alpha=0.0027 ist eine explizite statistische Konvention, kein 5-%-Limit
und keine Wahrscheinlichkeit für die Wahrheit einer Hypothese. Das numerische
Gate lautet T_lower>2. Die Python-Rechnung nutzt Double-Gleitkommazahlen,
keine zertifizierte Intervallarithmetik.

Zusätzlich wird die Großstichproben-Näherung sigma_E=sqrt((1−E²)/N) und
sigma_S=sqrt(Summe sigma_E²) ausgegeben. Sie setzt zusätzlich unabhängige
Messblöcke voraus. Bei weniger als fünf positiven oder fünf negativen Produkten
wird kein Normalfehler ausgegeben; insbesondere bedeutet ein beobachteter
Randwert E=±1 keine exakt bekannte Korrelation. Der Normal-3sigma-Test ist
sekundäre Diagnostik. Kalibrierfehler und Drift sind nicht in diesen Fehlern.

Unverifiziertes iid, Detektor-Totzeiten, Nachpulse, Ratenänderungen oder Drift
können die genannten statistischen Voraussetzungen verletzen. Ein bestandener
Zählerkonsistenztest prüft diese Physik nicht. Daher bleibt in jeder Ausgabe
`physical_quantum_claim = NOT_ASSESSED`.

## Falsifikationsbeispiel

Der reproduzierbare synthetische Datensatz simuliert Singulett-Wahrscheinlichkeiten
mit unabhängigem Verlust eta=0.75 an beiden Seiten. Die bedingte Statistik liefert
|S|≈2.825; die feste Zuordnung aller Trials liefert |S|=1.4125. Damit demonstriert
die Prüfkette ausdrücklich, warum die beiden Aussagen nicht verwechselt werden
dürfen. Das Beispiel belegt die Softwareverarbeitung, nicht die Entstehung realer
verschränkter Photonen und auch keine allgemeine physikalische Verlustschwelle.

Die CLI prüft vor Statistik die Trial-, Klick-, Wiederholungs- und
Doppelport-Bilanzen, vollständige Snapshots, Fehlerflags, Setting-Vollständigkeit
sowie gleiche Kalibrier-ID, Fensterbreite und Datenherkunft. Unsichtbare
Transportfehler müssen zusätzlich durch den Hostadapter verhindert werden.
