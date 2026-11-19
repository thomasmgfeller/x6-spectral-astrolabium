"""Generate the German research brief. Optional dependency: ReportLab, DejaVu fonts."""
from pathlib import Path
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.styles import ParagraphStyle
from reportlab.platypus import Paragraph
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen.canvas import Canvas

root=Path(__file__).resolve().parent
for face,file in [('Sans','DejaVuSans'),('Bold','DejaVuSans-Bold'),('Serif','DejaVuSerif')]:
    pdfmetrics.registerFont(TTFont(face,'/usr/share/fonts/truetype/dejavu/'+file+'.ttf'))
p=Canvas(str(root/'CST_DUST_N15_Erweiterungsstabilitaet_v0_7.pdf'),pagesize=A4)
p.setTitle('CST-DUST · Erweiterungsstabilität bei fünfzehn Ereignissen')
W,H=A4;L=49;R=W-L
ink='#142c35';muted='#4a6168';teal='#066a60';line='#ccdcd7';pale='#edf6f1'
def colour(s):return colors.HexColor(s)
def txt(x,y,s,font='Sans',sz=10,c=ink):
    p.setFillColor(colour(c));p.setFont(font,sz);p.drawString(x,y,s)
def para(y,s,sz=10.5,height=16,x=L,width=None,c=ink,font='Sans'):
    o=Paragraph(s,ParagraphStyle('body',fontName=font,fontSize=sz,leading=height,textColor=colour(c)))
    _,h=o.wrap(width or R-L,730);o.drawOn(p,x,y-h);return y-h
def rule(y):
    p.setStrokeColor(colour(line));p.line(L,y,R,y)
def title(y,s):
    txt(L,y,s,'Serif',23)
def section(y,s):
    txt(L,y,s,'Bold',13,teal)
def page(no,sec):
    txt(L,H-44,'CST-DUST   /   ETAPPE 1', 'Bold',9,teal)
    p.setFont('Sans',9);p.setFillColor(colour(muted));p.drawRightString(R,H-44,'19. November 2026')
    rule(H-58);txt(L,H-88,sec.upper(),'Bold',8.5,muted)
    rule(49);txt(L,31,'N11–N15  ·  Erweiterungsstabilität v0.7','Sans',8,muted)
    p.setFont('Sans',8);p.drawRightString(R,31,f'{no} / 3')
def table(y,widths,headers,rows):
    xs=[L]
    for w in widths:xs.append(xs[-1]+w)
    p.setFillColor(colour(pale));p.rect(L,y-27,xs[-1]-L,27,fill=1,stroke=0)
    for j,s in enumerate(headers):txt(xs[j]+7,y-17,s,'Bold',9,teal)
    y-=27
    for row in rows:
        for j,s in enumerate(row):txt(xs[j]+7,y-18,s,'Sans',9)
        y-=30;rule(y)
    return y
page(1,'Befund')
title(717,'Wie weit trägt die N11-Präparation?')
para(690,'Die vierte Einfügung vergrössert das Innere von sechs auf sieben Ereignisse. Der Rand, die Anfangsdichten und der vierteilige Detektor bleiben wie in PR #311. Untersucht wird, wie viel Amplitudengewicht jede der beiden N11-Ausgangshistorien an ihre erlaubten Nachkommen abgeben kann.')
p.setFillColor(colour(pale));p.roundRect(L,534,R-L,76,7,fill=1,stroke=0)
txt(L+16,580,'4,0008 % auf dem gesamten N15-Träger','Bold',16,teal)
txt(L+16,555,'Bis zu diesem Anteil hält jede zulässige Aufteilung alle drei Toleranzen.','Sans',10)
section(500,'Was bei fünf Prozent schon entschieden ist')
para(480,'Auf beiden Referenzgittern sind die Änderung des vierteiligen Dichtekontrasts und das Vorzeichen der Erfolgsdifferenz für alle Aufteilungen unter Kontrolle. Für das absolute Detektorniveau reicht die gemeinsame Schranke bei fünf Prozent noch nicht aus.')
table(408,[228,99,93,76],['Obere Schranke','Bei 4,0008 %','Bei 5 %','Erlaubt'],[
    ('Niveauabweichung bei Dichte 1/8','9,98208 %','12,39730 %','10 %'),
    ('Niveauabweichung bei Dichte 1/4','9,99978 %','12,41919 %','10 %'),
    ('Änderung des Dichtekontrasts','18,65911 %','24,14800 %','25 %')])
para(277,'Die Niveauwerte beziehen sich auf den jeweiligen N11-Referenzerfolg, die Kontrastwerte auf den ursprünglichen vierteiligen Dichtekontrast. Alle Tabellenwerte sind nach oben gerundet.',sz=9.2,height=14,c=muted)
section(209,'Der direkt berechnete Teilträger')
para(188,'Mit allen bisherigen 169 Zuständen und 23 neuen N15-Endtypen gilt weiterhin die scharfe Eingrenzung aus PR #311. Bis 5,0210 % besteht jede Mischung. Bei 5,0211 % scheitert die bekannte Mischung der N14-Typen 734, 760 und 8191. Diese Mischung ist auch auf dem vollständigen N15-Träger zulässig.')
p.showPage()
page(2,'Historien und Zulässigkeit')
title(717,'Welche Fortsetzungen sind zugelassen?')
para(687,'Die vier Vergangenheits- und vier Zukunftsereignisse begrenzen sieben innere Ereignisse. Jede der 139 zugelassenen N14-Geometrien erhält ein weiteres Ereignis. Die Vorwärtszählung prüft jede Lage in der Kausalordnung.')
table(605,[242,127,127],['Zählung','Vor Skalarprüfung','Nach Skalarprüfung'],[
 ('Verschiedene N15-Endtypen','1 652','1 048'),
 ('Eltern-Tochter-Paare','5 029','4 165'),
 ('Markierte Pfade aus der Dreierkette','74 410','64 088'),
 ('Pfade aus der Ein-Kanten-Ordnung','107 466','92 800'),
 ('Markierte Pfade insgesamt','181 876','156 888')])
section(386,'Zwei unabhängige Kontrollen')
para(366,'<b>Ordnung.</b> Eine zweite Rechnung löscht aus jedem der 2 045 unmarkierten Sieben-Punkt-Typen jeweils ein Ereignis. Nach Berücksichtigung der Automorphismen stimmen alle 284 255 Vergleiche mit der Vorwärtszählung überein. Jeder der 139 Eltern besitzt mindestens eine zugelassene Tochter.')
para(276,'<b>Skalarer Rand.</b> Exakte ganzzahlige Rangprüfungen und die ursprüngliche Kernrechnung stimmen überein. 257 Endtypen scheitern ausschliesslich an einer freien inneren Nullrichtung, 273 ausschliesslich am Defekt des gemischten Legendre-Systems und 74 an beiden Bedingungen.')
para(174,'Die Dreierkette erreicht 1 011 der zugelassenen Endtypen, die Ein-Kanten-Ordnung 1 047. Beiträge beider Eltern zum gleichen Endtyp werden vor der Detektorauslese kohärent addiert. Die Zahl der Pfade legt ihre physikalischen Gewichte nicht fest.',sz=10,height=16,c=muted)
p.showPage()
page(3,'Rechenweg und Reichweite')
title(717,'Wie die Schranke geprüft wurde')
section(670,'Für 23 Endtypen wurden die komplexen Uhren integriert')
para(650,'Die Auswahl umfasst alle zugelassenen N15-Typen, deren Zwischenfaktoren bei geeigneter Summationsreihenfolge höchstens drei Uhren verbinden. Beide Dichten wurden auf den Gittern (32,6), (48,8) und (64,10) geprüft. Direkte Siebenfachsummation auf kleinem Gitter und Faktorisierung unterscheiden sich um weniger als 3,5 × 10⁻¹⁷.')
section(543,'Für alle 1 048 Endtypen sind die Ankerüberlappungen bekannt')
para(522,'Je Detektorausgang wurden die Überlappungen mit beiden N11-Eltern und der Diagonalwert berechnet. Für die 1 025 übrigen N15-Uhrantworten lässt die Rechnung jeden komplexen Phasenwinkel zu. Eine obere Betragsschranke folgt aus den inneren Dichtefaktoren, die sich auf dem Gitter als Baumprodukte aufsummieren lassen.')
para(430,'Bei vier Ausgängen genügen sieben Teilsummen, um die gesamte Niveau- und Kontrastabweichung zu begrenzen. Die Prüfung berücksichtigt beide Elternfamilien getrennt und das ganze Intervall des übertragenen Gewichts. Sie entscheidet die Ungleichungen rational für die gespeicherten numerischen Eingaben.')
section(325,'Wo der nächste gezielte Test ansetzt')
para(305,'Bei Dichte 1/4 begrenzen vor allem die N15-Typen 47037 und 45950 die garantierte Projektion auf die Anfangspräparation. Beide sind von beiden Eltern erreichbar. Individuelle Uhrenrechnungen für diese Typen würden die offene Niveauprüfung bei 5 % gezielt verschärfen.')
para(226,'Die Ergebnisse gelten für den festen Detektor und die beiden endlichen Referenzgitter. Eine Fehlereinschliessung bis zu den kontinuierlichen Uhrintegralen, die physikalische Auswahl der Historiengewichte und die Kollapsdynamik bleiben offen.',sz=9.8,height=15,c=muted)
rule(153);txt(L,130,'Offline nachrechnen','Bold',11,teal)
para(113,'Im entpackten Prüfpaket rekonstruiert <font name="Bold">python3 -B verify.py</font> das Inventar und beide Zertifikate. README.md und Methode.md enthalten Datenwege und Herleitung.',sz=9.5,height=14)
p.showPage();p.save()
