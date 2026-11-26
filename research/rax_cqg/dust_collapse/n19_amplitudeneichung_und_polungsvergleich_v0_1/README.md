# CST-DUST · Welche Kalibrierung braucht der N19-Senderstrom?

**26. November 2026.** Die frühen Felder und die Kragenimpulse G₀,G₁ lassen die absolute Senderantwort weit offen. Zwei stationäre Zustände mit exakt diesen gemeinsamen Daten verlangen beim selben Puls die Stromänderungen −4,88457·10⁻⁸ und −1,46453·10⁻⁷. Jeder gemeinsame Schätzwert hat für mindestens einen der Zustände mehr als 49,97 % relativen Fehler. Bei bekanntem nominalem Nullstrom K₀ reichen dagegen die übrigen geprüften Zeit- und Gewichtsgrenzen für einen Fehler unter 1,38 %, auch ohne G₀ und G₁.

Für zwei entgegengesetzte Pulse am **selben** ungepulsten Zustand ergibt die ursprüngliche Wirkung eine Vorhersage ohne Amplitudeneichung. Über beide registrierten Zeitfenster, das archivierte e-Intervall und alle kompatiblen positiven Endpunktgewichte liegt das Verhältnis der Beträge innerhalb von [0,99999973; 1,000944]. Die spätere Stromänderung ist eine rechnerische Modellgrösse. Eine physische Auslese und eine verifizierte Wiederherstellung desselben Ausgangszustands bleiben offen.

## Was bei gleichen frühen Feldern frei bleibt

Auf den neunzehn Ereignissen gilt A=19Σⱼwⱼ+Σᵢ≺ⱼbᵢⱼwⱼ(Yⱼ−Yᵢ)². Der Sender ist z=16, der passive Empfänger r=18. Der zuletzt hinzugekommene Beitrag zum Uhrstrom des leeren Vorgängers 15 ist K=w_z(Y_z−Y₁₅). K₀ bezeichnet diesen Strom im ungepulsten Vergleichszustand. Für den Versuch wird nur der lokale Term −J_w w_z hinzugefügt. J_Y ist null. Während der jeweiligen Fortsetzung sind alle Felder ausser z und seiner Zukunft identisch mit ihrem Nullarm. Der Zukunftskragen darf sich ändern.

Der Anfangskragen P={0,1,2,3} enthält sämtliche Vorgänger seiner Ereignisse. Halte alle Uhren und alle vier Gewichte in P fest und multipliziere alle übrigen Gewichte mit λ>0. Für die quellbehaftete Wirkung A_J gilt exakt

    A_J(Y,w_neu) = A_P(Y,w) + λ [A_J(Y,w) − A_P(Y,w)].

Jede freie Uhrzeile wird mit λ multipliziert. Die neun Dichtezeilen hängen nur von den Uhren und der vorgegebenen Quelle ab. Deshalb überführt die Skalierung jeden geprüften stationären Zustand samt seiner reinen Dichtepulse wieder in einen stationären Zustand, solange die Gewichte im zulässigen Bereich bleiben. Die frühe leere Uhr hat w₁₅=0. Daher bleibt auch der ganze strikte Sendervorlauf {0,1,2,15} unverändert, einschliesslich Y₁₅. K₀ und die gepaarte Differenz ΔK skalieren beide exakt mit λ.

| λ | K₀ | ΔK bei J_w=+10⁻⁶ |
|---:|---:|---:|
| 1 | 0,17004955 | −9,76494·10⁻⁸ |
| 1/2 | 0,08502478 | −4,88247·10⁻⁸ |
| 1/4 | 0,04251239 | −2,44123·10⁻⁸ |

Diese Skalierungsfamilie gestattet beliebig kleine positive λ. Damit können die frühen Felder allein im betrachteten Zustandsraum für eine von null verschiedene absolute Antwort keinen einheitlichen relativen Fehler unter 100 % garantieren. Eine unabhängige Vorbereitung, die die Masse oder den Nullstrom festlegt, würde den zulässigen Zustandsraum einschränken.

## Was die beiden Kragenimpulse beitragen

Wir halten jetzt zusätzlich G₀ und G₁ des nominalen Referenzzustands exakt fest. Das verlangt eine eigene Konstruktion, da die einheitliche Skalierung die Kragenimpulse ändern kann. Bei fixen Nicht-Zukunftsuhren verwenden wir neun innere Gewichte sowie vier Gewichte und vier erste Momente wⱼYⱼ des Zukunftskragens. Die elf freien Uhrzeilen, G₀, G₁ und die Normierungsuhr Y₇ ergeben vierzehn lineare Differenzgleichungen. Für die beiden Zeugen wählen wir Δw_z=±1/30 sowie Δw₆=−(5/6)Δw_z und Δ(w₁₀Y₁₀)=−(2/3)Δw_z. Die letzten beiden Bedingungen wählen eine zulässige Richtung für die Konstruktion aus. Sie sind keine Präparationsregeln. Die so bestimmte 17×17-Matrix ist auf der exakten Referenzlösung regulär. Die Richtungswahl wurde numerisch gesucht, anschliessend mit den festen rationalen Werten und Intervallrechnung verifiziert.

Beide Nullarme haben identische innere Uhren, identische Kragenuhren am Anfang, gleiche frühe Gewichte, dieselben G₀,G₁ und dieselben beiden Materialfenster. Ihre K₀ sind rund 0,08502054 und 0,25507857. An der späteren Grenze und bei einigen ausserhalb des Sendervorlaufs liegenden Gewichten unterscheiden sie sich. Beide Pulse besitzen vollständige stationäre Fortsetzungen mit passivem Empfänger. Der relative Unterscheidungsfehler lässt sich ohne Wahrscheinlichkeitsannahme bestimmen. Für mögliche Antwortbeträge a<b minimiert m=2ab/(a+b) den grössten der beiden relativen Fehler. Dieser beträgt (b−a)/(b+a). Für die positive und negative Quelle liegt er in den beiden gebauten Beispielen jeweils über 49,97 %. Die beiden Kragenimpulse können den fehlenden K₀ in diesem Vertrag deshalb auch für eine 5-%-Vorhersage der Modellstromänderung nicht ersetzen.

## Absolute Antwort bei bekanntem oder begrenztem K₀

Schreibe u=Y₁₅, s=Y₁₆, h=Y₁₇ und t=Y₁₈ im gemeinsamen Nullzustand. d und q bezeichnen die gepaarten Änderungen der Sender- und Empfängeruhr. Die Vorstudie leitet aus den unveränderten nativen Vorgängerzeilen und der passiven Empfängerzeile folgende Beziehung her, die auch bei frei wählbaren zukünftigen Kragenwerten notwendig ist:

    ΔK = A_z w_z + A_r w_r,
    A_z = d [1+(s+d−u)/(s−h)],
    A_r = q (s+d−u)(s+d−h)/[m_z(t+q−h)],    m_z=−(u+3).

Für beide Pulse haben A_z und A_r dasselbe Vorzeichen, entgegengesetzt zum Vorzeichen von J_w. Mit w_z=K₀/(s−u) umschliessen wir den Antwortbetrag. Für diese **absolute** Schranke genügt die Annahme 0<wᵣ<1. Es wird weder eine Verteilung für wᵣ angenommen noch ein Empfangswert als Ziel vorgegeben. Als Schätzwert dient der harmonische Mittelpunkt der äusseren Betragsschranken.

| Eingaben für die absolute Vorhersage | Verwendete Hülle | Garantierter grösster relativer Fehler bei J_w=±10⁻⁶ |
|---|---|---:|
| Nominales K₀ und nominale frühe Uhr | Komplettes nominales Empfangsfenster; 0<wᵣ<1 | <1,38 % |
| K₀ exakt 1/8 | Ganze Sender- und Empfangsfenster, einschliesslich e-Intervall; 0<wᵣ<1 | <1,90 % |
| K₀ innerhalb ±3,1 % um 1/8 | Dieselben vollständigen Fenster und Gewichtsgrenze | <4,94 % |

Die beiden letzten Zeilen setzen keinen exakten Y₁₅-Messwert voraus. Die Senderdichtezeile des Nullarms liefert u=s−√(s²+6s+6). Die frühere Wurzel für h folgt aus der Empfängerdichtezeile. Beide werden für jede Uhrbox neu eingeschlossen. Die Schranken verwenden somit kalibrierte Zeitfenster, gegebenenfalls aus früheren Vergleichsläufen.

Die früheste positive Verbindung hat den vor dem Senden berechenbaren Strom I₀₁=w₁(Y₁−Y₀)=1/8. Eine skalierte Referenz mit λ≈0,73507985 belegt, dass der Sollwert K₀=I₀₁ im Nullarm mit der ursprünglichen Wirkung und den beiden anschliessenden Pulsversuchen verträglich ist. Die Skalierungsfamilie zeigt zugleich, dass derselbe frühe I₀₁ zu beliebig kleineren K₀ passt. Auf dem letzten Glied 2→15 ist der eingehende native Beitrag wegen w₁₅=0 exakt null. Eine physische Übertragung des Sollwerts zum positiven Sender ist offen.

Für eine symmetrische relative Toleranz ε berechnen wir je Vorzeichen eine Hülle [L(1−ε), H(1+ε)+B]. Hier sind L und H die äusseren Schranken des Senderbeitrags bei K₀=1/8, B die obere Schranke des Empfängerbeitrags. Die Anforderung an den harmonischen Schätzer mit maximalem relativen Fehler p=0,05 ergibt

    ε ≤ [(1+p)L − (1−p)(H+B)] / [(1+p)L + (1−p)H].

Nach Abrunden auf ε=0,031 liegt das ausreichende K₀-Band bei [0,121125; 0,128875]. Dies ist eine hinreichende Präparationsgenauigkeit für diese zwei Modellpulse. Wie eng eine reale Präparation K₀ tatsächlich festlegt, wurde nicht gemessen.

## Polungsversuch ohne Amplitudeneichung

Wir wählen Q=−ΔK(+10⁻⁶)/ΔK(−10⁻⁶) am selben ungepulsten Ausgangszustand. Die beiden Antwortbeträge sind positive Linearkombinationen derselben Gewichte w_z,w_r. Daher ist Q ein gewichtetes Mittel der beiden Koeffizientenverhältnisse |A_z⁺|/|A_z⁻| und |A_r⁺|/|A_r⁻|. Diese Aussage benötigt Positivität und keine obere Schranke für die Gewichte. Sie gilt für kompatible Zustände und Fortsetzungen.

Die Dichtegleichungen geben D=10⁻⁶/[2(u+3)]>0 und d=±D. Die kleine, im Empfangsfenster liegende Wurzel erfüllt q²+2(mᵣ−d)q+d(d−2(t−s))=0. Für den gesamten registrierten Bereich ist die zweite Wurzel weiter als das volle Empfangsfenster vom Nullarm entfernt. Um die nahe bei eins liegenden Verhältnisse sicher einzuschliessen, wird für jeden gemeinsamen Faktor das Verhältnis als eins plus die kleine gepaarte Differenz ausgewertet. Die Rechnung deckt 24×24 zusammenhängende Uhrboxen ab. Der benutzte Bereich in s,t überdeckt auch alle gemeinsamen e∈[1/6−2⁻²²,1/6+2⁻²²].

| Verhältnis über allen zugelassenen Uhrboxen | Nach aussen gerundete Hülle |
|---|---:|
| Senderkoeffizient | [0,99999973608; 0,99999973611] |
| Empfängerkoeffizient | [1,0008847; 1,0009438] |
| Q bei beliebigen positiven Gewichten | **[0,99999973; 1,000944]** |

Daraus folgt die Vorzeichenumkehr mit einer Abweichung der Beträge von weniger als 0,095 %, bezogen auf den Betrag bei negativer Quelle. Die Schranke betrifft den normierten Strom der N19-Wirkung in zwei stationären Vergleichsläufen. Sie weist weder einen gerichteten Staubtransport noch eine physische Messung der beiden Ströme nach.

**Kontrolle mit vertauschten Hintergründen.** Für die beiden Nullzustände mit identischem G₀,G₁ liegen die jeweils richtig gepaarten Q bei 1,00000087 und 1,00000029. Verwendet man dagegen den positiven Puls des einen und den negativen Puls des anderen Zustands, erhält man je nach Zuordnung 2,99828 oder 0,33352. Die drei frühen Staubuhren, die Leeruhr und auch G₀,G₁ würden die Verwechslung hier nicht anzeigen. Für einen physischen Polungsversuch ist daher die Wiederholbarkeit der Ausgangspräparation entscheidend.

## Reproduktion

Nach dem Entpacken genügen Python ab 3.10 und die Standardbibliothek.

    python3 -B pruefen.py

Der Lauf prüft die SHA-256-Festlegungen und reproduziert zuerst das unveränderte Vorgängerpaket samt dessen Vorstudien. Alle sechs hier aufgeführten Nullarme einschliesslich der vier Skalierungsbeispiele wurden mit beiden Quellen, den zwanzig inneren Gleichungen, Ordnungs- und Fensterbedingungen geprüft. Die gewählte lineare Richtung, die konservativen Fensterhüllen, Schätzer, relativen Schranken und die falsch gepaarten Kontrollen stehen in Amplituden.json und Fenster.json.

Die unabhängige Gegenrechnung prüft die Skalierung an 18 exakten rationalen Wirkungswerten und das Polungsverhältnis an 72 Paaren durch Bisektion der ursprünglichen Empfängerdichtegleichung und Einsetzen in die Uhrströme. Die 72 Punkte testen die Auswertungsformel. Die kontinuierliche Hülle folgt aus dem Intervallbeweis, und eine stationäre Einbettung wird nur für die gesondert vollständig konstruierten Nullarme behauptet. Die Vorgaben und die ergänzende Toleranzfrage sind jeweils lokal vor der betreffenden Rechnung gehasht, ohne externen Zeitstempel.

Alle **60 physischen P3-Prüfpunkte bleiben auf `NOT_RUN`**. Der nächste physikalische Nachweis müsste eine Vorbereitung realisieren, die den tatsächlichen Nullstrom in einem bekannten Band hält oder die Identität der Nullzustände für zwei Quellenarme unabhängig belegt.

[Öffentlicher N19-Ausgangsstand, PR 388](https://github.com/thomasmgfeller/x6-spectral-astrolabium/pull/388)
