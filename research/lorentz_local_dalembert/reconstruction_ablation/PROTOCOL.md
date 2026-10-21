# Rekonstruktionsfehler und Diskretisierungsrest trennen

## Aussage und Datenstatus

Dieser Nachfolger von PR #74 analysiert dieselben 64 bereits veröffentlichten
Wolken. Er ist eine **retrospektive Diagnose**, keine neue unabhängige
Validierung. Der frühere Testteil (32, davon 28 vollständig) ist die primäre
Berichtsgruppe; der frühere Kalibrierteil (32, davon 30 vollständig) wird
separat berichtet. Es werden keine Wolken nachgezogen und keine Testdaten
nachträglich als unberührt bezeichnet. Code und Auswertungsregeln werden vor
der ersten Oracle-Auswertung veröffentlicht; die Eingabedaten waren bereits
bekannt. Die vier vorgegebenen Sinus-/Kosinusfelder bleiben unverändert.

## Kontrollierter Eingriff

Für jede bislang vollständige Wolke bleiben Root, Stützpunktidentitäten,
Reihenfolge, lokale Skala s und analytisches Feld fest. Es gibt keine neue
Supportauswahl und keinen Zugriff der Produktionsinferenz auf wahre Koordinaten.
Die rauschfreien Antworten der vorhandenen vier Varianten bleiben archiviert.

Für den Oracle wird genau das vorhandene Minimum-Varianz-Problem auf den
wahren relativen Koordinaten x/s gelöst:

    min aᵀ (I + 11ᵀ) a   unter D(x/s) a = t,
    t = (0,0,0,−2,2,2,0,0,0),
    B = (−sum(a),a)/s².

D enthält die drei linearen, drei quadratischen und drei gemischten Monome.
Die Zielfunktion berücksichtigt den gemeinsamen Rootwert. Sie ist strikt
konvex; bei vollem Zeilenrang ist die Lösung eindeutig. Sie verwendet keine
Feldwerte. Der Oracle ist eine Diagnose mit verborgenen Simulatorinformationen,
kein praktisch verfügbarer Rekonstruktor und kein generelles Optimalitätslimit.

Die vorhandene QP-Lösung wird zusätzlich durch einen unabhängig formulierten
SVD-Minimumnormweg mit Cholesky-Whitening kontrolliert. Rang, Kondition,
Momentbedingungen und KKT-Zertifikat müssen bestehen. Die Bedingungen werden
mit der vorhandenen Grenze 10^5 geprüft; Scheitern wird protokolliert.
Einen Support aufgrund von Wahrheitsdaten zu ersetzen ist ausgeschlossen.

Eine Änderung der bloßen Normierungsskala verändert die physikalischen
Oracle-Koeffizienten in exakter Arithmetik nicht. Ebenso ist das Problem unter
Lorentztransformationen invariant: Der Raum der Polynome bis Grad zwei und
der d'Alembert-Zielvektor transformieren konsistent; die eindeutigen Gewichte
bleiben gleich. Beide Eigenschaften werden auf synthetischen Kontrollen
geprüft. Damit wird kein willkürlicher euklidischer Frameabgleich eingeführt.

## Exakte Zerlegung

Für Original und Relationsprojektion jeweils:

    e = B_rek f − Lf,
    d = B_wahr f − Lf,
    r = (B_rek − B_wahr) f,
    e = d + r,
    mean(e²) = mean(d²) + mean(r²) + 2 mean(d r).

d ist der **Diskretisierungsrest bei wahrer Geometrie und festem Support**.
Er beinhaltet die Folgen dieser diskreten Stützpunktanordnung und des
festgehaltenen Operators. Er isoliert weder einen universellen
Diskretisierungsfehler noch den Effekt einer besseren Supportauswahl.
r ist der durch den Geometrieaustausch verursachte Antwortunterschied bei
gleichem Minimum-Varianz-Verfahren. Original und Projektion besitzen denselben
Oracle. Der vorzeichenbehaftete Kreuzterm kann positiv oder negativ sein;
eine erzwungene Aufteilung in zwei positive Prozentanteile wäre falsch.
Mittelwerte, Varianzen, Kovarianzen und unzentrierte zweite Momente werden
getrennt angegeben. Die Identität wird pro Feld und aggregiert geprüft.

Metadatenkorrekturen ändern die Gewichtspolitik zusätzlich. Deshalb wird ihr
Einfluss c = (B_meta − B_basis) f separat ausgewiesen:

    e_meta = d + r_basis + c.

Alle drei Quadrate und drei Kreuzterme werden berichtet. Es wird kein
Metadatenmodell mit wahren Geometrien nachtrainiert oder außerhalb seines
ursprünglichen Bezugsrahmens als geometrischer Oracle ausgegeben.

## Physikalische Moment- und Taylor-Diagnose

Für jede ebene Welle mit u = k·x wird der Feldkontrast exakt geschrieben als

    f(x) − f(0) = f'(0) u + (1/2) f''(0) u² + remainder(x).

Der Rest ist die Differenz zum vollständigen analytischen Feld, keine
abgeschnittene Näherung. Für jede Gewichtsversion werden lineare Antwort,
quadratische Antwort minus wahrer Ableitung und volle Restantwort getrennt
ausgewertet. Die drei summieren sich zum ursprünglichen Fehler. Beim Oracle
müssen die ersten beiden numerisch null sein. Die physischen Momentfehler
werden direkt auf den wahren Stützkoordinaten geprüft. Das zeigt, ob niedrige
Polynomgrade durch die Rekonstruktion gestört werden.

## Auswertung, Grenzen und Kontrollen

Berichtet werden pro Phase und Feld die gepaarten RMSEs, quadratische
Fehlerzerlegung, Kreuzterme, Fehler des ursprünglichen und projizierten
Operators sowie die beiden Metadatenzusätze. Bootstrap mit 2000 Ziehungen
zieht ganze Wolken samt sämtlichen Feldern und Varianten. Die Intervalle sind
deskriptiv, nicht simultan und keine unabhängige Bestätigung einer neu
ausgewählten Hypothese. Die Felder zählen nicht als zusätzliche Wolken.

Ein vorab deklarierter diagnostischer Hinweis auf geometrischen Spielraum
liegt vor, wenn Oracle/Original-RMSE <0,5 und die obere Grenze des gepaarten
Bootstrapintervalls <1 ist. Dieser Hinweis ersetzt keinen unabhängigen Test
einer tatsächlich implementierbaren Geometriekorrektur.

Kontrollen: Polynome bis Grad zwei, alternative SVD-Lösung, Lorentz- und
Skaleninvarianz, exakte Taylor-Identität, unveränderte Geometrie mit r=0,
kontrollierte Geometrieverzerrung, vorzeichenbehaftete Kreuzterme und ein
rangdefizienter Oracle, der ablehnen muss. Archivdaten werden nicht verändert.
Replays prüfen alle numerischen Größen mit den vorher festgelegten
Toleranzen. Bytehashes dienen Eingabe-/Quellidentität; neu berechnete
Gleitkommazahlen werden numerisch verglichen.

**HOLD_PHASE3, HOLD_EMBEDDING_COVARIANCE und METADATA_HOLD bleiben bestehen.**
Keine neue Dichte, Dimension, Krümmung, Kalman-Verstärkung oder Gerätemessung.

Quellen sind die im Quellmanifest festgeschriebenen vorhandenen Implementierungen
`feasibility.py`, `variance_weights.py`, `cg_inference.py` und die Daten von
`error_calibration`. Die Zerlegungen oben folgen durch Addition/Subtraktion
derselben Oracle-Antwort und vollständiges Ausmultiplizieren.
