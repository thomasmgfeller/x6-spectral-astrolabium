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
add(p('FORSCHUNGSNOTIZ  08.11.2026  /  VERSION 0.1','kicker'),p('Zulässige Randdaten und<br/>Störungsgrenzen','title'),p('Die Zweiblock-Lösung ist jetzt vollständig klassifiziert','sub'))
add(p('Für die feste Sechserkette sind zwei unabhängige Bedingungen an die vier äußeren Uhren notwendig und hinreichend. Zusammen mit strikter zeitlicher Ordnung bestimmen sie genau, wann zwei positive freie Materiezeilen gemeinsam stationär sein können.'))
add(table([['Ergebnis','Bedeutung'],['Zwei Gleichheiten plus Vorzeichen','Vollständige Existenzbedingung in der erklärten Klasse'],['Zweidimensionale Randfläche','Eine Form und eine gemeinsame Uhrverschiebung'],['Unabhängige Einzelstörungen','Keine Reparatur durch Neuwahl der inneren Werte'],['Korrelierte Randänderungen','Lösungen bleiben entlang der zulässigen Fläche erhalten'],['Berechenbare Restfehlergrenzen','Notwendige Toleranzprüfung bei Dichteboden und begrenztem Zukunftsabstand']], [215,260]))
add(Spacer(1,12),p('Was sich gegenüber PR 269 geklärt hat','sub'),p('Der frühere exakte Zeuge ist Teil einer vollständig beschriebenen Familie. Er ist weiterhin keine physikalisch ausgewählte Präparation. Die äußere Reaktion bleibt erforderlich; sie ist nun für die ganze Familie explizit bestimmt.'))
add(code(['Geprüft: endliche Kette und gemeinsame Stationarität', 'Nicht hergeleitet: physikalische Randpräparation', 'Alle acht physikalischen Gates: HOLD']))
add(p('Die vier äußeren Materiezeilen sind in dieser Klasse null. Die beiden inneren Gewichte liegen frei in (0,1). Kein Vakuum-Außenraum, keine Geometrievariation, kein Bounce. Keine kostenpflichtige Rechnung und kein n=5-Produktionslauf.','small'))
add(p('Basis: Main adb6ea2de0dc56417da3493e8aabf8903981090f nach PR 269. Vollständige Beweise, Quellidentitäten und Reproduktionscode im Prüfpaket.','small'))

page('01  /  EXISTENZSATZ','Vier Bedingungen entscheiden die ganze Klasse')
add(p('Die vier festgehaltenen äußeren Uhren heißen a&lt;b&lt;c&lt;d. Gesucht werden d&lt;t&lt;u und frei variierte Gewichte 0&lt;w,v&lt;1. Die unveränderte Materiewirkung lautet S=-(w C_f+v C_g)/2.'))
add(code(['P = -8a+16b-9c+d', 'A = 1+(-8a²+16b²-9c²+d²)/2', 't_* = 8b-16c+9d', 'D = 1+(-8b²+16c²-9d²)/2', 'E = D+t_*²/2;   F = A-P t_*']))
add(p('Die vollständigen Zeilen der ursprünglichen Wirkung vereinfachen sich zu:'))
add(code(['C_f = A-Pt', 'C_g = D+t²/2-(t-t_*)u', 'q_u = v(t-t_*)/2', 'q_t = [wP+v(u-t)]/2']))
add(p('Weil v positiv ist, erzwingt q_u=0 den Wert t=t_*. Die beiden Normierungen sind dort genau F und E. Die letzte Uhrgleichung bestimmt den zweiten inneren Wert.'))
add(code(['Existenz genau dann, wenn:', 'E=0,   F=0,   t_*>d,   P<0', 'Dann für jedes 0<w,v<1:', 't=t_*;   u=t_*-(w/v)P']))
add(p('Dies ist notwendig und hinreichend. Zusätzliche innere Variablenwahl kann eine Verletzung von E=0 oder F=0 nicht ausgleichen. Der Null-Dichte-Zweig und andere Kausalordnungen sind nicht Teil dieses Satzes.'))

page('02  /  VOLLSTÄNDIGE FAMILIE','Ein Formparameter und eine Verschiebung')
add(p('Mit x=c-b, s=(d-c)-(c-b) und z=b-a lauten die ersten Bedingungen t_*=d+8s, P=8z-7x+s und E=1-8x²+36s². Die strikte Zukunftsordnung verlangt s&gt;0.'))
add(code(['Z = √[(71x²+414xs+559s²)/8]', 'z = Z-2x-9s', 'P<0 ⇔ 39x²+46xs-569s²<0']))
add(p('Der positive Quadratwurzelzweig ist durch die äußere Reihenfolge eindeutig. Der andere Zweig ist unzulässig. Setze r=s/x; dann liefert die folgende Parametrisierung sämtliche zulässigen Kragen:'))
add(code(['r₀ = (23+8√355)/569', 'r₀ < r < √2/3', 'x = 1/√(8-36r²);   s=r x', 'z = x{√[(71+414r+559r²)/8]-2-9r}', 'd=λ;   c=λ-x-s;   b=λ-2x-s;   a=b-z']))
add(p('λ ist eine beliebige gemeinsame Uhrverschiebung. Der Zeuge aus PR 269 liegt bei r=1/3 und λ=-4/3: x=1/2, s=1/6 und a=-√305/6.'))
add(p('Warum zwei Bedingungen wirklich unabhängig sind','sub'),p('Es gilt ∂aE=0, aber ∂aF=8(t_*-a)&gt;0 und ∂bE=16x+72s&gt;0. Der Jacobi-Rang von (E,F) ist deshalb überall zwei. Die Randfläche besitzt Dimension zwei und enthält keine offene vierdimensionale Umgebung.'))
add(p('Am unteren Formrand wird P=0 und damit u=t; die strikte Ordnung endet. Zur oberen Grenze wachsen die vergangenen Abstände unbeschränkt. Das sind Grenzen dieser Parametrisierung in festen Modelleinheiten, keine hergeleiteten physikalischen Singularitäten.','small'))

page('03  /  STÖRUNGSPRÜFUNG','Neue innere Werte reparieren beliebige Randfehler nicht')
add(p('Für jeden gestörten Kragen wird t_* neu berechnet. Die Prüfung erlaubt danach jede Neuwahl von u,w,v innerhalb der erklärten Klasse. Trotzdem müssen E=F=0 gelten. Die inneren Werte werden also nicht künstlich eingefroren.'))
add(p('Einzelstörungen des Zeugen aus PR 269','sub'),p('Wird jeweils nur eine äußere Uhr um ε verschoben, ergeben sich die folgenden exakten Hindernisse:'))
add(table([['Geänderte Uhr','Verbleibendes Hindernis'],['a','F=(4√305/3)ε-4ε²; E=0'],['b','E=20ε+28ε²'],['c','E=-32ε+136ε²'],['d','E=12ε+36ε²']], [100,375]))
add(Spacer(1,12),p('Für ε=±10⁻³, ±10⁻⁴ und ±10⁻⁵ bleiben die strikte Reihenfolge sowie t_*&gt;d und P&lt;0 erhalten. In allen 24 Fällen ist aber mindestens eine Gleichheit verletzt. Es existiert dann keine exakte gemeinsame innere Lösung.'))
add(p('Welche Störungen weiterhin zulässig sind','sub'),p('Eine gemeinsame Verschiebung sämtlicher Uhren erhält alle Abstände und Gleichungen. Auch korrelierte Änderungen des Formparameters auf der Randfläche bleiben zulässig. Gezeigt ist fehlende offene Robustheit gegenüber unabhängigen Randfehlern, kein allgemeines Störungsverbot.'))
add(code(['Für zwei zulässige Kragen, bei festem ρ=w/v:', '|δt| ≤ 33ε', '|δu| ≤ (33+34ρ)ε', 'wenn max|δ(a,b,c,d)| ≤ ε']))
add(p('Diese Sensitivitätsgrenze gilt entlang der Fläche. Ohne obere Grenze für das Dichteverhältnis wird sie nicht uniform. Sie ist keine Aussage über dynamische Stabilität einer Kollapsentwicklung.','small'))

page('04  /  REAKTION UND FEHLERBUDGET','Die äußere Aufgabe bleibt quantitativ sichtbar')
add(p('Für jeden zulässigen Kragen sind die äußeren Reaktionen durch die beiden unabhängigen Normalrichtungen der Fläche bestimmt:'))
add(code(['q_aussen = -(w ∇F+v ∇E)/2', 'q_a = -4w(t_*-a) < 0', 'Σ_aussen q_i=0;   Σ_aussen T_i q_i=w+v>0']))
add(p('Die Reaktionen verschwinden auf Tangentialvariationen, aber nicht als Vektor. Die positiven Gewichte sind weiterhin frei. Eine physikalische Vorgeschichte müsste die Randdaten und diese Reaktionen erklären. Andere feste Vergangenheitswirkungen können zusätzliche äußere Beiträge liefern.'))
add(p('Notwendige Schranken bei endlicher Genauigkeit','sub'),p('Setze η=t-t_* und g=u-t. Für beliebige Randdaten gelten exakt F=C_f+Pη und E=C_g+ηg+η²/2, mit q_u=vη/2. Unter v≥v_min&gt;0 und 0&lt;g≤G folgt:'))
add(code(['|F| ≤ |C_f| + 2|P||q_u|/v_min', '|E| ≤ |C_g| + 2G|q_u|/v_min', '                + 2|q_u|²/v_min²']))
add(p('Übersteigen die Randhindernisse diese Grenzen bei vorgegebenen Resttoleranzen, ist eine Lösung innerhalb des Budgets ausgeschlossen. Das Bestehen der Prüfung ist nur notwendig; weitere Gleichungen müssen ebenfalls erfüllt sein.'))
add(p('Wozu die zusätzlichen Budgetannahmen dienen','sub'),p('Der Dichteboden verhindert, dass ein kleines Gewicht einen großen Normierungsfehler verdeckt. Die Zeitgrenze G begrenzt die Verstärkung eines Uhrrestes. Beide sind erklärte Budgetannahmen, keine physikalischen Vorhersagen. 432 rationale Fälle prüfen die Grenzen mit v_min=1/4 und G=1.'))

page('05  /  VERIFIKATION UND WEITERARBEIT','Die Randbedingungen sind geklärt, ihre Herkunft bleibt offen')
add(table([['Kontrolle','Ergebnis'],['Symbolische Polynomidentitäten','16 vollständige Koeffizientenvergleiche'],['Parametrisierte Kragen','21: 12 zulässig, 9 chronologisch ausgeschlossen'],['Gemeinsame stationäre Fälle','108, jeweils beide Normen und beide Uhrgleichungen'],['Unabhängige Randableitungen','168'],['Unabhängige Randstörungen','24 exakte Ausschlüsse bei neu berechnetem t_*'],['Restfehlerbudgets','432 Fälle; 1296 exakte Identitätsprüfungen'],['Gemeinsame Uhrverschiebungen','108 erhaltene Lösungen'],['Negativkontrollen','6 zurückgewiesene Annahmen']], [265,210]))
add(Spacer(1,10),p('Alle Kontrollen bestehen exakt mit rationaler Arithmetik und quadratischen Zahlkörpern. Die allgemeinen Aussagen folgen aus den Beweisen; die endlichen Kontrollen ergänzen sie. Vier Ergebnisdateien werden isoliert bytegleich reproduziert.'))
add(code(['python3 -O -B verify_package.py', 'python3 -O -B replay.py']))
add(p('Nächster sinnvoller Schritt','sub'),p('Einen kleinen verzweigten Rand-/Zukunftsblock vorab definieren und seine vollständige Intervallkopplung sowie Randbedingungen ableiten. Eine physikalische Vorgeschichte müsste erklären, warum ihre Randwerte auf der zulässigen Fläche liegen. Nachträgliches Einstellen auf E=F=0 ist keine Vorhersage.'))
add(p('Quellen und Grenzen','sub'))
for title,url in [('Projekt PR 269: unveränderte Wirkung, Zweiblock-Zeuge und unabhängiger Referenzcode; Quellidentitäten im Paket.','https://github.com/thomasmgfeller/x6-spectral-astrolabium/pull/269'),('Dittrich und Höhn (2013), Constraint analysis for variational discrete systems: methodischer Kontext, keine physikalische Validierung dieses Kandidaten.','https://arxiv.org/abs/1303.4294v3')]:
    add(p('<link href="'+url+'" color="#16756F">'+escape(title)+'</link>','small'))
add(p('Plan nach analytischem Entwurf vor dem endlichen Kontrolllauf gehasht. Keine externe Präregistrierung, externe Replikation oder Beweisassistentenprüfung. Alle acht physikalischen Gates bleiben HOLD.','small'))

def footer(c,doc):
    c.saveState();w,h=doc.pagesize;c.setStrokeColor(TEAL);c.setLineWidth(1);c.line(60,49,w-60,49)
    c.setFont('DV',7.5);c.setFillColor(MUTED);c.drawString(60,34,'CST-DUST · Randdaten und Störungsgrenzen v0.1 · 08.11.2026');c.drawRightString(w-60,34,f'{doc.page} / 6');c.restoreState()
def invariant_canvas(*a,**kw):kw['invariant']=1;return canvas.Canvas(*a,**kw)
out=ROOT/'CST_DUST_Randdaten_Klassifikation_Stoerungsgrenzen_v0_1.pdf'
doc=SimpleDocTemplate(str(out),pagesize=(595.2756,841.8898),rightMargin=60,leftMargin=60,topMargin=48,bottomMargin=65,title='CST-DUST: Zulässige Randdaten und Störungsgrenzen v0.1',author='Thomas Gfeller · Forschungsprojekt mit ChatGPT')
doc.build(story,onFirstPage=footer,onLaterPages=footer,canvasmaker=invariant_canvas)
print(out)
