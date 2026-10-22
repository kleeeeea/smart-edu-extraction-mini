"""Write honest scope and provenance audits for the current partial extraction."""
import json
from pathlib import Path
R=Path(__file__).resolve().parents[1]
def write(n,v): (R/n).write_text(json.dumps(v,ensure_ascii=False,indent=2))
selection=json.loads((R/'selection.json').read_text())
report=json.loads((R/'source_report.json').read_text())
report.update({'subject':'化学','education_stage':'初中','publisher':'人民教育出版社','grade':9,'volume':'上册','curriculum_revision':'根据2022年版课程标准修订','cover_approval':'教育部审定2024','resource_id':'8c419b19-b3a9-4dbf-a8b4-546b7d337528','edition_date':'未确认，不依据审定年份推断','file_bytes':Path(report['source_pdf']).stat().st_size,'printed_page_offset':-7})
write('source_report.json',report)
mapping=json.loads((R/'website/ebook_mapping.json').read_text())
node_names={8:'绪论 化学使世界变得更加绚丽多彩',14:'第一单元 走进化学世界',15:'课题1 物质的变化和性质',21:'课题2 化学实验与科学探究',36:'第二单元 空气和氧气',37:'课题1 我们周围的空气',45:'课题2 氧气',50:'课题3 制取氧气',59:'实验活动1 氧气的实验室制取与性质',61:'跨学科实践活动1 微型空气质量“检测站”的组装与使用',62:'第三单元 物质构成的奥秘',63:'课题1 分子和原子',72:'课题2 原子结构',79:'课题3 元素',87:'跨学科实践活动2 制作模型并展示科学家探索物质组成与结构的历程',88:'第四单元 自然界的水',89:'课题1 水资源及其利用',98:'课题2 水的组成',103:'课题3 物质组成的表示',114:'实验活动2 水的组成及变化的探究',115:'跨学科实践活动3 水质检测及自制净水器',116:'第五单元 化学反应的定量关系',117:'课题1 质量守恒定律',124:'课题2 化学方程式',133:'跨学科实践活动4 基于特定需求设计和制作简易供氧器',134:'第六单元 碳和碳的氧化物',135:'课题1 碳单质的多样性',143:'课题2 碳的氧化物',152:'课题3 二氧化碳的实验室制取',161:'实验活动3 二氧化碳的实验室制取与性质',163:'跨学科实践活动5 基于碳中和理念设计低碳行动方案',164:'第七单元 能源的合理利用与开发',165:'课题1 燃料的燃烧',176:'课题2 化石能源的合理利用',188:'实验活动4 燃烧条件的探究',189:'跨学科实践活动6 调查家用燃料的变迁与合理使用',190:'附录Ⅰ 初中化学实验室常用仪器',192:'附录Ⅱ 相对原子质量表',193:'附录Ⅲ 名词索引'}
nodes=[]
for n in mapping['mappings']:
 v=dict(n);v['name_from_pdf_toc']=node_names.get(n['page_number']);v['name_source']='本地PDF目录视觉读取，网页映射响应未提供名称';v['toc_visual_status']='reviewed' if n['page_number']<=62 else '目录页已读、正文未核验';nodes.append(v)
write('outline_alignment.json',{'resource_url':'https://s-file-1.ykt.cbern.com.cn/zxx/ndrv2/resources/tch_material/details/8c419b19-b3a9-4dbf-a8b4-546b7d337528.json','identity_basis':'资源ID、修订标记、册次、PDF封面和目录；未核实远端PDF哈希相同','website_role':'mappings中的节点路径、物理页与顺序；不据网站课题数量确定知识点数量','nodes':nodes,'differences':['网站映射不返回节点名称，名称来自本地PDF视觉目录。','整理与提升、复习与提高未在该映射中作为节点列出。','实验活动和跨学科实践活动在网站映射中为独立根节点，按实际层级保留。']})
exclusions=[{'pages':'P1-P7','reason':'封面、版权、目录、空白，保留为身份与目录依据，不作正文知识点。'},{'pages':'P8-P12','reason':'绪论选择P11-P12研究内容与特征；其余动机、纯历史和评价叙述不单列知识点。'},{'pages':'P13','reason':'栏目说明，不作学科知识点。'},{'pages':'P14','reason':'章引言科学探究段保留章级；评价、动机和装饰图不另立记录。'},{'pages':'P19-P20','reason':'P19思考与讨论和P20未解习题排除；小结重复已抽正文，不追加重复页码。'},{'pages':'P21','reason':'实验室历史叙述不单列；实验基础和实验室规则保留。'},{'pages':'P24-P25;P27','reason':'未解思考与讨论/想一想不补答案；必要操作图保留源页。'},{'pages':'P29','reason':'交流与讨论任务不录入；实验步骤及后文明示内容保留。'},{'pages':'P31-P35','reason':'小结与整理重复已抽概念及方法，未解练习与复习题不录。'},{'pages':'P36','reason':'单元引入问题和学习目标，不单列。'},{'pages':'P38','reason':'历史成分认识演进不单列；实验与现代空气成分保留。'},{'pages':'P41','reason':'讨论问题不补答，氮气空表保留空白，标准状况脚注保留。'},{'pages':'P42-P44','reason':'未解思考、调查与练习排除；空气污染、氩氦刀、空气质量指数有效内容保留。'},{'pages':'P47-P49','reason':'实验总结重复内容不追加第二次；未解反应表、小结和练习不录。'},{'pages':'P53-P54','reason':'未解比较题不补答案；催化剂有效内容保留，人物经历与评价排除。'},{'pages':'P55-P58','reason':'重复小结、空白整理表及未解习题排除，包括红砖粉末催化剂判断题。'},{'pages':'P59-P60','reason':'实验目的任务指标、问题与交流不补答；器材步骤和新增方法条件完整保留。'},{'pages':'P61','reason':'目标、参观、调查及展示任务不单列；监测器组装操作与P39数字化实验重复，监测污染物与P43重复。'},{'pages':'P63-P199','reason':'待视觉核对与抽取，属于未处理，不属于内容排除。'}]
write('exclusion_audit.json',exclusions)
visual=[]
for p in range(1,200):
 visual.append({'pdf_page':p,'status':'visually_reviewed_initial_pass' if p<=62 else 'not_reviewed','image':f'images/chemistry-pep-9a/page-{p:03}.png','note':'首轮视觉检查；已入表记录另经转录读回，整册审校未完成。' if p<=62 else '不得据文字层判定核验通过。'})
write('visual_audit.json',visual)
write('progress.json',{'status':'incomplete','pdf_pages':199,'visual_first_pass_pages':'P1-P62','records':len(selection),'record_scope':'绪论、第一单元、第二单元及实验活动1；尚未完成整册','pending':['P63-P199逐页视觉核对及具体知识点抽取','全册目录层级、去重及原例字段复核','全册完成后统一确认ID及完整校验'],'provisional_ids':True,'image_rendering':'199页已渲染，不等于已核验199页'})
write('change_log.json',[{'action':'new_partial_extraction','date':'2026-10-22','resource_id':report['resource_id'],'sha256':report['sha256'],'before':None,'after_file':'selection.json','records':len(selection),'status':'incomplete','restore_source':'原始PDF及transcription_candidates.jsonl','notes':['未合并至既有知识库','未修改原PDF或物理教材输出','新ID暂定，未声明全册最终编号']}])
(R/'README.md').write_text('''# 人教版化学九年级上册抽取（未完成）

当前为阶段文件，不能视为整册交付：首轮视觉核对到 PDF P62；当前47条记录覆盖绪论、第一单元、第二单元及实验活动1。P63—P199尚待处理。

- `knowledge_points.partial.csv`：UTF-8 BOM八字段阶段数据。
- `knowledge_points.partial.md`：阶段阅读视图。
- `selection.json`：当前人工选择、正文修正及位置依据，是构建输入。
- `source_records.jsonl`、`transcription_candidates.jsonl`：来源位置及文字层候选。
- `outline_alignment.json`：同版网站映射和本地视觉目录名称的对应。网站响应未提供节点名称，未伪称名称来自网站。
- `visual_audit.json`、`exclusion_audit.json`、`progress.json`：已检查范围、排除原因及未处理范围。
- `validation.json`：仅当前阶段结构检查；不代表整册原文审校通过。

图片采用 `images/chemistry-pep-9a/page-NNN.png`，每条记录每字段仅引用一次同一整页路径，跨页讲解合并后附图。实验空表保持空白，文字反应式保留条件；未自行配平或升级为后续章节化学方程式。

当前范围没有可以自然分离的补充已讲解原例，example留空。实验、核心情境及据此建立的概念保留在detail。

重建阶段数据：

```sh
/Users/l/miniconda3/envs/base124/bin/python extraction/outputs/chemistry-pep-9a/scripts/build.py
/Users/l/miniconda3/envs/base124/bin/python extraction/outputs/chemistry-pep-9a/scripts/write_audits.py
```

`select_initial.py`、`select_unit2.py`、`refine_initial.py`为形成当前selection的编辑过程，继续工作应直接维护selection.json，避免覆盖后续人工修订。当前ID为阶段编号。
''')
print('audits written')
