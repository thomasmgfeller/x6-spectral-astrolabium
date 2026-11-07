"""Render the human-readable report. Calculation/replay need only stdlib."""
from pathlib import Path
from fractions import Fraction as F
import json
from xml.sax.saxutils import escape
from reportlab.pdfgen import canvas
from reportlab.platypus import SimpleDocTemplate,Paragraph,Spacer,Table,TableStyle,PageBreak,KeepTogether
from reportlab.lib.styles import getSampleStyleSheet,ParagraphStyle
from reportlab.lib import colors
from reportlab.lib.enums import TA_LEFT
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
ROOT=Path(__file__).resolve().parent
OUT=ROOT/'CST_DUST_Praeparation_Rueckkehrtest_Fehlerbudget_v0_1.pdf'
FONT='/usr/share/fonts/truetype/dejavu/'
for name,file in [('DV','DejaVuSans.ttf'),('DV-Bold','DejaVuSans-Bold.ttf'),('Mono','DejaVuSansMono.ttf')]:
    pdfmetrics.registerFont(TTFont(name,FONT+file))
pdfmetrics.registerFontFamily('DV',normal='DV',bold='DV-Bold',italic='DV',boldItalic='DV-Bold')
NAVY=colors.HexColor('#12354A');TEAL=colors.HexColor('#087E8B');PALE=colors.HexColor('#EDF5F7')
styles={
'title':ParagraphStyle('title',fontName='DV-Bold',fontSize=23,leading=28,textColor=NAVY,spaceAfter=16),
'sub':ParagraphStyle('sub',fontName='DV',fontSize=10,leading=15,textColor=TEAL,spaceAfter=10),
'h1':ParagraphStyle('h1',fontName='DV-Bold',fontSize=15,leading=20,textColor=NAVY,spaceAfter=12),
'h2':ParagraphStyle('h2',fontName='DV-Bold',fontSize=11,leading=16,textColor=TEAL,spaceBefore=10,spaceAfter=6),
'body':ParagraphStyle('body',fontName='DV',fontSize=9.3,leading=14,spaceAfter=8),
'small':ParagraphStyle('small',fontName='DV',fontSize=8,leading=11.5,spaceAfter=6),
'formula':ParagraphStyle('formula',fontName='Mono',fontSize=8.1,leading=12,backColor=PALE,borderPadding=7,spaceBefore=4,spaceAfter=12),
'cell':ParagraphStyle('cell',fontName='DV',fontSize=8.2,leading=11.5),
'head':ParagraphStyle('head',fontName='DV-Bold',fontSize=8.2,leading=11.5,textColor=colors.white)}
story=[]
def p(text,style='body'):story.append(Paragraph(text,styles[style]))
def h(text):p(text,'h2')
def f(text):p(escape(text).replace('\n','<br/>'),'formula')
def page(title):story.append(PageBreak());p(title,'h1')
def table(headers,rows,widths):
    data=[[Paragraph(escape(str(x)),styles['head']) for x in headers]]
    data.extend([[Paragraph(escape(str(x)),styles['cell']) for x in row] for row in rows])
    t=Table(data,colWidths=widths,repeatRows=1,hAlign='LEFT')
    t.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,0),NAVY),('VALIGN',(0,0),(-1,-1),'TOP'),
        ('LEFTPADDING',(0,0),(-1,-1),7),('RIGHTPADDING',(0,0),(-1,-1),7),
        ('TOPPADDING',(0,0),(-1,-1),7),('BOTTOMPADDING',(0,0),(-1,-1),7),
        ('ROWBACKGROUNDS',(0,1),(-1,-1),[colors.white,PALE]),('LINEBELOW',(0,-1),(-1,-1),0.6,TEAL)]))
    story.append(t);story.append(Spacer(1,10))

p('CST-DUST<br/>Präparation, Rückkehrtest<br/>und Fehlerbudget','title')
p('Analytischer Prüfbericht v0.1 · 7. November 2026','sub')
p('<b>Ergebnis:</b> Die Referenzsichtbarkeit lässt sich unter klaren operationalen Zusatzbedingungen eindeutig festlegen. Eine bekannte Rang-eins-Auslese, eine passende phasenfreie Kalibrierung und eine vorgegebene vollständige Recordverteilung genügen. Diese Bedingungen sind noch nicht aus einer physikalischen CST-Kopplung hergeleitet.')
table(['Prüffrage','Gesichertes Ergebnis'],[
('Reichen vollständige klassische Recorddaten?','Nein. Dieselben Daten erlauben verschiedene kohärente Präparationen und Auslesen.'),
('Was legt den Rückkehrtest bedingt fest?','Ein qualifizierter Rang-eins-Projektor plus perfekte Nullphasen-Kalibrierung erzwingen die passende reine Präparation.'),
('Wie wirken unvollkommene Bedingungen?','Eine bewiesene Fehlergrenze trennt Kalibrierung, Effektabweichung und die gesamte klassische Verteilung.'),
('Ist damit der physikalische Detektor gefunden?','Nein. Zustandsquelle, Kopplung, Zugänglichkeit und gravitative Rückwirkung bleiben offen.')],[160,345])
h('Was dieser Schritt konkret leistet')
p('Der vorherige Maßvergleich wird auf Zustände, Effekte und vollständige Messinstrumente erweitert. Eine explizite Familie zeigt die verbleibende Unterbestimmtheit. Danach wird ein bedingter Eindeutigkeitssatz mit einer quantitativen Fehlerschranke bewiesen. Die zugehörigen Kontrollen benötigen nur kleine rationale Rechnungen.')
h('Grenze der Aussage')
p('<b>Alle acht physikalischen Gates bleiben HOLD.</b> Keine vollständige CST-Dynamik, physikalische Detektorkopplung, gravitative Rückwirkung, Singularitätsauflösung oder Bounce werden hergeleitet. Die Zahlenbudgets sind diagnostische Beispiele und keine gemessenen Kalibrierwerte.')
p('Kein n=5-Produktionslauf und keine kostenpflichtige Rechenleistung. Der bestehende Community-Auftrag bleibt unverändert.','small')
p('Basis: Main nach PR 260, Commit c04214b9b6397abe9384bbcd728998b5c6b75173. Vollständige Beweise, fünf gepinnte Quellen und Reproduktionscode liegen im Prüfpaket.','small')

page('1 · Gleiche klassische Daten, andere Kohärenz')
p('Im bedingten Ein-Element-Raum H=L²(dx ν₀) verwenden wir den Nullatom-Anteil |a> und den kontinuierlichen Anteil |c>. Beide sind normiert, orthogonal und in der Uhr x konstant. Auf ihrem Spannraum gilt:')
f('ρ_η = (1/2) [[1, η], [η, 1]]\nE_κ = (1/2) [[1, κ], [κ, 1]],     -1 ≤ η, κ ≤ 1')
p('Die Eigenwerte (1±η)/2 und (1±κ)/2 sichern einen gültigen Zustand und einen gültigen Effekt. Außerhalb dieses Spannraums sind beide null; der zweite vollständige Ausgang ist I−Eκ.')
p('<b>Für jede diagonale Recordfunktion f gilt</b> Tr(ρη f)=∫f dx dν₀, unabhängig von η. Damit stimmen die gesamte klassische Recordverteilung und alle existierenden Wirkungs-Momente überein. Die inneren Kohärenzen im kontinuierlichen Anteil werden dabei festgehalten.')
f('B = ∫₀¹ dx ∫₀¹ dw exp[-i μ w(1/2 + 4h²x²)]\nP(η,κ) = [1 + |B|² + 2ηκ Re(B)] / 4')
p('Bei μ=0 folgt P=(1+ηκ)/2. Für κ=1 reicht die Erfolgswahrscheinlichkeit von null bis eins, obwohl die klassischen Daten gleich bleiben. Ein Scan dieser Wahrscheinlichkeiten bestimmt nur das Produkt ηκ; Präparation und Detektorkohärenz sind damit nicht getrennt identifizierbar.')
rows=[]
data=json.loads((ROOT/'results/continuous_readout.json').read_text())
for hv in ['1/4','1/2']:
    row=[hv]
    for ev in ['1','0','-1']:
        item=next(x for x in data['cases'] if x['h']==hv and x['mu']=='1' and x['eta']==ev and x['kappa']=='1')
        row.append(f"{float(F(item['center'])):.9f}")
    rows.append(row)
table(['h','P(η=1)','P(η=0)','P(η=−1)'],rows,[65,145,145,150])
p('Tabelle: κ=1, μ=1; ungefähre Mittelpunkte der exakten Einschließungen. Keine Messwerte. η=κ=1 gewinnt die bisherige Referenzsichtbarkeit zurück.','small')
h('Kontrollierte kontinuierliche Rechnung')
p('Re B und |B|² werden aus exakten rationalen Momenten bis Kosinusgrad 24 berechnet. Mit A=1/2+4h² ist jeder Kosinusrest höchstens r=(|μ|A)²⁶/26!; für P beträgt der Rest höchstens (1+2|ηκ|)r/4. Alle 150 vorab festgelegten Fälle sind dokumentiert.','small')

page('2 · Wann der Rückkehrtest eindeutig wird')
p('Die folgenden Bedingungen sind zusätzliche Annahmen im erklärten Referenzmodell. Sie sind nicht allein aus Momenten, Maßkovarianz oder einer abstrakten Messdilatation ableitbar.')
table(['Bedingung','Bedeutung'],[
('Qualifizierter Effekt','E=|φ><φ| ist ein bekannter Rang-eins-Projektor; ||φ||=1. Ausfall I−E bleibt ein echter Ausgang.'),
('Phasenfreie Kalibrierung','Tr(Eρ)=1 bei unveränderter Präparation und Auslese.'),
('Vollständige klassische Verteilung','dλ=|φ(Y)|²dν(Y) ist vorgegeben, einschließlich aller gemeinsamen Abhängigkeiten.'),
('Festgehaltene Wirkungsphase','D ist die erklärte Multiplikation mit exp(iS(Y)). Es wird keine CST-Bewegungsgleichung daraus abgeleitet.')],[165,340])
h('Bedingter Eindeutigkeitssatz')
f('Tr(Eρ)=1  und  Rang(E)=1  ⇒  ρ=E\nP(S) = |<φ|D|φ>|² = |∫ exp(iS) dλ|²')
p('Beweis: Aus Tr[(I−E)ρ]=0 folgt ||(I−E)√ρ||²_HS=0. Der Träger von ρ liegt daher im eindimensionalen Bild von E; die Spur eins erzwingt ρ=E. Die Erfolgsformel folgt unmittelbar.')
p('Eine zusätzliche Wellenfunktionsphase φ→exp(if)φ hebt sich im abgestimmten Rückkehrtest auf, weil sie mit D kommutiert. Bei einem äquivalenten Maßwechsel werden φ und E gemeinsam transportiert. Die Recordverteilung λ und die Erfolgsvorhersage bleiben gleich.')
h('Warum der Nulltest allein nicht genügt')
p('<b>Der stets erfolgreiche Detektor E=I besteht denselben phasenfreien Test.</b> Er reagiert jedoch auf keine Wirkungsphase. Die Rang-eins-Eigenschaft muss deshalb unabhängig qualifiziert werden. Ebenso legt eine endliche Momentliste die benötigte vollständige Recordverteilung nicht fest.')
p('Die Eindeutigkeit betrifft die Erfolgsvorhersage unter diesen Bedingungen. Sie wählt keinen kosmologischen Zustand, keinen zulässigen CST-Detektor und keinen eindeutigen Nachmesskanal aus.','small')

page('3 · Ein überprüfbares Fehlerbudget')
p('Sei E das ideale Rang-eins-Ziel und Ẽ der tatsächliche Effekt. Die drei Größen haben getrennte Bedeutungen:')
table(['Größe','Erforderlicher Nachweis'],[
('ε','Obergrenze für den phasenfreien Ausfall: Tr(Ẽρ) ≥ 1−ε.'),
('τ','Unabhängige Effektqualifizierung: ||Ẽ−E|| ≤ τ.'),
('δ','Totalvariation zwischen der vollständigen gemeinsamen Recordverteilung von φ und der Referenzverteilung.')],[55,450])
f('|P_tatsächlich − P_Referenz|\n ≤ min{1, τ + √min(1, ε+τ) + 4δ}')
p('Begründung: Die Kalibrierung liefert Tr(Eρ)≥1−ε−τ. Für ein reines Ziel gilt die Spurweiten-Schranke T(ρ,E)≤√(1−Tr(Eρ)). Ein Effekt unterscheidet zwei Zustände höchstens um diese Spurweite. Die Effektabweichung trägt höchstens τ bei. Die Änderung der Phasenamplitude ist höchstens 2δ, die der Sichtbarkeit höchstens 4δ.')
p('Die Spurweiten-Schranke wird im vollständigen Beweis aus der reinen Zustandsformel, einer spektralen Zerlegung und der Konkavität der Quadratwurzel hergeleitet. Ein exakter endlicher Kontrollsatz prüft 208 Fälle.')
table(['ε','τ','δ','Fehler höchstens'],[
('0','0','0','0'),('10⁻⁴','0','0','0,01'),('9·10⁻⁶','10⁻⁶','10⁻⁵','0,003203277661')],[100,100,100,205])
p('<b>Dies sind Diagnosebudgets, keine gemessenen Kalibrierwerte.</b> Der letzte Wert ist nach oben gerundet. Die Auswertung verwendet eine ganzzahlige Quadratwurzeleinschließung.','small')
h('Was in dieser Grenze nicht enthalten ist')
p('Eine endliche Momentliste oder einzelne Marginalverteilungen ersetzen δ nicht. Modell- und Dynamikfehler sind nicht enthalten: Beide Seiten müssen dieselbe erklärte Wirkungsphase D verwenden. Experimentelle Konfidenzgrenzen müssen gesondert erhoben werden.')
p('Für getrennte Zahlkanäle können die Grenzen mit den vorhandenen Normmassen gewichtet und unbekannte Sektoren über deren Restmasse begrenzt werden. Eine kohärente Auslese über verschiedene Elementzahlen benötigt dagegen eine Qualifizierung des gesamten Zustands.','small')

page('4 · Zustand, Effekt und Instrument transportieren')
p('Eine reine Umstellung der Maßdarstellung muss alle operationalen Objekte gemeinsam erfassen. Für U:Hθ→H₀ gilt:')
f('ρθ = U†ρ₀U       Eθ = U†E₀U\nKθ = U†K₀U       Dθ = U†D₀U')
p('Durch Einsetzen heben sich die U-Faktoren in jedem Produkt auf. Erfolgswahrscheinlichkeiten, unnormierte Zustandsupdates und sequentielle Instrumentwahrscheinlichkeiten stimmen überein. Im gewichteten endlichen Kontrollraum ist der richtige Adjungierte A♯=G⁻¹A†G mit G=U†U.')
p('Die Kontrollen bestätigen 300 gewichtete Wahrscheinlichkeitsvergleiche, 240 sequentielle Vergleiche und drei Kraus-Vollständigkeitsidentitäten. Diese kleinen Matrixräume prüfen die Algebra; sie sind keine Quadratur kontinuierlicher CST-Historien.')
h('Gleicher Effekt bedeutet nicht gleicher Nachmesszustand')
p('Für E=|+><+| sind sowohl {E,I−E} als auch {ZE,Z(I−E)} vollständige Instrumente, mit Z=diag(1,−1). Ihre Effekte und ersten Erfolgswahrscheinlichkeiten sind identisch.')
table(['Erfolgs-Update bei Eingang |+>','Erster Erfolg','Zweiter E-Test'],[
('Lüders: Zustand bleibt |+>','1','1'),
('Zusätzlicher Phasenwechsel: Zustand wird |−>','1','0')],[305,100,100])
p('Der erste Rückkehrtest identifiziert daher den Nachmesskanal nicht. Für Aussagen über aufeinanderfolgende Messungen ist die vollständige Zustandsänderung ein eigener Teil des physikalischen Modells.')
h('Reichweite')
p('Die mathematische Konstruktion gültiger Zustände und vollständig positiver Instrumente ist eine Konsistenzprüfung. Sie belegt weder eine verfügbare Apparatur noch einen zulässigen gravitativen Wechselwirkungs-Hamiltonoperator. Die Darstellungskovarianz ist auch keine Herleitung einer unitären CST-Zeitentwicklung.')

page('5 · Evidenz und nächster physikalischer Engpass')
table(['Kontrolle','Ergebnis'],[
('Kontinuierliche n=1-Auslese','150 rational eingeschlossene Fälle'),
('Publizierte Referenz wiedergewonnen','4 exakt gleiche Polynommittelpunkte'),
('Nur Produkt ηκ identifizierbar','108 exakte Entartungskontrollen'),
('Darstellung und Instrument','300 Wahrscheinlichkeits- und 240 Sequenzkontrollen'),
('Kalibrierschranke','208 exakte Matrixfälle'),
('Negativkontrollen','8 falsche Annahmen bzw. Eingaben zurückgewiesen'),
('Isolierte Nachrechnung','4 wissenschaftliche Dateien bytegleich reproduziert')],[260,245])
p('Die allgemeinen Sätze beruhen auf den ausgeschriebenen Beweisen. Die endlichen Kontrollen prüfen die Implementierung. Es handelt sich nicht um externe Replikation oder eine formale Beweisassistentenprüfung.','small')
h('Reproduktion')
f('python3 -B verify_package.py\npython3 -B replay.py')
p('Python-Standardbibliothek genügt. Prüfplan, Quellen, exakte Brüche, Beweise und Bericht sind im Prüfpaket enthalten. Die physikalischen Nachweisanforderungen stehen in operational_contract.json.','small')
h('Die nun präzise offene Aufgabe')
p('<b>Eine zulässige CST-Materie-/Randkopplung muss Präparation, vollständige Recordverteilung und den qualifizierten Rückkehrdetektor liefern.</b> Für sequentielle Aussagen ist zusätzlich das Zustandsupdate nötig; für gravitative Aussagen dessen Rückwirkung. Ohne diese Nachweise bleibt die Sichtbarkeit eine konditionale Referenzobservable. Eine genauere n=5-Integration allein löst diese Auswahl nicht.')
p('MODEL, CURRENT, CORRESPONDENCE, BOUNCE, REGULARITY, BOUNDARY, TRAPPING und EXTENSION bleiben HOLD. Keine kostenpflichtige Rechenleistung und kein n=5-Produktionslauf.','small')
h('Quellen und vollständige Herleitung')
p('Projektbasis: <link href="https://github.com/thomasmgfeller/x6-spectral-astrolabium/pull/260" color="#087E8B">GitHub PR 260</link>. Vollständige neue Beweise: DERIVATION.md. Gepinnte Originalquellen: provenance.json.','small')
p('Instrument-Kontext: <link href="https://www.preskill.caltech.edu/ph219/chap3_15.pdf" color="#087E8B">J. Preskill, Quantum Information, Kapitel 3</link>; <link href="https://arxiv.org/abs/1110.6815v2" color="#087E8B">M. G. A. Paris, The modern tools of quantum mechanics</link>. Diese Quellen liefern kein CST-Auswahlgesetz. Externe Volltexte werden nicht verteilt.','small')

def footer(c,doc):
    c.saveState();c.setStrokeColor(TEAL);c.setLineWidth(.6);c.line(45,42,550,42)
    c.setFont('DV',7.5);c.setFillColor(NAVY)
    c.drawString(45,29,'CST-DUST · Präparation / Rückkehrtest / Fehlerbudget · v0.1')
    c.drawRightString(550,29,str(doc.page));c.restoreState()

doc=SimpleDocTemplate(str(OUT),pagesize=(595.276,841.89),rightMargin=45,leftMargin=45,
    topMargin=43,bottomMargin=55,title='CST-DUST Präparation, Rückkehrtest und Fehlerbudget v0.1',
    author='Thomas Gfeller - Forschungsunterlagen',subject='Bedingte operationale Festlegung im erklärten Referenzmodell')
doc.build(story,onFirstPage=footer,onLaterPages=footer)
print(OUT)

