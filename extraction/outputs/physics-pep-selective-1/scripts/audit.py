"""Package provenance, page review log, exclusions and structural validation."""
import csv
import hashlib
import json
import re
from collections import Counter
from pathlib import Path
from build import BOOK, CHAPTERS, SECTIONS, RECORDS, FIELDS

R=Path(__file__).resolve().parents[1]
def save(name,data):
    (R/name).write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
def jsonl(name,data):
    (R/name).write_text(''.join(json.dumps(x,ensure_ascii=False)+'\n' for x in data),encoding='utf-8')

rows=list(csv.DictReader((R/'knowledge_points.csv').open(encoding='utf-8-sig')))
sources=[json.loads(l) for l in (R/'source_records.jsonl').read_text().splitlines()]
source=json.loads((R/'source_report.json').read_text())
website=json.loads((R/'website/resource-v2.json').read_text())
nav=json.loads((R/'website/ebook_mapping.json').read_text())
starts=[[7,11,17,22,26,30],[37,41,48,51,56,59],[67,72,76,79,84],[90,95,100,106,109,113]]
chapter_starts=[6,36,66,89]
alignment=[]
for c,(chapter,sections) in enumerate(zip(CHAPTERS,SECTIONS),1):
    cp=chapter_starts[c-1]
    node=next(a for a in nav['mappings'] if a['page_number']==cp)
    alignment.append(dict(kind='chapter',name=chapter,pdf_page=cp,printed_page=cp-5,website_node_id=node['node_id'],website_node_path=node['node_path'],status='matched'))
    for s,title in enumerate(sections,1):
        p=starts[c-1][s-1]
        node=next(a for a in nav['mappings'] if a['page_number']==p)
        alignment.append(dict(kind='section',name=title,chapter=chapter,pdf_page=p,printed_page=p-5,website_node_id=node['node_id'],website_node_path=node['node_path'],status='matched',records=[row['knowledge_point_id'] for row in rows if row['chapter']==chapter and row['subchapter']==f'第{s}节 {title}']))
node=next(a for a in nav['mappings'] if a['page_number']==121)
alignment.append(dict(kind='supplement',name='课题研究',pdf_page=121,printed_page=116,website_node_id=node['node_id'],website_node_path=node['node_path'],status='matched',records=['RJ-PHY-S1-082','RJ-PHY-S1-083'],editorial_group='按用户所引规范，就近归入第四章第6节；实际栏目与来源页保留'))
save('outline_alignment.json',dict(status='matched',name_basis='已下载并视觉核对同一网站资源的目录预览图website/directory-page-004.jpg；名称、章/节顺序及印刷页码与本地P4一致。ebook_mapping另提供节点ID、父子层级与物理页序。',website_resource_id=website['id'],website_directory_preview='website/directory-page-004.jpg',mapping_front_page=nav['front_page'],matched_nodes=28,sections=23,nodes=alignment,index_note='目录中的索引印刷P121对应物理P126；网站映射末节点物理P121对应课题研究，不将其误认作索引。索引无新增知识不进入主表。'))
meta={**source,'book_id':BOOK,'title':'普通高中教科书·物理选择性必修 第一册','publisher':'人民教育出版社','education_stage':'高中','subject':'物理','volume':'选择性必修 第一册','curriculum_basis':'普通高中物理课程标准（2017年版），本地PDF物理P128后记明示','approval':'2019年国家教材委员会专家委员会审核通过，本地PDF物理P128明示','edition_date':'版权页未列明年月版次，不推断','isbn':'978-7-107-34591-3','smartedu_resource_id':website['id'],'smartedu_updated_at':website['update_time'],'website_pdf_bytes':next(a['ti_size'] for a in website['ti_items'] if a.get('ti_format')=='pdf'),'identity_evidence':['文件名资源ID与同版网站资源ID一致','网站教材名称、学段、学科、出版社及册次一致','本地PDF与网站PDF元数据均130页、11644106字节','网站目录预览图与本地P4逐项视觉一致','网站映射4章23节及课题研究共28个节点的父子层级和页序与本地一致'],'remote_pdf_sha256_verification':'未下载远程整本PDF进行字节哈希比较；本地SHA-256单独保存，不将字节数相同当作哈希相同。','policy_reference':{'local_skill':'skills/smartedu-math/SKILL.md','local_policy':'skills/smartedu-math/references/extraction-policy.md','requested_url':'https://github.com/yyyrrrr7/smartedu_math/blob/main/skills/smartedu-math/references/extraction-policy.md','user_override':'按本次用户要求应用于物理；教材自行识别知识点、保留实验、完整detail及可分离example。'},'extraction_date':'2026-10-20','records':len(rows),'chapters':4,'sections':23,'page_images':130,'supplementary_example_fields':sum(bool(r['example']) for r in rows)}
save('metadata.json',meta)

exclusions=[]
def excluded(pages,kind,reason,retained=None):
    exclusions.append(dict(pdf_pages=pages,kind=kind,reason=reason,retained_in=retained or [],recovery='pages.jsonl及images/'+BOOK+'/page-NNN.png保留全页原始来源'))
excluded([1,2,3,4,5,127,128,129,130],'非知识正文','封面、扉页、版权、目录、空白、后记、封底；身份信息仅进入元数据')
excluded([6,36,66],'章引言重复概述','对本章学习任务、价值与后文内容的概述不重复录入；P89新增光学分类另保留',['RJ-PHY-S1-057'])
for pp in [[10],[15,16],[21],[25],[29],[33],[34,35],[40],[47],[50],[55],[58],[63],[64,65],[71],[75],[78],[83],[86],[87,88],[94],[99],[105],[108],[112],[118],[119,120]]:
    excluded(pp,'未解练习','仅排除本页练习与应用、复习与提高中的未解题目；同页正文、演示及有效栏文另按来源记录收录')
excluded([7,37,67,90],'历史引语与人物脚注','纯引语、人物年代、生平和评价不作为知识点')
excluded([9],'一般性方法侧栏','物理学家寻求规律与不变量的概括性评价，无新增物理概念；概念建立实验已完整保留',['RJ-PHY-S1-001','RJ-PHY-S1-002'])
excluded([14],'混合科学漫步中的历史片段','运动量度争论的历史过程与评价排除；动量/动能与力的比较保留',['RJ-PHY-S1-006'])
excluded([15],'历史新闻与任务评价','汽车碰撞试验发生时间、新闻评价等排除；测量过程与冲击力影响因素保留',['RJ-PHY-S1-007'])
excluded([18,31],'未解思考问题','弹簧分开小车的总动量提问及宇航员抛物体问题未给出原解；独立火箭喷气模型及完整原解保留',['RJ-PHY-S1-018'])
excluded([29],'重复概念建立的方法性回顾','抽象与概括栏目回顾动量概念，无新增物理定量规律；不重复建立动量记录',['RJ-PHY-S1-001','RJ-PHY-S1-002'])
excluded([32,54,62,99,104,111,112,116,117],'混合栏目的历史发展与评价','分离发展年代、人物获奖、技术成就等纯历史评价；多级火箭、计时原理、振动控制、波粒二象性、衍射及激光有效物理内容保留')
excluded([46],'泛化艺术评价','艺术与1+1=2的评价句排除；音阶表、谐和音频率比及音高适用条件保留',['RJ-PHY-S1-028'])
excluded([121,125],'研究任务指标与未给结果','排除问题提出中的任务询问、参考选题证明要求；完整杆线摆已讲解实验及参考选题已给操作保留，不补弹簧周期公式或实测结论',['RJ-PHY-S1-082','RJ-PHY-S1-083'])
excluded([126],'索引重复','索引只列已有名词及首次页码，无新增知识，不再次录入')
jsonl('exclusion_audit.jsonl',exclusions)

special={
 7:'等质量与不同质量小球的实验情境，保留至P8的比较；历史引语排除',8:'三组小车质量速度数据及m1/m2/v/v′表头逐格复核；碰撞前后时刻侧栏独立合并',9:'p=mv、单位、矢量方向；钢球原例跨P9-P10完整合并',10:'钢球负号与方向、动量代数运算侧栏；气球操作不补结果',11:'恒力推导三组分式、冲量定义及动量变化率侧栏',12:'N·s、合力冲量或矢量和、变力平均值及应用条件',13:'垒球原例初末动量及平均作用力跨P13-P14合并',14:'平均力-6300N与方向；科学漫步有效比较，排除历史',15:'试验50km/h及传感器信息，练习区不录入',17:'两个物体受力与动量变化推导跨P17-P18',18:'系统内外力、动量守恒条件、推导结束',19:'列车质量10^4指数、动量守恒近似条件及0.9m/s',20:'炸裂例题分式与地面参考系；正文普适性跨P20-P21',22:'实验系统条件与所测质量速度',23:'检验式、气垫导轨方案跨P23-P24',24:'三种滑块碰撞方案与斜槽小球器材；后者跨P24-P25',25:'相同下落高度、速度比与水平距离比；未给结果不补',27:'分类、等质量粘连原例能量1/2；正碰核心情境',28:'动量和动能方程、v1′/v2′分式、三种质量比较；末句跨P28-P29',30:'反冲的系统条件和喷灌应用',31:'气球及弯管操作；火箭极短喷气模型跨P31-P32',32:'喷气前火箭参考系、Δm/m、速度式、质量比及多级限制',37:'机械振动、理想弹簧振子与平衡位置',38:'位置-时间坐标、频闪0.05s、x-t图像',39:'数码相机0.04s，简谐运动两种检验方法跨P39-P40',41:'振幅、2A范围、全振动跨P41-P42',42:'f=1/T、ω=2π/T、Hz=s^-1；多周期计时',43:'振幅无关、相位差、双小球演示跨P43-P44',44:'滞后1/4周期、位移表达式；补充原例跨P44-P45',45:'原例初相π/2、路程2m与位移0.1m；声音图像方法跨P45-P46',46:'八列音阶频率表、4:5:6与10:12:15及中等音高条件',48:'回复力与简谐运动条件跨P48-P49',49:'F=-kx、原空白能量表不代填；能量段落跨P49-P50',50:'能量转换、理想模型及振幅与机械能条件；练习排除',51:'单摆长度质量体积及空气阻力条件；切向分力跨P51-P52',52:'小角度弧长与位移近似、F=-mgx/l、墨汁图样步骤不补结果',53:'控制变量演示、小偏角、周期根式T=2π√(l/g)',54:'计时有效原理分离于历史叙述',56:'g=4π²l/T²及单摆装置',57:'摆长两种测法、计时与数据分析跨P57-P58',58:'取平均值与比较方法，不补测量结果',59:'固有频率、阻尼能量损失、受迫振动跨P59-P60',60:'达到稳定后的驱动力频率、共振摆装置',61:'共振定义、共振曲线、转速计和避免共振；侧栏独立合并',62:'弹簧/阻尼器/质量块及反相减振条件',67:'绳波实验与振动的传播，历史引语排除',68:'1/4T、1/2T、3/4T与T分图含义；团体操类比',69:'横波/纵波、弹簧圈演示与疏密部跨P69-P70',70:'声波介质、机械波定义、能量信息及纸屑操作',72:'波形图坐标与简谐波条件跨P72-P73',73:'波形图/振动图对比、波速公式及0℃声速八行表',74:'T>0.5s，左右传播原例分式跨P74-P75',75:'原例末周期0.67s；练习排除',76:'水波反射演示、三线共面和反射角；折射跨P76-P77',77:'衍射两组控制变量、7/10、5/10、3/10分式及跨页句',78:'明显衍射条件与声波波长区间；练习排除',79:'波的独立传播、叠加位移矢量和跨P79-P80；侧栏分离',80:'同一振动片两细杆、稳定干涉区域；位移和末句',81:'增强/减弱解释、等振幅抵消及干涉三条件跨P81-P82',82:'干涉定义续句、声音实验不补分布，主动降噪反馈',84:'多普勒定义、蜂鸣器及模拟实验',85:'类比限制与靠近远离频率变化，测速跨P85-P86',86:'超声、血流与星球光波测速；练习排除',89:'章引言几何光学与物理光学新增分类单列章级位置',90:'反射/折射与角度定义、图4.1-1和4.1-2',91:'sinθ1/sinθ2=n12、光路可逆、折射率与符号脚注',92:'n=c/v、589.3nm/20℃折射率表及大头针实验跨P92-P93',93:'四大头针步骤完成；储油桶原例根式跨P93-P94',94:'v=1.9×10^8m/s；练习排除',95:'光疏光密相对性、半圆玻璃砖演示',96:'临界角、入射角等于或大于临界角、sinC=1/n及数值范围',97:'潜水员2C=97.6°原例，全反射棱镜改变方向',98:'内芯外套折射率、两组光纤、脚注适用范围与电子内窥镜区别',99:'水流导光步骤不补路径结论；历史评价及练习排除',100:'氦氖激光器双缝实验和图样',101:'亮暗路程差分式、中心零路程差侧栏',102:'杨氏单缝供光方法保留；d远小于l和小角度几何推导',103:'色光条纹比较，薄膜干涉实验与解释跨P103-P104',104:'薄膜彩色条纹及应用，波粒二象性片段；历史排除',106:'双缝实验器材与测量头跨P106-P107',107:'a/(n-1)、调节平行及轴线、三组条纹对比；传感器跨P107-P108',108:'光敏单元与光照强度方法，练习排除',109:'0.4/0.8mm单缝图样对比与衍射解释',110:'白光、圆孔/手指衍射、直线传播近似与光栅',111:'泊松亮斑条件、X射线晶格尺度与结构信息；历史获奖排除',112:'X射线衍射应用；历史、练习区排除',113:'偏振方向、横波狭缝和纵波必要对比',114:'偏振片P/Q演示，旁栏独立合并，电场方向脚注',115:'自然光、偏振光、反射偏振及相机滤光片',116:'观察操作、激光相干性及普通光源对比',117:'激光平行度/高亮度应用、立体电影跨P117-P118',118:'双眼视差、正交偏振、银幕反射、交替拍摄放映原文',121:'课题研究实际位置，g的实验含义及设计思路跨P121-P122',122:'等效重力加速度、杆线摆装置及条件',123:'θ=90°-β，T=t/20及三次平均；数据分析跨P123-P124',124:'六行实测数据、a=g sinθ、1/√a单位m^-1/2·s、原点直线结论',125:'控制变量及改变弹簧长度方法；证明任务排除，无周期公式或结果补写',126:'索引无新增知识排除',128:'后记只作为2017课程标准与2019审核身份依据'}
reviews=[]
for p in range(1,131):
    ids=[s['knowledge_point_id'] for s in sources if p in s['pdf_pages']]
    a=p if p%2 else p-1
    reviews.append(dict(pdf_page=p,printed_page=p-5 if 6<=p<=126 else None,image=f'images/{BOOK}/page-{p:03d}.png',review_sheet=f'review/pages-{a:03d}-{a+1:03d}.jpg',status='visually_reviewed',method='逐页查看已渲染页图；双页原尺寸联系表，关键公式表格另看原页。文字层仅作候选。',records=ids,checks=special.get(p,'本页无新增可录知识；检查练习、非正文或空白，并记录排除。'),cross_page_rule='跨页完整句与推导先合并，字段末尾再附对应图源，同页路径去重'))
jsonl('visual_review.jsonl',reviews)
save('page_map.json',dict(numbering='physical PDF page, 1-based',printed_offset=5,pages=[dict(pdf_page=p,printed_page=p-5 if 6<=p<=126 else None,image=f'images/{BOOK}/page-{p:03d}.png',records=[s['knowledge_point_id'] for s in sources if p in s['pdf_pages']]) for p in range(1,131)]))
jsonl('change_log.jsonl',[dict(action='new_extraction',old_id=None,new_id=row['knowledge_point_id'],before=None,after=row,source_pdf=source['source_pdf'],source_sha256=source['sha256'],reason='依教材自行细分，同版网站目录定序；本册新建，不替换其他册次',recovery='scripts/selection.json、scripts/patches.json、raw_candidates.jsonl、images/') for row in rows])
save('id_mapping.json',dict(operation='new_extraction',previous_records=0,records=[dict(old_id=None,new_id=r['knowledge_point_id']) for r in rows]))

errors=[];image_count=0
if (R/'knowledge_points.csv').read_bytes()[:3]!=b'\xef\xbb\xbf': errors.append('Missing UTF-8 BOM')
if list(rows[0])!=FIELDS:errors.append('Wrong CSV field order')
if hashlib.sha256(Path(source['source_pdf']).read_bytes()).hexdigest()!=source['sha256']:errors.append('Source SHA mismatch')
for i,(row,s) in enumerate(zip(rows,sources),1):
    kid=f'RJ-PHY-S1-{i:03d}'
    if row['knowledge_point_id']!=kid or s['knowledge_point_id']!=kid:errors.append('ID mismatch '+kid)
    if not row['knowledge_point'] or not row['detail']:errors.append('Empty required field '+kid)
    for f in ['detail','example']:
        value=row[f]; paths=re.findall(r'!\[page-\d{3}\]\((images/[^)]+)\)',value)
        if len(paths)!=len(set(paths)):errors.append('Duplicate path '+kid+' '+f)
        image_count+=len(paths)
        for path in paths:
            if not (R/path).exists():errors.append('Missing image '+path)
            p=int(re.search(r'page-(\d+)',path)[1])
            if p not in [x[0] for x in s[f+'_regions']]:errors.append('Wrong field image '+kid)
        for line in value.splitlines():
            if '![' in line and not re.fullmatch(r'!\[page-\d{3}\]\(images/'+BOOK+r'/page-\d{3}\.png\)',line):errors.append('Nonstandalone image '+kid)
        if value.count('$')%2:errors.append('Unbalanced math '+kid)
        for math in re.findall(r'\$\$.*?\$\$|\$[^$]*\$',value,re.S):
            if math.count('{')!=math.count('}'):errors.append('Unbalanced math braces '+kid)
        if '\x0c' in value or '练习与应用' in value or '复习与提高' in value:errors.append('Residual exercise heading '+kid)
    if not re.fullmatch(r'P\d+(?:-P\d+)?(?:;P\d+(?:-P\d+)?)*',row['pdf_page']):errors.append('Page syntax '+kid)
for a in alignment:
    if a['kind']=='section' and not a['records']:errors.append('Uncovered section '+a['name'])
if len(rows)!=83 or len(sources)!=83:errors.append('Record count mismatch')
report=dict(status='pass' if not errors else 'fail',records=len(rows),chapters=4,sections=23,matched_website_nodes=28,pdf_pages=130,visual_reviews=len(reviews),page_images=len(list((R/'images'/BOOK).glob('page-*.png'))),supplementary_example_fields=sum(bool(r['example']) for r in rows),image_references=image_count,errors=errors,separate_checks={'schema_bom_ids':'pass' if not errors else 'see errors','outline_coverage':'23/23 sections and chapter-level introduction, plus research source regions','image_existence_standalone_dedup':'pass' if not errors else 'see errors','source_identity':'local SHA-256 verified; official directory preview visually matched','content_review':'visual_review.jsonl and transcription_changes.jsonl record manual visual work; structural checks do not prove semantic fidelity','experiments':'retain source steps and explicit conclusions; no supplied answers to open results or exercise questions','math':'manual visual transcription of fractions, powers, roots, units and tables; delimiters/braces structurally checked'})
save('validation_report.json',report)
readme=f'''# 人教版高中物理选择性必修第一册抽取结果

已按本次要求整理 **83 条知识点**，覆盖 **4 章、23 节**，另保留章引言有效分类和书后课题研究；全书 **130 页**已视觉核对。8 个 example 字段收录可自然分离的补充已讲解原例（其中动量守恒字段保留两种不同条件的原例）。

- [知识点阅读版](knowledge_points.md)
- [八字段 CSV（UTF-8 BOM）](knowledge_points.csv)
- [来源身份与哈希](metadata.json)
- [同版网站目录对齐](outline_alignment.json)
- [逐页视觉记录](visual_review.jsonl)
- [来源区域](source_records.jsonl)、[排除记录](exclusion_audit.jsonl)
- [校验报告](validation_report.json)

网站目录使用同一资源的目录预览图及 ebook_mapping；目录名称、顺序、页码逐项与本地教材核对。教材正文作为知识内容依据，未用网站课题数限制知识点数量。网站与本地文件的书名、册次、130 页和字节数一致；没有声称对远程整本 PDF 做过哈希比对。版权页未给出年月版次，未推断。

detail 保留核心解释、必要实验、情境与推导；example 仅放补充原例原解。实验未给出的结果与未解练习答案未补写。混合历史栏文只保留有效物理片段；同类重复概述不再次录入。课题研究按规范就近归属末节，实际位置见来源记录。

页码均为 PDF 物理页序，正文印刷页加 5 即物理页。原图统一使用 `images/{BOOK}/page-NNN.png`，每条记录的每个字段内同一整页路径只出现一次。跨页语句先合并为完整正文，再附图。Markdown 与 CSV 都位于同一输出目录，图片相对路径相同。

可重建材料：`scripts/build.py` 是人工选择的源区域，`raw_candidates.jsonl` 保存未经核验的文字层候选，`scripts/correct.py` 保存显式视觉校正并生成 `scripts/patches.json`。重建依次运行 build.py、correct.py、build.py、audit.py，使用 `/Users/l/miniconda3/envs/base124/bin/python`。程序检查用于字段、来源和图片一致性，不替代逐页视觉核验。

此目录为本册新建结果，没有覆盖其他册次。
'''
(R/'README.md').write_text(readme,encoding='utf-8')
print(json.dumps(report,ensure_ascii=False,indent=2))
if errors:raise SystemExit(1)
