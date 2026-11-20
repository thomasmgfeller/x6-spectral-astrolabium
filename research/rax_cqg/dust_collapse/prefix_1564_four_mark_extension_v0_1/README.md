# Kann eine vierte austauschbare Einfügung A und B unterscheiden?

**Beide publizierten vollständigen N14-Gewichtstabellen scheitern an derselben Ungleichung. Für beide lokalen Verhältnisse am Präfix 1564 existieren dagegen streng positive Fortsetzungen.** Die konstruierten Gegenbeispiele erhalten sogar sämtliche zehn lokalen Endtypgewichte und die vollständige ältere N13-Marginale. Sie ändern die Verteilung auf dem übrigen N14-Träger.

## Annahme und Prüffrage

In der Ein-Kanten-Familie seien die ursprünglichen drei und die vierte Einfügungsmarke gemeinsam austauschbar. Beim Löschen der letzten Marke sollen die groben Amplitudenkoeffizienten als Marginale des nichtnegativen feinen Gewichts entstehen. Erhalten bleiben der veröffentlichte zulässige N14-Träger und die skalare N15-Zulassung aus dem Katalog. Die Austauschbarkeit aller vier Marken ist eine zusätzliche Modellannahme. Der veröffentlichte N15-Träger erlaubt auch Einfügungen an früheren Positionen in der Kausalordnung. Diese Austauschbarkeit ist deshalb eine Bedingung für die markierte Darstellung und keine Herleitung einer physikalischen Geburtsdynamik.

Die im ersten Commit fixierte Frage in `design.json` betrifft zwei vollständige N14-Zeugen. Die anschliessende ergänzende Frage lässt die übrigen N14-Gewichte frei und hält alle zehn lokalen Koeffizienten sowie die gesamte N13-Verteilung fest.

## Vollständige Projektion und Ausschluss

Auf N14 gehören die markierten Pfade der Ein-Kanten-Familie zu 191 zulässigen Orbits. Ein feiner Orbit ist die Menge der Markierungen einer Ordnung, die durch Permutation der vier Einfügungslabels entsteht. Unter Gleichgewicht pro Markierung kann jede dieser vier Marken als letzte gelöscht werden. Damit ist jede Projektionsspalte die Häufigkeitsverteilung der vier resultierenden N14-Orbits, einschliesslich Mehrfachnennungen, geteilt durch vier. Verschiedene feine Orbits dürfen dieselbe Spalte besitzen.

Der Prüfer zählt **928 verschiedene Spalten**. Die Vorwärtszählung ergänzt veröffentlichte N14-Ordnungen um alle transitiv zulässigen Beziehungen zum neuen Ereignis. Eine zweite Zählung geht rückwärts von allen 1 048 skalaren N15-Endtypen aus, wählt jede Beschriftung des alten Dreierkerns und löscht nacheinander jede der vier übrigen Marken. Sie liefert dieselbe Spaltenmenge. Beide Zählungen verlangen für jede Löschung die Zugehörigkeit zum N14-Träger.

Für das rationale lineare Funktional `y` in `proof.json` gilt $y^T c \ge 0$ für jede Projektionsspalte $c$. Für beide alten vollständigen N14-Gewichtstabellen $b$ ist $y^T b=-1$. Daher kann keine nichtnegative Linearkombination der Spalten diese Tabellen reproduzieren. Das gleiche Funktional gibt den beiden geänderten A/B-Orbits denselben Koeffizienten. Der Widerspruch bleibt somit über die gesamte publizierte eindimensionale A/B-Variation dieser vollständigen Tabellen erhalten.

## Sind die zehn lokalen Koeffizienten trotzdem erreichbar?

| Geprüftes A:B | Vollständiger alter N14-Zeuge | Neuer globaler Zeuge mit allen zehn gleichen lokalen Koeffizienten |
| --- | --- | --- |
| 1:1 | ausgeschlossen | rational konstruiert |
| 1:3 | ausgeschlossen | rational konstruiert |

Jeder neue Zeuge legt zunächst Gewicht $10^{-8}$ auf **jede** der 928 Spalten und addiert positive rationale Restgewichte. Insgesamt beträgt das Gewicht eins. Die Summen liefern exakt die archivierten Massen aller 72 markierten N13-Präfixe, am Präfix 1564 die zehn verlangten Endtypkoeffizienten und strikt positive Massen auf allen 191 N14-Orbits. Positivität aller N14-Orbitmassen ist hier eine Eigenschaft der **neuen** Zeugen. Ihre Einzelwerte auf N14 unterscheiden sich von den archivierten. Eine Gegenrechnung permutiert alle vier Marken auf 24 Arten, löscht jeweils dieselbe Marke und rekonstruiert so alle 1 026 einzelnen markierten N14-Koeffizienten. Gewichte innerhalb einer Spalte lassen sich gleichmässig auf die zugehörigen N15-Orbits verteilen.

Damit beschränkt die vorgeschlagene Erweiterungsregel die globale Gewichtsverteilung. Sie lässt beide lokalen Werte $q_A/q_B=1$ und $1/3$ zu. Durch konvexe Mischung der zwei positiven Fortsetzungen lässt sich auch jeder lokale Quotient zwischen 1/3 und 1 bei denselben N13-Massen realisieren. Eine physikalische Auswahl zwischen A und B, Etappe 6 und P3 bleiben offen.

## Offline nachprüfen

Python 3 mit Standardbibliothek genügt für beide Zählungen und alle rationalen Zertifikate.

~~~sh
sha256sum -c SHA256SUMS
python3 -B verify.py > replay.json
cmp result.json replay.json
~~~

`extension.py` rekonstruiert die markierten Gewichte und Vorwärtsprojektionen. `verify.py` prüft die Rückwärtszählung, beide Trennzeugnisse, die vollständige Positivität und die lokalen Koeffizienten. Die zur Zertifikatsuche benutzten Skripte `make_proof.py` und `local_test.py` verwenden zusätzlich NumPy, SciPy und SymPy; ihre Gleitkomma-Optimierung entscheidet über keine veröffentlichte Ungleichung. Alle Belege in `proof.json` und `local_proof.json` werden exakt geprüft.

[Ursprüngliche Gewichtszeugen](https://github.com/thomasmgfeller/x6-spectral-astrolabium/tree/8723cba93224931a6fdffc525c798524ab38bebb/research/rax_cqg/dust_collapse/prefix_1564_selection_v0_1) · [N15-Katalog und Zulassungsdefinition](https://github.com/thomasmgfeller/x6-spectral-astrolabium/tree/8723cba93224931a6fdffc525c798524ab38bebb/research/rax_cqg/dust_collapse/extension_stability_v0_7)
