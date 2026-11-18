/* Tiny client-side search over /search.json (built by Pelican).
   Supports ?q=words and ?tag=name. All terms must match (title, summary,
   tags, or category). */
(() => {
  const me = document.currentScript;
  const root = me.dataset.root;
  const form = document.querySelector(".search-form");
  const input = document.getElementById("q");
  const out = document.getElementById("search-results");
  const status = document.getElementById("search-status");
  let posts = [];

  // Results are built with DOM nodes and textContent only (no innerHTML),
  // so nothing from the URL or the index is ever parsed as HTML.
  const el = (tag, attrs = {}, ...kids) => {
    const n = document.createElement(tag);
    for (const [k, v] of Object.entries(attrs)) n.setAttribute(k, v);
    n.append(...kids);
    return n;
  };

  // Highlight terms by finding match ranges in the plain text, then wrapping
  // those ranges in <mark> elements.
  const mark = (text, terms) => {
    const lower = text.toLowerCase();
    const hit = new Array(text.length).fill(false);
    for (const t of terms) {
      for (let i = lower.indexOf(t); i !== -1; i = lower.indexOf(t, i + t.length)) {
        hit.fill(true, i, i + t.length);
      }
    }
    const frag = document.createDocumentFragment();
    let i = 0;
    while (i < text.length) {
      let j = i;
      while (j < text.length && hit[j] === hit[i]) j++;
      const chunk = text.slice(i, j);
      frag.append(hit[i] ? el("mark", {}, chunk) : chunk);
      i = j;
    }
    return frag;
  };

  const render = (raw) => {
    const query = raw.trim().toLowerCase();
    const tagMatch = query.match(/^#(\S+)$/);
    const terms = tagMatch ? [] : query.split(/\s+/).filter(Boolean);
    if (!query) { out.replaceChildren(); status.textContent = `${posts.length} posts loaded. Start typing…`; return; }

    const hits = posts.filter((p) => {
      if (tagMatch) return p.tags.some((t) => t.toLowerCase() === tagMatch[1]);
      const hay = [p.title, p.summary, p.category, ...p.tags].join(" ").toLowerCase();
      return terms.every((t) => hay.includes(t));
    });

    status.textContent = hits.length ? `${hits.length} result${hits.length === 1 ? "" : "s"}` : "No match. Try another password!";
    out.replaceChildren(...hits.map((p) => el("li", { class: "spine" },
      el("a", { class: "spine-link", href: root + p.url },
        el("span", { class: "spine-title" }, mark(p.title, terms)),
        el("time", { datetime: p.date }, p.date)),
      el("p", { class: "spine-summary" }, mark(p.summary, terms)),
      el("ul", { class: "tag-chips tag-chips--small" },
        ...p.tags.map((t) => el("li", {}, el("a", { href: "?tag=" + encodeURIComponent(t) }, "#" + t))))
    )));
  };

  const sync = (value) => {
    const url = new URL(location.href);
    url.search = "";
    const tag = value.trim().match(/^#(\S+)$/);
    if (tag) url.searchParams.set("tag", tag[1]);
    else if (value.trim()) url.searchParams.set("q", value.trim());
    history.replaceState(null, "", url);
  };

  const params = new URLSearchParams(location.search);
  input.value = params.get("tag") ? "#" + params.get("tag") : params.get("q") || "";

  fetch(me.dataset.index)
    .then((r) => r.json())
    .then((data) => { posts = data; render(input.value); })
    .catch(() => { status.textContent = "Couldn't load the search index."; });

  input.addEventListener("input", () => { render(input.value); sync(input.value); });
  form.addEventListener("submit", (e) => { e.preventDefault(); render(input.value); sync(input.value); });
  if (!input.value) input.focus();
})();
