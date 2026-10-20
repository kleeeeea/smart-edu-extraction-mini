"""Build provenance and validate the standalone Grade 8 first-volume extraction."""
from pathlib import Path
import csv,json,re,hashlib,collections
R=Path(__file__).resolve().parents[1]
def save(name,value): (R/name).write_text(json.dumps(value,ensure_ascii=False,indent=2)+'\n')
def jsonl(name,values): (R/name).write_text(''.join(json.dumps(v,ensure_ascii=False)+'\n' for v in values))
rows=list(csv.DictReader((R/'knowledge_points.csv').open(encoding='utf-8-sig')))
source=json.loads((R/'source_report.json').read_text());site=json.loads((R/'website/resource-v2.json').read_text());nav=json.loads((R/'website/ebook_mapping.json').read_text());patches=json.loads((R/'patches.json').read_text())
sha=hashlib.sha256(Path(source['source_pdf']).read_bytes()).hexdigest();assert sha==source['sha256']
chapters=[(0,'开启科学探索之旅',8,[8]),(1,'机械运动',17,[18,24,27,32]),(2,'声现象',38,[39,44,51,56,60]),(3,'物态变化',64,[65,71,77,84,88]),(4,'光现象',94,[95,100,105,110,114]),(5,'透镜及其应用',120,[121,125,129,133,137]),(6,'质量与密度',145,[146,151,156,159])]
nodes=[];idx=0
for c,title,cp,pages in chapters:
 cn=title if not c else f'第{["","一","二","三","四","五","六"][c]}章 {title}'
 parent=nav['mappings'][idx];idx+=1;assert parent['page_number']==cp and '/' not in parent['node_path']
 nodes.append({**parent,'local_title':cn,'local_pdf_page':cp,'name_basis':'PDF目录视觉核对','status':'page_and_hierarchy_matched'})
 for sn,p in enumerate(pages,1):
  node=nav['mappings'][idx];idx+=1;assert node['page_number']==p and node['node_path'].split('/')[0]==parent['node_id']
  rr=[r for r in rows if r['chapter']==cn and (not c or r['subchapter'].startswith(f'第{sn}节 '))];assert rr,(c,sn)
  nodes.append({**node,'local_title':rr[0]['subchapter'],'local_pdf_page':p,'records':[r['knowledge_point_id'] for r in rr],'name_basis':'PDF目录视觉核对','status':'page_and_hierarchy_matched'})
assert idx==len(nav['mappings'])==36
save('outline_alignment.json',{'status':'matched','website_resource_url':f"https://s-file-1.ykt.cbern.com.cn/zxx/ndrv2/resources/tch_material/details/{site['id']}.json",'ebook_id':nav['ebook_id'],'front_page':nav['front_page'],'nodes_matched':36,'name_basis':'网站 ebook_mapping 返回节点ID、父子层级与页序，不返回名称；名称取自同版本地PDF目录的逐页视觉核对。引言根节点和子节点同在P8，分别保留。','nodes':nodes})
meta={**source,'book_id':'physics-pep-8a','education_stage':'初中','subject':'物理','publisher':'人民教育出版社','grade':'八年级','volume':'上册','revision':'根据2022年版课程标准修订','cover_approval':'国家教材委员会专家委员会审核通过2024','isbn':'978-7-107-38258-1','edition_statement':'PDF版权页未明示年月版次，不推断','smartedu_resource_id':site['id'],'smartedu_title':site['title'],'website_resource_updated_at':site['update_time'],'local_pdf_bytes':Path(source['source_pdf']).stat().st_size,'website_pdf_bytes':next(a['ti_size'] for a in site['ti_items'] if a.get('ti_format')=='pdf'),'identity_evidence':['资源ID、修订标记、出版社、书名、年级与册次对应','网站PDF字节数与本地一致：19970967','网站36个目录节点的页序与父子层级全部对应本地目录'],'remote_pdf_hash_verification':'not_performed; local SHA-256 retained','extraction_date':'2026-10-20','records':len(rows),'chapters':6,'subchapters':28,'introduction_records':sum(r['chapter']=='开启科学探索之旅' for r in rows),'source_images':170,'policy':{'local_skill':'skills/smartedu-math/SKILL.md','local_policy':'skills/smartedu-math/references/extraction-policy.md','requested_github_policy':'https://github.com/yyyrrrr7/smartedu_math/blob/main/skills/smartedu-math/references/extraction-policy.md','remote_policy_status':'raw URL returned 404 in prior task; local policy applied','user_override':'适用于物理；按教材内容细分知识点；实验忠实转录；核心讲解与补充原例分工按本次要求'},'rendering':{'engine':'PyMuPDF','matrix':1.7,'image_type':'whole_page','crop':False}}
assert meta['local_pdf_bytes']==meta['website_pdf_bytes']==19970967
save('book_metadata.json',meta)
def page_set(label):
 out=set()
 for part in label.split(';'):
  a=part.split('-');out.update(range(int(a[0][1:]),int(a[-1][1:])+1))
 return out
sources=list(map(json.loads,(R/'source_records.jsonl').read_text().splitlines()))
for s in sources:
 p=patches.get(s['knowledge_point'],{});s['visual_correction']=s['knowledge_point'] in patches
 s['example_regions']=[{'pdf_page':a,'printed_page':a-7,'bbox':[0,b,521.575,c]} for a,b,c in p.get('example_regions_audit',[])]
 s['image_type']='whole_page';s['field_pages']={f:sorted(set(map(int,re.findall(r'!\[page-(\d+)\]',r[f])))) for r in rows if r['knowledge_point_id']==s['knowledge_point_id'] for f in ['detail','example']}
jsonl('source_records.jsonl',sources)
page_map=[{'pdf_page':p,'printed_page':p-7 if 8<=p<=166 else None,'image':f'images/physics-pep-8a/page-{p:03}.png'} for p in range(1,171)];save('page_map.json',page_map)
notes={9:'两项演示仅保留教材步骤，不补气压或电动机原理',15:'摆实验条件与原文一致，不外加小角度条件',19:'长度单位指数、量程脚注与跨页句子',22:'秒表空白不填；时间表指数核对',28:'v=s/t、组合单位及速度表逐项核对，出膛子弹约1000 m/s',29:'两车10s间隔、不同路程图保留；匀速与变速对比',30:'100m/9.83s=10.2m/s，作为补充原例',33:'小车不同区间无教材实测值，不补结果',42:'声速表介质温度条件及回声大于0.1s',46:'听觉频率范围、超声波和次声波阈值及图表',66:'摄氏温度标准大气压条件与负号',72:'海波与石蜡的器材步骤和明示温度规律',74:'标准大气压熔点表及晶体/非晶体曲线',78:'沸腾实验0.5min记录，沸腾4~5min，表格空白',79:'沸点表标准大气压；不混同沸点与所有汽化温度',82:'制冷剂循环及热棒冷暖季条件',86:'水循环跨页句子先合并；水资源百分比分母',98:'精确光速、近似光速、水中3/4c和玻璃中2/3c',101:'反射角空表不填；折纸板检验共面',106:'同形未点燃蜡烛找像，光屏不承接虚像',111:'斜射/垂直入射条件及折射光路可逆',116:'红外线与紫外线跨页句子，安全侧栏后附',130:'发光物体、透镜、光屏中心同高；空表不填',131:'四种物距条件按教材明示结论，不补焦点处结论',135:'Φ=1/f；0.5m对应2m⁻¹；度数正负',139:'望远镜不同远近的镜片间距条件及20cm/10cm镜片',149:'左物右码、游码左端及天平调节规则',153:'三种密度表数值、指数与温压条件',154:'铝棒原例54kg；水4℃密度最大',156:'盐水实验m₁−m₂表头条件，不填数据',157:'不吸水条件、量筒排水图、不补实验结果',159:'巨石原例跨页完整，42.6m³、119.3t按原书近似值',160:'金箔0.15μm及无损耗条件、5.2×10⁻⁷m³、3.5m²',161:'实心铅球的密度计算、不同物质密度可能相同',162:'保留青铜与气凝胶物性，排除纯发展史评价'}
review=[]
for pm in page_map:
 p=pm['pdf_page'];review.append({**pm,'visual_review':'reviewed','review_surface':f'review/pages-{((p-1)//2)*2+1:03}-{((p-1)//2)*2+2:03}.jpg','records':[r['knowledge_point_id'] for r in rows if p in page_set(r['pdf_page'])],'review_note':notes.get(p,'逐页检查正文、图示、表格、条件与跨页；录入与排除依据见选区和排除审计。'),'verification_basis':'page image visually viewed; PDF text is a candidate only'})
jsonl('visual_review.jsonl',review)
ex=[{'pdf_pages':[1,2,3,4,5,6,7,8,16,17,38,64,94,120,145,166,167,168,169,170],'reason':'封面、目录、寄语、纯引言评价、索引、后记、空白或封底；保留页图与身份信息，不单列知识点'}, {'pdf_pages':[11,12,13,14,15],'reason':'纯科普评价、学习任务与历史人物评价排除；P14科学探究情境与P15摆实验有效内容另保留'}, {'pdf_pages':[35,36,37,62,63,91,92,93,118,119,143,144,164,165],'reason':'章小结中的重复知识与复习提高的未解题不再收录'}, {'pdf_pages':[23,26,30,31,34,43,50,55,57,58,59,60,61,69,70,74,75,76,83,87,88,89,90,99,103,104,109,113,117,124,128,131,132,135,136,137,140,141,142,149,150,155,158,162,163],'reason':'混合页：练习、开放问题、展示交流、任务指标、纯历史评价等片段排除；同页有效正文、实验与侧栏按source_records选区保留'}, {'pdf_pages':[50,63,70,87,109,113,117,124,132,136,143,144,150,155,158,163,164,165],'reason':'未解练习不提供答案。实验栏内待测数据与待总结空白照录；P87结霜实验保留教材明确器材步骤和现象。'}, {'pdf_pages':[89,90],'reason':'厨房实践保留食用油与水沸点差异以及煮饺子火力调整完整讲解；表内已讲过的沸腾/液化示例不重复。'}, {'pdf_pages':[141,142,150,157,162],'reason':'望远镜发展史、千克由来及材料发展史的纯人物年代评价排除；银河系组成、密度差异实验事实、青铜和气凝胶物性分别保留。'}]
jsonl('exclusion_audit.jsonl',ex)
candidates={q['knowledge_point']:q['detail'] for q in map(json.loads,(R/'transcription_candidates.jsonl').read_text().splitlines())}
jsonl('change_log.jsonl',[{'action':'new_extraction','old_id':None,'new_id':r['knowledge_point_id'],'source_pdf_sha256':sha,'pdf_page':r['pdf_page'],'before':{'candidate_detail':candidates[r['knowledge_point']]},'after':r,'reason':'按视觉选区抽取、公式及表格校正、跨页合并、去重与字段分配；教材未给出的实验结果不补充','restore_from':'原PDF、pages.jsonl、selection.tsv、patches.json'} for r in rows])
save('id_map.json',[{'old_id':None,'new_id':r['knowledge_point_id'],'action':'new_extraction'} for r in rows])
errors=[];refs_count=0
fields=['knowledge_point_id','chapter','subchapter','section','knowledge_point','detail','example','pdf_page'];assert list(rows[0])==fields
for i,r in enumerate(rows,1):
 if r['knowledge_point_id']!=f'RJ-PHYSICS-8A-{i:03}':errors.append('ID order')
 if not all(r[f].strip() for f in fields if f!='example'):errors.append('empty required field')
 for field in ['detail','example']:
  text=r[field];refs=re.findall(r'!\[page-(\d{3})\]\((images/physics-pep-8a/page-\d{3}\.png)\)',text);refs_count+=len(refs)
  if len(refs)!=len(set(refs)):errors.append('duplicate image '+r['knowledge_point_id'])
  for n,path in refs:
   if not (R/path).is_file() or int(n) not in page_set(r['pdf_page']):errors.append('image source '+r['knowledge_point_id'])
   if f'page-{n}.png'!=Path(path).name:errors.append('image label')
   if not re.search(rf'(?m)^!\[page-{n}\]\({re.escape(path)}\)$',text):errors.append('image not standalone')
  if re.search(r'\^\{|_\{|10\s*\n\s*[⁻⁰¹²³⁴⁵⁶⁷⁸⁹]',text):errors.append('unresolved superscript '+r['knowledge_point_id'])
  if re.search(r'[\u0e00-\u1fff\u2c00-\u2dff\u3100-\u312f\u3300-\u33ff]',text):errors.append('encoding '+r['knowledge_point_id'])
 if not re.sub(r'!\[[^]]*\]\([^)]*\)','',r['detail']).strip():errors.append('image-only detail')
 assert page_set(r['pdf_page'])==set(sources[i-1]['field_pages']['detail']+sources[i-1]['field_pages']['example'])
assert (R/'knowledge_points.csv').read_bytes().startswith(b'\xef\xbb\xbf')
assert len({r['knowledge_point_id'] for r in rows})==len(rows)
for pm in page_map:assert (R/pm['image']).is_file()
report={'status':'pass' if not errors else 'fail','records':len(rows),'chapters':6,'subchapters':28,'introduction':True,'website_nodes_matched':36,'pdf_pages':170,'page_visual_reviews':len(review),'supplementary_worked_examples':sum(bool(r['example']) for r in rows),'image_references_checked':refs_count,'source_records':len(sources),'errors':errors,'checks':{'csv_schema_bom_ids':'pass','website_page_hierarchy_and_outline_coverage':'pass','image_paths_standalone_dedup':'pass' if not errors else 'see errors','physical_page_mapping':'pass','formula_table_conditions':'visual transcription; see patches.json and visual_review.jsonl','experiment_results':'only textbook-stated results; blank observations not filled'},'limitation':'结构检查不替代视觉核对；网站映射未返回名称，名称依据本地同版目录；未取得远端PDF哈希。'}
save('validation_report.json',report);print(json.dumps(report,ensure_ascii=False,indent=2));assert not errors,errors
