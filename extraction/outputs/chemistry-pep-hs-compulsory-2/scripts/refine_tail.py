from pathlib import Path
import json,re
R=Path(__file__).resolve().parents[1];S=json.loads((R/'selection.json').read_text());D={s['name']:s for s in S}
def edit(n,f):D[n]['detail']=f(D[n]['detail'])
def put(n,t):D[n]['detail']=t
def cut(n,t):edit(n,lambda x:x.split(t)[0].rstrip())
edit('淀粉检验与糖类水解',lambda x:x.replace('C12H22O11 + H2OC6H12O6 + C6H12O6','\n\nC₁₂H₂₂O₁₁（蔗糖）+ H₂O ─催化剂→ C₆H₁₂O₆（葡萄糖）+ C₆H₁₂O₆（果糖）').replace('(C6H10O5)n + nH2OnC6H12O6','(C₆H₁₀O₅)ₙ（淀粉或纤维素）+ nH₂O ─催化剂→ nC₆H₁₂O₆（葡萄糖）'))
edit('糖类在人体中的变化与制取乙醇',lambda x:x.replace('C6H12O62C2H5OH + 2CO2↑','\n\nC₆H₁₂O₆ ─酶→ 2C₂H₅OH + 2CO₂↑'))
cut('蛋白质的组成、水解与氨基酸','研究蛋白质的结')
edit('油脂的组成、结构与物理性质',lambda x:re.sub('其结构可以表示为：.*?油脂结构中','其结构见原图。\n\n油脂结构中',x))
edit('金属冶炼的方法与反应原理',lambda x:x.replace('2HgO △=2Hg + O2↑','\n2HgO ─加热→ 2Hg + O₂↑\n\n').replace('MgCl2(熔融)= Mg + Cl2↑2Al2O3(熔融)=4Al + 3O2↑2NaCl(熔融)=2Na + Cl2↑','\nMgCl₂（熔融）─电解→ Mg + Cl₂↑\n2Al₂O₃（熔融）─电解、冰晶石→ 4Al + 3O₂↑\n2NaCl（熔融）─电解→ 2Na + Cl₂↑\n\n').replace('Fe2O3 + 2Al= 2Fe + Al2O3','\nFe₂O₃ + 2Al ─高温→ 2Fe + Al₂O₃'))
edit('合理利用金属资源与回收铝的能耗',lambda x:x.split('\n\n')[0]+'\n\n计算表明，生产1 mol铝消耗的电能至少为1.8×10⁶ J，回收铝质饮料罐得到铝与从铝土矿制铝相比，前者的能耗仅为后者的3%～5%。')
edit('海水水资源与化学资源的利用',lambda x:x.replace('18 t，约占地球上总水量的海水中水的储量约为1.3×1097％。','海水中水的储量约为1.3×10¹⁸ t，约占地球上总水量的97％。'))
edit('海水中的化学元素及富集程度',lambda x:x.split('例如，')[0]+'例如，海水中金元素的总储量约为5×10⁶ t，而1 t海水中金元素的含量仅为4×10⁻⁶ g。海洋还是一个远未充分开发的巨大化学资源宝库。')
cut('海水提溴的吹出法','请分析并讨论')
edit('煤的气化、直接液化与间接液化',lambda x:x.replace('= CO + H2C + H2O(g)','\n\nC + H₂O(g) ─高温→ CO + H₂\n\n'))
cut('天然气水合物','目前，开发利用')
for old,new in [('C16H34加热、加压 C8H18 + C8H16','C₁₆H₃₄ ─催化剂、加热、加压→ C₈H₁₈ + C₈H₁₆'),('C8H18加热、加压 C4H10 + C4H8','C₈H₁₈ ─催化剂、加热、加压→ C₄H₁₀ + C₄H₈'),('C4H10加热、加压  CH4  + C3H6','C₄H₁₀ ─催化剂、加热、加压→ CH₄ + C₃H₆'),('C4H10加热、加压 C2H6  + C2H4','C₄H₁₀ ─催化剂、加热、加压→ C₂H₆ + C₂H₄')]:edit('石油的分馏、裂化、裂解与结构调整',lambda x,o=old,n=new:x.replace(o,n))
edit('生物质资源的利用',lambda x:'人们利用'+x.split('人们利用',1)[1])
cut('大宗化学品与精细化学品','生产精细化')
edit('DDT的稳定性、生物富集及抗药性',lambda x:'DDT'+x)
cut('营养强化剂','随着食品工业')
put('水华的形成及影响','水中氮、磷元素过多，造成藻类疯长，消耗水中溶解的氧，使水体变成浑浊的绿色，水质恶化。')
D['水华的形成及影响']['regions']=[[124,219,285,388,550]]
put('环氧乙烷生产工艺的不同反应','''以乙烯为原料生产环氧乙烷，过去使用的氯代乙醇法主要包括以下反应：
CH₂=CH₂ + Cl₂ + H₂O → ClCH₂CH₂OH + HCl
2ClCH₂CH₂OH + Ca(OH)₂ → 2环氧乙烷 + CaCl₂ + 2H₂O（环状结构式见原图）
总的反应可表示为：
CH₂=CH₂ + Cl₂ + Ca(OH)₂ → 环氧乙烷 + CaCl₂ + H₂O（环状结构式见原图）
现代石油化工采用银作催化剂，可以实现一步完成：
2CH₂=CH₂ + O₂ ─Ag、加热→ 2环氧乙烷（环状结构式见原图）''')
put('减量化、再利用与再循环','开发和利用自然资源，必须站在人与自然和谐共生的高度，遵循减量化（reduce）、再利用（reuse）和再循环（recycle）的原则，践行绿色发展理念，保护生态环境。')
cut('人工光合作用的资源转化设想','人工光合作用研究的')
put('环境污染物的分析与鉴定方法','应用光谱分析、滴定分析等化学分析方法对环境中的污染物进行分析和鉴定；研究大气中PM₁₀浓度、PM₂.₅浓度和臭氧浓度；测定土壤和水样品的成分，检测其中的农药残留和废弃物污染等。')
D['环境污染物的分析与鉴定方法']['regions'][0][1]=204
# Four effective reference appendices; index is navigation rather than a knowledge point.
for c,t,n,p,detail in [
('附录Ⅱ','部分酸、碱和盐的溶解性表（室温）','室温下部分酸、碱和盐的溶解性',132,'“溶”表示那种物质可溶于水，“难”表示难溶于水，“微”表示微溶于水，“挥”表示挥发性，“—”表示那种物质不存在或遇到水就分解了。\n\n室温下各阳离子与OH⁻、NO₃⁻、Cl⁻、SO₄²⁻、CO₃²⁻对应的完整溶解性表见原图。'),
('附录Ⅲ','一些常见元素中英文名称对照表','常见元素符号及中英文名称',133,'一些常见元素的元素符号、中文名称（拼音）和英文名对照见原表。'),
('附录Ⅳ','相对原子质量表','相对原子质量及表中符号含义',134,'相对原子质量表按照元素符号的字母次序排列。\n1. 相对原子质量录自国际纯粹与应用化学联合会（IUPAC）公布的“标准相对原子质量2009”，以¹²C=12为基准。\n2. 相对原子质量加方括号的为放射性元素半衰期最长的同位素的质量数。\n3. 相对原子质量末尾数的不确定度加注在其后的括号内。\n4. [a; b]表示该元素的相对原子质量依据其同位素丰度变化而介于a和b之间。'),
('元素周期表','元素周期表','元素周期表及图例',138,'元素周期表的周期、族、元素符号、名称、相对原子质量、核外电子层及元素分类见教材原图。')]:
 S.append(dict(chapter=c,topic=t,name=n,regions=[[p,58,765]],detail=detail,notes=['表格完整保留教材原图，不将多列对应关系乱序转录。']))
# Repair predictable chemistry subscripts only, never numbers in quantities or section labels.
sub=str.maketrans('0123456789','₀₁₂₃₄₅₆₇₈₉')
formula=re.compile(r'(?<![A-Za-z])(?:[A-Z][a-z]?(?:\d+)?|\((?:[A-Z][a-z]?\d*)+\)\d*){1,}(?![A-Za-z])')
for s in S:
 t=s['detail']
 t=formula.sub(lambda m:re.sub(r'\d+',lambda z:z[0].translate(sub),m[0]),t)
 t=t.replace('CnH2n+2','CₙH₂ₙ₊₂').replace('Cn(H₂O)m','Cₙ(H₂O)ₘ').replace('(C₆H₁₀O₅)n','(C₆H₁₀O₅)ₙ').replace('CH₄·nH₂O','CH₄·nH₂O')
 s['detail']=t
 s['visual_status']='reviewed'
(R/'selection.json').write_text(json.dumps(S,ensure_ascii=False,indent=2))
