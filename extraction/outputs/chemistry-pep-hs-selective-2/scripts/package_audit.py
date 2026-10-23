"""Provenance, editorial decisions, page coverage, and structural validation."""
from pathlib import Path
import json,csv,re,hashlib,collections
R=Path(__file__).resolve().parents[1];SLUG='chemistry-pep-hs-selective-2'
def save(n,o):(R/n).write_text(json.dumps(o,ensure_ascii=False,indent=2))
S=json.loads((R/'selection.json').read_text());report=json.loads((R/'source_report.json').read_text());rows=list(csv.DictReader((R/'knowledge_points.csv').open(encoding='utf-8-sig')));sources=[json.loads(x) for x in (R/'source_records.jsonl').read_text().splitlines()]
report.update(curriculum_revision='依据《普通高中化学课程标准（2017年版）》编写；2019年审核通过',curriculum_evidence_pages=[1,110],isbn='978-7-107-34603-3',isbn_evidence_page=115,edition_printing_status='未找到可确认的版次、印次日期；不从文件名推断',local_md5=hashlib.md5(Path(report['source_pdf']).read_bytes()).hexdigest())
save('source_report.json',report)
titles={8:'第一章 原子结构与性质',9:'第一节 原子结构',21:'第二节 原子结构与元素的性质',33:'整理与提升',36:'第二章 分子结构与性质',37:'第一节 共价键',44:'第二节 分子的空间结构',55:'第三节 分子结构与物质的性质',70:'第三章 晶体结构与性质',71:'第一节 物质的聚集状态与晶体的常识',81:'第二节 分子晶体与共价晶体',89:'第三节 金属晶体与离子晶体',98:'第四节 配合物与超分子',104:'整理与提升',107:'实验活动 简单配合物的形成'}
web=json.loads((R/'website/ebook_mapping.json').read_text());resource=json.loads((R/'website-resource.json').read_text());source=next(x for x in resource['ti_items'] if x.get('ti_is_source_file'))
assert source['ti_size']==report['file_bytes']==18413188
nodes=[]
for n in web['mappings']:
 p=n['page_number'];nodes.append(dict(n,depth=n['node_path'].count('/'),pdf_title=titles.get(p),alignment_status='对应同资源PDF目录及起始页' if p is not None else '网站节点页码为空，无法确认具体标题，保留未对齐状态',website_title_status='接口不含标题字符串；不虚构名称',title_evidence='PDF P4及对应正文起始页' if p else None))
save('outline_alignment.json',dict(resource_id=report['resource_id'],website_resource_title=resource['title'],resource_url='https://basic.smartedu.cn/tchMaterial/detail?contentType=assets_document&contentId='+report['resource_id'],resource_metadata_url='https://s-file-1.ykt.cbern.com.cn/zxx/ndrv2/resources/tch_material/details/'+report['resource_id']+'.json',identity_evidence=['资源ID与指定文件名一致','网站源文件与本地大小同为18413188字节','115个物理页；15个非空目录起始页均与本地目录/正文对应','书名、选择性必修2册次、2019审核、2017年版课标及封底ISBN经图像确认'],sha256=report['sha256'],local_md5=report['local_md5'],website_source_ti_md5=source['ti_md5'],hash_comparison='ti_md5带-3后缀，是对象标识，不直接与本地MD5比较；不声称远端与本地逐字节相同',nodes=nodes,ordering='按同资源网站节点层级与非空页码组织章节、小节；具体知识点按教材细分；章引言、正文小标题和平台未完整返回的整理栏目依PDF原位维护。',limitations=['网站ebook_mapping不返回标题字符串；具体名称来自同资源PDF目录。','17个节点中2个页码为空，无法逐节点确认；未用其他版本补齐。']))
by_page=collections.defaultdict(list)
for row,src,s in zip(rows,sources,S):
 src.update(chapter=row['chapter'],subchapter=row['subchapter'],section=row['section'],knowledge_point=row['knowledge_point'],image_placement='跨页跨栏句段完整合并后统一附图；同字段同整页路径一次',content_boundary='regions是文字候选定位范围；selection.detail覆盖时以核定正文为最终片段；整页图中其他内容不表示录入正文',visual_status='reviewed')
 for p in set(src['image_pages']+src.get('example_pages',[])):by_page[p].append(row['knowledge_point_id'])
(R/'source_records.jsonl').write_text(''.join(json.dumps(x,ensure_ascii=False)+'\n' for x in sources))
roles={1:'封面及2019审核',2:'编写人员',3:'致同学们',4:'目录',5:'引言',6:'引言',7:'引言',8:'第一章章引言',36:'第二章章引言',70:'第三章章引言',108:'名词索引',109:'空白页',110:'后记及课标依据',111:'图片来源致谢',112:'空白页',113:'空白页',114:'元素周期表',115:'封底与ISBN'}
exercise={20,31,32,34,35,42,43,53,54,65,66,68,69,79,80,87,88,97,103,105,106};reviews={33,67,104}
fragments=[
(5,'引言','保留组成结构决定性质与变化，删除一般学习目标；末尾提问不拆成残句'),
(6,'引言','乙醇/二甲醚同分异构、磺胺结构相似及模拟酶为有效原例；发现者、年代、获奖与评价删除'),
(7,'引言','方解石与霰石壳体结构、功能对比保留'),
(9,'能层能级','两表及能量顺序保留；未解讨论中的2n²概括不外补'),
(11,'原子光谱','吸收/发射、光谱分析及特征谱线保留；纯发现史删除'),
(12,'电子排布表','表1-1跨P12-P13完整转录，不补省略号所指其他元素'),
(13,'能级交错','4s先于3d填入与Cr/Cu例外、经验性和模型限制保留'),
(14,'思考与讨论','[Ne]3s¹、Fe[Ar]3d⁶4s²与价层定义为给定讲解；其他未解排布不填写'),
(14,'离散的谱线','保留钠双线、定态和跃迁解释；人物年代奖项删除'),
(17,'轨道表','d、f省略内容不外补；保留原图与轨道数'),
(18,'自旋、洪特规则','有效ESR与光谱磁场情境保留；只恢复正确给定轨道表示，不解额外练习'),
(21,'三张周期表','保留各表排列方法和结构依据，人物年代发展评价不单列'),
(24,'再探元素周期表','给定五区定义及ds脚注保留；问题、解释整理任务与预测119号元素不作答'),
(25,'原子半径','影响因素和图示保留；P26趋势问题不补答案'),
(27,'电离能','锯齿状例外解释、逐级表给定数据保留；推理讨论空格不填'),
(29,'稀有气体史话','保留两种氮气密度、假设、分离空气和光谱鉴别；人物年代删除'),
(30,'稀有气体与Og','保留已知化合物、八电子结构及理论预测条件，不把历史惰性观点当绝对规律'),
(33,'整理与提升','性质周期性清单有增补内容保留，其他重复及未解题不重录'),
(36,'章引言','单原子/高分子/巨分子及ATP合酶结构例图有效；历史与奖项删除'),
(39,'共价键探究','仅保留已给的乙炔p轨道形成π键提示；其余研究问题和空表不补'),
(40,'键能表','298.15K、101kPa、气态原子及平均值条件、全表键级和数据保留'),
(41,'键长键角','平衡位置条件及1pm=10⁻¹²m脚注保留'),
(42,'共价半径','数据表保留；半径差值讨论不补'),
(44,'红外光谱','羟基推测首讲原例与原图在detail，不能拆为example'),
(45,'质谱','甲苯92/91/65峰、m/z、离子电荷和原解完整在detail'),
(47,'空间模型','P4等模型图及S8皇冠、环己烷椅船稳定对比保留，评价删除'),
(48,'孤电子对','(a−xb)/2与阳减阴加、SO2/NH4⁺/CO3²⁻表为核心，不解S/P价电子讨论'),
(49,'VSEPR','先含孤电子对模型再略去的步骤完整；表2-4原图及数据保留'),
(50,'杂化','sp³甲烷矛盾情境、形成过程与水氨孤电子对完整留detail；过渡金属限制保留'),
(52,'模型制作','材料及给定键长键角表有效；自定目标、成果展示和气球问题不录'),
(55,'极性','图2-17原图保留；P55判断极性未解题不填'),
(56,'臭氧及表面活性剂','保留微弱极性28%、溶解对比、胶束去污；跨栏单分子膜句先合并'),
(57,'羧酸酸性','pKₐ=−lgKₐ、七种酸数据及卤素种类/数量/烷基长度条件保留'),
(58,'分子修饰','定义、三氯蔗糖及布洛芬酯化结构和明示性质保留，完美甜味剂评价删除'),
(59,'范德华力','全表保留；壁虎实验、模拟方法和仿生材料保留，历史评价删除；卤素趋势问题不解'),
(60,'氢键','保持分子内邻羟基苯甲醛与分子间对羟基苯甲醛的具体比较；不得换为未解练习中的苯甲酸'),
(61,'氢键表与生物结构','键长指A—H…B的A至B距离，不能误作H…B；DNA及蛋白原图保留'),
(62,'溶解性','相似相溶的一般性限定、戊醇对比保留；给定碘萃取/KI操作和I3⁻反应保留，不回答问题'),
(63,'溶解度和手性','1.01×10⁵Pa、293K、每100g水及单位完整；手性异构和药物作用保留、经济评价删除'),
(64,'巴斯德与手性','分晶实验、光学活性、假设及霉菌只利用一种的明示结论保留，奖项历史评价删除'),
(67,'整理与提升','知识框架和待填表均已首讲或未给解，不重录'),
(71,'状态及等离子体','非分子物质、三态模型图和等离子体构成/性质/应用保留；历史错误观点不作结论'),
(72,'液晶','熔点至澄清点的加热情境、取向序无位置序和显示方法保留；发现史删除'),
(73,'自范性','适当生长速率条件、玛瑙水晶对比及杂质脚注保留'),
(74,'实验3-1','三条途径和三组器材步骤完整；未给出的实验现象不补；原图3-5明示例图保留'),
(75,'各向异性','石蜡/红热铁针实验与现象、固定熔点及X射线鉴别方法保留'),
(77,'晶胞','铜均摊8×1/8+6×1/2=4完整；NaCl与Na/Zn/I2/金刚石计数题不作答；准晶查阅任务无给定结论排除'),
(78,'晶体结构测定','分立斑点/明锐峰与非晶体对比保留；准晶论文任务排除'),
(79,'乙酸原例','晶胞4个分子及坐标到键长键角的首讲完整；后半页练习排除'),
(81,'分子晶体','类别、性质、熔点表及分子密堆积的仅范德华力条件保留'),
(82,'冰与干冰','氢键方向性、紧邻4/12、4℃密度变化与制冷用途保留'),
(83,'镁与可燃冰','镁在干冰中继续燃烧实验含点燃条件与白光结论；笼状水合物假设式和实际占据差异跨页合并'),
(84,'共价晶体','金刚石键长/键能/键角和SiO2首讲保留'),
(85,'共价晶体','硅氧四面体螺旋、左右型及发光陶瓷取代保留；未解比较不外补'),
(86,'硬度与金刚石','莫氏十级、断裂方向性、天然形成温压/急冷条件保留；断代历史与稀有价值评价删除'),
(87,'人工金刚石','高压催化、爆炸、低压等离子体三法和条件差异保留；历史评价删除'),
(90,'离子晶体','NaCl/CsCl熔沸点及分子/共价键/氢键可能共存条件跨页保留'),
(91,'离子液体','CaO/NH4NO3/Ca(H2PO4)2/C2H5NH3NO3熔点反例保留，前面查阅空表不填'),
(92,'过渡晶体','离子键成分62/50/41/33%及电负性差提示保留，不按纯离子/纯共价机械二分'),
(93,'混合型晶体','石墨sp²、142/335pm、层内导电限定及轨道图保留，泛评价不单列'),
(94,'硅酸盐和纳米晶体','硅氧阴离子电荷、铝取代、铅晶粒r/nm与T/K表完整保留'),
(95,'纳米熔点','200nm（或250nm）限制及表面积原因保留'),
(96,'明矾制备','六步操作、各温差、2～3粒晶核、中央悬挂和交替包覆保留；目的指标、查阅、结果问题不解'),
(98,'实验3-2','六固体颜色、足量水操作、原图和四水合铜明示结论保留；空表不补'),
(99,'实验3-3','原书所有用量、浓度、乙醇95%、摩擦步骤、沉淀到深蓝透明液再到晶体及反应式完整保留'),
(100,'实验3-4和3-5','铁/SCN明示鉴定与Fe2+不红保留；AgCl消失及银氨反应保留，不扩写未给配离子式'),
(101,'天然配合物和超分子','卟啉配体、中心离子及首讲杯酚分离全步骤保留'),
(102,'超分子','完整分离流程图和冠醚原图保留；诺奖评价排除'),
(103,'冠醚表','原表五种碱金属离子及直径数据照录，自组装关联双分子膜；后续未解练习不录'),
(104,'整理与提升','已讲概念与空表不重复录入'),
(107,'实验活动','Cu/Ag形成方法与前文同法重复不再次单录；Fe3+/[Fe(CN)6]3−对比有新条件，保留用品与两组给定步骤，现象解释空表不补'),
(108,'索引','名词导航不重复抽取'),
(114,'元素周期表','正文已讲周期表结构；整张参考表不逐元素新增同类型知识点，原图留作核查附件')]
exclusions=[dict(pdf_page=p,scope=a,decision=b) for p,a,b in fragments];audit=[]
for p in range(1,116):
 role=roles.get(p,'正文、实验或有效侧栏')
 if p in exercise:role='练习/复习题'+('及同页讲解' if by_page[p] else '')
 if p in reviews:role='整理与提升：已讲知识、框架和待填表'
 why='保留给定讲解、实验与有效补充；未解问题、任务指标、纯历史评价及重复知识按片段排除。' if by_page[p] else role+'；不新增知识正文。'
 if not by_page[p]:exclusions.append(dict(pdf_page=p,scope='whole_page',decision=why))
 first=p if p%2 else p-1
 audit.append(dict(pdf_page=p,printed_page=p-3 if 5<=p<=108 else None,page_image=f'images/{SLUG}/page-{p:03}.png',review_image=f'review/pages-{first:03}-{min(first+1,115):03}.jpg',visual_status='reviewed',role=role,record_ids=by_page[p],checks=['公式、上下标、电荷、箭头、单位','表格、图示、明示条件','跨页跨栏及选段边界'],decision=why))
save('visual_audit.json',dict(total_pages=115,reviewed_pages=115,method='逐物理页查看渲染图；文字层仅候选；逐条回读，对分式/电荷/表格/跨栏错误按页图校正，复杂结构保留原图',pages=audit));save('page_map.json',audit);save('exclusions.json',exclusions)
save('id_map.json',[dict(old_id=None,new_id=x['knowledge_point_id'],knowledge_point=x['knowledge_point'],reason='新分册首次抽取，教材顺序连续编号') for x in rows])
save('changes.json',dict(action='initial_full_book_extraction',source_sha256=report['sha256'],records=len(rows),existing_book_outputs_modified=False,before=[],after=rows,reason='独立新增分册；按教材细分知识，合并跨页跨栏，保留完整核心首讲与明示实验，排除未解题、历史评价和重复片段。',recovery='selection.json为核定正文和选区；只运行scripts/build.py及scripts/package_audit.py重建。select和correct脚本是一次性过程记录，不重复执行。'))
fields=['knowledge_point_id','chapter','subchapter','section','knowledge_point','detail','example','pdf_page']
assert len(rows)==len(S)==len(sources)==105
assert list(rows[0])==fields and (R/'knowledge_points.csv').read_bytes().startswith(b'\xef\xbb\xbf')
assert [x['knowledge_point_id'] for x in rows]==[f'RJ-CHEMISTRY-HSS2-{i:03}' for i in range(1,106)]
assert len({x['knowledge_point'] for x in rows})==105
for row,src in zip(rows,sources):
 assert all(row[k].strip() for k in fields if k!='example')
 assert not any(ord(c)<32 and c not in '\n\r\t' for c in row['detail']+row['example'])
 assert row['knowledge_point_id']==src['knowledge_point_id'];ps=set()
 for field in ['detail','example']:
  refs=re.findall(r'!\[page-(\d{3})\]\((images/[^)]+)\)',row[field]);assert len(refs)==len(set(path for _,path in refs))
  for pn,path in refs:assert path==f'images/{SLUG}/page-{pn}.png' and (R/path).is_file();ps.add(int(pn))
  for line in row[field].splitlines():
   if '![' in line:assert re.fullmatch(r'!\[page-\d{3}\]\(images/'+SLUG+r'/page-\d{3}\.png\)',line)
 qs=set()
 for group in row['pdf_page'].split(';'):
  nn=list(map(int,re.findall(r'\d+',group)));qs.update(range(nn[0],nn[-1]+1))
 assert ps==qs==set(src['image_pages']+src.get('example_pages',[]))
 assert all(1<=x[0]<=115 for x in src['regions'])
assert len(audit)==115 and all((R/x['page_image']).is_file() and (R/x['review_image']).is_file() for x in audit)
assert hashlib.sha256(Path(report['source_pdf']).read_bytes()).hexdigest()==report['sha256']
terms={48:['(a−xb)/2','a=5−1=4','a=4+2=6'],57:['pKₐ=−lgKₐ','0.23','4.88'],64:['1.01×10⁵ Pa','293 K','100 g'],77:['8×(1/8)+6×(1/2)=4'],87:['4.5×10⁹','6.0×10⁹'],99:['4 mL','8 mL 95%','Cu²⁺+2NH₃·H₂O'],100:['Fe³⁺','Fe²⁺','1滴'],105:['2滴K₃[Fe(CN)₆]','|实验步骤|实验现象|解释|']}
for i,tt in terms.items():assert all(t in rows[i-1]['detail'] for t in tt),(i,tt)
md=['# 人教版高中化学选择性必修2 物质结构与性质\n\n全书105条记录。教材身份、来源及核验说明见 [README](README.md)。\n']
for x in rows:
 md.append(f"## {x['knowledge_point_id']} {x['knowledge_point']}\n\n{x['chapter']} / {x['subchapter']} / {x['section']} · {x['pdf_page']}\n\n{x['detail']}\n")
 if x['example']:md.append('### 补充原例与原解\n\n'+x['example'])
(R/'knowledge_points.md').write_text('\n'.join(md))
save('validation.json',dict(status='passed',records=105,pdf_pages=115,images=115,visually_reviewed_pages=115,chapter_counts=dict(collections.Counter(x['chapter'] for x in rows)),checks=['UTF-8 BOM及八字段','连续唯一ID与来源映射','必填及控制字符','115页原图和核对图存在','图片独立行及同字段去重','源页集合与页标签和图片一致','源PDF SHA-256未改变','关键公式与条件、实验用量检查','CSV与Markdown正文同源'],limitations=['网站目录17节点中2节点无页码，接口无标题字符串；不虚构完整网站标题对齐。','结构程序检查不能替代视觉核查；原书复杂二维图示以原图保留。']))
print(json.dumps(dict(records=105,pages=115,status='passed'),ensure_ascii=False))
