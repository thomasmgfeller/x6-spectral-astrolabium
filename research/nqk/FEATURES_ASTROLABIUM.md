# Mögliche spätere Astrolabium-Funktionen

Alle zehn Funktionen sind **Transferkandidaten**. Keine davon wird durch dieses
Dossier implementiert oder in der Anwendung aktiviert. Vorhandene NQK-Skripte
sind wissenschaftliche Ausgangsarbeiten, keine abgenommene Produktschnittstelle.
Die Priorität beschreibt den Transfernutzen; die Forschungspriorität liegt bei M2.

| ID | Funktion und konkreter Nutzen | Möglicher Zielbereich | Voraussetzung | Transferpriorität |
| --- | --- | --- | --- | --- |
| F01 | Matrixinspektor mit Gewichtsbedeutung, Dimension, Einheiten, Herkunft und Nullwertregeln; verhindert unbegründete Umdeutungen | Astrolabium Data Bridge oder eigenständiges NQK-Lab | G1 + G5 | Hoch |
| F02 | Metrikdiagnose mit konkreten verletzenden Tripeln, Verletzungshöhe, Vollprüfung/Stichprobe und Nenner; macht Fehler trotz hoher Gesamtquote sichtbar | Graphanalyse oder NQK-Lab | G1 + G5 | Hoch |
| F03 | Vergleich von Rohdistanz, Wegmetrik und euklidischer Einbettung; zeigt veränderte Paare, negative Gram-Eigenwerte und Rekonstruktionsstress | Geometrieansicht eines künftigen Moduls | G1 + G5 | Hoch |
| F04 | Robustheitsvergleich über Störmodelle, Seeds, Randregeln und Skalen; bewertet die Abhängigkeit vom Modell | Signal Validation Lab als spätere Erweiterung | G1 + G5; G4 für Messansprüche | Hoch |
| F05 | Notwendige Kompatibilitätsprüfungen für eindeutig definierte Quantengewichte; verwirft unzulässige Qubit-Zuordnungen mit Zeugen | Künftiges Quantenanalysemodul | G3 + G5 | Mittel |
| F06 | Anzeige von Informationsverlust in Paaren; ergänzt geeignete Mehrteilchenobservablen und Kontrollzustände | Künftiges Quantenanalysemodul | G3 + G5; G4 bei endlichen Messdaten | Mittel |
| F07 | Vergleich zulässiger Quantenkanäle mit Paar- und globalen Kennzahlen; zeigt blinde Flecken von Kohärenzdiagnosen | Simulationsbereich eines Quantenmoduls | G3 + G5 | Mittel |
| F08 | Unsicherheitsbewusste Zustandsrekonstruktion und Zeugen mit INCONCLUSIVE-Status | Spätere Tomografie-/Sagnac-Auswertung | G3 + G4 + G5 | Nach Messvalidierung |
| F09 | Kausalordnungs- und Zeitseparationsdiagnose mit Kollisionskorpus und Zeitumkehrkontrollen | Lorentzsches Forschungsmodul | G2 + G5 | Forschungspriorität hoch; Transfer später |
| F10 | Versionierter Import und Ergebnis-Replay zwischen NQK und Astrolabium mit gemeinsamen Herkunftsfeldern | Gemeinsame Evidenzinfrastruktur | G1 + G5 und Fachfreigabe des jeweiligen Ergebnistyps | Hoch als Voraussetzung für Transfer |

## Was eine Funktion nachweisen muss

**F01:** Ungültige, asymmetrische, unvollständige oder nicht endliche Eingaben
erhalten erklärbare Fehler. Eine klassisch geschätzte Korrelation oder
Kohärenz wird nicht automatisch zu Quanten-MI. Schätzverfahren, Normierung
und gemeinsame Datengrundlage sind Pflichtangaben.

**F02:** Ein hoher K-Wert ersetzt keinen Metriknachweis. Vollprüfung und
Tripelstichprobe werden deutlich getrennt. Eine Stichprobe ohne gefundenen
Fehler wird nicht als globale Erfüllung ausgegeben. Nullabstände und unendliche
Abstände erhalten eine eigene Klassifikation.

**F03:** Wegabschluss und eventuelle Quotientenbildung werden als Transformationen
protokolliert. Euklidische Darstellbarkeit wird separat geprüft. Eine gute
zweidimensionale Darstellung beweist weder die physische Dimension noch eine
lorentzsche Struktur. Rohdaten und abgeleitete Daten bleiben exportierbar.

**F04:** Vergleichsverfahren bekommen dieselben Eingaben und ein vorab festgelegtes
Abstimmungsbudget. Bei Zeitreihen bleibt die zeitliche Abhängigkeit erhalten;
Bootstrap oder Surrogatverfahren benötigen begründete Annahmen. Bessere
Clusterwerte allein belegen keine bessere Signalrekonstruktion. Der bestehende
synthetische Signal-Lab-Vertrag wird nicht stillschweigend auf Messdaten erweitert.

**F05:** Prüfung liefert beispielsweise EXCLUDED oder NOT_EXCLUDED_BY_THIS_TEST;
der zweite Status ist kein Nachweis eines gemeinsamen globalen Zustands.
Geltung der jeweiligen Schranke ist an lokale Dimension und Gewichtsfunktion gebunden.

**F06:** GHZ und separable Mischung müssen trotz gleicher Paardaten getrennt
bewertbar sein, sobald geeignete Zusatzdaten vorliegen. Ohne diese Daten lautet
das Ergebnis unentscheidbar. Die gewählten Zusatzdaten begründen nur die jeweils
definierte Unterscheidung und keine allgemeine vollständige Zustandsrekonstruktion.

**F07:** Kanaldefinition, CPTP-Kontrollen und Subsysteme werden angezeigt.
Der Modellparameter p wird ohne Kalibrierung nicht als Zeit oder Laborrauschstärke
ausgegeben. Eine Rauschsimulation ist keine Rauschunterdrückungstechnik.

**F08:** Endliche Statistik, Messfehler und Verluste gehen in den Geltungsbereich
ein. Punktweise Intervalle werden nicht als simultane Garantie dargestellt.
Zweiqubit- und Mehrteilchenaufgaben bleiben getrennt; der bestehende Sagnac-Entwurf
begründet keinen verfügbaren Dreiqubit-Aufbau.

**F09:** Ordnung, Richtung und Zeitseparation bleiben eigene Datenobjekte.
Gleiche Spektren werden nicht automatisch als gleiche Geometrie behandelt.
Graph-Laplacian-Zertifikate werden nicht auf andere Operatoren übertragen.

**F10:** Hashprüfung, Schema und tatsächliche Wiederberechnung sind getrennte
Prüfungen. Ein korrekter Hash beweist weder Urheberschaft noch Messherkunft.
Unbekannte Versionen und unzureichende Daten werden abgewiesen oder als
INCONCLUSIVE eingeordnet; sie erhalten keinen stillen PASS.

## Auswahl für einen ersten späteren Transfer

Nach G1 wären F01, F02 und F03 die kleinste fachlich zusammenhängende Auswahl.
F10 stellt den dafür nötigen Datenaustausch bereit. F04 folgt bei einem konkret
definierten Vergleichsproblem. F05–F09 bleiben an ihre Forschungsnachweise gebunden.
Es gibt derzeit keine Zusage eines Astrolabium-Releases oder einer Hardwarefunktion.
