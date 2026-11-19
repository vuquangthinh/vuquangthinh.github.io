"""Build a linked, text-selectable CV from the shared text source."""
from pathlib import Path
from xml.sax.saxutils import escape
import re
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, KeepTogether
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.colors import HexColor
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
ROOT=Path(__file__).resolve().parents[1]
pdfmetrics.registerFont(TTFont('CVRegular','/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'))
pdfmetrics.registerFont(TTFont('CVBold','/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf'))
styles=getSampleStyleSheet()
styles['Title'].fontName='CVBold';styles['Title'].fontSize=22;styles['Title'].leading=27
styles.add(ParagraphStyle(name='CVBody',fontName='CVRegular',fontSize=10,leading=12,spaceAfter=3))
styles.add(ParagraphStyle(name='CVTech',parent=styles['CVBody'],fontSize=9.2,leading=12,textColor=HexColor('#46576a')))
styles.add(ParagraphStyle(name='CVJob',parent=styles['CVBody'],fontName='CVBold',spaceBefore=7,spaceAfter=4))
styles.add(ParagraphStyle(name='CVSection',fontName='CVBold',fontSize=11.5,leading=15,textColor=HexColor('#185781'),spaceBefore=12,spaceAfter=7,keepWithNext=True))
styles.add(ParagraphStyle(name='CVContact',parent=styles['CVTech'],alignment=1))
def markup(s):
 s=escape(s)
 s=re.sub(r'https://[^\s|]+',lambda m:'<link href="'+m.group()+'" color="#185781">'+m.group()+'</link>',s)
 s=s.replace('quangthinh.dev@gmail.com','<link href="mailto:quangthinh.dev@gmail.com" color="#185781">quangthinh.dev@gmail.com</link>')
 return s
lines=(ROOT/'resume.txt').read_text().splitlines();flow=[];i=0
while i<len(lines):
 line=lines[i].strip()
 if not line:i+=1;continue
 if line=='Responsibilities:':i+=1;continue
 style=styles['CVBody']
 if i==0:style=styles['Title']
 elif i<4:style=styles['CVContact']
 elif line.isupper():style=styles['CVSection']
 elif line.startswith('Tech:'):style=styles['CVTech']
 elif line.count('|')>=2 and i>5:
  block=[Paragraph(markup(line),styles['CVJob'])];i+=1
  while i<len(lines) and lines[i].strip():
   if lines[i]!='Responsibilities:':block.append(Paragraph(markup(lines[i]),styles['CVTech'] if lines[i].startswith('Tech:') else styles['CVBody']))
   i+=1
  if flow and isinstance(flow[-1], Paragraph) and flow[-1].style.name=='CVSection':
   block.insert(0,flow.pop())
  flow.append(KeepTogether(block));continue
 flow.append(Paragraph(markup(line),style));i+=1

def footer(c,d):
 c.setTitle('Vu Quang Thinh (Tony Vu) — Curriculum Vitae');c.setAuthor('Vu Quang Thinh');c.setSubject('Full-stack and product engineering experience')
 c.setFillColor(HexColor('#185781'));c.rect(0,837,595,5,fill=1,stroke=0)
 c.setFont('CVRegular',8);c.drawString(42,25,'Vu Quang Thinh | CV');c.drawRightString(553,25,f'Page {d.page}')
SimpleDocTemplate(str(ROOT/'assets/Tony_CV.pdf'),pagesize=(595,842),rightMargin=42,leftMargin=42,topMargin=30,bottomMargin=38).build(flow,onFirstPage=footer,onLaterPages=footer)
