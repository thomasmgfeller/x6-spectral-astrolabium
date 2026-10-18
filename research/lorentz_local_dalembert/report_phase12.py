"""Render the already-frozen analysis, without changing scientific gates."""
import json
from pathlib import Path
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np

HERE=Path(__file__).resolve().parent
PILOT=HERE/'phase12'
s=json.loads((PILOT/'results/summary.json').read_text())
cells=s['cells']; densities=[c['rho'] for c in cells]
def fmt(v): return '—' if v is None else f'{v:.3f}'
rows=[]
for c in cells:
    rows.append('| '+ ' | '.join([str(c['rho']),fmt(c['mean_poisson_count']['mean']),
        fmt(c['time_relative_rmse']['rms']),fmt(c['space_relative_rmse']['rms']),
        f"{c['operator_available']['success']}/16",fmt(c['oracle_metric_error']['rms']),
        f"{c['chart_available']['success']}/16",fmt(c['chart_metric_error']['rms'])])+' |')
gaterows=[]
for phase in ['phase1_gates','phase2_gates']:
    for name,passed in s[phase].items():
        gaterows.append(f"| {phase} | {name} | {'PASS' if passed else 'FAIL'} |")
high=cells[-1]
text=f'''# BK Phase 1/2 — Ergebnisse des flachen Piloten

**Entscheid: `{s['decision']}`.** Die intrinsische Implementierung und der
Produktidentitäts-Test sind ausgeführt; die wissenschaftliche Abnahme ist
nicht bestanden. Das betrifft diesen begrenzten 2+1-Piloten und seine
Nachbarschafts-/Ankersuche. Es widerlegt weder den BK-Kontinuumsgrenzwert noch
belegt es ein grundsätzliches Scheitern intrinsischer Metrikrekonstruktion.

## Vor den Daten fixiert

- Öffentlicher Protokollcommit: `032024b2369a42e52538ec97466831623b1b47f5`.
- Öffentlicher Implementierungs- und Analysecommit: `{s['source_commit']}`.
- 48 unabhängige Testwolken, 16 je Dichte; sechs separate Entwicklungswolken.
- 2+1 Minkowski, bekannte konstante Poisson-Intensität; externe Koordinaten
  ausschliesslich im Sampler und im unabhängigen Prüfer.
- [Vertrag](phase12/contract.json), [Protokoll](phase12/PROTOCOL.md),
  [Implementierungsentscheidungen](phase12/IMPLEMENTATION.md),
  [Rohdaten und Quellhashes](phase12/results/execution.json),
  [vollständige Kennzahlen](phase12/results/summary.json).

## Quantitative Ergebnisse

| Dichte rho | Mittlere Punktzahl | Zeitfehler RMS | Raumfehler RMS* | Operator verfügbar | Metrikfehler, glatte Felder** | Intrinsische Karte | Metrikfehler, intrinsische Felder** |
| --- | --- | --- | --- | --- | --- | --- | --- |
{chr(10).join(rows)}

Fehler sind relativ und dimensionslos. Zeit-/Raumwerte aggregieren zuerst
innerhalb einer Wolke und dann gleichgewichtet über Wolken. *Raumfehler sind
bedingt auf eine erfolgreiche Ankersuche. **Metrikfehler sind relative
Frobeniusnormen, als RMS über verfügbare Fälle; die festgelegte Grenze ist 0,5.
Nicht verfügbare Fälle bleiben im Nenner der Verfügbarkeits- und Signaturquoten.

Bei rho=32768 beträgt der mittlere Rangkorrelationswert der verfügbaren
Abstandsschätzungen {high['space_spearman']['mean']:.4f} (15 auswertbare Wolken).
Gleichzeitig fehlen im Wolkenmittel {100*high['missing_distance_fraction']['mean']:.1f}% der räumlichen
Abstandsschätzungen. Die intrinsische Auswahl erfasst nur
{100*high['true_cap_recall']['mean']:.1f}% der im Prüfer bekannten wahren Kappenpunkte. Diese beiden
Quoten sind keine austauschbaren Grössen: die erste umfasst auch entfernte
Schalenpunkte, die zweite nur die tatsächlich gewünschte lokale Kappe.
Gute Rangwerte der verbleibenden Paare begründen daher keine zuverlässige
Nachbarschaftsrekonstruktion.

Die nachträgliche geometrische Randprüfung findet bei 15/16, 5/16 und 1/16
Wolken (aufsteigende Dichte) Kappenpunkte ausserhalb des Diamanten. Kausale
Intervalle bleiben vollständig; die gewünschte räumliche Schale kann dennoch
abgeschnitten sein. Der Dichtevergleich enthält somit auch einen abnehmenden
Randeffekt. Null Randzeugen in einem Einzelfall sind kein Einschlussbeweis.

Nur {high['operator_available']['success']}/16 der dichtesten Wolken haben mindestens vier verwendbare
Punkte auf beiden Zeitseiten. Nur {high['oracle_signature']['success']}/16 liefern die richtige Signatur
in der glatten Testkarte; dasselbe gilt für die intrinsische Karte. Unter den
drei verfügbaren Fällen sind das jeweils 2/3. Der Wilson-95%-Bereich der
Gesamtquote 2/16 liegt bei 3,5–36,0%; 16 Wolken erlauben keine präzise
Erfolgswahrscheinlichkeit. Die intrinsischen Felder selbst haben einen
bedingten relativen RMS-Fehler von {high['chart_field_error']['rms']:.3f}; ihre abgeleitete Metrik ist
wesentlich ungenauer. Bereits mit glatten vorgegebenen Feldern verfehlt der
Operator die Metrikvorgabe. Das Problem liegt deshalb nicht allein in den
rauschenden künstlichen Koordinaten.

![Dichte, Verfügbarkeit und Metrikfehler](phase12/results-overview.png)

Die Darstellung verbindet nur drei endliche Dichten; sie belegt keine
asymptotische Konvergenz. Mittelwerte, Standardfehler, Wilson-Intervalle und
alle einzelnen Feldantworten sind in der maschinenlesbaren Auswertung.

## Software und fachliche Abnahme

Konstanten werden exakt annihiliert. Die Produktformel stimmt mit der separat
akkumulierten gewichteten äusseren Produktform überein. Affine Kartenwechsel
einschliesslich Translation bestehen. Drei Umnummerierungsprüfungen, eine je
Dichte, transportieren die unabhängigen Zufallsmarken mit den Ereignissen.
2.272 längste Pfade wurden gegen erschöpfende Pfadsuche geprüft; fünf
Überlappungswerte gegen unabhängige adaptive Quadratur. Eine künstliche
symmetrische Referenzschablone prüft Komponenten und Vorzeichen und verwirft
Nullausgabe bzw. ein unverändert fest vorgegebenes eta nach Kartenwechsel.
Diese Kontrollen bestätigen Softwareeigenschaften, keine Forschungsfreigabe.

| Stufe | Festgelegtes Kriterium | Befund |
| --- | --- | --- |
{chr(10).join(gaterows)}

Der vollständige Testlauf dauerte {s['seconds']:.2f} Sekunden und erreichte
{s['peak_mib']:.1f} MiB gemessenen Spitzen-RSS; die Grenzen waren 600 Sekunden
und 2 GiB. Kein Testseed wurde ersetzt. Die ursprünglichen Kriterien wurden
nach Sichtung der Testdaten nicht verändert. Ein vollständiger numerischer
Replay ist mit `phase12/verify.py` vorgesehen; sein konkretes Ergebnis steht
in [VERIFICATION.json](phase12/VERIFICATION.json).

## Einordnung und nächster sachlicher Schritt

Der begrenzte Ankersuchraum (64 tiefste gemeinsame Anker), die harte
Balancierungsregel und kleine Schalenpopulationen sind konkrete Engpässe
dieser Implementierung. Dass der Ankerdeckel die Ursache sämtlicher Ausfälle
ist, wurde nicht isoliert nachgewiesen. Die absolute Skala nutzt bekannte
Dichte und den festen Literaturwert alpha2=1/sqrt(2), keine Anpassung an
Simulationskoordinaten. Unmarkierte kanonische Rahmen, unbekannte Intensitäten,
3+1 Dimensionen und gekrümmte Raumzeiten sind nicht validiert.

Ein nächster Vertrag sollte zuerst auf unabhängigen Entwicklungsdaten
Ankersuchabdeckung, Skalierung der Populationen und Randrobustheit verbessern,
bevor er auf frischen Testseeds erneut Metrikgenauigkeit beansprucht. Die
vorliegenden 48 Testwolken sind dafür ab jetzt bekannte Daten. Es folgt keine
Krümmungsberechnung und keine neue Behauptung über ein minimales Punktebudget.
Der frühere BD–C2-Entscheid `NO_GO_VARIABLE_CURVATURE_IN_THIS_BUDGET` und seine
Quelldaten bleiben unverändert.
'''
(HERE/'PHASE12_RESULTS.md').write_text(text)

plt.rcParams.update({'font.size':10,'axes.spines.top':False,'axes.spines.right':False})
fig,axs=plt.subplots(1,3,figsize=(13.5,4.2),layout='constrained')
for key,label,color in [('time_relative_rmse','Time distance','#3457a7'),('space_relative_rmse','Spatial distance*','#138b77')]:
    axs[0].plot(densities,[c[key]['rms'] for c in cells],'o-',label=label,color=color)
axs[0].set(title='Distance error',ylabel='Relative RMS',xlabel='Density rho',xscale='log')
axs[0].legend(frameon=False)
for key,label,color in [('operator_available','Usable stencil','#3457a7'),('oracle_signature','Correct signature','#bd6544')]:
    axs[1].plot(densities,[c[key]['fraction'] for c in cells],'o-',label=label,color=color)
axs[1].plot(densities,[c['true_cap_recall']['mean'] for c in cells],'s--',label='Mean true-cap recall',color='#138b77')
axs[1].axhline(.8,color='gray',ls=':',lw=1)
axs[1].set(title='Coverage remains inadequate',ylabel='Fraction of all clouds / cap events',xlabel='Density rho',xscale='log',ylim=(0,1))
axs[1].legend(frameon=False,fontsize=9)
axs[2].plot(densities,[c['oracle_metric_error']['rms'] for c in cells],'o-',label='Smooth coordinate fields',color='#3457a7')
axs[2].plot([densities[-1]],[high['chart_metric_error']['rms']],'s',label='Intrinsic coordinate fields',color='#bd6544')
axs[2].axhline(.5,color='gray',ls=':',label='Acceptance limit')
axs[2].set(title='Metric error on available clouds',ylabel='Relative Frobenius RMS',xlabel='Density rho',xscale='log',ylim=(0,6.5))
axs[2].legend(frameon=False,fontsize=9)
for ax in axs:
    ax.set_xticks(densities,[f'{d:,}' for d in densities]);ax.grid(alpha=.15)
fig.suptitle('BK phase 1/2: implementation tested; HOLD_PHASE3',fontsize=15)
fig.supxlabel('* Spatial errors use successfully estimated pairs. Metric samples: 2, 6, 3 smooth; 0, 0, 3 intrinsic. 16 clouds per density.',fontsize=9)
fig.savefig(PILOT/'results-overview.png',dpi=160)
plt.close(fig)
