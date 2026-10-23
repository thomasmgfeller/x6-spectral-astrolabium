# Kaskoden-Frontend: PCB-Entwurf v0.1

**Entwicklungsentwurf · 23.10.2026 · Hardwareprüfungen: NOT_RUN**

[PDF herunterladen / lesen](../../manuals/PCB_Kaskoden_Frontend_Entwurf_v0_1.pdf) ·
[Photonik-Projekt](../../README.md) · [Herkunft und Prüfsummen](../../PROVENANCE.json)

Der fünfseitige Vorschlag beschreibt eine einkanalige, vierlagige Messplatine für die
SPAD-Messkette. Er konkretisiert Lagenaufbau, Kaskoden-Startwerte, 50-Ω-Ausgangspfade
und vorläufige Abnahmekriterien. Er enthält **keinen vollständigen Schaltplan,
kein geroutetes PCB, keine Gerberdaten und keine Hardwarequalifikation**.

**English abstract.** A four-layer single-channel cascode frontend design proposal
with a 3.3 V analog stage, controlled 50-ohm CML output paths and proposed acceptance
criteria. Component values are starting points for circuit simulation. No fabricated
board, SPICE/EM validation, measured timing performance or fabrication approval is
claimed. The original German PDF is published unchanged.

## Vorgeschlagene Auslegung

| Bereich | Entwurfsziel / Startwert |
|---|---|
| Platine | Nominal 80 × 50 mm, 1,6 mm FR-4; nach Isolationsauslegung anpassen |
| Lagen | L1 schnelle Signale, L2 geschlossene Masse im Signalbereich, L3 Versorgung, L4 langsame Steuerung |
| L1-L2 | 0,18 mm Dielektrikum als Hersteller-Abstimmungswert |
| Analoger Signalpfad | Insgesamt ≤5 mm Leiterbahnlänge von APD-Anode bis Komparator als Platzierungsziel |
| Sense | 49,9 Ω / 0,1 %; keine automatische breitbandige Anpassung des gesamten Eingangs |
| Kaskode | Zwei BFP420 als Simulationskandidaten; 3,3 V, ca. 3 mA, RE 47 Ω, RC 330 Ω |
| Diskriminator / Schwelle | ADCMP607 und DAC80501 im 2,5-V-Bereich |
| Ausgang | Q und QN jeweils als 50 Ω ±5 %; CML-kompatibler Abschluss am Empfänger |
| Passive Ausgangsverbindung | Vorgeschlagenes Prüfband 0,1-3 GHz; an reale Flanken anzupassen |

Die Leiterbahnbreite folgt erst aus dem bestätigten Hersteller-Stackup einschließlich
Kupferdicke und Lötstoppmaske. Der ADCMP607 benötigt einen zur CML-Schnittstelle
passenden Abschluss gegen VCCO; ein 50-Ω-Oszilloskopeingang gegen Masse ist nicht
derselbe Abschluss. Ein vorhandener passender Empfängerabschluss wird berücksichtigt.

## Nachgerechnete Näherungen und Aussagegrenzen

- Bei angenommenen 3 mA und 25 °C ergibt das einfache Kleinsignalmodell
  `|Av| ≈ 330 / (47 + 0.02585 / 0.003) = 5.93`.
- Der angenäherte Ausgangsruhewert beträgt
  `3.3 - 0.003 * 330 = 2.31 V`. Deshalb sieht dieser Entwurf den
  **2,5-V-DAC-Bereich statt des früheren 1,25-V-Bereichs** vor.
- Ein RC-Modell mit 49,9 Ω und 10 pF ergibt rund 319 MHz Grenzfrequenz und
  1,096 ns Anstiegszeit. Die wirksame Kapazität umfasst auch Schutz, Gehäuse,
  Platine, Eingang und Messmittel.
- Ein einzelner Übergang zwischen idealen 50 Ω Last und einer Leitung mit
  47,5-52,5 Ω hat höchstens 2,56 % Reflexionskoeffizient. Damit ist das gesamte
  Ringing einer realen Verbindung nicht begrenzt.

Diese Berechnungen sind Näherungen und keine SPICE-/Feldlöser-Ergebnisse.
Die PDF trennt zufälligen Jitter, amplitudenabhängige Laufzeit und Quench-Rückkopplung.
Insbesondere wird aus den Kennzahlen des ADCMP607 kein pauschales
50-ps-Gesamttiming abgeleitet.

## Vorläufige Abnahmekriterien

| Prüfung | Vorgeschlagenes Ziel | Status |
|---|---|---|
| Impedanzcoupon | 47,5-52,5 Ω unter deklarierter TDR-Auswertung | NOT_RUN |
| Passive Ausgangsverbindung | S11/S22 ≤ -20 dB, 0,1-3 GHz, 50-Ω-Bezug | NOT_RUN |
| Pulsantwort | ≤10 % Über-/Unterschwingen; keine zusätzlichen Schwellwertübertritte | NOT_RUN |
| Elektrische Paarstreuung | ≤50 ps RMS bei festgelegten Pulsbedingungen | NOT_RUN |
| Kalibrierter Zeitfehler | Betrag der Restabweichung plus Unsicherheit ≤200 ps, unabhängige Prüfpunkte | NOT_RUN |
| Quench und optische Erholung | Ersatzlastprüfung, danach unabhängige Detektormessung | NOT_RUN |

Die Ziele werden vor dem Versuch samt Bedingungen eingefroren. Bei Verfehlen des
Zeitfehlerziels sind Komparator oder Diskriminationsverfahren zu überarbeiten.
Schwingungen, Sättigung oder Quench-Rücktrigger erfordern eine Korrektur des
Einzelkanals vor der Vervielfachung.

**Nächster technischer Schritt:** vollständiger Schaltplan mit Bias, Schutz,
Empfänger und Quench-Einkopplung; anschließend Simulation und Hersteller-Stackup,
danach KiCad-Routing und Abnahme. Die bestehende digitale Sagnac-Referenz wird
durch diese Dokumentveröffentlichung nicht verändert.

## Quellen

Die sechs Quellen sind im PDF verlinkt. Es werden eigene Entwurfstexte veröffentlicht;
Herstellerunterlagen werden nicht mitkopiert.

1. [Analog Devices, ADCMP606/ADCMP607, Rev. C](https://www.analog.com/media/en/technical-documentation/data-sheets/ADCMP606_607.pdf)
2. [TI, High-Speed Layout Guidelines, SCAA082A](https://www.ti.com/lit/an/scaa082a/scaa082a.pdf)
3. [Excelitas, C30902SH Series, Rev. 2022.02](https://www.excelitas.com/file-download/download/public/61601?filename=Excellitas_Si_APD_C30902SH_Series_Datasheet.pdf)
4. [Infineon, BFP420, Rev. 3.0](https://www.infineon.com/assets/row/public/documents/30/49/infineon-bfp420-datasheet-en.pdf)
5. [TI, DACx0501, SBAS794E](https://www.ti.com/lit/ds/symlink/dac80501.pdf)
6. [Analog Devices, ADCMP607 external 50-ohm pull-ups](https://ez.analog.com/other-products/a/documents/DO22689/adcmp607---why-example-circuits-have-external-50r-pull-ups)

Eigene Projektbeiträge folgen dem bestehenden [Apache-2.0-Lizenzumfang](../../../../LICENSE_SCOPE.md).
Die Veröffentlichung ist keine Bestätigung der Eignung durch die genannten Hersteller.
