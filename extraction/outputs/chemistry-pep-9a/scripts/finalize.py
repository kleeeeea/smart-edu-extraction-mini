"""Final content corrections from visual comparison and record readback."""
import json,csv,re,shutil,hashlib
from pathlib import Path
R=Path(__file__).resolve().parents[1]
a=json.loads((R/'selection.json').read_text()); b={s['name']:s for s in a}
b['分子探针及其应用']['detail']='分子探针是一类特殊的分子，它们既能与人体组织中的特定分子（靶分子）结合而对其进行标记，又能被检测设备识别定位。追踪靶分子可以获得疾病发生原因的相关信息，从而为精准医疗和药物研究等提供分子层次的科学依据。例如，一种能释放正电子的分子探针在癌症的PET/CT（正电子发射体层成像/计算机体层成像）诊断中发挥了重要作用。'
b['地壳中的元素含量']['detail']='各种元素在地壳中的含量如图3-19所示，其中含量最高的是氧元素，它的质量分数接近50%，其次是硅元素。在地壳中含量较低的碳、氢、氮等元素，对动植物的生命活动有着重要作用。'
b['地壳中的元素含量']['regions']=[[80,55,160,60,290]]
b['吸附净水及其局限']['detail']='如果用具有吸附作用的固体过滤液体，不仅可以滤去其中的难溶性物质，还可以吸附一些溶解的杂质，除去异味。市场上出售的净水器，有些就是利用活性炭来吸附、过滤水中的杂质的（如图4-12）。\n\n经沉降、过滤和吸附等净化处理后，浑浊的水变澄清了，但仍然不是纯水。水中的难溶性杂质被除去后，仍有一些溶解的杂质存在于水中。'
b['水组成及变化探究的实验用品']['detail']='【实验用品】\n\n水电解器、烧杯、直流电源、铁架台（带铁圈和滴定夹）、酒精灯、导线、火柴。\n\n硫酸钠溶液（或氢氧化钠溶液）、木条、蒸馏水。'
b['以化学方程式为工具定量认识反应']['detail']='在例题中，我们通过化学方程式描述高锰酸钾和碳酸钙的分解反应，根据反应物和生成物间的质量比例关系计算相关物质的质量。这是在对化学反应定性认识的基础上，以化学方程式为工具，从定量的角度认识和应用化学反应规律。'
b['以化学方程式为工具定量认识反应']['regions']=[[128,104,570,375,520]]
b['控制二氧化碳含量的低碳措施']['detail']='为应对全球变暖这一重大挑战，实现人类社会可持续发展，国际社会倡导采取低碳行动，控制大气中二氧化碳的含量，防止温室效应进一步增强（如图6-17）。例如：世界各国签署限制二氧化碳排放的国际公约，并严格执行；减少使用化石燃料，更多地利用太阳能、风能等清洁能源；促进节能产品和技术的进一步开发和普及，提高能源的生产效率和使用效率；大力植树造林，严禁乱砍滥伐森林；采用物理、化学等方法，捕集、利用与封存二氧化碳；等等。'
b['化石能源的来源与不可再生性']['detail']='目前，人类利用的能量大多来自化石能源，如煤、石油和天然气等。这些化石能源及其加工后的产品常被用作燃料，因此化石能源也被称为化石燃料。\n\n化石能源是由古代生物的遗骸经一系列复杂变化形成的，是不可再生能源。'
b['石油裂解与煤隔绝空气加强热的产品']['detail']='将石油中相对分子质量较大的分子裂解成相对分子质量较小的分子，就可以再把它们转化为多种产品（如图7-16）。将煤隔绝空气加强热，就能使煤分解成焦炉煤气、粗氨水、焦炭和煤焦油等，利用这些物质可以进一步生产多种有用的产品（如图7-17）。'
b['定比定律']['detail']='普鲁斯特提出假说，认为每一种物质都有固定的组成，不管这种物质是天然的还是人造的，组成该物质的各种元素的质量比都是相同的。该定律被称为定比定律或定组成定律。'
# Include the actual image pages cited by the text, after complete merged sentences.
b['品红扩散实验与物质的微观构成']['image_pages']=[64]
b['元素周期表的排列、周期、族和原子序数']['image_pages']=[198]
# Track figure-only references separately from text selection rectangles.
for s in a:
 valid=[]
 for z in s['regions']:
  if len(z)>3 and z[3:]==[0,0]:s.setdefault('image_pages',[]).append(z[0])
  else:valid.append(z)
 s['regions']=valid
# Standardize conditions above equality without changing reaction content.
b['乙醇燃烧与化学反应放热']['detail']=b['乙醇燃烧与化学反应放热']['detail'].replace('C₂H₅OH + 3O₂ ═（点燃）═ 2CO₂ + 3H₂O',r'$\mathrm{C_2H_5OH+3O_2\xlongequal{点燃}2CO_2+3H_2O}$')
# Recover complete original sentences for explanatory excerpts shortened in an earlier edit.
b['碳纳米管、石墨烯与新形态碳单质']['detail']='一些以新的形态存在的碳单质相继被发现，如碳纳米管。碳纳米管的直径一般为几纳米（符号为nm）到几十纳米，它独特的结构（如图6-5）和性质受到人们的广泛关注。碳纳米管具有尺寸小、机械强度高、导电性好等特点，可应用于材料、催化、信息等诸多领域。\n\n2004年，科学家成功地从石墨中分离出单层的石墨片（即石墨烯，如图6-6），证实它在室温下可以单独稳定存在（过去一直认为这是不可能的）。这是目前世界上人工制得的最薄的材料——厚度仅为0.335 nm。石墨烯优异的导电、导热性和其他奇特性质正激励着科学家不断去探索（如图6-7）。\n\n2010年，我国科学家通过化学方法合成了石墨炔。2017年，中外科学家联合研究团队又合成了T-碳。'
# The conceptual schema in the unit recap adds a concise structure-properties-use statement.
b['同种元素形成不同单质与碳单质结构差异']['regions'].append([141,220,265])
b['同种元素形成不同单质与碳单质结构差异']['detail']+='\n\n物质的性质与结构有关，在很大程度上决定了物质的用途。'
(R/'selection.json').write_text(json.dumps(a,ensure_ascii=False,indent=2))
print('corrected',len(a),'records')
