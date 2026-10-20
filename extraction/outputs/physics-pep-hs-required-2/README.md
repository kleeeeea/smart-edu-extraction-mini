# 人教版高中物理必修第二册抽取结果

整册114页已逐页视觉核查，整理为66条知识记录，覆盖第五至第八章的18节及课题研究。9个example字段收录10道可分离的补充已讲解原例；实验方案和甩手研究样例保留在detail。

- [CSV主表](knowledge_points.csv)：UTF-8 BOM，固定八字段。
- [Markdown阅读版](knowledge_points.md)：正文、补充原例及独立行整页图片。
- [结构校验结果](validation_report.json)：ID、目录覆盖、物理页码、图片和原PDF哈希。
- [教材身份与来源](metadata.json)、[网站目录对齐](outline_alignment.json)。
- [逐条来源](source_records.jsonl)、[逐页视觉核查](visual_review.jsonl)、[页码映射](page_map.json)。
- [排除审计](exclusion_audit.json)、[去重判断](deduplication_audit.json)、[修正日志](change_log.jsonl)、[临时ID到最终ID映射](id_map.json)。

网站资源ID、书名、学段、册次、12699093字节大小与114页数对应本地PDF；网站ebook_mapping提供23个节点的层级、顺序和起始物理页。接口未提供节点名称字符串，名称由PDF第4页目录视觉核对后与节点对齐，未以其他版次目录替代。网站原始响应保存在website目录。

按教材概念、规律、公式及条件、实验、有效补充独立细分知识点。detail保留核心情境、推导和必要算式；example只放可分离的补充原例、分析与原解。纯历史评价、任务性选题及未解练习不作为知识记录。实验保留教材器材、步骤、现象和明示结论；平抛与机械能实验未补写未提供的结果。原子钟实验的狭义和广义相对论共同效应脚注、蜡块先加速再受力平衡的脚注、斜抛空气阻力条件等一并保留。

PDF文字层只用于候选定位；所有正文锁定于patches.json。逐页联系原图校核，分式、根号、上下标和跨页句子作显式修正。原始候选保留在pages.jsonl和transcription_candidates.jsonl；选取窗口保留在selection.tsv。source_records中的bbox是候选定位窗口，原文和最终转录以完整源页核对。

图片统一为images/physics-pep-hs-required-2/page-NNN.png，共114张。正文使用PDF物理页；教材印刷页正文通常为PDF页减5。全页图片在同一记录的同一字段中只引用一次，跨页讲解合并完整后再附图片。同一页可以分别为不同记录或detail/example提供来源。

本包独立保存，未覆盖其他册次，未修改输入PDF。可用下列命令重建和校验：

```sh
/Users/l/miniconda3/envs/base124/bin/python scripts/build.py
/Users/l/miniconda3/envs/base124/bin/python scripts/package_audit.py
```

程序结构检查与人工视觉内容核对分别记录。教材明示公式及适用叙述按原书保留，不用外部推导替换教材或补充练习答案。未修改.tex文件。
