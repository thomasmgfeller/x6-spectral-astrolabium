# Wann die Massenauslese zwei Prozent Genauigkeit erreicht

CST-DUST · N = 15 · Modellstudie vom 22. November 2026

Bei markierter Masse M = 4 erfüllen 46 der 61 geeigneten Ordnungstypen die Zwei-Prozent-Grenze für jedes zugelassene positive normierte Hilfsmass an beiden Eingangsdichtezentren. Für die übrigen 15 gibt es an mindestens einem Zentrum eine konkrete Präparation mit grösserem Fehler. Alle 122 Kombinationen aus Typ und Dichtezentrum sind entschieden. Die Auswertung ist eine explorative Fortsetzung von [PR #351](https://github.com/thomasmgfeller/x6-spectral-astrolabium/pull/351).

| Rechnung | Typen an beiden Zentren zertifiziert | Einzelne Zentren zertifiziert |
|---|---:|---:|
| Publizierte Schranke aus PR #351 | 19 / 61 | 43 / 122 |
| Neue Winkelabschätzung mit den publizierten Wirkungsintervallen | 40 / 61 | 82 / 122 |
| Zusätzlich gemeinsame Abhängigkeit der Uhren und Dichten eingeschlossen | 43 / 61 | 89 / 122 |
| Zusätzlich vollständige Teilüberdeckung der fünf offenen Einzelzeilen ohne Gegenbeispiel | 46 / 61 | 94 / 122 |

Für die weiteren 28 Einzelzeilen gibt es einen verifizierten Fehler über 2 %. Davon betreffen 26 Zeilen beide Zentren von 13 Typen. Bei den Typen 2846 und 6622 besteht jeweils ein Zentrum, das andere hat ein Gegenbeispiel. Die 15 Typen mit Gegenbeispiel sind 2846, 3000, 6622, 6840, 7088, 39468, 41753, 41758, 41820, 41822, 45936, 58929, 59193, 59262 und 377978. Alle 19 bisherigen positiven Typentscheidungen wurden reproduziert. Für Typ 2324 ist der relative Fehler bei Masse 4 an beiden Zentren auf 1 % beschränkt. Bei den Massen 1/4 und 1 gilt der schon publizierte positive Befund für 61 von 61 Typen.

## Fragestellung und Modell

Es gelten die beiden vollständigen Uhrfenster, die Pfadanteile und die sieben inneren Uhren von PR #351, das relative Dichteband η = 1/100, die Kopplung λ = 1/2 und die Eingangsdichtezentren 1/8 und 1/4. Beide Zeigerarme verwenden dieselbe positive normierte Verteilung der Feinhistorien und dieselbe gleichphasige Eingangspräparation je festem Ordnungstyp. Der gemeinsame von den inneren Variablen unabhängige, nichtverschwindende Skalarfaktor kürzt sich. Die Markerantwort X erfüllt |X−M| ≤ ηM. Die Schätzung ist der Hauptwert des Winkels von A₊ mal dem komplex Konjugierten von A₋, geteilt durch λ. Gezählt wird ein Typ nur bei einer Garantie an beiden Zentren. Die untersuchte Fehlerart ist der systematische Fehler der modellierten Auslese.

## Beweis der Winkelschranke

Setze ξ = X−M und Z(t) = ∫ exp(i(S+tξ)) dμ für −λ/2 ≤ t ≤ λ/2. Liegt S im eingeschlossenen Intervall [L,H], belegen die Integranden bei festem t einen Sektor der Breite höchstens w = H−L+ληM. Für w < π liefert die Projektion auf seine Mittelrichtung |Z(t)| ≥ cos(w/2) > 0. Der stetige Winkel ist differenzierbar mit Ableitung Re(∫ ξ exp(i(S+tξ)) dμ / Z(t)). Das Ausklammern der idealen Phase fügt an den beiden Enden genau λM zum Differenzwinkel hinzu.

Die beiden Teilsummen P und N entstehen durch Multiplikation mit den positiven oder verschwindenden Faktoren (1+ξ/(ηM))/2 und (1−ξ/(ηM))/2. Es gilt P+N=Z und P−N=∫(ξ/(ηM)) exp(i(S+tξ)) dμ. Bei p=|P| und n=|N| ist der Betrag der normierten Winkelableitung höchstens

    |p²−n²| / (p² + n² + 2pn cos θ),

wobei θ der Winkel zwischen P und N ist und |θ| ≤ w gilt. Verschwindet einer der Beiträge, beträgt dieser Quotient eins. Bei w ≤ π/2 ist der Quotient höchstens eins. Bei π/2 < w < π ist er höchstens 1/sin(w). Für den Nachweis bei stumpfem θ dient die Identität

    (p²+n²+2pn cos θ)² − sin² θ (p²−n²)² = ((p²+n²) cos θ + 2pn)².

Integration über die Länge λ ergibt für den relativen systematischen Fehler η bzw. η/sin(w). Zusätzlich wird λM(1+Fehlerschranke) < 3 < π im Hauptzweig geprüft. Der Rechenkern verwendet für cos(w) ein unteres Taylorpolynom bis Grad zehn und rundet die relative Obergrenze nach oben. Bei w ≥ 3 wird dieser Test ausgelassen. Bei der Entscheidung werden ausschliesslich rationale Grenzen verwendet.

## Einschliessung der gemeinsamen Phase

Der publizierte Prüfer liefert je Typ 16 Wirkungsintervalle über beide Uhrlappen. Eine zweite Rechnung führt den Offset, das gemeinsame Eingangsdichtefeld, die sieben inneren Uhren und ihre Dichteabweichungen ausdrücklich als gemeinsame Variablen. Eine affine Form speichert den konstanten Anteil und die linearen Koeffizienten sowie eine symmetrische Fehlergrenze. Bei der Multiplikation gehen quadratische Abweichungen, die linearen Beiträge der Restfehler und die Rundung auf dem Binärgitter 2⁻⁷² in den Rest ein. Beide Einschliessungen werden je Zelle geschnitten. Erst danach werden Minimum und Maximum über die vollständigen Lappen genommen. 5 856 direkte Auswertungen der Staubwirkung kontrollieren diese Intervalle an repräsentativen Feldern.

Die optionale Teilung halbiert eine Zelle entlang einer Eingangsvariablen und behält beide Hälften. Die Prüfung rekonstruiert alle Blätter aus dem Schnittprotokoll und kontrolliert deren Gesamtvolumen. Für die Typen 2454, 2456 und 7069 genügten 7, 6 und 10 Halbierungen. Für die beiden zusätzlich überprüften Einzelzentren von 2846 und 6622 genügten 9 und 60 Halbierungen. Der Wirkungsbogen erstreckt sich auch nach der Teilung über die gesamte zugelassene Präparation.

## Gegenbeispiele aus denselben Feldern

Für den Test werden zwei erlaubte Feinhistorien desselben Typs und desselben Eingangsdichtezentrums mit positiven Gewichten p und n gewählt. Die Uhren, Eingangsdichte und alle inneren Dichten liegen im Inneren ihrer zulässigen Intervalle. Die inneren Dichteabweichungen werden für die erste Historie gleichsinnig positiv, für die zweite gleichsinnig negativ gesetzt. Die Vierwertquelle ergibt X± = M(1 ± η·1023/1024). Mit h = λMη·1023/1024 und den Staubphasen S₊ und S₋ folgt nach Abziehen der idealen Phase und bis auf einen positiven Faktor

    Re = (p²+n²) cos(h) + 2pn cos(S₊−S₋)
    Im = (p²−n²) sin(h).

Koordinaten und Gewichte stammen aus einer endlichen explorativen Suche. Für die Entscheidung werden der algebraische Skalenfaktor Δ⁴ = 3/722, beide Aktionen, die kausale Uhrenordnung, die Dichtekapazität, die Quellkoeffizienten und der Winkel durch rationale Intervalle geprüft. Der direkte Aufbau der beiden komplexen Amplituden dient als zusätzliche numerische Kontrolle. Die beobachtete Abweichung für Typ 6840, Zentrum 1/8, liegt im geprüften Intervall [3,6562 %, 3,6684 %]. Dieser Zeuge verwendet die Gewichte 7 und 4. Das freie Hilfsmass ist hier durch die beiden angegebenen Historien bestimmt. Eine fest vorgegebene kontinuierliche Verteilung kann denselben Typ anders bewerten.

## Physikalische Reichweite

Marke und Hilfsmass gehören zur Modellpräparation. Die Gegenbeispiele widerlegen eine gleichmässige Fehlerschranke für die betreffende Hilfsmassklasse. Um den Fehler eines tatsächlichen Staubensembles vorherzusagen, braucht es dessen unabhängig aus Wirkung und Randpräparation bestimmte Gewichte mitsamt Phasen. Endliche Messstatistik, Quellenkalibrierung, Interferenz zwischen verschiedenen Typen und physikalische Normierung sind offene Aufgaben. Die 60 physischen P3-Prüfpunkte stehen auf NOT_RUN.

## Offline wiederholen

Python ab 3.10 mit Standardbibliothek reicht aus. Im entpackten Ordner führt `python3 -B alles_pruefen.py` die Integritätskontrolle, die erneute Berechnung der Einschliessungen und die exakte Prüfung aller archivierten Zeugen aus. Mit `--suche` wird zusätzlich die Gleitkommasuche wiederholt. Sie dient der Auswahl der Zeugen. Alle 122 Entscheidungen stehen in `entscheidungen.csv`. Fehlergrenzen sind dort als exakte Brüche des relativen Fehlers angegeben. `upper_bound_applies_to` kennzeichnet den Unterschied zwischen einer Garantie für alle zugelassenen Masse und der Einschliessung eines individuellen Gegenbeispiels.

Die Quelldateien unter `basis/` stammen bytegleich aus dem [Modellordner auf Commit cd4d877](https://github.com/thomasmgfeller/x6-spectral-astrolabium/tree/cd4d877e2b592bd01ab983abfefd0578ca71acad/research/rax_cqg/dust_collapse/n15_massenquelle_v0_1). Die drei Python-Dateien liegen dort unter `basis/synchronisiert/`. Der publizierte Katalog friert die 61 Typen ein. Die vier lokalen Prüfpläne dokumentieren die Reihenfolge der explorativen Ergänzungen. Die Hashes prüfen die Dateiidentität. Eine öffentliche Präregistrierung dieser Folgestudie liegt nicht vor.
