"""SPDX-License-Identifier: Apache-2.0
Presentation only; all quantities come from frozen analysis outputs.
"""
import json
from pathlib import Path
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np

H=Path(__file__).resolve().parent
s=json.loads((H/'results/summary.json').read_text());c=json.loads((H/'contract.json').read_text());f=json.loads((H/'source_freeze.json').read_text())
p=s['pooled_development'];v=p['variants'];blocks=s['historical_blocks'];selection=s['selection']
names=c['references']+c['candidates']
labels=['Ausgangsgeometrie','Ungewichtet','Nur Diagonale','Volle Matrix','Korrelation 10 %','Korrelation 25 %','Korrelation 50 %','Korrelation 75 %','Nur innerhalb Gruppen','Ohne Endpunkt-Kreuzkorrelation','Ohne raumartige Endpunktkorrelation','Ohne raumartige Wolkenkorrelation','Ohne kausale Wolkenkorrelation','Ohne gemeinsame Skalenkorrelation']
label=dict(zip(names,labels))
fig,axes=plt.subplots(1,2,figsize=(14,8),gridspec_kw={'width_ratios':[1.7,1]})
y=np.arange(len(names));ax=axes[0]
for phase,offset,color,legend in [('calibration',-.13,'#186a87','Alter Kalibrierungsblock (59)'),('test',.13,'#bc6727','Alter Testblock (55)')]:
 ax.scatter([100*(blocks[phase]['variants'][n]['ratio_to_baseline']-1) for n in names],y+offset,label=legend,color=color,s=32)
ax.axvline(0,color='#64748b',lw=1);ax.axvline(-1,color='#527c41',ls='--',lw=1,label='Fortsetzungshürde: −1 % in beiden Blöcken')
ax.set_yticks(y,labels);ax.invert_yaxis();ax.set_xlabel('RMSE-Änderung gegenüber Ausgangsgeometrie (%)');ax.grid(axis='x',alpha=.18);ax.legend(loc='upper left',bbox_to_anchor=(0,-.11),fontsize=8)
ax.set_title('Keine Variante erfüllt die Fortsetzungshürde',loc='left',fontweight='bold')
ax=axes[1];ns=['diagonal','full','shrink_010','drop_cross_group_endpoint','drop_support_causal_cloud','drop_signed_common_scale'];ys=np.arange(len(ns))
ax.barh(ys-.16,[v[n]['cross_term'] for n in ns],height=.3,color='#186a87',label='Fehlerausrichtung: 2⟨e, δ⟩')
ax.barh(ys+.16,[v[n]['step_squared'] for n in ns],height=.3,color='#bc6727',label='Schrittgröße: ⟨δ, δ⟩')
ax.set_yticks(ys,[label[n] for n in ns],fontsize=8);ax.invert_yaxis();ax.axvline(0,color='#64748b',lw=1);ax.grid(axis='x',alpha=.18);ax.legend(fontsize=8,loc='upper left',bbox_to_anchor=(0,-.11));ax.set_xlabel('Beitrag zur MSE-Änderung (gepoolt)');ax.set_title('Schrittgröße dominiert',loc='left',fontweight='bold')
fig.suptitle('Korrelationsdiagnose nach PR78',fontsize=18,fontweight='bold',x=.025,ha='left')
fig.text(.025,.025,'Entwicklungsdiagnose: 114 archivierte Geometrien, 1140 neue Optimierungen, keine neuen Simulationen.\nAlle bisherigen Testdaten sind hier wiederverwendete Entwicklungsdaten; keine unabhängige Bestätigung.',fontsize=10,color='#475569')
fig.tight_layout(rect=[0,.14,1,.94],w_pad=2);fig.savefig(H/'results/correlation_audit.png',dpi=170);plt.close(fig)
lines=['# Korrelationsdiagnose nach dem negativen Geometriekorrekturtest','',f"**{s['decision']}**. Keiner der zehn vorab festgelegten Kandidaten erfüllt die Fortsetzungsbedingungen in beiden historischen Datenblöcken.",'',
 'Alle 128 archivierten PR78-Versuche wurden übernommen: 114 vollständige Geometrien und 14 Abstentionen. Auf den vollständigen Geometrien wurden 1140 neue lokale Optimierungen gerechnet. **Keine neuen Simulationen, keine unabhängige statistische Bestätigung.** Der frühere Testblock wird hier ausdrücklich zu Entwicklungsdaten.','',
 f"Der deskriptiv beste Kandidat ist **{label[selection['lowest_descriptive_rmse']]}** mit einer gepoolten RMSE-Änderung von **{100*(v[selection['lowest_descriptive_rmse']]['ratio_to_baseline']-1):+.2f} %**. Die geforderte Verbesserung von mindestens 1 % in beiden Blöcken wird verfehlt. Deshalb startet diese Korrekturfamilie keinen neuen Bestätigungslauf.",'',
 '![Korrelationsdiagnose](results/correlation_audit.png)','','## Vergleich bei gleichen Einzelvarianzen','',
 '| Variante | Alter Kalibrierungsblock | Alter Testblock | Gepoolter RMSE | Fortsetzung |','|---|---:|---:|---:|---|']
for n in names:
 gate='Referenz' if n in c['references'] else ('PASS' if selection['eligibility'][n]['passed'] else 'FAIL')
 lines.append(f"| {label[n]} | {100*(blocks['calibration']['variants'][n]['ratio_to_baseline']-1):+.3f} % | {100*(blocks['test']['variants'][n]['ratio_to_baseline']-1):+.3f} % | {v[n]['rmse']:.6f} | {gate} |")
lines+=['','Prozentwerte sind RMSE-Änderungen gegenüber der jeweiligen Ausgangsgeometrie; negative Werte sind besser. Alle Varianten erhalten die beobachtete Kausalordnung exakt. Es gab keine Solver-Rückfälle. Die vier Referenzen werden aus PR78 wiederverwendet und sind keine nachträglich auswählbaren Kandidaten.','',
 '## Was den Schaden erklärt','',
 f"Die volle Matrix verschlechtert den gepoolten RMSE um {100*(v['full']['ratio_to_baseline']-1):.2f} %. Im Mittel entfallen **{100*v['full']['scale_step_energy_fraction']['mean']:.2f} %** der gewichteten quadratischen Korrekturbewegung auf die Richtung einer gemeinsamen Intervallskalierung. Dies ist ein Mittel der wolkenweisen Projektionsanteile, kein Anteil an der Gesamtfehlervarianz.",'',
 f"Die exakte MSE-Zerlegung ergibt für die volle Matrix: Fehlerausrichtung {v['full']['cross_term']:.9f}, quadratische Schrittgröße {v['full']['step_squared']:.9f}, Summe {v['full']['mse_change']:.9f}. Der positive Schrittbeitrag dominiert. Die Korrektur bewegt sich stark, ohne dies durch eine entsprechend günstige Fehlerausrichtung auszugleichen.",'',
 f"Das Entfernen der Endpunkt-Kreuzkorrelation reduziert die gepoolte Verschlechterung auf {100*(v['drop_cross_group_endpoint']['ratio_to_baseline']-1):.2f} %, das Entfernen der kausalen Wolkenkorrelation auf {100*(v['drop_support_causal_cloud']['ratio_to_baseline']-1):.2f} %. Das isolierte Entfernen der gemeinsamen Skalenkorrelation lässt noch {100*(v['drop_signed_common_scale']['ratio_to_baseline']-1):.2f} % Verschlechterung übrig. **Ein einzelner Skalenterm erklärt den Schaden daher nicht vollständig.** Die Eingriffe verändern nur Korrelationen, keine Einzelvarianzen; ihre Wirkungen sind wegen der nichtlinearen Korrektur nicht additiv.",'',
 f"Die Rang-eins-Identität für den Skalenterm ist mit maximalem numerischem Fehler {p['maximum_rank_one_identity_error']:.2g} erfüllt. Der Median des rohen Präzisionsverhältnisses in Skalenrichtung beträgt {p['signed_scale_precision_attenuation']['median']:.4f}. Diese algebraische Abschwächung allein beweist keine Ursache der beobachteten Fehlerverschlechterung.",'',
 '| Spektralbereich der vollen Korrelationsmatrix | Mittel der wolkenweisen quadrierten standardisierten Residuen |','|---|---:|']
for n,labeln in [('lowest_quarter','Unteres Viertel'),('middle_half','Mittlere Hälfte'),('highest_quarter','Oberes Viertel')]:lines.append(f"| {labeln} | {p['spectral'][n]['mean']:.4f} |")
lines+=['','Diese unskalierten Spektraldiagnosen deuten auf eine unzureichende Form der Arbeitskovarianz für die Korrektur hin. Sie sind keine neuen Freigabeschwellen und keine erneute Conformal-Kalibrierung.','',
 '## Entscheidung und Grenzen','',
 'Jeder Kandidat verfehlt die 1%-Verbesserung in beiden alten Blöcken. Der Stopp folgt der vor Ausführung öffentlich eingefrorenen Regel; es gibt keine nachträgliche Lockerung oder Auswahl einer Referenz. Das widerlegt nicht jede mögliche Geometriekorrektur, sondern beendet diese festgelegte Familie mit unverändertem Modell, Ziel und lokalem Solver.','',
 'Für einen späteren Ansatz wäre zunächst auf expliziten Entwicklungsdaten die Form des gemeinsamen Fehlermodells beziehungsweise die Skalierungsrichtung neu zu begründen. Erst ein vorab qualifizierter Kandidat rechtfertigt einen getrennten neuen Bestätigungstest. Das ist eine Forschungsrichtung, kein bereits ausgeführter oder validierter Folgeversuch.','',
 '**HOLD_BATCH_CORRECTION**, **HOLD_EMBEDDING_COVARIANCE**, **HOLD_KALMAN**, **HOLD_PHASE3** und **METADATA_HOLD** bleiben. Die Untersuchung betrifft flaches 2+1 bei rho=32768; sie qualifiziert keine radiale 4D-Geometrie, Koordinatenkovarianz oder neue Trennung physikalischer Fehlerquellen.','',
 '## Reproduktion','',f"- Öffentlicher Quellen- und Kriterien-Freeze: `{f['commit']}`.",f"- {len(f['files'])} unveränderte Quell- und Eingabedateien, alle 128 Versuchsausgänge und Vorhersagesiegel.",
 '- Analytische Kontrollen prüfen positive Definitheit, gleiche Einzelvarianzen, Spektrum, einzelne Komponenten, Verlustidentität, Skalenprojektion und negative Kontrollen sämtlicher Fortsetzungsbedingungen.',
 '- Numerischer Replay berechnet die 1140 Optimierungen erneut, erzeugt die 114 Wahrheitspunktmengen neu und prüft Auswertung, Herkunft und Entscheidung. Auswahl und ursprüngliche Rekonstruktion bleiben archivierte Eingaben.',
 '- Replay ist eine Reproduzierbarkeitsprüfung, keine unabhängige statistische Stichprobe. Ergebnisse stehen in `results/verification.json`; die GitHub-Prüfung wiederholt den Replay.','',
 '```sh','OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 python -B research/lorentz_local_dalembert/correlation_audit/ca_controls.py','OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 python -B research/lorentz_local_dalembert/correlation_audit/ca_verify.py','```','',
 'Details: [PROTOCOL.md](PROTOCOL.md), [contract.json](contract.json), [results/summary.json](results/summary.json). Dieser Bericht und die Grafik werden ausschließlich aus der eingefrorenen Auswertung erzeugt.','']
(H/'README.md').write_text('\n'.join(lines))
