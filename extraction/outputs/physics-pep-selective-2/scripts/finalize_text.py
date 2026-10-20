from pathlib import Path
import json
R=Path(__file__).resolve().parents[1];p=json.loads((R/'patches.json').read_text())
def edit(n,f):p[n]['detail']=f(p[n]['detail'])
edit('可见光与各色光的波长频率',lambda s:'''能使人的眼睛产生视觉效应的电磁波，称为可见光。可见光的波长为400～760 nm。科学研究发现，波长（频率）范围不同的光表现为不同的颜色，如表2所示。不同波长的单色光组合也能产生不同的颜色，我们看到的阳光就是由各种色光组成的（图4.4-5）。人类的眼睛正是通过这一波段的电磁波，获得了外部世界的大量信息。

表2　各色光在真空中的波长和频率

'''+s[s.index('| 光的颜色'):])
edit('无线电波的波段与传播应用',lambda s:s.replace('部分波段划分如表1　我国','部分波段划分如表1所示。\n\n表1　我国'))
edit('门窗防盗报警装置的实验',lambda s:s.replace('参考表1　基本','参考表1。\n\n表1　基本'))
edit('光控开关的实验',lambda s:s.replace('参考表2　基本','参考表2。\n\n表2　基本'))
edit('洛伦兹力的大小及夹角条件',lambda s:s[:s.index('既然安培力')]+ '\n\n'+s[s.index('电荷量为q 的粒子'):])
# Explicit facts from effective footnotes and scientific-method sidebar.
p['历史上用安培力定义安培的条件']={'detail':'历史上曾经用安培力来定义电流的单位：真空中相距1 m的两根无限长且圆截面可忽略的平行直导线内通过等量恒定电流，当两导线之间产生的力在每米长度上等于2×10⁻⁷ N时，每根导线中通过的电流就是1 A。'}
p['归纳推理与楞次定律的研究方法']={'detail':'归纳推理是从一类事物的部分对象所具有的某种属性出发，推理出这类事物的所有对象都具有共同属性的推理方法，也就是由具体结论推理出一般规律的方法。楞次定律的得出就运用了归纳推理。通过研究不同磁极插入和拔出线圈等的实验现象，逐步归纳推理得出反映感应电流方向的规律。与演绎推理不同的是，归纳推理是从物理现象出发研究问题，而演绎推理则是由已知物理规律出发研究问题。'}
(R/'patches.json').write_text(json.dumps(p,ensure_ascii=False,indent=2))
# Regions include complete sentences and effective footnotes; images preserve source diagrams.
s=(R/'selection.tsv').read_text()
s=s.replace('1\t1\t通电螺线管','1\t1\t历史上用安培力定义安培的条件\t7:715:760\n1\t1\t通电螺线管',1)
s=s.replace('2\t2\t感应电动势','2\t1\t归纳推理与楞次定律的研究方法\t33:607:705\n2\t2\t感应电动势',1)
s=s.replace('13:534:639','13:534:639;13:715:760').replace('56:359:560','56:353:560')
s=s.replace('88:534:715','88:534:760').replace('90:408:688','90:408:760').replace('91:694:745','91:655:745')
s=s.replace('105:59:150;105:720:765','105:59:130;105:730:765').replace('105:153:540','105:144:540').replace('105:545:700','105:543:700')
s=s.replace('118:244:625','118:225:625').replace('119:190:355','119:221:340')
(R/'selection.tsv').write_text(s)
