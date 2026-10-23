"""Visual corrections to selected regions; no exercise answers are supplied."""
from pathlib import Path
import json,runpy,re
R=Path(__file__).resolve().parents[1]
B=runpy.run_path(str(R/'scripts/build.py')); reg=B['region']
S=json.loads((R/'selection.json').read_text());cand=json.loads('[]')
raw=[json.loads(t)['detail'] for t in (R/'transcription_candidates.jsonl').read_text().splitlines()]
def get(i):return S[i-1].get('detail',raw[i-1])
def d(i,t):S[i-1]['detail']=t.strip()
def fix(i,a,b):
 t=get(i)
 if a not in t:raise ValueError((i,a))
 d(i,t.replace(a,b))
def add(i,t):d(i,get(i)+'\n\n'+t)
def regions(i,rr):S[i-1]['regions']=rr
def base(i,rr):regions(i,rr);d(i,''.join(reg(r) for r in rr))
# Reading order, sentence boundaries and experiment annotations.
base(2,[[9,290,730,56,307],[9,60,165,307,550]])
fix(2,'以及反应产生（如离子反应、氧化还原反应、取代反应、的各种现象','以及反应产生的各种现象')
d(7,get(7).removesuffix('有些液'))
add(7,'有些液溶胶是透明的，用肉眼很难与溶液相区分。')
d(9,'与实验有关的图标及说明：\n\n护目镜：进行化学实验需要佩戴护目镜，以保护眼睛。\n洗手：实验结束后，离开实验室前需用肥皂等清洗双手。\n用电：实验中会用到电器。禁止湿手操作，实验完毕应及时切断电源。\n排风：实验中会用到或产生有害气体，或产生烟、雾。应开启排风管道或排风扇。\n热烫：实验中会遇到加热操作，或用到温度较高的仪器。应选择合适的工具进行操作，避免直接触碰。\n明火：实验中会用到明火。要正确使用火源，并束好长发、系紧宽松衣物。\n锐器：实验中会用到锋利物品。应按照实验操作使用，避免锐器指向自己或他人，防止扎伤或割伤。')
d(10,get(10).removeprefix('得名。'))
fix(11,'不同的酸+，不同的碱溶液中都含有OH溶液中都含有H-。','不同的酸溶液中都含有H⁺，不同的碱溶液中都含有OH⁻。')
fix(13,'干燥的NaCl 固体、KNO3 固体都不导电，①。但是，NaCl溶液、KNO3溶液却都能够蒸馏水也不导电导电。','干燥的NaCl固体、KNO3固体都不导电，蒸馏水也不导电。但是，NaCl溶液、KNO3溶液却都能够导电。')
add(13,'① 严格地说，蒸馏水也能导电，只是导电能力非常弱，用上述实验装置不能测出。')
fix(14,'在水分子的作用下，Na和Cl-','在水分子的作用下，Na⁺和Cl⁻');fix(14,'+ 和ClNa-','Na⁺和Cl⁻')
d(15,'电解质溶于水或受热熔化时，形成自由移动的离子的过程叫做电离。电解质的电离可以用电离方程式表示（为简便起见，一般仍用离子符号表示水合离子）。例如：\n\nNaCl = Na⁺ + Cl⁻\nKNO₃ = K⁺ + NO₃⁻\nHCl = H⁺ + Cl⁻\nH₂SO₄ = 2H⁺ + SO₄²⁻\nHNO₃ = H⁺ + NO₃⁻\n\n可以看出，HCl、H₂SO₄和HNO₃在水溶液中都能电离出H⁺，因此，我们可以从电离的角度认识酸的本质。即电离时生成的阳离子全部是氢离子（H⁺）的化合物叫做酸。\n\n① 氢原子失去电子后，剩余1个质子构成的核，即氢离子。氢离子是“裸露”的质子，半径很小，易与水分子结合成水合氢离子，通常用H₃O⁺表示。为了简便，也常把H₃O⁺写作H⁺。')
d(16,'在对研究对象进行实验观察和证据推理的基础上，利用简化、抽象和类比等方法，将反映研究对象的本质特征形成一种概括性的描述或认识思路，这就是模型。模型在科学认识中具有描述、解释和预测等功能，是理论发展的一种重要方式。化学中的模型有实物模型、理论模型等，其中，理论模型应用范围最广。\n\n电离模型，即电解质溶于水会自动地解离成离子，而不是当时流行的说法——离子是通电后才产生的。电离模型很好地解释了酸、碱、盐溶液的某些性质，如酸、碱的强度等，因此发展成为近代的电离理论。')
d(17,'【实验1-3】向盛有2 mL Na₂SO₄稀溶液的试管中加入2 mL BaCl₂稀溶液（二者恰好完全反应），观察现象并分析。\n\n通过上述现象和分析，我们可以得出这样的结论：当Na₂SO₄稀溶液与BaCl₂稀溶液混合时，Na⁺、Cl⁻都没有发生化学反应；而SO₄²⁻与Ba²⁺发生了化学反应，生成难溶的BaSO₄白色沉淀。也就是说，对于化学反应：\nNa₂SO₄ + BaCl₂ = 2NaCl + BaSO₄↓\n从微观角度看，其实质是：\nBa²⁺ + SO₄²⁻ = BaSO₄↓\n\n电解质在溶液中的反应实质上是离子之间的反应，这样的反应属于离子反应。用实际参加反应的离子的符号来表示反应的式子叫做离子方程式。离子方程式的书写一般按以下步骤（以Na₂SO₄溶液与BaCl₂溶液的反应为例）：\n（1）写出反应的化学方程式：\nNa₂SO₄ + BaCl₂ = 2NaCl + BaSO₄↓\n（2）把易溶于水且易电离的物质（如强酸、强碱和大部分可溶性盐）写成离子形式，难溶的物质、气体和水等仍用化学式表示。上述化学方程式可改写成：\n2Na⁺ + SO₄²⁻ + Ba²⁺ + 2Cl⁻ = 2Na⁺ + 2Cl⁻ + BaSO₄↓\n（3）删去方程式两边不参加反应的离子，并将方程式化为最简：\nBa²⁺ + SO₄²⁻ = BaSO₄↓\n（4）检查离子方程式两边各元素的原子个数和电荷总数是否相等。')
d(18,'以HCl与NaOH、HCl与KOH、H₂SO₄与NaOH、H₂SO₄与KOH的反应为例（原表见图）。\n\n上面的4个反应都是中和反应，虽然4个反应的化学方程式不同，但它们的离子方程式却是相同的。这表明：强酸与强碱发生中和反应的实质是，强酸电离出来的H⁺与强碱电离出来的OH⁻结合生成H₂O。\n\nH⁺ + OH⁻ = H₂O\n\n可以看出，离子方程式不仅可以表示某个具体的化学反应，还可以表示同一类型的离子反应。')
# Core introductory redox examples remain with the explanation.
d(20,'2CuO + C ─高温→ 2Cu + CO₂↑\nFe₂O₃ + 3CO ─高温→ 2Fe + 3CO₂\n\n'+get(20))
fix(21,'2Na + Cl2 △= 2NaClH2','2Na + Cl₂ ─△→ 2NaCl\n\nH2');fix(21,'点燃 2HClH2 + Cl2 =','H₂ + Cl₂ ─点燃→ 2HCl')
fix(23,'CuO + H2 △= Cu + H2O','CuO + H₂ ─△→ Cu + H₂O');fix(23,'2Na + Cl2 △= 2NaCl','2Na + Cl₂ ─△→ 2NaCl')
fix(24,'在催化转化器中，汽车尾气中的CO','在催化转化器中，汽车尾气中的CO和NO在催化剂的作用下发生反应，生成CO₂和N₂。')
fix(25,'那从钠的原子结构来看','从钠的原子结构来看')
fix(26,'密度：0.97 g/cm','密度：0.97 g/cm³')
fix(27,'2Na\u2005+\u2005O2 △=\u2005Na2O2过氧化钠','2Na + O₂ ─△→ Na₂O₂（过氧化钠）')
fix(29,'氧化钠与水反应生成氢氧化钠，过氧化钠与水反应【实验2-3】','氧化钠与水反应生成氢氧化钠，过氧化钠与水反应的情况又是怎样的呢？\n\n【实验2-3】')
fix(30,'有何现象碳酸钠','有何现象。\n\n碳酸钠');fix(30,'（Na2CO3·xH2O）①','（Na₂CO₃·xH₂O）')
add(30,'① 根据结晶条件的不同，生成的水合碳酸钠有Na₂CO₃·H₂O、Na₂CO₃·7H₂O、Na₂CO₃·10H₂O等。')
fix(31,'△2NaHCO3= Na2CO3\u2005+\u2005H2O\u2005+\u2005CO2↑','2NaHCO₃ ─△→ Na₂CO₃ + H₂O + CO₂↑')
d(32,'氨碱法以食盐、石灰石为主要原料制取碳酸钠，又称索尔维法。联合制碱法将制取碳酸钠和合成氨联合起来，也称侯氏制碱法。侯氏制碱法提高了食盐的转化率，缩短了生产流程，减少了对环境的污染。')
# Keep the verified flame-colour table in a usable row order.
t=get(33);start=t.index('一些金属元素的焰色');d(33,t[:start]+'一些金属元素的焰色：\n\n| 金属元素 | 焰色 |\n|---|---|\n|锂|紫红色|\n|钠|黄色|\n|钾|紫色|\n|铷|紫色|\n|钙|砖红色|\n|锶|洋红色|\n|钡|黄绿色|\n|铜|绿色|\n\n节日燃放的五彩缤纷的烟花，所呈现的就是锂、钠、钾、锶、钡等金属元素的焰色。\n\n① 蓝色钴玻璃可以滤去黄光，便于观察钾的焰色。')
fix(35,'△=2NaCl2Na\u2005+\u2005Cl2△2Fe\u2005+\u20053Cl2=2FeCl3Cu\u2005+\u2005Cl2 △=CuCl2','2Na + Cl₂ ─△→ 2NaCl\n2Fe + 3Cl₂ ─△→ 2FeCl₃\nCu + Cl₂ ─△→ CuCl₂')
fix(35,'点燃H2\u2005+\u2005Cl2= 2HClHCl','H₂ + Cl₂ ─点燃→ 2HCl\n\nHCl')
fix(36,'Cl2 + H2OHCl + HClO次氯酸次氯酸','Cl₂ + H₂O ⇌ HCl + HClO（次氯酸）\n\n次氯酸')
fix(37,'2HClO 光照=2HCl\u2005+\u2005O2↑','2HClO ─光照→ 2HCl + O₂↑')
fix(40,'△=MnCl2\u2005+\u2005Cl2↑+\u20052H2OMnO2 + 4HCl(浓)','MnO₂ + 4HCl(浓) ─△→ MnCl₂ + Cl₂↑ + 2H₂O')
fix(42,'+2H+\u2005=2Ag+\u2005+CO2↑ +H2OAg2CO3','Ag₂CO₃ + 2H⁺ = 2Ag⁺ + CO₂↑ + H₂O');fix(42,'检验Cl时','检验Cl⁻时')
d(43,get(43).replace('验的目的是','水质检验的目的是',1))
# Formulas, missing denominators and their first worked examples.
d(44,get(44)[:get(44).index('n =')]+ 'n = N/N_A。\n\n'+reg([59,325,535,218,550]))
d(45,'国际单位制（SI）的7个基本单位：\n\n|物理量|单位名称|单位符号|\n|---|---|---|\n|长度|米|m|\n|质量|千克（公斤）|kg|\n|时间|秒|s|\n|电流|安［培］|A|\n|热力学温度|开［尔文］|K|\n|物质的量|摩［尔］|mol|\n|发光强度|坎［德拉］|cd|')
d(46,'1 mol任何粒子集合体都约含有6.02×10²³个粒子。1 mol任何粒子或物质的质量以克为单位时，其数值都与该粒子的相对原子质量或相对分子质量相等。\n\n单位物质的量的物质所具有的质量叫做摩尔质量。摩尔质量的符号为M，常用的单位为g/mol（或g·mol⁻¹）。例如：Na的摩尔质量是23 g/mol；KCl的摩尔质量是74.5 g/mol；Cl₂的摩尔质量是71 g/mol；CO₃²⁻的摩尔质量是60 g/mol。\n\n物质的量（n）、质量（m）和摩尔质量（M）之间存在着下述关系：n = m/M。\n\n【例题1】26.5 g Na₂CO₃的物质的量是多少？\n【解】Na₂CO₃的相对分子质量为106，摩尔质量为106 g·mol⁻¹。\nn(Na₂CO₃) = m(Na₂CO₃)/M(Na₂CO₃) = 26.5 g/(106 g·mol⁻¹) = 0.25 mol\n答：26.5 g Na₂CO₃的物质的量是0.25 mol。')
fix(48,'Vm =   Vn','V_m = V/n。\n\n')
base(49,[[62,548,698,63,385]])
# Readback replaces the fraction while keeping the complete concentration explanation.
d(49,'在化学中，我们常用单位体积溶液里所含溶质B的物质的量来表示溶液的浓度，叫做物质的量浓度，符号为c_B。\n\nc_B = n_B/V\n\n物质的量浓度常用的单位为mol/L（或mol·L⁻¹）。如果1 L溶液中含有1 mol溶质，这种溶液中溶质的物质的量浓度就是1 mol/L。\n\nB代表各种溶质。')
add(50,'① aq表示水溶液，如NaOH(aq)表示NaOH水溶液。')
fix(51,'（对于玻璃磨口瓶塞，应在瓶塞与瓶口处垫使用容量瓶时','使用容量瓶时')
add(52,'① 实验室中要求准确称量物质的质量时，一般用分析天平，精度可达0.0001 g。')
fix(54,'①量取所需体积的1.00 mol / L NaCl溶液并注入烧杯中。用量筒','用量筒量取所需体积的1.00 mol/L NaCl溶液并注入烧杯中。')
fix(55,'密度：7.87 g/cm','密度：7.87 g/cm³')
d(56,get(56)[:get(56).index('\n\n')]+'\n\nFe − 2e⁻ → Fe²⁺\nFe − 3e⁻ → Fe³⁺')
fix(57,'3Fe\u2009+\u20094H2O(g)高温 Fe3O4\u2009+\u20094H2① =','3Fe + 4H₂O(g) ─高温→ Fe₃O₄ + 4H₂\n\n① g表示气态，s表示固态，l表示液态。')
(R/'selection.json').write_text(json.dumps(S,ensure_ascii=False,indent=2))
