# Geometriefehler und Messunsicherheit getrennt kalibrieren

Vorabplan vom 21. Oktober 2026. Basis ist der Forschungszweig von PR #69,
Commit `a17462f32b79ff7f8c8a71b9a0622366fc8da9e3`. Der eigenständige
4D-Demonstrator-Nachweis in PR #73 ist keine Qualifikation dieses
2+1-Operatorversuchs. Die bestehenden wissenschaftlichen HOLDs bleiben erhalten.

## Ziel und Modellgrenze

Bei einer vollständigen Wolke C sind die vier vorhandenen Operatoren feste
lineare Abbildungen B_a(C). Die Varianten sind Original, Metadatenkorrektur,
Relationsprojektion und Relationsprojektion plus Metadatenkorrektur. Gewichte,
Auswahl, Guards und trainiertes Metadatenmodell werden nicht verändert.
Alle vier nutzen dieselben Ereignisse einschließlich einer gemeinsamen
Rootmessung; das Feld wird erst nach dem Versiegeln der Inferenz ausgewertet.

Für ein bekanntes Prüffeld f mit Referenzwert Lf lautet das Modell:

    z(C,f,r) − Lf = e(C,f) + B(C) ε_r,
    e(C,f) = B(C) f − Lf,
    E[ε_r | C] = 0,   Cov(ε_r | C) = σ² I.

Der rauschfreie Fehler e enthält Rekonstruktions-, Diskretisierungs-, Auswahl-
und Feldabhängigkeit. Er wird nicht als reine Einbettungsabweichung bezeichnet.
Messunsicherheit meint in diesem kontrollierten Versuch zusätzliches
Feldrauschen. Im allgemeinen metrologischen Sinn können auch unsichere
systematische Effekte zur Messunsicherheit gehören; diese Terminologie
rechtfertigt kein Weglassen des hier separat ausgewiesenen Modellfehlers.

## Exakte Zerlegung und getrennte Größen

Je Prüffeld über Wolken: b_f=E_C[e], G_f=Cov_C(e). Bedingt auf eine Wolke:

    N(C) = σ² B(C) B(C)ᵀ.

Mit dimensionslosen Stützgewichten a und lokaler Skala s ist
B=(-sum(a), a)/s². Deshalb gilt für zwei Varianten:

    N_ab = σ² (a_a·a_b + sum(a_a) sum(a_b)) / s⁴.

Der zweite Term stammt vom geteilten Rootwert. Die Kreuzkovarianzen dürfen
nicht entfallen. Unter dem deklarierten Rauschmodell ist der Kreuzterm
zwischen e(C,f) und B(C)ε bedingt auf C null. Folglich:

    E[(z−Lf)(z−Lf)ᵀ] = b_f b_fᵀ + G_f + E_C[N(C)].

Bei R unabhängigen Wiederholungen derselben Wolke sinkt nur N(C)/R.
Der Geometrie-/Modellfehler bleibt. Die Analyse zeigt die Beiträge sowie die
erwarteten RMSEs bei 1, 16 und 512 gemittelten Messungen. Diese Rechnung ist
eine Modellfolge, keine neue physische Messung.

Die empirische G-Matrix über Wolken ist weder eine bedingte Kovarianz für
eine bestimmte Wolke noch eine Koordinaten-/Einbettungskovarianz. Aus ihr
wird keine anisotrope Projektionsmetrik abgeleitet. Auch die QP-Hesse-Matrix
wird nicht als statistische Einbettungspräzision verwendet.

## Referenzgeometrie separat prüfen

Simulator-Koordinaten stehen ausschließlich dem Auswertungskanal zur Verfügung.
Er prüft pro unveränderter und projizierter Rekonstruktion:

- die Lorentz-Gram-Matrix, ohne willkürlichen euklidischen Koordinatenabgleich;
- fehlende und zusätzliche gerichtete Kausalrelationen auf Root und Stützen;
- Eigenzeitfehler auf allen tatsächlich zeitartig verbundenen Paaren, normiert
  auf die äußere Dauer T=1,5. Bei falsch raumartiger Rekonstruktion wird τ̂=0
  eingesetzt und der Relationsfehler zusätzlich gezählt; kein Ausschluss.

Gleiche Relationslabels allein beweisen keine korrekten Abstände. Diese
Geometriediagnostik verwendet keine verrauschten Feldwerte und bleibt daher
von den Feldrauschwiederholungen getrennt.

## Datenaufteilung und neue Felder

1. Die bisherigen 32 Metadaten-Testwolken (29 vollständig) werden jetzt
   ausdrücklich als Entwicklung wiederverwendet. Vier neue ebene Sinus-/
   Kosinuswellen liefern je Variante einen separaten Bias, eine Streuung und
   feste Skalen. Dies sind keine neuen unabhängigen Wolken. Das bisherige
   Metadatenmodell wird nicht neu trainiert; seine ursprünglichen sechs
   Trainingsfelder waren eine andere analytische Familie.
2. Vor der nächsten Datenerzeugung werden vollständiger Code, Vertrag,
   Entwicklungswerte und alle 64 neuen Geometrie-/Rauschseeds öffentlich
   festgeschrieben. Danach exakt 32 neue Kalibrierwolken.
3. Aus deren rauschfreien Fehlern wird genau ein vorab definierter
   Kalibrierfaktor bestimmt. Daten und Faktor werden erneut öffentlich
   eingefroren, bevor die 32 Testwolken erzeugt werden.
4. Jede vollständige neue Wolke erhält vier feste Prüffelder, je 512
   unabhängige synthetische Rauschwiederholungen und eine zusätzliche,
   separat zurückgehaltene verrauschte Messung. Alle Varianten teilen pro
   Wiederholung denselben Eingaberauschvektor. Verschiedene Felder verwenden
   getrennte Rauschfolgen.

Geometrie, Feld und Wiederholung sind unterschiedliche Ebenen. Vier Felder
und 512 Wiederholungen zählen niemals als zusätzliche unabhängige Wolken.
Die Bootstrap-Diagnostik zieht vollständige Wolken samt allen Varianten und
Feldern. Fehlerhafte oder fehlende Supports bleiben mit ihrem Grund erhalten.

Die neuen Startseeds werden unabhängig mit Zurücklegen aus 32 Bit gezogen,
unter Ausschluss der protokollierten bisherigen Wolkenseeds und 0/1/2³²−1.
Neue Duplikate bleiben erhalten; überlappende PRNG-Zustandsfolgen werden
nicht nachträglich ausgesondert. Unabhängige Betriebssystem-Ziehungen sind
eine ausdrückliche Annahme. Separate 128-Bit-Schlüssel erzeugen die
Messrauschfolgen. NumPy-Gaußausgaben approximieren das angenommene
kontinuierliche IID-Modell; eine physikalische Zufallsquellenprüfung erfolgt nicht.

## Kalibrierung der Unsicherheitsintervalle

Aus den Entwicklungswolken werden je Feld/Arm feste positive Skalen berechnet:
`sqrt(mean(e²) + estimated Var(mean(e)))`. Der Bias wird nicht entfernt.
Die geschätzte Unsicherheit des Mittelwerts G/(n−1) wird ausgewiesen und in
diesen Skalen berücksichtigt. Ihre genaue Güte ist für die folgende
Rangkalibrierung nicht Voraussetzung; sie muss vor neuen Kalibrierdaten feststehen.

Für jede vollständige Kalibrierwolke ist der Score das Maximum von
`abs(e_fa)/scale_fa` über alle 4×4 Ausgaben. Mit n vollständigen Wolken
ist k=ceil((n+1)·0,96); q ist der k-kleinste Score. Falls k>n oder n<24,
wird auf ein endliches Intervall verzichtet. Sonst ist der Geometrieanteil
`q*scale_fa`. Unter Austauschbarkeit vollständiger Wolken liefert die
Rangargumentation simultane marginale Überdeckung mindestens k/(n+1).
Die Auswahlbedingung COMPLETE ist vorab festgelegt, rauschunabhängig und
in Kalibrierung/Test identisch. Ausfallraten werden separat berichtet.

Der Messanteil ist `z*sqrt(N_aa(C))`, mit
`z = Φ⁻¹(1−0,01/(2·16))`. Bonferroni erfordert keine Unabhängigkeit zwischen
Varianten. Das Gesamtintervall lautet

    [z_observed − geometry_radius − measurement_radius,
     z_observed + geometry_radius + measurement_radius].

Per Dreiecksungleichung und Vereinigungsabschätzung liegt die simultane
marginale Überdeckung unter den Modellannahmen bei mindestens
`k/(n+1)−0,01 ≥ 0,95`. Das gilt über neue Kalibrier- und Testziehungen,
nicht bedingt auf jede einzelne Wolke oder den realisierten Kalibrierfaktor.
Ein fester Sinus-/Kosinus-Prüfkatalog wird nicht zu einer Garantie für beliebige
unbekannte Felder oder Dichten verallgemeinert. Der Preis breiter Intervalle
wird als eigene Zahl berichtet; Breite wird nicht als Genauigkeit ausgegeben.

## Prüfungen und Entscheidungen vor neuen Daten

Die Messkovarianz wird auf jeder vollständigen Testwolke und jedem Feld
über vier Einzelausgaben und je sechs Summen/Differenzen geprüft. Für
normalverteiltes Rauschen sind standardisierter Mittelwert und skalare
Stichprobenvarianz durch Normal- bzw. Chi-Quadrat-Verteilung geprüft.
Maximal 32·4·16·2=4096 Tests teilen ein Familienfehlerbudget von 0,05.
Algebraisch entartete Richtungen werden mit festen numerischen Grenzen
geprüft. Die Auswertung muss außerdem die zwei absichtlich falschen Modelle
„Rootwert ausgelassen“ und „Kreuzkovarianzen ignoriert“ erkennen.

`CALIBRATION_COMPONENTS_SUPPORTED` verlangt vollständige Ressourcentelemetrie,
alle Daten und Quellnachweise, endliche Kalibrierung, mindestens 26/32
vollständige Testfälle, bestandene Rauschprüfungen und Kontrollen sowie
mindestens 90 % beobachtete gemeinsame Gesamtüberdeckung. Sonst
`CALIBRATION_HOLD`. Dies ist ein endlicher Pilotentscheid; 32 Testwolken
können 95%-Populationsüberdeckung nicht präzise empirisch zertifizieren.
Die drei Überdeckungsquoten erhalten zusätzlich simultane exakte binomiale
Konfidenzintervalle mit Gesamtfehlerniveau 0,05. Eine untere Grenze unter
95 % wird ausdrücklich als offene empirische Zertifizierung ausgewiesen.
Paare von RMSE-Verhältnissen und das frühere 5%-Verbesserungsziel werden
diagnostisch berichtet; sie ändern keine alte Entscheidung und wählen keinen Arm.

Je Phase vier Prozesse mit acht Wolken; maximal 1800 Sekunden und 2048 MiB
je Prozess, ein BLAS-Thread. Kein Nachziehen oder Ersetzen. Jeder Datensatz
und Laufzeit-/Speicherstand wird sofort gespeichert. Fehler bleiben erhalten
und verhindern die Freigabe des Kalibrierpiloten. Koordinaten und Rauschvektoren
sind aus den Seeds reproduzierbar; archiviert werden vollständige
Selektions-/Gewichtsdaten, wahre Stützkoordinaten, alle entscheidungsrelevanten
Rauschstatistiken, die zusätzliche Messung und Bytehashes der Rauschfolgen.
Keine Behauptung, alle Eingaberauschvektoren als Rohdateien zu speichern.

Der Replay regeneriert identische Daten, prüft Stützkoordinaten komponentenweise,
Gewichte, neue Felder, Kovarianzen, Intervalle und Entscheidungen mit
vorab festgelegten Toleranzen. Bytehash-Übereinstimmung wird separat berichtet.
Keine Wiederholung der teuren vollständigen Rahmensuche und keine externe Replikation.

**Unverändert: HOLD_PHASE3 und HOLD_EMBEDDING_COVARIANCE.** Keine neue
Kalman-Gewichtung, kein Filtervergleich, keine Krümmungs-, Online- oder Gerätefreigabe.

## Primärquellen

- [JCGM 100:2008](https://www.bipm.org/documents/20126/2071204/JCGM_100_2008_E.pdf):
  systematische Beiträge, Unsicherheit und korrelierte Eingangsgrößen.
- [Angelopoulos & Bates, Split-Conformal-Grundlagen](https://arxiv.org/abs/2107.07511):
  Rangquantil, Austauschbarkeit und Grenzen marginaler Überdeckung.
- [Vorhandene Einbettungskovarianz-Abgrenzung](../metadata_bias/EMBEDDING_COVARIANCE_AUDIT.md).

Diese Quellen begründen die Methoden, nicht die empirische Qualität unseres Operators.
