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

class Asymmetry(Flowable):
    def __init__(self):Flowable.__init__(self);self.width=475;self.height=180
    def draw(self):
        c=self.canv
        def box(x,y,w,label,accent=False):
            c.setFillColor(HexColor('#FFF4DC')if accent else LIGHT);c.setStrokeColor(GOLD if accent else TEAL);c.roundRect(x,y,w,25,5,fill=1,stroke=1)
            c.setFillColor(NAVY);c.setFont('DV',9);c.drawCentredString(x+w/2,y+8.5,label)
        def arrow(x1,y1,x2,y2):
            from math import atan2,cos,sin
            c.setStrokeColor(TEAL);c.setFillColor(TEAL);c.setLineWidth(1.2);c.line(x1,y1,x2,y2)
            a=atan2(y2-y1,x2-x1);p=c.beginPath();p.moveTo(x2,y2);p.lineTo(x2-7*cos(a-.45),y2-7*sin(a-.45));p.lineTo(x2-7*cos(a+.45),y2-7*sin(a+.45));p.close();c.drawPath(p,fill=1,stroke=0)
        box(137,149,200,'Kragen: a < b < c < d')
        box(70,101,150,'Zusätzliches Ereignis e',True);box(102,55,86,'Langer Ast: f');box(300,78,95,'Kurzer Ast: g')
        box(147,5,180,'Freier positiver Endpunkt j')
        arrow(190,149,145,126);arrow(285,149,345,103);arrow(145,101,145,80);arrow(145,55,205,30);arrow(347,78,270,30)

add(p('FORSCHUNGSNOTIZ  08.11.2026  /  VERSION 0.1','kicker'),p('Asymmetrie und<br/>Endpunktkriterium','title'),p('Die kleinste Astverlängerung scheitert am freien Endpunkt','sub'))
add(p('Ein zusätzliches Ereignis in einem Ast verändert die globalen Kausalintervalle. Für die Astlängen 2 und 1 kann die Uhrableitung am gemeinsamen positiven, frei variierten Endpunkt nicht verschwinden. Die Aussage gilt für alle streng kausal geordneten Uhren dieser Klasse.'))
add(Asymmetry(),Spacer(1,10),p('Die vier festen Vorgänger sind in einer Box zusammengefasst. Zwischen e bzw. f und g bestehen keine Kausalrelationen. Alle Pfeile schließen ihre transitiven Relationen ein; eine räumliche Einbettung wird nicht dargestellt.','small'))
add(code(['Für H=U-d>0 und r>0 gilt scharf:', '7 < 2q_j/(rH) < 17', 'Keine vollständige Stationarität dieses freien Blocks']))
add(p('Was die erweiterte Vorprüfung ergibt','sub'),p('Von 16 Astlängenklassen scheitern sechs bereits an der Endpunkt-Uhrgleichung. Zehn erlauben eine verschwindende Endpunktreaktion. Das erfüllt noch nicht die übrigen Uhrgleichungen oder Normierungen.'))
add(p('Alle acht physikalischen Gates bleiben HOLD. Kein allgemeines Asymmetrieverbot, kein physikalischer Vakuum-Außenraum, keine hergeleitete Präparation, Rückwirkung, dynamische Stabilität oder Bounce-Aussage. Keine kostenpflichtige Rechnung und kein n=5-Produktionslauf.','small'))
add(p('Basis: Main 5b5907de8ab087183e9a6a0072336226ae0fa771 nach PR 271. Beweise, genaue Variationsdomäne und Reproduktionscode im Prüfpaket.','small'))

page('01  /  GLOBALER VORZEICHENBEWEIS','Der Rest hat für jede erlaubte Uhrwahl dasselbe Vorzeichen')
add(p('Die unveränderten Gewichte sind B(k)=(1,-9,16,-8,0,…). Nach dem Einfügen von e werden die Intervalle zum Endpunkt j global neu gezählt:'))
add(table([['Vorgänger','Intervallgröße k','B'],['a, b, c','6, 5, 4','je 0'],['d','3','-8'],['e','1','-9'],['f','0','1'],['g','0','1']], [210,145,120]))
add(Spacer(1,10),code(['Cj=1+[-8(U-d)²-9(U-e)²', '       +(U-f)²+(U-g)²]/2', 'q_j=r[8(U-d)+9(U-e)-(U-f)-(U-g)]/2']))
add(p('Weil j keine Nachfolger hat, trägt keine spätere Materiezeile zur Ableitung nach U bei. Die feste gravitative Wirkung besitzt keine Uhrableitung. Der Ausdruck ist deshalb die gesamte Endpunktreaktion.'))
add(code(['2q_j/r = 15(U-e)+(f-e)+(g-d)+7(e-d) > 0']))
add(p('Jeder Term ist entlang der festgelegten Ordnung strikt positiv. Randuhren und andere Dichtegewichte können die notwendige Gleichung q_j=0 deshalb nicht herstellen. Die Normierungen müssen für diesen Ausschluss nicht erst gelöst werden.'))
add(p('Die quantitative Lücke','sub'),p('Mit x=e-d, y=f-e, z=U-f, α=g-d und β=U-g gilt H=x+y+z=α+β. Setze D=2q_j/r:'))
add(code(['D=7x+16y+15z+α', 'D-7H=9y+8z+α>0', '17H-D=9x+z+β>0']))

page('02  /  ASTLÄNGENMATRIX','Symmetrie allein entscheidet die Vorprüfung nicht')
add(p('Zwei getrennte Ketten mit p und q inneren Ereignissen treffen nach demselben viergliedrigen Kragen auf einen freien positiven Endpunkt. Die Tabelle klassifiziert ausschließlich dessen Uhrgleichung.'))
add(table([['p / q','1','2','3','≥4'],['1','Uhr möglich','q>0','q<0','Uhr möglich'],['2','q>0','q>0','Uhr möglich','Uhr möglich'],['3','q<0','Uhr möglich','q<0','Uhr möglich'],['≥4','Uhr möglich','Uhr möglich','Uhr möglich','Uhr möglich']], [55,105,105,105,105]))
add(Spacer(1,10),p('<b>q&gt;0 / q&lt;0:</b> für alle geordneten Uhrdaten strikt; eine vollständige stationäre Lösung ist unter den erklärten Endpunktbedingungen ausgeschlossen. <b>Uhr möglich:</b> exakter q_j=0-Zeuge vorhanden, aber keine Aussage über die übrigen Gleichungen.'))
add(p('Warum die Matrix analytisch folgt','sub'),p('Seien g₀,g₁,… die positiven Lücken rückwärts vom Endpunkt entlang eines Asts. Für S_j=ΣB(U-T) und q_j=-rS_j/2 lauten dessen Beiträge:'))
add(code(['F₁=g₀ > 0', 'F₂=-8g₀-9g₁ < 0', 'F₃=8g₀+7g₁+16g₂ > 0', 'Fₙ=-g₁+8g₂-8g₃ für n≥4']))
add(p('Bei p+q=2 kommt 16(U-d)-8(U-c) aus dem Kragen hinzu, bei p+q=3 noch -8(U-d). Ab p+q≥4 ist der gemeinsame Kragenbeitrag null.'))
add(p('Lange Äste besitzen beide Vorzeichen. Ihre letzten vier aktiven Uhrwerte können bei weiterer Verlängerung erhalten bleiben; ältere zusätzliche Astereignisse tragen am Endpunkt Gewicht null. Deshalb umfasst die letzte Zeile und Spalte tatsächlich alle endlichen Längen ab vier.','small'))

page('03  /  MACHBARKEIT IST NOCH KEINE LÖSUNG','Ein asymmetrischer Uhrzeuge verletzt weiterhin die Normierung')
add(p('Für die Astlängen (2,3) existieren streng geordnete Uhrdaten mit verschwindender Endpunktreaktion. Ein im Prüfpaket exakt gespeicherter Zeuge lautet:'))
add(table([['Elemente','Uhrwerte'],['Kragen a, b, c, d','-21/10, -11/10, -1/10, 0'],['Linker Ast, zwei Ereignisse','1/100, 1/50'],['Rechter Ast, drei Ereignisse','1/100, 1/50, 9/100'],['Gemeinsamer Endpunkt','U=1']], [225,250]))
add(Spacer(1,12),code(['S_j=0  ⇒  q_j=0 für jedes r>0', 'Aber: Cj=2507/2500 ≠ 0']))
add(p('Der Zeuge besteht damit nur die Endpunkt-Uhrprüfung. Schon die freie Dichtevariation am selben Endpunkt scheitert. Die Daten werden ausdrücklich nicht als vollständige asymmetrische stationäre Lösung ausgegeben.'))
add(p('Wie die Uhrzeugen konstruiert werden','sub'),p('Für jede nicht ausgeschlossene Klasse werden zwei streng geordnete rationale Uhrvektoren mit entgegengesetzten S_j-Vorzeichen gewählt. S_j ist bei festgehaltener Ordnung linear. Eine exakt berechnete Konvexkombination setzt S_j auf null und erhält alle strikten kausalen Uhrabstände.'))
add(p('Alle zehn Zeugen sind mit Mischungsgewicht, Uhrwerten und Normierungsrest gespeichert. Bei längeren Ästen werden nur zusätzliche ältere Ereignisse eingefügt; deren weitere Normierungen sind dadurch noch nicht erfüllt.'))
add(p('Welche Frage offen bleibt','sub'),p('Ob ein anderer Randkragen und andere innere Werte sämtliche Normierungen und Uhrgleichungen gemeinsam erfüllen, muss separat abgeleitet werden. Die konkrete Normierungsverletzung dieses Zeugen ist kein allgemeiner Ausschluss der Klasse (2,3).'))

page('04  /  SCHARFE GRENZEN UND RANDWAHL','Die Endpunktannahme gehört zur Aussage')
add(p('Bei H=1 lassen sich die Grenzen 7 und 17 innerhalb der strikten Ordnung beliebig annähern. Die analytischen Folgen liefern D=7+18ε und D=17-11ε, jeweils D=2q_j/r.'))
add(table([['ε','Untere Folge D','Obere Folge D'],['1/10','44/5 = 8,8','159/10 = 15,9'],['1/100','359/50 = 7,18','1689/100 = 16,89'],['1/1000','3509/500 = 7,018','16989/1000 = 16,989']], [120,175,180]))
add(Spacer(1,10),p('Die Endwerte sind nicht Teil der strikten Klasse: Sie erfordern verschwindende kausale Lücken. Mit deklarierten Böden r≥r_min und H≥H_min gilt die absolute Trennung:'))
add(code(['q_j > (7/2) r_min H_min']))
add(p('Ohne solche Böden kann der absolute Rest klein erscheinen, während die normierte Lücke bestehen bleibt. Ein kleiner absoluter Wert allein qualifiziert deshalb keine stationäre Lösung.'))
add(p('Freier Endpunkt oder feste Zukunftsranduhr','sub'),p('Wird U frei variiert, ist q_j=0 eine notwendige innere Gleichung. Wird U stattdessen als Randdatum festgehalten, wird diese Gleichung dort nicht verlangt; q_j ist dann eine Randreaktion. Das ist eine andere Variationsaufgabe.'))
add(p('Bei Nachfolgern von j können spätere Wirkungszeilen beitragen; die Ableitung ist dann neu zu berechnen. Bei r=0 fehlt die positive Endpunktzeile. Keine dieser Änderungen wird hier als geprüfte Reparatur ausgegeben.'))
add(p('Auch ein Null-Dichte-Ereignis innerhalb eines Asts bleibt Teil der globalen Intervallzählung. Es darf nicht allein wegen seines Dichtewerts aus der Ordnung entfernt werden.','small'))

page('05  /  VERIFIKATION UND NÄCHSTE AUFGABE','Die Vorprüfung spart ungeeignete Anschlussversuche')
add(table([['Kontrolle','Ergebnis'],['Symbolische Primäridentitäten','5 vollständige Koeffizientenvergleiche'],['Astlängenklassen','16: 6 ausgeschlossen, 10 nur Uhr-möglich'],['Strikte rationale Uhrprofile','588'],['Unabhängige Wirkungsableitungen','588'],['Normierte (2,1)-Schrankenfälle','162'],['Werte scharfer Grenzfolgen','6'],['Lange Äste, Längen 4 bis 7','26 Suffix-Kontrollen'],['Negativkontrollen','7 erwartete Ausschlüsse']], [270,205]))
add(Spacer(1,10),p('Alle Kontrollen rechnen exakt mit rationalen Zahlen und der Python-Standardbibliothek. Vier Ergebnisdateien werden isoliert bytegleich reproduziert. Die allgemeinen Aussagen folgen aus den Beweisen; die endlichen Kontrollen ergänzen sie.'))
add(code(['python3 -O -B verify_package.py', 'python3 -O -B replay.py']))
add(p('Nächster wissenschaftlicher Schritt','sub'),p('Einen vorab gewählten asymmetrischen Kandidaten wie (2,3) auf sämtliche inneren Uhr- und Normierungsgleichungen prüfen. Dabei muss die Entscheidung über freie oder festgehaltene Zukunftsranduhren sichtbar bleiben. Der jetzige Uhrzeuge ist noch kein Erfolg dieser vollständigen Prüfung.'))
add(p('Quellen und Grenzen','sub'))
for title,url in [('Projekt PR 271: geerbte Materiewirkung, symmetrischer Diamant, Intervallbuchhaltung und Referenzcode. Quellidentitäten sind im Paket gebunden.','https://github.com/thomasmgfeller/x6-spectral-astrolabium/pull/271'),('Dittrich und Höhn (2013), Constraint analysis for variational discrete systems: methodischer Kontext für Variationsgleichungen und Randbedingungen.','https://arxiv.org/abs/1303.4294v3')]:add(p('<link href="'+url+'" color="#16756F">'+escape(title)+'</link>','small'))
add(p('Plan nach analytischem Entwurf vor dem endlichen Kontrolllauf gehasht. Keine externe Präregistrierung oder Replikation. Keine vollständige asymmetrische stationäre Lösung oder physikalische Bounce-Aussage. Alle acht Gates bleiben HOLD.','small'))

def footer(c,doc):
    c.saveState();w,h=doc.pagesize;c.setStrokeColor(TEAL);c.setLineWidth(1);c.line(60,49,w-60,49);c.setFont('DV',7.5);c.setFillColor(MUTED);c.drawString(60,34,'CST-DUST · Asymmetrie und Endpunktkriterium v0.1 · 08.11.2026');c.drawRightString(w-60,34,f'{doc.page} / 6');c.restoreState()
def invariant_canvas(*a,**kw):kw['invariant']=1;return canvas.Canvas(*a,**kw)
out=ROOT/'CST_DUST_Asymmetrie_Endpunktkriterium_v0_1.pdf'
doc=SimpleDocTemplate(str(out),pagesize=(595.2756,841.8898),rightMargin=60,leftMargin=60,topMargin=48,bottomMargin=65,title='CST-DUST: Asymmetrie und Endpunktkriterium v0.1',author='Thomas Gfeller · Forschungsprojekt mit ChatGPT')
doc.build(story,onFirstPage=footer,onLaterPages=footer,canvasmaker=invariant_canvas)
print(out)

