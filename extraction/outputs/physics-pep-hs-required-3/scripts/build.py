"""Render explicitly reviewed textbook selections; the PDF text layer is only a candidate."""
from pathlib import Path
import csv,json,re,hashlib
import fitz
R=Path(__file__).resolve().parents[1]
META=json.loads((R/'source_report.json').read_text());PDF=Path(META['source_pdf']);DOC=fitz.open(PDF)
BOOK='physics-pep-hs-required-3'
CH={9:'第九章 静电场及其应用',10:'第十章 静电场中的能量',11:'第十一章 电路及其应用',12:'第十二章 电能 能量守恒定律',13:'第十三章 电磁感应与电磁波初步',14:'课题研究'}
SE={9:['电荷','库仑定律','电场 电场强度','静电的防止与利用'],10:['电势能和电势','电势差','电势差与电场强度的关系','电容器的电容','带电粒子在电场中的运动'],11:['电源和电流','导体的电阻','实验：导体电阻率的测量','串联电路和并联电路','实验：练习使用多用电表'],12:['电路中的能量转化','闭合电路的欧姆定律','实验：电池电动势和内阻的测量','能源与可持续发展'],13:['磁场 磁感线','磁感应强度 磁通量','电磁感应现象及应用','电磁波的发现及应用','能量量子化'],14:[]}

SKIP={'问题','？','演    示','实    验','做一做','练习与应用','复习与提高','科学漫步','STSE','拓展学习','思考与讨论','科学方法','参考案例','参考案例1','参考案例2'}
def region(p,y0,y1):
 main=[];small=[]
 for b in DOC[p-1].get_text('dict')['blocks']:
  if b['type']:continue
  for l in b['lines']:
   ss=l['spans'];y=l['bbox'][1];x=l['bbox'][0]
   if not y0-1<=y<min(y1,777) or max(z['size'] for z in ss)<9.5:continue
   if any(z['font']=='SimSun' and z['size']>17 for z in ss):continue
   t=''
   for z in ss:
    a=z['text'];bases=[s['origin'][1] for s in ss if s['size']>=9]
    if z['size']<8 and re.fullmatch('[−\\-0-9xy]+',a.strip() or ' '):
     a=('_' if bases and z['origin'][1]>min(bases)+1 else '^')+'{'+a.strip()+'}'
    t+=a
   t=t.strip()
   if not t or t in SKIP or re.search('[\u0e00-\u1fff\u2c00-\u2dff\u3100-\u312f\u3300-\u33ff]',t):continue
   # A heading uses FZLT and contains predominantly bold sans-serif glyphs; mixed blue key terms are body text.
   if ss and all('FZLT' in z['font'] for z in ss) and max(z['size'] for z in ss)>=12:t='**'+t+'**\n\n'
   (main if max(z['size'] for z in ss)>=11.5 else small).append((y,x,t))
 main.sort(key=lambda a:(round(a[0]/2)*2,a[1]));small.sort(key=lambda a:(round(a[0]/2)*2,a[1]))
 out='';prev=None
 for y,x,t in main+small:
  sep='\n\n' if prev and (y-prev[0]>28 or y<prev[0] or (x-prev[1]>16 and y-prev[0]>15)) else ''
  if out and not sep and re.search('[A-Za-z0-9]$',out) and re.match('[A-Za-z0-9]',t):sep=' '
  out+=sep+t;prev=(y,x,t)
 return out

def clean(s):
 s=re.sub(r'\^\{(-)\}\^\{(\d+)\}',r'^{\1\2}',s)
 s=re.sub(r'_\{([0-9]+)\}',lambda m:m[1].translate(str.maketrans('0123456789','₀₁₂₃₄₅₆₇₈₉')),s)
 s=re.sub(r'\^\{(-?\d+)\}',lambda m:m[1].translate(str.maketrans('-0123456789','⁻⁰¹²³⁴⁵⁶⁷⁸⁹')),s)
 s=re.sub(r'(?<=10)\s+(?=[⁻⁰¹²³⁴⁵⁶⁷⁸⁹])','',s)
 return re.sub(r'\n{3,}','\n\n',s).strip()

def join(parts):
 out=''
 for part in parts:
  if out:out+='\n\n' if out.rstrip()[-1:] in '。！？：；.!?}|*' else ''
  out+=part
 return clean(out)

def imgs(pages):return '\n\n'.join(f'![page-{p:03}](images/{BOOK}/page-{p:03}.png)' for p in dict.fromkeys(pages))
def label(pages):
 gs=[]
 for p in sorted(set(pages)):
  if gs and p==gs[-1][-1]+1:gs[-1].append(p)
  else:gs.append([p])
 return ';'.join(f'P{g[0]}' if len(g)==1 else f'P{g[0]}-P{g[-1]}' for g in gs)
P=json.loads((R/'patches.json').read_text()) if (R/'patches.json').exists() else {}
rows=[];sources=[];candidates=[]
for i,line in enumerate((R/'selection.tsv').read_text().splitlines(),1):
 c,s,n,rs=line.split('\t');c=int(c);s=int(s);regions=[list(map(int,x.split(':'))) for x in rs.split(';')]
 raw=join([region(*x) for x in regions]);q=P.get(n,{});text=q.get('detail',raw)
 for a,b in q.get('replace',[]):text=text.replace(a,b)
 pages=list(dict.fromkeys(a[0] for a in regions));ep=q.get('example_pages',[]);ex=q.get('example','')
 if ex:ex=clean(ex)+'\n\n'+imgs(ep)
 chapter=CH[c];sec=(f'{s}. '+SE[c][s-1]) if s else chapter
 kp=f'RJ-PHYSICS-HS-R3-{i:03}'
 row=dict(zip(['knowledge_point_id','chapter','subchapter','section','knowledge_point','detail','example','pdf_page'],[kp,chapter,sec,sec,n,clean(text)+'\n\n'+imgs(pages),ex,label(pages+ep)]))
 rows.append(row);candidates.append({'knowledge_point':n,'candidate_detail':raw})
 sources.append({'knowledge_point_id':kp,'knowledge_point':n,'chapter':chapter,'subchapter':sec,'source_sha256':META['sha256'],'regions':[{'pdf_page':p,'printed_page':p-5,'bbox':[0,y0,DOC[p-1].rect.width,y1]} for p,y0,y1 in regions],'example_pages':ep,'reviewed_text':clean(text),'example_text':q.get('example',''),'scope':'chapter_introduction' if s==0 else 'section','policy':'user physics extraction instructions'})
with (R/'knowledge_points.csv').open('w',encoding='utf-8-sig',newline='') as f:
 w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
(R/'knowledge_points.md').write_text('# 人教版高中物理必修第三册\n\n'+'\n'.join(f"## {r['knowledge_point_id']} {r['knowledge_point']}\n\n{r['chapter']} / {r['subchapter']} · PDF {r['pdf_page']}\n\n{r['detail']}\n"+ ('\n### 补充原例与原解\n\n'+r['example']+'\n' if r['example'] else '') for r in rows))
for file,rr in [('source_records.jsonl',sources),('transcription_candidates.jsonl',candidates)]:
 (R/file).write_text(''.join(json.dumps(x,ensure_ascii=False)+'\n' for x in rr))
print('records',len(rows))
