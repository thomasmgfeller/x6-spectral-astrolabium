# Bewegte Staubkante, Schnittladung und Seitenfluss

CST-DUST · Endlicher Versuch auf einem offenen Zeit-Raum-Gitter · 25. November 2026

Eine scharfe, nach innen wandernde Grenze zu exakt leerem Raum verletzt auf dem untersuchten Gitter unter den unten angegebenen Rückzugsbedingungen die freie Uhrgleichung. Ein glattes, überall positives Vergleichsprofil trägt eine positive orientierte Schnittladung. Dessen nach innen wandernde Dichteschwelle weist über 7 680 Ticks einen kleinen Nettofluss und erhebliche einander aufhebende Einzelbeiträge auf. Ein Kriterium für eine mitbewegte materielle Oberfläche muss diese Beiträge sowie seine räumliche Zuordnungsregel berücksichtigen.

## Ausgangsdaten

Das Verzeichnis `source/` enthält das unveränderte Prüfpaket „Innen und aussen auf derselben diskreten Staubhistorie“. SHA-256 lautet `0317a41ba23a35e5fe14d47a2fc69895909bc25881fc9bbf0231fc7e8c2723e2`. Der Vorversuch verwendet die endliche Projektwirkung aus dem Quellstand [PR 378](https://github.com/thomasmgfeller/x6-spectral-astrolabium/pull/378) und beschreibt den räumlichen Kontrollträger sowie die selektiven Uhrpulse. Dessen Ergebnisse und 60 P3-Eingangsakten sind im Archiv enthalten. Der vorliegende Anschlussversuch ist explorativ, ohne externe Vorregistrierung. Lauf und Reproduktion benötigen nur Python ab 3.10 mit Standardbibliothek.

## 1. Eine freie Aussenuhr an der bewegten Kante

Auf dem ursprünglichen Gitter gilt für kausal geordnete Ereignisse Δt > 0 und Δt ≥ 12 |Δj|. Die Dichte sei auf der Seite j > R(t) exakt null. Auf der letzten besetzten Station R(t) sei sie positiv. R(t) ist ganzzahlig, geht in Einzelschritten um eine Station zurück und bleibt zwischen zwei Rückzügen mindestens 12 Ticks lang auf derselben Station (Zeitabstand der Sprünge ≥ 12). Wir betrachten ein vollständig im freien räumlichen und zeitlichen Gitterinneren liegendes Wirkungsfenster [t,t+48]. Im letzten Abschnitt (t+36,t+48] erfolgt kein Rückzug. Auch eine konstante Grenze erfüllt diese Bedingungen.

Setze J = R(t+48)+4. In den letzten 12 Ticks erfolgt kein Rückzug, in den davor liegenden drei 12-Tick-Blöcken jeweils höchstens einer. Also J > R(t), und die Teststation (t,J) ist leer. Für einen räumlich nach innen weisenden Versatz −k mit Zeitabstand 12k und k = 1,2,3 gilt R(t+12k) ≤ R(t+48)+3−k. Somit ist J−k > R(t+12k). Die Verzögerung auf der zusätzlichen Kante (13,−1) kann bei monotoner Grenze nur zu einem gleich grossen oder kleineren R führen. Alle nicht nach innen weisenden Zukunftskanten enden ebenfalls im Vakuum. Genau die Kante (48,−4) endet auf der besetzten Station R(t+48). Sie hat drei Zwischenereignisse und den Koeffizienten b = −8. Das Vorgängerpaket leitet die vollständige Liste der 14 wirksamen Verschiebungen aus der Ordnung ab.

Für die Projektwirkung ist 19 ∂S/∂Y am Ausgangspunkt gleich der Summe b w(Empfänger) ΔY über ausgehende Kanten abzüglich der entsprechenden Summe über eingehende Kanten. Alle Eingänge sind hier null, weil ihr Empfänger leer ist. Daher gilt an dieser frei variierten Uhr genau

    19 ∂S/∂Y(t,J) = −8 w(t+48,R(t+48)) [Y(t+48,R(t+48))−Y(t,J)] < 0.

Die Stationarität fordert null. Das Vorzeichen gilt für jede auf der Ordnung streng wachsende Uhr und jede strikt positive Besetzung dieses einen Empfängers. Bei der affinen Uhr Y=h t und Besetzung 1/4 beträgt der Gradient 19 (∂S/∂Y)/h = −96. Amplitude, Messschwelle und Lage einer gewählten Kontrollprobe gehen nicht in das Vorzeichenargument ein.

Der Prüfer erzeugt alle 4 680 Rückzugsfolgen auf 48 Ticks mit Sprungabstand ≥12. Alle 701 Folgen mit der zusätzlichen Ruhephase ergeben denselben Einzelkantenzeugen. Der analytische Beweis gilt für jedes entsprechende Fenster auch auf einer längeren Historie. Bei einem Rückzug um eine Station alle 12 Ticks hat eine leere Aussenstation für alle zwölf Gitterphasen keinen wirksamen besetzten Empfänger. Für diesen Grenzfall liefert die Aussenuhr keinen Widerspruch. Ob die übrigen Feldgleichungen eine solche Front zulassen, bleibt offen.

### Ein einzelnes zusätzliches Geometrieereignis

Beispiel R(t)=32−⌊t/24⌋. Bei (95,31) führt der Zeuge nach (143,27). Wir fügen eine leere Station als einzelnes Ereignis (137,27½) in die bestehende Ordnung ein, nach derselben kausalen Vergleichsregel. Das offene Intervall erhält vier Zwischenereignisse. Sein Koeffizient wechselt von −8 auf 0. An der ursprünglichen Aussenuhr fällt der normierte Gradient von −96 auf 0. Eine spätere freie Aussenuhr bei (167,28) liefert auf der geänderten Ordnung wieder −96. Damit ist das geänderte Beispiel ebenfalls nicht stationär. Diese Variation prüft die Abhängigkeit vom einzelnen Ordnungsintervall. Die zusätzliche Position und ihre Dichte waren vorgegeben. Die Rechnung liefert keine aus einer gekoppelten Wirkung ausgewählte Geometrie.

## 2. Vorzeichenbehaftete Schnitte auf dem glatten Vergleichsprofil

Hier gilt wieder die unveränderte Ordnung des Vorversuchs. Das positive Feld ist w(t,j)=qᵗrʲ/2 mit r=511/512 und der damals ausgewählten langsameren zeitlichen Änderung q≈0,999899084914. Der Prüfer übernimmt die zertifizierte Wurzeleinschliessung und bestätigt ihre Vorzeichenklammer direkt an der Gleichung Σ b d (qᵈrˢ−1)=0. Randdaten und räumlicher Abfall sind vorgegeben. Die freie Gleichung bestimmt q innerhalb dieses Ansatzes.

Wir schreiben den gerichteten Kantenstrom in normierten Einheiten als I = −b d w(Empfänger). Diese Orientierung entspricht dem gemeinsamen Faktor −19/h relativ zum Wirkungsstrom. Sie ergibt auf einer homogenen Eichkontrolle die positive Schnittladung 83 w pro Station. Sie ordnet keine physikalischen Masseneinheiten zu. Q(n,j) summiert I über alle Kanten, die den Zeitschnitt zwischen n und n+1 an der zugewiesenen Station j kreuzen. F(n,k) summiert mit räumlichem Vorzeichen über den Seitenrand zwischen k und k+1 am Tick n. F > 0 bedeutet Fluss nach aussen.

Eine lange Kante überquert mehrere zeitliche und räumliche Zellen. In der Empfängerregel erfolgt ihr räumlicher Wechsel beim Abgang, und ihr zeitlicher Beitrag zählt an der Empfängerstation. In der Senderregel erfolgt der räumliche Wechsel bei Ankunft, und der Zeitbeitrag zählt an der Senderstation. Dies sind zwei diskrete Buchungen derselben Kante. Für beide gilt an den freien Zellen

    Q(n,j)−Q(n−1,j) + F(n,j)−F(n,j−1) = 0.

Für das separierbare Profil sind Q und F jeweils ein fester Faktor mal w(n,j). Die Werte folgen aus den Kanten einzeln. Die Einzelzählung mit unabhängiger Schleifenreihenfolge an drei Schnitten und die lokale Bilanz bestätigen die Berechnung.

| Räumliche Zuordnung des Zeitschnitts | Q/w | F/w bei festem Seitenrand | F/Q pro Tick |
|---|---:|---:|---:|
| Empfängerstation | 60,26534 | −3,10805 | −0,05157281 |
| Senderstation | 60,74607 | −3,13285 | −0,05157281 |

Dass beide normierten Quotienten übereinstimmen, folgt auch aus der lokalen Bilanz und dem separierbaren Feld. Die aus der Kantenliste berechneten absoluten Zuordnungen unterscheiden sich. Die Positivität gilt für dieses Profil und diese beiden Schnitte. Das ist keine allgemeine Positivitätsaussage über die Wirkung.

### Kontrolle mit selektiven Uhrpulsen

Am festen Seitenrand bei Station 2 547 werden die Projektkanten bei Tick 38 400 und 46 080 lokal mit vier Uhrstellungen pro Kante abgefragt. Hinzu kommt bei Tick 46 080 die nach innen gewanderte Schwelle bei Station 2 151. Der Generator berechnet alle betroffenen Kanten der ursprünglichen Wirkung mit dem Vierarm-Verfahren des Vorgängerpakets. Der getrennte Ausleser erhält Endpunkte, Armantworten und Sollabdeckung. Er erhält weder Profilparameter noch Stromvorzeichen. Aus a−b−c+d und dem gemessenen Tickabstand folgt das gerichtete Signal. Pro Arm gilt die vorgegebene absolute Unsicherheit von einer letzten gespeicherten Einheit. Der Prüfer verwirft fehlende und doppelte Kanten.

Die drei Aufnahmen umfassen je 576 verschiedene Kanten, insgesamt 1 728 Vierarmaufnahmen. Sämtliche sechs Intervalle der beiden Zuordnungen schliessen F/Q=−0,05157281 ein und liegen strikt unter null. Sie liegen gemeinsam zwischen −0,051604 und −0,051541. Diese Messungen sind synthetische Wirkungsantworten mit idealen Uhrquellen. Die über 7 680 Ticks summierten Flüsse weiter unten stammen aus der zertifizierten Lösung.

## 3. Bewegte Schwelle und unabhängig bilanzierter Seitenfluss

Die bisherigen fünf Schnitte liegen bei 38 400, 40 320, 42 240, 44 160 und 46 080 Ticks. B bezeichnet die letzte Station oberhalb der jeweiligen Schwelle. In der ersten Auslese wird die Schwelle auf jedem Schnitt als 1 % der dann gemessenen mittleren Dichte der Stationen 190–194 definiert. In der zweiten wird dieselbe Schwelle einmal beim ersten Schnitt festgelegt und anschliessend absolut festgehalten. Das Profil steht für beide vor Beginn der Rechnung fest.

| Tick | Letzte innere Station, relatives Kriterium | Letzte innere Station, feste Anfangsschwelle |
|---:|---:|---:|
| 38 400 | 2 547 | 2 547 |
| 40 320 | 2 547 | 2 448 |
| 42 240 | 2 547 | 2 349 |
| 44 160 | 2 547 | 2 250 |
| 46 080 | 2 547 | 2 151 |

Die feste Anfangsschwelle wechselt 396-mal um eine Station nach innen. Zwischen aufeinanderfolgenden Wechseln liegen 19 oder 20 Ticks. Für jeden einzelnen Tick ist die Schwelle strikt zwischen den Dichteintervallen zweier benachbarter Stationen eingeschlossen. Durch die Separierbarkeit bleibt ein relatives Profil unverändert, während ein fester Amplitudenpegel bei zeitlichem Abfall nach innen wandert. In jeder Zelle gilt weiterhin w > 0.

Bisherige Wandstation k=B(n−1). Beim Rückzug auf k−1 verlässt die Zelle k den Innenbereich. Im Seitenfluss nach aussen wird dann zu F(n,k) der Term +Q(n,k) addiert. Bei ruhender Grenze ist dieser Term null. Als Gegenrechnung wird die Ladungsänderung im endlichen Gebiet 2 100 < j ≤ B mit dem separat bestimmten Fluss am festen linken Rand bilanziert. Beide Wege stimmen an allen vier Folgezeitpunkten für beide Zuordnungen und beide Regeln innerhalb von Intervallschranken überein.

| Definition der Schwelle | Nettofluss nach aussen, 7 680 Ticks | Summe der Beträge der einzelnen Tickflüsse |
|---|---:|---:|
| Jeweils 1 % der aktuellen Innendichte | −275,596 | 275,596 |
| 1 % der anfänglichen Innendichte | −0,446 | 750,767 |

Einheit ist die orientierte Schnittladung einer Zelle bei Station 2 547 am Anfang, jeweils in der verwendeten Zuordnung. Die Beträge werden nach der räumlichen Bilanz jedes Ticks und vor der Zeitsummation gebildet. Diese Grösse hängt von Zeitraster und Wandbuchung ab. Sie misst keine Zahl ausgetauschter Staubteilchen. Eine kleine Nettosumme über das gesamte Fenster allein zertifiziert keine mitbewegte Oberfläche. Der feste räumliche Rand hat in beiden Zuordnungen einen dauerhaften nach innen gerichteten Nettostrom.

## Reproduktion und Geltungsbereich

Im entpackten Verzeichnis:

    sha256sum -c SHA256SUMS
    python -B pruefen.py --vorversuch

Der erste Befehl kontrolliert die Archivdateien. Der zweite reproduziert auch die vollständige vorangegangene Studie. `python -B pruefen.py` allein wiederholt alle neuen Rechnungen und Rohaufnahmen und vergleicht die dekomprimierten Aufnahmedaten und die Ergebnisdatei mit dem Archiv. Alle Vorzeichenprüfungen und numerischen Entscheidungen verwenden rationale Zahlen oder nach aussen gerundete ganzzahlige Intervalle. Freitext und Tabellen runden die Zahlen für die Anzeige.

Der geprüfte Träger hat eine räumliche Dimension und eine festgelegte Ordnung. Die einzelne Variation eines Ordnungsintervalls veranschaulicht, wie ein lokaler Widerspruch unter einer Geometrieänderung verschwinden kann. Die orientierte Schnittsumme ist in diesem Profil positiv und in Modelleinheiten angegeben. Eine nach unabhängiger Präparation bestimmte Staubmasse, eine dynamisch ausgewählte materielle Grenze und ihre intrinsische Fläche bleiben offen. Ein nächster physikalischer Test benötigt eine gekoppelte Ordnungsvariation mit gleicher Randpräparation, eine über solche Variationen verfolgte materielle Oberfläche und einen separat gemessenen Seitenfluss. Der physische P3-Status lautet HOLD_NOT_ELIGIBLE. Alle 60 Prüfpunkte stehen auf NOT_RUN.
