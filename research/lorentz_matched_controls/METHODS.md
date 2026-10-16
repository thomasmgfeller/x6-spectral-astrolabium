# Exakter Dichte-/Höhenabgleich: Aussage und Grenzen

## Die neue Frage

PR #40 untersuchte vier Erzeugerfamilien ohne aneinander angepasste
Relationsdichte oder Höhe. Die einfache Trennung geschichteter Kontrollen
konnte deshalb bereits von solchen globalen Unterschieden profitieren.
Der vorliegende Versuch vergleicht jeweils Minkowski-Ziehungen mit einer
Kontrollfamilie bei **exakt gleicher Knotenzahl N, Relationszahl R und Höhe H**.
Er prüft eine endliche bedingte Unterscheidbarkeit. Eine geometrische
Rekonstruktion oder ein Kausalitätseffekt wird daraus nicht abgeleitet.

Die Generatoren, Basismerkmale B, P123-Merkmale und der Klassifikator aus
[PR #40](../lorentz_matching_geometry/README.md) bleiben unverändert.
Alle neuen Ziehungen besitzen einen getrennten Zufallsschlüssel-Namensraum.
Das Vorwissen aus dem früheren negativen Versuch motiviert diese Auswahl;
die Studie ist prospektiv festgelegt, aber nicht verblindet.

## Vorauswahl ohne die zu prüfenden Merkmale

Für jedes N∈{16,36,64}, jede der vier Familien und jeden der beiden getrennten
Trainings-/Testpools werden genau 1.024 Kandidaten erzeugt: insgesamt 24.576.
Die Referenzfamilie ist immer Minkowski; Kontrollen sind Dreischichtordnung,
ausgedünntes Gitter und gestörtes ausgedünntes Gitter.

Innerhalb eines Größen-/Pool-/Kontrollvergleichs werden Kandidaten nach (R,H)
gruppiert. Je Gruppe werden die ersten Kandidaten beider Familien in aufsteigender
Ziehungsnummer gepaart, dann die zweiten usw. Jeder Kandidat kann innerhalb
dieses Vergleichs höchstens einmal vorkommen. Alle so möglichen Paare erhalten
eine festgelegte SHA-256-Priorität aus ihren IDs; die ersten 64 Trainings- und
128 Testpaare bilden die Auswertung. **Die Priorität benutzt weder
Koordinatenwerte, Relationshashes noch Spektren oder Schnittprofile.** Der Hash
ordnet die Auswahl; er entscheidet keine mathematische Gleichheit.

Reichen die verfügbaren Paare in einem der beiden Pools nicht aus, lautet der
Status des gesamten Vergleichs `INSUFFICIENT_COMMON_SUPPORT`. Die vorhandenen
Paare und alle Häufigkeiten werden erhalten, aber es gibt für diese Zelle keine
Leistungsbewertung. Eine nachträgliche Verbreiterung der Toleranz, zusätzliche
Ziehungen oder Wiederholungen derselben Beobachtung sind ausgeschlossen.

Die Auswahl erzeugt eine neue **gemeinsame Teilverteilung**. Sie ist nicht
repräsentativ für die ursprünglichen Erzeugerpopulationen und kann seltene
Ausprägungen bevorzugen. Ein fehlender Abgleich ist eine Aussage über den
begrenzten Pool und das festgelegte Kriterium; er ist kein Nachweis, dass ein
Geometrieindikator erfolgreich arbeitet.

## Warum die D-Kontrolle genau 50 % ergeben muss

Sei D(C)=(R(C)/binomial(N,2), H(C)/N). In jedem ausgewählten Testpaar
(Cᵢ⁰,Cᵢ¹) aus den zwei verschiedenen Familien gilt D(Cᵢ⁰)=D(Cᵢ¹).
Ein deterministischer binärer Klassifikator f, der ausschließlich D sieht,
muss beiden Mitgliedern desselben Paares dasselbe Label zuweisen. Genau eines
dieser beiden Labels ist richtig. Deshalb beträgt seine Trefferquote auf jedem
vollständigen Paar und damit auf dem gesamten balancierten Testsatz genau 1/2.

Auch die Trainingsverteilungen von D sind identisch, einschließlich sämtlicher
Multiplizitäten. Der verwendete Schwerpunkt-Klassifikator bestätigt den
50%-Wert als ausführbare Negativkontrolle. Ein abweichender Wert wäre ein Fehler
in Auswahl, Datenaufteilung, Merkmalsübergabe oder Auswertung. Die Aussage gilt
für denselben deterministischen Entscheider auf beiden Paarmitgliedern;
sie ist kein Verbot zufälliger endlicher Schwankungen eines separat randomisierten
Entscheiders.

Aus dem Erfolg eines anderen Merkmalsvektors folgt allenfalls, dass die
Unterscheidung nicht allein auf **diesen** beiden globalen Größen beruht.
Andere Strukturunterschiede, Randbedingungen, Diskretisierung, lichtartige
Gitterpaare oder die Erzeugervorschrift selbst können weiterhin entscheidend sein.

## Auswertung und statistische Einheit

Pro auswertbarer Zelle gibt es 128 Trainingsordnungen und 256 Testordnungen.
Die Modelle D, B, P123 und B+P123 verwenden dieselbe ausschließlich am Training
berechnete Standardisierung und denselben nächsten Klassenschwerpunkt. Es gibt
keine Parameterwahl anhand des Tests. Die Nullmarke für diese **binäre** Aufgabe
ist 50 %. Die Trefferquote darf nicht direkt mit dem Vierklassenwert aus PR #40
verglichen werden, dessen Nullmarke 25 % betrug.

Die statistische Einheit der Unsicherheitsauswertung ist das **ganze Paar**.
Für Modell m sei

\[
s_i^{(m)}=\frac{\mathbf{1}\{\hat y_i^0=0\}+\mathbf{1}\{\hat y_i^1=1\}}2.
\]

Die gleichgewichtete Klassentrefferquote entspricht dem Mittel dieser Werte.
Der primäre Endpunkt bei N=64, Kontrolle gestörtes Gitter, ist

\[
\Delta=\frac1{128}\sum_i\left(s_i^{(B+P123)}-s_i^{(B)}\right).
\]

Das Bootstrap zieht 2.000-mal vollständige Paare mit Zurücklegen und erhält
damit ihre Kopplung. Erfolg erfordert Δ≥0,05 und eine positive untere Grenze
des 95%-Perzentilintervalls. Der Trainingsdatensatz bleibt dabei fest.
Die Intervalle erfassen weder erneutes Training noch die Unsicherheit durch
neue Kandidatenpools, Matching, andere Erzeuger oder andere Größen.

Alle übrigen Modell-/Größen-/Kontrollvergleiche sind beschreibend. Für ihre
Trefferquoten wird zusätzlich ein exakter einseitiger Labeltauschwert angegeben:
Bei einem Paar mit identischen Vorhersagelabels ist stets genau eine Vorhersage
richtig. Bei gegensätzlichen Vorhersagen sind entweder beide richtig oder beide
falsch. Haben m Paare gegensätzliche Vorhersagen und davon k die richtige
Orientierung, gilt unter einer innerhalb jedes Paars austauschbaren Nullhypothese

\[
p=2^{-m}\sum_{j=k}^{m}\binom mj.
\]

Die Formel wird gegen vollständige Labeltauschaufzählung an 16 kleinen Fällen
geprüft. Sie setzt für die festgehaltenen Vorhersagen die bedingte
Austauschbarkeit voraus. Die zusätzlichen p-Werte sind **nicht** für die vielen
sekundären Vergleiche korrigiert und tragen hier keine konfirmatorischen
Entdeckungsbehauptungen. Ein gemeinsamer Erfolg über mehrere Kontrollen wird
auch deshalb nicht behauptet, weil Minkowski-Beobachtungen zwischen verschiedenen
Kontrollvergleichen wiederverwendet werden dürfen.

## Prüfbarkeit und Evidenzgrenzen

Der vollständige Kandidatenledger enthält IDs, Ziehungsnummern, Generator-
Namensraum, R, H und einen Hash der gesamten gerichteten Relation. Alle
Kandidaten werden vom Prüfer erneut erzeugt; jeder Hash und jedes (R,H) wird
gegengeprüft. Die Höhe wird einmal über Vorgängerreihenfolge, einmal über
iterative Entfernung der Minima berechnet. Die komplette Paarbildung wird
getrennt rekonstruiert und auf fehlende, wiederverwendete oder unpassende
Beobachtungen geprüft.

Für alle in auswertbaren Zellen verwendeten Ordnungen bleiben Koordinaten,
Relationsmatrizen und vollständige Merkmalsvektoren erhalten. Alle übrigen
Kandidaten sind aus Ledger und Quellen reproduzierbar; ihre vollständigen
Matrizen werden nicht zusätzlich dupliziert. Der Prüfer verwendet getrennte
Formeln für Intervalle und Schnittprofile, prüft den Hasse-Abschluss, die
Umnummerierungsinvarianz und einen separaten skalaren Klassifikator.

Quellenfixierung und unveränderte frühere Generatoren begrenzen nachträgliche
Anpassungen. Die Gegenrechnungen stammen dennoch aus demselben Bearbeitungsprozess;
eine personell unabhängige externe Replikation steht aus. Eine bestandene
Softwareprüfung darf sowohl einen negativen Zusatznutzenbefund als auch fehlende
gemeinsame Unterstützung korrekt reproduzieren.
