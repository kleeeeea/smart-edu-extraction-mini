# 人教版物理八年级下册抽取结果

来源为指定的《义务教育教科书·物理八年级下册（根据2022年版课程标准修订）》PDF。独立保存于本目录，没有替换其他分册。

- 6章、24节，74条知识点，9组可自然分离的补充已讲解原例及原解。
- PDF共131页，逐页视觉核对；21个重点页另打开整页核查公式、单位、表格或图示。
- CSV为UTF-8 BOM，固定八字段；Markdown与CSV由同一批记录生成。
- 图片引用按独立行保存，跨页文字先合并，同一字段的同一整页路径不重复。

## 阅读与导入

- [knowledge_points.csv](knowledge_points.csv)：主数据。
- [knowledge_points.md](knowledge_points.md)：完整阅读视图。
- [validation_report.json](validation_report.json)：结构、目录覆盖、ID、源页及图片引用校验结果。
- [book_metadata.json](book_metadata.json)：教材身份、资源ID、原PDF SHA-256、网站证据与修订标记。

`pdf_page`为PDF物理页序；P6-P129对应教材印刷页1-124。前后封面和无页码页不推断印刷页码。

## 目录依据与内容边界

同版网站新版资源元数据及`ebook_mapping`保存于`website/`。30个章/节节点的页序与父子层级逐项对应；标题名称依据本地PDF视觉目录，因为网站映射文件不返回标题文字。具体对应见[outline_alignment.json](outline_alignment.json)。本地与网站PDF均为131页、13,733,800字节；本地原文件哈希已记录，未对远端PDF另做逐字节哈希比对。

教材决定知识点粒度。`detail`保留完整核心讲解、必要情境、算式及用于介绍知识的原例；`example`仅放可自然分离的补充已讲解原例原解。保留实验原有器材、步骤、现象和明示结论，测量留空、空表和未给出的结果不补写。浮沉条件保留“由静止释放”“浸没”等原有条件，滑轮组保留忽略自重、绳重及摩擦的条件。

跨学科实践中的抽水机、微型密度计、杆秤保留原理、选材、制作、估算与标定方法；不录任务指标及未解交流问题。混合历史栏目保留有实质内容的方法或机构说明，纯历史评价和练习排除；详见[exclusion_audit.jsonl](exclusion_audit.jsonl)。

抽取采用指定本地技能及其`references/extraction-policy.md`，并以本次用户要求覆盖其数学学科限定与图片路径约定。

## 追溯与复现

- `source_records.jsonl`：每条记录的正文选区、例题选区、物理页序及字段图片。
- `page_map.json`：PDF页序、印刷页与原页图片映射。
- `visual_review.jsonl`：逐页核对与重点整页放大记录。
- `pages.jsonl`、`transcription_candidates.jsonl`：文字层候选，仅供定位，不代表视觉核验结果。
- `selection.tsv`、`patches.json`、`scripts/refine.py`：视觉选区与公式、表格、字段分配修正。
- `change_log.jsonl`、`id_map.json`：新抽取记录的前后内容、连续编号与恢复来源。
- `images/physics-pep-8b/`：131张PDF原页图；`review/`为核对拼图。

在本目录运行：

```sh
/Users/l/miniconda3/envs/base124/bin/python scripts/build.py
/Users/l/miniconda3/envs/base124/bin/python scripts/refine.py
/Users/l/miniconda3/envs/base124/bin/python scripts/build.py
/Users/l/miniconda3/envs/base124/bin/python scripts/package_audit.py
```

程序校验与人工视觉核对分别记录。图片文件存在、字段完整、哈希一致等程序检查不代替原文核对。
