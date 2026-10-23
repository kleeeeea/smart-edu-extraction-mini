# 人教版高中化学选择性必修2《物质结构与性质》教材抽取

已完成整册115个PDF物理页的视觉查看，抽取105条记录。章节、小节依同资源网站目录层级与起始页顺序，知识点依教材正文、实验及有效侧栏细分。此目录独立新增，未修改此前各册输出。

- [知识点CSV](knowledge_points.csv)：UTF-8 BOM，固定八字段，可直接导入。
- [Markdown阅读版](knowledge_points.md)：与CSV同源，配套完整源页图片。
- [来源记录](source_records.jsonl)：每条知识点的候选选区、实际源页、图片及编辑说明。
- [逐页视觉审计](visual_audit.json)、[页码映射](page_map.json)、[排除和去重记录](exclusions.json)。
- [同版目录对齐](outline_alignment.json)、[来源身份](source_report.json)、[校验结果](validation.json)。
- [ID映射](id_map.json)、[完整变更快照](changes.json)、[核定选段](selection.json)。

教材身份：人民教育出版社，普通高中教科书·化学选择性必修2 物质结构与性质。封面2019年审核，后记P110明示依据《普通高中化学课程标准（2017年版）》编写。封底P115 ISBN为978-7-107-34603-3。未发现可确认的具体版次、印次日期，不作推断，也不套用其他教材的2022年修订标记。

资源ID：`b82cefe7-d631-4bde-baf9-352ca033cba4`。

本地PDF SHA-256：`80bd01587de4d10cd78949e707477df14b2b6848cbc37c9154c72dfc37eedce3`。

文件大小18413188字节，共115页。网站同资源源文件大小与本地一致，封面、书名、册次、目录起始页对应；网站对象标识带有分段后缀，不将它当作本地MD5，不声称已做远端文件逐字节哈希比较。

网站目录接口共有17个节点，其中15个具有有效页码，均与同资源PDF目录/正文起始页对应；2个节点没有页码，保留未确认状态。接口不返回标题文字，具体名称取PDF P4目录及对应正文。网站原始响应保存在`website-resource.json`、`website/ebook_mapping.json`，详细限制见目录对齐文件。

抽取范围包括引言、三章正文、实验、数据表和有效侧栏。完整核心讲解、首次解释用的情境、算式与原例保留在detail。全书没有另行选入可自然分离的补充已解原例，example字段均留空。未解练习、查阅报告和任务指标不填答案；科学史混合栏只提取有效方法、实验与明示知识。复习和实验活动中与首讲相同的知识、同法操作不再次单录，新增条件和必要对比保留。实验空表保持为空，未给出的结果没有补写。

公式、表格数据、单位、电荷、上下标、条件以及跨页跨栏句均已回读校正。复杂二维模型、分子结构式、轨道图、光谱和晶胞图保留原页；图中其他内容并不表示属于该条知识正文。图片命名按本册学科使用`images/chemistry-pep-hs-selective-2/page-NNN.png`，每个引用独立成行，同一记录同一字段同一整页路径一次；跨页文字先合并，图片统一附在完整讲解后。pdf_page使用物理页序，正文印刷页码通常为物理页减3，前后封面、空白等不强行套用。

结构检查通过：105条连续唯一ID、八字段、UTF-8 BOM、必填项、控制字符、图片路径与独立行、同字段图片去重、记录源页与图片集合一致、全部115张源页及逐页核对图存在、源PDF哈希不变，以及关键公式和实验用量检查。结构检查不替代视觉核对，逐页情况见审计文件。

重建最终产物只需依次运行：

```sh
/Users/l/miniconda3/envs/base124/bin/python extraction/outputs/chemistry-pep-hs-selective-2/scripts/build.py
/Users/l/miniconda3/envs/base124/bin/python extraction/outputs/chemistry-pep-hs-selective-2/scripts/package_audit.py
```

`selection.json`是最终核定选段与正文；早期select/correct/finalize/polish脚本为一次性过程记录，不应重复执行。`transcription_candidates.jsonl`和`positioned_text.txt`仅为文字层候选，不能当作已校订正文。
