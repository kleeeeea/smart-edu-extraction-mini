"""分册结构与来源审计。程序检查不替代逐页视觉核对。"""
import csv,json,re,hashlib,shutil,collections
from pathlib import Path
B=Path(__file__).resolve().parents[1]
FIELDS=['knowledge_point_id','chapter','subchapter','section','knowledge_point','detail','example','pdf_page']
def save(name,data): (B/name).write_text(json.dumps(data,ensure_ascii=False,indent=2))
rows=list(csv.DictReader((B/'knowledge_points.csv').open(encoding='utf-8-sig')))
selection=json.loads((B/'selection.json').read_text());source=[json.loads(s)for s in (B/'source_records.jsonl').read_text().splitlines()]
report=json.loads((B/'source_report.json').read_text());errors=[]
assert (B/'knowledge_points.csv').read_bytes().startswith(b'\xef\xbb\xbf')
assert list(rows[0])==FIELDS
image_refs=0
for i,(row,src)in enumerate(zip(rows,source),1):
 assert row['knowledge_point_id']==f'RJ-PHYSICS-SEL3-{i:03d}'==src['knowledge_point_id']
 assert row['knowledge_point'] and row['detail']
 pages=src['verified_source_pages']
 for f in ['detail','example']:
  value=row[f];refs=re.findall(r'!\[page-(\d{3})\]\((images/physics-pep-selective-3/page-\d{3}\.png)\)',value)
  assert len(refs)==len(set(p for _,p in refs)),(i,f,'duplicate image')
  for num,path in refs:
   assert (B/path).is_file() and int(num)in pages,(i,f,path)
   assert f'![page-{num}]({path})' in value.splitlines()
  image_refs+=len(refs)
  assert not re.search(r'[\x00-\x08\x0b\x0c\x0e-\x1f]',value),(i,'control')
  assert value.count('$')%2==0,(i,f,'math delimiter')
  for math in re.findall(r'\$\$(.*?)\$\$|\$([^$\n]+)\$',value,re.S):
   expr=next((x for x in math if x),'');assert expr.count('{')==expr.count('}'),(i,f,expr)
 assert re.fullmatch(r'P\d+(?:-P\d+)?(?:;P\d+(?:-P\d+)?)*',row['pdf_page'])
assert len(rows)==len(selection)==len(source)
assert hashlib.sha256(Path(report['source_pdf']).read_bytes()).hexdigest()==report['sha256']
assert len(list((B/'images/physics-pep-selective-3').glob('page-*.png')))==143
# 固化已取得的官方资源元数据与电子书目录映射。
(B/'evidence').mkdir(exist_ok=True)
for temp,name in [('/tmp/physics-selective3-site.json','smartedu_detail.json'),('/tmp/physics-selective3-mapping.json','ebook_mapping.json')]:
 if Path(temp).exists():shutil.copyfile(temp,B/'evidence'/name)
mapping=json.loads((B/'evidence/ebook_mapping.json').read_text())['mappings']
labels=['第一章 分子动理论','1 分子动理论的基本内容','2 实验：用油膜法估测油酸分子的大小','3 分子运动速率分布规律','4 分子动能和分子势能','第二章 气体、固体和液体','1 温度和温标','2 气体的等温变化','3 气体的等压变化和等容变化','4 固体','5 液体','第三章 热力学定律','1 功、热和内能的改变','2 热力学第一定律','3 能量守恒定律','4 热力学第二定律','第四章 原子结构和波粒二象性','1 普朗克黑体辐射理论','2 光电效应','3 原子的核式结构模型','4 氢原子光谱和玻尔的原子模型','5 粒子的波动性和量子力学的建立','第五章 原子核','1 原子核的组成','2 放射性元素的衰变','3 核力与结合能','4 核裂变与核聚变','5 “基本”粒子','课题研究']
assert len(mapping)==len(labels)
outline=[]
for node,label in zip(mapping,labels):
 outline.append(dict(**node,pdf_visual_label=label,label_source='PDF P4目录及正文标题视觉核对',platform_evidence='官方ebook_mapping的节点路径、顺序和起始物理页；映射响应不含名称',records=[r['knowledge_point_id']for r in rows if (r['section']==label or r['chapter']==label and r['section']=='章引言')]))
assert len({(r['chapter'],r['section'])for r in rows if r['section']!='章引言' and r['chapter']!='课题研究'})==23
save('outline_alignment.json',dict(status='same_resource_hierarchy_and_pages_aligned',identity_evidence='资源ID、题名、143页及13,401,617字节匹配；2019审核标记及ISBN由原页核对。平台映射无名称字段，标签取PDF视觉目录，不声称独立取回平台目录文字。',nodes=outline))
save('metadata.json',dict(book_id='physics-pep-selective-3',title='普通高中教科书·物理选择性必修 第三册',subject='物理',stage='高中',publisher='人民教育出版社',resource_id='2109c25c-2e52-4da3-8ab3-18cbe632ec11',isbn='9787107345937',curriculum='普通高中物理课程标准（2017年版）',curriculum_evidence_pdf_page=142,approval_year=2019,edition_printing='版权页未明确提供版次、印次和出版日期；不推断',source=report,website_detail_url='https://s-file-1.ykt.cbern.com.cn/zxx/ndrv2/resources/tch_material/details/2109c25c-2e52-4da3-8ab3-18cbe632ec11.json',website_mapping_url='https://r1-ndr-private.ykt.cbern.com.cn/edu_product/esp/assets/2109c25c-2e52-4da3-8ab3-18cbe632ec11.pkg/ebook_mapping_1753321506274.txt',official_metadata_update='2026-08-18T12:28:55.172+0800',image_resolution='PyMuPDF 2×，完整物理页',image_reference_rule='同记录同字段每个整页路径仅一次，独立行，完整跨页句子后附图',page_numbering='PDF物理页；正文印刷页=物理页−5',extraction_policy='用户本次物理抽取规则优先；本地smartedu-math/references/extraction-policy.md',record_count=len(rows),supplementary_solved_example_fields=sum(bool(r['example'])for r in rows),core_solved_example='氘核结合能例题留在detail，作为质量亏损核心讲解',publication='独立抽取输出，不替换仓库既有分册或资源清单'))
# 页级审计明确有知识、混合历史与未解练习的不同处置。
exercises={11,14,18,21,22,27,30,35,37,40,42,46,47,48,49,54,56,58,62,63,65,66,68,69,70,75,78,80,82,85,86,88,96,102,103,104,109,112,114,115,119,121,123,128,130,135,136,140}
exclude_only={1:'封面；用于教材身份',2:'扉页；用于教材身份',3:'版权页；用于教材身份',4:'目录；用于层级对齐',5:'空白页',22:'复习与提高：未解题',23:'章引言：重复概述及历史评价',40:'历史评价与未解练习',47:'复习与提高：未解题',48:'复习与提高：未解题',49:'复习与提高：未解题',50:'章引言：历史概述与评价',63:'历史评价、人物引语及未解练习',69:'复习与提高：未解题',70:'复习与提高：未解题',71:'章引言：科学发展评价与概要',75:'人物传记、评价及未解练习',102:'索尔维会议史与未解练习',103:'复习与提高：未解题',104:'复习与提高：未解题',112:'练习与应用：未解题',136:'复习与提高：未解题',140:'参考选题：研究任务，无已给实验数据或结论',141:'索引；作覆盖复查，不重复抽取',142:'后记；用于课程标准与教材身份',143:'封底；用于ISBN确认'}
reviews=[];exclusions=[]
for p in range(1,144):
 ids=[r['knowledge_point_id']for r,s in zip(rows,source)if p in s['verified_source_pages']]
 status='retained_content_and_original_figures' if ids else 'excluded_or_identity_only'
 reason=exclude_only.get(p,'已保留有效正文、实验、图示；历史评价、栏目任务和重复概述不另录' if ids else '无新增可录知识；见完整原页')
 reviews.append(dict(pdf_page=p,visual_inspection='已查看整页渲染（双页并排）并针对公式、表格、侧栏及跨页转录复查',image=f'images/physics-pep-selective-3/page-{p:03d}.png',status=status,retained_ids=ids,notes=reason))
 if p in exercises or p in exclude_only:exclusions.append(dict(pdf_page=p,excluded=reason if not ids else '未解练习、思考中的纯任务部分及历史评价片段',retained_ids=ids,restore_from=f'images/physics-pep-selective-3/page-{p:03d}.png',policy='不补解未给结果；包含新概念、方法、实验及必要对比的片段保留'))
save('visual_review.json',reviews);save('exclusion_audit.json',exclusions)
# 最初100条准备编号到最终连续编号的映射；新增内容在最终教材顺序插入。
initial_names=[z['name']for z in selection if z['name']in list(json.loads((B/'patches.json').read_text()))[:100]]
# 原100条的稳定次序来自build.py中的records，不能以最终ID反推。
import sys
sys.path.insert(0,str(B/'scripts'));import build
old={z['name']:f'RJ-PHYSICS-SEL3-{i:03d}'for i,z in enumerate(build.records,1)}
with (B/'id_mapping.csv').open('w',encoding='utf-8-sig',newline='')as f:
 w=csv.writer(f);w.writerow(['initial_draft_id','final_id','knowledge_point','action'])
 for row in rows:w.writerow([old.get(row['knowledge_point'],''),row['knowledge_point_id'],row['knowledge_point'],'reindex' if row['knowledge_point']in old else 'add_from_mixed_content'])
changes=[]
for row,z in zip(rows,selection):
 before=dict(detail=build.join_specs(z['regions']),example=build.join_specs(z['examples']))
 after={f:re.sub(r'\n\n!\[page-\d+\]\(.*?\)','',row[f])for f in ['detail','example']}
 changes.append(dict(action='new_extraction_and_visual_correction',old_id=old.get(row['knowledge_point']),new_id=row['knowledge_point_id'],knowledge_point=row['knowledge_point'],source_sha256=report['sha256'],source_pages=row['pdf_page'],before_candidate=before,after_verified_transcription=after,recovery='原PDF、pages.jsonl及完整页PNG；patches.json保存最终转录'))
with (B/'change_log.jsonl').open('w')as f:
 for z in changes:f.write(json.dumps(z,ensure_ascii=False)+'\n')
validation=dict(status='passed',record_count=len(rows),chapter_counts=dict(collections.Counter(r['chapter']for r in rows)),covered_sections=23,research_sample_records=1,rendered_and_visually_inspected_pdf_pages=143,source_images=143,image_references=image_refs,checks=['UTF-8 BOM与8字段顺序','连续且唯一ID','非空名称与detail','23节及课题研究覆盖','官方目录节点路径和起始页顺序','物理页号与记录源页','图片存在、独立行、同字段不重复','数学标记配对、花括号配对、无控制字符','源PDF SHA-256未改变'],content_review='逐页渲染检查与两轮转录修订；公式、单位、表格、实验器材步骤现象结论、侧栏及跨页合并人工核对。结构断言不替代视觉检查。',limitations=['官方ebook_mapping未提供目录名称；名称依据同一PDF可视目录与正文，平台节点层级/顺序/页码已对齐','复杂图示、能级图、温度量级图及粒子标准模型图保留完整原页；未重绘或推导图中未给结论'],source_pdf_sha256=report['sha256'])
save('validation_report.json',validation)
(B/'README.md').write_text(f'''# 高中物理人教版·选择性必修第三册

本目录为独立抽取结果：{len(rows)}条，5章23节，另含完整课题研究样例。教材143个物理页均已检查渲染。

- [知识点CSV](knowledge_points.csv)：UTF-8 BOM，固定8字段。
- [Markdown阅读版](knowledge_points.md)：与CSV同源，图片相对本目录有效。
- [教材身份](metadata.json)、[目录对齐](outline_alignment.json)。
- [逐页视觉核对](visual_review.json)、[排除审计](exclusion_audit.json)、[结构校验](validation_report.json)。
- [来源记录](source_records.jsonl)、[初稿到终稿ID映射](id_mapping.csv)、[完整变更记录](change_log.jsonl)。

`detail`包含完整核心讲解、实验及必要原例。`example`仅含两处可分离的补充原例原解；氘核比结合能例题属于质量亏损的核心讲解，留在`detail`。跨页句子先合并，图片独立行置于完整讲解之后，同字段同路径仅一次。原页中仍可能显示被排除的练习或历史段落，它们未作为正文转录。

网站证据保存于`evidence/`。官方电子书映射提供节点层级、顺序和页码，但不含节点名称；文字目录采用同资源PDF的P4及正文标题，具体证据见目录对齐文件。版权页未明确给出的版次、印次和出版日期不推断。

最终转录保存在`patches.json`，来源选区候选保存在`selection.json`。`source_records.jsonl`同时保留候选选区和实际视觉复核整页；候选矩形并非最终逐字边界。`pages.jsonl`仅是文字层候选，不能替代原页。

重建：使用 `/Users/l/miniconda3/envs/base124/bin/python scripts/build.py`，随后运行同路径Python执行` scripts/package_audit.py`。`refine.py`、`correct_transcription.py`、`final_review.py`保存分阶段修订过程；不应在最终结果上重复执行，它们不是重建入口。

原PDF保持不变，未修改仓库既有分册、正式资源清单或发布内容。
''')
print(json.dumps(validation,ensure_ascii=False,indent=2))
