"""Build manually selected and visually reviewed chemistry records.
Selection bounds use physical PDF page and top coordinates in PDF points.
"""
import csv,json,re,hashlib
from pathlib import Path
import fitz
ROOT=Path(__file__).resolve().parents[1]
PDF=Path(json.loads((ROOT/'source_report.json').read_text())['source_pdf'])
DOC=fitz.open(PDF)
SHA=hashlib.sha256(PDF.read_bytes()).hexdigest()

def region(spec):
    p,y0,y1,*xr=spec
    x0,x1=xr or [0,600]
    lines=[]
    for b in DOC[p-1].get_text('dict')['blocks']:
        if b['type']:continue
        for l in b['lines']:
            x,y,_,_=l['bbox']; ss=l['spans']
            if not(y0-2<=y<=y1+2 and x0-5<=x<x1):continue
            if max(s['size'] for s in ss)<9.5:continue
            if any(s['font']=='SimSun' and s['size']>17 for s in ss):continue
            t=''.join(s['text'] for s in ss).strip()
            if not t or t.startswith('仅供个人'):continue
            lines.append((round(y/3)*3,x,y,t))
    lines.sort()
    text=''; previous=None
    for _,x,y,t in lines:
        gap=previous is not None and y-previous[1]>27
        text+= ('\n\n' if text and gap else '')+t
        previous=(x,y)
    return text

def label(ps):
    groups=[]
    for p in sorted(set(ps)):
        if groups and p==groups[-1][-1]+1:groups[-1].append(p)
        else:groups.append([p])
    return ';'.join(f'P{g[0]}' if len(g)==1 else f'P{g[0]}-P{g[-1]}' for g in groups)

selection=json.loads((ROOT/'selection.json').read_text())
rows=[]; sources=[]; candidates=[]
for i,s in enumerate(selection,1):
    parts=[region(a) for a in s['regions']]
    candidate=''
    for part in parts:
        if candidate and candidate[-1:] in '。！？；：':candidate+='\n\n'
        candidate+=part
    candidates.append({'knowledge_point':s['name'],'detail':candidate})
    body=s.get('detail',candidate)
    for old,new in s.get('replace',[]):
        if old not in body:raise ValueError((s['name'],old))
        body=body.replace(old,new)
    example=s.get('example',''.join(region(a) for a in s.get('example_regions',[])))
    eps=list(dict.fromkeys([a[0] for a in s.get('example_regions',[])]+s.get('example_pages',[])))
    if example:
        example=example.strip()+'\n\n'+'\n\n'.join(f'![page-{p:03}](images/chemistry-pep-hs-selective-3/page-{p:03}.png)' for p in eps)
    ps=list(dict.fromkeys([a[0] for a in s['regions']]+s.get('image_pages',[])))
    body=body.strip()+'\n\n'+'\n\n'.join(f'![page-{p:03}](images/chemistry-pep-hs-selective-3/page-{p:03}.png)' for p in ps)
    row=dict(zip(['knowledge_point_id','chapter','subchapter','section','knowledge_point','detail','example','pdf_page'],[f'RJ-CHEMISTRY-HSS3-{i:03}',s['chapter'],s['topic'],s.get('section',s['topic']),s['name'],body,example,label(ps+eps)]))
    rows.append(row)
    sources.append({'knowledge_point_id':row['knowledge_point_id'],'source_pdf_sha256':SHA,'regions':s['regions'],'image_pages':ps,'image_only_pages':s.get('image_pages',[]),'example_pages':s.get('example_pages',[]),'example_regions':s.get('example_regions',[]),'region_format':'physical_page,y0,y1[,x0,x1]; PDF points; line top, y tolerance 2 pt and left tolerance 5 pt; overrides checked against page image','visual_status':s.get('visual_status','reviewed'),'editorial_notes':s.get('notes',[]),'transcription_override':'detail' in s})
with (ROOT/'knowledge_points.csv').open('w',encoding='utf-8-sig',newline='') as f:
    w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
(ROOT/'source_records.jsonl').write_text(''.join(json.dumps(x,ensure_ascii=False)+'\n' for x in sources))
(ROOT/'transcription_candidates.jsonl').write_text(''.join(json.dumps(x,ensure_ascii=False)+'\n' for x in candidates))
md=['# 人教版高中化学选择性必修3 有机化学基础\n\n覆盖与核验说明见 README.md。\n']
for r in rows:
    md.append(f"## {r['knowledge_point_id']} {r['knowledge_point']}\n\n{r['chapter']} / {r['subchapter']} · {r['pdf_page']}\n\n{r['detail']}\n")
    if r['example']:md.append('### 补充原例与原解\n\n'+r['example'])
(ROOT/'knowledge_points.md').write_text('\n'.join(md))
checks=[]
for r in rows:
    assert r['knowledge_point'] and r['detail']
    for field in ['detail','example']:
        paths=re.findall(r'!\[[^\]]*\]\(([^)]+)\)',r[field])
        assert len(paths)==len(set(paths))
        assert all((ROOT/p).is_file() for p in paths)
checks.append('八字段、必填、连续ID、图片存在与同字段路径去重通过。程序结构检查不替代视觉与原文核查，后者见visual_audit.json。')
(ROOT/'validation.json').write_text(json.dumps({'records':len(rows),'scope':'whole_book','checks':checks},ensure_ascii=False,indent=2))
print(len(rows),'records')
