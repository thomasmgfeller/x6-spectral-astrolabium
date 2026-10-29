"""Build the quantitative decision report and complete proof appendix."""
from pathlib import Path
from xml.sax.saxutils import escape
import json,re
from reportlab.platypus import SimpleDocTemplate,Paragraph,Spacer,Table,TableStyle,PageBreak,Image
from reportlab.lib import colors
from reportlab.lib.styles import ParagraphStyle
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

HERE=Path(__file__).resolve().parent
OUT=HERE/'report';OUT.mkdir(exist_ok=True)
for name,file in [('D','DejaVuSans'),('DB','DejaVuSans-Bold'),('DM','DejaVuSansMono')]:
    pdfmetrics.registerFont(TTFont(name,f'/usr/share/fonts/truetype/dejavu/{file}.ttf'))
pdfmetrics.registerFontFamily('D',normal='D',bold='DB',italic='D',boldItalic='DB')
navy=colors.HexColor('#12394b');muted=colors.HexColor('#536873')
styles={
 'title':ParagraphStyle('title',fontName='DB',fontSize=25,leading=31,textColor=navy,spaceAfter=14),
 'sub':ParagraphStyle('sub',fontName='D',fontSize=10,leading=15,textColor=muted,spaceAfter=14),
 'h':ParagraphStyle('h',fontName='DB',fontSize=14,leading=19,textColor=navy,spaceBefore=12,spaceAfter=9,keepWithNext=True),
 'b':ParagraphStyle('b',fontName='D',fontSize=9.4,leading=14,spaceAfter=8,allowWidows=0,allowOrphans=0),
 'small':ParagraphStyle('small',fontName='D',fontSize=8,leading=11.5,spaceAfter=7),
 'cell':ParagraphStyle('cell',fontName='D',fontSize=8.7,leading=12.5),
 'code':ParagraphStyle('code',fontName='DM',fontSize=7.4,leading=11.2,spaceBefore=5,spaceAfter=11,backColor=colors.HexColor('#eef3f6'),borderPadding=7),
}
def p(text,kind='b'):return Paragraph(text,styles[kind])
def table(rows,widths):
    t=Table([[p(x,'cell') for x in row] for row in rows],colWidths=widths,repeatRows=1)
    t.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,0),colors.HexColor('#dfeaf0')),('ROWBACKGROUNDS',(0,1),(-1,-1),[colors.white,colors.HexColor('#f2f6f8')]),('VALIGN',(0,0),(-1,-1),'TOP'),('LEFTPADDING',(0,0),(-1,-1),8),('RIGHTPADDING',(0,0),(-1,-1),8),('TOPPADDING',(0,0),(-1,-1),8),('BOTTOMPADDING',(0,0),(-1,-1),8)]))
    return t
def markup(text):
    out=re.sub(r'\*\*(.*?)\*\*',r'<b>\1</b>',escape(text))
    if text.startswith('https://'):
        label='Projektbasis: PR #149' if 'github.com' in text else 'Last / Penrose: Autorenversion, Theorem 4.4'
        return f'<link href="{escape(text)}" color="#17617d">{escape(label)}</link>'
    return out
def footer(c,doc):
    c.saveState();c.setStrokeColor(colors.HexColor('#c9d9e1'));c.line(43,42,552,42)
    c.setFont('D',8);c.setFillColor(muted);c.drawString(43,28,'CSPP v0.18  |  29. Oktober 2026  |  METHOD_HOLD / G1 HOLD')
    c.drawRightString(552,28,str(doc.page));c.restoreState()
def plot(d):
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    from flint import arb,ctx
    ctx.prec=192
    rows=[r for r in d['grid'] if r['L_power']<=50]
    x=[float(arb(r['L']).log()/arb(10).log()) for r in rows]
    y=[float(arb(r['archive_tail'][0]['bound']).log()/arb(10).log()) for r in rows]
    z=[float(arb(r['archive_full_beyond5'][0]['bound']).log()/arb(10).log()) for r in rows]
    fig,ax=plt.subplots(figsize=(8.3,4.4),layout='constrained')
    ax.plot(x,y,'o-',ms=2.5,lw=1.7,color='#217a9b',label='Ferne History: $G_B D_B b_N(L)$')
    ax.plot(x,z,'s-',ms=2.5,lw=1.7,color='#b76b2a',label='Gesamtrest hinter $\\Omega_5$: $B_{5,N}(L)$')
    ax.axhline(-3,color='#66757d',ls='--',lw=1,label='Vergleichsmaßstab 0,001; kein Freigabegate')
    ax.set(xlabel='$\\log_{10} L$ (History-Zeitabstand)',ylabel='$\\log_{10}$ der berechneten Obergrenze',ylim=(-30,80),title='Bedingte L1-Majoranten für Archiv d0_r00')
    ax.grid(alpha=.2);ax.legend(fontsize=8,loc='lower left');ax.spines[['top','right']].set_visible(False)
    fig.savefig(HERE/'results/majorants.png',dpi=180)
    fig.savefig(HERE/'results/majorants.svg')
    plt.close(fig)
def build():
    d=json.loads((HERE/'results/BOUNDS_192.json').read_text());check=json.loads((HERE/'results/CHECKS.json').read_text())
    plot(d)
    s=[p('Quantitative<br/>Restmajoranten','title'),p('CSPP v0.18 | Quellkonstanten, Archivkonditionierung und kausaler Transport','sub')]
    s+=[p('<b>Der Konvergenzbeweis ist jetzt quantitativ ergänzt.</b> Alle verwendeten Quellkonstanten sind explizit eingeschlossen. Die Restabschätzung summiert sämtliche kausalen Pfade und berücksichtigt die Abhängigkeit zwischen Forcierung und Geometrie.')]
    s+=[table([['Erreicht','Bedeutung'],['Scharfe Schichtgewichtsschranke','κ = 4976184375 / 4294967296 ≈ 1,158608 ersetzt die grobe Zahl 16 bei aktiven Kanten.'],['Vollständiger Transport','Bedingte Pfadfaktoren der vier Archive: etwa 2,73 bis 3,79. Keine Faktorisierung abhängiger Erwartungswerte.'],['Explizite ferne History','Eine numerisch auswertbare, abklingende Majorante mit vollständig bestimmten Konstanten.'],['Gesamtrest hinter Ω₅','Explizite bedingte Erwartungswert-Obergrenzen, bislang um 10<super>54</super>. Damit ist keine Genauigkeitsentscheidung möglich.']],[177,332])]
    s+=[Spacer(1,12),p('<b>Eine große Obergrenze beweist keinen großen tatsächlichen Fehler.</b> Die Rechnung identifiziert die pauschalen Quell- und Konditionierungsschranken als Engpass dieser Abschätzung. Sie verwirft die Operatorfamilie nicht.')]
    s+=[p('<b>METHOD_HOLD und G1 HOLD bleiben bestehen.</b> Keine neue Zufallswolke, keine neue Konfidenzschwelle und keine Änderung des ursprünglichen Fehlerziels 0,001.')]
    s+=[p(f'Validierung: {check["precision_overlaps"]} Präzisionsvergleiche, drei Negativkontrollen und exakte algebraische Gegenprüfungen. Der vollständige Beweis und das reproduzierbare Rechenpaket sind beigefügt.','small')]
    s+=[PageBreak(),p('Was die Zahlen tatsächlich sagen','h')]
    s+=[table([['Archiv','Aktive Knoten','Pfadfaktor ≤','Beste Gitter-Obergrenze ≤'],['d0_r00','65','3,781','1,80 × 10<super>54</super>'],['d0_r01','49','2,726','1,30 × 10<super>54</super>'],['d0_r02','59','3,344','1,59 × 10<super>54</super>'],['d0_r03','50','2,782','1,32 × 10<super>54</super>']],[92,92,110,215])]
    s+=[Spacer(1,7),p('Die rechte Spalte begrenzt E[|A∞ − A₅| | Archiv] für beide normierten Detektorfenster. Sie zeigt die kleinsten Werte innerhalb der erklärten Familie N = 3,…,32 und L = 2³,…,2⁸⁰, keine unter allen Methoden optimale Restschranke.','small')]
    s+=[Image(str(HERE/'results/majorants.png'),width=509,height=270)]
    s+=[p('Die ferne History wird mit wachsendem Abschneidezeitpunkt klein. Der zuvor ausgelassene endliche Historybereich wächst jedoch mit und wird hier nur pauschal eingeschlossen. Deshalb wird der gesamte Rest hinter Ω₅ durch dieselbe Vergrößerung nicht klein. Linien verbinden die berechneten Gitterwerte.','small')]
    s+=[p('Erst bei L = 2⁴⁸ ≈ 2,81 × 10¹⁴ fällt die bedingte ferne Majorante auf dem Gitter unter 0,001. Das ist eine Diagnose dieser groben Abschätzung, keine notwendige Gebietsgröße. Die zusätzliche formale History-Stütze hätte dort bereits rund 6,28 × 10⁵⁷ Poissonpunkte im Mittel.')]
    s+=[p('<b>Anschlussentscheidung:</b> Keine Gebietserweiterung auf dieser Grundlage starten. Als Nächstes die tatsächlichen Quellableitungen und geometrischen Intervallüberlappungen einschließen. Eine Erwartungswertschranke ersetzt weiterhin keinen Fehlernachweis für eine konkrete Realisierung.')]
    s+=[PageBreak()]
    for block in (HERE/'PROOF.md').read_text().strip().split('\n\n'):
        if block.startswith('# '):s.append(p('Vollständige Herleitung und Aussagegrenzen','h'))
        elif block.startswith('## '):s.append(p(markup(block[3:]),'h'))
        elif block.startswith('    '):s.append(p('<br/>'.join(escape(x[4:] if x.startswith('    ') else x).replace(' ','&#160;') for x in block.splitlines()),'code'))
        else:
            regular=[]
            for line in block.splitlines():
                if line.startswith('https://'):
                    if regular:s.append(p(markup(' '.join(regular))));regular=[]
                    s.append(p(markup(line),'small'))
                else:regular.append(line)
            if regular:s.append(p(markup(' '.join(regular))))
    doc=SimpleDocTemplate(str(OUT/'Quantitative_Restmajoranten_v0_18.pdf'),pagesize=(595.276,841.89),leftMargin=43,rightMargin=43,topMargin=45,bottomMargin=56,title='CSPP v0.18 - Quantitative Restmajoranten',author='Thomas Gfeller / Forschungsprojekt X6')
    doc.build(s,onFirstPage=footer,onLaterPages=footer)
    print(OUT/'Quantitative_Restmajoranten_v0_18.pdf')
if __name__=='__main__':build()
