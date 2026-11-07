#!/usr/bin/env python3
"""Build the German audit report and exact-measure visualization."""
from pathlib import Path
import json
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from reportlab.pdfgen import canvas
from reportlab.platypus import SimpleDocTemplate,Paragraph,Spacer,Table,TableStyle,PageBreak,Image,KeepTogether
from reportlab.lib.styles import getSampleStyleSheet,ParagraphStyle
from reportlab.lib import colors
from reportlab.lib.enums import TA_LEFT
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.pagesizes import A4

ROOT=Path(__file__).resolve().parent
FIG=ROOT/'figures';FIG.mkdir(exist_ok=True)
OUT=ROOT/'CST_DUST_Eichstruktur_Randkonsistenz_v0_1.pdf'
FONTS=Path('/usr/share/fonts/truetype/dejavu')
for name,file in [('DejaVu','DejaVuSans.ttf'),('DejaVuBold','DejaVuSans-Bold.ttf'),('DejaVuMono','DejaVuSansMono.ttf')]:
    pdfmetrics.registerFont(TTFont(name,str(FONTS/file)))
pdfmetrics.registerFontFamily('DejaVu',normal='DejaVu',bold='DejaVuBold',italic='DejaVu',boldItalic='DejaVuBold')
NAVY=colors.HexColor('#142C3C');TEAL=colors.HexColor('#087F82');GRAY=colors.HexColor('#52616B')
LIGHT=colors.HexColor('#EDF4F5');PALE=colors.HexColor('#F5F7F9');AMBER=colors.HexColor('#835F12')
W,H=A4;WIDTH=W-88
styles={
 'body':ParagraphStyle('body',fontName='DejaVu',fontSize=10.2,leading=15.4,textColor=NAVY,spaceAfter=10),
 'small':ParagraphStyle('small',fontName='DejaVu',fontSize=8.5,leading=12.4,textColor=GRAY,spaceAfter=8),
 'title':ParagraphStyle('title',fontName='DejaVuBold',fontSize=25,leading=30,textColor=NAVY,spaceAfter=15),
 'h2':ParagraphStyle('h2',fontName='DejaVuBold',fontSize=14.2,leading=19,textColor=NAVY,spaceBefore=14,spaceAfter=9),
 'eyebrow':ParagraphStyle('eyebrow',fontName='DejaVuBold',fontSize=9,leading=12,textColor=TEAL,spaceAfter=12),
 'cell':ParagraphStyle('cell',fontName='DejaVu',fontSize=8.6,leading=12.6,textColor=NAVY),
 'cellhead':ParagraphStyle('cellhead',fontName='DejaVuBold',fontSize=8.7,leading=12.7,textColor=colors.white),
 'eq':ParagraphStyle('eq',fontName='DejaVu',fontSize=11,leading=17,textColor=NAVY,spaceAfter=0),
 'banner':ParagraphStyle('banner',fontName='DejaVuBold',fontSize=12,leading=18,textColor=TEAL),
}
story=[]
def p(text,style='body'):return Paragraph(text,styles[style])
def add(text,style='body'):story.append(p(text,style))
def eq(text):
    t=Table([[p(text,'eq')]],colWidths=[WIDTH]);t.setStyle(TableStyle([
        ('BACKGROUND',(0,0),(-1,-1),LIGHT),('BOX',(0,0),(-1,-1),0.4,colors.HexColor('#C7DCDD')),
        ('LEFTPADDING',(0,0),(-1,-1),12),('RIGHTPADDING',(0,0),(-1,-1),12),
        ('TOPPADDING',(0,0),(-1,-1),10),('BOTTOMPADDING',(0,0),(-1,-1),10)]))
    story.extend([t,Spacer(1,12)])
def table(headers,rows,widths=None):
    data=[[p(x,'cellhead') for x in headers]]+[[p(str(x),'cell') for x in row] for row in rows]
    t=Table(data,colWidths=widths or [WIDTH/len(headers)]*len(headers),hAlign='LEFT',repeatRows=1)
    t.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,0),NAVY),('VALIGN',(0,0),(-1,-1),'TOP'),
       ('ROWBACKGROUNDS',(0,1),(-1,-1),[PALE,colors.white]),('LINEBELOW',(0,0),(-1,0),.4,NAVY),
       ('LEFTPADDING',(0,0),(-1,-1),9),('RIGHTPADDING',(0,0),(-1,-1),9),
       ('TOPPADDING',(0,0),(-1,-1),9),('BOTTOMPADDING',(0,0),(-1,-1),9)]))
    story.extend([t,Spacer(1,12)])
def page(k,title,kicker):
    if story:story.append(PageBreak())
    add(f'CST-DUST / EICHSTRUKTUR v0.1 / {k:02d}','eyebrow')
    add(title,'title');add(kicker)
def footer(c,doc):
    c.saveState();c.setFillColor(TEAL);c.rect(44,H-29,WIDTH,3,fill=1,stroke=0)
    c.setStrokeColor(colors.HexColor('#CCD5DB'));c.line(44,40,W-44,40)
    c.setFont('DejaVu',7.4);c.setFillColor(GRAY)
    c.drawString(44,27,'X6 Astrolabium | 7. November 2026 | Physikalische CST-Quantendynamik: HOLD')
    c.drawRightString(W-44,27,str(doc.page));c.restoreState()

def make_figure():
    plt.rcParams.update({'font.family':'DejaVu Sans','font.size':10,'axes.spines.top':False,'axes.spines.right':False})
    x=np.linspace(-2.2,2.2,1201);tri=np.maximum(2-np.abs(x),0)/4
    fig,ax=plt.subplots(figsize=(7.4,3.7),layout='constrained')
    ax.fill_between(x,tri,color='#D8EEEE');ax.plot(x,tri,color='#087F82',lw=2.5,label='Induziertes Maß: Dreiecksverteilung')
    ax.plot([-2.2,-1,-1,1,1,2.2],[0,0,.5,.5,0,0],color='#B26835',lw=2,ls='--',label='Naive unabhängige Box')
    ax.set(xlim=(-2.2,2.2),ylim=(0,.62),xlabel='Relative Uhr r / L',ylabel='Dimensionslose Dichte L · W(r)')
    ax.legend(loc='upper center',frameon=False,fontsize=9)
    ax.grid(axis='y',alpha=.18);fig.savefig(FIG/'relative_clock_measure.png',dpi=180);plt.close(fig)

make_figure()
v=json.loads((ROOT/'results/verification.json').read_text())
quad=json.loads((ROOT/'results/quadrature_check.json').read_text())
rep=json.loads((ROOT/'results/replay.json').read_text())

page(1,'Eichstruktur und Randdaten<br/>gezielt geprüft',
     'Der endliche Staubkandidat besitzt eine konsistente gemeinsame Label- und Uhrverschiebungsstruktur. '
     'Drei naheliegende Reduktionen verändern jedoch das regulierte Modell.')
eq('<b>Endliche Kovarianz: nachgewiesen.</b><br/>Physikalische Eichquantisierung, Junction-Gesetz und globaler Bounce: weiterhin offen.')
table(['Befund','Konsequenz'],[
 ('Uhrnullpunkt gemeinsam verschoben','Wirkung, Integrationsgebiet, Randdaten und Zustand müssen gemeinsam transformiert werden.'),
 ('Referenzuhr gewählt','Das exakte Maß der Zeitdifferenzen ist korreliert; die ursprüngliche unabhängige Box ist nicht äquivalent.'),
 ('Vakuumuhr verändert','Ein innerer Knoten ohne Staub kann über nichtlokale Intervalle an spätere Materie koppeln.'),
 ('Teilgebiete getrennt zurückgesetzt','Die relative Lage ihrer Uhrnullpunkte darf bei vorhandener Kopplung nicht verloren gehen.')],[158,WIDTH-158])
add('Was die Prüfung tatsächlich umfasst','h2')
add('3 670 markierte endliche Fälle, 85 034 gemeinsame Umbenennungen und 49 992 Gebietsteilungen. '
    'Allgemeine algebraische Identitäten werden durch rationale Kontrollen und zertifizierte Amplitudenzeugen ergänzt.')
add('Aussagegrenze','h2')
add('Das Audit schließt konkrete mathematische Lücken. Es leitet keine gravitativen Constraints, Randladungen '
    'oder physikalische Quantenevolution ab. Alle acht physikalischen Entscheidungen bleiben HOLD. '
    'Der frühere Ausschluss der geprüften rohen Evolutionsinterpretation bleibt wirksam.')
add('Basis: Main nach PR 246, Commit 374acc67cb0e6. Lokaler Plan vor der Rechnung; erwartete Mechanismen '
    'vorher bekannt. Keine blinde Vorhersage, keine neuen dynamischen 4D-Ensembles, keine bezahlten Läufe.','small')

page(2,'Welche Symmetrie<br/>ist wirklich gemeint?',
     'Eine Invarianz der Wirkung ist nicht automatisch eine Eichredundanz. Ob eine Variable aus dem '
     'physikalischen Zustandsraum entfernt werden darf, benötigt zusätzliche dynamische und randbezogene Begründungen.')
table(['Transformation','Prüfergebnis / offene Grenze'],[
 ('Gemeinsame Elementumbenennung','Exakt konsistent, wenn Ordnung, Uhren, Dichtegewichte und Marken gemeinsam transformieren. Fixierte externe Daten bleiben respektiert.'),
 ('Konstante gemeinsame Uhrverschiebung','Exakte Wirkungssymmetrie. Vollständige Amplitudenkovarianz bei mitbewegtem Regulator und passenden Zuständen.'),
 ('Beliebige lokale Vakuumuhrverschiebung','Im Allgemeinen keine Symmetrie bei festem C und w. Das exakte Kriterium lautet L v = 0.'),
 ('Affine Uhrskalierung T → aT + b','Gamma skaliert mit a². Normierte, zukunftsorientierte Eigenzeit lässt bei unveränderten Einheiten keine beliebige Skalierung zu.'),
 ('Gravitative Eichtransformation','Dynamische Constraints, physikalisches Maß und Observablenalgebra bleiben herzuleiten.'),
 ('Randtransformation','Physikalische Redundanzen, Randdaten und mögliche Ladungen sind noch nicht klassifiziert.')],[163,WIDTH-163])
add('Geometrieänderung bleibt eine physikalische Variation','h2')
add('Viererkette und Viererdiamant haben bei denselben Anfangs-/Endmarken verschiedene BDG-Zähler: '
    '<b>3 und -16</b>. Das Ändern einer Kausalrelation wird durch keine gemeinsame Umbenennung aufgehoben.')
add('Die binären Dichtewerte 0 und 1 dienen als algebraische Kontrollpunkte. Weil der positive geerbte '
    'Stratum 0 &lt; w &lt; 1 ist, enthält der offengelegte Nachtrag zusätzlich explizite Zeugen bei w = 1/2.','small')

page(3,'Die Uhrbox gehört<br/>zur Kovarianzprüfung',
     'Die Wirkung hängt von Uhrdifferenzen ab. Eine feststehende Box oder eine unveränderte absolute '
     'Randpräparation kann dennoch eine zusätzliche Abhängigkeit einführen.')
eq('K<sub>μ+c</sub>(b + c·1) = K<sub>μ</sub>(b)<br/>I<sub>μ</sub> = [μ - L, μ + L]')
add('Der Beweis ist ein vollständiger Variablenwechsel mit Jacobi-Faktor eins. Er gilt auch nach endlicher '
    'Geometriesumme und Dichteintegration. Zustands- und Observableinsertionen müssen passend mittransformieren.')
table(['Zweistellenzeuge: L = 1, w = 1/2','Re K̃','Im K̃'],[
 ('b = 0, Boxmittelpunkt μ = 0','0,998438630','-0,041620187'),
 ('b = 1, μ = 1: gemeinsam verschoben','0,998438630','-0,041620187'),
 ('b = 1, μ = 0: Box festgehalten','0,975287688','-0,163714047')],[267,120,WIDTH-387])
add('Die gemeinsame Phase exp(-iw/2) ist abgetrennt. Die angezeigten Werte sind gerundet; '
    'die Ungleichheit wird mit rationalen Taylor-Restschranken zertifiziert. Es handelt sich um einen '
    'bedingten Festdichtezeugen, keine vollständige physikalische Amplitude.','small')
add('Ward-Identität einschließlich Boxfluss','h2')
eq('(∂<sub>μ</sub> + Σ<sub>a</sub> ∂<sub>bₐ</sub>) K<sub>μ</sub> = 0<br/>∂<sub>μ</sub>K ist die Summe der Integrandenflüsse an den Boxenden.')
add('Wer diese Randbeiträge weglässt, prüft eine andere Identität. Ein verbleibender Rest ist deshalb '
    'noch kein Nachweis einer gravitativen Anomalie. Eine Regulatorentfernung wird durch diese endliche Kovarianz nicht bewiesen.')
add('Zustandskontrolle','h2')
add('Eine kompakte normierte Wellenfunktion bleibt bei gemeinsamer Verschiebung von Zustand und Box normiert. '
    'Bei unveränderter Box erfasst dieselbe Beispielrechnung nur noch Norm 1/2. Dies ist ein Trägereffekt in der Hilfskonstruktion.')

page(4,'Relative Uhren brauchen<br/>das induzierte Maß',
     'Für N unabhängig gleichverteilte freie Uhren in [-L,L] sei rᵢ = Tᵢ - T₀. '
     'Die zulässige Länge des verbleibenden gemeinsamen Nullpunkts hängt von allen rᵢ ab.')
eq('W<sub>L</sub>(r) = [2L - (max(0,r) - min(0,r))]<sub>+</sub> / (2L)<super>N</super><br/>'
   '∫ W<sub>L</sub>(r) d<super>N-1</super>r = 1')
story.append(Image(str(FIG/'relative_clock_measure.png'),width=WIDTH,height=WIDTH*3.7/7.4))
story.append(Spacer(1,8))
table(['Hilfsmaß, L = 1','E[rᵢ²]','E[rᵢrⱼ], i ≠ j'],[
 ('Korrekt induziert','2/3','1/3'),
 ('Referenzuhr null, übrige Box beibehalten','1/3','0')],[267,100,WIDTH-367])
add('Die zweite Operation konditioniert eine Uhr; sie integriert den ursprünglichen Nullpunkt nicht aus. '
    'Bei N = 2 ist die korrekte Verteilung dreieckig und reicht bis ±2L. Auch die Amplitude '
    'von exp(-iwr²/4) unterscheidet sich nachweislich zwischen beiden Maßen.')
add('Das ist ein exakter Pushforward des bisherigen Hilfsmaßes. Eine physikalische Gauge-Fixierung oder '
    'Staubzeitfluktuation wird damit nicht behauptet. Festgehaltene Randuhren benötigen eine eigene Konditionierung.','small')

page(5,'Vakuum bedeutet nicht<br/>automatisch freie Uhr',
     'Eine Uhr ohne lokales Dichtegewicht kann in der Wirkungszeile eines späteren Materieelements vorkommen. '
     'Die relevante Bedingung betrifft daher die gesamte Kopplungsmatrix.')
eq('S<sub>d</sub> = -½ T<super>T</super>LT - ½ Σw<br/>'
   'S<sub>d</sub>(T + av) = S<sub>d</sub>(T) für alle T,a genau dann, wenn L v = 0.')
add('Viererkette mit innerem Vakuumknoten','h2')
add('0 ≺ 1 ≺ 2 ≺ 3, Dichtegewichte w = (0,0,1/2,0), Uhren T = (0,t,1,2). '
    'Element 1 trägt keinen Staub. Seine Uhränderung erhält in beiden Fällen die Reihenfolge.')
table(['Konfiguration','Materiewirkung S<sub>d</sub>'],[
 ('t = 1/4','103/128'),('t = 3/4','111/128'),('Änderung','1/16 ≠ 0')],[WIDTH*.64,WIDTH*.36])
add('Damit ist die unabhängige Verschiebung dieser Vakuumuhr bei festem C,w ausgeschlossen. '
    'Die Uhr am letzten Element 3 ist in diesem Beispiel hingegen eine flache Wirkungsrichtung.')
table(['Algebraische Kontrollklasse','Anzahl'],[
 ('Stellen mit w = 0','7 249'),('Davon mit nichtverschwindender Kopplungsspalte','2 541'),
 ('Davon mit verschwindender Kopplungsspalte','4 708')],[WIDTH*.77,WIDTH*.23])
add('Diese Zählwerte sind keine physikalischen Wahrscheinlichkeiten. Auch eine flache Wirkungsrichtung '
    'darf erst nach Prüfung von Maß, Randzustand und physikalischer Rolle entfernt werden. '
    'Eine gekoppelte Richtung ist umgekehrt noch kein bewiesener physikalischer Freiheitsgrad.','small')

page(6,'Beim Verkleben muss<br/>die relative Uhr erhalten bleiben',
     'Innen- und Außenbereich werden als Teilmengen derselben vollständigen Geschichte behandelt. '
     'Eine gemeinsame Verschiebung ist von einer relativen Verschiebung der Teilgebiete zu unterscheiden.')
eq('δ = c<sub>B</sub> - c<sub>A</sub>,  q = -LT<br/>'
   'ΔS<sub>d</sub> = δ Σ<sub>x∈B</sub> q<sub>x</sub> - ½ δ² · 1<sub>B</sub><super>T</super>L1<sub>B</sub>')
add('Eine unabhängige Verschiebung beider Teilgebiete ist für alle Uhrkonfigurationen nur dann '
    'Wirkungssymmetrie, wenn <b>L1<sub>B</sub> = 0</b>. Sonst wird die relative Nullpunktlage zum notwendigen Kopplungsdatum.')
table(['Geprüfte Gebietsteilungen','Anzahl'],[
 ('Geordnete nichttriviale Schnitte','49 992'),('Relative Verschiebungsrichtung gekoppelt','30 820'),
 ('Relative Verschiebungsrichtung flach','19 172')],[WIDTH*.77,WIDTH*.23])
add('Welche Aussage damit noch fehlt','h2')
add('Die Formel zeigt, warum getrenntes Zurücksetzen ohne relative Daten die Amplitude verändern kann. '
    'Sie konstruiert keine gravitative Randladung, keine CST-Edge-Modes und kein physikalisches Junction-Gesetz. '
    'Randzustände und verbleibende Redundanzen müssen im gemeinsamen Quantensystem bestimmt werden.')
add('Der bisherige Normierungsbefund bleibt bestehen','h2')
add('Der alte Zweistellenkern hängt von Uhrdifferenzen ab. Eine gemeinsame Verschiebung seiner Randlabels '
    'lässt deshalb sämtliche Matrixelemente unverändert. Das bereits nachgewiesene Hindernis für ein '
    'gemeinsames positives Evolutionsskalarprodukt wird durch Uhrnullpunkt-Kovarianz nicht beseitigt.')
add('MODEL, CURRENT, CORRESPONDENCE, BOUNCE, REGULARITY, BOUNDARY, TRAPPING und EXTENSION '
    'bleiben für diesen Audit-Record jeweils HOLD. Frühere kandidatenspezifische FAIL-Records werden nicht überschrieben.','small')

page(7,'Nachrechnung und<br/>der nächste physikalische Schritt',
     'Die algebraischen Ergebnisse sind reproduzierbar. Ihre physikalische Qualifikation bleibt eine '
     'gesonderte Aufgabe mit klar benanntem Zustands-, Maß- und Randproblem.')
table(['Kontrolle','Ergebnis'],[
 ('Markierte Fälle / gemeinsame Verschiebung','3 670 exakte Kontrollen'),
 ('Gemeinsame Umbenennungen','85 034 exakte Kontrollen'),
 ('Induziertes Maß','2 508 exakte Kontrollen'),
 ('Amplituden und Ward-Identität','24 Kontrollen je Dichtewert; w = 1 und w = 1/2'),
 ('Unabhängige numerische Quadratur',f"66 Vergleiche; maximale Abweichung {quad['max_absolute_difference']:.2e}"),
 ('Isolierte Nachrechnung','7 Ergebnisdateien bytegleich')],[WIDTH*.52,WIDTH*.48])
add('Konkretes nächstes Abnahmeziel','h2')
add('Eine physikalische Historienkonstruktion mit vollständigen relativen Randdaten und begründetem '
    'positivem Dekohärenzfunktional. Bei einer Referenzuhr ist das induzierte Maß zu erhalten; '
    'gekoppelte Vakuumuhren sind vollständig zu integrieren oder kontrolliert zu reduzieren. '
    'Ein zusätzlicher physikalischer Zeitquotient wird erst nach Begründung eingeführt.')
add('Quellen und Prüfpaket','h2')
add('Vollständige Beweise: DERIVATION.md. Ausgangscode und Vertragsstand sind unverändert archiviert. '
    'analyze.py und replay.py benötigen nur die Python-Standardbibliothek; die ergänzende Quadratur verwendet SciPy. '
    'Rationale Taylor-Schranken tragen die harten Entscheidungen, nicht die Gleitkomma-Abweichungen.','small')
for text in [
 '[1] Rideout &amp; Sorkin: klassische CST-Wachstumsdynamik und diskrete Kovarianz. <link href="https://arxiv.org/abs/gr-qc/9904062" color="#087F82">arXiv:gr-qc/9904062</link>.',
 '[2] Brown &amp; Kuchar: Staub als dynamisches Referenzsystem im Kontinuum. <link href="https://arxiv.org/abs/gr-qc/9409001" color="#087F82">arXiv:gr-qc/9409001</link>.',
 '[3] Donnelly &amp; Freidel: lokale Teilsysteme und Randfreiheitsgrade. <link href="https://arxiv.org/abs/1601.04744" color="#087F82">arXiv:1601.04744</link>. Keine fertigen CST-Randladungen.',
 '[4] Bahr &amp; Dittrich: Symmetriebruch und Wiederherstellung in diskreter Gravitation. <link href="https://arxiv.org/abs/0909.5688" color="#087F82">arXiv:0909.5688</link>. Keine Anomaliediagnose unseres Kandidaten.'
]:add(text,'small')
add('Quellenabruf: 7. November 2026. Entwicklungshinweis und nachträglich deklarierter Innenstratum-Zeuge '
    'sind im Prüfpaket offengelegt. Kein Neuheitsanspruch gegenüber der mathematischen Literatur.','small')

doc=SimpleDocTemplate(str(OUT),pagesize=A4,leftMargin=44,rightMargin=44,topMargin=53,bottomMargin=52,
                      title='CST-DUST: Eichstruktur, Uhrmaß und Randkonsistenz v0.1',author='X6 Astrolabium',
                      pageCompression=1)
doc.build(story,onFirstPage=footer,onLaterPages=footer)
print(str(OUT))
