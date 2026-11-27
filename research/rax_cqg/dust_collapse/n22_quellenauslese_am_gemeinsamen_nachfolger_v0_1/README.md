# Kann die Enduhr einer gemeinsamen Zukunft die Quelle unterscheiden?

**Ja, für drei stationäre Präparationsfamilien im endlichen N22-Modell. Die drei Familien unterscheiden sich zugleich im vollständigen Vorlauf des Senders.** In jedem der drei lokalen Zweige ist die Trennung an Uhr 21 für jede Drift zwischen −10⁻⁶ und +10⁻⁶ eingeschlossen. Alle drei Nachimpulse sind null. Die Aussage gilt für die Anbindung 216141 / P21 = 229383 / F21 = 0 mit positivem terminalem Gewicht. Die Grundlage mit den Fensterschranken ist in [PR 407](https://github.com/thomasmgfeller/x6-spectral-astrolabium/pull/407) veröffentlicht.

## Was der Leser erhält

Der Leser verwendet die lokale Uhr Y₂₁ in der festen Modelleichung und einen vorher festgelegten Referenzcode. Der Rasterschritt ist Δ = 0,0000002. Die Ablesung darf um Δ/4 gestört sein, der eingegebene Referenzcode unabhängig um eine ganze Stufe vom zentralen Nullcode B₀ = 4 073 422 abweichen. Bei einer halben Rasterstufe werden beide Rundungen berücksichtigt. Weder die Drift noch das Quelllabel gehen in den Leser ein.

| Quelle am Sender 16 | Mögliche Empfangscodes einschliesslich Ablesefehler | Differenz zum tatsächlich benutzten Referenzcode |
|---|---|---|
| +10⁻⁶ | 4 073 416 bis 4 073 418 | −7 bis −3 |
| 0 | 4 073 421 bis 4 073 423 | −2 bis +2 |
| −10⁻⁶ | 4 073 426 bis 4 073 428 | +3 bis +7 |

Bis einschliesslich −3 liest das Gerät die positive Quelle, ab +3 die negative und dazwischen die Nullquelle. Die Tabelle gibt sichere Hüllen an. Die kleinste nachgewiesene Lücke zwischen benachbarten analogen Empfangsbereichen ist grösser als 5,49·10⁻⁷. Die Regel wurde anhand der schon bekannten numerischen Näherungen gewählt. Eine physische Eichung steht aus.

## Woran die Deutung als Sendeversuch scheitert

Im strikten Vorlauf von Sender 16 liegen die Ereignisse 0, 1, 2 und 15. Die drei materiellen Ereignisse haben in allen zertifizierten Familien dieselben Uhren −5, −4 und −3 und jeweils das Gewicht 1/8. Ereignis 15 hat Gewicht null. Seine freie Uhr variiert mit der Quelle. Zwischen den zertifizierten Uhr-15-Hüllen benachbarter Quellen liegt über den gesamten Driftbereich eine Lücke von mehr als 7,04·10⁻⁸. Auch die Wahl verschiedener Driften liefert zwischen den drei eingeschlossenen Zweigen kein Paar mit identischem vollständigem Sendervorlauf. Ob die leere Uhr 15 physisch ausgelesen werden kann, ist offen.

Damit belegt die Rechnung eine Unterscheidbarkeit vorbereiteter stationärer Lösungen an einem gemeinsamen kausalen Nachfolger. Für ein Signal mit frei gewählter Quelle wäre ein Vergleich mit identischen relevanten Vorlaufdaten und eine physische Auslese erforderlich. Das Modell lässt weitere stationäre Zweige offen. Der Arealradius bleibt unbestimmt, alle 60 physischen P3-Prüfpunkte stehen auf `NOT_RUN`.

## Was zertifiziert wurde

Für jede Quelle wird um dieselbe in der Drift affine Näherung X₀ + sδ eine Umgebung der 14 freien Uhren und elf positiven Gewichte betrachtet. X₀ und s sind je Quelle fest. Die Rechnung überdeckt das geschlossene Driftintervall lückenlos mit acht Teilintervallen. Bei festen N19-Randdaten prüft sie Stationarität aller 25 freien N22-Gleichungen, alle 152 strikten Kausalrelationen, die Gerätebereiche und die Positivitätsbedingungen. Die N19-Randdaten werden ihrerseits für jede Drift und Quelle gemeinsam präpariert.

Mit dem stationären Residuum F, einer festen Vorkonditionierung C und dem Fehler e = X − X₀ − sδ ist die Fixpunktabbildung e ↦ e − C F(X₀ + sδ + e). Für jede Koordinate ist die normierte Bildschranke aus Residuum und Ableitungsfehler kleiner als eins. Die Ableitung der Abbildung hat Norm kleiner als eins. Das gibt für jede einzelne Präparation Existenz und Eindeutigkeit in der untersuchten Umgebung. Die Intervalle verwenden dieselbe affine Näherung und dieselben Fehlerradien, also gilt an gemeinsamen Endpunkten derselbe lokale Eindeutigkeitsnachweis. Die Summe der beiden Uhren 19 und 20 geht mit den Schichtkoeffizienten der rekonstruierten Ordnung in die Enduhrgleichung ein.

Die Randableitungen werden durch die algebraische Präparation nachgeführt. Für das lineare System A z = b wird insbesondere A z′ = b′ − A′ z eingeschlossen. Bei verschwindenden Nachimpulsen hängt die implizite Gerätekorrektur allein von den driftfesten Uhren 15 und 16 der ursprünglichen N19-Präparation, der Quelle und den Gerätekonstanten ab. Diese Aussage betrifft die N19-Randkonstruktion. Die später gemeinsam gelöste freie N22-Uhr 15 ist davon zu unterscheiden.

Ein zweiter, rationaler Punktprüfer aus der früheren Veröffentlichung bestätigt alle 15 Kombinationen der drei Quellen mit den fünf Driften −10⁻⁶, −½·10⁻⁶, 0, +½·10⁻⁶ und +10⁻⁶. Für die sechs neuen Zwischenpunkte werden die affinen Vorhersagen direkt verwendet. Der Prüfer kontrolliert für alle 25 Koordinaten, dass seine punktweise Lösung in derselben zertifizierten Umgebung liegt. Hinzu kommen 1 875 Prüfungen der N22-Jacobimatrix durch exakte zentrale Differenzen und 192 Konsistenzvergleiche der N19-Randableitungen mit Sekanten aus der ursprünglichen Punktpräparation.

## Offline wiederholen

Nach dem Entpacken im Paketverzeichnis ausführen. Benötigt wird Python ab 3.10 mit der Standardbibliothek.

```sh
sha256sum -c SHA256SUMS
python3 -B pruefen.py
```

`Driftregister.tsv` enthält alle 24 Überdeckungsintervalle mit rationalen Grenzen für beide Uhren. `Ergebnisse.json` enthält auch die Punktkontrollen, die exakten Hüllenabstände und die Kontraktionsschranken. `Startwerte.json` stellt die früheren Näherungen bereit. `Pruefplan.md` fixiert vor der neuen Zertifizierung die Leseregel, `Vorlaufkontrolle.md` kennzeichnet die ergänzende Gegenprobe nach Sichtung der Näherungen. Die Eingaben von PR 407 sind mit ihrem veröffentlichten SHA-256-Wert im Paket enthalten.
