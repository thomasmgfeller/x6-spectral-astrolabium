from pathlib import Path
from reportlab.pdfgen.canvas import Canvas
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.platypus import Paragraph, Table, TableStyle
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

ROOT=Path(__file__).resolve().parent
OUT=ROOT/'abgabe'
OUT.mkdir(exist_ok=True)
for family,fn in [('Sans','DejaVuSans'),('SansB','DejaVuSans-Bold'),('Serif','DejaVuSerif')]:
    pdfmetrics.registerFont(TTFont(family,'/usr/share/fonts/truetype/dejavu/'+fn+'.ttf'))
pdfmetrics.registerFontFamily('Sans',normal='Sans',bold='SansB')
c=Canvas(str(OUT/'CST_DUST_Nullzweig_Staubuhr.pdf'),pagesize=A4)
c.setTitle('Der Nullzweig am leeren Anfang der Staubuhr')
c.setAuthor('CST-DUST · interne Modellrechnung')
W,H=A4
M=45
WIDTH=W-2*M
ink='#152E37'
muted='#47616B'
teal='#006C68'
paper='#F1F7F5'
y=0
def color(x):return colors.HexColor(x)
def txt(s,size=10,leading=15,font='Sans',fg=ink):
    return Paragraph(s,ParagraphStyle('p',fontName=font,fontSize=size,leading=leading,textColor=color(fg),splitLongWords=False))
def para(s,after=8,size=10,leading=15):
    global y
    obj=txt(s,size,leading); _,h=obj.wrap(WIDTH,2000);y-=h;obj.drawOn(c,M,y);y-=after
def line(s,font,size,fg):
    global y
    c.setFont(font,size);c.setFillColor(color(fg));c.drawString(M,y-size,s);y-=size+4
def sub(s):
    global y
    y-=5;line(s,'SansB',12,teal);y-=3
def box(s):
    global y
    ob=txt(s,10,15,'Sans');_,h=ob.wrap(WIDTH-26,1500)
    c.setFillColor(color(paper));c.roundRect(M,y-h-18,WIDTH,h+18,4,stroke=0,fill=1)
    c.setFillColor(color(teal));c.rect(M,y-h-18,3,h+18,stroke=0,fill=1)
    ob.drawOn(c,M+13,y-h-8);y-=h+30
def table(header, rows, widths):
    global y
    data=[[txt(s,8,12,'SansB','#FFFFFF') for s in header]]+[[txt(s,9,13,'Sans') for s in row] for row in rows]
    t=Table(data,colWidths=widths,hAlign='LEFT')
    t.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,0),color('#234D56')),
        ('ROWBACKGROUNDS',(0,1),(-1,-1),[color('#F0F5F4'),colors.white]),
        ('VALIGN',(0,0),(-1,-1),'MIDDLE'),('TOPPADDING',(0,0),(-1,-1),6),
        ('BOTTOMPADDING',(0,0),(-1,-1),6),('LEFTPADDING',(0,0),(-1,-1),8),
        ('LINEBELOW',(0,-1),(-1,-1),.6,color('#C5D2D0'))]))
    _,h=t.wrap(WIDTH,1000);y-=h;t.drawOn(c,M,y);y-=13
def page(n,kicker,title):
    global y
    c.setFillColor(color(teal));c.rect(0,H-6,W,6,stroke=0,fill=1)
    c.setFillColor(color(muted));c.setFont('SansB',9);c.drawString(M,H-35,'X6  /  CST-DUST')
    c.setFont('Sans',9);c.drawRightString(W-M,H-35,'Etappen 3 und 4   ·   19. November 2026')
    c.setStrokeColor(color('#BECFCB'));c.line(M,H-45,W-M,H-45)
    c.line(M,34,W-M,34);c.setFont('Sans',8);c.drawString(M,20,'Null- und Ein-Ereignis-Sektor   /   v0.1')
    c.drawRightString(W-M,20,f'{n} / 3')
    y=H-65;line(kicker,'SansB',9,teal);y-=3
    line(title,'Serif',23,ink);y-=12
def done():
    if y<45:raise ValueError(f'page overflow {y}')
    print('bottom',y)
    c.showPage()
base='https://github.com/thomasmgfeller/x6-spectral-astrolabium/blob/3caa6d8e3b7f13afb23e4ccb5380b15b8feaff12/research/rax_cqg/dust_collapse/'
def source(path,label):return f'<a href="{base}{path}" color="{teal}"><u>{label}</u></a>'
page(1,'PRÄPARATION','Der Nullzweig am leeren Uhranfang')
box('<b>Der leere Anfang erhält einen konkreten Randzustand.</b> Auf der präparierten Nulllinie ist die Zuordnung normtreu. Für den gemeinsamen Null- und Geburtssektor ist die vollständig akzeptierende kohärente Auslese ausgeschlossen. Ein gesonderter Messausgang mit kalibrierbarer Akzeptanz ermöglicht den Anschluss.')
sub('Welche Daten zum leeren Anfang gehören')
para('Die offene Staubuhr beginnt ohne inneres Ereignis an einem festen äusseren Anker. Der AA-Nullzweig hat je zwei unvergleichbare äussere Ereignisse am Eingangs- und Ausgangsrand, feste Dichteatome und ein skalares Eingangspaket. Beim Einschränken auf das Innere ergeben alle seine Randordnungen dasselbe leere Präfix.')
table(['Kragen nach Entfernen des inneren Punkts','Beschriftete Ordnungen','Kohärenter Koeffizient je Typgruppe'],[
    ['Zwei getrennte Kanten','2','4/33'],['Drei Kanten','4','20/33'],['Vier Kanten','1','9/33']],[230,110,WIDTH-340])
para('Die Gewichte stammen aus den 33 Ein-Geburts-Ordnungen. Mit diesen Gewichten und derselben Phase wie in den ursprünglichen Paketpaarungen ist die Nullantwort G₀ festgelegt. Der Präparationsoperator bildet z|∅⟩ auf zG₀ ab und erhält wegen ‖G₀‖² = 1 die Norm. Die Kragendaten und der äussere Uhrenanker sind ausdrücklich Teil der Zuordnung.')
sub('Was sich auf dieser Linie fortsetzen lässt')
para('Für eine der beiden offenen Referenzuhren sei h₀(s) = (1−β)s + exp(−s). Die bedingte Wahrscheinlichkeit, von a bis b leer zu bleiben, ist h₀(b)/h₀(a). Bei Unterteilung kürzt sich der Zwischenfaktor exakt. Die Nulllinie trägt damit beide Referenztransporte. Ihre Raten stammen aus den jeweiligen Referenzprodukten.')
table(['Offene Uhr','Keine Geburt bis d = 1/8','Genau eine Geburt bis d = 1/8'],[
    ['β = 5/4','0,85124690','0,14156211'],['β = 4/3','0,84083024','0,15197878']],[90,205,WIDTH-295])
para('Die Überlebenswahrscheinlichkeiten unterscheiden sich exakt um <b>1/96</b>. Eine absolute inklusive Auslese am selben präparierten Anfang und bei derselben Uhr könnte die Kandidaten bereits auf diesem Fenster unterscheiden.',size=9.6,leading=14)
para(source('zero_one_pairing_v0_1/README.md','Gemeinsame Nullnorm')+'   ·   '+source('first_birth_rate_v0_1/README.md','Offene Präparation und Ein-Geburts-Kern'),size=8.8,leading=12)
done()
page(2,'INTERFERENZ UND AUSLESE','Wo die verlustfreie Zuordnung scheitert')
para('Im offenen vollständigen Record sind der Nullzweig und genau eine Geburt orthogonal. Auch Geburten in disjunkten Zeitfenstern sind unterscheidbar. Der gekoppelte AA-Rand antwortet dagegen auf die kohärente Summe der Fenster. Die folgende Rechnung erhält die drei publizierten skalaren Paketpaarungen und ihre komplexen Phasen.')
sub('Ein Hindernis bereits auf zwei Zuständen')
para('Bei der Fensterbreite d = 1/8 ergibt sich für beide positiven AA-Produkte dieselbe gemischte Paarung C des normierten Nullzweigs mit der gesamten Geburtsantwort. Die Intervallrechnung liefert −0,0100200 &lt; Re C &lt; −0,0100199 und 0,0014268 &lt; Im C &lt; 0,0014269.')
box('Ein zulässiger einzelner Messausgang muss die Norm jeder Eingangsüberlagerung höchstens erhalten. Akzeptiert er den Nullzweig sicher, hat die Differenz aus Eingangs- und Ausgangs-Grammatrix links oben eine Null. Ihr gemischtes Element ist −C. Die Determinante beträgt <b>−|C|² ≈ −0,000102436</b>. Der Negativwert schliesst diese Auslese für beide Referenzuhren aus.')
sub('Eine gemeinsame Auslese für zwei Schnitte')
para('Die gemeinsame Verfeinerung hat die Uhrmarken 0, 1/24, 1/16 und 1/8. Aus 33 Geburtsordnungen und sieben Nullordnungen wurden die Paketantworten neu berechnet. Für beide Schnitte ergeben die Einzelgewichte mit dem reellen Interferenzbeitrag das direkte Gesamtgewicht. Auch die Summe der beiden komplexen Null–Geburts-Paarungen reproduziert C.')
table(['AA-Randprodukt','Gesamtgewicht relativ zum Nullzweig','Interferenzanteil bei c = 1/24','Interferenzanteil bei c = 1/16'],[
    ['t = 1','0,000636203548','44,26584 %','49,99432 %'],['t = 4','0,000614789365','44,27625 %','49,99492 %']],[95,145,130,WIDTH-370])
para('t bezeichnet die Form des skalaren Feldregulators. Der Interferenzanteil ist 2 Re⟨G<sub>L</sub>,G<sub>R</sub>⟩ / ‖G<sub>L</sub>+G<sub>R</sub>‖². Die Zahlen gelten für die Dreipaket-Auslese. In der früheren Rechnung mit einem zusätzlich verklebten späteren Uhr- und Dichterecord war der Anteil beim Mittelschnitt rund 49,91 %.')
sub('Was ein zweiter Ausgang ermöglicht')
para('Der Erfolgszweig wirkt mit demselben linearen Operator auf alle Fenster. Seine Gewichte skalieren mit der Nullakzeptanz η. Relativ zum akzeptierten Nullzweig reproduziert er die AA-Paarungen. Sofern dieser Operator eine Kontraktion ist, ergänzt ihn ein zweiter Ausgang zu einem normerhaltenden Instrument. Die Kreuzterme des Erfolgszweigs sind messkanalspezifisch. Der ergänzende Ausgang hebt sie in der inklusiven Bilanz orthogonaler Eingänge auf.')
para(source('two_clock_windows_v0_1/README.md','Frühere Fensterrechnung und späterer Messkanal'),size=8.8,leading=12)
done()
page(3,'AKZEPTANZ UND PHYSIKALISCHE ENTSCHEIDUNG','Welche Kalibrierung die Uhren trennt')
para('Für den Vergleich fixieren wir die dimensionslose Uhrkoordinate, den Markenfilter auf die offene Ein-Geburts-Phase und dieselbe skalare Auslese für alle Fenster. Die Rohabbildung sendet den leeren Zustand auf G₀ und ein Geburtsfenster auf seine gekoppelte AA-Antwort. Nur die relative Eingangsnorm κ = h₁(d)/h₀(d) hängt von β ab, mit h₁(d) = β−1+exp(−d).')
table(['Uhrkandidat','t','Grösste zulässige Nullakzeptanz η bei d = 1/8'],[
    ['β = 5/4','1','0,99938192 bis 0,99938237'],['β = 5/4','4','0,99938207 bis 0,99938245'],
    ['β = 4/3','1','0,99943144 bis 0,99943186'],['β = 4/3','4','0,99943158 bis 0,99943193']],[110,44,WIDTH-154])
box('<b>Ein bedingter Trennversuch.</b> Bei unabhängig festgelegter Nullakzeptanz von 99,94 % wäre β = 5/4 für diesen Messvertrag ausgeschlossen und β = 4/3 für beide AA-Randprodukte zulässig. Bei 98 % sind beide Uhren möglich. Die absolute Akzeptanz des physikalischen Messkanals ist offen. Die Rechnung wählt daher keine Geburtsrate aus.')
sub('Wie das gesamte kontinuierliche Zeitfenster geprüft wurde')
para('Auf dem Nullzweig und den drei Zeitabschnitten hat die Eingangs-Grammatrix H die Diagonale 1, κℓ₁, κℓ₂, κℓ₃. Für die gekoppelte Ausgangs-Grammatrix B prüfen wir H−ηB mit eingeschlossenen Schur-Pivots. ℓᵢ sind die Intervalllängen. Innerhalb der Abschnitte begrenzt die Variation der Wirkungsantwort die ausgelassenen Uhrmoden.')
para('Konkret ist F(u) = Z₁(u)A₁ + Z₂(u)A₂. Die beiden Z sind Uhrintegrale aus der Wirkung. Mit b = √(8/3) gilt |Z′ₚ| ≤ bp/4. Die Normkorrektur im positiven Operator SS† beträgt höchstens (L′)² Σℓᵢ³/(12κ), wobei L′ die Lipschitz-Schranke von F ist. Sie bleibt in allen vier Fällen unter 4,3 × 10⁻⁷. Eine separate Rechnung mit vollen Gaußmatrizen und zwei Quadraturordnungen bestätigt die vier Intervalle.')
sub('Reichweite und Nachrechnung')
para('Die Schranken gelten für diese Präparation und diesen Messvertrag im Null- und Ein-Geburts-Sektor. Die Zuordnung zu einem physikalisch ausgezeichneten Kragen, die absolute Sektornorm und die Kalibrierung zur Staubeigenzeit bleiben offen. Die Kontrolle zweier Unterteilungen ist eine Fensterprüfung. Ein gekoppelter 4D-Transport ist dafür weiterhin eigenständig herzuleiten.')
para('Das Prüfpaket enthält Herleitung, Quellstände, Intervallrechnung, numerische Gegenprobe und Einzelergebnisse. Ausgangsstand auf main ist 3caa6d8 vom 19. November 2026. Der dynamische P3-Pilot bei M = 1 steht auf der ersten Dichtestufe bei 0 von 38 Vergleichen.',size=9,leading=13)
done()
c.save()
