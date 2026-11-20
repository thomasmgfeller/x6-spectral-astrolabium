# CST-DUST · Synchronisierte, verteilte Anfangspräparation für zwei Massen

Untersuchung vom 20. November 2026, aufbauend auf [PR #334](https://github.com/thomasmgfeller/x6-spectral-astrolabium/pull/334). Der Stand von `main` für die Eingaben ist `b125a0e7bffdefe2b68be454d13c0af9099a53ff`. Die Rechnung untersucht die 1 048 skalaren Ordnungstypen des N15-Katalogs, eine endliche Hilfspräparation und die Staubwirkung auf denselben Feldern. Auf 998 Typen trägt der verteilte Fluss beide Massen über beide vollständigen Zeitfenster. Bei einer zusätzlichen Regel mit endlicher Präzision zeigen sich sowohl Träger mit strikt positiver als auch Träger mit strikt negativer Wirkungsstromladung. Der physikalische Eichfaktor und die physikalischen Sektornormen sind offen. Alle 60 P3-Datensätze stehen auf `NOT_RUN`.

## 1. Randzeit, Fluss und Massenvorgabe

Alle maximalen Überdeckungspfade vom Eintritt 3 bis zum Austritt 7 teilen sich den vorgegebenen Fluss M zu gleichen Teilen. Jeder vollständige Schnitt, der Eintritt und Austritt trennt, trägt damit die markierte Schnittmasse M. Das entspricht der Flusszählung aus PR #334. Alle Pfade beginnen bei derselben relativen Uhrzeit null. Sie enden bei D = T₇ − T₃ = 4Δ − δ. Hier gelten β = 4/√6, Δ² = 2/(19β) und die beiden archivierten δ-Fenster [−3/32,−1/32] und [1/32,3/32]. Die Zukunftsuhr ist bereits Teil des endlichen Randvertrags. Diese Synchronisation identifiziert Eintritt und Austritt der markierten Pfade. Die Rekonstruktion einer physikalischen P3-Anfangsfläche aus einer dynamischen vierdimensionalen Geometrie ist offen.

Die sieben relativen Uhren uᵥ = (Tᵥ − T₃)/D durchlaufen den offenen Bereich 0 < uᵥ < 1 mit uᵥ < u𝓏 für alle v ≺ z. Auf jedem Pfad teilen Mittelpunkte zwischen aufeinanderfolgenden inneren Uhren das Intervall [0,1] in Verweildauern. Die Randzellen reichen bis 0 bzw. 1. Die über die Pfade gemittelten Zellanteile fᵥ sind positiv und summieren sich zu 1. Entsprechend PR #334 setzen wir auf der markierten Referenzfamilie wᵥ = MD fᵥ. Zulässig sind 0 < wᵥ < 1. Die Regel verwendet weder die Stromantwort noch die Fläche. M ist eine kontrollierte Eingangsmarkierung. Die Gleichung für wᵥ setzt eine zusätzliche Beziehung zur integrierten Dichte der Wirkung voraus. Eine absolute physikalische Ruhemasse wird dadurch noch nicht geeicht.

## 2. Exakte Kapazität im offenen Uhrenbereich

Für jeden Typ wird z* = minᵤ maxᵥ fᵥ(u) auf dem abgeschlossenen Uhrenbereich bestimmt. Ein offener Bereich zulässiger Uhren existiert bei gegebenem δ genau dann, wenn MDz* < 1. Wegen der strikten Kapazitätsreserve lässt sich jeder zulässige Randzeuge etwas mit einer strikt inneren Uhrbelegung mischen. Die Ungleichungen gelten danach auf einer offenen Umgebung. Bei MDz* ≥ 1 ist die strikte Feldgrenze unerreichbar. Für beide Massen gemeinsam genügt es, die größere zu prüfen. Ein Zeuge im gesamten Doppelpaket kann bereits beim größten D gewählt werden.

| Markierte Masse | Offener Uhrenbereich bei jedem äußeren Offset | Nur in Teilen des Doppelpakets | Nirgends |
|---|---:|---:|---:|
| 1/4 | 1 048 | 0 | 0 |
| 1 | 1 048 | 0 | 0 |
| 4 | 998 | 35 | 15 |

Bei 33 der 35 Teilfälle trägt ausschließlich der gesamte rechte Lappen. Zwei tragen außerdem einen Teil des linken. Das Ergebnis zählt Ordnungstypen. Innerhalb eines tragenden Typs können einzelne Uhren unzulässig sein. Die 998 Typen erhalten durch die Zählung kein gemeinsames Gewicht.

`certificates.json` enthält je Typ einen rationalen Primärzeugen und einen dualen Zeugen mit identischem Zielwert. `verify.py` prüft die Ungleichungen und den Zielwert exakt, auch bei Lösungen am Rand. Ein zweiter Algorithmus enumeriert maximale paarweise vergleichbare Mengen, maximiert den Abstand von den Ungleichungsgrenzen bei fester Masse und prüft die Ergebnisse mit rationalen Schranken. Beide Verfahren stimmen bei M=4 für jeden der 1 048 Typen an allen vier Endpunkten überein.

## 3. Eigenzeit aus der freien Staubwirkung

Für eine unabhängige Variation einer positiven inneren Dichte ist 1 + Γᵥ = 0 eine notwendige Sattelgleichung. Mit Yᵥ = Tᵥ/Δ, e = δ/Δ und den diskreten Benincasa-Dowker-Koeffizienten gilt 19(1+Γᵥ) = 19 + Σᵧ bᵧᵥ(Yᵥ−Yᵧ)². Alle minimalen inneren Ereignisse haben deshalb den gleichen erzwungenen Wert a = (e²−4e−2)/(2(1+e)). An einem ersten nichtminimalen Ereignis liegen d minimale Vorgänger. Die nächste Uhr muss oberhalb von a und vor der Austrittsuhr 2 liegen. `saddle.py` rekonstruiert die Koeffizienten aus der tatsächlichen Ordnung, prüft die quadratische Gleichung bei e = ±1/4 und zertifiziert Vorzeichenausschlüsse auf jeweils 256 rationalen Teilintervallen.

Ein streng wachsender freier Sattel mit sieben inneren positiven Dichten scheitert auf dem **ganzen linken Lappen bei allen 1 048 Typen**, auf dem **ganzen rechten bei mindestens 942**. Die restlichen 106 rechts bestehen nur diese notwendige lokale Prüfung. Auf der markierten Familie konditioniert die Verweildauerregel die Dichten. Für eine Quantensumme werden die Dichten integriert. Deshalb begrenzt dieser Befund die Interpretation als freien klassischen Sattel.

## 4. Endliche Präzision, Hilfsmaß und Stromvorzeichen

Der genaue Graph wᵥ = MDfᵥ(u) hat bei M>0 im ursprünglichen Produktmaß der sieben inneren Dichten bedingt auf u das Maß null. Das positive Gewicht jeder Einzelzelle gehört zur stetigen Komponente. Diese Aussage bleibt nach Integration der Uhren gültig. Um auf einem Bereich mit positivem Hilfsmaß zu rechnen, wurde eine zusätzliche endliche Präparation untersucht. Die Uhrenzentren sind durch die längste innere Kette bis zum Ereignis, geteilt durch die maximale innere Kettenlänge plus eins, festgelegt. Isolierte Ereignisse sitzen bei 1/2. Jede relative Uhr erhält eine Halbbreite von 1/64 und jede positive Dichte ein symmetrisches Band von ±1 % um ihre Verweildauervorgabe. Die Breiten sind diagnostische Annahmen. Sie definieren für jede Masse einen eigenen Feldbereich. Die endliche Breite verändert die exakte Markierung in eine Toleranz für die Dichtesumme W = Σw. W/D liegt innerhalb von ±1 % der eingesetzten Masse.

Von 1 048 Typen enthalten 164 **den ganzen so gewählten Bereich** bei beiden Zielmassen und allen Randuhrwerten innerhalb der Dichtegrenzen. Bei den übrigen 884 überschreitet mindestens ein Teil dieser fest gewählten Box die Grenze. Der größere offene Uhrenbereich aus Abschnitt 2 bleibt dadurch je nach Typ zugänglich.

Für die 164 Typen wird der signierte feine Anfangsstrom der Originalwirkung ausgewertet, p = −∂S/∂τ bei gemeinsamer Verschiebung aller vier Vergangenheitsuhren. Die 32 Teilintervalle je Lappen schließen p/M auf allen inneren Uhr- und Dichtewerten ein. 94 Typen liefern auf beiden Lappen durchgehend positives p, 26 durchgehend negatives. Für 44 liefern die verwendeten Schranken keine gemeinsame strikte Vorzeichenaussage über beide Lappen. Die vollständigen Einschließungen stehen in `census.json` in Milliardstel-Einheiten. Direkte symmetrische Differenzen der archivierten Staubwirkung kontrollieren die Vorzeichenkonvention und die Einhüllungen an 328 Typ-Offset-Kombinationen. Die 94 sind ein Ergebnis der Auswertung. Ihre nachträgliche Auswahl als neues Ensemble würde eine eigene physikalische Begründung verlangen.

## 5. Fünf verteilte Pfade auf dem bisherigen Referenztyp 2324

Die Pfade enthalten die inneren Ereignisse (4,11), (4,13), (5,12), (6,11) und (14). Bei M=4 liegt die belegte Dichte im gesamten geprüften endlichen Bereich unter 0,925. Auf dem einzelnen Weg aus PR #334 hatte Zelle 13 bei derselben Masse schon die Grenze 1 überschritten.

Für jede der sieben Uhren beträgt das unbedingte innere Hilfsmaß ihres Fensters 2rD/3 bei fester äußerer Uhr und r=1/64. Jede Dichte trägt bedingt auf die Uhr die halbe Bandbreite εMDfᵥ bei. Aus den vollständigen Intervallen der fᵥ folgen für das Produktmaß konservative, positive Untergrenzen von 1,71 × 10⁻³⁹ bei M=1/4 und 4,61 × 10⁻³¹ bei M=4. Das sind Untergrenzen im ursprünglichen inneren Hilfsmaß auf diesem einen Typ. Sie beschreiben keine empirische Häufigkeit.

Zusätzlich wird die Phase der ursprünglichen Staubwirkung auf dem ganzen Feldbereich, beiden Randuhrlappen und beiden äußeren Dichtepräparationen eingeschlossen. Für eine reelle gleichphasige Eingangspräparation und positives Hilfsmaß liegt der Betrag des mittleren Phasenfaktors mindestens bei 1−(Smax−Smin)²/8. Das folgt durch Rotation in die Mitte des Phasenintervalls und cos x ≥ 1−x²/2. Der ungünstigste der sechs geprüften Massen-/Anfangsdichtefälle hat die untere Schranke 0,7702. Die Gravitationsphase ist auf diesem Träger konstant. Ein gemeinsamer Skalarfaktor wurde ausgeklammert. Die Schranke bezieht sich auf den Staubfaktor vor der Ladungsauswahl.

| Randuhrfenster | Garantierte äußere Schranken für p/M auf Typ 2324 |
|---|---|
| Links | [−0,564583, −0,308422] |
| Rechts | [−0,327591, −0,143908] |

Im Zentrum der inneren Box liefern die symmetrischen Wirkungsdifferenzen bei e = −1/4 bzw. +1/4 exakt −391/912 und −69/304. Der algebraische echte Staubvakuumwert und die Kontrolle mit leerem Inneren bei unverändertem positivem Außenkragen ergeben jeweils p=0. Die positive Massenauswahl gemäß PR #333 mit positivem Eichfaktor und Vakuumnullpunkt hat auf diesem Bereich **exakt leeren Träger**. Die unselektierte Kohärenzschranke und der verschwindende selektierte Beitrag sind miteinander verträglich.

## 6. Physikalische Entscheidung

Die Flussaufteilung und die Synchronisation definieren eine nachrechenbare Referenzpräparation. Eine Hilfsnorm, eine signierte Quellantwort und ein einzelner Staubfaktor liefern keine positive physikalische Messverteilung auf dem gekoppelten Ensemble. Dafür fehlen weiterhin eine unabhängig bekannte Schnittmasse samt Skala, die zugehörige physikalische Ladungsmessung und Vakuumkontrolle sowie die gemeinsame Paarung für die Geometrie-, Staub- und Skalarbeiträge. Das gesamte Ensemble muss seine vorgegebenen Historiengewichte behalten. Für die Quotienten der bedingten Auslese braucht es eine positive Untergrenze des physischen Nenners einschließlich Unsicherheit. Erst dann lassen sich ein Eichfaktor, seine ±2-%-Kontrolle bei M=1 und seine Übertragbarkeit bis M=4 beurteilen.

Die 60 Originaldatensätze und ihre gespeicherte Zulassungsentscheidung werden bei der Wiederholung eingelesen. Der physikalische M=1-Pilot, die Flächenmessung bei T* und die Radiendifferenz bleiben offen. Die Zusatzprüfungen auf endlich breiten Feldbereichen und die katalogweite Vorzeichenanalyse sind explorativ. Die einzelnen Entwurfsdateien dokumentieren die Reihenfolge. Es gab keine öffentliche Vorregistrierung.

## Offline nachrechnen

Das entpackte Verzeichnis enthält Eingaben, Herkünfte mit Git-Prüfsummen, exakte Zertifikate und die von den Prüfern gelesenen Ergebnisse. Python ab 3.10 genügt für die vollständige Zertifikats- und Ergebnisprüfung.

```sh
sha256sum -c SHA256SUMS
python3 -B verify.py > wiederholung.json
cmp result.json wiederholung.json
```

Mit SciPy und NumPy können beide Optimierungsrechnungen zusätzlich neu erzeugt werden. `solve.py` schreibt `certificates.json`. Je nach Optimiererversion sind andere ebenso gültige optimale Zeugen möglich.

```sh
python3 -B solve.py > kapazitaet_neu.json
python3 -B crosscheck.py inputs/catalog.json > unabhaengig_neu.json
```

[Referenzrechnung und Flusszuordnung](https://github.com/thomasmgfeller/x6-spectral-astrolabium/tree/b125a0e7bffdefe2b68be454d13c0af9099a53ff/research/rax_cqg/dust_collapse/cut_mass_charge_vacuum_v0_1) · [Ladungsselektor](https://github.com/thomasmgfeller/x6-spectral-astrolabium/tree/b125a0e7bffdefe2b68be454d13c0af9099a53ff/research/rax_cqg/dust_collapse/boundary_mass_sector_v0_1) · [P3-Prüfplan und Zulassung](https://github.com/thomasmgfeller/x6-spectral-astrolabium/tree/b125a0e7bffdefe2b68be454d13c0af9099a53ff/research/rax_cqg/dust_collapse/correspondence_v0_1)
