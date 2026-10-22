import csv,json,re,hashlib
from pathlib import Path
R=Path(__file__).resolve().parents[1]
def save(n,v): (R/n).write_text(json.dumps(v,ensure_ascii=False,indent=2))
S=json.loads((R/'selection.json').read_text());old=json.loads(json.dumps(S))
removed=next(s for s in S if s['name']=='测定生活中物质的pH');S.remove(removed)
for s in S:
 if s['name']=='常见合金的成分、性能和用途':s['detail']=s['detail'].replace('K表示金的纯度，如18K表示含金量为75%，14K表示含金量为58.5%。','K是表示金的纯度的指标。例如，18K表示含金量达75%，14K表示含金量达58.5%。')
 if s['name']=='金属之最':s['detail']=s['detail'].replace('●','\n\n●').strip()
 if s['name']=='常见酸、碱的化学性质实验':
  t=s['detail'];a=t.index('1. 参考');b=t.index('3. （1）');s['detail']=t[:a]+t[b:];s['regions']=[a for a in s['regions'] if a[0]!=95 or a[1] not in [281,407]];s.setdefault('notes',[]).append('活动步骤1、2为已录入指示剂和pH重复操作，排除；保留不同条件的新实验3—6。')
# Give exact table/footnote regions in addition to intact source-page images.
regions={
'一些金属物理性质的比较':[[8,435,655]],
'常见合金的成分、性能和用途':[[11,340,665]],
'常见合成材料的性能、类型和用途':[[111,55,665]],
'塑料包装制品回收标志':[[114,200,305]],
'部分酸、碱和盐的溶解性（室温）':[[121,76,530]],
'元素周期表':[[126,0,740,0,1100]],
'有机化合物和无机化合物':[[100,630,665]],
'酸碱度在健康和生产中的意义':[[68,237,449,290,480]],
'元素摄入与人体健康':[[100,355,612],[101,65,252]],
'化肥的种类与主要作用':[[88,55,284]],
'浓硫酸的腐蚀性与脱水作用':[[72,630,650]],
'浓硫酸的稀释与使用注意事项':[[72,650,665]],
'高分子材料、天然材料和合成材料':[[110,630,665]],
'六类营养物质':[[102,645,665]],
'溶液的应用':[[39,645,665]],
'气体的溶解度':[[48,645,665]],
'合理膳食与食品安全':[[103,298,320],[103,368,635,185,480]]}
for s in S:
 for a in regions.get(s['name'],[]):
  if a not in s['regions']:s['regions'].append(a)
 s['visual_status']='reviewed'
save('selection.json',S)
new_ids={s['name']:f'RJ-CHEMISTRY-9B-{i:03}' for i,s in enumerate(S,1)}
save('id_mapping.json',[{'old_id':f'RJ-CHEMISTRY-9B-{i:03}','knowledge_point':s['name'],'new_id':new_ids.get(s['name']),'status':'retained' if s['name'] in new_ids else 'excluded_duplicate_task'} for i,s in enumerate(old,1)])
save('change_log.json',{'source':'source_report.json','initial_extraction':True,'changes':[{'action':'exclude','reason':'同类pH操作已在实验10-2完整讲解，实验10-3只要求自行选材记录，不重复建点。','before':removed,'after':None}],'transcription_changes':['refinement_log.json','content_changes.json'],'id_map':'id_mapping.json'})
source=json.loads((R/'source_report.json').read_text());pdf=Path(source['source_pdf']);v=json.loads((R/'website/resource-v2.json').read_text());mapping=json.loads((R/'website/ebook_mapping.json').read_text())
source['pdf_md5']=hashlib.md5(pdf.read_bytes()).hexdigest();source['website_pdf_md5']=next(i['ti_md5'] for i in v['ti_items'] if i.get('ti_file_flag')=='source' or i.get('ti_format')=='pdf');source['website_pdf_md5_matches']=source['pdf_md5']==source['website_pdf_md5'];assert source['website_pdf_md5_matches'];source['cover_audit']='国家教材委员会专家委员会审核通过2024；不将审核标记冒充出版年月';save('source_report.json',source)
names={6:'第八单元 金属和金属材料',7:'课题1 金属材料',15:'课题2 金属的化学性质',21:'课题3 金属资源的利用和保护',32:'实验活动5 常见金属的物理性质和化学性质',33:'跨学科实践活动7 垃圾的分类与回收利用',34:'第九单元 溶液',35:'课题1 溶液及其应用',42:'课题2 溶解度',51:'课题3 溶质的质量分数',60:'实验活动6 一定溶质质量分数的氯化钠溶液的配制',61:'实验活动7 粗盐中难溶性杂质的去除',63:'跨学科实践活动8 海洋资源的综合利用与制盐',64:'第十单元 常见的酸、碱、盐',65:'课题1 溶液的酸碱性',71:'课题2 常见的酸和碱',83:'课题3 常见的盐',95:'实验活动8 常见酸、碱的化学性质',97:'跨学科实践活动9 探究土壤酸碱性对植物生长的影响',98:'第十一单元 化学与社会',99:'课题1 化学与人体健康',108:'课题2 化学与可持续发展',120:'跨学科实践活动10 调查我国航天科技领域中新型材料、新型能源的应用'}
save('outline_alignment.json',{'website_resource_id':source['resource_id'],'identity':'同资源ID，网站PDF MD5与本地完全一致，127页，front_page=5','website_title':v['title'],'title_status':'网站映射提供node_id、node_path和物理页码，无标题字段；名称由本册P4-P5目录及对应页标题视觉核对，不宣称独立取得网站节点标题。','mapping':[dict(x,pdf_title=names[x['page_number']],name_evidence='本册视觉目录/页标题') for x in mapping['mappings']],'pdf_extra_nodes':{29:'整理与提升',30:'复习与提高',56:'整理与提升',57:'复习与提高',91:'整理与提升',93:'复习与提高',117:'整理与提升',118:'复习与提高',121:'附录Ⅰ',122:'附录Ⅱ',126:'元素周期表'},'ordering':'网站node_path确定单元/课题层级与顺序；知识点按册内位置细分；附录按教材原位。'})
ex=[]
def exclude(ps,why,retained=None):ex.append({'pdf_pages':ps,'reason':why,'retained':retained})
exclude('P1-P6;P34;P64;P98','封面、书名、编写与目录、单元导读和目标；教材身份与目录另存元数据。')
exclude('P14;P20;P27-P31;P40-P41;P49-P50;P54-P59;P69-P70;P81-P82;P90-P94;P106-P107;P115-P119','练习与应用、复习与提高为未解练习，整理与提升和小结重复讲解不再录；新增明示条件按来源片段保留。','P13共性、P27防锈、P81酸碱性质、P90碳酸根/碳酸氢根类别结论已保留。')
exclude('P9;P10;P12;P13;P19;P25-P27;P44;P47-P49;P52;P65-P70;P74-P75;P77-P78;P80-P82;P86-P87;P89;P101;P103-P105;P108;P112;P114','思考讨论、调查研究中的要求、报告和待解问题排除；其中有效性质、方法、表图、已讲解内容逐片段保留。')
exclude('P33;P63;P97;P120','跨学科实践活动以查阅、调查、自拟方案、展示和任务指标为主，没有新增给定器材步骤现象结论；不补做任务。')
exclude('P7;P12;P22;P26;P66;P71;P87;P89;P104-P105','纯使用史、发展评价、人物事迹与荣誉排除；合金性能、稀土性质、植物指示剂、制碱法特点、药物与抗生素性质等有效补充保留。')
exclude('P67','实验10-3为自行选物测pH、记录空表，与实验10-2相同操作，不重复建点。')
exclude('P95','实验活动8步骤1、2与已录指示剂、pH操作重复；器材及新实验3—6完整保留。')
exclude('P122-P125;P127','名词索引、空白页、后记、照片致谢、封底，不建知识记录。')
exclude('P10;P16;P18;P32;P36-P38;P42-P43;P51-P52;P60-P62;P65-P67;P71-P72;P74;P76-P78;P85-P86;P95-P96;P112','实验待填现象、数据、分析、方程式与结论栏保留原图/空格，不自行填答案；后文明确给出结论者只照录后文。')
save('exclusion_audit.json',ex)
page_to_ids={p:[] for p in range(1,128)}
for i,s in enumerate(S,1):
 for p in set([a[0] for a in s['regions']]+s.get('image_pages',[])):page_to_ids[p].append(new_ids[s['name']])
save('visual_audit.json',{'pdf_pages':127,'reviewed_pages':127,'method':'逐页查看已渲染整页/双页图；文字层仅定位候选，逐条读回并修订串栏、上标、脚注、跨页及表格。','review_images':'review/pages-NNN-NNN.jpg；images/chemistry-pep-9b/page-NNN.png','pages':[{'pdf_page':p,'status':'visually_reviewed','records':page_to_ids[p],'disposition':'included_fragments_and_exclusions' if page_to_ids[p] else 'excluded_or_metadata_only; see exclusion_audit.json'} for p in range(1,128)],'rechecked_tables':[8,11,45,68,71,74,83,86,88,100,101,111,114,121,126],'cross_page_merges':[[7,8],[9,10],[25,26],[39,40],[51,52],[79,80],[83,84],[99,100],[102,103]],'open_issues':[]})
save('page_mapping.json',[{'pdf_page':p,'printed_page':p-5 if 6<=p<=122 else None,'image':f'images/chemistry-pep-9b/page-{p:03}.png'} for p in range(1,128)])
print('audit prepared',len(S))
