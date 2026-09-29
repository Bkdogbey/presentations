# iHuman Lab Presentations

Every iHuman Lab talk, poster and tutorial lives here and is published as a website (see [Website](#website)). Students submit their own presentation with a pull request.

## Structure

The layout mirrors the people pages on the [lab website](https://github.com/iHuman-Lab/lab-website): one folder per person, grouped by role.

```
pi/<First_Last>/<deck>.qmd
phd/<First_Last>/<deck>.qmd
master/<First_Last>/<deck>.qmd
undergraduate/<First_Last>/<deck>.qmd
alumni/<First_Last>/<deck>.qmd
<name>/<name>.qmd            # lab-authored tutorials and outreach decks (e.g. shasta-tutorial/)
_assets/                     # shared lab theme, used by every deck
_template/deck.qmd           # starter deck to copy
```

Put everything a deck needs (images, video, data) in your own folder.

## Submit a presentation (students)

1. **Fork** this repo (or create a branch if you have write access) and clone it.
2. Create your folder, e.g. `phd/Jane_Doe/`. Use `First_Last` with underscores, the same as your folder on the lab website.
3. Copy [`_template/deck.qmd`](_template/deck.qmd) into it and rename it for your talk (e.g. `phd/Jane_Doe/smc2026.qmd`). Keep the `metadata-files` line: it gives your deck the lab theme, logo and footer.
4. Fill in the front matter (`title`, `author`, `date`, `description`, `image`, `event_type`). These make your card on the home page. Put the card picture in your folder.
5. Preview it while you write: `quarto preview phd/Jane_Doe/smc2026.qmd`
6. Open a pull request. The PR template has a checklist, and a check runs `quarto render` on the whole site, so a green check means your deck builds.
7. When the PR is merged into `main`, the site rebuilds and your card appears.

Tips:

- Use a fixed `date` (`2026-01-31`), not `today`, so cards sort correctly.
- Don't commit build output (`*.html`, `*_files/`); `.gitignore` already skips it.
- Keep media small (compress video, aim under 25 MB per deck).
- You can only put decks in your own folder. Don't edit `_assets/` or other people's folders; ask a maintainer if the theme needs a change.
- Posters that are PDFs or images aren't shown yet. Make them a `.qmd` page that embeds the image or PDF.

## Website

This repo is a Quarto website (same look as the [lab website](https://github.com/iHuman-Lab/lab-website)) that lists every lab presentation (tutorials, talks and posters) as a card on the home page. Pushing to `main` builds and publishes it to GitHub Pages (`gh-pages` branch) via `.github/workflows/publish.yml`.

```bash
quarto preview     # live-reload the whole site
quarto render      # build to _site/
```

Any `.qmd` matching the layout above shows up on the home page automatically. Its YAML `title`, `author`, `description`, `date`, `image` and `event_type` fill the card.
