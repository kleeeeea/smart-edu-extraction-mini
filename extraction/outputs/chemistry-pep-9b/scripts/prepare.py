from pathlib import Path
import fitz,json,hashlib,requests
from PIL import Image,ImageDraw
R=Path(__file__).resolve().parents[1];P=next((R.parents[1]/'inputs/初中化学教材').glob('02_*.pdf'))
for q in ['images/chemistry-pep-9b','review','website']:(R/q).mkdir(parents=True,exist_ok=True)
d=fitz.open(P)
(R/'source_report.json').write_text(json.dumps({'source_pdf':str(P),'sha256':hashlib.sha256(P.read_bytes()).hexdigest(),'pdf_pages':len(d),'file_bytes':P.stat().st_size,'subject':'化学','grade':9,'volume':'下册','publisher':'人民教育出版社','resource_id':'1998204c-f017-4f49-9000-0ba0b93d2a4d','curriculum_revision':'根据2022年版课程标准修订'},ensure_ascii=False,indent=2))
lines=[];positions=[]
for i,p in enumerate(d,1):
 p.get_pixmap(matrix=fitz.Matrix(1.7,1.7)).save(R/f'images/chemistry-pep-9b/page-{i:03}.png')
 lines.append(json.dumps({'pdf_page':i,'text':p.get_text()},ensure_ascii=False))
 positions.append(f'\nPAGE {i}')
 for b in p.get_text('dict')['blocks']:
  if b['type']:continue
  for l in b['lines']:
   if max(s['size'] for s in l['spans'])>=9.5 and l['bbox'][1]<665:
    positions.append(f"{l['bbox'][0]:.0f},{l['bbox'][1]:.0f}: "+''.join(s['text'] for s in l['spans']))
(R/'pages.jsonl').write_text('\n'.join(lines));(R/'positioned_text.txt').write_text('\n'.join(positions))
for i in range(1,len(d)+1,2):
 canvas=Image.new('RGB',(1640,1190),'white');dr=ImageDraw.Draw(canvas)
 for j in range(i,min(i+2,len(d)+1)):
  im=Image.open(R/f'images/chemistry-pep-9b/page-{j:03}.png');im.thumbnail((810,1150))
  x=5+(j-i)*820;canvas.paste(im,(x,30));dr.text((x+5,5),f'PDF P{j}',fill='black')
 canvas.save(R/f'review/pages-{i:03}-{min(i+1,len(d)):03}.jpg',quality=92)
u='https://s-file-1.ykt.cbern.com.cn/zxx/ndrv2/resources/tch_material/details/1998204c-f017-4f49-9000-0ba0b93d2a4d.json'
v=requests.get(u,timeout=30);v.raise_for_status();v=v.json();(R/'website/resource-v2.json').write_text(json.dumps(v,ensure_ascii=False,indent=2))
for item in v['ti_items']:
 if item.get('ti_file_flag')=='ebook_mapping':
  z=requests.get(item['ti_storages'][0],timeout=30);z.raise_for_status();(R/'website/ebook_mapping.json').write_text(z.text);break
print('pages',len(d),'title',v['title'])
