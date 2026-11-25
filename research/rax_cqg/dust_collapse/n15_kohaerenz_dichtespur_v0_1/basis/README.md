# Uhr 4, Ereignis 12 und die Dichtespur am Endrand

CST-DUST · N15 · Ordnungstyp 2097151 · 25. November 2026

**Ergebnis.** Der gewöhnliche Übergang zum nächsten Ereignis liefert auf den geprüften Uhrpaketen zwei fast parallele Ausgangswellen. Werden dagegen zwei getrennte Uhrpakete schon bei der Präparation mit gleicher Phase besetzt, liegt die gemeinsame Endintensität der hohen Dichteklasse bei festem Dichteprofil um 1,3296 bis 1,3890 Milliardstel über der niedrigen. Das ursprüngliche mitlaufende Dichteprofil ergibt exakt gleiche Intensitäten. Die Aussage gilt für die hier gewählten Randzustände, die flache Hilfsnorm und die gemeinsame Endauslese. Der physische P3-Status beträgt 60 × NOT_RUN.

## Reproduktion

Paket vollständig entpacken und in seinem Verzeichnis mit Python 3.10 oder neuer ausführen:

```sh
python3 -B pruefen.py
```

Der Prüfer kontrolliert die SHA-256-Einträge und die mitgelieferten Git-Quellen, berechnet alle rationalen und nach aussen gerundeten Intervalle neu und vergleicht eine getrennt implementierte Gleitkommarechnung auf zwei Auflösungen. Er braucht weder Internet noch Zusatzpakete. Die Intervallresultate stehen in `ergebnisse.json`, die numerischen Resultate in `quadratur.json`. Der Plan und seine späteren Erweiterungen sind in `Pruefplan.md` dokumentiert. Die Prüfsummen erlauben den Vergleich mit dieser Ausgabe. Es gab keine externe Vorregistrierung.

## 1. Was von Ereignis 4 am Ereignis 12 ankommt

Die letzten vier Uhrwerte des Schnitts hinter 11 sind (Y4,Y5,Y6,Y11). Nach dem nächsten Ereignis lautet der Schnitt (Y5,Y6,Y11,Z), mit Z=Y12. Die gewöhnliche Verklebung integriert über den alten Uhrwert y=Y4. Der einzige noch offene Wirkungsterm mit y gehört zur Kante 4 → 12. Die Gewichte nach 12 von 4,5,6,11 sind −8,16,−9,1. Bei festen übrigen Variablen und mit offener Dichte w an 12 hat der lokale Kern daher die Form

```
K(z,w;y) = H(z,w) exp[i a w (z−y)²],       a = 8/38.
```

H ist unabhängig von y. Die Kontrollpräparation mit festem Referenzwert für Uhr 4 lässt für beide Eingangspakete dieselbe Dichteauslese zu. In der lokalen Prüfung werden gleichphasige flache Pakete gleicher Breite direkt am alten Schnitt eingesetzt. Bei der Endrechnung weiter unten werden sie dagegen durch den ganzen Verlauf propagiert. Beide Rechnungen verwenden denselben Wirkungsterm.

Seien die Eingangsfenster [c−r,c+r] und seine Verschiebung um t. Mit K₀=15/4, D=K₀(3/722)^(1/4), R=K₀/2²² und C=−7/4+K₀/8 gelten für die getrennten Pakete (c,r,t)=(C,R,1/(32√D)), für die benachbarten Hälften (C−R/2,R/2,R). Das spätere Uhrfenster liegt um Z₀=−7/4+5K₀/8. Für |z−Z₀|≤Δz, |w−wₘ|≤Δw und w≤wₘₐₓ ist die Phase zwischen entsprechenden Integranden bis auf die konstante Phase a wₘ t(t−2(Z₀−c)) höchstens um E verschieden:

```
E = a t [Δw (2(Z₀−c)−t) + 2 wₘₐₓ (Δz+r)].
η = a wₘₐₓ r [2(|Z₀−c|+Δz+t)+r],      b = 1−η²/2.
```

Nach Division durch das gemeinsame Eingangsvolumen hat jede Spalte punktweise mindestens den Betrag b, und ihre Differenz nach Phasenausgleich höchstens den Betrag E. Diese Schranken gelten auch in der Norm mit beliebigem gemeinsamen, positiven, normierten Ausgangsmass, das |H|² enthält. Der Abstand einer Spalte zum Strahl der anderen liefert für die normierten reinen Ausgänge den Spurabstand T≤E/b. Die beste Trefferquote bei gleichen bedingten Vorchancen ist (1+T)/2. Die ausgeglichene Differenz bzw. Summe der beiden Spalten begrenzt das Singulärwertverhältnis durch E/(2b−E).

| Alter Uhreingang | Auslesefenster an 12 | Obergrenze der Trefferquote | Obergrenze für σmin/σmax |
|---|---|---:|---:|
| Zwei getrennte Pakete | präparierte Dichte und Uhr, je Klasse | 50,000001915 % | 1,915 · 10⁻⁸ |
| Benachbarte Hälften | präparierte Dichte und Uhr, je Klasse | 50,000000000053 % | 5,288 · 10⁻¹³ |
| Zwei getrennte Pakete | w von 0 bis 1, Uhr Z₀ ± K₀/64 | 50,666214 % | 0,006707 |
| Benachbarte Hälften | w von 0 bis 1, Uhr Z₀ ± K₀/64 | 50,000018750 % | 1,875 · 10⁻⁷ |

Die letzten beiden Zeilen öffnen die Fenster rechnerisch. Im präparierten Fall ist Δz=R. Die Schranken gelten für die zwei definierten Eingänge mit derselben Auswahl bei bekannter Dichteklasse. Die Rechnung nimmt die Hilfsnorm L² und eine gemeinsame Gewichtung der offenen Zielkoordinaten an. Normiert man die Abbildung auf σmax=1, kann eine nachfolgende kontraktive Filterung einen unbekannten Zweimodenzustand mit exakter Normtreue höchstens mit gleichförmiger Erfolgswahrscheinlichkeit (σmin/σmax)² übertragen. Im getrennten präparierten Fall ist dies weniger als 3,67 · 10⁻¹⁶. Diese relative Schranke erfordert keine absolute Normierung des lokalen Kerns.

Bei positivem flachem Gewicht auf einem offenen Dichteintervall sind die Spalten mathematisch linear unabhängig. Nach Abspalten von H sind sie für festes z ganze Funktionen in w mit gleichem Wert bei w=0. Ihre Ableitungen dort unterscheiden sich um i a t(t−2(z−c)). Dieser Ausdruck ist im geprüften Uhrbereich ungleich null. Die unabhängige Quadratur ergibt bei getrennten Eingängen im Zentrum des positiven Uhr-5-Pakets in der hohen Klasse T≈1,317 · 10⁻⁸.

**Kontrolle der Präparation.** Wird das Dichtefenster stattdessen mit dem tatsächlichen y mitgeführt, ändert sich bereits das Zentrum der an 12 präparierten Gleichverteilung. Hält man Klasse, Begleituhren und die Position im jeweiligen Eingangspaket fest, beträgt die klassische optimale Trefferquote für das Paket anhand dieser Dichte 80,5269 bis 80,6349 % bei getrennten Fenstern. Diese Zahl beschreibt die Information in der bedingten Präparation. Sie lässt sich direkt aus dem Versatz zweier gleich breiter Intervalle bestimmen.

## 2. Allgemeine Wirkung mit zwei kohärenten Eingangsfenstern

Beide Pakete werden jetzt von Anfang an mit ihrem wirklichen Y4 präpariert. Auch die frühen Dichtezentren werden jeweils neu berechnet. In beiden Armen und beiden Dichteklassen laufen dieselben 50 Paarterme, beide Uhr-5-Pakete und dieselbe Endprojektion. Die benachbarten Hälften gehören zum ursprünglichen schmalen Paket. Für das getrennte Paar kommt ein zweites echtes Eingangsfenster innerhalb u4=1/8 ± 1/64 hinzu. Das erweitert die Präparation. Jeder der sieben inneren Dichtewerte bleibt im jeweiligen ±1-%-Band. An 12 werden die absolute Schwelle 1/8 und die lokale Profilschwelle für jede Dichteklasse geprüft.

In der Originalpräparation hängt der Nenner q(y) der drei hinteren Dichteverschiebungen von der wirklichen Uhr 4 ab. Dann ist die Phasendifferenz beider Dichteklassen für jede Geschichte exakt 2D εQ₀ (ε=2⁻¹⁴, Q₀=−5/4). Jede gemeinsame Eingangsmaske liefert identische Endintensitäten. In der Kontrollpräparation wird nur zur Festlegung dieser Dichtezentren Uhr 4 auf C gesetzt. Die Funktion q(C) hängt weiterhin von den übrigen Uhren ab. Nach Entfernen einer konstanten Klassenphase bleibt der klassenungerade Phasenterm

```
g = D ε Q₀ [q(y)−q(C)] / q(C).
```

**Gleichphasiger Eingang.** J bezeichnet das Integral von |(L+R′)/2|² über dieselbe Endauslese. L und R′ sind die beiden komplexen Paketbeiträge, keine Wahrscheinlichkeiten. Die hohe Klasse hat bei getrennten Fenstern die grössere Intensität. Für beide Anfangsdichten 1/8 und 1/4 ergibt sich

```
0,00000000132963016 ≤ (Jhoch − Jniedrig)/Jniedrig ≤ 0,00000000138895812.
```

Zur Vorzeichenprüfung werden zwei unabhängige innere Geschichten bei gleichem Endrand verwendet. Bezeichnen S und S′ ihre klassenneutralen Phasen, lautet die Intensitätsdifferenz in gemeinsamen Einheiten −2 E[sin(S−S′) sin(g−g′)]. Der Nenner ist E[cos(S−S′−g+g′)]. Die vier gleich gewichteten Bereiche (zwei Uhr-4-Fenster × zwei Uhr-5-Pakete) ergeben 16 Paarungen. Alle werden vor der Division mit nach aussen gerundeter Arithmetik eingeschlossen. Der frühere gemeinsame Randfaktor kürzt sich. Die separate Rechnung aus den 50 Termen ergibt rund 1,3593 · 10⁻⁹.

**Kontrolle mit vorgegebener Phase.** Zwei gleich häufig gewählte Präparationen geben dem zweiten Paket die Phase −i oder +i. Aus ihren Intensitäten am selben Ausgang folgt der bedingte Anteil p=I₋/(I₋+I₊) der −i-Präparation an den Erfolgen. Bei festem Dichteprofil beträgt p(hoch)−p(niedrig) rund −1,4361 · 10⁻⁶ für getrennte Pakete bzw. −4,04 · 10⁻¹¹ für benachbarte Hälften. Beim ursprünglichen Profil sind beide Werte exakt null. Die Intensitäten der vier Eingangsphasen in der Gegenrechnung stehen in der Reihenfolge −i,+i,+1,−1, jeweils in gemeinsamen Einheiten.

## Physikalischer Status und Quellen

Die Intensitätsaussage setzt eine kohärente Eingangspräparation, vergleichbaren Eingangsfluss und dieselbe Ausleseeffizienz beider Klassen voraus. Sie folgt im endlichen N15-Modell ohne zusätzlichen Tausch am Schnitt. Offen ist, ob das physische Randmass diese gemeinsame Präparation mit kontrollierter Kohärenz und Normierung liefert. Die unabhängige Massenkalibrierung und die 60 P3-Prüfpunkte sind dadurch weiterhin offen.

- [Veröffentlichte Kontrollpräparation und Quellstand, PR 371](https://github.com/thomasmgfeller/x6-spectral-astrolabium/pull/371)
- [Exakter Basiscommit](https://github.com/thomasmgfeller/x6-spectral-astrolabium/commit/cd54fe04a7e77df0db08d0eaf90ba0a1accc7b2c)
- [Allgemeine Theorie zur Unterscheidbarkeit, J. Watrous, The Theory of Quantum Information, Kapitel 3](https://cs.uwaterloo.ca/~watrous/TQI/TQI.3.pdf)
