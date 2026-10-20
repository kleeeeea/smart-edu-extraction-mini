"""Build traceable records from visually selected PDF regions; no OCR auto-approval."""
from pathlib import Path
import csv, json, re, hashlib
import fitz
ROOT=Path(__file__).resolve().parents[1]
PDF=Path(json.loads((ROOT/'source_report.json').read_text())['source_pdf'])
DOC=fitz.open(PDF)
SHA256=hashlib.sha256(PDF.read_bytes()).hexdigest()
SKIP={'演  示','实  验','想想议议','想想做做','小资料','拓展实验','科学世界','科学技术社会环境','问  题','练习与应用','复习与提高'}

def region(page,y0,y1):
    lines=[]; small=[]
    for b in DOC[page-1].get_text('dict')['blocks']:
        if b['type']: continue
        for l in b['lines']:
            ss=l['spans']; top=l['bbox'][1]
            if not (y0-1<=top<y1) or max(s['size'] for s in ss)<9.5: continue
            if any(s['font']=='SimSun' and s['size']>17 for s in ss):continue
            t=''
            for s in ss:
                v=s['text']
                if s['size']<8 and v.strip():
                    # PDF superscripts and subscripts are preserved as explicit Markdown/LaTeX.
                    if re.fullmatch(r'[−\-0-9]+',v.strip()):
                        bases=[z['origin'][1] for z in ss if z['size']>=9]
                        is_sub=bool(bases) and s['origin'][1]>min(bases)+1
                        v=('_' if is_sub else '^')+'{'+v.strip()+'}'
                t+=v
            t=t.strip()
            if not t or t in SKIP:continue
            if re.search(r'[\u0e00-\u1fff\u2c00-\u2dff\u3100-\u312f\u3300-\u33ff]',t):continue
            if any(('FZLTZHJW' in z['font'] and z['size']>13) or ('FZLTHJW' in z['font'] and z['size']>=11.5) for z in ss):t='**'+t+'**\n\n'
            (small if max(s['size'] for s in ss)<11.5 else lines).append((round(top,1),l['bbox'][0],t))
    lines.sort(key=lambda a:(round(a[0]/3)*3,a[1]))
    small.sort(key=lambda a:(round(a[0]/3)*3,a[1]))
    lines+=small
    out='';prev=None
    for y,x,t in lines:
        gap=prev and y-prev[0]
        sep='\n\n' if prev and (gap>28 or gap<0 or (x-prev[1]>16 and gap>15)) else ''
        if out and not sep and re.search(r'[a-zA-Z0-9]$',out) and re.match('[a-zA-Z0-9]',t):sep=' '
        out+=sep+t
        prev=(y,x,t)
    return out

chapters={7:'力',8:'运动和力',9:'压强',10:'浮力',11:'功和机械能',12:'简单机械'}
sections={7:['力','弹力','重力'],8:['牛顿第一定律','二力平衡','摩擦力','同一直线上二力的合成'],9:['压强','液体的压强','大气压强','跨学科实践：制作简易活塞式抽水机','流体压强与流速的关系'],10:['浮力','阿基米德原理','物体的浮沉条件及应用','跨学科实践：制作微型密度计'],11:['功','功率','动能和势能','机械能及其转化'],12:['杠杆','跨学科实践：制作简易杆秤','滑轮','机械效率']}
def page_label(values):
    values=sorted(set(values)); ranges=[]
    for v in values:
        if ranges and v==ranges[-1][-1]+1:ranges[-1].append(v)
        else:ranges.append([v])
    return ';'.join(f'P{g[0]}' if len(g)==1 else f'P{g[0]}-P{g[-1]}' for g in ranges)

rows=[];sources=[];candidates=[]
patches=json.loads((ROOT/'patches.json').read_text()) if (ROOT/'patches.json').exists() else {}
for n,line in enumerate((ROOT/'selection.tsv').read_text().splitlines(),1):
    c,s,name,spec=line.split('\t'); c=int(c);s=int(s)
    regions=[list(map(int,q.split(':'))) for q in spec.split(';')]
    parts=[region(*a) for a in regions]
    body=''
    for part in parts:
        body+=('\n\n' if not body or body.rstrip()[-1:] in '。！？：；.!?}' else '')+part
    body=body.strip()
    candidates.append({'knowledge_point':name,'detail':body})
    patch=patches.get(name,{})
    for old,new in patch.get('replace',[]):body=body.replace(old,new)
    if 'detail' in patch:body=patch['detail']
    # Normalize text-layer indices outside math; preserve explicit LaTeX formulas.
    def normalize_text(t):
        t=re.sub(r'\^\{(-)\}\^\{(\d+)\}',r'^{\1\2}',t)
        t=re.sub(r'_\{(\d+)\}',lambda m:m.group(1).translate(str.maketrans('0123456789','₀₁₂₃₄₅₆₇₈₉')),t)
        return re.sub(r'\^\{(-?\d+)\}',lambda m:m.group(1).translate(str.maketrans('-0123456789','⁻⁰¹²³⁴⁵⁶⁷⁸⁹')),t)
    body=''.join(v if i%2 else normalize_text(v) for i,v in enumerate(re.split(r'(\$[^$]+\$)',body)))
    if patch.get('example_regions'):
        er=patch['example_regions'];patch['example']='\n\n'.join(region(*a) for a in er)+'\n\n'+'\n\n'.join(f'![page-{p:03}](images/physics-pep-8b/page-{p:03}.png)' for p in dict.fromkeys(a[0] for a in er))
    pages=list(dict.fromkeys(a[0] for a in regions))
    # Merge cross-page sentence fragments before appending all relevant page images.
    body=re.sub(r'(?<=[0-9a-zA-Z])\s+(?=[⁻⁰¹²³⁴⁵⁶⁷⁸⁹])','',body)
    body=re.sub(r'(\*\*[^*]+\*\*)\s+\1',r'\1',body)
    body=re.sub(r'\n{3,}','\n\n',body)
    body=re.sub(r'(?<=[，、])\n\n(?=[^\n])','',body)
    pages=list(dict.fromkeys(pages+[a[0] for a in patch.get('example_regions',[])]))
    images='\n\n'.join(f'![page-{p:03}](images/physics-pep-8b/page-{p:03}.png)' for p in pages)
    detail=body.strip()+'\n\n'+images
    all_pages=list(dict.fromkeys(pages+patch.get('example_pages',[])))
    kp=f'RJ-PHYSICS-8B-{n:03}'
    sec=f'第{s}节 {sections[c][s-1]}'
    row=dict(zip(['knowledge_point_id','chapter','subchapter','section','knowledge_point','detail','example','pdf_page'],[kp,f'第{dict(zip(range(7,13),["七","八","九","十","十一","十二"]))[c]}章 {chapters[c]}',sec,sec,name,detail,patch.get('example',''),page_label(all_pages)]))
    rows.append(row)
    sources.append({'knowledge_point_id':kp,'knowledge_point':name,'regions':[{'pdf_page':p,'printed_page':p-5,'bbox':[0,y0,DOC[p-1].rect.width,y1]} for p,y0,y1 in regions],'example_pages':patch.get('example_pages',[]),'content_basis':'local_pdf','transcription':'PDF text candidates with region selection and visual corrections','source_pdf_sha256':SHA256})
with (ROOT/'knowledge_points.csv').open('w',encoding='utf-8-sig',newline='') as f:
    w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
(ROOT/'transcription_candidates.jsonl').write_text(''.join(json.dumps(q,ensure_ascii=False)+'\n' for q in candidates))
(ROOT/'source_records.jsonl').write_text(''.join(json.dumps(s,ensure_ascii=False)+'\n' for s in sources))
md=['# 人教版物理八年级下册（根据2022年版课程标准修订）\n']
for r in rows:
    md.append(f"## {r['knowledge_point_id']} {r['knowledge_point']}\n\n{r['chapter']} / {r['subchapter']} · PDF {r['pdf_page']}\n\n{r['detail']}\n")
    if r['example']:md.append('### 补充原例与原解\n\n'+r['example']+'\n')
(ROOT/'knowledge_points.md').write_text('\n'.join(md))
print('records',len(rows))
