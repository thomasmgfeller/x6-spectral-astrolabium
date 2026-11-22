# CST-DUST · Ladungsverteilung des gemeinsam präparierten N15-Ensembles

20. November 2026, Anschluss an [PR #335](https://github.com/thomasmgfeller/x6-spectral-astrolabium/pull/335). Die Rechnung liefert eine normierte Ladungsverteilung in der endlichen Drei-Moden-Randauslese H3 mit ausdrücklich eingeführtem Ladungsregister. Sie enthält die kohärenten Beiträge beider Elternordnungen, beider Randuhrfenster und aller durch die benutzten Gewichte belegten N15-Endtypen. Eine physikalisch eindeutige P3-Verteilung ist mit den gegenwärtigen Eingaben unterbestimmt. Bei identischer Randpräparation, identischem Messregister, unverändertem Ein-Kanten-Zweig und identischen 70 älteren Präfixgewichten bewirken zwei zulässige Fortsetzungen des Kettenzweigs bei der markierten Masse 1/4 rund 4,8 Prozentpunkte Unterschied.

## Festgelegte Präparation und Ladung

Im synchronisierten Versuch aus PR #335 teilen alle maximalen Staubpfade den markierten Eingangsfluss gleich. Auf jedem Typ benutzen wir die dort fixierte Box für alle sieben inneren Uhren mit relativer Halbbreite 1/64 und die positiven Dichtebänder mit ±1 % um MDfᵥ. Das ursprüngliche offene Feldintervall 0 < wᵥ < 1 beschneidet jedes Band. Alle zugänglichen Teile gehen ein, auch wenn eine Box die Feldgrenze schneidet. M ist eine Flussmarkierung in der Referenzpräparation. Die beiden äußeren Uhrfenster haben die ursprüngliche gemeinsame reelle Phase. Die frühere Kollektivdichte am Anfangskragen liegt um r=1/8 oder r=1/4 mit Halbbreite 1/32, die Zukunftsdichte beträgt 1/8.

Der Strom p = −∂S/∂τ verschiebt die vier Anfangsuhren gemeinsam bei festgehaltenen übrigen Feldern. Für Δ⁴=3/722, Y=T/Δ und die retardierten Koeffizienten b gilt

    p = Σᵥ wᵥ Σᵢ∈Anfang bᵢᵥ(Yᵢ−Yᵥ)/(19Δ).

Die sechs geordneten Messklassen sind p<−1, −1≤p<−1/4, −1/4≤p<0, 0<p<1/4, 1/4≤p<1 und p≥1. Ein siebtes Ergebnis ist die Punktladung p=0. Bei den positiven Präparationen hat diese im feinen Feldmaß exakt Gewicht null. Bereits für ein minimales inneres Ereignis ist der Ladungskoeffizient proportional zu 1+δ/Δ und auf beiden Fenstern von null getrennt. Seine Dichte wird über ein stetiges Intervall integriert. Die Klasse {0} ist in der Verteilung für positive Masse daher separat als null angegeben.

## Historiengewichte vor der Stromauslese

Für die Ein-Kanten-Elternordnung ergeben die beiden publizierten Vier-Marken-Zeugen mit lokalen Verhältnissen A:B=1:1 und 1:3 je 928 Löschspalten und 310 Endtypen. Die 72 älteren N13-Marginalen und die beiden archivierten lokalen Verhältnisse werden rational nachgerechnet. Innerhalb einer Spalte gilt das vor der Ladungsauswertung festgelegte gleiche Gewicht je unterschiedlichem Vier-Marken-Orbit.

Für die Dreierkette liefert die unabhängige Rückwärtszählung 634 Löschspalten, 154 N14-Orbits und 206 Endtypen. Die vollständige ältere N14-Gewichtstabelle ist mit der geprüften Vier-Marken-Austauschbarkeit unvereinbar. Der rationale Trennzeuge in `chain.json` ist auf jeder Spalte nichtnegativ und liefert für die vierfach skalierte Zielmarginale exakt −7129/14994. Die neue Kettenfortsetzung erhält sämtliche 70 N13-Präfixgewichte und legt wie beim Ein-Kanten-Zeugen mindestens 10⁻⁸ auf jede Spalte. Die nach der Mindestbelegung verbleibenden Gewichte werden mit einem von p unabhängigen linearen Ziel aus der Spaltenreihenfolge festgelegt. Sie sind eine zusätzliche Modellwahl. Für die Gegenprobe kehren wir die Kostenreihenfolge um. Eine zweite Gegenprobe hält zusätzlich die 154 N14-Gewichte der neuen Basisfortsetzung fest. Alle benutzten positiven Gewichte und Gleichungen sind exakt nachprüfbar. Die früheren Familien mit festen N14-Gewichten werden auf diese Weise nicht als fortsetzbar vorausgesetzt.

Beide Eltern tragen zunächst je 1/2 Amplitudengewicht. 63 Endtypen sind gemeinsam. Auf jedem gemeinsamen Typ addieren sich beide Elternbeiträge zur selben Feldamplitude. Die gemeinsame Familie enthält so 453 verschiedene Endtypen. Für alle 1 048 skalaren Katalogtypen liegen die Ladungsamplituden zur Weiterverwendung vor. Die übrigen 595 erhalten in den hier ausgewerteten Gewichtszeugen kein Gewicht. Die Untersuchung gilt für die N15-Schicht mit den genannten Markierungs- und Austauschregeln.

## Messung und Born-Norm im Referenzraum

Für einen Typ c und ein Ladungsfenster B wird der komplexe Feldbeitrag a(c,B) im ursprünglichen inneren Uhr- und Dichtehilfsmaß mit dem Phasenfaktor exp(iF₄+iS_Staub) integriert. Die gemeinsame positive Eingangs-Gaußfunktion des Skalars liefert den ausgehenden dreidimensionalen Zustand φ꜀ einschließlich seiner Fresnelphase. Im passenden H3-Skalarprodukt ist G(cd)=⟨φ꜀,φ𝒹⟩. Für reale Amplitudengewichte q berechnen wir

    v_B(c) = q(c) a(c,B)
    D(B,B′) = v_B† G v_B′
    P(B | orthogonales Register, H3) = D(B,B) / Σ_A D(A,A).

Löschgewichte, Randuhren und Typen werden kohärent addiert. Die Diagonalisierung der Messklassen ist die ausdrückliche Annahme unterscheidbarer Registerzustände. Ohne ein solches Register gehört beim Zusammenlegen zweier Klassen auch 2 Re D(B,B′) zur Norm. Das Produkt der sieben Uhr-Jakobifaktoren und die sieben tatsächlichen, beschnittenen Dichteintervallbreiten gehen für jeden Typ separat ein. Die gespeicherten Amplituden sind pro positiver Masse durch den gemeinsamen Faktor [(2rᵤ/3) ε M/7]⁷ geteilt, mit rᵤ=1/64 und ε=1/100. Gemeinsame äußere Paketkonstanten sind ebenfalls ausgeklammert. Sämtliche angegebenen Wahrscheinlichkeiten sind Quotienten bei derselben Präparation. Die skalierten Nenner in den JSON-Dateien erlauben keine massenübergreifende Absolutnormierung.

Die 453 Ausgangsgaußfunktionen besitzen paarweise verschiedene exakt berechnete komplexe symmetrische Präzisionsmatrizen. Bei einer generischen reellen Richtung sind auch die 453 Werte der zugehörigen quadratischen Formen verschieden. Auf dieser Geraden sind die Exponentialfunktionen linear unabhängig, wie die Ableitungen nach dem quadrierten Geradenparameter am Ursprung zeigen. Die H3-Grammatrix der Zeugenfamilie ist deshalb strikt positiv definit. Auf dem vollständigen Feldbereich der Typen 39854 und 46509 ist die bare Ladung jeweils strikt positiv bzw. strikt negativ. Für beide Typen schließt eine rationale Intervallrechnung die Auslöschung des jeweiligen Staubfaktors für alle drei Massen und beide Eingangsdichten aus. Neben der Phasenspanne wird das Verhältnis der Hilfsvolumina über beide Uhrfenster verwendet. Bei vollständig zugelassenen Dichtebändern ist das Volumen bei fester äußerer Uhr proportional zu D¹⁴. Damit sind beide Vorzeichensektoren im definierten H3-Register tatsächlich besetzt und sein Normnenner ist positiv. Das gilt auch auf den konvexen Verbindungen der angegebenen strikt positiven Gewichtszeugen. Die physikalische Paarung von Geometrie, Staub und Skalar im P3-Vertrag bleibt offen.

## Verteilung und Kontrollen

Die Tabelle zeigt Prozente für das Sechsklassenregister bei r=1/8, A:B=1:1 und der ersten beschriebenen Kettenfortsetzung. Die Rechenwerte sämtlicher Klassen, beider Dichtezentren und der anderen Gewichte stehen in `distribution.csv`. Werte unter 0,01 % werden hier ohne Anspruch auf exakte Null gezeigt.

| Bare Ladung p | M=1/4 | M=1 | M=4 |
|---|---:|---:|---:|
| p < −1 | <0,01 | <0,01 | 0,56 |
| −1 ≤ p < −1/4 | <0,01 | 1,14 | 0,06 |
| −1/4 ≤ p < 0 | 7,80 | 5,32 | 0,03 |
| 0 < p < 1/4 | 90,62 | 5,75 | 0,15 |
| 1/4 ≤ p < 1 | 1,58 | 86,16 | 3,45 |
| p ≥ 1 | <0,01 | 1,63 | 95,76 |

Im selben Sechsklassenregister ändert sich bei M=1/4 die Gesamtwahrscheinlichkeit aller positiven Ausgänge von 92,20 % auf 97,05 %, wenn nur der Kettenzeuge mit denselben 70 N13-Marginalen ausgetauscht wird. Im zusätzlich betrachteten Zweiklassenregister mit ausschließlich dem Vorzeichen als Record ergibt dieselbe Änderung 92,23 % und 97,05 %. Bei unveränderter Basisfortsetzung zeigt M=1 die Wirkung der Messauflösung besonders deutlich. Das Zweiklassenregister liefert bei r=1/8 und A:B=1:1 rund 92,27 % positive Ergebnisse, das Zusammenfassen der drei positiven Ausgänge des bereits gemessenen Sechsklassenregisters rund 93,55 %. Die beiden Instrumente unterscheiden sich durch die Kohärenz innerhalb eines Vorzeichensektors.

In der Basisreihe trägt auch die Interferenz zwischen positivem und negativem Vorzeichen zur Norm der unregistrierten Amplitude bei. 2 Re D(−,+)/[D(−,−)+D(+,+)] liegt numerisch zwischen rund 0,19 % und 4,02 % für die zwölf angegebenen Basisfälle. Damit kann man die beiden Vorzeichen bei dieser Auslese nicht allein durch Weglassen ihrer Interferenz als klassische Alternativen behandeln. Die Dateien weisen auch die Interferenz der beiden Eltern sowie die rechnerische Kontrolle mit vollständig dephasierten Typen aus.

Bei vollständig staubfreiem Feld und bei leerem Inneren mit ursprünglichem positivem Außenkragen ist p=0 exakt. Direkte Anfangs-Zukunfts-Kopplungen im Strom verschwinden. `joint.json` enthält die beiden separat geprüften Referenzkontrollen. Die volle Vakuumpräparation verändert die Randdichte. Beide Kontrollen prüfen den Nullpunkt des Rechenmodells. Ein positiv geeichter physikalischer Massenstandard wird durch sie nicht bestimmt.

## Numerik und Wiederholung

Die Hauptrechnung rekonstruiert die Skalar-Grammatrizen mit fortgesetzten komplexen Gaußwurzeln. Eine positive Dichte wird für die Ladungsgrenzen analytisch integriert, die kollektive äußere Dichte durch ihren sinc-Faktor. Die übrigen Integrale werden mit verschachtelten, digital gescrambelten Sobol-Punkten und vier festen Scrambles gerechnet. Pro Lappen und Scramble wurden für die Typen der Gewichtszeugen bis zu 4 096 Punkte verwendet, im gesamten Katalog bis zu 1 024. Die beiden Rechenwege stimmen auf dem gemeinsamen 1 024er-Gitter überein. Für die gemeinsame Basisreihe betrug die größte Änderung einer Klassenwahrscheinlichkeit von 1 024 auf 4 096 Punkte rund 0,023 Prozentpunkte. Eine weitere Rechnung bildet die Staubwirkung direkt über die Kanten, zieht alle sieben Dichten und die äußere Dichte und sortiert die Einzelwerte von p unmittelbar ein. Mit zwei neuen Scrambles und je 2 048 Punkten pro Lappen prüft sie die leichte und schwere Masse bei r=1/8 für drei Gewichtsentscheidungen. Die größte festgestellte Abweichung der Klassenwahrscheinlichkeiten beträgt rund 0,010 Prozentpunkte. Dies sind Auflösungs- und Wiederholungskontrollen. Sie liefern kein umfassendes physikalisches Fehlerbudget.

`joint.json` enthält alle Basisverteilungen, die komplexen Dekohärenzmatrizen, die Kontrollrechnungen und Extremwerte entlang der Verbindung der zwei Ein-Kanten-Zeugen. `sensitivity.json` enthält die beiden Kettenvariationen bei festem A:B. `results.json` dokumentiert die getrennte Ein-Kanten-Auswertung. `exact_norm_final.json` enthält die exakten Formmatrizen in Einheiten von β und die Nichtauslöschungszeugen. Die NPZ-Dateien enthalten keine serialisierten Python-Objekte.

Python 3.11+ und die Versionen aus `requirements.txt` genügen. Vor der Wiederholung empfiehlt sich ein einzelner BLAS-Thread. Im entpackten Verzeichnis:

```sh
sha256sum -c SHA256SUMS
OPENBLAS_NUM_THREADS=1 python -B verify.py
```

Die vollständige numerische Neuberechnung ist ebenfalls lokal möglich. Die Befehle schreiben die mitgelieferten Rechenprodukte erneut in das Arbeitsverzeichnis.

```sh
export OPENBLAS_NUM_THREADS=1
python -B weights.py > weights.new.json
python -B chain.py > chain.new.json
python -B scalars.py
python -B integrate.py --all --power 10 --output all_raw.npz
python -B integrate.py --power 12 --output family_raw.npz
python -B integrate.py --combined --power 12 --output combined_raw.npz
python -B evaluate.py --combined > joint.new.json
python -B sensitivity.py > sensitivity.new.json
```

Die lokal festgehaltenen Designs dokumentieren, wann die Zwei-Eltern-Fortsetzung und die Gewichtsvariationen ergänzt wurden. Es gab keine öffentliche Vorregistrierung. Die Eingaben sind mit Git-Blob-Kennungen in `sources.json` an den veröffentlichten Stand gebunden. Der nächste physikalische Entscheid benötigt eine unabhängige Festlegung oder kontrollierte Eingrenzung der Wachstumsgewichte sowie eine aus der gekoppelten Dynamik begründete Ladungsregistrierung und Paarung. Zur Umrechnung von p in P3-Ruhemasse fehlt zusätzlich eine unabhängige positive Schnittmasse mit dort gemessener Ladung. Alle 60 P3-Checkpoints stehen auf NOT_RUN.

[Gemeinsame Staubpräparation](https://github.com/thomasmgfeller/x6-spectral-astrolabium/tree/6d4bc7967cb0d8b43c4d5bdf84fc68b40775e4ad/research/rax_cqg/dust_collapse/synchronized_distributed_dust_v0_1) · [Vier austauschbare Marken](https://github.com/thomasmgfeller/x6-spectral-astrolabium/tree/6d4bc7967cb0d8b43c4d5bdf84fc68b40775e4ad/research/rax_cqg/dust_collapse/prefix_1564_four_mark_extension_v0_1) · [Zwei Elternordnungen](https://github.com/thomasmgfeller/x6-spectral-astrolabium/tree/6d4bc7967cb0d8b43c4d5bdf84fc68b40775e4ad/research/rax_cqg/dust_collapse/extension_stability_v0_10) · [Physikalischer Randvertrag](https://github.com/thomasmgfeller/x6-spectral-astrolabium/tree/6d4bc7967cb0d8b43c4d5bdf84fc68b40775e4ad/research/rax_cqg/dust_collapse/physical_boundary_readout_v0_1)
