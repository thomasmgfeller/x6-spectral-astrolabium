# X6 Neutral Discovery — Gesetzeskandidaten, Generatoren, Geometrie, Theorie

**Status: ausführbare, endliche Softwarekontrolle; keine entdeckte physikalische Theorie.**
X6 sucht die nächste zulässige Intervention, deren Ergebnis voraussichtlich am
meisten zwischen den noch möglichen Erklärungsklassen unterscheidet. Eine
bestimmte Geometrie ist kein Optimierungsziel. **Lorentz darf Kandidat sein,
aber weder Zielfunktion noch Erfolgsbedingung.** Dasselbe gilt für jede Alternative.

Diese Erweiterung baut auf dem [Experiment Fabric](../experiment_fabric/README.md)
und dem [mehrschichtigen Fingerprint](../../research/fingerprint_v1/README.md) auf.
Sie enthält einen endlichen Gesetzessucher, drei kausale Generatoren, einen
Klassenplaner, einen Adapter zum bestehenden JS-Planer und ein separates
Widerlegungsgate. Die Geometrie- und Theoriephasen sind hier spezifiziert, noch
nicht als allgemeine Entdeckungsalgorithmen implementiert.

## 1. Die Forschungsfrage und die Entscheidung

Für Daten D, Erklärungsklasse C und einen zulässigen Interventionsbatch B gilt:

    B* = argmax_B I(C; Y_B | D, do(B))

unter vorab festgelegten Grenzen für Kosten, Dauer, Eingriffsstärke,
Gerätefähigkeit, Probenzustand und Kalibrierung. C ist eine Erklärungsklasse,
nicht ein gewünschtes Ergebnis und nicht nur ein freier Parameter. Der
allgemeine Prädiktor muss Parameter und Störgrössen integrieren:

    p(y | C, do(B), D) = integral p(y | theta, C, do(B)) p(theta | C, D) dtheta

Gemeinsame Störgrössen und Probenabhängigkeiten gehören in die gemeinsame
Verteilung. Informationswerte einzelner Nodes dürfen nicht einfach addiert
werden. Die bestehende Fabric modelliert persistente latente Zustände; diese
kleinere Referenz verwendet feste Generatoren und unabhängige Replikate.

Es gibt zwei verschiedene Entscheidungen:

- **Unterscheiden:** erwartete Information zwischen Erklärungsklassen maximieren.
- **Angreifen:** registrierte Eingriffe priorisieren, die bei relevanten
  Alternativen eine hohe Wahrscheinlichkeit haben, den Favoriten zu verwerfen.

Auch ein Favorit mit Gewicht 1 braucht externe Gegenhypothesen, Kontrollen und
Prüfungen seiner absoluten Vorhersagen. EIG=0 bei nur einer verbleibenden Klasse
bedeutet nicht, dass eine Theorie bewiesen ist. Sind alle Kandidaten verworfen,
lautet das Ergebnis `MODEL_SET_INADEQUATE`; die Suche muss erweitert werden.

## 2. Vom Gesetz zu den Generatoren, dann zur Geometrie und Theorie

Die Schritte sind Evidenzanforderungen mit Rückkopplung, keine automatische
Beförderung. In manchen Problemen sind geometrische und dynamische Annahmen
nur gemeinsam identifizierbar. Dann bleiben sie gekoppelte Kandidaten.

| Schritt | Was X6 erzeugt | Was den nächsten Anspruch rechtfertigt | Möglicher Rückschritt |
|---|---|---|---|
| Gesetzeskandidat | Kompakte Relation mit Einheiten, Gültigkeitsbereich, Residuen und Unsicherheit | Vorhersage auf zurückgehaltenen Daten und veränderten Bedingungen; Stabilität gegenüber Messfehlern und Darstellungswahl | Überanpassung, Einheitenfehler, Bereich zu eng |
| Generator | Zustände, Mechanismus bzw. Evolutionsregel, Anfangs- und Randbedingungen, Interventionssemantik und Messabbildung | Unterschiedliche Generatoren machen quantitative, überprüfbare Antworten auf denselben Eingriff | Mehrere Mechanismen bleiben ununterscheidbar; Katalog unvollständig |
| Geometriekandidat | Relationale, metrische, kausale oder andere Struktur samt operativer Messzuordnung | Unabhängige räumliche, zeitliche, sektorielle und Transformationsvorhersagen; Kontrolle von Koordinaten- und Eichfreiheit | Struktur nicht identifizierbar, nur effektiv oder nicht geometrisch |
| Theoriepaket | Gesetze, Generator, gegebenenfalls Geometrie, Annahmen, Parameter und neue quantitative Vorhersagen | Gemeinsam konsistente Vorhersagen in mehreren vorab definierten Regimen mit erklärter Unsicherheit | Nachträgliche Zusatzannahmen erfordern neue Version und neue Prüfdaten |
| Widerlegungsgate | Gezielte Gegenversuche, Negativkontrollen, externe Replikation, Bereichswechsel | Alle obligatorischen Prüfungen abgeschlossen; kein registriertes Ausschlusskriterium getroffen | Einzelkandidat fällt oder gesamter Modellraum ist unzureichend |

**Generator** meint hier einen Mechanismus, der Beobachtungen unter Eingriffen
vorhersagt. Ein Zeitentwicklungsoperator, ein stochastischer Generator und ein
infinitesimaler Symmetriegenerator sind verschiedene mathematische Objekte.
Der Typ und seine Domäne müssen angegeben werden. Aus einem Generator folgt
nicht ohne zusätzliche Voraussetzungen eine eindeutige Geometrie.

Ein nicht verworfenes Theoriepaket ist `NOT_REJECTED_WITHIN_TESTED_DOMAIN`,
niemals `TRUE`. Eine nicht geometrische Erklärung bleibt zulässig. Der
Fingerprint liefert Beobachtungen und Trennzeugen; er ersetzt nicht die
Messabbildung eines Generator- oder Geometriemodells.

## 3. Lorentz-Neutralität als Vertrag

Vor Datenerhebung und Entblindung werden festgelegt:

1. Variablen, Einheiten, Auflösung, Messkanal und erlaubte physische Eingriffe.
2. Kandidatengrammatik, Zulassungskriterien, Komplexitätsmass, Rechenbudget,
   Klassenbildung und Prioren. Alternativen erhalten dieselben Zugangsregeln.
3. Likelihood, Messfehler, Störgrössen, Probenabhängigkeit und Gültigkeitsbereiche.
4. Trennziel, Gleichstandsregel, Kosten und Abbruchbedingungen.
5. Datenteilung, Challenge-Katalog, Ausschlussschwellen und Fehlerbudget.

Der Planer erhält Vorhersagen und neutrale Klassenkennungen. Historische Namen
und interpretative Zuordnungen befinden sich ausserhalb seines Eingangs.
Der geschlossene Referenzvertrag erlaubt kein Feld für Zielgeometrie,
Lorentz-Bonus, gewünschte Signatur oder bevorzugte Theorie. Ein blosses Umbenennen
von Kandidaten oder Vervielfältigen ihrer Schreibweisen erzeugt keinen Vorteil.

**Blindheit ist keine Garantie voraussetzungsloser Forschung.** Messgrössen,
Grammatik, Prioren und Modellraum können das Ergebnis bereits vorprägen. Deshalb
müssen sie veröffentlicht und auf Sensitivität geprüft werden. In dieser
endlichen Referenz sind die drei vorab bekannten, verschiedenen Klassen gleich
gewichtet; das ist eine deklarierte Wahl, keine universell neutrale Prior.
Identische Vorhersagen werden vor Vergabe der Klassenprior zusammengefasst.
Eine spätere Erweiterung um neue Klassen ist eine neue Kampagne mit neuem
Vertrag und neuem Fehlerbudget, kein heimliches Nachjustieren.

Für reale Geometrieforschung wären unter denselben Zugangsregeln zum Beispiel
lorentzsche, galileische, bevorzugt gerahmte, anisotrope, effektive und nicht
metrische Erklärungen zu formulieren. Diese Namen allein sind keine testbaren
Modelle. Jede Klasse braucht eine quantitative Messabbildung, einen definierten
Bereich und unterscheidbare Vorhersagen. Ein Lorentz-Kandidat darf bestehen,
scheitern oder ununterscheidbar bleiben. Ein einzelnes Spektrum, eine endliche
Ausbreitungsgeschwindigkeit oder ein guter Fit identifiziert keine Lorentz-Geometrie.

Die früheren Lorentz-spezifischen Atlasprüfungen dieses Repositories untersuchen
einen ausdrücklich eingeschränkten Modellraum. Sie sind keine neutrale Auswahl
zwischen sämtlichen Geometrien und kein Nachweis, dass Lorentz entstanden ist.
Die neue Discovery-Zielfunktion bewertet keinen Abstand zu einem Lorentz-Zielbild.

## 4. Ausführbare Kontrolle: gleiche Relation, andere Generatoren

Aus der vollständigen binären Beobachtungsstütze `(0,0), (1,1)` enumeriert
`law_candidates` affine Ausdrücke `c + a X + b Y = 0` mit Koeffizienten aus
`{-1,0,1}`. Nach Entfernung von Nullausdruck, Vielfachen und Vorzeichenvarianten
bleibt `X - Y = 0`. Das ist eine Relation auf der registrierten Stütze, noch kein
physikalisches Gesetz.

Drei Generatoren aus einer expliziten endlichen Grammatik sind damit vereinbar:

| Generator | Beobachtung ohne Eingriff | `do(X=1)`: P(Y=1) | `do(Y=1)`: P(X=1) |
|---|---|---:|---:|
| X=U, Y=X | X=Y | 1 | 1/2 |
| Y=U, X=Y | X=Y | 1/2 | 1 |
| X=U, Y=U | X=Y | 1/2 | 1/2 |

U ist pro Replikat ein neuer fairer binärer Zufallswert. Ein `do`-Eingriff ersetzt
die Gleichung der betroffenen Variablen; er ist keine Auswahl von Beobachtungen
mit passendem X oder Y. Alle Grössen sind dimensionslos. Die Simulatoren bilden
keine reale Aktuatorik und keine Raumzeit ab.

Die Klassenbildung verwendet exakte rationale Vorhersagen für den gesamten
registrierten Katalog. Gleichheit auf diesem Katalog ist eine Äquivalenzrelation;
sie behauptet keine physikalische Gleichheit ausserhalb dieses Katalogs.
Keine Epsilon-Nähe wird zu einer transitiven Äquivalenz erklärt.

Bei gleichen Prioren wählt der erste Batch `do(X=1)` und `do(Y=1)` auf getrennten
Replikaten: rund **0,491678 Bit** erwartete gemeinsame Klasseninformation.
Passive Wiederholungen liefern hier keine Klasseninformation. In drei
veröffentlichten Kontrollen mit je einem anderen wahren Simulator überlebt nach
dem Challenge-Gate jeweils nur dessen Klasse. Diese kleinen positiven Kontrollen
messen keine allgemeine Entdeckungsleistung und keine Power über alle Alternativen.

## 5. Das Gate darf den Favoriten verwerfen

Die Referenz fixiert vor den Challenge-Daten **24 neue Beobachtungen pro Eingriff**,
beide Eingriffe, alle drei Klassen und genau einen Auswertungszeitpunkt. Sie nutzt
einen exakten zweiseitigen Binomialtest nach Wahrscheinlichkeitsordnung.
Das gemeinsame Fehlerbudget ist alpha=0,05; Bonferroni liefert die Schwelle
`alpha / (3 Klassen * 2 Eingriffe) = 1/120` pro Test.

Unter den registrierten festen Nullwahrscheinlichkeiten und den angenommenen
i.i.d.-Replikaten ist die Wahrscheinlichkeit, mindestens eine wahre registrierte
Null zu verwerfen, höchstens alpha. Das ist weder die Wahrscheinlichkeit, dass
eine überlebende Klasse falsch ist, noch ein Fehlerbudget für unbegrenzt viele
später gestartete Kampagnen. Für Parameterschätzung, Drift und adaptive
Zwischenanalysen muss ein eigener gültiger Testvertrag entwickelt werden.

`challenge_order` priorisiert nach erwarteter Verwerfungswahrscheinlichkeit des
aktuellen Favoriten unter den gewichteten Alternativen. Alle sechs registrierten
Tests bleiben obligatorisch; Reihenfolge und Posterior ändern weder N noch
Schwelle. In einem ausdrücklich konstruierten Stresstest erhält ein Kandidat
zuerst über 99 % Gewicht und fällt anschliessend am gleichen Gate wie jeder andere.
Eine zweite Negativkontrolle verwirft sämtliche Klassen. Ein niedriger Posterior
allein ist kein statistischer Ausschluss; das Gate prüft auch Klassen mit Gewicht 0.

Weitere Kontrollen prüfen Vertragsänderungen nach Freeze, Daten-IDs aus der
Lernphase, doppelte IDs, falsche Bindung, vorzeitige Auswertung und zweiten Look.
Der Gatezustand ist derzeit **nur im Speicher**. Neue IDs beweisen keine neue
Messung; Hashes beweisen weder Urheberschaft noch zeitliche Präregistrierung.
Ein Produktionssystem braucht ein dauerhaftes unabhängiges Evidenzregister,
Akquisitionsidentitäten, gespeicherte Gateverbräuche und kontrollierte Zugriffe
auf zurückgehaltene Daten. Ein Neustart dieser Demo ist keine neue unabhängige
wissenschaftliche Prüfung.

## 6. Die verteilte Fabric und physische Interventionen

Der Koordinator friert Vertrag, Klassen und gemeinsame Vorhersageverteilung ein.
Der Planer weist unterschiedlichen Nodes komplementäre Eingriffe zu. Jeder Node
liefert Eingriff, tatsächliche Aktuatorwerte, Rohdaten, Proben- und
Kalibrieridentität sowie Quality Flags. Gemeinsame Drifts und gekoppelte Proben
werden gemeinsam modelliert. Erst vollständige, gültige Evidenz aktualisiert
die Klassen. Eine Wiederzustellung ist keine weitere Replikation.

| Rolle | Aufgabe | Grenze |
|---|---|---|
| Browser | Planung, Inspektion, Visualisierung und freigegebene Aufträge | Keine zeitkritische Gerätesteuerung |
| Vorschlagsagent | Gesetzes- und Generatorkandidaten im registrierten Suchraum erzeugen | Keine Änderung von Prüfdaten, Fehlerbudget oder Erfolgsdefinition |
| Planer | Gemeinsamen Informationsgewinn zulässiger Batches bewerten | Kein Zielmodell und keine angenommene wahre Klasse als Eingang |
| Messnode | Kalibrierten Eingriff ausführen und Rohdaten protokollieren | Keine selbst erfundene Beobachtung oder stillschweigende Parametervariation |
| Widerlegungsinstanz | Gegenversuche aus registriertem Katalog und separate Prüfung | Kein nachträgliches Reparieren des Favoriten auf denselben Prüfdaten |

Ein möglicher physischer Einstieg ist ein mechanischer Prüfstand. Kandidaten
wie lineare Feder, amplitudenabhängige Steifigkeit, geschwindigkeitsabhängige
Dämpfung und ein zusätzlich gekoppelter Freiheitsgrad müssen jeweils die
**gemessene Kraft und Antwort** vorhersagen. Eingriffe wären kontrollierte
Anregungsamplitude, Frequenz, Zusatzmasse, Kopplung oder Randbedingung. Die
Anregung muss innerhalb vorab qualifizierter Grenzen liegen. Das ist ein
vorgeschlagenes Experimentprofil, kein bereits angeschlossenes Gerät.

Der bisherige Modalpilot liefert mit Kraftreferenz und zwei synchronen
Antwortkanälen einen Einstieg für Generatorvergleiche. Für geometrische Aussagen
kommen kalibrierte Positionen, Zeitbezüge und gezielt variierte Messanordnungen
hinzu; die nötige Zahl der Sensoren hängt von den zu trennenden Kandidaten ab.
Ein Softwareparameter, eine Koordinatentransformation oder ein weiterer Worker
ist für sich kein physischer Eingriff und keine unabhängige physische Replikation.

## 7. Nächste Umsetzungsschritte und konkrete Gates

| Paket | Ergebnis | Freigabekriterium |
|---|---|---|
| A — Referenz, hier umgesetzt | Endliche Gesetzessuche, Generatortrennung, EIG, neutrales Ausschlussgate | Reproduzierbare Kontrollen, Gegenbeispiele und unabhängiger Planerabgleich |
| B — Physischer Generatorbenchmark | Kalibrierter Aktuator-/Sensoradapter, Gerätemodell, Rohdaten und dauerhafter Evidenzspeicher | Eingriff beobachtbar; Störgrössen erfasst; gleiches Budget gegen zufällige und feste Messpläne |
| C — Generatorensuche | Einheitengeprüfte dynamische Grammatiken; Parameterunsicherheit und Messkanal; Kandidatenversionen | Vorhersagen für zurückgehaltene Eingriffe; keine Wiederverwendung von Challenge-Daten als Test |
| D — Geometrievergleich | Operativ definierte relationale und geometrische Kandidaten einschliesslich nicht geometrischer Alternativen | Neue, unterscheidende Vorhersagen; Blindregeln und Sensitivität gegenüber Modellraum/Prior |
| E — Theorie und Gegenversuch | Bereichsübergreifendes Theoriepaket, unabhängige Replikation und Gegenhypothesen | Alle obligatorischen Prüfungen abgeschlossen; Fehlerbudget über Kampagnen kontrolliert |

Die neue Fähigkeit ist zunächst **messbare Trennung konkurrierender Erklärungen**.
Ob daraus eine neue physikalische Struktur entsteht, entscheidet erst die Evidenz.

## 8. Ausführen und Prüfen

Im Repository-Wurzelverzeichnis; Python mit `jsonschema` und Node >=22:

```bash
python -m unittest discover -s experimental/neutral_discovery/tests -p 'test_*.py' -v
python experimental/neutral_discovery/discovery.py verify experimental/neutral_discovery/examples/control.json
python experimental/neutral_discovery/discovery.py run /tmp/x6-discovery-new.json
python experimental/neutral_discovery/discovery.py fabric /tmp/x6-discovery-campaign-new.json
```

`run` und `fabric` überschreiben keine bestehende Datei. `verify` reproduziert
alle veröffentlichten Kontrollen. Der Adapter liefert Eingaben für den bestehenden
JS-Informationsplaner; der mechanikspezifische Fabric-Executor akzeptiert dieses
Profil nicht. Diese Erweiterung startet weder echte Nodes noch Hardware.
Die Planerprüfung vergleicht alle neun binären Zweierbatches und alle zugehörigen
Ausgänge mit der getrennten JS-Implementierung. Das ist algorithmische
Gegenprüfung innerhalb dieses Projekts, kein unabhängiges externes Review.

Dateien: `discovery.py`, `contract.schema.json`, `build_schema.py`,
`tests/test_discovery.py`, `examples/control.json`, `VALIDATION.md`.

## Methodische Quellen

- Schmidt & Lipson (2009), *Distilling Free-Form Natural Laws from Experimental
  Data*, Science, DOI [10.1126/science.1165893](https://doi.org/10.1126/science.1165893).
  Symbolische Gesetzeskandidaten und zurückgehaltene Validierung; Variablenwahl
  und Ausdrucksgrammatik beeinflussen, welche Beziehungen gefunden werden.
- Hauser & Bühlmann (2012/2014), *Two Optimal Strategies for Active Learning of
  Causal Models from Interventional Data*, [arXiv:1205.4174](https://arxiv.org/abs/1205.4174).
  Eingriffe können beobachtungsäquivalente kausale Modelle unterscheiden, unter
  den jeweiligen Modellannahmen. Unsere binäre Softwarekontrolle ist eine eigene
  endliche Demonstration, keine Implementierung sämtlicher Verfahren des Papers.
