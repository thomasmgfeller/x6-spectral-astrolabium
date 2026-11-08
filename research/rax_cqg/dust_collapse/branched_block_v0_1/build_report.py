#!/usr/bin/env python3
from pathlib import Path
from reportlab.pdfgen import canvas
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak, Table, TableStyle, KeepTogether, Flowable
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.colors import HexColor, white
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.enums import TA_LEFT
from xml.sax.saxutils import escape
import json
ROOT=Path(__file__).resolve().parent
FONT=Path('/usr/share/fonts/truetype/dejavu')
for n,f in [('DV','DejaVuSans.ttf'),('DV-Bold','DejaVuSans-Bold.ttf'),('Mono','DejaVuSansMono.ttf')]:
    pdfmetrics.registerFont(TTFont(n,str(FONT/f)))
NAVY=HexColor('#173447'); TEAL=HexColor('#16756F'); INK=HexColor('#233640'); MUTED=HexColor('#59717C'); LIGHT=HexColor('#EEF4F5'); GOLD=HexColor('#AE701D')
styles={
 'kicker':ParagraphStyle('kicker',fontName='DV-Bold',fontSize=9,leading=13,textColor=TEAL,spaceAfter=14),
 'title':ParagraphStyle('title',fontName='DV-Bold',fontSize=25,leading=31,textColor=NAVY,spaceAfter=18),
 'h':ParagraphStyle('h',fontName='DV-Bold',fontSize=16,leading=21,textColor=NAVY,spaceAfter=12),
 'sub':ParagraphStyle('sub',fontName='DV-Bold',fontSize=10.3,leading=15,textColor=TEAL,spaceBefore=12,spaceAfter=6),
 'body':ParagraphStyle('body',fontName='DV',fontSize=9.4,leading=14.8,textColor=INK,spaceAfter=9),
 'small':ParagraphStyle('small',fontName='DV',fontSize=8.1,leading=11.5,textColor=MUTED,spaceAfter=6),
 'formula':ParagraphStyle('formula',fontName='Mono',fontSize=9,leading=14,textColor=NAVY,spaceAfter=0),
}
def p(s,sty='body'): return Paragraph(s,styles[sty])
def code(lines):
    rows=[[p(escape(line),'formula')] for line in lines]
    t=Table(rows,colWidths=[475]);t.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,-1),LIGHT),('LEFTPADDING',(0,0),(-1,-1),12),('RIGHTPADDING',(0,0),(-1,-1),10),('TOPPADDING',(0,0),(-1,0),10),('BOTTOMPADDING',(0,-1),(-1,-1),10)]))
    return KeepTogether([t,Spacer(1,11)])
def table(rows,widths):
    data=[[p(str(c),'small' if i else 'kicker') for c in row] for i,row in enumerate(rows)]
    t=Table(data,colWidths=widths,hAlign='LEFT');t.setStyle(TableStyle([('VALIGN',(0,0),(-1,-1),'TOP'),('BACKGROUND',(0,0),(-1,0),LIGHT),('LINEBELOW',(0,0),(-1,0),.6,TEAL),('LINEBELOW',(0,1),(-1,-1),.3,HexColor('#D4DFE2')),('TOPPADDING',(0,0),(-1,-1),7),('BOTTOMPADDING',(0,0),(-1,-1),5)]));return t
story=[]
def add(*xs):story.extend(xs)
def page(k,title):
    if story:add(PageBreak())
    add(p('CST-DUST  /  '+k,'kicker'),p(title,'h'))

class Topology(Flowable):
    def __init__(self):Flowable.__init__(self);self.width=475;self.height=170
    def draw(self):
        c=self.canv
        def box(x,y,w,label):
            c.setFillColor(LIGHT);c.setStrokeColor(TEAL);c.roundRect(x,y,w,26,5,fill=1,stroke=1)
            c.setFillColor(NAVY);c.setFont('DV',9);c.drawCentredString(x+w/2,y+9,label)
        def arrow(x1,y1,x2,y2):
            from math import atan2,cos,sin
            c.setStrokeColor(TEAL);c.setFillColor(TEAL);c.setLineWidth(1.2);c.line(x1,y1,x2,y2)
            a=atan2(y2-y1,x2-x1);path=c.beginPath();path.moveTo(x2,y2);path.lineTo(x2-7*cos(a-.45),y2-7*sin(a-.45));path.lineTo(x2-7*cos(a+.45),y2-7*sin(a+.45));path.close();c.drawPath(path,fill=1,stroke=0)
        for x,title,joined in ((0,'Offene Gabel',False),(260,'Mit Wiederanschluss',True)):
            c.setFont('DV-Bold',10);c.setFillColor(NAVY);c.drawCentredString(x+105,157,title)
            box(x+25,112,160,'Kragen: a < b < c < d')
            box(x+10,60,65,'Ast f');box(x+135,60,65,'Ast g')
            arrow(x+80,112,x+43,86);arrow(x+130,112,x+168,86)
            if joined:
                box(x+60,6,90,'Nachfolger j');arrow(x+43,60,x+90,32);arrow(x+168,60,x+120,32)
            else:
                c.setFillColor(MUTED);c.setFont('DV',8.5);c.drawCentredString(x+105,23,'f und g bleiben unvergleichbar')

add(p('FORSCHUNGSNOTIZ  08.11.2026  /  VERSION 0.1','kicker'),p('Verzweigung und<br/>Wiederanschluss','title'),p('Ein exakt lösbarer Schritt über die reine Zeitkette hinaus','sub'))
add(p('Die unveränderte Materiewirkung wird auf einer offenen Gabel und einem anschließend wieder verbundenen Diamanten geprüft. Die globale Intervallzählung verändert die Anschlussgleichungen. Beide erklärten Klassen sind vollständig klassifiziert.'))
add(Topology(),Spacer(1,9))
add(p('Die vier festen Vorgänger sind jeweils in einer Box zusammengefasst. Pfeile erzeugen die Kausalordnung einschließlich ihrer transitiven Relationen. Zwischen f und g besteht keine Relation; das Bild zeigt keine räumliche Einbettung.','small'))
add(table([['Befund','Ergebnis'],['Offene Gabel','Stationarität bei A=P=0; Astuhren frei'],['Positiver Wiederanschluss','P<0; gleiche Astuhren und Astgewichte'],['Zulässige Diamantkragen','Dreidimensionale Familie; eine Randgleichheit'],['Äußere Reaktion','Explizit bestimmt und weiterhin ungleich null']], [210,265]))
add(Spacer(1,12),code(['54 exakte Diamantfälle erfüllen alle inneren Gleichungen', 'Alle acht physikalischen Gates: HOLD']))
add(p('Die Nachfolger tragen positive Materie. Kein hergeleiteter Vakuum-Außenraum, keine physikalisch ausgewählte Randpräparation, keine Geometrie-Rückwirkung, keine dynamische Stabilität und kein Bounce. Kein n=5-Produktionslauf und keine kostenpflichtige Rechnung.','small'))
add(p('Basis: Main 3ddc2a6a22f2cc084806b2917c036593912e3d43 nach PR 270. Vollständige Beweise und Reproduktionscode im Prüfpaket.','small'))

page('01  /  VOLLSTÄNDIGE INTERVALLE','Der gemeinsame Nachfolger verändert die Gewichte')
add(p('Vier äußere Uhren a&lt;b&lt;c&lt;d sind fest; ihre Dichtezeilen sind null. Die unvergleichbaren Äste tragen Uhren t₁,t₂ und Gewichte w₁,w₂. Der gemeinsame Nachfolger trägt U und r. Alle inneren Uhren und positiven Gewichte werden frei variiert.'))
add(code(['P=-8a+16b-9c+d', 'A=1+(-8a²+16b²-9c²+d²)/2', 'C₁=A-Pt₁;   C₂=A-Pt₂', 'S=-(w₁C₁+w₂C₂+rCj)/2']))
add(p('Die geerbten Intervallgewichte sind B(k)=(1,-9,16,-8,0,…). Die globale Ordnung liefert am gemeinsamen Nachfolger:'))
add(table([['Vorgänger','Innere Elemente k','Gewicht B'],['a','5','0'],['b','4','0'],['c','3','-8'],['d','2','16'],['f und g','je 0','je 1']], [185,160,130]))
add(Spacer(1,10),code(['Cj = 1+[(U-t₁)²+(U-t₂)²', '          +16(U-d)²-8(U-c)²]/2']))
add(p('Warum die offene Gabel anders ist','sub'),p('Ohne Nachfolger j sind die Uhrableitungen w₁P/2 und w₂P/2. Positive Gewichte verlangen P=0; die beiden Normierungen dann A=0. Der alte Kragen (-5/2,-2,-4/3,0) erfüllt beides. Die beiden Astuhren sind frei und dürfen verschieden sein.'))
add(p('Mit einem positiven Nachfolger entsteht dagegen in jeder Astgleichung der Beitrag r(U-tᵢ)/2&gt;0. Derselbe P=0-Kragen kann ihn nicht tragen. Die vollständige Kopplung verlangt neue Randdaten.'))

page('02  /  EXISTENZSATZ','Der Diamant bindet beide Äste gemeinsam')
add(p('Die drei Uhrgleichungen und die drei freien Dichtegleichungen ergeben:'))
add(code(['q₁=[w₁P+r(U-t₁)]/2', 'q₂=[w₂P+r(U-t₂)]/2', 'qj=-r[10U-t₁-t₂-16d+8c]/2', 'C₁=C₂=Cj=0']))
add(p('Positive Gewichte und U&gt;t₁,t₂ erzwingen P&lt;0. Damit setzen die beiden Astnormierungen t₁=t₂=τ=A/P. Die Uhrgleichungen binden auch die Astgewichte: w₁=w₂=w.'))
add(code(['U=(τ+8d-4c)/5', 'g=U-τ=4(2d-c-τ)/5', 'w=-r g/P']))
add(p('Mit L=d-c und h=τ-d ist die verbleibende Normierung J=1+(4/5)(h²-2hL-9L²).'))
add(code(['Existenz genau dann, wenn:', 'P<0,   d<τ=A/P<2d-c,   J=0', 'Alle positiven Lösungen:', '0<r<min(1,-P/g);   w₁=w₂=-r g/P']))
add(p('Die Bedingungen sind notwendig und hinreichend für diese feste Ordnung und diese freien Variationen. Bei festem Kragen bleibt genau ein positiver Gewichtsparameter frei. Null-Dichte-Zweige und andere Variationsklassen sind nicht erfasst.'))
add(p('Gleiche Uhren erzeugen keine Kausalrelation','sub'),p('Die Ereignisse f und g bleiben verschieden und kausal unvergleichbar. Ein zusätzliches Verlangen t₁&lt;t₂ allein aufgrund der Beschriftung würde die vorhandenen Lösungen künstlich ausschließen. Die Uhrgleichheit folgt hier aus identischen Astnormierungen.'))

page('03  /  VOLLSTÄNDIGE RANDDATEN','Eine ganze Familie statt eines einzelnen Zeugen')
add(p('Setze k=L-h. Die gemeinsame Normierung liefert k²=10L²-5/4 und 0&lt;k&lt;L. Die jüngeren äußeren Daten sind deshalb genau im folgenden offenen Bereich zulässig:'))
add(code(['1/8<L²<5/36', 'k=√(10L²-5/4);   h=L-k']))
add(p('Für x=c-b und ell=b-a definiere H=h+L. Die übrigen Bedingungen lassen sich explizit lösen:'))
add(code(['Z=√[1/4+2(H+x)²-(9/8)H²+h²/8]', 'ell=Z-H-x', 'x>L/8+(1/4)√(2+9L²/8)', 'd=λ;   c=λ-L;   b=λ-L-x;   a=b-ell']))
add(p('Jedes erlaubte L, jedes x oberhalb der Grenze und jede gemeinsame Verschiebung λ liefern einen zulässigen Kragen. Der positive Wurzelzweig ist durch a&lt;b eindeutig. Das sind drei äußere Parameter.'))
add(p('Konkreter exakter Kontrollfall','sub'))
add(code(['L=√(5/39),   r=1/2', '(a,b,c,d)=L((5-√2395)/10, -3, -1, 0)', 't₁=t₂=L/2;   U=9L/10', 'w₁=w₂=1/(215-4√2395)']))
add(p('Diese Werte gehören zum vorher deklarierten Kontrollraster. Alle inneren Normierungen und Uhrgleichungen verschwinden exakt. Die Daten sind konstruierte Existenzzeugen und noch keine physikalisch ausgewählte Präparation.'))
add(p('Die Grenzen des L-Intervalls markieren Kollisionen innerer Uhrwerte in den festgelegten Modelleinheiten. Daraus folgen keine physikalischen Planck-, Bounce- oder Singularitätsskalen.','small'))

page('04  /  VERKLEBUNG UND RANDREAKTION','Zwei Kettenarme allein ergeben die falsche Wirkung')
add(p('Die induzierten Arme Larm={a,b,c,d,f,j} und Rarm={a,b,c,d,g,j} teilen fünf Elemente. Trotzdem fehlt in jedem Arm ein Ast innerhalb globaler Intervalle. Beide Arme sind dort nicht ordnungskonvex.'))
add(code(['Sglobal=Sleft+Sright-Sshared+ΔS', 'ΔS=-r[-8(U-a)²+32(U-b)²', '          -49(U-c)²+35(U-d)²]/4']))
add(p('Die feste gravitative Kombination Fg=N-ΣB liefert global -4, je Arm 5 und im gemeinsamen Teil 4. Die notwendige gravitative Korrektur beträgt daher -10. Das ist eine Buchhaltungsidentität, keine Geometrievariation.'))
add(p('Eine unabhängige Randbedingung bleibt','sub'))
add(code(['∂a J=-64k(τ-a)/(5P)>0', 'q_aussen=-(r/2)∇J', 'q_a=-8w(τ-a)<0', 'Σ q_i=0;   Σ T_i q_i=2w+r>0']))
add(p('J=0 besitzt überall Rang eins und beschreibt eine glatte dreidimensionale Randfläche. Die Reaktion steht normal auf dieser Fläche und bleibt ungleich null. Die physikalische Vorgeschichte müsste sowohl die Randdaten als auch diese Reaktion begründen.'))
add(p('Notwendige Grenzen für ungleiche Äste','sub'))
add(code(['|P||t₁-t₂| ≤ |C₁|+|C₂|', '|P||w₁-w₂| ≤ 2(|q₁|+|q₂|)+r|t₁-t₂|']))
add(p('Diese Restfehlergrenzen sind notwendig, nicht hinreichend. Ohne unteren Betrag für P werden sie beim Auflösen nach Astabweichungen nicht uniform. Sie beweisen keine dynamische Stabilität.','small'))

page('05  /  PRÜFUNG UND NÄCHSTER SCHRITT','Der Wiederanschluss ist geprüft, die Symmetrie bleibt zu testen')
add(table([['Kontrolle','Ergebnis'],['Symbolische Identitäten','10 vollständige Koeffizientenvergleiche'],['Wirkungsverklebung / Reaktionen','32 Fälle / 224 Komponenten'],['Offene Gabel','81 exakte stationäre Fälle'],['Diamantformen','12 geprüft: 6 zulässig; 18 verschobene Vorzeichenausschlüsse'],['Stationärer Diamant','54 vollständige Fälle'],['Randableitungen','216 durch automatisches Differenzieren geprüft'],['Astuhrstörungen / Restfehlerbudgets','108 / 108'],['Negativkontrollen','8 erwartete Ausschlüsse']], [265,210]))
add(Spacer(1,9),p('Alle Rechnungen verwenden rationale Arithmetik und exakte quadratische Zahlkörper. L², skalierte Uhren Y=T/L und Reaktionen q/L sind ausdrücklich gespeichert. Die Normierungen rechnen den Faktor L² mit. Vier Ergebnisdateien werden isoliert bytegleich reproduziert.'))
add(code(['python3 -O -B verify_package.py', 'python3 -O -B replay.py']))
add(p('Nächster sinnvoller Schritt','sub'),p('Eine kleine asymmetrische Verzweigung vorab festlegen, etwa mit unterschiedlich langer Vorgeschichte beider Äste. Dann lässt sich prüfen, welche der jetzigen Astgleichheiten nur aus identischen Zeilen folgen und welche Kopplungsbedingungen bestehen bleiben. Alle Intervalle müssen erneut global gezählt werden.'))
add(p('Quellen und Grenzen','sub'))
for title,url in [('Projekt PR 270: geerbte Materiewirkung, Kettenklassifikation und Referenzcode. Die allgemeine Verklebungsidentität stammt bereits aus PR 269 und dessen Ausgangsarbeit.','https://github.com/thomasmgfeller/x6-spectral-astrolabium/pull/270'),('Dittrich und Höhn (2013), Constraint analysis for variational discrete systems: methodischer Kontext, keine physikalische Validierung der zusätzlichen Modellwahl.','https://arxiv.org/abs/1303.4294v3')]:add(p('<link href="'+url+'" color="#16756F">'+escape(title)+'</link>','small'))
add(p('Plan nach analytischem Entwurf vor dem endlichen Kontrolllauf gehasht. Keine externe Präregistrierung oder Replikation. Keine physikalische Präparation, kein Vakuum-Außenraum, keine Rückwirkung, kein Bounce. Alle acht Gates bleiben HOLD.','small'))

def footer(c,doc):
    c.saveState();w,h=doc.pagesize;c.setStrokeColor(TEAL);c.setLineWidth(1);c.line(60,49,w-60,49);c.setFont('DV',7.5);c.setFillColor(MUTED);c.drawString(60,34,'CST-DUST · Verzweigung und Wiederanschluss v0.1 · 08.11.2026');c.drawRightString(w-60,34,f'{doc.page} / 6');c.restoreState()
def invariant_canvas(*a,**kw):kw['invariant']=1;return canvas.Canvas(*a,**kw)
out=ROOT/'CST_DUST_Verzweigung_Wiederanschluss_v0_1.pdf'
doc=SimpleDocTemplate(str(out),pagesize=(595.2756,841.8898),rightMargin=60,leftMargin=60,topMargin=48,bottomMargin=65,title='CST-DUST: Verzweigung und Wiederanschluss v0.1',author='Thomas Gfeller · Forschungsprojekt mit ChatGPT')
doc.build(story,onFirstPage=footer,onLaterPages=footer,canvasmaker=invariant_canvas)
print(out)
