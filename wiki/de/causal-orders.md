# Kausale Ordnungen und Raumzeitfragen

Hier geht es um die Frage, welche Struktur in Beziehungen steckt, bevor man eine räumliche Zeichnung voraussetzt.

[English](https://thomasmgfeller.github.io/x6-spectral-astrolabium/wiki/en/causal-orders.md) · [Wiki-Übersicht](https://thomasmgfeller.github.io/x6-spectral-astrolabium/wiki/de/)

Quellenstand: 2026-10-19 · `6738f129ca31e56a88690a9d17941516ccefb321`

## Ereignisse und ihre Reihenfolge

Eine kausale Ordnung beschreibt, welche Ereignisse vor welchen anderen liegen können. Denke an drei Arbeitsschritte: A muss vor B passieren und B vor C. Dann muss auch A vor C liegen. Diese Folgerung heißt Transitivität.

Manche Paare haben keine vorgegebene Reihenfolge. In einer kausalen Raumzeitinterpretation können sie räumlich getrennt sein. Bei einem beliebigen erzeugten Netzwerk ist diese physikalische Interpretation aber noch nicht begründet.

Ein Hasse-Diagramm zeichnet nur die unmittelbaren Beziehungen. Die vollständige Relationsmatrix enthält zusätzlich alle Beziehungen, die durch Transitivität folgen. Eine hübsche Anordnung der Punkte auf dem Bildschirm ist noch keine gemessene Geometrie.

## Warum ein Spektrum nicht alles verrät

Eine gezeichnete Ordnung kann durch Umnummerieren ihrer Knoten anders aussehen und dennoch dieselbe Struktur haben. Isomorphie bedeutet hier: Es gibt eine bijektive Zuordnung der Knoten (jeder Knoten wird genau einmal zugeordnet), die alle gerichteten Beziehungen erhält. Die Zuordnung muss nicht die einzig mögliche sein.

Ein Fingerabdruck fasst die Struktur in wenigen Zahlen oder Häufigkeiten zusammen. Verschiedene Strukturen können dabei denselben Fingerabdruck erhalten – ähnlich wie verschiedene Menschen gleich groß sein können.

| Kürzel im Projekt | Was dahintersteckt |
| --- | --- |
| H7 | Eine konkret festgelegte Kombination von Spektren und Zählgrößen; keine eindeutige Kennung. |
| N1 | Lokale Nachbarschaftsprofile. |
| Q1 | Spektren gezielter Einpunkt-Erweiterungen. |
| R2 | Wiederholte Verfeinerung von Merkmalen geordneter Knotenpaare. |
| P123 | Histogramme gemeinsamer Vorgänger und Nachfolger für Ein-, Zwei- und Dreiermengen. |

Die veröffentlichten Gegenbeispiele zeigen Grenzen solcher Zusammenfassungen. Die vollständige gerichtete Relation und eine exakte Isomorphieprüfung bleiben die Vergleichsreferenz.

## Was leisten die faireren Kontrollen?

Zwei Erzeuger sind leicht zu unterscheiden, wenn einer viel dichtere oder höhere Ordnungen liefert. Deshalb wurden Vergleichspaare mit gleicher Knotenzahl N, Relationszahl R und Höhe H ausgewählt. Höhe meint hier die Länge einer längsten Kette, gezählt in Knoten.

Im veröffentlichten Hauptvergleich bei N=64 brachte P123 keinen nachgewiesenen Zusatznutzen: Die Basis erreichte 54,30 %, die Kombination 50,39 %. Vier von neun Vergleichszellen hatten zu wenige passende Paare und blieben ohne Leistungsbewertung. Das Ergebnis grenzt eine getestete Methode ein; es beweist keine allgemeine Unmöglichkeit geometrischer Erkenntnis.

- [Kontrollstudie mit Originaldaten](https://github.com/thomasmgfeller/x6-spectral-astrolabium/blob/main/research/lorentz_matched_controls/README.md)
- [Gegenbeispiele und Rekonstruktionsgrenzen](https://github.com/thomasmgfeller/x6-spectral-astrolabium/blob/main/research/lorentz_relational_boundary/README.md)

## Eigenzeit: Was wurde jetzt geprüft?

Eigenzeit ist die Zeit, die eine mitbewegte Uhr entlang ihres Weges misst. In diesem Versuch geht es um den Eigenzeitabstand einer geraden zeitartigen Verbindung zwischen zwei markierten Ereignissen in einem bekannten flachen Modell mit einer Raum- und einer Zeitdimension (1+1). Gesucht wird das Verhältnis theta = tau/T zum vorgegebenen äußeren Zeitmaßstab T.

Die einfache Referenz V zählt die K Ereignisse, die strikt zwischen den Markierungen liegen. Bei m = N−2 Hintergrundpunkten lautet ihre Schätzung sqrt(K/m). Anschaulich: Ein größeres Zeitintervall enthält im gleichmäßig befüllten Modell im Mittel mehr Punkte. Die Endpunkte selbst werden nicht mitgezählt. Koordinaten und wahre Testzielwerte erhält der Schätzer nicht.

Der erste Datenlauf ist mit vollständigen Rohdaten, Bericht und Reproduktionscode veröffentlicht. Er umfasst 6.912 Ordnungen: 768 für die Kalibrierung und 6.144 für Tests. Die Hauptbewertung war vorab auf 1.024 uniforme Testordnungen bei m=256, also N=258, festgelegt.

| Verfahren | RMSE im Hauptvergleich |
| --- | --- |
| V: Intervallpunktzahl | 0,031614 |
| D: globale Dichte-/Höhenregression | 0,177785 |
| C0: feste Konstante | 0,176774 |
| L: lokale längste Kette (beschreibend) | 0,084021 |

RMSE fasst die Schätzfehler zusammen; kleiner bedeutet hier genauer. Die Zahlen sind in Einheiten der normierten Eigenzeit angegeben. 0,031614 bedeutet nicht 3,16 % relativen Fehler bei jedem einzelnen Ereignispaar. V erfüllt die festgelegte Grenze 0,05 und alle weiteren Hauptkriterien. Das bedingte 95%-Bootstrap-Intervall der RMSE ist [0,030068; 0,033199]. Dabei bleibt die Kalibrierung fest.

D nutzt nur globale Größen und keine lokalen Merkmale der Markierungen. Der Abstand zu D ist deshalb keine Überlegenheit gegenüber allen möglichen Schätzern. V ist eine bekannte Referenz; dieser Versuch weist keinen spektralen Zusatznutzen nach.

- [Ergebnisbericht und Reproduktion](https://github.com/thomasmgfeller/x6-spectral-astrolabium/blob/main/research/lorentz_proper_time/RESULTS.md)
- [Definition, Annahmen und ursprünglicher Vertrag](https://github.com/thomasmgfeller/x6-spectral-astrolabium/blob/main/research/lorentz_proper_time/README.md)

## Welche Grenzen bleiben?

Die Zusatzkontrollen vergleichen uniforme Ordnungen mit einem gestörten Gitter bei exakt gleicher Knotenzahl, Relationszahl und Höhe. Bei m=64 und m=144 wurden jeweils 128 Paare ausgewertet. Bei m=256 waren nur 63 statt der geforderten 128 Paare verfügbar. Diese größte Zusatzkontrolle bleibt INSUFFICIENT_COMMON_SUPPORT und erhält keine Leistungsbewertung; die Grenze wurde nicht nachträglich gelockert.

- Dimension und äußerer Zeitmaßstab sind vorgegeben, nicht aus der Ordnung entdeckt.
- Dieselbe endliche Ordnung kann verschiedene Eigenzeiten zulassen; die Schätzung bleibt statistisch.
- Die Ergebnisse gelten für das festgelegte synthetische Modell. Gekrümmte Räume, andere Dimensionen und physische Messungen sind damit nicht geprüft.
- Externe Replikation und stärkere lokale Vergleichsschätzer bleiben offen. Die früheren negativen P123-Ergebnisse bleiben bestehen.

## Wie lässt sich der Befund nachprüfen?

Das Archiv enthält alle 6.912 vollständigen Ordnungen, Referenzkoordinaten, Markierungen und Einzelvorhersagen. Die interne Gegenprüfung überprüft 27.648 Vorhersagen und alle Ordnungen samt Umnummerierungen. Der GitHub-Prüflauf wiederholt die gesamte Studie ohne Netzwerkzugang und vergleicht die Ergebnisse. Dies ist interne Reproduktion, keine unabhängige externe Bestätigung.

Die Anleitung im Ergebnisbericht nennt Softwareversionen, Quellencommit und Befehle. Das ursprüngliche Archiv und der fixierte Rechenstand bleiben unverändert. Die Dokumentation unterscheidet außerdem den datierten Quellencommit von einem unabhängig belegten Zeitpunkt öffentlicher Vorabregistrierung.

- [Prüfbericht der Gegenrechnung](https://github.com/thomasmgfeller/x6-spectral-astrolabium/blob/main/research/lorentz_proper_time/results/verification.json)
- [Rohdatenarchiv und Prüfsummen](https://github.com/thomasmgfeller/x6-spectral-astrolabium/blob/main/research/lorentz_proper_time/results/RESULTS.json)
- [Veröffentlichung und GitHub-Prüfungen: PR #44](https://github.com/thomasmgfeller/x6-spectral-astrolabium/pull/44)
- [Causal-Set-Labor (eigenständiger Browserprototyp)](https://thomasmgfeller.github.io/x6-spectral-astrolabium/app/rax-cqg-lab.html)

## Wann sind Eigenzeit und Unsicherheit verlässlich?

Die neue Erweiterung gilt für bekannte flache Diamanten in d Raumzeitdimensionen. Dimension und Zeitmaßstab müssen bekannt sein, das innere Intervall muss vollständig enthalten sein, und die Hintergrundpunkte müssen unabhängig und uniform bezüglich des Volumens gezogen werden. Endpunkte und Gebiet stehen vor der Bestätigungsstichprobe fest. Dann folgt aus K inneren Punkten unter m Hintergrundpunkten die rohe Schätzung tau/S = (K/m)^(1/d).

49.152 neue Punktwolken in d=2,3,4 stimmen mit dem deklarierten Binomialmodell überein. Die daraus abgeleiteten 95%-Intervalle sind konservativ. Gute Überdeckung bedeutet jedoch keine enge Schätzung: Bei d=4, tau/T=0,1 und m=256 bleibt die innere Punktzahl mit etwa 97,47% Wahrscheinlichkeit null.

Unbekannte Dichte, abgeschnittene Intervalle, Relationsfehler oder abhängige Beobachtungen können diese Unsicherheitsaussage ungültig machen. Ein endlicher gültiger Poset beweist keine Kausalitätsbedingung für ein glattes Kontinuum.

- [Gemeinsamer Einstieg: Voraussetzungen, Ergebnisse und Grenzen](https://github.com/thomasmgfeller/x6-spectral-astrolabium/blob/main/research/lorentz_proper_time_publication/README.md)
- [Einschlussbeweis und endliche Fehlergrenzen](https://github.com/thomasmgfeller/x6-spectral-astrolabium/blob/main/research/lorentz_proper_time_domain/README.md)
- [Eigenzeit-Labor ausprobieren (feste Stichprobe)](https://thomasmgfeller.github.io/x6-spectral-astrolabium/app/proper-time.html)
- [Eigenständiges Jupyter-Notebook mit Beispielausgaben](https://thomasmgfeller.github.io/x6-spectral-astrolabium/research/lorentz_proper_time_lab/eigenzeit.ipynb)

## Nachbeproben bis zur gewünschten Präzision

Die sequenzielle Variante erlaubt, nach jedem Block frischer unabhängiger Punkte auf das Ergebnis zu schauen und bei hinreichender Genauigkeit zu stoppen. Dafür verwendet sie eine zeituniforme Konfidenzfolge nach Howard et al.; das Zeitfehlerbudget beträgt 2,5%. Wenn relative Präzision unter 10% gemeldet wird, beträgt die Wahrscheinlichkeit einer solchen Meldung bei tatsächlich größerem Fehler höchstens 2,5%, unter den Modellannahmen. Das ist keine automatische bedingte Garantie nur unter erfolgreichen Stopps.

Es gibt kein garantiert ausreichendes endliches Budget. Der Status BUDGET_EXHAUSTED verweigert die Präzisionsmeldung. In den gespeicherten 4D-Zählläufen erreichten alle je 1.024 Wiederholungen das Ziel; der Median betrug 2.592 lokale bzw. 1.673.216 globale Punkte. Das sind beobachtete Bedarfe. Der lokale Fall setzt einen bekannten, vollständig einschließenden Diamanten mit Zeitmaßstab 0,2T voraus.

Ein fest geplanter Versuch mit 480 lokalen Punkten hat bei wahrem tau/T=0,1 eine andere Aussage: 97,34% Wahrscheinlichkeit für unter 10% relativen Fehler der rohen Schätzung. Er bietet nicht dieselbe Garantie beim wiederholten Nachschauen. Die publizierte Planung trennt diese Kriterien.

- [Zeituniforme Schranke, Stoppregel und vollständige Ergebnisse](https://github.com/thomasmgfeller/x6-spectral-astrolabium/blob/main/research/lorentz_proper_time_sequential/README.md)
- [Reproduzierbare Rechnung der festen Budgets](https://github.com/thomasmgfeller/x6-spectral-astrolabium/blob/main/research/lorentz_proper_time_publication/planning.py)

## Was warnt die längste Kette – und was nicht?

Ein einmaliger Vergleich der längsten inneren Kette mit frischen Referenzordnungen bei gleicher Punktzahl K prüft zusätzliche Forminformation. Die beobachteten Nullmodell-Warnungen betrugen 5/512. Bei absichtlich räumlich komprimierter Beprobung in weiterhin flacher Geometrie waren es 506/512. Das zeigt eine Dichtestörung, keinen Krümmungsnachweis.

Eine Warnung setzt die wissenschaftliche Zeitfreigabe auf WITHHELD_MODEL_WARNING. Kein Alarm beweist das Modell nicht. Die Diagnose hat ein eigenes Fehlalarmbudget von 2,5%; zusammen mit der Zeitkonfidenzfolge beträgt die Wahrscheinlichkeit mindestens eines der beiden Fehlereignisse unter dem gemeinsamen Nullmodell höchstens 5%.

Die Hauptsimulation arbeitet mit Zählblöcken; ein zusätzlicher Lauf prüft tatsächliche Geometriepunkte. Beide neuen Pakete wurden lokal vor den Ziehungen fixiert und erst danach veröffentlicht. Eine behobene JSON-Serialisierungspanne samt Originalcode und identischen Rohzählungen bleibt dokumentiert. Interne Reproduktion und GitHub CI sind keine unabhängige externe Replikation.

- [Ausführungsverlauf und erhaltene Reparaturbelege](https://github.com/thomasmgfeller/x6-spectral-astrolabium/blob/main/research/lorentz_proper_time_sequential/EXECUTION_HISTORY.md)
- [Beide neuen Versuche vollständig reproduzieren](https://github.com/thomasmgfeller/x6-spectral-astrolabium/blob/main/research/lorentz_proper_time_publication/replay.py)

## Hat der Krümmungs-Rauchmelder bestanden?

Der neue Versuch untersucht 4D-de-Sitter-Raumzeit mit bekannter positiver Krümmung. Er verwendet 64 oder 128 Ereignisse pro Ordnung, drei Krümmungsstärken und getrennte flache Kontrollen. Vertrag, Schwellen und Stichproben waren vor dem ersten Ziellauf öffentlich fixiert. Alle 8.702 Ordnungen sind archiviert und intern vollständig reproduziert.

| Diagnose bei N=128 | Flache Referenz | Stärkster Krümmungsfall |
| --- | --- | --- |
| Gemeinsame 2er-/3er-/4er-Kettenstatistik | 10/512 Warnungen (1,95 %) | 118/512 Warnungen (23,05 %) |
| Längste Kette | 1/512 Warnungen (0,20 %) | 5/512 Warnungen (0,98 %) |

Beide Methoden bestehen die vorgegebene Fehlalarmgrenze, verfehlen aber das Empfindlichkeitsziel. Gefordert waren eine obere Fehlalarmgrenze von höchstens 5 % und eine untere Erkennungsgrenze von mindestens 80 %. Die vier ausgewählten einseitigen Grenzen berücksichtigen gemeinsam ein Fehlerbudget von 5 %. Die Intervalle gelten bedingt auf das festgehaltene Training und die gemeinsame Kalibrierungsbank.

Das Ergebnis heißt PRIMARY_SENSITIVITY_NOT_ESTABLISHED. Ein bestandener Software-Replay ändert daran nichts. Die frühere Zahl 506/512 betraf eine andere Dichtestörung in flacher Geometrie; sie ist keine Krümmungs-Erkennungsrate. Eine stille Diagnose ist kein Beweis für flache Raumzeit.

Technischer Nachtrag: Der erste GitHub-Replay scheiterte an Koordinatenbytes, die sich zwischen NumPy-Rechenpfaden geringfügig unterscheiden. Der vollständige Vergleich aller Punktwolken ergab höchstens 2,22e-16 Abweichung und exakt gleiche Kausalrelationen. Ein ergänzter Prüfweg akzeptiert nur die konkret geprüften Varianten. Der ursprüngliche strenge Check, Fehlerlog und das wissenschaftliche Negativergebnis bleiben erhalten.

- [Vollständiger Ergebnisbericht und alle Zielzellen](https://github.com/thomasmgfeller/x6-spectral-astrolabium/blob/main/research/lorentz_curvature/RESULTS.md)
- [Vorab festgelegter Prüfvertrag](https://github.com/thomasmgfeller/x6-spectral-astrolabium/blob/main/research/lorentz_curvature/contract.json)
- [Dokumentierte Portabilitätskorrektur](https://github.com/thomasmgfeller/x6-spectral-astrolabium/blob/main/research/lorentz_curvature/PORTABILITY.md)

## Warum kann eine Dichtestörung wie Krümmung aussehen?

Stell dir dieselbe Punktwolke in zwei Modellen vor. Im ersten liegt sie gleichmäßig im physikalischen Volumen einer gekrümmten Raumzeit. Im zweiten liegt sie in flacher Raumzeit, wird dort aber zeitabhängig dichter beprobt. Für die hier konstruierten konformen Zwillinge stimmen sämtliche Kausalbeziehungen exakt überein. Krümmung und wirkliche Eigenzeit sind trotzdem verschieden.

Alle 3.072 gekoppelten Zwillinge bestätigen die analytische Konstruktion. Das sind Identitätskontrollen, keine zusätzlichen unabhängigen Versuche. Bei unbeschränkt unbekannter Beprobungsdichte kann deshalb kein Verfahren allein aus diesen Ordnungen die beiden Modelle eindeutig unterscheiden. Mehr Merkmale derselben Ordnung beseitigen diese Mehrdeutigkeit nicht.

Ein sinnvoller Demonstrator darf eine Modellabweichung anzeigen und die Zwillinge gegenüberstellen. Eine Anzeige in Planck-Einheiten wäre eine Umrechnung der simulierten Skala. Ein physisches Planck-Zeitmessgerät ist damit nicht gebaut. Für neue geometrische Aussagen brauchen wir zuerst unabhängiges Wissen über Beprobung oder Volumen; fortlaufendes interaktives Testen benötigt einen eigenen vorab festgelegten Fehlerkontrollplan.

- [Geometrie und Beweis der Dichteverwechslung](https://github.com/thomasmgfeller/x6-spectral-astrolabium/blob/main/research/lorentz_curvature/DESIGN.md)
- [Reproduktion und nächste Abnahme](https://github.com/thomasmgfeller/x6-spectral-astrolabium/blob/main/research/lorentz_curvature/README.md)

## Was ändert eine feste Punktzahl an den Krümmungsformeln?

Nachtrag vom 18. Oktober 2026: Roy–Sinha–Surya untersuchen eine Beprobung mit schwankender Punktzahl. Unsere Versuche halten die Zahl der Ereignisse fest. Deshalb ändern sich die erwarteten Kettenzahlen und ihre Krümmungskoeffizienten durch die Normierung mit dem physikalischen Volumen.

Die Anpassung ist hergeleitet und mit 24.576 unabhängigen Punktwolken geprüft. Eine unabhängige Integration für Zweierketten stimmt sehr gut mit der korrigierten Vorhersage überein. Das gemeinsame Ziel, alle drei führenden Kettenkoeffizienten auf ±5% einzugrenzen, bleibt jedoch unerreicht: Für Dreier- und Viererketten sind die Unsicherheitsintervalle zu breit.

Eine Formel algebraisch umkehren zu können reicht nicht für eine brauchbare Messung. Bei 128 Punkten und wahrem RT² von etwa 0,12 beträgt der mittlere quadratische Fehler der untersuchten Rekonstruktion, als Wurzel angegeben, etwa 96,53. Die Kettenzahlen hängen stark zusammen. Ein universeller Krümmungssensor ist damit nicht qualifiziert; die Grenze durch Dichtezwillinge bleibt bestehen.

Vertrag, Seeds und Budget waren vor dem ersten Zielversuch öffentlich fixiert. Der vollständige Replay reproduziert alle Ordnungen und Entscheidungen. Eine dokumentierte Importhülle behebt einen Namenskonflikt des Prüfers, ohne eingefrorene Quellen, Daten oder Schwellen zu ändern. Externe Replikation bleibt offen.

- [RSS: Ergebnisse / Results](https://github.com/thomasmgfeller/x6-spectral-astrolabium/blob/8ee417ba8c44c1f32f4e310a6566168d84982d3a/research/lorentz_rss_fixed_n/RESULTS.md)
- [RSS: Herleitung / Derivation](https://github.com/thomasmgfeller/x6-spectral-astrolabium/blob/8ee417ba8c44c1f32f4e310a6566168d84982d3a/research/lorentz_rss_fixed_n/DERIVATION.md)

## Eigenzeit v0.2: Wann helfen mehr Daten?

Die neue Gültigkeitskarte berechnet 1.176 Kombinationen aus Modell, beobachteter Punktzahl und Intervallverfahren direkt. Es sind keine neuen Punktwolken oder Messungen. Alle 714 Kombinationen innerhalb ihrer jeweils angenommenen Modellklasse erreichen mindestens 95% Überdeckung. Davon erfüllen 192 zusätzlich das festgelegte Präzisionsziel; 522 bleiben zu unpräzise. 462 weitere Kombinationen liegen ausserhalb der vorausgesetzten Klasse.

Viele Daten beheben keinen unbekannten Dichtefehler. Im Beispiel mit nur halb so guter Erfassung im inneren Intervall meldet die ungeschützte Rechnung bei 65.536 beobachteten Punkten mit rund 98,81% Wahrscheinlichkeit fälschlich höchstens 10% relativen Fehler. Diese Zahl ist keine Krümmungs- oder Fehlerdetektionsrate.

Wenn das Verhältnis der mittleren Erfassungsintensität innen zu aussen von einer unabhängigen Quelle begrenzt ist, lässt sich ein konservativeres Intervall berechnen. Für das breite Verhältnis von 0,5 bis 2 erhält dieses im selben Beispiel rund 97,74% Überdeckung, verweigert aber die gewünschte 10%-Präzision. Das ist eine begründete Enthaltung.

Im uniformen flachen 4D-Beispiel mit wahrer Eigenzeit 0,2 des äusseren Massstabs ist 65.536 der erste erfolgreiche Punktumfang des geprüften Gitters. Mit einer vorsichtigeren Dichteannahme von 0,8 bis 1,25 sind es 262.144. Diese Werte sind keine globalen Minimalbudgets und keine sequenziellen Stoppgarantien. Der Browser-Demonstrator behält sein bisheriges flaches Modell.

- [Ergebnisse und Budgettabelle](https://github.com/thomasmgfeller/x6-spectral-astrolabium/blob/e5840afa7c7865a48766d1a5366210508a7b1f05/research/lorentz_proper_time_validity/RESULTS.md)
- [Herleitung und Annahmen](https://github.com/thomasmgfeller/x6-spectral-astrolabium/blob/e5840afa7c7865a48766d1a5366210508a7b1f05/research/lorentz_proper_time_validity/DERIVATION.md)

## Krümmung: Mehr Ketten helfen hier nur wenig

Der neue Versuch vereinfacht das Problem auf eine bekannte de-Sitter-Familie mit nur einer unbekannten Krümmungsgrösse. Er verbindet Zweier-, Dreier- und Viererketten und berücksichtigt, dass diese Merkmale aus denselben Ereignissen stammen und stark zusammenhängen.

Die Gewichtung wurde aus alten, veröffentlichten Daten bestimmt. Erst nach Veröffentlichung des Prüfvertrags wurden 16.384 neue unabhängige Punktwolken mit je 128 Ereignissen erzeugt. Im Hauptvergleich sank der mittlere quadratische Schätzfehler, als Wurzel ausgedrückt (RMSE), nur um 1,37%. Das vorab gesetzte Ziel von mindestens 10% wurde verfehlt.

Bei schwacher Krümmung ergibt die Rechnung etwa 1,7 Millionen unabhängige Wolken für eine nominelle relative 20%-Halbbreite. Bei der stärkeren geprüften Krümmung sind es etwa 2.700. Das sind überschlägige Planwerte für Zufallsstreuung, keine ausgeführten Grossversuche oder garantierten Präzisionsgrenzen. Systematische Modellfehler bleiben bestehen.

Der nächste sinnvolle Ansatz konzentriert sich auf Zweierketten und eine vollständigere geometrische Vorhersage mit kontrollierten Fehlern. Eine abgesicherte gekrümmte Uhr ist damit noch nicht erreicht. Dichteannahmen, eine unabhängige Zeitskala und externe Replikation bleiben offen.

- [Ergebnisse und Datenbedarf](https://github.com/thomasmgfeller/x6-spectral-astrolabium/blob/01430ce5f0a648ad63d611a451f0d0fd7ccb16aa/research/lorentz_de_sitter_information/RESULTS.md)
- [Prüfvertrag und Quellen](https://github.com/thomasmgfeller/x6-spectral-astrolabium/blob/01430ce5f0a648ad63d611a451f0d0fd7ccb16aa/research/lorentz_de_sitter_information/README.md)

## Krümmungsintervalle: verlässlich innerhalb klarer Annahmen

Der nächste Schritt verwendet nur Zweierketten. Für eine festgelegte de-Sitter-Modellfamilie wurde die vollständige geometrische Vorhersage mit exakten Brüchen und einer begrenzten Restunsicherheit berechnet. Eine mathematische Ungleichung bestätigt, dass sich die Vorhersage im gesamten untersuchten Bereich eindeutig umkehren lässt.

Viele Paare aus derselben Punktwolke sind nicht unabhängig. Die neue Fehlerschranke berücksichtigt das. Unter bekannter uniformer physischer Volumendichte, unabhängigen gleichartigen Wolken und einem vorab festen Datenbudget enthalten die Intervalle den wahren Modellwert mit mindestens 95% Wahrscheinlichkeit. Diese Aussage stammt aus der Herleitung; die Simulation allein beweist sie nicht.

16.384 neue Punktwolken wurden gerechnet und vollständig reproduziert. Alle geprüften Intervalle enthalten ihren Modellwert, aber keines erreicht die geforderte relative 20%-Präzision. Bei der stärksten geprüften Krümmung reicht das Intervall nach 4.096 Wolken ungefähr von 0,843 bis 3,131. Der wahre Wert ist 3,131. Das Verfahren verweigert zu Recht die Präzisionsfreigabe.

Die konservative Planung nennt je nach wahrer Krümmung sehr grosse ausreichende Budgets. Diese sind keine notwendigen Mindestzahlen und wurden nicht simuliert. Deshalb ist der nächste Schritt eine schärfere statistische Schranke mit derselben endlichen Absicherung. Unbekannte Dichte, frei gewähltes Stoppen und eine reale Uhr bleiben ausserhalb der jetzigen Garantie.

- [Ergebnisse und Grenzen](https://github.com/thomasmgfeller/x6-spectral-astrolabium/blob/e6a5bce4cafe44ddb929da3ae32d9afa4d64eca1/research/lorentz_de_sitter_c2/RESULTS.md)
- [Vollständige Herleitung](https://github.com/thomasmgfeller/x6-spectral-astrolabium/blob/e6a5bce4cafe44ddb929da3ae32d9afa4d64eca1/research/lorentz_de_sitter_c2/DERIVATION.md)

## Schärfere Intervalle: der Effizienzschritt ist bestanden

Die neue Stufe nutzt genauer aus, dass ein Paar kausal vergleichbar ist oder nicht. Sie berücksichtigt weiterhin, dass Paare innerhalb derselben Wolke voneinander abhängen. Die neue KL-Schranke erzeugt Intervalle, die niemals breiter als die bisherige Referenz sind. Die mathematisch begründete Überdeckung von mindestens 95% gilt unter denselben bekannten Modellannahmen und bei vorher festem Datenbudget.

Der Prüfvertrag wurde vor den neuen Rechnungen veröffentlicht. Die hinreichenden Planungsbudgets sinken an allen drei vorgegebenen Krümmungen um den Faktor 2,71 bis 2,77. Bei h=0,5 sind es beispielsweise 31.707 statt 85.871 unabhängige Wolken zu je 128 Punkten. Das sind ausreichende Grenzen der geprüften Verfahren, keine bewiesenen optimalen Mindestzahlen.

77.824 neue Wolken wurden gerechnet und vollständig reproduziert. Bei h=0,5 mit je 16.384 Wolken erreichen alle vier KL-Intervalle die relative 20%-Vorgabe; die alte Schranke erreicht sie einmal. Im gesamten Datensatz von 65.536 Wolken beträgt der relative Radius 4,89% statt 9,16%. Vier Gruppen erlauben keine präzise Schätzung einer Erfolgsquote; verschiedene Gruppengrössen verwenden dieselben Daten erneut.

Bei kleineren Krümmungen reichen die ausgeführten Budgets weiterhin nicht. Die vorab feste obere Modellgrenze hilft bei h=0,5. Unbekannte Dichte und freie Stoppregeln bleiben ausgeschlossen; ein flaches Modell mit anderer Dichte kann dieselben Relationen haben. Als Nächstes sind eine externe Prüfung und Replikation sinnvoll. Weitere Effizienzarbeit braucht wieder eine endliche Absicherung vor zusätzlichen Grossläufen.

- [Ergebnisse und Präzisionsgrenzen](https://github.com/thomasmgfeller/x6-spectral-astrolabium/blob/d9bd4d0266faff0fddd70b4067ad4422367f25a1/research/lorentz_de_sitter_kl/RESULTS.md)
- [Herleitung und Prüfvertrag](https://github.com/thomasmgfeller/x6-spectral-astrolabium/blob/d9bd4d0266faff0fddd70b4067ad4422367f25a1/research/lorentz_de_sitter_kl/DERIVATION.md)

## Weniger Daten durch eine abgesicherte Wolkenvarianz

Die nächste Stufe nutzt die Streuung ganzer Punktwolken. Diese wird aus der bekannten Geometrie mathematisch nach oben begrenzt. Die Rechnung zählt ausdrücklich die Abhängigkeit von Paaren mit einem gemeinsamen Punkt und benötigt keine als sicher behandelte empirische Varianz.

Die neue Bennett-Schranke behält mindestens 95% Überdeckung im bekannten uniformen Modell und bei vorher festem Budget. Gegenüber der KL-Referenz sinken die hinreichenden Budgets um Faktor 2,89 bis 4,10. Bei h=0,5 werden 10.981 statt 31.707 Wolken benötigt; bei h=0,1 bleiben es trotz Verbesserung rund 14,2 Millionen. Diese Planungszahlen sind ausreichende Grenzen, keine optimalen Mindestzahlen.

Der Vertrag wurde vor den Zielrechnungen veröffentlicht. 45.056 neue Wolken wurden vollständig reproduziert. Bei h=0,5 mit je 4.096 Wolken erreichen fünf von acht Bennett-Intervallen die relative 20%-Vorgabe, gegenüber null von acht mit KL. Im gesamten Datensatz von 32.768 Wolken sinkt der relative Radius von 8,88% auf 4,64%. Verschiedene Gruppengrössen verwenden dieselben Daten erneut; kleine Gruppenzahlen liefern keine präzise Erfolgsrate.

Ein Gegenbeispiel bleibt erhalten: In einer Gruppe mit nur 256 Wolken ist Bennett breiter als KL. Die beiden Intervalle werden deshalb nicht ungesichert geschnitten oder nachträglich nach ihrer Breite ausgewählt. Der belegte Budgetgewinn bedeutet keine allgemeine Überlegenheit jeder einzelnen Ausgabe.

Eine zweite geometrische Rechnung über Kugelschnittvolumina prüft die neue Formel gegen. Ein Prüfpaket benennt Beweisstellen und mögliche Fehler für eine externe Begutachtung. Bekannte Dichte, unabhängige Wolken und festes Budget bleiben erforderlich. Bei h=0,5 hilft die obere Modellgrenze; kleine Krümmungen bleiben schwierig. Als Nächstes ist zu klären, wie begrenzte Fehler in Dichte und Zeitskala die Freigabe beeinflussen.

- [Ergebnisse und Gegenbeispiel](https://github.com/thomasmgfeller/x6-spectral-astrolabium/blob/78a150f27fdf52187d140f9fcf440ce29c89cb48/research/lorentz_de_sitter_variance/RESULTS.md)
- [Prüfpaket für externe Begutachtung](https://github.com/thomasmgfeller/x6-spectral-astrolabium/blob/78a150f27fdf52187d140f9fcf440ce29c89cb48/research/lorentz_de_sitter_variance/REVIEW.md)
- [Vollständige Herleitung](https://github.com/thomasmgfeller/x6-spectral-astrolabium/blob/78a150f27fdf52187d140f9fcf440ce29c89cb48/research/lorentz_de_sitter_variance/DERIVATION.md)

## BD gegen C2: Was bedeutet der gestoppte Ausbau?

Die Benincasa–Dowker-Referenz schätzt Krümmung aus der Anzahl von Ereignissen in kleinen kausalen Intervallen. Der abgeschlossene Pilot verwendet eine bekannte physische Dichte und die vorgegebene Eigenzeit T=1 in vierdimensionalen Minkowski- und de-Sitter-Modellen. Die Punktzahlen sind tatsächlich Poisson-verteilt.

384 flache Entwicklungswolken wählen die Glättung; 6.144 weitere Wolken bilden zwölf getrennte Testzellen. Alle 6.528 Wolken wurden vollständig reproduziert, 102 zusätzlich mit einem zweiten Kausalitätstest. Vertrag und Quellen waren vor den Daten lokal in Git fixiert. Die Veröffentlichung erfolgt danach; dies ist keine öffentliche Vorregistrierung.

Im Hauptvergleich beträgt der mittlere quadratische Fehler als Wurzel (RMSE) 14,924 für BD und 0,448 für C2. Das Verhältnis ist 33,34. Die Kriterien für RMSE, Bias und Intervallbreite sowie die flache Bias-Kontrolle scheitern. Überdeckungs- und Kostenkriterium bestehen. Deshalb gilt NO_GO für variable Krümmung innerhalb dieses Budgets.

Das Ergebnis ist begrenzt: C2 kennt die de-Sitter-Modellfamilie und profitiert an der oberen Grenze von der Begrenzung seiner Schätzung. Bei der kleinsten Dichte hat BD in drei Testzellen den kleineren RMSE. Die nominalen Student-Intervalle haben keine bewiesene 95%-Überdeckung, und auch C2 erreicht im Hauptfall die 20%-Breitenvorgabe nicht. Der Vergleich widerlegt weder die BD-Kontinuumsgrenze noch begründet er eine universelle Überlegenheit von C2.

Der damalige BK-Koeffizientenvortest wurde inzwischen durch den getrennten intrinsischen Phase-1/2-Piloten ergänzt; dessen Abnahme scheitert ebenfalls. Details folgen im nächsten Abschnitt. Die BD-Regel −2B(1) ist weiterhin keine Krümmungsformel für den konstantenannihilierenden BK-Operator.

- [Ergebnisse und Grenzen](https://github.com/thomasmgfeller/x6-spectral-astrolabium/blob/49710201cdb2e2941404266b25e88051a659b08e/research/lorentz_bd_reference/RESULTS.md)
- [Methoden und Vertrag](https://github.com/thomasmgfeller/x6-spectral-astrolabium/blob/49710201cdb2e2941404266b25e88051a659b08e/research/lorentz_bd_reference/METHODS.md)
- [Prüfprotokoll](https://github.com/thomasmgfeller/x6-spectral-astrolabium/blob/49710201cdb2e2941404266b25e88051a659b08e/research/lorentz_bd_reference/VERIFICATION.json)
- [BK Phase 1/2: Ergebnisse](https://github.com/thomasmgfeller/x6-spectral-astrolabium/blob/e947dfbdd49890dcb119940548537d1db59272c2/research/lorentz_local_dalembert/PHASE12_RESULTS.md)

## BK Phase 1/2: Was trägt die intrinsische Rekonstruktion?

Der lokale Boguñá–Krioukov-Pilot implementiert Nachbarschaften aus längsten Ketten und Kausalüberlappungen. Die eigentliche Rekonstruktion erhält Kausalordnung, bekannte Dichte und unabhängige Zufallsmarken für Gleichstände. Einbettungskoordinaten werden nur zum Simulieren und Prüfen benutzt. Untersucht wird zunächst 2+1-dimensionaler flacher Minkowski-Raum.

Protokoll und danach Implementierung samt Auswertung wurden vor den jeweiligen Daten öffentlich fixiert. Auf sechs Entwicklungswolken folgen 48 getrennte Testwolken, je 16 bei drei Dichten. Alle Testwolken wurden vollständig nachgerechnet; Produktidentität, konstante Felder, affine Kartenwechsel und drei Umnummerierungsprüfungen bestehen.

Bei der höchsten Dichte sinkt der relative Raumabstandsfehler auf 0,104, bedingt auf erfolgreiche Ankersuche. Gleichzeitig fehlen im Mittel 87,8 Prozent der Abstandsschätzungen, und die Auswahl findet nur 15,1 Prozent der gewünschten lokalen Kappenpunkte. Gute Rangkorrelation der verbleibenden Paare ist daher noch keine gute Nachbarschaft.

Nur 3 von 16 dichten Wolken liefern einen verwendbaren Operator. Der relative Metrik-RMS-Fehler beträgt 3,110 mit glatten Testkoordinaten und 5,524 mit intrinsisch erzeugten Koordinaten; verlangt waren höchstens 0,5. Die richtige Signatur gelingt jeweils in 2 von 16 Wolken. Deshalb gilt HOLD_PHASE3.

Das ist ein negativer Befund für diesen begrenzten Such- und Skalenplan, kein Gegenbeweis zum BK-Kontinuumsgrenzwert. Ein nächster Versuch braucht bessere Suchabdeckung, ausreichende Populationen, einen neuen Vertrag und frische Testdaten. Der BD-C2-NO_GO wird dadurch nicht geändert.

- [Results / Ergebnisse](https://github.com/thomasmgfeller/x6-spectral-astrolabium/blob/e947dfbdd49890dcb119940548537d1db59272c2/research/lorentz_local_dalembert/PHASE12_RESULTS.md)
- [Protocol / Protokoll](https://github.com/thomasmgfeller/x6-spectral-astrolabium/blob/e947dfbdd49890dcb119940548537d1db59272c2/research/lorentz_local_dalembert/phase12/PROTOCOL.md)
- [Data / Daten](https://github.com/thomasmgfeller/x6-spectral-astrolabium/blob/e947dfbdd49890dcb119940548537d1db59272c2/research/lorentz_local_dalembert/phase12/results/summary.json)

## BK-Ankersuche: mehr Nachbarn, aber noch keine genaue Metrik

Am 19. Oktober wurde der Suchengpass mit 48 neuen Punktwolken isoliert geprüft. Bisher wurden zuerst 64 Anker gewählt und erst danach auf Eignung geprüft. Die neue Variante prüft zuerst die unveränderten Kriterien und begrenzt danach auf 64 geeignete Anker. Protokoll und Rechenquellen waren vor den jeweiligen Daten öffentlich fixiert.

Bei der höchsten Dichte liefern jetzt 16 von 16 Wolken verwendbare Nachbarschaften, gegenüber 2 von 16 mit der alten Suche auf denselben neuen Daten. Der Anteil wiedergefundener wahrer Nachbarschaftspunkte steigt von 11,5 auf 94,9 Prozent. Allerdings liegen nur 68,3 Prozent aller ausgewählten Punkte tatsächlich in der gewünschten Nachbarschaft.

Der Metrikfehler steigt im neuen Verfahren auf 7,326, weit über die ursprüngliche Grenze 0,5. Auch wenn die Nachbarn anhand der exakten Simulationsabstände gewählt werden, bleibt der Fehler bei 6,012. Diese Kontrolle ist kein intrinsisches Verfahren; sie zeigt, dass eine bessere Ankersuche allein nicht genügt. Vergleiche auf der gemeinsam verfügbaren Teilmenge sind im Bericht separat ausgewiesen.

Alle 48 neuen Testwolken wurden vollständig wiederholt. Ergebnis: bessere Suchabdeckung, weiterhin HOLD_PHASE3. Als nächster Schritt sollen die Zeit- und Raummomente der diskreten Schablone getrennt geprüft werden. Die früheren Daten, der BD-C2-NO_GO und die beendeten Hintergrundläufe bleiben unverändert.

- [Results / Ergebnisse](https://github.com/thomasmgfeller/x6-spectral-astrolabium/blob/c58cc26adb2b4a646e3940e417351040b5dc9ff0/research/lorentz_local_dalembert/anchor_audit/RESULTS.md)
- [Protocol / Protokoll](https://github.com/thomasmgfeller/x6-spectral-astrolabium/blob/c58cc26adb2b4a646e3940e417351040b5dc9ff0/research/lorentz_local_dalembert/anchor_audit/PROTOCOL.md)
- [Data / Daten](https://github.com/thomasmgfeller/x6-spectral-astrolabium/blob/c58cc26adb2b4a646e3940e417351040b5dc9ff0/research/lorentz_local_dalembert/anchor_audit/results/summary.json)

## BK-Momentendiagnose: Schalen und Zeitrichtungen als Engpässe

Weitere 48 frische Wolken prüfen alle acht vorab festgelegten Kombinationen von drei Kontrollen: richtige Eigenzeiten der Zeitstützpunkte (T), konstante Eigenzeit aller Schalenpunkte (S) und eine gemeinsame Zeitrichtung für Endpunkte und Schalenreferenzen (D). Die Auswahl bleibt je Arm unverändert. Alle Eingriffe verwenden bekannte Simulationskoordinaten und sind daher diagnostische Kontrollen.

Bei höchster Dichte stehen beide Arme in 16 von 16 Wolken zur Verfügung. Mit allen Kontrollen sinkt der relative Metrik-RMS von 7,387 auf 2,267 bei intrinsischer Nachbarauswahl und von 5,893 auf 1,002 bei exakter Abstandskappe. Beide Restfehler überschreiten die ursprüngliche Grenze 0,5.

Die vollständige faktorielle Fehlerzuordnung weist wesentlich grössere Beiträge für S und D aus als für T. Die Zeitstützpunkte liegen im Mittel bereits nahe der richtigen Eigenzeit; die Schalen besitzen eine systematisch grössere Eigenzeit und erhebliche Streuung. Die exakte Momentenbilanz berücksichtigt auch die gegenseitige Aufhebung von Zeit- und Schalenfehlern.

Das vorab festgelegte Diagnosekriterium ist erfüllt, Phase 3 bleibt auf HOLD. Bei niedriger Dichte verschlechtert die Gesamtkontrolle den intrinsischen Arm sogar. Der nächste Kandidat ist eine intrinsische Schalenkalibrierung über kausale Intervallzählungen, zusammen mit einer Prüfung gemeinsamer Referenzrichtungen. Das erfordert eine neue Entwicklung und frische Validierung. Alle 48 Wolken wurden vollständig wiederholt; frühere wissenschaftliche Dateien und BD-C2 NO_GO bleiben unverändert.

- [Results / Ergebnisse](https://github.com/thomasmgfeller/x6-spectral-astrolabium/blob/d6c9f3d9ddf975cdc6f0c2ce055c5becb1f7a2ee/research/lorentz_local_dalembert/moment_audit/RESULTS.md)
- [Protocol / Protokoll](https://github.com/thomasmgfeller/x6-spectral-astrolabium/blob/d6c9f3d9ddf975cdc6f0c2ce055c5becb1f7a2ee/research/lorentz_local_dalembert/moment_audit/PROTOCOL.md)
- [Data / Daten](https://github.com/thomasmgfeller/x6-spectral-astrolabium/blob/d6c9f3d9ddf975cdc6f0c2ce055c5becb1f7a2ee/research/lorentz_local_dalembert/moment_audit/results/summary.json)

## BK-Schalenkalibrierung: erste intrinsische Gewichtsverbesserung

Der nächste Versuch verwendet die Anzahl der Ereignisse im kausalen Intervall, um die Eigenzeit jedes ausgewählten Schalenpunkts zu schätzen. Daraus entstehen inverse quadratische Gewichte. Die Nachbarn und Referenzrichtungen bleiben unverändert. Der primäre Kandidat braucht nur Kausalordnung und bekannte Dichte, keine Einbettungskoordinaten.

Protokoll und Rechenquellen wurden vor den jeweiligen Daten öffentlich festgelegt. Fünf feste Arme wurden auf 48 frischen Wolken verglichen: ursprüngliche Gewichte, Intervallgewichte nur für Schalen beziehungsweise für Schalen und Zeitpunkte sowie zwei Kontrollen mit exakten Eigenzeiten. Die Kontrollen wählen keine anderen Nachbarn.

Bei höchster Dichte verbessert der primäre Kandidat den Metrik-RMS von 7,089 auf 3,765 und die normierte Drift auf linearen Feldern von 3,692 auf 2,882. Alle 16 Wolken sind verfügbar. Damit bestehen die drei vorab festgelegten Verbesserungsgrenzen gemeinsam; der sekundäre Arm wird nicht nachträglich zum Hauptkandidaten erklärt.

Die richtige Lorentz-Signatur gelingt dennoch nur in 8 von 16 Wolken; der absolute Metrikfehler bleibt über 0,5 und verschwindet in dieser Dichtefolge nicht. Phase 3 bleibt HOLD. Alle 48 Wolken wurden numerisch nachgerechnet; Koordinaten-Bytehashes werden getrennt ausgewiesen. Als nächstes sind gemeinsame Referenzrichtungen und die verbleibenden ersten und zweiten Momente zu untersuchen, mit neuem Protokoll und frischen Testdaten.

- [Results / Ergebnisse](https://github.com/thomasmgfeller/x6-spectral-astrolabium/blob/aa2c3dae7bb7afb564cdf4f08b0fe8f2c64c9bfb/research/lorentz_local_dalembert/volume_shell/RESULTS.md)
- [Protocol / Protokoll](https://github.com/thomasmgfeller/x6-spectral-astrolabium/blob/aa2c3dae7bb7afb564cdf4f08b0fe8f2c64c9bfb/research/lorentz_local_dalembert/volume_shell/PROTOCOL.md)
- [Data / Daten](https://github.com/thomasmgfeller/x6-spectral-astrolabium/blob/aa2c3dae7bb7afb564cdf4f08b0fe8f2c64c9bfb/research/lorentz_local_dalembert/volume_shell/results/summary.json)

## BK: gemeinsame Referenzrichtungen und beide Momente

Die neue Auswahlregel verwendet zwei vorhandene zeitliche Anker, um aus kausalen Intervallzählungen eine gemeinsame Bezugsrichtung zu schätzen. Auf jeder Schale wird der dazu passendste Referenzpunkt gesucht. Die bisherige Überlappungsauswahl und intrinsische Schalengewichtung bleiben erhalten. Einbettungskoordinaten gehen nicht in den primären Kandidaten ein.

Vier vorher festgelegte Arme werden auf 48 frischen Wolken verglichen: ursprüngliche Gewichte, die bisherige Intervallgewichtung als Basis, die neue intrinsische Referenzwahl und eine diagnostische Referenzwahl mit exakten Eigenzeiten. Die letzte Kontrolle verändert nur die Auswahlzeiten, nicht die intrinsischen Kappenabstände oder Schalengewichte; sie ist keine Fehleruntergrenze.

Bei höchster Dichte beträgt der Metrik-RMS 4.840 → 3.709, die normierte Antwort auf lineare Felder 3.271 → 3.085. Verfügbar sind 16 von 16 Wolken, die richtige Lorentz-Signatur entsteht in 14 von 16. Der vorab festgelegte Gesamtentscheid lautet COMMON_AXIS_HOLD. Beide Fehler müssen im gepaarten Vergleich mindestens 25 Prozent sinken; eine bessere Richtung allein genügt nicht.

Protokoll und Quellen einschliesslich Analyse wurden vor den jeweiligen Daten veröffentlicht. Alle 48 Zielwolken wurden vollständig numerisch nachgerechnet; Koordinaten-Bytehashgleichheit wird separat berichtet. Phase 3 bleibt HOLD. Die nächsten Hypothesen müssen erste und zweite Momente gemeinsam berücksichtigen und benötigen ein eigenes Prüfprotokoll.

- [Results / Ergebnisse](https://github.com/thomasmgfeller/x6-spectral-astrolabium/blob/26432e3d4cde20adabb510f17d5639891f4ac642/research/lorentz_local_dalembert/common_axis/RESULTS.md)
- [Protocol / Protokoll](https://github.com/thomasmgfeller/x6-spectral-astrolabium/blob/26432e3d4cde20adabb510f17d5639891f4ac642/research/lorentz_local_dalembert/common_axis/PROTOCOL.md)
- [Data / Daten](https://github.com/thomasmgfeller/x6-spectral-astrolabium/blob/26432e3d4cde20adabb510f17d5639891f4ac642/research/lorentz_local_dalembert/common_axis/results/summary.json)

## BK: gemeinsame Momente sind auf dichten Kappen machbar

Nach dem gescheiterten Referenzrichtungsversuch wird zuerst eine grundsätzliche Frage geprüft: Können die vorhandenen Punkte bei geeigneten Gewichten gleichzeitig lineare Felder vernichten und die vorgegebene Metrik liefern? Diese Diagnose nutzt bekannte Simulationskoordinaten und die Zielmetrik. Passende polynomiale Antworten sind daher Nebenbedingungen, kein unabhängiger Erfolg eines intrinsischen Operators.

Zwei feste Stützpunktmengen werden verglichen: bisherige Kappen und vollständige Kettenschalen. Jeweils bleiben die Zeitgewichte fest, werden bei erhaltenen Vorzeichen freigegeben oder alle Vorzeichen werden freigegeben. Minimiert wird die absolute Gewichtssumme. Jede Lösbarkeitsaussage benötigt einen geprüften primären und dualen Zeugen; Unlösbarkeit benötigt einen separaten trennenden Zeugen.

Bei höchster Dichte erlauben 16 von 16 bisherigen Kappen gemeinsame Momente mit unveränderten negativen Zeitgewichten und nichtnegativen Schalengewichten. Alle 16 erfüllen auch die vorab gesetzte Massengrenze. Die minimale Gewichtssumme beträgt im Mittel 0.845 der bisherigen. Bei niedrigster Dichte gelingt diese feste Regel nur auf 3 von 16 Wolken; sechs Kappen sind unverfügbar und sieben nach den numerischen Zeugen unlösbar.

48 neue Wolken und alle verfügbaren linearen Programme wurden vollständig nachgerechnet. Nicht eindeutige Gewichts- und Dualvektoren dürfen abweichen, müssen aber jeweils gültige Zeugen sein und denselben minimalen Zielwert liefern. Die Diagnose zeigt bei hoher Dichte Spielraum in der Gewichtswahl; eine Konstruktion ohne Einbettungskoordinaten und Tests auf unabhängigen Feldern bleiben offen. Phase 3 bleibt HOLD.

- [Results / Ergebnisse](https://github.com/thomasmgfeller/x6-spectral-astrolabium/blob/5e164bdc0feaf529af34e019f43dfda949c47302/research/lorentz_local_dalembert/moment_feasibility/RESULTS.md)
- [Protocol / Protokoll](https://github.com/thomasmgfeller/x6-spectral-astrolabium/blob/5e164bdc0feaf529af34e019f43dfda949c47302/research/lorentz_local_dalembert/moment_feasibility/PROTOCOL.md)
- [Data / Daten](https://github.com/thomasmgfeller/x6-spectral-astrolabium/blob/5e164bdc0feaf529af34e019f43dfda949c47302/research/lorentz_local_dalembert/moment_feasibility/results/summary.json)

## BK: Landmarkenregel scheitert vor der Kalibrierung

Der nächste feste Versuch leitet ein lokales Bezugssystem ausschließlich aus kausalen Intervallzählungen ab. Drei Landmarken sollen gemeinsam die Koordinatenbasis für eine regulierte Momentenanpassung liefern. Ein zusätzlicher Zählrauschschutz soll instabile Anpassungen abweisen. Bei jedem Ausfall bleiben die bisherigen Intervallgewichte erhalten.

Alle 48 vorab festgelegten Testwolken sind abgeschlossen und vollständig nachgerechnet. Sechs Nachbarschaften bei niedrigster Dichte sind unverfügbar. Auf allen 42 verfügbaren Nachbarschaften fehlt ein zulässiges Landmarken-Triplett. Daher übernehmen beide intrinsischen Varianten in 0 von 48 Wolken neue Gewichte. Bei höchster Dichte bleiben alle drei Fehlerverhältnisse bei 1.0; verlangt war jeweils höchstens 0.75.

Die Auswertung von 20 unabhängigen Sinus- und Kosinusfeldern folgt erst nach der Konstruktion. Ein Vergleich mit bekannten Simulationskoordinaten senkt bei höchster Dichte den Feld-RMS von 27.652 auf 0.964. Dieser diagnostische Erfolg gehört zum koordinatengestützten Vergleich und kann den gescheiterten intrinsischen Ansatz nicht freigeben.

INTRINSIC_MOMENT_HOLD und HOLD_PHASE3 bleiben bestehen. Das Ergebnis verwirft diese konkrete Landmarkenregel in diesem Testbereich. Der Rauschschutz wurde auf den Testwolken nie erreicht und ist damit empirisch noch nicht bewertet. Vor einem neuen Versuch muss die Verfügbarkeit geeigneter Landmarken untersucht werden; Grenzwerte und Testdaten dieses Versuchs bleiben unverändert.

- [Results / Ergebnisse](https://github.com/thomasmgfeller/x6-spectral-astrolabium/blob/694dd9ec0409f35c9c6fd3e835ef187ada72c598/research/lorentz_local_dalembert/intrinsic_moments/RESULTS.md)
- [Protocol / Protokoll](https://github.com/thomasmgfeller/x6-spectral-astrolabium/blob/694dd9ec0409f35c9c6fd3e835ef187ada72c598/research/lorentz_local_dalembert/intrinsic_moments/PROTOCOL.md)
- [Data / Daten](https://github.com/thomasmgfeller/x6-spectral-astrolabium/blob/694dd9ec0409f35c9c6fd3e835ef187ada72c598/research/lorentz_local_dalembert/intrinsic_moments/results/summary.json)
- [Replay](https://github.com/thomasmgfeller/x6-spectral-astrolabium/blob/694dd9ec0409f35c9c6fd3e835ef187ada72c598/research/lorentz_local_dalembert/intrinsic_moments/VERIFICATION.json)

## BK: Warum eine größere Landmarkensuche nicht genügt

Die folgende Diagnose verwendet die bereits bekannten 48 Wolken des gescheiterten Landmarkenversuchs. Sie ist ausdrücklich retrospektiv. Sechs Nachbarschaften bleiben unverfügbar; alle 42 verfügbaren Stützbereiche werden vollständig durchsucht.

Auch ohne die Begrenzung auf 40 Kandidaten findet sich kein zulässiges Dreiergespann. Bei höchster Dichte erreicht der beste kleinste gegenseitige Intervallzählwert nur 2 statt der verlangten 8. Für 31 von 42 Nachbarschaften beweist bereits eine notwendige Zählschranke die Unmöglichkeit: Drei passend getrennte Landmarken benötigen mindestens 27 Zwischenereignisse bis zum äußeren Rand.

Werden Landmarken nur um den Mittelpunkt gesucht, gelingen bei höchster Dichte 16 von 16 Fälle. Diese Lockerung liefert jedoch nicht alle für den Operator benötigten Abstände. Auch exakte Volumenwerte aus Simulationskoordinaten ergeben am vollständigen Stützbereich 0 von 42 zulässigen Gruppen. Damit ist weder Zählrauschen allein noch die 40er-Grenze eine ausreichende Erklärung auf diesen Wolken.

Alle 48 Wolken wurden vollständig wiederholt. Die nächste Konstruktion muss die gemeinsame Abdeckung und ausreichende kausale Tiefe lösen, beispielsweise durch mehr äußeren Raum oder eigenständig entwickelte überlappende Rahmen. Das benötigt eigene Entwicklung, ein öffentliches Protokoll und frische Testdaten. HOLD_PHASE3 bleibt bestehen; die Diagnose qualifiziert keinen neuen Operator.

- [Report / Bericht](https://github.com/thomasmgfeller/x6-spectral-astrolabium/blob/ac519f5e4a83de0e570680fe4cfeb2da133db351/research/lorentz_local_dalembert/landmark_availability/RESULTS.md)
- [Protocol / Protokoll](https://github.com/thomasmgfeller/x6-spectral-astrolabium/blob/ac519f5e4a83de0e570680fe4cfeb2da133db351/research/lorentz_local_dalembert/landmark_availability/PROTOCOL.md)
- [Full replay / Vollständiger Replay](https://github.com/thomasmgfeller/x6-spectral-astrolabium/blob/ac519f5e4a83de0e570680fe4cfeb2da133db351/research/lorentz_local_dalembert/landmark_availability/VERIFICATION.json)

## BK: Mehr äußerer Raum reicht für die Rekonstruktion nicht

48 frische Punktwolken wurden jeweils in drei ineinander liegenden Diamanten untersucht. Die innere Punktwolke, ihre Stützpunkte, Dichte, Gewichte und Prüfregeln bleiben gleich; nur außerhalb kommen unabhängig gestreute Punkte hinzu. Die äußeren Zeitdurchmesser 1, 1.25 und 1.5 waren vorab festgelegt.

Bei höchster Dichte entstehen bei vollständiger Suche passende Landmarkentripel in 0, 10 und schließlich 16 von 16 Fällen. Die äußere Begrenzung war damit tatsächlich ein Hindernis. In der größten Variante liefert die bisherige Suche unter jeweils 40 Kandidaten jedoch nur in 13 Fällen Tripel; daraus entstehen acht zulässige Bezugssysteme. Keines besteht den unveränderten Rauschschutz.

Alle 42 verfügbaren inneren Nachbarschaften besitzen mindestens ein benötigtes Intervall mit weniger als 16 Ereignissen. Ein Intervall zwischen inneren Punkten liegt vollständig im inneren Diamanten. Zusätzliche äußere Punkte können seinen Zählwert deshalb nicht erhöhen. Alle acht Bezugssysteme scheitern außerdem an der Konditionsgrenze, also an der geforderten numerischen Stabilität.

Der Entscheid lautet OUTER_DIAMOND_HOLD. Weitere reine Vergrößerungen können diese festen Supports unter den gleichen Regeln nicht retten. Vor einer neuen Kampagne müssen Supportauswahl, nötige Zählwerte und stabile Bezugssysteme gemeinsam auf Machbarkeit geprüft werden. Adaptive Supports und mehrere überlappende Bezugssysteme sind mögliche neue Verfahren, aber hier nicht validiert. HOLD_PHASE3 bleibt bestehen.

- [Report / Bericht](https://github.com/thomasmgfeller/x6-spectral-astrolabium/blob/6738f129ca31e56a88690a9d17941516ccefb321/research/lorentz_local_dalembert/outer_diamond/RESULTS.md)
- [Protocol / Protokoll](https://github.com/thomasmgfeller/x6-spectral-astrolabium/blob/6738f129ca31e56a88690a9d17941516ccefb321/research/lorentz_local_dalembert/outer_diamond/PROTOCOL.md)
- [Full replay / Vollständiger Replay](https://github.com/thomasmgfeller/x6-spectral-astrolabium/blob/6738f129ca31e56a88690a9d17941516ccefb321/research/lorentz_local_dalembert/outer_diamond/VERIFICATION.json)
