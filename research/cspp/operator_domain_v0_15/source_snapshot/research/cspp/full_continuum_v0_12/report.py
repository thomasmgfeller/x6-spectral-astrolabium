"""Human-readable summary; authoritative bounds are the archived ball intervals."""
import json
from decimal import Decimal, ROUND_FLOOR, ROUND_CEILING
from flint import ctx
from run import HERE,gzread,unpack

ctx.prec=256
d=gzread(HERE/'results/BENCHMARK_192.json.gz')
c=json.loads((HERE/'results/CHECKS.json').read_text())
f=json.loads((HERE/'results/FOURIER_DIAGNOSTIC.json').read_text())

def scalar(x):return float(unpack(x).real.mid())
def upper(x):return float(unpack(x).real.upper())
def lower(x):return float(unpack(x).real.lower())
def outward(x,up):
    if x==0:return '0'
    v=Decimal.from_float(x);unit=Decimal(1).scaleb(v.adjusted()-2)
    return f'{v.quantize(unit,rounding=ROUND_CEILING if up else ROUND_FLOOR):.2E}'
def bounds(m,k):
    p=m['components'][k]['magnitude']
    return '['+outward(lower(p['lower']),False)+', '+outward(upper(p['upper']),True)+']'
def total(m):return f"{upper(m['total_magnitude']['upper']):.6f}"

lines=['# Ergebnisse: vollständige skalare Kontinuumsreferenz v0.12','',
'**Referenz abgeschlossen; METHOD_HOLD und G1 HOLD bleiben bestehen.**','',
'Die neue Referenz integriert den ganzen bisherigen Detektorball und die ganzen beiden Zeitfenster. Das Zeitintegral wird exakt als Differenz des Sine-Propagators an den Fenstergrenzen berechnet. Die räumliche Reduktion und alle Restgrenzen stehen in README.md. Der Code verwendet keine diskreten Kausalsetantworten zur Konstruktion der Referenz.','',
'## 1. Kontinuumsantwort und Referenzfehler','',
'Die folgende komplexe Antwort ist durch die bisherige Feldskala F0=A/e geteilt. Sie ist ein linearer Feldmittelwert, keine Intensität. Die Tabellenmitten sind auf 24 Nachkommastellen gerundet; der jeweils genannte gemeinsame Radius gilt separat für Real- und Imaginärteil und schließt diese Anzeigerundung ein.','',
'| Zeitfenster | Realteil | Imaginärteil | Radius je Komponente |',
'|---|---:|---:|---:|',
'| [3/4, 1] | -0.020732687086922060979949 | +0.001678303092685356509942 | 4.9e-22 |',
'| [1, 5/4] | -0.005907886606641349247619 | +0.006495610877105028863749 | 3.2e-22 |','',
'Unskaliert, einschließlich der Unsicherheit der L2-Normierung A:','',
'| Zeitfenster | Realteil | Imaginärteil | Radius je Komponente |',
'|---|---:|---:|---:|',
'| [3/4, 1] | -0.069588630157516998691090 | +0.005633173004514621729117 | 1.7e-21 |',
'| [1, 5/4] | -0.019829640719433989552519 | +0.021802319259385140507689 | 1.1e-21 |','',
'Die folgenden nach oben gerundeten Schranken beziehen sich auf die normierte Antwort. Ein komplexer Fehlerbetrag wird zur sicheren Einschließung auf beide Komponenten übertragen.','',
'| Referenzbeitrag | Fenster 1 | Fenster 2 |', '|---|---:|---:|']
for key,label in [('quadrature_and_arithmetic_radius','Quadratur plus Intervallarithmetik (Komponentenradius)'),('source_tail_upper','Abgeschnittener Quellenrand (Betrag)'),('bessel_tail_upper','Rest der Bessel-Reihe (Betrag)')]:
    lines.append('| '+label+' | '+' | '.join(outward(upper(w[key]),True) for w in d['reference']['windows'])+' |')
lines+=['| Zusätzliche zeitliche Quadratur | 0 | 0 |','| Ausgelassener Detektorrand | 0 | 0 |','',
'Die Referenztoleranz 1e-12 ist in beiden Fenstern erfüllt. Quellenrand und Reihenrest werden analytisch begrenzt; sie werden nicht aus der Differenz zweier Auflösungen geschätzt.','',
'## 2. Getrennte Bilanz der diskreten Rechnung','',
'Für jede vorhandene Wolke, jedes Fenster und beide Adapter wird dieselbe signierte Identität geprüft:','',
r'\[a_{\rm num}-\mathcal C=E_A+E_O+E_I+E_S.\]','',
'- EA: ideale Adapterhistory gegenüber der exakten KG-History, bis zum Detektor übertragen.',
'- EO: diskreter Operator und endliches Gebiet bei exakter KG-History gegenüber der vollen Kontinuumsantwort.',
'- EI: Anfangsdatenintegration/-rundung plus Detektorkubatur; beide Teilbeiträge bleiben in den Rohdaten einzeln verfügbar.',
'- ES: Koeffizientenrundung, endlicher Dreieckssolve und abschließende Gleitkommasummation.','',
'Die bis zum Detektor fortgepflanzte Zertifikatsunsicherheit der KG-Kontrollhistory beträgt höchstens 1.7e-23. Sie ist in den Beitragsintervallen eingeschlossen und erklärt deren Größenordnung nicht.','',
'Die Kontrollhistory ist kein neuer Adapter und wird nicht in die eigentliche Modellrechnung eingesetzt. Operator und Gebiet werden gemeinsam bilanziert; ihre weitere Trennung ist noch offen. Die idealen PU-Koeffizienten und ihre numerischen Repräsentanten dürfen nicht gleichgesetzt werden.','',
'Die nächste Tabelle gibt je Fenster und Methode die größte Betragsobergrenze unter den acht Wolken an (nach oben gerundet). Das sind konservative Obergrenzen einzelner Beiträge, keine positiven Fehlernachweise und keine unabhängigen Varianzen.','',
'| Fenster | Adapter | EA | EO | EI | ES |','|---|---|---:|---:|---:|---:|']
for wi in range(2):
    for mi,label in enumerate(['lokal H1','nichtlokal PU H1']):
        models=[r['windows'][wi]['models'][mi] for r in d['rows']]
        vals=[outward(max(upper(m['components'][k]['magnitude']['upper']) for m in models),True) for k in ['adapter','operator_domain','integration','solution']]
        lines.append(f'| {wi+1} | {label} | '+' | '.join(vals)+' |')
lines+=['','Bei der nichtlokalen Projektion sind EA und der Anfangsdatenanteil von EI korreliert. Ihre breiten Intervalle lassen derzeit keine eindeutige Attribution zu. Sie belegen weder einen so großen tatsächlichen Projektionsfehler noch eine Verschlechterung gegenüber dem lokalen Adapter. Der direkte Gesamtfehler der ausdrücklich festgelegten numerischen Realisierung bleibt trotzdem eng eingeschlossen.','',
'## 3. Woher kommt die Abweichung?','',
'Ein Beitrag gilt nur dann als dominant, wenn seine Betragsuntergrenze die Summe aller anderen Betragsobergrenzen übersteigt. In der folgenden Tabelle bezeichnet O diesen Nachweis für EO, ein Fragezeichen eine unentschiedene Zuordnung. Die EO-Intervalle sind für beide Adapter gleich. Gesamtfehlerbeträge sind gerundete Anzeigen der engen Intervalle.','',
'| Wolke | Fenster | Betrag EO: untere/obere Grenze | Gesamt lokal | Ursache lokal | Gesamt PU |','|---|---:|---:|---:|:---:|---:|']
for row in d['rows']:
    for wi,w in enumerate(row['windows']):
        local,pu=w['models']
        cause='O' if local['dominant_component']=='operator_domain' else '?'
        lines.append(f"| {row['key']} | {wi+1} | {bounds(local,'operator_domain')} | {total(local)} | {cause} | {total(pu)} |")
lines+=['','Bei der nichtlokalen PU-History bleibt die Ursache in allen 16 Fällen unentschieden. Die lokale Zuordnung ist in d0_r02/Fenster 2 und d0_r07/Fenster 2 unentschieden.','',
'**Belastbarer Befund:** Mit exakter Kontinuumshistory liegt der Operator-/Gebietsbeitrag in allen 16 Wolken-Fenster-Fällen nachweislich über 1e-3. Beim lokalen H1-Adapter dominiert er in 14/16 Fällen nach dem strengen Kriterium. Die maximale Lösungsfehlerschranke liegt unter 6.3e-18. Eine genauere Lösung des gleichen endlichen Systems würde diese Abweichung daher nicht beseitigen.','',
'Alle 32 festgelegten numerischen Realisierungen überschreiten die Gesamtvergleichstoleranz 1e-3. Dies ist eine Aussage über diese deklarierten numerischen Realisierungen, nicht über jede mögliche genaue Realisierung der noch breit eingeschlossenen idealen PU-Projektion.','',
'Für die drei Wolken d0_r01, d0_r04 und d0_r06 löscht der lokale H1-Adapter die Quelle weiterhin exakt aus. Seine numerische Antwort ist null; Integrations- und Lösungsfehler sind dort exakt null. Die Gesamtfehlerbeträge sind dann etwa 0.0208005052 und 0.0087804376. Die nichtlokale Konstruktion ändert diesen geometrischen Befund nicht rückwirkend.','',
'## 4. Prüfstatus und verbleibende Arbeit','',
f"- {c['analytical_tests']} analytische Kontrollen bestanden; {c['enclosed_target_comparisons']} Intervalle derselben Zielgrößen bei 128 und 192 Bit überlappen.",
f"- {c['signed_ledgers_checked']} signierte Fehlerbilanzen geprüft, verteilt auf zwei Präzisionsläufe.",
f"- {c['oracle_history_nodes_per_precision']} zertifizierte KG-Historywerte je Präzision; alle bisherigen Koordinaten- und Kausalzählwerte unverändert.",
'- Keine zusätzlichen Zufallswolken, Kausalsetknoten, angepassten Quellen oder geänderten Detektorfenster.',
'- Eine unabhängige Fourier-Diagnose bestätigt die Zahlen bis ungefähr 2.3e-13. Deren Fourier-Abschneidung ist nicht zertifiziert; sie ist nur eine zusätzliche Kontrolle.','',
'Abgeschlossen ist die volle skalare Kontinuumsreferenz für diese kompakte massive Quelle und diese zwei Fenster. Offen bleiben eine ausreichend enge nichtlokale Projektionsintegration, die getrennte Untersuchung von Operator und Gebietsrand, die Genauigkeitsqualifikation der Adapterhistory sowie G1 und die weitergehende physikalische Interpretation. Die acht Archivwolken sind Entwicklungsfälle, keine unabhängige Bestätigungsstichprobe.','',
'`continuum.py` enthält die unabhängige Referenz, `run.py` die Bilanz, `verify.py` die Ausgabekontrolle. `PROTOCOL.json` und `FREEZE.json` halten Parameter, Datenidentität und lokalen Methodenstand fest. Die vollständigen signierten Intervalle stehen in den beiden komprimierten Benchmarkdateien; `CHECKS.json` enthält die maschinenlesbaren Entscheidungen. Die Reproduktionsbefehle und die vollständige Herleitung stehen in README.md.','']
(HERE/'RESULTS.md').write_text('\n'.join(lines))
