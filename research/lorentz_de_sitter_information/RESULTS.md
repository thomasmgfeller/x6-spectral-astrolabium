# Ergebnis: zusätzliche Ketten bringen hier wenig Präzision

Die Einschränkung auf die bekannte vierdimensionale de-Sitter-Familie
vermeidet die instabile freie Zweiparameter-Inversion. Innerhalb dieser
Familie liefert die kovarianzbewusste Kombination längerer Ketten jedoch
nur einen kleinen zusätzlichen Gewinn gegenüber Zweierketten allein.

## Vorabstand und Durchführung

- Bereits öffentliche Pilotdaten: `ca43cc55677012bca0884b2e8a4dd6d91a4e28f5`;
  die Planung daraus ist ausdrücklich eine nachträgliche Auswertung.
- Öffentlicher Prüfvertrag und ausführbarer Quellenstand:
  `746efa4a74e78dadc9c49e4e26ea65957d64f3aa`, vor dem neuen Ziellauf.
- Erster Ziellauf: 18.10.2026, 09:03:37–09:03:52 UTC; 14,63 Sekunden,
  maximal 82.752 KiB Prozessspeicher (plattformabhängige RSS-Angabe).
- Vier unabhängige Testzellen mit h = 0; 0,1; 0,25; 0,5, je 4.096 Wolken
  und N=128. Insgesamt 16.384 Wolken bzw. 2.097.152 simulierte Ereignisse.
- Feste Gewichte aus den alten flachen Pilotwolken, frischer Seed-Namensraum,
  unveränderte Geometrie, keine Nachanpassung oder Entfernung negativer Schätzer.

Der Budgetentscheid war positiv: Für h=0,5 prognostizierte die Pilotplanung
2.562 unabhängige Wolken für die kombinierte Schätzung und eine nominelle
relative 20%-Halbbreite. Die Grenze für die Durchführung lag bei 4.096.
Das ist eine Planung für Zufallsstreuung, keine Präzisionsfreigabe.

## Vorab festgelegter Hauptvergleich

N=128, h=0,5, q=R T²=3,1313138148:

| Schätzer | RMSE pro Wolke | Standardabweichung | beobachteter Mittelwertfehler |
| --- | ---: | ---: | ---: |
| Zweierketten C2 | 16,807961 | 16,809917 | 0,056916 |
| C2+C3, volle Kovarianz | 16,578757 | 16,580730 | 0,041454 |
| C2+C3+C4, volle Kovarianz | 16,577842 | 16,579815 | 0,040858 |

RMSE-Verhältnis GLS234/C2: **0,986309**, entsprechend **1,369%** kleinerem
RMSE. Das gepaarte approximative 95%-Bootstrapintervall ist
**[0,980811; 0,991709]** (1.999 festgelegte Wiederholungen). Für das
Erfolgskriterium hätte die obere Grenze höchstens 0,9 betragen dürfen.

**`TEN_PERCENT_RMSE_GAIN_NOT_ESTABLISHED`** bleibt als negatives Ergebnis
erhalten. Der kleine beobachtete Gewinn ist mit diesem Bootstrap vereinbar;
ein praktisch grösserer Gewinn ist damit nicht belegt. C4 bringt gegenüber
C2+C3 in dieser festgelegten Konstruktion kaum weiteren Nutzen. Es ist
keine Aussage über alle möglichen nichtlinearen Ordnungsmerkmale.

## Wie viele unabhängige Wolken wären nötig?

Nachstehend die **nachträglich aus der neuen Streuung berechneten**
Normalapproximationen für eine 95%-Halbbreite von 20% des wahren q.
Jede Wolke enthält 128 Ereignisse. Dies sind weder bereits ausgeführte
Grossläufe noch garantierte Mindestzahlen. Der wahre Wert ist hier nur
wegen des Simulationsmodells bekannt.

| h | q=R T² | C2 allein | C2+C3+C4 |
| --- | ---: | ---: | ---: |
| 0,1 | 0,120200 | 1.704.723 | 1.706.298 |
| 0,25 | 0,757907 | 43.885 | 43.243 |
| 0,5 | 3,131314 | 2.768 | 2.693 |

Bei q=0 ist eine relative Fehlervorgabe nicht definiert; die Pilotdatei
enthält dafür absolute Ziele. Die neuen Streuungen sind von ähnlicher
Grössenordnung wie die Pilotplanung, aber nicht identisch: bei h=0,5 steigt
der GLS234-Planwert von 2.562 auf 2.693 Wolken. Unsicherheit der geschätzten
Kovarianz ist in diesen einfachen Zahlen nicht eingerechnet.

Die Gewichte bei N=128 für y_k=F_k/p_k−1 sind
GLS234 = (111,868714; −10,026807; −0,114810), während C2 allein (90; 0; 0)
verwendet. Negative Gewichte gleichen Korrelationen aus; sie bedeuten keine
negativen Ereigniszahlen. Wegen der starken Korrelation bringen zusätzliche
Kettenzahlen hier wenig neue Information für diese lineare Schätzung.

## Grenzen und nächster sinnvoller Versuch

Die Krümmungsintervalle bleiben **`NOT_QUALIFIED`**. Die Streuung einzelner
Wolken ist gross, und die lokale lineare Vorwärtsformel hat einen Restterm.
Mehr unabhängige Wolken verkleinern die Streuung, beseitigen diesen Fehler
aber nicht. Die simultanen approximativen Mittelwertfehlerintervalle sind
zu breit, um einen kleinen systematischen Fehler auszuschliessen.

Für C2 liefert die getrennte geometrische Quadratur bei h=0,5 einen
linearen Erwartungswertfehler von −0,00144281 in q (etwa −0,0461% von q).
Das ist ein numerischer Referenzwert an dieser Stelle, kein bewiesener
gleichmässiger Restterm. Für die Kombination mit C3/C4 fehlt eine solche
Resttermkontrolle. Auch bei bekannter de-Sitter-Geometrie sind gleichmässige
physische Volumendichte und unabhängige Wolken echte Modellannahmen.

**Entscheidung:** Keine Vergrösserung dieses Kettenkombinationsversuchs.
Als nächste Forschungsstufe ist C2 allein mit der vollständigen
geometrischen Vorwärtsfunktion sinnvoll: erst Monotonie und numerische
Fehler kontrollieren, dann eine vorab festgelegte, konservative
Konfidenzmenge invertieren. Abhängige Paare innerhalb einer Wolke müssen
dabei ausdrücklich berücksichtigt werden. Eine endliche Überdeckungsprüfung
und ein klarer Verweigerungsbereich gehen einer Nutzung als Uhr voraus.
Dieser Folgeversuch ist hier beschrieben, noch nicht ausgeführt.

Extern begründete Dichte-/Erfassungsgrenzen und eine externe Replikation
bleiben erforderlich. Eine absolute Krümmung R braucht zusätzlich eine
unabhängige Eigenzeitskala T; der flache Schätzer darf diese Voraussetzung
nicht zirkulär ersetzen. Historische Quellen und Daten wurden nicht verändert.

## Vollständige Nachprüfbarkeit

`results/planning.json` enthält alle 24 Planzeilen und Gewichte für N=64/128.
Die vier NPZ-Dateien enthalten alle neuen Kettenzählungen und Relationshashes.
`results/summary.json` enthält zwölf neue Ergebniszeilen, alle Fehlerintervalle
und den Hauptentscheid. `execution.json` bindet Laufzeit, Versionen und
Quellen; `hashes.json` bindet sämtliche Originalausgaben.
`VERIFICATION.json` dokumentiert den vollständigen internen Replay mit
unabhängigen Kausalitäts-, Kettenzahl-, Gewichts- und Momentprüfungen.
