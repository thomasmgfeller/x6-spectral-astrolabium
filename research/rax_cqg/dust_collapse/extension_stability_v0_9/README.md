# CST-DUST · N15-Stabilität bei fünf Prozent

[Bericht (PDF)](../reports/CST_DUST_N15_Fuenf_Prozent_v0_9.pdf) · [Offline-Prüfpaket (ZIP)](../packages/CST_DUST_N15_Fuenf_Prozent_v0_9_Pruefpaket.zip) · [Typenlisten und Zertifikate](planes.json)

Etappe 1 · v0.9 · 19. November 2026. Die Studie schliesst an [PR #313](https://github.com/thomasmgfeller/x6-spectral-astrolabium/pull/313) an. Die Studie verwendet das [unveränderte v0.8-Prüfpaket](../packages/CST_DUST_N15_Uhrantworten_v0_8_Pruefpaket.zip). Im Offline-Paket trägt es den Namen `input_v08.zip`. Der SHA-256-Wert lautet `52ac3f60c7acf3fde998f45b4bd6cdac9b0723de08e7d050379bdb46a794bcc4`.

## Befund

Beide N11-Eltern starten mit Amplitudengewicht ½ und übertragen jeweils denselben Anteil λ. Jede darf ihre eigene nichtnegative Verteilung auf erreichbare Nachkommen wählen. Für die Anfangsdichten 1/8 und 1/4 gelten dieselben Gewichte. Alle Angaben gelten für jeden Transfer von null bis zum genannten Wert und für beide Referenzgitter (32,6) und (48,8).

| Zulässige Verteilung | Gesicherter Transfer λ |
| --- | ---: |
| Alle 1 217 Zustände, freie Mischung (v0.8) | 4,4357 % |
| Alle 1 217 Zustände, freie Mischung (v0.9) | 4,6904 % |
| Alle zulässigen Mischungen auf dem ausgewiesenen Träger mit 1 098 Zuständen | 5,0000 % |
| Bis zu 0,0685 % des übertragenen Gewichts auf die 119 übrigen Typen | 5,0000 % |
| Bis zu 5,7642 % des übertragenen Gewichts ausserhalb eines engeren Trägers aus 1 022 Zuständen | 5,0000 % |

Die beiden letzten Zeilen beschreiben getrennte hinreichende Bedingungen. Der engere Träger enthält den früheren 196-dimensionalen Pilotträger. Beide Trägerangaben zählen die zwei Ausgangszustände mit. Die 119 bzw. 195 übrigen Typen sind vollständig in `planes.json` aufgeführt. Bei λ = 5 % entspricht die zweite Aussengrenze 0,28821 % des gesamten anfänglichen Amplitudengewichts. Sie erlaubt eine beliebige Aufteilung dieses Anteils unter den 195 Typen im Rahmen der ursprünglichen Erreichbarkeit. In jeder Zeile bestehen die relative Niveauabweichung (höchstens 10 %), die relative Änderung des vierteiligen Dichtekontrasts (höchstens 25 %) und das negative Vorzeichen der Erfolgsdifferenz.

Für freie Mischungen aller 1 217 Zustände bei genau 5 % bleiben Dichtekontrast und Vorzeichen gesichert. Die Schranke für die maximale relative Niveauabweichung bei Dichte 1/4 beträgt 10,6417 % (aufgerundet). Die tatsächliche Existenz einer Verletzung bei 5 % bleibt offen. Das vorhandene Gegenbeispiel bei 5,0211 % ist weiterhin zulässig. Mit dem Zertifikat aus v0.8 beträgt der gesicherte Transfer auf den ursprünglichen 196 Zuständen 5,0210 %.

## Vier zusätzliche komplexe Uhrantworten

Die ersten vier Typen der publizierten Rangliste aus v0.8 sind auf beiden Gittern und bei beiden Eltern dieselben. Es sind 339773, 524287, 45885 und 45851. Die Rechnung übernimmt alle sieben inneren Uhren, beide Randloben, die gravitative Phase, den Detektor und den Prüfradius 10⁻⁷. Die direkten N15-Uhrantworten steigen von 27 auf 31.

- Bei 339773 wird der Dichtefaktor der Uhr 13 als H(C) = [1 + ∫₀¹ exp(−iuC/2) du]/2 geschrieben. Bei festem u und fester Uhr 13 zerfällt die Summe über die beiden Zweige bei Uhr 4 in zwei unabhängige Kontraktionen. Die Hilfsintegration verwendet 86 Gauss-Knoten. Es gilt |C| < 208. Für festes reelles C ist das Taylorrestglied um u = ½ bis Grad 171 durch (|C|/4)¹⁷²/172! begrenzt. Positive normierte Gaussgewichte, Exaktheit für Polynome bis Grad 171 und der Faktor ½ ergeben eine obere Schranke von 6,66 × 10⁻¹⁷ für den Fehler in H. Diese Schranke betrifft allein die zusätzliche Hilfsquadratur.
- Bei 524287 werden zuerst die Uhren 13 und 14 über ihre jeweiligen vier Vorgänger bedingt summiert. Dann wird Uhr 12 mit der ersten bedingten Summe integriert und mit der zweiten multipliziert. Die letzten vier Uhren werden mit der vorhandenen C99-Routine kontrahiert. Die grössten Zwischentabellen haben vier Uhrenachsen.
- Für 45885 und 45851 verwendet die Studie die geerbte Vier-Eltern-Kontraktion. Für alle vier Typen liegen Ergebnisse auf (32,6), (48,8) und (64,10) vor. Die direkten siebenfachen Kontrollsummen auf (4,3) und (5,4) verwenden ein separates Rechenverfahren. Auf (5,4) liegt die grösste Abweichung unter 1,6 × 10⁻¹⁷.
- Wenn beide Eltern ihre gesamten jeweiligen 5 % auf denselben der vier neuen Typen übertragen, beträgt die direkt berechnete relative Niveauabweichung auf beiden Referenzgittern und bei beiden Dichten zusammen 9,4229 % bis 9,8174 % (gerundet). Die drei ursprünglichen Tests bestehen in allen vier Fällen.

## Wie der Nachweis bei 5 % funktioniert

Die sieben nichtleeren Teilsummen der drei akzeptierten Ausgänge kontrollieren die Totalvariation der vier Ausgänge einschliesslich Misserfolg. Beim Transfer von null bis 5 % beträgt die relative Niveauschranke für die sechs echten Teilmengen und die positive Änderung des Gesamterfolgs höchstens 7,5269 %. Die Änderung des Dichtekontrasts bleibt für den gesamten Träger unter 17,851 %. Die einzige verbleibende Prüfung betrifft die Untergrenze des Gesamterfolgs.

Sei S die Summe der drei positiven Effekte, b der jeweilige N11-Referenzzustand, p = ⟨b,Sb⟩ und x = (1−λ)b + λv. Aus der Positivität von S folgt für jeden festen Testvektor q die Ungleichung

    ⟨x,Sx⟩ ≥ 2 Re⟨q,Sx⟩ − ⟨q,Sq⟩.

Für q werden die in der N14-Studie eingefrorenen 5-%-Testvektoren verwendet. Sie bestehen aus den beiden Eltern und den drei Zuständen N14_734, N14_760 und N14_8191. Die jeweiligen drei Nachkommengewichte lauten (202741, 693388, 103871) bzw. (201682, 691688, 106630) in Millionsteln. Die Wahl von q ändert die physikalische Präparation nicht.

Für alle 1 048 N15-Endtypen wurden die skalaren Überlappungen mit diesen drei N14-Zuständen aus den Gaußkernen bei 70 Dezimalstellen berechnet. Je Paar speichert die Studie drei Detektorintervalle. An den bereits vorhandenen N15-Zuständen wurde die Übereinstimmung mit den gespeicherten Gram-Matrizen geprüft. Für jede gerundete Effekttabelle testet eine rationale LDL*-Zerlegung den gemeinsamen positiven 5×5-Block und den Schurrest jeder zusätzlichen Spalte. Diese Daten erlauben positive Vervollständigungen. Die Stützebene gilt für jede damit verträgliche positive Vervollständigung.

Für jeden Zustand j berechnet der Prüfer eine rationale untere Schranke hⱼ für Re⟨q,Sψⱼ⟩. Bei bekannten Uhren zieht er den Projektionsbetrag mal Uhrradius ab. Bei unbekannten Uhren verwendet er die gesamte komplexe Betragsscheibe. Mit T = 1/20, z = Re⟨q,Sb⟩ und Q = ⟨q,Sq⟩ ist

    h* = [0,9p + Q − 2(1−T)z] / (2T)

die ausreichende Untergrenze am rechten Endpunkt. Am linken Ende prüft das Programm 2z−Q > 0,9p. Affinität der unteren Schranke in λ deckt das ganze Intervall ab. Für den 1 098er-Träger muss jeder erreichbare Typ hⱼ ≥ h* für beide Dichten und Gitter erfüllen. Der engere 1 022er-Träger behält nur Typen, die für jede erreichbare Elternhistorie deren bisheriges Minimum auf dem 196er-Pilotträger erhalten.

Für einen zugelassenen Aussengewichtsanteil setzt man aᵣ und bᵣ gleich den kleinsten unteren Projektionen unter den erreichbaren Typen innerhalb bzw. ausserhalb des betreffenden Trägers. Ist der Mittelwert der beiden elternspezifischen Aussenanteile höchstens δ, so ist die untere Projektion mindestens

    (a₀ + a₁)/2 − δ · max(0, a₀−b₀, a₁−b₁).

Die veröffentlichten Prozentwerte wurden auf ein Millionstel der jeweiligen Gewichtsfraktion abgerundet. Eine zweite Implementierung löst für beide Eltern gemeinsam ein lineares Programm. Sie rekonstruiert die Projektionen mit NumPy und prüft sie gegen die rationalen Schranken. Auf dem 1 098er-Träger liegt der schlechteste untere Gesamterfolg bei 90,000454 % der Referenz. Unter Einbezug des ausgewiesenen Aussenanteils ist der verbleibende Abstand zur 90-%-Toleranz klein. Die rationale Rechnung entscheidet die Grenzfälle.

## Nachrechnung und Reichweite

Im Studienordner und im entpackten Offline-Paket lassen sich die Rechnungen reproduzieren. Mit Python 3.12, NumPy 2.3.5, SciPy 1.17, SymPy 1.14, mpmath 1.3 und C99-Compiler lassen sich die Zertifikate so prüfen.

```sh
OPENBLAS_NUM_THREADS=1 python3 -B verify.py
OPENBLAS_NUM_THREADS=1 python3 -B verify.py --rebuild
```

Der erste Aufruf kontrolliert Prüfsummen, vier unabhängige kartesische Vergleichsrechnungen, direkte Detektortests, sieben Teilsummenschranken, Schurreste und Mischungszertifikate. Der zweite rekonstruiert zusätzlich die vier neuen Uhren auf allen drei Gittern und sämtliche 3 144 skalaren Überlappungen. Die Eingabe `input_v08.zip` wird lokal entpackt. Der Cache ist reproduzierbar. `bounds.json` enthält die unbedingte Vollträgerschranke und die nächsten Projektionskandidaten. `planes.json` enthält beide Typenlisten und die exakten rationalen Schwellen. `mixcheck.json` enthält die unabhängigen LP-Ergebnisse.

Alle Aussagen betreffen die endliche Historienfamilie und die vorgegebenen numerischen Eingangstabellen, Hüllen und Radien. Eine vollständige Fehlerfortpflanzung vom kontinuierlichen Uhrintegral bleibt offen. Für ein physikalisches Historienmass oder einen Bounce folgt aus diesen Rechnungen keine Entscheidung. In beiden unbedingten Rechnungen liefert N15_356087 jetzt die schwächste untere Projektion bei Dichte 1/4 auf beiden Gittern.
