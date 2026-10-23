# 人教版高中化学选择性必修1《化学反应原理》

全册抽取完成：103 条记录，已逐页查看 139 个 PDF 物理页。正文按教材细分知识点，覆盖四章、五个实验活动、有效侧栏、附录参考数据和元素周期表。

- [八字段 CSV](knowledge_points.csv)：UTF-8 BOM，供导入使用。
- [Markdown 阅读版](knowledge_points.md)：与 CSV 使用同一正文和图片路径。
- [校验结果](validation.json)、[逐页视觉核对记录](visual_audit.json)、[片段取舍记录](exclusions.json)。
- [教材身份与哈希](source_report.json)、[目录对齐](outline_alignment.json)、[记录来源选区](source_records.jsonl)、[页码映射](page_map.json)。
- [ID 映射](id_map.json)、[新增记录快照及变更说明](changes.json)、[核定正文与选区](selection.json)。

教材为人民教育出版社普通高中教科书，ISBN 978-7-107-34602-6。封面标记2019审核；P134后记明确依据《普通高中化学课程标准（2017年版）》编写。原文件未提供可确认的版次、印次日期，未推断。资源 ID 为 `3502fe81-b23e-4f68-aa3d-7921e7932ec9`。

目录采用国家中小学智慧教育平台同资源的26个节点及其层级、起始页。平台返回的 `ebook_mapping.json` 没有标题字符串；名称来自对应PDF目录和正文，未冒充已取得网站末级标题。网站源文件大小与本地一致；远端 `ti_md5` 是带后缀的分段对象标识，未据此宣称逐字节相同。

`detail`保留核心讲解、必要条件、首次方法计算和原解；可自然分离的补充转化率例题置于`example`。同类型葡萄糖热量计算例题不重复录入；盖斯定律的不同方法保留。实验保留教材给定器材、数量、操作、明示现象和结论，空表、待测数据和未给出的结果不补。科学史话按片段保留有效技术内容，人物年代、获奖评价、研究任务指标和未解练习排除。完整附录表有意保留表格结构，不拆成重复条目。

页码为PDF物理页序；正文印刷页码通常为物理页减5。跨页、跨栏句段先合并，再附图。图片使用独立行 `![page-NNN](images/chemistry-pep-hs-selective-1/page-NNN.png)`，同一字段同一整页路径仅一次。整页图中包含的未选练习或历史文字不表示录入该记录。复杂二维示意图及元素周期表保留原图，文字层只用作转录候选。

本目录为独立新分册，未合并或覆盖其他册次。程序校验包括八字段、BOM、连续唯一ID、来源与页码集合、图片存在及去重、关键数值条件和源PDF哈希；程序检查与逐页视觉核对分别记录。

重建只需运行 `scripts/build.py`，随后运行 `scripts/package_audit.py`，Python使用 `/Users/l/miniconda3/envs/base124/bin/python`。早期`select*.py`、`correct*.py`及`finalize_selection.py`保留为过程记录，包含追加或定点修改，不应重复执行。最终`selection.json`是重建依据。
