from pathlib import Path
import json,csv,hashlib
R=Path(__file__).resolve().parents[1]
rows=list(csv.DictReader((R/'knowledge_points.csv').open(encoding='utf-8-sig')))
sources=[json.loads(x) for x in (R/'source_records.jsonl').read_text().splitlines()]
candidates=[json.loads(x) for x in (R/'transcription_candidates.jsonl').read_text().splitlines()]
meta=json.loads((R/'source_report.json').read_text());mapping=json.loads((R/'website/ebook_mapping.json').read_text())
def write(n,v): (R/n).write_text(json.dumps(v,ensure_ascii=False,indent=2)+'\n')
identity={'book_key':R.name,'title':'普通高中教科书·物理 必修 第一册','publisher':'人民教育出版社','stage':'普通高中','subject':'物理','volume':'必修 第一册','curriculum_standard':'普通高中物理课程标准（2017年版）','curriculum_standard_evidence':'PDF P132 后记明示','approval':'2019年国家教材委员会专家委员会审核通过','approval_evidence':'PDF P1、P132','edition_and_printing':'版权页未提供版次和印次日期，未推断','isbn':'978-7-107-33756-1','isbn_evidence':'PDF P134','resource_id':'708256b6-6f06-4d14-89c7-4df16dfe3b81','website_title':'普通高中教科书·物理必修 第一册','website_resource_url':'https://basic.smartedu.cn/tchMaterial/detail?contentType=assets_document&contentId=708256b6-6f06-4d14-89c7-4df16dfe3b81','website_metadata_url':'https://s-file-1.ykt.cbern.com.cn/zxx/ndrv2/resources/tch_material/details/708256b6-6f06-4d14-89c7-4df16dfe3b81.json','website_mapping_url':'https://r1-ndr-private.ykt.cbern.com.cn/edu_product/esp/assets/708256b6-6f06-4d14-89c7-4df16dfe3b81.pkg/ebook_mapping_1753410208620.txt','identity_match_basis':['本地文件名资源ID与官方资源ID相同','书名、学段、学科、出版社及册次相符','官方与本地PDF均134页，12944482字节','官方电子书章节节点起页与本地目录及正文相符'],'source_pdf':meta['source_pdf'],'source_sha256':meta['sha256'],'source_bytes':Path(meta['source_pdf']).stat().st_size,'pdf_pages':134,'review_date':'2026-10-20','scope':'本次独立结果，未合并替换其他册次'}
write('book_identity.json',identity)
names={7:'序言 物理学：研究物质及其运动规律的科学',15:'第一章 运动的描述',16:'1. 质点 参考系',20:'2. 时间 位移',26:'3. 位置变化快慢的描述——速度',32:'4. 速度变化快慢的描述——加速度',40:'第二章 匀变速直线运动的研究',41:'1. 实验：探究小车速度随时间变化的规律',44:'2. 匀变速直线运动的速度与时间的关系',47:'3. 匀变速直线运动的位移与时间的关系',52:'4. 自由落体运动',61:'第三章 相互作用——力',62:'1. 重力与弹力',68:'2. 摩擦力',73:'3. 牛顿第三定律',77:'4. 力的合成和分解',81:'5. 共点力的平衡',87:'第四章 运动和力的关系',88:'1. 牛顿第一定律',93:'2. 实验：探究加速度与力、质量的关系',99:'3. 牛顿第二定律',104:'4. 力学单位制',109:'5. 牛顿运动定律的应用',114:'6. 超重和失重',121:'课题研究',126:'学生实验'}
nodes=[]
for m in sorted(mapping['mappings'],key=lambda a:a['page_number']):
 pg=m['page_number'];label=names[pg];rs=[r['knowledge_point_id'] for r in rows if r['section']==label or r['chapter']==label]
 nodes.append({**m,'name':label,'name_basis':'本地同版PDF P4 目录及节标题视觉核对；官方映射提供节点ID、层级和物理起页，不包含名称','printed_start':pg-5,'record_ids':rs,'status':'aligned'})
write('outline_alignment.json',{'resource_id':identity['resource_id'],'order_and_hierarchy_basis':'website/ebook_mapping.json 官方实际电子书导航节点；按page_number排序','names_basis':'同版PDF P4及节标题；没有声称官方映射返回了名称','front_page':5,'nodes':nodes,'differences':[],'chapter_intro_rule':'章引言保留章级位置；侧栏按出现位置就近归属'})
page_to_records={p:[] for p in range(1,135)}
for src in sources:
 for field in ['detail','example']:
  for reg in src[field+'_regions']:
   p=reg[0];v={'id':src['knowledge_point_id'],'field':field}
   if v not in page_to_records[p]:page_to_records[p].append(v)
write('page_map.json',[{'pdf_page':p,'printed_page':p-5 if 6<=p<=130 else None,'image':f'images/{R.name}/page-{p:03}.png','records':page_to_records[p]} for p in range(1,135)])
# All omitted source text remains recoverable from the complete page candidates and PNGs.
excluded=[
([1,2,3,4,5,6],'封面、版权、目录、空白、学习导语；身份信息单独保留。'),
([7,8,9,10,11,12,13,14],'序言中纯历史、评价、应用发展叙述、未来未解问题不入主表；P9研究对象和方法、P10电磁规律、P11微观和高速情况下的适用范围提示分别保留。'),
([18,19,22,24,25,27,31,33,36,38,39],'未解思考问题、练习与应用、复习与提高不单独录入；实验过程与必要引入中的问题保留，不补答案。'),
([35,37],'交通工具与社会发展的历史评价；章小结重复知识，不重复录入。'),
([43],'WPS菜单操作不构成新增物理知识；作图物理方法在P42、P44保留。'),
([43,46,51,57,58,59,60],'未解练习、复习题及伽利略生平与社会评价剔除；P51求和方法讲解保留。'),
([66,67,72,76,80,84,85,86],'各节未解习题和章复习题剔除；同页正文及有效侧栏保留。'),
([88,90],'人物评价和纯史实脚注不抽取；P89理想实验、P90第一定律与状态变化条件保留。'),
([92,97,98,103,107,108,112,113,117,118,119,120],'未解练习与复习题剔除；同页动力学测质量、单位定义、误差分析方法及超失重应用讲解按片段保留。'),
([121,124,125],'研究任务指标、报告要求、未给结果的橡皮筋参考选题不录入；P122-P124已讲解气球实验保留原数据和结论范围。'),
([126,127,128],'纯实验发展史和一般学习要求不单列；P126粒子物理学与宇称条件及实验、P126-P127引力波不同探测方法及结果、P128-P129误差和有效数字讲解分别保留。'),
([130,131,132,133,134],'索引、空白、后记、封底不作知识点；P132课程标准与P134 ISBN用于教材身份。')]
write('exclusion_audit.json',{'rules':'用户本次要求及本地extraction-policy.md','source_recovery':['pages.jsonl','images/physics-pep-senior-compulsory-1/'],'decisions':[{'pdf_pages':ps,'reason':reason} for ps,reason in excluded],'duplicate_examples':'未追加章小结及习题中的同类情境；补充原例均有原解，不补解未解问题。','blank_tables':'P28、P29、P42、P96原表格通过整页图片保留空白，未补实验结果。','core_example_placement':['P82滑梯例介绍正交分解，置于detail','P106-P107单位换算原例与简化算法连续置于detail','P109-P112冰壶与滑雪原例是应用方法核心，置于detail','P114-P117下蹲、电梯原例及后续结论在同一detail中保留']})
notes={11:'从历史段落中保留牛顿学说不适用于微观和高速情况的明确条件。',126:'从混合历史段落中保留粒子物理学定义、宇称的强/电磁与弱相互作用区别、钴60统计实验；引力波引入跨P127完整合并。',127:'铝棒天线、－270 ℃、无肯定结果、双星观测的推测与激光干涉仪探测结果分别忠实保留。',16:'质点模型和侧栏按区域分离。',17:'地球数量级、列车例、质点条件与模型侧栏核对。',20:'时刻与时间间隔图示和位置段落跨P21合并。',21:'位移与路程、矢量标量；P20-P21、P21-P22跨页衔接。',23:'8 V、50 Hz、0.02 s及器材步骤核对；原始数据侧栏移至完整步骤之后。',28:'计数点间隔、0.1 s与0.06 s、空表及误差侧栏。',32:'a＝Δv/Δt与m/s²；数值引入情境保留。',33:'加速度方向和v-t斜率；跨P34句子合并。',41:'器材与先启动计时器再放小车；不补测量结果。',47:'两种位移公式及初位置x₀脚注；单页放大复核。',49:'v²－v₀²＝2ax；动车原例的负号、单位和跨P50原解。',53:'牛顿管操作、原文结论与自由落体条件；下落实验不补数据。',54:'g的地理差异、标准值、纬度表与本书默认9.8注释。',64:'桌面微小形变演示只保留原文观察步骤，不追加现象答案。',65:'弹性限度、弹簧实验步骤，F-x图保留原图。',69:'动摩擦因数表、雪橇原例与跨P70计算。',71:'0＜F≤Fmax、力突然减小的实测现象；流体段跨P72合并。',74:'F与F′区分，作用力与反作用力大小方向和驱动实例。',78:'橡皮条等效效果条件与平行四边形定则，续至P79。',82:'正交分解核心滑梯原例保留detail。',83:'悬绳原例两种方法均保留，不机械删重。',93:'槽码质量远小于小车质量的明示条件。',94:'a＝2x/t²与相同运动时间下的位移比。',95:'两种实验参考案例器材、平衡阻力与同步启停步骤。',97:'a－1/m检验图和控制变量法。',100:'合力条件、比例系数和牛顿单位。',106:'原例属于统一单位算法核心；与P107相连保留。',108:'普朗克常量分式、10⁻³⁴、m²·s⁻¹与定义生效日期；单页放大复核。',110:'冰壶分段运动初末速度、负号、摩擦因数90%。',112:'滑雪加速度、正交分量及压力方向；原值650 N不自行更改。',115:'下蹲先失重后超重，原力传感器曲线不补站起阶段答案。',116:'电梯原例与后续“这个结果”合并在detail；603 N与压力F_N′。',123:'气球原始数据、l＝(ln－l₀)/n及v＝l/T₀；跨P124结论合并，单页放大复核。',128:'双栏先左后右；偶然/系统误差边界。',129:'相对误差脚注、8%与0.8%、19.0 mm、末位0含义及有效数字数量；单页放大复核。'}
vis=[]
for pg in range(1,135):
 spread=(pg-1)//2*2+1
 vis.append({'pdf_page':pg,'status':'visually_inspected','evidence_image':f'review/pages-{spread:03}-{spread+1:03}.jpg','method':'逐页查看双页视觉图；公式、单位、表格、图示和条件与候选文字对照；必要处单页放大','record_refs':page_to_records[pg],'note':notes.get(pg,'正文与有效栏目按教材位置核对；非知识内容见 exclusion_audit.json。' if page_to_records[pg] else '已查看；无新增主表片段，排除原因见 exclusion_audit.json。')})
(R/'visual_review.jsonl').write_text(''.join(json.dumps(x,ensure_ascii=False)+'\n' for x in vis))
write('id_map.json',{'mode':'new_extraction','previous_published_ids':[],'mappings':[{'old_id':None,'new_id':r['knowledge_point_id'],'knowledge_point':r['knowledge_point']} for r in rows]})
changes=[]
for row,src,cand in zip(rows,sources,candidates):
 changes.append({'action':'add_new_extraction','reason':'按教材概念、规律、方法、实验及有效补充独立识别；视觉核对后定稿','old_id':None,'new_id':row['knowledge_point_id'],'before':None,'candidate_before_visual_corrections':cand,'after':row,'source_regions':src,'source_identity':'book_identity.json','recovery':'pages.jsonl及对应整页PNG；selection.tsv、patches.json和scripts/build.py可重建'})
(R/'change_log.jsonl').write_text(''.join(json.dumps(x,ensure_ascii=False)+'\n' for x in changes))
readme='''# 人教版高中物理必修第一册抽取结果

本册独立保存，共 **82条知识点**，覆盖 **4章19节**，另收录序言中的实质知识、课题研究及实验附录。7个 example 字段保留可分离的补充原例与原解（其中牛顿第二定律字段含两道不同方法的原例）。

- [主CSV（UTF-8 BOM，八字段）](knowledge_points.csv)
- [Markdown阅读版](knowledge_points.md)
- [教材身份](book_identity.json)、[官方目录对齐](outline_alignment.json)
- [来源片段](source_records.jsonl)、[逐页映射](page_map.json)
- [逐页视觉核对](visual_review.jsonl)、[排除与去重说明](exclusion_audit.json)
- [校验结果](validation_report.json)、[变更记录](change_log.jsonl)、[ID映射](id_map.json)

## 内容与来源

教材依据《普通高中物理课程标准（2017年版）》编写，2019年审核通过（PDF P132明示）。版次与印次日期在版权页未提供，未推断。不能将本册标为义务教育2022修订版。

网站实际电子书导航映射用于目录层级和顺序，共26个节点；节点映射本身不含名称，名称由同版PDF P4目录及正文节标题视觉核对补全，依据在目录对齐文件中明确记录。官方元数据和原始导航映射保存在website/。

页码均为PDF物理页序。正文印刷页码通常为物理页减5。跨页文字先合并，再附图；各字段内整页图片路径去重，图源为 images/physics-pep-senior-compulsory-1/page-NNN.png。整页图中可包含未录入的相邻内容，以正文选择区域和排除记录为准。

PDF文字层只作为候选。已逐页查看134页，重点复核分式、上下标、单位、表格、图示条件和跨页。实验保留教材器材、步骤、明示现象及结论；空表不填数据，开放问题不补答案。核心原例随完整讲解保留detail，可分离的补充原例置于example。复杂图示及原始空表保留整页图，不自行重绘或补结果。

## 重建与校验

在本目录执行：

```sh
/Users/l/miniconda3/envs/base124/bin/python scripts/build.py
/Users/l/miniconda3/envs/base124/bin/python scripts/audit.py
```

selection.tsv记录人工选择区域；patches.json记录全文校正；build.py中的MATH记录按页按区域转录的分式。原始候选保存在pages.jsonl与transcription_candidates.jsonl。程序结构检查不替代逐页视觉核对。
'''
(R/'README.md').write_text(readme)
print('metadata written',len(nodes),'nodes',len(vis),'reviewed pages')
