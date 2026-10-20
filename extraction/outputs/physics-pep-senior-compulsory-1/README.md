# 人教版高中物理必修第一册抽取结果

本册独立保存，共 **82条知识点**，覆盖 **4章19节**，另收录序言中的实质知识、课题研究及实验附录。7个 example 字段保留可分离的补充原例与原解（其中牛顿第二定律字段含两道不同方法的原例）。

- [主CSV（UTF-8 BOM，八字段）](knowledge_points.csv)
- [Markdown阅读版](knowledge_points.md)
- [教材身份](book_identity.json)、[官方目录对齐](outline_alignment.json)
- [来源片段](source_records.jsonl)、[逐页映射](page_map.json)
- [逐页视觉核对](visual_review.jsonl)、[排除与去重说明](exclusion_audit.json)
- [校验结果](validation_report.json)、[变更记录](change_log.jsonl)、[ID映射](id_map.json)

## 内容与来源

教材依据《普通高中物理课程标准（2017年版）》编写，2019年审核通过（PDF P132明示）。版次与印次日期在版权页未提供，未推断。不能将本册标为义务教育2022修订版。

网站实际电子书导航映射用于目录层级和顺序，共26个节点；节点映射本身不含名称，名称由同版PDF P4目录及正文节标题视觉核对补全，依据在目录对齐文件中明确记录。官方元数据和原始导航映射保存在website/。

页码均为PDF物理页序。正文印刷页码通常为物理页减5。跨页文字先合并，再附图；各字段内整页图片路径去重，图源为 images/physics-pep-senior-compulsory-1/page-NNN.png。整页图中可包含未录入的相邻内容，以正文选择区域和排除记录为准。

PDF文字层只作为候选。已逐页查看134页，重点复核分式、上下标、单位、表格、图示条件和跨页。实验保留教材器材、步骤、明示现象及结论；空表不填数据，开放问题不补答案。核心原例随完整讲解保留detail，可分离的补充原例置于example。复杂图示及原始空表保留整页图，不自行重绘或补结果。

## 重建与校验

在本目录执行：

```sh
/Users/l/miniconda3/envs/base124/bin/python scripts/build.py
/Users/l/miniconda3/envs/base124/bin/python scripts/write_metadata.py
/Users/l/miniconda3/envs/base124/bin/python scripts/audit.py
```

selection.tsv记录人工选择区域；patches.json记录全文校正；build.py中的MATH记录按页按区域转录的分式。原始候选保存在pages.jsonl与transcription_candidates.jsonl。程序结构检查不替代逐页视觉核对。
