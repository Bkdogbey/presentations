# iHuman Lab Presentation Template

A [Quarto reveal.js](https://quarto.org/docs/presentations/revealjs/) starter deck in the lab's visual theme (dark background, orange `#EC672C` accent, Rubik font). Used for outreach talks, workshops, and conference presentations.

## Quick Start

1. Copy this whole `presentation/` folder and rename it for your talk (e.g. `my-neurips-talk/`).
2. Edit the frontmatter at the top of `template.qmd`: `title`, `subtitle`, `author`, `institute`, `date`.
3. Replace `assets/logo.png` and `assets/background.jpg` if you want different art (keep the same filenames, or update the paths in the frontmatter).
4. Delete the placeholder slides and write your own, reusing the components below.
5. Render:

   ```bash
   quarto render template.qmd     # build once
   quarto preview template.qmd    # live-reload while editing
   ```

The rendered deck opens with arrow keys / space bar to navigate, `f` for fullscreen, `s` for speaker notes.

## File Layout

```
presentation/
├── template.qmd       # the deck itself — copy & edit this
├── theme.scss          # the shared visual theme — usually leave this alone
├── README.md           # this file
└── assets/
    ├── logo.png         # iHuman Lab logo, used on every slide + closing slide
    └── background.jpg   # campus photo, used on title + closing slide backgrounds
```

## Reusable Components

Each of these is demonstrated in `template.qmd` — copy the block you need.

| Component | What it's for | How |
|---|---|---|
| `[text]{.accent}` | Highlight a word/phrase in orange | Inline anywhere in a heading or paragraph |
| `::: {.hook}` | A bold one-line opener at the top of a slide | Wrap one sentence in a `.hook` div |
| `::: {.punchline}` | A bold, orange closing line at the bottom of a slide | Wrap one sentence in a `.punchline` div |
| `::: {.columns}` / `::: {.column width="50%"}` | Two-column layout | Nest two `.column` divs inside `.columns` |
| `::: {.cards}` / `::: {.card}` / `[text]{.card-title}` | A card grid (wraps automatically based on card count) for comparisons or short concept lists | See the "Comparing Two Things" slide. Add `::: {.cards .vertical}` to stack cards in a single column instead of a grid |
| `::: {.flow-diagram}` / `::: {.flow-step}` / `::: {.flow-arrow}` | Step-by-step vertical process/pipeline | See the "A Process or Pipeline" slide |
| `::: {.flow-branch}` | Two parallel steps merging into one flow | Nest two `::: {.flow-step}` blocks inside a `::: {.flow-branch}` inside `::: {.flow-diagram}` |
| `::: {.stats}` / `::: {.stat}` / `[10+]{.stat-number}` / `[Label]{.stat-label}` | Big number + label callouts for quick credibility/impact stats | See the "By the Numbers" slide |
| `[text]{.badge}` | A small inline pill tag | Use inline anywhere, e.g. next to a `.card-title` |
| `.secondary` modifier | De-emphasizes a component, or marks it as an alternate/second category (gray instead of orange) | Add alongside the base class: `::: {.card .secondary}`, `::: {.stat .secondary}`, `::: {.flow-step .secondary}`, `[text]{.badge .secondary}` |
| `::: {.quote}` / `[— Name]{.quote-attribution}` | A large italic pull-quote with an attribution line | See the "What People Are Saying" slide |
| `::: {.divider}` / `[Title]{.divider-title}` / `[Subtitle]{.divider-subtitle}` | A big centered slide marking a transition between major sections | See the un-headed divider slide after "A Process or Pipeline" — no `##` heading needed, `---` alone starts the slide |
| `::: {.impact-grid}` / `::: {.impact-card}` / `::: {.impact-text}` / `[label]{.impact-label}` / `[desc]{.impact-desc}` | Full-bleed photo tiles with a gradient caption overlay | See the "Real-World Impact" slide |
| `::: {.slide-caption}` | A caption pinned to the bottom of a full-bleed background-image slide | See the un-headed full-bleed image slide before the closing slide |
| Markdown tables | Results tables | Standard `\| col \| col \|` markdown — themed automatically |
| Code fences | Code snippets | Standard ```` ```python ```` fences — themed automatically |
| `{background-image="..." background-opacity="..."}` | Full-bleed background image for a slide (title/closing/divider slides) | Add after a slide heading (or with no heading text at all), or use `title-slide-attributes` in the frontmatter for the title slide |

The dark slide background (`#252525`) is the theme's default — you don't need to set `background-color` on every heading.

## Adding a Speaker-Photo Row to the Title Slide

If your talk has multiple presenters and you want photo cards under the title (like the outreach decks on the lab website), add this to the frontmatter's `format.revealjs`:

```yaml
format:
  revealjs:
    include-in-header:
      text: |
        <script>
        document.addEventListener("DOMContentLoaded", function () {
          var titleSlide = document.getElementById("title-slide");
          if (!titleSlide) return;
          var row = document.createElement("div");
          row.style.cssText = "display:flex; gap:2rem; align-items:center; margin-top:2.5rem;";
          var people = [
            { src: "assets/me.jpg", name: "Your Name", role: "Your Role" }
          ];
          people.forEach(function(p) {
            var card = document.createElement("div");
            card.style.cssText = "display:flex; align-items:center; gap:0.9rem;";
            var img = document.createElement("img");
            img.src = p.src;
            img.alt = p.name;
            img.style.cssText = "width:130px; height:130px; border-radius:50%; object-fit:cover; border:3px solid #EC672C; box-shadow:0 2px 8px rgba(0,0,0,0.4);";
            var info = document.createElement("div");
            info.innerHTML = '<div style="font-weight:700; font-size:1.3rem; color:#fff; line-height:1.3;">' + p.name + '</div>' +
                             '<div style="font-size:1.1rem; color:rgba(255,255,255,0.5); margin-top:0.2rem;">' + p.role + '</div>';
            card.appendChild(img);
            card.appendChild(info);
            row.appendChild(card);
          });
          titleSlide.appendChild(row);
        });
        </script>
```

Add one entry to the `people` array per presenter.

## Videos

If you embed a `<video src="...">` tag directly (rather than a markdown image), Quarto won't automatically copy the video file into the rendered output. Declare it explicitly in the frontmatter so it isn't dropped:

```yaml
resources:
  - assets/my-video.mov
```

## Customizing the Theme

`theme.scss` controls colors, fonts, and the custom component styles (`.card`, `.flow-step`, etc.). Avoid renaming existing CSS classes if you want to stay compatible with future updates to this template.

### Color System

Five SCSS variables at the top of `theme.scss` drive every component's color:

| Variable | Default | Used for |
|---|---|---|
| `$primary-color` | `#EC672C` (orange) | Accent, emphasis, the "primary" of a two-category comparison |
| `$secondary-color` | `#757575` (OSU Cool Gray 10) | De-emphasis, the "secondary"/alternate of a two-category comparison |
| `$gray-light` | `#DDDDDD` (OSU Cool Gray 2) | Light surfaces, e.g. `.card` backgrounds |
| `$gray-dark` | `#757575` | Dark text on light surfaces |
| `$body-bg` | `#252525` | The slide background |

Change `$primary-color` and `$body-bg` to re-theme most of the deck at once. Every card, stat, and flow-step also accepts a `.secondary` modifier class that swaps its orange accents for `$secondary-color` — useful for visually separating two categories (e.g. current vs. proposed, required vs. optional) without introducing a third color. `[text]{.badge}` / `[text]{.badge .secondary}` are small inline tags built on the same two colors.

## Publishing

To share a deck as a link, render it and host the output `.html` file (and its `_files` folder) anywhere static files can be served — GitHub Pages, the lab website's `outreach/` section, or a simple file share.

## License

See [LICENSE](../LICENSE) in the repository root.
