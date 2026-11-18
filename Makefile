PY ?= .venv/bin/python
PELICAN ?= .venv/bin/pelican
PORT ?= 8000

.PHONY: help setup dev build publish new clean

help:
	@echo "make setup               create .venv and install requirements"
	@echo "make dev                 build + serve on http://localhost:$(PORT) with auto-reload"
	@echo "make build               one-off development build into output/"
	@echo "make publish             production build (absolute URLs, feeds)"
	@echo "make new title=\"...\"     scaffold a new post in content/articles/"
	@echo "make clean               remove output/"

setup:
	python3 -m venv .venv
	.venv/bin/pip install -r requirements.txt

dev:
	$(PELICAN) content -s pelicanconf.py --listen --autoreload --port $(PORT)

build:
	$(PELICAN) content -s pelicanconf.py

publish:
	$(PELICAN) content -s publishconf.py

# The title is passed through the environment ("$$title"), never pasted into
# the shell command, so quotes, $ and backticks in a title are just text.
export title
new:
	@test -n "$$title" || (echo 'usage: make new title="My Post"' && exit 1)
	$(PY) scripts/new_post.py "$$title"

clean:
	rm -rf output
