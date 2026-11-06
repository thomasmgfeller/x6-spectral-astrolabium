#!/usr/bin/env python3
"""Build the German research report from archived calibration outputs."""
import csv, json, math
from pathlib import Path
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, Image
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
from reportlab.lib.enums import TA_LEFT
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.pagesizes import A4

ROOT=Path(__file__).resolve().parent
OUT=ROOT.parent/'output/pdf';OUT.mkdir(parents=True,exist_ok=True)
FIG=ROOT/'figures';FIG.mkdir(exist_ok=True)
S=json.loads((ROOT/'results/verification.json').read_text())
def rows(name):return list(csv.DictReader((ROOT/'results'/name).open()))
levels=S['poisson']['levels']
plt.rcParams.update({'font.family':'DejaVu Sans','font.size':10,'axes.spines.top':False,'axes.spines.right':False})
fig,ax=plt.subplots(figsize=(7.0,3.2),layout='constrained')
x=np.arange(4);ys=[r['joint_pass_probability_lower'] for r in levels]
ax.bar(x,ys,color=['#a7b2bc','#a7b2bc','#218878','#218878'],width=.6)
ax.axhline(.95,color='#a65d20',ls='--',lw=1.3,label='Freigabeschwelle 95 %')
for xx,y,lab in zip(x,ys,['0¹','0¹','98,1203 %','99,9999723 %']):
    ax.text(xx,max(.03,y+.035),lab,ha='center',fontsize=10)
ax.set(xticks=x,xticklabels=['1 λ₀','2 λ₀','4 λ₀','8 λ₀'],ylim=(0,1.19),
       ylabel='Untere Wahrscheinlichkeitsschranke',xlabel='Zähldichte bei unveränderten physikalischen Detektoren')
ax.set_yticks([0,.25,.5,.75,1],['0 %','25 %','50 %','75 %','100 %'])
ax.legend(loc='upper left',frameon=False)
fig.savefig(FIG/'precision_probability.png',dpi=180);plt.close(fig)

bc=rows('boundary_mask.csv');ref=rows('reference_cells.csv')
fig,axs=plt.subplots(1,2,figsize=(7.0,3.0),layout='constrained')
for m in [.25,1,4]:
    rr=[r for r in bc if float(r['M'])==m]
    axs[0].plot([float(r['T']) for r in rr],[float(r['full_to_bulk_ratio']) for r in rr],marker='o',label=f'M = {m:g}')
axs[0].set(xlabel='Eigenzeit T',ylabel='Volle Randdichte / Bulk-Dichte',ylim=(.45,.49))
axs[0].legend(frameon=False,fontsize=8)
for mult,color in [((1,1),'#1e6075'),((1,2),'#b55d35'),((2,1),'#218878')]:
    rr=[r for r in ref if float(r['M'])==4 and r['probe']=='whole' and
        int(r['past_multiplier'])==mult[0] and int(r['future_multiplier'])==mult[1]]
    axs[1].plot([float(r['T']) for r in rr],[100*(float(r['F_time'])-1) for r in rr],marker='o',label=str(mult))
axs[1].axhline(0,color='#9ba4ab',lw=.7)
axs[1].set(xlabel='Eigenzeit T, M = 4',ylabel='Naiver Volumenbias [%]')
axs[1].legend(title='Fenster (vor, nach)',frameon=False,fontsize=8,title_fontsize=8)
fig.savefig(FIG/'boundary_and_window.png',dpi=180);plt.close(fig)

fontdir=Path('/usr/share/fonts/truetype/dejavu')
pdfmetrics.registerFont(TTFont('DV',str(fontdir/'DejaVuSans.ttf')))
pdfmetrics.registerFont(TTFont('DVB',str(fontdir/'DejaVuSans-Bold.ttf')))
pdfmetrics.registerFont(TTFont('DVM',str(fontdir/'DejaVuSansMono.ttf')))
pdfmetrics.registerFontFamily('DV',normal='DV',bold='DVB',italic='DV',boldItalic='DVB')
blue=colors.HexColor('#163d50');teal=colors.HexColor('#187c70');grey=colors.HexColor('#52636e')
styles=getSampleStyleSheet()
styles.add(ParagraphStyle(name='BodyX',fontName='DV',fontSize=9.4,leading=13.5,textColor=blue,spaceAfter=8))
styles.add(ParagraphStyle(name='SmallX',parent=styles['BodyX'],fontSize=8.1,leading=11.4,spaceAfter=5))
styles.add(ParagraphStyle(name='TitleX',fontName='DVB',fontSize=27,leading=32,textColor=blue,spaceAfter=15))
styles.add(ParagraphStyle(name='H1X',fontName='DVB',fontSize=20,leading=25,textColor=blue,spaceAfter=15))
styles.add(ParagraphStyle(name='H2X',fontName='DVB',fontSize=11.5,leading=16,textColor=teal,spaceBefore=7,spaceAfter=7))
styles.add(ParagraphStyle(name='EqX',fontName='DV',fontSize=10.2,leading=16,backColor=colors.HexColor('#edf3f5'),borderPadding=8,spaceBefore=5,spaceAfter=14))
styles.add(ParagraphStyle(name='CellX',parent=styles['BodyX'],fontSize=8.3,leading=11.2,spaceAfter=0))
styles.add(ParagraphStyle(name='LabelX',parent=styles['BodyX'],fontName='DVB',fontSize=8.5,leading=12,textColor=teal,spaceAfter=10))
story=[]
def p(text,style='BodyX'):story.append(Paragraph(text,styles[style]))
def h(text):p(text,'H2X')
def eq(text):p(text,'EqX')
def page(n,title):
    if story:story.append(PageBreak())
    p(f'CST-DUST · PRÜFBERICHT v0.1  /  {n:02d}','LabelX');p(title,'H1X')
def table(data,widths):
    cells=[[Paragraph(str(x),styles['CellX']) for x in row] for row in data]
    t=Table(cells,colWidths=widths,repeatRows=1,hAlign='LEFT')
    t.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,0),colors.HexColor('#e5eef0')),
        ('VALIGN',(0,0),(-1,-1),'TOP'),('TOPPADDING',(0,0),(-1,-1),7),('BOTTOMPADDING',(0,0),(-1,-1),7),
        ('LEFTPADDING',(0,0),(-1,-1),7),('RIGHTPADDING',(0,0),(-1,-1),7),
        ('LINEBELOW',(0,0),(-1,0),.7,teal),('LINEBELOW',(0,1),(-1,-1),.25,colors.HexColor('#cfd8dc'))]))
    story.append(t);story.append(Spacer(1,10))
def fig(name,height):story.append(Image(str(FIG/name),width=504,height=height));story.append(Spacer(1,8))

page(1,'Staubstrom und Messgrößen')
p('Definition und Kalibrierung','TitleX')
p('6. November 2026 · CST-DUST-CURRENT-CAL-001<br/>Auf Grundlage des veröffentlichten CST-DUST Model Contract v0.1','SmallX')
h('Ergebnis')
p('Ein konservativer, mit Materiemarken versehener Strom ist definiert. Schnittmasse, seitlicher Massenfluss, räumliches Volumen und gemittelte Dichte sind an der festgelegten <b>endlichen klassischen Staubball-Referenz</b> kalibriert. Oberfläche und ein in den Vakuumaußenraum reichender Detektor sind ausdrücklich enthalten.')
p('Die Kalibrierung ist bedingt: Bewegung, Geometrie, Uhren, Materiemarken und Zähldichte werden als bekannt eingesetzt. Ihre Erzeugung durch den gekoppelten CST-Kandidaten ist weiterhin offen.')
table([['Prüfebene','Ergebnis'],
 ['Konservativer markierter Strom','Exakte Bilanz- und Coarse-graining-Identitäten; 86 Kontrollen bestanden.'],
 ['Masse und Fluss','420 Massen- und 144 Flussfälle innerhalb analytischer Quadraturgrenzen.'],
 ['Volumen und Dichte','Referenz-Zählplan ab 4 λ₀ für das erklärte 5-%-Präzisionsziel qualifiziert.'],
 ['Physikalischer CST-Strom','HOLD: keine aus dem gekoppelten Kern erzeugten Ströme.'],
 ['Regularität / Singularitätsauflösung','Eigene Entscheidung: CST weiterhin HOLD.']],[154,350])
h('Was tatsächlich gerechnet wurde')
p('Deterministische radiale Materiequadratur, analytische Volumenintegrale, Poisson-Wahrscheinlichkeiten und Überlappungskovarianzen. <b>Keine neuen Zufallsstichproben und keine neuen dynamischen CST-Ensembles.</b> Der Zählplan wurde lokal vor diesen Rechnungen fixiert; dies ist keine externe Präregistrierung.')
p('Vollständige Definitionen, Herleitungen, Quelltexte, Rohwerte und Prüfsummen stehen im begleitenden Prüfpaket. Die hier berichteten numerischen Wahrscheinlichkeiten beruhen auf Gleitkommaauswertung exakter Formeln.','SmallX')

page(2,'Ein Strom mit erklärten Materiemarken')
h('Kontinuumsgröße und diskrete Entsprechung')
eq('J<super>a</super> = ρ u<super>a</super>,  u<super>a</super>u<sub>a</sub> = −1,  T<super>ab</super> = ρ u<super>a</super>u<super>b</super><br/>Q<sub>Σ</sub> = −∫<sub>Σ</sub> J<super>a</super>n<sub>a</sub> dΣ')
p('ρ ist die Ruhemassendichte; Q ist die von einem Schnitt gemessene Masse. Nur bei n = u ist Q unmittelbar das räumliche Integral von ρ. Diese Bedingung erfüllt der gewählte Referenzschnitt im Staubinneren.')
p('Auf einer endlichen kausalen Ordnung C werden vorwärtsgerichtete Transportkanten E und nichtnegative Marken f<sub>xy</sub> angegeben. Jede Marke trägt <b>integrierte Masse</b>, nicht Masse pro Zeit. Zusätzliche Kausalrelationen erzeugen für sich keine Materie.')
eq('d<sub>x</sub> = Σ<sub>y</sub> f<sub>xy</sub> − Σ<sub>y</sub> f<sub>yx</sub> = s<sub>x</sub><br/>Σ<sub>(x,y)</sub> f<sub>xy</sub>(φ<sub>y</sub> − φ<sub>x</sub>) = −Σ<sub>x</sub> φ<sub>x</sub>d<sub>x</sub>')
p('s<sub>x</sub> deklariert Quellen und Senken an den zeitlichen Ein- und Austritten; im Bulk gilt s<sub>x</sub> = 0. In der Summe über eine Ereignismenge heben sich innere Kanten paarweise auf. Es bleibt genau ausgehender minus eingehender Fluss: die diskrete Gaussidentität.')
h('Schnittmasse und Coarse graining')
p('Für eine Vergangenheitsmenge P ist Q(P) die Summe der f-Markierungen über ihren zukunftsseitigen Schnitt. Zwei geschachtelte Schnitte ohne dazwischenliegende Quellen haben dieselbe Masse. Bei einer kompatiblen Blockpartition werden die Flüsse zwischen Blöcken addiert; innere Flüsse verschwinden. Für Schnitte aus ganzen Blöcken bleibt Q exakt erhalten. Partitionen mit zyklischem Quotienten werden abgewiesen.')
h('Welche Physik dadurch noch nicht feststeht')
p('Derselbe Kausalgraph erlaubt f und 2f; bei gleicher Gesamtmasse sind unterschiedliche Zweigströme möglich. Die Ordnung bestimmt daher weder Masse noch lokale Stromverteilung. Auch konservative Gegenströme können Druck tragen: Für zwei gleich starke Ströme mit ±v ist T<super>xx</super>/ρ<sub>rest,total</sub> = v²/(1−v²) &gt; 0.')
p('<b>Einströmigkeit, Druckfreiheit, geodätische Bewegung und Rückwirkung benötigen zusätzliche dynamische Begründung.</b> Die Stromdefinition allein ist ein kinematischer Baustein.','SmallX')

page(3,'Referenz mit Innenraum, Oberfläche und Vakuum')
eq('G = c = 1,  R₀ = 10,  M ∈ {0,25; 1; 4}<br/>T<sub>s</sub> = (2/3)√[R₀³/(2GM)],  R<sub>b</sub>(T) = R₀(1−T/T<sub>s</sub>)<super>2/3</super><br/>0 ≤ T ≤ T<sub>end</sub> = ½ min T<sub>s</sub> = 3,7267799625')
p('Die Referenz besitzt einen homogenen flachen Staubinnenraum und einen Schwarzschild-Außenraum mit derselben Masse. Die mitbewegende Materieoberfläche trägt keine zusätzliche dünne Schicht. Es gibt keine periodische Identifikation.')
p('Die Volumendictionary ist die marginal gebundene Painlevé–Gullstrand-Fortsetzung der Oberflächeneigenzeit: ds² = −dT² + (dR−v dT)² + R²dΩ², mit v = HR innen und v = −√(2GM/R) außen. An der Oberfläche stimmen beide Werte überein. Die T-Schnitte sind räumlich flach; dV₄ = R² sinθ dT dR dθ dφ.')
table([['Detektor','Radialbereich','Bedeutung'],
 ['whole','0 … R<sub>b</sub>','gesamter Staubball'],
 ['core','0 … 0,5 R<sub>b</sub>','zentrale Region'],
 ['bulk','0,5 R<sub>b</sub> … 0,8 R<sub>b</sub>','innere Schale'],
 ['rim','0,8 R<sub>b</sub> … R<sub>b</sub>','materialseitiger Rand'],
 ['fixed_R4','0 … 4','durchströmter fester Arealradius'],
 ['surface_material','R<sub>b</sub>−0,5 … R<sub>b</sub>','bekannte Materialmaske'],
 ['surface_total','R<sub>b</sub>−0,5 … R<sub>b</sub>+0,5','Material und Vakuum']],[113,170,221])
h('Auflösung ist nicht Änderung der Messgröße')
p('Die Randbreite w = 0,5 und die physikalischen Detektorregionen an jedem T bleiben bei Zählverfeinerung unverändert. Mitbewegende Regionen schrumpfen während des Kollapses. Dies sind räumlich gemittelte Observablen, kein Nachweis punktweiser Dichtekonvergenz.')
p('Einheiten bei c = 1: Q und f in M; ρ und J in M/L³; V₃ in L³; Ω₄ in L⁴; λ in L⁻⁴; A in L; K in L⁻⁴. λ bezeichnet die Zähldichte und darf nicht mit der Materiedichte ρ verwechselt werden. Keine SI- oder Planckskalierung wurde gemessen.','SmallX')

page(4,'Masse und durchströmte Grenzen')
h('Radiale Materiequadratur')
eq('s<sub>i</sub> = (i+½)/P,  χ<sub>i</sub> = s<sub>i</sub><super>1/3</super>,  m<sub>i</sub> = M/P<br/>P ∈ {64; 256; 1024; 4096}<br/>|Q̂−Q| ≤ M/P;  |Φ̂−Φ| ≤ 2M/P')
p('Die Marker repräsentieren gleich schwere radiale Massenzellen und folgen der eingesetzten klassischen Mitbewegung. An jedem Intervallende beträgt der kumulative Mittelpunktfehler höchstens 1/(2P); für ein radiales Intervall folgt die Massenschranke M/P. Zwei Zeitpunkte liefern die konservative Flussschranke 2M/P. Die Masse der ganzen Kugel ist exakt M.')
h('Vorzeichen und Bilanz')
eq('Q(T₂) − Q(T₁) + Φ<sub>out</sub> = 0<br/>dΦ<sub>out</sub>/dT = 4πR<sub>D</sub>²ρ(HR<sub>D</sub>−dR<sub>D</sub>/dT)<br/>= −3Mχ<sub>D</sub>² dχ<sub>D</sub>/dT')
table([['Weltrohr','Erwarteter Fluss','Geprüftes Verhalten'],
 ['χ<sub>D</sub> = 1','null','mitbewegende Materieoberfläche'],
 ['R<sub>D</sub> = 4','negativ','Einstrom bei Kollaps'],
 ['χ<sub>D</sub> = 0,8−0,2T/T<sub>end</sub>','positiv','schrumpfender Detektor lässt Materie austreten']],[176,100,228])
p('Alle drei Wände sind im Fenster zeitartig. Die Flüsse werden zusätzlich unabhängig aus der Kontinuumsrate integriert. 420 Massenfälle und 144 Flussfälle erfüllen die Grenzen; der diskrete Bilanzrest ist null.')
table([['P = 4096; jeweils relativ zur Gesamtmasse M','Masse','Fluss'],
 ['Größter beobachteter Fehler','0,011868 %','0,012516 %'],
 ['Analytische obere Fehlerschranke','0,024414 %','0,048828 %']],[316,94,94])
p('Die Schranken beziehen sich auf M, nicht auf die kleinere Detektormasse. Die Bilanz wird durch dieselben transportierten Marken gewährleistet. Sie beweist Konsistenz der Darstellung, aber keine aus CST zurückgewonnene Staubbewegung. Es wurde keine vierdimensionale Punktwolke oder Winkelquadratur erzeugt.','SmallX')

page(5,'Volumen benötigt eine Zeitfensterkorrektur')
eq('N ∼ Poisson(λΩ₄),  Ω₄ = ∫ V<sub>D</sub>(T) dT<br/>A = Ω₄/V<sub>D</sub>(T<sub>c</sub>),  V̂ = N/(λA)<br/>E[V̂] = V<sub>D</sub>(T<sub>c</sub>),  Var(V̂) = V²/µ,  µ = λΩ₄')
p('<b>N/λ zählt Vierervolumen.</b> Für räumliches Volumen ist der Faktor A nötig. Die Fenster haben Vergangenheit/Zukunft-Multiplikatoren (1,1), (1,2), (2,1) von 0,1T<sub>end</sub> und werden am gemeinsamen Zeitbereich abgeschnitten. Die tatsächlich verbleibenden Grenzen gehen in die Integration ein.')
p('Für mitbewegendes V ∝ (T<sub>s</sub>−T)² gilt mit d = T<sub>s</sub>−T<sub>c</sub>:')
eq('F = A/ΔT = 1 − (h₊−h₋)/d + (h₊²−h₊h₋+h₋²)/(3d²)')
p('Der naive Schätzer N/(λΔT) besitzt relativen Mittelwertfehler F−1. Dessen Betrag erreicht im Plan <b>21,3333 %</b>. Randdetektoren fester physikalischer Breite benötigen ihr eigenes Integral; die Mitbewegungsformel ist dort nicht allgemein gültig.')
fig('boundary_and_window.png',216)
p('<b>Links:</b> Der ganze Randdetektor enthält Vakuum und misst nur 46,04–47,50 % der Bulk-Dichte. Dies ist eine andere Messgröße, kein zufälliger Schätzfehler. Die bekannte materialseitige Maske reproduziert in der Referenz die Bulk-Dichte. <b>Rechts:</b> Zeitfensterasymmetrie und Abschneidung erzeugen den unkorrigierten Volumenbias.','SmallX')
p('315 analytische Expositionen stimmen mit unabhängiger adaptiver Quadratur relativ bis 5,33·10⁻¹⁵ überein; weitere 1575 Mittelpunktvergleiche dokumentieren numerische Verfeinerung. Ein späterer CST-Test muss A, Uhr und Oberfläche unabhängig bestimmen. Eine aus der gesuchten Referenz berechnete Korrektur ist keine unabhängige Vorhersage.','SmallX')

page(6,'Dichte, Nullzählungen und Fehlerbudget')
h('Intervalle statt unkontrollierter Kehrwerte')
p('Für jeden Zählwert verwenden wir ein zentrales Garwood-Intervall [µ<sub>L</sub>, µ<sub>U</sub>] mit α* = 0,05/1260. Die Grenzen folgen aus Chi-Quadrat-Quantilen [3, 4]. Mit der deterministischen Massenschranke ergibt sich:')
eq('V<sub>L,U</sub> = µ<sub>L,U</sub>/(λA)<br/>ρ ∈ [Q<sub>L</sub>/V<sub>U</sub>, Q<sub>U</sub>/V<sub>L</sub>]')
p('Bonferroni sichert für alle 1260 Zählintervalle mindestens 95 % gleichzeitige Überdeckung. Dafür wird keine Unabhängigkeit benötigt. Diese Überdeckung ist von der Wahrscheinlichkeit zu unterscheiden, dass die Intervalle auch eng genug für das 5-%-Präzisionsziel sind.')
h('N = 0 bleibt sichtbar')
p('Bei N = 0 ist V<sub>L</sub> = 0. Für positive mögliche Masse wird die obere Dichtegrenze unendlich: <b>HOLD_ZERO_COUNT</b>. Es wird kein Pseudocount addiert. Für jedes endliche µ bleibt P(N=0) = exp(−µ) &gt; 0. Ein bei null als unendlich fortgesetzter Kehrwert hat daher keine endlichen positiven Momente.')
p('Das ist eine Grenze des Zähladapters. Sie besteht auch bei vollständig regulärer klassischer Geometrie und darf nicht mit einer physikalischen Singularität gleichgesetzt werden.')
h('Überlappende Messungen sind korreliert')
eq('Cov(N<sub>A</sub>,N<sub>B</sub>) = λ Vol₄(A ∩ B)')
p('Zwölf 6×6-Matrizen für überlappende whole/core-Fenster erfüllen Diagonal- und Positivitätskontrollen. Bei der geprüften Fensterdifferenz würde eine falsche Unabhängigkeitsannahme die Varianz um den Faktor 1,4945–1,4998 überschätzen. Das ersetzt keine dynamische Kovarianz der Materie- oder Geometriemarken.')
h('Kalibriergrenzen gehören in das Gesamtbudget')
eq('V ∈ [µ<sub>L</sub>/(λ<sub>U</sub>A<sub>U</sub>), µ<sub>U</sub>/(λ<sub>L</sub>A<sub>L</sub>)]')
p('Der implementierte Adapter propagiert deterministische Unsicherheit auf λ und A. Eine Zusatzkontrolle mit ±1 % auf λ und ±2 % auf A verbreitert Volumen- und Dichteintervalle. Das 5-%-Ziel wird für diese erweiterten Grenzen hier nicht neu freigegeben. Statistische Kalibrierintervalle benötigen ein eigenes Fehlerbudget.','SmallX')

page(7,'Ergebnis der Zählverfeinerung')
p('Vorab fixiert: 3 Massen × 5 Zeiten × 3 Fenster × 7 Detektoren = 315 Fälle je Stufe. Die vier Stufen liefern 1260 Zählintervalle. λ₀ = 92,894688446 L⁻⁴ ergibt im kleinsten Detektorfenster einen Erwartungswert von 5000; die Materiequadratur bleibt bei P = 4096.')
p('<b>Präzisionsziel:</b> Alle Volumen- und Dichteintervalle einer Stufe liegen vollständig innerhalb ±5 % ihres jeweiligen Referenzwertes. Die Erfolgswahrscheinlichkeit wird aus Poisson-Schwänzen berechnet. Eine Vereinigungsabschätzung liefert die gemeinsame untere Schranke.')
fig('precision_probability.png',230.4)
p('¹ Eine untere Schranke von null bedeutet nicht, dass die tatsächliche gemeinsame Erfolgswahrscheinlichkeit exakt null ist. Die unkorrektierte Kontrollrechnung erhält auf keiner Stufe eine positive gemeinsame Untergrenze.','SmallX')
table([['λ/λ₀','min µ','Untergrenze Präzisionserfolg','Referenzentscheidung'],
 ['1','5 000','0','HOLD'],['2','10 000','0','HOLD'],
 ['4','20 000','0,9812029663','PASS, bedingt'],
 ['8','40 000','0,9999997228','PASS, bedingt']],[55,74,192,183])
p('Die kleinste numerisch ausgewertete Einzelüberdeckung beträgt 0,99996032098 und erfüllt 1−α*. Diese Formelprüfung erzeugt keine gemessene Trefferquote. Die Zahlen sind nicht durch Intervallarithmetik zertifiziert.','SmallX')
p('Ressourcenprognose für ein vollständiges zeitliches Innenweltrohr je Masse: bei 4λ₀ etwa 3,38–5,11 Millionen Punkte, bei 8λ₀ etwa 6,77–10,21 Millionen. Solche Punktwolken wurden nicht erzeugt. Kausalrelationen, zusätzlicher Außenraum und dynamische Historien können wesentlich teurer sein.','SmallX')

page(8,'Regularität erhält eine eigene Entscheidung')
h('Bedingte Aussage über die klassische Referenz')
p('Die eingesetzte Geometrie ist im gesamten festen Zeitfenster einschließlich beider Seiten der Materieoberfläche kontrolliert. Die Schranken folgen direkt aus R<sub>b</sub>(T) und den klassischen Krümmungsinvarianten:')
table([['Größe','Schranke im gemeinsamen Fenster'],
 ['Oberflächenradius R<sub>b</sub>','≥ 6,29960525'],
 ['Materiedichte ρ','≤ 0,003819718635'],
 ['K<sub>innen</sub> = 60G²M²/R<sub>b</sub>⁶','≤ 0,01536'],
 ['K<sub>außen</sub> = 48G²M²/R⁶, R ≥ R<sub>b</sub>','≤ 0,012288']],[277,227])
p('Der endliche Dichtesprung an der Oberfläche führt in dieser Referenz zu einem endlichen Krümmungssprung, ohne zusätzliche Delta-Materieschicht. Vakuumdichte null bedeutet keine verschwindende Krümmung. Diese Aussage reicht nicht bis T → T<sub>s</sub> und beweist keine Fortsetzung durch den Kollapsendpunkt.')
h('Physikalischer CST-Prüfpunkt P2')
table([['Gate','Entscheidung'],
 ['MODEL / CURRENT / CORRESPONDENCE','HOLD / HOLD / HOLD'],
 ['BOUNCE / REGULARITY','HOLD / HOLD'],
 ['BOUNDARY / TRAPPING / EXTENSION','HOLD / HOLD / HOLD']],[365,139])
p('Der Datensatz wird mit dem unveränderten Gate-Programm des Elternvertrags geprüft: <b>record_valid = true</b>. Das bestätigt formale Vollständigkeit der Bewertung, keinen physikalischen Beweis. Die bedingten Referenz-PASS werden gesondert geführt.')
p('Für CST fehlen weiterhin physikalische Dichte- und Krümmungsoperatoren mit Domänen und Maß, uniforme Momentenschranken, kontrollierte Tails sowie ein physikalisch abgeglichener Grenzprozess. Ein kleines Bilanzresiduum oder ein endliches Volumenmittel darf diese Anforderungen nicht ersetzen.')
p('Es folgt keine neue Aussage über Horizonte, Schwarze Löcher oder Singularitätsauflösung. Ein „Fenster vor der Singularität“ behauptet auch nicht, dass darin keine gefangenen Flächen auftreten können.','SmallX')

page(9,'Reproduzierbarkeit und Anschluss an den Vertrag')
h('Was als Nächstes tatsächlich fehlt')
p('Der gekoppelte Kandidat muss Materiemarken f, Uhr, Oberflächenmaske und Exposition erzeugen, ohne die zu prüfenden Referenzwerte einzusetzen. Erst mit unabhängig bestimmtem Bias-, Varianz-, Auflösungs- und Gebietsbudget ist ein physikalischer Korrespondenztest freigabefähig. Druckfreiheit und Einströmigkeit bleiben zusätzliche Anforderungen.')
p('Die bekannte endliche Referenz ersetzt keinen dynamischen CST-Randnachweis. Kausale Beziehungen und Wirkungsbeiträge über die Materieoberfläche, Anschlussgesetz, äußerer Gebietsfehler und Coarse-Fibre-Gewichte bleiben offen. Die früheren geglätteten BD-Paarstromschätzer besitzen eine andere Definition; ihre bisherigen Entscheidungen werden durch diese Arbeit nicht geändert.')
h('Prüfpaket')
table([['Datei / Bereich','Inhalt'],
 ['DERIVATION.md','Definitionen, Identitäten, Schranken und vollständige Quellen'],
 ['plan.json / plan.sha256','Unveränderte lokale Planversion'],
 ['current.py / observables.py','Markierter Strom und Messadapter'],
 ['calibrate.py','Reproduktion der Referenzrechnungen'],
 ['audit_checkpoint.py','Systematikadapter und Vertragsprüfung P2'],
 ['results/','Vollständige CSV-Werte und getrennte Entscheidungen'],
 ['inputs/ / SHA256SUMS','Elternvertrag, Herkunft und Integritätsprüfung']],[185,319])
p('Ausführung mit Python, NumPy und SciPy: <font name="DVM">python3 calibrate.py</font>, danach <font name="DVM">python3 audit_checkpoint.py</font>. Die ausgeführten Versionsstände stehen im Manifest. Bericht und Figuren lassen sich mit <font name="DVM">build_report.py</font> sowie Matplotlib und ReportLab neu erzeugen.','SmallX')
h('Primärquellen und Projektbezug')
p('[1] <link href="https://github.com/thomasmgfeller/x6-spectral-astrolabium/pull/239" color="#187c70">CST-DUST Model Contract v0.1, PR #239</link>, Main 0e47038f15d93edef486fbb68da5dad6bf017221.<br/>[2] Brown &amp; Kuchař, <i>Dust as a Standard of Space and Time in Canonical Quantum Gravity</i>, <link href="https://arxiv.org/abs/gr-qc/9409001" color="#187c70">arXiv:gr-qc/9409001</link>.<br/>[3] Garwood, <i>Fiducial Limits for the Poisson Distribution</i>, Biometrika 28 (1936), 437–442, <link href="https://doi.org/10.1093/biomet/28.3-4.437" color="#187c70">doi:10.1093/biomet/28.3-4.437</link>.<br/>[4] Krishnamoorthy, Xia &amp; Xie (2011), <i>A Simple Approximate Procedure for Constructing Binomial and Poisson Tolerance Intervals</i>, <link href="https://userweb.ucs.louisiana.edu/~kxk4695/2011-Xia-Xie-CS.pdf" color="#187c70">Autorenfassung</link>; hier nur die explizite Garwood-Formel.','SmallX')
p('Die endlichen Graphidentitäten, Expositionsformeln und Quadraturgrenzen werden im Paket unmittelbar hergeleitet. Die Literatur begründet keine dynamische Qualifikation der vorgeschlagenen CST-Materiemarken.','SmallX')

def decorate(canvas,doc):
    canvas.saveState();w,h=A4
    canvas.setStrokeColor(colors.HexColor('#d6e0e4'));canvas.line(44,h-33,w-44,h-33)
    canvas.setFont('DV',7);canvas.setFillColor(grey)
    canvas.drawString(44,24,'CST-DUST · Bedingte Referenzkalibrierung · 06.11.2026')
    canvas.drawRightString(w-44,24,str(doc.page));canvas.restoreState()

target=OUT/'CST_DUST_Staubstrom_Kalibrierung_v0_1.pdf'
doc=SimpleDocTemplate(str(target),pagesize=A4,rightMargin=44,leftMargin=44,topMargin=49,bottomMargin=43,
    title='CST-DUST: Staubstrom und Messgrößen v0.1',author='CST-DUST Forschungsprogramm',
    subject='Definition und bedingte Kalibrierung am endlichen klassischen Staubball')
doc.build(story,onFirstPage=decorate,onLaterPages=decorate)
print(target)
