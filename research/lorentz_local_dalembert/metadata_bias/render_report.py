"""Presentation only: reads frozen-analysis outputs, never selects a model."""
import json
from pathlib import Path
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np

HERE=Path(__file__).resolve().parent


def main():
    s=json.loads((HERE/'summary.json').read_text())
    frozen=json.loads((HERE/'frozen_model.json').read_text())
    names=['original','metadata','projected','projected_metadata','constant_ablation','projected_constant_ablation']
    labels=['Original','Metadaten','Relationskorrektur','Relation + Metadaten','Konstante Korrektur','Relation + konstant']
    t=s['groups']['transfer']
    fig,axes=plt.subplots(1,2,figsize=(12,5.2),gridspec_kw={'width_ratios':[1.1,1]})
    colors=['#64748b','#2563eb','#94a3b8','#0891b2','#cbd5e1','#cbd5e1']
    y=np.arange(len(names))
    vals=[t[n]['clean']['rmse'] for n in names]
    axes[0].barh(y,vals,color=colors)
    axes[0].set_yticks(y,labels); axes[0].invert_yaxis()
    axes[0].set_xlabel('Rauschfreier Operator-RMSE')
    axes[0].set_title('Vier untrainierte Transferfelder')
    for yy,v in zip(y,vals): axes[0].text(v+max(vals)*.015,yy,f'{v:.4f}',va='center',fontsize=9)
    axes[0].set_xlim(0,max(vals)*1.22)
    keys=['metadata_vs_original','projected_metadata_vs_projected']
    for i,k in enumerate(keys):
        c=s['comparisons'][k]; lo,hi=c['paired_cloud_bootstrap_95']; ratio=c['clean_rmse_ratio']
        axes[1].plot([lo,hi],[i,i],color=colors[1+2*i],lw=3)
        axes[1].plot(ratio,i,'o',color=colors[1+2*i],ms=7)
        axes[1].annotate(f'{ratio:.4f} [{lo:.4f}, {hi:.4f}]',(ratio,i),xytext=(0,16),textcoords='offset points',ha='center',fontsize=9)
    axes[1].axvline(1,color='#64748b',lw=1,label='Gleichstand')
    axes[1].axvline(.95,color='#dc2626',lw=1,ls='--',label='5%-Ziel')
    axes[1].set_yticks([0,1],['Originalarm','Relationsarm']);axes[1].set_ylim(1.6,-.65)
    axes[1].set_xlabel('RMSE mit / ohne Metadatenkorrektur')
    axes[1].set_title('95%-Bootstrap über ganze Wolken')
    axes[1].legend(loc='lower left',fontsize=8)
    for ax in axes:
        ax.spines[['top','right']].set_visible(False)
        ax.grid(axis='x',alpha=.15);ax.set_axisbelow(True)
    fig.suptitle(f"Eigenzeit · Metadatenkorrektur · {s['decision']}",fontsize=14,fontweight='bold')
    fig.text(.5,.015,f"{s['complete']}/{s['total']} Wolken vollständig · Felder sind keine unabhängigen Replikate · keine Einbettungskovarianz",ha='center',fontsize=9)
    fig.tight_layout(rect=[0,.04,1,.94]); fig.savefig(HERE/'results.png',dpi=180); plt.close(fig)
    lines=['# Eigenzeit: Metadatenkorrektur auf neuen Feldern','',
           f"**Entscheid: {s['decision']}; HOLD_PHASE3.**",'',
           'Der Pilot prüft eine feldlineare, metadatenabhängige Korrektur der Operatorgewichte. '
           'Konstanten und rekonstruierte lineare/quadratische Momente bleiben erhalten. '
           'Die Geometrie selbst wird durch diese neue Korrektur nicht geändert. Die vorhandene '
           'Relationsprojektion ist weiterhin euklidisch, keine kovarianzgewichtete Einbettungskorrektur.','',
           f"Code, Protokoll und Kalibrierung wurden vor den neuen Testwolken öffentlich unter `{s['execution'][0]['source_commit']}` eingefroren. "
           f"Training: {frozen['training_complete']}/{frozen['training_clouds']} alte Wolken. Residualkalibrierung: "
           f"{frozen['calibration_complete']}/{frozen['calibration_clouds']} weitere alte Wolken. Neuer Test: **{s['complete']}/{s['total']}**. "
           'Keine Ersatzseeds, kein Nachjustieren auf Testdaten.','',
           'Sechs Trainingsfelder und vier zuvor untrainierte Parameterkombinationen derselben analytischen '
           'Feldfamilie `exp(a t) cos(b x + px) cos(c y + py)`. Der wahre Operatorwert variiert. '
           'Dies prüft einen begrenzten Feldtransfer, keine beliebigen Feldfamilien oder Dichten. '
           'Die Ablationen verwenden konstante Korrekturkoeffizienten ohne Metadaten im Regressionsmodell, '
           'aber denselben metadatenbasierten OOD-Schutz.','',
           '## Primärer Vergleich: vier Transferfelder','',
           '| Verfahren | Sauberer RMSE | Mittlerer Fehler | Zentrierte RMS | Posterior-RMSE | Nominelle 95%-Überdeckung |',
           '|---|---:|---:|---:|---:|---:|']
    for name,label in zip(names,labels):
        v=t[name]
        lines.append(f"| {label} | {v['clean']['rmse']:.6f} | {v['clean']['bias']:.6f} | {v['clean']['centered_rms']:.6f} | {v['posterior']['rmse']:.6f} | {v['coverage_hits']}/{v['field_responses']} |")
    lines += ['', 'Feldantworten innerhalb einer Wolke sind abhängig. Die Überdeckungszahlen sind '
              'beschreibend; alle Unsicherheitsintervalle werden über ganze Wolken gebootstrapt. '
              'Der Bootstrap konditioniert auf die eingefrorene Kalibrierung und ist keine Überdeckungsgarantie.','',
              '| Vergleich | Sauberer RMSE-Quotient | Wolken-Bootstrap 95% | Größter Einzel-Feld-Quotient |','|---|---:|---:|---:|']
    for k in keys:
        v=s['comparisons'][k]; lo,hi=v['paired_cloud_bootstrap_95']
        lines.append(f"| {k} | {v['clean_rmse_ratio']:.6f} | [{lo:.6f}, {hi:.6f}] | {v['maximum_per_transfer_field_ratio']:.6f} |")
    lines += ['', '![Transfervergleich](results.png)','', '## Vorab festgelegte Kriterien','', '| Kriterium | Ergebnis |','|---|---|']
    for k,v in s['gates'].items(): lines.append(f"| {k} | {'PASS' if v else 'FAIL'} |")
    lines += ['', '## Relationsverträglichkeit und Einsatzbereich','',
              f"Vor der bisherigen Relationsprojektion: {s['relations']['before_failed']}/{s['complete']} Rekonstruktionen mit Fehlpaaren. "
              f"Danach: {s['relations']['after_failed']}/{s['complete']}, bei {s['relations']['pairs']} geprüften gerichteten Paaren. "
              'Das betrifft Root/Stützen und ist eine Konstruktionsbedingung, kein Nachweis korrekter Abstände.','',
              '| Korrektur | Außerhalb Trainingsbereich | Normbegrenzung aktiv | Max. Rauschvarianzfaktor |','|---|---:|---:|---:|']
    for name,v in s['diagnostics'].items():
        lines.append(f"| {name} | {v['ood_clouds']} | {v['clipped_clouds']} | {v['maximum_noise_ratio']:.6f} |")
    lines += ['', 'Alle OOD-Fälle verbleiben in der Auswertung und verwenden unveränderte Gewichte. '
              'Geometrisch nicht verfügbare Fälle werden nicht ersetzt; die ergänzende Kennzahl '
              '`all_clouds_with_prior_fallback_rmse` umfasst alle 32 Wolken.','',
              '## Fehlertrennung','',
              'Die sechs tatsächlichen Gewichtsvektoren liefern `N(C)=sigma² B Bᵀ`, einschließlich '
              'gemeinsamen Rootwerts und aller Kreuzterme. Die saubere Residualkovarianz und ihr Mittelwert '
              'werden separat kalibriert. Der Filter verwendet `R=G+mu muᵀ+N(C)` als zweites Fehlermoment. '
              'Das ist keine validierte bedingte Geometriekovarianz. Modell-/Kalibrierunsicherheit ist nicht '
              'vollständig erfasst. Keine zusätzliche globale Bias-Subtraktion; deshalb sind diese '
              'Posteriorwerte nicht unmittelbar mit dem früheren Ein-Feld-Piloten vergleichbar.','',
              '## Reproduktion und offene Grenze','',
              'Fünf Kontrollgruppen prüfen Moment-/Konstantenerhaltung und Linearität, Umnummerierung, '
              'OOD-Rückfall/Informationsgrenze, gemeinsames Rootrauschen und analytische Feldwahrheit. '
              'Der numerische Replay prüft Residualkalibrierung, erneute Relationsprojektion, '
              'Momentzertifikate, gemeinsame Rauschkovarianz, Feldantworten und Auswertung. '
              'Die teure vollständige Rahmensuche wird dabei nicht wiederholt; keine externe Replikation.','',
              'Siehe [Prüfvertrag](PROTOCOL.md), [vollständige Kennzahlen](summary.json), '
              '[Reproduktion](README.md) und [Audit zur Einbettungskovarianz](EMBEDDING_COVARIANCE_AUDIT.md). '
              'Ansatz 2 bleibt bis zur eigenständigen Einbettungskovarianz-Validierung offen; '
              'Ansatz 3 bis zum Identifizierbarkeitsnachweis. Keine Online-, Geräte- oder Krümmungsfreigabe.','']
    (HERE/'RESULTS.md').write_text('\n'.join(lines))


if __name__=='__main__': main()
