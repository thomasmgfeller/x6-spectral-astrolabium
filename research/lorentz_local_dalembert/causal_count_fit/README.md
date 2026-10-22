# Eigenzeit: gemeinsamer Rohzähl-Fit mit vollständiger Kausalordnung

**22.10.2026 — neuer Kandidat implementiert, auf 32 neuen Auswahlwolken geprüft;
Gesamtentscheidung: HOLD. Keine Übernahme in eine freigegebene Pipeline.**

Die [vorangegangene Diagnose](../causal_order_diagnosis/README.md) lokalisierte
die Ordnungsfehler in der Rekonstruktion aus endlichen Intervallzählungen.
Dieser Folgeschritt nimmt die bekannten Beziehungen bereits in den Fit auf
und verwendet das nichtlineare Zählmodell direkt. Das verbessert die
geometrische Konsistenz, liefert aber noch keine ausreichend verfügbare und
stabile Operatorschätzung. Alle bisherigen wissenschaftlichen HOLDs bleiben.

## Drei ausgeführte Schritte

1. **Neuen Kandidaten gebaut und kontrolliert.** Alle vier Landmarken sowie
   Wurzel und Stützpunkte werden gemeinsam in einer flachen 2+1-Geometrie
   geschätzt. Vollständige gerichtete Kausalordnung als Nebenbedingungen;
   zehn synthetische Kontrollen bestanden.
2. **Verfahren eingefroren und neue Daten ausgewertet.** 32 neue unabhängige
   Auswahlwolken A, 19 erfolgreiche Auswahlen, je neun unabhängige Zählwolken B:
   insgesamt 171 neue Zählläufe. Keine Ersatzauswahlen oder Nachoptimierung
   der Regeln. Der alte Archivvergleich bleibt separat.
3. **Entscheidung geprüft und dokumentiert.** Alle 64 alten/neuen
   Auswahlversuche und alle Fit-/Zählausfälle sind enthalten. Eine zweite
   Rechenformulierung prüft 177 gültige Fits. Der Kandidat verfehlt die
   vorab gesetzten Verfügbarkeits-, Genauigkeits- und Wiederholungsvarianzgates.

## Hauptbefund auf neuen Wolken

Die alte und neue Methode erhalten dieselben ausgewählten Knoten, bekannten
Ordnungsbeziehungen und unabhängigen B-Zählungen. Die 13 Fälle ohne vierte
Landmarke bleiben im Nenner. Ein weiterer B0-Fall, Wolke 09, scheitert an der
unveränderten Mindestzählgrenze. Beide Verfahren haben damit 18 rechnerisch
verfügbare Hauptfälle; der alte Schätzer erfüllt bei nur zwei davon die Ordnung.

| Kennzahl | Alter Vier-Landmarken-Schätzer | Neuer gemeinsamer Fit | Kriterium / Einordnung |
| --- | ---: | ---: | --- |
| Vollständig ordnungskonforme B0-Systeme | 2/32 | 18/32 | Mindestens 26/32: verfehlt |
| Gemeinsame berechenbare B0-Fälle | 18 | 18 | Mindestens 26: verfehlt |
| Operator-RMSE auf diesen 18 Fällen | 2,442938 | 2,210551 | Verhältnis 0,904874; gefordert ≤0,9: verfehlt |
| RMS der linearen Feldantwort | 2,472175 | 2,203803 | Verhältnis 0,891443: bestanden |
| Mittlere Varianz durch iid Feldrauschen | 1,093872 | 1,305702 | Verhältnis 1,193652; Grenze 1,25: bestanden |
| Normierter RMSE der vorzeichenbehafteten Paarintervalle | 0,425861 | 0,265856 | Deskriptive geometrische Diagnose |
| Mittlere Antwortvarianz über B1–B8 | 6,665545 | 14,764487 | Verhältnis 2,215046; Grenze 1,25: verfehlt |
| Vollständige B1–B8-Vergleichsgruppen | 14 | 14 | Mindestens 16: verfehlt |

**Die Ordnung wurde als Eingabe erzwungen. Ihr Bestehen ist deshalb kein
unabhängiger Genauigkeitsnachweis.** Die RMSE-Zeilen vergleichen gemeinsame
berechenbare Fälle, einschließlich alter Systeme mit verletzter Ordnung.
Dies ist ein bedingter Diagnosevergleich, kein Vergleich zweier freigegebener
Verfahren. Auf der winzigen beidseitig ordnungskonformen Teilmenge von zwei
Fällen beträgt das RMSE-Verhältnis 0,896289; daraus folgt keine Qualifikation.

Der Punktschätzer des Operatorfehlers verbessert sich um 9,51 %, knapp unter
den geforderten 10 %. Das deskriptive 95%-Cluster-Bootstrap-Intervall für das
Verhältnis lautet **[0,739868; 1,443213]** und schließt 1 ein. Ein gesicherter
Genauigkeitsgewinn ist damit nicht gezeigt. Die wahre Koordinatenreferenz hat
auf denselben 18 Fällen RMSE 0,048077; sie ist ein nicht intrinsischer Oracle.

Die verschiedenen Rauschgrößen dürfen nicht vermischt werden: Die Zeile für
iid Feldrauschen betrifft verrauschte Feldwerte bei festen Gewichten. Die
Wiederholungsvarianz misst die Änderung der Gewichte/Antworten durch neue
Zählwolken bei festem A. Gerade diese zweite Größe verschlechtert sich deutlich.
Sie wird nur auf 14 vollständigen, gepaarten B1–B8-Gruppen berechnet. Acht
Wiederholungen und vier Testfelder ergeben keine zusätzlichen unabhängigen
Landmarkenauswahlen; eine Unsicherheits- oder Coveragekalibrierung fehlt weiterhin.

Alle 171 Wiederholungen: jeweils **160 WEIGHTS_VALID und 11 COUNT_HOLD** bei
beiden Verfahren. Alle 160 neuen gültigen Fits bestehen die vollständige
Ordnung. Kein Fit brauchte einen Ersatzstart. Median der Fitzeit einschließlich
Enthaltungen: 0,098702 s; Maximum: 0,362773 s. Die beiden gesamten Arbeiterläufe
brauchten 342,35 beziehungsweise 355,41 s und maximal 1368,04 MiB pro Prozess.
Das Rechenbudget ist hier nicht die Hauptgrenze.

## Was der neue Schätzer tatsächlich macht

Für normierte Koordinaten z und eta = diag(-1,+1,+1) sei
q_ab = -(z_b-z_a)^T eta (z_b-z_a). Das erwartete Intervallzählmaß lautet

```text
lambda_ab = rho * (pi/12) * scale^3 * q_ab^(3/2).
loss = 2 * mean(lambda - N + N * log(N/lambda)).
```

Alle vier Landmarken bewegen sich gemeinsam mit Wurzel und Stützpunkten.
Translation, Lorentz-Boost und räumliche Rotation werden durch eine feste
Eichung entfernt. Die bekannten kausalen Paare müssen zeitartig mit korrekter
Zeitrichtung sein, die unverbundenen Paare raumartig. Beide erhalten den
festen Abstand 1e-8 von der Nullgrenze in normierten Einheiten. Exakt lichtartige
Paare sind nicht Teil dieses Kandidaten. Der einzige Start kommt aus der alten
Vier-Landmarken-Inversion. Fehlerhafte Startsignatur und zu kleine Zählungen
werden nicht repariert, sondern führen zur Enthaltung.

Die nichtlineare Transformation N^(2/3) dient nur dem Start, nicht als Zielgröße
des Fits. Das vermeidet einen Fit an den verzerrten transformierten Mittelwert,
beweist aber **keinen unverzerrten endgültigen Schätzer**. Die Zählungen
überlappen: Die Summe marginaler Poisson-Deviancen ist eine **zusammengesetzte
Zielfunktion**, keine gemeinsame Likelihood unabhängiger Zählungen. Die
Überlappungsmatrizen bleiben in den Rohdaten; der Kandidat nutzt sie nicht zur
Gewichtung seiner Zielfunktion. Wiederholungswolken erhalten die tatsächlichen
Korrelationen. Aus der Hesse-Matrix wird keine Konfidenz abgeleitet.

Nach dem Fit bleiben der unabhängige vollständige Ordnungscheck und die alten
Gram-/Momenten-/KKT-Prüfungen erforderlich. Der lokale SLSQP-Solve garantiert
kein globales Optimum. Die positive Ordnungsmarge, endliche Auswahl und der
einzige Start begrenzen den Gültigkeitsbereich.

Dies ist ein eigenständiger neuer Kandidat innerhalb der geometrischen
Schätzung. Die [verworfene V1-Korrektur](../intrinsic_correction_development/README.md)
hielt drei Landmarken fest und verwendete eine andere Abstandszielgröße.
Ihr negativer Nutzenbefund wird hier weder überschrieben noch aufgehoben.

## Bekannte Archivdaten: separat, keine neue Bestätigung

Alle ursprünglichen 32 Versuche wurden einmal auf B0 wiederholt; 18 hatten
eine Auswahl, 17 waren rechnerisch verfügbar. Der neue Fit besteht bei 17/32
die Ordnung, der alte bei 1/32. Auf 17 gemeinsamen Fällen sinkt der
Operator-RMSE 2,358922 → 1,762579, während die iid Feldrauschvarianz um den
Faktor 1,694375 steigt. Auf dem einzigen beidseitig ordnungskonformen Fall
verschlechtert sich der Operatorfehler stark. Diese bereits bekannten Daten
sind Entwicklungsdiagnostik. Kein Parameter wurde nach ihrem Replay geändert.
Die neue 32er-Kampagne war unabhängig davon vorab festgelegt.

## Rechenkontrollen und Provenienz

- [Protokoll](PROTOCOL.md), [Vertrag](contract.json), [lokaler Freeze](freeze.json).
  Basis: Commit `38a67dddb9f95ff8c0078af44e39870ca8009dc9`.
- [Zehn synthetische Kontrollen](controls.json): Eichungsinvarianz, exakte
  Mittelwerte/Referenzgewichte, unabhängige Ableitungsdifferenzen, Zeitumkehr,
  Zähl-HOLD, gleiches Eingabemaskenset, Umbenennung der Knoten.
- [Prüfbericht](verification.json): 140 ursprüngliche Manifest-Einträge und
  alle 64 Auswahlaufzeichnungen geprüft. Für 177 qualifizierte Fits maximale
  direkte Momentenabweichung 7,92e-11; relative Abweichung eines unabhängigen
  Gewichts-Solves 1,20e-7; Abweichung der direkt berechneten Deviance 1,15e-13.
  Erste/letzte neue verfügbare Konfiguration: B0-Zählwolke bitgleich reproduziert,
  Fitgewichte innerhalb 1e-8 identisch. Interne Rechenprüfung, keine externe
  Replikation, keine neue Sage-Prüfung und kein globales Optimalitätszertifikat.
- [Neue Analyse](analysis-fresh.json), [Archivanalyse](analysis-archive.json),
  Rohdaten unter [results](results/) und [archive](archive/), jeweils mit
  separaten, an den Inferenzhash gebundenen Wahrheitsdateien.
- Python 3.12.14, NumPy 2.3.5, SciPy 1.17.0, OPENBLAS_NUM_THREADS=1.
  Zufallsseeds, Laufzeit und Speicher sind vollständig gespeichert.

Der lokale Freeze erfolgte vor den neuen Wolken, nicht öffentlich. Der erste
Freeze-Helfer erfasste wegen eines relativen Pfadfehlers nur sieben
Kandidatendateien. Die fehlenden Abhängigkeitshashes wurden **vor der ersten
neuen Auswahl** ergänzt (97 Dateien insgesamt). Der ursprüngliche Freeze
bleibt unter [attempts](attempts/) erhalten; Code und Kriterien blieben gleich.

Die Logs enthalten eine RuntimeWarning von log1p bei unzulässigen
Zwischenschritten. Der bereits eingefrorene Code benutzt dann die algebraisch
gleichwertige positive-lambda-Formel; die unabhängige Endwertprüfung besteht.
Diese Warnung wurde nicht nachträglich aus den Logs entfernt.

## Reproduktion

Schneller Integritäts- und Rechenaudit im vorliegenden Verzeichnis:

```sh
sha256sum -c SHA256SUMS.txt
OPENBLAS_NUM_THREADS=1 python3 verify.py
```

Für eine vollständige Wiederholung zuerst eine neue Arbeitskopie anlegen;
der Runner überschreibt vorhandene Ergebnisdateien absichtlich nicht:

```sh
python3 prepare_replay.py /tmp/eigenzeit-causal-replay
cd /tmp/eigenzeit-causal-replay/causal_count_fit
OPENBLAS_NUM_THREADS=1 python3 run.py archive
OPENBLAS_NUM_THREADS=1 python3 analyze.py archive
OPENBLAS_NUM_THREADS=1 python3 run.py fresh --worker 0
OPENBLAS_NUM_THREADS=1 python3 run.py fresh --worker 1
OPENBLAS_NUM_THREADS=1 python3 analyze.py fresh
OPENBLAS_NUM_THREADS=1 python3 verify.py
```

Die beiden frischen Arbeiter dürfen parallel laufen; zusammen ist entsprechend
mehr Arbeitsspeicher erforderlich. Verstrichene Zeiten und davon abhängige
Aufzeichnungshashes unterscheiden sich bei Wiederholung. Die wissenschaftlichen
Eingaben, Seeds und Kriterien bleiben fest. Das Originalpaket wird nicht berührt.

## Entscheidung und nächster Forschungsbedarf

**HOLD; keine Übernahme.** Die Ursache der ursprünglichen Ordnungsverletzungen
ist technisch adressiert, aber Verfügbarkeit und stabile Genauigkeit fehlen.
Der neue Befund begründet zwei getrennte offene Aufgaben: eine intrinsische
Auswahl mit ausreichend verfügbaren, stabilen Landmarkensystemen und ein
Schätzer, dessen Fehler über neue korrelierte Zählwolken nicht anwächst. Eine
gemeinsame Kovarianz-/Zählmodellierung mit kontrollierter Regularisierung wäre
ein neu zu prüfender Kandidat, keine durch diesen Lauf bestätigte Lösung.
Der aktuelle Kandidat wird nach dem negativen Gate nicht weiter nachgetunt.

`HOLD_PHASE3`, `HOLD_EMBEDDING_COVARIANCE` und `METADATA_HOLD` bleiben.
Kein Krümmungs-/3+1-Transfer, Kalman-Nutzen oder physischer Sensor ist qualifiziert.

## English scope

A new joint four-landmark fit uses a nonlinear raw-count marginal Poisson
composite objective with complete directed-order constraints. Ten synthetic
controls pass. A locally frozen campaign completes 32 fresh selection attempts,
19 selected configurations and 171 independent count repetitions. Primary
order-consistent availability rises from 2/32 to 18/32. Conditional operator
RMSE falls by 9.51%, narrowly missing the fixed 10% target; the descriptive
cluster-bootstrap ratio interval includes one. Conditional B1–B8 response
variance rises by a factor 2.215 on 14 complete groups. Overall **HOLD**.
Enforced order is input consistency, not independent accuracy evidence. No
joint-likelihood, uncertainty-coverage, global-optimality or physical claim.
All failures, frozen inputs, raw records and an internal numerical audit are
included. Rejected V1 and previous scientific holds remain unchanged.

SPDX-License-Identifier: Apache-2.0
