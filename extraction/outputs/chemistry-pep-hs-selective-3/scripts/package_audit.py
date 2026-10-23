"""Write provenance, visual-page decisions, identity alignment and package checks."""
from pathlib import Path
import json,csv,re,hashlib,collections
R=Path(__file__).resolve().parents[1];SLUG='chemistry-pep-hs-selective-3'
def save(n,x):(R/n).write_text(json.dumps(x,ensure_ascii=False,indent=2))
S=json.loads((R/'selection.json').read_text());rows=list(csv.DictReader((R/'knowledge_points.csv').open(encoding='utf-8-sig')));srcs=[json.loads(x) for x in (R/'source_records.jsonl').read_text().splitlines()];report=json.loads((R/'source_report.json').read_text());pdf=Path(report['source_pdf'])
report.update(curriculum_revision='依据《普通高中化学课程标准（2017年版）》编写；2019年审核通过',curriculum_evidence_pages=[1,160],isbn='978-7-107-34604-0',isbn_evidence_page=163,edition_printing_status='PDF未见可确认的版次、印次日期；不从文件名推断',local_md5=hashlib.md5(pdf.read_bytes()).hexdigest())
save('source_report.json',report)
titles={6:'引言',8:'第一章 有机化合物的结构特点与研究方法',9:'第一节 有机化合物的结构特点',18:'第二节 研究有机化合物的一般方法',28:'整理与提升',32:'第二章 烃',33:'第一节 烷烃',39:'第二节 烯烃 炔烃',48:'第三节 芳香烃',55:'整理与提升',58:'第三章 烃的衍生物',59:'第一节 卤代烃',64:'第二节 醇 酚',73:'第三节 醛 酮',78:'第四节 羧酸 羧酸衍生物',89:'第五节 有机合成',98:'整理与提升',103:'实验活动1 乙酸乙酯的制备与性质',104:'实验活动2 有机化合物中常见官能团的检验',106:'第四章 生物大分子',107:'第一节 糖类',117:'第二节 蛋白质',127:'第三节 核酸',132:'整理与提升',135:'实验活动3 糖类的性质',136:'第五章 合成高分子',137:'第一节 合成高分子的基本方法',141:'第二节 高分子材料',157:'整理与提升'}
web=json.loads((R/'website/ebook_mapping.json').read_text());res=json.loads((R/'website-resource.json').read_text());source=next(x for x in res['ti_items'] if x.get('ti_is_source_file'));assert source['ti_size']==report['file_bytes']==22093382
nodes=[]
for n in web['mappings']:
 p=n['page_number'];assert p in titles;nodes.append(dict(n,depth=n['node_path'].count('/'),pdf_title=titles[p],alignment_status='网站同资源节点的层级与物理起始页对应本地PDF目录及正文',website_title_status='接口未返回标题字符串；名称以本PDF目录及正文转录',title_evidence_pages=[4,5,p]))
assert len(nodes)==29
save('outline_alignment.json',dict(resource_id=report['resource_id'],website_resource_title=res['title'],resource_url='https://basic.smartedu.cn/tchMaterial/detail?contentType=assets_document&contentId='+report['resource_id'],resource_metadata_url='https://s-file-1.ykt.cbern.com.cn/zxx/ndrv2/resources/tch_material/details/'+report['resource_id']+'.json',identity_evidence=['指定PDF文件名资源UUID与网站资源一致','网站源文件大小与本地PDF均22093382字节','29节点均有物理起始页，逐项对应本地目录及正文','2019审核见P1；2017年版课标依据见P160；封底ISBN见P163'],sha256=report['sha256'],local_md5=report['local_md5'],website_source_ti_md5=source['ti_md5'],hash_comparison='ti_md5含-3后缀，为对象标识；不作本地MD5等值断言，也不声称逐字节验证远端PDF',nodes=nodes,ordering='网站同资源实际节点层级与起始页确定章、节顺序；节内按教材具体知识和侧栏原位细分。',limitations=['ebook_mapping接口没有标题字符串，无法逐字符核对网站目录标题；同资源PDF提供标题名称。','版次、印次日期未确认，不使用其他教材补齐。']))
by=collections.defaultdict(list)
for row,src,s in zip(rows,srcs,S):
 src.update(chapter=row['chapter'],subchapter=row['subchapter'],section=row['section'],knowledge_point=row['knowledge_point'],image_placement='完整合并跨页跨栏句段后统一附图；同记录同字段同整页路径一次',content_boundary='regions为文字候选或图示定位；selection.detail是最终核定正文。整页图中的未解题、历史或其他知识不表示纳入本条正文。',visual_status='reviewed')
 for p in src['image_pages']+src.get('example_pages',[]):by[p].append(row['knowledge_point_id'])
(R/'source_records.jsonl').write_text(''.join(json.dumps(x,ensure_ascii=False)+'\n' for x in srcs))
roles={1:'封面、书名与2019审核',2:'编写人员',3:'书名与出版信息',4:'目录',5:'目录',6:'引言',7:'引言及有效合成知识',8:'第一章章引言',32:'第二章章引言',58:'第三章章引言',106:'第四章章引言',136:'第五章章引言',159:'名词索引',160:'后记及课标依据',161:'图片来源致谢',162:'元素周期表',163:'封底与ISBN'}
reviews={28,29,30,55,98,99,132,157}
exercises={17,27,30,31,37,38,40,46,47,54,56,57,63,72,77,80,87,88,92,95,97,100,101,102,105,111,112,115,116,118,122,125,126,128,130,131,133,134,140,146,150,152,153,154,155,156,158}
frags={7:'保留碳骨架、官能团和分析仪器知识；一般愿景与评价排除。',9:'碳骨架分类图保留，不按分类树每个代表物另造重复记录。',10:'表1-1各类别、官能团和代表物以表格与原图保留。',12:'实验1-1的用量、反应程度和明示H₂结论保留。',13:'戊烷实验空表与模型制作任务不填写；同分异构说明保留。',14:'表1-2分类与给定结构原例保留。',15:'键线式、跨页表1-2和碳价四面体的必要对比保留；纯历史评价排除。',16:'保留对映异构及两模型对比，人物奖项评价排除。',19:'苯甲酸粗品杂质、数据表、溶剂条件保留。',20:'重结晶用品步骤与收率式保留，现象和质量空表不填。',21:'色谱定义与植物色素分离方法保留；年代人物与获奖排除。',22:'元素分析的完整已解原例在detail，分式不按文字层乱序转录。',23:'质谱分子离子46与两候选结构、红外光谱跨页说明保留。',24:'红外峰和核磁3∶2∶1解释、δ脚注保留。',25:'X射线10⁻¹⁰ m、青蒿素有效分析方法保留。',26:'青蒿素测定方法续文保留，历史奖项评价排除。',35:'表2-1甲烷/乙烷不同温度密度脚注保留。',36:'支链异构沸点对比与系统命名四步保留。',37:'系统命名首讲结构和2,3-二甲基己烷保留；未解枚举表不填。',38:'题8给定伯仲叔季碳定义及已给n₁～n₄例保留，其后氢原子关系式空格不填。',40:'顺反异构的给定讲解保留；让读者解释的练习不补解。',41:'顺反物理数据与二烯烃1,2/1,4两种条件相关竞争反应保留。',42:'乙炔结构、制法和除杂条件保留。',43:'乙炔探究完整给定操作和装置保留；预测、空记录表及问题不答。',44:'分步溴加成、H₂/HCl/H₂O加成、乙烯醇不稳定脚注、聚乙炔及氧炔焰保留；发展史排除。',45:'导电聚合物的掺杂、共轭通路及应用保留，奖项历史排除。',46:'研究与实践均为自拟设计、指标和成果任务，不新增知识。',49:'苯σ键、大π键与取代反应保留。',50:'硝化、加氢、磺化不同条件保留；表示式的必要结构对比保留。',51:'表2-2与实验2-2对比步骤保留。',52:'续实验空现象解释不填；甲基/苯环相互影响与TNT明示性质保留。',53:'稠环芳香烃、萘蒽有效补充保留。',60:'水解实验的水层、酸化、浅黄AgBr明示结论及氯乙烷侧栏保留。',61:'消去与水解条件区别、1-溴丁烷不同用量实验保留，空表不填。',62:'PTFE、卤代烃用途与氟利昂/臭氧反应保留；历史评价排除。',65:'醇的两表数据与氢键跨页解释保留。',66:'浓氢溴酸取代、乙醇消去实验跨页完整合并。',67:'170/140℃不同反应、醚定义与氧化实验保留。',68:'有机氧化还原、代谢两种酶、苯酚物理性质和条件保留。',69:'苯酚酸性实验步骤与明示解释保留，空表不填。',70:'通CO₂酸性比较和三溴苯酚实验保留。',71:'FeCl₃显色与废水、消毒有效性质保留，人物年代排除。',73:'羰基、醛基、乙醛结构及跨页加氢完整。',74:'银镜与新制氢氧化铜实验用量、HCN加成方向提示保留。',75:'银镜和Cu₂O方程式、催化氧化与甲醛苯甲醛性质保留。',76:'桂皮/杏仁醛、酮和丙酮有效内容保留，不答搜索任务。',78:'羧酸分类、甲酸双功能结构、乙二酸跨页句完整。',79:'羧酸物理表、羟基酸及羧基断键位置保留。',80:'给定弱酸性说明保留，自拟验证酸性实验任务不新增或作答。',81:'酯化氧同位素示踪原式、酯定义及跨页天然酯实例完整。',82:'酯水解的给定酸碱条件与空设计表区分，不填后者。',83:'油脂组成原图和油/脂肪状态定义保留。',84:'皂化与硬化不同反应原式保留。',85:'顺式脂肪酸、反式风险限定及胺定义脚注保留。',86:'酰胺结构及取代氨基脚注、酸碱水解原式保留。',87:'仅录给定皂化/盐析/洗涤/成形工序和洗涤剂组成，排除自制、搜索、报告任务。',89:'碳骨架增长、缩短与HCN官能团转化原式保留。',90:'羟醛缩合和环加成的有效补充保留。',91:'引入、保护官能团与正向路线设计跨页完整。',92:'正向与逆合成分析给定方法保留；计算产率未解题不作答。',93:'乙二酸二乙酯首讲分析连同原结构式在detail。',94:'完整五步合成及各条件、最佳路线选择依据留在detail。',95:'未解合成路线讨论和收集资料、报告任务不作答。',96:'实验室装置的操作能力与工业小试中试有效说明保留。',103:'实验活动1完整用品与定量操作，导管0.5cm、先取下接收管、70～80℃、三管等总液量不漏，不补气味变化结果。',104:'实验活动2完整用品与不同配比1-己烯/1-溴丁烷步骤保留；苯酚醛基同法已首讲，不重复；空表现象和方程式不填。',105:'阿司匹林样品处理及羧基/酯基检验，NaHCO₃中和硫酸脚注保留，未解谱图不补。',107:'单/寡/多糖边界、通式例外与缩合脚注保留。',108:'葡萄糖原实验、银镜/砖红现象、五羟基醛糖和酶氧化原式保留。',109:'环链平衡、果糖、戊糖和手性跨栏跨页完整。',110:'手性续文、蔗糖、麦芽糖跨页完整。',111:'乳糖有效侧栏保留，蔗糖麦芽糖自行设计与空结果表不填。',112:'甜味剂正文和三结构式保留；搜索问题排除；多糖组成保留。',113:'淀粉结构性质应用及纤维素实验保留，不补实验4-2未给现象。',114:'纤维素续文、衍生物与甲壳质/壳聚糖有效侧栏保留。',115:'纤维素制乙醇给定流程及5吨/1吨保留；产业评价和未解练习排除。',117:'蛋白质功能、氨基酸定义、21/8种照原书、α结构及给定五结构原图保留。',118:'两性与成肽原式保留；味精成分有效，历史/搜索任务排除。',119:'肽链续文、蛋白质各级结构和氮含量16%、6.25倍测定保留。',120:'蛋白质两性、水解和盐析实验跨页完整。',121:'盐析可逆和变性不可逆的区别、全实验和影响因素保留。',122:'蛋白质显色实验和胰岛素双链结构有效片段保留；历史评价排除。',123:'胰岛素原结构图及烫发的二硫键/巯基知识保留；发现史不录。',124:'酶定义、高效10⁷、温和条件与专一性保留。',125:'大豆调查、研究目的与报告任务不录。',127:'核酸组成、核苷定义脚注、戊糖环式脚注和原图保留。',128:'核酸基本单元、ATP侧栏跨栏跨页完整；指认任务不作答。',129:'ATP水解能量转换与DNA双螺旋跨页讲解保留；发现史排除。',130:'碱基配对、RNA、基因与复制给定内容保留；未解类比不填。',131:'PCR有效知识保留；人类基因组历史评价与练习排除。',135:'完整用品与蔗糖/淀粉水解前后新条件保留；同法葡萄糖原实验不重复；不补还原糖判断及结果。',137:'高分子10⁴、平均量、单体链节聚合度和PVC原式保留。',138:'己二酸/乙二醇缩聚首讲、端基与副产物条件跨页完整。',139:'n−1/2n−1不同单体条件和两原式保留；施陶丁格纯史话与重复概念排除。',141:'材料分类、助剂和热塑/热固定义保留。',142:'PVC增塑原理，聚乙烯两条件全表和引发剂脚注保留。',143:'链卷曲、支链及分子间作用力原因、图示与跨页用途保留。',144:'命名、降解的有效侧栏保留；聚乳酸复杂结构以图保留。',145:'CO₂稀土催化有效工艺保留，发展评价排除；酚醛实验定量步骤和酸催化过程保留。',146:'碱催化酚醛、网状结构与纤维分类保留；脲醛未解方程式不填写。',147:'纤维性能与混纺、涤纶的完整合成原式保留；人物年代排除。',148:'锦纶66/6/1010的区别与芳纶1414结构原式、500℃与1/5条件保留。',149:'顺丁橡胶、硫化原理与交联不宜过大条件保留。',150:'天然顺式聚异戊二烯与杜仲胶反式区别、性能用途保留，不补杜仲胶结构题。',151:'功能材料及高吸水树脂两条思路、交联与亲水基团保留。',152:'吸水对比实验、1g/70mL/100mL/5min与吸水率保留，数据空表不补。',153:'探究空结论不填，分离膜正文与四类膜原图保留。',154:'海水淡化资料检索、报告任务排除。',157:'整理框架与待填表均已首讲或未给答案，不重复。',158:'复习题及已知条件属于未解任务，不答题、不独立拆出答案。',159:'名词索引为导航，不重复抽取。',162:'参考元素周期表原图保留为核查附件，不按逐元素新增重复知识。'}
audit=[];excluded=[]
for p in range(1,164):
 role=roles.get(p,'正文、实验和侧栏')
 if p in reviews:role='整理与提升及同页讲解或练习'
 if p in exercises:role+='；含未解题或研究任务'
 decision=frags.get(p,'保留教材给定的核心讲解及有效图表；未解练习、任务指标、纯历史评价和重复片段排除。' if by[p] else '本页无新增知识正文；身份信息、目录、致谢或未解/重复内容按页性质排除。')
 first=p if p%2 else p-1
 audit.append(dict(pdf_page=p,printed_page=p-5 if 6<=p<=159 else None,page_image=f'images/{SLUG}/page-{p:03}.png',review_image=f'review/pages-{first:03}-{min(first+1,163):03}.jpg',visual_status='reviewed',role=role,record_ids=by[p],checks=['公式、结构式、上下标、电荷、箭头','单位、表格、图示与明示条件','跨页跨栏完整性与实验结果边界'],decision=decision))
 if not by[p] or p in frags or p in exercises or p in reviews:excluded.append(dict(pdf_page=p,scope='whole_page' if not by[p] else 'fragments',decision=decision))
save('visual_audit.json',dict(total_pages=163,reviewed_pages=163,method='逐物理页查看渲染图；文字层仅候选；逐条回读校正上下标、结构式、表格及跨栏；复杂二维原式和图示由对应整页图完整保留。',pages=audit));save('page_map.json',audit);save('exclusions.json',excluded)
draft=json.loads((R/'draft_order.json').read_text());dmap={x['name']:x['draft_position'] for x in draft}
save('id_map.json',[dict(old_id=None,new_id=x['knowledge_point_id'],draft_position=dmap.get(x['knowledge_point']),knowledge_point=x['knowledge_point'],reason='新分册首次抽取；最终教材顺序编号，未替换已发布ID') for x in rows])
save('changes.json',dict(action='initial_full_book_extraction',source_sha256=report['sha256'],records=len(rows),before=[],after=rows,existing_book_outputs_modified=False,reason='独立新增有机化学基础分册；教材内细分，完整保留核心首讲，复杂结构式原图核查，合并跨页跨栏，排除无解任务、纯历史评价与重复片段。',recovery='selection.json冻结最终核定正文及选区。只运行scripts/build.py和scripts/package_audit.py重建；select/correct/finalize脚本是一次性过程记录，不重跑。'))
fields=['knowledge_point_id','chapter','subchapter','section','knowledge_point','detail','example','pdf_page']
assert len(rows)==len(S)==len(srcs)==153
assert list(rows[0])==fields and (R/'knowledge_points.csv').read_bytes().startswith(b'\xef\xbb\xbf')
assert [r['knowledge_point_id'] for r in rows]==[f'RJ-CHEMISTRY-HSS3-{i:03}' for i in range(1,154)]
assert len({r['knowledge_point'] for r in rows})==153
for row,src in zip(rows,srcs):
 assert all(row[f].strip() for f in fields if f!='example')
 assert row['knowledge_point_id']==src['knowledge_point_id'];pages=set()
 assert not any(ord(c)<32 and c not in '\n\r\t' for c in row['detail']+row['example'])
 for field in ['detail','example']:
  refs=re.findall(r'!\[page-(\d{3})\]\((images/[^)]+)\)',row[field]);assert len(refs)==len(set(path for _,path in refs))
  for pn,path in refs:assert path==f'images/{SLUG}/page-{pn}.png' and (R/path).is_file();pages.add(int(pn))
  for ln in row[field].splitlines():
   if '![' in ln:assert re.fullmatch(r'!\[page-\d{3}\]\(images/'+SLUG+r'/page-\d{3}\.png\)',ln)
 qs=set()
 for group in row['pdf_page'].split(';'):
  ns=list(map(int,re.findall(r'\d+',group)));qs.update(range(ns[0],ns[-1]+1))
 assert pages==qs==set(src['image_pages']+src.get('example_pages',[]))
 assert all(1<=a[0]<=163 for a in src['regions'])
assert len(audit)==163 and all((R/a['page_image']).is_file() and (R/a['review_image']).is_file() for a in audit)
assert hashlib.sha256(pdf.read_bytes()).hexdigest()==report['sha256']
byname={r['knowledge_point']:r['detail'] for r in rows}
terms={'酶的催化作用、条件与专一性':['10⁷','专一性'],'乙醇消去制乙烯与分子间脱水制乙醚':['170','140'],'乙二酸二乙酯的逆合成分析与五步合成原例':['2O₂','加压','2NaOH'],'ATP的组成、水解及能量转换':['磷酸酐键','ADP和AMP'],'阿司匹林中羧基与酯基的检验实验':['中和过量的硫酸','2 mL'],'高压法与低压法聚乙烯的结构、性能和用途':['150～300 MPa','0.1～2 MPa','10⁶'],'高吸水性树脂与一般材料吸水性能对比实验':['70 mL','5 min','(m₂−m₁)/m₁']}
for n,tt in terms.items():assert all(t in byname[n] for t in tt),(n,tt)
md=['# 人教版高中化学选择性必修3 有机化学基础\n\n全书153条记录。教材身份、来源及核验说明见 [README](README.md)。\n']
for x in rows:
 md.append(f"## {x['knowledge_point_id']} {x['knowledge_point']}\n\n{x['chapter']} / {x['subchapter']} / {x['section']} · {x['pdf_page']}\n\n{x['detail']}\n")
 if x['example']:md.append('### 补充原例与原解\n\n'+x['example'])
(R/'knowledge_points.md').write_text('\n'.join(md))
save('validation.json',dict(status='passed',records=153,pdf_pages=163,images=163,visually_reviewed_pages=163,website_nodes=29,chapter_counts=dict(collections.Counter(r['chapter'] for r in rows)),checks=['UTF-8 BOM及八字段','连续唯一ID、名称与来源映射','必填及控制字符','163页原图与核对图存在','图片独立行及同字段路径唯一','源页集合、页标签与图像一致','源PDF SHA-256未改变','关键公式与实验条件检查','CSV与Markdown同源'],limitations=['网站目录节点返回层级与页码，没有标题字符串；名称据同资源PDF，不声称逐字网站标题对齐。','版次印次日期未确认。','程序检查只验证结构；复杂二维公式和图示依所附教材原图，不能将程序通过等同原文核验。']))
print('153 records; 163 pages; package checks passed')
