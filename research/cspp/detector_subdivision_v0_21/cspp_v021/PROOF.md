# CSPP v0.21: unterteilter Detektor und monotone Kernhülle

29. Oktober 2026. Ausgangspunkt ist Main-Commit
`22eab46877dc03b1c0f1bee81c2d1d65bbf45d65` (v0.20, PR #152).

## Aussage und festgehaltener Umfang

Dieser Schritt verschärft den direkten, räumlich und zeitlich gemittelten
Detektorbeitrag der bereits vollständig integrierten Historyregion
P = [-6,-5] x [-2,2]^3. Die 256 Wurzelzellen, ihre uniformen KG-Feldhüllen,
die vier archivierten Wolken, Quelle, Modellparameter und Detektor bleiben
unverändert. Die bereits eingeschlossenen Beiträge des bekannten aktiven
Transports und der unbekannten aktiven Außenpfade werden unverändert
übernommen. Neue Poissonpunkte, Zufallsaufrufe oder statistische Regeln gibt
es nicht. Die Detektorunterteilung ist eine deterministische Integration,
keine zusätzliche physikalische Stichprobe.

Die neue Patchschranke ist eine bedingte Erwartungswertschranke. Sie gilt
nicht für den gesamten äußeren Historybereich und ist keine Aussage über
die Genauigkeit einer einzelnen Realisierung. METHOD_HOLD und G1 HOLD
bleiben bestehen. Die unveränderte Vergleichsgröße 0,001 ist kein neu
verteiltes Patchbudget. Der komplementäre Wurzelbereich wird nicht neu
integriert; die globale v0.19-Majorante wird nicht durch Subtraktion eines
Patchwerts verändert.

## 1. Eine exakt bewiesene fallende Hülle

Der unveränderte Schichtkern lautet w(n) = r^n P(n), r=15/16,

    P(n) = 1 - 9n/15 + 8n(n-1)/225 - 4n(n-1)(n-2)/10125.

Bei n=95+x lauten die Koeffizienten von P in aufsteigender x-Potenz:

    [-44944/675, -44063/10125, -256/3375, -4/10125].

Die Koeffizienten von r P(96+x) - P(95+x) sind

    [109/10800, 20843/162000, 49/13500, 1/40500].

Damit ist w(n)<0 und w(n+1)>w(n) für jedes ganzzahlige n>=95;
|w(n)| fällt dort gegen null. Der unendliche Rest ist also analytisch
kontrolliert, nicht durch ein endliches Abbruchkriterium ersetzt.

Definiere die kleinste fallende Majorante auf den ganzen Zahlen:

    H(n) = max_{k>=n} |w(k)|.

Für n<=95 wird sie durch eine endliche Rückwärtsfolge von Maxima exakt
rational berechnet; für n>=95 gilt H(n)=-w(n). H ist nichtnegativ,
fallend und höchstens kappa=4976184375/4294967296. Der größte frühe
Betragswert liegt bei n=8, weitere lokale Spitzen bei 36 und 95.

Für Z~Poisson(mu) ist die neue Hülle

    M(n,mu) = E H(n+Z)
            = -E w(n+Z)
              + exp(-mu) Sum_{k=n}^{94} [H(k)+w(k)] mu^(k-n)/(k-n)!.

Eine leere Summe ist null. E w wird durch dieselbe endliche erzeugende
Funktion wie in v0.19/v0.20 berechnet. Alle Größen werden mit Arb
eingeschlossen. Ein eigener Test wertet die Poissonsumme von H bis 1024
aus und fügt den rigorosen Chernoff-Rest hinzu.

Aus H fallend folgt M fallend in n. Für mu2>=mu1 koppelt man
Z2=Z1+Zextra mit unabhängigen Poissonvariablen der Mittelwerte mu1 und
mu2-mu1; daraus folgt M(n,mu2)<=M(n,mu1). Diese Kopplung beweist eine
Eigenschaft der eindimensionalen Poissonverteilung. Sie behauptet keine
Unabhängigkeit verschiedener räumlicher Intervallzählungen.

Für gemeinsame zulässige Zellparameter n0>=n_min und mu>=mu_min gilt somit

    E |w(n0+Poisson(mu))| <= M(n_min,mu_min).

Es ist keine Unabhängigkeit von n0 und mu nötig. Die gemeinsame zulässige
Menge wird durch einen konservativen Parameterbereich eingeschlossen.
Zusätzlich nehmen wir das Minimum mit kappa und bei Verfeinerung mit
der gültigen Schranke der Elternzelle. Das Minimum gültiger Obergrenzen
bleibt gültig. Die Hülle wird aus dem unveränderten Kern hergeleitet;
sie ändert weder das Modell noch die Fehlerzielgröße.

## 2. Exakte Zählgrenzen über ganze Wurzel- und Detektorboxen

Für eine Box mit Mittelpunkt (t,x), zeitlicher Halblänge ht und räumlichen
Halblängen hj, und einen archivierten Punkt z, seien

    Rmax² = Sum_j (|xj-zj|+hj)²,
    Rmin² = Sum_j max(0,|xj-zj|-hj)².

Die ganze Box liegt strikt vor z, wenn zt-t-ht>0 und
(zt-t-ht)²>Rmax². Eine kausale Beziehung irgendeines Boxpunkts zu z
ist nur möglich, wenn zt-t+ht>0 und (zt-t+ht)²>Rmin². Für eine Box
nach z gelten die vertauschten Zeitdifferenzen. Alle Entscheidungen
erfolgen mit exakten rationalen Darstellungen der ursprünglichen
Binary64-Koordinaten. Es gibt keine numerische Kausalitätstoleranz.

Für ein Wurzel-/Endpunkt-Zellpaar zählt n_min diejenigen Archivpunkte,
die nach allen Wurzeln und vor allen Endpunkten liegen. n_max zählt eine
Obermenge aller möglicherweise dazwischen liegenden Archivpunkte.
So gilt gleichzeitig n_min<=n0(y,d)<=n_max für jedes zulässige Paar.
Die neue monotone Hülle braucht nur n_min; n_max wird zur Kontrolle
ebenfalls ausgewiesen. Eine separate, mit ganzen Zahlen skalierte
Prüfung enumeriert die acht räumlichen Ecken und kontrolliert ausgewählte
Zählbereiche. Deterministische Mittelpunkte dienen ausschließlich als
zusätzliche Kontrollpunkte, niemals als Integrationsersatz.

## 3. Gemeinsame Volumengrenzen

Die geschlossene Intervallüberlappung aus v0.20 wird unverändert benutzt:
für d in B=Omega5 ist I(y,d) Schnitt B = J+(y) Schnitt I(b,d), b=(-5,0).
Die vollständige Formel und ihre Herleitung liegen in evidence/v20_PROOF.md.

Für jede kubische Raumzelle setzen wir lag=ht+(7/4)hx. Weil 7/4>sqrt(3),
liegen y_minus vor sämtlichen Wurzeln und diese vor y_plus. Dasselbe gilt
für d_minus,d_plus der Detektorzelle. Die künstlichen Detektorendpunkte
liegen in B; jede Formelauswertung prüft diese Voraussetzung.

    I(y_plus,d_minus) Teilmenge I(y,d) Teilmenge I(y_minus,d_plus).

Nach Entfernen derselben Menge B bleibt diese Inklusion erhalten.
Daher erhält man mu_min und mu_max aus zwei exakten Überlappungsformeln.
Ein nichtkausales Unterintervall liefert null. Die untere Zahl für die
monotone Auswertung wird nach unten aus dem Arb-Intervall entnommen.
Damit werden n_min und mu_min über dasselbe Produktgebiet begrenzt.
Ihre Extrema müssen nicht beim selben Paar erreicht werden, da M in
beiden Argumenten fällt. Die Doppelpräzisionsrechnung vergleicht sämtliche
physikalischen Volumenintervalle auf Überlappung.

## 4. Der vollständige normierte Kugeldetektor

Der unveränderte Detektor ist die Kugel K mit Zentrum (0,0,3/2), Radius
1/2 und Volumen pi/6, jeweils normiert über W0=[3/4,1] und W1=[1,5/4].
Die umschließende Raumwürfelbox wird je Achse in n=2 und n=4 Teile zerlegt,
das Zeitfenster ebenfalls in n Teile. Das ergibt 16 und 256 Endpunktboxen
je Fenster. Die Kugel wird dadurch nicht zum Würfeldetektor geändert.

Zur eingeschlossenen Gewichtung unterteilen wir die Raumwürfelbox auf
einem festen Gitter mit 128 Teilungen je Achse. Eine kleine Box wird nur
dann als sicher innerhalb der Kugel gezählt, wenn ihre entfernteste Ecke
die Kugelbedingung erfüllt. Dies wird ganzzahlig entschieden. Die Summe
dieser disjunkten Boxvolumina ist eine bewiesene untere Kugelvolumengrenze.
Eine weitere Ganzzahlprüfung liefert die äußere Volumengrenze. Das bekannte
analytische Kugelvolumen pi/6 liegt zwischen beiden.

Die sicheren Teilvolumina werden exakt auf die übergeordneten Detektorboxen
verteilt. Ihre normierten Raum-/Zeitgewichte l_E sind nichtnegative untere
Grenzen der tatsächlichen Detektormassen; der unaufgelöste Kugelrand erhält
die gültige Schranke für die gesamte Kugel. Er wird nicht weggelassen und
die aufgelösten Zellen werden nicht künstlich auf Masse eins renormiert.

Sei K0(C) die neue Kernhülle für die ganze Detektorkugel in einem Fenster
und eine feste Wurzelzelle C. Hier dienen die alten ganzen Kugelpunkte
d_minus=(Fensterbeginn-1/2,Zentrum) und d_plus=(Fensterende+1/2,Zentrum)
als sichere Endpunkte. Jede verfeinerte Schranke K_E(C) wird mit K0 und
der Elternschranke gekappt. Dann ist

    Kavg(C) = K0(C) - Sum_E l_E [K0(C)-K_E(C)]

eine obere Grenze des vollständigen normierten Detektormittels.
Begründung: Die tatsächliche Masse m_E ist >=l_E und die abzuziehende
Verbesserung ist nichtnegativ. Es wird eine **untere Grenze einer
punktweise bewiesenen Verbesserung** abgezogen. Das ist kein Subtrahieren
zweier oberer Fehlergrenzen. Auf nicht aufgelöster Masse verbleibt K0.
Die exakte Massenerhaltung zwischen Eltern und Kindern zusammen mit
K_child<=K_parent garantiert monotone Verfeinerung bei n=2 nach n=4.

## 5. Vollständige Patchbilanz und verbleibende Arbeit

Mit den unveränderten uniformen KG-Zellhüllen U_C aus v0.20 folgt

    D_new = beta rho Sum_C |C| U_C Kavg(C),
    B_P,new = D_new + B_known,v20 + B_unknown,v20.

Die drei Beiträge stehen für direkten Detektor, ausschließlich bekannte
aktive Knoten, beziehungsweise mindestens einen unbekannten aktiven
Außenknoten. Die vollständige Pfadklassifikation und die Mecke-Majorante
für unbekannte Knoten werden aus v0.20 übernommen. Keine neue
Unabhängigkeitsannahme wird eingeführt. Bekannte und unbekannte
Transportterme werden absichtlich unverändert als geprüfte Eingaben
weitergeführt, sodass die Änderung dem direkten Detektorbeitrag zugeordnet
werden kann.

Die Rechnung wird mit 128 und 192 Bit wiederholt. Physikalische Volumina
müssen überlappende Intervalle besitzen. Bei konstruierten Obergrenzen
prüfen wir positive, gültige Zerlegungen und relative Stabilität von 1e-8;
die unterschiedliche Rundung bei der Entnahme oberer Endpunkte ist kein
physikalischer Fehler. Die Rechenradien der Obergrenzen sind nicht die
Breite eines Einschlusses des tatsächlichen Fehlers.

Als nächstes bleibt die vollständige Überdeckung des übrigen endlichen
äußeren Historybereichs einschließlich der räumlichen Flanken außerhalb P.
Diese muss mit einer kompatiblen unendlichen Schwanzmajorante kombiniert
werden, bevor das globale Fehlerziel und die bisherigen Freigabegates neu
bewertet werden können. Die neuen lokalen Ergebnisse allein heben keines
dieser Gates auf.

## Quellen und Provenienz

- Gepinnte v0.20-Projektdateien und Ergebnisse, Git-Blob- und SHA256-
  Identitäten in PROVENANCE.json und evidence/MAIN_TREE.json.
- Die mathematischen Grundlagen für KG-Hülle, exakte Überlappung und
  Pfadtransport sind unverändert in evidence/v20_PROOF.md dokumentiert.
- FLINT / python-flint, Arb-Ballarithmetik und Intervallendpunkte:
  https://python-flint.readthedocs.io/en/latest/arb.html . Der tatsächlich
  verwendete und gepinnte Laufzeitstand ist python-flint 0.8.0.
- Die neue diskrete Hülle und ihre Monotonie werden oben vollständig
  hergeleitet. Ein unabhängiges externes Fachreview wird nicht behauptet.
