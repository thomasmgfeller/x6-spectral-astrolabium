# Der Nachfolgersektor im N22-Messfenster

CST-DUST · Forschungsnotiz vom 27. November 2026

Für alle 40 im Eingangsregister noch offenen Anbindungen mit positivem Nachfolger 21 ist ein stationäres Messpaar im gemeinsamen Fenster ausgeschlossen. Zusammen mit den publizierten Vorrechnungen sind damit alle 406 142 Anbindungen mit positivem Nachfolger und alle 406 142 mit leerem Nachfolger entschieden. Die Aussage gilt für die definierte Familie endlicher etikettierter N22-Ordnungen. Der ursprüngliche N22-Test unterscheidet vier Kombinationen aus Lage und Gewicht von 21. [Letzter veröffentlichter Ausgangsstand](https://github.com/thomasmgfeller/x6-spectral-astrolabium/pull/403) · [Definition der N22-Familie](https://github.com/thomasmgfeller/x6-spectral-astrolabium/pull/402)

| Lage von 21 | Gewicht | Fälle | Vorher offen | Neu ausgeschlossen | Jetzt offen |
|---|---|---:|---:|---:|---:|
| Unmittelbar vor 19 | null | 406 142 | 6 | 0 | 6 |
| Unmittelbar vor 19 | positiv | 406 142 | 15 | 0 | 15 |
| Unmittelbar nach 20 | null | 406 142 | 0 | 0 | 0 |
| Unmittelbar nach 20 | positiv | 406 142 | 40 | 40 | 0 |
| Gesamt | | 1 624 568 | 61 | 40 | 21 |

## Stationarität und Zeitordnung

Die Uhren des positiven Punkts 19 und des leeren Punkts 20 sollen beide im normierten Intervall [31/64,33/64] liegen. Die Normierung lautet x = (Y−Y₃)/(Y₇−Y₃). Die gemeinsame Rohzeithülle beträgt [0,023437499; 0,143229167]. Die alte Ordnung, Gewichtsvorgabe und Randfamilie bleiben Teil des Versuchs. In Familie B hat der Nachfolger 21 dieselben alten Vorgänger und Nachfolger wie 20. Nur die Uhren 19 und 20 haben ein Messfenster.

Für einen gerichteten Schichtbeitrag cᵢⱼ gilt Dⱼ = 19 + Σᵢ cᵢⱼ(Yⱼ−Yᵢ)² und Gⱼ = Σₖ cⱼₖ wₖ(Yₖ−Yⱼ) − wⱼ Σᵢ cᵢⱼ(Yⱼ−Yᵢ). Die Koeffizienten sind 1, −9, 16 oder −8 für null bis drei Ereignisse im offenen Intervall und sonst null. Am positiven Punkt 19 und am positiven Nachfolger 21 gilt D = 0. An den neuen Punkten gilt G = 0. Für die Geräte 15–18 liegt der Korrekturterm in G innerhalb von ±10⁻⁸. Für die Dichte an 16 und 18 wird die obere Schranke 2,001 × 10⁻⁶ verwendet. Bei Gewichten ab 10⁻⁸ gilt zusätzlich die untere Schranke −2,001 × 10⁻⁶. Das rechnerische Minimum −100 000 im kleinen Gewichtsbereich liegt ausserhalb der möglichen Dichtewerte. Für diese Geräte liegen die Vorgängeruhren und die Geräteuhr zwischen −5 und 2. Bereits 21 Terme mit |c| ≤ 16 und Zeitabstand ≤ 7 ergeben |D| ≤ 19 + 21 × 16 × 49 < 100 000.

| Schritt | Grundlage der Zeitschranken | Fälle | Suchbäume | Geschlossene Blätter |
|---|---|---:|---:|---:|
| 1 | Nur 19≺7 fehlt unter den getesteten Relationen. Die Messzeit beschränkt Uhr 19. | 21 | 84 | 123 751 |
| 2 | 20≺7 und 21≺7 fehlen. Wo auch 19≺7 fehlt, greift das Messfenster. Für 21 gilt 21≺8. | 10 | 40 | 46 642 |
| 3 | Gerichtete Schichtkopplungen vom Staub zur Messung. Alle kausal möglichen Wurzeln der alten Staubdichtegleichungen werden eingeschlossen. | 9 | 36 | 61 728 |

Für jede Ordnung wird der transitive Abschluss aus der alten Ordnung und den Anbindungsmasken rekonstruiert. Eine Zeitbeschränkung fügt keine Kante hinzu. In Schritt 2 und, wo erforderlich, in Schritt 3 wird für die anfängliche obere Schranke der Uhr 21 die verifizierte Randuhr 8 verwendet (Y₈ ≤ 3,000720059). Die Schichtkoeffizienten werden auf der tatsächlichen Ordnung berechnet.

Bei neun Anbindungen gehen sämtliche Schichtkanten zwischen den sieben Staubereignissen und der Gerätegruppe vom Staub zu den neuen Messereignissen. Die Dichtegleichungen der sieben positiven Staubereignisse können in der Reihenfolge 4, 5, 6, 11, 12, 13, 14 eingegrenzt werden. Der Prüfer bestimmt für jede Uhr Zeitgrenzen aus ihren Vorgängern und bekannten Nachfolgern. Er unterteilt diese Hülle in geschlossene Intervalle und verwirft eine Box, wenn das mit ganzzahligen Endpunkten ausgewertete Dichteintervall null ausschliesst. Aus sämtlichen verbleibenden Boxen bildet er eine Hülle. Sie geht als äusserer Parameter in die späteren Gleichungen ein. Ein Beispiel für ID 202359 ist Y₄ ∈ [−1,130952951; −1,130951793]. Staubgewichte werden dabei nicht festgelegt. Die sieben separaten Dichteüberdeckungen sind pro Anbindung mit Ausgangsbereich, Endhülle und Blattzahlen protokolliert.

## Überdeckung und Kontrollen

Die Randhülle wird aus 256 geschlossenen Driftintervallen und drei Quellen berechnet. Die Driftabweichung ist höchstens 10⁻⁶, die Quellen sind −10⁻⁶, 0 und +10⁻⁶. Alle drei Nachimpulse erfüllen |vₐ| ≤ 1,12 × 10⁻¹² bei κ = 10⁻¹¹. Für die Gewichte der beiden Geräte 16 und 18 werden die Intervalle [0,10⁻⁸] und [10⁻⁸,1] gekreuzt. Die vier Kombinationen überdecken auch beliebig kleine positive Gewichte. Die stationären Referenzlösungen ausserhalb des Fensters werden separat mit allen 25 Gleichungen und den strikten Ordnungsrelationen erneut zertifiziert.

Alle 160 Bäume der neuen Rechnung schlossen ohne offene Blattbox. Sie umfassen 464 082 besuchte Boxen und 232 121 geschlossene Blätter. Der unveränderte Intervallkern aus dem Vorgängerarchiv prüft jede Verwerfung mit nach aussen gerundeten Ganzzahlschranken. Gleitkommawerte wählen lediglich Linearkombinationen oder Teilungen aus. 5 280 Vergleiche prüfen Residuen und Ableitungen anhand von exakten Wirkungsdifferenzen. In den neun gekoppelten Fällen prüfen 693 Einzelvergleiche die Auswirkung der Verschiebung je einer alten Staubuhr auf jede der elf Bedingungen. Das Ausgangsregister wird über Sektor, ID und die vier Anbindungsmasken mit dem ursprünglichen Register von 406 142 Projektionen abgeglichen.

## Offene Vorgänger und physische Messung

Die verbliebenen 21 Fälle liegen auf 16 verschiedenen etikettierten Anbindungen. Die fünf IDs 178526, 178542, 178609, 178625 und 178660 sind jeweils bei leerem und positivem Vorgänger offen. Bei ihrer Untersuchung lässt sich die Ordnung festhalten und allein die Gewichtsvorgabe wechseln. Bei Gewicht null bleibt die Uhrgleichung von 21 erhalten. Bei positivem Gewicht kommt die Dichtegleichung von 21 hinzu. Die Positivität ist strikt. Der physische Arealradius ist offen. Alle 60 physischen P3-Prüfpunkte stehen auf NOT_RUN.

## Offline nachrechnen

Unter Linux mit Python ab 3.11 und einem C++17-fähigen g++ im entpackten Verzeichnis ausführen.

```sh
sha256sum -c SHA256SUMS
python3 -B pruefen.py
```

Das Standardkommando baut den Rechenkern aus dem festgelegten Archiv neu, rekonstruiert die Randdaten, durchläuft alle 160 Bäume und vergleicht Entscheidungen und Restregister. Die Option `--jobs 4` führt bis zu vier Bäume gleichzeitig aus. Unterschiedliche gültige Pivotentscheidungen können die Baumgrössen ändern. Ein Ausschluss erfordert stets null offene Blätter.

`Ergebnisse.json` enthält Eingangs- und Ausgangszahlen, Kopplungen, Staubuhrhüllen, Kontrolldaten und Suchbaumstatistiken. `Offene_Faelle.tsv` enthält die 21 verbliebenen Zeilen. Die letzte Spalte stammt aus dem älteren Zusatztest mit begrenzter Trägheitslast. `basis/Vorstudie.zip` enthält die Eingangsregister und Abhängigkeiten. Die drei Prüfpläne kennzeichnen die ursprüngliche Gruppe und die beiden anschliessend gewählten Erweiterungen.
