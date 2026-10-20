# 人教版物理八年级上册抽取结果

教材：根据2022年版课程标准修订，国家教材委员会专家委员会审核通过2024。SmartEdu 资源 ID：`e5618f17-c06e-4c4c-944e-0ee8ced25391`。

本册独立抽取，共 **118 条知识点**，覆盖“开启科学探索之旅”和六章、28节；逐页视觉检查了全部 **170 个 PDF 页面**。不修改既有其他册次数据。

- [CSV 主表](knowledge_points.csv)：UTF-8 BOM，固定八字段，连续编号 `RJ-PHYSICS-8A-001` 至 `RJ-PHYSICS-8A-118`。
- [Markdown 阅读版](knowledge_points.md)：与主表同步，整页图片以独立行引用。
- [教材身份](book_metadata.json)、[目录对齐](outline_alignment.json)、[页码映射](page_map.json)。
- [视觉核对记录](visual_review.jsonl)、[来源选区](source_records.jsonl)、[排除审计](exclusion_audit.jsonl)、[完整修订日志](change_log.jsonl)。
- [校验报告](validation_report.json)：字段、ID、来源页码、图片存在及独立行去重检查通过。程序检查与内容视觉核对分开记录。

网站同版 ebook_mapping 的36个节点确定顺序、页锚点及父子层级；该映射不返回标题，名称逐项依据同版 PDF 目录视觉核对。引言有同页的根、子两个节点，均保留。未取得远端 PDF 哈希；已记录本地 SHA-256，且网站 PDF 字节数与本地一致（19,970,967）。版权页未明示年月版次，未自行推断。

`detail` 保留核心讲解、必要情境和完整原解；巨石质量、金箔面积及实心铅球鉴别等核心应用不拆走。`example` 仅收录两个自然可分离的补充已解原例：百米平均速度与铝棒质量。实验中的空表、待测值及未给出的观察结论不补写。不同条件与方法保留；小结重复知识、纯历史评价、任务指标和未解练习排除。混合侧栏保留有效物理内容。

公式、单位、表格和图示依据页图核对；`pages.jsonl` 和 `transcription_candidates.jsonl` 为文字层候选，不能视为核验结果。跨页句子先合并，再附相关整页图片；同记录同字段内不重复整页路径。PDF物理页序与印刷页码不同，正文印刷页码为 PDF 页序减7。

复现主表及审计：

```sh
/Users/l/miniconda3/envs/base124/bin/python scripts/build.py
/Users/l/miniconda3/envs/base124/bin/python scripts/package_audit.py
```

在本目录执行。`selection.tsv` 保存视觉选区，`patches.json` 保存经核对的显式转录修订。`scripts/refine.py` 是早期候选整理过程的历史脚本，不是最终构建入口；最终修订以 `patches.json` 为准。
