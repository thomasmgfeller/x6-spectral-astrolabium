# N22 · Matched clock controls for the dust vacuum and mass normalization

Die feste Ordnung 216141/229383/0/+ umfasst 22 Ereignisse und 152 Paare in der strikten Transitivrelation. Beim quellenfreien Staub dieser Studie sind 0 bis 3 sowie 7 bis 10 Dirichlet-Kragen. Die 14 übrigen Uhren sind frei. Das Ordnungspaar und die Elemente der Kragenuhrhülle stammen aus der in PR 418 veröffentlichten Vergleichsdatei. Die im Folgenden konstruierten Innenzeiten sind neue Prüfzeugen.

## Bei positiven späten Randgewichten scheitert das vollständig leere Innere

Setzt man alle Innengewichte auf null, können in der Uhrgleichung an 6 nur die vier späten Randgewichte als positive Empfänger beitragen. Die Anzahlen der offenen Zwischenereignisse von 6 zu den Punkten 7, 8, 9 und 10 betragen 3, 4, 5 und 6. Die zugehörigen Koeffizienten sind −8, 0, 0 und 0. Der eingehende Term ist proportional zu w₆=0. Damit gilt G₆=−8 w₇(Y₇−Y₆)<0. Die strikte Uhrordnung 6 vor 7 und die gesicherte Positivität von w₇ gelten bei schwerer und leichter Präparation. Der Widerspruch ist unabhängig von den unbekannten Innenzeiten. Ereignis 15 liefert dasselbe Argument. Damit scheitert das vollständige Staubvakuum im Inneren schon an je einer Uhrgleichung, wenn die positive späte Dirichlet-Besetzung beibehalten wird.

## Nullkontrolle mit eigens leer präparierten Kragen

Bei wᵢ=0 an allen 22 Punkten und unveränderten Gerätekoeffizienten ist jeder der 152 gerichteten Wirkungsströme identisch null; ebenso jeder der 22 Uhrgradienten, die signierte Anfangsladung Q und das Verweildauermass B. Der Nachweis gilt für dieselben Randuhrintervalle und für alle Zwischenwerte in ihrer gemeinsamen rechteckigen Hülle. Die neuen, rational gewählten 14 Innenzeiten in Nullkontrolle.tsv lassen eine strikte Uhrordnung mit Mindestabstand 3/100 zu. Beide Zeitwerte 18 und 19 liegen gemeinsam mit 17 und 20 weiterhin im frühen Fenster. In dieser Präparation haben alle vier Gewicht null.

Das Nullatom der veröffentlichten regulierten Feldvariation verlangt an unbesetzten Innenereignissen keine Variation nach der Dichte. Als stärkere Bedingung prüfen wir zusätzlich Dⱼ=19+Σᵢ kᵢⱼ(Yⱼ−Yᵢ)²≥0 für sämtliche 14 Innenereignisse. Dies ist die einseitige Anstiegsbedingung in der Konvention +D für zulässige Dichtezunahmen ab null. Die Mindestuntergrenze ist grösser als 19/100; sie tritt an 21 auf. Die Nullkontrolle enthält mithin auch unter dieser Zusatzforderung ein Beispiel. Sie behauptet keine Auswahl dieses Zustands durch eine Pfadintegraldynamik oder durch Minimierung der vollständigen Geometrie-Materie-Wirkung. Die acht Kragengewichte sind Dirichlet-Daten. Falls man auch diese acht Gewichte als einseitig variabel behandelt und ihre Uhrenhülle beibehält, gilt D₂<−15 für sämtliche zulässigen frühen Uhren. Diese andere Randbedingung scheitert somit ebenfalls exakt.

## Positiver Massengewinn bleibt unbestimmt

In jeder feldabhängigen Kante steht das Empfängergewicht linear. Das frühe Ideal E={0,1,2,3} ist nach unten abgeschlossen. Geht w außerhalb E in λw über, skalieren bei festem Y alle freien Uhrgradienten mit λ. Die Dichtegleichungen hängen nur von Y ab. In −Σᵢ∈E Gᵢ heben sich die Beiträge innerhalb E weg. Deshalb skalieren die Ladung Q und die lineare Aufenthaltsauslese B ebenfalls mit λ. Auf der aus der Vorstudie bekannten positiven Lösung bleibt mit jedem 0<λ≤1 ein (anders randpräparierter) Modellzweig zulässig, sofern die späten Dirichlet-Gewichte mitskaliert werden. Modellmassenziele dürfen bei diesem Argument keine zusätzlich festgehaltenen Randdaten sein. Bei λ=0 und positiven frühen Gewichten können interne Kragenströme bleiben. Die oben ausgewiesene vollständige Nullkontrolle setzt deshalb auch die frühen Gewichte auf null. Eine rein ordnungs- oder nur uhrabhängige Auslese ist gegenüber der positiven Gewichtsskalierung blind.

Ein sicherer Nullpunkt eines linearen oder affinen Messkanals fixiert seine additive Verschiebung, lässt den positiven Multiplikator offen. Angenommen, man fordert für zwei auf der identischen Ordnung definierte Kalibrierziele die **Modellzahlen** 1/4 und 4. Jeder nur aus derselben unmarkierten Ordnung abgeleitete gemeinsame Schätzwert m besitzt maximalen relativen Zielfehler von mindestens 15/17. Das Minimum liegt bei m=8/17, wo sich beide Fehler gleichen. Diese arithmetische Schranke betrifft diese beiden geforderten Labels und deren relativen Fehler. Als gemessene physische Massen sind sie weiterhin unbestätigt. Ein unabhängiger positiver Gravitations- oder Ruhemassenstandard mit quantitativ geklärter Beziehung zur Staubladung fehlt der Vergleichsdatei.

Der Nullzeuge betrifft die Staub-Feldgleichungen auf einer festen Ordnung. Eine vollständig gekoppelte Gravitations-/Vakuumgeschichte, ein physisch nachgewiesenes Aussenfeld, ein positiver Masseneichpunkt und eine Fläche folgen daraus nicht. Acht physische Pilotradien und alle 60 P3-Prüfpunkte bleiben offen.

## Reproduktion

Mit Python ab 3.10 aus dem entpackten Verzeichnis ausführen. Der Prüfer benötigt nur die Standardbibliothek, liest die quellengeprüfte JSON-Eingabe, rekonstruiert den Schichtkern und gleicht beide Ausgaben byteweise ab.

```sh
python3 -B pruefen.py
```

[Quellenzustand der N22-Vergleichsdaten](https://github.com/thomasmgfeller/x6-spectral-astrolabium/tree/2c08c72af7fa7d075f50decc48c9531d64d61c66/research/rax_cqg/dust_collapse/n22_anfangsladung_zwei_massen_transfer_v0_1) · [Nullatom und klassische LTB-Kontrolle](https://github.com/thomasmgfeller/x6-spectral-astrolabium/tree/2c08c72af7fa7d075f50decc48c9531d64d61c66/research/rax_cqg/dust_collapse/n15_materie_vakuum_und_masseneichung_v0_1)
