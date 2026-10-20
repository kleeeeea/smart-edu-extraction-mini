"""Build this book from visually selected source regions and explicit corrections.

Run with /Users/l/miniconda3/envs/base124/bin/python. No OCR is treated as proof.
The selection and corrections are deliberately book-specific and reviewable.
"""
import csv
import json
import re
from pathlib import Path
import fitz

ROOT = Path(__file__).resolve().parents[1]
BOOK = 'physics-pep-selective-1'
FIELDS = ['knowledge_point_id', 'chapter', 'subchapter', 'section', 'knowledge_point', 'detail', 'example', 'pdf_page']
DOC = fitz.open(json.loads((ROOT / 'source_report.json').read_text())['source_pdf'])
CHAPTERS = ['第一章 动量守恒定律', '第二章 机械振动', '第三章 机械波', '第四章 光']
SECTIONS = [
 ['动量', '动量定理', '动量守恒定律', '实验：验证动量守恒定律', '弹性碰撞和非弹性碰撞', '反冲现象 火箭'],
 ['简谐运动', '简谐运动的描述', '简谐运动的回复力和能量', '单摆', '实验：用单摆测量重力加速度', '受迫振动 共振'],
 ['波的形成', '波的描述', '波的反射、折射和衍射', '波的干涉', '多普勒效应'],
 ['光的折射', '全反射', '光的干涉', '实验：用双缝干涉测量光的波长', '光的衍射', '光的偏振 激光'],
]

def reg(p, y0=55, y1=782, x0=55, x1=545):
    return [p, x0, y0, x1, y1]

def main(p, y0=55, y1=782):
    return reg(p, y0, y1, 215 if p % 2 else 62, 540 if p % 2 else 385)

RECORDS = []
def add(c, s, name, regions, examples=None, notes='正文；图示与条件逐页视觉核对'):
    RECORDS.append(dict(c=c, s=s, name=name, detail_regions=regions, example_regions=examples or [], notes=notes))

# Chapter 1. Cross-page derivations are kept in a single record/field.
add(1,1,'寻求碰撞中的不变量', [reg(7,240,705),main(8,55,782),reg(8,55,165,395,540),main(9,55,177)], notes='问题实验、演示、小车实验及数据分析作为概念建立的核心情境；历史引语不收录')
add(1,1,'动量及其矢量性', [main(9,202,435),reg(10,55,195,55,205)], [reg(9,450,747),reg(10,55,238,220,540)])
add(1,1,'体验物体动量的改变', [reg(10,275,442)], notes='做一做；仅保留教材操作与感受提示，不补观察结果')
add(1,2,'动量定理与冲量', [main(11,351,782),main(12,55,487),reg(11,560,670,55,205),reg(12,223,282,395,540)])
add(1,2,'动量定理的应用', [main(12,500,782),main(13,55,140)], [reg(13,180,747),reg(14,55,155)])
add(1,2,'动量定理与动能定理的比较', [reg(14,380,551,67,533)], notes='科学漫步中的有效物理比较；历史争论与评价排除')
add(1,2,'汽车碰撞试验', [reg(15,110,208),reg(15,471,550)], notes='STSE；保留碰撞过程、传感器测量及影响因素；历史新闻与评价排除')
add(1,3,'相互作用的两个物体的动量改变', [main(17,446,782),main(18,55,255)])
add(1,3,'系统、内力和外力', [main(18,277,470)])
add(1,3,'动量守恒定律及其应用条件', [main(18,475,537)], [reg(19,55,747),reg(20,55,645)], notes='保留列车结合和火箭炸裂两种不同条件的完整原例原解；参考系和近似条件随例题保留')
add(1,3,'动量守恒定律的普适性', [main(20,682,782),main(21,55,270)])
add(1,4,'验证动量守恒定律的实验思路与数据分析', [main(22,213,782),reg(23,90,128),main(23,180,345)], notes='实验；未给实测结果，不补结论；质量、速度测量和检验式保留')
add(1,4,'气垫导轨上滑块碰撞的动量守恒实验', [reg(23,381,747),reg(24,55,395)], notes='实验参考案例1；弹性分离、粘连、弹簧分离三种方案均保留')
add(1,4,'斜槽末端小球碰撞的动量守恒实验', [reg(24,440,747),reg(25,55,277)], notes='实验参考案例2；相同下落高度下用水平距离之比代替速度之比；不补教材提问答案')
add(1,5,'弹性碰撞与非弹性碰撞', [reg(26,421,782),main(27,55,161)], [reg(27,180,508)], notes='保留动能变化实验；等质量粘连原例作为补充原例')
add(1,5,'正碰及弹性碰撞的实例分析', [main(27,540,782),main(28),main(29,55,80),reg(28,285,415,395,540)], notes='保留静止靶球、三种质量关系及特例检验方法；条件比较不去重')
add(1,6,'反冲现象', [main(30,347,690),reg(31,55,245)], notes='反冲定义、应用及做一做；不补气球未明示的观察结论')
add(1,6,'火箭的喷气反冲模型', [main(31,260,441),main(31,675,782),main(32,55,270)], notes='喷气前火箭为参考系，极短时间喷气模型与推导；未解宇航员问题不收录')
add(1,6,'多级火箭', [reg(32,330,604)], notes='科学漫步；保留质量比、分级工作和级数限制；技术发展评价排除')

# Chapter 2.
add(2,1,'机械振动、平衡位置与弹簧振子', [reg(37,275,391),main(37,410,711),reg(37,655,712,55,205)])
add(2,1,'弹簧振子的位移—时间图像', [main(38,62,280),main(38,385,670),reg(39,65,392)], notes='核心记录方法及数码相机绘制方法保留；图像与坐标条件保留')
add(2,1,'简谐运动', [main(39,419,508),main(39,615,782),main(40,55,356)])
add(2,2,'简谐运动的表达式与振幅', [main(41,305,655)])
add(2,2,'全振动、周期、频率与圆频率', [main(41,683,782),main(42,55,560)], notes='全振动跨页段落合并；周期频率及圆频率公式保留')
add(2,2,'测量振动周期与周期和振幅的关系', [reg(42,580,755),main(43,55,125)], notes='做一做及明示实验结论；多次全振动计时减小误差')
add(2,2,'相位、初相位与相位差', [main(43,145,415),reg(43,440,782),main(44,55,320)], [reg(44,345,747),reg(45,55,365)], notes='演示及跨页步调比较是核心；补充原例保留路程与位移的不同')
add(2,2,'用计算机呈现声音的振动图像', [reg(45,395,782),reg(46,55,218)], notes='做一做；保留录音、显示波形及周期比较方法；操作任务句排除')
add(2,2,'乐音、音阶与频率比', [reg(46,255,755)], notes='科学漫步；保留频率表、和弦频率比与音程适用条件')
add(2,3,'回复力与简谐运动的动力学条件', [main(48,305,782),main(49,55,255)])
add(2,3,'简谐运动的能量', [reg(48,535,711,395,540),main(49,272,365),reg(49,395,645),main(49,675,782),main(50,55,220)], notes='表格原有空格保留，不代填；能量变化及守恒条件完整保留')
add(2,4,'单摆模型及其理想化条件', [main(51,310,421),reg(51,310,482,55,205)])
add(2,4,'单摆的回复力与小摆角条件', [main(51,530,782),main(52,55,391),reg(52,97,157,395,540)])
add(2,4,'观察单摆运动的墨汁图样', [reg(52,424,519)], notes='做一做；保留器材与匀速拖板步骤，不补未给出的图样结论')
add(2,4,'单摆周期的影响因素及周期公式', [reg(53,65,367),reg(53,400,565),main(53,604,745)], notes='演示、定量探究及公式均保留；人名历史评价与肖像说明排除')
add(2,4,'振荡器与计时', [reg(54,310,427)], notes='科学漫步；保留机械振荡器、晶体振荡器和原子跃迁频率的计时原理，历史年代评价排除')
add(2,5,'用单摆测量重力加速度', [main(56,256,782),main(57,386,782),main(58,55,172)], notes='完整实验思路、装置、摆长和周期测量、数据处理；悬挂方式问题不代答')
add(2,6,'固有振动与固有频率', [main(59,310,418)])
add(2,6,'阻尼振动与振动中的能量损失', [main(59,434,705)])
add(2,6,'受迫振动及其频率', [main(59,714,782),reg(60,55,487)], notes='定义、驱动力、实验装置与稳定后的频率结论；保留稳态条件')
add(2,6,'共振现象及其应用', [reg(60,500,755),main(61,55,480),reg(61,288,350,55,205)])
add(2,6,'调谐质量阻尼器的振动控制', [reg(62,215,311)], notes='科学漫步；保留装置组成与抵消驱动力原理；灾难故事及技术评价排除')

# Chapter 3.
add(3,1,'波动与绳波的形成', [main(67,400,711),main(68,55,505),reg(68,540,747)], notes='演示与质点依次振动过程为核心，保留团体操类比；历史引语排除')
add(3,1,'横波、波峰与波谷', [main(69,62,222)])
add(3,1,'纵波、疏部、密部及声波', [reg(69,255,782),main(70,55,255)], notes='弹簧演示及声音传播的物理解释保留，疏密定义跨页合并')
add(3,1,'机械波、介质与能量和信息的传递', [main(70,272,642),reg(70,670,757)])
add(3,2,'波的图像与简谐波', [main(72,435,782),main(73,55,170),reg(73,80,161,55,205)], notes='保留波形图和振动图像对比及正弦波条件')
add(3,2,'波长、频率和波速', [reg(68,180,505,395,540),main(73,188,782),reg(73,510,720,55,205)], [reg(74,185,747),reg(75,55,142)], notes='声速表含0℃条件；原例同时保留左右传播两种解法与T>0.5s条件')
add(3,3,'波的反射', [reg(76,322,690)], notes='水波反射演示、观察及规律')
add(3,3,'波的折射', [main(76,710,782),main(77,55,172)])
add(3,3,'波的衍射及明显衍射的条件', [reg(77,188,782),reg(78,55,205),main(78,225,440)], notes='两种控制变量实验、7/10、5/10、3/10波长对比及跨页句子保留')
add(3,4,'波的叠加', [reg(79,350,782),main(80,55,83)], notes='长绳演示及位移矢量和；波的独立传播与侧栏条件')
add(3,4,'波的干涉及干涉条件', [reg(80,104,782),main(81),main(82,55,172)], notes='水波实验、增强减弱分析及三项条件；跨页总定义合并')
add(3,4,'声音的干涉实验', [reg(82,190,371)], notes='做一做；相同扬声器与同一信号源条件，不补位置分布答案')
add(3,4,'主动降噪技术', [reg(82,395,755)], notes='STSE；相同频率、相反相位及反馈麦克风机制')
add(3,5,'多普勒效应', [main(84,310,418),reg(84,425,782),reg(85,55,505)], notes='蜂鸣器演示、模拟实验和频率变化解释；人数类比不误作介质质点移动')
add(3,5,'多普勒效应的应用', [main(85,705,782),main(86,55,371)])

# Chapter 4.
add(4,0,'几何光学与物理光学', [main(89,382,502)], notes='章引言有效分类；保留章级位置，不提前归入第一节')
add(4,1,'光的反射与折射、入射角与折射角', [main(90,400,711)], notes='物理现象和角度定义；问题与纯历史引语不收录')
add(4,1,'折射定律与光路可逆', [main(91,55,410),reg(91,720,770,215,540)], notes='原文从折射定律定义开始；比例常数和光路可逆保留')
add(4,1,'折射率及其与光速的关系', [main(91,440,703),main(92,55,433),reg(91,477,600,55,205)], [reg(93,210,755),reg(94,55,164)], notes='表格保留λ=589.3nm、20℃；储油桶原例及原解跨页合并')
add(4,1,'测量玻璃的折射率', [reg(92,455,782),reg(93,55,190)], notes='保留四枚大头针、描边、光路与角度测量完整步骤；不补误差提问答案')
add(4,2,'光疏介质与光密介质', [main(95,280,515)])
add(4,2,'全反射、临界角及其条件', [reg(95,535,782),main(96,55,230),reg(96,255,465),main(96,493,755)], [reg(97,55,417)], notes='半圆玻璃砖演示、明示入射角等于或大于临界角条件；潜水员圆锥原例保留')
add(4,2,'全反射棱镜', [reg(97,441,782)])
add(4,2,'光导纤维及其应用', [reg(98,62,782)], notes='演示、全反射、芯套折射率、传像与通信；脚注中电子内窥镜对比有效信息保留')
add(4,2,'水流导光实验', [reg(99,240,395)], notes='做一做；保留器材与步骤，不补实验结果')
add(4,3,'光的双缝干涉与明暗条纹', [reg(100,391,782),main(101,55,725),reg(101,630,725,55,205),main(102,55,140)], notes='实验及必要明暗路程差推理保留；纯历史年代排除')
add(4,3,'双缝干涉条纹间距与光的波长', [main(102,166,782),main(103,55,84),main(103,225,345),reg(102,572,633,395,545)], notes='完整几何推导、d远小于l、小角度近似及不同色光的原文比较')
add(4,3,'薄膜干涉及其应用', [reg(103,373,782),main(104,55,320)], notes='肥皂膜实验及两反射光解释跨页完整合并')
add(4,3,'光的波粒二象性', [reg(104,598,697)], notes='科学漫步末段的有效结论；历史学说发展评价排除')
add(4,4,'用双缝干涉测量光的波长', [reg(106,264,782),reg(107,55,642)], notes='完整思路、器材、测量头、n条纹跨度/(n-1)、调节步骤及数据分析；不补练习测量值')
add(4,4,'用光传感器做双缝干涉实验', [reg(107,665,782),reg(108,55,334)], notes='拓展学习；传感器、计算机及自上而下光路完整保留')
add(4,5,'光的衍射及光沿直线传播的条件', [reg(109,335,782),main(110,55,334)], notes='单缝宽度对比、白光、图示和直线传播近似条件保留')
add(4,5,'衍射光栅', [reg(110,356,782)])
add(4,5,'泊松亮斑', [reg(111,178,329)], notes='科学漫步；保留圆盘阴影中心亮斑的条件与名称，历史争论排除')
add(4,5,'X射线晶体衍射与结构探测', [reg(111,400,455),reg(112,144,193)], notes='科学漫步；晶格尺度与衍射强度位置所含结构信息；历史获奖评价排除')
add(4,6,'偏振现象与横波的偏振方向', [reg(113,310,782)], notes='保留狭缝方向实验与纵波的必要对比')
add(4,6,'光的偏振、自然光与偏振光', [reg(114,62,782),main(115,55,440),reg(115,185,270,55,205)], notes='两偏振片演示、旋转、透振方向及边栏；脚注电场方向保留')
add(4,6,'偏振现象的应用与观察', [reg(115,460,782),reg(116,55,222)])
add(4,6,'激光的特点及其应用', [main(116,233,782),main(117,55,602)], notes='普通光源与激光相干性对比、平行度与测距、高亮度与加工医学等；历史评价排除')
add(4,6,'立体电影与偏振光', [reg(117,625,782),reg(118,55,466)], notes='科学漫步；双眼视差、正交偏振片、银幕反射及左右眼图像完整保留')
add(4,6,'单摆周期与重力加速度定量关系的实验研究', [main(121,492,782),main(122,55,575),main(123,55,782),reg(124,55,510)], notes='实际位置为课题研究，按就近归属第四章第6节；保留完整已讲解实验样例、实测表和明示结论，排除研究任务指标')
add(4,6,'弹簧振子周期实验的控制变量方法', [main(125,220,495)], notes='实际位置为课题研究参考选题；仅保留已给出的器材和操作方法，不补周期公式与未给出的结果')

def extract(region):
    p, x0, y0, x1, y1 = region
    items=[]
    for block in DOC[p-1].get_text('dict')['blocks']:
        for line in block.get('lines', []):
            spans=line['spans']
            x,y,xx,yy=line['bbox']
            if not (x0 <= (x+xx)/2 <= x1 and y0 <= (y+yy)/2 < y1):
                continue
            # Captions and tiny diagram labels remain faithfully available in page images.
            if max(s['size'] for s in spans)<10.0:
                continue
            t=''.join(s['text'] for s in spans).strip()
            if not t or '仅供个人学习' in t:
                continue
            items.append((y,x,t))
    items.sort()
    return '\n'.join(t for y,x,t in items)

def pagestr(pages):
    groups=[]
    for p in sorted(set(pages)):
        if groups and p==groups[-1][-1]+1: groups[-1].append(p)
        else: groups.append([p])
    return ';'.join(f'P{g[0]}' if len(g)==1 else f'P{g[0]}-P{g[-1]}' for g in groups)

def build():
    patches=json.loads((ROOT/'scripts/patches.json').read_text()) if (ROOT/'scripts/patches.json').exists() else {}
    rows=[]; sources=[]; candidates=[]
    for i, rec in enumerate(RECORDS,1):
        kid=f'RJ-PHY-S1-{i:03d}'
        c,s=rec['c'],rec['s']
        sub=f'第{s}节 {SECTIONS[c-1][s-1]}' if s else ''
        row=dict(zip(FIELDS,[kid,CHAPTERS[c-1],sub,sub or CHAPTERS[c-1],rec['name'],'','','']))
        for field in ['detail','example']:
            regions=rec[field+'_regions']
            raw='\n\n'.join(extract(r) for r in regions)
            candidates.append(dict(knowledge_point_id=kid,knowledge_point=rec['name'],field=field,regions=regions,text_layer_candidate=raw))
            content=patches.get(kid,{}).get(field, raw)
            if content:
                # Images come after complete merged text, never inside a cross-page sentence.
                content=content.strip()+'\n\n'+'\n\n'.join(f'![page-{p:03d}](images/{BOOK}/page-{p:03d}.png)' for p in sorted({r[0] for r in regions}))
            row[field]=content
        pages=sorted({r[0] for f in ['detail','example'] for r in rec[f+'_regions']})
        row['pdf_page']=pagestr(pages)
        rows.append(row)
        sources.append(dict(knowledge_point_id=kid,knowledge_point=rec['name'],chapter=row['chapter'],subchapter=sub,actual_column=rec['notes'],detail_regions=rec['detail_regions'],example_regions=rec['example_regions'],pdf_pages=pages,source_sha256=json.loads((ROOT/'source_report.json').read_text())['sha256'],transcription='explicit visual correction' if kid in patches else 'candidate awaiting final correction'))
    with (ROOT/'knowledge_points.csv').open('w',encoding='utf-8-sig',newline='') as f:
        w=csv.DictWriter(f,fieldnames=FIELDS); w.writeheader(); w.writerows(rows)
    md=['# 普通高中教科书·物理 选择性必修 第一册','']
    for row in rows:
        md += [f"## {row['knowledge_point_id']} {row['knowledge_point']}",'',f"{row['chapter']} / {row['subchapter'] or '章引言'} · {row['pdf_page']}",'',row['detail'],'']
        if row['example']: md += ['### 补充原例原解','',row['example'],'']
    (ROOT/'knowledge_points.md').write_text('\n'.join(md),encoding='utf-8')
    for name,records in [('source_records.jsonl',sources),('raw_candidates.jsonl',candidates)]:
        (ROOT/name).write_text(''.join(json.dumps(r,ensure_ascii=False)+'\n' for r in records),encoding='utf-8')
    (ROOT/'scripts/selection.json').write_text(json.dumps(RECORDS,ensure_ascii=False,indent=2)+'\n')
    print(f'{len(rows)} records, {sum(bool(r["example"]) for r in rows)} supplementary-example fields')

if __name__=='__main__': build()
