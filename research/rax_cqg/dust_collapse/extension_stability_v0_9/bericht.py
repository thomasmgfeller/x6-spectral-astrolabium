"""Render the German short report from the accompanying finite-grid certificate."""
from pathlib import Path
import json
from reportlab.lib.colors import HexColor
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_LEFT
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen.canvas import Canvas
from reportlab.platypus import Paragraph

ROOT=Path(__file__).resolve().parent
FONT=Path('/usr/share/fonts/truetype/dejavu')
for key,name in [('Text','DejaVuSans'),('Bold','DejaVuSans-Bold')]:
    pdfmetrics.registerFont(TTFont(key,str(FONT/(name+'.ttf'))))
W,H=A4
ink='#172c36';teal='#146756';muted='#435963';line='#bfcfca'
pdf=Canvas(str(ROOT/'CST_DUST_N15_Fuenf_Prozent_v0_9.pdf'),pagesize=A4,invariant=1)
pdf.setTitle('CST-DUST · N15-Stabilität bei fünf Prozent')
pdf.setAuthor('X6 Spectral Astrolabium')
def label(x,y,txt,size=10,font='Text',color=ink):
    pdf.setFillColor(HexColor(color));pdf.setFont(font,size);pdf.drawString(x,y,txt)
def rule(y):
    pdf.setStrokeColor(HexColor(line));pdf.line(44,y,W-44,y)
def para(y,txt,size=10.5,lead=16):
    style=ParagraphStyle('body',fontName='Text',fontSize=size,leading=lead,textColor=HexColor(ink),alignment=TA_LEFT)
    p=Paragraph(txt,style);_,h=p.wrap(W-88,720);p.drawOn(pdf,44,y-h);return y-h
def top(n):
    label(44,797,'X6   /   CST-DUST',11,'Bold',teal)
    pdf.setFont('Text',9);pdf.setFillColor(HexColor(muted));pdf.drawRightString(W-44,797,'Etappe 1     ·     19. November 2026')
    rule(783);rule(44);label(44,27,'N15-Erweiterungsstabilität     /     v0.9',8,'Text',muted)
    pdf.drawRightString(W-44,27,f'{n} / 2')
def section(y,title):
    label(44,y,title,14,'Bold',teal);return y-12
r=json.loads((ROOT/'planes.json').read_text())
if (r['joint_full_transfer_per_million'],r['safe_state_count'],r['reserve_state_count'],
    r['reserve_outside_share_per_million_at_five'],r['outside_transfer_share_per_million_at_five'])!=(46904,1098,1022,57642,685):
    raise ValueError('Report numbers differ from the certificate')
top(1)
label(44,734,'N15-Stabilität bei fünf Prozent',26,'Bold')
y=para(708,'Für alle 1 217 Zustände sind bis zu 4,6904 % übertragenes Amplitudengewicht abgesichert. Bei 5 % bestehen alle zulässigen Mischungen auf einem ausdrücklich benannten Träger mit 1 098 Zuständen. Beide Aussagen gelten auf den zwei Referenzgittern.',12,19)
y=section(y-34,'Welche Verteilungen die drei Tests bestehen')
head=y-25
pdf.setFillColor(HexColor('#e5f0eb'));pdf.roundRect(44,head-8,W-88,28,3,fill=1,stroke=0)
label(55,head,'Träger und Verteilung',10,'Bold');label(451,head,'Transfer',10,'Bold')
pairs=[('1 217 Zustände, frei gemischt (v0.8)','4,4357 %'),
       ('1 217 Zustände, frei gemischt (v0.9)','4,6904 %'),
       ('1 098 Zustände, frei gemischt','5,0000 %'),
       ('1 022 Zustände plus begrenzter Aussenanteil¹','5,0000 %')]
for i,(s,t) in enumerate(pairs,1):
    yy=head-32*i;label(55,yy,s,10.5);label(451,yy,t,10.5,'Bold');rule(yy-10)
y=para(yy-22,'¹ Bis zu 5,7642 % des übertragenen Gewichts dürfen auf die übrigen 195 Typen entfallen. Bei 5 % Transfer sind das 0,28821 % des anfänglichen Gesamtgewichts. Für den 1 098er-Träger gilt eine zweite Grenze von 0,0685 % des Transfers auf die übrigen 119 Typen.',9.5,14)
y=section(y-32,'Was bei 5 % auf dem gesamten Träger offen ist')
y=para(y,'Der vierteilige Dichtekontrast und das negative Vorzeichen der Erfolgsdifferenz bleiben für jede zulässige Verteilung erhalten. Für die relative Niveauabweichung bei Anfangsdichte 1/4 ergibt die unbedingte Abschätzung höchstens 10,6417 %. Die Toleranz beträgt 10 %. Eine tatsächliche Verletzung bei 5 % ist damit weiterhin offen.')
y=para(y-14,'Der bekannte N14-Zeuge überschreitet die Toleranz bei 5,0211 %. Auf dem früheren Träger mit 196 Zuständen reicht die Garantie bis 5,0210 %.')
if y<54:raise ValueError('page one overflow')
pdf.showPage()
top(2);label(44,734,'Rechnung und Gegenproben',24,'Bold')
y=section(688,'Vier neue Uhrantworten')
y=para(y,'Die in v0.8 am stärksten begrenzenden Endtypen 339773, 524287, 45885 und 45851 wurden jeweils auf (32,6), (48,8) und (64,10) berechnet. Beim ersten Typ trennt eine zusätzliche Gauss-Integration zwei Zweige. Beim zweiten lassen sich drei innere Uhren nacheinander bedingt summieren. Alle sieben inneren Uhren, beide Randloben und die ursprünglichen Phasen gehen ein.')
y=para(y-10,'Auf dem kleinen Gitter (5,4) beträgt die grösste Abweichung gegenüber einer direkten Siebenfachsumme weniger als 1,6 × 10⁻¹⁷. Der gemeinsame Prüfradius der neuen komplexen Uhrwerte beträgt wie in der Vorstudie 10⁻⁷.')
y=section(y-35,'Ein gemeinsamer Test für alle Mischungen')
y=para(y,'Für jeden der 1 048 N15-Endtypen wurden die skalaren Überlappungen mit drei N14-Zuständen berechnet. Daraus folgt für jede erreichbare Tochter eine Untergrenze ihres Beitrags zur Stützebene des Gesamterfolgs. Bestehen alle Töchter eines Trägers diese lineare Prüfung, gilt die Untergrenze auch für jede erlaubte Mischung.')
y=para(y-10,'Beim 1 098er-Träger beträgt der kleinste abgesicherte Gesamterfolg bei 5 % Transfer 90,000454 % der Referenz. Rationale Arithmetik prüft die Schranke für beide Dichten und Gitter. Eine unabhängige lineare Optimierung über beide Elternverteilungen bestätigt die Ergebnisse.')
y=section(y-35,'Nachrechnen')
y=para(y,'Das Offline-Paket enthält beide vollständigen Typenlisten, die vier neuen Uhrantworten, die 3&#160;144 Paarüberlappungen, die exakten Zertifikate und die unveränderte Studie aus PR #313. Im entpackten Ordner prüft der folgende Aufruf die archivierten Befunde.')
y-=24;label(54,y,'python3 -B verify.py',11,'Bold')
y=para(y-14,'Mit der Option --rebuild werden auch die Uhrwerte und Skalarprodukte neu berechnet. Die Aussage betrifft die endliche Historienfamilie und ihre numerischen Eingangsschranken. Der Kontinuumsgrenzwert, die physikalische Gewichtsauswahl und die Kollapsdynamik bleiben offen.',9.5,14)
if y<54:raise ValueError('page two overflow')
pdf.showPage();pdf.save()
