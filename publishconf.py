"""Production settings, used by `make publish` and the GitHub Actions deploy."""

import os
import sys

sys.path.append(os.curdir)
from pelicanconf import *  # noqa: E402,F401,F403

# Set this to your real URL, e.g. "https://your-username.github.io" or
# "https://www.example.com" once a custom domain is configured.
# The deploy workflow can also override it with the SITEURL env variable.
SITEURL = os.environ.get("SITEURL", "https://your-username.github.io")
RELATIVE_URLS = False

FEED_ALL_ATOM = "feeds/all.atom.xml"
CATEGORY_FEED_ATOM = "feeds/{slug}.atom.xml"

DELETE_OUTPUT_DIRECTORY = True
