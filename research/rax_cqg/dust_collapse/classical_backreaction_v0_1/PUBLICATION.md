# Klassische Staubbewegung und gravitative Rückwirkung v0.1

**5. November 2026 · Reduzierte Referenz bestanden; vollständige CST-Herleitung offen.**

Die ausdrücklich gewählte Einstein-Staub-Referenz liefert geodätischen Staubtransport, Massenerhaltung und gravitative Quellwirkung. Im homogenen flachen Sektor reproduziert der reduzierte Quantenkern den klassischen Kollaps in der geprüften semiklassischen Zustandsfamilie vor der Singularität. Diese Referenz beginnt mit der gekoppelten Kontinuumswirkung. Sie ist kein Nachweis, dass eine vollständige Summe vierdimensionaler Kausalsets dieselbe Bewegung hervorbringt.

- [Bericht (PDF, sechs Seiten)](../reports/CST_Staubball_Klassik_Rueckwirkung_v0_1.pdf)
- [Unverändertes Prüfpaket (ZIP)](../packages/CST_Staubball_Klassik_Rueckwirkung_v0_1_Pruefpaket.zip)
- [Prüfcode](verify.py), [Einzelergebnisse](results/verification.json), [Testspezifikation](plan.json) und [Quellenbindung](provenance.json)
- [Ursprüngliche Anleitung](README.md), [bearbeitbare Herleitung](report.tex) und [Abbildung](figures/classical_checks.png)

## Was geprüft wurde

Die diskrete stationäre Wirkung ergibt auf einem ungleichmäßigen Zeitgitter eine lineare Bewegung von `q = sqrt(V)`; die erste Variation wurde exakt mit rationaler Arithmetik kontrolliert. Neun unabhängige Beschleunigungsintegrationen in `a` bestätigen drei Massen auf drei Schrittweiten. 90 Auswertungen des normierten Quantenkerns prüfen drei zentrale Massen, drei hbar-Werte, fünf Zeiten und zwei Ortsgitter gegen eine unabhängige analytische Halbgeradenlösung. Norm, Volumenmoment und Energieerwartung stimmen im angegebenen Fehlerbudget überein.

Bei festem Anfangsvolumen verdoppelt vierfache klassische Masse den Betrag von `q_dot`, sofern die Anfangszwangsgleichung erfüllt wird. Die lokalisierten Quantenzustände haben eine endliche Massenstreuung; die im Bericht unterschiedenen zentrale Masse und Energieerwartung werden nicht gleichgesetzt.

## Neue Grenze des bisherigen Zeitfensters

Die alten frühen Werte `a(0)=1` und `a(0.4)=0.8` implizieren in dieser flachen klassischen Referenz eine Singularität bei `T=1.4061817646`. Der positive Historienkatalog reicht bis `T=1.6`. Für einen kontrollierten Klassikvergleich wird daher zuerst ein Fenster vor diesem Zeitpunkt benötigt. Dass einzelne diskrete Pfade nicht stationär sind, ist kein allgemeiner Ausschluss eines Quantenpfadintegrals.

Die frühere Massenantwort der Randfamilie C wurde aus den archivierten Polynomen nachgerechnet und stimmt bis auf Gleitkommafehler mit den früheren Ergebnissen überein. Auch ohne Gravitationsphase bleibt Materieinterferenz. Diese Kontrolle ist nicht der physikalische Grenzfall `G -> 0`. Die lineare Verwendung klassischer Wachstumsgewichte als Amplituden bleibt eine Modellannahme des übernommenen Vergleichs.

## Wissenschaftlicher Status

`G4-REF = PASS` unter den angegebenen Referenzannahmen; `G4-CST = HOLD`. Die Herleitung klassischer Bewegung und gravitativer Rückwirkung aus der vollständigen CST-Summe bleibt offen. Es fehlen insbesondere der konsistente gekoppelte Kern, die Anfangszwänge und kalibrierte mehrzeitige Volumina aus denselben dynamischen Historien. Der alte Kandidat bleibt `CLOSED_REJECTED_FOR_DOMINANT_BOUNCE`; neuer Bounce-Test `NOT_RUN`; Singularitätsauflösung nicht nachgewiesen. Die numerischen Prüfungen sind keine neuen Intervallzertifikate.

## Veröffentlichung und Nachrechnung

Das ursprüngliche ZIP und alle 23 Mitglieder sind bytegleich übernommen; die PDF-Kopie im Berichtsverzeichnis ist identisch. Die ergänzenden Dateien `PUBLICATION.md`, `publication_check.py` und `publication-requirements.txt` dienen der Veröffentlichung und Nachrechnung. Die ursprünglichen Ergebnisdateien bleiben unverändert.

```sh
python3 -m pip install -r research/rax_cqg/dust_collapse/classical_backreaction_v0_1/publication-requirements.txt
python3 research/rax_cqg/dust_collapse/classical_backreaction_v0_1/publication_check.py --replay
```

Die Kontrolle bindet alle Mitglieder und Eingaben an die bereits veröffentlichten Quellen. Die Nachrechnung erfolgt in einer temporären Kopie. Strukturelle Resultate und Entscheidungen müssen exakt stimmen; Gleitkommawerte werden mit absoluter Toleranz `2e-10` und relativer Toleranz `1e-10` verglichen. Der Originalprüfer wendet zusätzlich seine in `plan.json` festgehaltenen Einzelkriterien an. Angaben zu Laufzeitversionen dürfen sich unterscheiden. Der physikalische Status wird durch CI nicht aufgewertet.

Keine neuen Kausalsets, Sprinkling-Ensembles oder physikalischen Messungen. Keine erneute alte Intervallzertifizierung und keine externe Präregistrierung. Projektbeiträge gemäß [Lizenzumfang](../../../../LICENSE_SCOPE.md).
