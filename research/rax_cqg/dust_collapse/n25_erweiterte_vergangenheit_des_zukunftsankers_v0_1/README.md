# CST-DUST · Zusätzliche alte Vorgänger des N25-Zukunftsankers

Auf der N22-Grundordnung 216141/229383/0/+ braucht ein stationärer Kontakt der hier untersuchten Sonde 22 mit Partner 18 oder 19 mindestens drei weitere **alte** Vorgänger des letzten Ankers 24 über das Hauptideal des Partners hinaus. Diese notwendige Bedingung gilt im frühen Fenster, für die schwere und die leichte Präparation, bei einer ursprünglich terminalen Sonde und genau zwei frei variierenden positiven Nachfolgern. Ob drei alte Vorgänger genügen, ist offen.

[Vorstudie auf GitHub · PR 417](https://github.com/thomasmgfeller/x6-spectral-astrolabium/pull/417) · [Modell, Eingaben und bisherige Minimalfamilie am verwendeten Commit](https://github.com/thomasmgfeller/x6-spectral-astrolabium/tree/9d476610314a68f0a8b413ddc843aa5e24b90071/research/rax_cqg/dust_collapse/n24_n25_zukunftsanker_terminaler_sonden_v0_1)

## Messfrage und Umfang

Die 22 alten Ereignisse behalten ihre gegenseitigen Relationen. Die induzierte N23-Ordnung enthält die leere quellenfreie Sonde 22 mit einer ursprünglichen Zukunft ohne Ereignisse. Die neuen positiven Innenereignisse 23 und 24 bilden mit ihr die strikte Kette 22 vor 23 vor 24. Für einen Kontakt müssen 22 und der positive Partner q ∈ {18,19} im geschlossenen Fenster [15/32,17/32] der normierten Uhr xᵢ=(Yᵢ−Y₃)/(Y₇−Y₃) liegen, kausal unvergleichbar sein und gemeinsame positive Anker in Vergangenheit und Zukunft besitzen. Die bisherigen inneren Uhren und Gewichte dürfen sich mit den neuen Ereignissen stationär einstellen. Weder die späteren Innenfelder noch die Uhren der beiden Nachfolger werden auf ihre alten Werte oder auf das Messfenster fixiert.

P,A,B bezeichnen die Mengen der alten Vorgänger von 22,23,24. Das Hauptideal I(q) besteht aus q und allen seinen alten Vorgängern. Jede zulässige Einfügung entspricht genau drei nach unten abgeschlossenen Mengen mit P ⊆ A ⊆ B, I(q) ⊆ B, q ∉ P und P ≠ ∅. Jedes nichtleere P enthält das positive Ereignis 0, einen gemeinsamen Vorgänger. In Stufe k umfasst B genau k weitere alte Ereignisse ausserhalb von I(q). Die Gesamtzahl der Ereignisse ist auf beiden Stufen 25.

| Zusätzliche alte Vorgänger | Partner 18 | Partner 19 | Fälle je Präparation | Ergebnis |
|---|---:|---:|---:|---|
| 0, PR 417 | 155 | 20 | 175 | Alle ausgeschlossen, übernommener Befund |
| 1, vereinbarter Lauf | 582 | 166 | 748 | Alle ausgeschlossen |
| 2, Anschlusslauf | 2 667 | 699 | 3 366 | Alle ausgeschlossen |
| 3, nur gezählt | 7 471 | 2 801 | 10 272 | Feldgleichungen offen |

In Stufe 1 ergeben sich für Partner 18 die Zusatzmengen {3} mit 349 und {19} mit 233 Fällen. Für Partner 19 ergeben sich {3} mit 46, {17} mit 60 und {20} mit 60 Fällen. Stufe 2 besteht aus elf Partner/Zusatzmengen-Gruppen. Ergebnisse.json enthält die Aufschlüsselung. Die 4 114 neuen Zertifikate gelten jeweils auf der gemeinsamen Kragenuhrhülle beider Randpräparationen. Das ergibt 8 228 Einträge in den Fallregistern. Die rechtwinklige Hülle umfasst auch Zwischenwerte und bewahrt jede frühere Unsicherheit der vorgegebenen Kragenuhren. Die Ausschlüsse verwenden die Positivität der betreffenden Gewichte. Die 8 228 Einträge zählen die Anwendung der Zertifikate auf beide Präparationen.

## Feldgleichungen und Zertifikate

Die Schichtkoeffizienten der strikten Transitivrelation sind 1, −9, 16, −8, 0 bei null, eins, zwei, drei oder mindestens vier Ereignissen im offenen Intervall. Auf den vier vorgegebenen Gerätepaaren gilt zusätzlich −10⁻¹¹. Die notwendige Dichtegleichung an jedem variierten positiven Innenereignis j lautet Dⱼ=19+Σᵢ kᵢⱼ(Yⱼ−Yᵢ)²=0. Mit Hⱼ=Σᵢ kᵢⱼ(Yⱼ−Yᵢ) lautet die Uhrgleichung Gⱼ=Σₘ kⱼₘ wₘ(Yₘ−Yⱼ)−wⱼHⱼ=0. Alle strikten Relationen verlangen streng wachsende Uhren.

Die Sonde hat nur zwei Nachfolger. Mit t=Y₂₃−Y₂₂>0 und v=Y₂₄−Y₂₃>0 ergibt G₂₂=0 das Verhältnis w₂₄/w₂₃=t/[9(t+v)]. Damit erzwingt G₂₃=0 die Gleichung 9H₂₃(t+v)=tv. Insbesondere gilt 0<9H₂₃<min(t,v). Ereignis 24 ist terminal und positiv, also H₂₄=0.

| Verwendeter Nachweis | Stufe 1 | Stufe 2 |
|---|---:|---:|
| Lineare Uhrbedingungen | 431 | 2 031 |
| Dichte- und Uhrbedingungen mit Intervallschranken | 317 | 1 333 |
| Zusätzlich algebraische Elimination beider Nachfolgeruhren | 0 | 2 |

Eine physische Lösung erfüllt jede verwendete notwendige Bedingung. Jede Multiplikation von Intervallvariablen wird nach aussen eingeschlossen. Grundlage sind die vier McCormick-Ungleichungen für Produkte sowie Tangenten und Sekanten für Quadrate. Jede Verschärfung einer Uhrgrenze wird aus ihrer vorherigen Box rational verifiziert. Die Summe gültiger Ungleichungen L≤0 mit nichtnegativen rationalen Multiplikatoren kann keine strikt positive Untergrenze haben. Jede veröffentlichte Endentscheidung weist genau diesen Widerspruch nach. Wenn der Prüfer eine Uhrgrenze für einen Nachfolger benutzt, verifiziert er diese zuvor auf dem unbeschränkten linearen Problem. Drei Zertifikate der zweiten Stufe verwenden je eine Intervallteilung. Beide geschlossenen Teilintervalle werden nachgerechnet.

### Wenn Ereignis 21 einen Nachfolger bekommt

Bei Partner 18 und der Zusatzmenge {19,21} liegt 21 in B. In 233 der 283 Ordnungen gehört es nur B an, in 48 auch A, in zwei auch P. Die notwendige Uhrbedingung an diesem alten positiven Ereignis folgt jetzt aus seinen tatsächlichen ausgehenden Beiträgen.

- Nur 24 als Nachfolger liefert w₂₁H₂₁=w₂₄(Y₂₄−Y₂₁)>0.
- In A und ausserhalb P liefern die Koeffizienten +1,−9 nach Einsetzen des Gewichtsverhältnisses w₂₁H₂₁=w₂₃v(Y₂₂−Y₂₁)/(t+v). Daher ist H₂₁(Y₂₂−Y₂₁)≥0.
- In P folgt 22 auf 21 und hat Gewicht null. Die beiden positiven Nachfolger haben die Koeffizienten −9 und 16. Für d=Y₂₂−Y₂₁>0 ist ihre Summe, geteilt durch w₂₃, gleich −9(d+t)+16t(d+t+v)/[9(t+v)]. Wegen t(d+t+v)/(t+v)≤d+t ist sie strikt negativ.

Auch die Dichtegleichung an 21 bleibt aktiv. Wenn eine Uhrhülle benötigt wird, kann der Prüfer aus der quadratischen Gleichung in Y₂₁ eine Cauchy-Wurzelschranke herleiten. Die frühere Gleichung H₂₁=0 wird nur auf Ordnungen benutzt, auf denen 21 nach wie vor terminal ist.

### Zwei Fälle ohne obere Schranke für die Nachfolgeruhren

Bei den Registerfällen 2467 und 2483 der zweiten Stufe ist q=18 und B=I(18)∪{19,21}. Im ersten Fall ist P={0,1,17} und A={0,1,2,15,16,17}, im zweiten steht in beiden Mengen 20 anstelle von 17. Beide Fälle haben Σᵢkᵢ,₂₃=0 und Σᵢ≠₂₃ kᵢ,₂₄=0 bei k₂₃,₂₄=1. Aus H₂₄=0 folgt v=V mit V=Σᵢ≠₂₃ kᵢ,₂₄Yᵢ. Ferner ist h=H₂₃=−Σᵢ kᵢ,₂₃Yᵢ unabhängig von Y₂₃. Definiere

    A₀ = 19 + Σᵢ kᵢ,₂₃ (Y₂₂−Yᵢ)²,
    B₀ = 19 + Σᵢ≠₂₃ kᵢ,₂₄ (Y₂₂−Yᵢ)² − V².

Die Dichtegleichungen lauten dann A₀+2ht=0 und B₀−2Vt=0. Die Uhrgleichung 9h(t+V)=tV eliminiert t und liefert B₀+9A₀−18hV=0. Es gelten zugleich A₀≤0, B₀≥0 und 0≤9h≤V. Diese notwendigen Bedingungen enthalten nur die alten Uhren und die Fensteruhr 22. Die beiden Zertifikate benutzen diese Projektion ohne jede Vorannahme über die maximale Uhrzeit von 23 oder 24. Der zweite Prüfer vergleicht die Polynomkoeffizienten symbolisch mit denen der Originalgleichungen.

## Offline wiederholen

Nach dem Entpacken im Studienverzeichnis mit Python ab 3.10 und seiner Standardbibliothek ausführen. Mit dem optionalen Argument --jobs 4 kann jeder Prüfer vier CPU-Kerne verwenden.

```sh
sha256sum -c SHA256SUMS
python3 -B auswerten.py
python3 -B gegenprobe.py
```

auswerten.py rekonstruiert die Zertifikatszeilen aus der exakten Relation und vergleicht beide Fallregister sowie die Ergebnisdatei byteweise. gegenprobe.py enumeriert die alten Ideale unabhängig über Antiketten, baut alle zulässigen Teilmengen auf und prüft die in den einzelnen Fällen verwendeten Feldumformungen anhand der Originalkoeffizienten. Die Fallnummern beginnen in jeder Stufe bei 0. input/Vergleichspaar.json ist bytegleich mit der Eingabe aus PR 417. Die numerische lineare Optimierung lieferte die Multiplikatorvorschläge. Die archivierten rationalen Nachweise lassen sich ohne Optimierer prüfen.

Die erste Stufe und das gemeinsame Beweiskriterium sind in Pruefplan.md festgehalten. Erweiterung.md dokumentiert die zusätzliche Stufe nach Sichtung der ersten Zertifikate. Es gab keine externe Vorregistrierung. Die Grenze von mindestens drei alten Zusatzvorgängern betrifft diese Grundordnung, diese Partner, die Kette mit zwei positiven Nachfolgern und das vereinbarte Messfenster. Andere Sonden, Vergangenheiten mit drei oder mehr Zusätzen, andere Materiepartner und der physische Rand des Staubballs erfordern eigene Feld- und Geometrienachweise. Acht physische Pilotradien und 60 P3-Prüfpunkte stehen auf NOT_RUN.
