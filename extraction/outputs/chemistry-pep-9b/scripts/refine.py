import json,re
from pathlib import Path
R=Path(__file__).resolve().parents[1]
S=json.loads((R/'selection.json').read_text());before=json.loads(json.dumps(S))
# Only reuse the region reader, without rebuilding outputs.
ns={'__file__':str(R/'scripts/build.py')};exec((R/'scripts/build.py').read_text().split('selection=json.loads')[0],ns)
def candidate(s):
 t=''
 for a in s['regions']:
  part=ns['region'](a)
  if t and t[-1:] in '。！？；：':t+='\n\n'
  t+=part
 return t
for s in S:
 if 'detail' not in s:
  s['detail']=candidate(s)
  for a,b in s.get('replace',[]):s['detail']=s['detail'].replace(a,b)
 s.pop('replace',None)
def get(n):return next(s for s in S if s['name']==n)
def replace(n,a,b):
 s=get(n);assert a in s['detail'],(n,a);s['detail']=s['detail'].replace(a,b)
s=get('常见金属的物理性质与用途');s['regions'][0]=[7,518,665,185,480];s['detail']=candidate(s)
s=get('选择材料时需要考虑的因素');s['regions']=[[9,330,414,185,480]];s['detail']=candidate(s)
replace('钛和钛合金的性能与用途','g/cm3','g/cm³')
s=get('金属与稀盐酸、稀硫酸的反应及探究');s['regions'][2]=[17,57,118,185,480];s['detail']=candidate(s)
# The preceding region ends before the continuation line; restore the complete explicit statement.
s['detail']=s['detail'].replace('分析镁、锌、铁与','')
replace('溶液的应用','医疗上常用的葡①和一些眼药水等，都是根据萄糖溶液、生理盐水人的生理需求配制的溶液。','医疗上常用的葡萄糖溶液、生理盐水和一些眼药水等，都是根据人的生理需求配制的溶液。')
get('溶液的应用')['detail']+='\n\n100 mL生理盐水中含0.9 g医用氯化钠。'
# Remove overlap in the solvent introduction.
replace('溶液的形成与特征','水是一种最常用的溶剂，能溶解很多种物质。','')
s=get('气体的溶解度');s['detail']='因为称量气体的质量比较困难，所以气体的溶解度常用体积来表示。通常用的气体的溶解度，是指该气体的压强为101 kPa和一定温度时，在1体积水里溶解达到饱和状态时的气体体积。例如，氮气的压强为101 kPa、温度为0 ℃时，1体积水里最多能溶解0.024体积的氮气，则在0 ℃时，氮气的溶解度为0.024。\n\n非标准状况时的气体体积要换算成标准状况时的体积。'
replace('配制及稀释一定溶质质量分数的氯化钠溶液','（密度为3），配制50 g 质量分数为3% 的氯化钠溶液。1.04 g/cm','（密度为1.04 g/cm³），配制50 g质量分数为3%的氯化钠溶液。')
replace('浓硫酸的稀释与使用注意事项','盐酸、硫酸等酸具有非常广泛的用途（如','')
get('浓硫酸的腐蚀性与脱水作用')['detail']+='\n\n严格地说，浓硫酸能将这些物质中的氢、氧按水的组成比脱去，这种作用通常叫作脱水作用。'
get('浓硫酸的稀释与使用注意事项')['detail']+='\n\n实验10-6由教师演示。'
replace('酸溶液的导电性与共同离子','H+','H⁺')
replace('复合肥料与合理施用化肥','成为农作物增产的有力措施','成为农作物增产的有力措施（如图10-20），解决了部分地区粮食短缺的问题。')
replace('复合肥料与合理施用化肥','NH4H2PO4','NH₄H₂PO₄');replace('复合肥料与合理施用化肥','KNO3','KNO₃')
replace('常见酸、碱的化学性质实验','【问题与交流】','')
replace('区分棉纤维、羊毛纤维和涤纶的实验','【结论与思考】','')
get('六类营养物质')['detail']+='\n\n无机盐也被称为矿物质。'
get('高分子材料、天然材料和合成材料')['detail']+='\n\n高分子的相对分子质量比较大（通常在1万以上），淀粉、蛋白质、橡胶等高分子的相对分子质量可达几十万，甚至百万。'
# Explicit source table inputs, without filling blank outcome columns.
get('配制不同质量分数的氯化钠溶液实验')['detail']+='\n\n|溶质质量/g|溶剂（水）质量/g|固体能否全部溶解|溶质的质量分数|\n|---|---|---|---|\n|10|90| | |\n|20|80| | |'
get('溶液的酸碱度与pH的测定')['detail']=get('溶液的酸碱度与pH的测定')['detail'].replace('下列溶液','白醋、食盐水、肥皂水')
get('盐酸和硫酸的性质观察')['detail']+='\n\n常用浓盐酸（质量分数为37%～38%）的密度为1.19 g/cm³；常用浓硫酸（质量分数为98%）的密度为1.84 g/cm³。'
get('酸碱度在健康和生产中的意义')['detail']+='\n\n人体内的一些液体和排泄物的正常pH范围：\n\n|液体|正常pH范围|\n|---|---|\n|血浆|7.35～7.45|\n|唾液|6.6～7.1|\n|胃液|0.9～1.5|\n|乳汁|6.8～7.3|\n|肝胆汁|7.1～8.5|\n|胰液|7.8～8.4|\n|尿液|4.4～8.0|'
# Improve readability without changing source semantics or filling any blank.
for s in S:
 t=s['detail'].replace('①','').replace('②','')
 t=t.replace('NaCl、NH4NO3、NaOH','NaCl、NH₄NO₃、NaOH')
 t=t.replace('你还需要的实验用品：。','你还需要的实验用品：________。')
 t=re.sub(r'(?<=[。；])(?=[（(][1-9一二三四五六七八九][）)])','\n\n',t)
 t=re.sub(r'(?<=[。；])(?=[1-6]\. )','\n\n',t)
 t=t.replace('【实验步骤】','\n\n【实验步骤】\n\n').replace('【实验】','\n\n【实验】\n\n')
 s['detail']=re.sub(r'\n{3,}','\n\n',t).strip()
# Move the same-page sidebar back to its actual textbook position.
x=get('植物色素作为酸碱指示剂');S.remove(x);S.insert(S.index(get('酸度计')),x)
changes=[]
for old in before:
 new=next(s for s in S if s['name']==old['name'])
 if old!=new:changes.append({'action':'visual_transcription_refinement','reason':'读回逐条校正文字层串栏、上标、脚注、边界、表格条件与顺序','before':old,'after':new})
(R/'refinement_log.json').write_text(json.dumps(changes,ensure_ascii=False,indent=2))
(R/'selection.json').write_text(json.dumps(S,ensure_ascii=False,indent=2))
print('refined',len(S))
