from pathlib import Path
import json
R=Path(__file__).resolve().parents[1];S=json.loads((R/'selection.json').read_text());cs=[json.loads(x)['detail'] for x in (R/'transcription_candidates.jsonl').read_text().splitlines()]
# Make every final text explicit, freezing the visually checked transcription.
for s,c in zip(S,cs):s.setdefault('detail',c)
for s in S:
 for a,b in [('实验记录表中的现象和质量数据留空。',''),('实验现象及解释栏保留原空格，见原图。',''),('现象、质量数据与结论栏留空。','')]:s['detail']=s['detail'].replace(a,b)
 s['detail']=s['detail'].strip()
# Freeze remaining diagram references without implying missing linear formula text.
for s in S:
 if s['name']=='酯化反应的断键方式与同位素示踪法':s['detail']+='\n\nCH₃COOH＋C₂H₅¹⁸OH ⇌（浓硫酸、加热）CH₃CO¹⁸OC₂H₅＋H₂O，标记氧的成键位置见原式。'
 if s['name']=='烃的衍生物、官能团与有机化合物的主要类别':s['regions'].append([10,300,760])
 if s['name']=='糖分子的手性与对映异构':s['detail']=s['detail'].replace('，其结构简式','，其结构简式')
 if s['name']=='酶的催化作用、条件与专一性':s['detail']=s['detail'].replace('107倍','10⁷倍')
# Preserve given science in a mixed research-task box at its actual section position.
i=next(i for i,s in enumerate(S) if s['topic']=='第五节 有机合成')
S.insert(i,dict(chapter='第三章 烃的衍生物',topic='第四节 羧酸 羧酸衍生物',section='三、酰胺',name='肥皂的工业工序与洗涤剂组成',regions=[[87,239,380]],detail='工业上生产肥皂要经过皂化、盐析、洗涤、成形等步骤。肥皂和合成洗涤剂都含有表面活性剂，大多数的合成洗涤剂是由阴离子表面活性剂及助剂等组成的。',notes=['研究与实践混合栏目仅保留给定工序及组成知识；自制实验设计、去污原理检索、作品展示与报告任务排除。']))
(R/'selection.json').write_text(json.dumps(S,ensure_ascii=False,indent=2))
