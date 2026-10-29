"""Build an overview and the complete readable proof from preserved sources."""
from pathlib import Path
from xml.sax.saxutils import escape
import json,re
from reportlab.platypus import SimpleDocTemplate,Paragraph,Spacer,Table,TableStyle,PageBreak,KeepTogether
from reportlab.lib import colors
from reportlab.lib.styles import ParagraphStyle
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

HERE=Path(__file__).resolve().parent
OUT=HERE.parent/'output';OUT.mkdir(exist_ok=True)
for name,file in [('D','DejaVuSans'),('DB','DejaVuSans-Bold'),('DM','DejaVuSansMono')]:
    pdfmetrics.registerFont(TTFont(name,f'/usr/share/fonts/truetype/dejavu/{file}.ttf'))
pdfmetrics.registerFontFamily('D',normal='D',bold='DB',italic='D',boldItalic='DB')
navy=colors.HexColor('#12394b');muted=colors.HexColor('#536873')
styles={
 'title':ParagraphStyle('title',fontName='DB',fontSize=25,leading=31,textColor=navy,spaceAfter=14),
 'sub':ParagraphStyle('sub',fontName='D',fontSize=10,leading=15,textColor=muted,spaceAfter=14),
 'h':ParagraphStyle('h',fontName='DB',fontSize=14,leading=19,textColor=navy,spaceBefore=13,spaceAfter=9,keepWithNext=True),
 'b':ParagraphStyle('b',fontName='D',fontSize=9.4,leading=14,spaceAfter=8),
 'small':ParagraphStyle('small',fontName='D',fontSize=8,leading=11.5,spaceAfter=7),
 'cell':ParagraphStyle('cell',fontName='D',fontSize=9,leading=13),
 'code':ParagraphStyle('code',fontName='DM',fontSize=7.5,leading=11.5,spaceBefore=5,spaceAfter=11,backColor=colors.HexColor('#eef3f6'),borderPadding=7),
}
def p(text,kind='b'):return Paragraph(text,styles[kind])
def table(rows):
    t=Table([[p(x,'cell') for x in row] for row in rows],colWidths=[179,330],repeatRows=1)
    t.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,0),colors.HexColor('#dfeaf0')),('ROWBACKGROUNDS',(0,1),(-1,-1),[colors.white,colors.HexColor('#f2f6f8')]),('VALIGN',(0,0),(-1,-1),'TOP'),('LEFTPADDING',(0,0),(-1,-1),8),('RIGHTPADDING',(0,0),(-1,-1),8),('TOPPADDING',(0,0),(-1,-1),9),('BOTTOMPADDING',(0,0),(-1,-1),9)]))
    return t
def markup(text):
    out=escape(text)
    out=re.sub(r'\*\*(.*?)\*\*',r'<b>\1</b>',out)
    # Long reference URLs remain clickable; use a short legible label.
    if out.startswith('https://'):
        url=text
        label=('Projektbasis: PR #148' if 'github.com' in url else
               'Sussman: arXiv 2305.01119' if 'arxiv.org' in url else
               'Sussman: veröffentlichter Artikel, DOI 10.1007/s40818-026-00232-8' if 'springer' in url else
               'Last / Penrose: Autorenversion des Lehrbuchs')
        return f'<link href="{escape(url)}" color="#17617d">{escape(label)}</link>'
    return out
def footer(c,doc):
    c.saveState();c.setStrokeColor(colors.HexColor('#c9d9e1'));c.line(43,42,552,42)
    c.setFont('D',8);c.setFillColor(muted);c.drawString(43,28,'CSPP v0.17  |  29. Oktober 2026  |  METHOD_HOLD / G1 HOLD')
    c.drawRightString(552,28,str(doc.page));c.restoreState()
def build():
    check=json.loads((HERE/'results/ANALYTIC_CHECKS.json').read_text())
    s=[p('Endliche aktive Hülle<br/>und Konvergenz der<br/>KG-History','title'),p('CSPP v0.17 | Analytischer Folgeschritt nach dem Merge von v0.16','sub')]
    s += [p('<b>Die unendliche Vergangenheit lässt sich für das festgelegte Modell auf eine absolut summierbare History-Forcierung zurückführen.</b> Die aktive Entwicklung selbst passt vollständig in Ω<sub>21/4</sub>. Daraus folgt im Poisson-Modell fast sicher eine endliche Antwort des kompakten Detektors.')]
    s += [table([['Ergebnis','Bedeutung'],['Aktive Hülle: H = 5,25','Ab dieser scharfen Grenze sind alle relevanten aktiven Knoten erfasst. Die aktive Inverse ist endlich.'],['Hinter Ω₅ noch aktiv','Volumen 29π/1536; erwartete zusätzliche Punktzahl 29/512. Modellwahrscheinlichkeit für mindestens einen Punkt: 5,50664 %.'],['KG-History','Ein Fourierargument nahe dem Lichtkegel und eine Gaußmajorante im übrigen Gebiet beweisen absolute Summierbarkeit.'],['Numerischer Rest hinter Ω₅','Weiterhin NOT_CERTIFIED. Die Quellseminormen sind noch nicht numerisch eingeschlossen; der konkrete Transport bleibt zu kontrollieren.']])]
    s += [Spacer(1,12),p('<b>METHOD_HOLD und G1 HOLD bleiben bestehen.</b> Das Fehlerziel 0,001 ist unverändert. Keine neue Zufallswolke und keine neue statistische Freigaberegel wurden eingeführt.')]
    s += [p(f'{check["check_count"]} exakte oder intervallgestützte Kontrollen bestanden. Die folgenden Seiten enthalten den vollständigen analytischen Beweis. Die Rechenkontrollen ersetzen keine unabhängige wissenschaftliche Begutachtung.','small')]
    s += [PageBreak()]
    text=(HERE/'PROOF.md').read_text()
    for block in text.strip().split('\n\n'):
        if block.startswith('# '):
            s.append(p('Herleitung und Aussagegrenzen','h'))
        elif block.startswith('## '):
            if block.startswith('## 7.'):
                s.append(PageBreak())
            s.append(p(markup(block[3:]),'h'))
        elif block.startswith('    '):
            lines=[x[4:] if x.startswith('    ') else x for x in block.splitlines()]
            s.append(p('<br/>'.join(escape(x).replace(' ','&#160;') for x in lines),'code'))
        else:
            # Reference URLs are rendered separately so links remain valid.
            lines=block.splitlines();regular=[]
            for line in lines:
                if line.startswith('https://'):
                    if regular:s.append(p(markup(' '.join(regular))));regular=[]
                    s.append(p(markup(line),'small'))
                else:regular.append(line)
            if regular:s.append(p(markup(' '.join(regular))))
    doc=SimpleDocTemplate(str(OUT/'Aktive_Huelle_KG_History_v0_17.pdf'),pagesize=(595.276,841.89),leftMargin=43,rightMargin=43,topMargin=45,bottomMargin=56,title='CSPP v0.17 - Endliche aktive Hülle und Konvergenz der KG-History',author='Thomas Gfeller / Forschungsprojekt X6')
    doc.build(s,onFirstPage=footer,onLaterPages=footer)
    print(OUT/'Aktive_Huelle_KG_History_v0_17.pdf')
if __name__=='__main__':build()
