"""SPDX-License-Identifier: Apache-2.0
Presentation only: render the frozen analyzer's outputs without changing gates.
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
    cal=json.loads((HERE/'frozen_calibration.json').read_text())
    checks=json.loads((HERE/'results/noise_checks.json').read_text())
    nd=sum(t['degenerate'] for r in checks for t in r['tests'])
    ns=2*(s['noise_checks']['tested_directions']-nd)
    source=json.loads((HERE/'source_freeze.json').read_text())['commit']
    freeze=json.loads((HERE/'calibration_freeze.json').read_text())['commit']
    labels=['Original','Metadaten','Projektion','Projektion +\nMetadaten']
    comp=s['components'];x=np.arange(4)
    plt.rcParams.update({'font.family':'DejaVu Sans','font.size':10})
    fig,axs=plt.subplots(1,2,figsize=(12,4.8),layout='constrained')
    base=np.zeros(4)
    for key,label,color in [('bias_squared','Mittlere Abweichung²','#8c4b4b'),
                            ('geometry_spread','Geometrie-/Modellstreuung','#4477aa'),
                            ('measurement_variance','Messrauschen (eine Messung)','#ddaa33')]:
        values=np.array([v[key] for v in comp])
        axs[0].bar(x,values,bottom=base,label=label,color=color,width=.65)
        base+=values
    axs[0].set_xticks(x,labels);axs[0].set_ylabel('Mittlerer quadratischer Operatorfehler')
    axs[0].set_title('Getrennte Fehlerbeiträge')
    axs[0].legend(fontsize=8,loc='upper left')
    axs[0].set_ylim(0,float(np.max(base))*1.35)
    colors=['#333333','#aa3377','#228833','#4477aa']
    r=np.geomspace(1,512,100)
    for v,label,color in zip(comp,labels,colors):
        g=v['bias_squared']+v['geometry_spread']
        axs[1].plot(r,np.sqrt(g+v['measurement_variance']/r),label=label.replace('\n',' '),color=color)
        axs[1].axhline(np.sqrt(g),color=color,linestyle=':',alpha=.6)
    axs[1].set_xscale('log');axs[1].set_xticks([1,16,512],['1','16','512'])
    axs[1].set_xlabel('Unabhängige Messungen derselben Geometrie')
    axs[1].set_ylabel('Erwarteter RMSE');axs[1].set_title('Mittelung erreicht eine Fehlergrenze')
    axs[1].legend(fontsize=8)
    for ax in axs:
        ax.spines[['top','right']].set_visible(False);ax.grid(axis='y',alpha=.18);ax.set_axisbelow(True)
    fig.suptitle(f"Synthetischer 2+1-Pilot · {s['complete']} vollständige Testwolken · vier feste Prüffelder",fontsize=13)
    fig.savefig(HERE/'results/error_components.png',dpi=170)
    plt.close(fig)
    lines=['# Geometriefehler und Messunsicherheit getrennt kalibriert','',
        f"**{s['decision']} — HOLD_PHASE3 und HOLD_EMBEDDING_COVARIANCE bleiben bestehen.**",'',
        f"32 neue Kalibrierwolken, davon {s['calibration_complete']} vollständig; 32 neue Testwolken, davon {s['complete']} vollständig. "
        'Vier feste neue Sinus-/Kosinusfelder und 512 synthetische Rauschwiederholungen je Feld und vollständiger Wolke. '
        'Eine zusätzliche verrauschte Messung pro Feld wurde für die Intervallprüfung zurückgehalten. '
        'Das bekannte Eingangsrauschen ist IID Gauß mit σ=0,001, einschließlich des gemeinsamen Rootwerts.','',
        '## Getrennte Beiträge','',
        'Alle Zahlen sind über die vier festen Felder und vollständigen Testwolken gemittelt. '
        'Der rauschfreie Operatorfehler enthält Rekonstruktion, Diskretisierung und Auswahl. '
        'Er ist keine isolierte Koordinatenkovarianz. Die geometrischen Abstands- und Relationsfehler stehen separat weiter unten.','',
        '| Variante | Mittlere Abweichung² | Streuung zwischen Wolken | Messvarianz | Rauschfreier RMSE | Geometrie-/Modellanteil am MSE |',
        '|---|---:|---:|---:|---:|---:|']
    for v,label in zip(comp,labels):
        lines.append(f"| {label.replace(chr(10),' ')} | {v['bias_squared']:.6g} | {v['geometry_spread']:.6g} | {v['measurement_variance']:.6g} | {v['clean_rmse']:.6g} | {100*v['geometry_fraction']:.2f} % |")
    lines+=['','`MSE = mittlere Abweichung² + Geometrie-/Modellstreuung + Messvarianz`. '
        'Bei R unabhängigen Wiederholungen derselben Wolke sinkt allein der letzte Term um 1/R. '
        'Die folgenden Werte sind Folgen dieses Modells, keine zusätzlichen Beobachtungen.','',
        '| Variante | RMSE, 1 Messung | RMSE, 16 Messungen | RMSE, 512 Messungen | Grenze ohne Messrauschen |',
        '|---|---:|---:|---:|---:|']
    for v,label in zip(comp,labels):
        r=v['expected_rmse_by_measurement_averages']
        lines.append(f"| {label.replace(chr(10),' ')} | {r['1']:.6g} | {r['16']:.6g} | {r['512']:.6g} | {v['clean_rmse']:.6g} |")
    lines+=['','![Getrennte Fehlerbeiträge und Grenze der Messmittelung](results/error_components.png)','','Punktlinien markieren die Grenze ohne Messrauschen.','',
        '## Rauschmodell und Überdeckung','',
        f"{s['noise_checks']['tested_directions']} Richtungsprüfungen: regulär mit Mittelwert- und Varianztest, bei algebraischer Entartung mit festen numerischen Grenzen; "
        f"{len(s['noise_checks']['rejected'])} Ablehnungen bei einem vorab geteilten Familienfehlerbudget von 0,05 "
        f'(maximal 4096 statistische Tests; hier {ns} statistische Tests und {nd} deterministische Prüfungen). Die absichtlich falschen Modelle wurden erkannt: '
        f"Rootwert ausgelassen = {'ja' if s['noise_checks']['positive_controls']['root_omission_detected'] else 'nein'}, "
        f"Kreuzkovarianzen ignoriert = {'ja' if s['noise_checks']['positive_controls']['ignored_cross_covariance_detected'] else 'nein'}.",'',
        f"Der eingefrorene Geometriefaktor ist q={cal['quantile']:.6g}, Rang {cal['rank']} bei n={cal['complete']}. "
        f"Die gemeinsame marginale Nominalüberdeckung aller 16 Ausgaben beträgt unter den deklarierten Annahmen mindestens {100*cal['total_nominal_marginal_coverage_lower']:.3f} %. "
        'Sie gilt über unabhängige Kalibrier- und Testziehungen, nicht bedingt auf jede Wolke oder dieses eine Kalibrierergebnis.','',
        '| Anteil | Gemeinsame Testüberdeckung | Simultanes 95%-Binomialintervall | 95%-Populationsüberdeckung empirisch zertifiziert |',
        '|---|---:|---:|---|']
    for key,label in [('geometry','Geometrie/Modell'),('measurement','Messrauschen'),('total','Gesamt')]:
        v=s['coverage'][key];lo,hi=v['simultaneous_95_binomial_interval']
        lines.append(f"| {label} | {v['successes']}/{v['total']} ({100*v['rate']:.2f} %) | {100*lo:.2f}–{100*hi:.2f} % | {'Ja' if v['population_95_percent_empirically_certified'] else 'Nein'} |")
    radii=np.array([r['total_radii'] for r in s['coverage_records']])
    lines+=['',f"Gesamte Intervallhalbbreiten über Wolken/Felder/Varianten: Median {np.median(radii):.6g}, "
        f"Minimum {np.min(radii):.6g}, Maximum {np.max(radii):.6g}. "
        'Breite Intervalle sind kein Nachweis hoher Operatorgenauigkeit.','',
        '## Geometrie unabhängig vom Feldrauschen','',
        '| Rekonstruktion | Wolken mit Relationsfehlern | Fehlende / zusätzliche Relationen | Relativer Gram-RMS | Eigenzeit-RMSE / T, alle kausalen Paare |',
        '|---|---:|---:|---:|---:|']
    for key,label in [('original','Original'),('projected','Projiziert')]:
        v=s['geometry_diagnostics'][key]
        lines.append(f"| {label} | {v['clouds_with_relation_errors']}/{v['clouds']} | {v['missing']} / {v['extra']} | {v['gram_relative_rms']:.6g} | {v['proper_time_rmse_all_causal_pairs']:.6g} |")
    lines+=['','Die Eigenzeitprüfung umfasst alle tatsächlich kausalen Paare, auch falsch raumartig rekonstruierte Paare (τ̂=0). '
        'Relationskorrektheit allein belegt keine Abstandsgenauigkeit. Die vollständigen Kovarianzmatrizen und feldweisen Biaswerte stehen in [summary.json](results/summary.json).','',
        '## Deskriptiver Variantenvergleich','',
        '| Vergleich | Rauschfreies RMSE-Verhältnis | 95%-Bootstrapintervall, ganze Wolken |',
        '|---|---:|---:|']
    for key,v in s['descriptive_comparisons'].items():
        lo,hi=v['paired_cloud_bootstrap_95']
        lines.append(f"| {key} | {v['clean_rmse_ratio']:.6g} | {lo:.6g}–{hi:.6g} |")
    lines+=['','Diese Vergleiche sind deskriptiv. Sie ersetzen weder den historischen Metadaten-Test noch sein METADATA_HOLD. '
        'Keine Gewichte, Projektionsmetrik oder Kalman-Verstärkung wurden angepasst.','',
        '## Durchführung und Nachweise','',
        f"Quell-/Seed-Freeze: `{source}`. Kalibrier-Freeze vor Testbeginn: `{freeze}`. "
        f"Alle acht Prozesse mit vollständiger Laufzeit-/RSS-Telemetrie; Testbudget eingehalten: {'ja' if s['execution_within_budget'] else 'nein'}. "
        'Ausfälle werden behalten, nicht ersetzt. Die früheren 29 Wolken wurden ausdrücklich nur für Entwicklungsskalen wiederverwendet.','',
        '- [Vorabplan und Geltungsgrenzen](PROTOCOL.md)',
        '- [Vertrag](contract.json), [Seeds](seed_schedule.json), [eingefrorene Kalibrierung](frozen_calibration.json)',
        '- [Ergebnisdaten](results/summary.json), [Rauschprüfungen](results/noise_checks.json), [lokaler Replay](results/verification.json)',
        '- Rohprotokolle: `results/calibration/worker-*` und `results/test/worker-*`.','',
        '```sh',
        'OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 python -B research/lorentz_local_dalembert/error_calibration/ec_controls.py',
        'OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 python -B research/lorentz_local_dalembert/error_calibration/portable_verify.py',
        '```','',
        'Der [Portabilitätsadapter](REPLAY_PORTABILITY.md) berichtet die historischen Entwicklungs-Bytehashes separat; '
        'der unveränderte Originalverifier bleibt als `ec_verify.py` verfügbar. '
        'Replay prüft dieselben Beobachtungen numerisch mit eingefrorenen Toleranzen; Bytehashes werden separat berichtet. '
        'Keine vollständige Rahmensuche und keine externe Replikation. Dieser synthetische Flachraum-Pilot in 2+1 Dimensionen '
        'qualifiziert weder beliebige Felder und Dichten noch den 4D-Sampler, reale Geräte, Krümmung oder Onlinebetrieb.','']
    (HERE/'README.md').write_text('\n'.join(lines))


if __name__=='__main__':main()
