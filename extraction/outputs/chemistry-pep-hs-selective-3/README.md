# 人教版高中化学选择性必修3：有机化学基础

已完成整册抽取：163个PDF物理页逐页视觉核对，153条知识记录。输出独立保存，未合并或替换其他分册。

- [八字段CSV](knowledge_points.csv)：UTF-8 BOM，供导入使用。
- [Markdown阅读版](knowledge_points.md)：与CSV正文同源，包含教材整页图。
- [校验报告](validation.json)、[逐页视觉核对](visual_audit.json)、[目录对齐](outline_alignment.json)。
- [来源片段](source_records.jsonl)、[排除与去重记录](exclusions.json)、[ID映射](id_map.json)、[变更记录](changes.json)。

## 教材身份

人民教育出版社，普通高中教科书《化学 选择性必修3 有机化学基础》。封面标注2019年审核通过；后记P160说明依据《普通高中化学课程标准（2017年版）》编写。封底P163 ISBN为978-7-107-34604-0。版次、印次日期未确认，不从文件名或其他分册补齐。

SmartEdu资源ID：`c561d8ee-7c06-4cb1-9a4d-e34036f02d53`。

[网站资源](https://basic.smartedu.cn/tchMaterial/detail?contentType=assets_document&contentId=c561d8ee-7c06-4cb1-9a4d-e34036f02d53)。网站原始元数据保存于`website-resource.json`，目录节点保存于`website/ebook_mapping.json`。29个节点均有物理起始页，层级及顺序逐项与本地目录和正文对应。接口没有返回目录标题字符串，标题据同资源PDF目录及正文转录，不能声称网站标题已逐字核验。网站源文件大小与本地均为22,093,382字节；带`-3`后缀的`ti_md5`对象标识不直接作为本地MD5比较值。

PDF SHA-256：`2ecb6f80c879131a0bb8cf14bb58751b638e5d849fa1cded2c6ef72cc70fab40`。完整本地路径、大小和哈希见`source_report.json`。

## 覆盖与组织

|位置|记录数|
|---|---:|
|引言|1|
|第一章 有机化合物的结构特点与研究方法|20|
|第二章 烃|24|
|第三章 烃的衍生物|50|
|第四章 生物大分子|37|
|第五章 合成高分子|21|

章、节顺序沿同资源网站节点，节内按教材明确的概念、性质、反应条件、实验和有效侧栏细分。侧栏按实际出现位置归属，不因主题相似回挂前节。复习中相同知识与同法原例不重录，不同条件、方法和必要对比保留。混合任务栏目仅保留给定的有效知识，不填练习、空表或实验结论。

核心讲解及首讲原例全部留在`detail`，包括元素分析已解原例、系统命名原图和有机合成的逆推分析与五步反应。这册没有另行拆出的可自然分离的补充已解原例，`example`留空。

实验保留教材给定器材、配比、步骤及明示现象和结论。图中或正文未给出的反应现象、记录数据和答案不外补。跨页、跨栏句段先完整合并，再集中附图。复杂二维有机结构、谱图和反应图式不能无歧义线性转写时，以教材原图保留；图中其他内容不因此变成本条知识正文。

## 页码与图片

`pdf_page`使用PDF物理页序，如`P93-P94`；P6～P159的印刷页码为物理页序减5。不能用印刷页码直接索引图片。

图片采用化学分册路径：`![page-NNN](images/chemistry-pep-hs-selective-3/page-NNN.png)`。这是用户图片格式中册次占位的化学适配。图片独立成行，同一记录同一字段同一整页路径只出现一次。163张原页PNG及双页核对JPG均已保存。

## 核验与重建

文字层只作候选，已逐页查看渲染图，回读全部记录，并修正结构式乱码、上下标、分式、单位和跨栏错序。`selection.json`冻结最终正文、选区、图源和编辑依据；`transcription_candidates.jsonl`保留最后一次构建产生的原始候选，不代表核验结论。

结构校验已通过：八字段、BOM、连续唯一ID、必填、来源映射、163页图像存在、独立图片行、同字段路径去重、页码集合一致、源文件SHA-256及关键实验条件。程序通过不代替内容核对，视觉记录见`visual_audit.json`。

在本目录执行：

```sh
/Users/l/miniconda3/envs/base124/bin/python scripts/build.py
/Users/l/miniconda3/envs/base124/bin/python scripts/package_audit.py
```

`select*.py`、`correct*.py`、`finalize_selection.py`是一次性工作记录，不应再次运行，以免重复追加或按旧草稿位置覆盖。原始选区提取与渲染准备过程见`scripts/prepare.py`。
