# CST-DUST · Erweiterungsstabilität der N11-Anfangspräparation v0.1

18. November 2026. **Für die durchgerechnete Erweiterung auf drei Historien bleibt das Vorzeichen der kohärenten Dichteantwort erhalten. Die Grösse verfehlt die vorab festgelegte Toleranz.** Die Zwölf-Ereignis-Historie enthält alle elf ursprünglichen Ereignisse und ein neues inneres Ereignis. Die getestete Gewichtung gehört zum Versuch. Eine physikalische Grössenskalierung oder ein Bounce folgt daraus nicht.

## Prüfvertrag

Ausgangsstand ist [PR 294, Commit 82758d4](https://github.com/thomasmgfeller/x6-spectral-astrolabium/tree/82758d4983ada37d71b6ac92df629a7f495df6a6/research/rax_cqg/dust_collapse/initial_preparation_v0_1). Die drei Dateien in `reference/` wurden mit den entsprechenden Git-Blobs abgeglichen. Die Gaussausgänge stammen aus `physical_boundary_readout_v0_1/checks/canonical_scalar/gaussian_outputs.json`, die übrigen beiden Dateien aus `initial_preparation_v0_1`.

`contract.json` wurde vor der wissenschaftlichen Auswertung fixiert (SHA-256 9df8c47f1f7d26be411626867e6ed1bdeb2dba9f4f5219ffb3528366b0e6f013). `supplement.json` wurde nach der exakten Rangprüfung und vor der Berechnung neuer Ausgangswahrscheinlichkeiten ergänzt. Die Aufspaltung in alte und neue Beiträge sowie die direkte Abel-Gegenrechnung sind nachträgliche Diagnosen. Alles ist intern festgelegt, ohne externe Präregistrierung.

Der Vergangenheitskragen 0–3, der Zukunftskragen 7–10 und ihre gegenseitigen Relationen bleiben fest. Die Anfangsuhr T₃, ihre beiden Fenster, die kollektiven Dichtezentren, deren Halbbreite, Zukunftsdichte, Skalargrundzustand, Quotient, q₇-Detektor und Fehlschlageffekt folgen PR 294. Für jeden neuen inneren Knoten gelten dasselbe normierte Uhrmass dT/3 auf [−3/2,3/2] und das Dichtemass (δ₀+dr)/2. Die Summe verwendet gleiche positive **Amplitudengewichte** pro unbeschriftetem Ordnungstyp. Bei Erweiterung wird auf Summe eins normiert, das relative Gewicht der beiden Ausgangshistorien bleibt eins zu eins. Die Wahl der Gewichtung über verschiedene Ereigniszahlen ist eine zusätzliche Annahme.

Die fünf N11-Typen sind genau die unbeschrifteten partiellen Ordnungen auf dem Inneren {4,5,6}, wenn Vergangenheit und Zukunft vollständig daran anschliessen. Kette und Ein-Kanten-Ordnung bilden die Ausgangsfamilie F2. F4 fügt eine Verzweigung und ihre Zeitumkehr hinzu, F5 die Antikette. F7 fügt darüber hinaus zwei N12-Erweiterungen der Ausgangstypen hinzu. Ihr neues inneres Ereignis 11 ist mit jedem alten inneren Ereignis unvergleichbar und steht zwischen beiden Kragen. Löschen von 11 ergibt jeweils die ursprüngliche Ordnung. Alle einzelnen Zusätze zu F2 und der gemeinsame N12-Zusatz sind ebenfalls vorab festgelegt. Diese verschachtelten Träger und Nebenvergleiche umfassen bewusst nur zwei Zwölf-Ereignis-Typen.

## Beobachtungsgrösse und Entscheidung

p(r) enthält die drei gemeinsamen Zeigerwahrscheinlichkeiten und den Fehlschlag pro präpariertem Versuch. Hauptversuch ist das kohärente Anfangsuhrpaket mit gleicher Phase. Δp=p(1/4)−p(1/8). Die Kriterien sind

- TV(p_neu(r),p_F2(r)) ≤ 0,10 P_F2(Erfolg|r) bei beiden Dichten, mit TV gleich halber L¹-Distanz,
- ½‖Δp_neu−Δp_F2‖₁ ≤ 0,25 × ½‖Δp_F2‖₁,
- gleiches Vorzeichen des Erfolgskontrasts bei beiden Familien.

Die vergleichsweise seltene Akzeptanz begründet die Skalierung des ersten Kriteriums. Die 10- und 25-Prozent-Schwellen sind deklarierte Vergleichswerte. Die Zahlen erlauben eine Auswertung mit eigenen Toleranzen. Die numerische Toleranz 5×10⁻¹² dient ausschliesslich der Reproduktion. Vorgeschriebene Gruppen mit nicht definierten Mitgliedern erhalten keine Wahrscheinlichkeitszuweisung.

## Skalaralgebra und Messung

`geometry.py` rekonstruiert die Intervallgewichte (1,−9,16,−8), die Wirkung F und die skalare Hesse-Matrix jeder Ordnung aus den vergleichbaren Paaren. Im skalierten Skalarteil gilt H=−L/2. Die beiden alten Randgeneratoren, die Koordinatensektionen und die Chirpphasen bleiben erhalten. Nach Wechsel in innere und die beiden Rand-Eichkoordinaten werden der reguläre Block exakt eliminiert, verbleibende Fourier-Deltas als lineare Randbeziehungen gelöst und die reduzierte gemischte Legendre-Matrix auf vollen Rang getestet. Eine reine innere Nullrichtung hat unendliches ungedämpftes Volumen. Die Ausgangspublikation regelt nur die dort vorhandenen Rand-Eichvolumina.

Die Zusatzkonvention teilt je orthonormaler innerer Nullrichtung bei Dämpfung exp(−εz²/2) durch √(2π/ε). Alle endlichen Normierungen sind positiv. Bei vollem gemischtem Rang sind beide symplektischen Identitäten der reduzierten 6×6-Karte exakt getestet. Die normierte Ausgabe auf dem zentrierten Gausszustand hat Präzision βΩ. Signatur der reellen Integration und fortgesetzte Wurzeln der komplexen Gaussintegrale bestimmen die Phase. Die Übereinstimmung der beiden alten komplexen Ausgangsfunktionen mit der gespeicherten Referenz wird in 55-stelliger Rechnung geprüft.

Für Zustände ψᵢ=Nᵢ exp(−yᵀPᵢy/2) gilt T=Pᵢ*+Pⱼ, z=Nᵢ* Nⱼ(2π)^(3/2)/√det(T) mit fortgesetzter Wurzel. Das mittlere Zeigerintervall hat das Matrixelement z erf[1/√(2u)] mit u=1+(T⁻¹)₀₀. Parität teilt die verbleibende Amplitude gleich auf die beiden äusseren Intervalle. Für jede Präparation werden die positiven Detektormatrizen mit den komplexen präparierten Historienamplituden kontrahiert. Der Fehlzweig ergänzt zur Einheit. Die kohärente Historienmischung ist eine Kontraktion, weil die normierten Zweige und die positiven Gewichte auf Summe eins begrenzt sind.

## Uhren, Validierung und Grenzen

`clocks.py` integriert die inneren Dichten analytisch und die inneren Uhren mit normierter Gauss-Legendre-Quadratur. Die Pastphase exp(−irB(T₃)/2) ist für jedes feste T₃ und alle Historien gemeinsam. Über das äussere Dichtefenster liefert sie den sinc-Faktor. Das zum alten Inneren unvergleichbare N12-Ereignis hat keine quadratische Uhrkopplung zu dessen drei Knoten. Daher faktorisiert seine Integration als eigene eindimensionale Quadratur. Die übrigen Koeffizienten, einschliesslich möglicher Änderungen an Intervallen zwischen den Kragen, werden aus der vollständigen neuen Ordnung bestimmt. Eine direkte vierdimensionale Rechnung am selben 12-Knoten-Gitter prüft diese Faktorisierung. Die regulären Produktionsgitter sind (64,8) und (96,12) Knoten je innerer Uhr bzw. je äusserem Uhrfenster.

`abel_check.py` integriert Eingangs-, Innen- und Rand-Eichvariablen gemeinsam mit positiver Dämpfung und prüft Phasen und komplexe Ausgangsbreiten der fünf ausgewerteten Zweige gegen die exakte Rangreduktion. `results.json` enthält jede Entscheidung und sämtliche vier unbedingten Ausgänge, einen Gewichtspfad und die Bilanz von altem, neuem und Interferenzbeitrag. `abel_results.json` enthält alle drei Dämpfungsstufen. Die Gitterdifferenzen sind empirisch. Ein rigoroses Float64-Rundungszertifikat sowie eine physikalisch ausgewählte Gewichtung oder globale CST-Evolution bleiben offen.

## Reproduktion

Im entpackten Ordner, mit Python 3.12 und den in `requirements.txt` angegebenen bereits installierten Bibliotheken:

```bash
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 python -B verify.py
```

Der Prüfer liest ausschliesslich lokale Dateien. Er berechnet die Resultate neu und vergleicht sie mit den archivierten Ergebnissen. Einzelauswertungen können mit `python -B run.py --output neue_ergebnisse.json` oder `python -B abel_check.py --output neue_abelwerte.json` gespeichert werden. Die Originalreferenzen und Projektlizenz sind im Paket enthalten.
