# CST-DUST · Erweiterungsstabilität bei erhaltenem Elterngewicht

Bericht v0.2 zum Übergang von elf auf zwölf Ereignisse. Der Versuch setzt die in PR #295 publizierte Anfangspräparation mit zwei Elternhistorien fort. Als Erfolg gilt eines der drei akzeptierten Ergebnisse des q₇-Detektors pro präpariertem Versuch. Der vierte Ausgang erfasst jeden Fehlschlag. Das Dichtezentrum des Eingangspakets wechselt von 1/8 auf 1/4. Die Änderung der Erfolgswahrscheinlichkeit ist im ganzen hier auswertbaren Bereich negativ. Wie stark sie ausfällt und ob die vier Ausgänge die Toleranzen einhalten, hängt von der Erweiterung ab.

## Vergleich bei identischer neuer Historie

Die inneren Ereignisse 4, 5, 6 bilden entweder eine Kette oder eine Ordnung mit genau einer Kante. Der ursprüngliche Träger enthält beide mit Amplitudengewicht 1/2. In diesem Vergleich kommt genau eine Tochter der Kette mit einem zu allen drei alten inneren Ereignissen unvergleichbaren Ereignis hinzu. Beide Varianten geben ihr Gewicht 1/3.

| Gewichte in der Reihenfolge alte Kette, alte Ein-Kanten-Ordnung, Tochter | Änderung von P(Erfolg) in 10⁻⁶ | Relative Änderung des Dichtekontrasts über vier Ausgänge | Niveauabstand bei 1/8 und 1/4 |
|---|---:|---:|---|
| 1/2, 1/2, 0 | −6,68047 | 0 % | 0 %, 0 % |
| 1/3, 1/3, 1/3 (PR #295) | −3,36693 | 49,60 % | 43,36 %, 43,25 % |
| 1/6, 1/2, 1/3 (gewichtserhaltend) | −5,60283 | 16,13 % | 14,46 %, 14,45 % |

Beim dritten Versuch erfüllen Vorzeichen und Dichtekontrast ihre Kriterien. Die beiden Niveaus überschreiten die Toleranz. Beim vollständigen Ersatz **nur der Kette** (0, 1/2, 1/2) sind alle Kriterien wieder erfüllt. Auf diesem Einzelpfad liegt die erste Toleranzgrenze bei einem **gesamten** Tochtergewicht von rund 0,11187. Die Einhaltung entlang des Pfads verläuft somit nicht monoton.

## Welche Töchter zählen?

Die vier vergangenen und vier künftigen Kragenereignisse bleiben benannt und geordnet. Das neue Ereignis 11 liegt über allen vergangenen und unter allen künftigen. Beim Löschen von 11 muss exakt dieselbe alte induzierte Ordnung entstehen. Je altem inneren Ereignis sind drei Relationen zu 11 möglich. Im Feld `relations_to_new` bedeutet −1 „alt vor neu“, 0 „unvergleichbar“, +1 „neu vor alt“. Transitivität wird vor der Auswertung geprüft. Ein zweiter Zählweg durchsucht alle 4096 Teilmengen der zwölf gerichteten Relationen auf vier beschrifteten Punkten. Er ergibt 219 strikte Ordnungen und dieselben Löschfasern.

| Elternhistorie | Markierte Einfügungen | Tochtertypen ohne Markierung | Zulässige Einfügungen | Zulässige Typen und Häufigkeiten |
|---|---:|---:|---:|---|
| Kette | 10 | 7 | 7 | 11 × 1, 15 × 1, 53 × 1, 63 × 4 |
| Eine Kante | 12 | 8 | 7 | 11 × 3, 14 × 2, 15 × 1, 53 × 1 |

Eine Typnummer ist die kleinste Bitmaske der gerichteten Vorwärtsrelationen über alle topologischen Beschriftungen der vier inneren Ereignisse. Die Bitreihenfolge ist die lexikografische Paarfolge auf (4,5,6,11), beginnend mit Bit 0. Über beide Eltern gibt es zwölf verschiedene Töchter, davon fünf mit zulässigem Skalarzweig. Bei 31, 55 und 62 fehlt eine Volumennormierung für eine freie innere Richtung. Für 1, 3 und 10 kommt ein singuläres reduziertes gemischtes System hinzu. Typ 12 ist auch ohne freie innere Richtung im gemischten System singulär. Exakte Ränge, Nullvektoren und alle markierten Einfügungen stehen in `grids.json`.

Eine strikt positive Vorschrift über alle 22 Einfügungen liefert unter der übernommenen Skalarpaarung keine gemeinsame Auslese. Die folgenden Aussagen sind ausdrücklich auf die je sieben zulässigen Einfügungen konditioniert. Die Einfügungsmarkierung dient der Zuordnung zum Elternzweig. Sie wird am Detektor nicht ausgelesen.

## Zwei bedingte Gewichtungen

Jeder Elternzweig behält insgesamt 1/2. Ein gemeinsamer Anteil λ seines Gewichts wird auf seine zulässigen Töchter übertragen. Damit ist λ zugleich das gesamte neue Gewicht. Die Zahlen sind reelle, nichtnegative **Amplitudenkoeffizienten** mit Summe eins. Erreichen zwei Wege dieselbe unmarkierte Tochter, werden ihre Koeffizienten vor der Messung addiert. Alle Zweige interferieren. Gleiche Elterngewichte sind eine kontrollierte Modellannahme.

| Verteilung innerhalb jedes Elternzweigs | Erste Toleranzgrenze für λ | ΔP(Erfolg) bei λ = 1, in 10⁻⁶ | Kontraständerung bei λ = 1 |
|---|---:|---:|---:|
| Jede markierte Einfügung gleich | 0,051740 | −0,80689 | 87,92 % |
| Jeder unterschiedliche Tochtertyp gleich | 0,051984 | −1,07733 | 83,87 % |

Für jede Dichte ist der Niveauabstand die halbe L¹-Distanz der Vierer-Verteilungen geteilt durch die ursprüngliche Erfolgswahrscheinlichkeit bei derselben Dichte. Zulässig sind höchstens 10 %. Der Dichtekontrast ist die vorzeichenbehaftete Differenz beider Vierer-Verteilungen. Sein Abstand vom alten Kontrast, relativ zu dessen halber L¹-Norm, darf 25 % nicht übersteigen. Das Vorzeichen von ΔP(Erfolg) muss erhalten bleiben. Diese Regeln betreffen die ursprünglichen kohärenten Uhrfenster. Die vier Kontrollpräparationen bleiben im Ergebnisdatensatz separat verfügbar.

## Was für alle Gewichte gilt

1. **Jede zulässige Aufteilung bis einschliesslich λ = 0,050.** Der mögliche Endpunkt v ist eine konvexe Mischung der 16 Paare aus je einer Tochter pro Elternzweig. Für w = (1−λ)b + λv und jede Effektmatrix M zerfällt wᵀMw in den Ausgangs-, Kreuz- und Tochterterm. Die Dreiecksungleichung liefert für jede auf ihre Toleranz normierte Änderung die Schranke 2λ(1−λ)A + λ²B. A maximiert den Abstand der 16 Kreuzterme zum Ausgangswert und B jenen aller Tochter-Paarterme. Über das ganze angegebene Intervall bleiben beide Niveaus unter 0,986 ihrer Toleranz, der Kontrast unter 0,394 seiner Toleranz. Die konservative erste Grenze der Schranke liegt bei 0,0507558. Der Befund gilt für beliebige nichtnegative Aufteilung pro Elternzweig bei gleichem ersetztem Anteil.
2. **Vorzeichen für den ganzen berechenbaren Träger.** Für die kohärente Präparation ergibt sich ΔP(Erfolg) = wᵀDw auf den zwei Eltern und fünf zulässigen Tochtertypen. In der symmetrischen Matrix D gilt in jeder Zeile Dᵢᵢ + Σⱼ≠ᵢ |Dᵢⱼ| < 0. Die grösste Zeilenschranke beträgt −1,82968 × 10⁻⁶. D ist negativ definit. Das Vorzeichen bleibt für jeden nichtverschwindenden reellen Gewichtsvektor erhalten, insbesondere für jede hier zugelassene Mischung.
3. **Vollständiger Ersatz beider Eltern.** Für jede Mischung allein aus den fünf zulässigen Tochtertypen verfehlt mindestens ein Niveau- oder Kontrastkriterium seine Toleranz um den Faktor ≥ 1,6688 (Verhältnis Ist/Toleranz). Die Aussage gilt sogar ohne Zwang zur Erhaltung beider Elterngewichte. Dazu wird der ganze Simplex der fünf Gewichte durch zweimaliges Halbieren einer Kante in drei Teilsimplexe überdeckt. Auf jedem beweist eine vorzeichenbehaftete Linearkombination der vier Ausgänge die Überschreitung. Für Eckpunkte uᵢ eines Teilsimplex sind sämtliche Koeffizienten uᵢᵀMuⱼ dieser normierten Kombination grösser als eins. Dasselbe gilt deshalb für jede konvexe Mischung. In zwei Teilen belegt dies das Niveau bei 1/8 (Faktor ≥ 2,2887), im dritten der Dichtekontrast (Faktor ≥ 1,6688).

Die Punkte 2 und 3 sind ergänzende Auswertungen nach der vorab festgelegten Kampagne. Die Zertifikate rechnen mit exakten Brüchen der übergebenen binären Matrixeinträge. Beide Produktionsgitter ergeben dieselbe Einteilung und dieselben Schlüsse. Die Uhrintegrale selbst besitzen hier ein empirisches Gitterfehlerbudget. Eine Intervallschranke für die ursprünglichen Integrale ist weiterhin offen.

## Reproduktion

Getestet mit Python 3.12 und den Versionen aus `reference/requirements.txt`. Mit bereits vorhandenen Abhängigkeiten genügt im entpackten Verzeichnis der folgende Aufruf.

```sh
python -B verify.py
```

Bei Bedarf lassen sich die drei Python-Abhängigkeiten mit `python -m pip install -r reference/requirements.txt` in einer lokalen Umgebung installieren. Der Prüflauf kontrolliert zuerst die SHA-256-Dateihashes und den lokal vor der Rechnung fixierten Vertrag. Danach wiederholt er die Zählung, die Ränge, die Uhrintegrale, die Skalar- und Auslesekontrollen sowie sämtliche Gewichtstests in einem temporären Verzeichnis. Der lokale Rechenaufwand betrug rund eine halbe Minute pro Durchlauf. Die Berechnung benötigt keinen externen Dienst.

`compute_grids.py` und `analysis.py` sind die beiden Einstiegspunkte zur getrennten Ausführung. `reference/` enthält unveränderte benötigte Bestandteile aus PR #295. `reference/ORIGIN.json` dokumentiert Quellpfade und verifizierte Git-Blob-Kennungen. Der vollständige Vorgängerversuch ist in der verlinkten Quelle verfügbar. `fibre_contract.json` ist Version 0.1 des Versuchsplans zu Bericht v0.2. Die beiden Kontrollrechnungen reproduzieren die Vierer-Verteilungen des ursprünglichen Trägers und des publizierten Drei-Historien-Falls auf besser als 2 × 10⁻¹⁵. Der maximale beobachtete Unterschied eines Effektmatrixeintrags zwischen den letzten Gittern beträgt 2,56 × 10⁻¹⁴ über alle fünf Präparationen. Gegenprüfungen umfassen eine direkte Tensorquadratur, Umbenennung der inneren Ereignisse, die Dephasierungsidentität und eine unabhängige gedämpfte Skalarrechnung bei ε = 10⁻²⁸.

Der Versuch betrifft einen bestimmten endlichen Wachstumsschritt, eine benannte Präparation, einen festen Rand und einen festen Detektor. Eine physikalische Auswahl von Historiengewichten, weitere Grössenstufen, ein CST-Grenzwert und die Dynamik des Staubkollapses bleiben offen.

[Ausgangsversuch auf GitHub, festgeschriebener Stand](https://github.com/thomasmgfeller/x6-spectral-astrolabium/tree/90afbd33cbbe6fd3c6482090c65aa326dbaa4d8a/research/rax_cqg/dust_collapse/extension_stability_v0_1)
