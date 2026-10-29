# Ergebnis: engere Integrale, strukturelle Adaptergrenze

**METHOD_HOLD.** Derselbe Entwicklungsbestand aus acht bekannten Wolken
wurde bei unveränderten Quellen, Detektoren und Operatorparametern geprüft.
Es wurden keine neuen Sprinklings gezogen. Die ursprünglichen 80 H1-Signale
bleiben getrennt von 16 zusätzlichen kompakten H3-Signalen ausgewiesen.

## Detektorintegration

| Räumliches Gitter | Zellen pro Fenster | Bestandene ursprüngliche H1-Budgets | Normierte Wellenradien | Normierte kompakte H1-Radien bei nichtleerer History |
|---|---:|---:|---|---|
| 4^3 | 64 | 6/80 | 0,3899–2,9373 | 0,001091–0,009323 |
| 8^3 | 512 | 8/80 | 0,1878–1,4901 | 0,0004506–0,005100 |
| 16^3 | 4096 | 11/80 | 0,09000–0,7258 | 0,0002067–0,002545 |

Das Ziel bleibt ein Komponentenradius von höchstens 0,001 der Feldskala.
Gegenüber v0.9 sind alle 74 nichttrivialen ursprünglichen Radien auf der
feinsten Stufe um Faktoren **5,005–6,254**, Median **5,476**, enger. Diese
Entwicklungsstufe verwendet zugleich ein größeres räumliches Zellenbudget;
der Faktor ist kein isolierter Effizienznachweis bei gleicher Rechenzeit.
Schon das neue 64-Zellen-Gitter verengt diese Intervalle um Faktoren
1,082–1,627, erfordert aber ebenfalls andere Arbeit je Zelle.

Von den elf bestandenen ursprünglichen Budgets sind weiterhin sechs
exakte Nullsignale aus drei leeren kompakten Quellhistorien. **Fünf weitere,
nichtverschwindende kompakte H1-Signale** erreichen jetzt das Integrationsziel.
Alle 64 Wellenantworten verfehlen es weiterhin. Die Radien beschreiben
Rechenunsicherheit; sie sind keine RMS-Schätzung physikalischen Rauschens.

## Anfangsdatenadapter

Der zusätzliche H3-Vergleich besteht nur bei den sechs identischen
Nullsignalen. Bei nichtleeren kompakten Historien liegen seine normierten
Integrationsradien auf dem feinsten Gitter zwischen 0,05038 und 0,5567.
Insgesamt bestehen somit **17/96** Integrationsbudgets, davon zwölf
Nullintegrale und fünf nichtverschwindende H1-Signale.

Für H1 und H3 existieren jetzt explizite Sobolev-/Energie-Obergrenzen der
Abweichung von der exakten Kontinuumshistory. Diese werden über die
diskrete adjungierte Transferabbildung bis zum Detektor weitergeleitet.
**0/32** der getrennten Anfangsdatenbudgets werden durch diese Schranken
qualifiziert. Auf der feinsten Stufe liegen die normierten H1-Oberwerte
zwischen 3,75e6 und 6,56e6, die H3-Oberwerte zwischen 3,80e11 und 1,42e12.
Diese absichtlich konservativen Oberwerte sind **keine gemessenen Fehler
und keine Fehleruntergrenzen**. Insbesondere beweisen sie keine physikalische
Verstärkung dieser Größe.

Davon unabhängig gilt ein strukturelles Ergebnis: Jede endliche lokale
Taylor-History aus den Jets des unveränderten kompakten Bumps bleibt
außerhalb seiner Quellstütze null. Höhere Ordnung kann eine auf der Wolke
vollständig verfehlte Quellstütze nicht wiederherstellen.

Die [separate analytische Einordnung](ADAPTER_OBSTRUCTION.md) ergibt im
idealen Poisson-Modell für nu512 eine Leerwahrscheinlichkeit
exp(-21/16), ungefähr **26,9 Prozent**. Diese Zahl folgt aus dem exakten
Volumen der Quellhistoryregion, nicht aus einer Schätzung anhand der acht
bekannten Wolken. Sie ist keine universelle Quantenrauschkonstante.

## Getrennte numerische Kontrolle

Im 128-Bit-Lauf bleiben die normierten Weiterleitungseffekte der
Anfangsdatenrundung unter 8,60e-15 und der Float-Knotenlösung unter 9,37e-16.
Der größte normierte Arb-Knotenradius liegt unter 2,97e-24. Diese Beiträge
erklären die breiten Integrationsintervalle nicht.

Die vollständigen Präzisions-, CPU- und Reproduktionsnachweise stehen in
[CHECKS.json](results/CHECKS.json): **52.284 Einschließungsvergleiche bestehen**;
alle drei Läufe liefern dieselben Entscheidungen und identische
Geometrie-Hashes. Jeder der beiden Präzisionsläufe benötigte lokal etwa
7,5–7,6 Minuten und weniger als 87 MiB maximalen Hauptspeicher.
Quellen und Verfahren wurden vor der
neuen Integration [öffentlich fixiert](REGISTRATION.json). Neun analytische
Vorprüfungen decken signierte Mehrereignis-Integrale, exaktes Kugelvolumen,
wechselnde bzw. gebundene Eintrittsreihenfolgen, Nullrand/ULP-Fälle,
Ableitungen, Taylor-Restterme und den vollständigen synthetischen Transfer ab.

Eine [offengelegte Prüfkorrektur](VERIFICATION_AMENDMENT.json) entfernt
eine falsche Gleichheitsanforderung des ursprünglichen Verifiers:
`abs_upper`-basierte Fehleroberwerte dürfen bei verschiedener Präzision
unterschiedlich ausfallen. Ihre relativen Differenzen liegen hier unter
2,01e-9. Alle Feld- und Transferintervalle überlappen bereits ohne diese
Korrektur. Jede Obergrenze und Budgetentscheidung wird weiterhin im eigenen
Lauf geprüft. Der korrigierte Einstieg heißt `verify10a.py`; ursprünglicher
Prüfer, Rechenquellen, Budgets und Rohdaten bleiben unverändert erhalten.

## Anschlussentscheidung

1. Kein neuer großer Sprinkling-Lauf: Das Integrationsziel und die
   Anfangsdatenkontrolle sind weiterhin offen.
2. Keine reine Erhöhung der lokalen Taylor-Ordnung als Lösung für leere
   Quellhistorien. Eine ausdrücklich definierte nichtlokale Projektion
   oder andere diskrete Anfangswertformulierung braucht eigene Kontrollen.
3. Die Integration muss gemeinsame Abhängigkeiten und Auslöschungen der
   Feldbeiträge besser erhalten. Eine bloße Verlängerung der gleichmäßigen
   Gitterfolge erhält keine behauptete Erfolgs- oder Budgetgarantie.
4. Kompakte Kontinuumsdetektorreferenz, prädiktiver Kovarianzkern und
   unabhängiger Fluktuationstest bleiben offen. G1 HOLD; kein Dirac-Ausbau.

Belege: [Rohdaten 128 Bit](results/BENCHMARK_128.json.gz),
[192 Bit](results/BENCHMARK_192.json.gz), [CPU-Vergleich](results/BASELINE_128.json.gz),
[Entscheidung](results/DECISION_128.json), [deskriptive Auswertung](results/DESCRIPTIVE.json).
`report10.py`, dieser Text und die analytische Einordnung wurden nach dem
Quellen-Freeze ergänzt; sie verändern keine registrierte Eingabe oder Entscheidung.
