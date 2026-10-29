"""Compact report, built from the checked certificate values."""
import json
from pathlib import Path
from reportlab.pdfgen import canvas
from reportlab.platypus import SimpleDocTemplate,Paragraph,Spacer,Table,TableStyle,PageBreak,KeepTogether
from reportlab.lib.styles import getSampleStyleSheet,ParagraphStyle
from reportlab.lib.colors import HexColor,white
from reportlab.lib.enums import TA_LEFT
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

ROOT=Path(__file__).resolve().parent
OUT=ROOT/'report/Skalarer_Kandidat_Zweiskalenpruefung_v0_25.pdf'
OUT.parent.mkdir(exist_ok=True)
F=Path('/usr/share/fonts/truetype/dejavu')
for name,file in [('DV','DejaVuSans.ttf'),('DV-Bold','DejaVuSans-Bold.ttf'),('DVM','DejaVuSansMono.ttf')]:
    pdfmetrics.registerFont(TTFont(name,str(F/file)))
pdfmetrics.registerFontFamily('DV',normal='DV',bold='DV-Bold',italic='DV',boldItalic='DV-Bold')
navy=HexColor('#142B3C'); teal=HexColor('#166B75'); gray=HexColor('#52616B'); light=HexColor('#EFF4F6'); orange=HexColor('#A34E20')
styles={
'kicker':ParagraphStyle('kicker',fontName='DV-Bold',fontSize=8.5,leading=12,textColor=teal,spaceAfter=14),
'title':ParagraphStyle('title',fontName='DV-Bold',fontSize=25,leading=31,textColor=navy,spaceAfter=16),
'heading':ParagraphStyle('heading',fontName='DV-Bold',fontSize=15,leading=20,textColor=navy,spaceBefore=13,spaceAfter=9),
'body':ParagraphStyle('body',fontName='DV',fontSize=10,leading=14.7,textColor=navy,spaceAfter=10),
'small':ParagraphStyle('small',fontName='DV',fontSize=8,leading=11.5,textColor=gray,spaceAfter=8),
'formula':ParagraphStyle('formula',fontName='DVM',fontSize=9,leading=14,textColor=navy,backColor=light,borderPadding=9,spaceBefore=5,spaceAfter=14),
'cell':ParagraphStyle('cell',fontName='DV',fontSize=9,leading=12.5,textColor=navy),
'headcell':ParagraphStyle('headcell',fontName='DV-Bold',fontSize=8.5,leading=12,textColor=white),
}
story=[]
def p(text,style='body'):return Paragraph(text,styles[style])
def add(text,style='body'):story.append(p(text,style))
def table(headers,rows,widths):
    cells=[[p(x,'headcell') for x in headers]]+[[p(str(x),'cell') for x in row] for row in rows]
    t=Table(cells,colWidths=widths,hAlign='LEFT',repeatRows=1)
    t.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,0),teal),('ROWBACKGROUNDS',(0,1),(-1,-1),[light,white]),
      ('VALIGN',(0,0),(-1,-1),'TOP'),('LEFTPADDING',(0,0),(-1,-1),9),('RIGHTPADDING',(0,0),(-1,-1),9),
      ('TOPPADDING',(0,0),(-1,-1),8),('BOTTOMPADDING',(0,0),(-1,-1),8),('LINEBELOW',(0,-1),(-1,-1),0.5,HexColor('#CBD6DC'))]))
    story.extend([t,Spacer(1,12)])
def page():story.append(PageBreak())
def start(kicker,title):add(kicker,'kicker');add(title,'title')

start('CSPP / EIGENZEIT · FORSCHUNGSNOTIZ 0.25 · 29.10.2026','Ein zusätzlicher Schichtgrad<br/>reicht bei dieser Skala nicht')
add('<b>Der nächste Kandidatenschritt ist mit einem begründeten negativen Ergebnis abgeschlossen.</b> Ein konkret geänderter skalarer Operator verbessert den bisherigen Gauß-Zeugen, scheitert aber an einer zusätzlichen Skalenkontrolle. METHOD und G1 bleiben HOLD.')
add('Konkreter Kandidat: θ = 21','heading')
table(['Kontrollfeld','Sollwert','Neuer Mittelwert','Relativer Fehler'],[
['Gauß L = 2<br/>bisheriger Zeuge','−0,5','−0,499237374','<b>0,153 %</b>'],
['Gauß L = 4<br/>neue Skalenkontrolle','−0,125','−0,230811174','<b>84,65 %</b>']], [137,70,135,163])
add('Stärkeres Ergebnis für die ganze Minimalfamilie','heading')
add('Bei festem q₀ = 3/(16π) erreicht <b>kein reeller Parameter θ</b> zugleich höchstens 10 % Mittelwertfehler an beiden Gauß-Feldern. Der bestmögliche maximale Fehler beträgt <b>28,4733 %</b>. Das ist ein analytischer Allparameter-Ausschluss mit eingeschlossenen Zahlen, kein Suchgitterbefund.')
add('Die Aussage gilt für die normierte Familie mit Kernpolynomgrad höchstens vier und voller kausaler Vergangenheit. Andere Skalen q, höhere Grade, Randkorrekturen und andere skalare Operatoren bleiben offen.')
add('<b>Folge:</b> Dieser Kandidat wird für die Fortsetzung des erweiterten Kontrollprogramms verworfen. Die kompakte Detektorproduktion und eine vollständige Spektralsuche wurden nach dem Kontrollfehlschlag nicht begonnen.')
add('L = 4 ist ein neuer deterministischer Entwicklungszeuge. Die kompakte physikalische Quelle wurde nicht verbreitert. Ein Mittelwert-PASS bei L = 2 wäre weiterhin kein RMS- oder Genauigkeitsnachweis für den Detektor.','small')

page();start('01 / KANDIDAT UND NORMIERUNG','Was genau geändert wurde')
add('Unverändert: ρ = 3/π, ε = 1/16, q = ερ; Masse m = 1; kompakte Quelle mit Radius 1/2, Trägerwellenzahl 4 und Anfangszeit −1. Detektorball und beide Zeitfenster bleiben gleich. Der absolute kompakte Zielwert bleibt 0,001.')
add('Bθ u = a [dθ u + ε Σ wθ(n) u]<br/>a = 4√(q/6),  dθ = −1 − 3θ/8','formula')
add('Die Summe enthält nur kausal vergangene Punkte. Die geglätteten Gewichte entstehen aus fünf Schichtkoeffizienten durch dieselbe Binomialglättung wie bisher. Der konkrete Koeffizientenvektor lautet:')
add('θ = 21: c = (197/8, −3033/8, 2363/2, −1331, 504)<br/>d = −71/8','formula')
add('Warum diese Familie vollständig ist','heading')
add('Die drei Infrarot-Aufhebungen und die Normierung auf □ lassen bei Polynomgrad höchstens vier genau einen freien Parameter. In einer Mellin-Polynomdarstellung ist die zulässige Änderung proportional zu:')
add('Q(s) = (s−1/2)(s−1)(s−3/2)²','formula')
add('Die doppelte Nullstelle erhält die Normierung. Zugleich muss sich der lokale Diagonalterm ändern. Alle Bedingungen und der Rang der rationalen Gleichungen wurden exakt geprüft. Der Ansatz baut auf den IR-Bedingungen von Aslanbeigi, Saravani und Sorkin auf; die konkrete Familie und ihr Ausschluss sind eigene Rechnungen.')
add('Eingabeabbildung ausdrücklich festgelegt','heading')
add('Die finite Diagnose verwendet Ω₅ und die exakte KG-Kontinuumshistory auf t ≤ −1. Das ist eine History-Kontrolle und kein neuer qualifizierter Cauchy-Adapter. H1 und PU-H1 werden dadurch nicht ersetzt. Die volle Vergangenheit wird hier nur für die integrierbaren Gauß-Kontrollfelder ausgewertet.')
add('θ = 21 wurde nach einer explorativen Rechnung nahe dem L = 2-Fit gewählt. Die Entwicklung wird nicht als vorregistriert oder als Prüfung auf unabhängigen Daten ausgegeben.','small')

page();start('02 / AUSSCHLUSS UND STABILITÄT','Was bewiesen ist - und was offen bleibt')
table(['Für ≤ 10 % Mittelwertfehler','Erlaubtes θ-Intervall, gerundet'],[
['Gauß L = 2','17,973854 bis 24,119888'],['Gauß L = 4','6,336495 bis 9,434999']], [243,262])
add('Die Intervalle sind nachweislich disjunkt. Weil beide signierten Fehler affin in θ sind, lässt sich θ algebraisch eliminieren. Daraus folgt die scharfe Untergrenze 28,4733 %. Selbst der optimale Kompromiss θ ≈ 12,296978 verfehlt das gemeinsame Ziel.')
add('Retardierte finite Dynamik','heading')
add('Für den gewählten Kandidaten ist der Gleichungsnenner D = m² + 71a/8 strikt positiv. Der aktive Transferblock K ist nach Zeitsortierung strikt dreieckig. Deshalb existiert (I−K)⁻¹ als endliche Pfadsumme für jede endliche History-Konfiguration.')
add('|δu| ≤ γ N_H (1+γ)^N_A ‖δh‖∞<br/>γ ≈ 7,30893 für m = 1','formula')
add('Diese Schranke kontrolliert beliebige History-Störungen, kann aber sehr gross sein. Für endliche Gebiete und gleichmässig beschränkte History folgen unter dem idealen Poisson-Gesetz endliche Momente aller ganzzahligen Ordnungen. Gemeinsame Originalmomente wurden damit noch nicht ausgewertet.')
table(['Prüfpunkt','Status'],[
['IR-Normierung; Retardierung; finite Lösbarkeit','Nachgewiesen im angegebenen Modell'],
['Zweiskalen-Genauigkeit','Verletzt; Kandidat ausgeschieden'],
['Kompakter Gesamtfehler; volle Spektralsuche','Nicht ausgeführt: begründeter Abbruch'],
['Unendliche / dichteuniforme Stabilität','Nicht zertifiziert']], [265,240])
add('Ein Kontrollgraph bestätigt den Transfer durch dichte Ballinversion und Vorwärtsrekursion. Endliche Lösbarkeit beweist keine langfristige Stabilität. Eine grosse obere Schranke beweist umgekehrt keine Instabilität.','small')

page();start('03 / REPRODUKTION UND ANSCHLUSS','Ein prüfbarer negativer Befund')
table(['Prüfung','Ergebnis'],[
['Herkunft','9 Eingaben gegen Git-Blobs und SHA256'],
['Exakte Algebra','21 rationale Identitäten je Präzision'],
['Intervallrechnung','128 und 192 Bit; 40 gemeinsame Ballziele überlappen'],
['Finite Dynamik','7 Kontrollen je Präzision; dichte Inverse und Rekursion'],
['Unabhängige Koordinatenrechnung','6 Doppelintegrale; maximale Abweichung < 3,51 × 10⁻¹³'],
['Weitere Regressionen','2 alte Referenzen; 128 rationale Binomialgewichte'],
['Isolierter Replay','Beide Produktionsdateien bytegenau reproduziert']], [208,297])
add('Die Zertifikate enthalten analytische Restschranken an beiden Integrationsenden. Die unabhängigen SciPy-Doppelintegrale sind diagnostische Gegenrechnungen. Ihre Fehlerabschätzungen ersetzen die Ballzertifikate nicht.')
add('Konsequenz für die weitere Arbeit','heading')
add('Die nächste Kandidatenentwicklung muss die geprüfte eindimensionale Familie bei festem q verlassen. Vor einem weiteren Fit werden mehrskalige Kontrollen und spektrale Stabilitätskriterien festgelegt. Eine zusätzliche Schicht oder eine geänderte q-Skala verlangt eine neue Kandidatendefinition. Frische Ensembles bleiben hinter der Methodenzulassung.')
add('Nachrechnen','heading')
add('Im entpackten Paket: <b>python3 reproduce.py</b><br/>Nur Prüfungen: <b>python3 reproduce.py --quick</b><br/>Vollständiger Beweis: PROOF.md · Zahlen: results/ · Definition: PROTOCOL.json')
add('Python 3.12.14 · python-flint 0.8.0 · SciPy 1.17.0. Kein externes Peer Review, keine Beweisassistent-Verifikation. Das Paket wurde in diesem Arbeitsschritt nicht auf GitHub veröffentlicht.','small')
add('Quellen: Projekt Main nach PR #156 (4c755221…); Aslanbeigi et al., arxiv.org/abs/1403.1622, Gl. 3.14; Belenchia et al., arxiv.org/abs/1510.04656; NIST DLMF §10.32; python-flint Acb-Dokumentation. Genaue URLs und Verwendungsgrenzen stehen in PROOF.md.','small')

def footer(c,doc):
    c.setStrokeColor(HexColor('#CAD6DC'));c.line(45,48,550,48)
    c.setFont('DV',7.5);c.setFillColor(gray)
    c.drawString(45,33,'CSPP v0.25 · Kandidat begründet verworfen · METHOD / G1: HOLD')
    c.drawRightString(550,33,str(doc.page))
doc=SimpleDocTemplate(str(OUT),pagesize=(595.2756,841.8898),leftMargin=45,rightMargin=45.2756,topMargin=42,bottomMargin=63,
  title='CSPP v0.25 - Skalarer Kandidat und Zweiskalenprüfung',author='Thomas Gfeller / Forschungsprojekt CSPP')
doc.build(story,onFirstPage=footer,onLaterPages=footer)
print(OUT)
