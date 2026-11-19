"""Render the two-page German research note from the saved results."""
from html import escape
from fractions import Fraction as F
from pathlib import Path
import json
from reportlab.lib.colors import HexColor, white
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen.canvas import Canvas
from reportlab.platypus import Paragraph

ROOT = Path(__file__).resolve().parent
OUT = ROOT / "CST_DUST_N15_Uhrantworten_v0_8.pdf"
FONTS = Path("/usr/share/fonts/truetype/dejavu")
for name, font in (("Sans","DejaVuSans"), ("Bold","DejaVuSans-Bold"), ("Serif","DejaVuSerif")):
    pdfmetrics.registerFont(TTFont(name, str(FONTS / (font + ".ttf"))))
ink = HexColor("#142d39")
dim = HexColor("#465c64")
teal = HexColor("#006b65")
line = HexColor("#cbdad6")
pale = HexColor("#eaf3f0")
W,H = A4
x0, x1 = 47, W-47
c = Canvas(str(OUT), pagesize=A4, pageCompression=1)
c.setTitle("CST-DUST · Vier Uhrantworten und die N15-Stabilitätsgrenze")
c.setAuthor("CST-DUST / X6-Spectral-Astrolabium")

def read(name):
    return json.loads((ROOT / name).read_text())
def pct(value, places=4):
    return f"{100*float(F(value)):.{places}f}".replace(".",",") + " %"
def label(x,y,s, font="Sans",size=10, color=ink):
    c.setFont(font,size); c.setFillColor(color); c.drawString(x,y,s)
def rule(y, color=line):
    c.setStrokeColor(color); c.setLineWidth(.7); c.line(x0,y,x1,y)
def body(y,s, color=ink, size=10.4, width=None):
    para=Paragraph(escape(s),ParagraphStyle("body",fontName="Sans",fontSize=size,
        leading=size*1.54,textColor=color))
    _,height=para.wrap(width or (x1-x0),1000); para.drawOn(c,x0,y-height)
    return y-height
def heading(y,s):
    label(x0,y,s,"Bold",13);return y-11
def top(page,section):
    label(x0,795,"CST-DUST   /   ETAPPE 1", "Bold",9,teal)
    c.setFont("Sans",9);c.setFillColor(dim);c.drawRightString(x1,795,section)
    rule(782)
    rule(54);label(x0,35,"X6-Spectral-Astrolabium    ·    19. November 2026    ·    v0.8","Sans",8,dim)
    c.setFont("Bold",8);c.drawRightString(x1,35,f"{page} / 2")
def table(y, headers, rows, positions):
    c.setFillColor(pale);c.rect(x0,y-23,x1-x0,23,fill=1,stroke=0)
    for t,x in zip(headers,positions): label(x,y-15,t,"Bold",9,teal)
    y-=23
    for row in rows:
        for t,x in zip(row,positions): label(x,y-18,t,"Sans",10)
        y-=28;rule(y)
    return y

full=read("volltraeger.json")
pilot=read("teiltraeger.json")
single=read("einzeltests.json")
clocks=read("uhren.json")
top(1,"Erweiterungsstabilität  /  Ergebnis")
label(x0,742,"Wie stabil ist die N15-Erweiterung?","Serif",24)
y=body(718,"Vier neu berechnete Uhrantworten verschieben die nachgewiesene Grenze für den vollständigen Träger. Die Rechnung verwendet denselben Detektor und dieselben zwei Anfangsdichten wie PR #312.")
c.setFillColor(teal);c.roundRect(x0,573,x1-x0,83,9,fill=1,stroke=0)
label(x0+16,619,pct(full["second"]["bound_fraction"]),"Bold",25,white)
label(x0+17,596,"Bis zu diesem Transfer besteht jede zulässige Mischung alle drei Kriterien.","Sans",10,white)
y=heading(545,"Zwei gezielte Rechnungen")
y=table(y-4,("Direkt integrierte N15-Typen","Neue Typen","Gesicherter Transfer"),[
    ("23 · Referenz aus PR #312","–","4,0008 %"),
    ("25 · erste Ergänzung","47037, 45950",pct(full["first"]["bound_fraction"])),
    ("27 · zweite Ergänzung","46509, 46525",pct(full["second"]["bound_fraction"]))],[x0+8,x0+221,x0+359])
y=body(y-14,"Der Träger umfasst 169 frühere Zustände und alle 1 048 zulässigen N15-Endtypen. Jede der beiden Ausgangshistorien überträgt den gleichen Anteil ihres Amplitudengewichts auf frei gewählte, erreichbare Nachkommen.",dim,10.1)
y=heading(y-31,"Was bei genau 5 % entschieden ist")
a=full["second"]["metrics"]["fine"]["1/20"]
y=table(y-4,("Kriterium","Schranke¹","Vorgabe"),[
    ("Niveau bei Anfangsdichte 1/8",pct(a[0]),"≤ 10 %"),
    ("Niveau bei Anfangsdichte 1/4",pct(a[1]),"≤ 10 %"),
    ("Änderung des Dichtekontrasts",pct(a[2]),"≤ 25 %")],[x0+8,x0+275,x0+405])
y=body(y-12,"¹ Auf beiden Referenzgittern auf vier Dezimalstellen gerundet. Auch das negative Vorzeichen des Erfolgsunterschieds bleibt erhalten. Für das Niveau ist weiterhin offen, ob eine zulässige Mischung bei 5 % die Toleranz verletzt.",dim,9.8)
c.showPage();top(2,"Erweiterungsstabilität  /  Evidenz")
label(x0,742,"Was die Rechnung prüft","Serif",24)
y=body(719,"Die Rangliste aus PR #312 bestimmt das erste Typenpaar. Nach Einsetzen seiner komplexen Uhrantworten liefern beide Ausgangshistorien und beide Gitter dieselben nächsten zwei Typen. Auch dieses Paar wurde integriert.")
y=heading(y-28,"Einzeltests bei 5 % Transfer")
y=body(y,"In jedem Test übertragen beide Ausgangshistorien ihre gesamten 5 % auf denselben erreichbaren Typ. Die Tabelle zeigt die relative Änderung der vier Detektorausgänge als Totalvariationsdistanz, bezogen auf den Referenzerfolg.",dim,9.8)
y=table(y-11,("Endtyp","Niveauänderung bei 1/8","Niveauänderung bei 1/4"),[(str(m),pct(single["fine"][str(m)]["relative_level_change"][0],3),pct(single["fine"][str(m)]["relative_level_change"][1],3)) for m in (47037,45950,46509,46525)],[x0+8,x0+126,x0+320])
y=body(y-11,"Alle vier Einzeltests bestehen auf beiden Gittern. Auf dem Teilträger aus 169 früheren Zuständen und den 27 direkt integrierten N15-Typen bestehen auch beliebige zulässige Mischungen bis 5,0210 %. Bei 5,0211 % verletzt die bekannte Mischung dreier N14-Typen die Niveautoleranz.",ink,10)
y=heading(y-30,"Numerische Kontrollen und Gültigkeit")
y=body(y,"Eine unabhängige direkte Siebenfachsumme kontrolliert jeden Typ auf dem kleinen Gitter (4,3). Auf (32,6), (48,8) und (64,10) beträgt die grösste Änderung einer Uhrantwort zwischen benachbarten Gittern 9,62 × 10⁻¹¹ oder weniger. Der im Zertifikat berücksichtigte Radius beträgt 10⁻⁷.",dim,10)
y=body(y-10,"Die Garantie gilt für den endlichen Gittervertrag. Bei 4,4358 % verfehlt die verwendete Abschätzung erstmals die Niveautoleranz. Die nächsten begrenzenden Projektionen gehören zu den Typen 339773 und 524287. Der kontinuierliche Uhrgrenzwert und die physikalischen Historiengewichte bleiben offen.",dim,10)
y-=25
label(x0,y,"Ausgangsstudie und Reproduktion","Bold",10,teal)
url="https://github.com/thomasmgfeller/x6-spectral-astrolabium/pull/312"
label(x0,y-19,"PR #312 auf GitHub","Sans",9,teal); c.linkURL(url,(x0,y-22,x0+96,y-8),relative=0)
label(x0+107,y-19,"·  Offline-Prüfpaket mit README, Daten und ausführbarer Nachrechnung","Sans",9,dim)
if y-22<58: raise RuntimeError("Footer overlap")
c.save()
