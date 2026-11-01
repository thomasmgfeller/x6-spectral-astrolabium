# Entscheidungsregel, Unsicherheit und Gegenproben

Die primäre Unsicherheitsbilanz und die acht Rechenschritte stehen in GUM_BILANZ.md. Dieses Dokument beschreibt den getrennten Konformitätsentscheid und seine statistischen Grenzen.

## Ein Kriterium für die 2 ppm

Die Referenzbescheinigung ist eine Aussage für den Knoten C01 bei z=1/4 und einen identifizierten Gültigkeitsbereich. Erforderlich sind nach unabhängiger fachlicher Prüfung zeitgleich gültige Intervalle P=[p₋,p₊] für das Zielmittel, A=[a₋,a₊] für den gemeinsamen Gain und Y=[y₋,y₊] für das Vergleichsmittel in der Kalibrierkonfiguration. Hinzu kommt b≥0, eine zusätzliche absolute Schranke für die Differenz zwischen den Abweichungen in Kalibrier- und Anwendungsbedingungen am selben Stützpunkt. Ein Beitrag darf genau einmal eingehen. b ist hier Teil der 2 ppm und getrennt von der v0.11-Extrapolation auf andere Zustände.

Wegen 0≤p≤1 und 0,99≤a≤1,01 liegt ap in [a₋p₋, a₊p₊]. Das obere Ende wird auch bei Produkten über eins nicht abgeschnitten. Die größte mögliche absolute Differenz über diese Intervalle liegt an einem Paar gegenüberliegender Endpunkte. Die zulässige Schranke ist damit

    B = max(|y₋ − a₊ p₊|, |y₊ − a₋ p₋|) + b.

Der Rechenweg erfüllt die numerische Bedingung, wenn B≤2/1.000.000 gilt. Abhängigkeiten der Eingangsgrößen schaden dieser konservativen Intervallrechnung nicht, sofern die Intervalle gemeinsam überdecken. Wer Korrelationen für einen kleineren Fehler ansetzen will, braucht eine gesonderte begründete gemeinsame Schranke. Die bloße Deklaration, die Referenz treffe das Ziel bereits auf 2 ppm, ist kein unabhängiger Nachweis. Ein Labor muss die Bestimmung von P und Y, die Messgleichung, die Herkunft der Substitutionskorrektur und die Unsicherheiten der unabhängigen Beobachtungen offenlegen.

Die Summen der vorab begründeten Nichtüberdeckungsrisiken für P, A, Y und b werden konservativ auf **0,000002 pro Knoten** begrenzt. Das ist eine neue Planwahl. Sie betrifft die Wahrscheinlichkeit eines falschen Zertifikats und ist von der gleich geschriebenen absoluten Wahrscheinlichkeitstoleranz zu unterscheiden. Deterministische technische Schranken dürfen Risiko null nur mit belastbarem Nachweis erhalten. Ein gewöhnliches 95-%-Intervall hat für sich allein kein entsprechend kleines Risiko. Ein Erweiterungsfaktor k genügt nur mit begründeter Verteilung und Überdeckung. Keine ungestützte Extrapolation in einen extremen Verteilungsschwanz.

Würde man die Zuteilung vorab für alle 32 Knoten verwenden, ergäbe die Vereinigungsabschätzung 0,000064. Zusammen mit der konservativen v0.11-Grenze 0,009837802283 blieben bis zur 1-%-Grenze weitere 0,000098197717 für **alle übrigen** externen Fehlzertifizierungen. Mehrfach genutzte Quellen, Wiederholungsläufe und neue Konfigurationen müssen in das Gesamtbudget eingeordnet werden. Ein erfolgreicher C01-Rechencheck allein gibt keinen weiteren Knoten, keine laufende Anlage und keine Geometrie frei.

## Was sich mit null Widersprüchen belegen ließe

In einem *eigenen* vorab festgelegten Vergleich gegen korrekte externe Ereignislabels seien die Fehlindikatoren unabhängig und identisch Bernoulli-verteilt, m ihre Fehlerwahrscheinlichkeit. Bei n Vergleichen hat null Fehler die Wahrscheinlichkeit (1−m)ⁿ. Der einseitige obere Grenzwert beträgt bei null Fehlern 1−α^(1/n). Für α=0,000002 reichen 3.300.000 Vergleiche selbst dann nur für höchstens 3,976465845 ppm (nach außen gerundet). Für 2 ppm und 1 ppm sind bei null Fehlern mindestens 6.561.176 bzw. 13.122.357 nötig. Die halbe Toleranz von 1 ppm wäre beispielsweise relevant, falls für andere *deterministisch* belegte Fehler 1 ppm verbraucht wird. Die Zahlen verwenden das ganze Knotenzertifikatsrisiko für diesen einen Test und dürfen nicht zu weiteren statistisch unsicheren Komponenten addiert werden, ohne das Budget neu aufzuteilen.

Dies sind Mindestzahlen für **diese Nullfehlerregel**. Der vorgelagerte ideale Vergleich ist keine vorhandene Funktion des optischen Aufbaus. Sind X und Y zwei Auslesungen desselben Detektors, darf m allein die digitale Widerspruchsrate beschreiben. Die v0.11-Regel mit höchstens 25 Abweichungen in 3,3 Millionen Paaren prüft die übrigen 14 ppm Diskordanz (zuzüglich 6 ppm äußerer Modellreserve). Sie kann die externe 2-ppm-Komponente dieser Reserve nicht mit denselben Daten selbst bescheinigen.

## Kontrolle auf gemeinsamen Fehler

Bei Gain 1 sei Y in beiden Welten exakt dieselbe Bernoulli-Antwort mit Mittelwert 0,5, und X=Y für jedes Ereignis. In Welt A sei p₀₁=0,5, in Welt B sei p₀₁=0,500050. Das Gesetz aller X/Y-Register ist identisch, die Zielabweichungen sind 0 und 50 ppm. Nur unabhängige Information über das Ziel oder den Vergleich kann die Welten trennen. Die synthetischen Kontrollen prüfen zusätzlich ein belegtes enges Intervall (1,40000006 ppm), eine gemeinsam verschobene Antwort mit enger aber zu weit entfernter Referenz (50,69999994 ppm) und enge Zahlen bei unzureichender Überdeckung.

## Wissenschaftliche Bezüge

- [Eigenzeit v0.11, PR 174](https://github.com/thomasmgfeller/x6-spectral-astrolabium/pull/174) und [v0.5, Definition von Referenzpartition und Detektionswahrscheinlichkeit](https://github.com/thomasmgfeller/x6-spectral-astrolabium/blob/084b2ed8b52e099e4ce6205e5b4217fad89e1e1e/research/eigenzeit/calibration_v0_5/BEWEIS.md).
- [Optikplan des Projekts, Seite mit D0–D3/E01](https://github.com/thomasmgfeller/x6-spectral-astrolabium/blob/084b2ed8b52e099e4ce6205e5b4217fad89e1e1e/experiments/photonic-two-qubit/optics/optikplan-v0.1/Optikplan_v0_1.pdf) und [Herstellerunterlagen der SPCM-AQRH-Familie](https://www.excelitas.com/product/spcm-aqrh).
- [JCGM VIM 2.41, metrologische Rückführbarkeit](https://jcgm.bipm.org/vim/en/2.41.html) und [JCGM 106, Messunsicherheit bei Konformitätsentscheidungen](https://www.bipm.org/en/doi/10.59161/jcgm106-2012).
- [Gerrits et al., Metrologia, DOI 10.1088/1681-7575/ab4533](https://www.nist.gov/publications/calibration-free-space-and-fiber-coupled-single-photon-detectors-0) und [Jin et al., Applied Optics, DOI 10.1364/AO.461154, Substitutionsverfahren](https://www.nist.gov/publications/calibration-and-comparison-detection-efficiency-free-space-single-photon-avalanche).
- [NIST IR 8486, Definition von Systemdetektionseffizienz und Bezugsebene](https://nvlpubs.nist.gov/nistpubs/ir/2023/NIST.IR.8486.pdf), [NIST, exakte einseitige Binomialgrenze](https://www.itl.nist.gov/div898/software/dataplot/refman2/auxillar/exacbino.htm).
- [Grangier, Roger und Aspect (1986), Antikorrelation am Strahlteiler](https://doi.org/10.1209/0295-5075/1/4/004). [METAS, Schweizer Fachbereiche für Optik und Photonik](https://www.metas.admin.ch/de/optik-p).
