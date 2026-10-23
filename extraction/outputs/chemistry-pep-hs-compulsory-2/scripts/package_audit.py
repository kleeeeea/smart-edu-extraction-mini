"""Package the completed visual extraction and audit its source/image relationships."""
from pathlib import Path
import csv,json,re,hashlib,collections
R=Path(__file__).resolve().parents[1]
def save(name,obj): (R/name).write_text(json.dumps(obj,ensure_ascii=False,indent=2))
S=json.loads((R/'selection.json').read_text()); report=json.loads((R/'source_report.json').read_text())
rows=list(csv.DictReader((R/'knowledge_points.csv').open(encoding='utf-8-sig')))
# Actual printed subheadings, including headings not separately exposed as platform nodes.
starts={
'第一节 硫及其化合物':[(7,380,'一、硫和二氧化硫'),(9,531,'二、硫酸'),(11,526,'三、硫酸根离子的检验'),(12,438,'四、不同价态含硫物质的转化')],
'第二节 氮及其化合物':[(16,401,'一、氮气与氮的固定'),(18,60,'二、一氧化氮和二氧化氮'),(18,503,'三、氨和铵盐'),(20,268,'四、硝酸'),(21,407,'五、酸雨及防治')],
'第三节 无机非金属材料':[(24,379,'一、硅酸盐材料'),(26,335,'二、新型无机非金属材料')],
'第一节 化学反应与能量变化':[(37,338,'一、化学反应与热能'),(41,60,'二、化学反应与电能')],
'第二节 化学反应的速率与限度':[(47,296,'一、化学反应的速率'),(51,513,'二、化学反应的限度'),(52,586,'三、化学反应条件的控制')],
'第一节 认识有机化合物':[(65,317,'一、有机化合物中碳原子的成键特点'),(67,60,'二、烷烃')],
'第二节 乙烯与有机高分子材料':[(72,317,'一、乙烯'),(74,513,'二、烃'),(76,659,'三、有机高分子材料')],
'第三节 乙醇与乙酸':[(82,275,'一、乙醇'),(84,468,'二、乙酸'),(86,60,'三、官能团与有机化合物的分类')],
'第四节 基本营养物质':[(88,359,'一、糖类'),(90,511,'二、蛋白质'),(92,59,'三、油脂')],
'第一节 自然资源的开发利用':[(103,314,'一、金属矿物的开发利用'),(105,59,'二、海水资源的开发利用'),(107,60,'三、煤、石油和天然气的综合利用')],
'第二节 化学品的合理使用':[(112,358,'一、化肥、农药的合理施用'),(114,533,'二、合理用药'),(116,634,'三、安全使用食品添加剂')],
'第三节 环境保护与绿色化学':[(122,337,'一、化学与环境保护'),(124,307,'二、绿色化学')]}
for s,row in zip(S,rows):
 p,y=(s['regions'][0][:2] if s['regions'] else [min(s['image_pages']),0]); current=s['topic']
 for hp,hy,title in starts.get(s['topic'],[]):
  if (p,y)>=(hp,hy):current=title
 row['section']=current;s['section']=current
# Preserve supplement location: a whole sidebar belongs to its preceding topic, not to a thematic back-link.
for s,row in zip(S,rows):
 if s['name']=='基本营养物质与糖类的分类':s['section']=row['section']='一、糖类'
 if s['name']=='自然资源的分类与可持续发展':s['section']=row['section']=s['topic']
 if s['name']=='大宗化学品与精细化学品':s['section']=row['section']=s['topic']
(R/'selection.json').write_text(json.dumps(S,ensure_ascii=False,indent=2))
with (R/'knowledge_points.csv').open('w',encoding='utf-8-sig',newline='') as f:
 w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
md=['# 人教版高中化学必修第二册\n\n全册156条记录。教材身份、目录对齐及核验范围见 [README](README.md)。\n']
for r in rows:
 md += [f"## {r['knowledge_point_id']} {r['knowledge_point']}\n\n{r['chapter']} / {r['subchapter']} / {r['section']} · {r['pdf_page']}\n\n{r['detail']}\n"]
 if r['example']:md += ['### 补充原例与原解\n\n'+r['example']]
(R/'knowledge_points.md').write_text('\n'.join(md))
# Website hierarchy has stable node paths and physical pages, but no node-title strings.
web=json.loads((R/'website/ebook_mapping.json').read_text()); title_pages={6:'第五章 化工生产中的重要非金属元素',7:'第一节 硫及其化合物',16:'第二节 氮及其化合物',24:'第三节 无机非金属材料',31:'整理与提升',34:'实验活动4 用化学沉淀法去除粗盐中的杂质离子',35:'实验活动5 不同价态含硫物质的转化',36:'第六章 化学反应与能量',37:'第一节 化学反应与能量变化',47:'第二节 化学反应的速率与限度',57:'整理与提升',61:'实验活动6 化学能转化成电能',62:'实验活动7 化学反应速率的影响因素',64:'第七章 有机化合物',65:'第一节 认识有机化合物',72:'第二节 乙烯与有机高分子材料',82:'第三节 乙醇与乙酸',88:'第四节 基本营养物质',96:'整理与提升',100:'实验活动8 搭建球棍模型认识有机化合物分子结构的特点',101:'实验活动9 乙醇、乙酸的主要性质',102:'第八章 化学与可持续发展',103:'第一节 自然资源的开发利用',112:'第二节 化学品的合理使用',122:'第三节 环境保护与绿色化学',128:'整理与提升'}
nodes=[]
for n in web['mappings']:
 depth=n['node_path'].count('/'); z=dict(n,depth=depth,website_title_status='not_present_in_mapping')
 if depth<=1:z.update(pdf_title=title_pages[n['page_number']],title_evidence='PDF P4-P5目录及对应起始页视觉核对')
 else:
  z['pdf_title_status']='按同页小标题与节点位置辅助核对；不虚构网站标题'
 nodes.append(z)
source_item=next(x for x in json.loads((R/'website/resource-v2.json').read_text())['ti_items'] if x.get('ti_is_source_file'))
save('outline_alignment.json',dict(resource_id=report['resource_id'],website_title='普通高中教科书·化学必修 第二册',resource_url='https://basic.smartedu.cn/tchMaterial/detail?contentType=assets_document&contentId='+report['resource_id'],identity_evidence=['资源ID与输入文件名一致','网站源文件大小12793174字节、139页与本地一致','ISBN9787107335754与本地封底一致','目录章、节、实验活动起始页及层级与本地P4-P5和正文一致'],local_sha256=report['sha256'],local_md5=report['local_md5'],website_source_ti_md5=source_item['ti_md5'],hash_comparison='网站ti_md5为带-2后缀的分段对象标识，不能当作本地文件MD5比较，未宣称远端与本地逐字节相同',nodes=nodes,ordering='章/节依平台节点路径及页码；知识点依教材正文、跨栏阅读顺序细分；平台未单列的小标题由教材补充',limitations=['ebook_mapping没有标题字符串，不能声称逐字核验了网站各末级名称。章、节名称来自同版PDF目录；小标题来自视觉核定的正文。','附录与元素周期表由教材目录/原页定位，未虚构网站独立节点。']))
by_page=collections.defaultdict(list)
sources=[json.loads(l) for l in (R/'source_records.jsonl').read_text().splitlines()]
for row,src,s in zip(rows,sources,S):
 src.update(chapter=row['chapter'],subchapter=row['subchapter'],section=row['section'],knowledge_point=row['knowledge_point'],image_placement='所有跨页/跨栏句段完整合并后，统一附本记录图源；同字段同路径一次')
 for p in src['image_pages']:by_page[p].append(row['knowledge_point_id'])
(R/'source_records.jsonl').write_text(''.join(json.dumps(x,ensure_ascii=False)+'\n' for x in sources))
roles={1:'封面：书名、2019审核标记',2:'扉页/编写说明',3:'编写人员与出版信息',4:'目录',5:'目录与栏目索引',6:'章引言与章图',36:'章引言与章图',64:'章引言与章图',102:'章引言与章图',131:'名词索引（导航，不重复知识）',135:'空白页',136:'后记：课程标准与审核年证据',137:'图片来源致谢',139:'封底、ISBN'}
exercise=set([15,23,30,32,33,46,54,55,56,58,59,60,71,81,87,95,98,99,111,121,126,127,129,130])
review=set([31,57,96,97,128])
tasks={45:'了解车用能源：资料搜集和报告任务',94:'了解食品中的有机化合物：资料搜集和研究任务'}
exclusions=[]; audit=[]
for p in range(1,140):
 role=roles.get(p,'正文、实验或有效侧栏')
 if p in exercise:role='练习/复习题'+('，同页正文已另行抽取' if by_page[p] else '')
 if p in review:role='整理与提升，复现已有知识与待填图表'
 if p in tasks:role=tasks[p]
 note='逐页查看双页图；对入选内容核对公式、单位、条件、表格/图示及跨页、跨栏衔接。'
 if not by_page[p]:
  why=role+'；不含本次应新增的完整知识讲解，或其知识已在首次讲解中收录。'
  exclusions.append(dict(pdf_page=p,scope='whole_page',reason=why))
 else:
  why='仅选取source_records标明的正文、已给步骤及明示现象/结论；同页未解练习、任务目的、历史评价、重复总结及版式内容不进入主字段。'
 audit.append(dict(pdf_page=p,printed_page=p-5 if 6<=p<=134 else None,review_image=f'review/pages-{(p if p%2 else p-1):03}-{min((p if p%2 else p-1)+1,139):03}.jpg',page_image=f'images/chemistry-pep-hs-compulsory-2/page-{p:03}.png',visual_status='reviewed',role=role,record_ids=by_page[p],checks=note,exclusion_policy=why))
fragments=[(17,'科学史话 合成氨','保留500～600℃、17.5～20.0MPa、锇催化剂、超过6%数据；排除人物年代、获奖及评价'),(28,'新型陶瓷','不同材料的组成性能用途全部保留，不因同属陶瓷而去重'),(29,'富勒烯','排除发现的意义评价，保留定义结构用途'),(44,'电池研发人员','保留材料相容性、温湿度、容量等技术因素；排除职业人才要求'),(49,'探究影响化学反应速率的因素','保留给定温度对比实验；自拟浓度方案、空表及讨论不补答案'),(51,'神奇的催化剂','保留选择性、酶、仿酶催化；排除纯评价'),(75,'烃的分子结构探究','方法与已有模型知识/实验活动8重复，不重复自拟模型任务'),(76,'苯的发现与结构研究史','保留芳香族含义、苯用途及现代平面正六边形结构；排除历史假说及评价'),(93,'奶油、营养师','奶油材料性能及人造奶油组成保留；重复氢化原理与职业性叙述不再录'),(100,'实验活动8问题讨论','保留器材及搭建步骤；表内空格与未解同分异构问题不作答'),(101,'实验活动9','用量/方法与正文不同，保留；不填自拟验证实验和讨论答案'),(113,'滴滴涕的功与过','保留稳定性、脂溶性、富集及DDT→DDE结构变化；排除历史功绩与评价'),(114,'化肥农药辩论','排除辩论任务与未证实论点，不作为知识结论'),(116,'青蒿素及缓释药物','保留结构图和药物改造、缓释方法；排除历史获奖评价'),(119,'食品添加剂限量表','原表GB2760—2014数据作为教材内容保留，不更新为外部现行标准'),(120,'豆腐制作','原图六步方法保留；搜集资料、研究目的和评价任务排除，不补点卤温度用量'),(125,'环氧乙烷、人工光合作用','保留已给反应与资源转化设想；不解答比较题，不录宏观评价和任务指标'),(126,'环境保护工程师','仅保留光谱/滴定分析方法及检测对象，排除职业要求')]
exclusions.extend(dict(pdf_page=p,scope=scope,reason=why) for p,scope,why in fragments)
save('visual_audit.json',dict(total_pages=139,reviewed_pages=139,method='所有物理页的渲染图逐页视觉查看；文字层仅作候选；重点反应式及跨栏页再次复核',pages=audit))
save('exclusions.json',exclusions)
save('page_map.json',audit)
save('changes.json',dict(action='initial_full_book_extraction',source_sha256=report['sha256'],records=len(rows),existing_book_outputs_modified=False,description='新增独立分册；正文知识点细分，跨页句合并，视觉校正化学式及条件，未给结果不补，表格/结构原图保留。',record_snapshots=rows))
save('id_map.json',[dict(old_id=None,new_id=x['knowledge_point_id'],knowledge_point=x['knowledge_point'],reason='新分册首次抽取，按教材次序连续编号') for x in rows])
fields=['knowledge_point_id','chapter','subchapter','section','knowledge_point','detail','example','pdf_page']
assert list(rows[0])==fields and (R/'knowledge_points.csv').read_bytes().startswith(b'\xef\xbb\xbf')
assert len(rows)==len(S)==len(sources)==156
assert len({x['knowledge_point'] for x in rows})==len(rows)
assert [x['knowledge_point_id'] for x in rows]==[f'RJ-CHEMISTRY-HSC2-{i:03}' for i in range(1,157)]
for row,src,s in zip(rows,sources,S):
 assert row['knowledge_point_id']==src['knowledge_point_id']
 assert s['detail'].strip() and all(row[k].strip() for k in fields if k!='example')
 assert not any(ord(c)<32 and c not in '\n\t\r' for c in row['detail'])
 for field in ['detail','example']:
  refs=re.findall(r'!\[page-(\d{3})\]\((images/chemistry-pep-hs-compulsory-2/page-\d{3}\.png)\)',row[field])
  assert len(refs)==len(set(v for _,v in refs))
  for pn,path in refs:assert (R/path).is_file() and f'page-{pn}.png' in path
  for line in row[field].splitlines():
   if '![' in line:assert re.fullmatch(r'!\[page-\d{3}\]\(images/chemistry-pep-hs-compulsory-2/page-\d{3}\.png\)',line)
 assert set(int(p) for p in re.findall(r'!\[page-(\d{3})\]',row['detail']))==set(src['image_pages'])
 assert all(1<=reg[0]<=139 for reg in src['regions'])
assert hashlib.sha256(Path(report['source_pdf']).read_bytes()).hexdigest()==report['sha256']
assert len(audit)==139 and all((R/x['page_image']).is_file() and (R/x['review_image']).is_file() for x in audit)
required={'原电池实验、电子转移与正负极':['Zn²⁺','H⁺','e⁻'],'化学键变化与反应中的能量变化':['25 ℃','101 kPa','436','243','679','862'],'乙醇、乙酸性质及乙酸乙酯制取实验':['0.5 mL','0.5 cm','3 mL'],'硫酸的工业制备与用途':['400～500','V₂O₅','98.3%'],'链状烷烃通式与同系物':['CₙH₂ₙ₊₂'],'海水中的化学元素及富集程度':['5×10⁶','4×10⁻⁶']}
byname={x['knowledge_point']:x for x in rows}
for name,terms in required.items():assert all(t in byname[name]['detail'] for t in terms),(name,terms)
save('validation.json',dict(status='passed',records=156,pdf_pages=139,images=139,visually_reviewed=139,chapter_counts=dict(collections.Counter(x['chapter'] for x in rows)),checks=['UTF-8 BOM和八字段','ID连续唯一及一一来源映射','必填正文非空','全部139页原图与双页核对图存在','图片独立行、标签与文件页号一致、同字段路径去重','记录页码对应源页和图片','原PDF SHA256未变','关键公式、实验用量、反应条件与科学计数法回归检查','完整正文回读与图源视觉核对；复杂二维结构及表格保留原图'],limitations=['网站目录映射不含标题字符串，具体名称核验状态见outline_alignment.json。','程序检查不独立证明原文忠实性；视觉核对与片段排除依据另附。']))
print(json.dumps({'records':len(rows),'pages':139,'validation':'passed'},ensure_ascii=False))
