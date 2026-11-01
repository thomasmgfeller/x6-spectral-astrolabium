# C01 · Unsicherheitsbilanz nach JCGM 100:2008

**Grundlage.** Die acht Arbeitsschritte entsprechen der Reihenfolge in JCGM 100:2008, Abschnitt 8 (gedruckte Seite 27). Abschnitts-, Gleichungs- und Anhangsverweise beziehen sich auf dieses Dokument. Für das Produkt von Verstärkung und Zielmittel wird zusätzlich die Änderung JCGM 100:2008/Amd.1:2026 zur Nichtlinearität berücksichtigt. Entscheidungen zur Konformität stehen gesondert in NACHWEIS.md. Alle unten eingesetzten Zahlen sind synthetische Eingaben. [GUM, vollständiger Originaltext](https://www.bipm.org/documents/20126/2071204/JCGM_100_2008_E.pdf) · [Änderung 2026, Originaltext](https://www.bipm.org/documents/20126/2071204/JCGM_100_Amd1_2026.pdf/18b8a72a-6caf-69e8-8bbd-dd13056a4a84) · [Publikationsverzeichnis](https://www.bipm.org/en/committees/jc/jcgm/publications)

### 1 · Messmodell für eine skalare Ausgangsgröße (§§ 4.1.1–4.1.2)

D = Y − A·P + C. D ist die vorzeichenbehaftete Abweichung des Vergleichswegs vom skalierten Ziel am festgelegten Stützpunkt. Y ist das Vergleichsmittel, P das wissenschaftlich verankerte Zielmittel, A der gemeinsame Gain. C bringt die Abweichung aus der Kalibrier- in die spezifizierte Einsatzkonfiguration. Alle vier Größen sind dimensionslos. Ein ppm bedeutet hier 10⁻⁶ auf der absoluten Wahrscheinlichkeitsskala. Die Toleranz ist |D|≤2 ppm. Der vorzeichenbehaftete Ansatz erhält die Ableitungen auch bei D=0.

P und Y müssen als bereits korrektionsbereinigte Eingangsgrößen aus validierten Untermodellen vorliegen. Das Feldlabor dokumentiert für jede relevante Quelle Messgleichung, angewandte Korrektur, Restunsicherheit und Korrelation. Dazu zählen Quellenstatistik, Verluste bis zur Bezugsebene, spektrale und räumliche Empfindlichkeit, Dunkelereignisse, Nachpulse, Totzeit, Flankenzuordnung, Zählrate und Rückwirkung. Eine bekannte signifikante Abweichung wird mit ihrem Vorzeichen korrigiert. Nur der verbleibende Kalibrier-zu-Einsatz-Transfer geht einmal in C ein. Ein unbekannter Einfluss erhält keine Nullunsicherheit. Die vorliegende ausführbare Variante setzt voraus, dass A und C unabhängig voneinander und vom gemeinsam erhobenen Paar (Y,P) bestimmt wurden. Bei weitergehender Abhängigkeit muss das Vollmodell der gemeinsamen Eingangsgrößen neu ausgewertet werden.

### 2 · Schätzwerte der Eingänge (§§ 4.1.3–4.1.4)

Für n unabhängige, unter Wiederholbedingungen erhobene Blockpaare (Yᵢ,Pᵢ) werden die beiden arithmetischen Mittel y und p verwendet. Jeder Block enthält zusammengehörige **Schätzungen beider Zustände**, etwa aus vorab gepaarten Kalibrierdurchgängen. Die Blockschätzungen unterscheiden sich von den X/Y-Einzelbits im späteren Audit. a ist der korrigierte Wert aus dem Gain-Zertifikat. Bei begründet rechteckig verteilter Transferkorrektur zwischen l und h gilt c=(l+h)/2. In diesem Design werden unterschiedliche Blöcke gleich gewichtet; bei wechselnden Unsicherheiten oder ungleichen Zielgewichten ist ein angepasstes Modell nötig.

### 3 · Standardunsicherheiten (§§ 4.2–4.3)

Typ A nutzt u²(y)=Σ(Yᵢ−y)²/[n(n−1)] und entsprechend u²(p), jeweils mit n−1 Freiheitsgraden. Voraussetzung sind unabhängige Blockpaare und ein stabiler Mittelwert. Typ B nutzt u(a)=Uₐ/kₐ, wenn Zertifikat, Überdeckung und Faktor diese Umrechnung rechtfertigen. Für C mit begründet gleich wahrscheinlichen Werten im Bereich [l,h] gilt u²(c)=(h−l)²/12. Bei anderer Information muss die zugehörige Verteilung ausgewertet werden. Die numerische Beispielroute setzt die Typ-B-Varianzen als ausreichend zuverlässig (effektive Freiheitsgrade unendlich) an. Reale endliche oder unbekannte Zuverlässigkeit erfordert eine erweiterte Rechnung.

### 4 · Kovarianzen (§ 5.2, Gl. 17)

Die Kovarianz der beiden Mittelwerte schätzt das Programm mit u(y,p)=Σ(Yᵢ−y)(Pᵢ−p)/[n(n−1)]. Es protokolliert die vollständige Matrix V in der Eingangsreihenfolge (Y,P,A,C). Weitere Kovarianzen sind nur in dem begründeten unabhängigen Referenzmodell null. Ein gemeinsam benutzter Leistungsstandard, dieselbe Zeitbasis oder derselbe Quellenmonitor kann zusätzliche Kovarianzen erzeugen. Diese Einflüsse müssen explizit als gemeinsame Größen modelliert oder in V nachgewiesen werden. Eine nicht begründete Diagonalmatrix sperrt die Bewertung.

### 5 · Ausgangsschätzwert (§ 4.1.4, Amd.1:2026)

d=y−ap+c. Im implementierten unabhängigen Gain-Modell ist E[AP]=a·p. Bei einem gemeinsam ausgewerteten, korrelierten Gain und Zielmittel gilt dagegen E[AP]=a·p+Cov(A,P). Dann muss auch der Schätzwert auf Nichtlinearität geprüft werden. Das Hinzufügen eines Kovarianzterms allein zur Varianz genügt in diesem Fall nicht.

### 6 · Kombinierte Standardunsicherheit (§§ 5.1–5.2, Gl. 13)

Für den Sensitivitätsvektor J=(1,−a,−p,1) gilt in erster Ordnung u_c²=JVJᵀ. Mit den oben festgelegten Unabhängigkeiten ergibt dies u²(y)+a²u²(p)+p²u²(a)+u²(c)−2a·u(y,p). Ein unabhängiger Produktmomentvergleich ergibt für das zugrunde gelegte Modell die exakte Varianz als u_c²+u²(a)u²(p), wenn die angegebenen Varianzen als Eingangsvarianzen eingesetzt werden. Die Differenz prüft die Vernachlässigung höherer Ordnung. Die projektinterne Rechenschwelle ist 0,001 ppm Unterschied in u; sie ist keine JCGM-Vorgabe. Bei Überschreitung werden beide Werte ausgewiesen und die lineare Überdeckungsrechnung gesperrt. Bei relevanter Nichtlinearität sind höhere Terme oder die Fortpflanzung der gemeinsamen Eingangsverteilung nach JCGM 101 erforderlich. [JCGM 101](https://www.bipm.org/en/doi/10.59161/jcgm101-2008)

### 7 · Erweiterte Unsicherheit (§ 6, Gl. 18 und Anhang G.4/G.6)

Für den angenähert normal verteilten Blockkontrast Q=Y−aP gilt vQ=u²(y)+a²u²(p)−2a·u(y,p). Seine Typ-A-Varianzschätzung stammt aus n unabhängigen Blockkontrasten (νQ=n−1). Damit lässt sich Anhang G auf **unabhängige Beitragsgruppen** anwenden. Bei effektiv bekannten Typ-B-Varianzen ergibt sich νeff=u_c⁴/[vQ²/(n−1)]. Für die angeforderte beispielhafte zweiseitige Überdeckung von ungefähr 95 % verwenden wir ν=⌊νeff⌋, k=t₀,₉₇₅(ν) und U=k·u_c. Das ist die GUM-Näherung für die festgelegte Modellklasse. Der Rechner verlangt eine Begründung für die Näherung und sperrt die Ausgabe von U bei dominierendem Rechteckbeitrag (hier projektintern über 10 % der Varianz), zu wenigen Blöcken (unter zehn) oder signifikanter Nichtlinearität. Diese Schwellen sind zusätzliche Ausschlusskriterien, kein Nachweis der Normalität. Für asymmetrische oder schlecht bekannte Eingangsverteilungen ist eine validierte Verteilungsrechnung mit numerisch kontrollierten Quantilen oder eine andere ausgewiesene Überdeckungsmethode nötig. Ein unterstelltes k=2 oder ein ungefähr 95-prozentiges Intervall begründet kein Fehlfreigaberisiko von 2·10⁻⁶.

### 8 · Angabe und Nachvollziehbarkeit (§ 7.2)

Das Rechenbeispiel verwendet 16 synthetische Blockpaare. Die Tabelle zeigt Standardunsicherheiten und vorzeichenbehaftete Sensitivitätsbeiträge. Die Einheit ppm für A bezeichnet hier 10⁻⁶ des dimensionslosen Gain-Faktors.

| Eingangsgröße | Eingangs-Schätzwert | Ermittlung | Standardunsicherheit in ppm | Sensitivität | cᵢuᵢ in ppm |
|---|---:|---|---:|---:|---:|
| Y | 0,50000020 | Typ A, Blockmittel | 0,136745 | +1 | +0,136745 |
| P | 0,50000000 | Typ A, Blockmittel | 0,103280 | −1,0000001 | −0,103280 |
| A | 1,00000010 | Typ B, Uₐ=0,16 ppm, kₐ=2 | 0,080000 | −0,5 | −0,040000 |
| C | +0,040 ppm | Typ B, Bereich [−0,010; +0,090] ppm | 0,028868 | +1 | +0,028868 |

Kreuzterm −2a·u(y,p) = −0,016473335 ppm². Zusätzliche Produktvarianz = 6,83·10⁻¹⁷ ppm². Ergebnis für die synthetische Konfiguration: **d=(0,19 ± 0,26) ppm**, u_c=0,124 ppm; U=0,25745 ppm vor Rundung, k=2,07961, νeff=21,20, für die Tabelle ν=21, Überdeckung ungefähr 95 %. Gesonderter Konformitätsnachweis mit den synthetischen externen Intervallen: B=1,40000006 ppm. Letzterer verlangt eigenständige Risikobelege. Die synthetischen Dokumente stellen dafür nur Testeingaben dar.

Das reale Ergebnis lautet **HOLD_GUM_INPUT**. Zu allen Eingangswerten fehlen belastbare Daten der identifizierten Anlage. evaluate.py gibt für die leere Feldvorlage weder d noch u_c noch U aus. Eingangsdaten, Berechnung, V, Sensitivitätsbeiträge, Freiheitsgrade, Überdeckung, Ergebnis und Zusatzprüfungen sind maschinenlesbar im Prüfpaket enthalten. Die Näherung des GUM und der experimentelle Nachweis seiner Anwendbarkeit werden getrennt beurteilt.
