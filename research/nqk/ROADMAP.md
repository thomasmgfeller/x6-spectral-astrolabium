# NQK-Roadmap 0.1

Stand: 12. Oktober 2026. Planung eines eigenständigen Forschungszweigs auf Basis
der [Forschungsfassung 2.0](baseline/NQK_Forschungsfassung_2_0.pdf).
Die Meilensteine bezeichnen Arbeitspakete, keine zugesagten Termine.

## Reihenfolge und Status

| Meilenstein | Ergebnis | Abhängigkeit | Stand |
| --- | --- | --- | --- |
| M0 — Forschungsstand festhalten | Bericht, Roadmap, Grenzen, Quellen und zukünftige Funktionskandidaten | Forschungsfassung 2.0 | Dossier erstellt; bisherige Befunde intern geprüft |
| M1 — Eigenständige Reproduktionsbasis | NQK-Kern, Datenvertrag, Referenzfälle, unabhängige Kontrollen | M0 | Geplant; nächster Arbeitsschritt |
| M2 — Lorentzscher Anschluss | Endliche Kausalordnung, Zeitseparation, unterscheidbare Gegenmodelle | M1 | Geplant; erste Forschungspriorität |
| M3 — Quanteninformation und Informationsverlust | Vergleich von Paaren, zusätzlichen Observablen und globaler Information | M1 | Geplant; eigener ergänzender Arbeitsstrang |
| M4 — Endliche Messdaten und Robustheit | Quantifizierte Unsicherheit, Fehler- und Verlustmodelle, danach reale Referenzen | M3; für kausale Aussagen zusätzlich M2 | Geplant |
| M5 — Transfer ausgewählter Funktionen | Separat qualifizierte Adapter für Astrolabium oder künftige Module | Je Funktion ihre eigenen Nachweise; siehe Featurekatalog | Nur Option; noch nicht zur Umsetzung freigegeben |

M2 und M3 können fachlich unabhängig bearbeitet werden. Bei begrenzter Kapazität
folgt nach M1 zunächst M2. M5 verlangt keinen Abschluss der gesamten Forschung:
eine eng begrenzte Metrikdiagnose kann früher qualifiziert werden als ein
Messdatenmodul. Diese Roadmap startet keine automatischen oder zeitgesteuerten Läufe.

## M0 — Dokumentierte Ausgangslage

**Lieferumfang:** Dieses Dossier, unveränderter Forschungsbericht, maschinenlesbare
Zusammenfassung und Prüfsummen der bisherigen Archive.

Der Bericht trennt die neue synthetische Serie, deren Robustheitsuntersuchung
und das kleine Quantenmodell von den nicht auffindbaren historischen Tests.
Die 171 Abschlussprüfungen betreffen Konsistenz und Archive; sie sind keine
weiteren wissenschaftlichen Produktionsläufe. Öffentliche Code-Reproduktion
und unabhängiges fachliches Review bleiben gesonderte Aufgaben.

**Abschluss:** Dokumente sind verlinkt, Zahlen stimmen mit dem Bericht überein,
der Veröffentlichungsumfang ist verifiziert. M0 bestätigt keine Theorie.

## M1 — Unabhängig ausführbarer NQK-Kern

**Frage:** Kann eine andere Person die ausdrücklich benannten Befunde ohne die
Astrolabium-Oberfläche und ohne die ursprüngliche Arbeitsumgebung reproduzieren?

**Liefergegenstände:**

- Kontrollierte Übernahme der vier vorhandenen Prüfpakete mit ihren originalen
  Protokollen, Ergebnissen und Herkunftsnachweisen; Altstände bleiben erkennbar.
- Separater Python-Kern für Gewichte, Distanzabbildungen, Dreieckszeugen,
  Einbettungsdiagnose und Berichtsexport. Abhängigkeiten und Laufbefehle festhalten.
- Ein gemeinsamer Eingabevertrag mit Knotenbedeutung, Gewichtsfunktion, Dimension,
  Normierung, Einheiten, Nullwertregeln und numerischen Toleranzen.
- Kleine feste Kontrollsuite: metrische und nichtmetrische Matrizen, Nullgewichte,
  Maximalgewichte, nichtverbundene Netze, relabelte Eingaben sowie Fälle mit
  guter Clusterrekonstruktion trotz Metrikverletzung.

**Freigabe G1:** Frischer Checkout reproduziert alle festgelegten kleinen
Kontrollbefunde. Kleine Dreiecksprüfungen werden vollständig und durch einen
separat implementierten direkten Vergleich geprüft. Eingangsdaten und abgeleitete
Wegmatrizen bleiben getrennt. Gespeicherte Produktionsfälle werden nach einem
vorab festgelegten Plan reproduziert; Abweichungen erhalten einen Fehlerbericht.
Numerische Toleranzen werden vor den Läufen pro Grösse festgelegt und begründet.

**Stoppregel:** Fehlende Herkunft, nicht erklärbare Ergebnisabweichungen oder
unbeabsichtigtes Überschreiben von Referenzen stoppen die Freigabe. Ein Fehler
darf nicht durch nachträgliche Änderung des Sollwerts verborgen werden.

## M2 — Lorentzsche Struktur als eigener Prüfgegenstand

**Frage:** Welche zusätzliche Information liefert eine explizite gerichtete
Kausalstruktur gegenüber symmetrischen Gewichten und Spektren?

**Erster Umfang:** Endliche kausale Ordnungen mit 3–5 Elementen und wohldefinierten
Gegenkontrollen. Die im Astrolabium vorhandene kleine Ordnungsstudie dient als
versionierte Referenz; ihr Code, ihre Agenten und ihr Zeitfenster werden nicht
durch NQK verändert. Siehe [Quellenstand](REFERENCES.md).

**Liefergegenstände:** Definition von strikter Ordnung, Transitivität, Richtung,
Zeitseparation und Operatoren; exakte kleine Ordnungsfälle; dokumentierte
Spektralkollisionen; Vergleich mit Zeitumkehr und zusätzlicher gerichteter
Information. Für ein erstes diskretes Modell kann die längste Kette in Kanten
als Zeitseparation gewählt werden; diese Wahl ist eine Modellkonvention und
noch keine kalibrierte Eigenzeit.

**Freigabe G2:**

- Ordnungsaxiome und Relabeling-Invarianz bestehen alle kleinen Kontrollfälle.
- Bei einem Modell mit längster Kette gilt für geordnete Tripel die zugehörige
  umgekehrte Dreiecksrelation; auch absichtlich ungültige Eingaben werden geprüft.
- Spektral gleiche, aber nicht isomorphe Ordnungen werden als mehrdeutig erhalten.
  Isomorphieentscheidungen der kleinen Fälle werden unabhängig exakt kontrolliert.
- Eine behauptete Verbesserung durch Zusatzinformation wird auf allen vorab
  festgelegten Fällen berichtet, einschliesslich verbleibender Kollisionen.

**Stoppregel:** Symmetrische Log-Distanzen werden nicht als Zeitseparation
umetikettiert. Eine übergebene Ordnung zählt nicht als aus Quantenkorrelationen
hergeleitete Ordnung. Eine Brücke zwischen Zustandsdynamik und Kausalstruktur
braucht eigene Annahmen und Gegenprüfungen.

**Späterer Horizont:** Erst danach Grössenfolgen, korrekte dimensionsabhängige
Operatoren, Skalierung, begründete Cutoffs und Konvergenzbegriffe untersuchen.
Ein mLGH-/Kontinuumslimes, eine vierdimensionale Dominanz und eine Dynamikherleitung
sind offene Fernziele mit eigenen Beweisaufgaben.

## M3 — Quanteninformation jenseits der Paarmatrix

**Frage:** Welche Zustandsänderungen bleiben einer Paaranalyse verborgen, und
welche zusätzlichen Observablen helfen für eine präzise definierte Zielaufgabe?

**Liefergegenstände:** Zustände und Subsysteme vor den Gewichten festlegen;
Hermitizität, Spur und Positivität kontrollieren; MI und Negativität getrennt
auswerten. GHZ, separable Mischung, W, Produkt-, Bell- und Graphzustandskontrollen
bilden einen dokumentierten Vergleichskorpus. Zusätzliche Pauli-Observablen oder
höhere Randzustände erhalten einen expliziten Messaufwand.

**Freigabe G3:** Die bekannten GHZ-/Mischungs- und Fünferzyklus-Gegenbeispiele
werden reproduziert. Die notwendige Qubit-Schranke für E=I/2 wird korrekt
verwendet: Verletzung verwirft diese Deutung; Bestehen beweist keine globale
Kompatibilität. Zusatzobservablen müssen die beanspruchte Unterscheidung auf
den festgelegten Kontrollen tatsächlich leisten. ⟨XXX⟩ allein wird nicht als
allgemeiner Verschränkungsnachweis ausgegeben.

**Stoppregel:** Ein negatives Paar-Verschränkungsergebnis darf globale
Verschränkung nicht ausschliessen. Ein neuer Zustandsraum oder eine neue
Normierung erfordert einen neuen Modellvertrag und neue Kontrollen.

## M4 — Unsicherheit, Drift und Messbezug

**Frage:** Welche Diagnosen bleiben bei endlicher Stichprobe und realistischen
Fehlern aussagekräftig, und wann muss das Ergebnis unentschieden bleiben?

**Liefergegenstände:** Festgelegte Modelle für endliche Zählstatistik,
Präparations- und Messfehler, Achsenfehler, Drift, Detektorverluste und fehlende
Daten; getrennte Auswertung von Rekonstruktionsfehler und Unsicherheit.
Danach ein datensparsamer Pilot mit unabhängig aufgenommenen Referenzdaten,
Kalibrierung, Einheiten und Unsicherheitsbudget.

**Freigabe G4:** Vor Produktion Zielgrössen, zulässige Fehlalarm- und
Übersehensraten, Stichprobenzahlen, Abhängigkeiten und Mehrfachvergleiche
festlegen. Empirische Intervallabdeckung und Fehlerraten werden mit eigenen
Unsicherheitsintervallen berichtet; die entscheidungsrelevante Obergrenze muss
unter dem vorab gewählten Grenzwert liegen. Fehlende Evidenz führt zu
INCONCLUSIVE. Simulationsbefunde und reale Daten bleiben getrennt gekennzeichnet.

**Stoppregel:** Unmodellierte Selektion/Verluste oder unqualifizierte
Kalibrierdaten verhindern einen Messanspruch. Eine physikalische Projektion
einer geschätzten Dichtematrix darf Unsicherheit und Schätzverzerrung nicht verbergen.

Der vorhandene photonische Zwei-Qubit-Entwurf wäre ein möglicher späterer
Partner für Zweiqubit-Tomografie. Er liefert keine GHZ-Dreiqubit-Messung;
diese benötigt einen eigenen Versuchsaufbau. Hardwaresteuerung ist nicht Teil
der vorliegenden Roadmap-Freigabe.

## M5 — Kontrollierter Transfer

**Ziel:** Einzelne bestandene NQK-Funktionen können künftig als optionales
Astrolabium-Modul oder als gemeinsame Prüfkomponente übernommen werden.
Die Forschungsmodelle und ihre Veröffentlichungen bleiben eigenständig.

**Freigabe G5:** Je Funktion müssen fachliche Vorbedingungen aus dem
[Featurekatalog](FEATURES_ASTROLABIUM.md), ein versionierter Datenvertrag,
unabhängige Referenzkontrollen, Grenzfalltests, Ressourcenlimits und vollständige
Ergebniswiederholung erfüllt sein. Für einen Browseradapter kommen echte
Import-/Export-, Sprach-, Mobil- und Fehlerzustandsprüfungen hinzu. Bestehende
Astrolabium-Prüfungen müssen am konkreten Integrationscommit bestehen.

Transfer geschieht über einen eigenen späteren Änderungsauftrag und Pull Request.
Ein NQK-Ergebnis wird nicht allein durch die Einbettung in Astrolabium gültiger.
Mathematische, numerische und empirische Nachweise erhalten getrennte Statusfelder.

## Arbeitsregeln für alle Meilensteine

Vor jedem neuen Produktionslauf: Frage und Null-/Gegenmodell, Datenauswahl,
Parameterraum, unabhängige Auswertungseinheiten, Toleranzen, Erfolgs- und
Abbruchkriterien sowie Rechenbudget versioniert festlegen. Danach Ergebnisse
vollständig archivieren, negative Resultate erhalten und Planänderungen als
neue Version kenntlich machen. Explorative Läufe werden als explorativ geführt.
Neue Seeds allein machen einen Lauf nicht zu einer unabhängigen Implementierung.
