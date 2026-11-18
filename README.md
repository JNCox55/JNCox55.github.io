# Player One's Cartridge Shelf

A personal blog built with [Pelican](https://getpelican.com) and a custom theme
inspired by 90s home consoles. On the home page, each post is a **cartridge**.
Pick one and it drops into the console, and the **CRT TV** boots up with a preview.
Clicking through takes you to a clean reading page.

No JavaScript frameworks. The console runs on HTML and CSS (radio buttons + `:has()`).
There are only two small vanilla JS files: keyboard/swipe controls for the console
(optional) and the search page.

> First time setting up, or ready to deploy? See **[INSTALL.md](INSTALL.md)**.

## Day-to-day

```bash
make dev                         # http://localhost:8000, rebuilds on save
make new title="My Next Post"    # scaffold a post (starts as a draft)
make build                       # one-off build into output/
```

## Writing a post

Posts are Markdown files in `content/articles/`. `make new` creates one like this:

```markdown
Title: Why Chrono Trigger Still Holds Up
Date: 2026-11-01 10:00
Slug: why-chrono-trigger-still-holds-up
Tags: rpg, snes, retrospective
Category: Games
Summary: One or two sentences. This shows up on the CRT screen and in search.
Cover: images/covers/chrono.svg
Cart_color: #5b4b8a

Your post in Markdown…
```

| Field | Required | What it does |
| --- | --- | --- |
| `Title`, `Date` | yes | The basics. |
| `Tags` | recommended | Comma separated. Each tag gets a page at `/tag/<tag>/` and is searchable. |
| `Category` | recommended | One per post (e.g. Games, Tech, Life). |
| `Summary` | recommended | The CRT preview text. Without it, Pelican uses the first ~40 words. |
| `Cover` | optional | Cartridge label art. Put images in `content/images/covers/`. Pixel art and SVG look great (they're rendered `pixelated`). Without a cover, the label shows the title on a coloured stripe. |
| `Cart_color` | optional | The cartridge shell colour (any CSS colour). Defaults to classic grey. |
| `Slug` | optional | URL becomes `/posts/<slug>/`. Defaults to a slug of the title. |
| `Status: draft` | optional | Keeps the post out of the build until you remove the line. |

To link to another post or page, use Pelican's `{filename}` syntax:
`[my rankings]({filename}/pages/game-rankings.md)`.

## Special pages

- **Game Rankings** (`/game-rankings/`): edit `data/rankings.yaml`. Each entry
  has `rank, title, platform, year, score (0–100), verdict`, plus an optional `cover`
  and an optional `review_slug`, which links the row to one of your posts. Platform
  filter chips are generated automatically. Text in `content/pages/game-rankings.md`
  shows above the table.
- **About**: `content/pages/about.md`.
- **Search** (`/search/`): uses `search.json`, which is generated at build time. Supports
  `/search/?q=words` and `/search/?tag=rpg` (or type `#rpg`).
- **404**: the "GAME OVER / CONTINUE?" screen.

### Adding another special page

1. Create `content/pages/my-page.md` with `Title:`, `Slug: my-page`, and `Template: my_page`.
2. Create `themes/cartridge/templates/my_page.html` that `{% extends "base.html" %}`.
3. Need data? Add `data/my-data.yaml` and load it in `pelicanconf.py` like
   `GAME_RANKINGS`. Every UPPERCASE setting is available in templates.
4. To show it in the top nav, add its slug to `MENU_PAGES` in `pelicanconf.py`.

## Settings you'll probably touch (`pelicanconf.py`)

- `AUTHOR`, `SITENAME`, `SITE_TAGLINE`, `SOCIAL`
- `CONSOLE_SLOTS`: how many recent posts load into the console and shelf
- `LIBRARY_PAGE_SIZE`: posts per page in the home page's Game Library list (default 20).
  Older posts continue on `/page/2/`, `/page/3/`, … with numbered page links. The
  console is the same on every page; only the library list changes.
- `MENU_PAGES`: which pages appear in the nav
- `publishconf.py`: the production `SITEURL` (see INSTALL.md)

## Security notes

It's a static site with no server, logins or database, so the attack surface is small.
These guard rails keep it that way, so please keep them when editing:

- **Templates autoescape** (`JINJA_ENVIRONMENT` in `pelicanconf.py`). Quotes or `< > &` in titles,
  tags or `rankings.yaml` are always shown as text. Only rendered post/page bodies are
  marked `|safe`. Don't add `|safe` to anything else.
- **`Cart_color` is validated** (`css_color` filter). Anything that isn't a plain CSS colour is
  replaced by the default, with a build warning.
- **Content-Security-Policy** (`CONTENT_SECURITY_POLICY` in `pelicanconf.py`, sent as a `<meta>` tag).
  Scripts only load from this site. Inline `<script>` and `onclick=` don't run, so keep JS in
  `static/js/`. To embed something external (e.g. YouTube), add its host to the policy.
- **Search renders results with DOM APIs** (`textContent`), never `innerHTML`.
- **Deploy workflow** uses per-job least-privilege permissions and doesn't keep the
  GitHub token after checkout. It has no secrets and doesn't run on pull requests.
- **Dependencies:** `requirements.txt` sets safe minimum versions. To check for known
  vulnerabilities, run `pip install pip-audit && pip-audit -r requirements.txt`.
- **Never commit secrets.** The site needs none. `.gitignore` already excludes `.venv/` and `output/`.

## How the theme is put together

```
themes/cartridge/
  templates/
    base.html            header/nav/footer shell
    index.html           TV + console + controller + shelf + library
    article.html         reading page (no console)
    page.html            plain pages
    listing.html         shared by tag.html / category.html / archives.html
    tags.html            "Genre Select" tag + category grid
    search_page.html     search UI     search_index.html → /search.json
    rankings.html        high-score table   404.html  game over screen
    partials/macros.html cartridge, tag chips, post "spines", read time, pixel icons
  static/css/
    base.css             colour tokens, fonts, header/footer, chips, spines
    console.css          console, cartridges, controller, shelf
    crt.css              TV, scanlines, power-on animation, 404
    article.css          reading + listing + search
    rankings.css         arcade table
  static/js/
    console.js           ←/→ keys, Enter, swipe (progressive enhancement)
    search.js            search page
  static/fonts/          Press Start 2P + VT323 (self-hosted WOFF2, OFL)
```

**How the console works without JS:** each cartridge is a `<label>` for a hidden
radio button. `index.html` generates one CSS rule per slot,
`.deck:has(#cart-3:checked) [data-slot="3"] { --on: 1; --show: block; --vis: visible }`.
Everything else reads those custom properties. The old cart ejects, the new one
drops in after a short delay, and the screen preview replays its power-on
animation because it switches from `display: none` to visible. Keyboard users can
tab to the console and use the arrow keys (native radio behaviour). Motion is
turned off for `prefers-reduced-motion`.

**Icons:** the bundled fonts don't include ▶ ◀ ▼ ↩ ★ 🔍, so don't type those
characters in templates. Use `{{ m.icon('right') }}` (also `'left'`, `'down'`, `'return'`,
`'star'`, `'search'`). It outputs a pixel-art SVG sized to one Press Start 2P character cell
and coloured with `currentColor`. The arrows are traced from the font itself; the others
are drawn on the same 8×8 grid. Set `--px-icon` to resize next to other fonts (the CRT
uses `.64em` to match VT323). In CSS pseudo-elements, use the `--px-right` / `--px-left` /
`--px-down` / `--px-star` masks from `base.css`, as `.section-title::before` does. To add an
icon, add its path to `PX_ICONS` in `partials/macros.html` (one `M x y h w v1 H x z` run per row).

**Colours:** the theme uses the [Gruvbox Material](https://github.com/sainnhe/gruvbox-material)
palette (dark, medium background, "material" foreground) and is always dark. The raw palette is
defined once as `--gb-*` variables at the top of `base.css`. Everything else uses semantic
tokens built from it (`--bg`, `--ink`, `--link`, `--plastic*`, `--accent`, `--phosphor`, …), so
change those to restyle. Cartridge colours in posts (`Cart_color`) and the fallback label
colours (`CART_PALETTE` in `partials/macros.html`) use the same palette.
