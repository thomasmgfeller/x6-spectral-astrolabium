# Eigenzeit: Suchbegrenzung und Zählvarianz getrennt geprüft

**22.10.2026 — Diagnose abgeschlossen; neuer Kovarianzkandidat bleibt auf HOLD.**

Der technische Abschluss der vorherigen Forschung ist mit [PR #85](https://github.com/thomasmgfeller/x6-spectral-astrolabium/pull/85)
und dem [CI-Abschlussnachweis](../CAUSAL_FIT_CI_COMPLETION.json) veröffentlicht:
alle fünf Workflows von PR #84 einschließlich aller acht Lorentz-BD-Teiljobs
bestanden. Anschließend wurden die folgenden drei Forschungsarbeiten ausgeführt.

1. Alle 13 gescheiterten Landmarkenauswahlen identisch rekonstruiert und ihren
   vollständigen, fest definierten Kandidatenraum untersucht.
2. Die Varianz des bisherigen Fits lokalisiert und drei festgelegte
   Modellvarianten auf allen vorhandenen Zählwiederholungen verglichen.
3. Einen Schätzer mit vollständiger Zählkovarianz auf **171 neuen Zählwolken**
   geprüft, mit vorher fixierten Kriterien und unveränderten Ausfallregeln.

Die 171 neuen Wolken wiederholen **dieselben 19 zuvor ausgewählten
A-Konfigurationen**. Sie sind neue unabhängige B-Zählungen, keine 171 neuen
Landmarkenauswahlen und keine neue Bestätigung der Auswahlpipeline.

## 1. Neun Auswahlfehler entstehen durch die Reihenfolge der Suche

Der bisherige Selektor bildet gemeinsame Vergangenheits-/Zukunftskandidaten
von Wurzel und Stützpunkten, sortiert sie nach unabhängigen Markierungen und
behält zuerst nur 128 pro Seite. **Erst danach** prüft er Vergleichbarkeit
mit den ersten drei Landmarken sowie alle Mindestzählungen. Auf den 13
gescheiterten Fällen blieb dadurch kein zählgeeigneter Kandidat übrig.

Die vollständige Suche hält Wurzel, Support, erste drei Landmarken und sämtliche
Schwellen unverändert. Sie erschöpft genau diese beiden vollständigen gemeinsamen
Kegel und prüft **31.293 Kandidaten**. Alle 13 ursprünglichen Auswahlaufzeichnungen
wurden bei der Regeneration bytegleich reproduziert.

| Vollständige Prüfung | Kandidaten |
| --- | ---: |
| Mit mindestens einem erforderlichen Knoten nicht kausal vergleichbar | 30.033 |
| Vergleichbar, aber Vollzählgrenze unterschritten | 1.190 |
| Alle Vergleichbarkeits- und Zählbedingungen erfüllt | 70 |
| Davon auch Gram-/Momentenbedingungen erfüllt | 55 |
| Davon durch Geometriebedingungen abgelehnt | 15 |

Die 55 zulässigen Kandidaten verteilen sich auf **9 der 13 alten Ausfälle**:
Wolken 02, 03, 05, 12, 14, 17, 19, 25 und 29. Sie liegen sämtlich außerhalb
der alten 128er-Begrenzung. In Wolken 06, 07, 08 und 11 existiert in diesem
vollständig untersuchten Kandidatenraum kein zählgeeigneter vierter Punkt.
Das ist keine Unmöglichkeitsaussage über andere Supports oder gemeinsam neu
gewählte erste drei Landmarken.

Eine konkrete Folgerung ist **Eignung vor Suchbegrenzung prüfen**: erst alle
notwendigen Vergleichbarkeits-/Zählbedingungen, danach höchstens 128 geeignete
Kandidaten je Seite für die teureren Geometrieprüfungen behalten. In den neun
betroffenen Fällen gibt es insgesamt jeweils weniger als 128 zählgeeignete
Kandidaten pro Seite, weshalb diese Reihenfolge sämtliche 55 zulässigen
Kandidaten behielte. Die alten erfolgreichen Kandidaten würden ebenfalls
nicht durch diese Umordnung ausgeschlossen, da ihr Rang beim Filtern nur sinkt.

Damit wäre auf den **bekannten** 32 A-Konfigurationen eine Auswahlverfügbarkeit
von **28/32 statt 19/32** möglich. Das ist ein nachträglich belegter
Machbarkeitsvergleich, **keine neue ausgeführte Gewichtsqualifikation** und
keine nachträgliche Verbesserung des ursprünglichen 18/32-Hauptbefunds.
Die Standardauswahl und historischen Dateien wurden nicht umgeschrieben.

Alle Einzelentscheidungen, Ausschlusszeugen und zulässigen Pakete liegen unter
[selection](selection/); die [Zusammenfassung](diagnostic-summary.json) enthält
alle 13 Fälle und die vollständigen Nenner.

## 2. Der alte Varianzanstieg ist stark konzentriert

Im alten, bereits bekannten Vergleich der 14 vollständigen B1–B8-Gruppen
liefert Wolke 04 **72,44 % der gesamten Antwortvarianz des Poisson-Fits**.
Ihre mittlere Varianz beträgt 149,733911, gegenüber 12,746499 bei der direkten
Vier-Landmarken-Inversion. Andere Konfigurationen kompensieren einen Teil des
Anstiegs; deshalb übersteigt ihr Anteil am *Nettoanstieg* rechnerisch 100 %.

Ohne Wolke 04 wäre das alte Varianzverhältnis 0,707 statt 2,215.
**Die Wolke wurde aus keinem Kriterium entfernt.** Das Weglassen dient nur
als nachträgliche Konzentrationsdiagnose und ist keine zulässige Rettung des Fits.

Die drei zusätzlichen Varianten wurden auf allen 19 ausgewählten Konfigurationen
mit je neun alten B-Wolken ausgeführt, nach lokalem Code-/Kriterienfreeze:

| Variante auf alten Entwicklungsdaten | Gemeinsame vollständige Gruppen | Mittlere Antwortvarianz | Vergleichbare alte Poisson-Varianz |
| --- | ---: | ---: | ---: |
| Ursprünglicher Poisson-Fit mit vollständiger Ordnung | 14 | 14,764487 | 14,764487 |
| Nichtlineares GLS, diagonale Kovarianz, vollständige Ordnung | 14 | 4,209720 | 14,764487 |
| Nichtlineares GLS, vollständige Kovarianz, vollständige Ordnung | 14 | 3,198616 | 14,764487 |
| Poisson-Fit ohne Stützpunkt-Stützpunkt-Ordnungsbedingungen | 13 | 3,522773 | 4,382223 |

Die letzte Zeile hat eine **andere gemeinsame Teilmenge**: Wolke 04 fehlt,
weil B3 am Momentenrang/-konditionsgate scheitert. Zusätzlich scheitert Wolke
21/B0 an diesem Gate. Nur 4/19 Hauptfälle dieser Negativkontrolle erfüllen
die vollständige Ordnung. Aus ihrer scheinbar niedrigeren Varianz darf daher
nicht geschlossen werden, dass das Weglassen der Kausalbedingungen das Problem
löst. Die bereits zuvor kritische Konfiguration verschwindet aus diesem
vollständigen Gruppenvergleich.

Auch die diagonale GLS-Variante reduziert die Entwicklungsvarianz stark.
Fehlende Zählkorrelationen allein erklären den alten Anstieg somit nicht:
Die Form und Gewichtung der Zielfunktion sowie die nichtlineare Rekonstruktion
wirken zusammen. Die volle Kovarianz liefert hier einen weiteren Rückgang.
Das ist eine kontrollierte endliche Algorithmusdiagnose, keine additive
physikalische Ursachenzerlegung oder globale Optimierungsaussage.

## 3. Neue Zählwolken: stabiler, aber Genauigkeitskriterium verfehlt

Der eine vorher festgelegte Kandidat minimiert

```text
C_alpha = 0.95 * C + 0.05 * diag(C)
lambda(z) = rho * (pi/12) * scale^3 * q(z)^(3/2)
loss = (lambda-N)^T C_alpha^(-1) (lambda-N) / number_of_intervals
```

C enthält die beobachteten Intervallüberschneidungszählungen, einschließlich
der Diagonale N. Vollständige gerichtete Ordnung, Start, Mindestzählungen,
Gram-/Momentengates und Rechenbudget bleiben erhalten. Der feste 5%-Anteil
stabilisiert die Matrix; er wurde nicht anhand neuer Ergebnisse gewählt.

Dies ist ein regularisierter GLS-Fit mit geschätzter Kovarianz, **keine exakte
gemeinsame Likelihood**. C ist selbst zufällig und mit den Zählresiduen
korreliert. Unverzerrtheit, kalibrierte Unsicherheit und globale Optimalität
folgen daraus nicht. Wahre Koordinaten und Testfelder gehen nicht in den Fit ein.

19 unveränderte A-Konfigurationen × neun neue B-Zählwolken, neuer Seed-Tag
782071. B0 ist Haupttest; B1–B8 messen die bedingte Wiederholungsvarianz.
Keine Ersatzläufe oder Parameteränderungen nach Einsicht in die Ergebnisse.

| Neue bedingte Prüfung | Direkte Vier-Inversion | Bisheriger Poisson-Fit | Vollständiger GLS-Fit |
| --- | ---: | ---: | ---: |
| Berechenbare B0-Fälle | 19 | 19 | 19 |
| Operator-RMSE, gleiche 19 Fälle | 2,083374 | 3,251465 | 2,419883 |
| Mittlere Varianz durch iid Feldrauschen | 1,505660 | 1,671942 | 1,473125 |
| Antwortvarianz über B1–B8, gleiche 12 vollständige Gruppen | 3,679587 | 4,506017 | 2,676974 |

Alle 19 GLS-Hauptsysteme erfüllen die vollständige Ordnung. Diese wird
allerdings als Eingabe erzwungen und ist kein unabhängiger Genauigkeitsbeleg.
Die Vergleichsinversion ist nur rechnerisch verfügbar; ihre Ordnung muss
gesondert geprüft werden. Die Tabelle ist kein Vergleich dreier freigegebener
physikalischer Verfahren.

Der GLS-Fit reduziert die Wiederholungsvarianz gegenüber dem Poisson-Fit um
**40,59 %** (Verhältnis 0,594089), gegenüber der direkten Inversion um **27,25 %**
(0,727520). Beide Varianzkriterien bestehen auf der angegebenen Teilmenge.
Die Feldrauschkosten bleiben ebenfalls innerhalb der Grenze.

**Die Gesamtentscheidung bleibt HOLD:** Der B0-Operator-RMSE ist um **16,15 %**
größer als bei der direkten Inversion (1,161521; gefordert ≤0,9). Außerdem
stehen nur **12 statt mindestens 14 vollständige Wiederholungsgruppen** zur
Verfügung. Das ist ein negativer festgelegter Test, kein Signifikanznachweis
einer allgemeinen Verschlechterung. Die guten Entwicklungswerte werden nicht
anstelle dieses Ergebnisses zur Freigabe benutzt.

Alle 171 neuen B-Läufe bleiben enthalten: direkte Inversion und GLS jeweils
160 WEIGHTS_VALID, 10 COUNT_HOLD, 1 UNRESOLVED; Poisson-Fit 159 WEIGHTS_VALID,
10 COUNT_HOLD, 2 UNRESOLVED. Wolke 04/B6 scheitert bei allen drei Verfahren
an der Startsignatur; Wolke 22/B7 erreicht beim Poisson-Fit das Iterationslimit.
Median/Maximum des GLS-Fits: 0,183220 / 0,702151 s.

## Evidenz, Kontrollen und Reproduktion

- [Festgelegtes Protokoll](PROTOCOL.md), [Vertrag](contract.json),
  [lokaler Freeze von 277 Dateien](freeze.json). Keine öffentliche Präregistrierung.
- [Sechs synthetische Kontrollen](controls.json): unabhängige Ableitungsprüfung,
  Korrelations-Negativkontrolle, diagonaler Grenzfall, exakte Mittelwert-/Oracle-
  Gewichte, Mindestzähl-HOLD und fehlerhafte Kovarianz zurückgewiesen.
- [Entwicklungsanalyse](analysis-development.json) und
  [neue bedingte Analyse](analysis-conditional.json), vollständige Rohdaten unter
  [development](development/) und [conditional](conditional/).
- [Interne Gegenprüfung](verification.json): **638 gültige Variantenfits**,
  171 verschiedene neue B-Koordinatenhashes, 38 gebundene Ergebnis-/Wahrheitsdateien,
  alle 31.293 Kandidaten bilanziert und 55 zulässige Gram-/Momentensysteme erneut
  geprüft. Maximale direkte Momentenabweichung 8,80e-11, relative Abweichung
  eines separaten Gewichts-Solves 8,04e-8, unabhängige Verlustabweichung 1,36e-13.
  Neue B0-Wolken 00/31 bitgleich und GLS-Gewichte innerhalb 1e-8 reproduziert.
- Python 3.12.14, NumPy 2.3.5, SciPy 1.17.0; OPENBLAS_NUM_THREADS=1.
  Auswahlreplays: 154,26/137,06 s, maximal 1345,93 MiB je Prozess.
  Entwicklungslauf 66,62 s, neuer bedingter Lauf 70,96 s.

Die Gegenprüfung wurde nach dem Freeze ergänzt; Fit und Erfolgskriterien
blieben unverändert. Dies ist keine externe Replikation oder neue Sage-Prüfung.
Die Warnung der alten Poisson-Implementierung bei log1p-Zwischenschritten bleibt
in den Logs; ihr bereits vorhandener algebraischer Fallback wird unverändert benutzt.

Im vorliegenden Verzeichnis:

```sh
sha256sum -c SHA256SUMS.txt
OPENBLAS_NUM_THREADS=1 python3 verify_followup.py
```

Vollständige Wiederholung in einem neuen, noch nicht vorhandenen Verzeichnis:

```sh
python3 prepare_replay.py /tmp/eigenzeit-stability-replay
cd /tmp/eigenzeit-stability-replay/stability_followup
OPENBLAS_NUM_THREADS=1 python3 selection_audit.py 0
OPENBLAS_NUM_THREADS=1 python3 selection_audit.py 1
OPENBLAS_NUM_THREADS=1 python3 runner.py development
OPENBLAS_NUM_THREADS=1 python3 runner.py conditional
OPENBLAS_NUM_THREADS=1 python3 analyze.py development
OPENBLAS_NUM_THREADS=1 python3 analyze.py conditional
OPENBLAS_NUM_THREADS=1 python3 verify_followup.py
```

Laufzeiten und davon abhängige Aufzeichnungshashes ändern sich bei Wiederholung;
Seeds, wissenschaftliche Eingaben und Kriterien bleiben fest. Vorhandene
Rohdaten werden absichtlich nicht überschrieben. Die Basis ist Commit
`4e5e76bd24d2f37de61c3e86257e8e9458eaaeb4`.

## Entscheidung

Die **Suchreihenfolge** ist als konkrete Ursache für neun der 13 Auswahlfehler
nachgewiesen. Ein künftiger Selektor sollte Vergleichbarkeit und Zählbedingungen
vor die Begrenzung der Geometriesuche setzen und anschließend auf neuen A-Wolken
geprüft werden. Die hier belegten 28/32 sind ausschließlich bekannte Geometrie-
Machbarkeit, keine nachträgliche wissenschaftliche Freigabe.

Die vollständige Zählkovarianz stabilisiert den untersuchten neuen bedingten
Vergleich, genügt aber nicht für die festgelegte Operatorgenauigkeit. Dieser
GLS-Kandidat wird **nicht übernommen und nicht nachträglich nachgetunt**.
Sechs Kontroll-PASS und ein technischer Audit-PASS ändern den wissenschaftlichen
HOLD nicht. `HOLD_PHASE3`, `HOLD_EMBEDDING_COVARIANCE`, `METADATA_HOLD` bleiben;
kein Krümmungs-/3+1-, Kalman- oder physischer Sensoranspruch.

## English scope

After publishing successful completion of PR84 CI, this follow-up exhausts the
fixed candidate domain of all 13 failed A selections. It finds 55 feasible
fourth landmarks outside the early cap in nine failures; 31,293 candidates are
accounted for. Eligibility-before-cap would permit 28/32 selections on these
known A configurations, a retrospective feasibility result only.
Three fixed ablations diagnose count-response variance. A prespecified regularized
full-count-covariance nonlinear GLS candidate is then tested on 171 fresh B clouds
conditional on the same 19 A configurations. Paired repeat variance falls by
40.59% versus the previous Poisson fit, but primary RMSE is 16.15% worse than
direct inversion and only 12/14 required complete groups are available: **HOLD**.
All failures, frozen inputs, raw records, controls and internal audits are retained.
No new independent-A qualification, exact joint likelihood or calibrated coverage.

SPDX-License-Identifier: Apache-2.0
