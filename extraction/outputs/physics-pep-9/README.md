# 人教版物理九年级全一册：教材知识点抽取

依据本次指定的“根据2022年版课程标准修订”教材PDF，按教材内容细分为 **129条知识点**，覆盖 **10章、40节**。全册218个物理页保留原页图片与核对记录，3组可以自然分离的补充已讲解原例原解放入`example`。

## 主要文件

- [knowledge_points.csv](knowledge_points.csv)：UTF-8 BOM，八字段主表。
- [knowledge_points.md](knowledge_points.md)：阅读视图，正文与主表一致。
- [book_metadata.json](book_metadata.json)：教材身份、资源ID、本地PDF SHA-256及版本证据。
- [outline_alignment.json](outline_alignment.json)：网站50个章/节节点与本地教材页序对齐，40节均有记录。
- [source_records.jsonl](source_records.jsonl)：每条知识点的PDF选区、印刷页及补充原例来源。
- [visual_review.jsonl](visual_review.jsonl)：218页视觉核对记录；复杂公式、表格另外放大核对。
- [exclusion_audit.jsonl](exclusion_audit.jsonl)：未解练习、任务、历史评价及重复片段的排除依据。
- [change_log.jsonl](change_log.jsonl)：候选文本与最终记录的完整前后内容。
- [validation_report.json](validation_report.json)：结构、ID、目录覆盖、来源映射、图片独立行及同字段去重检查。

`pages.jsonl`和`transcription_candidates.jsonl`是文字层候选，不能作为已核验主表使用。`images/physics-pep-9/page-NNN.png`为教材物理页整页图；图内的未解练习只属于源页上下文，不构成主表收录内容。

## 来源及目录

网站新版接口`ndrv2`提供218页教材元数据，其`ebook_mapping`含50个章/节节点、父子关系与页码，本地目录和小节起始页逐项对齐。目录名称取自本地PDF视觉目录；网站映射本身不返回节点名称，详见对齐记录。旧`ndrs`接口仍返回190页旧版，已保留为版本差异证据，没有用它替代新版目录。

本地PDF字节数与新版网站元数据一致。网站私有PDF直链返回401，未声称远程文件哈希一致；本地原PDF的SHA-256独立记录。用户给定GitHub规则链接的raw访问返回404，本次采用其指定的本地同名抽取规范，并以本次用户规则覆盖数学学科限定。

## 内容处理

必要的原情境、实验、核心算式及串并联应用原例原解留在`detail`。`example`仅存欧姆定律补充计算、电热水壶计算、焦耳定律串并联对比计算。原实验的空表、待读数及开放观察不补答案；模型试验没有补写比较结果。

跨页句子先合并完整，再附原页图；同一记录同一字段同一路径只出现一次。表格、分式与上下标依据原页复核，二维图示仍由教材原页表达。

本次为独立新抽取，原PDF、技能文件和原有comment均未改动。ID按最终教材顺序连续编排，`id_map.json`中旧ID为空。

## 重新生成与结构校验

以`selection.tsv`和`patches.json`为最终编辑依据：

```sh
/Users/l/miniconda3/envs/base124/bin/python scripts/build.py
/Users/l/miniconda3/envs/base124/bin/python scripts/package_audit.py
```

请在本目录运行。`scripts/review_patches.py`和`scripts/final_review.py`保留本次人工校订过程，不是日常重建入口。程序检查不能替代逐页原文与图示核验。
