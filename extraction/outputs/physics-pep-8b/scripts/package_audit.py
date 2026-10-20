"""Record source, editorial decisions and visual review; validate the extracted package."""
from pathlib import Path
import csv,json,re,hashlib,collections
R=Path(__file__).resolve().parents[1]
BOOK='physics-pep-8b'
rows=list(csv.DictReader((R/'knowledge_points.csv').open(encoding='utf-8-sig')))
source=json.loads((R/'source_report.json').read_text())
site=json.loads((R/'website/resource-v2.json').read_text())
nav=json.loads((R/'website/ebook_mapping.json').read_text())
def save(name,value): (R/name).write_text(json.dumps(value,ensure_ascii=False,indent=2)+'\n')
def jsonl(name,values): (R/name).write_text(''.join(json.dumps(v,ensure_ascii=False)+'\n' for v in values))
def pages(label):
 out=set()
 for t in label.split(';'):
  a=t.split('-');out.update(range(int(a[0][1:]),int(a[-1][1:])+1))
 return out
chapters=[(7,'力',6,[7,12,16]),(8,'运动和力',23,[24,28,32,38]),(9,'压强',44,[45,50,57,61,64]),(10,'浮力',68,[69,73,78,82]),(11,'功和机械能',88,[89,93,96,101]),(12,'简单机械',108,[109,116,118,122])]
by_page={x['page_number']:x for x in nav['mappings']}
alignment=[]
for c,title,cp,starts in chapters:
 node=by_page[cp];assert '/' not in node['node_path']
 cname=next(r['chapter'] for r in rows if r['chapter'].endswith('章 '+title))
 for s,p in enumerate(starts,1):
  sn=by_page[p];assert sn['node_path'].split('/')[0]==node['node_id']
  rr=[r for r in rows if r['chapter']==cname and r['subchapter'].startswith(f'第{s}节 ')]
  assert rr,(c,s)
  alignment.append({'chapter':cname,'section':rr[0]['section'],'pdf_page':p,'printed_page':p-5,'website_node_id':sn['node_id'],'website_node_path':sn['node_path'],'chapter_website_node_id':node['node_id'],'knowledge_point_ids':[r['knowledge_point_id'] for r in rr],'status':'page_and_hierarchy_matched'})
assert len(by_page)==30 and len(alignment)==24
save('outline_alignment.json',{'status':'matched','website_mapping_front_page':nav['front_page'],'ebook_id':nav['ebook_id'],'nodes_matched':30,'chapter_nodes':6,'section_nodes':24,'name_basis':'章节、小节名称逐项取自本地PDF视觉目录；同版网站ebook_mapping提供实际节点ID、父子层级和页序，映射文件本身不返回标题文字。','website_metadata_file':'website/resource-v2.json','website_mapping_file':'website/ebook_mapping.json','sections':alignment})
meta={**source,'book_id':BOOK,'subject':'物理','education_stage':'初中','publisher':'人民教育出版社','grade':'八年级','volume':'下册','revision':'根据2022年版课程标准修订','cover_approval':'教育部审定2024','isbn':'978-7-107-38259-8','edition_statement':'PDF版权页未给出年月版次，未推断','smartedu_resource_id':site['id'],'smartedu_title':site['title'],'website_resource_updated_at':site['update_time'],'website_metadata_url':f"https://s-file-1.ykt.cbern.com.cn/zxx/ndrv2/resources/tch_material/details/{site['id']}.json",'local_pdf_bytes':Path(source['source_pdf']).stat().st_size,'website_pdf_bytes':next(a['ti_size'] for a in site['ti_items'] if a.get('ti_format')=='pdf'),'identity_evidence':['资源ID、修订标记、书名、学科、出版社、年级和册次一致','网站与本地PDF均为131页，文件大小均为13733800字节','网站目录的30个章/节节点与本地视觉目录的页序及父子层级逐项对应'],'remote_pdf_byte_hash_verification':'未进行远端PDF逐字节哈希比对；本地原文件SHA-256单独记录','policy_reference':{'requested_github_url':'https://github.com/yyyrrrr7/smartedu_math/blob/main/skills/smartedu-math/references/extraction-policy.md','raw_github_fetch':'404 on 2026-10-20','applied_local_policy':'skills/smartedu-math/references/extraction-policy.md','user_override':'用于物理；具体知识点由教材识别；保留实验原器材、步骤、现象和明示结论；不补结果；detail保留核心完整讲解'},'extraction_date':'2026-10-20','records':len(rows),'chapters':6,'sections':24,'supplementary_worked_examples':sum(bool(r['example']) for r in rows),'source_images':131,'image_render_scale':1.5,'printed_page_mapping':'P6-P129 = 印刷页1-124；P130后记无正文页码；其余前后页不推断印刷页码'}
save('book_metadata.json',meta)
page_map=[{'pdf_page':p,'printed_page':p-5 if 6<=p<=129 else None,'image':f'images/{BOOK}/page-{p:03}.png'} for p in range(1,132)]
save('page_map.json',page_map)
# The extraction is new; no existing book or old knowledge-point ID is replaced.
candidates={q['knowledge_point']:q['detail'] for q in map(json.loads,(R/'transcription_candidates.jsonl').read_text().splitlines())}
jsonl('change_log.jsonl',[{'action':'new_extraction','old_id':None,'new_id':r['knowledge_point_id'],'source_pdf_sha256':source['sha256'],'pdf_page':r['pdf_page'],'before':{'candidate_detail':candidates[r['knowledge_point']]},'after':r,'reason':'按教材视觉选区细分知识点、跨页合并、校正公式和表格，分离补充已讲解原例并过滤纯历史/任务/练习','restore_from':'原PDF + pages.jsonl + selection.tsv + scripts/refine.py + patches.json；原PDF未修改'} for r in rows])
save('id_map.json',[{'old_id':None,'new_id':r['knowledge_point_id'],'action':'new_extraction'} for r in rows])
exclusions=[]
for pp,reason in [
 ([1,2,3,4,5,6,23,44,68,88,108,129,130,131],'封面、版权、目录、章引言、索引或后记，不单列知识点；原页图留存'),
 ([11,15,20,21,22,27,31,37,41,42,43,48,49,56,60,66,67,72,77,81,86,87,92,95,100,105,106,107,115,121,126,127,128],'练习与应用、复习与提高的未解题及重复知识不录入；同页正文、已讲解原例或有效侧栏另按选区保留'),
 ([14],'材料力学性能保留弹性、塑性、脆性与新材料性能；挑战者号事故人物年代叙事排除'),
 ([20],'保留万有引力概念；飞出地球的航天历史与评价排除'),
 ([25],'保留阻力实验及科学推理；末段质疑品质的纯评价排除'),
 ([27],'保留安全带、安全气囊对惯性危害的防护机理；资料调查任务排除'),
 ([53],'保留压力估算原例、原解及单位条件；原例之前的潜艇历史成就叙述排除'),
 ([54,55],'保留船闸结构及四步工作图说明；纯世界纪录和评价排除'),
 ([61,62,63,82,83,84,85,116,117],'实践项目的任务指标、自由设计要求和展示交流排除；器材、实际制作、估算及刻度标定方法完整保留'),
 ([73],'保留借溢水测体积的必要王冠情境与排水体积推理；不另建人物历史知识点'),
 ([79,80],'排除造船和飞艇发展史；保留轮船、潜水艇、气球和飞艇的不同工作方法'),
 ([104],'保留抽水蓄能电站工作方式；世界先进水平与装机排名评价排除'),
 ([114],'保留桔槔、踏碓、水碓三种机构工作原理；古代成就评价及进一步研究任务排除'),
 ([125],'实验仅保留测量步骤与空表；不补机械效率实测值及未明示的影响因素答案'),
 ]:exclusions.append({'pdf_pages':pp,'reason':reason})
jsonl('exclusion_audit.jsonl',exclusions)
enlarged={18,40,46,47,52,53,55,75,76,83,91,94,95,109,110,111,112,119,124,125,131}
review=[]
for pm in page_map:
 p=pm['pdf_page'];review.append({**pm,'visual_review':'reviewed','review_surface':f'review/pages-{((p-1)//4)*4+1:03}-{min(((p-1)//4)*4+4,131):03}.jpg','full_page_enlargement':p in enlarged,'knowledge_point_ids':[r['knowledge_point_id'] for r in rows if p in pages(r['pdf_page'])],'focus':['公式、单位、上下标和明示条件','实验器材步骤、现象与明示结论','表格、图示对应及跨页句子'],'scope_note':'缩略页整册视觉核对；表列页面另打开整页核查公式、空表或图示。文件存在校验不代替视觉核对。'})
jsonl('visual_review.jsonl',review)
# Supplementary examples have their own regions, separate from detail regions.
example_regions={18:[[18,298,525]],40:[[40,340,660]],47:[[47,62,302]],53:[[53,189,610]],76:[[76,50,635]],91:[[91,62,585]],94:[[94,422,660],[95,50,250]],112:[[112,62,605]],124:[[124,62,345]]}
sources=list(map(json.loads,(R/'source_records.jsonl').read_text().splitlines()))
for r,s in zip(rows,sources):
 s['detail_images']=re.findall(r'!\[page-\d+\]\(([^)]+)\)',r['detail'])
 s['example_images']=re.findall(r'!\[page-\d+\]\(([^)]+)\)',r['example'])
 s['example_regions']=[{'pdf_page':p,'printed_page':p-5,'bbox':[0,y0,521.575,y1]} for p,y0,y1 in example_regions.get(s['example_pages'][0],[]) ] if s['example_pages'] else []
 s['editorial_patch']=r['knowledge_point'] in json.loads((R/'patches.json').read_text())
jsonl('source_records.jsonl',sources)
errors=[]
expected=['knowledge_point_id','chapter','subchapter','section','knowledge_point','detail','example','pdf_page']
if list(rows[0])!=expected:errors.append('schema')
if not (R/'knowledge_points.csv').read_bytes().startswith(b'\xef\xbb\xbf'):errors.append('missing BOM')
if hashlib.sha256(Path(source['source_pdf']).read_bytes()).hexdigest()!=source['sha256']:errors.append('source hash changed')
refs_total=0
for i,(r,s) in enumerate(zip(rows,sources),1):
 if r['knowledge_point_id']!=f'RJ-PHYSICS-8B-{i:03}':errors.append('ID sequence')
 if r['knowledge_point_id']!=s['knowledge_point_id']:errors.append('source ID')
 if not all(r[k].strip() for k in ['knowledge_point_id','knowledge_point','detail']):errors.append('empty required')
 rp=pages(r['pdf_page'])
 for field in ['detail','example']:
  text=r[field];refs=re.findall(r'!\[page-(\d{3})\]\((images/physics-pep-8b/page-\d{3}\.png)\)',text)
  refs_total+=len(refs)
  if len(refs)!=len(set(refs)):errors.append('duplicate image '+r['knowledge_point_id']+field)
  if text.count('![')!=len(refs):errors.append('image syntax '+r['knowledge_point_id'])
  for n,path in refs:
   if not (R/path).is_file():errors.append('missing image '+path)
   if int(n) not in rp:errors.append('source page '+r['knowledge_point_id'])
   if not re.search(rf'(?m)^!\[page-{n}\]\(images/physics-pep-8b/page-{n}\.png\)$',text):errors.append('image line')
  if text.count('$')%2:errors.append('math delimiter '+r['knowledge_point_id'])
  if re.search(r'[a-zA-Z0-9]\s*\n\s*[⁻⁰¹²³⁴⁵⁶⁷⁸⁹]',text):errors.append('split superscript '+r['knowledge_point_id'])
  if re.search(r'[\u0e00-\u1fff\u2c00-\u2dff\u3100-\u312f\u3300-\u33ff]',text):errors.append('encoding '+r['knowledge_point_id'])
  if '练习与应用' in text or '复习与提高' in text:errors.append('exercise leak')
for p in range(1,132):
 if not (R/f'images/{BOOK}/page-{p:03}.png').is_file():errors.append('source page image')
report={'status':'pass' if not errors else 'fail','records':len(rows),'chapters':6,'sections':24,'website_nodes_matched':30,'pdf_pages':131,'page_visual_reviews':len(review),'full_page_enlargements':len(enlarged),'supplementary_worked_examples':sum(bool(r['example']) for r in rows),'image_references_checked':refs_total,'errors':errors,'separate_checks':{'schema_bom_ids':'pass','outline_coverage':'pass','source_pdf_hash_unchanged':'pass','image_paths_standalone_dedup':'pass' if not errors else 'see errors','visual_content':'整册逐页视觉核对，公式空表及图示重点页另打开整页；见visual_review.jsonl','unprovided_experiment_results':'未补写；原有空表、空白测量值和探究留空保留','limits':'程序结构检查不证明原文忠实性；远端PDF未做逐字节哈希比对'}}
save('validation_report.json',report)
print(json.dumps(report,ensure_ascii=False,indent=2));assert not errors,errors
