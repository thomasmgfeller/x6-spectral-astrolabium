# Skalarer Fluktuationstransfer zu endlichen Detektoren v0.9

28. Oktober 2026. Neuer, ausdrücklich getrennter Entwicklungsbenchmark.
Die [bisherige Testreihe wird abgeschlossen](CLOSURE.md); G1 bleibt HOLD,
G2/G3 NOT_RUN. Weder eine Quantenrausch-Deutung noch eine Dirac-Freigabe
werden aus den bisherigen Abweichungen abgeleitet.

## Auftrag und erste Ausführung

Quelle, räumlicher Detektor und Testwellenlängen bleiben fest. Zwei neue,
vorab deklarierte endliche Zeitfenster um t=1 machen die zeitliche Korrelation
eines Detektorsignals explizit. Ein koordinatenbasierter retardierter
Auswertungsadapter ist an jedem Punkt des Detektorvolumens definiert.
Seine Integralgewichte und der gesamte History-zu-Detektor-Transfer werden
eingeschlossen berechnet; unabhängige Vorwärts- und Adjungiertenrechnungen
prüfen einander. Keine Glattheit der diskreten Fortsetzung wird vorausgesetzt.

Der erste Lauf verwendet die ersten acht bereits bekannten nu512-Wolken,
epsilon=1/16, m=1, die vier unveränderten Wellen k=0,2,4,8 und die kompakte
Quelle mit H1-History. Beide Zeitfenster benutzen jeweils dieselbe Wolke.
Die 256 Boxen je Fenster, Budgets und Abbruchregeln sind vor der neuen
Integration festgelegt. Es werden keine neuen Zufallswolken erzeugt.

**Vor Produktionsbeginn:** nur synthetische analytische Methodenkontrollen
ausführen, Quellen einfrieren und den Entwicklungsvertrag öffentlich
registrieren. Nach dem festgelegten Lauf werden hier die Ergebnisse ergänzt.
Die unabhängige Bestätigungsserie ist NOT_RUN; sie benötigt einen eigenen
vorher festgelegten Vorhersage- und Statistikvertrag.

## Was dieses Paket leistet und was offen bleibt

- Echte räumliche und zeitliche Einschließung eines definierten linearen
  Detektorsignals, einschließlich aller nicht aufgelösten Randzellen.
- Ein exakter endlicher kausaler Transfer pro Wolke, ohne unbegründete
  Kleinrausch- oder Gaußannahme.
- Getrennte History-, Operator-/Gebiets-, Präzisions- und Integrationskontrollen
  bei den analytisch integrierbaren Wellenreferenzen.
- Eingeschlossene endliche Stichprobenmomente; keine Populationskonfidenz
  aus acht bereits bekannten Entwicklungswolken.
- Ein breites Quadraturintervall ist Integrationsunsicherheit, kein Nachweis
  großer physikalischer Detektorfluktuationen.

Die vollständige analytische Paar-Kovarianzintegration, der prädiktive
Operator-Rauschkern zwischen verschiedenen Beobachtungspunkten und die
kompakte massive Kontinuumsdetektorreferenz bleiben eigenständige Aufgaben.
Die Punktreferenzen der Vorgänger werden nicht als Volumenreferenz ausgegeben.

## Reproduktion

Aus der Repository-Wurzel, Python3.12 und g++:

```bash
python -m pip install -r research/cspp/detector_transfer_v0_9/requirements.txt
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 python -O -B \
  research/cspp/detector_transfer_v0_9/verify_publication.py --preflight
# Nach Vorliegen des veröffentlichten Ergebnispakets:
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 python -O -B \
  research/cspp/detector_transfer_v0_9/verify_publication.py
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 python -B \
  research/cspp/detector_transfer_v0_9/verify_publication.py --replay
```

Der Replay berechnet 128/192-Bit-Produktion und den CPU-Lauf ohne AVX-512
in temporären Verzeichnissen. Er prüft sämtliche benutzten Punktrelationen,
Intervallzahlen und die exakten ganzzahligen Box-/Kugelentscheidungen.
Die unabhängigen Kontrollen enthalten ein analytisches Lichtkegelvolumen,
konstante Kugelintegration, Null-/ULP-Prädikate, negative Kreuzkovarianzen
sowie einen exakt lösbaren stochastischen Transfer mit nachgewiesenem
Linearisierungsrest und Mittelwertverschiebung.

Siehe [METHODS.md](METHODS.md), [PROTOCOL.json](PROTOCOL.json) und
[CLOSURE.md](CLOSURE.md). Eine methodische Analogie zur Optomechanik oder
Festkörperphysik wäre erst der nächste Schritt nach einer ausreichend engen
skalaren Detektorrechnung. Testmassen, Astrometrie und Kosmologie benötigen
zusätzliche physikalische Kopplungen.
