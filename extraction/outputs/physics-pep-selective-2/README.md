# 人教版高中物理选择性必修第二册抽取结果

已逐页视觉检查本地 PDF 的 122 页，按 5 章、19 节细分为 88 条知识记录，另保留“课题研究”3条，共 91 条。3个 example 字段包含4道可自然分离的已讲解原例及完整原解；必要装置情境、核心推导、实验、原始表格与明示结论保留在 detail。

- [knowledge_points.csv](knowledge_points.csv)：UTF-8 BOM，固定8字段。
- [knowledge_points.md](knowledge_points.md)：逐条阅读视图，原页图片可直接访问。
- [source_report.json](source_report.json)：教材身份、源PDF路径、哈希与平台资源信息。
- [outline_alignment.json](outline_alignment.json)：平台节点、层级、页序与教材目录对齐。
- [source_records.jsonl](source_records.jsonl)：每条记录的物理页、原文区域及原例来源。
- [visual_audit.json](visual_audit.json)、[exclusion_audit.json](exclusion_audit.json)：逐页视觉核对与取舍。
- [validation_report.json](validation_report.json)：字段、ID、来源、图片与目录覆盖校验。
- [change_log.jsonl](change_log.jsonl)、[id_mapping.json](id_mapping.json)：首次建立记录及完整内容快照。

## 来源和编号

教材：人民教育出版社《普通高中教科书·物理选择性必修 第二册》。封面为“教育部审定2019”，后记明示依据《普通高中物理课程标准（2017年版）》编写。未确认具体出版版次与印次，不把审定年份当作出版年份。

平台资源 ID 为 `2ee7d7fa-1920-4d37-a179-91d5fd59b8c1`。平台元数据与本地文件均为 122 页、12,047,352 字节；资源身份、同册书名和实际节点页序匹配。平台 `ebook_mapping` 返回25个目录节点的ID、父子层级和页码，不返回节点标题。章节、小节名称取自本地 PDF P4 视觉目录，逐项与平台节点页序对齐；未声称接口返回了标题。

PDF SHA-256：`e134c14fbfe6d4242a6dcb8677d43bd889fe6a6d48b3dc7358ed911f86033bed`。

`pdf_page` 与 `page-NNN.png` 均使用从1开始的 PDF 物理页序，正文印刷页码 = 物理页序 − 5。连续来源页写作 `P20-P21`，不连续来源用分号分隔。CSV和Markdown同处本目录，均使用独立行 `![page-NNN](images/physics-pep-selective-2/page-NNN.png)`；同一记录同一字段同一整页路径仅出现一次。

## 抽取取舍

文字层只作为候选。`patches.json` 保存视觉校订后的正文和完整原例；分式、根号、指数与上下标已按原页修正。公式的几何条件、单位和模型条件一并保留；跨页句子先合并，再附整页图片。

实验保留原有器材、操作、明示现象和结论。不补写二极管演示、强磁体下落、热敏电阻研究等未给出的结果；楞次定律实验表2保留原有空白。门窗报警与光控开关的器材参数表、压力传感器16组原始数据均已逐格核对。图示和合并表格关系保留整页图源。

纯生平、历史评价、任务目标及未解练习按片段排除。混合侧栏中的有效物理内容按原位置保留，如正电子云室实验、归纳推理、无线充电和霍尔元件。速度选择器、练习中的霍尔电压待证明公式等未解内容没有补写。不同条件、反推方法及必要实验对比不机械去重。

## 重建与检查

在仓库根目录运行：

```sh
/Users/l/miniconda3/envs/base124/bin/python extraction/outputs/physics-pep-selective-2/scripts/build.py
/Users/l/miniconda3/envs/base124/bin/python extraction/outputs/physics-pep-selective-2/scripts/package_audit.py
```

重建使用 `selection.tsv` 的来源位置和 `patches.json` 的校订文本。`scripts/correct_transcription.py`、`correct_remaining.py`、`finalize_text.py` 保留本次初次校订过程，依赖当时的候选编号，不是日常重建入口，也不应重复执行。

程序校验不替代逐页视觉核对。完整候选文字、122页PNG、双页审阅图和来源快照均保存在本目录，便于复核。本次只创建本册独立结果，未替换其他册数据或改动原PDF。
