"""Build this separate textbook package from visually selected source regions.
Selection and formula corrections are editorial inputs, never OCR approval.
"""
from pathlib import Path
import csv,json,re,fitz
R=Path(__file__).resolve().parents[1]
META=json.loads((R/'source_report.json').read_text()); D=fitz.open(META['source_pdf'])
BOOK=R.name
# Replacements use physical-page rectangles; typeset fractions and scripts are
# transcribed explicitly rather than linearized in PDF drawing order.
MATH={
26:[(480,515,r'$v=\frac{\Delta x}{\Delta t}$'),(716,739,'变化的。所以，由 Δx/Δt 求得的速度 v，表示的只是物体在')],
27:[(298,320,'时，运动快慢的差异可以忽略不计，此时，我们就把 Δx/Δt 叫'),(658,686,r'$v=\frac{\Delta x}{\Delta t}$')],
32:[(680,712,r'$a=\frac{\Delta v}{\Delta t}$')],
33:[(240,270,'Δv。由于加速度 a＝Δv/Δt，所以加速度 a 的方向与速度的变')],
45:[(75,100,'代入 a＝Δv/Δt 中，得到'),(675,710,r'$t=\frac{v-v_0}{a}=\frac{0-16\ \mathrm{m/s}}{-6\ \mathrm{m/s^2}}=2.67\ \mathrm{s}$')],
47:[(560,583,r'$x=\frac12(v_0+v)t$'),(610,640,r'$x=v_0t+\frac12at^2$'),(670,695,'初速度为0，这个公式可以简化为 $x=\frac12at^2$。')],
48:[(375,405,r'$x=v_0t+\frac12at^2=10\ \mathrm{m/s}\times2.4\ \mathrm{s}+\frac12\times25\ \mathrm{m/s^2}\times(2.4\ \mathrm{s})^2=96\ \mathrm{m}$'),(500,535,r'$a=\frac{v-v_0}{t}=-\frac{v_0}{t}=-\frac{80\ \mathrm{m/s}}{2.5\ \mathrm{s}}=-32\ \mathrm{m/s^2}$'),(590,620,r'$x=v_0t+\frac12at^2=v_0t+\frac12(-\frac{v_0}{t})t^2=\frac12v_0t=\frac12\times80\ \mathrm{m/s}\times2.5\ \mathrm{s}=100\ \mathrm{m}$')],
49:[(110,134,'式 $x=v_0t+\frac12at^2$，上一节我们还学习了匀变速直线运动的'),(185,210,r'$v^2-v_0^2=2ax$'),(705,748,r'$a=\frac{v_M^2-v_0^2}{2x_1}=\frac{(15\ \mathrm{m/s})^2-(35\ \mathrm{m/s})^2}{2\times3000\ \mathrm{m}}=-0.167\ \mathrm{m/s^2}$')],
50:[(115,148,r'$x_2=\frac{v^2-v_M^2}{2a}=\frac{0-(15\ \mathrm{m/s})^2}{2\times(-0.167)\ \mathrm{m/s^2}}=674\ \mathrm{m}$')],
55:[(467,495,r'$v=gt,\quad x=\frac12gt^2$')],
69:[(118,150,r'$\mu=\frac{F_\mathrm{f}}{F_\mathrm{N}}$')],
82:[(499,528,r'$F_\mathrm{f}=G_x=G\sin\theta=G\frac{h}{l}\qquad(1)$'),(575,602,r'$F_\mathrm{N}=G_y=G\cos\theta=G\frac{b}{l}\qquad(2)$'),(650,680,r'$G\frac{h}{l}=\mu G\frac{b}{l}$')],
83:[(438,468,r'由图可知，$F_1=\frac{F_4}{\cos\theta}=\frac{G}{\cos\theta}$'),(690,716,r'由（1）（2）式解得 $F_1=\frac{G}{\cos\theta}$，$F_2=G\tan\theta$。'),(720,748,r'根据牛顿第三定律，绳 AO 和绳 BO 所受的拉力大小分别为 $\frac{G}{\cos\theta}$ 和 $G\tan\theta$。')],
94:[(255,290,r'$a=\frac{2x}{t^2}\qquad(1)$'),(490,530,r'$\frac{x_1}{x_2}=\frac{a_1}{a_2}\qquad(2)$')],
97:[(76,104,'1/m 成正比。作 a－1/m 图像进行检验（图4.2-5）。如果检验')],
100:[(230,265,r'$a\propto\frac{F}{m}$')],
101:[(505,535,r'$a_1=\frac{0-v_0}{t}=-\frac{v_0}{t}$'),(555,582,r'$F_\mathrm{阻}=ma_1=-\frac{mv_0}{t}=-\frac{1100\ \mathrm{kg}\times27.8\ \mathrm{m/s}}{70\ \mathrm{s}}=-437\ \mathrm{N}$'),(700,730,r'$a_2=\frac{F_\mathrm{合}}{m}=\frac{1563\ \mathrm{N}}{1100\ \mathrm{kg}}=1.42\ \mathrm{m/s^2}$')],
102:[(445,480,r'$a=\frac{F}{m}=g\tan\theta$')],
104:[(420,448,r'$v=\frac{\Delta x}{\Delta t}$'),(545,580,r'$a=\frac{\Delta v}{\Delta t}$')],
106:[(425,460,r'$a=\frac{F}{m}=\frac{1.4\ \mathrm{N}}{0.7\ \mathrm{kg}}=2\ \mathrm{N/kg}=2\ \mathrm{m/s^2}$'),(575,610,r'$x=\frac12at^2=\frac12\times2\ \mathrm{m/s^2}\times25\ \mathrm{s^2}=25\ \mathrm{m}$')],
107:[(165,191,r'$a=\frac{F}{m}=\frac{1.4}{0.7}\ \mathrm{m/s^2}=2\ \mathrm{m/s^2}$'),(227,255,r'$x=\frac12at^2=\frac12\times2\times25\ \mathrm{m}=25\ \mathrm{m}$')],
110:[(520,550,r'$a_1=\frac{F_\mathrm{f}}{m}=-\frac{\mu_1mg}{m}=-\mu_1g=-0.02\times10\ \mathrm{m/s^2}=-0.2\ \mathrm{m/s^2}$'),(610,645,r'$x_1=-\frac{v_0^2}{2a_1}=-\frac{3.4^2}{2\times(-0.2)}\ \mathrm{m}=28.9\ \mathrm{m}$')],
111:[(115,150,r'$x_2=-\frac{v_{10}^2}{2a_2}=-\frac{v_0^2+2a_1x_{10}}{2a_2}=-\frac{3.4^2+2\times(-0.2\times10)}{2\times(-0.18)}\ \mathrm{m}=21\ \mathrm{m}$')],
112:[(210,240,r'$x=v_0t+\frac12at^2$'),(280,315,r'$a=\frac{2(x-v_0t)}{t^2}=\frac{2\times(60-2\times5)}{5^2}\ \mathrm{m/s^2}=4\ \mathrm{m/s^2}$')],
123:[(319,352,r'$l=\frac{l_n-l_0}{n}$')],
128:[(75,103,'1/10，肯定会有误差。')],
129:[(100,130,r'相对误差＝$\frac{\text{绝对误差}}{\text{测量值}}$'),(200,235,r'$\frac{0.1\ \mathrm{mm}}{1.3\ \mathrm{mm}}=8\%$'),(345,380,r'$\frac{0.1\ \mathrm{mm}}{13.0\ \mathrm{mm}}=0.8\%$')]
}
# Explicitly bounded original supplementary solved examples.
EX={
'匀变速直线运动的速度与时间的关系':[[45,200,755]],
'匀变速直线运动的位移与时间的关系':[[48,70,755]],
'匀变速直线运动的速度与位移的关系':[[49,310,755],[50,65,205]],
'滑动摩擦力与动摩擦因数':[[69,410,710],[70,60,175]],
'力的合成和分解与平行四边形定则':[[79,290,545]],
'共点力平衡中的正交分解法':[[83,70,755]],
'牛顿第二定律':[[101,135,770],[102,70,770]],


}
CH={0:'序言 物理学：研究物质及其运动规律的科学',1:'第一章 运动的描述',2:'第二章 匀变速直线运动的研究',3:'第三章 相互作用——力',4:'第四章 运动和力的关系',5:'课题研究',6:'学生实验'}
SEC={1:['质点 参考系','时间 位移','位置变化快慢的描述——速度','速度变化快慢的描述——加速度'],2:['实验：探究小车速度随时间变化的规律','匀变速直线运动的速度与时间的关系','匀变速直线运动的位移与时间的关系','自由落体运动'],3:['重力与弹力','摩擦力','牛顿第三定律','力的合成和分解','共点力的平衡'],4:['牛顿第一定律','实验：探究加速度与力、质量的关系','牛顿第二定律','力学单位制','牛顿运动定律的应用','超重和失重']}
SKIP={'实验','演示','拓展学习','科学漫步','思考与讨论','做一做','科学方法','问题','？'}

def region(spec):
 p,y0,y1,*xx=spec; x0,x1=xx or [0,595]; spans=[]
 active_math=MATH.get(p,[]) if (not xx or (p==128 and x0>300) or (p==129 and x0<100)) else []
 for b in D[p-1].get_text('dict')['blocks']:
  if b['type']:continue
  for l in b['lines']:
   for s in l['spans']:
    x,y=s['bbox'][:2]
    if y0-0.5<=y<y1 and x0<=x<x1 and y<775 and s['text'].strip() and s['size']<20 and s['size']>=5:
     spans.append(s)
 # Keep independent reading areas: marginal blue notes follow the completed body.
 groups=[[],[]]
 for s in spans:
  side=s['color']==154505 and not xx
  groups[int(side)].append(s)
 outputs=[]
 for gi,ss in enumerate(groups):
  threshold=10.0 if p in {24,30,34,50,51,55,56,71,72,75,91,92,103,107,108} else 11.5
  bases=[s for s in ss if s['size']>=threshold]
  rows=[]
  for s in bases:
   if any(a<=s['bbox'][1]<b for a,b,t in active_math if gi==0):continue
   y=s['origin'][1]
   match=next((r for r in rows if abs(r[0]-y)<3.5),None)
   if match is None:rows.append([y,[s]])
   else:match[1].append(s)
  for s in ss:
   if s['size']>=threshold:continue
   if any(a<=s['bbox'][1]<b for a,b,t in active_math if gi==0):continue
   if rows:
    near=min(rows,key=lambda r:abs(r[0]-s['origin'][1]))
    if abs(near[0]-s['origin'][1])<8 and any(abs(z['bbox'][2]-s['bbox'][0])<6 or abs(z['bbox'][0]-s['bbox'][2])<6 for z in near[1]):near[1].append(s)
  lines=[]
  for y,rr in rows:
   rr.sort(key=lambda s:s['bbox'][0]); t=''
   for z in rr:
    v=z['text']
    if z['size']<10 and v.strip() and re.fullmatch(r'[0-9−\-]+',v.strip()):
     sub=z['origin'][1]>y+1
     v=v.strip().translate(str.maketrans('0123456789-−','₀₁₂₃₄₅₆₇₈₉₋₋' if sub else '⁰¹²³⁴⁵⁶⁷⁸⁹⁻⁻'))
    t+=v
   t=t.strip()
   if not t or re.sub(r'\s','',t) in SKIP or t=='~':continue
   if len(t)<3 and not re.search(r'[\u4e00-\u9fff]',t):continue
   if p==44 and rr[0]['bbox'][0]>395:continue
   if p==79 and rr[0]['bbox'][0]<200 and y>575:continue
   if not re.search(r'[\u4e00-\u9fffA-Za-zΔθμµ＝=0-9]',t):continue
   lines.append([min(z['bbox'][1] for z in rr),rr[0]['bbox'][0],t])
  if gi==0:
   for a,b,t in active_math:
    # x clipping prevents patches in the other column from leaking in.
    if y0<=a<y1 and (not xx or (p==128 and x0>300) or (p==129 and x0<100)):
     lines.append([a,220,t])
  lines.sort(key=lambda a:a[0]); out=''; last=None
  for y,x,t in lines:
   sep=''
   if out:
    if last and (y-last[0]>30 or (x-last[1]>18 and y-last[0]>16) or '$' in t or '$' in last[2]):sep='\n\n'
    elif re.search('[A-Za-z0-9]$',out) and re.match('[A-Za-z0-9]',t):sep=' '
   out+=sep+t;last=[y,x,t]
  outputs.append(out.replace('\x0crac',r'\frac'))
 return outputs

def assemble(regs):
 body='';notes=[]
 for spec in regs:
  a,b=region(spec)
  if a:body+= ('\n\n' if body and body[-1:] in '。？！：；.!?$' else '')+a
  if b:notes.append(b)
 if notes:body+='\n\n'+'\n\n'.join(notes)
 return body.strip()

def labels(ps):
 groups=[]
 for p in sorted(set(ps)):
  if groups and p==groups[-1][-1]+1:groups[-1].append(p)
  else:groups.append([p])
 return ';'.join(f'P{g[0]}' if len(g)==1 else f'P{g[0]}-P{g[-1]}' for g in groups)

def pics(regs):return '\n\n'.join(f'![page-{p:03}](images/{BOOK}/page-{p:03}.png)' for p in dict.fromkeys(r[0] for r in regs))
patch=json.loads((R/'patches.json').read_text()) if (R/'patches.json').exists() else {}
rows=[];sources=[];candidates=[]
for i,line in enumerate((R/'selection.tsv').read_text().splitlines(),1):
 c,s,name,sp=line.split('\t');c=int(c);s=int(s);regs=[list(map(int,r.split(':'))) for r in sp.split(';')]
 detail=assemble(regs); er=EX.get(name,[]);example=assemble(er)
 candidates.append({'knowledge_point':name,'detail':detail,'example':example})
 pt=patch.get(name,{})
 detail=pt.get('detail',detail);example=pt.get('example',example)
 detail=detail.replace('\x0crac',r'\frac');example=example.replace('\x0crac',r'\frac')
 for old,new in pt.get('replace',[]):detail=detail.replace(old,new);example=example.replace(old,new)
 def inline_scripts(t):
  parts=re.split(r'(\$[^$]*\$)',t)
  for k in range(0,len(parts),2):
   for old,new in {'F₁x':r'$F_{1x}$','F₁y':r'$F_{1y}$','Fmax':r'$F_{\max}$','FN′':r"$F_\mathrm{N}′$",'Ff':r'$F_\mathrm{f}$','FN':r'$F_\mathrm{N}$','FT':r'$F_\mathrm{T}$','Fx':r'$F_x$','Fy':r'$F_y$','Gx':r'$G_x$','Gy':r'$G_y$','vM':r'$v_M$','ln':r'$l_n$','xA':r'$x_A$','xB':r'$x_B$'}.items():
    parts[k]=parts[k].replace(old,new)
  return ''.join(parts)
 for old,new in [('G＝mg其中','G＝mg\n\n其中'),('G＝mg另一种','G＝mg\n\n另一种'),('F＝kx这个','F＝kx\n\n这个'),('Ff＝μF压其中','Ff＝μF压\n\n其中'),('0 <F≤ Fmax瓶子','0 <F≤ Fmax\n\n瓶子'),('F＝Ff由于','F＝Ff\n\n由于'),('v＝v₀＋at＝10 m/s＋0.6 m/s²×10 s＝ 16 m/s（2）','v＝v₀＋at＝10 m/s＋0.6 m/s²×10 s＝16 m/s\n\n（2）'),('F ＝5.4 cm×10 N/cm ＝54 N用量角器','F＝5.4 cm×10 N/cm＝54 N\n\n用量角器'),('h＝µb＝ 0.4×6 m ＝2.4 m滑梯','h＝µb＝0.4×6 m＝2.4 m\n\n滑梯'),('F合＝2 000 N －437 N＝1 563 N由','F合＝2 000 N－437 N＝1 563 N\n\n由'),('F＝ma＝1 kg·m/s²如果','F＝ma＝1 kg·m/s²\n\n如果'),('x∝t²这样','x∝t²\n\n这样')]:
  detail=detail.replace(old,new);example=example.replace(old,new)
 detail=inline_scripts(detail);example=inline_scripts(example)
 sec=f'{s}. {SEC[c][s-1]}' if s else CH[c]
 row=dict(zip(['knowledge_point_id','chapter','subchapter','section','knowledge_point','detail','example','pdf_page'],[f'RJ-PHYSICS-SC1-{i:03}',CH[c],sec,sec,name,detail+'\n\n'+pics(regs),example+'\n\n'+pics(er) if example else '',labels([r[0] for r in regs+er])]))
 rows.append(row)
 sources.append({'knowledge_point_id':row['knowledge_point_id'],'knowledge_point':name,'source_pdf_sha256':META['sha256'],'detail_regions':regs,'example_regions':er,'coordinates':'PDF points: [physical_page,y0,y1,optional_x0,x1]','formula_corrections':'scripts/build.py:MATH','text_patches':name in patch,'images_follow_complete_cross_page_text':True})
with (R/'knowledge_points.csv').open('w',encoding='utf-8-sig',newline='') as f:
 w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
for name,data in [('source_records',sources),('transcription_candidates',candidates)]:
 (R/f'{name}.jsonl').write_text(''.join(json.dumps(x,ensure_ascii=False)+'\n' for x in data))
md=['# 普通高中教科书·物理 必修 第一册（人教版）\n']
for r in rows:
 md.append(f"## {r['knowledge_point_id']} {r['knowledge_point']}\n\n{r['chapter']} / {r['section']} · PDF {r['pdf_page']}\n\n{r['detail']}\n")
 if r['example']:md.append('### 补充原例与原解\n\n'+r['example']+'\n')
(R/'knowledge_points.md').write_text('\n'.join(md))
print(len(rows),'records')
