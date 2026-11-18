"""Development settings for the site. Production overrides live in publishconf.py."""

import logging
import re
from pathlib import Path

import yaml

ROOT = Path(__file__).parent

# --- Site identity ----------------------------------------------------------
AUTHOR = "Justin Cox"
SITENAME = "Justin's Online Space"
SITE_TAGLINE = "Can we just go back to the 90's? Please?"
SITEURL = "https://JNCox55.github.io"

TIMEZONE = "America/New_York"
DEFAULT_LANG = "en"
DEFAULT_DATE_FORMAT = "%b %d, %Y"

# --- Content ----------------------------------------------------------------
PATH = "content"
ARTICLE_PATHS = ["articles"]
PAGE_PATHS = ["pages"]
STATIC_PATHS = ["images", "extra"]
EXTRA_PATH_METADATA = {
    "extra/.nojekyll": {"path": ".nojekyll"},
    # Uncomment once you own a custom domain (see INSTALL.md):
    # "extra/CNAME": {"path": "CNAME"},
}
# Never treat the example CNAME as content.
IGNORE_FILES = [".#*", "CNAME.example"]

THEME = "themes/cartridge"

# --- Template safety -------------------------------------------------------------
# Escape every {{ value }} by default, so quotes or < > & in titles, tags, summaries
# or rankings.yaml can't break the HTML. Rendered post/page bodies are the only
# things marked |safe in the templates.
JINJA_ENVIRONMENT = {"autoescape": True}

_CSS_COLOR = re.compile(
    r"#(?:[0-9a-fA-F]{3,4}|[0-9a-fA-F]{6}|[0-9a-fA-F]{8})"
    r"|[a-zA-Z]{3,20}"
    r"|(?:rgba?|hsla?|hwb|lab|lch|oklab|oklch)\([0-9a-zA-Z.,%/\s+-]*\)"
)


def css_color(value, default="#928374"):
    """Return `value` if it's a plain CSS colour, else `default` (with a build warning).

    Used for the Cart_color front-matter field, which ends up in a style attribute.
    """
    value = str(value or "").strip()
    if not value:
        return default
    if _CSS_COLOR.fullmatch(value) and "url" not in value.lower():
        return value
    logging.getLogger("pelican").warning("Ignoring invalid Cart_color %r; using %s", value, default)
    return default


JINJA_FILTERS = {"css_color": css_color}

# Content-Security-Policy, sent as a <meta> tag (GitHub Pages can't set headers).
# Scripts may only come from this site, so injected HTML can't run JavaScript.
# Inline styles are allowed because the console's CSS-only state uses them.
# Embedding videos later? Add e.g. "frame-src https://www.youtube-nocookie.com".
# Set to "" to disable.
CONTENT_SECURITY_POLICY = "; ".join([
    "default-src 'self'",
    "script-src 'self'",
    "style-src 'self' 'unsafe-inline'",
    "img-src 'self' data:",
    "font-src 'self'",
    "connect-src 'self'",
    "object-src 'none'",
    "base-uri 'self'",
    "form-action 'self'",
])

# --- URLs (clean, folder-style) ----------------------------------------------
ARTICLE_URL = "posts/{slug}/"
ARTICLE_SAVE_AS = "posts/{slug}/index.html"
PAGE_URL = "{slug}/"
PAGE_SAVE_AS = "{slug}/index.html"
TAG_URL = "tag/{slug}/"
TAG_SAVE_AS = "tag/{slug}/index.html"
TAGS_URL = "tags/"
TAGS_SAVE_AS = "tags/index.html"
CATEGORY_URL = "category/{slug}/"
CATEGORY_SAVE_AS = "category/{slug}/index.html"
CATEGORIES_URL = "categories/"
CATEGORIES_SAVE_AS = "categories/index.html"
ARCHIVES_URL = "archives/"
ARCHIVES_SAVE_AS = "archives/index.html"
AUTHOR_SAVE_AS = ""
AUTHORS_SAVE_AS = ""

# "search_index" renders templates/search_index.html into /search.json
DIRECT_TEMPLATES = ["index", "tags", "categories", "archives", "search_index"]
SEARCH_INDEX_SAVE_AS = "search.json"

SUMMARY_MAX_LENGTH = 40

# --- Theme options ------------------------------------------------------------
CONSOLE_SLOTS = 8  # how many recent posts load into the console on the home page
LIBRARY_PAGE_SIZE = 20  # posts per page in the home page's Game Library list

# Only the home page is paginated, and only the Game Library list changes from
# page to page (the console always shows the newest posts). Tag, category and
# archive pages list everything. URLs: /, /page/2/, /page/3/, …
DEFAULT_PAGINATION = False
DEFAULT_ORPHANS = 0
PAGINATED_TEMPLATES = {"index": LIBRARY_PAGE_SIZE}
PAGINATION_PATTERNS = (
    (1, "{base_name}/", "{base_name}/index.html"),
    (2, "{base_name}/page/{number}/", "{base_name}/page/{number}/index.html"),
)
MENU_PAGES = ["game-rankings", "about"]  # page slugs shown in the top nav
SOCIAL = [
    ("GitHub", "https://github.com/JNCox55"),
]

# --- Data files ----------------------------------------------------------------
with open(ROOT / "data" / "rankings.yaml", encoding="utf-8") as fh:
    GAME_RANKINGS = yaml.safe_load(fh)

# --- Markdown ------------------------------------------------------------------
MARKDOWN = {
    "extension_configs": {
        "markdown.extensions.codehilite": {"css_class": "highlight"},
        "markdown.extensions.extra": {},
        "markdown.extensions.meta": {},
        "markdown.extensions.toc": {},
    },
    "output_format": "html5",
}

# No feeds while developing.
FEED_ALL_ATOM = None
CATEGORY_FEED_ATOM = None
TRANSLATION_FEED_ATOM = None
AUTHOR_FEED_ATOM = None
AUTHOR_FEED_RSS = None

RELATIVE_URLS = True
