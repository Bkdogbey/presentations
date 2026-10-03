"""One 3×3 slide figure per results slide (rows = outcomes, columns = reported coefficients).

Sized to fill the content area of a 1280×720 reveal.js slide, for presentation/smc-no-tabs.qmd.
"""
import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator
from make_reported_effects import (DATA, TITLES, XLABELS, XTITLES, BASELINES, SLIDE_DIR,
                                   SLIDE_COLORS, number)

GROUPS={
    'grid_performance':['Victims per step','Total rewards','Saved victims'],
    'grid_eye_area':['Pupil-size SD','Game-area fixation','Chat-area fixation'],
    'grid_eye_fixation':['Fixation duration','Fixation count','Saccade count'],
}
# Column titles for the slide grids; the first drops the '(Novices)' qualifier.
GRID_TITLES=['LLM effect',*TITLES[1:]]
# Baseline notes without the 'Novice' wording.
GRID_BASELINES=['Baseline: No LLM','Baseline: No LLM','Baseline: LLM effect']
INK,MUTED,ACCENT,XACCENT='#FFFFFF','#B5BCC3','#EC672C','#FFD54F'

def draw(name,outcomes):
    rows=[next(d for d in DATA if d[0]==o) for o in outcomes]
    with plt.rc_context({'text.color':INK,'axes.labelcolor':INK,'xtick.color':INK,
                         'ytick.color':INK,'axes.edgecolor':'#8A9299',
                         'axes.spines.top':False,'axes.spines.right':False,
                         'font.family':'DejaVu Sans'}):
        fig,axes=plt.subplots(3,3,figsize=(12.6,5.75),sharex='col')
        fig.subplots_adjust(left=.16,right=.99,bottom=.115,top=.905,wspace=.2,hspace=.28)
        for i,d in enumerate(rows):
            lo=min(0,*d[2]); hi=max(0,*d[2]); span=hi-lo
            for j,ax in enumerate(axes[i]):
                beta=d[2][j]; q=d[4][j]
                qtext='q: ns' if q=='ns' else 'q '+q
                ax.set_facecolor('none')
                ax.plot([0,1],[0,beta],color=SLIDE_COLORS[j],lw=2.6,marker=['o','s','D'][j],ms=7,
                        ls=['-','--','-.'][j])
                ax.axhline(0,color=MUTED,lw=1,ls=(0,(2,3)),zorder=0)
                ax.annotate(GRID_BASELINES[j],(.5,0),xytext=(0,-4 if beta>=0 else 4),
                            textcoords='offset points',ha='center',
                            va='top' if beta>=0 else 'bottom',fontsize=8.5,
                            color=MUTED,style='italic')
                ax.set_xlim(-.1,1.1)
                # Shared y-scale within an outcome row; headroom for the β / q label.
                ax.set_ylim(lo-.25*span,hi+.6*span)
                ax.yaxis.set_major_locator(MaxNLocator(3))
                ax.tick_params(labelsize=10,length=3)
                if j: ax.set_yticklabels([])
                ax.text(.5,.86,f'β = {number(beta)}   {qtext}',transform=ax.transAxes,
                        ha='center',va='center',fontsize=12,fontweight='bold',color=SLIDE_COLORS[j])
                if i==0:
                    ax.set_title(GRID_TITLES[j].replace('\n',' '),fontsize=13,fontweight='bold',pad=8)
                if i==2:
                    ax.set_xticks([0,1],[l.split('\n')[1] for l in XLABELS[j]])
                    ax.set_xlabel(XTITLES[j],labelpad=2,color=XACCENT,fontsize=12,fontweight='bold')
                else:
                    ax.tick_params(axis='x',labelbottom=False)
            axes[i][0].set_ylabel(f'Δ ({d[1].lower()})',fontsize=9.5,color=MUTED,labelpad=4)
            # Outcome name as a row label, left of the y axis.
            box=axes[i][0].get_position()
            fig.text(.012,(box.y0+box.y1)/2,d[0].replace(' ','\n'),
                     ha='left',va='center',fontsize=13,fontweight='bold',color=ACCENT,linespacing=1.15)
        fig.savefig(SLIDE_DIR/f'{name}.png',dpi=200,transparent=True)
        plt.close(fig)

if __name__=='__main__':
    for name,outcomes in GROUPS.items(): draw(name,outcomes)
    print('Wrote',', '.join(GROUPS))
