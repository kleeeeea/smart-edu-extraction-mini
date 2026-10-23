"""Create source, directory, page and exclusion audits; validate the whole book."""
from pathlib import Path
import json,csv,hashlib,re,collections,runpy
R=Path(__file__).resolve().parents[1]
def save(n,o):(R/n).write_text(json.dumps(o,ensure_ascii=False,indent=2))
S=json.loads((R/'selection.json').read_text())
# Last exact footnote and sidebar check; the chemistry notation is that of this edition.
S[35]['detail']+='\n\n① “⇌”表示可逆反应，可逆反应将在第五章介绍。' if '表示可逆反应' not in S[35]['detail'] else ''
for i,t,reg in [(26,'注意：不要用手直接接触钠，而要用镊子夹取！',[39,520,557,56,210]),(27,'注意：不要近距离俯视坩埚！',[40,322,347,391,550]),(28,'注意：不要近距离俯视烧杯！',[41,449,470,355,510])]:
 if t not in S[i-1]['detail']:S[i-1]['detail']+='\n\n'+t;S[i-1]['regions'].append(reg)
if [51,745,755,56,550] not in S[35]['regions']:S[35]['regions'].append([51,745,755,56,550])
# These starts and titles were reread from the textbook; preceding introductory content stays at section level.
for s in S:
 if s['name']=='分散系、分散质、分散剂及分类':s['section']='一、物质的分类'
 if s['name']=='酸、碱、盐性质相似的微观依据':s['section']='二、物质的转化'
 if s['name']=='离子反应与离子方程式的书写':s['section']='二、离子反应'
 if s['name']=='氯化钠溶解、熔化与导电的微观解释':s['section']='一、电解质的电离'
(R/'selection.json').write_text(json.dumps(S,ensure_ascii=False,indent=2))
runpy.run_path(str(R/'scripts/build.py'))
rows=list(csv.DictReader((R/'knowledge_points.csv').open(encoding='utf-8-sig')))
report=json.loads((R/'source_report.json').read_text());pdf=Path(report['source_pdf'])
report.update(local_md5=hashlib.md5(pdf.read_bytes()).hexdigest(),curriculum_revision='普通高中化学课程标准（2017年版）',approval_year=2019,isbn='978-7-107-33574-7',identity_evidence={'cover':'P1：2019审核','title':'P2：普通高中教科书 化学 必修 第一册','curriculum':'P135：依据普通高中化学课程标准（2017年版）编写，2019年审核通过','isbn':'P139：978-7-107-33574-7'},printed_page_offset=-5)
save('source_report.json',report)
web=json.loads((R/'website/ebook_mapping.json').read_text());resource=json.loads((R/'website/resource-v2.json').read_text());srcfile=next(x for x in resource['ti_items'] if x.get('ti_is_source_file'))
titles={7:'绪言',10:'第一章 物质及其变化',11:'第一节 物质的分类及转化',19:'第二节 离子反应',27:'第三节 氧化还原反应',34:'整理与提升',38:'第二章 海水中的重要元素——钠和氯',39:'第一节 钠及其化合物',49:'第二节 氯及其化合物',58:'第三节 物质的量',67:'整理与提升',70:'实验活动1 配制一定物质的量浓度的溶液',72:'第三章 铁 金属材料',73:'第一节 铁及其化合物',83:'第二节 金属材料',92:'整理与提升',95:'实验活动2 铁及其化合物的性质',96:'第四章 物质结构 元素周期律',97:'第一节 原子结构与元素周期表',112:'第二节 元素周期律',118:'第三节 化学键',123:'整理与提升',127:'实验活动3 同周期、同主族元素性质的递变'}
nodes=[]
for n in web['mappings']:
 assert n['page_number'] in titles
 nodes.append(dict(n,depth=n['node_path'].count('/'),pdf_title=titles[n['page_number']],title_evidence='本地PDF P5-P6目录与对应起始页视觉核对',website_title_status='not_present_in_mapping'))
save('outline_alignment.json',dict(resource_id=report['resource_id'],ebook_id=web['ebook_id'],website_title=resource['title'],resource_url='https://basic.smartedu.cn/tchMaterial/detail?contentType=assets_document&contentId='+report['resource_id'],identity_evidence=['资源ID与输入文件名一致','网站源文件大小14050385字节与本地相同','网站front_page=5，目录节点起始页与本地目录及正文一致','本地封面2019审核，P135明确2017年版课标；未套用2022年版初中教材信息'],local_sha256=report['sha256'],local_md5=report['local_md5'],website_source_ti_md5=srcfile['ti_md5'],hash_comparison='网站ti_md5带-2后缀，为分段对象标识，不能直接当作本地MD5；未宣称远端与本地逐字节相同',ordering='章、节、实验活动顺序按网站节点层级与页码；小标题及知识点由教材视觉核实和细分',nodes=nodes,limitations=['网站ebook_mapping不含标题字符串，不能据此宣称逐字核验网站末级名称。具体名称取自本册目录与原页。','附录与折页元素周期表依本地目录、原页补充，未虚构网站节点。']))
sources=[json.loads(t) for t in (R/'source_records.jsonl').read_text().splitlines()];by_page=collections.defaultdict(list)
for s,row,src in zip(S,rows,sources):
 src.update(chapter=row['chapter'],subchapter=row['subchapter'],section=row['section'],knowledge_point=row['knowledge_point'],original_column={'水质检测对象与目的':'化学与职业：水质检验员','菠菜中铁元素的检验实验':'研究与实践：检验食品中的铁元素','同位素在科技考古中的应用':'化学与职业：科技考古研究人员'}.get(s['name'],'见指定原页栏目与regions'),image_placement='所有跨页、跨栏句段合并后统一附图源；同字段同路径仅一次',selected_detail=s['detail'],selected_example=s.get('example',''))
 for p in src['image_pages']:by_page[p].append(row['knowledge_point_id'])
(R/'source_records.jsonl').write_text(''.join(json.dumps(x,ensure_ascii=False)+'\n' for x in sources))
roles={1:'封面及审核标记',2:'扉页',3:'编写人员',4:'栏目说明',5:'目录',6:'目录及栏目索引',7:'绪言',8:'绪言中科学史与评价',9:'绪言中宏微观方法',10:'章引言',38:'章引言',72:'章引言',96:'章引言',47:'研究与实践：生产历史资料搜索与报告任务',82:'未解练习',91:'未解练习',110:'研究与实践：自制周期表及报告任务',111:'未解练习',117:'未解练习',122:'未解练习',123:'整理与提升，重复已收录原理',124:'整理与提升，待填图及重复原理',125:'未解复习题',126:'未解复习题',131:'名词索引（导航）',132:'室温溶解性表',133:'元素中英文名称表',134:'相对原子质量表',135:'后记，课标身份依据',136:'图片来源致谢',137:'空白页',138:'折页元素周期表',139:'封底ISBN'}
exercises={18,25,26,32,33,36,37,48,56,57,66,69,82,91,93,94,111,117,122,125,126}
reviews={34,35,67,68,92,123,124}
audit=[];exclusions=[]
for p in range(1,140):
 role=roles.get(p,'正文、实验及侧栏')
 if p in exercises:role='未解练习或复习题'+('（同页正文另选）' if by_page[p] else '')
 if p in reviews:role='整理复习、重复原理及待填表图'+('（同页实验另选）' if by_page[p] else '')
 why='入选片段以source_records的regions、转录及原图为准；未选任务指标、未解练习、空表答案、历史评价和重复讲解不进入主字段。'
 if not by_page[p]:
  why=role+'；本页无本次应新增的知识记录，或知识已在首讲中收录。'
  exclusions.append(dict(pdf_page=p,scope='whole_page',reason=why))
 audit.append(dict(pdf_page=p,printed_page=p-5 if 7<=p<=134 else None,page_image=f'images/chemistry-pep-hs-compulsory-1/page-{p:03}.png',review_image=f'review/pages-{(p if p%2 else p-1):03}-{min((p if p%2 else p-1)+1,139):03}.jpg',visual_status='reviewed',role=role,record_ids=by_page[p],checks=['正文与侧栏识别','公式、离子电荷与指数','单位、数值与实验用量','反应条件、表格及图示','跨页及跨栏连续句'],exclusion_policy=why))
frags=[(9,'绪言','保留宏微观方法与二氧化硅原例；排除历史评价和学习任务'),(15,'丁达尔效应资料卡片','保留散射解释与波长/直径；排除人名命名历史'),(17,'化学科研工作者','工作描述与绪言研究对象重复，职业要求和评价不录'),(22,'模型','保留模型功能与电离不需通电的对比；排除获奖历史'),(24,'中和反应思考表','保留四组反应情境与下方已讲实质；未填化学方程式不补'),(27,'得失氧分析表','首讲所用反应与后续解释保留，空表不补'),(30,'氧化还原概念发展','其三种标准已由正文首讲完整收录；历史评价不录'),(31,'尾气催化转化','保留CO/NO在催化剂作用下生成CO2/N2明示过程，不补方程式和讨论答案'),(41,'钠与水探究','步骤、图与P42明示结论保留；不填浮熔游响等外部口诀'),(44,'水合碳酸钠','正文与三种水合物脚注保留；不填溶解实验空表'),(45,'侯氏制碱法','保留氨碱法原料与联合生产方式；排除人物经历和评价'),(49,'氯气发现和命名','排除历史命名；性质及数据保留'),(51,'氯水与有色鲜花','保留纸条干湿对比、鲜花实验及原图；不补文字未给实验结果'),(54,'气体制取讨论','装置选择方法已给则保留；NaOH尾气作用为提问，不代答'),(65,'容量瓶误差讨论','保留配液操作及稀释守恒；不代答错误操作后的浓度变化'),(70,'复习题与实验活动1交界','只取实验活动1所给器材及步骤，复习题不录'),(79,'覆铜板探究','给定制作原理和实验保留；不补Cu与FeCl3方程式'),(81,'检验食品中的铁','仅菠菜已有步骤保留，不补红色结果及研究任务'),(85,'测试工程师','保留成分检测方法与技术实例；排除职业要求'),(86,'超级钢','保留合金配方与性能；排除科研历史及评价'),(89,'稀土元素','保留定义、组成与用途；排除资源产量评价'),(95,'实验活动2','器材及所给步骤全部保留，不补实验现象；KI和淀粉提示是明示内容'),(99,'原子模型史','只取模型定义和现代电子云说明，不把历史模型作为现行结论'),(102,'科技考古','保留C14衰变测年和C13/N15分析食物结构；排除奖项和职业评价'),(103,'周期表历史','重复分类信息和纯历史不再录'),(104,'碱金属空表','原子半径及结构示意留原图；不补空格'),(108,'卤素性质空表','保留已给四组反应事实和条件，不补待推断项'),(113,'周期性质空表','保留已给表4-5数据原图；不补空白结论'),(114,'第三周期探究','保留全部给定实验、两性反应式和水化物酸性表；不补预测和结论空格'),(116,'门捷列夫预言','纯历史预言与验证不独立录；正文周期律应用完整保留'),(127,'实验活动3','保留点滴实验已有步骤及器材；要求自行设计的镁/水、氢氧化物实验不代拟'),(131,'索引','仅导航，与已有知识重复'),(138,'折页周期表','字体编码异常，不使用文字层候选代替二维原表')]
exclusions.extend(dict(pdf_page=p,scope=scope,reason=reason) for p,scope,reason in frags)
save('visual_audit.json',dict(total_pages=139,reviewed_pages=139,method='逐页查看渲染图；化学式、用量、表格与跨页/跨栏重点二次核对。文字层仅候选，复杂二维结构保留原图。',pages=audit))
save('page_map.json',audit);save('exclusions.json',exclusions)
save('id_map.json',[dict(old_id=None,new_id=r['knowledge_point_id'],knowledge_point=r['knowledge_point'],reason='独立新分册首次抽取，按教材顺序连续编号') for r in rows])
save('changes.json',dict(action='initial_full_book_extraction',source_sha256=report['sha256'],records=len(rows),existing_book_outputs_modified=False,description='新建独立分册，按教材细分知识点、合并跨页句并视觉校正式子、离子电荷及条件；空表及未给实验结果不补；完整核心讲解与首次原例原解放detail。',record_snapshots=rows))
fields=['knowledge_point_id','chapter','subchapter','section','knowledge_point','detail','example','pdf_page'];assert list(rows[0])==fields
assert (R/'knowledge_points.csv').read_bytes().startswith(b'\xef\xbb\xbf')
assert len(rows)==len(S)==len(sources)==116
assert [x['knowledge_point_id'] for x in rows]==[f'RJ-CHEMISTRY-HSC1-{i:03}' for i in range(1,len(rows)+1)]
assert len({x['knowledge_point'] for x in rows})==len(rows)
for row,s,src in zip(rows,S,sources):
 assert all(row[k].strip() for k in fields if k!='example')
 assert src['selected_detail']==s['detail']
 assert row['detail'].split('\n\n![page-')[0].strip()==s['detail'].strip()
 assert not any(ord(c)<32 and c not in '\n\r\t' for c in row['detail'])
 for k in ['detail','example']:
  refs=re.findall(r'!\[page-(\d{3})\]\((images/chemistry-pep-hs-compulsory-1/page-\d{3}\.png)\)',row[k]);assert len(refs)==len(set(t[1] for t in refs))
  for p,path in refs:assert (R/path).is_file() and path.endswith(f'page-{p}.png')
  for l in row[k].splitlines():
   if '![' in l:assert re.fullmatch(r'!\[page-\d{3}\]\(images/chemistry-pep-hs-compulsory-1/page-\d{3}\.png\)',l)
 assert set(int(x) for x in re.findall(r'!\[page-(\d{3})\]',row['detail']))==set(src['image_pages'])
 assert all(1<=a[0]<=139 for a in src['regions'])
 ps=sorted(set(src['image_pages']));groups=[]
 for p in ps:
  if groups and p==groups[-1][-1]+1:groups[-1].append(p)
  else:groups.append([p])
 label=';'.join(f'P{g[0]}' if len(g)==1 else f'P{g[0]}-P{g[-1]}' for g in groups)
 assert row['pdf_page']==label
assert hashlib.sha256(pdf.read_bytes()).hexdigest()==report['sha256']
assert len(audit)==139 and all((R/a['page_image']).is_file() and (R/a['review_image']).is_file() for a in audit)
checks={15:['SO₄²⁻','H₃O⁺'],27:['─△→','Na₂O₂'],36:['⇌','25 ℃'],44:['6.02×10²³','N/N_A','1.204×10²⁴'],46:['26.5 g','106 g·mol⁻¹','0.25 mol'],48:['22.4','24.5','101 kPa'],49:['n_B/V','单位体积'],52:['2~3','1~2','分析天平'],57:['高温','H₂O(g)'],73:['2Na[Al(OH)₄]','6H₂O'],77:['0.50 mol','11.2 L'],84:['¹⁴₆C','²³⁸₉₂U'],92:['⇌','不断加热'],97:['[Al(OH)₄]⁻','HClO₄']}
for i,terms in checks.items():assert all(t in rows[i-1]['detail'] for t in terms),(i,terms)
save('validation.json',dict(status='passed',records=len(rows),pdf_pages=139,visually_reviewed=139,chapter_counts=dict(collections.Counter(r['chapter'] for r in rows)),checks=['八字段及UTF-8 BOM','连续唯一ID与来源映射','必填正文与selected_detail一致','139页图源和审阅图存在','图片独立行、页号一致、同字段同路径去重','物理页范围与来源和图片一致','PDF SHA256未变','电离式、可逆反应、分式、标准状况、配液用量、四羟基合铝酸盐和核素符号回归检查','原文回读、关键式子及跨页/跨栏视觉复核'],limitations=['网站目录映射没有标题文字，不能声称逐字核验平台末级标题；名称与细分依本册教材原页。','二维电子式、部分完整表格及折页周期表保留源图。','程序结构校验不替代视觉核验。']))
md=['# 人教版高中化学必修第一册\n\n全册116条记录；教材身份、目录对齐和核验范围见 [README](README.md)。\n']
for r in rows:
 md.append(f"## {r['knowledge_point_id']} {r['knowledge_point']}\n\n{r['chapter']} / {r['subchapter']} / {r['section']} · {r['pdf_page']}\n\n{r['detail']}\n")
 if r['example']:md.append('### 补充原例与原解\n\n'+r['example'])
(R/'knowledge_points.md').write_text('\n'.join(md))
print(json.dumps({'records':len(rows),'pages':139,'validation':'passed'},ensure_ascii=False))
