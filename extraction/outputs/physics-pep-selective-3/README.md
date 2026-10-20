# 高中物理人教版·选择性必修第三册

本目录为独立抽取结果：110条，5章23节，另含完整课题研究样例。教材143个物理页均已检查渲染。

- [知识点CSV](knowledge_points.csv)：UTF-8 BOM，固定8字段。
- [Markdown阅读版](knowledge_points.md)：与CSV同源，图片相对本目录有效。
- [教材身份](metadata.json)、[目录对齐](outline_alignment.json)。
- [逐页视觉核对](visual_review.json)、[排除审计](exclusion_audit.json)、[结构校验](validation_report.json)。
- [来源记录](source_records.jsonl)、[初稿到终稿ID映射](id_mapping.csv)、[完整变更记录](change_log.jsonl)。

`detail`包含完整核心讲解、实验及必要原例。`example`仅含两处可分离的补充原例原解；氘核比结合能例题属于质量亏损的核心讲解，留在`detail`。跨页句子先合并，图片独立行置于完整讲解之后，同字段同路径仅一次。原页中仍可能显示被排除的练习或历史段落，它们未作为正文转录。

网站证据保存于`evidence/`。官方电子书映射提供节点层级、顺序和页码，但不含节点名称；文字目录采用同资源PDF的P4及正文标题，具体证据见目录对齐文件。版权页未明确给出的版次、印次和出版日期不推断。

最终转录保存在`patches.json`，来源选区候选保存在`selection.json`。`source_records.jsonl`同时保留候选选区和实际视觉复核整页；候选矩形并非最终逐字边界。`pages.jsonl`仅是文字层候选，不能替代原页。

重建：使用 `/Users/l/miniconda3/envs/base124/bin/python scripts/build.py`，随后运行同路径Python执行` scripts/package_audit.py`。`refine.py`、`correct_transcription.py`、`final_review.py`保存分阶段修订过程；不应在最终结果上重复执行，它们不是重建入口。

原PDF保持不变，未修改仓库既有分册、正式资源清单或发布内容。
