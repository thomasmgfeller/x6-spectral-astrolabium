# Ergebnis: vollständiger Entwicklungsdurchlauf, Integrationsziel offen

28. Oktober 2026. **QUADRATURE_HOLD**, kein neuer Sprinkling-Lauf und keine
physikalische Rauschfreigabe. Alle vorab festgelegten Entwicklungsfälle
wurden ausgeführt. Die historische Testreihe bleibt mit ihren ursprünglichen
Ergebnissen abgeschlossen; G1 HOLD, G2/G3 NOT_RUN.

## Umfang und Kontrollen

| Prüfung | Ergebnis |
|---|---|
| Archivwolken | 8/8, nu=512, keine neuen Zufallszahlen |
| Feldsignale | 5 Felder × 2 Fenster × 8 Wolken = 80 |
| Integrationsbudget | 6/80 bestehen; alle sechs sind identisch null |
| Numerische Teilbudgets | 8/8 Wolken bestehen |
| Präzision und CPU | 128/192 Bit und ohne AVX-512, 17.396 eingeschlossene Wertvergleiche |
| Analytische Methodenkontrollen | 7/7 bestehen |
| Populationsbestätigung | NOT_RUN |
| Prädiktiver Operator-Rauschkern | NOT_QUALIFIED |
| Kompakte massive Kontinuumsdetektorreferenz | NOT_QUALIFIED |

Das feste Integrationsbudget verlangt einen komplexen Komponentenradius
höchstens 0,001 der Feldskala. Die Wellen haben Skala1; die kompakte Quelle
verwendet ihre anfängliche maximale Amplitude A/e. Die beobachteten Radien
der Einschließungen liegen ungefähr bei:

- Wellen: **0,5075 bis 3,7654**;
- kompakte Quelle auf Wolken mit nichtleerer Quellhistorie:
  **0,001260 bis 0,01307**.

Dies sind Auflösungsgrenzen der gegenwärtigen eingeschlossenen Kubatur mit
256 Boxen, keine RMS-Schätzungen des physikalischen Detektorrauschens.
Der Integrator behandelt den gesamten endlichen Detektor einschließlich
Kugelrand und kausaler Zellgrenzen; es fehlt kein unkontrolliert weggelassener
Integralrest. Seine Oberhüllen sind jedoch zu breit.

Die separaten normierten Effekte der gerundeten History und der Float-
Knotenlösung liegen unter 1,12e-15 bzw. 3,92e-16. Der größte normierte
Arb-Komponentenradius der Knotenlösung liegt unter 1,57e-26. Diese
numerischen Beiträge erklären die breiten Detektorintervalle nicht.

## Warum sechs Nullsignale kein Erfolg der Physik sind

Die nach dem Lauf hinzugefügte exakte Belegungsdiagnose zählt History-Knoten
mit t<=-1 und r<1/2. Für die kompakte H1-Quelle mit g=0 sind nur diese
Knoten ungleich null. Die Diagnose verwendet dieselben dyadischen
Archivkoordinaten und verändert keine Eingabe oder Entscheidung.

| Wolke | Nichtverschwindende kompakte History-Knoten |
|---|---:|
| d0_r00 | 2 |
| d0_r01 | 0 |
| d0_r02 | 2 |
| d0_r03 | 2 |
| d0_r04 | 0 |
| d0_r05 | 1 |
| d0_r06 | 0 |
| d0_r07 | 2 |

Bei d0_r01, d0_r04 und d0_r06 ist die gesamte kompakte diskrete History null.
Das homogene lineare Dreieckssystem und seine Query-Fortsetzung liefern
daher exakt null, in beiden Fenstern. Die sechs bestandenen
Integrationsbudgets sind korrekte Nullintegrale. Sie qualifizieren den
Anfangsdatenadapter oder die physikalische Quellenübertragung nicht.
Aus acht bereits bekannten Wolken wird keine Populationshäufigkeit leerer
Quellen mit Konfidenzgarantie abgeleitet.

## Wissenschaftliche Entscheidung

1. Der definierte endliche Detektor und der pfadweise History-Transfer sind
   implementiert, mit analytischen Kontrollen und reproduzierbaren Einschließungen.
2. Der feste Entwicklungsdurchlauf reicht noch nicht für eine genaue
   Detektor-Kovarianz oder einen unabhängigen Fluktuationsnachweis.
3. Vor neuen Bestätigungswolken müssen Integrationsgenauigkeit und
   Anfangsdatenabbildung verbessert bzw. qualifiziert werden.
4. Die ursprünglichen G1-Negativbefunde werden durch diesen neuen
   Beobachtungsansatz weder aufgehoben noch zu Quantenrausch-Evidenz erklärt.

Die gespeicherten Mittelwerte und Kovarianzen sind eingeschlossene
**endliche Stichprobenmomente**. Deren breite Intervallradien dürfen nicht
als beobachtete Streuung ausgegeben werden. Eine statistische
Populationsfreigabe ist in diesem Paket ausdrücklich nicht implementiert.

## Belege

- [Vorab festgelegter Vertrag](PROTOCOL.json), [Quellen-Freeze](FREEZE.json),
  [öffentliche Registrierung](REGISTRATION.json), [analytische Vorprüfungen](PRE_DATA_AUDIT.json).
- [128-Bit-Entscheidung](results/DECISION_128.json), [192-Bit-Entscheidung](results/DECISION_192.json),
  [Reproduktionsprüfung](results/CHECKS.json).
- [128-Bit-Rohdaten](results/BENCHMARK_128.json.gz), [192-Bit-Rohdaten](results/BENCHMARK_192.json.gz),
  [CPU-Vergleich](results/BASELINE_128.json.gz).
- [Deskriptive Quellbelegung und numerische Größen](results/DESCRIPTIVE.json),
  reproduzierbar mit `python -B research/cspp/detector_transfer_v0_9/report.py`.

Die Methodenquellen des öffentlichen Vorab-Commits bleiben unverändert.
`report.py` und dieser Ergebnistext wurden nach dem Lauf hinzugefügt und
sind keine nachträglich als vorregistriert bezeichneten Hypothesentests.
