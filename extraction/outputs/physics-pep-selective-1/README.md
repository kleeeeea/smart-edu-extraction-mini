# 人教版高中物理选择性必修第一册抽取结果

已按本次要求整理 **83 条知识点**，覆盖 **4 章、23 节**，另保留章引言有效分类和书后课题研究；全书 **130 页**已视觉核对。8 个 example 字段收录可自然分离的补充已讲解原例（其中动量守恒字段保留两种不同条件的原例）。

- [知识点阅读版](knowledge_points.md)
- [八字段 CSV（UTF-8 BOM）](knowledge_points.csv)
- [来源身份与哈希](metadata.json)
- [同版网站目录对齐](outline_alignment.json)
- [逐页视觉记录](visual_review.jsonl)
- [来源区域](source_records.jsonl)、[排除记录](exclusion_audit.jsonl)
- [校验报告](validation_report.json)

网站目录使用同一资源的目录预览图及 ebook_mapping；目录名称、顺序、页码逐项与本地教材核对。教材正文作为知识内容依据，未用网站课题数限制知识点数量。网站与本地文件的书名、册次、130 页和字节数一致；没有声称对远程整本 PDF 做过哈希比对。版权页未给出年月版次，未推断。

detail 保留核心解释、必要实验、情境与推导；example 仅放补充原例原解。实验未给出的结果与未解练习答案未补写。混合历史栏文只保留有效物理片段；同类重复概述不再次录入。课题研究按规范就近归属末节，实际位置见来源记录。

页码均为 PDF 物理页序，正文印刷页加 5 即物理页。原图统一使用 `images/physics-pep-selective-1/page-NNN.png`，每条记录的每个字段内同一整页路径只出现一次。跨页语句先合并为完整正文，再附图。Markdown 与 CSV 都位于同一输出目录，图片相对路径相同。

可重建材料：`scripts/build.py` 是人工选择的源区域，`raw_candidates.jsonl` 保存未经核验的文字层候选，`scripts/correct.py` 保存显式视觉校正并生成 `scripts/patches.json`。重建依次运行 build.py、correct.py、build.py、audit.py，使用 `/Users/l/miniconda3/envs/base124/bin/python`。程序检查用于字段、来源和图片一致性，不替代逐页视觉核验。

此目录为本册新建结果，没有覆盖其他册次。
