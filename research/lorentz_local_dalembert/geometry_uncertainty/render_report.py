"""SPDX-License-Identifier: Apache-2.0
Presentation only; does not alter the frozen analysis or decisions.
"""
import json
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from gu_common import HERE,load_phase

def main():
    s=json.loads((HERE/'results/summary.json').read_text());q=s['calibration_rule']['quantile']
    cal=s['phases']['calibration'];test=s['phases']['test'];a=test['arms']['original'];p=test['arms']['projected']
    source=json.loads((HERE/'source_freeze.json').read_text())['commit']
    executions,rows=load_phase('test');calcommit=executions[0]['execution_commit']
    fig,axes=plt.subplots(1,2,figsize=(12.5,5.1),layout='constrained')
    colors=['#42718e','#b55b42']
    for phase,color in zip(['calibration','test'],colors):
        _,records=load_phase(phase)
        values=sorted(r['evaluation']['score'] for r in records if r['evaluation']['status']=='COMPLETE')
        axes[0].plot(range(1,len(values)+1),values,'o-',ms=4,lw=1.2,color=color,label=f'{phase}: n={len(values)}')
    axes[0].axhline(q,color='#222222',ls='--',label=f'Frozen radius {q:.3f}')
    axes[0].set(xlabel='Accepted clouds, sorted within phase',ylabel='Joint standardized geometry error',title='Fresh-cloud joint coverage')
    axes[0].legend(fontsize=9);axes[0].grid(alpha=.18)
    names=list(a['standardized_blocks']);idx=np.arange(len(names))
    axes[1].axhspan(.5,2,color='#d5e4d3',alpha=.65,label='Prespecified screening range')
    axes[1].axhline(1,color='#505050',ls='--',lw=1)
    for k,(arm,color) in enumerate(zip(['original','projected'],colors)):
        vals=[test['arms'][arm]['standardized_blocks'][n].get('second_moment',np.nan) for n in names]
        axes[1].plot(idx+(k-.5)*.10,vals,'o',ms=7,color=color,label=arm)
    axes[1].set(xticks=idx,xticklabels=names,ylabel='Mean squared standardized block error',title='Uninflated covariance: separate screen')
    axes[1].tick_params(axis='x',rotation=35);axes[1].legend(fontsize=8);axes[1].grid(axis='y',alpha=.18)
    cov=test['simultaneous']
    fig.suptitle(f"Invariant geometry calibration · 2+1 dimensions · joint test coverage {cov['covered']}/{cov['n']}",fontsize=14)
    fig.savefig(HERE/'results/geometry_uncertainty.png',dpi=170);plt.close(fig)
    cp=cov['clopper_pearson_95'];f=s['calibration_rule'];model=s['development']
    lines=[
        '# Unsicherheit der Geometrie: Kalibrierung an neuen Wolken',
        '',
        f"**Prüfung abgeschlossen; Arbeitskovarianz nicht freigegeben.** Der technische Status **{s['decision']}** bezeichnet den Abschluss der vorab festgelegten Kalibrierung, keinen bestandenen Modelltest. Untersucht werden gemeinsame Vorhersagebänder für Lorentz-invariante Geometriegrößen im bestehenden **flachen 2+1-Modell bei rho=32768**.",
        '',
        f"Im unabhängigen Test liegen **{cov['covered']} von {cov['n']}** auswertbaren Wolken vollständig innerhalb der Bänder: gleichzeitig für beide Rekonstruktionen, alle Paarintervalle, alle Wurzel-Gram-Einträge und alle nichtleeren Gruppenmittel. Die beobachtete Rate beträgt {100*cov['rate']:.2f}%; ihr exaktes 95%-Binomialintervall ist [{100*cp[0]:.2f}%, {100*cp[1]:.2f}%]. Diese kleine Stichprobe zertifiziert keine populationsweite 95%-Deckung empirisch.",
        '',
        f"Das unskalierte Kovarianzmodell erhält für Original und Projektion jeweils **{a['covariance_screen']}** beziehungsweise **{p['covariance_screen']}**. Die Bandkalibrierung und diese Modellprüfung sind getrennte Ergebnisse. Eine konditionale Kovarianz der eingebetteten Koordinaten ist damit weiterhin nicht validiert.",
        '',
        '![Geometry uncertainty calibration](results/geometry_uncertainty.png)',
        '',
        '## Drei ausgeführte Schritte',
        '',
        '1. **Geometrische Fehler direkt modelliert.** Für alle Paare wird das vorzeichenbehaftete Intervallquadrat q = (−Δt² + Δx² + Δy²)/s² untersucht. Die systematische Verzerrung wird separat geschätzt; positive Varianzanteile modellieren unabhängige Fehler, gemeinsame Endpunkte und gemeinsame Wolkenfehler. Die letzten beiden bilden Abhängigkeiten ab, identifizieren aber keine einzelnen Landmarkenstörungen.',
        f"2. **Unsicherheitsradius unabhängig kalibriert.** {model['development_complete']} frühere vollständige Wolken dienen ausschließlich zur Modellentwicklung. Von {cal['attempts']} neuen Kalibrierungsversuchen sind {cal['complete']} auswertbar. Der gemeinsame Radius q*={q:.6f} ist Rang {f['rank']} von {f['complete']} und wurde vor dem Test öffentlich fixiert.",
        f"3. **Auf neuen Wolken geprüft.** {test['attempts']} weitere Versuche ergeben {test['complete']} auswertbare Wolken und {test['abstentions']} dokumentierte Abstentionen. Alle Versuche bleiben erhalten; es gibt keine Ersatzwolken oder Anpassung an Testresultate.",
        '',
        '## Unabhängiger Test',
        '',
        '| Größe | Original | Relationsprojektion |',
        '|---|---:|---:|',
        f"| RMSE der normierten Intervallquadrate, roh | {a['raw_rmse']:.6f} | {p['raw_rmse']:.6f} |",
        f"| RMSE nach Bias-Zentrierung | {a['bias_adjusted_rmse']:.6f} | {p['bias_adjusted_rmse']:.6f} |",
        f"| Mittlerer Fehler, roh | {a['raw_cloud_balanced_mean']:.6f} | {p['raw_cloud_balanced_mean']:.6f} |",
        f"| Mittlerer Fehler nach Zentrierung | {a['adjusted_cloud_balanced_mean']:.6f} | {p['adjusted_cloud_balanced_mean']:.6f} |",
        f"| Mediane Intervall-Halbbreite, normiert | {a['interval_halfwidth_cloud_medians']['median']:.6f} | {p['interval_halfwidth_cloud_medians']['median']:.6f} |",
        f"| Mediane Intervall-Halbbreite, physische Quadrat-Einheit | {a['interval_halfwidth_physical_cloud_medians']['median']:.8f} | {p['interval_halfwidth_physical_cloud_medians']['median']:.8f} |",
        f"| Mediane Gram-Halbbreite, normiert | {a['gram_halfwidth_cloud_medians']['median']:.6f} | {p['gram_halfwidth_cloud_medians']['median']:.6f} |",
        f"| Punktweises standardisiertes zweites Moment, wolkengewichtet | {a['pointwise_second_moment']:.4f} | {p['pointwise_second_moment']:.4f} |",
        f"| Größte Kovarianz-Konditionszahl | {a['covariance_condition']['max']:.1f} | {p['covariance_condition']['max']:.1f} |",
        '',
        'Alle Fehleraggregate gewichten Wolken gleich. Halbbreiten sind Mediane der wolkenweisen Mediane. Ein Intervallquadrat ist keine Eigenzeit; nahe dem Lichtkegel darf daraus keine symmetrische Eigenzeit-Fehlerangabe abgelesen werden.',
        '',
        '**Das 95%-Ziel ist empirisch nicht bestätigt.** Das breite Binomialintervall enthält 95%; die kleine Testserie widerlegt daher auch keine solche populationsweite Rate. Alle drei Bandverletzungen betreffen die Paarintervalle (Testindizes 15, 23, 25); Gram-Einträge und Gruppenmittel liegen in sämtlichen 29 Testwolken innerhalb ihrer Bänder. Die Bias-Zentrierung erhöht den Original-RMSE von 0,15028 auf 0,15282 und wird nicht als Geometriekorrektur übernommen.',
        '',
        'Nachträgliche Eingrenzung ohne Modelländerung: Die größte Verletzung jeder dieser drei Wolken liegt jeweils bei einem raumartigen Paar zwischen zwei Stützpunkten. Die standardisierten Beträge sind 5,519, 5,657 und 6,963. Diese Beobachtung bestimmt eine mögliche nächste Hypothese, keinen nachträglich bestandenen Test.',
        '',
        '## Abhängigkeiten und Modellprüfung',
        '',
        'Die Arbeitskovarianz lautet K = D [v_ind I + v_endpoint A Aᵀ + v_cloud 11ᵀ] D, mit D_aa=√(1+q_hat,a²) und zwei Einträgen 1/√2 pro Zeile der Endpunkt-Inzidenzmatrix A. Die Gram-Unsicherheit wird mit allen Kreuztermen linear fortgepflanzt. Gemeinsame Abdeckung wird auf Wolkenebene kalibriert; Paare werden nicht als unabhängige Stichproben gezählt.',
        '',
        '| Varianzkomponente, Entwicklung | Original | Relationsprojektion |',
        '|---|---:|---:|'
    ]
    for i,name in enumerate(['Unabhängig','Gemeinsamer Endpunkt','Gemeinsame Wolke']):
        lines.append(f"| {name} | {model['arms']['original']['variance_components'][i]:.8f} | {model['arms']['projected']['variance_components'][i]:.8f} |")
    lines += ['', '| Gruppe, Original | Wolken | Mittel z | Mittel z² | Varianz K / diagonale Näherung, Median |', '|---|---:|---:|---:|---:|']
    for name,b in a['standardized_blocks'].items():
        if b['n']:lines.append(f"| {name} | {b['n']} | {b['mean_z']:.4f} | {b['second_moment']:.4f} | {b['shared_to_diagonal_variance_ratio']['median']:.2f} |")
    lines += ['', 'Vorab festgelegte Modellprüfung: |Mittel z| ≤ 0,5 und Mittel z² in [0,5; 2], zusätzlich das punktweise zweite Moment in [0,5; 2]. Das ist ein beschreibender Mindesttest, kein statistischer Nachweis einer konditionalen Kovarianz. Alle Gruppen beider Arme stehen in `results/summary.json`.',
        '', '## Reichweite und Grenzen', '',
        f"Der Split-Conformal-Satz ergibt unter den festgehaltenen Austauschbarkeitsannahmen mindestens {100*f['marginal_joint_coverage_bound']:.3f}% marginale gemeinsame Abdeckung für eine neue akzeptierte Wolke, gemittelt über Kalibrierungs- und Testziehungen. Er behauptet keine Abdeckung für jede einzelne beobachtete Ordnung oder jedes Teilgebiet. Die ausgeschlossenen historischen Seeds und alle neuen Seeds stehen im Protokollarchiv.",
        '', f"{test['outside_development_range']} Testwolken liegen außerhalb des Entwicklungsbereichs von Stützpunktzahl oder Designkondition. Die vorab festgelegten Untergruppen werden nachfolgend deskriptiv ausgewiesen.",
        '', '| Untergruppe | Vollständig gedeckt / auswertbar |', '|---|---:|']
    for feature,levels in test['strata'].items():
        for level,v in levels.items():lines.append(f"| {feature}: {level} | {v['covered']}/{v['n']} |")
    lines += ['', '**HOLD_EMBEDDING_COVARIANCE**, **HOLD_PHASE3** und historisches **METADATA_HOLD** bleiben bestehen. Die zentrierten Intervallwerte müssen keine realisierbare Einbettung bilden. Dieses Ergebnis aktiviert weder eine anisotrope Geometriekorrektur noch einen Kalman-Schritt und qualifiziert nicht die radiale 4D-Geometrie.',
        '', '## Nächster gezielter Versuch', '',
        'Die Form gemeinsamer Fehler benötigt eine bessere Prüfung: Wurzelabstände, Abstände zwischen Stützpunkten und die Randbereiche der Fehlerverteilung sind getrennt zu modellieren. Das Wurzel-Gruppenmittel hat ein standardisiertes zweites Moment von 0,418 statt des Zielwerts nahe 1; zugleich treten drei große Paarfehler auf. Eine bloße gemeinsame Vergrößerung aller Varianzen behebt diese unterschiedliche Skalierung nicht. Ein Nachfolgemodell muss auf Entwicklungsdaten festgelegt und wiederum an vollständig neuen Kalibrierungs- und Testwolken geprüft werden. Die hier veröffentlichten Grenzwerte bleiben unverändert.',
        '', '## Reproduktion und öffentliche Reihenfolge', '',
        f'- Quell-/Modell-/Seed-Freeze vor neuen Wolken: `{source}`.',
        f'- Kalibrierungs-Freeze vor Testwolken: `{calcommit}`.',
        '- Unveränderte Quell-Pins: `source_freeze.json`; vollständige Versuche und Ressourcenprotokolle: `results/calibration` und `results/test`.',
        '- `gu_verify.py` prüft Commit-Abstammung, eingefrorene Quellen, das Entwicklungsmodell, alle neuen Datensätze, aus Seeds neu erzeugte wahre Stützpunktkoordinaten, Kalibrierung und Auswertung. Die gespeicherte Auswahl/Rekonstruktion wird dabei wiederverwendet.',
        '- `gu_controls.py` prüft acht Gruppen analytischer Kontrollfälle einschließlich Lorentz-Invarianz, Gram-Kreuztermen und einer falschen diagonalen Kovarianznäherung.',
        '', '```sh', 'OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 python research/lorentz_local_dalembert/geometry_uncertainty/gu_controls.py',
        'OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 python research/lorentz_local_dalembert/geometry_uncertainty/gu_verify.py', '```',
        '', 'Methodische Quelle: [Lei et al., Distribution-Free Predictive Inference for Regression, JASA 2018](https://www.stat.cmu.edu/~ryantibs/papers/conformal.pdf), Abschnitt 2.2. Das konkrete Geometriemodell und die Gruppenprüfung sind hier festgelegte Arbeitsmodelle.', '']
    (HERE/'README.md').write_text('\n'.join(lines))

if __name__=='__main__':main()
