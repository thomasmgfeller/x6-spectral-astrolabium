# Vier n=6-Restkollisionen: Separatoren und Grenzen

Alle vier Kollisionspaare nach Ergänzung der Minimal-/Maximalanzahlen sind
getrennt. Die gerichteten Gradpaare `D` genügen; sogar die einzelne ganze Zahl
`W_future` trennt jedes dieser vier Paare. Das ist eine endliche Aussage über
den vollständig geprüften n=6-Korpus. Drei Paare sind Zeitumkehrungen voneinander.

Die [ausgeführte Abnahme](ACCEPTANCE.md) belegt den frischen lokalen Checkout und
den erfolgreichen CI-Lauf ohne Netzwerk mit identischem vollständigem Bundle.

## Ausführen und erwartetes Ergebnis

Aus dem Repository-Hauptverzeichnis, Python 3.12, ausschließlich Standardbibliothek:

```sh
python3 -S -B research/lorentz_n6_residuals/verify.py --output /tmp/lorentz-residuals.json
python3 -S -B research/lorentz_n6_residuals/verify.py --verify-report /tmp/lorentz-residuals.json
```

Erwartet: Exit 0, `PASS_WITH_SCOPE_LIMITS`, `primary_pairs_resolved=4`,
`primary_pairs_unresolved=0`, 36 mit Wolfram verglichene Polynome, 6 Wolfram-Prüfungen,
5.760 Umbenennungen und 17 abgelehnte Fehlerkontrollen. Eine fehlende oder veränderte
Ergebniszeile scheitert mit Exit 1. `-O` entfernt keine Prüfungen.
Der Prüfer ruft weder Wolfram noch das Netzwerk auf.

Die gemeinsame [Offline-Referenzsuite](../../docs/OFFLINE_REFERENCE.md) enthält
zusätzlich den Bericht `lorentz-residuals.json` und läuft bei relevanten Änderungen
in der GitHub-CI mit getrenntem Netzwerk-Namespace:

```sh
python3 -S -B x6.py reference qualify --output /tmp/x6-reference-evidence
```

## Konventionen und Ergebnis je Paar

`C[i][j]=1` bedeutet `i < j` in der Ordnung: **die vollständige transitive Relation**,
nicht nur Hasse-Kanten. Es gelten `S=C+Cᵀ`, `A=C−Cᵀ` und
`K=SA−AS=2(CᵀC−CCᵀ)`. Polynome sind monisch, `det(tI−M)`, mit ganzzahligen
Koeffizienten in absteigender Reihenfolge.

`F0=(n, χS, χA, χK, n_min, n_max)` ist die bisherige Signatur.
`D=sort{(d⁻(v),d⁺(v)):v∈P}` enthält die gepaarten Vergangenheits-/Zukunftsgrößen
**mit Multiplizitäten**. Ein Zeitumkehrpaar wird nicht als isomorph identifiziert.

\[
W_+(P)=\sum_v {d^+(v)\choose2},\qquad
W_-(P)=\sum_v {d^-(v)\choose2}.
\]

`W_future=W+` zählt Tripel aus einem gemeinsamen Vorgänger und einem ungeordneten
Paar seiner Nachfolger. `W_past=W−` zählt die umgekehrte Situation. Bei Höhe zwei
sind das induzierte Gabeln. Bei größeren Höhen dürfen die beiden Nachfolger
vergleichbar sein. Beide Zahlen sind aus `D` abgeleitet, keine unabhängigen Daten.

| Paar, Reihenfolge links/rechts | W+ links / rechts | W− links / rechts | Zeitumkehr-isomorph? | Ergebnis |
| --- | ---: | ---: | --- | --- |
| `n6-0073` / `n6-0181` | 3 / 2 | 3 / 2 | nein | getrennt durch D, W+ und W− |
| `n6-0082` / `n6-0087` | 3 / 2 | 2 / 3 | ja | getrennt durch D, W+ und W− |
| `n6-0099` / `n6-0131` | 4 / 3 | 3 / 4 | ja | getrennt durch D, W+ und W− |
| `n6-0100` / `n6-0135` | 6 / 5 | 5 / 6 | ja | getrennt durch D, W+ und W− |

Für alle acht Ordnungen gilt `(n_min,n_max,n_isoliert)=(3,3,0)` und Höhe zwei.
Innerhalb jedes Paares stimmen alle drei charakteristischen Polynome exakt überein;
ordnungserhaltend isomorph ist keines. Beim ersten Paar unterscheidet zusätzlich
der Zusammenhang: `0073` ist zusammenhängend, `0181` nicht.

| ID | D, als Multimenge; Hochzahl bezeichnet Multiplizität |
| --- | --- |
| `n6-0073` | `(0,1)², (0,3), (1,0)², (3,0)` |
| `n6-0181` | `(0,1), (0,2)², (1,0), (2,0)²` |
| `n6-0082` | `(0,1)², (0,3), (1,0), (2,0)²` |
| `n6-0087` | `(0,1), (0,2)², (1,0)², (3,0)` |
| `n6-0099` | `(0,1), (0,2), (0,3), (2,0)³` |
| `n6-0131` | `(0,2)³, (1,0), (2,0), (3,0)` |
| `n6-0100` | `(0,1), (0,3)², (2,0)², (3,0)` |
| `n6-0135` | `(0,2)², (0,3), (1,0), (3,0)²` |

Die zwölf vollständigen Matrizen stehen in [inputs.json](inputs.json), alle
Polynome und Paarprüfungen in [local-results.json](evidence/local-results.json).
Die Paarliste wird aus dem vollständigen Atlas neu ermittelt und mit der fixierten
Auswahl verglichen; es werden nicht nur vier handverlesene Erfolgsmeldungen geprüft.

## Warum die zusätzliche Zahl hilft

Bei diesen Höhe-zwei-Ordnungen ist nach geeigneter Beschriftung

\[
C=\begin{pmatrix}0&B\\0&0\end{pmatrix},\quad
S=\begin{pmatrix}0&B\\B^T&0\end{pmatrix},\quad
A=\begin{pmatrix}0&B\\-B^T&0\end{pmatrix},\quad
K=\begin{pmatrix}-2BB^T&0\\0&2B^TB\end{pmatrix}.
\]

Für das hier quadratische `B` bestimmen seine Singulärwerte alle drei Spektren;
die drei Spektren tragen in dieser Teilklasse weitgehend dieselbe Information.
Mit `G=BBᵀ` gilt

\[
\chi_S(t)=\det(t^2I-G),\quad \chi_A(t)=\det(t^2I+G),\quad
\chi_K(t)=\det(tI+2G)\det(tI-2G).
\]

Dagegen ist

\[
W_+=\tfrac12\bigl(\|B\mathbf1\|^2-|E|\bigr)
=\tfrac12\bigl(\mathbf1^TB^TB\mathbf1-\mathrm{tr}(B^TB)\bigr).
\]

Darin steckt die Lage des Einsvektors relativ zu den Eigenräumen, die aus den
Eigenwerten allein nicht hervorgeht. Umbenennungen permutieren die Gradpaare und
lassen `D`, `W+`, `W−` invariant. Zeitumkehr vertauscht `W+` und `W−`.
Damit erklärt sich die Trennung der drei Dualpaare, ohne eine neue Spektralgröße
oder Quill-Erweiterung einzuführen.

## Geltungsbereich und konkrete Gegenbeispiele

| Korpus | F0 | F0 + W+ | F0 + W+ + W− | F0 + D |
| --- | ---: | ---: | ---: | ---: |
| Alle 318 n=6-Ordnungen | 314 Klassen | 318 | 318 | 318 |
| Alle 164 n=7-Ordnungen mit Höhe ≤2, einschließlich Isolierter | 158 | 163 | 164 | 164 |
| Ausgewähltes verbundenes n=8-Dualpaar | 1 | 1 | 1 | 1 |

`D` allein bildet bei n=6 nur 311 Klassen: sieben Paare bleiben gleich.
Es ergänzt die Spektren, ersetzt sie also nicht. Aus der Vollständigkeit bei n=6
folgt auch die Trennung gleich großer Ordnungen mit `n<6`: Man kann auf beiden
Seiten gleich viele isolierte Punkte ergänzen. Die Polynome erhalten denselben
Faktor `t`, Endpunktzahlen dieselben Zuschläge, und `W±` bleiben gleich;
isomorphe Ergänzungen erlauben das Kürzen der isolierten Punkte.

Die Höhe-zwei-Enumeration zerlegt jede Ordnung eindeutig in `p` nichtisolierte
minimale, `q` nichtisolierte maximale und `z=7−p−q` isolierte Punkte. Sie prüft alle
binären `p×q`-Matrizen ohne Nullzeilen/-spalten und identifiziert ausschließlich
unabhängige Zeilen-/Spaltenpermutationen. `(p,q,z)` bleibt geordnet gespeichert;
das Transponieren zur Beschleunigung der kanonischen Wortbildung identifiziert
keine Zeitrichtungen. Dazu kommt die leere Relation. Stratumzahlen und sämtliche
Restkollisionen stehen im Ergebnis. Dies ist **keine vollständige n=7-Enumeration**.

Das gespeicherte n=7-Paar hat die Blöcke

\[
B_{7a}=\begin{pmatrix}0&0&1\\0&0&1\\0&1&1\\1&0&1\end{pmatrix},\qquad
B_{7b}=\begin{pmatrix}0&0&1\\0&1&0\\1&0&1\\1&0&1\end{pmatrix}.
\]

Beide haben `W+=2`, aber `W−=6` beziehungsweise `4`. Damit ist die unbeschränkte
Fortsetzung des einzelnen Zukunftsseparators bereits bei sieben Punkten widerlegt.

Für n=8 verwenden wir `C(B8)` und `C(B8ᵀ)` mit

\[
B_8=\begin{pmatrix}0&0&0&1\\0&0&0&1\\0&1&1&0\\1&0&1&1\end{pmatrix}.
\]

Beide Ordnungen sind verbunden und nicht isomorph, haben aber dasselbe `F0`,
dasselbe `D` und `W+=W−=4`. Das ist ein explizites Gegenbeispiel auch gegen eine
allgemeine Vollständigkeit der **vollen Gradpaare plus Spektren**.
Es wurde lokal bei aufsteigender, zeilenweiser 16-Bit-Suche als Wort 4459 gefunden;
der Bericht erhebt keinen Anspruch auf eine vollständige n=8-Klassifikation.

## Präzise nächste Hypothese

**H7-bidirectional-moments:** Für strikte endliche Ordnungen `P,Q` gleicher Größe
`n≤7`, bei beibehaltener Zeitrichtung, impliziert die Gleichheit von
`(F0,W+,W−)` eine ordnungserhaltende Isomorphie.

Status: für `n≤6` und für Höhe ≤2 bei `n=7` durch die endlichen Prüfungen gestützt;
**offen für n=7 und Höhe ≥3**. Eine allgemeine Erweiterung auf `n≥8` ist widerlegt.
Die stärkere Datenmenge `D` darf bei der Prüfung dieser komprimierten Hypothese
nicht stillschweigend an die Stelle der beiden Zahlen treten.

Nächste Abnahme: alle 2.045 n=7-Ordnungen unabhängig vollständig erfassen, die
`F0`-Kollisionen mit beiden Zahlen prüfen und jedes verbleibende Paar ausweisen.
Vor diesem Lauf Eingaben, Enumeration, Laufzeitbudget und Abbruchregel festhalten.
Keine Aussage über Kontinuumsrekonstruktion, physische Lorentz-Geometrie oder eine
unabhängige externe Begutachtung folgt aus diesen endlichen Tests.

## Herkunft, Wolfram-Evidenz und Fehlerkontrollen

Der Atlas stammt unverändert aus `research/lorentz-v1-workpackages`, Commit
`f5116b9970a6b7dc788c18623a8386b4cde33ad4`; siehe seine
[Provenienz](../../references/causal-order-n6/PROVENANCE.json).
Der Separator `0073/0181` war bereits in `research/x6-fingerprint-v1`, Commit
`f22030f2dae0aa670cdbc450c5e881ce250b36b8`, `research/fingerprint_v1/README.md`
vorhanden. Er wird hier bestätigt und auf alle Restpaare erweitert.

Yazdi, Letizia und Kempf, [*Lorentzian Spectral Geometry with Causal Sets*](https://arxiv.org/abs/2008.02291),
Abschnitt 3.2 und Tabelle 2, definieren bereits gepaarte Ein-/Ausgangsgrade und
berichten die vollständige Trennung mit Spektren bis n=7. Bei n=8 bleiben dort
Kollisionen. Die Verwendung von `D` ist daher eine Replikation. Unser konkreter
Zusatz sind die prüfbaren vier Paarzeugen, die Kompression zu `W±` und die
expliziten Grenzen dieser Kompression.

[contract.json](contract.json) und die drei `freeze*.json` dokumentieren die
vor jedem Wolfram-Aufruf festgeschriebenen Quellen. Die lokalen Entdeckungen
waren vorher bekannt: keine nachträgliche Behauptung einer Entdeckungs-Präregistrierung.
Alle drei tatsächlichen Antworten sind unverändert gespeichert:

1. `wolfram_check.wl`: abgeschnittene Textausgabe; als unvollständig abgelehnt.
2. `wolfram_check_compact.wl`: vollständige Ausgabe, aber sechs n=7-Polynome mit
   falschem Leitvorzeichen. `CharacteristicPolynomial[M,t]` verwendet `det(M−tI)`.
   Die lokale Gegenrechnung hat den Unterschied zum fixierten monischen Vertrag
   erkannt; dieser Versuch bleibt ausdrücklich fehlgeschlagen.
3. [wolfram_check_monic.wl](wolfram_check_monic.wl): Multiplikation mit `(-1)^n`;
   alle 36 Polynome und vollständigen Datensätze stimmen mit Python überein.
   Wolfram 15.0.1 verwendet `CharacteristicPolynomial` und `IsomorphicGraphQ` für
   gerichtete Graphen; lokal werden Faddeev–LeVerrier und vollständige, durch
   notwendige Gradbedingungen verkürzte Permutationsprüfungen verwendet.

Zusätzlich rekonstruiert der ursprüngliche unabhängige Atlasprüfer alle 4.824
natürlich beschrifteten Ordnungen und prüft 4.208 Polynome durch Bareiss-Determinanten
und Interpolation. Die neuen drei Polynome werden für alle 318 Repräsentanten
nochmals mit Faddeev–LeVerrier berechnet. Für alle acht Primärfälle werden sämtliche
720 Umbenennungen der Gradpaare geprüft; Wolfram prüft zusätzlich die vollständigen
Merkmale nach umgekehrter Beschriftung für alle zwölf Eingaben.

Die 17 Fehlerkontrollen umfassen beide tatsächlich gescheiterten Wolfram-Versuche,
fehlende Fälle/Paare, falsche Zählung oder K-Normierung, verlorene Multiplizität,
falsche Dualität, verborgenes n=8-Gegenbeispiel, fehlende Prüfungen, Zahl statt
Boolean, falschen Eingabehash, doppelte JSON-Schlüssel/IDs, eine nichttransitive
Hasse-Kette sowie konsistent ersetzte Rohantwort und Ergebnis mit falscher Rechnung.
Ein zusätzlicher Höhe-drei-Fall erkennt ein falsches K-Vorzeichen, das in den
symmetrischen Höhe-zwei-Spektren unsichtbar wäre.

Hashes binden Dateien an den überprüften Checkout; sie belegen weder Urheberschaft
noch einen vergangenen Ausführungszeitpunkt. Veränderte Prüfer und zugleich
veränderte Vertrauensquellen liegen außerhalb dieser Replay-Garantie.
