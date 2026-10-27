# Eigenzeit 3+1: schärfere Schranke und Informationsbudget, v0.4

27. Oktober 2026. **Gesamtstatus HOLD.** Bei sechzehnfacher erwarteter
Punktzahl bestehen 19 von 20 Geometrien das vorab festgelegte
Verfügbarkeitskriterium. Die Geometrie `fresh_11` bleibt darunter.
Beim ursprünglichen Budget bestehen weiterhin nur 14 von 20 Geometrien.

Die verbesserte Rechnung allein bringt vier zusätzliche Zertifikate über
alle 3.840 neuen Versuche. Der größere Gewinn stammt vom höheren
Informationsbudget. Eine ergänzende Prüfung weist außerdem nach, dass
die untersuchten Gegenzeugen der bisherigen Konfidenzregion geometrisch
unmöglich sind. Das eröffnet einen konkreten Ansatz zur engeren Eingrenzung
der Region, liefert selbst aber noch keine zusätzliche Fehlergarantie.

## Frische, vorab festgelegte Vergleichsläufe

| Informationsbudget | Erwartete Punkte im äußeren Intervall | Neue Schranke: Zertifikate | v0.3 auf denselben Daten | Geometrien mit Verfügbarkeits-Untergrenze ≥90 % |
| --- | ---: | ---: | ---: | ---: |
| bisheriges Budget | 268.435.456 | 956 / 1.280 | 955 / 1.280 | 14 / 20 |
| vierfach | 1.073.741.824 | 961 / 1.280 | 961 / 1.280 | 15 / 20 |
| sechzehnfach, primäres Kriterium | 4.294.967.296 | 1.229 / 1.280 | 1.226 / 1.280 | 19 / 20 |

Je Budget wurden 64 neue unabhängige Zählvektoren für jede der bisherigen
20 Geometrien gezogen. Nur das sechzehnfache Budget ist die vorab erklärte
primäre Freigabeprüfung. Die beiden niedrigeren Budgets dienen dem Vergleich.
Für jede Geometrie wird eine einseitige Clopper-Pearson-Untergrenze mit
Bonferroni-Niveau 0,05/20 berechnet. 64/64 Zertifikate ergeben eine Untergrenze
von rund 91,06 %. Die Freigabe verlangt mindestens 90 % für **jede** Geometrie.

Am primären Budget bestehen 19 Geometrien mit jeweils 64/64 Zertifikaten.
`fresh_11` erreicht lediglich 13/64, gegenüber 10/64 mit v0.3; ihre
Untergrenze beträgt rund 8,49 %. Der hohe Gesamtanteil von 96,02 % ersetzt
das geometrieweise Kriterium nicht. Der Median der relativen Schranke für
das Eigenzeitquadrat liegt dort bei etwa 18,26 %, zusammengesetzt aus
14,25 % linearem/Quadratwurzel-Anteil und 4,01 % inverser Restschranke.
Die beiden Teilmediane addieren sich wegen verschiedener Beobachtungen
nicht exakt zum Median der Summe.

Insgesamt wurden 3.146 Zertifikate der neuen Methode und 3.142 der Vorversion
mit gerichteter 60-stelliger Dezimalrechnung validiert. Kein ausgestelltes
neues Zertifikat widersprach dem bekannten Simulationsziel. Dies ist eine
beobachtete Eigenschaft des Versuchs, kein Ersatz für die Konfidenzherleitung.

## Was geändert wurde

1. Der Quadratwurzelrest wird durch eine exakte rationalisierte Identität
   begrenzt. Das verbessert die bisherige Taylor-Restschranke.
2. Zwei positiv semidefinite 4×4-Matrizen liefern engere Grenzen für die
   linearen Matrix- und Vektorfluktuationen. Die kleinste von drei mit
   gerichteter Rundung geprüften Grenzen wird verwendet; ein gewöhnlicher
   Eigenwertsolver entscheidet kein Zertifikat.

Die gemeinsame Poisson-Konfidenzregion bleibt unverändert. Die neuen
analytischen Grenzen können die alten nicht verschlechtern. Alle zuvor
zertifizierten Beobachtungen der frischen Vergleichsläufe werden erhalten.
Herleitung: [THEORY.md](THEORY.md).

Die unveränderte statistische Aussage lautet: Für jeden festen zulässigen
Modellparameter ist die unbedingte Wahrscheinlichkeit, ein falsches
10%-Zertifikat auszustellen, höchstens `2^30 exp(-24)`, also rund 4,054 %
pro Beobachtung. Das ist weder dieselbe Garantie bedingt auf die Auswahl
zertifizierter Beobachtungen noch eine simultane Garantie für den gesamten
Versuch. Nicht zertifizierte Fälle bleiben HOLD.

## Die Konfidenzregion enthält geometrisch unmögliche Fälle

Für je eine archivierte v0.3-Beobachtung der fünf schwierigen
Familie-3-Geometrien wurden zwei explizite Mittelwertvektoren konstruiert.
Exakte rationale Prüfungen zeigen, dass sie in der bisherigen Region liegen;
Intervallrechnung zeigt, dass kein gemeinsamer 10%-Schätzwert beide abdecken
kann. Diese fünf Paare begrenzen die Zertifizierung über diese volle Region.

Die nach dem Freeze ergänzte Realisierbarkeitsprüfung zeigt jedoch:
**Alle zehn Mittelwertvektoren verletzen notwendige Normbedingungen einer
flachen Fünf-Anker-Geometrie.** Für die exakten Mittelwerte der 20 bekannten
Geometrien bestehen dagegen alle 40 Normkontrollen.

Damit sind diese Paare keine physikalischen Gegenbeispiele und kein
allgemeiner Unmöglichkeitsbeweis. Der gezielte nächste Schritt ist, die
beiden Normbedingungen der Zielpunkte in die gemeinsame Region aufzunehmen
und die eingeschränkte Region rigoros auszuwerten. Die bisherige Abdeckung
bleibt unter dem Modell bei dieser exakten Einschränkung erhalten; ein
entsprechender zusätzlicher Genauigkeitsgewinn ist noch nicht nachgewiesen.
Details: [REALIZABILITY.md](REALIZABILITY.md),
[REGION_WITNESSES.json](REGION_WITNESSES.json),
[REALIZABILITY.json](REALIZABILITY.json).

## Prüfung, Protokollkorrektur und Geltungsbereich

- 910 Kontrollen für die neue Methode und die fünf Zeugen bestanden.
- Alle 3.840 neuen Zählvektoren exakt aus dem Seed reproduziert.
- Alle 3.146 neuen Zertifikate mit exakten Entscheidungsungleichungen und
  einer separaten Intervalllösung der Punktschätzung geprüft.
- 102 Zertifikate zusätzlich mit 90 signifikanten Dezimalstellen berechnet.
- 26.112 zusätzliche Randrichtungen des Ellipsoids und 60 Maskierungsprüfungen
  der unbenutzten Zielzählung bestanden. Randtests ersetzen den Beweis nicht.
- Der Publikationsprüfer wiederholt beide Zertifikatsmethoden vollständig,
  den Audit, die Entwicklungsdiagnostik und die Realisierbarkeitsprüfung.

Ein erster Lauf wurde wegen einer Importverwechslung gestoppt: Der Runner
lud die Kontrollen von v0.3. Seine teilweise beobachteten Ergebnisse zählen
nicht zur Validierung. Nach Korrektur der Importreihenfolge und Ergänzung
von Prüfungen der Modulherkunft wurde vor den neuen Ziehungen ein zweiter
Freeze mit unabhängigem Seed erstellt. Mathematik, Budgets, Stichprobengröße
und Erfolgskriterien wurden nicht verändert. [AMENDMENT.json](AMENDMENT.json),
[ABORT_LOG.txt](ABORT_LOG.txt) und [aborted_attempt/](aborted_attempt/)
erhalten den Verlauf und den ursprünglichen Quellstand. Der lokale Freeze
ist keine externe Präregistrierung.

Vorausgesetzt bleiben flache 3+1-Minkowski-Geometrie, bekannte Intensität
und extern festgelegte, beschriftete Landmarken. Die 20 Geometrien sind
unverändert aus v0.2; die Namen `fresh_00` bis `fresh_15` bezeichnen hier
keine neuen Geometrien. Intrinsische Landmarkenwahl, Generalisierung auf
neue Geometrien, Krümmung, Operatoren und die bestehenden GFEST/HOLD-Fragen
sind nicht freigegeben. Die Prüfungen sind intern, ohne unabhängige
fachliche Begutachtung oder Beweisassistenten-Verifikation.

Die Milliardenwerte sind erwartete Punktzahlen des Modells. Die gemeinsame
Zählverteilung wird über 20 disjunkte Zellen gezogen; es wurden keine
Milliardenpunkte-Wolken erzeugt. Ein höheres Informationsbudget bedeutet
keinen entsprechend gemessenen Laufzeitnachweis für vollständige Causal Sets.

## Dateien und Reproduktion

[PROTOCOL.json](PROTOCOL.json), [FREEZE.json](FREEZE.json),
[RESULTS.json](RESULTS.json), [CERTIFICATES.json](CERTIFICATES.json),
[AUDIT.json](AUDIT.json), [fresh_counts.npz](fresh_counts.npz).
[DEVELOPMENT.json](DEVELOPMENT.json) enthält ausdrücklich explorative
Diagnosen auf den alten v0.3-Daten und keine neue Validierungsstichprobe.

Aus dem Repository-Hauptverzeichnis, mit Python 3.12:

```sh
python3 -m pip install -r research/eigenzeit_4d/poisson_v0_2/requirements.txt
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 python3 -B research/eigenzeit_4d/verify_refined_publication.py
```

Der Prüfer arbeitet in einer temporären Kopie und vergleicht die vollständige
Wiederholung mit den veröffentlichten Daten. Die archivierten Belege bleiben
unverändert. Code und eigener Text stehen unter der Apache-2.0-Lizenz des
Repositorys. Es wird kein Neuheitsanspruch erhoben.
