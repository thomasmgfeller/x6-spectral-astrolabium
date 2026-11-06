"""Build the German report and standalone scientific figures."""
from pathlib import Path
from fractions import Fraction as F
import csv,json,math
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from reportlab.platypus import SimpleDocTemplate,Paragraph,Spacer,Table,TableStyle,PageBreak,Image
from reportlab.lib.styles import getSampleStyleSheet,ParagraphStyle
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

ROOT=Path(__file__).resolve().parent;OUT=ROOT.parent/'output/pdf';OUT.mkdir(parents=True,exist_ok=True)
FIG=ROOT/'figures';FIG.mkdir(exist_ok=True)
S=json.loads((ROOT/'results/verification.json').read_text())
plt.rcParams.update({'font.family':'DejaVu Sans','font.size':10,'axes.spines.top':False,'axes.spines.right':False})
Tend=5*math.sqrt(5)/3;xh=2*(1-(.8)**1.5)
xs=[i/500 for i in range(501)];rb=[10*(1-.5*x)**(2/3) for x in xs]
inside=[xh]+[x for x in xs if x>xh]
ra=[1.5*Tend*(2-x) for x in inside]
fig,ax=plt.subplots(figsize=(7,3.5),layout='constrained')
ax.fill_between(inside,ra,[8]*len(inside),color='#f0b99c',alpha=.55,label='Gefangene runde Sphären')
ax.plot(xs,rb,color='#173e50',lw=2.2,label='Materieoberfläche Rb')
ax.plot(inside,ra,color='#187c70',lw=2.2,label='Innerer marginaler Ast')
ax.plot([xh,1],[8,8],color='#a4512b',lw=2.2,label='Äußerer marginaler Ast')
ax.plot([0,xh],[8,8],color='#a4512b',lw=1,ls=':',alpha=.7)
ax.axvline(xh,color='#536570',lw=1,ls='--')
ax.plot([xh],[8],'o',color='#173e50',ms=5)
ax.annotate('Oberflächendurchgang\nx = 0,568916',xy=(xh,8),xytext=(.16,6.15),
            arrowprops={'arrowstyle':'->','color':'#536570'},fontsize=9)
ax.set(xlim=(0,1),ylim=(4.9,10.7),xlabel='Gemeinsame Eigenzeit x = T / Tend',ylabel='Arealradius R (G = c = 1)',title='M = 4, R0 = 10: festes reguläres Zeitfenster')
ax.legend(loc='upper right',fontsize=8,frameon=False,ncols=2)
fig.savefig(FIG/'trapped_round_region.png',dpi=190);plt.close(fig)

chis=[.5+i/1000 for i in range(501)];rend=10*(.5)**(2/3);vv=[z*math.sqrt(8/rend) for z in chis]
ep=[1-v for v in vv];lo=[1-1.1025*v for v in vv];hi=[1-.9025*v for v in vv]
fig,ax=plt.subplots(figsize=(7,3.0),layout='constrained')
ax.fill_between(chis,lo,hi,color='#c7dfe6',label='Hypothetische ±5 % in H und R')
ax.plot(chis,ep,color='#173e50',lw=2,label='Exakte klassische Referenz')
ax.axhline(0,color='#a4512b',lw=1.2)
ca=math.sqrt(rend/8)
ax.axvline(ca,color='#187c70',ls='--',lw=1)
ax.set(xlim=(.5,1),xlabel='Mitbewegte Schale χ = R / Rb',ylabel='e+ = R θ+ / 2',title='M = 4 am Fensterende: Vorzeichen nahe der Grenze')
ax.text(ca-.009,.35,'χA = 0,887384',rotation=90,ha='right',va='center',fontsize=8,color='#187c70')
ax.legend(loc='lower left',frameon=False,fontsize=8)
fig.savefig(FIG/'sign_uncertainty.png',dpi=190);plt.close(fig)

fonts=Path('/usr/share/fonts/truetype/dejavu')
for name,file in [('DV','DejaVuSans.ttf'),('DVB','DejaVuSans-Bold.ttf'),('DVM','DejaVuSansMono.ttf')]:
    pdfmetrics.registerFont(TTFont(name,str(fonts/file)))
pdfmetrics.registerFontFamily('DV',normal='DV',bold='DVB',italic='DV',boldItalic='DVB')
blue=colors.HexColor('#163d50');teal=colors.HexColor('#187c70');muted=colors.HexColor('#536570')
st=getSampleStyleSheet()
st.add(ParagraphStyle(name='B',fontName='DV',fontSize=9.3,leading=13.3,textColor=blue,spaceAfter=8))
st.add(ParagraphStyle(name='S',parent=st['B'],fontSize=8,leading=11.2,spaceAfter=6))
st.add(ParagraphStyle(name='T',fontName='DVB',fontSize=23,leading=29,textColor=blue,spaceAfter=14))
st.add(ParagraphStyle(name='H',fontName='DVB',fontSize=11.2,leading=15,textColor=teal,spaceBefore=7,spaceAfter=7))
st.add(ParagraphStyle(name='E',parent=st['B'],fontSize=10,leading=16,backColor=colors.HexColor('#edf3f5'),borderPadding=8,spaceBefore=4,spaceAfter=13))
st.add(ParagraphStyle(name='C',parent=st['B'],fontSize=8,leading=11.1,spaceAfter=0))
st.add(ParagraphStyle(name='L',parent=st['B'],fontName='DVB',fontSize=8.1,leading=12,textColor=teal,spaceAfter=10))
story=[]
def p(t,style='B'):story.append(Paragraph(t,st[style]))
def h(t):p(t,'H')
def eq(t):p(t,'E')
def page(n,title):
    if story:story.append(PageBreak())
    p(f'CST-DUST · EXPANSION UND TRAPPING v0.1 / {n:02d}','L');p(title,'T')
def table(rows,widths):
    t=Table([[Paragraph(str(c),st['C']) for c in row] for row in rows],colWidths=widths,repeatRows=1,hAlign='LEFT')
    t.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,0),colors.HexColor('#e6eef1')),('VALIGN',(0,0),(-1,-1),'TOP'),
        ('TOPPADDING',(0,0),(-1,-1),7),('BOTTOMPADDING',(0,0),(-1,-1),7),('LEFTPADDING',(0,0),(-1,-1),7),
        ('RIGHTPADDING',(0,0),(-1,-1),7),('LINEBELOW',(0,0),(-1,0),.7,teal),('LINEBELOW',(0,1),(-1,-1),.25,colors.HexColor('#cdd8dd'))]))
    story.append(t);story.append(Spacer(1,8))
def fig(name,height):story.append(Image(str(FIG/name),width=504,height=height));story.append(Spacer(1,8))
def num(x,n=6):return f'{float(x):.{n}f}'.replace('.',',')

page(1,'Expansion und Trapping')
p('Auf der geprüften klassischen Staubball-Dynamik<br/>6. November 2026 · CST-DUST-EXPANSION-TRAPPING-001','S')
eq('<b>Klassische Referenz: lokale gefangene Flächen nachgewiesen.</b><br/>Physikalischer CST-Test: HOLD_NOT_ELIGIBLE / NOT_RUN<br/>Regularität: eigenständig HOLD · Ereignishorizont: nicht bestimmt')
p('Die abgesicherte Dynamik ist die eingesetzte Einstein-Staub-Referenz. Der gekoppelte CST-Kern und vollständige Messadapter fehlen weiterhin. Die neue Rechnung untersucht deshalb den endlichen klassischen Ball einschließlich seiner Oberfläche und des Schwarzschild-Außenraums.')
h('Ergebnis im unveränderten gemeinsamen Zeitfenster')
table([['Masse M','Runde Symmetrieflächen auf 0 ≤ T ≤ Tend'],
 ['1/4','Keine gefangenen runden Sphären; maximale Oberflächenkompaktheit 0,054655.'],
 ['1','Keine gefangenen runden Sphären; maximale Oberflächenkompaktheit 0,242283.'],
 ['4','Erster marginaler Durchgang an der Oberfläche bei T/Tend = 0,5689164944 und Rb = 8. Danach ein gefangener Ringbereich im Staub und Vakuum.']],[90,414])
p('G = c = 1, R0 = 10, Tend = 5√5/3 ≈ 3,726780. Für M = 4 liegt der Oberflächendurchgang bei T ≈ 2,120227. Das Zentrum und die Krümmung bleiben im betrachteten Fenster regulär. Die klassische Lösung wird später singulär.','S')
h('Was neu abgesichert ist')
p('Staubexpansion und beide Null-Expansionen sind getrennt definiert. Die marginalen Äste sind innen zeitartig und „future inner“, außen null und „future outer“. Fehlerintervalle werden bis in die Vorzeichenentscheidung fortgepflanzt; ein Null enthaltendes Intervall ist noch kein Marginalflächenbeweis.')
p('Keine neuen Zufallsstichproben oder CST-Ensembles. Kein physikalischer CST-Verfeinerungsnachweis, keine Singularitätsauflösung und keine globale Schwarze-Loch-Aussage. Der lokale Plan-Freeze ist keine externe Präregistrierung.','S')

page(2,'Staubexpansion und Null-Expansionen')
p('Die Signatur ist (-+++). T ist Staubeigenzeit im Inneren und die passend fortgesetzte ingoing PG-Zeit im Außenraum. Auf der runden Sphäre ist A = 4πR². Beide Nullrichtungen sind zukunftsgerichtet und auf l·n = -2 sowie l(T) = n(T) = 1 normiert.')
eq('u = ∂<sub>T</sub> - v ∂<sub>R</sub>, &nbsp; e = ∂<sub>R</sub><br/>l = u + e, &nbsp; n = u - e<br/>θ<sub>l</sub> = 2(1-v)/R, &nbsp; θ<sub>n</sub> = -2(1+v)/R')
table([['Observable','Bedeutung und Bereich'],
 ['Θ<sub>dust</sub> = 3H','Volumenexpansion der Staubkongruenz; im ganzen Fenster negativ. Nur im Materieinneren als Staubobservable definiert.'],
 ['θ<sub>l</sub>, θ<sub>n</sub>','Lokale Flächenänderung entlang auswärts/einwärts orientierter zukünftiger Nullrichtungen. Beide Vorzeichen sind nötig.'],
 ['e<sub>l,n</sub> = Rθ<sub>l,n</sub>/2','Dimensionslose Größen für Kalibrierung nahe θ = 0; keine relative Fehlerdivision durch eine verschwindende Expansion.'],
 ['C = 2Gm/R','Geometrische Kompaktheit. m = Mχ³ innen, m = M außen gilt hier durch die klassische Lösung.']],[156,348])
eq('θ<sub>l</sub> θ<sub>n</sub> = (4/R²)(2Gm/R - 1)<br/>Zukunftsgefangen: θ<sub>l</sub> &lt; 0 und θ<sub>n</sub> &lt; 0')
p('Bei Kollaps ist θn stets negativ. Eine kleine kontrahierende Kugel kann trotzdem θl &gt; 0 haben und ungefangen sein. Bei Expansion kann C &gt; 1 dagegen vergangenheitsgefangene Flächen bezeichnen.')
h('Orientierung, Normierung und Flächenauswahl')
p('Positive reziproke Boosts l → b l, n → b⁻¹n bewahren Vorzeichen und Produkt, ändern aber die einzelnen Beträge. Negative Flächenmittelwerte genügen bei nicht-runden rekonstruierten Flächen nicht: Erforderlich ist eine kontrollierte Aussage auf der gesamten geschlossenen Fläche. R = 0 wird als entartete Sphäre ausgeschlossen.')

page(3,'Endlicher Ball mit konsistentem Rand')
eq('ds² = -dT² + (dR + v dT)² + R² dΩ²<br/>Innen: v = -HR, &nbsp; R = χRb, &nbsp; m = Mχ³<br/>Außen: v = √(2GM/R), &nbsp; R ≥ Rb')
p('Die PG-Koordinaten sind auch bei R = 2GM regulär. Am mitbewegten Rand stimmen die Verschiebung v, beide Null-Expansionen, die eingeschlossene Masse M und die Oberflächenbeschleunigung überein. Der Außenraum wird nicht in die Materiezählung eingerechnet.')
table([['Anschlussgröße','Innen und außen'],
 ['Induzierte Metrik h','-dT² + Rb² dΩ²'],
 ['Extrinsische Krümmung','K<sub>TT</sub> = 0; K<sub>θθ</sub> = Rb; K<sub>φφ</sub> = Rb sin²θ'],
 ['Oberflächenbewegung','Ṙb = -√(2GM/Rb); R̈b = -GM/Rb²'],
 ['Druck und mitbewegter Fluss','Beide null; kein klassischer dünner Oberflächenstress erforderlich.'],
 ['Dichte und Krümmung','Endliche einseitige Sprünge sind zulässig; sie sind keine Delta-Schicht.']],[174,330])
p('Die einseitigen v-Ableitungen unterscheiden sich. Innen gilt ∂Tv = 3v²/(2Rb), ∂Rv = v/Rb; außen gilt ∂Tv = 0, ∂Rv = -v/(2Rb). Entlang der bewegten Oberfläche liefern beide dv/dT = GM/Rb². Die Kontinuität der Geschwindigkeit und dieser Beschleunigung ist an allen 15 Massen-/Zeitpunkten kontrolliert.')
h('Notwendige Gebietskontrolle')
p('Vor dem Oberflächendurchgang liegt R = 2GM im Staub. Dort darf die Vakuumformel nicht eingesetzt werden. Bei M = 4, T = 0, R = 8 ist 2m/R = 0,512 und die Kugel ungefangen. Die unzulässige Ersetzung der inneren Masse m durch die Gesamtmasse M würde eine falsche Marginalfläche erzeugen.')
p('420 feste Außenraum-Prüfplätze werden deshalb mit expliziter Gebietsprüfung ausgewertet. Innere Punkte und unaufgelöste Überlappungen werden nicht als Vakuumbelege gezählt. Dieser Anschluss ist eine klassische Referenzkontrolle; ein CST-Randgesetz bleibt offen.','S')

page(4,'Zwei marginale Äste')
fig('trapped_round_region.png',252)
table([['Ast nach dem Durchgang','Ort','Typ und Kausalität'],
 ['Im Staub','R<sub>A</sub> = 1/|H|','L<sub>n</sub>θ<sub>l</sub> = +1/R<sub>A</sub>²<br/>future inner; zeitartig'],
 ['Im Vakuum','R = 2GM','L<sub>n</sub>θ<sub>l</sub> = -2/R²<br/>future outer; null']],[164,130,210])
p('Auf beiden Ästen gilt θl = 0 und θn = -4/R. Innen ist ṘA = -3/2; die Tangentennorm beträgt -3/4 und die Fläche nimmt ab. Außen ist R konstant; die Tangentennorm ist null und die Fläche bleibt konstant.')
p('Der gefangene Bereich runder Sphären ist RA &lt; R &lt; 2GM. Die Materieoberfläche liegt darin. Am Fensterende für M = 4: RA ≈ 5,590170, Rb ≈ 6,299605, äußere Grenze R = 8; entsprechend χA ≈ 0,887384.')
p('Die gepunktete Linie vor dem Durchgang ist nur die formale Lage 2GM im Materieinneren, keine Vakuum-Marginalfläche. Am gemeinsamen Anfangspunkt der beiden Äste springen die einseitigen Ableitungen und die Tangenten. Es wird dort keine glatte durchgehende marginale Röhre behauptet.','S')

page(5,'Fehler bis zum Ereignis kontrolliert')
p('Die bewiesenen klassischen Zustandsintervalle aus der Korrespondenzprüfung werden auf beide Null-Expansionen propagiert. Alle 420 inneren Vergleichsfälle enthalten die analytischen Referenzwerte. Numerisches Cap: absolut 0,005 für e = Rθ/2; erklärtes Referenz-Toleranzband: ±0,05.')
table([['Euler-Schritte N','Größte absolute e-Fehlerhülle','Numerisches Cap'],
 *[[r['N'],num(r['max_absolute_e_error'],8),'PASS' if r['numerical_cap_pass'] else 'HOLD'] for r in S['numerical_levels']]],[118,245,141])
h('Ereigniszeit unabhängig eingeschlossen')
p('Die Ereignissuche verfolgt die globale Euler-Fehlerhülle zwischen den bisherigen Ablesezeiten. Die letzte sicher positive und erste sicher negative Expansion begrenzen die eindeutige Wurzel. Alle zwölf Intervalle enthalten die analytischen Ereignisse und erfüllen das Breiten-Cap 0,025 Tend.')
br=list(csv.DictReader((ROOT/'results/numerical_event_brackets.csv').open()))
table([['N','Oberflächendurchgang: Intervall für T/Tend'],
 *[[r['N'],f"[{num(F(r['x_lower']),8)}; {num(F(r['x_upper']),8)}]"] for r in br if r['chi']=='1']],[118,386])
h('Unabhängige Kalibrierung der Flächenableitung')
p('216 symmetrische Flächenableitungen entlang separat entwickelter radialer Nullstrahlen prüfen die Definition von θ. Alle Strahlen bleiben innerhalb des freigegebenen Zeitfensters und der Materie. Bei δx = 1/512 ist die größte e-Fehlerhülle kleiner als 2,142·10⁻⁶.')
p('60-stellige nach außen gerundete Decimal-Arithmetik und 100 exakte rationale Wurzelbisektionen kontrollieren Rundung und Referenzwerte. Die vier numerischen Zeitgitter sind keine physikalischen CST-Dichtestufen.','S')

page(6,'Nahe null reicht eine Prozentzahl nicht')
fig('sign_uncertainty.png',216)
eq('Hypothetisch: |ΔH/H| ≤ 0,05 und |ΔR/R| ≤ 0,05<br/>Dann: 0,9025 v ≤ v̂ ≤ 1,1025 v, &nbsp; v = |H|R<br/>e<sub>l</sub> &lt; 0 sicher erst bei 0,9025 v &gt; 1')
p('Die Fehlerbox wird ohne Unabhängigkeitsannahme fortgepflanzt. Sie ist eine Sensitivitätsdiagnose und kein aus CST-Daten gewonnenes Konfidenzintervall. Unbekannte weitere Fehlerbeiträge verhindern eine physikalische Freigabe ohnehin.')
table([['105 vorab gewählte innere Kugelfälle','Gefangen','Ungefangen','HOLD'],
 ['Eng eingeschlossene klassische Referenz','4','101','0'],
 ['Hypothetische ±5-%-Box in H und R','1','95','9']],[286,68,82,68])
p('Ein Intervall, das null enthält, belegt keine exakt marginale Fläche. Dafür wird ein eigener Gleichheits- oder Wurzelnachweis mit eingeschlossener Lage benötigt. Auch eine negative mittlere Staubexpansion oder Kompaktheit allein ersetzt die Prüfung beider zukünftiger Nullrichtungen nicht.')
p('Für dynamische CST-Flächen bleiben zusätzlich Flächenrekonstruktion, Nullrichtungen und deren Normierung, räumliche Abdeckung, Randfehler sowie die Statistik einer Flächensuche festzulegen. Die physikalischen Verfeinerungsregeln des Modellvertrags gelten weiterhin.','S')

page(7,'Trapping und Regularität bleiben getrennt')
p('Die eingefügte klassische Lösung ist im gesamten festen Zeitfenster regulär, obwohl für die größte Masse bereits runde gefangene Flächen existieren. Die Regularitätsaussage wird weder aus dem Trapping-Nachweis noch aus einem Volumenminimum abgeleitet.')
eq('(ρ/ρ<sub>0</sub>)² ≤ 16<br/>K<sub>innen</sub>/K<sub>0</sub> ≤ 960, &nbsp; K<sub>außen</sub>/K<sub>0</sub> ≤ 768<br/>ρ<sub>0</sub> = M/V<sub>0</sub>, &nbsp; K<sub>0</sub> = (GM/R<sub>0</sub>³)²')
p('Diese Schranken gelten analytisch im gesamten Referenzfenster einschließlich der einseitigen Oberflächenwerte. Beim Oberflächendurchgang M = 4 sind Kin = 15/4096 und Kout = 3/1024 endlich. Die klassische Referenz wird außerhalb des geprüften Fensters später singulär; sie demonstriert keine Singularitätsauflösung.')
table([['Entscheidungsebene','Status'],
 ['Klassische lokale runde Trapping-Flächen','Nachgewiesen für M = 4 nach dem angegebenen Durchgang.'],
 ['Klassischer Innen-/Außenanschluss','Analytisch konsistent, 15 numerische Referenzkontrollen.'],
 ['Physikalische CST-Gates an P4','72 gültige Datensätze; alle acht Gates separat HOLD.'],
 ['CST-Regularität','HOLD: Operatoren, gemeinsame Momentenschranken, Tailkontrolle und physikalische Konvergenz fehlen.'],
 ['Globaler Ereignishorizont / Fortsetzung','Nicht aus dem endlichen Zeitfenster bestimmt.']],[242,262])
h('Welche Horizonte hier nicht bestimmt sind')
p('Ein globaler Ereignishorizont hängt von der Zukunftsfortsetzung und dem kausalen Zugang zur zukünftigen Nullunendlichkeit ab. Diese Daten werden nicht ergänzt. Die Rechnung klassifiziert lokale marginale Äste und runde gefangene Sphären. Fehlendes rundes Trapping schließt allgemeine deformierte gefangene Flächen nicht aus.')

page(8,'Nachrechnung, Herkunft und nächste Bedingung')
h('Prüfmaterial')
table([['Datei / Verzeichnis','Inhalt'],
 ['plan.json, plan.sha256','Unveränderter lokaler Prüfplan mit Toleranzen, Flächen, Zeiten und Aussagegrenzen.'],
 ['analyze.py, intervals.py','Deterministische Rechnung; Python-Standardbibliothek, auch mit -O.'],
 ['inputs/','Veröffentlichte Vorgängerdaten; SHA-256 und Main-Commit dokumentiert.'],
 ['results/','Expansionen, Gebietsprüfungen, 216 Flächenableitungen, zwölf Ereignisintervalle, 25 Kontrollen und 72 P4-Entscheidungen.'],
 ['DERIVATION.md','Vollständige Ableitung, Randprüfung, Fehlerfortpflanzung und Quellen.']],[180,324])
eq('Nachrechnung im entpackten Paket:<br/><font face="DVM" size="9">python3 -O -B analyze.py</font>')
p('Der Modellvertrag und die unabhängige Korrespondenzvorprüfung stammen aus dem veröffentlichten Main-Stand b4a52636c506288462e21d88e0f6bd152a78b540. Die neuen Rechnungen verwenden keine physikalischen CST-Validierungsdaten. Sämtliche Paketdateien sind durch SHA-256 erfasst.','S')
h('Nächste wissenschaftliche Voraussetzung')
p('Für einen physikalischen CST-Trapping-Nachweis müssen der gekoppelte Dynamikkern und die korrespondierende Geometrie zuerst qualifiziert sein. Danach werden geschlossene Flächen und beide Nullrichtungen aus denselben dynamischen Daten rekonstruiert, mit vollständigem Fehlerbudget und physikalisch abgeglichener Verfeinerung. Regularität bleibt an jedem Ereignis ein eigener Prüfpunkt.')
h('Primärquellen und Begriffe')
p('1. S. A. Hayward, General laws of black-hole dynamics, Phys. Rev. D 49, 6467 (1994). DOI: 10.1103/PhysRevD.49.6467; arXiv:gr-qc/9303006. Lokale marginale Flächen und innere/äußere Klassifikation.','S')
p('2. I. Bengtsson, E. Jakobsson, J. M. M. Senovilla, Trapped surfaces in Oppenheimer-Snyder black holes, Phys. Rev. D 88, 064012 (2013). DOI: 10.1103/PhysRevD.88.064012; arXiv:1306.6486. Grenzen der Beschränkung auf runde Sphären.','S')
p('3. H. Andréasson, G. Rein, Oppenheimer-Snyder type collapse for a collisionless gas, arXiv:2410.06701, Abschnitt 5.1. Marginal gebundene klassische Staubreferenz in PG-Koordinaten; kein Übertrag der Vlasov-Sätze auf CST.','S')
p('Die konkreten Expansionen, Anschlussgrößen und Schranken sind für die feste Referenz hier direkt hergeleitet. Die Literaturbegriffe sind keine neue CST-Ableitung.','S')

def footer(c,doc):
    c.setStrokeColor(colors.HexColor('#cdd8dd'));c.line(44,809,551,809)
    c.setFillColor(muted);c.setFont('DV',7)
    c.drawString(44,25,'CST-DUST · Klassische Referenz; physikalischer CST-Test HOLD / NOT_RUN · 06.11.2026')
    c.drawRightString(551,25,str(doc.page))
pdf=OUT/'CST_DUST_Expansion_Trapping_v0_1.pdf'
doc=SimpleDocTemplate(str(pdf),pagesize=A4,rightMargin=45,leftMargin=50,topMargin=53,bottomMargin=45,
    title='CST-DUST: Expansion und Trapping v0.1',author='Thomas Gfeller · CST-DUST Forschungsprogramm')
doc.build(story,onFirstPage=footer,onLaterPages=footer)
print(pdf)
