# Früher Radiuspilot · Ladung bei festem Zukunftsrand

**Der leichte Ladungssektor Q*/16 ist auf der geprüften N22-Ordnung bei unveränderten späten Feldern ausgeschlossen.** Die Dichtegleichung am besetzten Ereignis 13 und die Ladungsbilanz verlangen dafür unvereinbare Uhrzeiten. Werden nur die vier späten Randgewichte herabgesetzt und die freien Felder entsprechend gelöst, entstehen zwei leichte Modellpräparationen, die beide Massendiagnosen innerhalb von 2 % treffen und im frühen Fenster materiell-leere Kontakte behalten. Die physische Eichung und Flächenmessung bleiben offen. [Ausgangsstudie auf GitHub, PR 411](https://github.com/thomasmgfeller/x6-spectral-astrolabium/pull/411)

## Was wird verändert?

Die Kausalordnung ist 216141/229383/0/+. Der Gerätequellterm und die drei Nachimpulse sind null. Die Referenzwerte der vier frühen und vier späten Feldpaare sind die rationalen Mittelpunkte aus dem veröffentlichten Nullquellenfall mit festen Y₁₀ und w₁₀. Gemeinsam bleiben zunächst alle vier frühen Gewichte, die Uhr Y₃ und die acht späten Werte an 7 bis 10. Variiert werden die Uhren an 0, 1 und 2. Die freien 14 Uhren und elf positiven Innengewichte werden stationär mitbestimmt. Drei innere Gewichte bleiben null. Die abgeleiteten einzelnen Randimpulse dürfen sich ändern.

Q = −Σ Gᵢ über i = 0,1,2,3 ist die signierte Wirkungsladung. Auf jeder stationären Lösung gilt auch Q = Σ Gⱼ über j = 7,8,9,10. B = Σ wᵢ/(Y₇−Y₃) über die elf positiven Innenereignisse ist das bedingte Massenmass der Verweildauerregel aus PR 411. Die zwei Auswertungen verwenden unterschiedliche Funktionen derselben Felder. Eine unabhängige physische Ruhemasse ist weiterhin offen. Als Referenzen gelten Q* = 0,181585581308965 und B* = 0,051689012322820. B* wurde aus dem publizierten Referenzzustand auf 15 Dezimalstellen gerundet.

## Ausschluss unabhängig vom numerischen Suchweg

Der Zukunftskragen ist gegenüber kausalen Nachfolgern abgeschlossen. Die Kanten innerhalb des Kragens heben sich in der Summe seiner Uhrimpulse auf. Für jede kreuzende Kante i→j mit j im Kragen ergibt sich der Term kᵢⱼ wⱼ (Yᵢ−Yⱼ). Bei festen späten Feldern hat Q deshalb die exakte Form C + Σ aᵢYᵢ. Die Koeffizienten, auch die verschwindenden Beiträge der frühen Uhren, werden direkt aus dem archivierten Kern berechnet. Das frühe Feld wirkt über die mitveränderten inneren Uhren.

1. Die 152 Kausalrelationen, die Geräteschranken und die festen Uhren geben lineare Ungleichungen. Eine nichtnegative rationale Kombination davon ergibt Q ≥ b − m(x₁₃−1/2), mit xⱼ = (Yⱼ−Y₃)/(Y₇−Y₃), b ≈ 0,01622066347 und m ≈ 0,13970016898. Jeder Multiplikator und jede Koeffizientensumme werden exakt geprüft. Für Q*/16 müsste x₁₃ > 0,53487 gelten. Dasselbe notwendige Seitenkriterium ergibt sich an 12.
2. Wegen w₁₃ > 0 ist seine Dichtegleichung stationär. Setze t = Y₁₃−Y₃ und dᵢ = Y₁₃−Yᵢ für i = 4,5,6. Die vier wirksamen eingehenden Koeffizienten sind −8,1,1,1. Aus 3 ≺ i ≺ 13 folgt 0 < dᵢ < t. Damit gilt 19 = 8t² − Σ dᵢ² > 5t² und x₁₃ < √(19/5)/(Y₇−Y₃) < 0,508529.
3. Einsetzen in die Ladungsschranke ergibt **Q > 0,01502924**. Das leichte Ziel liegt bei 0,01134910, auch sein 2-%-Band liegt vollständig darunter. Mit der Modellverstärkung 4/Q* liegen die Ladungsmassen oberhalb 0,33106. Auch verschwindende Ladung ist in diesem positiven Sektor ausgeschlossen. Der Nachweis gilt für jede zulässige stationäre Lösung unter den genannten Bedingungen. Der schwere Referenzwert und der Ladungsnullpunkt sind dabei ausdrücklich festgehalten.

Bei gemeinsamer Skalierung aller vier späten Gewichte um s > 0 skaliert die aus dem Zukunftskragen berechnete affine Form exakt um s. Die Dichtegrenze an 13 bleibt gültig. Für dieselben späten Uhren und das exakte leichte Ladungsziel muss deshalb s < 0,75514 sein. Das ist eine notwendige Bedingung. Die folgende Kontrolle benutzt s = 1/16. Andere Gewichtsverhältnisse, andere Ordnungen, ein unbesetztes Ereignis 13 oder ein physisch anders bestimmter Ladungsnullpunkt erfordern eigene Untersuchungen.

## Wie eindeutig ist Q als Massenablesung?

Alle vier Kombinationen der beiden Q-Ziele 1 und 0,95 in Einheiten von Q* mit den beiden B-Zielen 1 und 0,8 in Einheiten von B* besitzen stationäre Lösungen. Weitere zertifizierte Fälle haben bei exakt Q = Q* die beiden Werte B = B* und B = 0,65 B*. Der beste allein aus Q geschätzte gemeinsame Zahlenwert hat für dieses B-Paar einen maximalen relativen Fehler von mindestens 7/33, rund 21,21 %. Das ist ein Gegenbeispiel zur eindeutigen Übertragung einer Q-Eichung auf B bei freier Anfangsuhrpräparation. Es ist kein Fehlerwert eines physischen Massengeräts.

Sieben Vergleiche geben Q und B als Ziele vor und legen die dritte frühe Uhr aus dem jeweiligen Vorschlag rational fest. Sechs weitere Vergleiche geben nur eine frühe Uhrverschiebung von ±1/1024 vor. Alle 13 Lösungen sind mit Intervallkontraktionen zertifiziert, einschliesslich aller 152 strikten Kausalrelationen, Gewichts- und Gerätegrenzen. Das Fenster ist weiterhin x = 1/2 ± 1/32.

## Transfer bei geänderten späten Gewichten

Die schwere Modellreferenz normalisiert Q und B jeweils auf 4. In den sechs leichten Testfällen werden die vier späten Gewichte nach derselben Vorschrift durch 16 geteilt. Die vier frühen Gewichte und alle späten Uhren bleiben gleich. Bei jeder vorgegebenen frühen Uhränderung skalieren die bereits stationär bestimmten Innengewichte ebenfalls um 1/16. Denn jede Kante an einem freien Knoten hat ihren Empfänger ausserhalb des Anfangsideals. Alle freien Uhrgleichungen sind bezüglich dieser Gewichte homogen, und die Dichtegleichungen hängen nur von den Uhren ab. Die Modelleinheit für beide Auswertungen wird in keinem der sechs Fälle neu bestimmt.

| Veränderte frühe Uhr | Masse aus Q | Masse aus B | Beide innerhalb 2 % um 1/4 | Gemischter Kontakt im Fenster |
|---|---:|---:|---|---|
| Y₀ − 1/1024 | 0,251499 | 0,245027 | ja | ja |
| Y₀ + 1/1024 | 0,248376 | 0,254958 | ja | nein |
| Y₁ − 1/1024 | 0,247884 | 0,257884 | nein | nein |
| Y₁ + 1/1024 | 0,251880 | 0,242407 | nein | ja |
| Y₂ − 1/1024 | 0,250675 | 0,247221 | ja | ja |
| Y₂ + 1/1024 | 0,249305 | 0,252866 | ja | nein |

Ein gemischter Kontakt bedeutet hier ein positives und ein leeres unvergleichbares Ereignis im Fenster mit gemeinsamen positiven Ankern. In den zwei Fällen mit beiden erfüllten Bedingungen sind dies (19,17) und (19,20). Bei Y₂ − 1/1024 liegen die beiden Transferfehler bei +0,2701 % und −1,1115 %; die normierte Uhr 19 verschiebt sich von rund 0,5268775 auf 0,5211282. Im offenen kausalen Intervall (0,21) bleiben sieben Ereignisse. Das Maximum des nach der Verweildauerregel beidseitig markierten Massenanteils liegt bei rund 28,071 % gegenüber 28,206 % in der Referenz. Es wurde für alle sechs Vergleichsfälle durch rationale untere und obere Optimierungszeugen geprüft. Die Verkleinerung aller positiven Innengewichte im selben Verhältnis ändert diesen normierten Anteil nicht.

Ein separater, auf beide Modellgrössen abgestimmter Kontrollfall verringert Q und B zunächst um genau 10 % und skaliert dann mit 5/72. Er trifft 1/4 in beiden Auswertungen exakt; sein Messfenster enthält kein Ereignis. Die sechs Fälle in der Tabelle bewerten die beiden Auswertungen bei gemeinsam festgesetztem Faktor 1/16. Die Regel und die weiterführenden Auswertungen entstanden im Verlauf dieser Studie und wurden nicht öffentlich vorregistriert.

## Konsequenz für P3

Für eine anschliessende geometrische Rechnung ist das Paar aus der schweren Referenz und dem leichten Fall Y₂ − 1/1024 der genauere der beiden Kontaktfälle nach dem grösseren absoluten Modelltransferfehler. Seine Eingangsfelder, die eingeschlossenen freien Felder, die Kontaktanker und Uhrwerte sind angegeben. Eine physische Masseneichung mit unabhängigem Positivstandard und Vakuumkontrolle, die Identifikation der äusseren Materiegrenze und deren Eigenfläche auf denselben Historien sind weiter offen. Zwei Kontaktpaare liefern weder eine geschlossene materielle Oberfläche noch die separat kalibrierten Schalenvolumina und radialen Eigendicken. Alle acht physischen Pilotradien und alle 60 physischen P3-Einträge bleiben NOT_RUN.

## Offline wiederholen

Python ab 3.10 mit der Standardbibliothek genügt. Nach dem Entpacken im Studienverzeichnis ausführen.

```sh
sha256sum -c SHA256SUMS
python3 -B pruefen.py
```

Ergebnisse.json enthält die vollständigen Lösungsboxen für die 13 Grundfälle, die exakten Zielwerte, die nachprüfbare Ladungsschranke und die skalierte Modellauswertung. Für eine leichte Lösung werden die in Transferregister.tsv angegebenen Faktoren auf alle Gewichte ausserhalb der Knoten 0 bis 3 angewendet. Fallregister.tsv führt die 13 Grundfälle mit ihren Ladungs-, Gewichts- und Uhrenintervallen auf. Transferregister.tsv enthält die sechs leichten Modelltests und die separat angepasste Kontrolle. Vergleichspaar.json enthält die vollständigen Feldboxen der schweren Referenz und des ausgewählten leichten Falls, bereits mit angewandter Skalierung, die Kausalrelation und die Kontakte. Die Vorschlagsdateien enthalten gerundete Startwerte und rationale Prüfzeugen. Der Nachweis prüft ihre Gültigkeit ohne Optimierer und vergleicht beide Register sowie die Ergebnisdatei byteweise.
