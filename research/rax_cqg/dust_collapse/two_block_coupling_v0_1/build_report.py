#!/usr/bin/env python3
from pathlib import Path
from reportlab.pdfgen import canvas
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak, Table, TableStyle, KeepTogether
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
add(p('FORSCHUNGSNOTIZ  08.11.2026  /  VERSION 0.1','kicker'),p('Zweiblock-Kopplung und<br/>gemeinsame Randreaktion','title'),p('Ein konkreter Anschlussversuch nach PR 268','sub'))
add(p('Der zweite Block wird aus derselben Materiewirkung aufgebaut. Die vollständige Kopplung ist geprüft. Der alte festgehaltene Kragen scheitert an den gemeinsamen stationären Gleichungen; mit veränderten äußeren Randdaten existiert ein exakter Positivkontrollfall.'))
add(table([['Ergebnis','Reichweite'],['Exakte Blockverklebung','Kreuzpaare, Intervalländerungen und Überlappung vollständig berücksichtigt'],['Vier gemeinsame Vorgänger','Minimal auf der untersuchten Kettenklasse'],['Bisheriger eingefrorener Kragen','Kein gemeinsamer innerer Sattel mit ein oder zwei positiven Zukunftselementen'],['Neu konstruierter Kragen','Exakte gekoppelte Familie mit zwei freien positiven Elementen']], [220,255]))
add(Spacer(1,12),p('Der Fortschritt','sub'),p('Die linke und rechte Blockreaktion müssen nicht einzeln null sein. Im neuen Kontrollfall gleichen sie sich am gemeinsamen Element exakt aus. Die notwendige äußere Randreaktion bleibt erhalten.'))
add(code(['Gleiche Materiewirkung; kein neuer Randterm', 'Stationäre Familie, kein isoliertes Minimum', 'Alle acht physikalischen Gates: HOLD']))
add(p('Der neue Zukunftsblock trägt positive Materiedichte. Er ist kein hergeleiteter Vakuum-Außenraum. Die Randdaten sind konstruiert, noch nicht physikalisch ausgewählt. Kein Bounce, kein n=5-Produktionslauf, keine kostenpflichtige Rechnung.'))
add(p('Basis: Main 483358692a06cc1f17e12f9e392fad550a7494ca nach PR 268. Beweise, Quellen und Reproduktionscode im begleitenden Prüfpaket.','small'))

page('01  /  VOLLSTÄNDIGE KOPPLUNG','Alle Intervalle gehören zur Bilanz')
add(p('Die geerbte Wirkung verwendet B=b(k) mit b=(1,-9,16,-8,0,…). k zählt die Elemente strikt innerhalb eines kausalen Intervalls. Für überlappende induzierte Blöcke L,R mit D=L∩R und C=L∪R ist die disjunkte frühere Buchhaltung entsprechend zu ergänzen.'))
add(code(['S_d(X) = -Σ_x w_x/2', '         -Σ_(y≺x) w_x B^X_yx(T_x-T_y)²/4', 'S_d(C) = S_d(L)+S_d(R)-S_d(D)+ΔS_d']))
add(p('Die Korrektur verwendet für jedes globale Paar die Differenz seiner Koeffizienten in C, L, R und D. Sie enthält sowohl fehlende Kreuzpaare als auch interne Intervalle, deren Elementzahl sich im Teilblock verändert. Die konstante Dichtezeile schließt bereits durch Inklusion und Exklusion.'))
add(code(['δB = B^C - 1_L B^L - 1_R B^R + 1_D B^D', 'ΔS_d = -Σ w_x δB_yx(T_x-T_y)²/4', 'F_g(C)-F_g(L)-F_g(R)+F_g(D) = -Σ δB']))
add(p('Auch die geerbte feste BDG-Wirkung wird damit korrekt zusammengesetzt. Sie ist bei festgehaltener Geometrie unabhängig von den Uhren; eine Geometrievariation wird hier nicht ausgeführt.'))
add(p('Gemeinsame statt getrennte Stationarität','sub'))
add(code(['q_z = ∂S_d/∂T_z', 'q_z^C = q_z^L+q_z^R-q_z^D+∂z ΔS_d = 0']))
add(p('Der Impulsabgleich verlangt die verschwindende Gesamtsumme. Getrennt stationäre Teilblöcke sind keine Voraussetzung. Die globale Ordnung einschließlich aller blockübergreifenden Relationen muss bekannt sein; die lokalen Restriktionen allein bestimmen sie im Allgemeinen nicht.'))

page('02  /  GEMEINSAME VORGESCHICHTE','Vier Elemente genügen auf einer Kette')
add(p('Auf C=0≺1≺…≺N-1 werden L={0,…,j} und R={j-m+1,…,N-1} gewählt. Beide Blöcke sind ordnungskonvex und teilen m aufeinanderfolgende Elemente. Interne Intervalle bleiben unverändert.'))
add(code(['Kürzestes fehlendes Kreuzpaar:', 'y=j-m,   x=j+1,   k_C(y,x)=m', 'm=1,2,3: B=-9,16,-8 ≠ 0', 'm≥4: alle fehlenden Paare haben B=0']))
add(p('Bei zwei nichtleeren exklusiven Blockteilen ist die Überlappung von vier Elementen damit minimal für eine korrigierungsfreie Verklebung bei beliebigen Felddaten. Die Überlappungswirkung muss trotzdem abgezogen werden, damit keine Zeile doppelt zählt.'))
add(p('Ein einzelnes gemeinsames Element lässt Terme weg','sub'),p('Auf der Sechserkette mit vier festen Vorgängern und zwei freien Elementen t,u fehlt dem isolierten Zweipunkt-Zukunftsblock:'))
add(code(['ΔS_d = -v[-9(u-T3)²', '           +16(u-T2)²-8(u-T1)²]/4']))
add(p('Dieser Beitrag gehört zur ursprünglichen Wirkung. Ein zusätzlicher frei gewählter Oberflächenterm ist dafür nicht nötig.'))
add(p('Die Grenze der Aussage','sub'),p('Bei fünf unvergleichbaren Vorgängern eines gemeinsamen Nachfolgers können vier geteilte Elemente den fünften Link nicht abdecken. Das Gegenbeispiel ist exakt geprüft. Vier gemeinsame Elemente sind daher keine allgemeine Speicher- oder Lokalitätsgrenze der CST.'))

page('03  /  EINGEFRORENER KRAGEN','Die bisherige Lösung lässt sich so nicht fortsetzen')
add(p('Der Kragen aus PR 266 bleibt in dieser Prüfung unverändert: (-5/2,-2,-4/3,0). Das erste freie Element t&gt;0 erfüllt isoliert beide inneren Gleichungen.'))
add(p('Ein zusätzliches positives Zukunftselement','sub'))
add(code(['u>t, v>0  ⇒  q_f = v(u-t)/2 > 0']))
add(p('Die gemeinsame Uhrgleichung ist damit unmöglich. Dieser Rest bleibt auch nach Ergänzung aller fehlenden Intervalle bestehen. Ein angehängtes Nullatom v=0 erzeugt hier keine zusätzliche Materiezeile und liefert keine aktive Fortsetzung.'))
add(p('Zwei zusätzliche positive Zukunftselemente','sub'),p('Für drei freie Uhren t&lt;u&lt;z und positive Dichten w,v,r erzwingen die letzten beiden Uhrgleichungen:'))
add(code(['u = 9t-32/3;   4/3<t<16/3', 'C_g = H(t) = -17t²/2+176t/3-173/3', 'H(4/3)=49/9;   H(16/3)=121/9']))
add(p('H ist konkav und liegt im ganzen notwendigen Intervall über seiner positiven Verbindungsgeraden. Die Normierungsbedingung C_g=0 kann daher ebenfalls nicht erfüllt werden.'))
add(p('Was ausgeschlossen ist','sub'),p('Genau diese positive Fortsetzung mit eingefrorenem Kragen, der festen Kettenordnung und freien inneren Uhr-/Dichtevariationen. Andere Kragen, längere Zukunft, andere Ordnungen oder andere physikalisch begründete Variationsklassen sind damit nicht ausgeschlossen.'))

page('04  /  POSITIVKONTROLLE','Eine exakte gemeinsame Lösung existiert')
add(p('Für einen veränderten äußeren Kragen wird die gekoppelte Wirkung explizit lösbar. Die folgenden Daten sind ein konstruierter Existenzzeuge, keine unabhängig vorhergesagte Präparation.'))
add(code(['R=√305;   k=(70-4R)/3 > 0', '(T0,T1,T2,T3)=(-R/6,-5/2,-2,-4/3)', 'C_f=k t;   C_g=-ut+t²/2', 'S_d = t(vu-wk)/2 - v t²/4']))
add(p('Für beliebige 0&lt;w,v&lt;1 sind beide inneren Normierungen und beide Uhrgleichungen exakt erfüllt durch:'))
add(code(['t=0;   u=k w/v > 0', 'q_f^links = -wk/2', 'q_f^Zukunft = vu/2 = wk/2', 'q_f^gesamt = 0']))
add(p('Die getrennten Reaktionen verschwinden nicht. Sie tragen gemeinsam den Anschluss aus derselben Wirkung. Bei w=v=1/2 ist u=k≈0,0476677 in reduzierten Modelleinheiten; geprüft wird exakt in Q(√305).'))
add(p('Was weiterhin getragen werden muss','sub'))
add(code(['Σ_aussen q_y = 0', 'Σ_aussen T_y q_y = w+v > 0', 'Rang der inneren Hesse-Matrix = 2']))
add(p('Die äußere Reaktion verschwindet nicht. Es bleibt eine stationäre Familie mit flachen Richtungen und einem Sattel, kein isoliertes Minimum. Bereits eine kleine alleinige Änderung von T₀ verletzt im Allgemeinen die Normierung. Eine robuste oder physikalisch ausgewählte Randpräparation ist damit nicht gezeigt.'))

page('05  /  PRÜFUNG UND NÄCHSTER SCHRITT','Exakte Kontrollen und klare Grenzen')
add(table([['Kontrolle','Umfang / Ergebnis'],['Natürliche Ordnungen / Überdeckungen','50 / 3350'],['Materie- / gravitative Identitäten','6700 / 3350, jeweils PASS'],['Reaktionskomponenten','26388, PASS'],['Kettenüberlappungen','95, PASS; Gegenbeispiel außerhalb der Kettenklasse'],['Eingefrorener Kragen','81 Fälle; analytischer Zwei-Zukunfts-Ausschluss'],['Neuer stationärer Kragen','27 Fälle, 108 Ableitungen, 432 Hesse-Komponenten, PASS'],['Konkrete Negativkontrollen','8 erwartete Ausschlüsse']], [270,205]))
add(Spacer(1,11),p('Vier Ergebnisdateien werden isoliert bytegleich reproduziert. Alle wissenschaftlichen Kontrollen laufen mit der Python-Standardbibliothek, rationaler Arithmetik und Q(√305). Die kleinen Kettentests sind keine n=5-Produktionsintegration.'))
add(code(['python3 -O -B verify_package.py', 'python3 -O -B replay.py']))
add(p('Nächster Schritt','sub'),p('Die gemeinsam zulässigen Kragendaten klassifizieren und unabhängige Randstörungen prüfen. Dabei ist festzustellen, welche Bedingungen die Vorgeschichte erfüllen muss und welche äußeren Reaktionen verbleiben. Die neuen Werte dürfen nicht nachträglich als physikalische Vorhersage ausgegeben werden.'))
add(p('Quellen und Einordnung','sub'))
for title,url in [
 ('Projekt PR 268 und geerbte Variationsarbeit: ursprüngliche Wirkung, disjunkte Verklebung und Variationsstrom; vier Quellen unverändert im Paket.','https://github.com/thomasmgfeller/x6-spectral-astrolabium/pull/268'),
 ('Dittrich und Höhn (2013), Constraint analysis for variational discrete systems: Kontext für aktionsbasierte diskrete Impulsabgleiche.','https://arxiv.org/abs/1303.4294'),
 ('Benincasa und Dowker (2010), The Scalar Curvature of a Causal Set: Hintergrund der Operatorgewichte, keine Herleitung dieser Staubpräparation.','https://arxiv.org/abs/1001.2725')
]:add(p('<link href="'+url+'" color="#16756F">'+escape(title)+'</link>','small'))
add(p('Plan nach analytischem Entwurf vor den endlichen Kontrollen gehasht. Keine externe Präregistrierung oder Replikation. Kein physikalischer Vakuum-Außenraum, keine Geometrie-Rückwirkung, kein Bounce. Alle acht Gates bleiben HOLD.','small'))
def footer(c,doc):
    c.saveState();w,h=doc.pagesize
    c.setStrokeColor(TEAL);c.setLineWidth(1);c.line(60,49,w-60,49)
    c.setFont('DV',7.5);c.setFillColor(MUTED)
    c.drawString(60,34,'CST-DUST · Zweiblock-Kopplung v0.1 · 08.11.2026')
    c.drawRightString(w-60,34,f'{doc.page} / 6')
    c.restoreState()
def invariant_canvas(*a,**kw): kw['invariant']=1;return canvas.Canvas(*a,**kw)
out=ROOT/'CST_DUST_Zweiblock_Kopplung_Randreaktion_v0_1.pdf'
doc=SimpleDocTemplate(str(out),pagesize=(595.2756,841.8898),rightMargin=60,leftMargin=60,topMargin=48,bottomMargin=65,title='CST-DUST: Zweiblock-Kopplung und gemeinsame Randreaktion v0.1',author='Thomas Gfeller · Forschungsprojekt mit ChatGPT')
doc.build(story,onFirstPage=footer,onLaterPages=footer,canvasmaker=invariant_canvas)
print(out)
