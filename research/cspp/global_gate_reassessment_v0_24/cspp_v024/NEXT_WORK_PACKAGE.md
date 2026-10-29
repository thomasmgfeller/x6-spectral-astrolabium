# Nächster Arbeitsauftrag nach v0.24

29. Oktober 2026. Dieser Auftrag ist vorbereitet, noch nicht ausgeführt.
Schritt 3, die Neubewertung nach der vollständigen globalen Bilanz, ist
abgeschlossen. METHOD und G1 bleiben HOLD; frische Bestätigungsdaten
werden weiterhin nicht erzeugt.

## 1. Primär: deterministischer skalarer Kandidat und Stabilität

Die unveränderte Operatorzelle allein durch größere Vergangenheitsdiamanten
zu reparieren, scheitert bereits am notwendigen Gauß-Zeugen aus v0.15.
Deshalb ist als nächster Hauptweg ein ausdrücklich geänderter skalarer
Kandidat zu entwickeln und deterministisch zu prüfen.

Vor der Rechnung sind die Kandidatenidentität, Quelle, Detektor, physikalische
Skalen, Normierung und zulässigen Änderungen festzuhalten. Änderungen an
q, epsilon oder Schichtkoeffizienten sind neue Kandidaten und keine bloße
Verbesserung einer Fehlerabschätzung. v0.24 wählt keine Parameter und kein
Suchgitter. Die vorhandenen Archive sind Entwicklungsdaten.

Für jeden Kandidaten sind zunächst die notwendigen Kontrollfelder mit
validierter Arithmetik zu prüfen: Normierung, Kontinuumsvoraussetzungen,
der bisherige Gauß-Zeuge und der konkrete kompakte KG-Detektor. Ein
Kontroll-PASS ersetzt keinen Gesamtfehlernachweis. Frühere H1- und PU-H1-
Adapter dürfen nicht stillschweigend durch die volle KG-History ersetzt
werden; eine Änderung der Eingabeabbildung gehört in die Definition.

Zusätzlich sind Retardierung, Definition für das deklarierte Ensemble
und Stabilität des resultierenden Propagators zu untersuchen. Die
Mittelwertgleichung allein ist kein Beweis für das Verhalten des mittleren
inversen Propagators. Das neue L1-Zertifikat ist keine dichteuniforme
Stabilitätsaussage.

Der erste konkrete Liefergegenstand ist eine reproduzierbare
Kandidatenspezifikation mit notwendigen Kontroll- und Stabilitätsergebnissen,
einschließlich begründeter Abbrüche. Ohne ausreichende Ergebnisse wird
kein statistisches Bestätigungsdesign begonnen.

## 2. Optional: Attribution im unveränderten bisherigen Modell

Eine gezielte Fehlerdiagnose des bisherigen Modells kann getrennt
weitergeführt werden. Sie muss das gesamte endliche und unendliche
Außengebiet, direkte und vermittelte Pfade sowie die tatsächlichen
Korrelationen berücksichtigen. Ein später großer Cutoff darf den
dazwischenliegenden Bereich nicht auslassen.

Die nahe Hülle verursacht über 99,9999 % des aktuellen Zertifikats,
aber nicht nachweislich desselben Anteils am physikalischen Fehler.
Auch die unverändert endliche Majorante liegt über dem Ziel. Eine neue
Genauigkeitsfolgerung verlangt daher einen vollständigen verbesserten
Nachweis, gegebenenfalls mit kontrollierten Aufhebungen. Das bloße
Entfernen positiver Zertifikatsterme ist unzulässig.

Dieser Diagnosezweig kann Fehlerursachen eingrenzen. Er hebt die bereits
zertifizierte notwendige Gauß-Verletzung der festen Zelle nicht auf.

## 3. Methodische Zulassung vor jeder Bestätigungsplanung

Ein hinreichend begründeter neuer Kandidat muss alle sechs bestehenden
Kriterien erfüllen: Kontrollreproduktion, totale Ensembleabbildung,
gemeinsame Originalmomente, viertes Moment oder geeignete Tail-Kontrolle,
ensembleweiter numerischer Fehlernachweis sowie Samplinggesetz-Konformität.
Insbesondere sind gemeinsame zweite Momente und Kreuzkorrelationen für
eine Kovarianzvorhersage ausdrücklich zu behandeln.

Erst dann werden Alpha, Power, Stichprobenumfang, Rechenbudget,
Abbruchregeln und öffentliche Vorregistrierung festgelegt. Erst nach
diesem eingefrorenen Design folgen frische Daten. Fluktuations- und
makroskopische Entscheidungen bleiben getrennt.

Ein späterer Auftrag zur GitHub-Publikation betrifft das abgeschlossene
v0.24-Paket; die Veröffentlichung führt diesen neuen Arbeitsauftrag
nicht automatisch aus.
