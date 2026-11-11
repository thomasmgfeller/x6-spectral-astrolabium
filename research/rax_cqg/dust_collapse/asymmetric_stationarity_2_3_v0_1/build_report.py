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

class OrderDiagram(Flowable):
    def __init__(self):Flowable.__init__(self);self.width=475;self.height=173
    def draw(self):
        c=self.canv
        def box(x,y,w,label):
            c.setFillColor(LIGHT);c.setStrokeColor(TEAL);c.roundRect(x,y,w,23,4,fill=1,stroke=1)
            c.setFillColor(NAVY);c.setFont('DV',9);c.drawCentredString(x+w/2,y+7,label)
        def line(x,y,xx,yy):
            c.setStrokeColor(TEAL);c.setLineWidth(1.1);c.line(x,y,xx,yy)
            c.setFillColor(TEAL);c.circle(xx,yy,2.1,stroke=0,fill=1)
        box(137,146,200,'Fester Kragen: a < b < c < d')
        box(94,106,90,'e');box(94,52,90,'f')
        box(291,108,90,'g');box(291,74,90,'h');box(291,40,90,'i')
        box(147,1,180,'Freier Endpunkt j: U, r')
        line(193,146,139,129);line(280,146,336,131);line(139,106,139,75)
        line(336,108,336,97);line(336,74,336,63)
        line(139,52,196,24);line(336,40,280,24)

add(p('FORSCHUNGSNOTIZ  08.11.2026  /  VERSION 0.1','kicker'),p('Vollständige<br/>Asymmetrieprüfung (2,3)','title'))
add(p('Ein Uhrzeuge lässt sich nicht zur stationären Lösung ergänzen','sub'),p('Die Astlängen zwei und drei bestanden die frühere Prüfung der einzelnen Endpunkt-Uhrgleichung. Die vollständigen inneren Variationsgleichungen schließen diese feste Klasse jetzt aus. Der Beweis gilt für alle zulässigen Randuhren, einschließlich des besonderen Kragenfalls P=0.'))
add(OrderDiagram(),Spacer(1,6),p('Zwei kausal unvergleichbare Ketten treffen auf j. Die Linien laufen von älteren zu jüngeren Ereignissen nach unten. Die vier Kragenereignisse sind zusammengefasst; sämtliche transitiven Relationen werden mitgerechnet.','small'))
add(code(['Notwendige Teilgleichungen erzwingen:', 'C_j > 1 + (87/32)(h-g)² > 1', 'Freie Endpunkt-Dichtevariation verlangt: C_j = 0']))
add(p('Gültigkeitsbereich','sub'),p('Zehn Ereignisse, sechs freie innere Uhren und sechs freie positive Dichten in (0,1). Vier feste äußere Uhren tragen Dichte-Nullzeilen. Uhren steigen entlang kausaler Relationen strikt. Der gemeinsame Endpunkt ist frei und hat keine Nachfolger. Die ursprüngliche Wirkung bleibt unverändert.'))
add(p('<b>Alle acht physikalischen Gates bleiben HOLD.</b> Kein allgemeines CST- oder Asymmetrieverbot, keine physikalische Randpräparation, kein Bounce. Keine kostenpflichtige Rechnung und kein n=5-Produktionslauf.','small'))
add(p('Quelle: PR 272, Main c544521e4db792b9d01b083378a2cba5879a8a59. Vollständige Herleitung und reproduzierbare exakte Kontrollen im Prüfpaket.','small'))

page('01  /  VOLLSTÄNDIGES VARIATIONSSYSTEM','Sechs Normen und sechs Uhrgleichungen')
add(p('Bei B(k)=(1,-9,16,-8,0,...) gilt S_d=-Σw_x C_x/2 mit C_x=1+ΣB_yx(T_x-T_y)²/2. Alle Intervalle werden in der globalen Ordnung gezählt. Die feste gravitative Wirkung besitzt hier keine Uhr- oder Dichteableitung.'))
add(code(['P=-8a+16b-9c+d', 'A=1+(-8a²+16b²-9c²+d²)/2', 'P_e=-8b+16c-9d+e;  P_g=-8b+16c-9d+g', 'A_e=1+(-8b²+16c²-9d²+e²)/2', 'A_g=1+(-8b²+16c²-9d²+g²)/2', 'Q=-8c+16d-9g+h', 'B=1+(-8c²+16d²-9g²+h²)/2', 'L=9e-f-16g+9h-i', 'M=-9e²+f²+16g²-9h²+i²']))
add(p('Freie Dichtevariationen: alle rechten Seiten sind null','sub'))
add(code(['C_e=A-P·e;   C_f=A_e-P_e·f', 'C_g=A-P·g;   C_h=A_g-P_g·h', 'C_i=B-Q·i;   C_j=1+U·L+M/2']))
add(p('Freie Uhrvariationen: alle rechten Seiten sind null','sub'))
add(code(['2q_e=w_e·P+w_f(f-e)-9r(U-e)', '2q_f=w_f·P_e+r(U-f)', '2q_g=w_g·P+w_h(h-g)-9w_i(i-g)+16r(U-g)', '2q_h=w_h·P_g+w_i(i-h)-9r(U-h)', '2q_i=w_i·Q+r(U-i)', '2q_j=-r·L']))
add(p('Spätere Materiezeilen tragen zu früheren Uhrableitungen bei. Eine nur zeilenweise Uhrvariation würde wesentliche Terme verlieren. Äußere Uhrreaktionen werden nicht auf null gesetzt: Der Kragen ist fest.','small'))

page('02  /  ENDPUNKT UND REGULÄRER KRAGEN','Ein positiver Normrest ist unvermeidbar')
add(p('Die globalen Endpunktgewichte sind e:-9, f:1, g:16, h:-9, i:1. Die vier Kragengewichte sind null. Weil r positiv ist, setzt q_j=0 den Ausdruck L auf null.'))
add(code(['t=f-e>0,  v=h-g>0,  w=i-h>0,  s=g-e', 'L=0  ⇒  s=v-(t+w)/8', 'C_j=1+(9t²+7w²)/16+2vw-8v²']))
add(p('Der Kragen teilt die Prüfung in genau zwei Fälle','sub'),p('Die ersten Normgleichungen liefern C_e-C_g=P(g-e)=0. Für P ungleich null müssen die beiden ersten Astuhren gleich sein. Das identifiziert die Ereignisse nicht und erzeugt keine neue Kausalrelation.'))
add(code(['P≠0  ⇒  e=g  ⇒  s=0  ⇒  t+w=8v', 'C_j=1+(w-7v/2)²+(63/4)v² > 1']))
add(p('Damit scheitert der gesamte reguläre Kragenfall an C_j=0, unabhängig von den weiteren inneren Dichten. Der Sonderfall P=0 wird auf der folgenden Seite ohne Division durch P behandelt.'))
add(p('Eine gemeinsame konservative Schranke','sub'))
add(code(['9t²+7w²-(7/2)(t+w)²', '  =(7/2)(t-w)²+2t² ≥ 0', 't+w>7v  ⇒  C_j > 1+(87/32)v²']))
add(p('Die Schranke ist nicht als scharf beansprucht. Sie reicht aus, um die exakte Endpunkt-Normgleichung auszuschließen. Für nur ungefähr erfüllte Teilgleichungen ist damit noch kein zertifiziertes Restfehlerbudget abgeleitet.'))

page('03  /  BESONDERER KRAGEN','Auch P=0 lässt keine Lösung offen')
add(p('Bei P=0 verlangen die ersten Normen zusätzlich A=0. Der folgende Widerspruch benötigt A=0 nicht einmal. Setze K=8b-16c+9d, γ=K-e und u=U-f>0.'))
add(code(['q_f=0  ⇒  w_f·γ=r·u  ⇒  γ>0', 'q_e=0  ⇒  w_f·t=9r(u+t)', 'u(t-9γ)=9γt  ⇒  t>9γ']))
add(p('Für s≤0 liefert die Endpunkt-Uhrgleichung sofort t+w≥8v>7v. Es bleibt s>0. Aus der notwendigen Gleichheit C_f=C_h folgt nach Subtraktion:'))
add(code(['γ(v+s-t)=s(v+s/2)', 'v+s-t>0', 'γ=s·(v+s/2)/(v+s-t)']))
add(p('Der Quotient ist größer als 1/2, denn 2(v+s/2)-(v+s-t)=v+t>0. Also γ>s/2. Zusammen mit t>9γ folgt t>9s/2>s/2. Der Quotient ist damit sogar größer als eins: Die Differenz seines Zählers und Nenners beträgt t-s/2>0.'))
add(code(['γ>s  ⇒  t>9s', 't<v+s  ⇒  v>8s', 't+w=8(v-s)>7v', 'C_j > 1+(87/32)v² > 1']))
add(p('<b>Beide Kragenfälle sind geschlossen.</b> Eine notwendige Teilmenge der Gleichungen widerspricht der Endpunkt-Normierung. Deshalb können auch die übrigen vollständig hergeleiteten Uhrgleichungen und C_i=0 keine gemeinsame stationäre Lösung herstellen.'))
add(p('Verwendete notwendige Teilmenge: C_e=C_g, C_f=C_h und q_e=q_f=q_j=0, gemeinsam mit der strikten Domäne. Die einzelnen Normen müssen für diese Teilprüfung noch nicht null sein. Der Beweis schließt (2,3) aus; ein vollständiger Asttausch überträgt ihn auf (3,2).','small'))

page('04  /  EINORDNUNG UND GRENZEN','Acht Astlängenfelder sind jetzt ausgeschlossen')
add(table([['p / q','1','2','3','≥4'],['1','Familie bekannt','ausgeschlossen','ausgeschlossen','offen'],['2','ausgeschlossen','ausgeschlossen','neu ausg.','offen'],['3','ausgeschlossen','neu ausg.','ausgeschlossen','offen'],['≥4','offen','offen','offen','offen']], [55,105,105,105,105]))
add(Spacer(1,12),p('Die sechs früheren Ausschlüsse folgten aus der Endpunkt-Uhrgleichung. Hinzu kommen nun (2,3) und (3,2). Für (1,1) ist aus PR 271 eine stationäre Familie bei passenden Kragenwerten bekannt. Sieben Felder bleiben für vollständige Stationarität offen.'))
add(p('Die Sammelklasse ≥4 umfasst viele endliche Längen. Ihre Uhrzeugen aus PR 272 sind weiterhin keine vollständigen stationären Lösungen. Eine neue Ordnung muss wieder global gezählt und vollständig variiert werden.','small'))
add(p('Wann ein anderes Variationsproblem vorliegt','sub'))
add(table([['Änderung','Konsequenz'],['U festgehalten','q_j=0 ist dort keine innere Gleichung.'],['Zusätzliche Nachfolger','Spätere Zeilen ändern die Uhrableitungen.'],['Dichte null oder fest','Variationsdomäne und Randbedingungen neu festlegen.'],['Nur kleine Gleichungsreste','Fehlerbudget fehlt; exakter Satz reicht nicht.']], [175,300]))
add(Spacer(1,10),p('Bei r=0 fällt zwar -rL/2 weg; eine weiterhin freie Dichtevariation verlangt dennoch -C_j/2=0. Ob eine solche Variation am Rand zugelassen ist, muss gesondert entschieden werden. Keine der Änderungen wird als bewiesene Reparatur ausgegeben.'))
add(p('Physikalische Aussage bleibt begrenzt','sub'),p('Keine Auswahl der Materiewirkung aus einer vollständigen CST-Amplitude, keine hergeleitete Randpräparation, kein Vakuum-Außenraum, keine Geometrie-Rückwirkung, keine dynamische Stabilität und kein Bounce. Alle acht physikalischen Gates bleiben HOLD.'))

page('05  /  EXAKTE VERIFIKATION','Beweis und Reproduktion sind getrennt prüfbar')
summary=json.loads((ROOT/'results/verification.json').read_text())
add(table([['Kontrolle','Ergebnis'],['Vollständige Polynomidentitäten',str(summary['symbolic_identities'])],['Streng geordnete rationale Profile','1.458'],['Unabhängige Uhrableitungen','8.748'],['Unabhängige Dichteableitungen','8.748'],['Bedingte Zeugen für P=0','9; keine vollständigen Lösungen'],['Kontrollen für e=g','27'],['Negativkontrollen','6'],['Asttausch','Wirkung und 10 Gleichungskomponenten']], [275,200]))
add(Spacer(1,10),p('Die Kontrollen verwenden exakte rationale Zahlen und die Python-Standardbibliothek. Die zentralen Wirkungsdifferenzen sind bei quadratischer Uhr- und linearer Dichteabhängigkeit exakt. Die allgemeinen Ausschlüsse folgen aus den Beweisen, nicht aus einer numerischen Stichprobe.'))
add(p('Die neun bedingten Zeugen erfüllen P=0, q_e=q_f=q_j=0 und C_f=C_h. Ihre Normen sind aber nicht null. Damit wird die Teilprüfung nachvollziehbar, ohne einen solchen Zeugen zu einer vollständigen Lösung aufzuwerten.'))
add(code(['python3 -O -B verify_package.py', 'python3 -O -B replay.py']))
add(p('Vier Ergebnisdateien werden isoliert bytegleich reproduziert. Der Plan wurde nach dem ersten analytischen Fallentwurf vor den endlichen Kontrollen fixiert; keine externe Präregistrierung oder unabhängige Replikation.','small'))
add(p('Nächster mathematischer Schritt','sub'),p('Die kleinste noch offene konkrete asymmetrische Ordnung (1,4) auf sämtliche Norm- und Uhrgleichungen prüfen. Das sollte vor einem freiwilligen Community-Rechenlauf geschehen. Ein neuer Produktionslauf wurde nicht gestartet.'))
add(p('Projektquellen','sub'),p('<link href="https://github.com/thomasmgfeller/x6-spectral-astrolabium/pull/272" color="#16756F">PR 272: Asymmetrie und Endpunktkriterium</link><br/><link href="https://github.com/thomasmgfeller/x6-spectral-astrolabium/pull/271" color="#16756F">PR 271: Verzweigung und Wiederanschluss</link>','small'))
add(p('Neue eigene Rechnung innerhalb der geerbten Wirkung. MODEL, BOUNDARY, CURRENT, CORRESPONDENCE, EXTENSION, TRAPPING, REGULARITY und BOUNCE: jeweils HOLD.','small'))

def footer(c,doc):
    c.saveState();w,h=doc.pagesize;c.setStrokeColor(TEAL);c.setLineWidth(1);c.line(60,49,w-60,49);c.setFont('DV',7.2);c.setFillColor(MUTED);c.drawString(60,34,'CST-DUST · Vollständige Asymmetrieprüfung (2,3) v0.1 · 08.11.2026');c.drawRightString(w-60,34,f'{doc.page} / 6');c.restoreState()
def invariant_canvas(*a,**kw):kw['invariant']=1;return canvas.Canvas(*a,**kw)
out=ROOT/'CST_DUST_Vollstaendige_Asymmetriepruefung_2_3_v0_1.pdf'
doc=SimpleDocTemplate(str(out),pagesize=(595.2756,841.8898),rightMargin=60,leftMargin=60,topMargin=48,bottomMargin=65,title='CST-DUST: Vollständige Asymmetrieprüfung (2,3) v0.1',author='Thomas Gfeller · Forschungsprojekt mit ChatGPT')
doc.build(story,onFirstPage=footer,onLaterPages=footer,canvasmaker=invariant_canvas)
print(out)

