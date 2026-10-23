# 人教版高中化学必修第一册抽取结果

本包覆盖所给 PDF 全部 139 个物理页，逐页查看渲染图；提取 **116 条知识记录**，按绪言、四章及附录顺序组织。概念、性质、规律、公式、实验和有效侧栏由教材内容细分。网站同册目录节点用于章、节、实验活动的顺序与页码对齐。

- [八字段 CSV](knowledge_points.csv)：UTF-8 BOM，适合导入。
- [Markdown 阅读版](knowledge_points.md)：完整 detail、必要原例原解及源页图片。
- [来源记录](source_records.jsonl)：每条记录的物理页、区域、教材哈希、选定正文和编辑说明。
- [逐页视觉核对](visual_audit.json)、[页码映射](page_map.json)、[排除记录](exclusions.json)。
- [教材身份](source_report.json)、[网站目录对齐](outline_alignment.json)、[校验结果](validation.json)。
- [新增记录快照](changes.json)、[ID 映射](id_map.json)。

CSV 字段固定为 `knowledge_point_id,chapter,subchapter,section,knowledge_point,detail,example,pdf_page`。ID 为 `RJ-CHEMISTRY-HSC1-001` 至 `RJ-CHEMISTRY-HSC1-116`。`pdf_page` 使用 PDF 物理页序，正文印刷页码一般为物理页减 5。

核心解释、必要情境、首次讲解的例题及原解保留在 `detail`。本册入选计算原例均属于首讲所需，没有另行保留可分离的补充原例，因此 `example` 留空。保留不同条件和方法的实验，不填空表、讨论题或教材未给的观察结果。纯历史评价、任务指标、未解练习及重复总结排除；混合页面的取舍见排除记录和来源区域。

公式、离子电荷、分母、指数、单位、反应条件、实验用量及跨页/跨栏衔接已对照页图核查。二维电子式、部分完整表格、图示及折页周期表直接保留教材原图。全部跨页文字先合并，再在完整段落后附图；图片独立成行，同一记录同一字段同一路径仅一次。图片目录为本学科本册的 `images/chemistry-pep-hs-compulsory-1/`。

教材为人民教育出版社《普通高中教科书·化学 必修 第一册》。封面标示 2019 审核；P135 后记明确依据《普通高中化学课程标准（2017年版）》编写。ISBN 为 978-7-107-33574-7。资源 ID 为 `5cd19072-e40d-4a73-8580-7b7ada5d4005`。PDF SHA-256 为 `26697bcbfb058051aefe2533789b81312759a28f3c0e6e507295ac5e2fddaf8b`。

网站资源元数据及 ebook 映射保存在 `website/`。平台映射提供节点路径、层级和起始物理页，**没有节点标题字符串**；章、节名称由本册 PDF 的 P5—P6 目录及正文核实，不把本地标题冒称为网站逐字核验结果。平台源文件大小与本地一致，但其 `ti_md5` 是带 `-2` 后缀的分段对象标识，未用它宣称远端与本地逐字节相同。

程序检查包括八字段与 BOM、连续唯一 ID、来源对应、图源存在、图片独立行和去重、页码一致、关键公式与条件回归、原 PDF 哈希。程序检查不替代逐页视觉核查。

`selection.json` 是最终人工选取与修正源；`scripts/prepare.py`、`select.py`、`append*.py`、`refine*.py` 和 `finalize_selection.py` 保留准备及编辑过程，不应对最终结果重复执行追加步骤。需要从最终选取重建并校验时，在仓库根目录运行：

```sh
/Users/l/miniconda3/envs/base124/bin/python extraction/outputs/chemistry-pep-hs-compulsory-1/scripts/package_audit.py
```

本包单独新增，未改动其他分册或仓库既有索引。
