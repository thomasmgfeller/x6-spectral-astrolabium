# CST-DUST · Gemeinsamer Nachfolger und stationäres Uhrenfenster

Stand vom 27. November 2026. Betrachtet werden die drei N21-Referenzordnungen 216141, 216427 und 217269. Die materiell besetzte Messuhr 19 und die leere Messuhr 20 sind kausal unvergleichbar. Ereignis 21 liegt in ihrer gemeinsamen strikten Zukunft. Die 671 zulässigen Anbindungen werden jeweils mit verschwindendem und mit positivem Gewicht an 21 geprüft.

## Ergebnis

Die normierte Uhr ist xⱼ = (Yⱼ − Y₃)/(Y₇ − Y₃). Gesucht ist das Infimum h* von max(|x₁₉ − ½|, |x₂₀ − ½|) über alle zulässigen stationären Zustände dieser Familie. Beide Uhren müssen im selben geschlossenen Fenster [½ − h, ½ + h] liegen.

| Halbbreite h | Durchführung | Ausgeschlossene Fälle | Offene Fälle |
|---|---|---:|---:|
| 27/1024 | Letzten offenen Fall geschlossen, 1 341 Ausschlüsse aus PR 406 übernommen | 1 342 | 0 |
| 55/2048 | Alle Ordnungs- und Gewichtsfälle neu geprüft | 1 342 | 0 |

Daraus folgt **0,02685546875 ≤ h* ≤ 0,02687714**. Die untere Grenze ist exakt, die obere ist nach aussen gerundet. Die exakten rationalen Schranken liegen weniger als 0,00002167 auseinander. Ob ein Zustand das Infimum erreicht, ist offen.

Für die obere Schranke wurde eine zulässige stationäre Lösung in Referenz 216141 mit P21 = 229383, F21 = 0 und positivem Gewicht an 21 eingeschlossen. Ihre Präparation hat Drift −10⁻⁶, Quelle +10⁻⁶ und drei verschwindende Nachimpulse. Die rationale Krawczyk-Prüfung umfasst alle 25 freien Gleichungen. Der eingeschlossene Zustand erfüllt 152 strikte Kausalrelationen und die elf strikten Positivitätsbedingungen. Die normierte Uhr 19 bestimmt die obere Schranke. Der zentrale Kontrollzustand wird separat reproduziert.

## Wie der Ausschluss zustande kommt

Die alte Präparation verschiebt die Uhren 17 und 18 durch denselben Driftparameter. Die neue Auswertung hält diesen gemeinsamen Faktor in den Randgleichungen fest. Für jede Driftzelle und jede der drei Quellen werden alle drei Nachimpulsintervalle zugleich berücksichtigt. Die so eingeschlossenen Randuhren und Gewichte ergeben eine äussere Hülle. Ein Ausschluss auf dieser Hülle schliesst sämtliche von ihr überdeckten Präparationen aus.

Bei 27/1024 blieb zuvor nur der reguläre Gewichtsbereich der Anbindung 216141/229383/0/+ offen. Die 16 lückenlos anschliessenden Intervalle der Uhr 19 überdecken den gesamten noch offenen Bereich aus PR 406. Alle 16 schliessen mit der aus 16 Driftintervallen und drei Quellen gebildeten Hülle.

Bei 55/2048 schliessen im selben Gewichtsbereich zunächst 95 von 96 Uhrintervallen. Für das verbleibende Intervall genügen die Hülle aus 256 Driftintervallen und drei Quellen und eine Unterteilung in 32 Uhrintervalle. Acht der 1 342 Fälle schliessen bereits durch ihre Uhrenbedingungen. Für den Rest enthält die endgültige Überdeckung 5 462 Prüfbäume mit 33 149 geschlossenen und null offenen Blättern.

## Wiederholen

Das Paket enthält die Eingaben aus [PR 406](https://github.com/thomasmgfeller/x6-spectral-astrolabium/pull/406) mit festgelegtem SHA-256-Wert. Zum Wiederholen werden Python ab 3.10 und g++ mit C++17 und UBSan benötigt. Nach dem Entpacken im Paketverzeichnis ausführen.

```sh
sha256sum -c SHA256SUMS
python3 -B pruefen.py --jobs 4
```

Der zweite Befehl berechnet beide Fensterprüfungen und die stationären Kontrollen offline. Er vergleicht Fallentscheidungen, Randzellen und rationale Schranken mit den beiliegenden Daten. Die Zahl der parallelen Prozesse ist wählbar. Ein anderer gültiger Vorkonditionierer kann die Baumgrössen verändern.

- `Pruefplan.md` und `Pruefplan.sha256` halten die vor der Feldrechnung festgelegte Reihenfolge fest.
- `Fallregister_55_2048.tsv` enthält eine Zeile je Fall. Bit j von P21 bzw. F21 bezeichnet ein altes Ereignis j vor bzw. nach dem Nachfolger, für 0 ≤ j < 19.
- `Randzellen.json` enthält beide Präparationsgitter, ihre Hüllen und die Punktkontrollen gegen die frühere Rechnung.
- `Randzeuge.json` enthält die numerische Startnäherung. Die rationalen Einschliessungen und die vollständigen Baumstatistiken stehen in `Ergebnisse.json`.
- `basis/Gemeinsamer_Nachfolger.zip` enthält die frühere Studie mit ihrem eigenen Wiederholungsprogramm.

Ein physisch auslesbares Empfangssignal am Nachfolger, der Arealradius und die Fortsetzung des Staubballs bleiben offen. Alle 60 physischen P3-Prüfpunkte stehen auf `NOT_RUN`.
