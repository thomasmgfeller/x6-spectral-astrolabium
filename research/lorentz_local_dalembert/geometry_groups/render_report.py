"""SPDX-License-Identifier: Apache-2.0
Presentation only; the protocol, analysis and decisions remain frozen.
"""
import json
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from gg_common import HERE,load_phase,cfg

def main():
    s=json.loads((HERE/'results/summary.json').read_text());cal=s['phases']['calibration'];test=s['phases']['test']
    frozen=s['calibration_rule'];paired=s['paired_test_comparison'];models=test['models']
    source=json.loads((HERE/'source_freeze.json').read_text())['commit']
    executions,rows=load_phase('test');calcommit=executions[0]['execution_commit']
    accepted=[r for r in rows if r['evaluation']['status']=='COMPLETE']
    fig,axes=plt.subplots(1,2,figsize=(12.5,5.1),layout='constrained')
    colors={'pooled':'#42718e','grouped':'#b55b42'};groups=cfg()['groups'];x=np.arange(len(groups))
    axes[0].axhspan(.5,2,color='#d5e4d3',alpha=.65,label='Prespecified screening range')
    axes[0].axhline(1,color='#555555',ls='--',lw=1)
    for k,which in enumerate(cfg()['models']):
        values=[models[which]['arms']['original']['blocks'][g]['second_moment'] for g in groups]
        axes[0].plot(x+(k-.5)*.12,values,'o',ms=8,color=colors[which],label=which)
        q=frozen['models'][which]['quantile'];scores=sorted(r['evaluation']['models'][which]['score']/q for r in accepted)
        cov=models[which]['simultaneous']
        axes[1].plot(range(1,len(scores)+1),scores,'o-',ms=3,lw=1,color=colors[which],label=f"{which}: {cov['covered']}/{cov['n']}")
    axes[0].set(xticks=x,xticklabels=['Root','Spacelike support','Causal support'],ylabel='Mean squared standardized block error',title='Group calibration · original reconstruction')
    axes[0].legend(fontsize=9);axes[0].grid(axis='y',alpha=.18)
    axes[1].axhline(1,color='#222222',ls='--',label='Frozen band limit')
    axes[1].set(xlabel='Accepted test clouds, sorted within each model',ylabel='Joint score / own frozen radius',title='Independent joint test · both reconstruction arms')
    axes[1].legend(fontsize=9);axes[1].grid(alpha=.18)
    fig.suptitle('Separate root and spacelike geometry uncertainty · paired 2+1 study',fontsize=14)
    fig.savefig(HERE/'results/geometry_groups.png',dpi=170);plt.close(fig)
    target=models['grouped']['simultaneous'];reference=models['pooled']['simultaneous'];ci=target['clopper_pearson_95']
    decision='Die vorab festgelegten Pilotkriterien sind erfüllt.' if s['decision']=='GROUP_MODEL_PILOT_SUPPORTED' else 'Die vorab festgelegten Pilotkriterien sind nicht vollständig erfüllt; das Modell bleibt auf HOLD.'
    lines=['# Wurzel- und raumartige Geometriefehler getrennt prüfen','',f"**{s['decision']}**. {decision}",'',
        f"Im bestehenden **flachen 2+1-Modell bei rho=32768** wurden {cal['attempts']+test['attempts']} vollständig neue Wolken erzeugt. {cal['complete']} Kalibrierungswolken und {test['complete']} unabhängige Testwolken sind auswertbar; {cal['abstentions']+test['abstentions']} Abstentionen bleiben dokumentiert. Die {s['development']['development_complete']} früheren vollständigen Wolken dienen ausschließlich als Entwicklungsdaten.",'',
        f"Die gemeinsame Testabdeckung beträgt **{target['covered']}/{target['n']} = {100*target['rate']:.2f}%** für das gruppierte Modell und **{reference['covered']}/{reference['n']} = {100*reference['rate']:.2f}%** für den neu angepassten gemeinsamen Vergleich. Das exakte 95%-Binomialintervall der gruppierten Abdeckung ist [{100*ci[0]:.2f}%, {100*ci[1]:.2f}%]. Es umfasst jeweils beide Rekonstruktionsarme, alle Paarintervalle, Wurzel-Gram-Einträge und nichtleeren Gruppenmittel. Die Modelle besitzen eigene, vor dem Test eingefrorene Radien.",'',
        '![Grouped geometry uncertainty](results/geometry_groups.png)','',
        '## Was getrennt modelliert wurde','',
        '- **Wurzelpaare:** alle Paare mit dem gewählten Ursprung als Endpunkt.',
        '- **Raumartige Stützpunktpaare:** zwei Stützpunkte ohne beobachtete Kausalrelation.',
        '- **Kausale Stützpunktpaare:** die restlichen Stützpunktpaare, damit alle Abstände erfasst bleiben.','',
        'Die Gruppenzuordnung verwendet nur Wurzelidentität und beobachtete Ordnung. Das gruppierte Modell besitzt getrennte Bias- und Varianzanteile, erhält Abhängigkeiten über gemeinsame Punkte und ergänzt einen vorzeichenabhängigen gemeinsamen Skalenfehler. Dieser kann negative Kreuzkovarianzen zwischen zeit- und raumartigen Intervallquadraten darstellen. Alle Arbeitsmatrizen sind positiv definit. Sie sind keine identifizierte konditionale Koordinatenkovarianz.','',
        'Der Vergleich wurde auf genau denselben Entwicklungswolken neu angepasst; er ist nicht das unveränderte historische PR76-Modell. Beide Modelle verwenden dieselben Wolken- und Gruppengewichte sowie dieselbe interne Auswahl einer gedämpften Bias-Korrektur. Der Vergleich bewertet das gesamte neue Modellpaket; er isoliert nicht allein den Effekt einer Gruppentrennung.','',
        '## Vorab festgelegte Entscheidung','', '| Kriterium | Ergebnis |','|---|---|']
    labels={'minimum_complete':'Mindestens 48 vollständige Wolken je neuer Phase','observed_joint_coverage_at_least_95':'Beobachtete gemeinsame Testabdeckung mindestens 95%','all_grouped_shape_screens':'Alle Gruppen- und Blockprüfungen in beiden Armen bestanden','paired_focus_improvement':'Gepaarte Verbesserung der Fokusgruppen im Bootstrap-Intervall'}
    for name,value in s['gates'].items():lines.append(f"| {labels[name]} | {'PASS' if value else 'FAIL'} |")
    lines+=['',f"Fokus-Verzerrungsmaß: gemeinsam {paired['pooled_distortion']:.6f}, gruppiert {paired['grouped_distortion']:.6f}. Differenz gruppiert minus gemeinsam: {paired['difference_grouped_minus_pooled']:.6f}; gepaartes 95%-Bootstrap-Intervall [{paired['paired_percentile_bootstrap_95'][0]:.6f}, {paired['paired_percentile_bootstrap_95'][1]:.6f}]. Kleinere Werte sind besser. Das Maß mittelt |log(E[z²])| der Wurzel- und raumartigen Gruppenmittel über beide Rekonstruktionsarme. Der Bootstrap resampelt ganze Wolken und liefert approximative Pilot-Evidenz.",'',
        '## Gruppen im unabhängigen Test','',
        'Für standardisierte Fehler gilt als vorab festgelegter Prüfbereich: |Mittel z| ≤ 0,5 und Mittel z² in [0,5; 2]. Gruppenmittel und einzelne Paarfehler werden separat geprüft. Alle Aggregate gewichten Wolken gleich.','',
        '| Arm / Gruppe | z² Gruppenmittel: gemeinsam | z² Gruppenmittel: getrennt | z² Paarfehler: getrennt | Halbe Bandbreite: gemeinsam | Halbe Bandbreite: getrennt |','|---|---:|---:|---:|---:|---:|']
    for arm in cfg()['arms']:
        for g in groups:
            p=models['pooled']['arms'][arm];t=models['grouped']['arms'][arm]
            lines.append(f"| {arm} / {g} | {p['blocks'][g]['second_moment']:.4f} | {t['blocks'][g]['second_moment']:.4f} | {t['groups'][g]['point_second_moment']:.4f} | {p['groups'][g]['interval_halfwidth_cloud_medians']['median']:.5f} | {t['groups'][g]['interval_halfwidth_cloud_medians']['median']:.5f} |")
    lines+=['','Bandbreiten sind Mediane der wolkenweisen Mediane in normierten Intervallquadrat-Einheiten q=(−dt²+dx²+dy²)/s². Multiplikation mit s² ergibt die physische Quadrat-Einheit. Diese Größen sind keine symmetrischen Eigenzeitfehler.','',
        '| Modell / Arm | Intervall-RMSE roh | Nach Bias-Zentrierung | Gewählter Bias-Faktor | Kovarianz-Kondition, Maximum |','|---|---:|---:|---:|---:|']
    for which in cfg()['models']:
        for arm in cfg()['arms']:
            a=models[which]['arms'][arm];f=s['development']['models'][which][arm]
            lines.append(f"| {which} / {arm} | {a['raw_rmse']:.6f} | {a['adjusted_rmse']:.6f} | {f['bias_shrinkage']:.2f} | {a['covariance_condition']['max']:.1f} |")
    p=models['pooled']['arms']['original'];g=models['grouped']['arms']['original']
    reductions={name:100*(1-g['groups'][name]['interval_halfwidth_cloud_medians']['median']/p['groups'][name]['interval_halfwidth_cloud_medians']['median']) for name in groups}
    lines+=['',f"Im Originalarm werden die medianen Halbbreiten für Wurzelpaare um {reductions['root']:.1f}% und für kausale Stützpunktpaare um {reductions['support_causal']:.1f}% kleiner. Bei raumartigen Stützpunktpaaren bleiben sie praktisch gleich (Änderung −{reductions['support_spacelike']:.2f}%). Der gemeinsame Vergleich deckt eine zusätzliche Testwolke ab, verletzt aber die vorab festgelegten Formprüfungen. Es wird deshalb keine allgemeine Überlegenheit in der Abdeckungsrate behauptet. Ein Nutzen für eine spätere Geometriekorrektur muss separat geprüft werden."]
    lines+=['','## Abweichungen und Grenzen','']
    failed=[]
    for arm,a in models['grouped']['arms'].items():
        for name,v in a['blocks'].items():
            if not v['passed']:failed.append(f"- {arm}, Block {name}: Mittel z={v['mean_z']:.4f}, Mittel z²={v['second_moment']:.4f}, n={v['n']}.")
        for name,v in a['groups'].items():
            if not v['passed']:failed.append(f"- {arm}, Paargruppe {name}: Mittel z={v.get('point_mean_z')}, Mittel z²={v.get('point_second_moment')}, n={v['n']}.")
    lines+=failed or ['Keine gruppierte Block- oder Paargruppenprüfung verletzt den vorab festgelegten Prüfbereich.']
    misses=[r for r in accepted if r['evaluation']['models']['grouped']['score']>frozen['models']['grouped']['quantile']]
    if misses:
        lines+=['','Nachträgliche Diagnose der verbleibenden Bandverletzungen; keine Änderung von Modell oder Kriterien:','',
            '| Testindex | Seed | Größte Fehlergruppe/-familie | Score / Radius | Außerhalb Entwicklungsbereich |','|---|---:|---|---:|---|']
        for r in misses:
            e=r['evaluation']['models']['grouped'];arm=max(e['arms'],key=lambda a:e['arms'][a]['score']);a=e['arms'][arm]
            family=max(a['family_scores'],key=a['family_scores'].get)
            group=max(a['groups'],key=lambda name:a['groups'][name]['max_abs_z']) if family=='interval' else family
            lines.append(f"| {r['index']} | {r['seed']} | {arm}: {group} | {e['score']/frozen['models']['grouped']['quantile']:.4f} | {r['prediction']['outside_development_range']} |")
    lines+=['',f"{test['outside_development_range']} auswertbare Testwolken liegen außerhalb des Entwicklungsbereichs von Stützpunktzahl oder Designkondition. Untergruppen, alle Familienabdeckungen und gemeinsame gegenüber diagonalen Varianzen sind in `results/summary.json` dokumentiert.",'',
        f"Die marginale Split-Conformal-Untergrenze beträgt {100*frozen['marginal_joint_coverage_bound_per_model']:.3f}% je Modell unter den festgehaltenen Austauschbarkeitsannahmen, gemittelt über Kalibrierungs- und Testziehungen. Sie gilt für neue akzeptierte Wolken und ist keine Zusage für jede einzelne Ordnung, feste Kalibrierungsrealisierung oder beide Modelle zugleich. Ausfälle werden nicht durch Ersatzwolken entfernt.",'',
        '**HOLD_EMBEDDING_COVARIANCE**, **HOLD_PHASE3** und historisches **METADATA_HOLD** bleiben bestehen. Ein bestandener Pilot wäre keine empirische Zertifizierung populationsweiter 95%-Abdeckung. Dieses Experiment aktiviert weder eine Geometriekorrektur noch einen Kalman-Schritt und qualifiziert keine radiale 4D-Geometrie.','',
        '## Reproduktion und öffentliche Reihenfolge','',
        f'- Quell-, Modell- und Seed-Freeze: `{source}`.',f'- Kalibrierungs-Freeze vor Testbeginn: `{calcommit}`.',
        '- `source_freeze.json`: 265 unveränderte Quell- und Eingabedateien.',
        '- `results/calibration` und `results/test`: alle 128 Versuche, Vorhersagesiegel und Ressourcenprotokolle.',
        '- `gg_verify.py`: erneute Entwicklungsanpassung, Quellen/Abstammung, Vorhersagen, aus Seeds regenerierte wahre Stützpunktkoordinaten, Kalibrierung, Auswertung und gepaarter Bootstrap. Die gespeicherte Auswahl/Rekonstruktion wird wiederverwendet.',
        '- `gg_controls.py`: acht geerbte und vierzehn neue analytische Kontrollgruppen einschließlich negativer Kontrollen für falsche Modellfreigaben.','',
        '```sh','OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 python research/lorentz_local_dalembert/geometry_groups/gg_controls.py',
        'OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 python research/lorentz_local_dalembert/geometry_groups/gg_verify.py','```','',
        'Methodische Quelle: [Lei et al., Distribution-Free Predictive Inference for Regression, JASA 2018](https://www.stat.cmu.edu/~ryantibs/papers/conformal.pdf), Abschnitt 2.2. Die Gruppenmodelle und Pilotkriterien sind hier vorab festgelegte Hypothesen.','']
    (HERE/'README.md').write_text('\n'.join(lines))

if __name__=='__main__':main()
