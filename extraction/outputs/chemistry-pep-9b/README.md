# 人教版化学九年级下册抽取结果

根据2022年版课程标准修订。全书127个PDF物理页已逐页视觉查看，形成95条知识记录：第八单元23条、第九单元21条、第十单元28条、第十一单元21条，附录溶解性表与元素周期表各1条。

- 主数据：[knowledge_points.csv](knowledge_points.csv)，UTF-8 BOM，固定八字段。
- 阅读版：[knowledge_points.md](knowledge_points.md)。
- 核验结果：[validation.json](validation.json)。
- 逐页记录：[visual_audit.json](visual_audit.json)。
- 目录依据：[outline_alignment.json](outline_alignment.json)。
- 来源片段：[source_records.jsonl](source_records.jsonl)；人工选区与完整转录：[selection.json](selection.json)。
- 排除与去重：[exclusion_audit.json](exclusion_audit.json)。
- 修改记录：[change_log.json](change_log.json)、[refinement_log.json](refinement_log.json)、[content_changes.json](content_changes.json)；草稿到最终编号：[id_mapping.json](id_mapping.json)。

教材资源ID：`1998204c-f017-4f49-9000-0ba0b93d2a4d`。本地PDF SHA-256：`d6d86ca7b3578d337ec9d1a893c8bf395cbbdb1817d7253a246ae2c2e77f7df5`。网站PDF元数据的MD5与本地文件一致，页数同为127。身份与文件路径见[source_report.json](source_report.json)。封面“审核通过2024”为审核标记，不作为精确出版日期。

同资源网站的电子教材映射保存在`website/`，其`node_path`与物理页码用于确定单元、课题和活动的层级、顺序。映射不含节点标题字段；名称由同一教材P4-P5目录与对应页标题视觉核对，未以旧版本代替，也未声称独立取得网站标题文本。整理复习、附录等网站未单列位置按本册原位处理。

`detail`保留核心讲解、必要情境、公式条件、首次完整计算原例与原解。该册保留的计算例题均承担方法讲解，因此置于`detail`；没有另行可自然分离的补充已解原例，`example`全部留空。实验保留教材给出的器材、用量、操作及明示观察和结论；空表与待解方程式不补写。相同操作的任务、重复复习、纯历史评价及未解练习按片段排除；不同条件、比较对象与新操作保留。

页码使用PDF物理页序；正文印刷页与物理页相差5页，映射见`page_mapping.json`。跨页句子先合并，再附图。图片均为独立行`![page-NNN](images/chemistry-pep-9b/page-NNN.png)`，按化学下册使用`chemistry-pep-9b`分册目录。同一记录同一字段相同整页路径只保留一次。整页图也会显示周边未录入片段，主表收录范围由文字和来源选区限定。复杂二维附录和周期表保留完整原图，不用损坏的文字层替代。

复现最终输出：在仓库根目录使用`/Users/l/miniconda3/envs/base124/bin/python extraction/outputs/chemistry-pep-9b/scripts/build.py`，随后运行同目录`verify.py`。其余`select*.py`、`refine.py`、`finalize_content.py`及`package_audit.py`为抽取过程脚本，保留编辑历史，不应在最终`selection.json`上重复执行。

校验包含BOM、八字段、连续ID、来源映射、127张原页图片存在、物理页码范围、图片独立行与同字段去重、公式定界符和花括号、源文件哈希。结构检查不代替逐页视觉与逐条原文核对。该结果独立保存在本目录，未覆盖上册或仓库其他分册。
