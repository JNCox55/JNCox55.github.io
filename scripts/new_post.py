#!/usr/bin/env python3
"""Scaffold a new blog post.

    python scripts/new_post.py "My New Post" [--tags a,b] [--category Games]

Creates content/articles/YYYY-MM-DD-my-new-post.md with front matter filled in.
"""

import argparse
import datetime as dt
import re
import sys
import unicodedata
from pathlib import Path

ARTICLES = Path(__file__).resolve().parent.parent / "content" / "articles"


def slugify(text: str) -> str:
    text = unicodedata.normalize("NFKD", text).encode("ascii", "ignore").decode()
    return re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-")[:80].strip("-")


def one_line(text: str) -> str:
    """Collapse newlines/control characters so a value can't add extra front-matter lines."""
    return " ".join("".join(c if c.isprintable() else " " for c in text).split())


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("title")
    ap.add_argument("--tags", default="", help="comma separated, e.g. rpg,snes")
    ap.add_argument("--category", default="Games")
    args = ap.parse_args()

    title, tags, category = one_line(args.title), one_line(args.tags), one_line(args.category)
    if not title:
        print("Title can't be empty.", file=sys.stderr)
        return 1

    now = dt.datetime.now()
    slug = slugify(title) or f"post-{now:%H%M%S}"
    path = ARTICLES / f"{now:%Y-%m-%d}-{slug}.md"

    text = f"""Title: {title}
Date: {now:%Y-%m-%d %H:%M}
Slug: {slug}
Tags: {tags}
Category: {category}
Summary: One or two sentences. This is what shows up on the CRT screen.
Status: draft
Cover:
Cart_color:

Write your post here. Markdown works: **bold**, *italic*, [links](https://example.com),
lists, `code`, and fenced code blocks.

<!-- When you're ready to publish:
  - Remove the "Status: draft" line
  - Optional: set Cover to an image under content/images/covers/ (e.g. images/covers/{slug}.png)
  - Optional: set Cart_color to any CSS color, e.g. #ea6962
  - Delete any front-matter lines you leave empty -->
"""
    try:
        with path.open("x", encoding="utf-8") as fh:  # "x" = fail if it already exists
            fh.write(text)
    except FileExistsError:
        print(f"Already exists: {path}", file=sys.stderr)
        return 1
    print(f"Created {path.relative_to(ARTICLES.parent.parent)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
