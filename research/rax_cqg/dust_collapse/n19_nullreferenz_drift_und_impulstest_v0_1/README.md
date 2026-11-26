# N19 · Gespeicherte Nullreferenz, verbleibende Fehlpulse und Impulseichung

**26. November 2026.** Wer an beiden Lesestellen zusätzlich die vor dem Puls gespeicherte Anfangsanzeige derselben Spur kennt, kann eine anfängliche Ortsverschiebung von einer Quellenantwort trennen. In der diskreten Gegenverteilung der Vorgängerstudie beseitigt das auf dem stärkeren Gerät alle Fehlklassifikationen. Beim schwächeren Gerät bleiben Fehler durch die Impulsausläufer. Zusätzlich zeigt eine synthetische Eichreihe, wie ein quadratischer zeitlicher Untergrund die Entscheidung zur Wirkungsskala umkehren kann. Das Paket enthält einen dafür korrigierten Auswerter und einen direkten Test des Impulses **nach** der Aufnahme der Anfangsanzeige. [Veröffentlichter Ausgangsstand, PR 392](https://github.com/thomasmgfeller/x6-spectral-astrolabium/pull/392)

## Eine zusätzliche Anzeige pro Spur

Für jedes vorbereitete Tripel registriert der modellierte Leser am Ereignis 0 die Anfangspositionen der drei Zeiger mit einer Schrittweite von 2·10⁻¹². Zu jeder Ziffer gehören Spur und Versuch. Die Ziffern werden auf kausal erlaubten Wegen an 18 und später an 7 verfügbar gemacht. Am Empfänger genügen die ersten beiden, am Speicher werden alle drei gebraucht. Die Anfangsziffer kann bei |q|≤1 über 10¹² verschiedene Werte annehmen und benötigt dafür bis zu 40 Bit je Spur. Die verlustfreie Übertragung und die Zuordnung zum selben Versuch sind zusätzliche Eigenschaften des Geräts. Die native Staubwirkung implementiert keinen solchen Digitalspeicher.

Der Leser subtrahiert von jeder gerundeten Endanzeige die zugehörige gerundete Anfangsanzeige. Im Modell ist X_j=q+Signal_j+A_j p/κ. Die Differenz enthält Signal_j+A_j p/κ, die beiden Rundungsfehler und einen möglichen analogen Fehler der Anfangsreferenz. Der Empfänger liest seine lokale Staubuhr unmittelbar. Am Speicher wird die Empfangsuhr aus der dortigen Staubuhr und der korrigierten dritten Spur rekonstruiert. Der Klassifikator für die drei möglichen Pulsstärken ist der veröffentlichte Leser aus PR 391. Eine andere Versuchskennung oder eine fehlende bzw. gesättigte notwendige Anzeige ergibt keine Entscheidung. Eine falsch beschriftete, plausibel aussehende Ziffer kann weiterhin einen Fehlpuls auslösen.

Die acht Vergleichsfälle mit ausgeschalteter Quelle und Anfangsverschiebung ±64·10⁻¹², die bei PR 392 einen Puls vortäuschten, ergeben so an **beiden Orten null**. Wir haben zusätzlich die gesamte Dreipunktverteilung mit unabhängigen standardisierten Koordinaten aus {−64,0,64} ausgewertet, mit den ursprünglichen rationalen Wahrscheinlichkeiten für jedes der 729 Atome. Die nachgewiesene Translationskovarianz der Rundung um ganze Rasterschritte reduziert die neue Rechnung auf 27 Impulstripel pro Familie. Bei allen berücksichtigten Verschiebungen bleiben die Anzeigen innerhalb ihres Messbereichs. Die Geräteparameter in dieser diskreten Auswertung sind nominal, die Referenzabbildung ist ideal.

| Gerät | Geprüfte Familien | Wahrscheinlichkeitsbereich für eine falsche Quellwahl an mindestens einem der beiden Orte |
|---|---:|---:|
| Stärkere Trägheit κ=1, mit Ortsreferenz | 72 | exakt 0 für diese endliche Verteilung |
| Schwächere Trägheit κ=10⁻¹¹, mit Ortsreferenz | 72 | 0,00271264 % bis 0,00813780 % |
| Beide Geräte, ursprünglicher Leser, nur Referenzhintergrund | 12 | 0,00542513 % bis 0,01356260 % |

Auf den zwölf direkt paarweise verglichenen Referenzfamilien ist die Fehlerwahrscheinlichkeit mit Ortsreferenz jedes Mal kleiner. Alle diskreten Entscheidungen waren eindeutig. In jeder Zeile von `Volltest.json` stehen die exakten Brüche. Die zwölf Hintergründe, drei Quellstärken und zwei Transportwege sind diskrete geprüfte Modellbedingungen. Die Fehlerquoten charakterisieren nur die gewählte endliche Eingangsverteilung.

## Uniforme Grenze ohne Verteilungsannahme

Eine zweite Rechnung lässt alle Anfangsorte |q|≤1, alle Vorzeichen der drei Impulse und die in PR 391 spezifizierten Abgleichfehler zu. Für den nach der Ortsaufnahme vorliegenden halben kanonischen Impuls p=P/2 prüfen wir |p|≤m·10⁻²⁵, jeweils unabhängig pro Spur. Vor jeder Auslese begrenzt der stationäre N19-Löser den Lastbeitrag zur Staubgleichung für das ganze Impulsintervall. Für den Entscheidungsabstand berechnen wir die endliche Änderung des Quellenresiduums mit einer exakten Sekantenformel. Sie erhält den gemeinsamen Zeitfehler der drei gelesenen Uhren. Ein positiver Abstand an beiden Orten zertifiziert die Familie.

| Impulsgrenze m | Zertifiziert von 144 Familien, zusätzliche analoge Abweichung der Anfangsreferenz ≤10⁻¹² |
|---:|---:|
| 1/2 | 144 |
| 1 | 144 |
| 2 | 138 |
| 3 | 132 |

Bei m=1 sind damit auch Positionen von der Grössenordnung einer ganzen Modelleinheit zugelassen, während die entscheidende Anzeige auf einem Raster von 2·10⁻¹² liegt. Die kleinste positive Residuenreserve beträgt rund 7,64·10⁻¹¹ in Modelleinheiten des Residuums. Für die sechs offenen Familien bei m=2 liefert die Abschätzung keine Entscheidung. Die Rückwirkung beim Anlegen der Referenz geht als Bestandteil des **verbleibenden** Impulses in die Voraussetzung ein. Spätere zusätzliche Kräfte, fehlerhafte Ziffernübertragung und Messrückwirkung am zweiten Leseort sind durch diesen Satz nicht abgedeckt.

## Wie sich die Schwellenentscheidung der Impulseichung umkehren kann

Im synthetischen Gegenversuch ist S₀=2 350 J·s fest vorgegeben. Bei beiden Impulsstärken und beiden Trägheiten kommt ein über den jeweiligen Block quadratisch driftender Untergrund hinzu. Seine Krümmung hängt von der gewählten Stärke ab. Die unabhängige Massenreferenz ist korrekt, hat aber 3 % Unsicherheit. Die ersten vier Polaritäten bilden den veröffentlichten + − − +-Block. Er besteht die damaligen Kontrollen und meldet **2 396,32 bis 2 403,68 J·s**. Das liegt auf der falschen Seite der für die frühere Gaußpräparation berechneten Schwelle von 2 372,79 J·s. Dieses Beispiel realisiert die bereits in PR 392 dokumentierte Einschränkung des Viererblocks. Die Beseitigung linearer Drift durch Viererkontraste ist auch in der Vergleichsmetrologie gebräuchlich. [NIST, Drift bei Kalibriermessungen](https://itl.nist.gov/div898/handbook/mpc/section3/mpc3312.htm)

Die neue Folge + − − + − + + − hat bei gleichen Zeitabständen die vorzeichenbehafteten Zeitmomente 0, 0, 0, −48 für die Grade 0 bis 3. Der Auswerter benutzt die einzelnen Zeitstempel und lässt je Block ein eigenes unbekanntes quadratisches Polynom zu. Aus jeder der 70 Viererauswahlen werden mit dividierten Differenzen notwendige Bedingungen für den positiven Gewinn gebildet. Für die beiden Enden des resultierenden Gewinnintervalls konstruiert der Code ein konkretes gemeinsames Hintergrundpolynom, das alle acht Rohablesungen zulassen. Die dazwischenliegenden Gewinne sind durch Konvexität zulässig. Die zweite Impulsstärke bleibt zurückgehalten. Die Nullkontrolle prüft mit derselben Zeitbasis den zugelassenen Hintergrund und die Auflösung.

Der Achtfachblock liefert im selben Beispiel **2 346,40 bis 2 353,60 J·s**, einschliesslich des wahren Werts. Eine zusätzliche Rechnung mit ungleichmässigen, genau angegebenen Zeitstempeln besteht ebenfalls. Wirksame Zeitstempelunsicherheit und unbeobachtete Beiträge ausserhalb des quadratischen Modells sind durch unabhängige Fehlergrenzen abzudecken. Eine Störkraft, die proportional zum Eichimpuls ist, lässt sich aus dessen Positionsantwort allein auch bei acht Polaritäten nicht identifizieren. Mit einer entsprechend breiten unabhängigen Fehlergrenze verweigert das Programm im getesteten Beispiel die Schwellenentscheidung.

## Eine direkte Prüfung des Impulses nach der Ortsaufnahme

Ein separat verbrauchtes Dreierensemble durchläuft zuerst die normale Ortsaufnahme. Danach wird je Spur ein Impulsleser angeschlossen, dessen Positionsausgang ideal Z=ΓB·p/(κ₀V)+c q+z₀ ist, mit B=10⁻¹², κ₀V=10⁻²⁵. Ein klassischer linearer kanonischer Austausch von Position und Impuls liefert eine mögliche Modellabbildung. Die Geräte müssen bei der Prüfung dieselbe Präparation, Kopplung und Ortsregistrierung wie im Normalbetrieb erfahren. Drei über den ganzen beanspruchten Bereich unabhängig geeichte Kanäle sind Voraussetzung.

Die Eichung setzt Γ=32 innerhalb ±1 %, |c|≤10⁻¹², einen Ausgangsnullpunktfehler ≤B/4 und einen zusätzlichen analogen Kopierfehler ≤B voraus. Der kleine Koeffizient c ist wegen der nun zugelassenen breiten Anfangsorte wichtig. Beim gleichen SI-Impulsstandard und derselben schwachen Kragenantwort G folgt Γ=βV/(BμG), wobei β die Ausgangsantwort auf einen externen SI-Impuls ist. Die Position wird getrennt variiert, um c zu begrenzen. Ein endlicher Referenzhub allein schliesst verborgene Nichtlinearitäten oder Übersteuerung für unbekannte Eingaben nicht aus. Die reale Gerätezuordnung, der Gültigkeitsbereich der Abbildung und die Erkennung von Sättigung bleiben messtechnisch nachzuweisen.

Für jede Spur begrenzen die gespeicherte Anfangsziffer und die neue Impulsanzeige zuerst |q|, dann |p|. Fehlende oder unklare Daten und Überschreitung eines der Grenzwerte zählen als Auffälligkeit. Bei unabhängigen identisch verteilten Dreierpräparationen genügen **59 vorab festgelegte, vollständig unauffällige Versuche** für die Aussage „mindestens 95 % liegen im zertifizierten Bereich“ mit einseitig 95 % Konfidenz. Es gilt 0,95⁵⁹ ≤ 0,05 < 0,95⁵⁸. Bei vorab zugelassener einzelner Auffälligkeit beträgt die Mindestzahl 93. Der frühere Zweistellungstest benötigte für seine andere Zielmenge 119 unauffällige Versuche. Die neue Stichprobenrechnung setzt einen unabhängig kalibrierten Leser für den Nachimpuls und die zusätzliche Anfangsreferenz voraus. Die beigefügten 59 Datensätze sind synthetische Positivkontrollen. [NIST, einseitige exakte Binomialgrenzen](https://itl.nist.gov/div898/software/dataplot/refman2/auxillar/exacbino.htm)

Für die Eingangskopie selbst zeigt ein einfaches kanonisches Modell die Rückwirkung. Bei Verstärkung g und separatem Register (r,π) lautet die Abbildung (q,P,r,π) → (q,P−gπ,r+gq,π). Der Ortsfehler des Registers ist r/g, der Impulsstoss −gπ. Bei kanonischer Quantisierung gilt für deren RMS-Breiten σ(r/g)·σ(gπ)≥ℏ/(2S₀). Teilt man der Aufnahme eine analoge RMS-Ortsbreite von 10⁻¹² und höchstens die Hälfte des kanonischen Impulsbudgets von 2·10⁻²⁵ zu, ergibt sich als notwendige Bedingung S₀≥527,29 J·s. Diese Zahl gilt für die gewählte RMS-Aufteilung am Kopierregister. Ein RMS-Budget allein garantiert keine harte Intervallschranke und keine Erfolgswahrscheinlichkeit am nichtlinearen Staubleser. Die frühere Schwelle von 2 372,79 J·s bezieht sich auf die konkret festgelegte Gaußkovarianz des Eingangszeigers. [Kanonische Quantenzeiger und Kovarianzen](https://arxiv.org/abs/1110.3234)

## Datenstand und Reproduktion

Alle Rechnungen sind mit Python ab 3.10 und der Standardbibliothek offline wiederholbar. Die drei Prüfpläne tragen lokale SHA-256-Prüfsummen und wurden jeweils vor der zugehörigen Rechnung festgehalten. Das Vorgängerpaket ist unter seiner publizierten Prüfsumme eingebettet.

    python3 -B pruefen.py
    python3 -B drifteichung.py Synthetische_Eichreihe.json
    python3 -B impulstest.py Synthetische_Eichreihe.json Synthetische_Impulsproben.json
    python3 -B impulstest.py Messstand.json Messstand.json

`pruefen.py` reproduziert den Vorgängerstand und vergleicht alle sechs neuen JSON-Ergebnisse und Eingabebeispiele bytegenau. Für reale Daten zeigen die beiden synthetischen Eingaben das vollständige Format. Dezimalzahlen und Brüche werden als Strings, geschlossene Intervalle als Paare und digitale Codes als ganze Zahlen gespeichert. Je Eichlauf umfasst das Zusatzfeld `nonquadratic_error_q` auch den maximalen Rest aus Synchronisation und bekannten nichtquadratischen Beiträgen. Die Herkunftskennung `measurement_records` braucht zugehörige externe Referenzen. Die Software kann Nachweise für reale Geräte nicht beglaubigen.

Der nächste physische Schritt ist die Messung von Ortsübertrag, Kopierrückwirkung und Impulsantwort am selben Speicher. Die N19-Daten dieses Pakets enthalten keine solche Messreihe. **Alle 60 physischen P3-Prüfpunkte stehen auf NOT_RUN.**
