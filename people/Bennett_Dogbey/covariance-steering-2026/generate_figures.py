"""Generate explanatory vector figures, not experimental results."""
from pathlib import Path
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, Ellipse

OUT = Path(__file__).resolve().parent / 'assets'
OUT.mkdir(exist_ok=True)
BG, FG, ORANGE, GRAY = '#252525', '#eeeeee', '#EC672C', '#a8a8a8'
plt.rcParams.update({'font.family': 'DejaVu Sans', 'font.size': 13,
                     'text.color': FG, 'axes.labelcolor': FG,
                     'svg.fonttype': 'none', 'savefig.transparent': True})


def base_map():
    fig, ax = plt.subplots(figsize=(6.5, 4.5))
    ax.set(xlim=(-0.8, 11), ylim=(-4.5, 4.8), aspect='equal')
    ax.axis('off')
    for low, high in [(-4, -3), (-1.5, 1.1), (1.9, 4)]:
        ax.add_patch(Rectangle((4.2, low), 1.4, high-low,
                              facecolor='#666666', edgecolor=GRAY, lw=1.2, zorder=3))
    ax.add_patch(Ellipse((0.8, 0), 0.95, 1.25, fill=False, edgecolor=ORANGE, lw=2.2, zorder=5))
    ax.plot(0.8, 0, 'o', color=ORANGE, ms=5, zorder=6)
    ax.plot(9.6, 0, 'o', color=FG, ms=7, zorder=6)
    ax.add_patch(Ellipse((9.6, 0), 0.45, 0.55, fill=False, edgecolor=FG, lw=1.5, zorder=5))
    ax.text(0.8, -1.2, 'Start', ha='center')
    ax.text(9.6, -0.9, 'Target', ha='center')
    return fig, ax


fig, ax = base_map()
ax.annotate('Narrow passage', xy=(4.9, 1.5), xytext=(6.6, 3.4),
            color=ORANGE, arrowprops={'arrowstyle': '-', 'color': ORANGE, 'lw': 1.4})
ax.annotate('Wider passage', xy=(4.9, -2.2), xytext=(6.6, -3.8),
            arrowprops={'arrowstyle': '-', 'color': GRAY, 'lw': 1.4})
ax.text(0.1, 4.4, 'Double-slit schematic', color=GRAY, fontsize=11)
fig.savefig(OUT / 'double-slit.svg', bbox_inches='tight', pad_inches=0.05)
plt.close(fig)

fig, ax = base_map()
regions = [((-0.2, -4), 4.4, 8, ORANGE),
           ((-0.2, 1.1), 10.5, 0.8, '#8b9cac'),
           ((-0.2, -3), 10.5, 1.5, '#8b9cac'),
           ((5.6, -4), 4.7, 8, ORANGE)]
for xy, w, h, color in regions:
    ax.add_patch(Rectangle(xy, w, h, facecolor=color, alpha=0.09, zorder=1))
    ax.add_patch(Rectangle(xy, w, h, fill=False, edgecolor=color, lw=1.2, zorder=2))
for x, y, text in [(1.3, 3.0, 'Left'), (7.1, 1.49, 'Upper'),
                    (7.1, -2.25, 'Lower'), (8.2, 3.0, 'Right')]:
    ax.text(x, y, text, ha='center', va='center', fontsize=12, zorder=7)
fig.savefig(OUT / 'convex-regions.svg', bbox_inches='tight', pad_inches=0.05)
plt.close(fig)

fig, ax = plt.subplots(figsize=(5.1, 3.8))
x = np.linspace(-3.4, 3.6, 700)
y = np.exp(-x*x/2)/np.sqrt(2*np.pi)
b = 1.65
ax.plot(x, y, color=FG, lw=2)
ax.fill_between(x, 0, y, where=x>=b, color=ORANGE, alpha=0.75)
ax.axvline(0, ymin=0, ymax=0.86, color=GRAY, linestyle='--', lw=1)
ax.axvline(b, color=ORANGE, lw=1.6)
ax.annotate('', xy=(b, .28), xytext=(0, .28),
            arrowprops={'arrowstyle': '<->', 'color': ORANGE, 'lw': 1.5})
ax.text(b/2, .305, r'$z_\delta\sigma$', ha='center', color=ORANGE, fontsize=16)
ax.text(0, -.035, r'$a^\top\mu_k$', ha='center', fontsize=15)
ax.text(b, -.035, r'$b$', ha='center', color=ORANGE, fontsize=15)
ax.annotate(r'Allowed tail $\delta$', xy=(2.15, .024), xytext=(1.15, .15),
            arrowprops={'arrowstyle': '-', 'color': GRAY}, fontsize=12)
ax.text(-3.25, .43, r'Projection $a^\top x_k$', color=GRAY, fontsize=12)
ax.set(xlim=(-3.4, 3.7), ylim=(-.085, .47))
ax.axis('off')
ax.plot([-3.4, 3.5], [0, 0], color=GRAY, lw=.8)
fig.savefig(OUT / 'safety-margin.svg', bbox_inches='tight', pad_inches=.05)
plt.close(fig)
