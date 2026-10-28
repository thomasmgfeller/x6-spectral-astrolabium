"""Readable summaries; all displayed decimals are rounded, raw Arb balls govern."""
import json
from flint import ctx
from run import HERE,unpack
ctx.prec=256
d=json.loads((HERE/'results/PREDICTIONS_192.json').read_text());c=json.loads((HERE/'results/CHECKS.json').read_text())
s=d['skeleton'];o=d['original_source'];osc=d['oscillator']
def z(v):return unpack(v)
def real(v):return float(z(v).real.mid())
def number(v):return f'{real(v):.12g}'
def complex_number(v):
    a=z(v);x=float(a.real.mid());y=float(a.imag.mid())
    return f'{x:.12g} {"+" if y>=0 else "-"} {abs(y):.12g} i'
def diff(mu,other):return max(float((z(x)-z(y)).abs_upper()) for x,y in zip(mu,other))
def variance_row(label,mu,C):
    dc=max(float((z(C[i][j])-z(s['covariance'][i][j])).abs_upper()) for i in range(2) for j in range(2)) if label!='vollständig' else 0
    dm=diff(s['mean'],mu) if label!='vollständig' else 0
    return f'| {label} | {real(C[0][0]):.7g} | {real(C[1][1]):.7g} | {dc:.5g} | {dm:.5g} |'
lines=['# Ergebnisse: prädiktiver Fluktuationstransfer v0.13','',
'**Der gemeinsame Transfer ist hergeleitet und an zwei vollständig definierten Modellen geprüft. Für die ursprüngliche kompakte Quelle liegen zusätzliche rigorose Ensemble-Momentenschranken vor. Die vollständigen numerischen Ensemble-Mittelwerte und -Kovarianzen dieses ursprünglichen Detektors bleiben offen. METHOD_HOLD und G1 HOLD gelten weiter.**','',
'Alle Werte sind gerundete Anzeigen von Arb/Acb-Intervallen. Die Rohdateien enthalten die vollständigen Einschließungen. Die beiden Kontrollmodelle ersetzen weder die kompakte Quelle noch ihren räumlichen Detektor. Es wurden keine empirischen Kovarianzen angepasst und keine neuen Zufallswolken erzeugt.','',
'## 1. Vorhersage für die unveränderte kompakte Quelle','',
'Für den bisherigen lokalen H1-Adapter enthält die Quellstütze in der vorgeschriebenen History im Mittel genau 21/16 Poisson-Punkte. Mit Wahrscheinlichkeit p0=exp(-21/16) gibt es keinen solchen Punkt. Dann sind beide vollständigen Detektorantworten exakt null. Dieser gemeinsame Nullanteil ist aus der Geometrie vorhergesagt, nicht aus der Anzahl leerer Archivwolken geschätzt.','',
f'- Vorhergesagte gemeinsame Nullwahrscheinlichkeit: mindestens **{100*real(o["zero_response_probability_lower"]):.8f} %**.',
r'- Gemeinsame Kovarianzschranke: \(\Sigma\succeq[p_0/(1-p_0)]\mu\mu^*\), mit \(p_0/(1-p_0)\simeq0.368262987072\).',
r'- Gesamtfehler-Momentenmatrix: \(\Sigma+(\mu-c)(\mu-c)^*\succeq p_0cc^*\), mit der vollständigen Kontinuumsreferenz c aus v0.12.','',
'Die folgenden Untergrenzen gelten für die durch A/e normierte Originalantwort. Die letzte Spalte setzt ausdrücklich einen Mittelwertfehler von höchstens 0.001 voraus; sie ist keine unbedingte Varianzuntergrenze bei beliebigem Mittelwert.','',
'| Originalfenster | RMS-Untergrenze | SD-Untergrenze (bedingt) |','|---|---:|---:|']
for i,window in enumerate(['[3/4, 1]','[1, 5/4]']):
    # Conservatively downward-rounded displays of certified positive lower bounds.
    import math
    rms=math.floor(float(z(o['RMS_error_lower'][i]).real.lower())*1e10)/1e10
    sd=math.floor(float(z(o['SD_lower_if_mean_within_budget'][i]).real.lower())*1e10)/1e10
    lines.append(f'| {window} | {rms:.10f} | {sd:.10f} |')
lines+=['','Die Untergrenzen gelten unabhängig davon, wie genau das gleiche homogene endliche System gelöst wird. Sie gelten für den lokalen H1-Adapter; die nichtlokale Integralprojektion darf nicht mit derselben Quellverlustwahrscheinlichkeit bewertet werden.','',
'## 2. Vollständige Vorhersagen der Poisson-Transferkontrolle','',
'Die zwei Ausgangskanäle der Kontrolle stammen aus einem ausdrücklich definierten kausalen System mit vier Zuständen. Seine zufälligen Kantengewichte verwenden echte überlappende 4D-Intervalle und gemeinsame Poisson-Zählwerte. Die History ist mit diesen Gewichten korreliert. Hintergrundpunkte ändern die Zählwerte, sind aber keine weiteren Lösungszustände. Dies ist daher kein vollständiges Sprinkling des ursprünglichen CSPP-Systems.','',
'| Ausgang | Zielgröße | Realteil | Imaginärteil |','|---|---|---:|---:|']
for i in range(2):
    for name,label in [('mean','Mittelwert'),('mean_shift','Verschiebung')]:
        value=z(s[name][i]);lines.append(f'| {i+1} | {label} | {float(value.real.mid()):.12g} | {float(value.imag.mid()):.12g} |')
lines+=['','Die gemeinsame Hermitesche Kovarianz ist:','',r'\[\Sigma\simeq\begin{pmatrix}1.29534863\,10^{-4}&-4.07518006\,10^{-6}-6.28324909\,10^{-6}i\\-4.07518006\,10^{-6}+6.28324909\,10^{-6}i&2.06481262\,10^{-5}\end{pmatrix}.\]','',
'Die Relationsmatrix ist ebenfalls berechnet und von null verschieden:','',r'\[\Pi\simeq\begin{pmatrix}7.77209178\,10^{-5}+1.03627890\,10^{-4}i&-7.47170730\,10^{-6}+5.09805408\,10^{-7}i\\-7.47170730\,10^{-6}+5.09805408\,10^{-7}i&1.63842533\,10^{-5}-1.25033087\,10^{-5}i\end{pmatrix}.\]','',
'Diese Matrix darf bei einer Darstellung durch Real- und Imaginärteile nicht weggelassen werden. Der Nachweis positiver Varianzen und einer positiven Hermiteschen Determinante gelingt mit Intervallen; die Relationsmatrix ist symmetrisch.','',
'## 3. Welche Annahmen verändern die Vorhersage?','',
'Die folgende Tabelle zeigt Gegenrechnungen. Nur die Zeile mit vollständiger gemeinsamer Rechnung beschreibt das festgelegte Kontrollmodell. Entfernte Korrelationen sind Negativkontrollen, keine zulässigen Vereinfachungen.','',
'| Rechnung | Varianz 1 | Varianz 2 | max. Kovarianzfehler | max. Mittelwertfehler |','|---|---:|---:|---:|---:|',
variance_row('vollständig',s['mean'],s['covariance']),
variance_row('nur erste Variation',s['frozen_mean'],s['linear_covariance'])]
for key,label in [('independent_intervals','Intervalle unabhängig'),('omit_Palm_insertion','Palm-Einfügung fehlt'),('frozen_operator','Operator eingefroren'),('frozen_history','History eingefroren')]:
    v=s['counterfactuals'][key];lines.append(variance_row(label,v['mean'],v['covariance']))
lines+=['','Die lineare Vorhersage lässt eine tatsächliche Mittelwertverschiebung aus. Die exakte Summe endet in dieser Kontrolle nach dritter Variationsordnung. Ihre quadratischen und kubischen Beiträge werden vollständig berücksichtigt.','',
'| Rest nach erster Variation | Ausgang 1 | Ausgang 2 |','|---|---:|---:|',
'| L2-Restobergrenze (aufgerundet) | '+ ' | '.join(f'{math.ceil(float(z(v).real.upper())*1e12)/1e12:.12f}' for v in s['linear_remainder_L2_upper'])+' |','',
r'Für Mittelwert und Kovarianz gilt nachweislich \(|\Delta\mu_r|\le\delta_r\) und \(|\Delta\Sigma_{rs}|,|\Delta\Pi_{rs}|\le s_r\delta_s+s_s\delta_r+\delta_r\delta_s\). Alle Einträge erfüllen die berechneten Restgrenzen.','',
f'Das dritte zentrierte gemeinsame Gewichtsmoment von A, B und H beträgt ungefähr {number(s["third_joint_centered_moment_ABH"])} und ist eingeschlossen von null verschieden. Paarweise Momentendaten oder eine Gauß-Schließung würden diese Information verlieren.','',
'## 4. Zusätzliche lösbare Oszillatorkontrolle','',
'Der Oszillator hat omega²=1+xi/4, f=1+xi/5 und g=xi/10 mit xi=-1,+1 und jeweils Wahrscheinlichkeit 1/2. Frequenz und Anfangsdaten sind korreliert. Die Antworten sind analytische Mittel über die ganzen verschobenen Originalfenster; es werden keine Zeitpunktproben als Zeitintegral verwendet.','',
'| Fenster | Mittelwert | Eingefroren | Varianz |','|---|---:|---:|---:|']
for i,w in enumerate(osc['windows']):lines.append(f'| [{w["shifted_window"][0]}, {w["shifted_window"][1]}] | {number(w["mean"])} | {number(w["frozen_mean"])} | {number(osc["covariance"][i][i])} |')
lines += ['',f'Die Kovarianz zwischen den Fenstern beträgt {number(osc["covariance"][0][1])}. Sie folgt exakt aus der gemeinsamen Zweipunktverteilung. Die Kovarianz hat Rang eins. Die erste Variation verfehlt den Mittelwert deutlich; die zweite Ordnung erfasst die Verschiebung wesentlich besser. Für beide Ordnungen sind uniforme Volterra-Restgrenzen hergeleitet und geprüft.','',
'## 5. Reichweite der ursprünglichen Ensemblevorhersage','',
'Für die ursprüngliche lokale kompakte Quelle ist die exakte gemeinsame Pfadmomenten-Hierarchie angegeben, einschließlich identischer Knoten beider Pfade, gemeinsamer Intervalle, Palm-Einfügungen und der vollständigen Detektorfenster. Ihre Pfadlängen- und Poisson-Abschneidereste sind begrenzt:','',
'- Nach Pfadlänge 128: L2-Rest kleiner als 1.75e-48 je Detektorkanal.',
'- Nach Gesamtpunktzahl 1024: L2-Rest kleiner als 3.12e-28 je Detektorkanal.',
'- Die noch notwendigen hochdimensionalen räumlichen Integrale und ihre Quadraturfehler sind damit nicht bereits ausgewertet. Es gibt hier noch keine vollständigen numerischen Werte für die ursprünglichen Ensemble-Mittelwerte und -Kovarianzen.','',
f'Für den nichtlokalen P1-Adapter ist außerdem eine totale Ensembledefinition offen: Schon die Wahrscheinlichkeit für weniger als vier History-Knoten ist mit {number(o["nonlocal_adapter_fewer_than_four_history_points_probability"])} strikt positiv. Auf solchen Wolken fehlt der vorgeschriebene dreidimensionale Projektionsraum. Diese Zahl ist nur eine bewiesene Teilmenge möglicher Ausfälle, keine vollständige Ausfallquote. Momentengrenzen bei nahezu entarteten Geometrien fehlen ebenfalls. Ausfälle werden weder als Nullsignal eingesetzt noch aus der Stichprobe entfernt.','',
'Ein bedingtes Ensemble erfolgreicher Geometrien wäre eine gesonderte, ausdrücklich zu definierende Zielgröße. Die vollständige unbedingte PU-Vorhersage bleibt MODEL_HOLD.','',
'## 6. Prüfung und reproduzierbare Dateien','',
f'- {c["analytical_tests"]} analytische Tests bestanden.',
f'- {c["enclosed_prediction_comparisons"]} eingeschlossene Vorhersagegrößen bei 128 und 192 Bit überlappen.',
f'- Größter Komponentenradius der verglichenen exakten Kontrollgrößen: kleiner als 4.1e-27; Anzeigerundung kommt in diesem Bericht hinzu.',
f'- Unabhängige deterministische Summe über {c["count_sum_states"]:,} Zählzustände; maximale Abweichung {c["count_sum_max_abs_difference"]:.3g}.'.replace(',','.'),
'- Ausgelassene Wahrscheinlichkeit der Zählsumme kleiner als 1.07e-25; deren Gleitkommasummation wird nicht als rigoroses zweites Zertifikat ausgegeben.',
'- Keine empirisch angepassten Parameter, keine neuen Wolken und keine unabhängige Bestätigungsstichprobe.','',
'`kernel.py` implementiert die gemeinsamen Gewichtsmomente, `geometry.py` die sicheren allgemeinen Überlappungsgrenzen, `algebra.py` und `transfer.py` den zufälligen retardierten Transfer mit Restbilanz. `oscillator.py` enthält die zusätzliche Kontrolle. `run.py`, `audit.py` und `verify.py` erzeugen und prüfen alle Zahlen. Vollständige Herleitung, Annahmen, Quellen und Reproduktionsbefehle stehen in README.md.','']
(HERE/'RESULTS.md').write_text('\n'.join(lines))
