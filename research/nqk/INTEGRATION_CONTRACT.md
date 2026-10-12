# Vorschlag für einen späteren Integrationsvertrag

**Status: Entwurf 0.1.** Die nachfolgenden Felder und Regeln sind Anforderungen.
Es existiert durch dieses Dossier weder ein Parser noch eine freigegebene API.

## Trennung der Programme

NQK besitzt eigene Definitionen, Versuchsprotokolle, Referenzen und Releases.
Astrolabium kann später qualifizierte Ergebnisse importieren oder einen
qualifizierten Kern optional aufrufen. Eine gemeinsame Laufzeitabhängigkeit ist
für die selbstständige NQK-Forschung nicht erforderlich.

Die erste Verbindung soll ausschliesslich Analysedaten übertragen. Gerätesteuerung,
automatische Messfreigabe und Verlängerungen bestehender Agentenfenster benötigen
eigene Entwürfe und Aufträge. Es wird kein vorhandenes Exportschema überschrieben.

## Vorgeschlagene Ergebnisfelder

| Feldgruppe | Verlangte Information |
| --- | --- |
| Identität | Schema-ID und Version, NQK-Version, Quellrevision, Protokoll-ID, Laufkennung |
| Herkunft | SYNTHETIC_CLASSICAL, QUANTUM_SIMULATION, ARCHIVAL_MEASUREMENT oder LAB_MEASUREMENT; Erzeugungs-/Aufnahmeweg und separate Qualifikation |
| Modell | Knoten/Subsysteme, lokale Dimension, Gewichtsfunktion, Normierung, Entropiebasis, Einheiten, Rand- und Nullwertregeln |
| Eingaben | Unveränderte Arrays oder dauerhaft auflösbare Datenreferenzen mit Prüfsummen; Seeds und Generatorversion bei Simulationen |
| Transformationen | Geordnete Liste aller Ableitungen, insbesondere Log-Abbildung, Abschneiden, Wegabschluss, Rundung und Zustandsprojektion |
| Diagnosen | Getrennte Resultate für Quantenzulässigkeit, Metrik, Einbettung, Rekonstruktion und gegebenenfalls Kausalordnung |
| Prüfdetails | Vollprüfung oder Stichprobe, Anzahl und Auswahl der Fälle/Tripel, Toleranzen, Verletzungszeugen und numerische Residuen |
| Statistik | Zielgrösse, unabhängige Einheiten, Abhängigkeiten, Intervallmethode, Konfidenzniveau, punktweise oder simultane Geltung |
| Grenzen | Fehlende Observablen, nicht identifizierbare Parameter, Grössenlimits und ungetestete Annahmen |
| Integrität und Wiederholung | Inhaltsdigest, definierte Kanonisierung, Engineversion und getrennte Resultate von Hash-, Schema- und Replayprüfung |

NaN und Infinity gehören nicht als nichtstandardisierte Zahlen in JSON.
Mathematisch unendliche oder undefinierte Werte werden mit `null` plus explizitem
Status und Ursache kodiert. Das ursprüngliche Gewicht wird trotzdem erhalten.
Grössenlimits und zulässige Arrayformen werden vor Implementierung festgelegt.

## Keine gemeinsame Alles-bestanden-Ampel

Numerischer Status: PASS, FAIL, INCONCLUSIVE oder NOT_EXECUTED für ein genau
benanntes Kriterium. Dazu separat Modellannahmen, Evidenzherkunft, unabhängige
Replikation und empirische Qualifikation. Ein einzelner PASS wird nicht zu einem
Gesamturteil über einen Zustand, ein Gerät oder eine physikalische Theorie verdichtet.

Ein notwendiger Quantenkompatibilitätstest kann nur EXCLUDED oder
NOT_EXCLUDED_BY_THIS_TEST liefern. Ein mathematischer Beweis braucht eine
prüfbare Herleitung und seinen exakten Geltungsbereich; numerische Übereinstimmung
wird nicht als formaler Beweis exportiert.

## Bestehende X6-Verträge berücksichtigen

Das Signal Validation Lab verwendet aktuell `x6.signal-lab.evidence/1` für
bekannte synthetische Zeitreihen, Parameter, vollständige Ausgaben und Replay.
Dieses Schema beschreibt keine globale Quantendichtematrix. Ein späterer
Adapter braucht eine ausdrückliche Abbildung und bewahrt den ursprünglichen
Export unverändert. NQK-Ergebnisse erhalten einen eigenen versionierten Vertrag.

Bei Signal → Graph ist die Matrixbildung eine Modellentscheidung. Bei Graph →
Operator muss der Operator festgelegt werden. Ein Fourierfrequenzspektrum, das
Spektrum eines Graph-Laplacians und ein physikalisches Energiespektrum erhalten
unterschiedliche Typen und Einheiten. Eine Beziehung zwischen ihnen muss eigens
hergeleitet oder kalibriert werden.

## Integrationsfreigabe

1. Eingangs- und Ausgangsschema festlegen und anhand gültiger sowie absichtlich
   ungültiger Dateien prüfen.
2. Kleine bekannte Fälle unabhängig berechnen; fachliche Gates des Features bestehen.
3. Transformationsverluste, fehlende Daten, Zeit-/Speicherlimits und Fehlermeldungen prüfen.
4. Ergebniswiederholung auf dem archivierten Quellenstand durchführen.
5. Adapter im Zielmodul und bestehende Anwendung am konkreten Commit prüfen.
6. Dokumentation und Umfang in einem eigenen Transfer-Pull-Request freigeben.

Bis dahin ist der Status aller Astrolabium-Transferkandidaten PROPOSED.
