#!/usr/bin/env python3
from pathlib import Path
from fractions import Fraction as F
import json
import math
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from reportlab.pdfgen import canvas
from reportlab.lib.colors import HexColor, white
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import Paragraph, Table, TableStyle
from reportlab.lib.styles import ParagraphStyle

ROOT=Path(__file__).resolve().parent
OUT=ROOT/'report';OUT.mkdir(exist_ok=True)
FONT=Path('/usr/share/fonts/truetype/dejavu')
for name,file in [('DejaVu','DejaVuSans.ttf'),('DejaVuBold','DejaVuSans-Bold.ttf'),('DejaVuMono','DejaVuSansMono.ttf')]:
    pdfmetrics.registerFont(TTFont(name,str(FONT/file)))
pdfmetrics.registerFontFamily('DejaVu',normal='DejaVu',bold='DejaVuBold',italic='DejaVu',boldItalic='DejaVuBold')
INK='#132B3A'; MUTED='#526775'; TEAL='#007D7A'; PALE='#EDF5F4'; ORANGE='#B34B28'
plt.rcParams.update({'font.family':'DejaVu Sans','font.size':10,'axes.spines.top':False,'axes.spines.right':False})
fig,ax=plt.subplots(figsize=(8,3.2),layout='constrained')
for g,color,label in [(0,TEAL,'g = 0: bis Faktor 5'),(.5,'#5B82A4','g = 1/2: unter Faktor 9'),(1,ORANGE,'g = 1: linear'),(1.25,'#7C355A','g = 5/4: exponentiell')]:
    xs=list(range(1,25)); ys=[]
    for n in xs:
        sm=lambda k:sum(abs(g)**j for j in range(k))
        ys.append(max(2*sm(n),1+4*sm(n-1)))
    ax.plot(xs,ys,color=color,lw=2,label=label)
ax.set_yscale('log');ax.set_xlabel('Anzahl kausaler Zellen N (keine physikalische Zeit)')
ax.set_ylabel('Exakte maximale Fehlerverstärkung')
ax.grid(axis='y',alpha=.18);ax.legend(frameon=False,fontsize=9,loc='upper left')
fig.savefig(OUT/'cancellation_cells.png',dpi=180);plt.close(fig)

styles={
 'body':ParagraphStyle('body',fontName='DejaVu',fontSize=10.2,leading=15,textColor=HexColor(INK)),
 'small':ParagraphStyle('small',fontName='DejaVu',fontSize=8.5,leading=12.2,textColor=HexColor(MUTED)),
 'h2':ParagraphStyle('h2',fontName='DejaVuBold',fontSize=15,leading=20,textColor=HexColor(INK)),
 'eq':ParagraphStyle('eq',fontName='DejaVuMono',fontSize=10.7,leading=16,textColor=HexColor(INK)),
 'table':ParagraphStyle('table',fontName='DejaVu',fontSize=9.2,leading=13,textColor=HexColor(INK)),
 'white':ParagraphStyle('white',fontName='DejaVuBold',fontSize=9,leading=13,textColor=white),
}
W,H=595.28,841.89; M=48; CW=W-2*M
pdf=OUT/'Stabilitaet_Pfadkriterium_v0_26.pdf'
c=canvas.Canvas(str(pdf),pagesize=(W,H),invariant=1)
c.setTitle('CSPP v0.26 - Grenze universeller Stabilität und Pfadkriterium')
c.setAuthor('CSPP Forschungsnotiz')
y=0; page=0

def text(txt,style='body',gap=10):
    global y
    p=Paragraph(txt,styles[style]);_,h=p.wrap(CW,900)
    assert y-h>55,(page,txt[:60],y,h)
    p.drawOn(c,M,y-h);y-=h+gap

def title(kicker,heading):
    global y,page
    page+=1;y=H-55
    c.setFillColor(HexColor(TEAL));c.setFont('DejaVuBold',8.5)
    c.drawString(M,y,'CSPP / EIGENZEIT  ·  FORSCHUNGSNOTIZ 0.26  ·  31.10.2026')
    y-=39
    c.setFillColor(HexColor(MUTED));c.setFont('DejaVuBold',9);c.drawString(M,y,kicker)
    y-=14
    p=Paragraph(heading,ParagraphStyle('title',fontName='DejaVuBold',fontSize=25,leading=30,textColor=HexColor(INK)))
    _,h=p.wrap(CW,160);p.drawOn(c,M,y-h);y-=h+22

def footer():
    c.setStrokeColor(HexColor('#DCE5E8'));c.line(M,44,W-M,44)
    c.setFillColor(HexColor(MUTED));c.setFont('DejaVu',7.3)
    c.drawString(M,30,'CSPP v0.26 · analytischer Worst-Case-Befund · METHOD / G1: HOLD')
    c.drawRightString(W-M,30,str(page));c.showPage()

def box(txt):
    global y
    p=Paragraph(txt,styles['eq']);_,h=p.wrap(CW-26,160)
    c.setFillColor(HexColor(PALE));c.roundRect(M,y-h-22,CW,h+22,7,fill=1,stroke=0)
    p.drawOn(c,M+13,y-h-11);y-=h+35

def table(rows,widths):
    global y
    data=[[Paragraph(str(z),styles['white'] if i==0 else styles['table']) for z in row] for i,row in enumerate(rows)]
    t=Table(data,colWidths=widths,hAlign='LEFT')
    t.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,0),HexColor(INK)),('VALIGN',(0,0),(-1,-1),'TOP'),
                          ('LEFTPADDING',(0,0),(-1,-1),9),('RIGHTPADDING',(0,0),(-1,-1),9),
                          ('TOPPADDING',(0,0),(-1,-1),8),('BOTTOMPADDING',(0,0),(-1,-1),8),
                          ('ROWBACKGROUNDS',(0,1),(-1,-1),[HexColor('#F1F5F6'),white])]))
    _,h=t.wrap(CW,900);assert y-h>55;t.drawOn(c,M,y-h);y-=h+17

title('01 / ERGEBNIS','Eine universelle Schranke<br/>ist zu viel verlangt')
text('<b>Der nächste Schritt liefert einen begrenzten Unmöglichkeitssatz.</b> Nichttriviale Intervallkerne besitzen keine endliche deterministische Maximumsnorm-Schranke über alle endlichen Kausalsets. Eine konkrete Gegenfamilie erreicht beliebig grosse Verstärkung.')
box('‖(I − K)<super>−1</super>‖∞ = 1 + M |α|')
text('M unvergleichbare Vorgänger wirken mit demselben nichtverschwindenden Gewicht α auf einen Endpunkt. Die Formel ist die <b>erreichbare exakte Norm</b>, keine grobe obere Fehlerschranke. Im konstruierten System gilt sogar K² = 0.')
text('Beim bisherigen Kandidaten θ = 21:',gap=6)
box('α = 0,13522340238702773549704987529158493…')
table([['Vorgänger M','Maximale Fehlerverstärkung'],['10','2,352234'],['100','14,522340'],['1.000','136,223402']], [165,CW-165])
text('<b>Geltungsbereich:</b> unverändert angewandte, realisierungsunabhängige Intervallgewichte und beliebige punktweise begrenzte Gleichungsfehler. Die Gegenfamilie ist in Minkowski-Raum realisierbar. Der Ausschluss umfasst alle nichtsingulären Parameter der v0.25-Familie.')
text('Die Konstruktion zeigt räumliche Bündelung vieler Beiträge, nicht exponentielles Wachstum auf langen Wegen. Sie beweist weder typische zeitliche Instabilität noch einen Fehler des festgelegten KG-Detektors. Die positive physikalische Stabilitätsfrage bleibt offen.','small')
footer()

title('02 / BEWEIS UND QUANTOREN','Warum die Gegenfamilie<br/>den Test entscheidet')
text('<b>1. Erste wirksame Schicht wählen.</b> Sei r der kleinste Index mit t(r) ≠ 0. Zwischen jeden der M unvergleichbaren Vorgänger und den Endpunkt wird dieselbe Kette aus r Punkten gesetzt. Für r = 0 entfällt die Kette.')
text('<b>2. Alle Übertragungen auswerten.</b> Jeder Vorgänger-Endpunkt-Abstand enthält genau r Intervallpunkte. Alle anderen vergleichbaren Paare enthalten weniger als r Punkte und haben daher Gewicht null. Es verbleiben genau M Einträge mit α = t(r).')
text('<b>3. Die Schranke erreichen.</b> K² = 0 liefert R = I + K. Die Endzeile hat absolute Summe 1 + M|α|. Passende Eingabevorzeichen erreichen diese Summe. M ist beliebig: Eine endliche uniforme Konstante existiert nicht.')
text('Der Sonderfall ist geschlossen','h2',gap=8)
text('In v0.25 ist t(0) nur bei θ = −8/9 null. Dort gilt c₁ = 20/3 und t(1) ≠ 0. Der Fächer mit einem Zwischenpunkt liefert denselben Ausschluss. Weitere feste Schichten beseitigen dieses Hindernis nicht: Entscheidend ist jeweils die erste nichtverschwindende Schicht.')
text('Auch Poisson bedeutet nicht „jede Realisierung“','h2',gap=8)
text('Die Punkte können streng raumartig beziehungsweise zeitartig angeordnet werden. Kleine offene Umgebungen erhalten die Ordnung. Genau ein Poisson-Punkt je Umgebung und kein weiterer im beschränkten Gebiet hat für jedes endliche M positive Wahrscheinlichkeit [2].')
box('Für jedes endliche L: P(‖R‖∞ > L) > 0.')
text('Das gilt schon bei fester positiver Dichte und festem geeignetem Gebiet. Zugleich ist ‖R‖ auf jeder endlichen Realisierung endlich. <b>Wesentlich unbeschränkt ist nicht dasselbe wie unendlich auf einer Realisierung.</b> Die Zeugen können extrem selten sein; eine hohe typische Verstärkung folgt nicht.')
text('Offen bleiben Hochwahrscheinlichkeitsschranken, Momentabschätzungen und andere physikalisch begründete Normen. Eine punktweise begrenzte Störung hat bei wachsender Punktzahl nicht automatisch begrenzte Gesamtenergie.','small')
footer()

title('03 / POSITIVER MECHANISMUS','Pfade zuerst zusammenfassen,<br/>danach ihre Grösse begrenzen')
text('Interne Variablen e werden exakt eliminiert. Für die verbleibenden Variablen b entsteht der Transfer L. Er enthält direkte Pfade und alle Wege durch interne Punkte mit ihren Vorzeichen.')
box('Rₑ = (I − Kₑₑ)<super>−1</super><br/>L = K<sub>bb</sub> + K<sub>be</sub> Rₑ K<sub>eb</sub>')
text('Gelten uniform ‖Rₑ‖ ≤ Cₑ, ‖RₑK<sub>eb</sub>‖ ≤ U, ‖K<sub>be</sub>Rₑ‖ ≤ V und ‖L‖ ≤ r &lt; 1, dann gilt mit C<sub>b</sub> = (1 + V)/(1 − r):',gap=6)
box('‖R‖ ≤ max{C<sub>b</sub>, Cₑ + U C<sub>b</sub>}')
text('<b>Exakte Kontrollfamilie:</b> xₙ = fₓ,ₙ + 2yₙ₋₁ und yₙ = fᵧ,ₙ + xₙ + (−2 + g)yₙ₋₁. Nach Elimination bleibt der Gesamtbeitrag g statt der getrennten Pfadbeträge 2 und |−2 + g|.')
c.drawImage(str(OUT/'cancellation_cells.png'),M,y-200,width=CW,height=200,mask='auto');y-=211
text('Bei g = 0 ergibt sich für jede Länge höchstens <b>Faktor 5</b>, obwohl die ursprüngliche Zeilennorm 3 beträgt. Für |g| &lt; 1 bleibt die Familie beschränkt; bei |g| = 1 wächst sie linear, darüber exponentiell in der Zellenzahl.','body',gap=9)
text('Dies ist eine algebraische Positivkontrolle und ein elementarer Schurkomplement-Satz. Es ist noch kein stabiler, korrekt normierter 4D-Kausalset-Operator. History und Detektorkopplung benötigen eigene uniforme Grenzen.','small')
footer()

title('04 / VALIDIERUNG UND ANSCHLUSS','Ein präziser Ausschluss.<br/>Ein enger gefasster Auftrag.')
table([['Prüfung','Ausgeführt'],['144 rationale Fächerfälle','Ordnung aus Minkowski-Koordinaten; Intervalle; K²; exakte Norm'],['30 rationale Zellenfälle','Schur-Elimination; scharfe Norm; stabile und instabile Parameter'],['Zwei Rechenwege','Dichte Gauss-Jordan-Inverse und kausale Vorwärtsrekursion'],['4 Negativkontrollen','Falsche Intervalle, fehlender Beitrag, Vorzeichen und falsche Potenzbehauptung'],['Konstanten / Herkunft','3 überlappende rationale Einschliessungen; 3 Git-Blob- und SHA256-geprüfte Quellen']], [165,CW-165])
text('<b>Entscheidung:</b> Die Forderung nach einer Maximumsnorm-Schranke für alle Realisierungen wird für die definierte Klasse ausgeschlossen. Die pauschale Verwerfung physikalischer Kausalset-Dynamik folgt daraus nicht. METHOD und G1 bleiben HOLD.')
text('<b>Nächster Anschluss:</b> Für feste physikalische Zeitfenster Norm und Ausfallwahrscheinlichkeit festlegen; dann signierte Pfadsummen unter kontrollierter lokaler Punktkonzentration untersuchen. Die bisher offene Grad-5-Genauigkeitsprüfung bleibt ein eigener Auftrag.')
text('Nachprüfen','h2',gap=6)
text('Im Prüfpaket: <b>python3 reproduce.py</b><br/>Bytegenauer Ergebnisvergleich: <b>python3 reproduce.py --check</b><br/>Vollständige Beweise: PROOF.md · rationale Ergebnisse: results/RESULTS.json','small',gap=10)
text('Quellen und Reichweite','h2',gap=6)
text('[1] Aslanbeigi, Saravani, Sorkin (2014), <i>Generalized Causal Set d’Alembertians</i>, Abschnitte 1 und 3.5: <link href="https://arxiv.org/abs/1403.1622" color="#007D7A">arxiv.org/abs/1403.1622</link>. Kontext gemittelter Operatoren; kein übernommener Beweis unseres Fächersatzes.<br/>[2] Last / Penrose (2017), <i>Lectures on the Poisson Process</i>, Definition 3.1: <link href="https://stoch.math.kit.edu/img/Last/lastpenrose2017.pdf" color="#007D7A">Autorenfassung bei KIT</link>.<br/>[3] Projekt Main nach PR #158, Commit c156dab194bb…; unveränderliche Quellen und Hashes in evidence/SOURCES.json.','small',gap=10)
text('Eigene Herleitung mit exakten endlichen Kontrollen. Kein externes Peer Review, keine Beweisassistent-Verifikation und keine Prioritätsbehauptung. Keine neuen Ensembles oder physikalischen Freigaben.','small')
footer();c.save()
print(pdf)
