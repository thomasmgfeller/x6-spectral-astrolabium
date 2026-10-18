# Kausale Ordnungen und Raumzeitfragen

Hier geht es um die Frage, welche Struktur in Beziehungen steckt, bevor man eine räumliche Zeichnung voraussetzt.

[English](https://thomasmgfeller.github.io/x6-spectral-astrolabium/wiki/en/causal-orders.md) · [Wiki-Übersicht](https://thomasmgfeller.github.io/x6-spectral-astrolabium/wiki/de/)

Quellenstand: 2026-10-18 · `e5840afa7c7865a48766d1a5366210508a7b1f05`

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
