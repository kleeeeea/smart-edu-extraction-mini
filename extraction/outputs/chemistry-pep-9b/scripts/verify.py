import csv,json,re,hashlib
from pathlib import Path
from collections import Counter
R=Path(__file__).resolve().parents[1]
rows=list(csv.DictReader((R/'knowledge_points.csv').open(encoding='utf-8-sig')))
selection=json.loads((R/'selection.json').read_text());sources=[json.loads(t) for t in (R/'source_records.jsonl').read_text().splitlines()]
fields='knowledge_point_id chapter subchapter section knowledge_point detail example pdf_page'.split()
assert len(rows)==len(selection)==len(sources)==95
assert (R/'knowledge_points.csv').read_bytes().startswith(b'\xef\xbb\xbf')
assert list(rows[0])==fields
refs=0
for i,(r,s,p) in enumerate(zip(rows,selection,sources),1):
 assert r['knowledge_point_id']==p['knowledge_point_id']==f'RJ-CHEMISTRY-9B-{i:03}'
 assert r['knowledge_point']==s['name'] and r['chapter']==s['chapter']
 ps=sorted(set([a[0] for a in s['regions']]+s.get('image_pages',[])))
 assert ps==sorted(p['image_pages'])
 groups=[]
 for n in ps:
  if groups and n==groups[-1][-1]+1:groups[-1].append(n)
  else:groups.append([n])
 assert r['pdf_page']==';'.join(f'P{x[0]}' if len(x)==1 else f'P{x[0]}-P{x[-1]}' for x in groups)
 for f in ['detail','example']:
  t=r[f];paths=re.findall(r'!\[page-\d{3}\]\(([^)]+)\)',t)
  assert len(paths)==len(set(paths))
  for path in paths:
   assert (R/path).is_file();refs+=1
  for line in t.splitlines():
   if '![' in line:assert re.fullmatch(r'!\[page-\d{3}\]\(images/chemistry-pep-9b/page-\d{3}\.png\)',line)
  assert '\\\\' not in t, r['knowledge_point']
  assert t.count('$')%2==0
  for formula in re.findall(r'\$(.*?)\$',t,re.S):assert formula.count('{')==formula.count('}')
 assert r['detail'] and r['knowledge_point']
 assert '\ufffd' not in r['detail']
audit=json.loads((R/'visual_audit.json').read_text());assert [x['pdf_page'] for x in audit['pages']]==list(range(1,128))
assert all(x['status']=='visually_reviewed' for x in audit['pages'])
for n in range(1,128):assert (R/f'images/chemistry-pep-9b/page-{n:03}.png').is_file()
meta=json.loads((R/'source_report.json').read_text());assert hashlib.sha256(Path(meta['source_pdf']).read_bytes()).hexdigest()==meta['sha256']
assert meta['website_pdf_md5_matches']
report={'records':len(rows),'pages':127,'image_files':127,'image_references':refs,'chapter_counts':dict(Counter(r['chapter'] for r in rows)),'example_records':sum(bool(r['example']) for r in rows),'checks':{'csv_bom_and_eight_fields':'passed','ids_and_source_alignment':'passed','image_existence_standalone_and_no_same_field_duplicates':'passed','physical_page_ranges':'passed','math_delimiters_braces_and_backslashes':'passed','full_page_visual_audit':'127/127','source_sha256_and_website_md5':'passed'},'content_validation':'逐条读回与逐页图像核验见visual_audit.json、refinement_log.json及content_changes.json。结构校验不代替原文核验。','limitations':['网站ebook_mapping无节点标题字段，名称由同一PDF目录和页标题核验。','附录溶解性表和元素周期表以整页原图完整保留二维信息。']}
(R/'validation.json').write_text(json.dumps(report,ensure_ascii=False,indent=2));print(json.dumps(report,ensure_ascii=False,indent=2))
