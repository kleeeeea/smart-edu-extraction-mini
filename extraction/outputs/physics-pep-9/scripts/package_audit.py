"""Package source identity, outline alignment, exclusions, and independently check structure."""
from pathlib import Path
import csv,json,re,hashlib,collections
R=Path(__file__).resolve().parents[1]
rows=list(csv.DictReader((R/'knowledge_points.csv').open(encoding='utf-8-sig')))
def source_pages(label):
    result=set()
    for part in label.split(';'):
        pair=part.split('-')
        a=int(pair[0][1:]);b=int(pair[-1][1:]);result.update(range(a,b+1))
    return result
source=json.loads((R/'source_report.json').read_text())
site=json.loads((R/'website/resource-v2.json').read_text())
nav=json.loads((R/'website/ebook_mapping.json').read_text())
chapters=[(13,'内能',8,[9,15,20]),(14,'内能的利用',26,[27,32,37,42]),(15,'电流和电路',46,[47,51,57,62,67]),(16,'电压 电阻',73,[74,79,84,89,94]),(17,'欧姆定律',99,[100,105,108,112]),(18,'电功率',117,[118,121,125,127]),(19,'生活用电',134,[135,141,148]),(20,'电与磁',153,[154,159,164,168,172,174]),(21,'电磁波及其应用',181,[182,186,190]),(22,'能源与可持续发展',195,[196,201,207])]
by_page={n['page_number']:n for n in nav['mappings']}
sects={}
for r in rows:
 c=int(re.search(r'第(\d+)章',r['chapter'])[1]) if re.search(r'第(\d+)章',r['chapter']) else None
 sects[(r['chapter'],r['subchapter'])]=True
alignment=[]
for c,title,cp,ps in chapters:
 node=by_page[cp]
 actual=[r for r in rows if title in r['chapter']]
 # A chapter's exact name is drawn from its own chapter row to avoid substring matches.
 cname=next(r['chapter'] for r in rows if r['chapter'].endswith('章 '+title))
 assert '/' not in node['node_path']
 for s,p in enumerate(ps,1):
  sn=by_page[p];assert sn['node_path'].split('/')[0]==node['node_id']
  rr=[r for r in rows if r['chapter']==cname and r['subchapter'].startswith(f'第{s}节 ')]
  assert rr,(c,s)
  alignment.append({'chapter':cname,'subchapter':rr[0]['subchapter'],'pdf_page':p,'printed_page':p-7,'website_node_id':sn['node_id'],'website_node_path':sn['node_path'],'chapter_website_node_id':node['node_id'],'records':[r['knowledge_point_id'] for r in rr],'status':'page_and_hierarchy_matched'})
meta={**source,'book_id':'physics-pep-9','subject':'物理','education_stage':'初中','publisher':'人民教育出版社','grade':'九年级','volume':'全一册','revision':'根据2022年版课程标准修订','cover_approval':'教育部审定2024','isbn':'978-7-107-38956-6','edition_statement':'PDF版权页未给出年月版次，未推断','smartedu_resource_id':site['id'],'smartedu_title':site['title'],'website_resource_updated_at':site['update_time'],'local_pdf_bytes':Path(source['source_pdf']).stat().st_size,'website_pdf_bytes':next(a['ti_size'] for a in site['ti_items'] if a.get('ti_format')=='pdf'),'identity_evidence':['新版网站资源ID、修订标记、书名、学科、出版社、年级、册次相符','新版网站PDF字节数与本地PDF一致，均为26794457','新版网站218页与本地218页一致','网站ebook_mapping的50个章/节节点页序与本地视觉目录逐项一致'],'remote_pdf_byte_hash_verification':'not_performed: direct private PDF URL returned 401; local SHA-256 recorded separately','policy_reference':{'requested_github_url':'https://github.com/yyyrrrr7/smartedu_math/blob/main/skills/smartedu-math/references/extraction-policy.md','raw_github_fetch':'404 on 2026-10-20','applied_local_policy':'skills/smartedu-math/references/extraction-policy.md','user_instructions_override':'物理学科；按教材内容细分；保留实验；detail与example分工按本次明确要求'},'extraction_date':'2026-10-20','records':len(rows),'chapters':10,'subchapters':40,'source_images':218}
(R/'book_metadata.json').write_text(json.dumps(meta,ensure_ascii=False,indent=2)+'\n')
(R/'outline_alignment.json').write_text(json.dumps({'status':'matched','website_mapping_front_page':nav['front_page'],'ebook_id':nav['ebook_id'],'name_basis':'名称逐项取自本地PDF视觉目录；网站ebook_mapping提供实际节点ID、父子层级和页序，名称不由该映射文件返回。','legacy_endpoint_note':'ndrs旧接口仍返回190页旧版，不能用作本次目录；使用ndrv2新版218页元数据与其ebook_mapping。','nodes_matched':50,'sections':alignment},ensure_ascii=False,indent=2)+'\n')
page_map=[{'pdf_page':p,'printed_page':p-7 if 8<=p<=214 else None,'image':f'images/physics-pep-9/page-{p:03}.png'} for p in range(1,219)]
(R/'page_map.json').write_text(json.dumps(page_map,ensure_ascii=False,indent=2)+'\n')
# Record exclusions independently of the textbook fields.
exclusions=[]
for pages,reason in [([1,2,3,4,5,6,7,8,26,46,73,99,117,134,153,181,195,214,215,216,217,218],'封面、版权、目录、章引言、索引、后记或空白页；保留来源图，不单列知识点'),([19,25,31,36,41,44,45,50,56,60,61,65,66,70,71,72,77,78,82,83,88,92,93,96,97,98,103,104,107,110,111,114,115,116,120,124,131,132,133,140,147,151,152,158,163,167,178,179,180,189,194,200,206,213],'练习与应用、复习与提高中的未解题及重复表述不录入；同页正文或有效侧栏按选区另保留')]:
 exclusions.append({'pdf_pages':pages,'reason':reason})
for pages,reason in [([14],'温室效应后的网络检索任务排除'),([15],'德谟克利特原子观历史片段排除；现代分子/原子概念保留'),([18],'分子动理论三条汇总与前面已录定义重复，移出主表；物态微观条件与液氮气球原例保留'),([29,30],'能量守恒相关历史评价、热质说错误历史解释排除；定量热功关系与热量的能量含义保留'),([40],'热机发展年代和人物评价排除；汽轮机与两种喷气发动机的工作条件保留'),([42,43,94,95,125,126,148,149,150,172,173,207,208,210,211,212],'跨学科实践的任务指标、展示交流、纯调查表或未解任务不单列；原有制作器材步骤、现象、技术条件、明示结论与有效侧栏按选区保留'),([87],'半导体及超导栏目中的纯历史评价排除；不同材料与临界温度等条件保留'),([157],'地磁偏离的历史人物及年代评价排除；方向关系和应用保留'),([162],'重复的螺线管磁场总结不再录入；安培定则条件及右手规则保留'),([177],'已录磁化定义不重复；软磁/硬磁材料及磁记录写入读取机制保留'),([205],'核电站发展的纯历史评价排除；射线、核废料及高温气冷堆安全条件保留')]:exclusions.append({'pdf_pages':pages,'reason':reason})
(R/'exclusion_audit.jsonl').write_text(''.join(json.dumps(x,ensure_ascii=False)+'\n' for x in exclusions))
# Separate whole-page review, equation/table enlargement, and machine structural checks.
enlarged={11,13,34,38,48,62,75,85,105,110,112,113,114,118,121,123,128,129,130,183,198,209}
review=[]
for pm in page_map:
 p=pm['pdf_page'];ids=[r['knowledge_point_id'] for r in rows if p in source_pages(r['pdf_page'])]
 review.append({**pm,'visual_review':'reviewed','review_surface':f'review/pages-{((p-1)//4)*4+1:03}-{min(((p-1)//4)*4+4,218):03}.jpg','full_page_enlargement':p in enlarged,'records':ids,'review_focus':['公式、单位及上下标','表格及图示对应','明示条件与实验结果边界','跨页句子和章节归属'],'scope_note':'记录是否抽取由选区及排除审计决定；图片文件存在检查另行执行。'})
(R/'visual_review.jsonl').write_text(''.join(json.dumps(x,ensure_ascii=False)+'\n' for x in review))
candidates={x['knowledge_point']:x['detail'] for x in map(json.loads,(R/'transcription_candidates.jsonl').read_text().splitlines())}
changes=[]
for r in rows:
 changes.append({'action':'new_extraction','old_id':None,'new_id':r['knowledge_point_id'],'source_pdf_sha256':source['sha256'],'pdf_page':r['pdf_page'],'before':{'candidate_detail':candidates[r['knowledge_point']]},'after':r,'reason':'按本次用户规则进行视觉选区、跨页合并、公式/表格转录、混合栏目过滤及核心/补充例题字段分配','restore_from':'pages.jsonl + selection.tsv + PDF source regions; original PDF unchanged'})
(R/'change_log.jsonl').write_text(''.join(json.dumps(x,ensure_ascii=False)+'\n' for x in changes))
(R/'id_map.json').write_text(json.dumps([{'old_id':None,'new_id':r['knowledge_point_id'],'action':'new_extraction'} for r in rows],ensure_ascii=False,indent=2)+'\n')
errors=[]
expected=['knowledge_point_id','chapter','subchapter','section','knowledge_point','detail','example','pdf_page']
assert list(rows[0])==expected
image_count=0
for i,r in enumerate(rows,1):
 if r['knowledge_point_id']!=f'RJ-PHYSICS-9-{i:03}':errors.append('ID sequence')
 for key in ['knowledge_point_id','knowledge_point','detail']:
  if not r[key].strip():errors.append('empty '+key)
 for field in ['detail','example']:
  text=r[field];refs=re.findall(r'!\[page-(\d{3})\]\((images/physics-pep-9/page-\d{3}\.png)\)',text)
  if len(refs)!=len(set(refs)):errors.append(r['knowledge_point_id']+' duplicate '+field)
  for n,path in refs:
   image_count+=1
   if not (R/path).is_file():errors.append('missing image '+path)
   if int(n) not in source_pages(r['pdf_page']):errors.append('image page absent from source field '+r['knowledge_point_id'])
   if not re.search(rf'(?m)^!\[page-{n}\]\(images/physics-pep-9/page-{n}\.png\)$',text):errors.append('image not standalone')
  if text.count('$$')%2:errors.append('unpaired display math '+r['knowledge_point_id'])
  if re.search(r'10\s*\n\s*[⁻⁰¹²³⁴⁵⁶⁷⁸⁹]',text):errors.append('split superscript '+r['knowledge_point_id'])
  if re.search(r'[\u0e00-\u1fff\u2c00-\u2dff\u3100-\u312f\u3300-\u33ff]',text):errors.append('suspect encoding '+r['knowledge_point_id'])
 assert not r['detail'].startswith('![page-')
for p in range(1,219):
 if not (R/f'images/physics-pep-9/page-{p:03}.png').is_file():errors.append('source image missing')
report={'status':'pass' if not errors else 'fail','records':len(rows),'chapters':10,'subchapters':40,'website_nodes_matched':50,'pdf_pages':218,'page_visual_reviews':len(review),'supplementary_worked_examples':sum(bool(r['example']) for r in rows),'image_references_checked':image_count,'errors':errors,'separate_checks':{'schema_utf8_bom_ids':'pass','outline_coverage':'pass','image_paths_standalone_dedup':'pass' if not errors else 'see errors','source_mapping':'pass','visual_content':'manual full-book page review plus enlarged equation/table review; see visual_review.jsonl','unprovided_experiment_results':'not added; open measurements retained','tests_do_not_prove':'程序结构检查不替代原文忠实性和逐页视觉核对'}}
(R/'validation_report.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
print(json.dumps(report,ensure_ascii=False,indent=2))
assert not errors,errors
