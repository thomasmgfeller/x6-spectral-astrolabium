# Radiuskontrast der vorhandenen N22-Wirkung

Die Rechnung verwendet die N22-Ordnung 216141/229383/0/+, die beiden gepinnten Randpräparationen und das flache Zwei-Kugel-Gegenbeispiel aus [PR 419](https://github.com/thomasmgfeller/x6-spectral-astrolabium/pull/419). Die deklarierten Rohzeiten Y und Gewichte w definieren bei verschwindender Quelle und verschwindenden drei Nachimpulsen den feldabhängigen Ausdruck

    F = 19 Σⱼ wⱼ + Σᵢ≺ⱼ kᵢⱼ wⱼ (Yⱼ−Yᵢ)².

Die Koeffizienten k sind die Archiv-Schichtwerte 1, −9, 16, −8, 0 (ab vier Zwischenereignissen), mit Abzug 10⁻¹¹ an den vier Geräteabfragen 15→16, 16→18, 17→18 und 18→7. Der reine ungeschmierte Ordnungswert beträgt F₄ = N − N₀ + 9N₁ − 16N₂ + 8N₃ = 28. F bezeichnet hier die Skalierung der Variation nach den Feldern. Quellen- und Gerätebedingungen folgen aus dem publizierten Vergleichsversuch.

Die engen rationalen Wirkungseinschliessungen unterscheiden die schwere und leichte Feldpräparation. Für jede einzeln bleibt bei einer gemeinsamen Realisierung von Y,w und der Relation der komplette Polynomwert F unter beiden kinematischen Kugelergänzungen gleich. Der gepaarte Kontrast verschwindet identisch. Ein separates Subtrahieren zweier abstrakter Intervallhüllen würde die Gleichheit der Unbekannten verlieren. Dasselbe Argument gilt für die Variationen in Y und w und für die aus der Ordnung berechnete Gravitation F₄. Für eine neue Randphysik, bei der die äussere Materialoberfläche in die Wirkung, das Maß oder die Präparation eingeht, liefert der aktuelle Ausdruck keinen Wert.

Die als Außenereignisse vorgeschlagenen 17,20 liegen zugleich in der strikten Vergangenheit von 18. Der späte Kragen hat bei beiden Präparationen durchweg positive Gewichte und liegt zeitlich außerhalb des Fensters. Ein positiver Kragen ist allein keine materielle Außenraum-Messung. Die vier Fenstereignisse 17,18,19,20 liegen strikt nach der Modelluhr 1/2.

## Lokaler Kontrollversuch

Je Ausgangskugel verändert der Prüfer den Radius bei x=1/2 in einem geschlossenen Intervall von ±1/100000 Einheiten. Zentrum und Kontraktionsgeschwindigkeit bleiben fest. Die seitlichen Abstände der 22 Stichproben und der drei Geraden 3/4/5 durch 11 bleiben für beide Präparationen strikt auf derselben Seite. Es ist möglich, die 19 positiven Stichproben durch ein passendes radiales Profil zu realisieren, da ihre normierten Radialkoordinaten auch über die neuen Radius-/Zeitboxen getrennt bleiben (vgl. Konstruktion in PR 413). Für jede gerade Bahn ist der Abstand zum festen Zentrum minus dem affinen Radius konvex in der Zeit. Negative Werte an beiden Fenstergrenzen garantieren daher die Innenlage auf dem gesamten Zeitintervall. Die zusätzlich geprüften Radiusumgebungen sind [0,99999;1,00001] und [1,78499;1,78501]. Ihr Inneres erlaubt eine lokal konstante Familie in allen vorhandenen Beobachtungsdaten.

Ist auf einem solchen Intervall eine Zustandszuweisung ausschließlich aus diesen konstanten Eingaben und mit festem Messapparat vorgeschrieben, ist deren lokale Ableitung nach dem Radius null. Ihre Quanten-Fisher-Information für den Radius ist dann null. Eine physisch dynamische Zustandsfamilie auf anderen gekoppelten Geschichten und ein radiusabhängiger Detektor erfordern eigene Daten. Für sie ist die Information mit dem Archiv nicht bestimmt. Aus bloßer Gleichheit der beiden isolierten Endpunktzustände wäre kein allgemeines Urteil über lokale Ableitungen ableitbar.

## Offline-Aufruf

    python3 -B wirkungszeuge.py Vergleichspaar.json Gegenzeuge.json Ortskoordinaten.json

Die Originaleingaben liegen relativ zum Verzeichnis der [publizierten Studie](https://github.com/thomasmgfeller/x6-spectral-astrolabium/tree/e2e2597ce45b9fa1aa5982c99943cde002bda8a0/research/rax_cqg/dust_collapse/n22_n24_sondengeometrie_und_vakuumkontrolle_v0_1) unter eingaben/Vergleichspaar.json, schalen/Gegenzeuge.json und eingaben/Ortskoordinaten.json. Das Skript überprüft deren SHA-256-Werte. Es prüft den feldabhängigen Funktionswert an rationalen Mittelpunkten zusätzlich über die Empfängerableitungen, und schliesst ihn über die vollständigen archivierten Feldintervalle ein. Kugelgeometrie und Felddiagnose sind getrennte Kontrollen. Eine Zustandsrekonstruktion oder Bornsche Folgerung ist in diesen Daten nicht festgelegt.

- [N22-Quellen, Kragen und Massendiagnosen](https://github.com/thomasmgfeller/x6-spectral-astrolabium/blob/e2e2597ce45b9fa1aa5982c99943cde002bda8a0/research/rax_cqg/dust_collapse/n22_anfangsladung_zwei_massen_transfer_v0_1/README.md)
- [Koeffizienten und Eichskalen im N22-Pilot](https://github.com/thomasmgfeller/x6-spectral-astrolabium/blob/e2e2597ce45b9fa1aa5982c99943cde002bda8a0/research/rax_cqg/dust_collapse/n22_frueher_radiuspilot_massentransport_v0_1/pruefen.py)
- [Exakte Prüfung der vollständigen feldabhängigen Wirkung mit Gerätebeiträgen](https://github.com/thomasmgfeller/x6-spectral-astrolabium/blob/e2e2597ce45b9fa1aa5982c99943cde002bda8a0/research/rax_cqg/dust_collapse/n22_ein_drittes_ereignis_fuer_die_staubrandmessung_v0_1/kontrollen22.py)
- [Ordnungsterm und Konvention für isolierte Teilordnungen](https://github.com/thomasmgfeller/x6-spectral-astrolabium/blob/e2e2597ce45b9fa1aa5982c99943cde002bda8a0/research/rax_cqg/dust_collapse/n15_materie_vakuum_und_masseneichung_v0_1/basis/inputs/gluing.py)
