from pathlib import Path
import json
R=Path(__file__).resolve().parents[1];S=json.loads((R/'selection.json').read_text());B=[json.loads(x)['detail'] for x in (R/'transcription_candidates.jsonl').read_text().splitlines()]
for i in [8,14,17]:
 t=S[i-1]['detail']
 for text in ['\n\n表中省略号所指的未列元素不补写。','\n\n表中省略号保持教材未展开内容，轨道图见原页。','原图中方框与能级位置见下页图。']:t=t.replace(text,'')
 S[i-1]['detail']=t
# Use tables with blank cells to preserve unsupplied results rather than editorial instructions.
t=S[97]['detail'];start=t.index('固体分别为：');end=t.index('\n\n实验证明')
t=t[:start]+'\n\n|固体|①CuSO₄|②CuCl₂·2H₂O|③CuBr₂|④NaCl|⑤K₂SO₄|⑥KBr|\n|---|---|---|---|---|---|---|\n|颜色|白色|绿色|深褐色|白色|白色|白色|\n|哪些溶液呈天蓝色|||||||\n|实验说明什么离子呈天蓝色，什么离子没有颜色|||||||'+t[end:];S[97]['detail']=t
S[104]['detail']=S[104]['detail'].replace('简单离子与配离子的区别：（1）向盛有少量蒸馏水的试管里滴加2滴氯化铁溶液，然后再滴加2滴硫氰化钾溶液。（2）向盛有少量蒸馏水的试管里滴加2滴K₃[Fe(CN)₆]溶液，然后再滴加2滴硫氰化钾溶液。原表的“实验现象”和“解释”栏留空。','简单离子与配离子的区别：\n\n|实验步骤|实验现象|解释|\n|---|---|---|\n|（1）向盛有少量蒸馏水的试管里滴加2滴氯化铁溶液，然后再滴加2滴硫氰化钾溶液。|||\n|（2）向盛有少量蒸馏水的试管里滴加2滴K₃[Fe(CN)₆]溶液，然后再滴加2滴硫氰化钾溶液。|||')
S[66]['detail']=S[66]['detail'].replace('用教材所述的合成方法，可以','用手性催化剂生产手性药物，可以')
S[98]['detail']=S[98]['detail'].replace('Cu2+','Cu²⁺').replace('[Cu(NH3)4]2+','[Cu(NH₃)₄]²⁺')
# Place the acidity data before its interpretation, as in the original discussion.
t=S[56]['detail'];a,b=t.split('\n\npKₐ=−lgKₐ。');a=a.replace('如表2-6所示。由表2-6可见，','如表2-6所示。\n\npKₐ=−lgKₐ。'+b+'\n\n由表2-6可见，');S[56]['detail']=a
# Notes and blank marks are kept in source metadata rather than adding textbook answers.
for s in S:
 t=s.get('detail')
 if t:s['detail']=t.strip()
(R/'selection.json').write_text(json.dumps(S,ensure_ascii=False,indent=2))
