"""Build provenance, page audit and independent package validation for this book."""
from pathlib import Path
import json,csv,re,hashlib,collections
R=Path(__file__).resolve().parents[1]
SLUG='chemistry-pep-hs-selective-1'
def save(n,o):(R/n).write_text(json.dumps(o,ensure_ascii=False,indent=2))
S=json.loads((R/'selection.json').read_text());report=json.loads((R/'source_report.json').read_text())
rows=list(csv.DictReader((R/'knowledge_points.csv').open(encoding='utf-8-sig')))
sources=[json.loads(x) for x in (R/'source_records.jsonl').read_text().splitlines()]
report.update(curriculum_revision='依据《普通高中化学课程标准（2017年版）》编写；2019年审核通过',curriculum_evidence_pages=[1,134],isbn='978-7-107-34602-6',isbn_evidence_page=139,edition_printing_status='版权页未提供可确认的版次、印次日期，不推断',local_md5=hashlib.md5(Path(report['source_pdf']).read_bytes()).hexdigest())
save('source_report.json',report)
titles={8:'第一章 化学反应的热效应',9:'第一节 反应热',19:'第二节 反应热的计算',25:'整理与提升',28:'第二章 化学反应速率与化学平衡',29:'第一节 化学反应速率',37:'第二节 化学平衡',48:'第三节 化学反应的方向',51:'第四节 化学反应的调控',57:'整理与提升',60:'实验活动1 探究影响化学平衡移动的因素',62:'第三章 水溶液中的离子反应与平衡',63:'第一节 电离平衡',68:'第二节 水的电离和溶液的pH',76:'第三节 盐类的水解',84:'第四节 沉淀溶解平衡',93:'整理与提升',96:'实验活动2 强酸与强碱的中和滴定',99:'实验活动3 盐类水解的应用',100:'第四章 化学反应与电能',101:'第一节 原电池',109:'第二节 电解池',116:'第三节 金属的腐蚀与防护',123:'整理与提升',127:'实验活动4 简单的电镀实验',128:'实验活动5 制作简单的燃料电池'}
web=json.loads((R/'website/ebook_mapping.json').read_text())
resource=json.loads((R/'website-resource.json').read_text())
source=next(x for x in resource['ti_items'] if x.get('ti_is_source_file'))
assert source['ti_size']==report['file_bytes']==12241298
nodes=[]
for n in web['mappings']:
 nodes.append(dict(n,depth=n['node_path'].count('/'),pdf_title=titles[n['page_number']],website_title_status='mapping未返回标题字段，名称取同资源PDF目录及起始页',title_evidence='PDF P4-P5及对应起始页视觉核对'))
save('outline_alignment.json',dict(resource_id=report['resource_id'],website_resource_title=resource['title'],resource_url='https://basic.smartedu.cn/tchMaterial/detail?contentType=assets_document&contentId='+report['resource_id'],resource_metadata_url='https://s-file-1.ykt.cbern.com.cn/zxx/ndrv2/resources/tch_material/details/'+report['resource_id']+'.json',identity_evidence=['资源ID与指定文件名一致','源PDF大小12241298字节与本地一致','全书139个物理页，网站目录起始页与本地目录/正文逐项对应','书名、册次、审核年、封底ISBN由本地原图确认'],sha256=report['sha256'],local_md5=report['local_md5'],website_source_ti_md5=source['ti_md5'],hash_comparison='ti_md5带-2后缀，为分段对象标识；不将其当作本地文件MD5，不宣称远端与本地逐字节相同',nodes=nodes,ordering='章节、小节按网站同资源目录节点路径和物理页顺序；知识点依据教材正文细分。正文小标题、附录及章引言由原页补充，未虚构网站节点。',limitations=['网站ebook_mapping不含标题字符串，不能据此声称逐字核验网站末级名称。具体标题来自同资源PDF目录。']))
by_page=collections.defaultdict(list)
for row,src,s in zip(rows,sources,S):
 src.update(chapter=row['chapter'],subchapter=row['subchapter'],section=row['section'],knowledge_point=row['knowledge_point'],image_placement='完整合并跨页、跨栏句段后附图；同记录同字段同整页路径只出现一次',content_boundary='regions为候选定位范围；最终选取片段以selection.detail/selection.example为准；整页图片包含的其他内容不表示录入该记录',visual_status='reviewed')
 for p in set(src['image_pages']+src.get('example_pages',[])):by_page[p].append(row['knowledge_point_id'])
(R/'source_records.jsonl').write_text(''.join(json.dumps(x,ensure_ascii=False)+'\n' for x in sources))
roles={1:'封面、2019审核标记',2:'扉页',3:'编写及出版信息',4:'目录',5:'目录',8:'第一章章引言',28:'第二章章引言',62:'第三章章引言',100:'第四章章引言：电化学基础',129:'燃烧热附录',130:'电离常数附录',131:'溶度积附录',132:'名词索引',133:'空白页',134:'后记、2017年版课程标准证据',135:'空白页',136:'图片来源致谢',137:'空白页',138:'元素周期表',139:'封底、ISBN'}
exercise={17,18,24,26,27,36,46,47,50,56,58,59,67,75,83,92,94,95,107,108,115,122,124,125,126}
review={25,57,93,123};tasks={91:'了解水处理过程中的化学原理：资料查阅和报告任务',121:'暖贴的设计与制作：资料收集、设计、评价任务'}
# Specific editorial decisions supplement the page-level coverage record.
fragments=[
(6,'引言','保留键变化、物质能量与代谢的概念；宏观微观研究和一般评价不单列'),
(9,'热量及反应热','补入放热/吸热分类；等温脚注明确反应后恢复温度，不改成反应中温度恒定'),
(10,'中和热实验','保留全部给定步骤与空表；不填写温度差、放热量空格'),
(15,'燃烧热脚注','保留C、H、S、N的指定产物和物态'),
(21,'热化学研究的先驱','保留冰量热计按熔冰质量计算热量的方法；人物年代评价排除'),
(22,'例题1、例题2','例题1首次质量/物质的量/热量计算完整保留；例题2葡萄糖只替换物质与数值，同类计算不重复录入'),
(23,'例题3','盖斯定律代数组合法与前例方法不同，完整保留题干、反应式和原解'),
(31,'速率探究','给定实验用品、定量锌硫酸步骤保留；自拟定性方案和空表不补答案'),
(34,'催化作用','保留酶催化和改变历程/活化能的讲解，删除获奖与评价片段'),
(35,'飞秒化学','保留时间分辨技术、ICN实验测值和H·反应过渡态；人物年代奖项排除'),
(38,'表2-1','表格跨P38-P39，六组完整数据与平均值保留'),
(40,'平衡计算','例题1为核心讲解留detail；P40-P41例题2为不同条件的转化率补充原例，放example'),
(42,'浓度实验','不补空表现象；仅保留教材明示颜色标签和组成发生变化的结论'),
(43,'压强实验','先变浅后变深、先变深后变浅分别保留，避免删除即时与后续必要对比'),
(49,'熵与方向','熵增/熵减反例及孤立/绝热条件保留；末尾跨页句先合并'),
(50,'自由能','完整保留等温、等压、封闭体系、仅体积变化功限制及ΔG三种判据'),
(54,'合成氨史话','保留换热、低温分离循环等具体技术；人物、年代、获奖和宏观评价排除'),
(55,'合成氨史话续','保留锇催化条件、水煤气及液化空气原料来源、350℃和1MPa新条件；研发任务指标排除'),
(60,'实验活动1','与正文实验用量、操作有区别，保留完整给定器材、药品及步骤；空白结果不补'),
(63,'强弱电解质实验','保留给定比较条件，明示结果按正文；不逐项填写空表'),
(66,'实验3-2与思考讨论','醋酸加Na2CO3给定步骤保留；Ka大小推测题、镁与酸压强曲线未解讨论不作为答案'),
(70,'pH试纸和pH计','量程、分辨率照教材保留；图片仅作原页依据'),
(71,'应用与作物表','作物适宜pH表、土壤养分图保留原图，不用外部数据补充'),
(73,'中和滴定','指示剂范围侧栏按位置归入本节；完整计算例题跨P73-P74合并留detail'),
(76,'盐溶液酸碱性探究','自选测试方法及原表空格不补；P77正文给出的归纳结论保留'),
(77,'离子相互作用讨论','未解表格不填，随后NH4Cl水解完整讲解保留'),
(80,'水解平衡探究','给定用品和Fe(OH)3弱碱、难溶提示保留；不创造实验方案和现象'),
(88,'沉淀转化实验','两种转化方法均保留；只录图示与后文已给结论，不填空表'),
(90,'氟化物防龋','保留反应、溶解度比较及原书高氟地区/6岁以下限制'),
(96,'中和滴定实验','构造、检漏、润洗、加液、调零及聚四氟乙烯活塞脚注保留'),
(98,'滴定问题讨论','未解问题及待绘制曲线任务不录入知识正文'),
(99,'水解应用实验','保留给定四组操作，未给现象不补；胶体制备红褐色为明示步骤终点'),
(101,'锌铜原电池','保留盐桥组成脚注和取出盐桥的现象；未解绘图任务不作答'),
(106,'化学电源史话','人物历史评价排除；首讲之外的历史验电经历不作重复原电池结论'),
(109,'电解池','阳极/阴极命名脚注以及本例水电离离子未参与电极反应的限制保留'),
(114,'电解与元素发现','混合历史表只保留电解、还原制单质的具体方法及条件；人物年代奖项删除'),
(117,'腐蚀实验','两组给定对照实验步骤保留；不补观察答案'),
(118,'白铁皮与马口铁讨论','未解破损腐蚀比较不补答案，正文防护方法完整保留'),
(119,'牺牲阳极实验','保留3%NaCl酸化、Fe/Zn、琼脂/盐水/酚酞/铁氰化钾用量及培养皿对照，空表不填'),
(120,'铁氰化钾检验','依教材原式转录，不以外部配合物反应写法替换'),
(127,'电镀实验','保留2～3V、5cm、5～10min及铜氨溶液脚注；未解反接问题不填'),
(128,'燃料电池实验','保留烘干活化、3～6V、1mol/L Na2SO4、K1/K2切换和时间，不补未给的电流及颜色结果'),
(129,'附录数据','整体作为参考数据表保留，不拆成同类型知识点；与正文已引数据的重合用于维持完整表格'),
(132,'名词索引','仅导航，已有知识不重复录入'),
(138,'元素周期表','完整数据以原图保留；不以乱码OCR猜测电子排布或质量数')]
exclusions=[dict(pdf_page=p,scope=scope,decision=reason) for p,scope,reason in fragments]
audit=[]
for p in range(1,140):
 role=roles.get(p,'正文、实验或侧栏')
 if p in exercise:role='练习/复习题'+('及同页正文' if by_page[p] else '')
 if p in review:role='整理与提升：重复知识与待填图表'
 if p in tasks:role=tasks[p]
 why='选取正文、给定实验方法、明示现象/结论及有效侧栏；其余未解练习、任务指标、历史评价或重复表述排除。' if by_page[p] else role+'；不新增完整知识讲解，或知识已在首讲收录。'
 if not by_page[p]:exclusions.append(dict(pdf_page=p,scope='whole_page',decision=why))
 first=p if p%2 else p-1
 audit.append(dict(pdf_page=p,printed_page=p-5 if 6<=p<=132 else None,page_image=f'images/{SLUG}/page-{p:03}.png',review_image=f'review/pages-{first:03}-{min(first+1,139):03}.jpg',visual_status='reviewed',role=role,record_ids=by_page[p],checks=['公式及上下标、电荷、箭头、单位','表格、图示、明示条件','跨页、跨栏句段及记录边界'],decision=why))
save('visual_audit.json',dict(total_pages=139,reviewed_pages=139,method='逐物理页查看渲染图，文字层只作候选；对转录中的分式、指数、电荷、实验数量及跨页句再次核对',pages=audit))
save('page_map.json',audit);save('exclusions.json',exclusions)
save('id_map.json',[dict(old_id=None,new_id=x['knowledge_point_id'],knowledge_point=x['knowledge_point'],reason='新分册首次抽取，按教材顺序连续编号') for x in rows])
save('changes.json',dict(action='initial_full_book_extraction',source_sha256=report['sha256'],records=len(rows),existing_book_outputs_modified=False,before=[],after=rows,reason='独立新增分册；依教材细分、合并跨页文字、视觉校正公式、同类型例题去重，原书未给结果不补。',recovery='selection.json保存完整选区及核定正文，运行scripts/build.py和scripts/package_audit.py重建；早期select/correct脚本仅为过程记录，不重复运行。'))
fields=['knowledge_point_id','chapter','subchapter','section','knowledge_point','detail','example','pdf_page']
assert len(rows)==len(S)==len(sources)==103
assert list(rows[0])==fields and (R/'knowledge_points.csv').read_bytes().startswith(b'\xef\xbb\xbf')
assert [x['knowledge_point_id'] for x in rows]==[f'RJ-CHEMISTRY-HSS1-{i:03}' for i in range(1,len(rows)+1)]
assert len({x['knowledge_point'] for x in rows})==len(rows)
def pset(label):
 out=set()
 for z in label.split(';'):
  nums=[int(t) for t in re.findall(r'\d+',z)]
  out.update(range(nums[0],nums[-1]+1))
 return out
for row,src,s in zip(rows,sources,S):
 assert all(row[k].strip() for k in fields if k!='example')
 assert not any(ord(c)<32 and c not in '\n\r\t' for c in row['detail']+row['example'])
 assert src['knowledge_point_id']==row['knowledge_point_id']
 allps=set()
 for field in ['detail','example']:
  refs=re.findall(r'!\[page-(\d{3})\]\((images/[^)]+)\)',row[field]);paths=[v for _,v in refs]
  assert len(paths)==len(set(paths))
  for pn,path in refs:
   assert path==f'images/{SLUG}/page-{pn}.png' and (R/path).is_file()
   allps.add(int(pn))
  for line in row[field].splitlines():
   if '![' in line:assert re.fullmatch(r'!\[page-\d{3}\]\(images/'+SLUG+r'/page-\d{3}\.png\)',line)
 assert allps==pset(row['pdf_page'])
 assert allps==set(src['image_pages']+src.get('example_pages',[]))
 assert all(1<=reg[0]<=139 for reg in src['regions'])
assert len(audit)==139 and all((R/x['page_image']).is_file() and (R/x['review_image']).is_file() for x in audit)
assert hashlib.sha256(Path(report['source_pdf']).read_bytes()).hexdigest()==report['sha256']
terms={'水的电离和离子积常数':['0.115','54.5','1×10⁻¹⁴'],'自由能与化学反应的方向':['等温','等压','封闭','ΔG>0'],'中和滴定的数据处理与浓度计算':['27.84','27.83','27.85','0.114 9'],'牺牲阳极法的实验':['3%','50 mL','150 mL','250 mL','5~6'],'铁制镀件上镀铜的实验':['2~3 V','5 cm','5~10 min'],'化学反应速率的表示、计量数关系与计算':['0.02','0.06','0.04','v(A)/m'],'浓度商、化学平衡常数及反应限度':['457.6','48.70','10⁵'],'某些弱电解质的电离常数数据':['4.8×10⁻¹³','1.75×10⁻⁵']}
lookup={x['knowledge_point']:x for x in rows}
for n,tt in terms.items():assert all(t in lookup[n]['detail'] for t in tt),(n,tt)
# Markdown is generated from exactly the same field bodies.
md=['# 人教版高中化学选择性必修1 化学反应原理\n\n全书103条记录。教材身份、来源及核验范围见 [README](README.md)。\n']
for x in rows:
 md.append(f"## {x['knowledge_point_id']} {x['knowledge_point']}\n\n{x['chapter']} / {x['subchapter']} / {x['section']} · {x['pdf_page']}\n\n{x['detail']}\n")
 if x['example']:md.append('### 补充原例与原解\n\n'+x['example'])
(R/'knowledge_points.md').write_text('\n'.join(md))
save('validation.json',dict(status='passed',records=103,pdf_pages=139,images=139,visually_reviewed_pages=139,chapter_counts=dict(collections.Counter(x['chapter'] for x in rows)),checks=['UTF-8 BOM及固定八字段','ID连续、唯一、来源一一映射','必填字段及控制字符检查','全部139页原图及逐页核对图存在','图片独立行、页标签与文件一致、同字段路径无重复','pdf_page与detail/example源页及图片集合一致','源PDF SHA-256未改变','关键公式、实验用量与条件回归检查','CSV与Markdown正文一致；视觉逐页记录见visual_audit.json'],limitations=['目录映射不返回标题字符串，具体名称取同资源PDF目录；不虚构网站标题核验。','程序检查不替代原文忠实性的视觉核对；复杂二维示意和元素周期表以原图保留。']))
print(json.dumps({'records':len(rows),'pages':139,'validation':'passed'},ensure_ascii=False))
