"""Visual transcription corrections; run build.py, refine.py, build.py in order."""
from pathlib import Path
import json,re
R=Path(__file__).resolve().parents[1]
C={q['knowledge_point']:q['detail'] for q in map(json.loads,(R/'transcription_candidates.jsonl').read_text().splitlines())}
P={}
def body(name,text):P.setdefault(name,{})['detail']=text.strip()
def replace(name,old,new):
 t=P.get(name,{}).get('detail',C[name]);assert old in t,(name,old);body(name,t.replace(old,new))
def example(name,text,pages):
 P.setdefault(name,{})['example']=text.strip()+'\n\n'+'\n\n'.join(f'![page-{p:03}](images/physics-pep-8b/page-{p:03}.png)' for p in pages)
 P[name]['example_pages']=pages
# Join lines within words and preserve the original blank experiment tables.
replace('力的三要素和力的示意图','线\n\n段','线段')
n='探究重力与质量的关系及重力计算'
t=C[n].replace('重力G/N\n\n','').replace('1 2 3 4 5 6序号质量m/kg','')
t=t.replace('记录在下表中。','记录在下表中。\n\n| 序号 | 1 | 2 | 3 | 4 | 5 | 6 |\n| --- | --- | --- | --- | --- | --- | --- |\n| 质量 m/kg | | | | | | |\n| 重力 G/N | | | | | | |\n\n')
t=t.replace('g = Gm',' $g=\\frac{G}{m}$ ')
body(n,t)
example(n,r'''质量为0.25 kg的木块，所受的重力是多少牛？一个人所受的重力为450 N，他的质量是多少千克？g取10 N/kg。

解 由G=mg可知，木块所受的重力

$G_{木}=m_{木}g=0.25\,\mathrm{kg}\times10\,\mathrm{N/kg}=2.5\,\mathrm N$

由G=mg可得$m=\frac{G}{g}$，因此人的质量

$m_{人}=\frac{G_{人}}{g}=\frac{450\,\mathrm N}{10\,\mathrm{N/kg}}=45\,\mathrm{kg}$

木块所受的重力为2.5 N，人的质量为45 kg。''',[18])
n='阻力对物体运动的影响实验与推理'
body(n,C[n].split('正是基于')[0])
n='探究二力平衡的条件'
t=C[n].split('小车在水平方向所受二力的情况')[0]
t=t.replace('记录在下表中。','记录在下表中。\n\n| 大小 | 方向 | 是否在同一直线上 | 小车的运动状态是否改变 |\n| --- | --- | --- | --- |\n| 不相等 | | | |\n| 相等 | | | |\n| 相等 | | | |\n| …… | | | |\n\n')
body(n,t)
example('同一直线上二力合成的实验与规律',r'''某同学练习排球垫球时，排球离开胳膊后竖直上升，到达最高点后竖直下落。已知排球所受的重力约为2.7 N，排球所受的空气阻力与速度的大小有关，方向与运动方向相反。若排球在竖直上升的过程中某时刻所受空气阻力的大小约为0.5 N，试计算排球此时所受力的合力的大小，说明合力的方向。若排球在竖直下落过程的某时刻所受空气阻力的大小也约为0.5 N，则此时排球所受力的合力的大小和方向又是怎样的？

解 排球竖直上升时，受到的重力和空气阻力方向均竖直向下（图8.4-4甲），这两个力的方向相同。

$F_{合}=G+F_{阻}=2.7\,\mathrm N+0.5\,\mathrm N=3.2\,\mathrm N$

排球竖直下落时，受到的重力竖直向下，空气阻力竖直向上（图8.4-4乙），这两个力的方向相反。

$F'_{合}=G-F_{阻}=2.7\,\mathrm N-0.5\,\mathrm N=2.2\,\mathrm N$

排球上升时合力为3.2 N，排球下降时合力为2.2 N，方向均竖直向下。''',[40])
replace('压力作用效果的探究与压强','p = F S',r'$p=\frac{F}{S}$')
example('压力作用效果的探究与压强',r'''水平桌面上静止放一本书，书所受的重力为3 N，与桌面的接触面积为5×10⁻² m²，计算书对桌面的压强。

解 静止在桌面上的书对桌面的压力等于它所受的重力，即

$F=G=3\,\mathrm N$

桌面的受力面积

$S=5\times10^{-2}\,\mathrm{m^2}$

所以压强

$p=\frac{F}{S}=\frac{3\,\mathrm N}{5\times10^{-2}\,\mathrm{m^2}}=60\,\mathrm{Pa}$

书对桌面的压强为60 Pa。''',[47])
n='液体压强公式的推导与应用'
t=C[n].replace('p = F S = ρgh',r'$p=\frac{F}{S}=\rho gh$').replace('ρShg平面受到的压强','ρShg\n\n平面受到的压强')
body(n,t)
example(n,r'''有人说，设想你在万米深的“奋斗者”号全海深载人潜水器中把一只脚伸到外面的海水里，海水对你脚背的压力相当于2 000个人所受的重力！海水的压力果真有这么大吗？请通过估算加以说明。

解 因为是估算，海水的密度可以取ρ=1×10³ kg/m³，g取10 N/kg。脚背宽度取8~10 cm，脚背长度取12~15 cm，则脚背面积为96~150 cm²，近似取S=120 cm²=1.2×10⁻² m²。

万米深处海水的压强

$p=\rho gh=1\times10^3\,\mathrm{kg/m^3}\times10\,\mathrm{N/kg}\times10^4\,\mathrm m=10^8\,\mathrm{Pa}$

脚背所受的压力

$F=pS=10^8\,\mathrm{Pa}\times1.2\times10^{-2}\,\mathrm{m^2}=1.2\times10^6\,\mathrm N$

一个成年人的质量约为60 kg，所受的重力

$G=mg=60\,\mathrm{kg}\times10\,\mathrm{N/kg}=6\times10^2\,\mathrm N$

假设脚背所受的压力相当于n个成年人所受的重力，则

$n=\frac{1.2\times10^6\,\mathrm N}{6\times10^2\,\mathrm N}=2\,000$

估算结果表明，在万米深的海底，海水对脚背的压力确实相当于2 000个人所受的重力。

利用公式p=ρgh计算的时候，密度ρ的单位要用kg/m³，深度h的单位要用m，计算出的压强p的单位才是Pa。''',[53])
n='船闸的工作过程'
body(n,'''三峡大坝上、下游的水位差最大可达113 m。巨大的落差有利于生产可观的电力，但也带来了航运方面的问题：下游的船只驶往上游，怎样把这些船只举高一百多米？上游的船只驶往下游，又怎样让船只徐徐降落一百多米？解决这类问题的途径是修建船闸（图9.2-8）。

船闸由闸室和上、下游闸门以及上、下游阀门组成。图9.2-9描述了一艘轮船由上游通过船闸驶往下游的情况。

甲 关闭下游阀门B，打开上游阀门A，闸室和上游水道构成了一个连通器。

乙 闸室水面上升到跟上游水面相平后，打开上游闸门C，船驶入闸室。

丙 关闭上游闸门C和阀门A，打开下游阀门B，闸室和下游水道构成了一个连通器。

丁 闸室水面下降到跟下游水面相平后，打开下游闸门D，船驶向下游。''')
n='托里拆利实验与标准大气压'
t=C[n];t=t[:t.index('p_{0} =')]+r'''$p_0=\rho gh=13.6\times10^3\,\mathrm{kg/m^3}\times9.8\,\mathrm{N/kg}\times0.76\,\mathrm m=1.013\times10^5\,\mathrm{Pa}$

在粗略计算中，标准大气压可以取1×10⁵ Pa。'''
body(n,t)
n='浮力及称重法测量浮力'
t=C[n].replace('浸没\n\n①在','浸没在').replace('① “浸没”指物体完全处在液面下方。\n\n','').replace('铝块静止\n\n时','铝块静止时')
body(n,t+'\n\n“浸没”指物体完全处在液面下方。')
n='探究阿基米德原理'
t=C[n];tail=t.index('小桶所受物体所受');t=t[:tail]+'阿基米德原理不仅适用于液体，也适用于气体。'
t=t.replace('把测量的实验数据记录在下表中。','''把测量的实验数据记录在下表中。

| 序号 | 小桶所受的重力 G桶/N | 物体所受的重力 G物/N | 物体在水中时弹簧测力计的示数 F拉/N | 小桶和排开水所受的总重力 G总/N | 浮力 F浮/N | 排开的水所受的重力 G排/N |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | | | | | | |
| 2 | | | | | | |
| 3 | | | | | | |
| … | | | | | | |
''')
body(n,t)
example(n,r'''有一杯水、一杯盐水和一块重0.22 N、密度为1.1×10³ kg/m³的塑料块。

（1）该塑料块浸没在水中时所受的浮力是多少？

（2）若该塑料块在盐水中是漂浮的，浸在盐水中的体积是塑料块总体积的90%，则盐水的密度是多少？g取10 N/kg。

解 （1）根据塑料块所受的重力可以求得它的质量，再由体积、质量和密度的关系式就可以求得它的体积。

塑料块的质量

$m_{塑料}=\frac{G_{塑料}}{g}=\frac{0.22\,\mathrm N}{10\,\mathrm{N/kg}}=0.022\,\mathrm{kg}$

塑料块的体积

$V_{塑料}=\frac{m_{塑料}}{\rho_{塑料}}=\frac{0.022\,\mathrm{kg}}{1.1\times10^3\,\mathrm{kg/m^3}}=2\times10^{-5}\,\mathrm{m^3}$

浸没在水中的塑料块的体积V塑料等于它排开水的体积V排。根据阿基米德原理，塑料块受到浮力的大小等于它排开的水所受的重力

$F_{浮}=G_{排}=m_{水}g=\rho_{水}V_{排}g=1\times10^3\,\mathrm{kg/m^3}\times2\times10^{-5}\,\mathrm{m^3}\times10\,\mathrm{N/kg}=0.2\,\mathrm N$

（2）塑料块在盐水中是漂浮的，处于平衡状态，因此它所受浮力的大小等于它所受的重力，为0.22 N。根据阿基米德原理，可以求得排开盐水的质量。再由体积、质量和密度的关系式就可以求得盐水的密度。即

$m_{盐水}=\frac{G_{盐水}}{g}=\frac{0.22\,\mathrm N}{10\,\mathrm{N/kg}}=0.022\,\mathrm{kg}$

盐水密度

$\rho_{盐水}=\frac{m_{盐水}}{V_{盐水}}=\frac{0.022\,\mathrm{kg}}{2\times10^{-5}\,\mathrm{m^3}\times90\%}=1.22\times10^3\,\mathrm{kg/m^3}$

该塑料块浸没在水中所受的浮力为0.2 N。盐水的密度为1.22×10³ kg/m³。''',[76])
n='气球和飞艇的升空原理'
t=C[n];body(n,t[:t.index('20世')]+'\n')
n='微型密度计的设计依据及估算'
t=C[n].replace('0.87×10\n\n^{3} kg/m','0.87×10³ kg/m').replace('0.86×10\n\n^{3}~0.88×10^{3} kg/m是合格的','0.86×10³~0.88×10³ kg/m³是合格的')
body(n,t)
replace('功率的定义、公式和单位','P = W t',r'$P=\frac{W}{t}$'+'\n\n')
replace('功率的定义、公式和单位','^{3} W物体','^{3} W\n\n物体')
n='探究杠杆的平衡条件'
t=C[n].split('序号\n\n动力F_{1}')[0]
t=t.replace('把F_{1}、F_{2}、l_{1}、l_{2}的数据填入下表。','''把F_{1}、F_{2}、l_{1}、l_{2}的数据填入下表。

| 序号 | 动力 F₁/N | 动力臂 l₁/m | 阻力 F₂/N | 阻力臂 l₂/m |
| --- | --- | --- | --- | --- |
| 1 | | | | |
| 2 | | | | |
| 3 | | | | |
| 4 | | | | |
| 5 | | | | |
| 6 | | | | |
| … | | | | |
''')
body(n,t.replace('l_{1}\n\n和阻力臂','l_{1}和阻力臂'))
replace('滑轮组及省力条件','物重1 3 的力',r'物重$\frac{1}{3}$的力')
replace('机械效率的定义、公式及取值','η = W有用W总有用功',r'$\eta=\frac{W_{有用}}{W_{总}}$'+'\n\n有用功')
n='测量滑轮组的机械效率'
t=C[n].split('钩码所受提升的高度')[0]
body(n,t+'''

| 序号 | 钩码所受的重力 G/N | 提升的高度 h/m | 有用功 W有用/J | 拉力 F/N | 绳端移动的距离 s/m | 总功 W总/J | 机械效率 η |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | | | | | | | |
| 2 | | | | | | | |
| 3 | | | | | | | |
''')
example('力学中的功及做功条件',r'''目前，我国正在大力推广装配式建筑。这种建筑方式不仅施工效率高，还能大幅降低能耗，避免现场粉尘、泥浆等的污染，实现绿色施工（图11.1-5）。g取10 N/kg。

（1）把质量为1.5 t的构件匀速提升到30 m高的楼顶，竖直向上的拉力做了多少功？

（2）依据需要，又将这个构件沿水平方向匀速移动了3 m。在水平运动阶段，竖直向上的拉力又做了多少功？

解 （1）构件在竖直方向上做匀速直线运动，构件所受的拉力与重力大小相等，即

$F=G=mg=1.5\times10^3\,\mathrm{kg}\times10\,\mathrm{N/kg}=1.5\times10^4\,\mathrm N$

构件在竖直方向上移动的距离

$s=30\,\mathrm m$

所以，拉力做的功

$W=Fs=1.5\times10^4\,\mathrm N\times30\,\mathrm m=4.5\times10^5\,\mathrm J$

（2）拉力的方向竖直向上。构件在水平方向上移动了3 m，但在竖直方向上没有移动距离，即s′=0。所以，拉力做的功

$W'=Fs'=0$

在竖直上升阶段，拉力做的功为4.5×10⁵ J。在水平运动阶段，拉力做的功为0。''',[91])
example('功率的定义、公式和单位',r'''大石头的质量为6 t，起重机在15 s内将大石头沿竖直方向匀速提升1 m（图11.2-1），起重机提升大石头的功率是多少？g取10 N/kg。

解 因为匀速提升，起重机提升大石头的拉力与大石头所受的重力相等，即

$F=G=mg=6\times10^3\,\mathrm{kg}\times10\,\mathrm{N/kg}=6\times10^4\,\mathrm N$

大石头在拉力的方向上移动的距离

$s=1\,\mathrm m$

所以拉力做的功

$W=Fs=6\times10^4\,\mathrm N\times1\,\mathrm m=6\times10^4\,\mathrm J$

功率

$P=\frac{W}{t}=\frac{6\times10^4\,\mathrm J}{15\,\mathrm s}=4\times10^3\,\mathrm W$

起重机提升大石头的功率是4×10³ W。''',[94,95])
example('探究杠杆的平衡条件',r'''动物园内，一位物理老师利用一个小小的弹簧测力计，就测出了一头大象的质量（图12.1-5甲）。测量时用一根长度为12 m的槽钢作为杠杆。如图12.1-5乙所示，吊钩固定于槽钢的中点O。当槽钢水平静止时，弹簧测力计的示数F₁为200 N。测得l₁为6 m，l₂为4 cm。若不计铁笼的质量，请估算大象的质量。g取10 N/kg。

解 人通过弹簧测力计对杠杆的拉力为动力F₁=200 N，动力臂l₁=6 m；不计铁笼的质量，则大象对杠杆的拉力为阻力F₂，它等于大象所受的重力G，阻力臂l₂=4 cm=0.04 m。

根据杠杆的平衡条件F₁l₁=F₂l₂，有

$F_2=\frac{F_1l_1}{l_2}=\frac{200\,\mathrm N\times6\,\mathrm m}{0.04\,\mathrm m}=3\times10^4\,\mathrm N$

大象的质量

$m=\frac{G}{g}=\frac{F_2}{g}=\frac{3\times10^4\,\mathrm N}{10\,\mathrm{N/kg}}=3\times10^3\,\mathrm{kg}=3\,\mathrm t$

大象的质量是3 t。''',[112])
example('机械效率的定义、公式及取值',r'''起重机把质量为0.5 t的重物匀速提升了3 m，而它的电动机所做的功是3.4×10⁴ J，起重机的机械效率是多少？g取10 N/kg。

解 起重机匀速提升重物所用的力与物体所受的重力大小相等

$F=G=mg=0.5\times10^3\,\mathrm{kg}\times10\,\mathrm{N/kg}=5\times10^3\,\mathrm N$

起重机提升重物所做的功是有用功

$W_{有用}=Fh=5\times10^3\,\mathrm N\times3\,\mathrm m=1.5\times10^4\,\mathrm J$

起重机的电动机所做的功是总功

$W_{总}=3.4\times10^4\,\mathrm J$

因此，起重机的机械效率

$\eta=\frac{W_{有用}}{W_{总}}=\frac{1.5\times10^4\,\mathrm J}{3.4\times10^4\,\mathrm J}=0.44=44\%$

这台起重机的机械效率为44%。''',[124])

replace('气压计的构造与测量原理','水银\n\n气压计','水银气压计')
replace('轮船的排水量与漂浮原理','轮船轮船','轮船 轮船')
replace('等臂、省力与费力杠杆','是不\n\n动的','是不动的')
replace('探究重力与质量的关系及重力计算','g = 9.8 N/kg在粗略','g = 9.8 N/kg\n\n在粗略')

replace('水能和风能的利用','我们的祖先很早就开始利用水能和风能了。','')
replace('水能和风能的利用','到19 世纪，人类开始利用水能发电。','')
# Typographical normalization is limited to explicit formula layouts and paragraph boundaries.
for n,t in C.items():
 t=P.get(n,{}).get('detail',t)
 t=t.replace('W = Fs在国际','W = Fs\n\n在国际').replace('W总= W有用+W额外大量','W总= W有用+W额外\n\n大量')
 t=re.sub(r'(?<=10)\s+(?=\^\{)', '', t)
 if t!=C[n] or n in P:body(n,t)
(R/'patches.json').write_text(json.dumps(P,ensure_ascii=False,indent=2))
print('corrected records',len(P))
