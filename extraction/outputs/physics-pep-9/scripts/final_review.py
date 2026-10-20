"""Final field-level corrections after full-page review of diagrams and formulas."""
from pathlib import Path
import csv,json,re
R=Path(__file__).resolve().parents[1]
P=json.loads((R/'patches.json').read_text())
rows=list(csv.DictReader((R/'knowledge_points.csv').open(encoding='utf-8-sig')))
T={r['knowledge_point']:r['detail'].split('![')[0].strip() for r in rows}
def put(n,t):P.setdefault(n,{})['detail']=t.strip()
def edit(n,a,b):put(n,P.get(n,{}).get('detail',T[n]).replace(a,b))
put('欧姆定律在串联电路中的应用',r'''为开展科技活动，某同学设计了一个用开关S₂控制电阻为R₁的电阻器两端电压的工作电路，如图17.4-1所示，电源电压为18 V。已知通过电阻为R₁的电阻器的电流与其两端电压的关系如图17.4-2所示。

（1）电阻R₁是多少？

（2）闭合开关S₁，要使开关S₂断开时电阻为R₁的电阻器两端的电压变为16 V，另一个电阻器的电阻R₂应为多少？

解（1）从图17.4-2可知，电阻为R₁的电阻器两端的电压U′为18 V时，通过它的电流I′为0.9 A。由欧姆定律可得

$$R_1=\frac{U'}{I'}=\frac{18\,\mathrm{V}}{0.9\,\mathrm{A}}=20\,\Omega$$

（2）S₂断开后，电阻为R₁的电阻器两端的电压U₁为16 V。根据欧姆定律，此时通过电阻为R₁的电阻器的电流

$$I_1=\frac{U_1}{R_1}=\frac{16\,\mathrm{V}}{20\,\Omega}=0.8\,\mathrm{A}$$

由于S₂断开时电阻为R₁的电阻器和电阻为R₂的电阻器是串联的，因此它们两端的电压之和等于电源电压U。此时电阻为R₂的电阻器两端的电压

$$U_2=U-U_1=18\,\mathrm{V}-16\,\mathrm{V}=2\,\mathrm{V}$$

因为串联电路中各处的电流相等，所以此时通过电阻为R₂的电阻器的电流

$$I_2=I_1=0.8\,\mathrm{A}$$

由欧姆定律可得

$$R_2=\frac{U_2}{I_2}=\frac{2\,\mathrm{V}}{0.8\,\mathrm{A}}=2.5\,\Omega$$

欧姆定律公式中的电压、电流、电阻是对同一个研究对象而言的，因此在应用欧姆定律解决问题的时候，必须明确：公式中的三个量是不是这个研究对象的？而串、并联电路中的电流关系、电压关系，描述的是不同研究对象之间的相互联系。

在解决串、并联电路的问题时，我们可以先选择某个导体为研究对象，用欧姆定律求解通过它的电流或它两端的电压，再通过该导体与其他导体的串、并联关系求得题目的答案。我们也可以先通过两个导体的串、并联关系求得通过某一个导体的电流或它两端的电压，再以该导体为研究对象，用欧姆定律求解题目的答案。''')
put('欧姆定律在并联电路中的应用',r'''如图17.4-3所示，一个电阻器的电阻R₁为10 Ω，开关S₁闭合、S₂断开时，电流表的示数为1.2 A，再把S₂闭合后，电流表的示数变为1.5 A。

（1）开关S₁闭合、S₂断开时，电阻为R₁的电阻器两端的电压是多少？

（2）另一个电阻器的电阻R₂是多少？

解（1）开关S₁闭合、S₂断开时，电流表的示数等于通过电阻为R₁的电阻器的电流I₁。由欧姆定律可得此时电阻为R₁的电阻器两端的电压

$$U_1=I_1R_1=1.2\,\mathrm{A}\times10\,\Omega=12\,\mathrm{V}$$

（2）由于两个电阻器是并联的，它们两端的电压相等，即U₂=U₁=12 V，且电流表的示数等于通过两个支路的电流之和I，因此S₂闭合后通过电阻为R₂的电阻器的电流

$$I_2=I-I_1=1.5\,\mathrm{A}-1.2\,\mathrm{A}=0.3\,\mathrm{A}$$

由欧姆定律可得

$$R_2=\frac{U_2}{I_2}=\frac{12\,\mathrm{V}}{0.3\,\mathrm{A}}=40\,\Omega$$''')
put('原子核的结构与核能','''我们知道，分子是由原子构成的，原子的中心是原子核，原子核周围有一定数目的电子在运动。科学家通过进一步的研究表明，原子核还有如图22.2-1所示的更精细的内部结构：原子核通常由质子和中子组成，质子带正电荷，其电荷量跟电子的电荷量相等，中子不带电；质子的质量大约是电子的1 836倍，中子和质子的质量几乎相同。质子和中子构成非常小的原子核，就像几颗豆粒挤在一个非常大的广场中央。

质子、中子依靠强大的核力紧密地结合在一起，因此原子核十分牢固，要使它们分裂或结合是极其困难的。但是，一旦质量较大的原子核发生分裂或者质量较小的原子核相互结合，就有可能释放出惊人的能量。这种能量就是核能（nuclear energy）。

随着科学技术的发展，科学家发现了更多的新粒子，并发现质子、中子等本身也有自己的复杂结构。人们对微观世界的探索在不断深入。''')
edit('电流的磁效应','\n\n联系。','')
edit('电流的磁效应','偏转；\n\n切断','偏转；切断')
put('房屋保温模型的对比试验','''（4）制作模型与测试。在真正实施设计方案前，需要制作一个简易模型来模拟我们的家，通过测试来检验方案是否有效，并提出优化建议。小组内进行讨论：如何在测试中简单有效地模拟我们的家？给“家”安装哪些保温材料？怎样检验保温效果？

为了方便起见，可以选择身边容易获取、安装，与实际保温材料热导率相近的材料，将它安装在“家”中的相应部位。为了检验保温效果，可以将质量相等的冰块装在塑料袋中，分别放入没有保温材料和装有所选保温材料的“家”中，将“家”放置在相同的环境下，经过相同的时间后将冰块取出并进行比较，通过比较冰块质量的变化来评估设计的保温效果。

在工程技术中，方案最终实施前，通常需要制作简易模型来评估设计的可行性，以达到节约成本、保证质量的目的。''')
edit('房屋保温的原理、材料与热导率','在阅资料得知','查阅资料得知')
n='发电机、交流电及频率';t=T[n];note='之前我们学习的电路用电池供电，电路中的电流从电池的正极流向负极，方向不改变。这种电流叫作直流。';t=t.replace(note,'');t=re.sub(r'发的\s+电，','发的电，',t);put(n,t+'\n\n'+note)
# Repair the source text layer's equation/line-order errors, keeping exact numeric values.
edit('波长、频率与电磁波的传播','c = 2.997 924 58×10\n\n⁸ m/s','c=2.997 924 58×10⁸ m/s')
edit('激光的性质与应用','10\n\n⁻¹⁸s','10⁻¹⁸ s')
n='能量转化与转移的方向性及能源挑战';t=T[n];t=t.replace('热\n\n⁷ J/kg的标准煤来计算，1950值为2.93×10年','热值为2.93×10⁷ J/kg的标准煤来计算，1950年');put(n,t)
# Diagram labels are preserved by the page image, never interleaved into a sentence.
n='家庭电路、电功率过大与电流过大';t=T[n];a=t.index('根据电功率');b=t.index('用电器采用并联的方式接在电路中。')+len('用电器采用并联的方式接在电路中。');t=t[:b]+'\n\n'+t[a:];t=t.replace('I = P U','I=P/U');put(n,t)
n='电流过大的防护：熔断器与低压断路器';t=T[n];t=re.sub(r'保护\s+.*?作用。于是','保护作用。于是',t,flags=re.S);put(n,t)
# These small diagram symbols have no unambiguous linear text equivalent; use their source pages.
edit('电阻、电阻器与电阻的单位','²的家用铜导线，电阻为百分之几欧姆，通截面积1 mm','截面积1 mm²的家用铜导线，电阻为百分之几欧姆，通')
edit('电阻、电阻器与电阻的单位','长1 m、横\n\n截面积','长1 m、横截面积')
# Remove task-only tails; experiment questions and intentionally empty measurement fields stay intact.
edit('半导体','集成电路是20世纪最重要的发明之一，已经广泛应用于各行各业。','')
for n,tail in [('简易直流电动机的制作与换向方法','调试自己制作的简易电动机，让它更好地工作起来。'),('发光二极管的单向导电性','请你将LED接入某电路中，闭合开关，观察LED是否发光，判断电路中电流的方向。')]:edit(n,tail,'')
n='通电螺线管的磁场及探究实验';t=P.get(n,{}).get('detail',T[n]);t=t.split('通电螺线管的极性跟电流方向有什么关系？')[0];put(n,t)
n='磁场对通电导线的作用';t=T[n];t=t.split('如果把一个通电的线圈放到磁场中')[0];put(n,t)
# No new definition of magnetic declination is invented: the book states only the directional deviation.
n='家庭电路设计的安全原则';t=P[n]['detail'];t=t.replace('家庭电路中使用到的断路器、导线等配电器材进行选型，使器材之间相互匹配。','如果你有兴趣，最后还可对家庭电路中使用到的断路器、导线等配电器材进行选型，使器材之间相互匹配。');put(n,t)
n='化石能源及可再生、不可再生能源';put(n,'我们今天'+T[n])
n='核电站的辐射与核废料处理';put(n,P[n]['detail']+'\n\n高温气冷堆的安全性进一步提高，在发生异常情况时，可以在不需人为干预的情况下保持安全状态。')
# Additional nonhistorical physics from mixed historical sidebars.
put('热与功的关系及热量的能量含义','''证明做了多少机械功，就有多少机械能转化成与热相关的能量。

宏观的热现象原来是物体内部大量分子的无规则运动的表现，物体内部的能量就是前面讲过的内能。热量不表示物质所含“热质”的多少，而表示在热传递过程中传递的能量的多少。''')
put('汽轮机、空气喷气发动机与火箭发动机','''大型锅炉产生的高温高压水蒸气直接喷射到汽轮机的叶片上，使汽轮机转动。

空气喷气发动机，它需要用大气中的氧气来助燃，向后喷出高速气体，从而获得前进的动力。火箭上使用的喷气发动机自带燃料和氧化剂，工作时不需要空气，可以在大气层外工作。''')
# Ensure prose ends at a complete sentence; no unsolved tasks are promoted into examples.
for v in P.values():
 if 'detail' in v:v['detail']=re.sub(r'\n{3,}','\n\n',v['detail']).strip()
(R/'patches.json').write_text(json.dumps(P,ensure_ascii=False,indent=2)+'\n')
print('final patches',len(P))
