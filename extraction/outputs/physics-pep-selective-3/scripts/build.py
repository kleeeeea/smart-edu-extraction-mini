"""以人工视觉选区为依据生成分册。公式修订另存 patches.json；不改源 PDF。"""
import csv, json, re, shutil
from pathlib import Path
import fitz
B=Path(__file__).resolve().parents[1]
BOOK='physics-pep-selective-3'
REPORT=json.loads((B/'source_report.json').read_text())
DOC=fitz.open(REPORT['source_pdf'])
records=[]
# 选区以 PDF 点为单位；正文与侧栏分别选取，跨页正文先拼合。
def r(p,y0=55,y1=775,x0=210,x1=530,size=11):return dict(page=p,rect=[x0,y0,x1,y1],min_size=size)
def w(text):return dict(text=text)
def add(ch,sec,name,regions,examples=None):
 records.append(dict(ch=ch,sec=sec,name=name,regions=regions,examples=examples or []))
C=['第一章 分子动理论','第二章 气体、固体和液体','第三章 热力学定律','第四章 原子结构和波粒二象性','第五章 原子核','课题研究']
S={1:['1 分子动理论的基本内容','2 实验：用油膜法估测油酸分子的大小','3 分子运动速率分布规律','4 分子动能和分子势能'],2:['1 温度和温标','2 气体的等温变化','3 气体的等压变化和等容变化','4 固体','5 液体'],3:['1 功、热和内能的改变','2 热力学第一定律','3 能量守恒定律','4 热力学第二定律'],4:['1 普朗克黑体辐射理论','2 光电效应','3 原子的核式结构模型','4 氢原子光谱和玻尔的原子模型','5 粒子的波动性和量子力学的建立'],5:['1 原子核的组成','2 放射性元素的衰变','3 核力与结合能','4 核裂变与核聚变','5 “基本”粒子'],6:['研究样例']}
# 第一章
add(1,0,'热学', [r(6,420,480,240,540)])
add(1,1,'物体是由大量分子组成的',[r(7,445,665),r(8,55,122,55,370),r(7,697,730,210,530,8)])
add(1,1,'扫描隧道显微镜',[r(7,730,775,210,530,8)])
add(1,1,'扩散',[r(8,155,375,55,370)])
add(1,1,'布朗运动及其微观解释',[r(8,375,775,55,370),r(9,55,325),r(9,430,650),r(9,590,720,55,205)])
add(1,1,'分子热运动与温度',[r(9,660,775)])
add(1,1,'分子间的作用力',[r(10,55,775,55,370)])
add(1,1,'分子动理论与统计规律',[r(11,55,342)])
add(1,2,'用油膜法估测油酸分子的大小',[r(12,340,730,55,370),r(13,55,735,55,530),r(14,55,305,55,370),r(12,730,775,55,370,8),r(13,741,768,55,530,8)])
add(1,3,'统计规律',[r(15,190,380,55,370),r(15,403,510,210,530)])
add(1,3,'气体分子运动的特点',[r(15,565,775),r(16,55,222,55,370),r(16,742,775,55,530,8)])
add(1,3,'分子运动速率分布规律',[r(16,265,735,55,530)])
add(1,3,'气体压强的微观解释及豆粒模拟演示',[r(17,98,750,55,530),r(18,55,303,55,370)])
add(1,4,'分子动能和分子热运动的平均动能',[r(19,386,660),r(19,550,660,55,205)])
add(1,4,'分子势能',[r(19,718,775),r(20,159,643,55,530),r(20,742,775,55,530,8)])
add(1,4,'物体的内能及其与机械能的区别',[r(20,683,738,55,370),r(21,55,132),r(21,284,405)])
# 第二章
add(2,1,'热力学系统、状态参量与平衡态',[r(24,466,731,55,370),r(25,55,262)])
add(2,1,'热平衡、热平衡定律与温度',[r(25,310,632)])
add(2,1,'温度计、摄氏温标和热力学温标',[r(26,98,530,55,370),r(26,355,490,389,530)])
add(2,1,'不同温度计的测温原理',[r(26,560,755,55,530,9),r(27,230,415,55,530,9)])
add(2,2,'等温变化与探究气体等温变化的规律',[r(28,322,775,55,530),r(29,55,295,55,530)])
add(2,2,'玻意耳定律',[r(29,485,775),r(29,670,775,55,205)])
add(2,2,'用传感器探究气体等温变化的规律',[r(30,98,295,55,350)])
add(2,3,'气体的等压变化与盖—吕萨克定律',[r(31,190,260,55,370),r(31,280,331),r(31,375,688)])
add(2,3,'气体的等容变化与查理定律',[r(31,735,775),r(32,55,671,55,370),r(32,398,530,389,530)], [r(32,710,775,55,530),r(33,68,388,55,530)])
add(2,3,'理想气体与气体实验定律的适用条件',[r(33,435,775),r(34,55,186,55,370)])
add(2,3,'理想气体的状态方程',[r(34,235,420,55,530,9)])
add(2,3,'气体实验定律的微观解释',[r(34,490,775,55,370)])
add(2,3,'理想模型',[r(35,105,300,55,530,9)])
add(2,4,'晶体、非晶体与各向异性',[r(36,395,605,55,370),r(37,55,680,55,530)])
add(2,4,'单晶体和多晶体',[r(38,55,260,55,370)])
add(2,4,'晶体的微观结构及晶体与非晶体的转化',[r(38,320,775,55,370),r(39,55,180)])
add(2,4,'石墨烯的结构和物理性质',[r(39,267,347,65,400,9),r(39,663,747,65,530,9)])
add(2,5,'液体表面张力及肥皂膜实验',[r(41,328,775,55,530),r(42,55,385,55,370)])
add(2,5,'浸润和不浸润',[r(42,647,738,55,370),r(43,55,327)])
add(2,5,'毛细现象及观察实验',[r(43,365,775,55,530),r(44,55,140,55,370)])
add(2,5,'液晶',[r(44,195,775,55,370),r(45,55,182)])
add(2,5,'液晶显示的基本原理',[r(45,246,775,55,530,9),r(46,65,230,55,370,9)])
# 第三章
add(3,1,'焦耳实验、绝热过程与内能',[r(51,596,716),r(52,55,775,55,370),r(53,55,240)])
add(3,1,'功与内能的改变及绝热膨胀实验',[r(51,300,390,55,370),r(53,275,775,210,530),r(53,643,775,55,210),r(54,55,140,55,370)])
add(3,1,'热与内能的改变',[r(54,190,505,55,370),r(54,355,505,389,530)])
add(3,2,'热力学第一定律',[r(55,350,775),r(55,630,710,55,205)])
add(3,2,'热力学第一定律中功与热量的正负及应用',[r(56,225,370,55,370)], [r(56,415,775,55,530),r(57,55,413,55,530)])
add(3,2,'热的本质与钻孔实验的证据',[r(57,505,760,55,530,9),r(58,65,157,55,530,9)])
add(3,3,'能量的不同形式与转化',[r(59,350,590)])
add(3,3,'能量守恒定律',[r(61,275,680),r(61,555,655,55,205)])
add(3,3,'饮水小鸭的工作原理与永动机不可能制成',[r(62,160,405,55,370),r(62,620,710,55,370)])
add(3,4,'宏观过程的方向性与热力学第二定律的克劳修斯表述',[r(64,345,775,55,370),r(65,162,290)])
add(3,4,'热机与热力学第二定律的开尔文表述',[r(65,460,775),r(66,55,322,55,370),r(66,457,537,55,370)])
add(3,4,'能量耗散与能源的有限性',[r(66,590,738,55,370),r(67,55,304)])
add(3,4,'熵与熵增加原理',[r(67,365,740,55,530,9),r(68,65,550,55,530,9)])
# 第四章
add(4,1,'黑体与黑体辐射',[r(72,456,775,55,370)])
add(4,1,'黑体辐射的实验规律及理论解释',[r(73,98,518),r(74,55,115,55,370)])
add(4,1,'能量子与普朗克常量',[r(74,150,625,55,370),r(74,150,268,389,530)])
add(4,2,'光电效应及实验规律',[r(76,300,775,55,370),r(77,55,775),r(78,55,96,55,370)])
add(4,2,'逸出功与光电效应经典解释中的疑难',[r(78,245,775,55,370)])
add(4,2,'光子与爱因斯坦光电效应方程',[r(79,98,775),r(80,55,96,55,370)])
add(4,2,'遏止电压与入射光频率及光电效应理论的实验检验',[r(80,230,775,55,370)])
add(4,2,'康普顿效应和光子的动量',[r(81,98,775)])
add(4,2,'光的波粒二象性',[r(82,90,355,55,370)])
add(4,3,'阴极射线、电子及电荷量子化',[r(83,300,774),r(84,55,738,55,370),r(85,55,95)])
add(4,3,'原子结构模型与α粒子散射实验',[r(85,295,775),r(86,268,382,55,370),r(86,540,775,55,370),r(87,55,474)])
add(4,3,'原子核的电荷与尺度',[r(87,510,775),r(88,55,149,55,370),r(87,623,775,55,205)])
add(4,4,'光谱、特征谱线与光谱分析',[r(89,401,620),r(90,55,149,55,370)])
add(4,4,'氢原子光谱的实验规律与巴耳末公式',[r(90,195,539,55,370)])
add(4,4,'经典理论解释原子结构的困难',[r(90,585,775,55,370),r(91,55,256)])
add(4,4,'玻尔理论：轨道量子化、定态与频率条件',[r(91,309,775),r(92,55,535,55,370),r(92,450,540,389,530)])
add(4,4,'玻尔理论对氢光谱及原子发光的解释',[r(92,581,775,55,370),r(93,55,222),r(93,610,775),r(94,55,273,55,370),r(92,645,773,389,530)])
add(4,4,'玻尔理论的局限性与电子云',[r(94,329,705,55,370)])
add(4,4,'吸收光谱与光谱分析的应用',[r(95,288,524,55,530,9),r(96,300,775,55,530,9)])
add(4,5,'粒子的波动性与德布罗意波',[r(97,357,649)])
add(4,5,'物质波的实验验证与可观察条件',[r(97,698,748),r(98,55,775,55,370)])
add(4,5,'量子力学与波动力学和矩阵力学',[r(99,90,775),r(100,55,183,55,370)])
add(4,5,'量子力学的应用',[r(100,244,634,55,370),r(101,55,390)])
# 第五章
add(5,0,'核能',[r(105,190,240,230,540)])
add(5,1,'放射性、放射性元素与天然放射现象',[r(106,669,775,55,370)])
add(5,1,'α、β、γ射线的本质和特性',[r(107,98,275),r(107,446,775),r(108,55,160,55,370),r(107,486,599,55,205)])
add(5,1,'威耳逊云室及射线径迹',[r(108,236,505,55,530,9)])
add(5,1,'质子、中子与核子',[r(108,726,775,55,370),r(109,195,334),r(109,466,614),r(110,55,140,55,370)])
add(5,1,'电荷数、质量数、原子核符号与同位素',[r(110,140,616,55,370),r(110,198,275,389,530)])
add(5,2,'原子核的α衰变、β衰变及伴随γ辐射',[r(113,446,775),r(114,65,177,55,370),r(114,293,704,55,370),r(115,165,569),r(114,735,775,55,370,8)])
add(5,2,'半衰期及其统计意义',[r(115,627,775),r(116,55,493,55,370)])
add(5,2,'核反应与原子核的人工转变',[r(116,545,775,55,370),r(117,55,96)])
add(5,2,'放射性同位素的应用：测厚、治疗、培优和保鲜',[r(117,162,775),r(117,195,305,55,205)])
add(5,2,'示踪原子及应用',[r(118,55,480,55,370)])
add(5,2,'辐射与安全',[r(118,539,775,55,370)])
add(5,2,'碳14测年技术',[r(119,125,460,55,530,9)])
add(5,3,'核力与四种基本相互作用',[r(120,344,775,55,370),r(121,55,324)])
add(5,3,'结合能与比结合能',[r(121,374,530),r(122,55,196,55,370)])
add(5,3,'质能关系、质量亏损及结合能计算',[r(122,267,775,55,530),r(123,65,456,55,530)])
add(5,4,'核裂变、链式反应与临界质量',[r(124,423,775,55,370),r(125,55,775,55,530),r(126,55,119,55,370)])
add(5,4,'原子弹与核裂变能的释放',[r(126,188,470,55,530,9)])
add(5,4,'反应堆与核电站',[r(126,515,738,55,370),r(127,55,775,55,530),r(128,55,275,55,370),r(126,674,775,389,530),r(127,55,181,55,205)])
add(5,4,'核聚变、热核反应与太阳能',[r(128,329,474,55,370),r(128,643,775,55,370),r(129,55,508)])
add(5,4,'可控核聚变的磁约束与惯性约束',[r(129,508,775),r(130,294,480,55,370)])
add(5,5,'粒子及其内部结构',[r(131,303,540)])
add(5,5,'反粒子',[r(133,55,197)])
add(5,5,'强子、轻子、规范玻色子和希格斯玻色子',[r(133,245,633)])
add(5,5,'夸克与粒子物理标准模型',[r(133,716,764,55,530,9),r(134,265,485,55,530,9)])
add(6,1,'燃气灶火力对烧水效率的影响',[r(137,298,738,55,530),r(138,55,734,55,530),r(139,55,775,55,530),r(137,743,775,210,530,8),r(138,743,775,55,530,8)])

# 按选区内原生文本行抽取；不把页面上的图注与图中标签混入正文。
def extract(spec):
 if 'text' in spec:return spec['text']
 p=DOC[spec['page']-1]; x0,y0,x1,y1=spec['rect']; lines=[];small=[]
 for block in p.get_text('dict')['blocks']:
  for line in block.get('lines',[]):
   bx0,by0,bx1,by1=line['bbox']
   if not (y0<=by0<y1 and bx0>=x0-2 and bx0<x1-1):continue
   spans=line['spans']
   if any(s['size']>=20 for s in spans):continue
   txt=''.join(s['text'] for s in spans).strip()
   if not txt or '仅供个人学习' in txt:continue
   target=lines if any(s['size']>=spec['min_size'] for s in spans) else small
   target.append(dict(y=spans[0]['origin'][1],x=bx0,text=txt,spans=spans))
 # 保留正文指数/下标候选，表格和图中标签由原图承担；二维公式人工修订。
 for z in small:
  if max(s['size'] for s in z['spans'])>8.5:continue
  choices=[a for a in lines if abs(a['y']-z['y'])<9 and any(abs(s['bbox'][2]-z['x'])<12 or abs(s['bbox'][0]-z['x'])<12 for s in a['spans'])]
  if choices:
   near=min(choices,key=lambda a:abs(a['y']-z['y']))
   near['spans']+=z['spans']
 groups=[]
 for z in sorted(lines,key=lambda a:a['y']):
  if groups and abs(z['y']-groups[-1]['y'])<3:
   groups[-1]['spans']+=z['spans'];groups[-1]['x']=min(groups[-1]['x'],z['x'])
  else:groups.append(z)
 for z in groups:
  z['text']=''.join(t['text'] for t in sorted(z['spans'],key=lambda t:t['bbox'][0])).strip()
 out=[];last=None
 for z in groups:
  t=re.sub('[①②③④⑤⑥⑦⑧⑨]','',z['text'])
  if not t:continue
  if last and z['y']-last['y']<27 and last['text'][-1:]not in '。！？：；':out[-1]+=t
  else:out.append(t)
  last=z
 return '\n\n'.join(out).strip()

def join_specs(specs):
 parts=[]
 for spec in specs:
  t=extract(spec)
  if not t:continue
  if parts and parts[-1][-1:] not in '。！？：；）〕】' and t[:1] not in '（①②③':parts[-1]+=t
  else:parts.append(t)
 return '\n\n'.join(parts)
def pages_of(specs):return sorted({s['page'] for s in specs if 'page'in s})
def page_label(pages):
 groups=[]
 for n in pages:
  if groups and n==groups[-1][-1]+1:groups[-1].append(n)
  else:groups.append([n])
 return ';'.join(f'P{g[0]}' if len(g)==1 else f'P{g[0]}-P{g[-1]}' for g in groups)
def build():
 patches=json.loads((B/'patches.json').read_text()) if (B/'patches.json').exists() else {}
 rows=[];sources=[]
 final_records=records.copy()
 for extra in json.loads((B/'extra_records.json').read_text()) if (B/'extra_records.json').exists() else []:
  index=next(i for i,z in enumerate(final_records)if z['name']==extra['after'])
  final_records.insert(index+1,extra['record'])
 for i,z in enumerate(final_records,1):
  kid=f'RJ-PHYSICS-SEL3-{i:03d}'
  detail=join_specs(z['regions']);example=join_specs(z['examples'])
  patch=patches.get(z['name'],{})
  for field in ['detail','example']:
   val=detail if field=='detail' else example
   if field in patch:val=patch[field]
   for a,b in patch.get(field+'_replace',[]):
    if a not in val:raise ValueError((z['name'],field,'missing patch target',a))
    val=val.replace(a,b)
   specs=z['regions'] if field=='detail' else z['examples']
   if val:
    val=val.strip()+'\n\n'+'\n\n'.join(f'![page-{n:03d}](images/{BOOK}/page-{n:03d}.png)'for n in pages_of(specs))
   if field=='detail':detail=val
   else:example=val
  section=S[z['ch']][z['sec']-1] if z['sec'] else '章引言'
  rows.append(dict(knowledge_point_id=kid,chapter=C[z['ch']-1],subchapter=section,section=section,knowledge_point=z['name'],detail=detail,example=example,pdf_page=page_label(pages_of(z['regions']+z['examples']))))
  sources.append(dict(knowledge_point_id=kid,source_pdf_sha256=REPORT['sha256'],detail_regions=z['regions'],example_regions=z['examples'],editorial_patch=patch,candidate_selection_status='文字层定位候选；最终文字以逐页视觉修订为准',verified_source_pages=pages_of(z['regions']+z['examples']),visual_verification_regions=[dict(page=n,rect=[0,0,595.275,841.890])for n in pages_of(z['regions']+z['examples'])]))
 fields=['knowledge_point_id','chapter','subchapter','section','knowledge_point','detail','example','pdf_page']
 with (B/'knowledge_points.csv').open('w',encoding='utf-8-sig',newline='')as f:
  writer=csv.DictWriter(f,fieldnames=fields);writer.writeheader();writer.writerows(rows)
 with (B/'source_records.jsonl').open('w')as f:
  for s in sources:f.write(json.dumps(s,ensure_ascii=False)+'\n')
 (B/'selection.json').write_text(json.dumps(final_records,ensure_ascii=False,indent=2))
 md=['# 人教版高中物理 选择性必修第三册\n']
 for row in rows:
  md.extend([f"## {row['knowledge_point_id']} {row['knowledge_point']}\n",f"{row['chapter']} / {row['section']} · {row['pdf_page']}\n",row['detail']+'\n'])
  if row['example']:md.extend(['### 补充原例与原解\n',row['example']+'\n'])
 (B/'knowledge_points.md').write_text('\n'.join(md))
 (B/'review/transcription.txt').write_text('\n\n'.join(f"{r['knowledge_point_id']} {r['knowledge_point']}\n{r['detail']}\nEXAMPLE\n{r['example']}"for r in rows))
 print(f'{len(rows)} records')
if __name__=='__main__':build()
