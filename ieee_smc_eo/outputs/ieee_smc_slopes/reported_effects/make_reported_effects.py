"""Slope-style displays of the three coefficients actually reported in the tables."""
from pathlib import Path
import csv
import json
import zipfile
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
from matplotlib.ticker import MaxNLocator
plt.rcParams.update({'font.family':'DejaVu Sans','font.size':11,'text.color':'#26313C',
 'axes.labelcolor':'#26313C','xtick.color':'#26313C','ytick.color':'#26313C',
 'axes.spines.top':False,'axes.spines.right':False,'axes.edgecolor':'#ACB3BA',
 'pdf.fonttype':42,'svg.fonttype':'none'})
def number(value): return f'{value:+.3f}' if value else '0.000'
def slug(d): return d[0].lower().replace(' ','_').replace('-','_')

ROOT=Path(__file__).resolve().parent
DATA=json.loads((ROOT/'source_data.json').read_text(encoding='utf-8'))
TERMS=['LLM','Expertise','LLM × Expertise']
TITLES=['LLM effect\n(Novices)','Expertise effect\n(No LLM)','LLM × Expertise\n(Interaction)']
COLORS=['#2166AC','#B45B17','#6B4C9A']
# x is the 0/1 model predictor, so slope = Δy/Δx = β/1 = β.
XLABELS=[['0\nNo LLM','1\nLLM'],['0\nNovice','1\nExpert'],['0\nNovice','1\nExpert']]
XTITLES=['LLM','Expertise','Expertise']
BASELINES=['Baseline: Novice, No LLM','Baseline: Novice, No LLM','Baseline: LLM effect in Novices']

def main():
    ROOT.mkdir(exist_ok=True)
    rows=[]
    with PdfPages(ROOT/'reported_effects.pdf') as pdf:
        for d in DATA:
            fig,axes=plt.subplots(1,3,figsize=(13,5.6),sharey=True)
            fig.subplots_adjust(left=.08,right=.98,bottom=.2,top=.74,wspace=.24)
            fig.suptitle(d[0],x=.08,y=.97,ha='left',fontsize=22,fontweight='bold')
            lo=min(0,*d[2]); hi=max(0,*d[2]); span=hi-lo
            for j,ax in enumerate(axes):
                beta=d[2][j]
                q=d[4][j]
                qtext='q: ns' if q=='ns' else 'q '+q
                ax.set_title(TITLES[j],fontsize=13,fontweight='bold',pad=17,linespacing=1.5)
                ax.plot([0,1],[0,beta],color=COLORS[j],lw=2.5,marker=['o','s','D'][j],ms=7,
                        ls=['-','--','-.'][j])
                ax.axhline(0,color='#929AA2',lw=1,ls=(0,(2,3)),zorder=0)
                # Baseline label sits on the side of the dotted line away from the slope.
                ax.annotate(BASELINES[j],(.5,0),xytext=(0,-5 if beta>=0 else 5),
                            textcoords='offset points',ha='center',
                            va='top' if beta>=0 else 'bottom',fontsize=9.5,
                            color='#6B737B',style='italic')
                ax.set_xlim(-.13,1.13)
                # Dedicated clear space above every line for coefficient and q.
                ax.set_ylim(lo-.15*span,hi+.65*span)
                ax.set_xticks([0,1],XLABELS[j]); ax.set_xlabel(XTITLES[j],labelpad=4)
                ax.yaxis.set_major_locator(MaxNLocator(5))
                ax.text(.5,.90,f'β = {number(beta)}\n{qtext}',transform=ax.transAxes,
                        ha='center',va='center',fontsize=12,fontweight='bold',
                        color=COLORS[j],linespacing=1.6)
                rows.append(dict(outcome=d[0],effect=TERMS[j],beta=beta,q_table=q,model_scale=d[1]))
            axes[0].set_ylabel(f'Difference from baseline ({d[1].lower()})',fontsize=11)
            pdf.savefig(fig)
            for ext in ['png','svg','pdf']:
                fig.savefig(ROOT/f'{slug(d)}.{ext}',dpi=200)
            plt.close(fig)
    with (ROOT/'plotted_values.csv').open('w',newline='',encoding='utf-8-sig') as f:
        writer=csv.DictWriter(f,fieldnames=list(rows[0])); writer.writeheader(); writer.writerows(rows)
    (ROOT/'source_data.json').write_text(json.dumps(DATA,indent=2),encoding='utf-8')
    (ROOT/'README.md').write_text('''# Reported coefficients

These nine figures supersede the earlier combined-effect plots. Each shows the three coefficients directly from Tables I–II of IEEE_SMC (16).pdf (pp. 4–5). Beta values and q bounds / ns match the tables exactly; more precise prose q-values are not substituted. No coefficient sums are plotted.

Each slope connects zero effect to a reported coefficient. The endpoints are a visual encoding of a coefficient, not group means or a time trend. With Novice + No LLM as the model reference, LLM is the LLM effect among novices; Expertise is expert versus novice without LLM; LLM × Expertise is the difference in those conditional effects (the interaction). The interaction is not an Expert + LLM group estimate.

The three panels use the same vertical scale within an outcome; scales differ across outcomes. Count outcomes remain on the modeled log scale. ns means reported as not significant, not a numeric q-value. No CI, SE, or explanatory footer appears in the figures.

Source data and rendering scripts are included in the ZIP. Run `python make_reported_effects.py` in this directory (matplotlib required).
''',encoding='utf-8')
    with zipfile.ZipFile(ROOT/'reported_effects_bundle.zip','w',zipfile.ZIP_DEFLATED) as z:
        for p in ROOT.iterdir():
            if p.is_file() and p.suffix!='.zip': z.write(p,p.name)
    make_slide_figures()
    assert len(rows)==27
    print('Created nine figures with all 27 reported beta/q pairs, PDF, PNG, SVG, and ZIP.')

SLIDE_DIR=ROOT.parents[2]/'presentation'/'assets'/'reported_effects'
SLIDE_COLORS=['#6FB3F2','#EC672C','#B59AE0']

def make_slide_figures():
    """Dark, title-free copies for the tabbed slide in presentation/smc.qmd."""
    SLIDE_DIR.mkdir(parents=True,exist_ok=True)
    ink,muted='#FFFFFF','#B5BCC3'
    with plt.rc_context({'text.color':ink,'axes.labelcolor':ink,'xtick.color':ink,
                         'ytick.color':ink,'axes.edgecolor':'#8A9299'}):
        for d in DATA:
            fig,axes=plt.subplots(1,3,figsize=(13,4.9),sharey=True)
            fig.subplots_adjust(left=.08,right=.98,bottom=.2,top=.84,wspace=.24)
            lo=min(0,*d[2]); hi=max(0,*d[2]); span=hi-lo
            for j,ax in enumerate(axes):
                beta=d[2][j]; q=d[4][j]
                qtext='q: ns' if q=='ns' else 'q '+q
                ax.set_facecolor('none')
                ax.set_title(TITLES[j],fontsize=14,fontweight='bold',pad=12,linespacing=1.4)
                ax.plot([0,1],[0,beta],color=SLIDE_COLORS[j],lw=3,marker=['o','s','D'][j],ms=8,
                        ls=['-','--','-.'][j])
                ax.axhline(0,color=muted,lw=1.2,ls=(0,(2,3)),zorder=0)
                ax.annotate(BASELINES[j],(.5,0),xytext=(0,-6 if beta>=0 else 6),
                            textcoords='offset points',ha='center',
                            va='top' if beta>=0 else 'bottom',fontsize=11,
                            color=muted,style='italic')
                ax.set_xlim(-.13,1.13)
                ax.set_ylim(lo-.15*span,hi+.65*span)
                ax.set_xticks([0,1],XLABELS[j]); ax.set_xlabel(XTITLES[j],labelpad=4,color='#FFD54F',fontsize=13,fontweight='bold')
                ax.tick_params(labelsize=12)
                ax.yaxis.set_major_locator(MaxNLocator(5))
                ax.text(.5,.88,f'β = {number(beta)}\n{qtext}',transform=ax.transAxes,
                        ha='center',va='center',fontsize=14,fontweight='bold',
                        color=SLIDE_COLORS[j],linespacing=1.5)
            axes[0].set_ylabel(f'Difference from baseline ({d[1].lower()})',fontsize=12)
            fig.savefig(SLIDE_DIR/f'{slug(d)}.png',dpi=200,transparent=True)
            plt.close(fig)

if __name__=='__main__': main()
