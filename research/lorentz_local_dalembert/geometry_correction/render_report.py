"""SPDX-License-Identifier: Apache-2.0
Presentation only. No inference, calibration, test or decision logic.
"""
import json
from pathlib import Path
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

HERE=Path(__file__).resolve().parent
def main():
    s=json.loads((HERE/'results/summary.json').read_text());test=s['phases']['test'];cal=s['phases']['calibration']
    v=test['variants'];full=v['full'];base=v['baseline'];pair=s['paired_test_comparison']
    names={'baseline':'Ausgangsgeometrie','unweighted':'Ohne Gewichtung','diagonal':'Einzelvarianzen','full':'Volle Fehlermatrix'}
    groups={'root':'Wurzelpaare','support_spacelike':'Raumartige Stützpunktpaare','support_causal':'Kausale Stützpunktpaare'}
    plt.rcParams.update({'font.family':'DejaVu Sans','font.size':10,'axes.spines.top':False,'axes.spines.right':False})
    fig,ax=plt.subplots(1,2,figsize=(12.5,5),gridspec_kw={'width_ratios':[1.2,1]})
    colors=['#7397bd','#b89039','#d45e47'];xx=np.arange(3);width=.23
    for j,(name,color) in enumerate(zip(['unweighted','diagonal','full'],colors)):
        ratio=[v[name]['groups'][g]['rmse']/base['groups'][g]['rmse'] for g in groups]
        ax[0].bar(xx+(j-1)*width,ratio,width,label=names[name],color=color)
    ax[0].axhline(1,color='#203348',lw=1.3);ax[0].axhline(1.05,color='#9f3939',lw=1,ls=':')
    ax[0].set_xticks(xx,['Wurzel','Raumartig','Kausal']);ax[0].set_ylabel('Gruppen-RMSE / Ausgangs-RMSE')
    ax[0].set_title('Fehler nach geometrisch zulässiger Korrektur',loc='left',fontweight='bold')
    ax[0].legend(frameon=False,fontsize=8,loc='upper left');ax[0].grid(axis='y',alpha=.15);ax[0].set_axisbelow(True)
    comps=['baseline','diagonal','unweighted']
    for j,name in enumerate(comps):
        point=pair[name]['rmse_ratio_full_over_comparator'];lo,hi=pair[name]['paired_percentile_bootstrap_95']
        ax[1].plot([lo,hi],[j,j],color='#d45e47',lw=3);ax[1].scatter([point],[j],color='#203348',s=40,zorder=3)
    ax[1].axvline(1,color='#203348',lw=1,ls='--');ax[1].set_yticks(range(3),[names[n] for n in comps]);ax[1].invert_yaxis()
    ax[1].set_ylim(2.6,-.6);ax[1].set_xlabel('RMSE volle Matrix / Vergleichs-RMSE')
    ax[1].set_title('Gepaarter Vergleich ganzer Testwolken',loc='left',fontweight='bold');ax[1].grid(axis='x',alpha=.15)
    fig.suptitle(f'Geometriekorrektur · {test["complete"]} unabhängige Testwolken · flach 2+1',x=.06,ha='left',fontweight='bold',fontsize=15)
    fig.text(.06,.025,'Links: niedrigere Werte sind besser; gepunktet: 5%-Gruppengrenze. Rechts: approximative 95%-Bootstrap-Intervalle.',fontsize=9,color='#4b5968')
    fig.tight_layout(rect=(.02,.06,.99,.92));fig.savefig(HERE/'results/geometry_correction.png',dpi=180);plt.close(fig)
    coverage=full['simultaneous'];ci=coverage['clopper_pearson_95']
    source=json.loads((HERE/'source_freeze.json').read_text())['commit']
    execution=json.loads((HERE/'results/test/worker-0/execution.json').read_text());calcommit=execution['execution_commit']
    lines=['# Kontrollierte Geometriekorrektur mit gemeinsamem Fehlermodell','',
        f'**{s["decision"]}**. '+('Alle vorab festgelegten Pilotkriterien sind erfüllt.' if all(s['gates'].values()) else 'Die vorab festgelegten Pilotkriterien sind nicht vollständig erfüllt.'),'',
        f'128 neue Simulationsversuche im bestehenden **flachen 2+1-Modell bei rho=32768**: {cal["complete"]} auswertbare Kalibrierungswolken, {test["complete"]} unabhängige Testwolken und {cal["abstentions"]+test["abstentions"]} dokumentierte Abstentionen. Keine Ersatzwolken, keine Änderung der Kriterien nach Testbeginn.','',
        f'Die volle Fehlermatrix verändert den primären Geometrie-RMSE gegenüber der Ausgangsgeometrie um **{100*(pair["baseline"]["rmse_ratio_full_over_comparator"]-1):+.1f}%**. Bei kausalen Stützpunktpaaren beträgt die Änderung **{100*(s["group_rmse_ratios_full_over_baseline"]["support_causal"]-1):+.1f}%**. Positive Änderungen bedeuten größere Fehler. Der frühere Kalibrierungserfolg aus PR77 belegt damit keinen Nutzen dieser konkreten Korrektur.','',
        f'Die gemeinsame Testabdeckung der vollen Matrix ist **{coverage["covered"]}/{coverage["n"]} = {coverage["rate"]:.2%}**, mit exaktem 95%-Binomialintervall [{ci[0]:.2%}, {ci[1]:.2%}]. Alle vier Varianten verfehlen die vorab verlangte beobachtete 95%-Rate knapp. Das allein widerlegt keine marginale Conformal-Garantie; die Fehlerzunahme ist ein separater und deutlich größerer Befund.','',
        'Das eingefrorene Gruppenmodell aus PR77 liefert dieselben biaszentrierten Intervallziele für drei Korrekturen. Verglichen werden die unveränderte relationstreue Ausgangsgeometrie, ungewichtete Anpassung, Diagonalgewichtung und die volle gemeinsame Fehlermatrix. Der Vergleich volle Matrix/Diagonal isoliert die Nutzung der Kreuzterme innerhalb dieses Algorithmus.','',
        'Jede übernommene Lösung ist eine realisierbare 2+1-Geometrie mit exakt derselben beobachteten Kausalordnung. Ein kanonischer Gram-Rahmen, eine feste Vertrauensregion und eine konvexe innere Kausalregion begrenzen den lokalen SLSQP-Schritt. Die Zielfunktion ist nichtkonvex; ein globales Optimum wird nicht behauptet. Gescheiterte Korrekturen liefern die Ausgangsgeometrie und bleiben in allen Vergleichen enthalten.','',
        '![Geometriekorrektur im unabhängigen Test](results/geometry_correction.png)','','## Unabhängiger Test','',
        '| Variante | Gruppenbalancierter RMSE | Ungewichteter Intervall-RMSE | Gemeinsame Abdeckung | Rückfall auf Ausgangsgeometrie | Ordnungsverletzungen |',
        '|---|---:|---:|---:|---:|---:|']
    for name,x in v.items():
        cov=x['simultaneous'];lines.append(f'| {names[name]} | {x["group_balanced_rmse"]:.6f} | {x["interval_rmse"]:.6f} | {cov["rate"]:.2%} | {x["fallbacks"]} | {x["order_violations"]} |')
    lines+=['',f'Die direkt biaszentrierten, nicht zwingend geometrisch realisierbaren Intervalle haben einen gruppenbalancierten RMSE von {test["unconstrained_bias_group_balanced_rmse"]:.6f}. Dies ist nur eine Diagnose und kein fünfter freigegebener Kandidat.','',
        '| Vergleich volle Matrix / Referenz | RMSE-Verhältnis | Gepaarter 95%-Bootstrap-Bereich |','|---|---:|---:|']
    for name,x in pair.items():
        lo,hi=x['paired_percentile_bootstrap_95'];lines.append(f'| {names[name]} | {x["rmse_ratio_full_over_comparator"]:.6f} | [{lo:.6f}, {hi:.6f}] |')
    lines+=['','Kleinere Verhältnisse sind besser. Resampling-Einheit ist die ganze Wolke, einschließlich aller Paare und Varianten; 4000 gepaarte Bootstrap-Ziehungen. Die Bereiche sind approximative Pilot-Evidenz.','',
        '| Fehlergruppe | Ausgangs-RMSE | RMSE volle Matrix | Verhältnis |','|---|---:|---:|---:|']
    for g,label in groups.items():lines.append(f'| {label} | {base["groups"][g]["rmse"]:.6f} | {full["groups"][g]["rmse"]:.6f} | {s["group_rmse_ratios_full_over_baseline"][g]:.6f} |')
    labels={'minimum_complete':'Mindestens 48 vollständige Wolken pro Phase','all_orders_exact':'Alle gelieferten Geometrien erhalten die Ordnung exakt',
        'full_fallback_rate':'Höchstens 10% Rückfälle je Phase','full_joint_coverage':'Mindestens 95% beobachtete gemeinsame Testabdeckung',
        'practical_improvement_over_baseline':'Mindestens 1% RMSE-Verbesserung gegenüber Ausgangsgeometrie',
        'paired_improvement_over_baseline':'Bootstrap-Obergrenze gegenüber Ausgangsgeometrie unter 1',
        'paired_improvement_over_diagonal':'Bootstrap-Obergrenze gegenüber Diagonalgewichtung unter 1',
        'every_group_noninferior':'Keine Gruppe mehr als 5% schlechter'}
    lines+=['','## Vorab festgelegter Entscheid','','| Kriterium | Ergebnis |','|---|---|']
    for name,passed in s['gates'].items():lines.append(f'| {labels[name]} | {"PASS" if passed else "FAIL"} |')
    lines+=['','## Unsicherheit und Grenzen','',
        'Die Unsicherheitsradien aller vier Varianten wurden separat auf denselben neuen Kalibrierungswolken festgeschrieben. Die alte Fehlermatrix dient nach der Korrektur nur als Residuenskalierung; sie wird nicht als fortgepflanzte Koordinatenkovarianz ausgegeben. Die gemeinsame Abdeckung umfasst sämtliche Intervalle, Wurzel-Gram-Einträge und nichtleeren Blockmittel einer Wolke. Exakte Binomialintervalle, Familienabdeckungen und Bandbreiten stehen in `results/summary.json`.','',
        f'Die marginale Split-Conformal-Untergrenze je fester Variante beträgt {s["calibration_rule"]["marginal_joint_coverage_bound_per_variant"]:.3%} unter den festgelegten Austauschbarkeits- und Akzeptanzannahmen. Sie ist keine bedingte Zusage für jede Ordnung und keine gemeinsame Garantie über alle Varianten.','',
        '**HOLD_EMBEDDING_COVARIANCE**, **HOLD_KALMAN**, **HOLD_PHASE3** und **METADATA_HOLD** bleiben bestehen. Dieses Experiment qualifiziert weder eine konditionale Koordinatenkovarianz noch einen Online-Filter, einen Operatorvorteil, Krümmung oder radiale 4D-Geometrie. Ein anderer Kandidat wird bei einem negativen Primärentscheid nicht nachträglich ausgewählt.','',
        '## Reproduktion und öffentliche Reihenfolge','',
        f'- Quell-, Kriterien- und Seed-Freeze: `{source}`.',f'- Kalibrierungs-Freeze vor Testbeginn: `{calcommit}`.',
        '- `source_freeze.json`: 277 unveränderte Quell- und Eingabedateien.',
        '- `results/calibration` und `results/test`: alle 128 Versuche, Vorhersagesiegel und Ressourcenprotokolle.',
        '- `gc_controls.py`: 14 analytische Kontrollgruppen einschließlich negativer Kontrollen für sämtliche acht Entscheidungskriterien.',
        '- `gc_verify.py`: Quellen/Abstammung, Vorhersagesiegel, neu erzeugte wahre Koordinaten, erneute Optimierungen, Auswertung, Kalibrierung und Bootstrap. Gespeicherte Auswahl/Rekonstruktion werden wiederverwendet. Optimierer-Ausgaben werden auf invarianten Intervallen mit absoluter und relativer Toleranz 2e-5 verglichen; Iterationszahlen und Koordinatengauges müssen nicht bytegleich sein.','',
        '```sh','OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 python research/lorentz_local_dalembert/geometry_correction/gc_controls.py',
        'OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 python research/lorentz_local_dalembert/geometry_correction/gc_verify.py','```','',
        'Methoden, genaue Grenzen und Quellen: [PROTOCOL.md](PROTOCOL.md). Die Grafik und dieser Bericht werden ausschließlich aus der eingefrorenen Auswertung erzeugt.']
    (HERE/'README.md').write_text('\n'.join(lines)+'\n')
    print(json.dumps(dict(report=str(HERE/'README.md'),decision=s['decision'])))
if __name__=='__main__':main()
