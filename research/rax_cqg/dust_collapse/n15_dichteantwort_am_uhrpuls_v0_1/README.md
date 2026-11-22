# CST-DUST · Die Antwort der Dichte an Ereignis 11

Die beiden Randvorschriften aus PR #360 lassen sich im endlichen N15-Referenzmodell mit den vier äusseren Eingangsuhren unterscheiden. Ein festes Profil dieser Uhren greift gezielt die Dichte an Ereignis 11 heraus. Ein zweites Profil misst die Dichte an Ereignis 5 und erkennt eine kompensierte Änderung beider Verweilzellen.

## Was das Modell vorhersagt

Der Versuch verwendet Typ 2097151, markierte Masse 1, die beiden ursprünglichen breiten Uhrfenster und den symmetrischen Puls ±1/8 an der weitergereichten Uhr 6 hinter Ereignis 11. Für jede Pulsrichtung werden vier Varianten der originalen Wirkung an den Eingangsuhren integriert. Ihre gemischte Phasendifferenz ist die Auslese X. Die Tabelle zeigt X(−h)−X(+h) bei Randdichte 1/4. Die letzte Spalte ist die normierte Differenz der zwei ungefilterten Pulsintensitäten bei gleicher ursprünglicher Armnormierung.

| Verwendung der verschobenen Uhr | Antwort an 11 | Antwort an 5 | Intensitätsasymmetrie |
|---|---:|---:|---:|
| Nur in der weiterlaufenden Wirkung | +0,00000035 | +0,00000032 | −0,000061 |
| Auch im offenen Dichtefenster 11 | +0,02898052 | +0,00004003 | +0,229850 |
| Dichtefenster 11 und 5 gemeinsam neu präpariert | +0,02887621 | −0,02898313 | +0,000166 |

Am Zentrum 1/8 ergibt die gezielte Antwort an 11 entsprechend +0,00000018, +0,02898567 und +0,02892669. In der dritten Zeile werden die Verweilzellen zu neu gebildeten Mittelpunktsgrenzen passend neu präpariert. Die Wirkungsquelle bleibt wie in den anderen Rechnungen rechtsseitig. Diese Variante ändert auch die bereits früher abgeschlossene Zelle 5.

Die Profile der vier frühen Uhren lauten V₁₁=(29,23,16,8)/64 und V₅=(16,8,0,0)/64. Zusammen mit der gemeinsamen Verschiebung U=(1,1,1,1) liefert die gemischte Wirkungsdifferenz auf einer einzelnen Geschichte exakt w₁₁/D bzw. w₅/D. D bezeichnet die ursprüngliche präparierte Dauer. Die Tabelle verwendet die relativen Phasen der tatsächlich integrierten Amplituden. Die Übereinstimmung zweier Quadraturen ist eine numerische Kontrolle. Beide Antworten funktionieren ohne erneute Anpassung einer Masseneichung.

## Ein Test mit nur zwei Intensitäten

Für die zwei Vorschriften aus PR #360 ergibt sich bei der vorgeschriebenen gemeinsamen Normierung und beiden Randdichtezentren eine zertifizierte Trennung. Für das feste Fenster liegt A im gemeinsamen Einschluss [−0,02686; +0,02706], für das mitbewegte Fenster im Einschluss [+0,16662; +0,34320]. Die vorab gewählte Schwelle A=0,10 trennt diese beiden Modellvorhersagen. Die Originalamplituden waren öffentlich. Die neue Auswertung mit Intervallbeweis ist kein externer Blindtest.

Die Armgewichte beim mitbewegten Fenster betragen 0,88343126 für +h und 1,11656874 für −h relativ zum gemeinsamen Ausgangsmass. Normiert man jedes neu präparierte Armgewicht separat, fällt die Asymmetrie bei Randdichte 1/4 von +0,229850 auf −0,000171. Die Vier-Phasen-Antworten sind gegen positive reelle Verstärkungen invariant. Die kompensierte dritte Zeile zeigt ebenfalls, warum die Intensitäten allein die Dichte an 11 nicht allgemein bestimmen.

## Ein Test auf Erhaltung eines früheren Dichteprotokolls

Für den positiven Zweig M>0 gilt vor dem Puls für jede zulässige Belegung

    (99/100)·(7/64) ≤ w₁₁/(DM) ≤ (101/100)·(9/64).

Bei der blossen Phasenanregung bleibt das gesamte positive Präparationsmass innerhalb dieses Bandes. Wird das Dichtefenster mitverschoben, liegen beim positiven Puls nachweislich 36,93 bis 36,99 % unter der alten Untergrenze, beim negativen 35,42 bis 35,48 % über der alten Obergrenze. Das sind Anteile des je Arm normierten positiven Referenzmasses. Sie sind keine Detektorwahrscheinlichkeiten der kohärenten Auslese.

Wenn das frühere w₁₁/D bei fest präpariertem M bereits unabhängig und dauerhaft registriert ist und der späte Puls diesen Eintrag bewahren muss, kann die vollständig mitbewegte Vorschrift das alte Ensemble nicht fortsetzen. Die unverschobene Wirkung allein erzwingt eine solche Registrierung nicht. Die äusseren Phasendifferenzen prüfen eine Ensembleantwort und ersetzen keinen vor dem Puls verfügbaren Einzelrecord. Der physische P3-Test braucht einen entsprechend begründeten Randzugriff und eine unabhängige positive Masseneichung. Alle 60 physischen Prüfpunkte führen weiterhin den Status NOT_RUN.

## Reproduktion

Im entpackten Ordner prüft der folgende Befehl mit der Standardbibliothek von Python 3.10+ die Algebra, die nach aussen gerundeten Einschlüsse und die Dateiintegrität.

    python3 -B pruefen.py --nur-exakt

Die vollständige Wiederholung benötigt zusätzlich NumPy.

    OPENBLAS_NUM_THREADS=1 python3 -B pruefen.py

HERLEITUNG.md erklärt die bewegten Integrationsgrenzen, den Quellenentwurf, die beiden unabhängigen Trägerrechnungen und die Geltungsgrenzen. quelle.json, intensitaet.json und vorrecord.json enthalten die exakten Ergebnisse und Intervallschranken. auslese.json, zellkontrolle.json und kontrollen.json enthalten die numerischen Auswertungen. herkunft.json nennt die bytegleichen Git-Quellen. Die vier lokalen Prüfpläne dokumentieren die Reihenfolge von Hauptversuch und Erweiterungen.

[Git-Stand nach PR #360](https://github.com/thomasmgfeller/x6-spectral-astrolabium/commit/15d6e9d0f21b1baf7a84b26a74b0874823c1800d)
