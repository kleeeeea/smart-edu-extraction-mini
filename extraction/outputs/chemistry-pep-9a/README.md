# 人教版化学九年级上册抽取

已完成全书199个PDF物理页的视觉核对与内容抽取，共153条记录。覆盖绪论、第一至第七单元、有效实验活动与附录。按教材自行识别知识点，未限制为每个网站课题一条。

- [知识点CSV](knowledge_points.csv)：UTF-8 BOM，固定八字段。
- [阅读版](knowledge_points.md)：与CSV对应；图片路径相对于本目录。
- [来源与教材身份](source_report.json)、[目录对齐](outline_alignment.json)。
- [视觉核对](visual_audit.json)、[排除与去重说明](exclusion_audit.json)、[最终校验](validation.json)。
- [ID映射](id_mapping.json)、[语义变更](record_changes.json)、[变更记录](change_log.json)。

同版SmartEdu资源ID为8c419b19-b3a9-4dbf-a8b4-546b7d337528。网站ebook_mapping确认节点路径、顺序和物理页；响应未返回节点名称，名称来自本地教材视觉目录，未声称名称由网站返回。网站源文件元数据与本地文件字节数、页数一致；未下载远端PDF比对SHA-256。

`detail`保留核心讲解、必要情境和首次讲解原例。化学方程式计算的例题2可以自然分离，完整题干原解放在相应记录的`example`，并保留与例题1不同的反求方向和简化格式。其他核心原例不拆走。

实验按教材保留器材、步骤、现象及明示结论；未解的预测、实验现象空表和结论空格不补写。不同材料、条件或组织方式的实验保留必要对比。纯历史评价、任务目标、未解练习及重复小结不再次录入。

所有跨页句子先合并，再附整页图；同一记录、同一字段、同一整页路径只出现一次。图片使用`![page-NNN](images/chemistry-pep-9a/page-NNN.png)`。密集相对原子质量表和二维原子结构、装置等以源图保留，附录数据说明保留文字。

PDF页码为物理页序；正文印刷页通常为物理页减7。页码字段包含各字段必要图源的并集，例如周期表插页P198。源页候选定位和手工修正保存在`selection.json`、`source_records.jsonl`及`transcription_candidates.jsonl`中。

重建与校验：

```sh
/Users/l/miniconda3/envs/base124/bin/python extraction/outputs/chemistry-pep-9a/scripts/build.py
/Users/l/miniconda3/envs/base124/bin/python extraction/outputs/chemistry-pep-9a/scripts/package_audit.py
```

`selection.json`是最终构建输入。其他select、extend、unit、refine、finalize脚本是编辑过程留存，不应重跑覆盖最终修订。此前阶段链接保留，`.partial.csv`不是最终结果。前次交付001—047号保持不变；本轮候选至最终记录的编号变更见ID映射。
