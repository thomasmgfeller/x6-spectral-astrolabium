# Die letzten 21 Vorgängerfälle im N22-Messfenster

CST-DUST · 27. November 2026

Die Prüfung schliesst alle 21 verbliebenen Ordnungs- und Gewichtsfälle der festgelegten seriellen N22-Familie im gemeinsamen Messfenster aus. Fünf Anbindungen wurden bei beiden Gewichtsvorgaben direkt verglichen. Anschliessend wurde der gleiche Test auf die elf übrigen Registerzeilen angewandt. Eine neue stationäre Lösung des vollständigen Systems auf der A+-Anbindung 216141 dient als Kontrolle ausserhalb des Fensters.

## Modell und Aussage

Die Referenz ist xⱼ = (Yⱼ − Y₃)/(Y₇ − Y₃). Der materielle Messpunkt 19 und der leere Messpunkt 20 sind kausal unvergleichbar. Beide Uhren sollen im selben geschlossenen Fenster [31/64,33/64] liegen. Sie haben mindestens je einen gemeinsamen alten materiellen Anker in Vergangenheit und Zukunft. In Familie A liegt 21 unmittelbar vor 19 und hat dieselben alten Vorgänger und Nachfolger wie 19. In Familie B folgt 21 unmittelbar auf 20 und hat die alten Vorgänger und Nachfolger von 20. Die Uhr 21 ist in beiden Fällen nur durch die Kausalordnung und die Feldgleichungen beschränkt. Der Quellen-, Drift-, Nachimpuls- und Randvertrag bleibt derjenige der früheren Prüfungen. Für 21 werden Gewicht null und positives Gewicht in (0,1) getrennt untersucht. [Definition der Familie](https://github.com/thomasmgfeller/x6-spectral-astrolabium/pull/402) · [Veröffentlichte erste Nachfolgerprüfung](https://github.com/thomasmgfeller/x6-spectral-astrolabium/pull/403)

| Lage und Gewicht von 21 | Registrierte Fälle | Vor dieser Rechnung offen | Neu ausgeschlossen | Jetzt offen |
|---|---:|---:|---:|---:|
| Vorgänger, leer | 406 142 | 6 | 6 | 0 |
| Vorgänger, positiv | 406 142 | 15 | 15 | 0 |
| Nachfolger, leer | 406 142 | 0 | 0 | 0 |
| Nachfolger, positiv | 406 142 | 0 | 0 | 0 |
| **Gesamt** | **1 624 568** | **21** | **21** | **0** |

Die Zahl 1 624 568 umfasst 406 142 etikettierte Anbindungen mit je vier Varianten. Alle vier kommen aus derselben N19-Basis. Das Ergebnis gilt für dieses Modell, die festgelegte Randfamilie und das angegebene Messfenster. Andere Vergangenheiten oder Zukünfte des Zusatzereignisses führen zu anderen Ordnungsfamilien. Die physische Zuordnung eines Arealradius bleibt offen. Alle 60 physischen P3-Prüfpunkte stehen auf NOT_RUN.

## Vergleich bei identischer Ordnung

Auf den fünf IDs 178526, 178542, 178609, 178625 und 178660 ist jeweils dieselbe Kausalordnung mit beiden Gewichten geprüft. Die vier Gerätegewichtsbereiche betreffen die alten Geräte 16 und 18 und sind von der Gewichtsvorgabe für 21 zu unterscheiden. Eine Lösung im gemeinsamen Fenster ist bei allen zehn Paar-Einträgen ausgeschlossen.

Für beide Gewichtsvorgaben gilt G₂₁ = 0. Bei positivem Gewicht gilt zusätzlich D₂₁ = 0. Bei leerem Vorgänger ist w₂₁ exakt null, und die Gewichtsdichte wird dort nicht variiert. Der Prüfer verwendet in beiden Fällen elf Koordinaten. Im leeren Sektor steht in der sonst für D₂₁ vorgesehenen Zeile die exakte Nebenbedingung w₂₁ = 0. Alle anderen Gleichungen werden mit diesem Gewicht ausgewertet. Die sieben Uhren bleiben frei, soweit es die Chronologie und das Messfenster erlauben.

Für alle fünf Paarordnungen lässt sich die Zusatzbedingung des positiven Zweigs von Hand auswerten. Setze u = Y₁₅ + 3, v = Y₂₁ + 3 und t = Y₁₉ + 3 in den rohen Uhreneinheiten. Aus den Schichten in der Vergangenheit von 19 und 21 folgen

    D₂₁ = u² − 2uv + 3,
    D₁₉ = 11 + (18u − 2v − 16)t − 9u² + v².

Die strikte Ordnung liefert 0 < v < t < 13/4 und u < v. Aus D₂₁ = 0 folgen v = (u² + 3)/(2u) und 6/13 < u < √3. Einsetzen in 4u²D₁₉ ergibt

    P(u,t) = −35u⁴ + 68tu³ + (50 − 64t)u² − 12tu + 9.

Über der aus dem Messfenster folgenden t-Hülle [3,023437499; 3,143229167] ist P auf [6/13; 1,001] strikt negativ und auf [1,008; 7/4] strikt positiv. Der Prüfer zeigt beide Vorzeichen über die exakten rationalen Bernstein-Koeffizienten an den beiden t-Enden. P ist affin in t. Jede Lösung dieser beiden Dichtebedingungen im positiven Zweig müsste folglich −1,999 < Y₁₅ < −1,992 und −10583/10500 < Y₂₁ < −2003999/2002000 erfüllen. Diese notwendigen Schranken setzen die Existenz einer Lösung des vollen Systems nicht voraus. Im leeren Zweig entfällt die erste der beiden verwendeten Gleichungen.

## Überdeckung und Kontrollen

Die Randhülle wird aus 256 geschlossenen Driftintervallen für jede der drei Quellen −10⁻⁶, 0 und +10⁻⁶ erzeugt. Die Driftabweichung ist höchstens 10⁻⁶, die drei Nachimpulse erfüllen |vₐ| ≤ 1,12 × 10⁻¹² bei κ = 10⁻¹¹. Die Rohuhren 19 und 20 liegen in der nach aussen gerundeten Hülle [0,023437499; 0,143229167]. Für das Ereignis 21 kann stets seine echte Relation zu 19 als obere Zeitgrenze dienen. Zwischen dem Gerätesystem und den sieben alten freien Staubereignissen verschwinden für die ausgewählten Ordnungen die direkten Schichtkoeffizienten. Die Ordnung wird gegen den transitiven Abschluss geprüft.

Die Grenzen [0,10⁻⁸] und [10⁻⁸,1] an den Geräten 16 und 18 decken beliebig kleine positive Gerätegewichte mit ab. Die einseitige Dichtebedingung in diesem Bereich wird im etablierten Intervallkern berücksichtigt. Für die übrigen Gewichte gelten die ursprünglichen Bedingungen. Der Intervallkern schliesst Boxen durch notwendige Gleichungen aus. Rationale Zeilenkombinationen werden durch eine Gleitkommarechnung vorgeschlagen und mit nach aussen gerundeten ganzzahligen Endpunkten ausgewertet. Gezählt werden sämtliche Blätter des vollständigen Baums.

| Sektor | Gewichtskombinationen über alle Fälle | Besuche im Suchbaum | Widersprüchliche Blätter | Offene Blätter |
|---|---:|---:|---:|---:|
| A0 | 24 | 49 780 | 24 902 | 0 |
| A+ | 60 | 164 474 | 82 267 | 0 |
| Gesamt | 84 | 214 254 | 107 169 | 0 |

11 088 algebraische Vergleiche prüfen die elf Residuen und alle 121 Ableitungseinträge in den vier Gerätegewichtsbereichen aller 21 Fälle. Die Referenz berechnet exakte zentrierte Wirkungsdifferenzen für die physisch variierten Komponenten und prüft die Nebenbedingungen separat. Das unabhängige Nachzählen des transitiven Abschlusses vergleicht alle kausalen Paare einschliesslich ihrer Schichtkoeffizienten. Das Ausgangsregister aller 406 142 Projektionen wird nach Typ, ID und vier Anbindungsmasken abgeglichen.

## Neue stationäre Kontrolllösung

Auf A+ 216141 ist eine stationäre Lösung bei zentraler Drift, Senderquelle null und drei verschwindenden Nachimpulsen eingeschlossen. 14 freie Uhren und 11 positive Gewichte erfüllen die 25 freien Feldgleichungen. Alle 154 Kausalrelationen sind strikt erfüllt, alle positiven Gewichte liegen im offenen Einheitsintervall. Die drei Zeiger folgen ihren Abtastlücken. Das Einschlusszertifikat liefert β + q ≤ 0,000242878891 < 1 für normierten Mittelpunktfehler und Kontraktionsschranke.

| Uhr | Normierte Zeit, gerundeter Mittelpunkt | Zum Messfenster |
|---|---:|---|
| 19, materieller Messpunkt | 0,6958158 | darüber |
| 20, leerer Messpunkt | 0,4339639 | darunter |
| 21, positiver Vorgänger | 0,4890960 | darin |

Die Lageaussagen gelten jeweils für das gesamte zertifizierte Intervall. Sie betreffen einen lokal eindeutigen Zweig in seiner Lösungsbox. Der globale Ausschluss im Messfenster stammt aus der getrennten Überdeckung. Der örtliche Test verwirft diese Lösungsbox bei eingesetzten Referenzuhren nicht. Die beiden früheren stationären Nachfolgerlösungen werden ebenfalls erneut zertifiziert.

## Reproduktion

Linux, Python ab 3.11 und g++ mit C++17 genügen. Alle Eingaben sind im ZIP enthalten. Im entpackten Verzeichnis werden die aktuellen Entscheidungen, die Kontrolllösung und das Fallregister so nachgerechnet.

```sh
sha256sum -c SHA256SUMS
python3 -B pruefen.py
```

Das Prüfprogramm nutzt standardmässig zwei gleichzeitige Bäume. Die Option `--jobs 4` setzt die Parallelität auf vier. Gültige unterschiedliche Pivotentscheidungen dürfen Baumgrössen ändern. Die Klassifikation verlangt weiterhin null offene Blätter. Das vollständige zuvor verwendete Archiv ist unter `basis/Nachfolger.zip` beigefügt. Die drei vorherigen Rechenstufen einschliesslich der ursprünglichen seriellen N22-Aufzählung lassen sich zusätzlich mit `python3 -B vorlaeufe.py` aus den festgelegten Archivversionen neu starten.

`Ergebnisse.json` enthält alle Baumstatistiken, exakten Schranken und zertifizierten Uhrenintervalle. `Vorgaengervergleich.tsv` unterscheidet die 21 neuen Entscheidungen von früheren Ausschlüssen für dieselben Anbindungs-IDs. `Offene_Faelle.tsv` enthält nur noch die Spaltenüberschriften. Die als Zertifikatszentrum verwendeten Näherungswerte stehen in `Zeugenzentrum_216141.json`.
