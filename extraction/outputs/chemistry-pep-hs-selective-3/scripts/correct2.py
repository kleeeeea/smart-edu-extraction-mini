from pathlib import Path
import json
R=Path(__file__).resolve().parents[1];S=json.loads((R/'selection.json').read_text());cs=[json.loads(x)['detail'] for x in (R/'transcription_candidates.jsonl').read_text().splitlines()]
def get(i):return S[i-1].get('detail',cs[i-1])
def put(i,t):S[i-1]['detail']=t
def add(i,t):put(i,get(i)+'\n\n'+t)
def rep(i,a,b):assert a in get(i),(i,a);put(i,get(i).replace(a,b))
add(4,'|有机化合物类别|官能团|代表物|\n|---|---|---|\n|烷烃|—|甲烷 CH₄|\n|烯烃|碳碳双键 >C=C<|乙烯 CH₂=CH₂|\n|炔烃|碳碳三键 —C≡C—|乙炔 CH≡CH|\n|芳香烃|—|苯（原结构式见图）|\n|卤代烃|碳卤键 >C—X，卤素原子—X|溴乙烷 CH₃CH₂Br|\n|醇|羟基 —OH|乙醇 CH₃CH₂OH|\n|酚|羟基 —OH|苯酚（原结构式见图）|\n|醚|醚键 —C—O—C—|乙醚 CH₃CH₂OCH₂CH₃|\n|醛|醛基 —CHO|乙醛 CH₃CHO|\n|酮|酮羰基（羰基）>C=O|丙酮 CH₃COCH₃|\n|羧酸|羧基 —COOH|乙酸 CH₃COOH|\n|酯|酯基 —C(=O)—O—R|乙酸乙酯 CH₃COOCH₂CH₃|\n|胺|氨基 —NH₂|甲胺 CH₃NH₂|\n|酰胺|酰胺基 —CONH₂|乙酰胺 CH₃CONH₂|')
add(6,'2C₂H₅OH＋2Na → 2C₂H₅ONa＋H₂↑。\nC₂H₅OH＋HBr —浓氢溴酸、加热→ C₂H₅Br＋H₂O。')
add(31,'|性质|顺-2-丁烯|反-2-丁烯|\n|---|---|---|\n|熔点/℃|−138.9|−105.5|\n|沸点/℃|3.7|0.9|\n|密度/(g·cm⁻³)|0.621|0.604|')
add(35,'CH≡CH＋Br₂ → CHBr=CHBr（1,2-二溴乙烯）\nCHBr=CHBr＋Br₂ → CHBr₂CHBr₂（1,1,2,2-四溴乙烷）\nCH≡CH＋H₂ —催化剂、加热→ CH₂=CH₂\nCH≡CH＋HCl —催化剂、加热→ CH₂=CHCl\nCH≡CH＋H₂O —催化剂、加热→ CH₃CHO\nnCH≡CH —催化剂→ [—CH=CH—]ₙ。')
add(57,'C₂H₅OH —浓硫酸、170 ℃→ CH₂=CH₂↑＋H₂O\n2C₂H₅OH —浓硫酸、140 ℃→ C₂H₅OC₂H₅＋H₂O。')
rep(61,'实验内容实验现象','');rep(61,'稀盐酸由于','稀盐酸。\n\n由于')
add(61,'C₆H₅OH＋NaOH → C₆H₅ONa＋H₂O\nC₆H₅ONa＋HCl → C₆H₅OH＋NaCl\nC₆H₅ONa＋CO₂＋H₂O → C₆H₅OH＋NaHCO₃。')
add(67,'CH₃CHO＋2[Ag(NH₃)₂]OH —加热→ CH₃COONH₄＋2Ag↓＋3NH₃＋H₂O。')
add(68,'CH₃CHO＋2Cu(OH)₂＋NaOH —加热→ CH₃COONa＋Cu₂O↓＋3H₂O\n2CH₃CHO＋O₂ —催化剂、加热→ 2CH₃COOH。')
add(90,'1. CH₂=CH₂＋H₂O —催化剂、加热、加压→ CH₃CH₂OH\n2. CH₂=CH₂＋Cl₂ → CH₂ClCH₂Cl\n3. CH₂ClCH₂Cl＋2NaOH —水、加热→ HOCH₂CH₂OH＋2NaCl\n4. HOCH₂CH₂OH＋2O₂ —催化剂、加热→ HOOC—COOH＋2H₂O\n5. HOOC—COOH＋2CH₃CH₂OH ⇌（催化剂、加热）C₂H₅OOC—COOC₂H₅＋2H₂O。\n\n当通过以上方法得到了几条不同的合成路线后，还需要综合多方面因素进行选择，合理规划方案。如合成步骤较少，副反应少，反应产率高；原料、溶剂和催化剂尽可能价廉易得、低毒；反应条件温和，操作简便，产物易于分离提纯；污染排放少；等等。在进行有机合成时，要贯彻“绿色化学”理念，选择最佳合成路线，以较低的经济成本和环境代价得到目标产物。')
S[92]['name']='1-己烯与1-溴丁烷的官能团检验实验'
rep(93,'观察现象（2）','观察现象。\n（2）');rep(93,'观察现象向试管里','观察现象。\n\n向试管里')
add(97,'C₆H₁₂O₆＋6O₂ —酶→ 6CO₂＋6H₂O。')
rep(131,'（2）用以上实验中的方法制备Cu(OH)2','（2）在试管中加入2 mL 10% NaOH溶液，滴入5滴5% CuSO₄溶液，振荡，制备Cu(OH)₂')
rep(132,'子材料工业体系已经建立。除了','除了')
rep(133,'104以上','10⁴以上')
put(146,get(146).replace('聚对苯二甲酰对苯二胺纤维具有强度高、密度低，以及耐酸、耐碱、耐高温、耐磨等优异特性的芳香族聚酰胺纤维——聚对苯二甲酰对苯二胺纤维，','聚对苯二甲酰对苯二胺纤维具有强度高、密度低，并且耐酸、耐碱、耐高温、耐磨等优异特性，'))
# Source regions for added footnotes and diagrams; image pages already attached.
for i,rr in {14:[[19,548,724],[20,58,611]],19:[[24,731,755]],90:[[94,281,724]],94:[[105,738,760]],96:[[107,730,760]],126:[[127,734,770]],139:[[142,505,755]],151:[[152,546,738]]}.items():S[i-1]['regions']+=rr
# Snapshot the draft identity before final ordering; then use first source position.
(R/'draft_order.json').write_text(json.dumps([{'draft_position':i,'name':s['name']} for i,s in enumerate(S,1)],ensure_ascii=False,indent=2))
# Move the chlorinated ethane sidebar into its original P60 position within the same section.
x=S.pop(51);S.insert(49,x)
(R/'selection.json').write_text(json.dumps(S,ensure_ascii=False,indent=2))
