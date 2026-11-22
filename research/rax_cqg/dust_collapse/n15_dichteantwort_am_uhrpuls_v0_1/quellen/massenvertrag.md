# Welche Massen erfasst die Auslese mit zwei inneren Uhren?

CST-DUST · N15-Typ 2097151 · 22. November 2026 · Anschluss an [PR #355](https://github.com/thomasmgfeller/x6-spectral-astrolabium/pull/355)

Die bei Masse 1/4 und Dichtezentrum 1/8 einmal geeichte Auslese rekonstruiert die zurückgehaltene markierte Masse 1 mit 0,999855920 und 0,999812474 an den beiden Dichtezentren. Alle acht vorab festgelegten Kombinationen aus vier neuen positiven Massen und zwei Dichtezentren liegen numerisch innerhalb des Zwei-Prozent-Ziels. Nahe null erreicht dieselbe Eichung eine Auflösungsgrenze. Der Unterschied zwischen einer exakt leeren Präparation und dem normierten Grenzwert eines immer dünneren positiven Dichtefensters wurde durch Intervallrechnung eingeschlossen.

## Versuchsaufbau

Ordnung, die zwei kohärenten äusseren Uhrfenster, die frühen mittleren Dichten 1/8 und 1/4, die sieben inneren Uhrfenster, Dichtejitter ±1 %, Referenzpaarung, alle 15 Phaseneinstellungen und der Quellschritt h=1/8 stammen aus PR #355. Die Quellen setzen zwei innere Uhren an den Ereignissen 11 und 13 und zwei äussere Profile voraus. Der Decoder auslese.py liest ausschliesslich die 15 komplexen Amplituden. Der bekannte Zukunftskragen liefert die Referenzphase C/D mit C=−7/8 beim positiven Kragen und C=0 im vollständigen Vakuum. D wird vor den Verschiebungen abgelesen.

Das untere Eichereignis ist das leere Innere mit ursprünglichem positivem Kragen am Zentrum 1/8. Der Positivstandard ist die markierte Masse 1/4 am selben Zentrum. Vor dem Rechnen der weiteren Massen wurden die nach zwölf Nachkommastellen eingefrorenen Konstanten b=−0,000007859456 und g=0,999919967308 archiviert. Die Auslese ist g(Y−b). Der numerische Kalibrierlauf führt beim Nullatom zu einer Rundungsabweichung von wenigen Billionsteln. Die Prüfsumme von eichung.json steht in eichung.sha256, der ursprüngliche Plan liegt in pruefplan.txt. Die Festschreibung war lokal. Eine externe Verblindung erfolgte nicht. Die markierte Masse dient als Referenzmodellgrösse. Eine unabhängig gemessene positive Ruhemasse wäre ein weiterer physikalischer Eingang.

## Transfer an beiden Dichtezentren

| Markierte Masse | Kalibriert bei Zentrum 1/8 | Relativer Fehler | Kalibriert bei Zentrum 1/4 | Relativer Fehler |
|---|---:|---:|---:|---:|
| 1/64 | 0,015625706 | +0,00452 % | 0,015621826 | −0,02031 % |
| 1/8 | 0,125004334 | +0,00347 % | 0,125019886 | +0,01591 % |
| 1/2 | 0,499969249 | −0,00615 % | 0,500006121 | +0,00122 % |
| 1 | 0,999855920 | −0,01441 % | 0,999812474 | −0,01875 % |

Die grösste beobachtete absolute relative Abweichung dieser acht Rechnungen ist rund 0,02031 %. Der Standard 1/4 beim zweiten Zentrum ist ein zusätzlicher Transfer. Er liefert 0,250030445. Masse 4 war aus PR #355 bekannt und dient ausschliesslich als Rückwärtsvergleich. Die ursprünglichen Rohwerte 4,002411146 und 3,999285607 werden reproduziert. Alle Rohwerte, Modulbeträge und die 15 komplexen Amplituden des feinsten Gitters stehen in transfer.json. Normiert wird auf das jeweilige positive Rohmass vor Einsetzen der Wirkungsphase.

Die numerischen Gitter verwenden 3, 4 und 5 Gauss-Punkte je innerer Uhr und 4, 8 und 10 Punkte je äusserem Fenster. Die sieben inneren Jitter und die kollektive Eingangsdichte werden analytisch integriert. Die unabhängige Gegenrechnung verwendet volle Clenshaw-Curtis-Gitter, zählt Intervalllängen in der Gesamtordnung neu und gruppiert die Phasendifferenzen unmittelbar. Bei Masse 1 und 1/64 an beiden Zentren weicht sie um höchstens 2,1×10⁻⁸ Masseneinheiten von der feinsten Gauss-Rechnung ab. Das prüft die Reproduzierbarkeit. Ein validiertes Gesamtfehlerintervall für diese positiven Massenschätzungen steht aus.

## Drei Nullkontrollen

Die folgenden Werte für die Rohablesung Y sind nach aussen gerundete **absolute** Intervalle in Einheiten von 10⁻⁶ markierter Masse. Sie folgen aus nachprüfbarer Intervallarithmetik.

| Präparation | Dichtezentrum 1/8 | Dichtezentrum 1/4 |
|---|---:|---:|
| Alle 15 Dichten null | exakt 0 | exakt 0 |
| Sieben innere Dichten am Nullatom, ursprünglicher positiver Kragen | [−7,859460 bis −7,859458] | [−14,780049 bis −14,780047] |
| Normierter Grenzwert positiver Schläuche bei M→0⁺, ursprünglicher positiver Kragen | [−8,291788 bis −8,291787] | [−15,436358 bis −15,436357] |

Im vollständigen Vakuum ist auch der Kragen leer. Die beiden Spalten bezeichnen dort dieselbe Kontrolle. Seine Rohantwort ist exakt null. Nach Anwenden der am positiven Kragen bestimmten Eichung beträgt seine Anzeige rund +7,85883×10⁻⁶. Auf jeder einzelnen leeren Feldgeschichte gilt die feine Dichteidentität auch bei positivem Kragen exakt. Die von null verschiedene Randantwort entsteht beim kohärenten Integrieren der Amplituden vor der Phasenauslese.

Der Ursprung des Unterschieds zwischen den letzten beiden Zeilen ist im Modell bestimmbar. Beim Konditionieren auf sieben Dichteatome gewichtet das ursprüngliche Uhrmass mit D⁷. Auf dem kontinuierlichen positiven Schlauch erzeugen die sieben Dichteintegrationen einen weiteren Faktor D⁷∏fⱼ. Nach Normierung bleibt dieser Faktor auch im Grenzübergang M→0⁺ erhalten. Das gemeinsame Skalar- und Geometriegewicht eines festen Typs wird wie in PR #355 ausgeklammert. [Herleitung und Fehlernachweis](BEWEIS.md)

## Was die Auflösung begrenzt

Die beiden kalibrierten Limeswerte liegen nahe −4,3230×10⁻⁷ und −7,5763×10⁻⁶. Sie sind beide streng negativ. Eine beliebige andere gemeinsame Nullpunktwahl kann die voneinander getrennten Rohgrenzwerte ebenfalls nicht gleichzeitig auf null setzen. Bei fester von null verschiedener Verstärkung ist eine uniforme relative Zwei-Prozent-Garantie für beide Zentren bis zu beliebig kleinen positiven Massen ausgeschlossen.

Die ergänzende, explorative Prüfung benutzt ohne Neueichung M=2⁻ᵏ für alle k von 6 bis 20. Bei Zentrum 1/8 liegt die Abweichung der kalibrierten Auslese bei k=15 bei −1,41 %, bei k=16 bei −2,83 %. Bei Zentrum 1/4 lauten die benachbarten Werte −1,52 % bei k=11 und −3,07 % bei k=12. In beiden Fällen verfehlen auch alle kleineren untersuchten Rastermassen das Ziel. Die Aussage betrifft die abgetasteten Punkte. Eine validierte exakte Übergangsmasse zwischen ihnen ist offen. Ein zusätzlicher, bewusst konservativer Beweis schliesst sogar eine positive kalibrierte Anzeige für alle 0<M≤2⁻⁴⁶ bzw. 0<M≤2⁻⁴² aus.

Bei h=1/8 ist die Summe der absoluten Phasenkoeffizienten G=679816/9. Bei fest vorgegebenen Eichwerten pflanzt sich ein Phasenfehler von höchstens δ je Einstellung mit höchstens |g|Gδ in die Anzeige fort. Werden Zielwert, Nullwert und Standard jeweils getrennt mit Phasenfehlern gemessen, bezeichne d den roh abgelesenen Abstand des Standards vom Nullwert und η=Gδ. Für d>2η ist die zusätzliche absolute Abweichung vor Rundung der Parameter höchstens 2η(1/4+|M_kal|)/(d−2η). Der Beweis folgt durch Einsetzen der drei Fehler in den Quotienten (1/4)(Y−b)/d. Am numerischen Transfer M=1, Zentrum 1/8, genügen im Modell höchstens 2,5×10⁻⁸ rad je Phase bei drei betroffenen Ablesungen bzw. 2,6×10⁻⁷ rad bei fest bekannten Eichwerten (genaue Grenzwerte in grenzen.json). Die Abschätzung ist ein rechnerisches Fehlerbudget. Die physikalisch erreichbare Phasengenauigkeit wurde nicht gemessen.

## Offline reproduzieren

Python 3.10 oder neuer genügt für die exakten Tests. Die vollständige numerische Rechnung verwendet zusätzlich NumPy, geprüft mit 2.3.5. Im entpackten Verzeichnis laufen die Befehle

    python3 -B pruefen.py --nur-exakt
    OPENBLAS_NUM_THREADS=1 python3 -B pruefen.py

Der erste Befehl kontrolliert die Dateien, wiederholt die exakten Vorläufertests aus PR #355, isoliert die Knoten der 80-Punkt-Regel, reproduziert die beiden Vakuumsektoren und die rigorosen Ausschlussbereiche. Der vollständige Lauf berechnet zusätzlich Eichpunkte, zurückgehaltene Massen, das Auflösungsraster und die unabhängige Gegenprobe neu. Für die zertifizierten Nullwerte sind die rationalen Intervalle in nullgrenze.json massgeblich. Abweichungen im letzten Bereich der Gleitkommaausgabe können bei der Phasendifferenzbildung auftreten.

Alle 60 archivierten physischen P3-Prüfpunkte stehen auf NOT_RUN. Der Test belegt einen Transfer der markierten Referenz und eine sektorspezifische Auflösungsgrenze im endlichen Modell. Unabhängiger Ruhemasse-Standard, physikalischer Zugang zu den relationalen Uhren und gemeinsame dynamische Präparation bleiben offen. [Geprüfter Git-Stand](https://github.com/thomasmgfeller/x6-spectral-astrolabium/tree/82f744cda050235fc9cf6df4f20daf0f0449f2e8/research/rax_cqg/dust_collapse)
