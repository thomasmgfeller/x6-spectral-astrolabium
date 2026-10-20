"""Presentation only; does not change the frozen analysis or gates."""
import json
from pathlib import Path
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

HERE = Path(__file__).resolve().parent


def main():
    s = json.loads((HERE/'summary.json').read_text())
    v = json.loads((HERE/'verification.json').read_text())
    cal = json.loads((HERE/'frozen_calibration.json').read_text())
    executions = [json.loads((HERE/f'test-{i}/execution.json').read_text()) for i in [0,1]]
    names = ['global_original','conditional_original','conditional_projected','conditional_joint','noise_only_negative','prior_only']
    labels = ['Global, Original','Wolkenbedingt, Original','Wolkenbedingt, korrigiert','Gemeinsame Fusion','Nur Rauschen (Negativkontrolle)','Prädiktion allein']
    lines = ['# Eigenzeit: getrennte Rauschkovarianz und Relationskorrektur', '',
        f"**Entscheid: {s['decision']}; HOLD_PHASE3.**", '',
        'Die getrennte Fehlerrechnung und die Relationskorrektur sind implementiert und nachgeprüft. '
        f"Die wolkenbedingte Rauschbehandlung verbessert den Posterior-RMSE in diesem Test um "
        f"{100*(1-s['comparisons']['conditional_vs_global']['rmse_ratio']):.2f}%, verfehlt aber die vorab geforderten 5%. "
        'Das gepaarte Unsicherheitsintervall schließt Gleichstand und Verschlechterung ein. '
        'Die gemeinsame Fusion liefert keinen zusätzlichen Gewinn. Das ist ein überprüfter technischer Fortschritt '
        'bei Fehlertrennung und Relationskonsistenz, keine Filter- oder Geometriequalifikation.', '',
        'Quellcode, Prüfvertrag und Kalibrierung wurden unter '
        '`b5f8abc48fb74f426247ef77b4b265a77e63b72c` öffentlich eingefroren, bevor die 32 neuen Zielwolken erzeugt wurden. '
        'Die bisherigen 64 Wolken aus PR #69 dienen vollständig als Entwicklung/Kalibrierung; deren frühere Testrolle gilt hier nicht mehr.', '',
        f"Kalibrierung: **{cal['complete']}/64** vollständige gemeinsame Fälle. Frischer Test: **{s['complete']}/32**. "
        'Keine Ersatzseeds. Genauigkeit und Überdeckung unten gelten für die gemeinsame vollständige Teilmenge; '
        'die zusätzliche Rückfallkennzahl umfasst alle Wolken und verwendet bei fehlender Messung nur die Prädiktion.', '',
        '## Getrennte Fehlerrechnung', '',
        '`R(C) = G + G/n_cal + N(C)` mit `N(C) = sigma² B(C) B(C)^T`. '
        'Die volle Koeffizientenmatrix enthält den gemeinsamen Rootwert und beide Operatorarme. '
        'Damit werden gemeinsam genutzte Ereignisse nicht als unabhängige Messungen gezählt. '
        '`G` stammt ausschließlich aus rauschfreien Operatorfehlern der Kalibrierwolken; '
        'eine bereits verrauschte Gesamtstreuung wird nicht nochmals addiert.', '',
        '**Grenze:** `N(C)` ist unter dem bekannten IID-Feldrauschmodell exakt. '
        '`G` ist eine empirische Streuung über Wolken, keine bewiesene bedingte Geometriekovarianz jeder einzelnen Wolke. '
        'Rekonstruktions-, Diskretisierungs-, Auswahl- und Feldfehler sind darin gemeinsam enthalten. '
        'Der saubere Feldwert steht nur in dieser Simulation zur Kalibrierung bereit. '
        'Die Kalibrierungsunsicherheit wird durch `G/n_cal` nicht vollständig erfasst.', '',
        '| Originale bedingte Feldrauschvarianz im neuen Test | Minimum | Median | Maximum |',
        '|---|---:|---:|---:|']
    n = s['noise_diagonal_range'][0]
    lines.append(f"| N00(C) | {n['min']:.6f} | {n['median']:.6f} | {n['max']:.6f} |")
    lines += ['', '## Relationsverträglichkeit', '']
    rc = s['relation_counts']
    lines += [f"Vor Korrektur: **{rc['before_failed']}/{s['complete']}** vollständige Testrekonstruktionen mit mindestens einem Fehlpaar; "
              f"{rc['before_missing']} fehlende und {rc['before_extra']} zusätzliche gerichtete Relationen unter {rc['pairs']} geprüften Nichtdiagonalpaaren. "
              f"Nach akzeptierter Korrektur: **{rc['after_failed']}** betroffene Rekonstruktionen.", '',
              'Die Korrektur verändert rekonstruierte Koordinaten unter expliziten Kegel-/Trennbedingungen. '
              'Die beobachteten Relationslabels bleiben erhalten. Anschließend werden die Momentgewichte neu gelöst und geprüft. '
              'Eine exakte Relationserhaltung ist hier eine Konstruktionsbedingung; sie beweist keine richtigen Abstände oder Krümmung. '
              'Die Aussage betrifft Root und ausgewählte Stützen, nicht sämtliche Wolkenpunkte oder Landmarken.', '',
              f"Rauschfreier Operator-RMSE vor/nach Korrektur: **{s['clean_rmse'][0]:.6f} / {s['clean_rmse'][1]:.6f}** "
              f"(Quotient {s['clean_rmse'][1]/s['clean_rmse'][0]:.6f}; vorab erlaubt höchstens 1,05).", '',
              '## Eingefrorener Filtervergleich', '',
              'Skalare Operatorantwort im bekannten flachen 2+1-Modell, Testfeld '
              '`exp(t/2) cos(x/2) cos(y/2)` mit Operatorwert −0,75. '
              'Synthetische unabhängige Prädiktion mit Standardabweichung 0,5. '
              'Es wird noch kein räumlicher Einbettungszustand durch den Kalman-Filter geschätzt.', '',
              '| Verfahren | Posterior-RMSE | Nominelle 95%-Überdeckung | Exaktes 95%-Intervall der Überdeckungsquote | RMSE mit Prädiktionsrückfall |',
              '|---|---:|---:|---:|---:|']
    for name, label in zip(names, labels):
        a = s['arms'][name]
        lo,hi = a['coverage_exact_95']
        fallback = f"{a['all_clouds_with_prior_fallback_rmse']:.6f}" if 'all_clouds_with_prior_fallback_rmse' in a else '—'
        lines.append(f"| {label} | {a['rmse']:.6f} | {a['coverage_hits']}/{a['n']} | {100*lo:.1f}–{100*hi:.1f}% | {fallback} |")
    lines += ['', '| Gepaarter Vergleich | RMSE-Quotient | Bootstrap-95% |','|---|---:|---:|']
    for key, comp in s['comparisons'].items():
        lo,hi = comp['paired_bootstrap_95']
        lines.append(f"| {key} | {comp['rmse_ratio']:.6f} | {lo:.6f}–{hi:.6f} |")
    lines += ['', 'Die Bootstrapintervalle konditionieren auf die Kalibrierung. '
              'Nominelle Gaussian-Intervalle und die kleine Testzahl liefern keine Überdeckungsgarantie. '
              'Die rauschabhängigen Strata in `summary.json` zeigen zusätzlich, ob rauschfreie Fehler mit der Wolkenqualität variieren.', '',
              '| Vorab festgelegtes Kriterium | Ergebnis |', '|---|---|']
    for key, val in s['gates'].items():
        lines.append(f"| {key} | {'PASS' if val else 'FAIL'} |")
    lines += ['', '## Nachprüfung und Reproduktion', '',
        f"**{v['status']}**: {v['clouds']} Koordinatenhashes, {v['independently_counted_intervals']} unabhängig über Koordinaten gezählte Intervalle, "
        f"{v['qp_certificates']} QP-Zertifikate, sämtliche Feld-/Rauschantworten und die eingefrorene Auswertung. "
        'Die Relationsprojektion wird erneut gerechnet. Die vollständige teure Rahmensuche ist nicht Teil dieses Replay. '
        'Fünf Testgruppen decken Fehlrelationen, ungültige Ordnungen, Jacobian/Transport, gemeinsames Rootrauschen und exakte Kovarianzzerlegung ab.', '',
        '| Testshard | Wolken | Laufzeit (s) | Peak-RSS (MiB) | Status |', '|---|---:|---:|---:|---|']
    for e in executions:
        lines.append(f"| {e['shard']} | {len(e['records'])} | {e['seconds']:.1f} | {e['peak_mib']:.1f} | {e['status']} |")
    lines += ['', 'Vom Repository-Root (Python 3.12, NumPy 2.3.5, SciPy 1.17.0):', '', '```sh',
        'python -m zipfile -e research/lorentz_local_dalembert/conditional_geometry/test_clouds.zip research/lorentz_local_dalembert/conditional_geometry',
        'OPENBLAS_NUM_THREADS=1 python -B research/lorentz_local_dalembert/conditional_geometry/test_controls.py',
        'OPENBLAS_NUM_THREADS=1 python -B research/lorentz_local_dalembert/conditional_geometry/verify.py', '```', '',
        'Für eine vollständige Neuberechnung einen separaten Checkout des öffentlichen Freeze verwenden '
        'und dort `cg_run.py --shard 0` sowie `cg_run.py --shard 1` ausführen, danach `cg_analyze.py`. '
        'Bestehende Testordner werden nicht überschrieben. Rohdaten und Ausführungsprotokolle liegen in `test_clouds.zip` '
        'mit `test_manifest.json`; alle Entwicklungsergebnisse in `development_records.zip`.', '',
        '## Weiterhin offen', '',
        '- Bedingte Geometriefehler und Bias als Funktion beobachtbarer Wolkenmerkmale; bisher nur globale empirische Kalibrierung.',
        '- Andere Felder, Dichten und Modellabweichungen auf neuen unabhängigen Daten.',
        '- Vollständige Einbettungskovarianz und sequenzieller Filter einschließlich gemeinsamer Vergangenheit.',
        '- Unsichere oder unvollständige beobachtete Relationslabels. Die derzeitige Projektion verlangt eine vollständige exakte Ordnung.',
        '- Vergangenheitsbasierte Konstruktion oder deklarierte Verzögerung: die heutigen Stützen verwenden Zukunftsdaten.', '',
        'Keine Online-, Krümmungs- oder Gerätefreigabe. Keine externe Replikation oder Neuheitsbehauptung. '
        'Die konvexe Kegelformulierung verwendet Standardmethoden: '
        '[Lobo et al. (1998)](https://stanford.edu/~boyd/papers/socp.html).', '',
        '![Getrennte Kovarianz und Relationsprüfung](results.png)', '']
    (HERE/'RESULTS.md').write_text('\n'.join(lines))
    plt.rcParams.update({'font.size':10,'axes.spines.top':False,'axes.spines.right':False})
    fig, ax = plt.subplots(1,3,figsize=(14,4.5),layout='constrained')
    colors = ['#8c9aa8','#007f8b','#dc7934','#334ac0']
    short = ['Global','Wolken-\nbedingt','Korrigiert','Fusion']
    values = [s['arms'][n]['rmse'] for n in names[:4]]
    ax[0].bar(short,values,color=colors)
    ax[0].set(ylabel='Posterior-RMSE',title=f"Frischer Test: {s['complete']}/32 Fälle")
    for i,val in enumerate(values):ax[0].text(i,val,f'{val:.3f}',ha='center',va='bottom')
    nn = [r['arms']['conditional_original']['noise_contribution'] for r in s['records']]
    order = np.argsort(nn)
    ax[1].plot(np.array(nn)[order],'.-',color=colors[1],label='Bedingtes Feldrauschen N(C)')
    ax[1].axhline(cal['geometry_covariance'][0][0],color=colors[2],label='Empirisches G (global)')
    ax[1].set(yscale='log',xlabel='Testwolken, nach N(C) sortiert',ylabel='Varianz',title='Getrennte Fehlerbeiträge')
    ax[1].legend(fontsize=8)
    ax[2].bar(['Vorher','Nachher'],[rc['before_failed'],rc['after_failed']],color=[colors[0],colors[1]])
    ax[2].set(ylabel='Wolken mit Fehlrelationen',title='Akzeptierte Rekonstruktionen',ylim=(0,max(1,s['complete'])))
    for i,val in enumerate([rc['before_failed'],rc['after_failed']]):ax[2].text(i,val+.4,str(val),ha='center')
    fig.suptitle(s['decision']+' · Offline-Pilot · HOLD_PHASE3',fontweight='bold')
    fig.savefig(HERE/'results.png',dpi=160)
    plt.close(fig)


if __name__ == '__main__':
    main()
