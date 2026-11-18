"""Rebuild the downloadable PDF from the shared text CV."""
from pathlib import Path
from xml.sax.saxutils import escape
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, KeepTogether
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.colors import HexColor
from reportlab.lib.enums import TA_LEFT
ROOT=Path(__file__).resolve().parents[1]
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
pdfmetrics.registerFont(TTFont('CVRegular','/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'))
pdfmetrics.registerFont(TTFont('CVBold','/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf'))
styles=getSampleStyleSheet()
styles['Title'].fontName='CVBold'
styles.add(ParagraphStyle(name='CVBody',fontName='CVRegular',fontSize=8.7,leading=11.5,spaceAfter=3))
styles.add(ParagraphStyle(name='CVTech',parent=styles['CVBody'],textColor=HexColor('#46576a')))
styles.add(ParagraphStyle(name='CVJob',parent=styles['CVBody'],fontName='CVBold',spaceBefore=7))
styles.add(ParagraphStyle(name='CVSection',fontName='CVBold',fontSize=11,leading=15,textColor=HexColor('#185781'),spaceBefore=14,spaceAfter=8,keepWithNext=True))
lines=(ROOT/'resume.txt').read_text().splitlines()
flow=[]; i=0
while i<len(lines):
 line=lines[i].strip()
 if not line: i+=1;continue
 style=styles['CVBody']
 if i==0: style=styles['Title']
 elif line.isupper(): style=styles['CVSection']
 elif line.startswith('Tech:'):style=styles['CVTech']
 elif line.count('|')>=2 and i>5:
  block=[Paragraph(escape(line),styles['CVJob'])];i+=1
  while i<len(lines) and lines[i].strip():
   block.append(Paragraph(escape(lines[i]),styles['CVTech'] if lines[i].startswith('Tech:') else styles['CVBody']));i+=1
  flow.append(KeepTogether(block));continue
 flow.append(Paragraph(escape(line),style));i+=1

def footer(c,d):
 c.setFillColor(HexColor('#185781'));c.rect(0,837,595,5,fill=1,stroke=0)
 c.setFont('CVRegular',8);c.drawString(45,25,'Vu Quang Thinh | CV');c.drawRightString(550,25,f'Page {d.page}')
SimpleDocTemplate(str(ROOT/'assets/Tony_CV.pdf'),pagesize=(595,842),rightMargin=45,leftMargin=45,topMargin=35,bottomMargin=45).build(flow,onFirstPage=footer,onLaterPages=footer)
