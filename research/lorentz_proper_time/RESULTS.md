# Erster Eigenzeit-Versuch: Ergebnisse und Reichweite

**Die Intervallreferenz erfüllt die vorab festgelegten Hauptkriterien im
deklarierten flachen 1+1-Modell.** Der Lauf umfasst alle 6.912 vorgesehenen
Ordnungen und besteht die interne Gegenprüfung. Die größte exakt auf
Knotenzahl, Relationszahl und Höhe abgeglichene Zusatzkontrolle bleibt
wegen unzureichender Paarzahl ausdrücklich ohne Leistungsbewertung.

Dies qualifiziert einen bekannten, einfach begründeten Referenzschätzer für
eine konkrete synthetische Aufgabe. Es ist kein neues universelles
Geometrieverfahren und keine physikalische Validierung.

## Hauptbefund

Ziel ist theta=tau(p,q)/T zwischen zwei markierten Ereignissen. T und die
Dimension sind vorgegeben. Der Schätzer erhält nur die vollständige Ordnung,
Knotenzahl und Markierungen. V=sqrt(K/m) zählt die K Punkte im strikten
Intervall; m=N−2. Koordinaten und wahre Zielwerte sind bei der Inferenz
ausgeschlossen. Die erlaubten Kalibrierungszielwerte dienen ausschließlich
der D-Regressionsanpassung.

Der unveränderte [Vertrag](contract.json) legt den Hauptvergleich auf
1.024 uniforme Testordnungen bei m=256, also N=258, fest:

| Verfahren | RMSE | MSE | Mittlerer signierter Fehler |
| --- | ---: | ---: | ---: |
| V: Intervallpunktzahl | 0,0316139444 | 0,0009994415 | −0,0030637391 |
| D: globale Dichte-/Höhenregression | 0,1777849593 | 0,0316074918 | −0,0059855380 |
| C0: feste Konstante 64/225 | 0,1767739037 | 0,0312490130 | −0,0059760353 |
| L: lokale längste Kette, beschreibend | 0,0840211413 | 0,0070595522 | −0,0689544153 |

Die RMSE-Einheit ist die dimensionslose normierte Eigenzeit, keine relative
Prozentabweichung zur jeweils wahren Eigenzeit. Das bedingte
95%-Bootstrap-Intervall für RMSE(V) lautet [0,0300678878; 0,0331988034].

Alle Hauptbedingungen sind erfüllt:

| Vorab festgelegtes Kriterium | Ergebnis |
| --- | --- |
| RMSE(V) höchstens 0,05 | 0,0316139444 |
| Mindestens 10 % weniger MSE als D | 96,83796 % weniger |
| Mindestens 10 % weniger MSE als C0 | 96,80169 % weniger |
| Obere 95%-Grenze für MSE(V)−MSE(D) unter null | Intervall [−0,0333647714; −0,0279925844] |
| Obere 95%-Grenze für MSE(V)−MSE(C0) unter null | Intervall [−0,0330077150; −0,0276785215] |
| Vollständigkeit und Integrität | Interne Gegenprüfung PASS |

Die Punktdifferenzen der MSE betragen −0,0306080503 gegenüber D und
−0,0302495716 gegenüber C0. Der Ergebnisstatus lautet
`QUALIFIED_IN_DECLARED_MODEL`. Die 5.000 Bootstrap-Wiederholungen ziehen
ganze Ordnungen; die Kalibrierung bleibt fest. Sie erfassen weder neues
Training noch neue Modellfamilien. Das Kriterium ist die festgelegte
Abnahme dieses Versuchs, keine allgemeine Fehlerschranke.

V nutzt die Markierungen zur lokalen Intervallzählung. D verwendet nur die
zwei globalen Größen und die festgelegten quadratischen Regressionsspalten;
es nutzt keine markierungsbezogenen lokalen Merkmale. Der große Abstand
belegt daher keine Überlegenheit gegenüber allen regressionsbasierten oder
lokalen Vergleichsverfahren und keine algorithmische Neuheit.

## Vollständiger Umfang und beschreibende Größenvergleiche

Je m=64,144,256 gibt es 256 uniforme Kalibrierungsordnungen sowie je 1.024
neue Testordnungen aus uniformem Hintergrund und gestörtem ausgedünntem
Gitter: insgesamt 768 Kalibrierungs- und 6.144 Testordnungen. Jede Ordnung
trägt genau ein markiertes Paar. Alle Ziehungen und auch K=0 bleiben erhalten.

| Familie | m | RMSE(V) | RMSE(D) | RMSE(C0) | RMSE(L) |
| --- | ---: | ---: | ---: | ---: | ---: |
| Uniform | 64 | 0,065643 | 0,166073 | 0,166538 | 0,125788 |
| Gestörtes Gitter | 64 | 0,064294 | 0,176532 | 0,175418 | 0,125646 |
| Uniform | 144 | 0,042153 | 0,171163 | 0,168743 | 0,099594 |
| Gestörtes Gitter | 144 | 0,039113 | 0,171912 | 0,171777 | 0,098497 |
| **Uniform, primär** | **256** | **0,031614** | **0,177785** | **0,176774** | **0,084021** |
| Gestörtes Gitter | 256 | 0,028833 | 0,179855 | 0,179767 | 0,088150 |

Alle Zeilen außer dem vorher bestimmten Hauptvergleich sind beschreibend.
Die endliche Kettenreferenz L wird unverändert verwendet und nicht nach
Sichtung der Daten kalibriert. Die gleichverteilte Binomialrechnung für
K/m betrifft die quadrierte Eigenzeit und gilt nicht automatisch für das
Gitter, für sqrt(K/m) oder für selektierte Teilmengen.

## Exakt abgeglichene Zusatzkontrollen

Das Matching verwendet ausschließlich N,R,H und feste ID-Prioritäten.
Intervallinhalt, Koordinaten, Zielwerte und Vorhersagefehler gehen nicht in
die Auswahl ein. Der Abgleich ist ein Zusatzvergleich zwischen Familien;
er ersetzt die unselektierte Hauptanalyse nicht.

| m | N | Verfügbare Paare | Ausgewählte Paare | Status |
| --- | ---: | ---: | ---: | --- |
| 64 | 66 | 406 | 128 | Auswertbar |
| 144 | 146 | 147 | 128 | Auswertbar |
| 256 | 258 | 63 | 0 | INSUFFICIENT_COMMON_SUPPORT |

Bei m=256 werden keine Toleranzen gelockert, Paare wiederverwendet oder
zusätzlichen Ziehungen nachgeschoben. Aus dieser Zelle folgt keine
Leistungsbehauptung. Die unselektierte Gitterzeile oben darf diese fehlende
Kontrolle nicht ersetzen.

Bei m=64 beträgt RMSE(V) auf den gewählten uniformen/Gitter-Teilmengen
0,070184/0,062126, bei m=144 0,041983/0,046229. Die beschreibende
gepaarte MSE-Differenz Gitter minus uniform lautet −0,00106614
(95%-Intervall [−0,00293288; +0,00068367]) beziehungsweise +0,00037454
([−0,00041737; +0,00115372]). Beide Intervalle enthalten null. Das beweist
keine Gleichwertigkeit. Die Intervalle konditionieren auf die ausgewählten
Paare und die feste Kalibrierung; erneute Poolziehung und Auswahl sind
nicht enthalten.

## Gegenprüfung und Daten

[verification.json](results/verification.json) bestätigt:

- 6.912 vollständige Ordnungen mit separat nachgespielter Zufallserzeugung;
- 6.912 vollständige Relationsprüfungen aus t,x, mit rationaler Auflösung
  numerisch grenznaher Kausalvergleiche;
- getrennte Kettenhöhenrechnung und exakte Rekonstruktion des Matchings;
- 6.912 Umnummerierungen mit transportierten Markierungen;
- 27.648 Vorhersagen für V,L,C0,D, einschließlich der separat gekennzeichneten
  Kalibrierungsdatensätze; die Hauptbewertung nutzt ausschließlich Testdaten;
- separate Regression, Bootstrap-Reduktionen und Prüfung aller Hauptbedingungen;
- 13 Zurückweisungskontrollen sowie Prüfungen gegen unerlaubte Eingaben und
  Einfluss von Testmetadaten auf Inferenz und Matching.

Die beiden numerischen Regressionswege nutzen dieselbe NumPy-Installation.
Getrennte Implementierungen in derselben Autorenschaft und CI-Reproduktion
sind interne Gegenprüfungen, keine externe Replikation.

Das Archiv enthält alle Rohdaten, vollständigen Relationsmatrizen,
Markierungen, Koordinaten als Referenz, Einzelvorhersagen, Fehler,
Modellkoeffizienten, Paarlisten und Zusammenfassungen:

- [records.json.gz](results/records.json.gz): 6.912 vollständige Datensätze;
- [selection.json.gz](results/selection.json.gz): alle Gruppen und verfügbaren
  Paarungen, einschließlich unzureichender Unterstützung;
- [models.json](results/models.json), [summary.json](results/summary.json),
  [verification.json](results/verification.json): Anpassung und Auswertung;
- [RESULTS.json](results/RESULTS.json): ursprüngliche Quellenbindung,
  Ausführungszeiten und SHA-256-Prüfsummen;
- [costs.json](results/costs.json): Einzelbeobachtungen des Ressourcenverbrauchs.

Der erste Lauf benötigte rund 236 Sekunden für Erzeugung und Auswertung
sowie 98 Sekunden für die Gegenprüfung. Der Erzeugungsprozess meldete
549,54 MiB Spitzenspeicher einschließlich Interpreter und Bibliothek.
Dies sind Einzelmessungen und kein Geschwindigkeitsvergleich.

## Chronologie und Reproduktion

Das Design wurde mit [PR #42](https://github.com/thomasmgfeller/x6-spectral-astrolabium/pull/42)
vor dem Datenlauf veröffentlicht. Die ausführbaren Quellen sind unverändert
an [`9aca530`](https://github.com/thomasmgfeller/x6-spectral-astrolabium/commit/9aca530f2bd0b8ec68e7262013a5c8b3c8bce575)
gebunden. Der Quellencommit trägt den Zeitpunkt 16.10.2026, 18:55:28 UTC;
das ursprüngliche Laufprotokoll meldet Beginn 18:55:44 UTC und Abschluss
19:01:19 UTC. Der damalige Arbeitsstand berichtete die Veröffentlichung
des Quellenzweigs vor Ausführung. Ein gesonderter serverseitiger
Push-Eingangszeitnachweis wurde nicht archiviert; ein Commit-Zeitstempel
allein ist kein unabhängiger Nachweis öffentlicher Vorabregistrierung.
Die jetzige Ergebnisintegration ändert weder Vertrag noch Rechenquellen
noch die ursprünglichen Rohdaten. [publication.json](publication.json)
kennzeichnet diese Provenienzgrenze maschinenlesbar.

Linux/POSIX, vollständiger Git-Checkout, Python 3.12 und NumPy 2.3.5:

```sh
python3 -m pip install -r research/lorentz_proper_time/requirements.txt
OPENBLAS_NUM_THREADS=1 python3 -B -O research/lorentz_proper_time/run.py --selftest
OPENBLAS_NUM_THREADS=1 python3 -B -O research/lorentz_proper_time/run.py \
  --run /tmp/x6-proper-time-reproduction \
  --source-ref 9aca530f2bd0b8ec68e7262013a5c8b3c8bce575
python3 research/lorentz_proper_time/compare.py \
  research/lorentz_proper_time/results /tmp/x6-proper-time-reproduction
```

Das Ausgabeverzeichnis muss neu sein. Je Phase gelten 1.800 Sekunden und
2 GiB Adressraum. Fehler bleiben als `INCONCLUSIVE.json` erhalten.
Der [CI-Workflow](../../.github/workflows/lorentz-proper-time-run.yml)
wiederholt den gesamten Lauf in einem Netzwerk-Namespace ohne Netzwerkzugang.
Paarungen und Entscheidungen müssen exakt übereinstimmen; numerische
Vergleiche verwenden atol=1e-10 und rtol=1e-9. Zeit und Speichermessungen
werden nicht maschinenübergreifend gleichgesetzt.

## Was offen bleibt

Externe Replikation und ein neuer, vorab geplanter Umgang mit unzureichenden
Vergleichspaaren bleiben offen. Ebenso ungetestet sind gekrümmte und
inhomogene Modelle, andere Dimensionen, neue Randbedingungen und stärkere
markierungsbezogene Vergleichsschätzer. Die endliche Mehrdeutigkeit der
Eigenzeit und das Erfordernis einer externen absoluten Skala bleiben bestehen.
Der Lauf prüft weder P123 noch einen spektralen Zusatznutzen; die negativen
Ergebnisse aus PR #40/#41 bleiben unverändert. Ein Kontinuumslimes,
Mannigfaltigkeitsnachweis oder neues physikalisches Gesetz folgt daraus nicht.
