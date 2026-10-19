"""Presentation of the frozen summary, with no changes to estimator or gates."""
import json
from pathlib import Path
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np

HERE=Path(__file__).resolve().parent
s=json.loads((HERE/'results/summary.json').read_text())
high=s['cells'][-1]; names=['legacy64','balanced64','oracle_cap']
labels=['Bisherige Suche','Eignung vor Begrenzung','Exakte Abstandskappe*']
rows=[]
def fmt(x): return '—' if x is None else f'{x:.3f}'
for cell in s['cells']:
    for name,label in zip(names,labels):
        m=cell['methods'][name]
        rows.append('| '+' | '.join([str(cell['rho']),label,str(m['available']['success'])+'/16',
            fmt(m['cap_recall']['mean']),fmt(m['oracle_metric_error']['rms']),
            str(m['chart_available']['success'])+'/16',fmt(m['chart_metric_error']['rms'])])+' |')
p=high['paired']; a=high['methods']['legacy64']; b=high['methods']['balanced64']; o=high['methods']['oracle_cap']
gate_rows=['| '+k+' | '+('PASS' if v else 'FAIL')+' |' for k,v in s['primary_gates'].items()]
text=f'''# Eigenzeit / BK: Ankersuche isoliert geprüft

**Ergebnis: `{s['decision']}`; weiterhin `HOLD_PHASE3`.** Die neue Suche
schliesst einen nachgewiesenen Abdeckungsfehler. Die Genauigkeit der Metrik
erfüllt weiterhin nicht die ursprüngliche Fehlergrenze. Es gibt keine neue
Krümmungsfreigabe und keine allgemeine Widerlegung des BK-Verfahrens.

## Was wurde geändert?

Der ursprüngliche Code wählt die 64 tiefsten gemeinsamen Anker aus und prüft
erst danach, ob diese geeignet sind. Der neue Kandidat prüft die unveränderten
Eignungskriterien zuerst und begrenzt erst die gültigen Anker auf 64. Dichte,
Skalen, Balancierungsregel, Median, Operator und Grenzwerte bleiben identisch.
Ein explizites 85-Ereignis-Gegenbeispiel zeigt einen gültigen Anker auf Rang 66,
den die alte Suche verpasst. Zeitumkehr und Umnummerierung ändern dies nicht.

Für jede Wolke wird zusätzlich die exakte räumliche Abstandskappe auf denselben
diskreten Schalen ausgewählt. Diese *Kontrolle* nutzt Simulationskoordinaten;
sie ist kein intrinsisches Verfahren und keine theoretische Fehleruntergrenze.
Zeitpunkte, Kettenskala und diskrete Schalen bleiben dabei unverändert.

## Vorab festgelegt und vollständig ausgeführt

- Öffentlicher Vertrag: `4b7e7aea9ba935295dd0d21963080c31f8ffc9a9`.
- Öffentlicher Quellen- und Analysefreeze: `{s['source_commit']}`.
- Sechs separate Entwicklungswolken; danach 48 neue Testwolken, 16 je Dichte.
- Alle drei Verfahren arbeiten je Wolke auf derselben kausalen Ordnung.
- Keine nachträgliche Parameterauswahl, keine ersetzten Seeds.
- Laufzeit {s['seconds']:.2f} Sekunden; Spitzen-RSS {s['peak_mib']:.1f} MiB.
  Vorgaben: 600 Sekunden / 2048 MiB. Einzelarmzeiten nutzen gemeinsame Caches
  und begründen keinen belastbaren Geschwindigkeitsvergleich.

[Protokoll](PROTOCOL.md), [Vertrag](contract.json), [Umsetzung](IMPLEMENTATION.md),
[Entwicklung](development/execution.json), [Testquellen und Rohdaten](results/execution.json),
[vollständige Auswertung](results/summary.json), [Replay](VERIFICATION.json).

## Vergleich auf den neuen Daten

| Dichte | Verfahren | Verwendbar | Wahre Kappenpunkte erfasst | Metrik-RMS, glatte Felder | Intrinsische Karte | Metrik-RMS, intrinsische Felder |
| --- | --- | --- | --- | --- | --- | --- |
{chr(10).join(rows)}

Erfasste Kappenpunkte: Mittel der wolkenweisen Recall-Anteile, ohne Referenzpunkt.
Metrikfehler: relative Frobeniusnorm, als RMS über verfügbare Wolken; Grenze
**0,5**. Fehlende Fälle bleiben im Nenner der Verfügbarkeit und Signatur.
*Exakte Abstandskappe ist ausschliesslich die oben beschriebene Kontrolle.

![Abdeckung und Metrikfehler](comparison.png)

Bei höchster Dichte gewinnt die neue Suche {p['gained']} verwendbare Wolken und
verliert {p['lost']}. Die Verfügbarkeit steigt von {a['available']['success']}/16
auf {b['available']['success']}/16. Der Wilson-95%-Bereich der neuen Quote ist
{100*b['available']['wilson95'][0]:.1f}–{100*b['available']['wilson95'][1]:.1f}%;
16 Wolken begründen noch keine präzise Erfolgswahrscheinlichkeit.
Der exakte zweiseitige McNemar-Test ergibt p={p['mcnemar_exact_two_sided_p']:.6g}
als deskriptive Ergänzung des gepaarten Vergleichs. Die drei primären Kriterien
werden gemeinsam berichtet; es wird keine korrigierte Mehrfachtest-Aussage
oder allgemeine Überlegenheit daraus abgeleitet.

Die zusätzliche Abdeckung bringt auch Fehlselektionen mit sich: Nur
{100*b['cap_precision']['mean']:.1f}% der ausgewählten Nichtreferenzpunkte liegen
im Mittel tatsächlich in der gewünschten Kappe. Der bedingte räumliche RMS-Fehler
liegt bei {b['space_relative_rmse']['rms']:.3f} statt {a['space_relative_rmse']['rms']:.3f};
dabei werden unterschiedliche Mengen bestimmbarer Paare verglichen. Der
Kandidat ist deshalb als Abdeckungsverbesserung, nicht als allgemein genaueres
Verfahren einzustufen.

Der mittlere gepaarte Recall-Gewinn beträgt {p['recall_change']['mean']:.3f}
(Standardfehler {p['recall_change']['se']:.3f}, {p['recall_change']['n']} Wolken).
Von {p['originally_missing_distances']} zuvor fehlenden Abständen werden
{p['rescued_distances']} zusätzlich bestimmbar. Diese Paarzahlen sind keine
unabhängigen Replikate; die statistische Einheit bleibt die ganze Wolke.

| Vorab festgelegtes Abdeckungskriterium | Befund |
| --- | --- |
{chr(10).join(gate_rows)}

## Warum dies noch keine genaue Metrik ergibt

Die Mengen verfügbarer Wolken unterscheiden sich. Auf den {p['common_available']}
gemeinsam verfügbaren hochdichten Wolken beträgt der Metrik-RMS
{fmt(p['common_legacy_metric_error']['rms'])} für die alte und
{fmt(p['common_balanced_metric_error']['rms'])} für die neue Suche. Dieser kleine
gemeinsame Ausschnitt darf nicht als alleinige Leistungsbewertung dienen.
Auf sämtlichen verfügbaren Kandidatenwolken ist der Fehler
{fmt(b['oracle_metric_error']['rms'])}; bei exakt ausgewählter Abstandskappe
{fmt(o['oracle_metric_error']['rms'])}. Beide werden an derselben Grenze geprüft.

Auch die Kontrolle mit korrekter räumlicher Auswahl verfehlt damit die Vorgabe.
Fehlende Anker sind also ein realer Engpass, aber ihre Behebung reicht in diesem
Pilot nicht aus. Die Kontrolle isoliert keinen einzelnen verbleibenden Fehler:
Kettenskala, schwankende Schalen, Geodätenrichtung, Winkelverteilung und Ränder
können beitragen. Es ist kein Beleg, dass einer davon allein verantwortlich ist.

Die Produktidentität berechnet für beliebige Felder exakt die gewichteten
zweiten Differenzmomente der jeweiligen diskreten Schablone. Ihr algebraisches
Bestehen allein garantiert daher keine geometrisch richtigen Momente.
Konstanten-, Produkt- und affine Kartenkontrollen bestehen im gesamten Lauf;
beide intrinsischen Arme bestehen Umnummerierungen auf je einer Wolke jeder
Dichte. Der vollständige numerische Replay ist in VERIFICATION.json dokumentiert.
Das ist interne Reproduzierbarkeit, keine unabhängige externe Replikation.

## Nächster begrenzter Schritt

Vor weiteren Dichteerhöhungen sollten die zeitlichen und räumlichen Beiträge
zur Metrik getrennt als Momentenbilanz geprüft werden. Dazu zuerst auf bekannten
Entwicklungsdaten Kettenskala, Schalenstreuung und Richtungsschwankungen messen,
mit explizit gekennzeichneten Kontrollen jeweils einen Beitrag ersetzen und
die Auswirkung bestimmen. Eine darauf beruhende neue intrinsische Korrektur
braucht wieder einen eingefrorenen Vertrag und frische Testdaten.

Die bisherigen 48 Phase-1/2-Wolken und alle BD-C2-Ergebnisse bleiben unverändert.
Bekannte Intensität, transportierte Zufallsmarken und 2+1 Minkowski sind weiterhin
Voraussetzungen. 3+1, unbekannte Dichte, Konvergenz und Krümmung sind nicht validiert.
Die zeitlich beendeten Hintergrundagenten werden durch diesen Einzelauftrag
nicht neu gestartet.
'''
(HERE/'RESULTS.md').write_text(text)
plt.rcParams.update({'font.size':10,'axes.spines.top':False,'axes.spines.right':False})
fig,axes=plt.subplots(1,2,figsize=(10.8,4.4),layout='constrained')
colors=['#697586','#147d73','#bd6418']; xs=np.arange(3); offset=.24
for j,(name,label,color) in enumerate(zip(names,['Legacy 64','Balance before cap','Exact cap control'],colors)):
    values=[c['methods'][name] for c in s['cells']]
    axes[0].bar(xs+(j-1)*offset,[m['available']['success'] for m in values],width=offset,label=label,color=color)
    axes[1].plot(xs,[m['oracle_metric_error']['rms'] for m in values],marker='o',color=color,label=label)
axes[0].set(ylabel='Usable clouds / 16',ylim=(0,17),title='Coverage improves')
axes[0].set_yticks([0,4,8,12,16]);axes[0].legend(fontsize=8,loc='upper left')
axes[1].axhline(.5,color='#b42318',linestyle='--',label='Prespecified limit 0.5')
axes[1].set(ylabel='Relative metric RMS (available clouds)',title='Metric accuracy remains unresolved')
axes[1].set_ylim(bottom=0);axes[1].legend(fontsize=8,loc='upper left')
for ax in axes:
    ax.set_xticks(xs,[str(c['rho']) for c in s['cells']]);ax.set_xlabel('Density (2+1 Minkowski)');ax.grid(axis='y',alpha=.15);ax.set_axisbelow(True)
fig.suptitle('48 fresh paired test clouds • coverage result does not release phase 3',fontsize=12)
fig.savefig(HERE/'comparison.png',dpi=160)
plt.close(fig)
