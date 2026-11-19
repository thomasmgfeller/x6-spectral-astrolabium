# CST-DUST · Vier Uhrantworten und die N15-Stabilitätsgrenze

[Kurzbericht (PDF)](../reports/CST_DUST_N15_Uhrantworten_v0_8.pdf) · [Offline-Prüfpaket (ZIP)](../packages/CST_DUST_N15_Uhrantworten_v0_8_Pruefpaket.zip) · [Vollträgerzertifikate](volltraeger.json)

**Etappe 1 · 19. November 2026 · v0.8.** Grundlage ist die N15-Studie aus [PR #312](https://github.com/thomasmgfeller/x6-spectral-astrolabium/pull/312), Merge-Commit `a8fc2aad9c3b4d117bcf03aeab14670d8e4846ac`. Als Eingabe dient ihr [vollständiges Offline-Archiv](../packages/CST_DUST_N15_Erweiterungsstabilitaet_v0_7_Pruefpaket.zip). Im Prüfpaket v0.8 liegt es als `input_v07.zip` bei. Die Git-Blob-Kennung lautet `fddaaa65ede4d4adba3e31f78cd3828979f0cf16`. Der Lader prüft zusätzlich SHA-256.

## Ergebnis

| Träger und Rechnung | Grösster im Raster von 0,0001 Prozentpunkten gemeinsam zertifizierter Transfer |
| --- | ---: |
| Alle 1 217 Zustände, 23 direkt integrierte N15-Typen (v0.7) | 4,0008 % |
| Gleicher Träger, zusätzlich 47037 und 45950 | 4,1639 % |
| Gleicher Träger, zusätzlich 46509 und 46525 | 4,4357 % |
| Teilträger aus 169 früheren Zuständen und allen 27 direkt integrierten N15-Typen | 5,0210 %; zulässige Verletzung bei 5,0211 % |

Jede N11-Ausgangshistorie gibt denselben Anteil λ ihres Amplitudengewichts an ihre erreichbaren, nichtnegativ gewichteten Nachkommen ab. Die beiden Aufteilungen dürfen voneinander abweichen. Jede gilt für beide Anfangsdichten. Unter den drei ursprünglichen Detektorkriterien besteht jede solche Verteilung für 0 ≤ λ ≤ 0,044357. Die Aussage gilt auf den Gittern (32,6) und (48,8) unter den numerischen Eingabebedingungen aus v0.7. Das bestehende Gegenbeispiel bei λ = 0,050211 ist auch auf dem Vollträger zulässig.

Bei λ = 0,05 ergeben sich nach beiden Runden obere Schranken von rund 11,2229 % und 11,2349 % für die relative Niveauabweichung (Grenze 10 %). Die Änderung des vierteiligen Dichtekontrasts beträgt höchstens 20,02485 % seines Referenzbetrags (Grenze 25 %). Der Gesamterfolg bleibt bei Anfangsdichte 1/4 geringer als bei 1/8. Eine konkrete Verletzung der Niveaugrenze bei 5 % bleibt offen. Bei 4,4358 % überschreitet die berechnete obere Schranke für die höhere Dichte die 10-%-Grenze erstmals im geprüften Raster.

## Auswahl, Uhrrechnung und Zertifikate

Runde 1 verwendet die beiden schwächsten unteren Projektionen auf den N11-Referenzzustand bei Dichte 1/4 aus v0.7. Runde 2 verwendet die ersten beiden nach erneuter Berechnung derselben Rangliste. Beide Eltern und beide Gitter liefern jeweils dieselben zwei Namen. Am Ende stehen 339773 und 524287 an erster und zweiter Stelle.

Für jeden der vier Typen besitzt die innere Uhr mit vier inneren Vorgängern keinen Ausgang zu einer weiteren inneren Uhr und keine Kopplung an die variable äussere Uhr. Die in v0.6 implementierte bedingte Summe über diese Uhr lässt sich für alle äusseren Knoten wiederverwenden. Alle übrigen Uhren, beide Loben und beide Anfangsdichten gehen mit den ursprünglichen Phasen und Gewichten ein. Für die komplexen Projektionen gilt der in v0.7 verwendete Fehlerradius 10⁻⁷. Alle vier neuen Kreisscheiben liegen innerhalb der früheren Betragshüllen. Ein Vergleich mit der direkten Siebenfachsumme auf (4,3) und der Gitterfolge (32,6), (48,8), (64,10) kontrolliert die numerische Auswertung. Der grösste Abstand zwischen den zwei Referenzgittern beträgt 9,62 × 10⁻¹¹ oder weniger.

Für eine Summe F von Detektorausgängen, den Referenzzustand b und eine erreichbare Nachkommenmischung v ist der Erfolg bei x = (1−λ)b + λv gleich

    (1−λ)² 〈b,Fb〉 + 2λ(1−λ) Re〈b,Fv〉 + λ² 〈v,Fv〉.

Die direkten komplexen Uhrwerte schränken den mittleren Term ein. Für alle 1 217 Zustände werden die ursprünglichen rationalen Schranken für die sieben nichtleeren Teilsummen neu berechnet. Dies kontrolliert die Totalvariationsdistanz auf allen vier Ausgängen einschliesslich des Misserfolgs. Die Vorzeichen- und Kontrastprüfung verwendet dieselbe Nachkommenverteilung für die beiden Dichten.

Für den 196-dimensionalen Teilträger werden die Skalarprodukte mit den vier neuen Zuständen aus den auslaufenden Gaußzuständen berechnet. Zusätzliche Abel-Rechnungen prüfen die Präzision und Phase. Beide Elternzeilen und die Diagonalen stimmen mit den archivierten Ankerwerten überein. Ganzzahlige Kongruenzen prüfen Positivität, rationale Stützebenen die Mischungen. Der übernommene Zeuge verteilt den Transfer zu 21 %, 70 % und 9 % auf N14_734, N14_760 und N14_8191. Bei 5,0211 % liegt sein relativer Gesamterfolg bei Dichte 1/4 selbst mit den Uhrradien auf beiden Gittern unter 0,9.

Als separate Kontrolle übertragen beide Eltern ihre gesamten jeweiligen 5 % auf denselben neuen Typ. Direkte Auswertung der vier Ausgangswahrscheinlichkeiten ergibt relative Niveauänderungen zwischen 9,2825 % und 9,8210 % (gerundet, beide Dichten und Gitter). Diese Beispiele illustrieren den Unterschied zwischen einem konkreten Test und der Garantie über alle Verteilungen.

## Offline nachrechnen

Verwendet wurden Python 3.12, NumPy 2.3.5, SymPy 1.14.0, mpmath 1.3.0 und ein C99-Compiler (`cc`). Auf einem lokalen Rechner mit diesen Abhängigkeiten genügen in diesem Studienordner oder im entpackten Offline-Paket

```sh
python3 -B verify.py
python3 -B verify.py --rebuild
```

Der erste Befehl prüft die Prüfsummen, beide Vollträgerzertifikate, den positiven Teilträger, vier Vierausgangstests sowie vier unabhängige kleine Uhrkontrollen. Der zweite berechnet zusätzlich alle neuen Uhrwerte auf drei Gittern sowie die erweiterten Gram-Matrizen aus dem eingefrorenen Eingangspaket. Die Uhrrechnung verwendet einen CPU-Thread. Zwischendaten werden lokal im Ordner `cache_v07` erzeugt.

| Datei | Inhalt |
| --- | --- |
| `uhren.json`, `uhrtest.py` | Komplexe Uhrantwort je Typ, Gitter und Dichte mit Direktkontrolle |
| `volltraeger.json`, `volltraeger.py` | Zwei Auswahlrunden, exakte rationale Konstanten, Grenzen und nächste Endtypen |
| `gram.npy`, `teiltraeger.json`, `teiltraeger.py` | Drei Gram-Matrizen des 196-dimensionalen Teilträgers, Zertifikate und Skalarprüfungen |
| `einzeltests.json`, `kontrolle.py` | Vierausgangsprüfung bei 5 % und Kontrolle des aktiven Vollträgerpolynoms |
| `basis.py`, [Eingabearchiv v0.7](../packages/CST_DUST_N15_Erweiterungsstabilitaet_v0_7_Pruefpaket.zip) | Integritätsgeprüfter Zugang zu den unveränderten Quellen und Daten von #312 |

Der Prüfradius und die Konvergenztests beziehen sich auf die endlichen numerischen Eingaben. Eine strenge Fehlerfortpflanzung aus dem kontinuierlichen Uhrintegral, die physikalische Gewichtsauswahl und die Kollapsdynamik bleiben offen.
