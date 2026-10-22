"""Validate the standalone chemistry package; retain content-review provenance."""
import csv,json,re,hashlib
from pathlib import Path
R=Path(__file__).resolve().parents[1]
def write(n,v): (R/n).write_text(json.dumps(v,ensure_ascii=False,indent=2))
rows=list(csv.DictReader((R/'knowledge_points.csv').open(encoding='utf-8-sig')))
sel=json.loads((R/'selection.json').read_text())
sources=[json.loads(x) for x in (R/'source_records.jsonl').read_text().splitlines()]
outline=json.loads((R/'outline_alignment.json').read_text())
report=json.loads((R/'source_report.json').read_text())
sha=hashlib.sha256(Path(report['source_pdf']).read_bytes()).hexdigest()
assert sha==report['sha256']
assert len(rows)==len(sel)==len(sources)==153
assert list(rows[0])==['knowledge_point_id','chapter','subchapter','section','knowledge_point','detail','example','pdf_page']
assert (R/'knowledge_points.csv').read_bytes().startswith(b'\xef\xbb\xbf')
ids=[]
for i,(row,s,source) in enumerate(zip(rows,sel,sources),1):
 expected=f'RJ-CHEMISTRY-9A-{i:03}'
 assert row['knowledge_point_id']==source['knowledge_point_id']==expected
 ids.append(expected)
 for field in ['detail','example']:
  value=row[field]; imgs=re.findall(r'!\[page-(\d{3})\]\((images/chemistry-pep-9a/page-\d{3}\.png)\)',value)
  assert len(imgs)==len({v for _,v in imgs})
  for p,path in imgs:
   assert path.endswith(f'page-{p}.png') and (R/path).is_file()
  for line in value.splitlines():
   if '![' in line: assert re.fullmatch(r'!\[page-\d{3}\]\(images/chemistry-pep-9a/page-\d{3}\.png\)',line)
  assert all(ord(c)>=32 or c in '\n\t' for c in value)
  assert value.count('$')%2==0
 assert row['detail'].split('![')[0].strip()
 expected_pages={z[0] for z in s['regions']}|set(s.get('image_pages',[]))|set(s.get('example_pages',[]))
 def expand(label):
  ps=set()
  for g in label.split(';'):
   q=list(map(int,re.findall(r'\d+',g)));ps.update(range(q[0],q[-1]+1))
  return ps
 assert expand(row['pdf_page'])==expected_pages
 detail_pages={int(x) for x in re.findall(r'!\[page-(\d+)\]',row['detail'])}
 assert detail_pages=={z[0] for z in s['regions']}|set(s.get('image_pages',[]))
 source['candidate_region_role']='文字层候选定位；最终修正含完整源页上的表格、图示和脚注，整页图为最终视觉核对依据。'
 candidates=[n for n in outline['nodes'] if n.get('name_from_pdf_toc')==s['topic']]
 if candidates:
  node=max(candidates,key=lambda n:len(n['node_path']))
  source['website_node_id']=node['node_id'];source['website_node_path']=node['node_path']
 else:source['website_node_status']='本地教材附录；网站ebook_mapping未单列'
 source['visual_status']='page_visual_comparison_and_record_readback_completed'
(R/'source_records.jsonl').write_text(''.join(json.dumps(x,ensure_ascii=False)+'\n' for x in sources))
for node in outline['nodes']:
 node['toc_visual_status']='目录名称及对应正文位置已视觉核对'
 matched=[r['knowledge_point_id'] for r in rows if r['subchapter']==node.get('name_from_pdf_toc')]
 node['record_ids']=matched
 if not matched:
  node['disposition']='章级标题由其子课题承载；跨学科实践以任务为主，新增有效内容已就地识别，重复或未解任务排除。'
outline['appendices']=[{'title':s['topic'],'website_status':'ebook_mapping未单列，依据本地实际附录标题','record_id':r['knowledge_point_id']} for r,s in zip(rows,sel) if s['topic'].startswith('附录')]
outline['identity_basis']='资源ID、修订标记、册次、封面、目录、网站源文件元数据22372171字节及199页一致；未下载远端PDF作SHA-256相同性比较。'
outline['source_names_limit']='网站ebook_mapping仅有节点路径、页码和顺序；未返回名称，名称依据本地PDF目录视觉读取。'
write('outline_alignment.json',outline)
old=json.loads((R/'exclusion_audit.json').read_text()); old=[x for x in old if x['pages']!='P63-P199']
extra=[
('P63-P67','保留微观构成、分子运动、分子间隔、分子与原子概念及必要实验；探究空白表不补写。'),
('P68-P69','分子探针、定比定律、倍比定律、酸碱当量定律有效内容保留；人物生平及评价排除。P69质量守恒简述由P117-P121完整实验讲解承载，不重复录入。'),
('P70-P71','小结重复已录知识；未解练习排除。'),
('P72-P77','原子结构、核外电子、离子、相对原子质量、模型方法及模型具体结构保留；张青莲生平、奖项评价和重复小结排除。'),
('P78','未解练习排除。'),
('P79-P83','元素定义、元素组成、符号、地壳元素分布和周期表知识保留；名称字形规律保留，命名史及人物评价排除；未解讨论不作答案。'),
('P84-P87','未解练习、空白整理图、重复总结及实践目标、查阅、制作、展示任务排除。'),
('P88','章节引入问题，不单列。'),
('P89-P96','水资源、保护与净化、实验操作和硬软水保留；参观调查任务及调水历史评价不单列；重复小结不追加。'),
('P97','未解练习、调查任务不录。'),
('P98-P101','氢气性质与验纯、氢燃烧、电解水及历史生成分解实验、分子组成和分类保留；实验表空白不补写。'),
('P102','未解练习不录。'),
('P103-P109','化学式、化合价、表格与定量认识首次核心讲解及原例原解保留；未解思考和调查不补答。'),
('P110-P113','练习、复习和空白整理内容排除。'),
('P114','用品清单具体器材保留；重复的氢燃烧、电解水步骤已由P98-P100承载，未解问题不录。'),
('P115','跨学科实践目标、调查检测与自制净水器任务，未提供新的完整原理或已讲解原例，不单列。'),
('P116','章引言和示意图与后文实验重复，不单列。'),
('P117-P121','定量研究必要情境、密闭与开放装置实验、质量守恒定律及微观解释保留；未解预测与表格空白保留；科学史纯评价排除。'),
('P122-P123','重复小结和未解习题不录。'),
('P124-P128','化学方程式含义、书写配平、标注条件和计算保留；例题1在detail，例题2在example；不补未解思考。'),
('P129-P133','重复整理、未解练习、复习和供氧器任务目标不录。'),
('P134','章引言概括与后文重复，不单列。'),
('P135-P140','碳单质结构与性质、有效新材料侧栏、实验与化学反应条件保留；奖项评价和未解讨论不录。'),
('P141-P142','P141结构—性质—用途的明确概括补入相应记录；重复小结和未解练习不录。'),
('P143-P149','两种碳氧化物、实验、化学反应、干冰、碳循环、低碳措施和捕集利用封存保留；排放任务指标、评价和未解调查不录。'),
('P150-P151','P150小结首次明示二氧化碳不能燃烧、不支持燃烧，补入相关实验记录；其余重复小结、未解练习、讨论和调查任务排除。'),
('P152-P155','制取原理、装置设计依据、气体收集、检验与验满图示及一般方法保留；原表空白不补写。'),
('P156-P160','小结、空白关系图、未解复习练习和计算题不录。'),
('P161-P162','保留15 mL稀盐酸制取步骤和溶液对照、加热等与纸花实验不同的组织方法；任务目标、未解问题不补答。'),
('P163-P164','低碳实践调查展示与目标排除；能源章引言重复后文内容，不单列。'),
('P165-P173','燃烧条件实验、方法、灭火、安全、爆炸极限及反应能量变化保留；未解设计、展示任务不补写。'),
('P174-P175','小结重复及未解练习、调查任务排除。'),
('P176-P182','化石能源组成、加工和利用、甲烷实验、沼气与可燃冰、污染和氢能源、新能源保留；历史评价和未解储量年限估算不录。'),
('P183-P187','图7-28作为新能源的实际应用图保留；重复小结及未解练习、复习和推理任务排除。'),
('P188','材料与白磷红磷实验不同的木块煤块对比实验保留；未解方案及结论不补写。'),
('P189','家用燃料调查目标、分析与展示任务不单列。'),
('P190-P192','仪器用途和新增注意事项保留；密集相对原子质量表保留整页源图和数据说明，避免线性转录歧义。'),
('P193-P199','P198元素周期表作为P82明确引用的实际插页关联；名词索引、后记、空白、致谢、封底不作知识点。')]
old.extend({'pages':p,'reason':v} for p,v in extra)
old=[v for v in old if not (v['pages']=='P150-P151' and v['reason']=='小结、未解练习、讨论和调查任务排除。')]
old=list({(v['pages'],v['reason']):v for v in old}.values())
write('exclusion_audit.json',old)
visual=[]
for p in range(1,200):
 linked=[r['knowledge_point_id'] for r in rows if p in {int(v) for v in re.findall(r'!\[page-(\d+)\]',r['detail']+'\n'+r['example'])}]
 start=p if p%2 else p-1;end=min(start+1,199)
 visual.append({'pdf_page':p,'status':'visual_review_completed','image':f'images/chemistry-pep-9a/page-{p:03}.png','review_spread':f'review/pages-{start:03}-{end:03}.jpg','record_ids':linked,'checks':'正文、公式与单位、表格空白、图示条件、跨页及侧栏阅读顺序；入表条目再读回核查。','disposition':'included_or_referenced' if linked else 'reviewed_no_new_record; 具体原因见exclusion_audit.json'})
write('visual_audit.json',visual)
write('progress.json',{'status':'complete','pdf_pages':199,'visual_review_pages':'P1-P199','records':len(rows),'chapters':'绪论、第一至第七单元、有效实验活动与附录','example_nonempty_records':sum(bool(r['example']) for r in rows),'pending':[],'provisional_ids':False})
previous=json.loads((R/'change_log.json').read_text())
previous=[v for v in previous if v.get('action')!='complete_extraction']
previous.append({'action':'complete_extraction','date':'2026-10-22','before_delivered_records':47,'after_records':153,'previous_ids_001_047':'retained','source_sha256':sha,'changes_file':'record_changes.json','id_mapping':'id_mapping.json','content_source':'selection.json','recovery':'原始PDF、文字候选、源图与编辑过程脚本均保留','notes':['移除按单道补充例题建立的记录，完整原例原解并入example','所有跨页句子合并后统一附图','未对实验空表、预测和未解习题补写答案','未合并到既有数学或物理知识库']})
write('change_log.json',previous)
checks=['UTF-8 BOM和八字段顺序','153条连续唯一ID及来源一一对应','源PDF SHA-256与199页身份','必填正文非空','物理页码范围与detail/example实际图源一致','图片存在、文件名和alt一致、独立行','同记录同字段整页图片无重复','字段内无意外控制字符、行内数学分隔符成对','001—047既有ID保留，候选至最终重编映射已记录']
write('validation.json',{'status':'passed','records':len(rows),'example_nonempty':sum(bool(r['example']) for r in rows),'scope':'whole_book_standalone_package','structural_checks':checks,'content_review':'153条读回核查；199页视觉检查，实验空表与结果来源区分、反应条件及算式比较已记录。','limitations':['网站映射未返回节点名称；标题来源本地视觉目录，路径和顺序来源网站映射。','密集附录数值表及二维结构图使用教材源图，未强行线性展开。','未修改教材原PDF、未运行针对数学仓库全库的发布校验。']})
# Retain previously linked partial files, clearly mark them superseded.
(R/'knowledge_points.partial.md').write_text('# 阶段文件已被整册结果替代\n\n请使用 [整册阅读版](knowledge_points.md) 与 [整册CSV](knowledge_points.csv)。\n\n旧阶段CSV保留供追溯，不能作为最终结果。\n')
(R/'README.md').write_text('''# 人教版化学九年级上册抽取

已完成全书199个PDF物理页的视觉核对与内容抽取，共153条记录。覆盖绪论、第一至第七单元、有效实验活动与附录。按教材自行识别知识点，未限制为每个网站课题一条。

- [知识点CSV](knowledge_points.csv)：UTF-8 BOM，固定八字段。
- [阅读版](knowledge_points.md)：与CSV对应；图片路径相对于本目录。
- [来源与教材身份](source_report.json)、[目录对齐](outline_alignment.json)。
- [视觉核对](visual_audit.json)、[排除与去重说明](exclusion_audit.json)、[最终校验](validation.json)。
- [ID映射](id_mapping.json)、[语义变更](record_changes.json)、[变更记录](change_log.json)。

同版SmartEdu资源ID为8c419b19-b3a9-4dbf-a8b4-546b7d337528。网站ebook_mapping确认节点路径、顺序和物理页；响应未返回节点名称，名称来自本地教材视觉目录，未声称名称由网站返回。网站源文件元数据与本地文件字节数、页数一致；未下载远端PDF比对SHA-256。

`detail`保留核心讲解、必要情境和首次讲解原例。化学方程式计算的例题2可以自然分离，完整题干原解放在相应记录的`example`，并保留与例题1不同的反求方向和简化格式。其他核心原例不拆走。

实验按教材保留器材、步骤、现象及明示结论；未解的预测、实验现象空表和结论空格不补写。不同材料、条件或组织方式的实验保留必要对比。纯历史评价、任务目标、未解练习及重复小结不再次录入。

所有跨页句子先合并，再附整页图；同一记录、同一字段、同一整页路径只出现一次。图片使用`![page-NNN](images/chemistry-pep-9a/page-NNN.png)`。密集相对原子质量表和二维原子结构、装置等以源图保留，附录数据说明保留文字。

PDF页码为物理页序；正文印刷页通常为物理页减7。页码字段包含各字段必要图源的并集，例如周期表插页P198。源页候选定位和手工修正保存在`selection.json`、`source_records.jsonl`及`transcription_candidates.jsonl`中。

重建与校验：

```sh
/Users/l/miniconda3/envs/base124/bin/python extraction/outputs/chemistry-pep-9a/scripts/build.py
/Users/l/miniconda3/envs/base124/bin/python extraction/outputs/chemistry-pep-9a/scripts/package_audit.py
```

`selection.json`是最终构建输入。其他select、extend、unit、refine、finalize脚本是编辑过程留存，不应重跑覆盖最终修订。此前阶段链接保留，`.partial.csv`不是最终结果。前次交付001—047号保持不变；本轮候选至最终记录的编号变更见ID映射。
''')
print(json.dumps({'status':'passed','records':len(rows),'visual_pages':199,'example_nonempty':sum(bool(r['example']) for r in rows)},ensure_ascii=False))
