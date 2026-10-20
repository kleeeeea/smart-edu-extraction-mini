"""Validate and document this extraction package; program checks do not replace visual review."""
from pathlib import Path
import csv,json,re,hashlib,shutil,collections
R=Path(__file__).resolve().parents[1]
rows=list(csv.DictReader((R/'knowledge_points.csv').open(encoding='utf-8-sig')))
src=[json.loads(s) for s in (R/'source_records.jsonl').read_text().splitlines()]
info=json.loads((R/'source_report.json').read_text());mapping=json.loads((R/'website/ebook_mapping.json').read_text())
def save(name,o): (R/name).write_text(json.dumps(o,ensure_ascii=False,indent=2)+'\n')
page_map={i:[] for i in range(1,123)}
for r,s in zip(rows,src):
 for p in {z['pdf_page'] for z in s['regions']}|set(s['example_pages']):page_map[p].append(r['knowledge_point_id'])
chapters=['第一章 安培力与洛伦兹力','第二章 电磁感应','第三章 交变电流','第四章 电磁振荡与电磁波','第五章 传感器','课题研究']
section_names=[['磁场对通电导线的作用力','磁场对运动电荷的作用力','带电粒子在匀强磁场中的运动','质谱仪与回旋加速器'],['楞次定律','法拉第电磁感应定律','涡流、电磁阻尼和电磁驱动','互感和自感'],['交变电流','交变电流的描述','变压器','电能的输送'],['电磁振荡','电磁场与电磁波','无线电波的发射和接收','电磁波谱'],['认识传感器','常见传感器的工作原理及应用','利用传感器制作简单的自动控制装置'],['课题研究']]
starts=[[7,13,18,22],[29,35,40,45],[54,59,63,68],[76,81,85,88],[96,102,108],[116]]
node_by_page={n['page_number']:n for n in mapping['mappings']}
align=[]
for c,(names,pages) in enumerate(zip(section_names,starts)):
 for s,(name,page) in enumerate(zip(names,pages),1):
  n=node_by_page[page];sec=f'{s} {name}' if c<5 else name
  align.append({'chapter':chapters[c],'section':sec,'pdf_page':page,'printed_page':page-5,'website_node_id':n['node_id'],'website_node_path':n['node_path'],'records':[r['knowledge_point_id'] for r in rows if r['chapter']==chapters[c] and r['section']==sec],'status':'page_and_hierarchy_matched'})
save('outline_alignment.json',{'status':'matched_page_order_and_hierarchy','resource_id':'2ee7d7fa-1920-4d37-a179-91d5fd59b8c1','website_nodes':len(mapping['mappings']),'front_page':mapping['front_page'],'name_basis':'网站 ebook_mapping 返回实际节点ID、父子层级及物理起始页，不返回名称；名称由本地教材P4视觉目录逐项对齐，不伪称网站接口返回了标题。','sections':align})
save('page_map.json',{'numbering':'physical PDF page, printed textbook page = PDF page - 5 for body','pages':[{'pdf_page':p,'printed_page':p-5 if 6<=p<=120 else None,'image':f'images/physics-pep-selective-2/page-{p:03}.png','records':ids} for p,ids in page_map.items()]})
exclude_pages={1:'封面：核对书名、人教版及教育部审定2019。',2:'书名页：教材身份。',3:'编写人员与版权信息；无独立知识点。',4:'目录：5章19节及课题研究。',5:'空白页。',6:'第一章引言，无独立核心讲解。',12:'练习与应用：未解题。',17:'练习与应用：包括速度选择器、磁流体发电等未解题，未补解。',26:'复习与提高A组：未解题。',27:'复习与提高续：未解题。',28:'第二章引言。',34:'练习与应用：未解题。',39:'练习与应用续：未解题；不把题目中的装置设问当作已讲解原例。',44:'练习与应用：未解题。',49:'练习与应用：未解题。',50:'复习与提高：未解题。',51:'复习与提高续：未解题。',52:'复习与提高续：未解题。',53:'第三章引言。',58:'保留上方发电机正文；下方练习排除。',62:'保留上方电容器作用；练习排除。',67:'练习与应用：未解题。',72:'STSE历史工程叙述及练习排除。',73:'复习与提高：未解题。',74:'复习与提高：未解题。',75:'第四章引言，航天历史与章节导入。',84:'麦克斯韦生平与评价、练习排除；方程组仅为历史图示，没有展开讲解。',92:'保留混合STSE中的有效无线电信号事实，其余历史评价及未解练习排除。',93:'复习与提高：未解题。',94:'复习与提高：未解题。',95:'第五章引言，历史导入。',101:'保留机器人中传感器的功能；历史、评价与练习排除。',107:'保留顶部霍尔元件跨页段落；未解练习排除。',112:'练习与应用：未解设计题，不补电路或结论。',113:'复习与提高：未解题。',114:'复习与提高：未解题。',115:'复习与提高：未解题，霍尔电压公式为待证明设问，不追加到正文。',119:'保留热敏电阻研究装置方法，不补测量数据及结果；任务设想排除。',120:'术语索引：重复定义定位，不重新录入。',121:'后记：核对2017年版课程标准与2019审定信息，排除致谢。',122:'封底：ISBN 978-7-107-34592-0。'}
mixed={7:'保留安培力与历史安培定义的物理条件，排除纪念性评价。',8:'方向实验、左手定则与必要电场比较。',9:'垂直、平行及一般夹角条件，分解公式。',10:'磁电式电流表结构与径向磁场，指针响应。',11:'科学漫步仅保留通电螺线管及导线相互作用；生平评价和练习排除。',13:'电子束实验与洛伦兹力，保留荧光板脚注。',14:'合并跨页左手定则；未解的推导任务未补答案。',15:'洛伦兹力公式与显像管讲解，未解偏转方向设问排除。',16:'扫描跨页合并；正电子及云室实验保留，历史评价排除。',19:'半径公式与示踪实验。',20:'实验现象、周期及原例前半；与P21合并原解。',21:'保留完整已解原例，练习排除。',22:'质谱仪装置及推导保留detail；纯历史评价排除。',23:'合并质谱仪推导；回旋加速器核心情境。',24:'回旋加速器结构、周期同步及盒缝可忽略条件。',25:'保留回旋加速器同步失效条件；练习排除。',29:'条形磁体插拔实验；不补未明示的结果。',30:'四种情况与表1；表2空白保留。',31:'楞次定律及能量解释；未解金属环设问排除。',32:'两道不同方法用途的已解原例完整保留。',33:'右手定则与归纳推理；未解方向讨论排除。',35:'感应电动势与强磁体下落实验，无测量结果不补写。',36:'磁通量变化率、n匝与单位，侧注移出跨页句子。',37:'Blv推导及夹角条件，分式与sinθ校正。',38:'动生电动势与能量讲解保留；练习排除。',40:'感生电场、电子感应加速器完整分析。',41:'涡流定义、加热利用、减小和探测。',42:'探雷器跨页合并；电磁阻尼定义；未解讨论不补解。',43:'微安表做一做及铝框演示；只保留明示步骤及正文结论。',45:'互感、自感概念。',46:'通电及断电灯泡演示，完整电路条件。',47:'电流传感器实验及断电安全；未解设问排除。',48:'自感公式、单位与磁场储能，侧注移至完整正文后。',54:'交变电流与直流。',55:'二极管演示只保留操作，不补明示外现象；发电机结构。',56:'匀强磁场与转动发电机，跨页合并。',57:'正弦推导、峰值和纯电阻条件；波形图保留。',59:'周期频率与ω关系，未解读图题排除。',60:'有效值核心原例留detail，正弦适用限制，波形图保留。',61:'交流公式、感抗与容抗实验，分式根号校正。',63:'变压器原理与实验。',64:'控制变量、器材与量程安全，未补实验数据。',65:'理想模型、匝数比、电压比及效率。',66:'无线充电有效原理，重复互感表述仅一份。',68:'输电损耗与两条路径。',69:'高压输电条件与技术限制，未解问题不补算。',70:'电网供电层级与典型电压。',71:'仅保留交流同步问题和直流输电转换原理。',76:'振荡电路演示；跨页句子合并。',77:'LC电路充放电阶段与i、q图示。',78:'充放电续段及场能转换。',79:'能量损耗补充、固有周期公式，未解问题排除。',80:'完整频率范围原例、固有频率条件；练习排除。',81:'变化B产生E与变化E产生B；侧栏历史评价不混入句子。',82:'电磁波传播、互相垂直及赫兹实验前半。',83:'赫兹实验续、明确观测与场能传播，历史评价排除。',85:'有效辐射的两项条件和开放电路。',86:'跨页开放电路、调制、接收及调谐，侧注独立。',87:'接收跨页合并，电视广播流程；练习排除。',88:'电磁波谱定义、无线电波波段表前半、有效脚注。',89:'续表各行与合并单元格、雷达、通信；Wi-Fi有效事实保留，任务不补结果。',90:'红外、可见光表与频率单位、有效脚注。',91:'紫外线、X与γ射线及STSE有效波长事实，排除纯历史。',96:'干簧管与声控光控必要情境。',97:'传感器定义及实例完整保留detail。',98:'分类及应用，与P99合并跨页句。',99:'组成、转换、信号处理和应用框图。',100:'电容式话筒必要核心原例与解释留detail；生平历史排除。',102:'光敏电阻制作和对比实验，不补未给阻值。',103:'光敏载流子机制、光电计数及温敏材料。',104:'热敏实验、液位报警与应变片；跨页合并。',105:'应变片、力传感器、电容传感器及压阻脚注。',106:'电容位移与霍尔元件，插图文字不混入正文。',108:'门窗报警器材、电路、观察和原理。',109:'元件表1逐格核对；门窗操作与光控导入。',110:'光控两套电路、三极管条件、继电器保护二极管。',111:'元件表2逐格核对，明暗两种状态与操作。',116:'压力传感器装置与初始质量条件，不录入任务目标。',117:'16组数据、曲线与灵敏度明示结论。',118:'工作区间与苹果分拣完整原理，核心情境留detail。'}
save('visual_audit.json',{'method':'逐页查看122页原图的双页审阅图；公式、表格与疑点再查整页PNG。PDF文字层仅作候选；最终转录为patches.json。','source_page_count':122,'reviewed_page_count':122,'pages':[{'pdf_page':p,'visual_checked':True,'review_sheet':f'review/pages-{p if p%2 else p-1:03}-{p+1 if p%2 else p:03}.jpg','records':page_map[p],'notes':mixed.get(p,exclude_pages.get(p,'正文、公式、图示与条件已核对。')),'exclusions':exclude_pages.get(p,'无关导语、未解设问、重复表述或纯历史评价按片段排除。')} for p in range(1,123)]})
save('exclusion_audit.json',{'rules':['纯历史生平、年代与评价不单列；混合栏目的物理内容按原位置保留。','练习与应用、复习与提高中未解题排除；不把待证明公式录成已讲解规律。','实验操作保留，未明示的数据、观测与结论不补写。','任务目标、报告要求及自主设计输出要求排除。','重复知识不再次独立录入；必要实验背景、不同条件、不同方法及对比保留。'],'page_decisions':exclude_pages,'special_decisions':[{'pages':[31,32],'decision':'两道楞次定律原例分别为由磁通量变化判电流、由感应电流反推运动；不机械去重。'},{'pages':[20,21,80],'decision':'可自然分离的补充原例放example，完整原题原分析原解。'},{'pages':[22,23,24,36,37,56,57,60,100,108,109,110,111,116,117,118],'decision':'核心装置情境、算式、原例和实验数据留detail，不能拆成孤立知识标题。'},{'pages':[29,30,31],'decision':'表2空白原样保留，不代填方向。'},{'pages':[17,115],'decision':'速度选择器与霍尔电压公式为未解练习，不添加证明或外部公式。'}]})
errors=[]
fields=['knowledge_point_id','chapter','subchapter','section','knowledge_point','detail','example','pdf_page']
if list(rows[0])!=fields:errors.append('field_order')
if not (R/'knowledge_points.csv').read_bytes().startswith(b'\xef\xbb\xbf'):errors.append('bom')
seen=set()
for n,(r,s) in enumerate(zip(rows,src),1):
 k=r['knowledge_point_id']
 if k!=f'RJ-PHYSICS-SEL2-{n:03}' or k in seen:errors.append('id:'+k)
 seen.add(k)
 if any(not r[f] for f in fields if f!='example'):errors.append('empty:'+k)
 if s['knowledge_point_id']!=k:errors.append('source:'+k)
 allowed={z['pdf_page'] for z in s['regions']}|set(s['example_pages'])
 for f in ['detail','example']:
  refs=re.findall(r'!\[page-(\d{3})\]\((images/physics-pep-selective-2/page-\d{3}\.png)\)',r[f])
  paths=[z[1] for z in refs]
  if len(paths)!=len(set(paths)):errors.append('duplicate_image:'+k+f)
  for num,path in refs:
   if int(num) not in allowed or not (R/path).is_file():errors.append('image_source:'+k+path)
   if f'![page-{num}]({path})' not in r[f].splitlines():errors.append('image_line:'+k+f)
  if r[f].count('$')%2:errors.append('math_delimiter:'+k+f)
  if re.search(r'[\u0e00-\u1fff\u2c00-\u2dff\u3100-\u312f\u3300-\u33ff]',r[f].replace('ᵢ','')):errors.append('garbled:'+k)
 if s['source_pdf_sha256']!=info['sha256']:errors.append('source_hash:'+k)
for x in align:
 if not x['records']:errors.append('outline_empty:'+x['section'])
if len(list((R/'images/physics-pep-selective-2').glob('page-*.png')))!=122:errors.append('image_count')
if hashlib.sha256(Path(info['source_pdf']).read_bytes()).hexdigest()!=info['sha256']:errors.append('pdf_changed')
# Exact duplicate prose is flagged for review, not silently merged.
texts=[re.sub(r'!\[.*?\]\(.*?\)','',r['detail']).strip() for r in rows]
if len(set(texts))!=len(texts):errors.append('duplicate_detail')
save('validation_report.json',{'status':'passed' if not errors else 'failed','errors':errors,'records':len(rows),'chapters':5,'textbook_sections':19,'research_records':sum(r['chapter']=='课题研究' for r in rows),'example_fields':sum(bool(r['example']) for r in rows),'solved_original_examples':4,'source_pages':122,'reviewed_pages':122,'full_page_images':122,'sections_with_records':len(align),'source_sha256':info['sha256'],'checks':['UTF-8 BOM与8字段','连续唯一ID','来源记录一一对应','19节及课题研究覆盖','图片存在、来源页、一字段一路径一次及独立行','数学分隔符、乱码','原PDF哈希未变','无完全重复正文'],'content_review':'人工视觉核对记录见visual_audit.json；程序检查不宣称证明全部原文忠实性。'})
changes=[{'action':'create','reason':'按教材细分知识点，视觉核对后首次建立本册独立抽取包','old_id':None,'new_id':r['knowledge_point_id'],'before':None,'after':r,'source_pdf_sha256':info['sha256'],'version':'2026-10-20','recovery':'knowledge_points.csv; patches.json; source_records.jsonl'} for r in rows]
(R/'change_log.jsonl').write_text(''.join(json.dumps(x,ensure_ascii=False)+'\n' for x in changes))
save('id_mapping.json',{'operation':'initial_extraction','previous_records':0,'mapping':[{'old_id':None,'new_id':r['knowledge_point_id'],'knowledge_point':r['knowledge_point']} for r in rows]})
print(json.dumps({'records':len(rows),'errors':errors,'chapter_counts':dict(collections.Counter(r['chapter'] for r in rows))},ensure_ascii=False))
assert not errors
