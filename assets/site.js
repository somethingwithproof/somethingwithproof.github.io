// Progressive enhancements. Every page works without this file.
// Index entries and page text are treated as untrusted: only textContent.

const sameOrigin = (u) => {
  try { return new URL(u, location.origin).origin === location.origin; } catch { return false; }
};

function initSearch() {
  const box = document.querySelector("[data-search]");
  if (!box) return;
  box.hidden = false;
  const input = box.querySelector("input");
  const list = box.querySelector(".results");
  let index = null;
  const load = async () => {
    if (!index) {
      const res = await fetch("/search.json");
      index = res.ok ? await res.json() : [];
    }
    return index;
  };

  const render = (hits, query) => {
    list.replaceChildren();
    if (!query) { list.hidden = true; return; }
    if (hits.length === 0) {
      const li = document.createElement("li");
      li.className = "empty";
      li.textContent = "No pages match.";
      list.append(li);
    }
    for (const h of hits.slice(0, 12)) {
      if (!sameOrigin(h.u)) continue;
      const li = document.createElement("li");
      const a = document.createElement("a");
      a.href = h.u;
      const title = document.createElement("b");
      title.textContent = h.t;
      const where = document.createElement("small");
      where.textContent = h.p || "Home";
      const desc = document.createElement("small");
      desc.textContent = h.d;
      a.append(title, where, desc);
      li.append(a);
      list.append(li);
    }
    list.hidden = false;
  };

  const search = async () => {
    const q = input.value.trim().toLowerCase();
    const terms = q.split(/\s+/).filter(Boolean);
    const scored = [];
    for (const item of await load()) {
      const title = item.t.toLowerCase();
      const hay = `${title} ${item.d} ${item.p}`.toLowerCase();
      if (!terms.every((t) => hay.includes(t))) continue;
      // Title matches first: people scan titles before descriptions.
      scored.push([terms.every((t) => title.includes(t)) ? 0 : 1, item]);
    }
    scored.sort((a, b) => a[0] - b[0]);
    render(scored.map((s) => s[1]), q);
  };

  input.addEventListener("focus", load, { once: true });
  input.addEventListener("input", search);
  input.addEventListener("keydown", (e) => {
    if (e.key === "Escape") { input.value = ""; render([], ""); }
    if (e.key === "ArrowDown") { list.querySelector("a")?.focus(); e.preventDefault(); }
  });
  list.addEventListener("keydown", (e) => {
    const links = [...list.querySelectorAll("a")];
    const i = links.indexOf(document.activeElement);
    if (e.key === "ArrowDown" && i < links.length - 1) { links[i + 1].focus(); e.preventDefault(); }
    if (e.key === "ArrowUp") { (i > 0 ? links[i - 1] : input).focus(); e.preventDefault(); }
    if (e.key === "Escape") { input.focus(); render([], ""); }
  });
  document.addEventListener("keydown", (e) => {
    const typing = e.target.closest("input, textarea, select, [contenteditable]");
    if (e.key === "/" && !typing) { input.focus(); e.preventDefault(); }
  });
  document.addEventListener("click", (e) => { if (!box.contains(e.target)) list.hidden = true; });
}

function initFilters() {
  const chips = [...document.querySelectorAll("[data-filter]")];
  if (chips.length === 0) return;
  const cards = [...document.querySelectorAll(".cards .card")];
  const status = document.querySelector("[data-filter-status]");
  for (const chip of chips) {
    chip.addEventListener("click", () => {
      const f = chip.dataset.filter;
      for (const c of chips) c.setAttribute("aria-pressed", String(c === chip));
      let shown = 0;
      for (const card of cards) {
        card.hidden = f !== "all" && card.dataset.section !== f;
        if (!card.hidden) shown += 1;
      }
      if (status) status.textContent = `${shown} projects shown`;
    });
  }
}

function initCopy() {
  for (const pre of document.querySelectorAll(".prose pre:not(.mermaid)")) {
    const btn = document.createElement("button");
    btn.type = "button";
    btn.className = "copy";
    btn.textContent = "Copy";
    btn.addEventListener("click", async () => {
      try {
        await navigator.clipboard.writeText(pre.querySelector("code")?.innerText ?? pre.innerText);
        btn.textContent = "Copied";
      } catch {
        btn.textContent = "Press Cmd+C";
      }
      setTimeout(() => { btn.textContent = "Copy"; }, 1600);
    });
    pre.append(btn);
  }
}

function initToc() {
  const links = [...document.querySelectorAll(".toc a")];
  if (links.length === 0 || !("IntersectionObserver" in window)) return;
  const byId = new Map(links.map((a) => [decodeURIComponent(a.hash.slice(1)), a]));
  const visible = new Set();
  const update = () => {
    const first = [...byId.keys()].find((id) => visible.has(id));
    if (!first) return;
    for (const a of links) a.removeAttribute("aria-current");
    byId.get(first).setAttribute("aria-current", "true");
  };
  const obs = new IntersectionObserver((entries) => {
    for (const e of entries) (e.isIntersecting ? visible.add : visible.delete).call(visible, e.target.id);
    update();
  }, { rootMargin: "-64px 0px -60% 0px" });
  for (const id of byId.keys()) {
    const el = document.getElementById(id);
    if (el) obs.observe(el);
  }
}

function initSidebar() {
  // The docs menu ships open so it works without JS; fold it on narrow screens.
  const side = document.querySelector("[data-side]");
  if (side && matchMedia("(max-width: 61.99rem)").matches) side.open = false;
}

function initDiagrams() {
  const blocks = [...document.querySelectorAll("pre.mermaid")];
  if (blocks.length === 0) return;
  // Keep each diagram's source so a theme change can render it again.
  const sources = new Map(blocks.map((el) => [el, el.textContent]));
  const root = document.documentElement;
  const dark = () => (root.dataset.theme || (matchMedia("(prefers-color-scheme: dark)").matches ? "dark" : "light")) === "dark";
  let ready = null;
  const load = () => ready ??= new Promise((resolve, reject) => {
    const s = document.createElement("script");
    s.src = "/assets/vendor/mermaid.min.js";
    s.onload = () => resolve(window.mermaid);
    s.onerror = reject;
    document.head.append(s);
  });
  const render = async () => {
    const mermaid = await load();
    mermaid.initialize({ startOnLoad: false, securityLevel: "strict", theme: dark() ? "dark" : "default",
      fontFamily: getComputedStyle(document.body).fontFamily });
    for (const [el, src] of sources) {
      delete el.dataset.processed;
      el.textContent = src;
    }
    // A diagram that fails to parse stays visible as source instead of an error graphic.
    const ok = await Promise.all(blocks.map((el) => mermaid.parse(sources.get(el), { suppressErrors: true })));
    const valid = blocks.filter((_, i) => ok[i]);
    if (valid.length) await mermaid.run({ nodes: valid, suppressErrors: true });
  };
  // If Mermaid cannot load, every diagram stays readable as source.
  const draw = () => { render().catch(() => {}); };
  draw();
  document.addEventListener("themechange", draw);
  matchMedia("(prefers-color-scheme: dark)").addEventListener("change", () => { if (!root.dataset.theme) draw(); });
}

initSearch();
initDiagrams();
initFilters();
initCopy();
initToc();
initSidebar();
