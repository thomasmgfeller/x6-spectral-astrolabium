"""Render measured pilot outcomes; no fitting or selection."""
import json
from pathlib import Path
import numpy as np
HERE=Path(__file__).resolve().parent

def main():
    s=json.loads((HERE/'independent_summary.json').read_text());c=json.loads((HERE/'frozen_calibration.json').read_text())
    v=json.loads((HERE/'CALIBRATION_VERIFICATION.json').read_text())
    executions={k:json.loads((HERE/('independent_'+k)/'execution.json').read_text()) for k in ['calibration','test']}
    lines=['# Unabhängiger Operator-/Fusionspilot — 20. Oktober 2026','',
      '**Entscheid: '+s['decision']+'; HOLD_PHASE3.**','',
      'Öffentlicher computational Freeze vor den neuen Wolken: `315d7c31507a852edc84b9e52dece561c81c72b3`.',
      '32 Kalibrierwolken und 32 getrennte Testwolken bei rho=32768. Die Läufe wurden parallel berechnet; die Testauswertung erfolgte erst nach dem Einfrieren der aus Kalibrierdaten bestimmten Parameter. Keine Testdatenanpassung.','',
      '## Verfügbarkeit und Budget','',
      '| Split | Physische Wolken | Laufzeit (s) | Peak-RSS (MiB) | Status |','|---|---:|---:|---:|---|']
    for name,e in executions.items():lines.append(f"| {name} | {len(e['records'])} | {e['seconds']:.1f} | {e['peak_mib']:.1f} | {e['status']} |")
    lines += ['',f"Auswertbar: Kalibrierung {c['complete']}/{c['total']}, Test {s['complete']}/{s['total']}. Nicht verfügbare Wolken bleiben im Verfügbarkeitsnenner. Genauigkeitswerte gelten nur für vollständige, zuvor bewachte Fälle.",'',
      '## Festgelegter Vergleich','',
      'Drei Operatorantworten derselben Wolke und desselben verrauschten Feldes: übertragene Basis, unbeschränkte L1-Gewichte, unbeschränkte Varianzgewichte. Die Vorzeichenbeschränkung wird separat geprüft. Das Testfeld lautet exp(t/2) cos(x/2) cos(y/2) relativ zum Root; sein wahrer Operatorwert ist -0.75. Keine räumliche Einbettung wird hier durch den Filter korrigiert.','',
      'Eine synthetische unabhängige Prädiktion mit Standardabweichung 0.5 wird pro Testwolke für alle Filterarme gemeinsam verwendet. Die Kalman-Anbindung ist daher ein Ein-Schritt-Vergleich mit explizit C=0, kein nachgewiesenes Bewegungsmodell.','']
    if c['status']=='FROZEN' and s['arms']:
        lines += ['| Filterarm | Mess-RMSE nach Bias-Korrektur | Posterior-RMSE | 95%-Abdeckung | Exaktes 95%-Intervall der Abdeckungsquote |','|---|---:|---:|---:|---|']
        for name,a in s['arms'].items():lines.append(f"| {name} | {a['measurement_rmse']:.6f} | {a['posterior_rmse']:.6f} | {100*a['coverage']:.2f}% | {100*a['coverage_exact_95'][0]:.1f}–{100*a['coverage_exact_95'][1]:.1f}% |")
        lines += ['',f"Gepaarter Posterior-RMSE-Quotient joint/single: **{s['paired_rmse_ratio']:.6f}**; 95%-Bootstrapintervall {s['paired_bootstrap_95'][0]:.6f}–{s['paired_bootstrap_95'][1]:.6f}. Vorab gefordert: <=0.95. Das Bootstrapintervall konditioniert auf die eingefrorene Kalibrierung.",'',
          '### Eingefrorene Kalibrierung','',f"Ausgewählter Einzelarm (Index 0/1/2): {c['best_single']}. Gemeinsame Fusionsgewichte: {c['joint_weights']}. Kovarianzkondition: {c['covariance_condition']:.3g}.",'',
          '| Arm | Geschätzter Bias | Roh-RMSE Test | Fehler-RMSE ohne Feldrauschen |','|---|---:|---:|---:|']
        for i,name in enumerate(['Basis','L1','Varianz-QP']):lines.append(f"| {name} | {c['bias'][i]:.6f} | {s['raw_rmse_by_arm'][i]:.6f} | {s['clean_rmse_by_arm'][i]:.6f} |")
        lines+=['','Gemeinsame Fehlerkovarianz aus Kalibrierwolken (vor dem Faktor 1+1/n für Bias-Mittelschätzung):','','| | Basis | L1 | Varianz-QP |','|---|---:|---:|---:|']
        for name,row in zip(['Basis','L1','Varianz-QP'],c['joint_covariance']):lines.append('| '+name+' | '+' | '.join(f'{x:.6g}' for x in row)+' |')
        lines+=['','Korrelationen derselben Fehler:','','| | Basis | L1 | Varianz-QP |','|---|---:|---:|---:|']
        for name,row in zip(['Basis','L1','Varianz-QP'],s['calibration_correlation']):lines.append('| '+name+' | '+' | '.join(f'{x:.4f}' for x in row)+' |')
        lines+=['',f"Vorzeichenbeschränktes QP mit geprüftem Zertifikat auf den vollständigen Testfällen: {s['signed_qp_verified']}/{s['complete']}.",'',
          '| Vorab festgelegtes Kriterium | Ergebnis |','|---|---|']
        for name,value in s['gates'].items():lines.append(f"| {name} | {'PASS' if value else 'FAIL'} |")
    lines+=['','## Ergänzende Unsicherheitsdiagnose','',
      'Die bedingte Feldrauschvarianz des Varianz-QP ist stark wolkenabhängig. Der eingefrorene Pilot verwendete eine gemeinsame empirische Kovarianz; die folgende Diagnose ändert diese Auswertung nicht.','',
      '| Split | Minimum | Median | Maximum |','|---|---:|---:|---:|']
    for split in ['calibration','test']:
        rows=[json.loads(p.read_text()) for p in (HERE/('independent_'+split)).glob('seed-*.json')]
        vals=[r['operator']['conditional_field_covariance'][2][2] for r in rows if r['operator']['status']=='COMPLETE']
        lines.append(f"| {split} | {np.min(vals):.6f} | {np.median(vals):.6f} | {np.max(vals):.6f} |")
    lines+=['','Der Extremfall bleibt vollständig enthalten. Für einen Folgeversuch ist die bekannte wolkenabhängige Feldrauschkovarianz separat von der noch zu kalibrierenden Geometrieunsicherheit zu behandeln. Aus einer globalen mittleren Kovarianz folgt keine gleich gute Unsicherheitsbeschreibung jeder einzelnen Wolke.']
    rel=v['reconstructed_relation_diagnostic'];bad=[r for r in rel if not r['passed']]
    lines+=['','## Nachprüfung und Kausalität','',
      f"{v['clouds']} archivierte Wolken, {v['lp_certificates']} LP-Zertifikate, {v['qp_certificates']} QP-Zertifikate und {v['causal_intervals']} verwendete Intervalle nachgeprüft. Alle regenerierten Koordinaten-Hashes und Feld-/Rauschantworten stimmen überein. Die vollständige teure Rahmensuche wurde in dieser Nachprüfung nicht erneut ausgeführt.",'',
      f"Ergänzende, nicht als primäres Abnahmekriterium registrierte Relationsdiagnose: {len(bad)}/{len(rel)} ausgewählte rekonstruierte Punktmengen haben mindestens eine fehlende oder zusätzliche gerichtete Relation. Insgesamt fehlen {sum(r['missing'] for r in rel)} Relationen; {sum(r['extra'] for r in rel)} werden zusätzlich vorhergesagt. Geprüft werden Root und Stützpunkte, nach Orientierung der rekonstruierten Zeitachse am markierten Zukunftspunkt. Es erfolgt keine lautlose Reparatur.",'',
      f"Die Relationsdiagnose umfasst {sum(r['ordered_pairs_evaluated'] for r in rel)} gerichtete Nichtdiagonalpaare, davon {sum(r['true_relations'] for r in rel)} wahre Relationen. Eine Wolke mit mindestens einem Fehlpaar ist nicht gleichbedeutend mit einer überwiegend falschen Rekonstruktion.",'',
      'Alle zum Zählen verwendeten Intervalle sind im Simulator kausal. Das garantiert nicht, dass die rekonstruierten Koordinaten alle Paarrelationen erhalten. Die Stützen verwenden auch Zukunftsdaten; dieser Pilot ist offline. Eine Online-Ausgabe braucht eine deklarierte Verzögerung oder eine neu validierte vergangenheitsbasierte Konstruktion.','',
      '## Geltungsgrenzen','',
      '- Minimierte bedingte Feldrauschvarianz enthält keine Garantie über Geometriefehler. Gemeinsamer Bias kann trotz kleiner Streuung bestehen.',
      '- Bias und Kovarianz sind an genau diese Dichte, Auswahlregel und Testfeldverteilung gebunden. Unabhängige neue Felder und andere Skalen sind noch zu prüfen.',
      '- Die empirische Kovarianz und nominellen Gaussian-Intervalle sind keine garantierten Fehlergrenzen. Die kleine Testzahl erlaubt nur breite Abdeckungsintervalle.',
      '- Die ursprüngliche naive Unabhängigkeits-Negativkontrolle und die hier diagonalisierte kalibrierte Kovarianz sind unterschiedliche Versuche.',
      '- Keine validierte Einbettungskovarianz, keine sequenzielle Filtervalidierung, kein Neuheits-/Krümmungsnachweis. HOLD_PHASE3 bleibt bestehen.','',
      '## Reproduktion','',
      'Die vollständigen Einzelwolken liegen in `independent_clouds.zip` samt SHA256-Manifest. Im Modulordner entpacken, danach vom Repository-Root:','',
      '```sh',
      'python -m zipfile -e research/lorentz_local_dalembert/feynman_combiner/independent_clouds.zip research/lorentz_local_dalembert/feynman_combiner',
      'OPENBLAS_NUM_THREADS=1 python -B research/lorentz_local_dalembert/feynman_combiner/verify_calibration.py',
      'OPENBLAS_NUM_THREADS=1 python -B research/lorentz_local_dalembert/feynman_combiner/analyze_calibration.py test',
      '```','',
      'Für eine vollständige Neuberechnung in einem separaten Checkout ohne entpackte Ergebnisordner `run_calibration.py --split calibration`, dann `analyze_calibration.py fit`, dann `run_calibration.py --split test` und `analyze_calibration.py test` verwenden. Bestehende Ergebnisordner werden nicht überschrieben.']
    (HERE/'CALIBRATION_RESULTS.md').write_text('\n'.join(lines)+'\n')

if __name__=='__main__':main()
