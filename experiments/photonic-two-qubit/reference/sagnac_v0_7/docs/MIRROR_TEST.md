# Spiegel-Prüfkörper: Strahlstabilität vor Materialmodell

Status: ausführbarer Versuchsplan, **noch nicht physisch durchgeführt**.
Ergebnisziel: Positions- und gegebenenfalls Winkelstabilität des montierten
Spiegels. Keine direkte Bestimmung von Volumenschrumpfung, Scherverzerrung,
Elastizitätsmodul, Glasübergang oder garantierter Lebensdauer.

## 1. Prüflinge und Dokumentation

Zunächst eine mechanisch gehaltene Referenz und mindestens drei unabhängig
gefertigte geklebte Prüflinge als kleiner Screening-Lauf. Drei Prüflinge sind
ein vorgeschlagener Startumfang, keine statistische Serienqualifikation.
Spiegel, Träger, Basismaterial und Belichtungsgeometrie werden vor dem Versuch
festgelegt. Für jede Probe werden dokumentiert:

- Material und Abmessungen von Spiegel, Träger und Basis; Zeichnung/Foto mit
  Klebestellen, Dreh-/Messachsen und Referenzpunkten.
- Klebstoffprodukt, Charge, Lagerbedingungen und Verfallsdatum.
- Oberflächenbehandlung nach geeigneter Herstellervorgabe.
- Tatsächliche Klebstoffmenge, Spaltgeometrie, eventuelle Spacer und Montagekraft.
- UV-Zugangsweg zu jeder Klebefläche, Wellenlänge, lokale Bestrahlungsstärke und
  Dosis, Messmittel und dessen Kalibrierung; Temperatur am Prüfkörper.

Keine automatische Festlegung auf 50 µm oder 0.5 Vol.-% Glasperlen. Solche
Parameter wären getrennt zu untersuchende Varianten. Glaszwischenkörper gelten
nicht ohne weitere Auslegung als thermische Entkopplung. Verdeckte Fugen werden
nicht durch eine äußerlich sichtbare Randhärtung als vollständig gehärtet erklärt.

## 2. Messstrecke

Ein stabiler Laser beleuchtet den Prüflingsspiegel; der reflektierte Strahl trifft
auf einen PSD oder eine zuvor hinsichtlich Positionsmessung kalibrierte Kamera.
He-Ne ist möglich, aber für diesen Vorversuch keine zwingende Voraussetzung.
Die Messstrecke hat als Planwert etwa 1 m. Der tatsächliche Abstand entlang des
reflektierten Strahls, die Winkel und die Sensororientierung werden gemessen.
Der nutzbare Strahlweg ist eingehaust; Strahlenden sind abgefangen. UV-Härtung
und Positionsmessung werden optisch getrennt, damit Härtungslicht keine
Sensorverschiebung oder Sättigung vortäuscht.

Eine Referenzstrecke mit festem Spiegel und möglichst gemeinsamem Laser
beobachtet die Eigenstabilität. Laser, Referenz und Detektor stehen auf einem
gemeinsamen stabilen Träger. Eine thermische Kammer bringt zusätzliche Fenster-
und Luftwegdrift mit; diese wird mit Referenzläufen erfasst. Eine Referenzkorrektur
entfernt nur tatsächlich gemeinsame Störungen und beweist keine vollständige
Ursachentrennung. Rohsignal und korrigiertes Signal bleiben beide gespeichert.

## 3. Was ein Sensor misst

Im paraxialen, ebenen Spezialfall:

Delta x(Z) ≈ Delta b + 2 Z Delta theta.

Delta b ist ein Strahlversatz in einer definierten Bezugsebene, kein unmittelbar
gemessener Materialverschub. Bei festem Delta b ergibt sich aus 1 µm
Punktverschiebung bei Z=1 m eine Winkeländerung von etwa 0.5 µrad. Das ist eine
Umrechnung, keine behauptete Auflösung des Messgeräts.

Für eine kalibrierte Winkelaussage benötigen wir einen bekannten kleinen
Winkelschritt oder eine unabhängige Winkelreferenz. Bei schrägem Einfall und
zwei Achsen wird eine gemessene Abbildungsmatrix verwendet, nicht ungeprüft
dieselbe 2Z-Konstante für beide PSD-Koordinaten.

Optional liefern zwei **gleichzeitig erfasste**, kalibrierte Ebenen Z1 und Z2
eine Trennung von Strahlversatz und Strahlwinkel:

Delta theta ≈ (Delta x2−Delta x1)/(2(Z2−Z1)).

Auch diese Messung rekonstruiert nicht allgemein die vollständige 3D-Bewegung
des Spiegels oder die Scherverteilung in der Klebefuge. Ein bewegter Sensor
führt ohne zusätzliche Stabilitätsannahmen keine gleichzeitige Zweiebenenmessung
aus. Interferometrie wäre ein eigener Aufbau für Weglänge/Phasenänderung und
wird erst ergänzt, wenn das erforderliche Messbudget sie rechtfertigt.

## 4. Ablauf und getrennte Beobachtungen

| Phase | Durchführung | Zu protokollierendes Ergebnis |
|---|---|---|
| Messstrecken-Nullversuch | Referenz ohne Klebevorgang über vergleichbare Dauer beobachten | Rauschen, Laser-/Sensordrift, Temperatureinfluss |
| Baseline | Prüfling im Jig, vor UV, stabile Umgebung | Mittelwert, Streuung, Zeitreihe, Temperatur |
| Vorfixierung | Produktspezifische Belichtung bei dokumentierter Dosis | Signal während und nach Belichtung, lokale Erwärmung |
| Endhärtung | Jig in definierter Stellung halten; produktgerechte vollständige Belichtung | Drift durch Härtung und thermische Erholung |
| Jig lösen | Erst nach dokumentierter Endhärtung, Schritt separat markieren | Entlastungssprung und nachfolgende Drift |
| Alterung | Falls für den gesamten Aufbau geeignet, nach Produktspezifikation | Drift vor/nach Behandlung bei gleicher Bezugstemperatur |
| Temperaturprüfung | Vorab festgelegte Zyklen, tatsächliche Bauteiltemperatur erfassen | reversible Drift, Hysterese und Rückkehrfehler |

Die 10-s-Vorfixierung im NOA61-Datenblatt ist ein lampenspezifisches Beispiel.
Sie ist keine allgemeine Handlampenvorgabe. Das Datenblatt nennt 3 J/cm² im
Bereich 350–380 nm für vollständige Härtung. Die reale Baugruppe benötigt
nachgewiesene Belichtung der gesamten relevanten Fuge. Eine Wartezeit von fünf
Minuten wird nicht als Nachweis abgeschlossener Schrumpfung verwendet.
Die Angabe 50 °C/12 h betrifft die Ausbildung optimaler Glashaftung; sie ist
keine Kryoqualifikation des Moduls. Sie darf nur eingesetzt werden, wenn die
übrigen Komponenten und ihre Spezifikationen diese Behandlung erlauben.

## 5. Vorschlag für den ersten Temperatur-Screeninglauf

Nach vollständiger Härtung und geeignetem Alterungsprozess:
25 → 15 → 25 → 35 → 25 °C, dreimal wiederholen. Temperaturgrenzen sind ein
**Versuchsvorschlag** aus dem bisherigen Entwurf und vor Durchführung mit den
Bauteilspezifikationen abzugleichen. Rampenrate, Haltezeit, Messrate und
Auswerteabschnitte werden vor dem Lauf fixiert. Thermisches Gleichgewicht wird
an der Probe und nicht nur am Kammerregler beurteilt; geeignete Kriterien werden
im leeren Referenzlauf ermittelt. Kein nachträgliches Auswählen günstiger Plateaus.

Ergebnisgrößen pro Achse:

- Härtungsdrift bei gleicher Bezugstemperatur.
- Sprung beim Lösen des Jigs.
- Positions- bzw. kalibrierte Winkeländerung über Temperatur.
- Rückkehrfehler bei 25 °C nach jedem Zyklus.
- Zeitdrift bei konstanter Temperatur sowie Streuung zwischen Prüflingen.

Positionsmessunsicherheit, Laser-/Referenzstabilität, Temperaturunsicherheit,
Zeitabgleich und gegebenenfalls Winkelkalibrierung werden separat angegeben.
Ein linearer Fit über Temperatur wird nur als empirischer Zusammenhang
bezeichnet, nicht als direkt bestimmter CTE oder Klebstoffmodul.

## 6. Freigabegrenze

Solange kein optisches Toleranzbudget vorliegt, ist das Resultat CHARAKTERISIERT,
nicht FREIGEGEBEN. Das Budget wird am justierbaren Referenz-Sagnac durch
kontrollierte Winkel-/Positionsvariationen und Messung von Kopplung, Raten und
Zustandskorrelationen bestimmt. Für jedes Bauteil wird daraus ein zulässiger
Bereich abgeleitet. Ein Messwert einschließlich Messunsicherheit muss in diesem
vorab festgelegten Bereich bleiben. Die spätere Klebe-Freigabe gilt nur für die
geprüfte Geometrie, Charge/Prozessfamilie und Umweltbedingungen.

Vibration, Schock, Feuchte und Langzeitalterung werden hier nicht qualifiziert.
Ein Temperaturtest allein belegt keine Transport- oder Erschütterungsfestigkeit.
