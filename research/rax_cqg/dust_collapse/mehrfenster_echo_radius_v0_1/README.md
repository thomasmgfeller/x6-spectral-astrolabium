# Etappe 2b · Arealradius aus mehreren Echo-Zeitfenstern

**Befund vom 26. November 2026.** Ein kalibriertes Paar komovierender Materialsonden genügt in drei synthetischen Lemaître–Tolman–Bondi-Staubkugeln, um den Arealradius beim vorab festgelegten Schnitt T* deterministisch einzuschliessen. Der Leser kennt die Anfangseichung R₀=10, die Uhrfehler und grobe Ausbreitungs- und Regularitätsschranken für diese Kontrollfamilie. Für die tatsächliche Stützfläche fällt die garantierte relative Fehlergrenze in allen drei Fällen unter 2 %. Der Bezug auf reale Materiesonden, die Masseneichung und die Fensterbeobachtung in einer physischen CST-Historie bleiben offen.

## Auswertung des festgelegten Versuchs

Bei T*=5√5/6 wird das gleiche früh kalibrierte Paar für W=500, 502, …, 1500 Millionstel einer Projektzeiteinheit befragt. Die letzte sichere Verneinung und die erste sichere Bejahung klammern die früheste Ankunft eines bei T* gesendeten Lichts ein. Die 501 ineinanderliegenden Fenster pro Masse gehören zu derselben Abfragezeit und demselben Paar. Sie sind keine unabhängigen Stichproben.

| Masse | Letztes NEIN / erstes JA | Nominelle Einwegzeit am Marker¹ | Schätzung der Stützfläche | Referenzradius der Stützfläche | Beobachteter relativer Fehler | Garantierter relativer Fehler² |
|---|---:|---:|---:|---:|---:|---:|
| 1/4 | 1030 / 1050 | 1040,47431 | 9,571679 | 9,578868 | 0,07505 % | ≤1,856 % |
| 1 (Hauptvergleich) | 984 / 1004 | 993,64115 | 9,148392 | 9,148264 | 0,00140 % | ≤1,921 % |
| 4 | 888 / 906 | 896,46739 | 8,256112 | 8,254818 | 0,01568 % | ≤1,969 % |

¹ Alle Zeiten in Millionsteln einer Projektzeiteinheit. Der Zeitwert kommt aus einer separaten numerischen Strahlrechnung. Er geht weder in die Fensterzertifikate noch in die Radiusschätzung ein. Die untere Grenze der Schwellenklammer ist strikt, die obere inklusiv.

² Gesamte archivierte Hülle früher Uhrfehler und alle zugelassenen späteren Stempelfehler, konservativ aufgerundet. Dies ist ein Radiusfehler unter den unten aufgeführten Modellvoraussetzungen. Die Schätzung aus einem konkreten Satz einzelner früher Ticks und die Schätzung aus dem ganzen frühen Fehlerbereich stehen beide in Bewertung.json. Die Tabelle zeigt die zweite Auswertung. Die Hülle der frühen Ticks dient als synthetischer Belastungstest. Die einzelnen archivierten Ticks sind die ursprünglichen Instrumentaufnahmen.

Für den Hauptvergleich liegt der Radius der letzten positiven Station im garantierten Intervall [8,9760207; 9,3150138], derjenige der Stützfläche im Intervall [8,9760207; 9,3275138] (jeweils nach aussen gerundet). Die weiteren Hüllen der Stützflächen sind [9,3973443; 9,7526035] und [8,0967367; 8,4218879] für M=1/4 und 4. Im einzelnen früheren Fenster W=1000 gab es der Reihe nach NEIN, OFFEN, JA und damit für keine Masse ein beidseitig beschränktes Radiusintervall. Die Zeitklammern für die drei Modellkontrollen sind dagegen paarweise disjunkt. Bei der schweren Kontrolle verbleiben gegenüber der 2-%-Marke rund 0,032 Prozentpunkte Reserve.

## Was der Leser erhält

Aus PR 382 stammen die 21 frühen Echoaufnahmen von sieben asymmetrisch platzierten Sonden je Masse und die positiven Materialstationen auf dem frühen und späten Schnitt. Der Leser rekonstruiert für jeden gemeldeten ganzzahligen Tick das Winkelintervall mit den dortigen Grenzen für Stempel, Rundung und Reflexionsverzug. Genau ein ungeordnetes Paar (B–D) hat seinen ganzen Winkelbereich im Zielband um 1/9200 rad, sowohl bei den registrierten Ticks als auch über das kartesische Produkt aller zugelassenen frühen Tickintervalle. Die Eindeutigkeit ergibt sich, indem für jede Kante getrennt sämtliche Tickwerte geprüft werden. Die Richtung D nach B ist durch das archivierte Echonetz bestimmt. Die umgekehrte Richtung liefert im kugelsymmetrischen Kontrollmodell bei gleichen Uhren dieselbe Reichweite.

Die **1503 späten Fensterantworten werden neu aus dem Modell berechnet**. Sie sind keine im Archiv vorgefundenen späten Messungen. Jede Antwort gilt für die ganze kalibrierte Winkelhülle und beliebige zulässige Zeitfehler. Offene Fenster werden verworfen. Der Leser erhält weder Massen oder wahre Winkel noch den späten Sollradius oder numerische Strahlzeiten. Die Dateien mit Schätzungen wurden vor dem Sollvergleich erzeugt und per SHA-256 gebunden. Der Prüfer wiederholt diesen Schritt in einem leeren Verzeichnis mit nur dem Leser und den anonymisierten Fensteraufnahmen. Die zugrundeliegende Familie war öffentlich bekannt. Das ist ein zurückgehaltener Sollvergleich auf bekannten Kontrollhistorien, keine externe Verblindung.

## Begründung der Fehlerhüllen

Für den marginal gebundenen kollabierenden Staub lautet die Metrik −dT²+R'² da²+R² dΩ². Mit der eingeschlossenen Masse m(a) gilt bei f=1−3Ts/2, s=√(2m/a³), die Lösung R=a f^(2/3). Die Rechnungen verwenden den veröffentlichten Massenverlauf mit m≤4, regulärem Zentrum und Vakuum ausserhalb a=10. Die letzte positive Station liegt bei a=1599/160 und die nachfolgende im Vakuum. Die geometrische Stützgrenze ist in dieser Kontrollfamilie bei a=10 bekannt. [Originalquellen und Messkonventionen](https://github.com/thomasmgfeller/x6-spectral-astrolabium/tree/eb27671709306634e9cd96915dafe8996105daf9/research/rax_cqg/dust_collapse/materialmarker_aus_echos_und_vorlaeufertest_v0_1)

**Gültigkeit im ganzen Lichtkegel des kurzen Experiments.** Bei 0≤T≤2 und 9,99≤a≤10 ist s<0,09 und f>0,73. Deshalb liegt der Radius am komovierenden Sender über 9,99·0,73. Für R≥7 gilt entlang der Schale |∂ₜR|=√(2m/R)<2. Für beliebige kausale Bahnen ist |dR/dT|≤1+√(2m/R)<3, da die radiale Relativgeschwindigkeit |R' da/dT|≤1 ist. Ein erstes Erreichen von R=7 ist während der maximalen Dauer von 0,001504 unmöglich. Die Winkelgeschwindigkeit ist auf jedem zugelassenen Weg höchstens 1/R. Das schliesst auch Wege durch das Innere des Balls ein.

**Vorwärtsprüfung.** Sei sₜ=0,000002 die spätere Stempelhalbbreite und d₋=W−2sₜ, d₊=W+2sₜ. Sei Rₘₐₓ eine obere Schranke am frühesten möglichen Sendetermin, Rₘᵢₙ eine untere am spätesten. Beide werden mit rationalen Wurzelhüllen aus dem Vorwärtsmodell berechnet. Falls Rₘₐₓ θ₊≤d₋, genügt der Grosskreisbogen auf der kontrahierenden Schale für JA. Falls (Rₘᵢₙ−3d₊)θ₋>d₊, kann kein kausaler Weg das Ziel rechtzeitig erreichen. Alle übrigen Fenster erhalten OFFEN. Da Nullfehler zulässig sind, liegt die nominelle Schwelle zwischen letztem sicheren NEIN und erstem sicheren JA.

**Inversion.** Der Leser braucht die zwei massenspezifischen Modellradien Rₘᵢₙ und Rₘₐₓ nicht. Wäre (R*+2sₜ)θ₊≤d₋, wäre ein Grosskreissignal für jede zulässige Aussendung rechtzeitig. Ein beobachtetes NEIN erzwingt daher R*>d₋/θ₊−2sₜ. Bei JA kann die gesamte Winkelstrecke höchstens d₊/(R*−2sₜ−3d₊) betragen. Somit gilt R*≤d₊/θ₋+3d₊+2sₜ. Das Maximum der unteren und das Minimum der oberen Grenzen liefern [L,U]. Der Leser behandelt die sicheren Antworten wie einzelne fehlerbehaftete Beobachtungen und behält die Zeitmargen zusätzlich bei. Dadurch bleiben die Hüllen konservativ.

**Vom inneren Marker zur Stützfläche.** Auf dem kurzen radialen Zwischenstück gilt 0≤−a s'≤3s/2 und R'=f^(2/3)−aTs' f^(−1/3). Aus f>0,73, T≤2 und s<0,09 folgt 0<R'<2. Somit ist der Radius der Stützfläche R(T*,10) um höchstens 2·(10−1599/160)=0,0125 grösser als der Markerradius. Nur die obere Intervallgrenze wächst. Eine unbekannte Stützstelle innerhalb der ganzen Stationszelle oder andersartige Materieprofile würden eine andere Hülle erfordern.

**Punktschätzung.** Der harmonische Mittelwert 2LU/(L+U) gleicht die beiden maximalen relativen Endpunktfehler aus. Die deterministische Schranke ist daher (U−L)/(U+L). Ein sehr kleiner beobachteter Fehler innerhalb einer Hülle belegt für sich keine vergleichbare Auflösung. Insbesondere ersetzt das Ergebnis weder die statistische Stichprobenrechnung des P3-Vertrags noch eine unabhängige Masseneichung. Für R₀ ist ein exakter Anfangsstandard vorausgesetzt. Die 60 physischen Checkpoints wurden nicht ausgeführt.

## Gegenrechnungen und Reproduktion

Die nominelle Lichtlaufzeit wurde für beide Schalen mit zwei Parametrisierungen der Nullgeodäte und je zwei Schrittweiten berechnet. Alle 63 archivierten frühen Echo-Ticks werden reproduziert. Die vier numerischen Berechnungen der späten Dauer stimmen innerhalb 4,45·10⁻¹⁶ Projektzeiteinheiten überein. Der zertifizierte Einschluss aller kausalen Wege folgt aus den analytischen Schranken. Für den Sollwert jeder Masse und beider Schalen wurden ausserdem die rationale Hülle der geschlossenen Lösung und eine unabhängige Integration der Schalengleichung verglichen.

Mit Python ab Version 3.10 und der Standardbibliothek im entpackten Ordner ausführen.

    python -B pruefen.py

Pruefplan.md und Fensterkonvention.md dokumentieren die vor dem Lauf eingefrorenen Entscheidungen. Fensteraufnahmen.json enthält für jeden Fall die 501 Antworten in aufsteigender Fensterreihenfolge. In Schaetzungen.json stehen die massenfreien Intervalle. Bewertung.json öffnet die Zuordnung der Kontrollmassen und liefert rationale Einschliessungen. Strahlkontrolle.json enthält die separaten numerischen Laufzeiten. Die Quelldateien unter basis/ stimmen bytegenau mit dem oben verlinkten Commit überein.
