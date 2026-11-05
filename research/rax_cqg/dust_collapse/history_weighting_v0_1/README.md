# CST Staubball: physikalische Historiengewichtung v0.1

Ergebnis: bedingte Herleitung einer kanonischen Staubreferenz und exakter Zählregeln; das physikalische Maß der vollständigen vierdimensionalen CST bleibt offen.

Der Bericht trennt Wirkungsphase, Integrationsmaß und Anfangszustand. Für die explizit reduzierte homogene Staubzelle mit direkter Quantisierung in q = sqrt(V) folgt das Maß dq = dV / (2 sqrt(V)). Die Dirichlet-Randbedingung ist eine gewählte Referenz, kein CST-Ergebnis. Für beschriftete endliche Kausalsets wird der Symmetriefaktor unter einer klar angegebenen Ausgangsmaßwahl abgeleitet. Natürliche Beschriftungen erfordern eine andere Vielfachheitskorrektur als beliebige Beschriftungen.

Die alte Kandidatenentscheidung bleibt `CLOSED_REJECTED_FOR_DOMINANT_BOUNCE`. Es gibt keinen neuen Bounce-Test, keine Optimierung zugunsten einer Umkehr und keine Behauptung einer Singularitätsauflösung.

## Dateien

- `CST_Staubball_Historiengewichtung_v0_1.pdf`: neunseitiger Bericht mit Herleitung, Grenzen und Quellen.
- `report.tex`: bearbeitbarer Bericht und Formeln.
- `verify.py`: ausführbare endliche Prüfungen; nur Python-Standardbibliothek.
- `contract.json`: Modellannahmen, offene Entscheidungen und Gatter G0 bis G6.
- `provenance.json`: geprüfter GitHub-Stand und Originalhash des Abschlussarchivs.
- `inputs/`: bytegleiche Entwicklungs-/Prüftabellen und Kandidatensnapshot; keine neue Stichprobe.
- `results/verification.json`: tatsächlich ausgeführte Prüfungen.
- `SHA256SUMS`: Integrität aller übrigen Paketdateien.

## Wiederholung

Im entpackten Verzeichnis, Python 3.10 oder neuer:

```bash
sha256sum -c SHA256SUMS
python3 verify.py
```

Der Prüfer verifiziert die kopierten Eingaben, zählt alle Ordnungen bis fünf Elemente, kontrolliert die Quotienten und einen markierten Stabilisator, prüft Zusammensetzung und Unitarität im endlichen Sinusraum, demonstriert den Fehler eines fehlenden Jacobifaktors und vergleicht unabhängige Koordinatenquadraturen. Vier rationale Zeitpunkte prüfen den klassischen kontrahierenden Staubzweig. `results/verification.json` wird beim Wiederholen ersetzt; Gleitkommazahlen dürfen innerhalb der im Code angegebenen Toleranzen plattformabhängig abweichen. Hashprüfung daher vor der Wiederholung ausführen.

Die Kombinatorik und rationalen Identitäten sind exakt. Die numerischen Fehlerwerte sind keine rigorosen Intervallzertifikate. Die 16-/32-Moden-Referenz ist kein Nachweis einer CST-Verfeinerung oder des unendlichen Halbraums.

## Wissenschaftliche Grenze

Keine neue Gewichtung der 27/17 alten Volumenpfade wird eingesetzt: Es fehlen ein vollständiger Mikrohistorien-Träger, seine Vergröberungsfasern, ein konsistenter CST-Übergangskern, Rand-/Materiedaten und unabhängig begründete Sektorgewichte bei variabler Elementzahl. Der Faktor `1/|Aut|` ist bedingt begründet; Kovarianz allein macht ihn nicht zum einzig physikalischen Maß. Die alte No-go-Schranke wird für ungleiche Amplituden analytisch verallgemeinert, aber nicht als Auswahlregel für die Gewichte benutzt.

Die Quellen der bisherigen CSV-Dateien sind im veröffentlichten Projekt unter `research/rax_cqg/dust_collapse/packages/CST_Staubball_Kopplungsscan_v0_2_Pruefpaket.zip` enthalten. Ursprung und Hashes wurden gegen den Abschluss von PR 234 abgeglichen. Externe wissenschaftliche Artikel sind verlinkt, nicht als Volltexte kopiert. Dieses Paket erzeugt keine GitHub-Veröffentlichung und benötigt weder Netzwerk noch kostenpflichtige Rechenzeit.
