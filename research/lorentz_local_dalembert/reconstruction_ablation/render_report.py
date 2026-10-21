"""SPDX-License-Identifier: Apache-2.0
Presentation of frozen results; no statistical decisions are made here.
"""
import json
from pathlib import Path
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

HERE=Path(__file__).resolve().parent


def main():
    s=json.loads((HERE/'results/summary.json').read_text())
    execution=json.loads((HERE/'results/execution.json').read_text())
    p=s['phases']['test'];a=p['arms'];q=p['primary']['original']
    freeze=json.loads((HERE/'source_freeze.json').read_text())['commit']
    names={'original':'Original','projected':'Relationsprojektion','oracle':'Wahre Geometrie (Oracle)',
           'metadata':'Metadaten','projected_metadata':'Projektion + Metadaten'}
    plt.rcParams.update({'font.family':'DejaVu Sans','font.size':11})
    fig,ax=plt.subplots(figsize=(9,5),layout='constrained')
    for phase,color,offset,label in [('calibration','#4477aa',-.1,'Bisherige Kalibrierwolken (n=30)'),
                                     ('test','#aa3377',.1,'Bisherige Testwolken (n=28)')]:
        rows=[s['phases'][phase]['arms'][k] for k in ['original','projected','oracle']]
        y=np.array([r['rmse'] for r in rows]);lo,hi=np.array([r['paired_cloud_bootstrap_rmse_95'] for r in rows]).T
        ax.errorbar(np.arange(3)+offset,y,yerr=np.vstack((y-lo,hi-y)),fmt='o',color=color,capsize=5,markersize=7,label=label)
        if phase=='test':
            for i,v in enumerate(y):ax.annotate(f'{v:.4f}',(i+offset,v),xytext=(10,0),textcoords='offset points',color=color,va='center')
    ax.set_yscale('log');ax.set_ylim(.015,6);ax.set_xlim(-.35,2.45)
    ax.set_xticks(range(3),['Rekonstruierte\nGeometrie','Nach Relations-\nprojektion','Wahre Geometrie\n(nur Referenz)'])
    ax.set_ylabel('Rauschfreier RMSE · logarithmische Skala')
    ax.set_title('Gleiche Stützpunkte, gleiche Felder, gleiche Gewichtspolitik',pad=14)
    ax.legend(loc='upper right',fontsize=9)
    ax.grid(axis='y',which='both',alpha=.16);ax.spines[['top','right']].set_visible(False)
    fig.suptitle('Rekonstruktion und Diskretisierungsrest getrennt',fontsize=15)
    fig.savefig(HERE/'results/reconstruction_vs_discretization.png',dpi=170);plt.close(fig)
    lines=['# Rekonstruktionsfehler und Diskretisierungsrest','',
        '**DECOMPOSITION_VERIFIED — retrospektive Diagnose, keine Produktionsfreigabe.**','',
        f"Auf den 28 bisher vollständigen Testwolken sinkt der rauschfreie RMSE bei unverändertem Support und gleicher Gewichtspolitik von **{a['original']['rmse']:.6f} auf {a['oracle']['rmse']:.6f}**, wenn ausschließlich die rekonstruierte durch die wahre Simulationsgeometrie ersetzt wird. "
        'Das weist in diesem Versuch auf die Rekonstruktion als Hauptengpass hin. '
        'Die analytische Taylor-Zerlegung lokalisiert den größten Fehlerbeitrag in der Antwort auf den linearen Feldanteil.','',
        '64 veröffentlichte Datensätze wurden behalten: 30 vollständige Kalibrierwolken, 28 vollständige Testwolken und sechs bereits bekannte Supportausfälle. '
        'Alle 58 verfügbaren Supports besitzen einen zertifizierten Oracle. Es gab keine neuen Wolken, Ersatzfälle, Supportsuche oder Feldanpassung. '
        'Die Bezeichnungen Kalibrierung/Test stammen aus dem vorigen Versuch; beide Gruppen werden hier retrospektiv verwendet.','',
        '## Vergleich auf denselben Punktwolken','',
        '| Geometrie | RMSE: bisheriger Testteil | Deskriptives 95%-Bootstrapintervall | RMSE: bisheriger Kalibrierteil |',
        '|---|---:|---:|---:|']
    for name in ['original','projected','oracle']:
        r=a[name];lo,hi=r['paired_cloud_bootstrap_rmse_95']
        lines.append(f"| {names[name]} | {r['rmse']:.6f} | {lo:.6f}–{hi:.6f} | {s['phases']['calibration']['arms'][name]['rmse']:.6f} |")
    lo,hi=q['paired_cloud_bootstrap_95']
    lines+=['',f"Oracle/Original-RMSE = **{q['oracle_to_actual_rmse_ratio']:.6f}**, gepaartes Bootstrapintervall {lo:.6f}–{hi:.6f}. "
        'Resampling erfolgte mit ganzen Wolken; vier Felder zählen nicht als vier unabhängige Wolken. '
        'Diese Intervalle sind deskriptiv, nicht simultan und keine neue unabhängige Bestätigung.','',
        '![Gepaarter Vergleich rekonstruierter und wahrer Geometrie](results/reconstruction_vs_discretization.png)','',
        'Fehlerbalken zeigen die deskriptiven Bootstrapintervalle. Die y-Achse ist logarithmisch.','',
        '## Exakte Fehlerbilanz des Originaloperators','',
        '`e = d + r`, wobei d der Fehler mit wahrer Geometrie und r die Antwortänderung durch die Rekonstruktion ist. '
        'Damit gilt `MSE(e) = E[d²] + E[r²] + 2 E[d r]`.','',
        '| Beitrag | Mittlerer quadratischer Fehlerterm, bisheriger Testteil |',
        '|---|---:|',
        f"| Diskretisierungsrest bei wahrer Geometrie, E[d²] | {q['squared_terms']['discretization']:.9f} |",
        f"| Rekonstruktionsunterschied, E[r²] | {q['squared_terms']['reconstruction']:.9f} |",
        f"| Vorzeichenbehaftete Wechselwirkung, 2 E[d r] | {q['signed_cross_terms']['discretization x reconstruction']:+.9f} |",
        f"| Summe = bisheriger rauschfreier MSE | **{q['direct_mse']:.9f}** |",'',
        'Der Wechselwirkungsterm wird ausdrücklich mitgeführt. Eine allgemeine Aufteilung in zwei unabhängige positive Prozentanteile ist nicht zulässig. '
        'Der Diskretisierungsrest ist bedingt auf diesen Support, diese Felder und diese Dichte; er ist weder ein universelles Fehlerminimum noch ein Konvergenzbeweis.','',
        'Die bisherige Trennung vom Messrauschen bleibt konsistent: Zum rauschfreien MSE '
        f"{q['direct_mse']:.9f} kommt beim Original unter dem alten IID-Modell die Messvarianz {a['original']['mean_hypothetical_iid_variance']:.9f}. "
        'Wiederholtes Messen reduziert nur diesen zusätzlichen Rauschterm.','',
        '## Wo der Rekonstruktionsfehler auftritt','',
        'Für jede Sinus-/Kosinuswelle wird der Feldkontrast exakt in linearen Tayloranteil, quadratischen Anteil und vollständigen Rest zerlegt. '
        'Die folgende Tabelle zeigt Quadrate einzelner Beiträge; ihre Summe allein ist wegen der Kreuzterme noch nicht der Gesamtfehler.','',
        '| Beitrag zum Feldfehler | Original: mittleres Quadrat | Oracle: mittleres Quadrat |',
        '|---|---:|---:|']
    for key,label in [('linear','Linearer Anteil'),('quadratic','Quadratischer Anteil minus Sollwert'),('higher_order','Vollständiger höherer Rest')]:
        lines.append(f"| {label} | {p['taylor']['original']['squared_terms'][key]:.9g} | {p['taylor']['oracle']['squared_terms'][key]:.9g} |")
    cross=p['taylor']['original']['signed_cross_terms']
    lines+=['',f"Beim Original summieren sich die drei Taylor-Kreuzterme zu {sum(cross.values()):+.9f}. "
        'Die vollständige Bilanz stimmt mit dem direkt gemessenen rauschfreien Fehler überein.','',
        'Die Momentbedingungen werden in den rekonstruierten Koordinaten erfüllt, aber dadurch noch nicht in den wahren physischen Koordinaten. '
        f"Der größte lineare physische Momentfehler beträgt im Testteil {p['max_physical_linear_moment_error']['original']:.6g} beim Original und "
        f"{p['max_physical_linear_moment_error']['oracle']:.3g} beim Oracle. "
        'Das ist der konkrete nächste Diagnosepunkt: Warum bewahrt die intrinsische Rekonstruktion die physische Auslöschung linearer Felder nicht ausreichend? '
        'Dieser Versuch lokalisiert den Fehler; er entscheidet noch nicht zwischen Ursachen wie Skala, Rahmenrekonstruktion oder Landmarkenabhängigkeit.','',
        '## Metadatenzusatz und Rauschkosten','',
        'Metadatenänderungen werden als eigener Term c erfasst: `e_meta = d + r_basis + c`. '
        'Die sechs quadratischen und gekreuzten Beiträge stehen vollständig in [summary.json](results/summary.json). '
        'Eine Metadatenänderung wird dadurch nicht als reine Geometrieänderung bezeichnet.','',
        '| Variante | Rauschfreier RMSE | Hypothetische IID-Messvarianz bei σ=0,001 |',
        '|---|---:|---:|']
    for name in ['original','metadata','projected','projected_metadata','oracle']:
        lines.append(f"| {names[name]} | {a[name]['rmse']:.6f} | {a[name]['mean_hypothetical_iid_variance']:.6f} |")
    lines+=['','Die Oracle-Messvarianz ist im Testteil höher als beim Original. Die geringe rauschfreie Abweichung ist daher keine pauschale Aussage über optimale Rauschrobustheit. '
        'Diese Varianzen sind analytische Folgen des früher deklarierten Rauschmodells; es wurden hier keine neuen Rauschmessungen erzeugt.','',
        '## Reproduzierbarkeit und Grenzen','',
        f"Auswertungsfreeze vor Oracle-Berechnung: `{freeze}`. "
        f"177 Quell-/Eingabedateien fixiert; 64 Datensätze numerisch wiederholt; sieben analytische Kontrollgruppen bestanden. "
        f"Auswertung: {execution['seconds']:.3f} s, maximal {execution['peak_mib']:.2f} MiB (Budget 120 s / 512 MiB). "
        'Die ursprünglichen Rohdaten und wissenschaftlichen Entscheidungen bleiben unverändert.','',
        '- [Vertrag](contract.json) und [mathematische Definitionen](PROTOCOL.md)',
        '- [Vollständige Auswertung](results/summary.json), [Einzelresultate](results/records.json.gz), [Replay](results/verification.json)',
        '- Oracle-Gewichte: vorhandenes QP plus unabhängiger SVD-Weg; Polynome, Lorentz-/Skaleninvarianz, kontrollierte Verzerrung, Kreuzterme und Rangfehler geprüft.','',
        '```sh',
        'OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 python -B research/lorentz_local_dalembert/reconstruction_ablation/ra_controls.py',
        'OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 python -B research/lorentz_local_dalembert/reconstruction_ablation/ra_verify.py',
        '```','',
        '**HOLD_PHASE3, HOLD_EMBEDDING_COVARIANCE und METADATA_HOLD bleiben bestehen.** '
        'Wahre Simulatorgeometrie ist ausschließlich eine diagnostische Referenz. Keine nutzbare Geometriekorrektur, keine Einbettungskovarianz, '
        'keine 4D-/Krümmungs-/Gerätefreigabe und keine asymptotische Genauigkeitsgarantie.','']
    (HERE/'README.md').write_text('\n'.join(lines))


if __name__=='__main__':main()
