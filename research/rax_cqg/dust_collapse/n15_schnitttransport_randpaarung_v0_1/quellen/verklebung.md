# Zwei innere Uhren am integrierten Staubball-Randkern

CST-DUST · Typ 2097151 · 22. November 2026 · Anschluss an [PR #354](https://github.com/thomasmgfeller/x6-spectral-astrolabium/pull/354)

Die vierte und die sechste innere Uhr der Siebenerkette genügen zusammen mit den äusseren Randquellen für einen numerischen Massentest am integrierten Kern. Bei markierter Masse 4 ergeben 15 endliche Phaseneinstellungen 4,002411 und 3,999286. Die beiden Werte gelten für die beiden publizierten Anfangsdichtefenster. Die Rechnung setzt voraus, dass diese inneren Ereignisse adressierbar sind und sich die Randphasen kohärent vergleichen lassen.

## Versuch und Ergebnisse

Die innere Ordnung ist 4 ≺ 5 ≺ 6 ≺ 11 ≺ 12 ≺ 13 ≺ 14. Auf beiden Seiten liegen die bekannten vier Kragenereignisse. Es gelten die originalen zwei gleichphasigen äusseren Uhrfenster, die sieben inneren Uhrfenster und Dichteabweichungen und das konditionierte Produktmass aus PR #354. Der Vergleich innerhalb dieses Typs verwendet die dort geprüfte gemeinsame Skalarpaarung. Die Markermasse M = 4 wird zur Datenerzeugung festgelegt. Die Ausleseformel verwendet Uhrverschiebungen, Randphasen, bekannte Kragendichten und die unverschobene positive Randdauer D = T₇−T₃. Die Zahl 4 geht in die Ausleseformel nicht ein.

| Auslese im gleichen Referenzmodell | Dichtezentrum 1/8 | Dichtezentrum 1/4 |
|---|---:|---:|
| Alte äussere Quelle aus PR #354, geschätzte Masse | 2,15599 bis 2,34401 | 2,15685 bis 2,34315 |
| Vollständiger Marker als Einfügung vor der Integration, garantierter relativer Fehler | < 0,00295 % | < 0,00293 % |
| Innere Uhrverschiebung bei separat eingefügter sichtbarer Masse, Grenzwert kleiner Schritte | 4,002496208 | 3,999156357 |
| Innere und äussere Uhrverschiebungen, Grenzwert kleiner Schritte | 4,002410116 | 3,999284458 |
| Dieselben inneren und äusseren Quellen bei endlichem Schritt h = 1/8 | **4,002411146** | **3,999285607** |
| Vorzeichenbehafteter relativer Fehler bei h = 1/8 | **+0,06028 %** | **−0,01786 %** |

Die ersten beiden Zeilen haben rationale Schranken. In der zweiten Zeile gilt die Schranke sogar bei beliebiger konstanter relativer Phase der beiden Uhrfenster. Die letzten vier Zeilen sind deterministische Quadraturwerte für die gleichphasige Präparation. Der Datensatz enthält die Konvergenz über mehrere Gitter und fünf Schrittweiten. Eine validierte Quadratur- und Rundungsfehlerschranke für die beiden neuen Massenwerte steht aus.

## Welche Messung ausgeführt wurde

Auf jeder Feldgeschichte ist Y = T/Δ mit Δ⁴ = 3/722. Die vier festgelegten Richtungen sind A am Ereignis 11, B am Ereignis 13, U = (1,1,1,1) und V = (76,47,24,8)/64 auf dem Vergangenheitskragen. Alle übrigen Richtungskoeffizienten verschwinden. Eine Einstellung s erzeugt den Kernel

    Z(s) = ∫ exp[i S_d(Y + (s_A A + s_B B + s_U U + s_V V)/√D, w)] dμ .

Die Skalierung mit √D gibt jeder zweiten Ableitung den benötigten Faktor 1/D. D wird an der unverschobenen Präparation abgelesen. Zukunftsuhr 7 ist fest vorgegeben. Die Quellen verschieben die Uhren in der Wirkung. Das Mass einschliesslich aller Fenster und der Verweildauern bleibt für den Vergleich auf der vorbereiteten Belegung definiert. Ein gemeinsames Verschieben von Integrationsvariablen und Präparationsfenstern beschreibt einen anderen Versuch.

Schreibe Φ(s) = arg[Z(s)/Z(0)]. Als rein äussere Referenz verwendet eine weitere Quelle den bekannten Kragenbeitrag C/D mit C = −127w₇+240w₈−120w₉ = −7/8. Für deren Phase Φ_C(t) wird exp(itC/D) in den unverschobenen Kern eingefügt. Die neue Massenauslese lautet

    M_h = D_h Φ_C − 19 [D_AA Φ + (10/9) D_AB Φ − 15 D_BB Φ − D_UV Φ].

D_h ist der symmetrische erste Differenzenquotient. D_AA und D_BB sind zentrierte zweite Differenzen mit Nenner h². D_AB und D_UV sind die vier gemischten Eckmessungen mit Vorzeichen +,−,−,+ und Nenner 4h². Die 15 Einstellungen umfassen die gemeinsame Null, vier einzelne innere Verschiebungen, vier innere Eckmessungen, vier äussere Eckmessungen und zwei Kragenreferenzen. Bei h = 1/8 sind die relativen Phasen und Amplitudenbeträge in quadratur.json archiviert, zusätzlich die beiden für den Hybridvergleich benutzten Referenzphasen.

## Warum die beiden Antworten verschieden sind

Mit der komplexen normierten Gewichtung ⟨f⟩ = ∫f exp(iS_d)dμ / Z(0) und J_a = ∂ₐS_d gilt für den integrierten Kern exakt

    ∂ₐ∂ᵦ arg Z = Re ⟨∂ₐ∂ᵦ S_d⟩ − Im [⟨Jₐ Jᵦ⟩ − ⟨Jₐ⟩⟨Jᵦ⟩] .

Das Produkt der beiden ersten Wirkungsableitungen ist bilinear, ohne komplexe Konjugation. Alle Quellenableitungen halten die Feldbelegung im Integrationsmass fest. Beschränktheit auf der kompakten Box erlaubt das Differenzieren unter dem Integral. Die nachgewiesene Untergrenze für den Betrag des Kerns sichert den lokalen Zweig.

Vor der Integration erzeugt die Kombination der inneren Wirkungsableitungen und des Kragenanteils genau w₁₂+w₁₃+w₁₄ nach Rückrechnung der Dauer. Der äussere Mischterm erfasst die vier übrigen inneren Dichten. Im integrierten Antwortschätzer kommt zur reellen schwachen Gesamtmasse der Term

    19 Im [Cov(A,A) + (10/9) Cov(A,B) − 15 Cov(B,B) − Cov(U,V)]

hinzu. Die schwache Masse liegt an beiden Zentren numerisch bei fast 4. Der zusätzliche Term verschiebt die Uhrablesung bei den beiden Dichtezentren in unterschiedliche Richtungen. Die Ableitungen erhält man auf einem Weg aus den ersten beiden Momenten der linear in die Wirkung eingehenden Dichten und auf einem zweiten Weg aus den Phasen der tatsächlich verschobenen integrierten Kerne.

Als exakte Kontrolle werden zwei Feinhistorien bei identischen Uhren im rechten Fenster, mittleren inneren Uhrwerten und einer gegenüber dem Zentrum um ±0,5 % geänderten Dichte w₁₃ betrachtet. Ihre positiven Amplitudengewichte sind 2:1. Für die Phasendifferenz α und die normierten komplexen Historiengewichte p₁,p₂ gilt Im(p₁p₂) = 6 sin(α)/(5+4 cos(α))². Der vollständige Korrelationsterm ist in diesem Beispiel streng negativ. Die rational eingeschlossenen Werte stehen in exakt.json. Diese Zweipunktpräparation zeigt die prinzipielle Verschiedenheit beider Antworten. Die kontinuierliche Referenzpräparation wurde separat integriert.

## Welche Informationen über den Schnitt gelangen

Die Gesamtordnung besitzt 50 aktive Staubpaare mit Schichtkoeffizienten (1,−9,16,−8). Wir trennen hinter 11 und hinter 13. Jede Paarwirkung wird am späteren Endpunkt eingesetzt. Die folgende Tabelle zählt sämtliche Beiträge unabhängig über die Gesamtordnung und über die jeweils vier letzten Vorgänger.

| Früherer Endpunkt | Ziel bis 11 | Ziel 12 oder 13 | Ziel ab 14 einschliesslich Zukunftskragen |
|---|---:|---:|---:|
| Bis 11 | 22 | 7 | 3 |
| 12 oder 13 | 0 | 1 | 7 |
| Ab 14 | 0 | 0 | 10 |

Damit sind 17 von 50 Termen über eine Blockgrenze verteilt. Das Paar (11,13) hat Gewicht −9 und trägt die vollständige gemischte innere Wirkungsantwort. Direkte Intervallzählung und chronologische Rekursion über die letzten vier früheren Uhren ergeben dieselben Wirkungsterme und Quellenkoeffizienten auf jeder Feldgeschichte. Jeder Dichtefaktor des Produktmasses geht einmal ein. Ein innerer Zellanteil hängt vom nächsten Uhrwert ab und muss daher bis zu dessen Verfügbarkeit offenbleiben. Bei festen äusseren Daten kann man integrieren, sobald der letzte abhängige Faktor eingesetzt ist. Endliche Boxen und das integrierbare Referenzmass erlauben Fubini. Die bekannte skalare Reduktion auf dem festen Typ liefert beiden Wegen denselben gemeinsamen Faktor.

Hieraus folgt die Gleichheit der zusammengesetzten und der gemeinsamen Amplitude sowohl mit feinweise eingefügter Zeigerphase als auch mit gewöhnlichen Uhrverschiebungen. Bei vorberechneten Quellenbeiträgen je späterem Endpunkt wirkt die Einfügung als Multiplikation mit einer lokalen Phase. Die Herleitung dieser Kopplung als physikalische Operation steht aus. Zwei separate Quadraturkontraktionen prüfen die komplexen Amplituden für Quelle aus, beide Zeigerarme und zwei gemischte Uhrverschiebungen. Bei künstlichem Weglassen aller 17 Kreuzterme ändert sich die unverschobene komplexe Amplitude relativ um rund 47 %.

Am ersten Schnitt lässt sich der Informationsbedarf schärfer bestimmen. Bei festen äusseren Daten werden die vier linken Uhren (4,5,6,11) und die vier rechten Variablen (Y₁₂,Y₁₃,Y₁₄,W₁₂) variiert, mit W=w/Δ. Am inneren Mittelpunkt der Box bei äusserem Versatz e=1/4 hat die entsprechende gemischte 4×4-Ableitungsmatrix von S_d/Δ die Determinante 1974375/8340544. Die Referenzbox enthält hier eine offene Umgebung aller acht Variablen. Jede glatte klassische Zusammenfassung der linken Uhren in k reellen Zahlen, über die alle weiteren Abhängigkeiten der feinen Wirkung laufen, begrenzt den gemischten Rang auf k. Folglich braucht sie mindestens vier unabhängige Zahlen. Vier vergangene Uhren reichen für die späteren Paarterme auf dieser Kette aus. Die bedingte Präparation benötigt zusätzlich ihre gemeinsamen Randdaten und ausstehenden Massfaktoren. Die Rangaussage betrifft die Darstellung der feinen Wirkung, keine minimale Quanten-Hilbertraumdimension.

## Konditionierung und Reproduktion

Bei normiertem Rohmass bleibt der Betrag der Amplitude für alle 15 Einstellungen und entlang der geraden Wege von null dorthin über 0,7673 bei Zentrum 1/8 und über 0,7781 bei 1/4. Die Rechnung setzt auf den reproduzierten unverschobenen Schranken aus PR #354 auf und begrenzt die lineare und quadratische Wirkungsänderung je Zelle rational. Für die Kragenquelle gilt |ΔS| ≤ h |C|/D. Der Abstand jedes normierten Kerns vom unverschobenen Kernel bleibt kleiner als dessen Betragsuntergrenze. Deshalb muss der Phasenvergleich auf keinem dieser Wege eine Nullstelle überbrücken.

Die endlichen Differenzen verstärken Messfehler. Teilen sich die 15 Phasen einen stabilen Bezug und beträgt ihr jeweiliger absoluter Fehler höchstens δ Radiant, wächst der absolute Massenfehler durch diese Fehler höchstens um [10621/(9h²)+1/h] δ. Der zentrale Phasenwert wird dabei nur einmal gezählt und sein gemeinsamer Koeffizient zusammengefasst. Bei h=1/8 ist der Faktor 679816/9. Für δ=10⁻⁷ rad entspricht das höchstens 0,007554 Masseneinheiten beziehungsweise rund 0,189 % des Sollwerts 4. Das ist ein bedingtes Fehlerbudget für die Auslese. Ein tatsächlich erreichter Messfehler und die physikalische Kopplung an die zwei inneren Ereignisse sind offen.

Python 3.10 oder neuer genügt für die exakten Prüfungen und für die erneute Rechnung des archivierten Basispakets. Die zusätzliche Produktquadratur wurde mit NumPy 2.3.5 gerechnet. Die Befehle laufen im entpackten Ordner.

    python3 -B pruefen.py --nur-exakt
    python3 -B pruefen.py

Die drei Stufen benutzen 3, 4 und 5 Gauss-Legendre-Punkte je innerer Uhrenrichtung sowie 4, 8 und 10 je äusserem Uhrfenster. Die sieben Dichteabweichungen und die gemeinsame äussere Eingangsdichte werden analytisch integriert. Das umfasst den ganzen positiven Träger der ursprünglichen Box. Exakte Ergebnisse werden byteidentisch kontrolliert, numerische Resultate mit ausgewiesener Gleitkommatoleranz. Für die Phasenschritte h = 1/8 bis 1/128 stehen auch die Einzelergebnisse in den JSON-Dateien. Lokaler Prüfplan und explorative Erweiterung liegen mit Prüfsummen bei. Die 60 physischen P3-Einträge haben den archivierten Status NOT_RUN. Die unabhängige Ruhemasse-Eichung und ein physikalisch begründetes Instrument bleiben offen.

[Ausgangsstand auf GitHub](https://github.com/thomasmgfeller/x6-spectral-astrolabium/tree/b2bed7f165b561ba5362acb9413a14c65ce43f94/research/rax_cqg/dust_collapse/n15_traeger_uhrzugriff_v0_1)
