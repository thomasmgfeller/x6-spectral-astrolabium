# Wann bestimmen endliche Kausaldaten den Radius eines Staubballs?

**CST-DUST · Leitartikel, Arbeitsfassung 0.1 · 26. November 2026**

Zwei sphärische Geometrien können auf einer endlichen radialen Stichprobe dieselbe Kausalordnung, dieselben Uhren, dieselben Materiedichten und dieselben radialen Radarzeiten besitzen und am selben Staubuhrschnitt verschiedene Oberflächenradien haben. Für ein explizites Vergleichspaar beträgt der kleinste garantierbare relative Fehler eines gemeinsamen Punktschätzers 7/92. Dieser Satz bestimmt den Ausgangspunkt unseres frühen Zwei-Massen-Piloten.

### Satz 1 · Der endliche Radiuszeuge

Sei D die im N15-Vergleich zugängliche Beobachtung. Für zwei konstruierte Historien gilt D(h₁) = D(h₂). Bei halber Referenzzeit betragen die Arealradien der mitbewegten Oberfläche a = 8,5 und b = 9,9. Dann macht jeder deterministische Punktschätzer aus D bei mindestens einer der beiden Historien einen relativen Fehler von mindestens 7/92. Die Schranke ist für dieses Paar scharf. [Vollständige Konstruktion mit beiden Metriken](https://github.com/thomasmgfeller/x6-spectral-astrolabium/blob/7c45c6fc7dce37a34505d1f91cddd9da6002fdfc/research/rax_cqg/dust_collapse/n15_arealradius_und_schalenauslese_v0_1/README.md)

**Beweis.** Wegen der gleichen Eingabe muss der Schätzer denselben Wert s ausgeben. Ein s ausserhalb von [a,b] lässt sich durch Verschieben zum nächsten Endpunkt verbessern. Innerhalb des Intervalls wächst s/a − 1 mit s, während 1 − s/b fällt. Das Maximum beider Fehler ist daher am Schnittpunkt minimal. Auflösen ergibt s = 2ab/(a+b) und den Fehler (b−a)/(b+a) = 7/92, also rund 7,61 %.

Die Konstruktion lässt sogar das gesamte Kugelvolumen und die mitbewegte Testmateriemenge übereinstimmen. Die Geometrien unterscheiden sich im Winkelanteil der Metrik. Die endlichen Abtastpunkte liegen auf einem radialen Strahl. Damit betrifft der Satz eine genau benannte kinematische Datenklasse. Ein dynamisches Gegenbeispiel würde zwei unter denselben physikalischen Gesetzen und Randbedingungen zulässige Historien erfordern.

### Ergebnis des neuen Piloten

Mit getrennt ausgelesener Anfangsladung, Materialgrenze und lokalen Schalendaten lassen sich die beiden klassischen Kontrollen bei M=1/4 und M=4 auseinanderhalten. Auf dem N19-Modellzweig verhindern die vorhandenen positiven Ereignisse einen direkten triangulierten Oberflächenschnitt zur Zielzeit. Die acht angefragten physischen Radiuswerte bleiben offen. Der Pilot liefert ein endliches Ausschlussargument für einen konkreten Messweg.

[Veröffentlichtes Exposé](https://github.com/thomasmgfeller/x6-spectral-astrolabium/blob/7c45c6fc7dce37a34505d1f91cddd9da6002fdfc/research/rax_cqg/dust_collapse/reports/CST_DUST_Flagship_Expose_und_Forschungsprioritaet.pdf) · [P3-Prüfvertrag](https://github.com/thomasmgfeller/x6-spectral-astrolabium/blob/7c45c6fc7dce37a34505d1f91cddd9da6002fdfc/research/rax_cqg/dust_collapse/correspondence_v0_1/DERIVATION.md)

<div class="page"></div>

## Kausalordnung, Uhr und materielle Oberfläche

Eine kausale Menge ist eine partiell geordnete Ereignismenge, in der zwischen je zwei vergleichbaren Ereignissen nur endlich viele weitere liegen. In der strikten Konvention schreibt man i ≺ j für ein früheres Ereignis. Eine Antikette besteht aus paarweise unvergleichbaren Ereignissen. Eine Umbenennung der Ereignisse muss die physikalische Beobachtung erhalten. Für eine Kontinuumsinterpretation braucht es zusätzlich einen Zusammenhang zwischen Ordnung, Zählvolumen, Näherungsskala und Lorentzgeometrie. [Bombelli et al. (1987)](https://doi.org/10.1103/PhysRevLett.59.521) · [Surya (2019)](https://arxiv.org/abs/1903.11544)

Das Projekt stattet den Träger unter anderem mit Uhren Y, Materiegewichten w, Randdaten und einer endlichen Wirkung aus. Ein stationäres Feld auf einer solchen Ordnung beantwortet eine bedingte Variationsfrage. Einen Ensemblewert für einen Staubball erhält man erst mit einer physikalischen Regel zur Präparation, Gewichtung und Paarung der Historien. Die Wirkung allein wählt auch noch keine materielle Grenzfläche. Retardierte CST-Operatoren und ihre Kontinuumsnäherungen haben eigene Skalen- und Glattheitsvoraussetzungen. [Endliche Staubwirkung](https://github.com/thomasmgfeller/x6-spectral-astrolabium/blob/7c45c6fc7dce37a34505d1f91cddd9da6002fdfc/research/rax_cqg/dust_collapse/schalenvolumen_und_seitenfluss_v0_1/README.md) · [Benincasa und Dowker (2010)](https://arxiv.org/abs/1001.2725)

**Zielobservable.** Sei S(T) der vollständige Schnitt der äusseren, mitbewegten Materialgrenze zur Staubeigenzeit T. In Kugelsymmetrie ist der Arealradius R = √(A(S)/(4π)). Zur Messung gehören die Wahl der materiellen Weltfläche, die Identifikation ihres Schnitts und die Flächenmessung. Das Vorzeichen eines Pulses, eine markierte Sonde und ein verschwindender Materiedurchtritt durch eine Schale sind jeweils schwächere Angaben. Im klassischen Kontrollprofil hat auch die innere mitbewegte Schale bei a=5 keinen Durchtritt. Sie umschliesst nur 17/64 der Gesamtmasse. [Materie-, Vakuum- und Massenkontrolle](https://github.com/thomasmgfeller/x6-spectral-astrolabium/blob/7c45c6fc7dce37a34505d1f91cddd9da6002fdfc/research/rax_cqg/dust_collapse/n15_materie_vakuum_und_masseneichung_v0_1/README.md)

**Welche Zusatzdaten helfen?** Zwei lokale Schalenvolumina trennen das N15-Gegenpaar bereits in den synthetischen Vergleichsgeometrien. In drei klassischen Lemaître–Tolman–Bondi-Kontrollen schliessen 501 verschachtelte Echofenster desselben früh geeichten Sondenpaars pro Masse den Radius mit höchstens 1,969 % relativem Fehler ein. Diese Aussage verwendet vorgegebene Fehler- und Ausbreitungsgrenzen. Eine andere Forschungsrichtung rekonstruiert räumliche Distanzen aus kausaler Struktur und Volumen in einem geeigneten Bereich mittlerer Skalen. Die Übertragung auf die äussere Materialfläche einer endlichen Kollapshistorie ist eine eigene Aufgabe. [Echo-Studie](https://github.com/thomasmgfeller/x6-spectral-astrolabium/blob/7c45c6fc7dce37a34505d1f91cddd9da6002fdfc/research/rax_cqg/dust_collapse/mehrfenster_echo_radius_v0_1/README.md) · [Eichhorn, Surya und Versteegen (2019)](https://arxiv.org/abs/1809.06192)

**Prüfzeit.** Wir verwenden denselben Anfangsradius 10 und dieselbe gemeinsame Zeit T* = 5√5/6 für beide Massen, in Einheiten G=c=1. Die 5-%-Referenzbänder haben einen Abstand von etwa 0,4324. Die klassischen Zielwerte waren vor dieser Arbeit öffentlich. Der Versuch ist eine nachvollziehbare Kontrolle mit vorab festgelegter Auswertung. [Eingefrorener Zwei-Massen-Vergleich](https://github.com/thomasmgfeller/x6-spectral-astrolabium/blob/7c45c6fc7dce37a34505d1f91cddd9da6002fdfc/research/rax_cqg/dust_collapse/early_areal_radius_two_masses_v0_1/README.md)

<div class="page"></div>

## Gemeinsame Massen- und Radiusauslese in der Kontrolle

Wir verwenden pro Masse eine einzige marginal gebundene LTB-Lösung mit inhomogenem Innenprofil und Vakuumaussenraum. Die Modellfamilie stammt aus der veröffentlichten Massenstudie. Sie dient hier als Instrumentenkontrolle. Der vollständige physische P3-Vertrag verlangt unter anderem den Vergleich mit homogenem Staub und ein Gesamtfehlerbudget. [Profil, Dynamik und Standard](https://github.com/thomasmgfeller/x6-spectral-astrolabium/blob/7c45c6fc7dce37a34505d1f91cddd9da6002fdfc/research/rax_cqg/dust_collapse/n15_materie_vakuum_und_masseneichung_v0_1/klassik.py) · [Klassischer Hintergrund der Kollapsfrage](https://doi.org/10.1103/PhysRev.56.455)

**Masse und Rand.** Das separate Anfangssignal ist die skalierte Staubdichte auf einem bekannten radialen Anfangsgitter. Untere und obere Schalensummen begrenzen die Ladung. Die Vakuumprobe liefert null. Nur bei M=1/4 wird die Verstärkung mit dem gravitativen Aussenstandard geeicht. Bei M=4 wird sie unverändert übertragen. Am Zielschnitt identifiziert der Leser anhand der Materiesignale die letzte besetzte und die erste unbesetzte Station. Die beiden Indizes 492 und 493 stammen aus einem vollständigen Register mit 641 Stationen. Der Leser prüft zusammenhängende Besetzung und Aussenabdeckung. Die Kontrollrechnung gewährt genaue Materiesignale und bekannte radiale Reihenfolge.

**Geometrischer Kanal.** Der Leser fragt eine vollständig innere und eine vollständig äussere Nachbarschale derselben Lösung ab. Er bekommt das Eigenvolumen V und die radiale Eigendicke ℓ jeder Schale zur selben Zeit. Auf dem marginal gebundenen, regulären Raumschnitt gilt für ihre Endradien u < v

> ℓ = v − u, V/(4π) = (v³ − u³)/3, V/(4πℓ) = (u² + uv + v²)/3.

Der letzte Ausdruck liegt zwischen u² und v². Die innere Schale liefert damit eine untere, die äussere eine obere Schranke für den Oberflächenradius. Der Leser bekommt keine Stationsradien und keinen Zielwert. Die Simulation erzeugt ihre vier Kanäle aus der bekannten Kontrollgeometrie. Wir geben jedem V und ℓ ein eigenes Intervall von ±1 % um seinen Idealwert. Modellradien und Wurzeln werden rational nach aussen eingeschlossen.

| Modellmasse | Gemeinsame Masseneichung | Radius aus den beiden Schalen | 5-%-Referenzband, gerundet |
|---|---|---|---|
| 1/4 (Eichfall) | [0,24810; 0,25192] | [9,4669; 9,7002] | [9,09993; 10,05781] |
| 4 (Transferfall) | [3,9696; 4,0306] | [8,1548; 8,3648] | [7,84208; 8,66756] |

Die ersten beiden Intervallspalten sind nach aussen gerundet. Die exakte Prüfung nutzt die rationalen Endpunkte. Beide vollständigen Radiusintervalle liegen im jeweiligen Sollband. Die obere Grenze des relativen Radiusfehlers liegt bei 1,266 % bzw. 1,332 %. Der Vakuumfall hält die Flächenauslese an. Deterministische Intervalle in dieser Kontrolle liefern keine experimentelle Häufigkeitsaussage. Ohne eine entsprechende Beobachtung auf einer gekoppelten CST-Historie bleiben diese Radien klassische Kontrollwerte.

<div class="page"></div>

## Ein endliches Hindernis auf dem N19-Zweig

**Modell.** Auf dem stationären Viertelhintergrund prüfen wir den positiven Transportweg mit schwachem Gerät, festem Abgleich, drei Quellwerten 0 und ±10⁻⁶ sowie drei unabhängig begrenzten normierten Nachimpulsen im Betrag bis 112. Die sieben archivierten Intervallzellen decken Hintergrundverschiebungen δ von −10⁻⁶ bis +10⁻⁶ ab. Dieselben Ordnungs- und Feldgleichungen werden auf jeder Zelle erneut ausgewertet. Die Laufzeitkoordinate x = (Yᵢ − Y₃)/(Y₇ − Y₃) bezieht sich jeweils auf dieselbe Lösung. Ihre Zuordnung zur physischen P3-Uhr ist separat zu eichen. [Modell und Intervallzertifikat](https://github.com/thomasmgfeller/x6-spectral-astrolabium/blob/7c45c6fc7dce37a34505d1f91cddd9da6002fdfc/research/rax_cqg/dust_collapse/n19_driftfenster_und_voruhreneichung_v0_1/README.md)

**Satz 2 · Direkter materieller Schnitt.** Unter den 19 Ereignissen haben 17 positives Staubgewicht. Die Ereignisse 15 und 17 tragen Gewicht null. Ein gewöhnliches geschlossenes Dreiecksnetz einer 2-Sphäre benötigt mindestens vier verschiedene Eckpunkte. Sollen seine Eckpunkte vorhandene positive Ereignisse einer gemeinsamen Antikette sein, kommen auf dieser Ordnung genau zwei Vierergruppen in Betracht. In den archivierten Kennungen sind es {4,5,6,16} und {4,5,6,18}.

**Nachweis.** Die vollständige Relation enthält 129 vergleichbare geordnete Paare. Die Auswertung zählt alle Vierer-Teilmengen der positiven Ereignisse und verwirft jede mit einem vergleichbaren Paar. Eine zweite Aufzählung erweitert Antiketten schrittweise. Sie findet 17 Einergruppen, 22 Paare, 13 Dreiergruppen, zwei Vierergruppen und keine grössere. Die Ergebnisse transformieren bei allen 171 einzelnen Vertauschungen der Ereignisnamen mit den Gruppen. Das folgt für beliebige Umbenennungen auch unmittelbar daraus, dass das Kriterium nur die Ordnung und das Vorzeichen des Gewichts verwendet.

Für jede Lösung ist η das Minimum über die beiden Vierergruppen des maximalen Abstands ihrer vier Uhrwerte von x=1/2. Die Intervallrechnung über alle drei Quellen und sieben Driftzellen ergibt

> 0,31677018633540372 < η < 0,31677018633540374.

Selbst ein Zeitfenster mit Halbbreite 0,31 enthält demnach keinen vollständigen Kandidaten. Bei grösserer Breite folgt aus vier unvergleichbaren Ereignissen allein weder eine materielle Oberfläche noch ihre Fläche. Der Befund betrifft die direkte Netzkonstruktion aus Ereignissen auf diesem Träger. Nichtlokale oder zwischen Schnitten rekonstruierte Geometrie hat andere Voraussetzungen.

**Ergänzende Rückwegprüfung.** Die Relation hat einen Link von 16 nach 18. Die strikte Zukunft von 18 besteht aus {7,8,9,10}. Ihr frühester Kandidat ist 7 mit x=1. Ein eigens aufgezeichneter Rückempfang nach Reflexion an 18 hat deshalb im offenen Intervall zwischen x₁₈ und 1 kein Ereignis. Die Zugehörigkeit von 7 zur materiellen Weltlinie des Senders ist offen. Der Test prüft eine Zweiwegvariante. Die früheren Mehrfenster-Kontrollen betrafen die Ankunft an der zweiten Sonde.

<div class="page"></div>

## Entscheidung für die Kollapsfrage

Das Exposé verlangt, dass positive Anfangsmasse, Laufzeit, äussere Materialgrenze und Flächenauslese auf derselben gekoppelten Präparation verfügbar sind. Im untersuchten Quellenbestand liefert der Massenstandard eine klassische Referenz. Für den CST-Zweig sind unabhängiger positiver Standard und Vakuumnullpunkt offen. Der frühe N19-Paarbefund entstand mit Hilfe der gewünschten Sende- und Empfangszeiten bei der Wahl von Randgewichten. Die spätere Registrierung des Pulsvorzeichens liefert eine bedingte Gerätebeobachtung. Die materielle Zuordnung und ein kalibriertes Flächensignal am Zielzeitpunkt fehlen. [Quellenwahl am N19-Paar](https://github.com/thomasmgfeller/x6-spectral-astrolabium/blob/7c45c6fc7dce37a34505d1f91cddd9da6002fdfc/research/rax_cqg/dust_collapse/n19_stationaeres_sende_und_empfangspaar_v0_1/README.md) · [Masseneichung](https://github.com/thomasmgfeller/x6-spectral-astrolabium/blob/7c45c6fc7dce37a34505d1f91cddd9da6002fdfc/research/rax_cqg/dust_collapse/n15_materie_vakuum_und_masseneichung_v0_1/README.md)

| Prüfung | Ergebnis dieser Arbeitsfassung |
|---|---|
| N15-Identifizierbarkeit aus dem radialen Record | Exakte relative Minimaxgrenze 7/92 für das kinematische Paar |
| Gemeinsame Massen- und Flächenablesung | Beide klassischen LTB-Kontrollen liegen in ihren Zielbändern |
| Direkter materieller Dreiecksnetz-Schnitt auf N19 | Am Zielschnitt unter den geprüften Voraussetzungen ausgeschlossen |
| Physischer Zwei-Massen-Radiuspilot | HOLD_NOT_ELIGIBLE. Für zwei Massen und vier Dichten sind acht Radiuswerte offen |
| Gesamtes P3-Register | 60 Einträge mit NOT_RUN. Keine neuen dynamischen CST-Ensembles |

**Folgende Theorieentscheidung.** Als Nächstes ist ein räumlich ausgedehnter, unter Umbenennung definierter Messweg zu prüfen. Beispielsweise könnten je ein inneres und äusseres lokales Schalenvolumen sowie ihre radiale Dicke aus einem Zeitblock bestimmt werden. Vor der Prüfung wären der Materialmarker, die Erzeugung dieser Werte aus der Wirkung und dem Record sowie eine vom Sollradius unabhängige Uhreinheit festzulegen. Die innere mitbewegte Scheingrenze und der Vakuumfall bleiben Gegenkontrollen. Ein gültiger Massenstandard und ein gemeinsames Unsicherheitsbudget bleiben Voraussetzung für physische Radiuswerte. [P3-Entscheidungsregeln](https://github.com/thomasmgfeller/x6-spectral-astrolabium/blob/7c45c6fc7dce37a34505d1f91cddd9da6002fdfc/research/rax_cqg/dust_collapse/correspondence_v0_1/DERIVATION.md) · [Register](https://github.com/thomasmgfeller/x6-spectral-astrolabium/blob/7c45c6fc7dce37a34505d1f91cddd9da6002fdfc/research/rax_cqg/dust_collapse/correspondence_v0_1/results/checkpoint_P3_records.json)

Ein dynamisches Gegenpaar wäre ein eigenständiges Ergebnis. Dafür müssten bei gleichen zulässigen Eingaben und derselben Präparationsregel zwei dynamisch zugelassene Historien unvereinbare 5-%-Anforderungen ergeben. Gehört die Masse zu den Eingaben, muss sie bei beiden gleich sein. Der hier bewiesene Ausschluss einer direkten N19-Ablesung reicht dafür nicht aus. Kontinuumsverfeinerung, Gewichtung der Historien, Fortsetzung und Regularität bleiben gesonderte Fragen der Singularitätsauflösung.

### Nachrechnung und Stand

Das Offline-Paket enthält die editierbare Fassung, den lokal festgelegten Prüfplan und seine Ergänzung mit Prüfsummen, die archivierten Modelleingaben und die vollständigen Ergebnisse. Nach dem Entpacken reproduziert `python3 -B pruefen.py` die Ausgabe bytegenau. Ausgangspunkt ist der veröffentlichte Stand [PR #397](https://github.com/thomasmgfeller/x6-spectral-astrolabium/pull/397). Die neue Rechnung und dieser Manuskriptentwurf haben Arbeitsstand 0.1.
