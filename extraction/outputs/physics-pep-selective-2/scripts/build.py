"""Rebuild only this book from visually selected source regions and explicit corrections."""
from pathlib import Path
import csv,json,re,hashlib
import fitz
ROOT=Path(__file__).resolve().parents[1]
INFO=json.loads((ROOT/'source_report.json').read_text())
DOC=fitz.open(INFO['source_pdf'])
CH=['安培力与洛伦兹力','电磁感应','交变电流','电磁振荡与电磁波','传感器','课题研究']
SE=[['磁场对通电导线的作用力','磁场对运动电荷的作用力','带电粒子在匀强磁场中的运动','质谱仪与回旋加速器'],['楞次定律','法拉第电磁感应定律','涡流、电磁阻尼和电磁驱动','互感和自感'],['交变电流','交变电流的描述','变压器','电能的输送'],['电磁振荡','电磁场与电磁波','无线电波的发射和接收','电磁波谱'],['认识传感器','常见传感器的工作原理及应用','利用传感器制作简单的自动控制装置'],['课题研究']]
FIELDS=['knowledge_point_id','chapter','subchapter','section','knowledge_point','detail','example','pdf_page']
def region(p,y0,y1):
    lines=[]
    for b in DOC[p-1].get_text('dict')['blocks']:
        if b['type']:continue
        for l in b['lines']:
            spans=l['spans']; y=l['bbox'][1]
            size=max(s['size'] for s in spans)
            if not y0-1.5<=y<y1 or size<10 or size>13:continue
            if any('FZZDX' in s['font'] for s in spans):continue
            txt=''
            for s in spans:
                t=s['text']
                if s['size']<9 and t.strip():
                    base=[z['origin'][1] for z in spans if z['size']>=10]
                    if base:t=('_' if s['origin'][1]>min(base)+1 else '^')+'{'+t.strip()+'}'
                txt+=t
            txt=txt.strip()
            if not txt or txt in ['演    示','实    验','思考与讨论','做一做','拓展学习','科学漫步','练习与应用']:continue
            if re.search(r'[\u0e00-\u1fff\u2c00-\u2dff\u3100-\u312f\u3300-\u33ff]',txt):continue
            lines.append((y,l['bbox'][0],txt))
    lines.sort(key=lambda z:(round(z[0]/3)*3,z[1]))
    out='';prev=None
    for y,x,t in lines:
        sep=''
        if prev and (y-prev[0]>28 or (x-prev[1]>16 and y-prev[0]>15)):sep='\n\n'
        if out and not sep and re.search('[A-Za-z0-9]$',out) and re.match('[A-Za-z0-9]',t):sep=' '
        out+=sep+t;prev=(y,x,t)
    return out

def label(ps):
    groups=[]
    for p in sorted(set(ps)):
        if groups and p==groups[-1][-1]+1:groups[-1].append(p)
        else:groups.append([p])
    return ';'.join('P%d'%g[0] if len(g)==1 else 'P%d-P%d'%(g[0],g[-1]) for g in groups)
def imgs(ps):return '\n\n'.join(f'![page-{p:03}](images/physics-pep-selective-2/page-{p:03}.png)' for p in dict.fromkeys(ps))
patches=json.loads((ROOT/'patches.json').read_text()) if (ROOT/'patches.json').exists() else {}
rows=[];sources=[];candidates=[]
for n,line in enumerate((ROOT/'selection.tsv').read_text().splitlines(),1):
    c,s,name,spec=line.split('\t');c=int(c);s=int(s)
    regions=[list(map(int,q.split(':'))) for q in spec.split(';')]
    parts=[region(*a) for a in regions];body=''
    for part in parts:body+=('\n\n' if body and body[-1:] in '。！？：；' else '')+part
    candidates.append({'knowledge_point':name,'detail':body})
    patch=patches.get(name,{})
    if 'detail' in patch:body=patch['detail']
    for a,b in patch.get('replace',[]):body=body.replace(a,b)
    er=patch.get('example_regions',[])
    ex=patch.get('example','')
    dp=list(dict.fromkeys(a[0] for a in regions));ep=patch.get('example_pages',[a[0] for a in er])
    if er and not ex:ex='\n\n'.join(region(*a) for a in er)
    # Full cross-page prose is assembled before any page reference is appended.
    body=re.sub(r'(?<=[，、])\n\n','',body)
    body=re.sub(r'\n{3,}','\n\n',body)
    sec=SE[c-1][s-1]
    row=dict(zip(FIELDS,[f'RJ-PHYSICS-SEL2-{n:03}',('第'+['一','二','三','四','五'][c-1]+'章 ' if c<6 else '')+CH[c-1],f'{s} {sec}' if c<6 else sec,f'{s} {sec}' if c<6 else sec,name,body.strip()+'\n\n'+imgs(dp),ex.strip()+('\n\n'+imgs(ep) if ex else ''),label(dp+ep)]))
    rows.append(row)
    sources.append({'knowledge_point_id':row['knowledge_point_id'],'knowledge_point':name,'regions':[{'pdf_page':p,'printed_page':p-5,'bbox':[0,y0,595.276,y1]} for p,y0,y1 in regions],'example_regions':er,'example_pages':ep,'source_pdf_sha256':INFO['sha256'],'visual_review_basis':'review/pages-NNN-NNN.jpg and original full-page images','correction':name in patches})
with (ROOT/'knowledge_points.csv').open('w',encoding='utf-8-sig',newline='') as f:
    w=csv.DictWriter(f,fieldnames=FIELDS);w.writeheader();w.writerows(rows)
for path,data in [('source_records.jsonl',sources),('transcription_candidates.jsonl',candidates)]:
    (ROOT/path).write_text(''.join(json.dumps(x,ensure_ascii=False)+'\n' for x in data))
md=['# 普通高中教科书·物理 选择性必修 第二册（人教版）\n']
for r in rows:
    md.append(f"## {r['knowledge_point_id']} {r['knowledge_point']}\n\n{r['chapter']} / {r['section']} · PDF {r['pdf_page']}\n\n{r['detail']}\n")
    if r['example']:md.append('### 补充原例与原解\n\n'+r['example']+'\n')
(ROOT/'knowledge_points.md').write_text('\n'.join(md))
print('records',len(rows))
