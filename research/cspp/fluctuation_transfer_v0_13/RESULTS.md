# Ergebnisse: prädiktiver Fluktuationstransfer v0.13

**Der gemeinsame Transfer ist hergeleitet und an zwei vollständig definierten Modellen geprüft. Für die ursprüngliche kompakte Quelle liegen zusätzliche rigorose Ensemble-Momentenschranken vor. Die vollständigen numerischen Ensemble-Mittelwerte und -Kovarianzen dieses ursprünglichen Detektors bleiben offen. METHOD_HOLD und G1 HOLD gelten weiter.**

Alle Werte sind gerundete Anzeigen von Arb/Acb-Intervallen. Die Rohdateien enthalten die vollständigen Einschließungen. Die beiden Kontrollmodelle ersetzen weder die kompakte Quelle noch ihren räumlichen Detektor. Es wurden keine empirischen Kovarianzen angepasst und keine neuen Zufallswolken erzeugt.

## 1. Vorhersage für die unveränderte kompakte Quelle

Für den bisherigen lokalen H1-Adapter enthält die Quellstütze in der vorgeschriebenen History im Mittel genau 21/16 Poisson-Punkte. Mit Wahrscheinlichkeit p0=exp(-21/16) gibt es keinen solchen Punkt. Dann sind beide vollständigen Detektorantworten exakt null. Dieser gemeinsame Nullanteil ist aus der Geometrie vorhergesagt, nicht aus der Anzahl leerer Archivwolken geschätzt.

- Vorhergesagte gemeinsame Nullwahrscheinlichkeit: mindestens **26.91463487 %**.
- Gemeinsame Kovarianzschranke: \(\Sigma\succeq[p_0/(1-p_0)]\mu\mu^*\), mit \(p_0/(1-p_0)\simeq0.368262987072\).
- Gesamtfehler-Momentenmatrix: \(\Sigma+(\mu-c)(\mu-c)^*\succeq p_0cc^*\), mit der vollständigen Kontinuumsreferenz c aus v0.12.

Die folgenden Untergrenzen gelten für die durch A/e normierte Originalantwort. Die letzte Spalte setzt ausdrücklich einen Mittelwertfehler von höchstens 0.001 voraus; sie ist keine unbedingte Varianzuntergrenze bei beliebigem Mittelwert.

| Originalfenster | RMS-Untergrenze | SD-Untergrenze (bedingt) |
|---|---:|---:|
| [3/4, 1] | 0.0107911599 | 0.0120158723 |
| [1, 5/4] | 0.0045552310 | 0.0047215333 |

Die Untergrenzen gelten unabhängig davon, wie genau das gleiche homogene endliche System gelöst wird. Sie gelten für den lokalen H1-Adapter; die nichtlokale Integralprojektion darf nicht mit derselben Quellverlustwahrscheinlichkeit bewertet werden.

## 2. Vollständige Vorhersagen der Poisson-Transferkontrolle

Die zwei Ausgangskanäle der Kontrolle stammen aus einem ausdrücklich definierten kausalen System mit vier Zuständen. Seine zufälligen Kantengewichte verwenden echte überlappende 4D-Intervalle und gemeinsame Poisson-Zählwerte. Die History ist mit diesen Gewichten korreliert. Hintergrundpunkte ändern die Zählwerte, sind aber keine weiteren Lösungszustände. Dies ist daher kein vollständiges Sprinkling des ursprünglichen CSPP-Systems.

| Ausgang | Zielgröße | Realteil | Imaginärteil |
|---|---|---:|---:|
| 1 | Mittelwert | 0.000372109891596 | 0.000186054945798 |
| 1 | Verschiebung | 0.000413071052096 | 0.000206535526048 |
| 2 | Mittelwert | -0.0164781457766 | 0.00549800112238 |
| 2 | Verschiebung | 4.09035905976e-05 | -7.76680871687e-06 |

Die gemeinsame Hermitesche Kovarianz ist:

\[\Sigma\simeq\begin{pmatrix}1.29534863\,10^{-4}&-4.07518006\,10^{-6}-6.28324909\,10^{-6}i\\-4.07518006\,10^{-6}+6.28324909\,10^{-6}i&2.06481262\,10^{-5}\end{pmatrix}.\]

Die Relationsmatrix ist ebenfalls berechnet und von null verschieden:

\[\Pi\simeq\begin{pmatrix}7.77209178\,10^{-5}+1.03627890\,10^{-4}i&-7.47170730\,10^{-6}+5.09805408\,10^{-7}i\\-7.47170730\,10^{-6}+5.09805408\,10^{-7}i&1.63842533\,10^{-5}-1.25033087\,10^{-5}i\end{pmatrix}.\]

Diese Matrix darf bei einer Darstellung durch Real- und Imaginärteile nicht weggelassen werden. Der Nachweis positiver Varianzen und einer positiven Hermiteschen Determinante gelingt mit Intervallen; die Relationsmatrix ist symmetrisch.

## 3. Welche Annahmen verändern die Vorhersage?

Die folgende Tabelle zeigt Gegenrechnungen. Nur die Zeile mit vollständiger gemeinsamer Rechnung beschreibt das festgelegte Kontrollmodell. Entfernte Korrelationen sind Negativkontrollen, keine zulässigen Vereinfachungen.

| Rechnung | Varianz 1 | Varianz 2 | max. Kovarianzfehler | max. Mittelwertfehler |
|---|---:|---:|---:|---:|
| vollständig | 0.0001295349 | 2.064813e-05 | 0 | 0 |
| nur erste Variation | 0.0001285197 | 2.025084e-05 | 1.0152e-06 | 0.00046183 |
| Intervalle unabhängig | 0.0001294108 | 2.174384e-05 | 8.8817e-06 | 0.00046183 |
| Palm-Einfügung fehlt | 0.0001295349 | 1.674635e-05 | 4.6133e-06 | 0.00085529 |
| Operator eingefroren | 1.384754e-11 | 5.003732e-07 | 0.00012953 | 0.00046183 |
| History eingefroren | 0.000128562 | 2.090125e-05 | 4.0172e-06 | 0.00046183 |

Die lineare Vorhersage lässt eine tatsächliche Mittelwertverschiebung aus. Die exakte Summe endet in dieser Kontrolle nach dritter Variationsordnung. Ihre quadratischen und kubischen Beiträge werden vollständig berücksichtigt.

| Rest nach erster Variation | Ausgang 1 | Ausgang 2 |
|---|---:|---:|
| L2-Restobergrenze (aufgerundet) | 0.001030606173 | 0.000223754274 |

Für Mittelwert und Kovarianz gilt nachweislich \(|\Delta\mu_r|\le\delta_r\) und \(|\Delta\Sigma_{rs}|,|\Delta\Pi_{rs}|\le s_r\delta_s+s_s\delta_r+\delta_r\delta_s\). Alle Einträge erfüllen die berechneten Restgrenzen.

Das dritte zentrierte gemeinsame Gewichtsmoment von A, B und H beträgt ungefähr 0.00603775822808 und ist eingeschlossen von null verschieden. Paarweise Momentendaten oder eine Gauß-Schließung würden diese Information verlieren.

## 4. Zusätzliche lösbare Oszillatorkontrolle

Der Oszillator hat omega²=1+xi/4, f=1+xi/5 und g=xi/10 mit xi=-1,+1 und jeweils Wahrscheinlichkeit 1/2. Frequenz und Anfangsdaten sind korreliert. Die Antworten sind analytische Mittel über die ganzen verschobenen Originalfenster; es werden keine Zeitpunktproben als Zeitintegral verwendet.

| Fenster | Mittelwert | Eingefroren | Varianz |
|---|---:|---:|---:|
| [7/4, 2] | -0.34014714333 | -0.298754080193 | 0.0334033552053 |
| [2, 9/4] | -0.562044533538 | -0.524896919751 | 0.0568203662194 |

Die Kovarianz zwischen den Fenstern beträgt 0.0435659371037. Sie folgt exakt aus der gemeinsamen Zweipunktverteilung. Die Kovarianz hat Rang eins. Die erste Variation verfehlt den Mittelwert deutlich; die zweite Ordnung erfasst die Verschiebung wesentlich besser. Für beide Ordnungen sind uniforme Volterra-Restgrenzen hergeleitet und geprüft.

## 5. Reichweite der ursprünglichen Ensemblevorhersage

Für die ursprüngliche lokale kompakte Quelle ist die exakte gemeinsame Pfadmomenten-Hierarchie angegeben, einschließlich identischer Knoten beider Pfade, gemeinsamer Intervalle, Palm-Einfügungen und der vollständigen Detektorfenster. Ihre Pfadlängen- und Poisson-Abschneidereste sind begrenzt:

- Nach Pfadlänge 128: L2-Rest kleiner als 1.75e-48 je Detektorkanal.
- Nach Gesamtpunktzahl 1024: L2-Rest kleiner als 3.12e-28 je Detektorkanal.
- Die noch notwendigen hochdimensionalen räumlichen Integrale und ihre Quadraturfehler sind damit nicht bereits ausgewertet. Es gibt hier noch keine vollständigen numerischen Werte für die ursprünglichen Ensemble-Mittelwerte und -Kovarianzen.

Für den nichtlokalen P1-Adapter ist außerdem eine totale Ensembledefinition offen: Schon die Wahrscheinlichkeit für weniger als vier History-Knoten ist mit 6.10425363021e-31 strikt positiv. Auf solchen Wolken fehlt der vorgeschriebene dreidimensionale Projektionsraum. Diese Zahl ist nur eine bewiesene Teilmenge möglicher Ausfälle, keine vollständige Ausfallquote. Momentengrenzen bei nahezu entarteten Geometrien fehlen ebenfalls. Ausfälle werden weder als Nullsignal eingesetzt noch aus der Stichprobe entfernt.

Ein bedingtes Ensemble erfolgreicher Geometrien wäre eine gesonderte, ausdrücklich zu definierende Zielgröße. Die vollständige unbedingte PU-Vorhersage bleibt MODEL_HOLD.

## 6. Prüfung und reproduzierbare Dateien

- 27 analytische Tests bestanden.
- 105 eingeschlossene Vorhersagegrößen bei 128 und 192 Bit überlappen.
- Größter Komponentenradius der verglichenen exakten Kontrollgrößen: kleiner als 4.1e-27; Anzeigerundung kommt in diesem Bericht hinzu.
- Unabhängige deterministische Summe über 9.655.800 Zählzustände; maximale Abweichung 8.36e-18.
- Ausgelassene Wahrscheinlichkeit der Zählsumme kleiner als 1.07e-25; deren Gleitkommasummation wird nicht als rigoroses zweites Zertifikat ausgegeben.
- Keine empirisch angepassten Parameter, keine neuen Wolken und keine unabhängige Bestätigungsstichprobe.

`kernel.py` implementiert die gemeinsamen Gewichtsmomente, `geometry.py` die sicheren allgemeinen Überlappungsgrenzen, `algebra.py` und `transfer.py` den zufälligen retardierten Transfer mit Restbilanz. `oscillator.py` enthält die zusätzliche Kontrolle. `run.py`, `audit.py` und `verify.py` erzeugen und prüfen alle Zahlen. Vollständige Herleitung, Annahmen, Quellen und Reproduktionsbefehle stehen in README.md.
