"""Slope-style displays of the three coefficients actually reported in the tables."""
from pathlib import Path
import csv
import json
import zipfile
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
from matplotlib.ticker import MaxNLocator
from make_figures import DATA, number, slug

ROOT=Path(__file__).resolve().parent/'reported_effects'
TERMS=['LLM','Expertise','LLM × Expertise']
TITLES=['LLM effect\n(Novices)','Expertise effect\n(No LLM)','LLM × Expertise\n(Interaction)']
COLORS=['#2166AC','#B45B17','#6B4C9A']

def main():
    ROOT.mkdir(exist_ok=True)
    rows=[]
    with PdfPages(ROOT/'reported_effects.pdf') as pdf:
        for d in DATA:
            fig,axes=plt.subplots(1,3,figsize=(13,5.6),sharey=True)
            fig.subplots_adjust(left=.08,right=.98,bottom=.12,top=.74,wspace=.24)
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
                ax.set_xlim(-.13,1.13)
                # Dedicated clear space above every line for coefficient and q.
                ax.set_ylim(lo-.15*span,hi+.65*span)
                ax.set_xticks([0,1],['Zero effect','Estimate'])
                ax.yaxis.set_major_locator(MaxNLocator(5))
                ax.text(.5,.90,f'β = {number(beta)}\n{qtext}',transform=ax.transAxes,
                        ha='center',va='center',fontsize=12,fontweight='bold',
                        color=COLORS[j],linespacing=1.6)
                rows.append(dict(outcome=d[0],effect=TERMS[j],beta=beta,q_table=q,model_scale=d[1]))
            axes[0].set_ylabel(f'Reported effect ({d[1].lower()})',fontsize=11)
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

Source data and rendering scripts are included in the ZIP. Run `python make_reported_effects.py` with make_figures.py in the same directory (matplotlib and numpy required).
''',encoding='utf-8')
    with zipfile.ZipFile(ROOT/'reported_effects_bundle.zip','w',zipfile.ZIP_DEFLATED) as z:
        for p in ROOT.iterdir():
            if p.is_file() and p.suffix!='.zip': z.write(p,p.name)
        for name in ['make_reported_effects.py','make_figures.py']:
            z.write(ROOT.parent/name,name)
    assert len(rows)==27
    print('Created nine figures with all 27 reported beta/q pairs, PDF, PNG, SVG, and ZIP.')

if __name__=='__main__': main()
