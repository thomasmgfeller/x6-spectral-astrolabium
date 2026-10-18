"""Generate the report and research figure from the frozen evidence."""
import json
from pathlib import Path
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

HERE=Path(__file__).resolve().parent
s=json.loads((HERE/'results/summary.json').read_text())
e=json.loads((HERE/'results/execution.json').read_text())
v=json.loads((HERE/'VERIFICATION.json').read_text())
primary=s['rows'][-1]
lines=['# Eigenzeit: geglätteter BD-Operator gegen C2', '',
'**Entscheid: NO_GO für den Ausbau auf variable Krümmung innerhalb dieses Pilotbudgets.**', '',
'Die Referenz ist implementiert, alle 6.528 Wolken wurden vollständig wiederholt,',
'und 102 davon zusätzlich mit einem getrennten Kausalitätstest gegengeprüft.',
'384 flache Entwicklungswolken wählten die Glättung; 6.144 Testwolken blieben',
'davon getrennt. Die zwölf Testzellen umfassen Minkowski und drei de-Sitter-Stärken.', '',
'Der Quellen- und Vertragsstand wurde vor den Läufen lokal eingefroren:',
f'`{e["source_ref"]}`. Eine öffentliche Vorregistrierung fand nicht statt,',
'weil die automatische Freigabeprüfung den GitHub-Push blockierte.', '',
'## Hauptvergleich', '',
'Bekannte physische Dichte, bekannte Eigenzeit T=1, h=0,5; Zielwert',
f'R=q={primary["truth"]:.8f}. Je Schätzung 32 unabhängige Poisson-Wolken;',
'16 unabhängige Schätzungen pro Testzelle. Die Dichte entspricht im flachen',
'Fall 2.048 erwarteten Punkten pro Wolke. Gewählt wurde epsilon=0,025.', '',
'| Kennzahl | BD | C2 |', '|---|---:|---:|']
for label,key in [('Empirischer Bias','bias'),('Streuung der Gruppenschätzungen (SD)','sd_group_estimates'),('RMSE','rmse'),('Mediane Intervallhalbbreite','median_halfwidth')]:
    lines.append(f'| {label} | {primary["metrics"]["BD"][key]:.6f} | {primary["metrics"]["C2"][key]:.6f} |')
lines += [f'| Beobachtete Überdeckung nominaler 95%-Intervalle | {primary["metrics"]["BD"]["covered"]}/16 | {primary["metrics"]["C2"]["covered"]}/16 |', '',
f'Das RMSE-Verhältnis BD/C2 beträgt {primary["metrics"]["BD"]["rmse"]/primary["metrics"]["C2"]["rmse"]:.2f}.',
'Das deskriptive gepaarte Bootstrap-Intervall beträgt [20,24; 58,96].',
'Die vorab geforderten Grenzen für RMSE, Bias, Intervallbreite und flachen',
'Bias werden verfehlt. Die Mindestüberdeckung und Kostengrenze bestehen.', '',
'**Bias und Streuung trennen:** Das 95%-Monte-Carlo-Intervall des empirischen',
'BD-Bias reicht von −13,74 bis +1,15. Sein Punktschätzer allein belegt daher',
'keinen systematischen Fehler dieser Grösse. Die unabhängige Kontinuumsquadratur',
f'liefert bei derselben Glättung und demselben endlichen Diamanten E[Rhat]={primary["continuum_mean"]:.6f},',
f'also einen endlichen Skalen-/Randfehler von {primary["continuum_bias"]:.6f} gegenüber dem Ziel.',
'Die simulierten Mittelwerte sind in allen zwölf Zellen mit der unabhängigen',
'Quadratur innerhalb der vorab gewählten Kontrolltoleranz vereinbar.', '',
'## Alle Testzellen', '',
'| Flache erwartete Punktzahl | h | Wahrer R-Wert | RMSE BD | RMSE C2 | Überdeckung BD | Überdeckung C2 |',
'|---:|---:|---:|---:|---:|---:|---:|']
for r in s['rows']:
    b,c=r['metrics']['BD'],r['metrics']['C2']
    lines.append(f'| {r["flat_expected_count"]} | {r["h"]:.2f} | {r["truth"]:.4f} | {b["rmse"]:.4f} | {c["rmse"]:.4f} | {b["covered"]}/16 | {c["covered"]}/16 |')
lines += ['', '![RMSE bei den drei festgelegten Dichten](results-overview.png)', '',
'Bei der kleinsten Dichte hat BD in drei Zellen einen kleineren beobachteten',
'RMSE. Der Hauptvergleich verfehlt dennoch den vorab verlangten Nutzen.',
'Es wird deshalb kein allgemeines Überlegenheitsurteil für C2 und keine',
'Widerlegung der BD-Kontinuumsgrenze abgeleitet.', '',
'## Aussagegrenzen', '',
'- Die vier epsilon-Werte waren vorab festgelegt. Alle Dichten wählten den kleinsten Wert.',
'  Eine breitere Glättungssuche könnte das Ergebnis ändern und benötigt neue Testdaten.',
'- Bei festem epsilon schrumpft l_k mit steigender Dichte. Das ist kein Nachweis',
'  eines Grenzübergangs mit hinreichend unterdrückter Varianz. Im Hauptfall ist',
f'  l={primary["l"]:.4f}, l_k={primary["l_k"]:.4f}; die Skalen sind nur mässig getrennt.',
'- C2 nutzt die bekannte de-Sitter-Familie und den Bereich 0≤h≤0,5. Im Hauptfall',
'  werden 6/16 Punktschätzungen an der oberen Modellgrenze begrenzt. BD wird',
'  nicht entsprechend begrenzt. Das ist ein Vergleich der deklarierten Verfahren,',
'  keine allgemeine Rangordnung modellfreier Schätzer.',
'- Die Student-Intervalle sind nominal. 14/16 oder 16/16 beobachtete Treffer',
'  belegen keine garantierte 95%-Überdeckung. Die konservativen zusätzlichen',
'  C2-Hoeffding-Intervalle umfassen im Hauptfall den gesamten Modellbereich.',
'- Auch C2 erreicht dort mit einer medianen Halbbreite von rund 29% des Zielwerts',
'  die hier verwendete 20%-Breitenvorgabe nicht. Eine generische Krümmungsuhr',
'  ist damit weiterhin nicht nachgewiesen.',
'- Bei einer flachen Zelle entstehen einzelne unendliche Bootstrap-Verhältnisse,',
'  wenn alle gezogenen C2-Schätzungen auf null begrenzt sind. Die archivierten',
'  2,5%- und 97,5%-Quantile bleiben endlich; die Warnung wird nicht verschwiegen.', '',
'## Aufwand und Wiederholung', '',
f'Der Ziellauf benötigte {e["wall_seconds"]:.2f} s Wandzeit, {e["cpu_seconds"]:.2f} s CPU-Zeit',
f'und maximal {e["peak_rss_mib"]:.1f} MiB RAM; feste Grenzen: 600 s und 2 GiB.',
'Diese Zeiten betreffen den Benchmark, nicht Entwicklung und Gegenprüfung.',
'Zusätzliche kostenpflichtige Rechenressourcen wurden nicht verwendet.',
f'Im Hauptfall lagen die Extraktionszeiten für 512 Wolken bei {primary["c2_total_seconds"]:.3f} s für C2',
f'und höchstens {primary["bd_total_upper_seconds"]:.3f} s für BD (alle vier Glättungen berechnet).',
'Beide enthalten dieselbe Erzeugungs- und Relationsarbeit. Die Gruppenanalyse',
'und einmalige Einrichtung sind gesondert in den JSON-Daten ausgewiesen.', '',
'```sh', 'OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 python3 -B research/lorentz_bd_reference/verify.py --archive research/lorentz_bd_reference/results --replay', '```', '',
'Erwartet: `PASS_FULL_REPLAY`, 6.528 Wolken und 102 unabhängige Relationsprüfungen.',
'Ein C++17-Compiler, Python, NumPy und SciPy werden benötigt. Der Nachbau ist',
'eine interne unabhängige Gegenrechnung von Teilkomponenten, keine externe Replikation.', '',
'## Neuer lokaler Operator', '',
'[Boguñá–Krioukov-Zweig](../lorentz_local_dalembert/README.md): Quellenprüfung,',
'Akzeptanzfolge und getestete Koeffizientenzusammensetzung sind vorbereitet.',
'Eine intrinsische Reproduktion fehlt noch. Der konstante Feldtest ergibt dort',
'identisch null; die BD-Krümmungsregel −2B(1) darf nicht übernommen werden.', '',
'[Methoden und Primärquelle](METHODS.md) · [Vertrag](contract.json) ·',
'[Kontrollprotokoll](VERIFICATION.json) · [vollständige Rohdaten](results/)', '',
'English: Implemented and internally replayed 4D Poisson smoothed BD reference.',
'The preregistered-in-local-git finite-budget gate fails; variable curvature is stopped.',
'The restricted C2 comparator benefits from known model boundaries. No universal',
'dominance, certified Student coverage or curved-clock claim. The local-operator',
'track is a preflight, not an intrinsic reproduction.']
(HERE/'RESULTS.md').write_text('\n'.join(lines)+'\n')
plt.rcParams.update({'font.size':10,'axes.spines.top':False,'axes.spines.right':False})
fig,axes=plt.subplots(2,2,figsize=(9,6),layout='constrained')
for ax,h in zip(axes.flat,[0,.1,.25,.5]):
    rs=[r for r in s['rows'] if r['h']==h]
    for method,color in [('BD','#bf5b25'),('C2','#176d9c')]:
        ax.plot([r['flat_expected_count'] for r in rs],[r['metrics'][method]['rmse'] for r in rs],'-o',label=method,color=color)
    ax.set_xscale('log',base=2); ax.set_yscale('log'); ax.set_xticks([128,512,2048],['128','512','2048'])
    ax.set_title(f'h={h:g}; R={rs[0]["truth"]:.3f}'); ax.set_xlabel('Expected points in flat diamond'); ax.set_ylabel('RMSE of 32-cloud estimate'); ax.grid(alpha=.18)
axes[0,0].legend(frameon=False)
fig.suptitle('Poisson BD–C2 pilot: fixed development-selected smoothing',fontsize=13)
fig.savefig(HERE/'results-overview.png',dpi=180)
fig.savefig(HERE/'results-overview.svg')
svg=HERE/'results-overview.svg'
svg.write_text('\n'.join(line.rstrip() for line in svg.read_text().splitlines())+'\n')
