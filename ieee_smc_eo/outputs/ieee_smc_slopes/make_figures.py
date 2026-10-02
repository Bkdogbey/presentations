"""Reproduce slope figures from IEEE_SMC (16).pdf, Tables I–II.
Run: python outputs/ieee_smc_slopes/make_figures.py
Dependencies: matplotlib. No fitted means or combined-effect tests are inferred.
"""
from pathlib import Path
from decimal import Decimal
import csv
import json
import zipfile
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
from matplotlib.ticker import MaxNLocator
from matplotlib.path import Path as MplPath
from matplotlib.transforms import Bbox
import numpy as np

ROOT = Path(__file__).resolve().parent
# outcome, model scale, beta1..3, confidence intervals, table q labels,
# exact q values available in the Results prose (None = not reported).
DATA = [
 ('Victims per step', 'Victims per step', [.020,.016,-.009], [[.008,.032],[-.009,.041],[-.029,.011]], ['<0.01','ns','ns'], ['0.0049',None,None]),
 ('Total rewards', 'Reward units', [267.143,-17.714,181.857], [[90.345,443.941],[-282.673,247.245],[-92.037,455.751]], ['<0.01','ns','ns'], ['0.0074',None,None]),
 ('Saved victims', 'Log count', [.035,.221,.435], [[-.369,.439],[-.634,1.076],[-.192,1.062]], ['ns','ns','ns'], ['0.8973',None,None]),
 ('Fixation duration', 'Model units', [-19.326,-26.475,17.059], [[-31.509,-7.143],[-66.839,13.889],[-1.814,35.932]], ['<0.01','ns','ns'], ['0.005',None,None]),
 ('Pupil-size SD', 'Model units', [.122,-.042,-.051], [[.095,.149],[-.118,.034],[-.092,-.010]], ['<0.0001','ns','<0.05'], [None,None,'0.0349']),
 ('Game-area fixation', 'Model units', [-.184,-.015,.114], [[-.229,-.139],[-.088,.058],[.045,.183]], ['<0.0001','ns','<0.01'], [None,None,'0.004']),
 ('Chat-area fixation', 'Model units', [.092,.003,-.045], [[.061,.123],[-.040,.046],[-.094,.004]], ['<0.0001','ns','ns'], [None,None,None]),
 ('Fixation count', 'Log count', [.248,-.201,.815], [[-.185,.681],[-.799,.397],[.145,1.485]], ['ns','ns','<0.05'], [None,None,None]),
 ('Saccade count', 'Log count', [.234,-.482,.961], [[-.178,.646],[-1.019,.055],[.324,1.598]], ['ns','ns','<0.01'], [None,None,None]),
]
BLUE, ORANGE, INK = '#2166AC', '#B45B17', '#26313C'
plt.rcParams.update({'font.family':'DejaVu Sans','font.size':11,'text.color':INK,
 'axes.labelcolor':INK,'xtick.color':INK,'ytick.color':INK,'axes.spines.top':False,
 'axes.spines.right':False,'axes.edgecolor':'#ACB3BA','pdf.fonttype':42,'svg.fonttype':'none'})

def add(*values):
    return float(sum(Decimal(str(v)) for v in values))

def number(v):
    return f'{v:+.3f}' if v else '0.000'

def qlabel(d, j):
    exact = d[5][j]
    if exact is not None:
        return f'q = {exact}'
    q = d[4][j]
    return 'q: ns' if q == 'ns' else f'q {q}'

def interval(d,j):
    lo,hi=d[3][j]
    return f'95% CI [{lo:.3f}, {hi:.3f}]'

def limits(d):
    b1,b2,b3=d[2]
    vals=[0,b1,b2,add(b1,b2,b3)]
    lo,hi=min(vals),max(vals)
    span=hi-lo
    return lo-.23*span,hi+.23*span

def panel(ax,d,kind,compact=False):
    b1,b2,b3=d[2]
    both=add(b1,b2,b3)
    if kind=='A':
        series=[('Novice',[0,b1],b1,0),('Expert',[b2,both],add(b1,b3),None)]
        ticks=['No LLM','LLM']
        title='A  ·  LLM effect'
    else:
        series=[('No LLM',[0,b2],b2,1),('LLM',[b1,both],add(b2,b3),None)]
        ticks=['Novice','Expert']
        title='B  ·  Expertise effect'
    ax.set_title(title,loc='left',fontsize=13,fontweight='bold',pad=14)
    ax.axhline(0,color='#929AA2',lw=1,ls=(0,(2,3)),zorder=1)
    for k,((name,ys,effect,j),color) in enumerate(zip(series,[BLUE,ORANGE])):
        ax.plot([0,1],ys,color=color,lw=2.5,marker='o' if k==0 else 's',
                ms=7,ls='-' if k==0 else '--',zorder=3,label=name)
    ax.set_xlim(-.14,1.14)
    ax.set_ylim(*limits(d))
    ax.set_xticks([0,1],ticks)
    ax.yaxis.set_major_locator(MaxNLocator(5))
    ax.grid(axis='y',color='#E8EBEE',lw=.7)
    ax.set_axisbelow(True)
    ax.set_ylabel(f'Effect relative to Novice + No LLM\n({d[1].lower()})',fontsize=10)
    ax.legend(loc='upper left',fontsize=10,frameon=False,ncol=2,bbox_to_anchor=(0,1.02))
    # Measure actual text and find clear space near each corresponding line.
    labels=[]
    for k,((name,ys,effect,j),color) in enumerate(zip(series,[BLUE,ORANGE])):
        q=qlabel(d,j) if j is not None else 'q = —'
        line=f'β = {number(effect)}\n{q}'
        labels.append(ax.text(.5,.5,line,transform=ax.transAxes,ha='center',va='center',
                    color=color,fontsize=11,fontweight='bold',linespacing=1.5,zorder=5,
                    bbox=dict(facecolor='white',edgecolor='none',alpha=1,pad=3)))
    ax.figure.canvas.draw()
    renderer=ax.figure.canvas.get_renderer()
    bounds=ax.get_window_extent(renderer)
    legend=ax.get_legend().get_window_extent(renderer).padded(8)
    paths=[MplPath(ax.transData.transform([[0,s[1][0]],[1,s[1][1]]])) for s in series]
    zero=MplPath(ax.transData.transform([[-.14,0],[1.14,0]]))
    candidates=[]
    for k,label in enumerate(labels):
        box=label.get_window_extent(renderer)
        halfw,halfh=box.width/2+10,box.height/2+10
        a,b=paths[k].vertices
        ab=b-a
        choices=[]
        for x in np.linspace(.20,.80,31):
            for y in np.linspace(.10,.85,41):
                c=ax.transAxes.transform((x,y))
                rect=Bbox.from_extents(c[0]-halfw,c[1]-halfh,c[0]+halfw,c[1]+halfh)
                if not (bounds.contains(rect.x0,rect.y0) and bounds.contains(rect.x1,rect.y1)):
                    continue
                if rect.overlaps(legend) or any(p.intersects_bbox(rect,filled=False) for p in paths+[zero]):
                    continue
                t=np.clip(np.dot(c-a,ab)/np.dot(ab,ab),0,1)
                distance=np.linalg.norm(c-(a+t*ab))
                score=distance+35*abs(x-.5)
                choices.append((score,(x,y),rect))
        assert choices, f'No clear label position for {d[0]} {kind}'
        candidates.append(sorted(choices,key=lambda item:item[0]))
    best=None
    for first in candidates[0]:
        if best and first[0]+candidates[1][0][0]>=best[0]:
            break
        for second in candidates[1]:
            score=first[0]+second[0]
            if best and score>=best[0]:
                break
            if not first[2].overlaps(second[2]):
                best=(score,first,second)
                break
    assert best, f'Labels collide for {d[0]} {kind}'
    for label,choice in zip(labels,best[1:]):
        label.set_position(choice[1])

def slug(d):
    return d[0].lower().replace(' ','_').replace('-','_')

def main():
    (ROOT/'individual').mkdir(exist_ok=True)
    (ROOT/'paired').mkdir(exist_ok=True)
    rows=[]
    for d in DATA:
        for j,term in enumerate(['LLM','Expertise','LLM × Expertise']):
            rows.append({'outcome':d[0],'model_scale':d[1],'term':term,'beta':d[2][j],
                         'ci95_low':d[3][j][0],'ci95_high':d[3][j][1],
                         'q_table':d[4][j],'q_exact_prose':d[5][j] or '',
                         'source_page':4 if DATA.index(d)<3 else 5})
    with (ROOT/'reported_coefficients.csv').open('w',newline='',encoding='utf-8-sig') as f:
        w=csv.DictWriter(f,fieldnames=list(rows[0])); w.writeheader(); w.writerows(rows)
    contrasts=[]
    with PdfPages(ROOT/'all_18_slope_plots.pdf') as pdf:
        for d in DATA:
            b1,b2,b3=d[2]
            contrasts.append({'outcome':d[0],'novice_no_llm':0,'novice_llm':b1,'expert_no_llm':b2,
                'expert_llm':add(b1,b2,b3),'llm_effect_novice':b1,'llm_effect_expert':add(b1,b3),
                'expertise_effect_no_llm':b2,'expertise_effect_llm':add(b2,b3),
                'combined_effect_q':None,'combined_effect_ci95':None})
            fig,axes=plt.subplots(1,2,figsize=(13,6.3))
            fig.subplots_adjust(left=.08,right=.97,bottom=.10,top=.80,wspace=.32)
            fig.suptitle(d[0],x=.08,y=.96,ha='left',fontsize=22,fontweight='bold')
            for ax,kind in zip(axes,['A','B']): panel(ax,d,kind)
            pdf.savefig(fig)
            fig.savefig(ROOT/'paired'/f'{slug(d)}.png',dpi=180)
            plt.close(fig)
            for kind in ['A','B']:
                fig,ax=plt.subplots(figsize=(8.8,6.3))
                fig.subplots_adjust(left=.13,right=.94,bottom=.10,top=.80)
                fig.suptitle(d[0],x=.08,y=.96,ha='left',fontsize=22,fontweight='bold')
                panel(ax,d,kind)
                for ext in ['png','svg','pdf']:
                    fig.savefig(ROOT/'individual'/f'{slug(d)}_{kind}.{ext}',dpi=200)
                plt.close(fig)
    (ROOT/'derived_contrasts.json').write_text(json.dumps(contrasts,indent=2),encoding='utf-8')
    assert len(rows)==27 and len(contrasts)==9
    game=next(c for c in contrasts if c['outcome']=='Game-area fixation')
    assert game['llm_effect_expert']==-.070 and game['expert_llm']==-.085
    assert len(list((ROOT/'individual').glob('*.svg')))==18
    with zipfile.ZipFile(ROOT/'slope_figures_bundle.zip','w',zipfile.ZIP_DEFLATED) as z:
        for p in ROOT.rglob('*'):
            if p.is_file() and p.suffix!='.zip' and not p.name.startswith('source_page_'):
                z.write(p,p.relative_to(ROOT))
    print('Created 18 figures (PNG/SVG/PDF), 9 paired previews, 9-page PDF, data, and ZIP.')

if __name__=='__main__':
    main()
