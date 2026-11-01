# KVF-Messvertrag und Teststand · Entwurf v0.13

Stand: 2026-11-01. Status: **CONCEPT_ONLY / NOT_FROZEN / NOT_RUN**.
Dieser Entwurf enthält keine Gerätesteuerung. Er legt eine methodische
Erweiterung der [C01-GUM-Arbeit v0.12](../c01_gum_v0_12/README.md) fest.
Quellenkennungen beziehen sich auf [SOURCES.md](SOURCES.md).

## 1. Forschungsfrage und beanspruchter Umfang

Welche endlichen, mit Unsicherheit versehenen Feldmessungen können zwei
festgelegte Hypothesen über Zustand, Ausbreitung und gegebenenfalls
Raumzeitgeometrie unterscheiden?

Der KVF ist ein Arbeitsbegriff für einen Messgrößenvektor. Seine Komponenten
transformieren nicht allein aufgrund dieser Bezeichnung als Lorentz-Vektor.
Ein vollständiger Quantenzustand oder eine eindeutige Geometrie wird durch
diesen endlichen Vektor im Allgemeinen nicht bestimmt. Insbesondere müssen
Zustand, Randbedingungen und Detektoreigenschaften als mögliche Ursachen
unterschiedlicher Messsignale mitgeführt werden.

Die Versuche von Settembrini et al. und Herter et al. liefern experimentelle
Anknüpfungspunkte für elektrooptische Vakuumkorrelationsmessungen [Q1, Q2].
Die Publikation dieses Entwurfs begründet keine neue Vereinheitlichung von
Metrologie und Quantengravitation. Eine eigene wissenschaftliche Leistung
müsste aus einem nachvollziehbaren Messverfahren, kontrollierter Unsicherheit
und einem informativen Modelltest entstehen.

## 2. Definition der Messgrößen

Für reelle, hinreichend reguläre und räumlich wie zeitlich lokalisierte
Gewichtsfunktionen f_A und f_B seien die selbstadjungierten Feldobservablen

$$
\hat\Phi_A=\int dV_g(x)\,f_A(x)\hat\phi(x),\qquad
\hat\Phi_B=\int dV_g(x)\,f_B(x)\hat\phi(x).
$$

Das Skalarfeld dient hier zur Definition. Im elektromagnetischen Laborfall
wird eine festgelegte, eichinvariante Feldkomponente mit Polarisation,
Materialantwort und tatsächlichem Sensorgewicht verwendet. Die Gewichte,
ihre Einheiten und ihre Normierung gehören zum Messvertrag. Punktweise
Feldprodukte werden nicht als reguläre Messwerte vorausgesetzt.

Mit delta Phi = Phi minus ihrem Erwartungswert definieren wir

$$
H_{AB}=\frac12\langle\{\delta\hat\Phi_A,\delta\hat\Phi_B\}\rangle,
\qquad
\Delta_{AB}=\frac1i\langle[\hat\Phi_A,\hat\Phi_B]\rangle.
$$

Beide Größen sind reell. Bei gleichartigen Feldobservablen haben sie dieselbe
Einheit, nämlich das Quadrat der Einheit von Phi. H_AA und H_BB sind die
entsprechenden Feldvarianzen. Für eine festgelegte Einstellung s lautet der
Vektor

$$
\mathbf v(s)=(H_{AA}(s),H_{BB}(s),H_{AB}(s),\Delta_{AB}(s))^\top.
$$

Mehrere vorab gewählte Einstellungen werden gestapelt; gemeinsame
Kalibrierungen erzeugen dabei Kovarianzen auch zwischen Einstellungen.
Das Zustandsmittel ist für den tatsächlichen Feldzustand definiert. Seine
Interpretation als Vakuumgröße erfordert eine begründete Zustandsbeschreibung
und begrenzte thermische beziehungsweise technische Beiträge.

Die symmetrisierte, zusammenhängende Zweipunktfunktion ist damit explizit
festgelegt. Die Zuordnung einzelner Beiträge zu Vakuumfluktuationen und
Quellstrahlung kann von der Operatorordnung abhängen; diese Konvention muss
im theoretischen und experimentellen Modell übereinstimmen [Q2, Q3].

## 3. Korrelation und kausale Antwort getrennt prüfen

Für lokale relativistische Feldobservablen mit vollständig raumartig
getrennten Trägern fordert Mikrokausalität einen verschwindenden Kommutator.
Die symmetrisierte Korrelation kann zugleich von null verschieden sein
[Q1, Q3]. Eine gemessene Kreuzkorrelation allein trägt daher keinen
Signalübertragungsnachweis.

Ein Antwortkanal untersucht eine kontrollierte Anregung bei A und ihre
Wirkung bei B. Das Kopplungsgesetz, die zeitliche Ordnung, das Vorzeichen,
die Normierung und die Gültigkeit der linearen Antwort sind vorab
festzulegen. Erst dieser Transfer verbindet einen gemessenen Antwortkanal
mit Delta_AB. Reine Koinzidenzzählung oder das Subtrahieren zweier
Korrelationskurven ersetzt diese Herleitung nicht.

Für reale Pulse sind endliche Ausdehnung, Ausläufer, Timingfehler und
Detektorbandbreite einzubeziehen. Eine nominelle Trennung der Pulszentren
zertifiziert keine raumartige Trennung sämtlicher Wechselwirkungsbereiche.
Im Kristall müssen Materialdispersion, Absorption und die kausale
elektromagnetische Antwort modelliert werden; eine Gruppenlaufzeit wird
nicht ungeprüft als fundamentaler Lichtkegel verwendet.

Ein gemessener Rest außerhalb des erwarteten Antwortbereichs wird zunächst
gegen gewöhnliche Übertragungswege, Messfensterüberlappung und Modellfehler
geprüft. Für einen Nulltest ist eine absolute Nachweisgrenze nötig.

## 4. Vorgeschlagene Architektur

| Teil | Aufgabe | Offener Nachweis |
|---|---|---|
| Zwei räumlich versetzte Sondenpulse | Korrelationsmessung bei kontrollierter Verzögerung | Tatsächliche Raumzeitgewichte und Zustandsbeschreibung |
| Elektrooptischer Sensor mit balancierter Polarimetrie | Phasenempfindliche Aufzeichnung | Verstärkung, Phase, Bandbreite, Offset und Rückwirkung |
| Kontrollierte Anregung | Bestimmung des Antwortkanals | Kopplungsmodell, Linearitätsbereich und Übersprechen |
| Unabhängige Referenzen | Zeit, Abstand, Temperatur und optische Übertragung | Kalibrierkette, Kovarianzen und Stabilität |
| Gemeinsame Rohdatenaufzeichnung | Zuordnung aller Versuche und Einstellungen | Vollständigkeit, Sättigung, Totzeit und Auswahlregeln |
| Auswertung | Vorhersagevergleich mit Unsicherheit | Vollständiges Messmodell und vorab festgelegte Entscheidung |

Herter et al. verwendeten zwei Sondenpulse, einen ZnTe-Kristall und
balancierte Detektion bei 4 K zur Unterdrückung thermischer THz-Beiträge
[Q2]. Diese Angaben sind eine Literaturreferenz, keine bereits ausgewählte
Stückliste und kein Genauigkeitsnachweis für unseren Aufbau. Die Eignung
einer Variante ohne Kryotechnik ist separat zu untersuchen.

Für das bestehende Photonikprogramm kann die C01-Arbeit die Organisation
von Kalibrierbelegen, Zeitstempeln und vollständigen Versuchsregistern
beisteuern. Ein neu hergeleiteter Feld-zu-Detektor-Transfer bleibt nötig.

Zum Zwei-Schlüssel-Prinzip gehören eine unabhängig belegte metrologische
Referenz und ein bestandener physikalischer Modelltest. Beide können
gemeinsame Unsicherheitsquellen besitzen. Übereinstimmung zweier Kanäle
schließt gemeinsamen Bias nicht aus.

## 5. GUM-Verfahren für den Vektor

Die folgende Zuordnung folgt der Abfolge von JCGM 100:2008, Abschnitt 8,
unter Einbezug der Nichtlinearitäts-Ergänzung 2026 [G1, G2]. Für mehrere
Ausgangsgrößen ist JCGM 102:2011 maßgeblich [G3]. Dies ist eine
Verfahrensspezifikation; eine vollständige Bilanz kann erst nach Festlegung
des konkreten Detektormodells und seiner Eingänge gerechnet werden.

| Schritt | Verpflichtende Ausarbeitung |
|---|---|
| 1 · Messmodell | V = F(X) für die tatsächlichen Detektordaten einschließlich erforderlicher Korrekturen, Raumzeitgewichte und Transfergrößen definieren. |
| 2 · Eingangsschätzwerte | Schätzwerte x, Einheiten, Betriebsbereich und Herkunft jeder Eingangsgröße dokumentieren. |
| 3 · Standardunsicherheiten | Typ-A- und Typ-B-Auswertungen begründen; Zeitkorrelationen und gemeinsam ausgewertete Daten berücksichtigen. |
| 4 · Kovarianzen | Gemeinsame Referenzen, Offsets, Driften und wiederverwendete Rohdaten in der vollständigen Eingangskovarianz U_x erfassen. |
| 5 · Ausgangsschätzung | Schätzung v nach dem gewählten Auswerteverfahren bestimmen; bei Nichtlinearität den Unterschied zwischen F(E[X]) und E[F(X)] prüfen. |
| 6 · Fortpflanzung | Linearisierung prüfen; Sensitivitätsmatrix und Ausgangskovarianz berechnen oder geeignete Verteilungsfortpflanzung verwenden. |
| 7 · Überdeckung | Gewünschte Überdeckungswahrscheinlichkeit und gemeinsamen Überdeckungsbereich begründet bestimmen. |
| 8 · Ergebnisbericht | Schätzwert, Kovarianz, Überdeckungsbereich, Verfahren, Annahmen, Einheiten, Datenbezug und Einschränkungen gemeinsam berichten. |

Für eine hinreichend genaue Linearisierung gilt nach JCGM 102, Abschnitt
6.2.1, Gleichung (3), mit der an x ausgewerteten Sensitivitätsmatrix J

$$
J_{ki}=\left.\frac{\partial F_k}{\partial X_i}\right|_x,
\qquad
U_v=J U_x J^\top.
$$

Das ist die Fortpflanzung erster Ordnung. Ihre Voraussetzungen sind zu
prüfen; das Wort „GUM“ macht eine nichtlineare Näherung nicht exakt.
Bei relevanter Nichtlinearität oder ungeeigneten Verteilungsformen wird die
gemeinsame Eingangsverteilung gemäß JCGM 102, Abschnitt 7, fortgepflanzt,
einschließlich der dort behandelten Monte-Carlo-Auswertung [G3, G4].
Numerische Konvergenz und die Tragfähigkeit der Eingangsverteilungen müssen
belegt werden.

Einzelne 95-%-Intervalle ergeben nicht automatisch einen gemeinsamen
95-%-Überdeckungsbereich. Ein skalares k = 2 wird weder pauschal auf den
Vektor übertragen noch als extrem kleine Fehlentscheidungswahrscheinlichkeit
interpretiert. Die Entscheidung über eine Toleranz oder ein Modell braucht
zusätzlich eine festgelegte Entscheidungsregel und ihre Risikobewertung
[G3, G5].

Die C01-Grenze von 2 ppm gilt weiterhin für die in v0.12 definierte Größe.
Für jede KVF-Komponente sind Einheit, fester Referenzmaßstab und Toleranz
zu vereinbaren. Eine relative ppm-Angabe bezüglich eines verschwindenden
Kommutators ist ungeeignet; dort wird eine absolute Grenze benötigt.

## 6. Verbindung zu Kausalsets und Quantengravitation

Für bestimmte freie Skalarfeldmodelle auf Kausalsets lassen sich retardierte
und avancierte Greenfunktionen, eine Pauli-Jordan-Struktur und ein
spektral ausgewählter Sorkin-Johnston-Zustand konstruieren [T1, T2].
Zusätzliche Angaben zu Feld, Masse, Operator, Volumenskala, Gebiet und
Zustandswahl gehören zu einer solchen Konstruktion. Eine endliche
Kausalordnung mit Elementzahlen liefert noch keinen universell eindeutigen
experimentellen Vakuumvektor.

Brauns Rekonstruktion aus den Wahrscheinlichkeitsgesetzen zufälliger
Ordnungsdaten betrifft eine andere Ebene als die eindeutige, fehlerkontrollierte
Inversion einer einzelnen endlichen Messung [T3]. Ein endlicher KVF-Vektor
muss seine Identifizierbarkeit durch einen eigenen Modellvergleich zeigen.

Für den ersten Rechentest sind zwei Modelle innerhalb derselben Feld- und
Detektorbeschreibung zu wählen. Ein freies Skalarfeld auf einem Kausalset
und elektromagnetische Pulse in einem Kristall sind ohne begründete
Übersetzung kein direkt vergleichbares Modellpaar. Das zu prüfende Paar
bleibt in dieser Version offen.

Ein späterer Quantengravitationstest erfordert eine aus dem gewählten
Modell abgeleitete Abweichung in tatsächlich zugänglichen Observablen.
Eine frei angepasste Zusatzrauschamplitude oder ein analoges Raumzeitmodell
allein trägt diesen Nachweis nicht.

## 7. Ausführbarer Auftrag für die nächste Forschungsstufe

1. Zwei Modelle M0 und M1 samt festen Parametern beziehungsweise erlaubten
   Parameterbereichen, Zuständen und gemeinsamer Detektorabbildung festlegen.
2. Vorhersagen für denselben KVF und dieselben Rohdatensignale berechnen.
   Rand-, Diskretisierungs- und numerische Fehler separat kontrollieren.
3. Prüfen, ob Zustands-, Material- oder Kalibrierparameter den Modellunterschied
   nachbilden können. Solche Mehrdeutigkeiten im Ergebnis ausweisen.
4. Messbedingungen und tolerierte Fehlentscheidungen vorab festlegen.
   Benötigte Kovarianz, absolute Nachweisgrenzen und Stichprobenumfang aus
   dem Modellunterschied und der Entscheidungsregel ableiten.
5. Mit unabhängigen Kontrollen die Auswertung prüfen. Ein Feldversuch wird
   erst nach belegtem Detektortransfer und erfülltem Unsicherheitsbudget
   freigegeben.

Das Ergebnis dieser Stufe ist ein prüfbarer Empfindlichkeitsbericht mit
einem von drei Befunden: unterscheidbar unter ausgewiesenen Bedingungen;
mit dem verfügbaren Budget nicht unterscheidbar; wegen fehlender
Modell- oder Kalibrierinformation noch unentscheidbar. Bis dahin bleibt
der physikalische Einsatz auf HOLD.
