"""Generate the German report from the checked numerical results."""
from pathlib import Path
from xml.sax.saxutils import escape
import json
import math
from reportlab.pdfgen.canvas import Canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib.colors import HexColor
from reportlab.lib.styles import ParagraphStyle
from reportlab.platypus import Paragraph
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

ROOT=Path(__file__).resolve().parent
for label,file in [('Body','DejaVuSans'),('Strong','DejaVuSans-Bold'),('Book','DejaVuSerif')]:
    pdfmetrics.registerFont(TTFont(label,'/usr/share/fonts/truetype/dejavu/'+file+'.ttf'))
import sys
dest=Path(sys.argv[1]) if len(sys.argv)>1 else ROOT/'Bericht.pdf'
c=Canvas(str(dest),pagesize=A4); c.setTitle('CST-DUST · Fünf Prozent auf dem vollständigen N14-Träger')
W,H=A4;left=49;right=W-49;avail=right-left
dark='#153e49';green='#09685b';muted='#4e6570';fg='#222e31'
def tx(x,y,s,font='Body',size=10,color=fg):
    c.setFillColor(HexColor(color));c.setFont(font,size);c.drawString(x,y,s)
def line(y):
    c.setStrokeColor(HexColor('#c7d7d9'));c.line(left,y,right,y)
def start(i,section,heading):
    global y
    tx(left,H-39,'CST-DUST    /    ETAPPE 1', 'Strong',9,green)
    c.setFont('Body',9);c.drawRightString(right,H-39,'19. November 2026')
    line(H-49)
    tx(left,H-82,section,'Strong',9,green)
    tx(left,H-118,heading,'Book',22,dark);y=H-143
    line(46);tx(left,30,'N11–N14   ·   Erweiterungsstabilität v0.6','Body',8,muted)
    c.drawRightString(right,30,f'{i} / 3')
def body(s):
    global y
    p=Paragraph(escape(s),ParagraphStyle('body',fontName='Body',fontSize=10.2,leading=15.2,textColor=HexColor(fg)))
    _,height=p.wrap(avail,700);p.drawOn(c,left,y-height);y-=height+10
def sub(s):
    global y
    y-=9;tx(left,y,s,'Strong',12,dark);y-=8
def key(s,t):
    global y
    c.setFillColor(HexColor('#e8f3ef'));c.roundRect(left,y-56,avail,54,5,fill=1,stroke=0)
    tx(left+13,y-23,s,'Strong',12,green);tx(left+13,y-42,t,'Body',10,fg);y-=74
def table(rows,widths,fontsize=9):
    global y
    for k,row in enumerate(rows):
        if k==0:
            c.setFillColor(HexColor('#e4eff0'));c.rect(left,y-23,avail,23,fill=1,stroke=0)
        x=left+7
        for j,s in enumerate(row):
            tx(x,y-15,s,'Strong' if k==0 else 'Body',fontsize,dark if k==0 else fg);x+=widths[j]
        y-=24
    line(y);y-=13
def end():
    assert y>52,y;c.showPage()
results=json.loads((ROOT/'result.json').read_text()); refined=json.loads((ROOT/'refined.json').read_text())
start(1,'BEFUND','Fünf Prozent halten auf dem N14-Träger')
body('Beide N11-Ausgangshistorien dürfen je fünf Prozent ihres Amplitudengewichts auf erreichbare Nachkommen übertragen. Für jede zulässige Aufteilung hält die kohärente Auslese auf beiden geprüften Quadraturgittern alle drei ursprünglichen Toleranzen ein.')
key('Bis 5,0210 % bestehen alle Aufteilungen.','Bei 5,0211 % verletzt eine konkrete Mischung die Niveautoleranz.')
sub('Ergebnis für den festen Detektor')
body('Der Erfolg umfasst die drei akzeptierten Ausgänge. Der vierte Ausgang erfasst den Fehlschlag. Die Schranken sind für beide Gitter nach aussen gerundet.')
table([['Prüfgrösse','Bei 5,0000 %','Bis 5,0210 %'],['Erfolg relativ zu N11, Dichte 1/8, mindestens','90,04077 %','90,00027 %'],['Erfolg relativ zu N11, Dichte 1/4, mindestens','90,04051 %','90,00001 %'],['Änderung des vierteiligen Kontrasts, höchstens','17,513 %','17,613 %'],['Vorzeichen der Erfolgsdifferenz P(1/4) − P(1/8)','negativ','negativ']],[281,105,98])
body('Erlaubt sind 10 % Niveauabweichung bezogen auf den jeweiligen N11-Erfolg und 25 % Änderung des ursprünglichen Dichtekontrasts. Der Erfolgsunterschied zwischen den beiden Dichten muss sein Vorzeichen behalten.')
sub('Welche Lücke sich schliesst')
body('Die Vorstudie sicherte für den gesamten Träger 1,6 % ab. Die damalige 5,0282-Prozent-Garantie betraf eine Teilfamilie mit zehn N14-Endtypen. Die neue Prüfung erfasst alle 139 zulässigen N14-Endtypen samt den erreichbaren älteren Zweigen.')
url='https://github.com/thomasmgfeller/x6-spectral-astrolabium/pull/299'
tx(left,y-7,'Vorstudie auf GitHub · PR #299','Body',9,green);c.linkURL(url,(left,y-11,left+170,y+4));y-=19;end()
start(2,'RECHENWEG','Eine Schranke für jede Aufteilung')
body('Beide Eltern starten mit Gewicht ½. Jede überträgt den gleichen Anteil λ auf ihre Nachkommen, mit einer frei wählbaren reellen, nichtnegativen Aufteilung. Beide Anfangsdichten verwenden dieselben Gewichte. Amplituden für gemeinsame Endtypen werden vor der Auslese addiert.')
sub('169 Geometrien am selben Rand')
body('Für zwei N11-Eltern, fünf N12-, 23 N13- und 139 N14-Endtypen liegen die skalaren Überlappungen vor. Von den N14-Uhrantworten stammen zehn aus der Vorstudie. Weitere 24 wurden direkt berechnet. Für die übrigen 105 gehen obere Betragsschranken ein, die jede komplexe Phase zulassen.')
sub('Warum das Minimum kontrollierbar ist')
body('Seien b der Referenzvektor, v eine zulässige Nachkommenmischung und x = (1−λ)b + λv. Für jeden Prüfvektor q liefert das positive Skalarprodukt die Schranke')
key('‖x‖² ≥ 2 Re ⟨q, x⟩ − ‖q‖².','Die rechte Seite hängt linear von jeder Aufteilung ab.')
body('Für jede Elternfamilie genügen daher die kleinsten erreichbaren Projektionen. Für das ganze Intervall in λ genügen die beiden Enden der linearen Schranke. Eine zweite Rechnung zeigt, dass alle drei akzeptierten Kanäle abnehmen. Ihr gemeinsamer Verlust entspricht dann dem halben L¹-Abstand aller vier Ausgänge.')
sub('Ein zulässiges Gegenbeispiel')
table([['N14-Ziel','N12 → N13 von der Kette','Von der Ein-Kanten-Ordnung','Anteil'],['734','15 → 173','14 → 22','21 %'],['760','11 → 23','11 → 23','70 %'],['8191','15 → 255','15 → 255','9 %']],[77,159,198,62],8.5)
body('Beide Eltern verteilen ihren übertragenen Anteil nach dieser Tabelle. Bei λ = 5,0211 % und Dichte 1/4 beträgt der Erfolg rund 89,999848 % des N11-Werts. Selbst mit den geprüften Uhrenunsicherheiten liegt die Obergrenze unter 89,999944 %. Vorgeschrieben sind mindestens 90 %.')
end()
start(3,'KONTROLLEN UND REICHWEITE','Wie weit der Befund trägt')
sub('Bekannte Geometrien und unabhängige Rechenwege')
body('Die archivierten 40 × 40-Detektorblöcke wurden für beide Dichten und alle vier Ausgänge auf beiden Gitterstufen reproduziert. Eine ganzzahlige Rechnung bestätigt die Positivität der gespeicherten Effektmatrizen. Alle sechs Wege zum Gegenbeispiel wurden im publizierten Wachstumsinventar geprüft.')
body('Auf einem kleinen Gitter wurde für jede der 24 neuen Uhrantworten direkt über alle sechs inneren Uhren summiert. Die grösste Abweichung zur Faktorisierung lag unter 3,4 × 10⁻¹⁷. Die Gitter (32,6) und (48,8) bezeichnen die inneren Knoten je Uhr und die äusseren Knoten je Lobe. Die grösste Änderung der neuen Amplituden betrug 1,17 × 10⁻⁸.')
maxfine=max(r['change_from_48_8'] for r in refined.values())
rounded_bound=(f"{math.ceil(maxfine*1e13)/10:.1f}").replace(".",",")
body(f'Ein drittes Gitter (64,10) überprüfte {len(refined)} Endtypen, darunter die drei Ziele des Gegenbeispiels. Die grösste Änderung gegenüber (48,8) blieb unter {rounded_bound} × 10⁻¹².')
sub('Was die Fehlerrechnung berücksichtigt')
body('Das rationale Zertifikat erlaubt jeder der 24 neuen direkten Uhramplituden und dem übernommenen Typ 760 je Dichte eine unabhängige Änderung um 10⁻⁷. Die übrigen Betragshüllen folgen aus positiven Quadraturgewichten und dem Betrag höchstens eins der inneren Dichtefaktoren. Sie wurden numerisch mit Aufschlag berechnet.')
body('Die algebraischen Ungleichungen gelten für die gelieferten endlichen Skalarmatrizen, Uhrdaten und Hüllen. Eine durchgängige Fehlereinschliessung bis zu den exakten kontinuierlichen Integralen ist offen. Auch die physikalische Auswahl der Historiengewichte und die Stabilität über N14 hinaus benötigen eigene Nachweise.')
sub('Offline nachrechnen')
body('Im entpackten Paket prüft python3 -B verify.py die Prüfsummen, die Positivität, die Vergleichsdaten und die Grenzaussagen. Mit --rebuild werden auch die numerischen Eingaben neu aufgebaut. Der vollständige mathematische Rechenweg steht in README_DE.md.')
end();c.save()
