#!/usr/bin/env python3
"""German report of eligibility, fixed tolerances and controlled reference checks."""
from pathlib import Path
import json
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.ticker import NullLocator
from reportlab.platypus import SimpleDocTemplate,Paragraph,Spacer,Table,TableStyle,PageBreak,Image
from reportlab.lib.styles import getSampleStyleSheet,ParagraphStyle
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

ROOT=Path(__file__).resolve().parent
OUT=ROOT.parent/'output/pdf';OUT.mkdir(parents=True,exist_ok=True)
FIG=ROOT/'figures';FIG.mkdir(exist_ok=True)
S=json.loads((ROOT/'results/verification.json').read_text())
plt.rcParams.update({'font.family':'DejaVu Sans','font.size':10,'axes.spines.top':False,'axes.spines.right':False})
levels=S['numerical_reference_levels']
fig,ax=plt.subplots(figsize=(7,2.9),layout='constrained')
ax.loglog([x['steps'] for x in levels],[100*x['max_relative_enclosure_error'] for x in levels],'-o',color='#187c70',lw=2)
ax.axhline(.5,color='#af6a27',ls='--',label='Numerischer Budgetanteil: 0,5 %')
ax.set(xticks=[128,256,512,1024],xticklabels=['128','256','512','1024'],
       xlabel='Euler-Zeitschritte N (keine physikalischen Dichtestufen)',ylabel='Größte Fehlerhülle [%]')
ax.set_yticks([.1,.2,.5,1],['0,1','0,2','0,5','1,0']);ax.legend(frameon=False)
ax.xaxis.set_minor_locator(NullLocator())
ax.yaxis.set_minor_locator(NullLocator())
fig.savefig(FIG/'numerical_reference.png',dpi=180);plt.close(fig)
cases=S['volume_derivative_fixed_epsilon']
fig,ax=plt.subplots(figsize=(7,2.9),layout='constrained')
xx=[r['epsilon_decimal'] for r in cases]
ax.loglog(xx,[100*r['max_H_bound'] for r in cases],'-o',color='#1d6380',label='Hubble-Rate H')
ax.loglog(xx,[100*r['max_A_bound'] for r in cases],'-o',color='#b26432',label='Beschleunigung A')
ax.axhline(5,color='#667680',ls='--',label='Gesamttoleranz 5 %')
ax.axhline(2,color='#187c70',ls=':',label='Stichprobenanteil 2 %')
ax.set(xlabel='Gemeinsamer relativer Volumenfehler ε',ylabel='Hinreichende Fehlerhülle [%]')
ax.legend(frameon=False,ncols=2,fontsize=8,loc='upper left')
fig.savefig(FIG/'derivative_sensitivity.png',dpi=180);plt.close(fig)

fd=Path('/usr/share/fonts/truetype/dejavu')
for name,file in [('DV','DejaVuSans.ttf'),('DVB','DejaVuSans-Bold.ttf'),('DVM','DejaVuSansMono.ttf')]:
    pdfmetrics.registerFont(TTFont(name,str(fd/file)))
pdfmetrics.registerFontFamily('DV',normal='DV',bold='DVB',italic='DV',boldItalic='DVB')
blue=colors.HexColor('#163d50');teal=colors.HexColor('#187c70');muted=colors.HexColor('#536570')
styles=getSampleStyleSheet()
styles.add(ParagraphStyle(name='B',fontName='DV',fontSize=9.3,leading=13.4,textColor=blue,spaceAfter=8))
styles.add(ParagraphStyle(name='S',parent=styles['B'],fontSize=8,leading=11.3,spaceAfter=6))
styles.add(ParagraphStyle(name='T',fontName='DVB',fontSize=23,leading=29,textColor=blue,spaceAfter=14))
styles.add(ParagraphStyle(name='H',fontName='DVB',fontSize=11.3,leading=15,textColor=teal,spaceBefore=7,spaceAfter=7))
styles.add(ParagraphStyle(name='E',parent=styles['B'],fontSize=10,leading=16,backColor=colors.HexColor('#edf3f5'),borderPadding=8,spaceBefore=4,spaceAfter=13))
styles.add(ParagraphStyle(name='C',parent=styles['B'],fontSize=8.1,leading=11.2,spaceAfter=0))
styles.add(ParagraphStyle(name='L',parent=styles['B'],fontName='DVB',fontSize=8.1,leading=12,textColor=teal,spaceAfter=10))
story=[]
def p(t,style='B'):story.append(Paragraph(t,styles[style]))
def h(t):p(t,'H')
def eq(t):p(t,'E')
def page(n,title):
    if story:story.append(PageBreak())
    p(f'CST-DUST · KORRESPONDENZPRÜFUNG v0.1  /  {n:02d}','L');p(title,'T')
def table(data,widths):
    t=Table([[Paragraph(str(x),styles['C']) for x in row] for row in data],colWidths=widths,repeatRows=1,hAlign='LEFT')
    t.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,0),colors.HexColor('#e6eef1')),
      ('VALIGN',(0,0),(-1,-1),'TOP'),('TOPPADDING',(0,0),(-1,-1),7),('BOTTOMPADDING',(0,0),(-1,-1),7),
      ('LEFTPADDING',(0,0),(-1,-1),7),('RIGHTPADDING',(0,0),(-1,-1),7),
      ('LINEBELOW',(0,0),(-1,0),.7,teal),('LINEBELOW',(0,1),(-1,-1),.25,colors.HexColor('#cdd8dd'))]))
    story.append(t);story.append(Spacer(1,9))
def fig(name):story.append(Image(str(FIG/name),width=504,height=209));story.append(Spacer(1,8))

page(1,'Korrespondenz vor der Singularität')
p('Vorab festgelegte Toleranzen, physikalischer Abgleich und getrennte Regularität<br/>6. November 2026 · CST-DUST-PRE-SINGULARITY-001','S')
h('Entscheidung')
eq('<b>Physikalische CST-Korrespondenz: HOLD_NOT_ELIGIBLE</b><br/>Physikalischer Test: NOT_RUN · Regularität: separat HOLD')
p('Der veröffentlichte Kandidat CST-DUST-C1 besitzt noch keinen geschlossenen gekoppelten Dynamikkern und keine vollständig unabhängigen Messadapter. Daher kann die klassische Korrespondenz derzeit nicht physikalisch bestätigt oder widerlegt werden.')
p('Ausgeführt sind die Zulassungsprüfung, eine numerische klassische Referenz mit kontrollierten Einschließungen, die Prüfung der Toleranz- und Abgleichregeln sowie eine gesonderte Messbudgetdiagnose für zeitliche Ableitungen. Der Plan wurde vor diesen neuen lokalen Rechnungen fixiert; er ist keine externe Präregistrierung.')
table([['Prüfung','Ergebnis'],
 ['Toleranzen und Abgleich','Ausführbare Regeln; 26 Positiv- und Negativkontrollen bestanden.'],
 ['Klassische Integrationsreferenz','240 Vergleiche eingeschlossen; ab N = 512 alle 60 Werte je Gitter im numerischen 0,5-%-Budget.'],
 ['Bisheriges Zählbudget für Ableitungen','Über die geprüfte konservative Schranke auf keiner der vier Stufen freigegeben.'],
 ['Eigenständige Regularität','60 gültige P3-Datensätze; physikalische CST-Gates bleiben HOLD.']],[160,344])
h('Wesentliche Erkenntnis')
p('Eine auf 5 % kalibrierte Dichte liefert noch keine 5-%-Kontrolle der Hubble-Rate oder Beschleunigung. Zeitliche Ableitungen verstärken Fehler; bei der Beschleunigung kommt die Differenz zweier Terme hinzu. Dafür wird ein eigenes Messbudget benötigt.')
p('Keine neuen Zufallsstichproben, Punktwolken, dynamischen CST-Ensembles oder kostenpflichtigen Läufe. Die klassische Bewegung wird in der Referenz eingesetzt und nicht aus CST hergeleitet.','S')

page(2,'Toleranzen und vollständiges Fehlerbudget')
p('Unverändert aus dem veröffentlichten Modellvertrag. Fehler werden durch den Betrag des Referenzwertes normiert; bei verschwindendem Randfluss dient die gesamte Anfangsmasse M als feste Skala.')
table([['Vergleich','Toleranz'],
 ['Radius R, Dichte ρ, Hubble-Rate H, Beschleunigung A = ä/a','jeweils ±5 %'],
 ['Masse und integrierter Randfluss','±2 % von M'],
 ['Anfangsgeschwindigkeit und Massenantwort','±5 %'],
 ['Differenz der beiden feinsten physikalischen Stufen','±2,5 %']],[385,119])
eq('PASS: vollständiges Fehlerintervall innerhalb der Toleranz<br/>FAIL: Fehlerintervall und Toleranzband disjunkt<br/>HOLD: Überlappung, unzureichende Breite oder fehlende Fehlerbeiträge')
table([['Fehlerbeitrag','Anteil der Toleranz','Cap beim 5-%-Test'],
 ['Stichprobe','40 %','2,00 %'],['Operator','15 %','0,75 %'],
 ['Messabbildung / Coarse map','10 %','0,50 %'],['Anfangszustand','10 %','0,50 %'],
 ['Rand und Außenraum','15 %','0,75 %'],['Numerik','10 %','0,50 %']],[240,128,136])
p('Die Caps begrenzen die Halbbreiten. Ein gemessener Bias muss zusätzlich innerhalb der Gesamtgrenze bleiben. Unbekannte Beiträge sind HOLD und werden nicht als null eingetragen. Für 2-%- und 2,5-%-Vergleiche gelten dieselben Anteile; nachträgliche Umschichtung ist nicht vorgesehen.')
h('524 geplante gleichzeitige Vergleiche')
p('240 dynamische Werte + 60 Massen + 144 Randflüsse + 12 Anfangsgeschwindigkeiten + 8 Massenantworten + 60 Differenzen der letzten Stufen. Globales α = 0,05; feste Bonferroni-Zuteilung 0,05/524 je Vergleich, ohne Unabhängigkeitsannahme.')
p('Ein geeignetes Intervallverfahren, Ensemblegrößen und statistische Aussagekraft sind damit noch nicht bestimmt. Sie benötigen das physikalische Maß und die Unsicherheitsstruktur des tatsächlich ausführbaren Kandidaten.','S')

page(3,'Physikalische Verfeinerung eindeutig abgleichen')
eq('G = c = 1,  R₀ = 10,  M ∈ {1/4; 1; 4}<br/>T<sub>end</sub> = 5√5/3,  x = T/T<sub>end</sub> ∈ {0; 1/4; 1/2; 3/4; 1}')
p('Der Zeitmaßstab ist für alle Massen identisch. Individuelles T/T<sub>s</sub>(M) würde andere physikalische Zeitpunkte vergleichen. Das Gebiet ist ein endlicher Staubball einschließlich Materieoberfläche und Außenraum; eine periodische Zelle ist kein gleichwertiger Ersatz.')
table([['Verfeinerung','Was sie verändert','Was sie nicht ersetzt'],
 ['Physikalischer Regulatorabgleich','λ/λ₀ = 1, 2, 4, 8; ℓ ∝ λ⁻¹/⁴','Keine automatische Gleichwertigkeit ohne Kopplungs- und Zustandsabgleich'],
 ['Numerische Schrittverfeinerung','Zeitschritt bei gleicher Gleichung und Geometrie','Keinen CST-Kontinuumstest'],
 ['Mehr Realisierungen','Statistische Unsicherheit','Keine geometrische Verfeinerung']],[145,179,180])
h('Unveränderte physikalische Definitionen')
p('Einheiten, G, R₀, M, gemeinsame Zeiten, Gebiets- und Randregel, Nichtlokalitätslänge L<sub>k</sub>, Mittelungslänge L<sub>cg</sub>, relationale Detektoren, Uhr, Anfangspräparation und Messkalibrierung bleiben abgeglichen. Die Oberflächen-Detektionsregel bleibt gleich; ihr Messwert wird aus Kandidatendaten gewonnen.')
p('Mikroskopische Kopplungen dürfen entlang einer vorher festgelegten Abgleichvorschrift variieren. Ein Scan einer fundamentalen physikalischen Diskretheitskonstante ist dagegen ein Modellfamilienvergleich und nicht automatisch ein Regulatorgrenzprozess.')
h('Noch nicht freigegebene Laufparameter')
p('<b>Absolute physikalische CST-Dichten, L<sub>k</sub>, L<sub>cg</sub>, Ensemblegrößen, Seeds, Kopplungsabgleich und vollständige Fehlerverfahren bleiben offen.</b> Der alte λ₀-Wert wird hier nur für eine sekundäre klassische Zählbudgetdiagnose benutzt.')
p('Der Metadatenprüfer erkennt Änderungen von Gebiet, L<sub>cg</sub>, physikalischem G, Zeitnormierung, ℓ-Skalierung und Toleranzen. Sein positives Ergebnis lautet PASS_METADATA_ONLY; ein physikalischer Abgleich ist dadurch noch nicht bewiesen.','S')

page(4,'Klassische Referenz mit Fehler-Einschließung')
eq('r = R/R₀,  u = dr/dx,  κ = M/72<br/>r′ = u,  u′ = −κ/r²,  r(0) = 1,  u(0) = −√M/6<br/>q = √M/4,  s = 1−qx,  r<sub>ref</sub> = s<super>2/3</super>')
p('Verglichen werden r, ρ/ρ₀ = r⁻³, HT<sub>end</sub> = u/r und AT<sub>end</sub>² = −κ/r³. Ein Euler-Verfahren integriert die eingesetzten klassischen Gleichungen auf vier vorher festgelegten Gittern; die analytische Lösung wird getrennt ausgewertet.')
p('Auf D = {0,6 ≤ r ≤ 1,05; −0,5 ≤ u ≤ 0} gilt L = 1 und ||y″||∞ ≤ B = 125κ/27. Für h = 1/N liefert der lokale Taylorrest die globale Zustandsgrenze:')
eq('E<sub>n</sub> = [B/(2N)] · [(1+1/N)<super>n</super>−1]')
p('Auswärts gerundete Decimal-Intervalle mit 60 Stellen kontrollieren die arithmetischen Operationen. Die analytischen Kubikwurzeln werden durch 100 exakte rationale Bisektionsschritte eingeschlossen. Alle numerischen Iterierten liegen im erklärten Gebiet D.')
fig('numerical_reference.png')
table([['N','Im numerischen 0,5-%-Cap','Größte Fehlerhülle'],
 ['128','54 / 60','1,033346 %'],['256','58 / 60','0,519993 %'],
 ['512','60 / 60','0,260835 %'],['1024','60 / 60','0,130628 %']],[76,243,185])
p('Alle 240 analytischen Referenzwerte sind eingeschlossen. Auch die 60 Differenzkontrollen der letzten beiden numerischen Stufen liegen innerhalb von 2,5 %. Diese N-Verfeinerung ist ausdrücklich kein physikalischer λ-Test.','S')

page(5,'Zeitliche Ableitungen brauchen präzisere Messungen')
p('Die sekundäre Diagnose verwendet das ganze Kugelvolumen und die bereits kalibrierten symmetrischen Zeitfenster. Exposition und Zähldichte werden dabei als exakt bekannt eingesetzt. Auf dem gemeinsamen Raster Δx = 1/4 werden Dreipunktdifferenzen verwendet: innen zentriert, an den Endpunkten einseitig.')
eq('H<sub>diff</sub>T<sub>end</sub> = D₁V/(3V)<br/>A<sub>diff</sub>T<sub>end</sub>² = D₂V/(3V) − (2/9)(D₁V/V)²')
p('Für die klassische Referenz ist V/V₀ = (1−qx)² quadratisch. Deshalb haben diese Differenzen dort keinen Zeitdiskretisierungsbias. Für allgemeine CST-Verläufe ist dieser Bias zusätzlich zu begrenzen; eine vorausgesetzte quadratische Kurve wäre kein unabhängiger Dynamiktest.')
fig('derivative_sensitivity.png')
table([['Relative Volumenfehlergrenze ε','H-Fehlerhülle','A-Fehlerhülle'],
 ['10⁻⁴','0,620687 %','62,7067 %'],['10⁻⁵','0,0620631 %','6,26872 %'],
 ['5 · 10⁻⁶','0,0310314 %','3,13430 %'],['10⁻⁶','0,00620626 %','0,626852 %']],[236,134,134])
p('Die Fehlerhüllen stammen aus exakten rationalen Sensitivitätsrechnungen für sechs vorab bestimmte ε-Werte. ε = 5 · 10⁻⁶ genügt über diese Hülle für die volle 5-%-Toleranz, aber noch nicht für das zugeteilte 2-%-Stichprobencap; ε = 10⁻⁶ genügt auch dafür.')
p('<b>Die Hüllen sind hinreichende obere Abschätzungen, keine gemessenen Fehler oder notwendigen Mindestfehler.</b> Sie nutzen keine günstige Kovarianz. Direkte Messgrößen oder bessere Zeitreihenverfahren können andere Anforderungen haben.','S')

page(6,'Bisheriges Zählbudget: keine Ableitungsfreigabe')
p('Für die gesonderte Diagnose werden 60 ganze Kugelzeitfenster betrachtet. Aus der Poisson-Momentenerzeugenden und einer Vereinigungsabschätzung folgt bei J = 60 und α = 0,05 eine hinreichende gemeinsame Volumenfehlergrenze. Fensterkorrelationen müssen hierfür nicht als unabhängig behandelt werden.')
eq('P(|N/µ−1| &gt; ε) ≤ 2 exp[−µε² / (2(1+ε/3))]<br/>L = log(2J/α)<br/>ε<sub>suff</sub> = [L/3 + √(L²/9 + 2µL)] / µ')
table([['λ/λ₀','Kleinstes µ','ε<sub>suff</sub>','A-Fehlerhülle'],
 ['1','40 000','1,9792 %','13 285 %'],['2','80 000','1,3982 %','9 198 %'],
 ['4','160 000','0,9880 %','6 408 %'],['8','320 000','0,6983 %','4 484 %']],[70,112,137,185])
p('Auf der feinsten alten Zähldichtestufe beträgt die H-Fehlerhülle zusätzlich rund 43,64 %. <b>Keine Stufe erhält über diese konservative Ableitungsprüfung eine Freigabe.</b> Das widerlegt weder den früheren Dichtebefund noch den Erfolg eines verbesserten Schätzers.')
h('Ressourcenprognose dieser hinreichenden Methode')
table([['Ziel-ε','Erwartete Punkte je vollem innerem Weltrohr','Einordnung'],
 ['5 · 10⁻⁶','1,32 · 10¹³ bis 1,99 · 10¹³','5-%-Hülle, aber 2-%-Stichprobencap noch verfehlt'],
 ['10⁻⁶','3,29 · 10¹⁴ bis 4,97 · 10¹⁴','Hülle liegt auch im Stichprobencap']],[76,238,190])
p('Dies sind keine ausgeführten Läufe und keine unteren Komplexitätsschranken. Die Diagnose begründet keine Erhöhung des tatsächlichen Rechenbudgets. Sinnvoller zu prüfen sind direkte Rate-/Beschleunigungsobservablen oder ein unabhängig kalibrierter Zeitreihenadapter mit Kovarianz und kontrolliertem Glättungsbias.')
p('Die Sensitivitätsrechnung bei festem ε ist rational exakt. Logarithmen, Poisson-Ressourcenwerte und die abgebildeten Zahlen werden mit Gleitkommaarithmetik ausgewertet; dafür wird kein zusätzliches Intervallzertifikat behauptet. Das 60er-Diagnosebudget ist von der geplanten 524er-CST-Testfamilie getrennt.','S')

page(7,'Eigenständige Regularität an jedem Prüfpunkt')
h('Was die eingesetzte klassische Referenz beweist')
eq('s = 1−qx ≥ 1/2<br/>(ρ/ρ₀)² = s⁻⁴ ≤ 16<br/>K<sub>innen</sub>/K₀ = 60s⁻⁴ ≤ 960<br/>K<sub>außen</sub>/K₀ ≤ 48s⁻⁴ ≤ 768<br/>K₀ = (GM/R₀³)²')
p('Diese Schranken gelten für das ganze erklärte klassische Zeitfenster und die einseitigen Oberflächengrenzen. Die klassische Metrik enthält λ nicht. Damit ist keine aus einem physikalischen CST-Verfeinerungsprozess gewonnene Momentschranke bewiesen. Der spätere klassische Singularitätszeitpunkt liegt außerhalb des Fensters.')
h('60 getrennte P3-Bewertungen')
p('Für jede geplante Kombination aus vier Dichtestufen, drei Massen und fünf Zeitpunkten wird die Regularitätsentscheidung erneut eingetragen. Das unveränderte Eltern-Gate bestätigt die formale Gültigkeit aller 60 Akten. Physikalische Ausführung: NOT_RUN.')
table([['Physikalisches Gate','Entscheidung'],
 ['Modell / Strom / Korrespondenz','HOLD / HOLD / HOLD'],
 ['Bounce / Regularität','HOLD / HOLD'],
 ['Innen-Rand-Außenraum / Trapping / Fortsetzung','HOLD / HOLD / HOLD']],[366,138])
p('Offen bleiben die physikalischen Dichte- und Krümmungsoperatoren, ihre Domänen und ihr Maß, gemeinsame Momentenschranken, Tails, uniforme Integrierbarkeit und kontrollierte Konvergenz. Kleine numerische Fehler oder ein Volumenminimum können diese Pflichten nicht ersetzen.')
h('Negativkontrollen schützen vor falschen Freigaben')
p('26 Kontrollen umfassen überlappende Intervalle, fehlende Unsicherheiten, nachträgliche Budgetverschiebung, falschen physikalischen Abgleich und Referenzdaten mit perfekter Übereinstimmung. Auch solche Referenzdaten dürfen keine CST-Freigabe erzeugen. Eine um 20 % veränderte Anfangsbeschleunigung wird in allen drei Massenfällen verworfen.','S')

page(8,'Nächster Freigabeschritt und Nachrechnung')
h('Was vor einem physischen Bestätigungslauf fehlt')
table([['Pflicht','Offener Inhalt'],
 ['D1-D4','Geschlossener Historienträger, diskretes Materiegesetz und Maß, Geometriewirkung mit Randtermen, Zustand und Komposition.'],
 ['D5','Messgrößen aus eigenen Kandidatendaten: Strom, Geometrie, Uhr, Oberfläche, H und A; kontrollierte Messabbildung und Historiengewichte.'],
 ['D6','Dynamischer Innen-/Rand-/Außenraumabgleich und Fehler durch die äußere Abschneidung.'],
 ['D7','Tatsächliche Dichten, Skalen, Ensemblegrößen, Seeds, Unsicherheitsverfahren, Aussagekraft und erreichbares Budget.']],[76,428])
p('Der entscheidende nächste Schritt ist ein ausführbarer gekoppelter Kandidat mit unabhängigen Messadaptern. Insbesondere darf die klassische Bewegungsgleichung nicht zur Rekonstruktion von H oder A benutzt werden, wenn gerade ihre Emergenz getestet werden soll.')
p('Nach Schließen dieser Pflichten werden die fehlenden Laufparameter vor frischen Daten fixiert. Erst dann kann die geplante Familie von 524 Vergleichen die physikalische Korrespondenz prüfen. Ein endlicher PASS wäre weiterhin kein Kontinuumssatz und keine globale Singularitätsauflösung.')
h('Reproduzierbares Prüf-Paket')
p('<font name="DVM">python3 -B run.py</font> reproduziert Referenz, Fehlerhüllen, Negativkontrollen und P3-Akten. Python-Standardbibliothek für die Intervall- und Rationalrechnung; NumPy/SciPy nur als Abhängigkeiten des unveränderten früheren Expositionsmoduls. Auch <font name="DVM">python3 -O -B run.py</font> führt die Kontrollen aus.','S')
p('<b>plan.json / plan.sha256:</b> eingefrorener lokaler Plan. <b>DERIVATION.md:</b> vollständige Beweise und Geltungsgrenzen. <b>intervals.py / acceptance.py:</b> Rechen- und Entscheidungsregeln. <b>results/:</b> vollständige Tabellen und Akten. <b>inputs/:</b> unveränderte Elternquellen. <b>SHA256SUMS:</b> Inhaltsintegrität.','S')
h('Projektquellen und Kontinuumsbezug')
p('[1] <link href="https://github.com/thomasmgfeller/x6-spectral-astrolabium/pull/239" color="#187c70">CST-DUST Model Contract v0.1, PR #239</link>.<br/>[2] <link href="https://github.com/thomasmgfeller/x6-spectral-astrolabium/pull/240" color="#187c70">Staubstrom-Kalibrierung v0.1, PR #240</link>, Main eabb4ece77563b049caa3a30bacd7b75b850d3a8.<br/>[3] Brown und Kuchař, <i>Dust as a Standard of Space and Time in Canonical Quantum Gravity</i>, <link href="https://arxiv.org/abs/gr-qc/9409001" color="#187c70">arXiv:gr-qc/9409001</link>, <link href="https://doi.org/10.1103/PhysRevD.51.5600" color="#187c70">Phys. Rev. D 51, 5600</link>.','S')
p('Die Kontinuumsquelle begründet nicht die noch offene diskrete Materiedynamik. Euler-Einschließung, Sensitivitäts- und Poisson-Schranken sind im Prüf-Paket direkt hergeleitet.','S')

def decorate(canvas,doc):
    canvas.saveState();w,h=A4
    canvas.setStrokeColor(colors.HexColor('#d6e0e4'));canvas.line(44,h-33,w-44,h-33)
    canvas.setFont('DV',7);canvas.setFillColor(muted)
    canvas.drawString(44,24,'CST-DUST · Physikalischer Test HOLD / NOT_RUN · 06.11.2026')
    canvas.drawRightString(w-44,24,str(doc.page));canvas.restoreState()

target=OUT/'CST_DUST_Korrespondenz_v0_1.pdf'
SimpleDocTemplate(str(target),pagesize=A4,rightMargin=44,leftMargin=44,topMargin=49,bottomMargin=43,
    title='CST-DUST: Korrespondenz vor der Singularität v0.1',author='CST-DUST Forschungsprogramm',
    subject='Zulassung, feste Toleranzen, physikalischer Abgleich und klassische Referenzkontrollen').build(story,onFirstPage=decorate,onLaterPages=decorate)
print(target)
