# 人教版高中化学必修第二册抽取

整册已完成：139个PDF物理页逐页视觉查看，156条记录（正文、实验及有效补充152条，附录/元素周期表4条）。第五章44条、第六章24条、第七章46条、第八章38条。未改动其他分册。

- [八字段CSV](knowledge_points.csv)：UTF-8 BOM，可直接导入。
- [Markdown阅读版](knowledge_points.md)：全部知识记录及对应完整页图。
- [校验结果](validation.json)：结构、来源、图片、关键公式及实验条件检查。
- [逐页视觉审计](visual_audit.json)、[源片段映射](source_records.jsonl)、[排除记录](exclusions.json)、[页码映射](page_map.json)。
- [教材身份](source_report.json)、[目录对齐](outline_alignment.json)、[变更快照](changes.json)、[ID映射](id_map.json)。

## 教材与目录

教材为人民教育出版社《普通高中教科书·化学 必修 第二册》，ISBN 978-7-107-33575-4。后记P136注明依据《普通高中化学课程标准（2017年版）》编写，2019年审核通过。没有套用初中教材的2022年版修订标记。

SmartEdu资源ID：`07f7d663-a867-4eb6-ad39-03b55dbd4a65`。
本地PDF SHA-256：`fbaa88aa65396838361bf028f0c9f1490dd98bb4960cdefc7e265575ba527d61`。

同资源的网站元数据和51个目录节点保存在 `website/`。网站源文件大小、页数、ISBN、章节及实验活动起始页与本地对应。平台目录映射提供节点ID、父子路径和页码，但没有标题字符串：章、节名称按本地同版目录P4—P5及正文核定，正文小标题另外逐页核对；不声称已经逐字核验网站未返回的末级标题。部分正文小标题未被平台单列，仍按教材位置细分，不限制为一个平台课题一条记录。详情与证据在 `outline_alignment.json`。

网站 `ti_md5` 为带 `-2` 后缀的对象标识，不能直接当作本地文件MD5比较；本包保留其原值，没有宣称已证明远端PDF与本地逐字节相同。

## 内容处理

`detail` 保留完整核心讲解、首讲情境及算式、实验器材/用量/步骤、教材明示现象与结论。可自然分离的补充已解原例才进入 `example`；本册抽取未发现需要另放该字段的独立补充已解原例，因此留空，核心讲解没有移走。

实验中的自拟方案、空表和未给出的结果未补答。实验活动9与正文酯化实验用量不同，保留不同条件及操作，不机械去重。历史栏目按片段处理：保留合成氨实验数据、苯的现代结构、DDT的性质及转化等有效内容，排除纯历史功绩、评价、职业要求和研究任务指标。整理复习中的重复知识与未解练习不另录。

化学式、离子电荷、反应箭头/条件、科学计数法、密度单位、二维结构及跨页文字均以渲染页图核对，文字层只用于候选定位。复杂结构、完整工艺图和密集对照表保留教材原图，不用乱序文字替代。表8-2保留教材摘录的GB 2760—2014数据，没有用外部现行标准覆盖教材内容。

所有跨页、跨栏句段先合并为完整讲解，再统一附图。同一记录同一字段中的同一整页路径只出现一次。图片独立行采用 `![page-NNN](images/chemistry-pep-hs-compulsory-2/page-NNN.png)`；按本任务化学册次调整了用户示例中的物理路径。整页图可能同时包含未入选的练习或其他栏目，入选边界以正文和 `source_records.jsonl` 的片段/备注为准。

页码为PDF物理页序，正文印刷页1对应物理P6，不能把两者混用。完整页图139张，双页视觉核对图保存在 `review/`。图像文件存在检查与人工图文核对分别记录。

## 复现与校验

`selection.json` 是完成视觉修订后的分册选择稿，包含源片段边界、最终转录、分组和备注。`pages.jsonl`、`positioned_text.txt` 与 `transcription_candidates.jsonl` 是候选/定位资料，不能作为核验结论。

使用指定Python运行最终生成与审计：

```sh
/Users/l/miniconda3/envs/base124/bin/python extraction/outputs/chemistry-pep-hs-compulsory-2/scripts/build.py
/Users/l/miniconda3/envs/base124/bin/python extraction/outputs/chemistry-pep-hs-compulsory-2/scripts/package_audit.py
```

早期 `select.py`、`append*.py` 和 `refine*.py` 保留工作过程，不应在最终选择稿上重复运行（追加脚本会重复添加记录）。最终复现只需上面两步。程序检查通过不能独立证明原文忠实性，逐页视觉与片段处理依据见审计文件。
