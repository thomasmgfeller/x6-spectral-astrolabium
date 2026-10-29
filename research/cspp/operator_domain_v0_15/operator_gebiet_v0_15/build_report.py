"""Readable PDF from the complete scientific record; data remain in JSON."""
import re, html
from pathlib import Path
from reportlab.platypus import SimpleDocTemplate,Paragraph,Spacer,Table,TableStyle,Preformatted,KeepTogether
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet,ParagraphStyle
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.enums import TA_LEFT
HERE=Path(__file__).resolve().parent
for name,path in [('DejaVu','/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'),('DejaVuBold','/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf'),('DejaVuMono','/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf')]:
    pdfmetrics.registerFont(TTFont(name,path))
pdfmetrics.registerFontFamily('DejaVu',normal='DejaVu',bold='DejaVuBold')
styles=getSampleStyleSheet()
styles.add(ParagraphStyle(name='Body',fontName='DejaVu',fontSize=9.4,leading=13.5,spaceAfter=7,splitLongWords=True))
styles.add(ParagraphStyle(name='Title2',fontName='DejaVuBold',fontSize=20,leading=25,spaceAfter=12,textColor=colors.HexColor('#103c55')))
styles.add(ParagraphStyle(name='Section',fontName='DejaVuBold',fontSize=12.3,leading=17,spaceBefore=14,spaceAfter=8,keepWithNext=True,textColor=colors.HexColor('#103c55')))
styles.add(ParagraphStyle(name='Cell',fontName='DejaVu',fontSize=8,leading=11,spaceAfter=0))
styles.add(ParagraphStyle(name='Formula',fontName='DejaVuMono',fontSize=8.1,leading=11.7,leftIndent=9,spaceBefore=3,spaceAfter=8,splitLongWords=True))

def rich(x):
    x=html.escape(x)
    x=re.sub(r'\*\*(.*?)\*\*',r'<b>\1</b>',x)
    x=re.sub(r'`([^`]+)`',r'<font name="DejaVuMono">\1</font>',x)
    return x
lines=(HERE/'README.md').read_text().splitlines();story=[];i=0
while i<len(lines):
    line=lines[i]
    if not line.strip():i+=1;continue
    if line.startswith('# '):story.append(Paragraph(rich(line[2:]),styles['Title2']));i+=1;continue
    if line.startswith('## '):story.append(Paragraph(rich(line[3:]),styles['Section']));i+=1;continue
    if line.startswith('|'):
        rows=[]
        while i<len(lines) and lines[i].startswith('|'):
            l=lines[i]
            if not re.match(r'^\|[- :|]+\|$',l):rows.append([Paragraph(rich(c.strip()),styles['Cell']) for c in l.strip('|').split('|')])
            i+=1
        table=Table(rows,colWidths=[475/len(rows[0])]*len(rows[0]),repeatRows=1,hAlign='LEFT')
        table.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,0),colors.HexColor('#e0eef4')),('VALIGN',(0,0),(-1,-1),'TOP'),('LINEBELOW',(0,0),(-1,0),.7,colors.HexColor('#43859e')),('LINEBELOW',(0,1),(-1,-1),.25,colors.HexColor('#d3dce0')),('TOPPADDING',(0,0),(-1,-1),6),('BOTTOMPADDING',(0,0),(-1,-1),6)]))
        story.extend([table,Spacer(1,8)]);continue
    if line.startswith('```'):
        block=[];i+=1
        while i<len(lines) and not lines[i].startswith('```'):block.append(lines[i]);i+=1
        story.append(Preformatted('\n'.join(block),styles['Formula'],maxLineLength=94));i+=1;continue
    if line.startswith('    '):
        block=[]
        while i<len(lines) and lines[i].startswith('    '):block.append(lines[i][4:]);i+=1
        story.append(Paragraph('<br/>'.join(rich(x) for x in block),styles['Formula']));continue
    block=[line];i+=1
    while i<len(lines) and lines[i].strip() and not lines[i].startswith(('#','|','```','    ')):
        if re.match(r'^(- |[1-9]\. )',lines[i]):break
        block.append(lines[i]);i+=1
    story.append(Paragraph(rich(' '.join(block)),styles['Body']))

def page(canvas,doc):
    canvas.setStrokeColor(colors.HexColor('#c1d6df'));canvas.line(60,797,535,797)
    canvas.setFont('DejaVu',8);canvas.setFillColor(colors.HexColor('#406175'))
    canvas.drawString(60,808,'CSPP  |  Operator, Gebiet und Randbehandlung')
    canvas.drawRightString(535,808,'v0.15  |  29.10.2026')
    canvas.drawString(60,32,'Entwicklungsdiagnose  |  METHOD_HOLD und G1 HOLD bleiben bestehen')
    canvas.drawRightString(535,32,str(doc.page))
out=HERE.parent/'Operator_Gebietsfehler_v0_15.pdf'
doc=SimpleDocTemplate(str(out),pagesize=(595.28,841.89),rightMargin=60,leftMargin=60,topMargin=57,bottomMargin=55,title='Operator- und Gebietsfehler v0.15',author='Thomas Gfeller - Forschungsprojekt X6 / CSPP')
doc.build(story,onFirstPage=page,onLaterPages=page)
print(out)
