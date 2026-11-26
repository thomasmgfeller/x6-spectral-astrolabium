# CST-DUST · Sendepuls auf der festgehaltenen N19-Ordnung

**26. November 2026.** Ein lokaler positiver Skalarpuls am Sender verändert den ideal ausgelesenen Skalarfeldwert am Empfänger. Im bereits veröffentlichten masselosen Skalarwirkungsansatz beträgt die Änderung exakt 1/5 in den festgelegten Recheneinheiten. Ein Puls am Empfänger verändert den früheren Sender ebenfalls um 1/5. Eine ausschliesslich vorwärts gerichtete Lösung für die einzelne Senderquelle ist mit den elf inneren Wirkungsgleichungen unvereinbar. Dieser Widerspruch bleibt sogar bei vier frei wählbaren zukünftigen Skalar-Randwerten bestehen.

Ein zusätzlich als Ausbreitungsgesetz eingesetzter retardierter Benincasa-Dowker-Operator liefert beim gleichen Ein-/Aus-Versuch eine gerichtete Antwort. Die projektinterne Staubuhr und die Staubdichte am Empfänger haben auf dieser Ordnung in beiden Armen dieselbe stationäre Lösung. Für eine Lichtlaufzeitmessung fehlt ein aus der Dynamik begründeter Emissions- und Detektormechanismus. Die 60 physischen P3-Prüfpunkte stehen auf `NOT_RUN`.

## Versuch und Auslese

Als Hintergrund dient das N19-Paket aus dem Merge von PR 385. Beide Uhren, alle Staubgewichte, die Ordnung, die Randpräparation und die Skalar-Randwerte sind in den drei Hauptarmen identisch. Die vier gerundeten Staubgewichte am Zukunftsrand erfüllen 64w = (1,006543; 0,96181039; 0,95090962; 1). Zwei davon wurden bereits in der Vorstudie auf die gewünschten Uhrzeiten angepasst. In diesem Versuch wurden Quelle, Empfänger, Beobachtungsfenster und Amplitude vor der Antwortrechnung festgelegt. Der lokale Planhash dokumentiert den verwendeten Text und hat keinen extern beglaubigten Zeitstempel.

Der Leser erhält alle 19 Uhren und Staubgewichte als Intervalle sowie die strikte Kausalordnung. Das Sendefenster und das Empfangsfenster müssen jeweils genau ein sicher positives Ereignis enthalten. Diese Regel liefert den Sender z=16 bei x≈0,500000 und den Empfänger r=18 bei x≈0,500268. Der Quellort wird bei der Feldvariation festgehalten. Ein freies Vakuumereignis trägt Staubgewicht null und hat im Skalarfeld weiterhin einen Freiheitsgrad.

Der neue ideale Feldleser gibt die signierte skalare Feldänderung am Ort der jeweiligen Materialmarke zurück. Die bisherige materielle Auslese verwendet die lokale Staubuhr und das Dichtegewicht. Ein physisches Gerät, eine Rauschschwelle und eine absolute Skalareichung sind offen. Die Einheitsquelle, der Nullarm und die umgepolte Quelle dienen der Prüfung von Trennbarkeit, Linearität und Kausalrichtung im exakten Modell.

| Gleichung auf den elf freien Punkten | Empfänger bei Quelle 0 | Bei Quelle +1 am Sender | Bei Quelle −1 am Sender | Früherer Sender bei Quelle +1 am Empfänger |
|---|---:|---:|---:|---:|
| Stationärer masseloser Skalarwirkungsansatz | 0 | 1/5 | −1/5 | 1/5 |
| Retardierter BD-Testoperator | 0 | −1 | 1 | 0 |

Die Zahlen verwenden die jeweils im Prüfplan festgelegten dimensionslosen Quellnormierungen. Ein Verhältnis der beiden Beträge besitzt hier keine experimentelle Bedeutung.

## Der Widerspruch in den Wirkungsgleichungen

Bei einheitlichem geometrischem Volumen, verschwindender Skalarmasse und herausgekürztem positiven Faktor av lautet die zusätzliche Skalarwirkung

    Sφ = −(1/4) Σ_{i≺j} b(kᵢⱼ) (φⱼ−φᵢ)².

kᵢⱼ zählt die offenen Intervallpunkte, b nimmt in den ersten vier Schichten die Werte (1,−9,16,−8) an und verschwindet danach. Die Variation von Sφ−Σ jᵢφᵢ gibt Hφ=j auf den elf freien Ereignissen. Die vier Vergangenheits- und vier Zukunftskragen haben im Hauptversuch den Skalarwert null. Jede der 129 Ordnungsrelationen wird vor der Schichtauswahl berücksichtigt. Für den inneren Block gilt det(2H_II) = 63 030 600. Damit ist das stationäre Randwertproblem eindeutig lösbar.

Bei einem positiven Einheitspuls an z lauten die vier von null verschiedenen Feldwerte φ₁₅=9/5, φ₁₆=81/5, φ₁₇=1/5 und φ₁₈=1/5. Ereignis 15 liegt strikt vor z, Ereignis 17 ist mit z kausal unvergleichbar. Beide Ereignisse tragen Staubgewicht null. Die Rückwärtskontrolle erreicht dagegen eine **positive** Materialmarke. Die symmetrische Hesse-Matrix erklärt die Reziprozität der stationären Antwort. Das Modell gibt bei dieser Rechnung die Lösung eines Randwertproblems aus.

Für eine retardierte Differenz darf das Feld ausschliesslich am Sender und in seiner kausalen Zukunft von null abweichen. Bei festen Kragen sind dann nur φ₁₆ und φ₁₈ frei. Selbst wenn alle vier künftigen Skalar-Randwerte beliebig mitreagieren dürfen, erhält man für die Zeilen 16 und 17 auf allen zulässigen Spalten dieselben Koeffizienten.

| Innere Gleichung | φ₁₆ | φ₁₈ | φ₇ | φ₈ | φ₉ | φ₁₀ | Benötigte rechte Seite |
|---|---:|---:|---:|---:|---:|---:|---:|
| Am Sender 16 | 0 | 1/2 | −9/2 | 8 | −4 | 0 | 1 |
| Am leeren Vorläufer 17 | 0 | 1/2 | −9/2 | 8 | −4 | 0 | 0 |

Die Differenz dieser Gleichungen verlangt 0=1. Bei festen zukünftigen Kragen steigt der Rang durch Hinzunahme der Quelle von 2 auf 3. Bei freien zukünftigen Skalar-Kragenwerten steigt er von 6 auf 7. Die Vergangenheit, die elf inneren Gleichungen und die vier Staub-Randgewichte bleiben auch in diesem erweiterten Test fest. Der Ausschluss gilt auf dieser Ordnung für eine einzelne lokale Quelle, den verwendeten masselosen Wirkungsansatz und die angegebene Forderung an den Träger der Antwort. Er allein entscheidet weder die Frage nach einem Quantensignal noch die nach anderen Historien oder physikalischen Anfangsdaten.

## Gerichtete Testfeldkontrolle

Für diese Kontrolle wird der unverschmierte vierdimensionale Skalaroperator B direkt als Testfeldgleichung verwendet. Nach Herausnahme des positiven Vorfaktors stehen auf der Diagonale −1 und in den Vorgängerschichten die Koeffizienten b(k). Auf freien Ereignissen gilt Bφ=j. Beide äusseren Kragen haben wieder Skalarwert null. Ihre Werte sind vorgegeben, die Gleichungen werden auf den elf inneren Ereignissen geprüft.

Die Zeilen lassen sich in kausaler Reihenfolge lösen. Bei einem Einheitspuls hat φ₁₆ den Wert −1. Da 16 und 18 durch einen Link verbunden sind und alle übrigen Vorgänger von 18 in diesem Arm Feldwert null haben, folgt φ₁₈=−1. Bei Rückwärtseinspeisung bleibt φ₁₆=0. Für alle elf inneren Einzelquellen verschwindet die jeweilige Feldantwort ausserhalb von Quelle und kausaler Zukunft. Beim stationären Randwertproblem besitzt keine der elf Einheitsquellen diese Trägereigenschaft. Der lokale BD-Linkwert erklärt die gerichtete Positivkontrolle bereits algebraisch. Daraus folgt keine neue unabhängige Bestimmung der zuvor gewählten Empfangszeit.

Benincasa und Dowker untersuchen diesen Typ retardierter Skalaroperatoren und seine Kontinuumseigenschaften unter geometrischen und statistischen Voraussetzungen. Eine entsprechende vierdimensionale Kontinuumsapproximation der ausgewählten N19-Ordnung ist offen. [Primärquelle, Gleichung (2)](https://arxiv.org/pdf/1001.2725)

## Bedeutung für die Staubmessung

Der minimale Vertrag setzt die direkte Staub-Skalar-Kopplung auf null. Bei festgehaltener Ordnung und fest lokalisiertem Quellort hängt der zusätzliche Term Sφ−j·φ von keinem der freien Staubwerte ab. Die vollständigen Staubgleichungen stimmen deshalb in den Pulsarmen überein. Auf dem festgehaltenen stationären Zweig sind die Änderungen der Staubuhr und des Dichtegewichts exakt null. Die symbolische Trennung gilt auf diesem gesamten Zweig. Zwanzig exakte Differenzen an rationalen Testkoordinaten kontrollieren die Implementierung für alle elf Uhr- und neun positiven Dichtevariationen.

Der nächste physikalische Schritt ist ein dynamischer Sender- und Detektorvertrag. Er müsste eine retardierte Ausbreitung aus festgelegten Anfangsdaten begründen und am Empfänger eine separat definierte, mit der Materie gekoppelte Aufzeichnung liefern. Der Zeilenwiderspruch oben schliesst eine Reparatur allein durch neue spätere Skalar-Randwerte für diesen Versuch aus. Aus dem derzeitigen Zeitabstand wird kein Arealradius bestimmt.

## Daten und Reproduktion

Im entpackten Verzeichnis genügt Python ab 3.10 mit der Standardbibliothek.

    python3 -B pruefen.py

Der Prüfer reproduziert den archivierten N19-Ausgangsstand, vergleicht die rekonstruierte Ordnung mit der ursprünglichen Implementierung und kontrolliert die lokalen SHA-256-Summen. Er erzeugt beide Ergebnisdateien im Speicher neu und vergleicht sie byteweise. Eine zweite Rechnung polarisiert die ursprüngliche Skalarwirkung für alle 361 Matrixeinträge. Ganzzahlige Minoren und eine kausale Vorwärtsrekursion kontrollieren je 121 Antwortkoeffizienten. Alle 171 einzelnen Vertauschungen von Ereigniskennungen erhalten die Felder, ihre Gleichungen und die Markenauswahl.

* `Ergebnisse.json` enthält sämtliche vier Pulsarme, den Katalog der Einzelquellen und die Rangzeugen.
* `Gegenrechnung.json` enthält die Determinante, die identischen Gleichungszeilen und die Zahl der Prüfungen.
* `Quellen.json` benennt Commit, Repository-Pfade und Hashwerte der Originaleingaben. Der mitgeführte ursprüngliche Modellcode dient als Referenz. Die unabhängige Offline-Reproduktion läuft ohne dessen Drittbibliotheken.

[N19-Ausgangsstudie](https://github.com/thomasmgfeller/x6-spectral-astrolabium/tree/beb1b479f31fc14e4a82b57239fd0fcf22d57aad/research/rax_cqg/dust_collapse/n19_stationaeres_sende_und_empfangspaar_v0_1) · [Minimaler Skalarwirkungsansatz](https://github.com/thomasmgfeller/x6-spectral-astrolabium/tree/beb1b479f31fc14e4a82b57239fd0fcf22d57aad/research/rax_cqg/dust_collapse/minimal_scalar_action_v0_1)
