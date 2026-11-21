# Unabhängige Schnittmasse, Wirkungsstrom und Vakuum auf dem Anfangskragen

**Auf den veröffentlichten physikalischen P3-Datensätzen ist bislang kein Paar aus unabhängig bekannter positiver Schnittmasse und gemessener Wirkungsstromladung verfügbar.** Alle 60 archivierten Checkpoints, darunter die zwölf mit Anfangszeit null, tragen NOT_RUN. Die Massenangaben in ihren Kontextfeldern sind Sollwerte. Die positive Dichtepräparation des endlichen Kragens schliesst eine vollständig staubfreie Belegung aus. Frühere markierte Referenzablesungen und klassische Einstein-Staub-Massen besitzen keine ausgewiesene Paarung mit einer physischen P3-Ladungsmessung auf derselben Präparation.

Hier wird eine konkrete Zuordnung zwischen einem unabhängigen Massenzähler und den Dichten **derselben endlichen Wirkungsrechnung** geprüft. Sie liefert positive und leere Vergleichsbelegungen. Auf einem festen Transportweg reproduziert die Kalibrierung mit M=1/4 die zurückgehaltene Masse M=1, solange dasselbe innere Uhrprofil benutzt wird. Bereits eine Änderung zweier innerer Uhrwerte kann bei gleicher Masse, Dichtebelegung und gleichem äusserem Rand das Vorzeichen der abgelesenen Ladung ändern. Auch bei der Mittelung über das vollständige präparierte Uhrpaket sind die beiden nötigen Verstärkungen verschieden. Dieses Ergebnis gilt für die untersuchte Zuordnung. **Physikalische P3-Massenkalibrierung und Flächenauslese bleiben auf HOLD.**

## 1. Was unabhängig festgelegt wird

Grundlage ist der [veröffentlichte Ladungsselektor aus PR #333](https://github.com/thomasmgfeller/x6-spectral-astrolabium/tree/9f2842a1e25deeeb3e5c1a923902392a05e47e75/research/rax_cqg/dust_collapse/boundary_mass_sector_v0_1). Der zukünftige Staubtransport erhält eine vorab gewählte Quellstärke M in markierten Referenzeinheiten. Seine positiven Kantenmarken f tragen die Masse. Der archivierte Prüfer `current.py` zählt auf dem Anfangsideal P die Summe der es verlassenden Kantenmarken. Im Inneren ist die Divergenz null. Die Kontrollwerte sind 0, 1/4 und 1. Keiner wird aus Uhrantwort, Radius oder einem späteren Detektor gewählt.

Eine zusätzliche Annahme verbindet diesen Zähler mit dem Staubfeld der Wirkung. Jede markierte Weltlinie durchläuft das Zeitintervall D=T₇−T₃. Im Intervall werden ihre inneren Ereignisse nach Uhrzeit sortiert. Die Grenze zweier aufeinanderfolgender Zeitzellen liegt genau in der Mitte zwischen beiden Markierungen; die erste und letzte Zelle reichen bis zu den beiden Kragen. Jeder Markierung wird die auf dieser Linie transportierte Masse mal ihre Verweildauer zugeschrieben. Summieren über Linien ergibt das integrierte Dichtegewicht wᵥ am Ereignis. Folglich gilt **Σ wᵥ=MD** über die sieben inneren Ereignisse. Die Konstruktion verwendet ausschliesslich den markierten Fluss, die Ordnung und die Uhren. In der Kontinuumsreferenz motiviert die Identität ∫ρ dV₄=∫M(T)dT diese Wahl für vollständige materielle Zeitschichten und geeichte Staubeigenzeit. Eine Eigenzeit- und Volumenrekonstruktion dieser Art auf N15 ist noch nicht hergeleitet.

Die Ladung wird unabhängig mit der ursprünglichen Staubwirkung S in Einheiten von ℏ abgelesen. Für die gemeinsame Verschiebung η aller vier Vergangenheitsuhren gilt exakt p=[S(−η/2)−S(+η/2)]/η. Alle übrigen Felder und **sämtliche Dichtegewichte** werden während der Quellenvariation festgehalten. Es wird keine markierte Zusatzwirkung zu S addiert. Das verhindert, dass die eingespeiste Markermasse schon durch Definition als gemessene Ladung zurückkommt. Die beiden äusseren Dichtefenster, die zwei Uhrlappen und die Zukunftsdichte bleiben wie in der veröffentlichten endlichen Präparation gewählt. Im Inneren präpariert die Verweildauerregel zusätzliche Korrelationen zwischen w, T und f. Das ist ein bedingter Versuch mit derselben Wirkung und demselben äusseren Kragen. Er reproduziert nicht automatisch das ursprüngliche gemeinsame Integrationsmass oder einen physikalisch realisierten Staubstrahl.

## 2. Positivstandard und zwei Vakuumkontrollen

Der erste geeignete kanonische Ordnungstyp ist 2324. Der Weg 3→4→13→7 besteht aus drei Überdeckungsrelationen. Quelle und Senke bleiben fest. Sei Δ=√(2/(19β)), β=4/√6 und δ der Offset der letzten Anfangsuhr. Dann sind T₃=−2Δ+δ, T₇=2Δ und D=4Δ−δ. Den beiden inneren Ereignissen werden die Zeiten T₃+(1/2−k)D und T₃+kD zugewiesen. Beide vorab gewählten k liegen zwischen 1/4 und 1/2; alle Uhren können entlang jeder Kausalrelation streng wachsen. Die Zellgrenze zwischen den zwei Ereignissen liegt für jedes k bei T₃+D/4. Damit bleiben die beiden inneren Gewichte MD/4 und 3MD/4 **zwischen den Profilen identisch**. Die übrigen inneren Dichten liegen auf ihrem Nullatom.

Für M=1/4 und den Mittelpunkt des rechten Uhrlappens δ=1/16:

| Feldbelegung | Markierte Schnittmasse | Aus der Wirkung berechnetes p |
|---|---:|---:|
| Staubfrei auf allen 15 Ereignissen, gleicher Träger und gleiche Uhren | 0 | exakt 0 |
| Leeres Inneres mit ursprünglichem positivem Dichte-Paket am Kragen | 0 | exakt 0 |
| Positiver Fluss, k=1/3 | 1/4 | −0,01121290 |
| Positiver Fluss, k=11/24 | 1/4 | +0,00616939 |

Die erste Zeile ist eine **gesonderte** staubfreie Kontrollpräparation. Die zweite ist die Nullkontrolle mit demselben äusseren Paket wie beim positiven Standard. Denn direkte Kanten vom Vergangenheits- zum Zukunftskragen haben im BD-Kern hier Gewicht null. Eine leere innere Zeitschicht kann daher trotz der äusseren Dichte p=0 ergeben.

Auf diesem Weg lautet die unabhängig nachgeprüfte Formel p/M=(βD/8)[Δ−23δ+3kD]. Bei k=(23/16−Δ)/(3(4Δ−1/16))≈0,413968 ergibt sich auch bei positiver Schnittmasse exakt p=0. Die beiden vorab gewählten Vergleichsprofile klammern diesen Nullpunkt ein. Insgesamt besitzen 243 der 1 048 skalaren Ordnungstypen wenigstens einen solchen Weg; die Prüfung bestätigt das Vorzeichen auf allen 267 geeigneten Wegen.

## 3. Ganzes Uhrpaket und zurückgehaltene Masse

Als erste Auslese verwenden wir den Mittelwert der feinen Ladung mit dem positiven diagonalen Gewicht der beiden gleich präparierten Uhrlappen einschliesslich ihrer vollen Breite. Das ist eine definierte Referenzablesung vor physikalischer Paarung. Für θ=δ/Δ ist p/M ein quadratisches Polynom mit rationalen Koeffizienten. Der Prüfer integriert es mit E[δ]=0 und E[δ²]=13/3072. Die angegebenen Mittelwerte besitzen rationale Einschliessungen. Das gewählte M kommt dabei ausschliesslich vom Flusszähler.

| Inneres Profil, Typ 2324 | Mittleres p bei M=1/4 | Verstärkung M/⟨p⟩ | Mit dieser Verstärkung abgelesene Masse bei M=1 |
|---|---:|---:|---:|
| k=1/3 | 0,07097231 | 3,52250 | 1,00000 |
| k=11/24 | 0,09079014 | 2,75360 | 1,00000 |

Eine zweite Rechnung liest den Standard sowie die zurückgehaltene Dosis direkt durch symmetrische Wirkungsdifferenzen aus und bestätigt diese Übertragung innerhalb jedes Profils. Die beiden zulässigen Verstärkungsintervalle bei der publizierten Massentoleranz ±2 % sind disjunkt. Ein Punktwert aus einer positiven Dosis würde diese Profilabhängigkeit übersehen. Die Werte sind endliche Referenzeinheiten und liefern keinen Umrechnungsfaktor für die zwei physischen P3-Staubmassen.

Als zweite Auslese prüft `packet.py` die **kohärente Quellantwort** desselben einzelnen Ordnungstyps und derselben bedingten inneren Präparation. Die ursprünglichen zwei Randuhrlappen werden vor der Paarung amplitudenweise addiert. Das kollektive Anfangsdichtefenster wird analytisch integriert. Der dimensionslose Einfluss der Staub- und Gravitationsphase ist enthalten. Der Skalarfaktor der Ordnung ist für diese Staubvariationen gleich und kann für einen nichtverschwindenden Endkanal aus dem normierten Quotienten herausgekürzt werden. Mit A(η)=∫exp(iS+iηp) und den Paketgewichten wird A′(0)/(iA(0)) ausgewertet. Dieser komplexe Quotient ist eine postselektierte Amplitudenantwort, kein positiver Massenmesswert. Bei M=1/4 und Anfangsdichtezentrum 1/8 ergeben sich rund 0,071019+0,004787i und 0,090837+0,004861i. Beide Dichtezentren, beide Dosen und die Kontrolle mit leerem Inneren sind im JSON ausgewiesen. Gegenrechnungen benutzen die Quellendifferenz bei ±10⁻⁴ und die Quadraturen mit 64, 128 und 256 Teilintervallen pro Lappen. Die beobachteten Quadraturänderungen sind keine rigorose allgemeine Fehlergrenze für das physikalische Integrationsmass.

## 4. Wie allgemein ist das Ergebnis?

Die ergänzende Prüfung sendet die markierte Masse auf **allen** 1 048 Katalogträgern mit gleicher Aufteilung über ihre maximalen Überdeckungsketten von 3 bis 7. Derselbe Fluss wird bei beiden Uhrprofilen beibehalten. Die relative Uhrposition eines inneren Ereignisses sei u=L₋/(L₋+L₊), wobei L₋ und L₊ die maximalen Längen einer Überdeckungskette von der Quelle bzw. bis zur Senke sind. Das zweite Profil benutzt u². Beide sind unter Umbenennung invariant und kausal strikt zunehmend. Die Verweildauerregel bestimmt die inneren Gewichte anschliessend ohne Verwendung von p. Auch bei der zurückgehaltenen Dosis M=1 liegen alle Gewichte im zulässigen Bereich (0,1).

| Verteilung der diagonalen Antwort über Ordnungstypen | Uhrprofil u | Uhrprofil u² |
|---|---:|---:|
| Positives mittleres p bei positiver Masse | 735 | 834 |
| Negatives mittleres p bei positiver Masse | 313 | 214 |
| Bereich von ⟨p⟩/M, gerundet | −1,34452 bis +2,37987 | −1,06938 bis +2,51600 |

Der Flusszähler gibt in allen **65 376** Vergleichen den Sollwert (je 21 792 Schnitte für M=0, M=1/4 und M=1). Auf **956 von 1 048** Typen existiert bei ±2 % keine gemeinsame positive Verstärkung, die beide Profilmittelwerte auf die bekannte Dosis abbildet. Dies ist eine Aussage über die geprüfte Familie von Präparationen. Sie schliesst eine andere hergeleitete Stromobservable, eine dynamisch bestimmte Auswahl von Profilen oder eine kontrollierte Verfeinerung nicht aus.

Zusätzlich wird die unveränderte ursprüngliche Feldpräparation **ohne** markierte Linien untersucht. Die unabhängige innere Dichteinsertion W=Σw folgt durch Variation des konstanten Staubterms im inneren Bereich. Für festes W und feste letzte Randuhr liefert die Austauschbarkeit im feinen Hilfsmass E[wᵥ|W]=W/7. Die verborgenen Uhren sind in dieser Rechnung unabhängig und gleichverteilt mit Mittel null. Wird W/D lediglich als Massenvorschlag verwendet, haben an den Mittelpunkten des rechten und linken Lappens 283 bzw. 371 Ordnungstypen eine negative bedingte mittlere Ladung für W/D>0. Dieses Resultat erfordert keine neue Flussregel. W ist jedoch eine integrierte Dichte in Wirkungsdimension. Der Übergang von W/D zu einer tatsächlichen Ruhemasse benötigt eine physikalisch identifizierte, geschlossene materielle Zeitschicht und eine geeichte Eigenzeit.

## 5. Entscheidung für P3

Die bisherige Eingabe stellt kein unabhängig geeichtes Massenetikett für eine gekoppelte physikalische P3-Präparation bereit. Ein frei hinzugefügter markierter Strom könnte auf denselben C,T,w-Daten auch verdoppelt werden, ohne die Wirkungsableitung zu ändern. Die Verweildauerregel koppelt die beiden Beschreibungen konkret. Sie besteht die profilspezifische Dosisprüfung und verfehlt die universelle Verstärkung schon auf demselben Träger. Die staubfreie Kontrollrechnung bestimmt nur den algebraischen Nullpunkt. Eine physikalische Vakuum- oder Positivmessung lässt sich aus dem gegenwärtigen Paket nicht rekonstruieren.

Für eine experimentelle oder dynamische absolute Kalibrierung wäre eine **gemeinsame** Aufzeichnung erforderlich: die unabhängig bestimmte positive Ruhemasse und ihr Fehler, die Identität derselben Anfangspräparation samt Uhr- und Geometrieskala, die dort abgelesene Ladung mit ihrer Antwortverteilung und eine entsprechend definierte Nullmessung. Eine theoretische Alternative wäre eine aus der gekoppelten Dynamik begründete Zuordnung mit kontrolliertem Fehler auf dieser Zustandsklasse. Die offenen physischen Werte stehen in `results.json` als null im Sinn von „nicht bestimmt“. Es wurden weder neue dynamische 4D-Ensembles noch eine Flächen- oder Bounce-Auswertung erzeugt.

## Offline wiederholen

Mit Python 3.10 oder neuer und der Standardbibliothek im entpackten Verzeichnis:

```sh
sha256sum -c SHA256SUMS
python3 -B run.py --out wiederholung.json --types typen_wiederholung.json
cmp results.json wiederholung.json
cmp by_type.json typen_wiederholung.json
```

`design.json` hält die lokale Versuchsentscheidung vor dem Zweipfadtest fest; `supplement.json` die anschliessende Erweiterung auf alle Ordnungstypen. Es gab keine öffentliche Vorregistrierung. `sources.json` benennt alle übernommenen Quellen und ihre Git-Prüfsummen. `by_type.json` gibt die Polynomkoeffizienten und mittleren Ladungsantworten je Ordnungstyp an. [Stromdefinition](https://github.com/thomasmgfeller/x6-spectral-astrolabium/blob/9f2842a1e25deeeb3e5c1a923902392a05e47e75/research/rax_cqg/dust_collapse/current_calibration_v0_1/DERIVATION.md) · [Gemeinsamer Wirkungsvertrag](https://github.com/thomasmgfeller/x6-spectral-astrolabium/blob/9f2842a1e25deeeb3e5c1a923902392a05e47e75/research/rax_cqg/dust_collapse/minimal_scalar_action_v0_1/action_contract.json)
