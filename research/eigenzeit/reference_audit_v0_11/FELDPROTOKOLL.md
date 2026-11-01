# Messblatt · Prüfung einer konkreten Anlage

**Aktueller Status: HOLD_EVIDENCE.** Es liegen keine identifizierte Vergleichseinrichtung, unabhängigen Grenzen für den Transfer oder markierten Paardaten einer Anlage vor. Die Beispielrechnungen sind synthetisch.

## Vor der ersten Gelegenheit

1. Eine eindeutige scope_id für Gerät, Firmware, Zeitfenster, Zielzustand, Quelle, Vergleichsstandard, Zellzuordnung und die erlaubten Betriebsbedingungen vergeben. Dokumentieren, welche physikalische Größe z darstellt, wie sie normiert und mit welcher Unsicherheit sie erfasst wird. 1/4 und 3/4 sind feste Stützstellen dieser Skala. Unsicherheiten von z in den Nachweis der maximalen effektiven Entfernung bzw. die vorhandenen Fehlerzuteilungen einrechnen.
2. Den Standard Y unabhängig auf a(c)p_j zurückführen. Für beide Stützstellen jeder Zelle eine nachvollziehbare 2-ppm-Grenze für systematische Differenzen vorlegen. Ein gemeinsamer unkorrigierter Versatz bleibt durch Paarvergleich allein unsichtbar. Einen zweiten Kanal ohne eigene Rückführung als offenen Nachweis markieren.
3. Über die gesamte Zustandsmenge technische Belege für die Schranken von 8 ppm/Zustandseinheit (Prüfling) und 4 ppm/Zustandseinheit (gemeinsamer Faktor), den Gainbereich und die bedingte Abweichung von höchstens 1 ppm bei jeder Betriebsgeschichte dokumentieren. Nachlauf, Totzeit, Regelkreise, Temperatur, zeitliche Zuordnung und Rückwirkung des Vergleichskanals gehören in diesen Nachweis, wenn sie die konkrete Anlage beeinflussen. Fits an den zwei Stützstellen liefern keine globale Schranke. Statistische Risiken externer Belege gesondert ausweisen.
4. Die Überwachung muss jeden zulässigen Zustand und die externe gemeinsame Gain-Zuordnung abdecken. Bei Überschreitung oder fehlender Zustandsbeobachtung die nachgelagerte Auswertung sperren. Preflight, Audit, neue v0.10-Referenzzählungen und Geometrieordnung eindeutig trennen. Ein negativer Präfix gehört zum selben Audit und darf nicht durch Neustart ersetzt werden.
5. Tatsächliche Reihenfolge vor Beginn festlegen. Für frühen Abbruch mit C01 bei z=1/4 beginnen und die übrigen 31 Punkte seriell in der festen Reihenfolge des Formulars bearbeiten. Den vollständigen Plan, seine einmalige Versuchszuteilung, Quelldefinition, Abbruchregeln und Rohdatenpfade versionieren.

## Während der Messung

Jede markierte Gelegenheit bekommt eine eindeutige ID, Zeitpunkt, Zelle, Soll- und Istzustand sowie zwei binäre Antworten X,Y (in dieser Reihenfolge). Ein gültiger physischer Nichtnachweis ist 0. Ein verlorener oder doppelt zugeordneter Datensatz ist ein Erfassungsfehler und sperrt die Auswertung. Pro Messpunkt die vier disjunkten Zähler 00, 01, 10 und 11 aus dem vollständigen Rohprotokoll ableiten; Rohprotokoll und Auswertestand separat sichern. Eine wiederholte Kopie desselben Detektorbits ist kein unabhängig verankerter Vergleich.

Nach der 26. Diskordanz darf der gesamte Durchlauf negativ enden. Vorher zeigt der optionale Präfixprüfer nur NO_EARLY_STOP. Eine positive Zählentscheidung verlangt an *allen* 32 Punkten je exakt 3.300.000 vollständig belegte Paare. Sowohl Ausfälle des Standards als auch ungültige Nachweise führen zu HOLD.

## Nachweise für die Auswertung

Die ausgefüllte Kopie von examples/field_worksheet.json verweist unter evidence für jede der sieben Behauptungen auf eine lokale JSON-Quittung mit file und sha256. Pfade sind relativ zum Eingabeordner. Jede Quittung trägt denselben mode und dieselbe scope_id wie der Feldbogen. Ihr claims-Objekt verweist je Behauptung wiederum mit file und sha256 auf das inhaltliche Belegdokument. Die Dateien in examples zeigen das Format mit klar als synthetisch gekennzeichneten Belegen. Für echte Anlagen gehören die sieben belegten Aussagen, Verantwortliche und Umfang in fachlich geprüfte Nachweise.

audit.py prüft Dateiintegrität, Modus, Geltungsbereich, Vollständigkeit und Summen. Es kann die Echtheit des Ausstellers, die Richtigkeit der Rohzählungen und die Gültigkeit physikalischer Zusagen nicht aus Dateihashes ableiten. Ein vollständig bestandenes Feldformular liefert deshalb PASS_COUNTS_REVIEW_REQUIRED. Erst nach fachlicher Prüfung der sieben Belege darf ein Verantwortlicher die Residualbedingung im v0.10-Feldbogen referenzieren. Alle übrigen v0.10-Anforderungen bleiben separat zu prüfen.

## Praktischer erster Versuch

Für die Entscheidung über die Machbarkeit genügen am ersten Messpunkt zwei auf dieselben Ereignis-IDs bezogene Ausgangsfolgen. Stimmen die Kanäle selten überein, kann der Verlusttest den Audit früh beenden. Ohne gültigen unabhängigen Zielanker darf dieser erste Datensatz höchstens mangelnde Paarübereinstimmung feststellen. Ein positiver physikalischer Nachweis ist dann gesperrt.
