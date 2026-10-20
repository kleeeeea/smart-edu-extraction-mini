"""Validate the standalone extraction package; structural checks do not replace visual review."""
from pathlib import Path
import csv,json,re,hashlib,collections
R=Path(__file__).resolve().parents[1]; BOOK=R.name
FIELDS='knowledge_point_id,chapter,subchapter,section,knowledge_point,detail,example,pdf_page'.split(',')
rows=list(csv.DictReader((R/'knowledge_points.csv').open(encoding='utf-8-sig')))
sources=[json.loads(x) for x in (R/'source_records.jsonl').read_text().splitlines()]
meta=json.loads((R/'source_report.json').read_text());pdf=Path(meta['source_pdf'])
assert hashlib.sha256(pdf.read_bytes()).hexdigest()==meta['sha256']
assert (R/'knowledge_points.csv').read_bytes().startswith(b'\xef\xbb\xbf')
assert list(rows[0])==FIELDS and len(rows)==len(sources)==82
assert len({x['knowledge_point_id'] for x in rows})==len(rows)
for i,(row,src) in enumerate(zip(rows,sources),1):
 assert row['knowledge_point_id']==src['knowledge_point_id']==f'RJ-PHYSICS-SC1-{i:03}'
 assert row['knowledge_point'] and row['detail']
 allpages=set()
 for field,key in [('detail','detail_regions'),('example','example_regions')]:
  t=row[field];regs=src[key];ps=set(a[0] for a in regs);allpages|=ps
  refs=re.findall(r'!\[page-(\d{3})\]\((images/[^)]+)\)',t)
  paths=[v for p,v in refs]
  assert len(paths)==len(set(paths)),(i,field,'duplicate image')
  assert {int(p) for p,v in refs}==ps if t else not regs,(i,field,'source coverage')
  for p,v in refs:
   assert v==f'images/{BOOK}/page-{p}.png' and (R/v).is_file()
   assert f'![page-{p}]({v})' in t.splitlines()
  assert not re.search('[\x00-\x08\x0b\x0c\x0e-\x1f]',t)
  assert t.count('$')%2==0,(i,field,'math delimiters')
  if refs:
   # Every cross-page body precedes image references.
   first=t.index('![page-');assert not re.sub(r'!\[page-\d{3}\]\(images/[^)]+\)','',t[first:]).strip()
  for m in re.findall(r'\$([^$]*)\$',t):assert m.count('{')==m.count('}'),(i,m)
 listed=set()
 for part in row['pdf_page'].split(';'):
  nums=list(map(int,re.findall(r'\d+',part)));listed.update(range(nums[0],nums[-1]+1))
 assert listed==allpages,(i,listed,allpages)
assert len({r['section'] for r in rows if re.match('[1-6]\\.',r['section'])})==19
by={r['knowledge_point']:r for r in rows}
for title,tokens in {
 '匀变速直线运动的位移与时间的关系':['x-x_0','坐标原点','\\frac12at^2'],
 '实验：探究加速度与力、质量的关系':['质量小很多','同时开始运动','过原点的直线'],
 '秒、米、千克的定义':['299\\,792\\,458','10^{-34}','2019年5月20日'],
 '研究样例：球形物体空气阻力大小与速率关系':['体积不变','32.8','T_0'],
 '超重与失重':['60 kg','603 N','完全失重'],
 '有效数字与测量结果的记录':['19.0 mm','0.013 3 m','不可靠的']
}.items():
 for t in tokens:assert t in by[title]['detail'],(title,t)
assert not by['超重与失重']['example']
assert not by['统一单位后的计算方法']['example']
report={'status':'passed','records':len(rows),'sections':19,'supplementary_example_fields':sum(bool(r['example']) for r in rows),'physical_pdf_pages':134,'source_sha256_verified':True,'csv_bom_and_fields':True,'image_links_standalone_existing_and_deduplicated':True,'cross_page_text_precedes_images':True,'math_delimiters_and_braces':True,'source_page_mapping':True,'targeted_content_assertions':True,'visual_review_evidence':'visual_review.jsonl','limitation':'程序断言仅验证结构和指定内容锚点；逐页视觉核对另记于 visual_review.jsonl。'}
(R/'validation_report.json').write_text(json.dumps(report,ensure_ascii=False,indent=2))
print(json.dumps(report,ensure_ascii=False,indent=2))
