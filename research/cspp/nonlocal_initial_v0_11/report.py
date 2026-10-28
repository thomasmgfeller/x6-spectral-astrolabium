"""Descriptive report only; authoritative decisions are verify.py and ball data."""
import gzip
import json
from pathlib import Path
from flint import arb,ctx

HERE=Path(__file__).resolve().parent
ctx.prec=256
d=json.load(gzip.open(HERE/'results/BENCHMARK_192.json.gz','rt'))
c=json.loads((HERE/'results/CHECKS.json').read_text())
lines=['# Ergebnisse: nichtlokaler Anfangsdatenadapter v0.11','',
       '**Status: METHOD_HOLD.** Konstruktion und Fehlerrechnung sind prüfbar; die geforderte Genauigkeit ist nicht qualifiziert.','',
       '## Geprüfter Umfang','',
       f"- {c['analytical_tests']} analytische Tests bestanden.",
       f"- {c['enclosed_target_comparisons']:,} eingeschlossene Zielgrößen zwischen 128 und 192 Bit verglichen; alle überlappen.".replace(',','.'),
       '- Dieselben acht Archivwolken; keine neuen Kausalsetknoten oder Zufallswolken.',
       '- Alle acht Tetraederzerlegungen rational zertifiziert; alle acht Projektionsgebiete enthalten die ursprüngliche Quellkugel.',
       '- Die exakte Projektion löscht die kompakte Quelle in keiner der acht Wolken vollständig aus. Das schließt d0_r01, d0_r04 und d0_r06 mit zuvor leerer lokaler Quellhistory ein.',
       '- Dieser Nichtauslöschungsnachweis folgt aus Integralbewahrung und dem positiven Quellintegral. Er ist kein Nachweis einer von null verschiedenen Detektorantwort.',
       '', '## Räumlicher Fehler der unveränderten Wellen','',
       'Relative L2-Projektionsfehler auf dem jeweiligen konvexen Projektionsgebiet D. Die Dezimalwerte sind gerundete Anzeigen; vollständige Ballintervalle stehen in den Rohdaten. Da die Projektion L2-optimal ist, sind diese Fehler zugleich die beste erreichbare Genauigkeit im hier festgelegten kontinuierlichen P1-Raum.',
       '', '| Wolke | History-Knoten | Tetraeder | k=2 | k=4 | k=8 |',
       '|---|---:|---:|---:|---:|---:|']
for r in d['rows']:
    v=r['levels'][-1]['relative_L2_projection_error']
    values=[100*float(arb(v[k][0]).mid()) for k in [1,2,3]]
    lines.append(f"| {r['key']} | {r['history_nodes']} | {r['tetrahedra']} | "+' | '.join(f'{x:.3f} %' for x in values)+' |')
lines+=['','Alle 24 nichtkonstanten Wellenfälle überschreiten die festgelegte relative Toleranz 0.001 nachweislich. Die acht konstanten Felder werden mathematisch exakt reproduziert und bestehen die numerische Prüfung. Die hier verwendete Partition der Eins allein bietet also keine ausreichende Wellenauflösung. Diese Aussage betrifft genau diesen P1-Raum, nicht jede denkbare nichtlokale Abbildung.','',
        '## Kompakte Quelle und zeitliche History','',
        'Für die acht kompakten räumlichen Projektionsfehler liefern die festen Unterteilungstiefen 0, 2 und 4 noch keine entscheidenden Grenzen. Nach Schnitt mit der allgemeinen Projektionsschranke bleibt jeweils im Wesentlichen das zulässige relative Intervall [0,1]. Dies ist fehlende Genauigkeitsqualifikation; daraus folgt keine positive Fehleruntergrenze für die kompakte Quelle.','',
        'Auf allen Archivknoten wird ausdrücklich H1 = P f + (t+1) P g verwendet. Allgemeine höhere History-Polynome und ihre Reste sind hergeleitet und als Funktion verfügbar; sie wurden nicht als weitere Archivmethoden getestet. Die kompakte Historygrenze benutzt die konservative globale KG-Restschranke des Vorgängers. Wellen werden direkt mit ihrer exakten Kontinuumshistory verglichen.','',
        '| Prüfpunkt | Bestanden | Bedeutung |',
        '|---|---:|---|',
        f"| Räumliche Projektionsbudgets | {c['spatial_budget_pass']}/40 | Acht Konstanten; 24 belegte Überschreitungen; acht kompakte Fälle unentschieden |",
        f"| Historyfehler bis zum Detektor | {c['history_budget_pass']}/80 | Kein Anfangsdatenbudget qualifiziert |",
        f"| Kombinierter Integrationsradius | {c['integration_budget_pass']}/80 | Bestehende Transferintervalle plus neue Lastintegration bleiben zu breit |",
        '',
        'Auch das exakte Erhalten von Konstanten auf der Anfangsfläche macht die lineare History nicht zur exakten massiven Zeitentwicklung. Die null bestandenen Historybudgets sind konservative Budgetentscheidungen; sie sind nicht 80 gemessene Fehleruntergrenzen.','',
        '## Stabilität und Aussagegrenzen','',
        f"Die berechneten oberen Schranken für die spektrale Konditionszahl der Massenmatrix liegen zwischen {c['condition_upper_range_display'][0]:.3f} und {c['condition_upper_range_display'][1]:.3f}. Die ideale Projektion ist L2-kontraktiv. Nodal- und Detektornormen sind separat eingeschlossen; daraus folgt keine universelle zeitliche Stabilität des nichtlokalen Operators.",
        '',
        'Die Vorgeschichte wird gegenüber der ausdrücklich angenommenen freien KG-Cauchyfortsetzung kontrolliert. Eine solche History folgt nicht allein aus f,g für einen beliebigen retardierten nichtlokalen Operator. Die geometrische Konstruktion nutzt außerdem die vorhandenen Raumkoordinaten und ist nicht intrinsisch aus der Kausalordnung gewonnen.','',
        'G1 bleibt HOLD. Eine vollständige kompakte Kontinuumsdetektorreferenz, die Operator-/Gebietsqualifikation, physikalische Rauschinterpretation und Dirac-Freigabe sind nicht Bestandteil dieses Ergebnisses.','',
        '## Reproduzierbarkeit','',
        'Die vollständige Herleitung steht in README.md, der ausführbare Adapter in adapter.py, der Archivlauf in run.py und die unabhängige Ausgabekontrolle in verify.py. Die endgültigen Läufe verwendeten Python-FLINT 0.9.0, NumPy 2.3.5 und SciPy 1.17.0. Beide Präzisionsläufe benötigten hier jeweils weniger als eine Minute. Ein Leistungsbenchmark wird daraus nicht abgeleitet.','',
        'Der Methodenstand ist lokal gehasht, jedoch nicht öffentlich vorregistriert. Vorläufige Ergebnisse einer zu breiten reinen Wertebereichsintegration bleiben in development_draft/ dokumentiert. Die endgültige Wellenintegration nutzt analytische Simplexmomente mit bewiesenem Rest. Daten und Toleranzen wurden nicht nachgezogen.','']
(HERE/'RESULTS.md').write_text('\n'.join(lines))
