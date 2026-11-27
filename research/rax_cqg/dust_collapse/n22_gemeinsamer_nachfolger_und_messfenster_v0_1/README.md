# Wie breit muss das Zeitfenster für ein stationäres Messpaar mit gemeinsamem Nachfolger sein?

CST-DUST · Endliches Staubballmodell · 27. November 2026

Für die drei N21-Referenzordnungen 216141, 216427 und 217269 wurden alle Anbindungen eines zusätzlichen Ereignisses 21 in der gemeinsamen strikten Zukunft der unvergleichbaren Messpunkte 19 und 20 aufgezählt. Bei allen 671 Ordnungen und beiden Gewichtsvorgaben für 21 ist ein stationäres Messpaar im ursprünglichen Fenster [31/64, 33/64] ausgeschlossen. Unter denselben Randbedingungen besitzt eine dieser Ordnungen eine zertifizierte stationäre Lösung knapp ausserhalb dieses Fensters. [Ausgangsstand auf GitHub, PR 405](https://github.com/thomasmgfeller/x6-spectral-astrolabium/pull/405)

| Referenz | Beide Verbindungen direkt | Eine direkt | Beide indirekt | Ordnungen |
|---|---:|---:|---:|---:|
| 216141 | 160 | 80 | 10 | 250 |
| 216427 | 240 | 0 | 10 | 250 |
| 217269 | 81 | 0 | 90 | 171 |
| Gesamt | 481 | 80 | 110 | 671 |

„Direkt“ bedeutet, dass zwischen dem jeweiligen Messpunkt und 21 kein weiteres Ereignis liegt. Die beiden Schichtkoeffizienten werden aus den offenen Intervallen auf der vollständigen Ordnung errechnet. Ein gemeinsamer kausaler Nachfolger kann daher in einer oder beiden Messgleichungen einen verschwindenden Koeffizienten haben. Die 531 Ordnungen mit alten Nachfolgern von 21 sowie die 140 terminalen Ordnungen sind enthalten. In jeder Ordnung wird das Gewicht von 21 einmal auf null gesetzt und einmal in (0,1) frei variiert.

## Eine positive stationäre Lösung

Der Fall 216141 / P21 = 229383 / F21 = 0 besitzt bei zentraler Drift, Quelle null und verschwindenden Nachimpulsen eine stationäre Lösung mit positivem Gewicht an 21. Hier sehen **beide** Messpunkte den terminalen Empfänger unmittelbar. Die folgenden Dezimalintervalle sind nach aussen gerundet.

| Ereignis | Normierte Uhr | Ursprungstest |
|---|---|---|
| 19 · materieller Messpunkt | [0,52687746; 0,52687752] | oberhalb |
| 20 · leerer Messpunkt | [0,50698405; 0,50698412] | innerhalb |
| 21 · gemeinsamer Nachfolger | [0,69078721; 0,69078727] | freie Uhr |

Alle 25 freien Gleichungen, 152 strikten Kausalrelationen und elf freien positiven Gewichte wurden mit rationaler Intervallarithmetik geprüft. Die normierte obere Kontraktionsschranke einschliesslich des Residuums beträgt 0,000115040271 und liegt unter eins. Die bekannte Lösung wurde durch eine numerische Suche vorgeschlagen. Ausschlaggebend ist der anschliessende Einschluss mit der tatsächlichen gemeinsamen Nachfolgerordnung. Der Zeuge gibt keine globale Eindeutigkeit an. Das technische Kennzeichen B+ im wiederverwendeten Zertifizierer bezeichnet hier den positiven Gewichtsfall. Die beiden Relationen 19 ≺ 21 und 20 ≺ 21 sind ausdrücklich in der übergebenen Ordnung enthalten.

Für diesen Zeugen sind die einlaufenden Koeffizienten an 21, in der Reihenfolge 2, 15, 16, 17, 19, 20, genau −8, 16, −9, 1, 1, 1. Aus der Stationarität der Enduhr folgt deshalb die von Hand prüfbare Gleichung

    2 Y₂₁ = −8 Y₂ + 16 Y₁₅ − 9 Y₁₆ + Y₁₇ + Y₁₉ + Y₂₀.

## Abstand zum ursprünglichen Messfenster

Für einen Zustand sei h = max(|x₁₉ − 1/2|, |x₂₀ − 1/2|), wobei xⱼ = (Yⱼ−Y₃)/(Y₇−Y₃). Über alle stationären Lösungen, beide Gewichtsfälle und alle 671 Ordnungen betrachten wir das Infimum h*. Die abgeschlossenen Rechnungen und das positive Zeugnis liefern

**0,02579426 ≤ h* ≤ 0,02687752 (nach aussen gerundet).**

Bis einschliesslich 13/512 sind alle Fälle im geschlossenen Fenster ausgeschlossen. Bei 27/1024 bleibt bei Referenz 216141 nur P21 = 229383, F21 = 0 mit positivem Gewicht und beiden Gerätegewichten ≥ 10⁻⁸ offen. Alle noch offenen Teilboxen haben Y₁₉ ≥ 0,182211358. Mit Y₃ ≤ −1,833333333 und Y₇ = 2 ergibt das innerhalb dieses Fensters die zusätzliche untere Schranke h ≥ 197756049/7666666666. Ausserhalb ist h > 27/1024. Die obere Schranke für h* folgt aus der vollständig eingeschlossenen zentralen Referenzlösung. Die Prüffolge endet gemäss Ergänzungsplan bei 27/1024. Das ist eine Schranke für das Infimum. Ob ein Zustand das Infimum annimmt, bleibt offen. Der ursprüngliche Prüfplan bleibt bei der Halbbreite 1/64. Die weiteren Breiten wurden nach dem numerischen Zeugenfund gewählt und getrennt protokolliert.

| Halbbreite | Fälle | Ausgeschlossen | Offen |
|---|---:|---:|---:|
| 1/64 | 1342 | 1342 | 0 |
| 3/128 | 1342 | 1342 | 0 |
| 13/512 | 1342 | 1342 | 0 |
| 27/1024 | 1342 | 1341 | 1 |

## Unabhängige Kontrollen

Zwei Aufzählungen (abgeschlossene Mengen und sukzessives Einfügen der alten Ereignisse) liefern dieselben 671 Anbindungen. Zusätzlich werden alle Relationen transitiv geschlossen, alle 671 Schichttabellen zwischen Python und C++ abgeglichen und im Primärlauf 33 264 Werte von Residuen, Ableitungen und Nebenbedingungen mit rationalen Wirkungsdifferenzen bzw. den expliziten Gewichtsbedingungen verglichen. Die drei stationären Kontrolllösungen aus der seriellen Familie werden erneut zertifiziert.

Der Primärlauf schliesst alle 1 342 Ordnungs- und Gewichtsfälle mit den drei publizierten Quellen, 256 Driftintervallen und den erlaubten Nachimpulsen aus. In den Fällen mit endlicher, nichtleerer Uhrhülle deckt der Prüfer die vier Teilbereiche für die Gewichte an 16 und 18 ab. Für terminale positive Fälle ohne endliche Zeitschranke werden von Y₂₁ unabhängige Bedingungen eingesetzt. Die bekannte Schranke 6 darf dort nur in der alten Chronologie verwendet werden. Für einen leeren terminalen Empfänger kann die Enduhr in den alten Gleichungen entfallen.

Als zusätzliche Kontrolle eliminiert das Endpolynom die Enduhr. Mit cᵢ = cᵢ₂₁ und A = Σcᵢ ergibt sich aus G₂₁ = D₂₁ = 0 bei positivem terminalem Gewicht

    19 A + Σᵢ<ⱼ cᵢ cⱼ (Yᵢ − Yⱼ)² = 0.

Die Summe läuft über ungeordnete Paare verschiedener Eingangsetiketten. Bei A = 0 bleiben beide Momentenbedingungen erforderlich. In keinem der 140 positiven terminalen Primärfälle reicht die direkte Intervallauswertung des Endpolynoms auf der Anfangshülle alleine zum Ausschluss.

Für den kritischen positiven Endpunkt wird bei h ab 27/1024 zusätzlich G₂₁ durch w₂₁ geteilt. In dieser Ordnung haben 17 und 20 dieselben auslaufenden Koeffizienten und Gewicht null. Die Differenz ihrer Uhrgleichungen liefert eine Schranke für (−9w₇ + 16w₈ − 8w₉ + w₁₈ + w₂₁)(Y₁₇−Y₂₀) aus der Gerätetoleranz an 17. Im regulären Gewichtszweig verengt eine eindimensionale rationale Überdeckung von D₁₆ und D₁₉ die Uhren 15 und 16. D₁₈−D₁₉ liefert eine weitere Schranke. Im regulären Gewichtsbereich des kritischen Falls wird zusätzlich die Messuhr 19 in aneinandergrenzende geschlossene Intervalle geteilt. Jede Teilrechnung verwendet ihre jeweils eigene Hülle für die Uhren 15 und 16. Die zugrunde liegenden Koeffiziententabellen und der zertifizierte positive Kontrollzustand werden geprüft.

## Offline wiederholen

Das Archiv enthält Quelltext, Eingaben, die vorige Studienversion, Fallregister und sämtliche Baumstatistiken. Erforderlich sind Python ab 3.10, die Standardbibliothek und GNU g++ mit C++17.

```sh
sha256sum -c SHA256SUMS
python3 -B wiederholen.py --jobs 4
```

Für den ursprünglichen Versuch allein genügt `python3 -B pruefen.py`. Im Fallregister bedeutet Bit j der Dezimalmasken P21 und F21, dass Ereignis j vor bzw. nach 21 liegt (0 ≤ j < 19). Die Zahl der Zwischenereignisse zu 19 und 20 ist separat angegeben. Ergebnisse.json enthält die Baumstatistiken, rationalen Uhrenintervalle und Kontrollrechnungen. Die zusätzlichen Fenster stehen unter Fenstervergleich/. Fenstervergleich.tsv und Schranken.json fassen Überdeckung und Infimumsschranken zusammen. Unterschiedliche gültige Vorkonditionierer dürfen die Zahl der Baumblätter verändern. Der Wiederholungstest kontrolliert die Klassifikation für jeden Gewichtsbereich.

Die gemeinsame Zukunft belegt eine kausale Beziehung. Ob das Ereignis ein physisch auslesbares Signal trägt, wie sich daraus ein Arealradius ergibt und wie sich der Staubball fortsetzt, bleibt offen. Die 60 physischen P3-Prüfpunkte stehen auf NOT_RUN.
