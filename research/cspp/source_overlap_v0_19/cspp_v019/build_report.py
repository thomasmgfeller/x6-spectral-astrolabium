"""Build a human-readable report from the archived numerical results and proof."""
import json,re,math,textwrap
from pathlib import Path
from xml.sax.saxutils import escape
from flint import arb
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from reportlab.pdfgen import canvas
from reportlab.platypus import SimpleDocTemplate,Paragraph,Spacer,Table,TableStyle,PageBreak,Image,Preformatted,KeepTogether
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet,ParagraphStyle
from reportlab.lib.enums import TA_LEFT
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.pagesizes import A4

HERE=Path(__file__).resolve().parent
OUT=HERE.parent/'output/pdf/Quellnormen_Intervallgeometrie_v0_19.pdf'
NAVY=colors.HexColor('#16354a');TEAL=colors.HexColor('#087f8c');INK=colors.HexColor('#253744');GRAY=colors.HexColor('#617381');PALE=colors.HexColor('#eef4f6')


def plot(data,old):
    before=max(float(arb(a['best_grid_full_beyond5']['bound'])) for a in old['archives'])
    mid=max(float(arb(a['improved_v18_split_bound'])) for w in data['windows'] for a in w['archives'])
    after=max(float(arb(a['full_remainder_L1_bound'])) for w in data['windows'] for a in w['archives'])
    plt.rcParams.update({'font.family':'DejaVu Sans','font.size':10})
    fig,ax=plt.subplots(figsize=(7,2.7))
    xs=[math.log10(before),math.log10(mid),math.log10(after)]
    labs=['v0.18: globale Maxima','v0.19: neue Konstanten im alten Split','v0.19: integrierte Feld- und Kernhülle']
    for y,(x,lab) in enumerate(zip(xs,labs)):
        ax.plot([0,x],[y,y],color='#cfdee3',lw=5,zorder=1)
        ax.scatter([x],[y],s=72,color=['#617381','#32758c','#087f8c'][y],zorder=2)
        ax.text(x+1.3,y,f'{[before,mid,after][y]:.2e}',va='center',fontsize=9)
    ax.axvline(-3,color='#aa563c',lw=1.5,ls='--')
    ax.text(-2.1,-.57,'Vergleichsmaßstab 0,001',fontsize=8,color='#aa563c')
    ax.set_yticks(range(3),labs);ax.invert_yaxis();ax.set_xlim(-5,66)
    ax.set_xticks([0,10,20,30,40,50,60],['1','10¹⁰','10²⁰','10³⁰','10⁴⁰','10⁵⁰','10⁶⁰'])
    ax.set_xlabel('Größte obere Restschranke über die acht Fälle (logarithmisch)',fontsize=8)
    ax.spines[['top','right','left']].set_visible(False);ax.tick_params(axis='y',length=0)
    ax.grid(axis='x',alpha=.15)
    fig.tight_layout()
    fig.savefig(HERE/'results/majorant_comparison.png',dpi=200,bbox_inches='tight')
    fig.savefig(HERE/'results/majorant_comparison.svg',bbox_inches='tight')
    plt.close(fig)


def main():
    OUT.parent.mkdir(parents=True,exist_ok=True)
    data=json.loads((HERE/'results/BOUNDS_512.json').read_text())
    old=json.loads((HERE/'evidence/v18_BOUNDS_192.json').read_text())
    tests=json.loads((HERE/'results/CHECKS.json').read_text())
    plot(data,old)
    fonts='/usr/share/fonts/truetype/dejavu/'
    for name,file in [('DV','DejaVuSans.ttf'),('DVB','DejaVuSans-Bold.ttf'),('DVM','DejaVuSansMono.ttf')]:
        pdfmetrics.registerFont(TTFont(name,fonts+file))
    pdfmetrics.registerFontFamily('DV',normal='DV',bold='DVB',italic='DV',boldItalic='DVB')
    styles=getSampleStyleSheet()
    styles.add(ParagraphStyle(name='BodyX',fontName='DV',fontSize=9.2,leading=13.3,textColor=INK,spaceAfter=7))
    styles.add(ParagraphStyle(name='SmallX',parent=styles['BodyX'],fontSize=8,leading=11,textColor=GRAY))
    styles.add(ParagraphStyle(name='TitleX',fontName='DVB',fontSize=26,leading=31,textColor=NAVY,spaceAfter=16))
    styles.add(ParagraphStyle(name='H1X',fontName='DVB',fontSize=15,leading=20,textColor=NAVY,spaceBefore=8,spaceAfter=10,keepWithNext=True))
    styles.add(ParagraphStyle(name='H2X',fontName='DVB',fontSize=11.3,leading=15,textColor=TEAL,spaceBefore=12,spaceAfter=7,keepWithNext=True))
    styles.add(ParagraphStyle(name='CodeX',fontName='DVM',fontSize=7.4,leading=10.6,textColor=INK,leftIndent=9,spaceAfter=9))
    def p(s,style='BodyX'):return Paragraph(s,styles[style])
    story=[]
    story += [p('CSPP · ANALYTISCHE ENTWICKLUNG · v0.19','SmallX'),Spacer(1,16),p('Quellnormen und<br/>geometrischer Rest','TitleX'),p('Die Schranke wird enger.<br/>Die Genauigkeitsentscheidung bleibt offen.','H1X')]
    story += [p('29. Oktober 2026 | Fortsetzung von CSPP v0.18 / PR #150','SmallX'),Spacer(1,10)]
    story += [p('Die tatsächlichen Ableitungen des festgelegten Anfangsfelds ersetzen die bisherigen pauschalen Quellmaxima. Die Archivkonditionierung wird auf die kausale Vergangenheit des Detektors begrenzt. Eine gemeinsame Integration der Feld- und Kernhüllen liefert eine wesentlich kleinere Gesamtmajorante.')]
    table=[[p('<b>Größe</b>'),p('<b>v0.18</b>'),p('<b>v0.19</b>')],
      [p('Globale KG-Feldmajorante'),p('ca. 1,52 × 10⁹'),p('≤ 6,429644')],
      [p('Archivfaktor für W0 / W1'),p('ca. 1,36 × 10³⁵'),p('≤ 229327 / 1317148')],
      [p('Gesamter transportierter Rest'),p('ca. 1,3-1,8 × 10⁵⁴'),p('≤ 2,364-3,388 × 10¹⁴')]]
    t=Table(table,colWidths=[205,125,165]);t.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,0),PALE),('VALIGN',(0,0),(-1,-1),'TOP'),('BOTTOMPADDING',(0,0),(-1,-1),10),('TOPPADDING',(0,0),(-1,-1),8),('LINEBELOW',(0,0),(-1,0),.7,TEAL),('LINEBELOW',(0,1),(-1,-1),.4,colors.HexColor('#d7e1e6'))]));story += [t,Spacer(1,14)]
    story += [p('<b>Rund 40 Größenordnungen Verbesserung der Obergrenze.</b> Die neuen Werte bleiben weit über 0,001. Sie sind weder beobachtete Fehler noch Fehleruntergrenzen. Eine Widerlegung der Operatorfamilie folgt daraus nicht.')]
    call=Table([[p('<b>METHOD_HOLD · G1 HOLD</b><br/>Individuelle Genauigkeit: NOT_CERTIFIED<br/>Frisches Bestätigungsensemble: NOT_RUN')]],colWidths=[495]);call.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,-1),PALE),('BOX',(0,0),(-1,-1),.6,TEAL),('LEFTPADDING',(0,0),(-1,-1),12),('TOPPADDING',(0,0),(-1,-1),10),('BOTTOMPADDING',(0,0),(-1,-1),10)]));story += [call,Spacer(1,12),p('Unverändert: Quelle, Normierung, Dichte, Operator, Detektorfenster und Fehlerziel. Keine neue Zufallswolke und keine neue statistische Freigaberegel.','SmallX'),PageBreak()]
    story += [p('Was die Verbesserung trägt','H1X'),Image(str(HERE/'results/majorant_comparison.png'),width=495,height=191),p('Gezeigt ist jeweils die größte obere Schranke. Die drei Punkte sind unterschiedliche Abschätzungen derselben Restgröße, keine Messreihe.','SmallX'),Spacer(1,5)]
    story += [p('Acht Fälle, getrennt ausgewiesen','H2X')]
    rows=[[p('<b>Archiv</b>'),p('<b>W0: [3/4, 1]</b>'),p('<b>W1: [1, 5/4]</b>')]]
    rounded=[('d0_r00','3,278 × 10¹⁴','3,388 × 10¹⁴'),('d0_r01','2,364 × 10¹⁴','2,443 × 10¹⁴'),('d0_r02','2,900 × 10¹⁴','2,997 × 10¹⁴'),('d0_r03','2,413 × 10¹⁴','2,494 × 10¹⁴')]
    for row in rounded:rows.append([p(escape(x)) for x in row])
    t=Table(rows,colWidths=[165]*3);t.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,0),PALE),('VALIGN',(0,0),(-1,-1),'TOP'),('TOPPADDING',(0,0),(-1,-1),6),('BOTTOMPADDING',(0,0),(-1,-1),6),('LINEBELOW',(0,0),(-1,-1),.3,colors.HexColor('#d7e1e6'))]));story += [t,p('Alle Tabellenwerte nach oben gerundet. Gegenstand: E[|A∞ - A₅| | festes Ω₅-Archiv].','SmallX')]
    story += [p('Kontrolliert und reproduzierbar','H2X'),p(f"{tests['precision_overlap_count']} Präzisionsvergleiche bei 384/512 Bit; 35 Quellnormen über eine zweite Identität; eine validierte direkte Quadratur; 49 bedingte Kernkontrollen; drei Negativkontrollen. Wolfram bestätigt zusätzlich die erste Quellnorm und die Geometriekonstanten.")]
    story += [p('Was noch fehlt','H2X'),p('Die geometrische Hülle ist noch keine Auswertung aller tatsächlichen Archivintervalle. Offen bleiben die lokalen KG-Werte, ihre Überlappungsvolumina und die zugehörigen festen Punktzahlen im endlichen äußeren Historybereich. Der exakte bedingte Gewichtskern ist dafür jetzt implementiert und geprüft.')]
    story += [p('<b>Anschluss:</b> Diesen endlichen Bereich mit validierter Quadratur und tatsächlichen Archivdaten auswerten; nur den verbleibenden Fernteil durch eine analytische Hülle begrenzen. Keine neue Bestätigungsstichprobe und keine große Gebietserweiterung auf Grundlage dieser Majorante.'),PageBreak()]
    story += [p('Vollständige Herleitung','H1X'),p('Die folgenden Seiten dokumentieren Definitionen, Beweisschritte, Kontrollumfang und Aussagegrenzen.','SmallX')]
    lines=(HERE/'PROOF.md').read_text().splitlines();buf=[];code=[]
    def flush():
        if buf:story.append(p(escape(' '.join(buf))));buf.clear()
    def flushcode():
        if code:
            wrapped=[]
            for line in code:wrapped.extend(textwrap.wrap(line,width=104,replace_whitespace=False,drop_whitespace=False) or [''])
            story.append(Preformatted('\n'.join(wrapped),styles['CodeX']));code.clear()
    for line in lines[1:]:
        if line.startswith('    '):flush();code.append(line[4:]);continue
        flushcode()
        if line.startswith('## '):
            flush()
            if line.startswith('## 10.'):story.append(PageBreak())
            story.append(p(escape(line[3:]),'H2X'))
        elif not line.strip():flush()
        else:buf.append(line)
    flush();flushcode()
    def footer(c,doc):
        c.setStrokeColor(colors.HexColor('#d7e1e6'));c.line(48,43,A4[0]-48,43)
        c.setFont('DV',7);c.setFillColor(GRAY)
        c.drawString(48,30,'CSPP v0.19 | 29. Oktober 2026 | METHOD_HOLD / G1 HOLD')
        c.drawRightString(A4[0]-48,30,str(doc.page))
    doc=SimpleDocTemplate(str(OUT),pagesize=A4,rightMargin=48,leftMargin=48,topMargin=44,bottomMargin=56,title='CSPP v0.19 - Quellnormen und geometrischer Rest',author='CSPP Forschungsprojekt')
    doc.build(story,onFirstPage=footer,onLaterPages=footer)
    print(OUT)


if __name__=='__main__':main()
