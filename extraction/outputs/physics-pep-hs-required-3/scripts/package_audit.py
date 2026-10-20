"""Audit the standalone volume; structural checks do not establish textual fidelity."""
from pathlib import Path
import csv,json,re,hashlib,collections
R=Path(__file__).resolve().parents[1]
def save(n,x): (R/n).write_text(json.dumps(x,ensure_ascii=False,indent=2))
def jsonl(n,x): (R/n).write_text(''.join(json.dumps(a,ensure_ascii=False)+'\n' for a in x))
rows=list(csv.DictReader((R/'knowledge_points.csv').open(encoding='utf-8-sig')))
src=[json.loads(x) for x in (R/'source_records.jsonl').read_text().splitlines()]
meta=json.loads((R/'metadata.json').read_text())
ns={'__file__':str(R/'scripts/build.py')}
exec((R/'scripts/build.py').read_text().split('\nP=json.loads')[0],ns)
CH,SE=ns['CH'],ns['SE']
mapping=json.loads((R/'website/ebook_mapping.json').read_text())['mappings']
titles=[]
for c,ss in SE.items():titles.extend([CH[c]]+[f'{i}. {s}' for i,s in enumerate(ss,1)])
assert len(titles)==len(mapping)==29
alignment=[dict(m,title=t,title_source='PDF P4-P5 visual TOC, aligned to website actual node',printed_page=m['page_number']-5,matched=True) for m,t in zip(mapping,titles)]
save('outline_alignment.json',{'resource_id':meta['resource_id'],'identity_evidence':['local filename resource UUID equals website UUID','title / publisher / volume match','local and website PDF both 14530590 bytes; website images specify143 pages','all29 actual website node hierarchy/order/start pages align with the PDF'],'remote_pdf_hash_verified':False,'remote_pdf_status':401,'remote_titles_available':False,'title_note':'网站映射无标题字符串；名称依PDF目录视觉转录并逐项按节点起页对齐，不声称远端返回了名称。','nodes':alignment})
ex=[{'pages':'P1-P5','reason':'封面、版权、前言、目录用于身份核对，不作为独立知识点'},
{'pages':'P6;P30;P57;P83;P108','reason':'章引言情境、问题与学习指标；后续已完整讲解的内容不重复录入'},
{'pages':'P10;P15;P21-P22;P27-P29;P35;P39;P42;P48;P54-P56;P61;P66;P72;P76;P79-P82;P87;P93;P97;P104-P107;P113;P118;P122-P123;P128;P133-P135','reason':'页内练习与应用、复习与提高的未解题不录入；同页正文和补充原例按来源记录保留'},
{'pages':'P7;P9-P12;P16;P31;P58;P65;P98;P102;P109-P110;P119-P120;P122;P124-P125;P130-P132','reason':'纯人物年代、发展经过、评价和题辞排除；混合栏目的物理内容、条件、方法及实验另行保留'},
{'pages':'P44','reason':'传感器实验器材步骤和给定图像保留；未解图像面积估算和新充电图像设计任务不补答案'},
{'pages':'P99-P101','reason':'能源实际转化和发电原理保留，成就排名、发展预测等不单列；跨页正文完整合并'},
{'pages':'P112-P113;P117;P132','reason':'分子电流、地磁偏角、射电望远镜等有效内容保留；纯航海历史、人物评价、项目指标不录入'},
{'pages':'P136-P140','reason':'完整充电宝研究样例保留原器材、操作、四表、图像和明示结论；P140未开展的手机耗电参考选题排除'},
{'pages':'P141-P143','reason':'索引、后记和封底不重复录入'}]
save('exclusion_audit.json',ex)
enlarged={10,12,13,14,18,34,41,47,50,51,52,64,68,69,70,76,92,95,115,117,130,137,138}
review=[]
for p in range(1,144):
 ids=[s['knowledge_point_id'] for s in src if p in {a['pdf_page'] for a in s['regions']}|set(s['example_pages'])]
 review.append({'pdf_page':p,'printed_page':p-5 if 6<=p<=142 else None,'image':f'images/{meta["book_id"]}/page-{p:03}.png','visual_inspected':True,'inspection':'contact_sheet_and_individual_enlargement' if p in enlarged else 'contact_sheet','record_ids':ids,'note':'逐页检查正文、公式、单位、图示、栏目与跨页；无记录页的排除理由见exclusion_audit.json'})
jsonl('visual_review.jsonl',review);save('page_map.json',review)
candidates={x['knowledge_point']:x['candidate_detail'] for x in map(json.loads,(R/'transcription_candidates.jsonl').read_text().splitlines())}
changes=[]
for s in src:
 changes.append({'action':'new_extraction_with_visual_transcription','final_id':s['knowledge_point_id'],'old_id':None,'knowledge_point':s['knowledge_point'],'source_sha256':meta['sha256'],'candidate_selection_regions':s['regions'],'reviewed_source_pages':sorted({v['pdf_page'] for v in s['regions']}|set(s['example_pages'])),'before_candidate':candidates[s['knowledge_point']],'after_detail':s['reviewed_text'],'after_example':s['example_text'],'reason':'依据页面图像恢复公式、段落次序与跨页语句；排除任务、未解练习和纯历史评价','recovery':'patches.json; transcription_candidates.jsonl; page images'})
jsonl('change_log.jsonl',changes)
save('id_map.json',[{'old_id':None,'final_id':r['knowledge_point_id'],'knowledge_point':r['knowledge_point'],'action':'new extraction; contiguous final numbering after selection'} for r in rows])
errors=[]
fields=['knowledge_point_id','chapter','subchapter','section','knowledge_point','detail','example','pdf_page']
if list(rows[0])!=fields:errors.append('fields')
if not (R/'knowledge_points.csv').read_bytes().startswith(b'\xef\xbb\xbf'):errors.append('BOM')
if len(rows)!=len(src) or len(rows)!=91:errors.append('count')
refs=0
for i,(r,s) in enumerate(zip(rows,src),1):
 if r['knowledge_point_id']!=f'RJ-PHYSICS-HS-R3-{i:03}':errors.append(f'ID{i}')
 for f in ['knowledge_point_id','knowledge_point','detail']:
  if not r[f].strip():errors.append(f'empty{i}:{f}')
 for f in ['detail','example']:
  matches=re.findall(r'!\[page-(\d{3})\]\((images/physics-pep-hs-required-3/page-\d{3}\.png)\)',r[f]);refs+=len(matches)
  if len(matches)!=len(set(b for a,b in matches)):errors.append(f'duplicate image{i}:{f}')
  for a,b in matches:
   if not (R/b).exists() or a not in b:errors.append(f'image{i}:{f}')
   if f'![page-{a}]({b})' not in r[f].splitlines():errors.append(f'image line{i}:{f}')
  expect={v['pdf_page'] for v in s['regions']} if f=='detail' else set(s['example_pages']) if r[f] else set()
  if expect!={int(a) for a,b in matches}:errors.append(f'provenance{i}:{f}')
  if re.search(r'[\u0e00-\u1fff\u2c00-\u2dff\u3100-\u312f\u3300-\u33ff\x00-\x08\x0e-\x1f]',r[f]):errors.append(f'encoding{i}:{f}')
  if r[f].count('$')%2:errors.append(f'math{i}:{f}')
 if r['pdf_page']!=ns['label']([v['pdf_page'] for v in s['regions']]+s['example_pages']):errors.append(f'pages{i}')
 if r['knowledge_point_id']!=s['knowledge_point_id']:errors.append('source ID')
expected={(CH[c],f'{i}. {t}') for c,ss in SE.items() for i,t in enumerate(ss,1)}
actual={(r['chapter'],r['section']) for r in rows if r['section']!=r['chapter']}
if actual!=expected:errors.append('section coverage')
if hashlib.sha256(Path(meta['source_pdf']).read_bytes()).hexdigest()!=meta['sha256']:errors.append('PDF hash')
if len(list((R/f'images/{meta["book_id"]}').glob('page-*.png')))!=143:errors.append('image coverage')
report={'passed':not errors,'errors':errors,'records':len(rows),'chapters':5,'sections':len(actual),'research_records':sum(r['chapter']=='课题研究' for r in rows),'example_fields':sum(bool(r['example']) for r in rows),'page_images':143,'visual_page_reviews':143,'individually_enlarged_pages':sorted(enlarged),'image_references':refs,'source_pdf_sha256_verified':True,'chapter_counts':dict(collections.Counter(r['chapter'] for r in rows)),'checks':['8 fields + BOM','continuous unique IDs','23-section hierarchy coverage','page labels','image existence + unique standalone paths within each field','field provenance','encoding + math delimiters','source PDF hash unchanged'],'limitations':['程序校验不代替视觉内容核对','网站PDF直接请求401，未做远端PDF哈希相等验证；身份依据资源UUID、元数据、字节数、143页及29节点映射']}
save('validation_report.json',report)
if errors:raise SystemExit('\n'.join(errors))
print(json.dumps(report,ensure_ascii=False))
