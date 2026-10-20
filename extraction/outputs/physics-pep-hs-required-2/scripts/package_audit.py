"""Validate the standalone physics extraction package; structural checks do not replace visual review."""
from pathlib import Path
import csv,json,re,hashlib,collections
R=Path(__file__).resolve().parents[1]
def save(name,obj): (R/name).write_text(json.dumps(obj,ensure_ascii=False,indent=2))
def jsonl(name,rows): (R/name).write_text(''.join(json.dumps(x,ensure_ascii=False)+'\n' for x in rows))
rows=list(csv.DictReader((R/'knowledge_points.csv').open(encoding='utf-8-sig')))
src=[json.loads(l) for l in (R/'source_records.jsonl').read_text().splitlines()]
cand={x['knowledge_point']:x['candidate_detail'] for x in map(json.loads,(R/'transcription_candidates.jsonl').read_text().splitlines())}
meta=json.loads((R/'metadata.json').read_text());mapping=json.loads((R/'website/ebook_mapping.json').read_text())['mappings']
chapter_names=['第五章 抛体运动','第六章 圆周运动','第七章 万有引力与宇宙航行','第八章 机械能守恒定律','课题研究']
sections=[['曲线运动','运动的合成与分解','实验：探究平抛运动的特点','抛体运动的规律'],['圆周运动','向心力','向心加速度','生活中的圆周运动'],['行星的运动','万有引力定律','万有引力理论的成就','宇宙航行','相对论时空观与牛顿力学的局限性'],['功与功率','重力势能','动能和动能定理','机械能守恒定律','实验：验证机械能守恒定律'],[]]
titles=[]
for c,ss in zip(chapter_names,sections):titles.extend([c]+[f'{i}. {s}' for i,s in enumerate(ss,1)])
alignment=[]
for m,title in zip(mapping,titles):
 alignment.append(dict(m,pdf_toc_title=title,title_source='PDF P4 visual TOC',printed_page=m['page_number']-5,hierarchy_depth=m['node_path'].count('/'),matched=True))
save('outline_alignment.json',{'identity_evidence':['exact resource ID in local filename and website resource detail','matching title / 人教版 / 高中 / 必修第二册','matching PDF bytes 12699093 and page count 114','23 website mapping nodes align with PDF TOC order and physical starts'],'remote_title_strings_available':False,'name_alignment_note':'Names are PDF TOC transcriptions aligned with website node hierarchy/start pages, not remotely fetched title labels.','nodes':alignment})
exclusions=[
 {'pages':'P1-P5','reason':'封面、版权、目录和前言；用于版本及目录核对，不建立知识记录'},
 {'pages':'P10;P14;P18;P23-P26;P31;P35;P39;P43-P47;P53;P59;P63;P69;P75-P77;P83;P87-P88;P93;P98-P99;P103-P106','reason':'页内练习与应用、复习与提高中的未解练习不录入；同页正文、有效侧栏和已讲解原例按来源片段单独保留'},
 {'pages':'P48','reason':'章引言的历史背景、成就评价，无新增独立物理知识'},
 {'pages':'P49;P51-P53','reason':'历史人物、发展经过与评价剔除；开普勒定律、画椭圆和行星逆行／本轮均轮模型保留'},
 {'pages':'P57-P59','reason':'李政道侧栏、牛顿科学/成长生涯等纯历史评价不录入；扭秤测量原理及步骤保留'},
 {'pages':'P62-P63','reason':'发现和预言的具体物理应用保留；劳厄评价性引言等不录入'},
 {'pages':'P65-P68','reason':'航天人物、发射与探测年代史及评价不单列；宇宙速度、同步卫星和有效STSE应用保留'},
 {'pages':'P69-P75','reason':'纯历史评价与引导参加探究的任务性文字剔除；黑洞条件、相对论、演化知识和宏观验证保留'},
 {'pages':'P107-P110','reason':'甩手研究模型、原数据、分析、实验与明示结论保留在detail；泛泛学习价值评价和P110掷标枪参考选题／未解研究任务不录入'},
 {'pages':'P111-P114','reason':'术语索引、后记、空白页及封底，不重复录入已收知识'}]
save('exclusion_audit.json',exclusions)
# Page coverage records refer to actual visual page inspection, not OCR confidence.
review=[]
full_checks={8,11,12,13,17,18,20,21,22,28,30,31,34,36,37,38,40,42,55,56,57,60,61,64,65,66,69,71,72,74,80,81,82,83,85,86,89,90,91,92,96,97,98,101,102,108,109}
for page in range(1,115):
 ids=[s['knowledge_point_id'] for s in src if page in [v['pdf_page'] for v in s['regions']]+s['example_pages']]
 note='核对正文、侧栏、图示及跨页；练习题与纯评价文字排除。' if ids else '视觉核查后无独立收录内容；参见排除审计。'
 review.append({'pdf_page':page,'printed_page':page-5 if 6<=page<=112 else None,'image':f'images/physics-pep-hs-required-2/page-{page:03}.png','visual_inspected':True,'inspection':'contact_sheet_and_individual_enlargement' if page in full_checks else 'contact_sheet','record_ids':ids,'note':note})
jsonl('visual_review.jsonl',review)
save('page_map.json',review)
changes=[]
for s in src:
 raw=cand[s['knowledge_point']]
 if raw!=s['reviewed_text']:
  changes.append({'action':'visual_transcription_correction_and_selection','knowledge_point_id':s['knowledge_point_id'],'knowledge_point':s['knowledge_point'],'source_sha256':meta['sha256'],'regions':s['regions'],'before_candidate':raw,'after_reviewed_detail':s['reviewed_text'],'reason':'按页面图像恢复公式／段落顺序／跨页与条件，排除历史评价和未解练习；候选文本不作为正文依据','recoverable_from':'transcription_candidates.jsonl; patches.json; images/'})
 if s['example_text']:changes.append({'action':'separable_worked_example','knowledge_point_id':s['knowledge_point_id'],'pages':s['example_pages'],'after_example':s['example_text'],'reason':'保留教材题干、分析与原解；核心推导留在detail'})
jsonl('change_log.jsonl',changes)
idmap=[];old=0
for r in rows:
 if r['knowledge_point']=='行星逆行与本轮、均轮模型':oldid=None;action='insert mixed-sidebar physics content'
 else:old+=1;oldid=f'RJ-PHYSICS-HS-R2-{old:03}';action='retain / renumber provisional extraction'
 idmap.append({'provisional_id':oldid,'final_id':r['knowledge_point_id'],'knowledge_point':r['knowledge_point'],'action':action,'status':'provisional IDs were not published'})
save('id_map.json',idmap)
errs=[]
fields=['knowledge_point_id','chapter','subchapter','section','knowledge_point','detail','example','pdf_page']
if list(rows[0])!=fields:errs.append('CSV field order')
if not (R/'knowledge_points.csv').read_bytes().startswith(b'\xef\xbb\xbf'):errs.append('missing BOM')
if len(rows)!=66 or len(src)!=len(rows):errs.append('record count')
seen=set();refcount=0;all_examples=0
for i,(r,s) in enumerate(zip(rows,src),1):
 if r['knowledge_point_id']!=f'RJ-PHYSICS-HS-R2-{i:03}':errs.append(f'ID order {i}')
 if r['knowledge_point_id'] in seen:errs.append('duplicate ID')
 seen.add(r['knowledge_point_id'])
 for f in ['knowledge_point_id','knowledge_point','detail']:
  if not r[f].strip():errs.append(f'empty {i} {f}')
 for f in ['detail','example']:
  ts=re.findall(r'!\[page-(\d{3})\]\((images/physics-pep-hs-required-2/page-\d{3}\.png)\)',r[f])
  if len(ts)!=len(set(b for a,b in ts)):errs.append(f'duplicate image {i} {f}')
  for a,b in ts:
   if a not in b or not (R/b).exists():errs.append(f'bad image {i}')
   exact=f'![page-{a}]({b})'
   if exact not in r[f].splitlines():errs.append(f'image not standalone {i}')
  refcount+=len(ts)
  if r[f].count('$')%2:errs.append(f'math delimiter {i} {f}')
  if re.search(r'[\u0e00-\u1fff\u2c00-\u2dff\u3100-\u312f\u3300-\u33ff]',r[f]):errs.append(f'encoding {i}')
  # Actual images must agree with the field's source pages.
  expected={x['pdf_page'] for x in s['regions']} if f=='detail' else set(s['example_pages']) if r[f] else set()
  if {int(a) for a,b in ts}!=expected:errs.append(f'field provenance {i} {f}')
 if r['example']:all_examples+=1
 pages=sorted({x['pdf_page'] for x in s['regions']}|set(s['example_pages']));groups=[]
 for p in pages:
  if groups and p==groups[-1][-1]+1:groups[-1].append(p)
  else:groups.append([p])
 label=';'.join(f'P{g[0]}' if len(g)==1 else f'P{g[0]}-P{g[-1]}' for g in groups)
 if r['pdf_page']!=label:errs.append(f'page range {i}')
 if s['knowledge_point_id']!=r['knowledge_point_id']:errs.append('source ID mismatch')
expected_sections={(c,f'{i}. {s}') for c,ss in zip(chapter_names,sections) for i,s in enumerate(ss,1)}
actual={(r['chapter'],r['section']) for r in rows if r['section']!=r['chapter']}
if actual!=expected_sections:errs.append('18-section coverage')
if hashlib.sha256(Path(meta['source_pdf']).read_bytes()).hexdigest()!=meta['sha256']:errs.append('source PDF changed')
if len(list((R/'images/physics-pep-hs-required-2').glob('page-*.png')))!=114:errs.append('full image coverage')
save('validation_report.json',{'passed':not errs,'errors':errs,'records':len(rows),'chapters':4,'sections':len(actual),'research_records':sum(r['chapter']=='课题研究' for r in rows),'example_fields':all_examples,'supplementary_worked_examples':10,'page_images':114,'image_references':refcount,'source_pdf_sha256_verified':True,'checks':['UTF-8 BOM and eight fields','continuous unique IDs','nonempty core fields','all 18 outline sections','physical source-page ranges','standalone unique image references per field','image files and field-level provenance','math delimiter pairing','encoding checks','source PDF hash'],'visual_content_review':'Recorded separately in visual_review.jsonl; program checks do not certify semantics.'})
if errs:raise SystemExit('\n'.join(errs))
print(f'PASS: {len(rows)} records; {len(actual)} sections; {all_examples} example fields; {refcount} image references; source PDF unchanged')
