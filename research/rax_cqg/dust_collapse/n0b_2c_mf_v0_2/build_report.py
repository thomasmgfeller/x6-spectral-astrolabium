#!/usr/bin/env python3
"""Build the reader PDF from REPORT.md; full equations remain in technical MD."""
from pathlib import Path
import html
import os
from reportlab.lib import colors
from reportlab.lib.enums import TA_LEFT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import SimpleDocTemplate, Paragraph, PageBreak

ROOT = Path(__file__).resolve().parent
FONT_ROOT = Path(os.environ.get('N0B_FONT_DIR', '/usr/share/fonts/truetype/dejavu'))
for name, filename in [('N0B', 'DejaVuSans.ttf'), ('N0B-Bold', 'DejaVuSans-Bold.ttf')]:
    pdfmetrics.registerFont(TTFont(name, str(FONT_ROOT / filename)))
styles = {
    'h1': ParagraphStyle('h1', fontName='N0B-Bold', fontSize=22, leading=28, textColor=colors.HexColor('#123b50'), spaceAfter=18),
    'h2': ParagraphStyle('h2', fontName='N0B-Bold', fontSize=12, leading=16, spaceBefore=13, spaceAfter=7, keepWithNext=True),
    'p': ParagraphStyle('p', fontName='N0B', fontSize=10, leading=15, spaceAfter=10, alignment=TA_LEFT),
}

def footer(canvas, doc):
    canvas.saveState()
    canvas.setStrokeColor(colors.HexColor('#b9c8cf'))
    canvas.line(48, 43, A4[0]-48, 43)
    canvas.setFont('N0B', 8)
    canvas.setFillColor(colors.HexColor('#42606e'))
    canvas.drawString(48, 30, 'X6 · N0B-2C-MF v0.2 · Lesefassung · 11.11.2026')
    canvas.drawRightString(A4[0]-48, 30, str(doc.page))
    canvas.restoreState()

def main():
    story = []
    for block in (ROOT/'REPORT.md').read_text(encoding='utf-8').strip().split('\n\n'):
        if block.startswith('# '):
            if story:
                story.append(PageBreak())
            story.append(Paragraph(html.escape(block[2:]), styles['h1']))
        elif block.startswith('## '):
            story.append(Paragraph(html.escape(block[3:]), styles['h2']))
        else:
            story.append(Paragraph(html.escape(block.replace('\n', ' ')), styles['p']))
    doc = SimpleDocTemplate(str(ROOT/'N0B_2C_MF_v0_2_Bericht.pdf'), pagesize=A4,
                            rightMargin=48, leftMargin=48, topMargin=45, bottomMargin=58,
                            title='N0B-2C-MF v0.2: Referenzmodell und offene CST-Brücken',
                            author='Thomas Gfeller / X6', invariant=True)
    doc.build(story, onFirstPage=footer, onLaterPages=footer)
    print('Built N0B_2C_MF_v0_2_Bericht.pdf from REPORT.md')

if __name__ == '__main__':
    main()
