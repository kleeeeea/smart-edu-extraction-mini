---
name: smartedu-math
description: 查询 SmartEdu 数学知识点、教材原文、例题、图示与 PDF 源页，维护分册数据及来源映射；适用于教材检索与原文抽取，不适用于课程标准整理或其他学科。
---

# SmartEdu 数学知识点

## 数据定位与查询

从 [知识点索引](../../references/index.md) 定位教材册次，使用 [资源清单](../../references/books.json) 查找 `knowledge-points/<book>.md`、CSV、图片与 PDF。CSV 位于 `sources/feishu/`，是 Markdown 阅读视图的数据源。

在仓库根目录执行：

```sh
python skills/smartedu-math/scripts/query.py --book math-pep-1a --keyword 加法
python skills/smartedu-math/scripts/query.py --id RJ-MATH-1A-01-001
```

引用结果应包含知识点 ID、名称与 PDF 源页。教材原文、例题和解析保持原有含义；缺失条目明确说明，不补写教材答案、条件或知识点关系。

## 数据维护

源字段顺序为 `knowledge_point_id,chapter,subchapter,section,knowledge_point,detail,example,pdf_page`。CSV 首行可能包含教材来源地址，需定位字段行后再解析。

数据以册次维护。保留教材资源 ID、PDF SHA-256、知识点 ID、源页和图片路径。名称、正文、例题、ID 与页码的内容修改应与格式转换分开，不在转换过程中自动合并或改写记录。

```sh
python scripts/render_books.py --book math-pep-1a
python scripts/validate_package.py
```

图片在分册 Markdown 中使用 `../images/<book>/page-NNN.png`；分册裁剪图可使用 `<book>-<version>/` 子目录，须保留完整路径与来源信息。PDF 页码导航的配置与访问要求见 [页码导航](../../references/pdf-navigation.md)。文件替换后需同步更新资源清单、哈希、页码映射及相关校验。

## 教材抽取

执行新抽取或内容修订前阅读 [数学教材抽取规范](references/extraction-policy.md)。查询与格式转换不触发教材抽取或内容修订。

同版 SmartEdu 实际目录用于章节与课题层级，本地对应 PDF 用于正文、公式和例题。小学采用实际课题组织记录；初高中按教材明确的数学内容细分知识点。补充内容按教材位置就近归入前一小节，不按相似主题回挂。逐页核对公式、图示、明示条件及跨页内容；核心讲解与补充原例分别收录，同字段中的相同整页图片引用不重复。整册顺序修订后连续重编 ID，并保存旧新映射。

`scripts/prepare_pdf.py` 提取 PDF 文字层候选，依赖 `pdfplumber`。`scripts/validate_results.py` 适用于七字段章节中间记录，不直接处理本仓库的八字段 CSV；数据包校验使用仓库根目录 `scripts/validate_package.py`。
