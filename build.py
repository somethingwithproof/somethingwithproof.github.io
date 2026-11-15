#!/usr/bin/env python3
"""Build the static site into _site/.

    python3 build.py --fetch   # refresh repo metadata and READMEs via gh
    python3 build.py           # build from cache/
"""

from __future__ import annotations

import argparse
import html
import json
import math
import re
import shutil
import subprocess
import sys
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timezone
from html.parser import HTMLParser
from pathlib import Path
import urllib.request
from urllib.parse import urljoin, urlsplit

ROOT = Path(__file__).resolve().parent
CONTENT = ROOT / "content"
CACHE = ROOT / "cache"
OUT = ROOT / "_site"

# ---------------------------------------------------------------- colour
# Material 3 assigns colour roles by tone, where tone is CIELAB L*. Contrast
# depends only on luminance, so a tone gap of 50 guarantees >= 4.5:1 whatever
# the hue. Hue is held in CIELAB LCh here instead of CAM16; that changes how
# hues look at a given chroma, not the contrast guarantee.

def _lin(c: float) -> float:
    return c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4


def _gam(c: float) -> float:
    return 12.92 * c if c <= 0.0031308 else 1.055 * c ** (1 / 2.4) - 0.055


_WHITE = (0.95047, 1.0, 1.08883)


def _lab_f(t: float) -> float:
    return t ** (1 / 3) if t > 216 / 24389 else (24389 / 27 * t + 16) / 116


def _lab_finv(t: float) -> float:
    return t ** 3 if t ** 3 > 216 / 24389 else (116 * t - 16) / (24389 / 27)


def hex_to_lch(hx: str) -> tuple[float, float, float]:
    r, g, b = (_lin(int(hx[i:i + 2], 16) / 255) for i in (1, 3, 5))
    x = 0.4124 * r + 0.3576 * g + 0.1805 * b
    y = 0.2126 * r + 0.7152 * g + 0.0722 * b
    z = 0.0193 * r + 0.1192 * g + 0.9505 * b
    fx, fy, fz = (_lab_f(v / w) for v, w in zip((x, y, z), _WHITE))
    lightness, a, bb = 116 * fy - 16, 500 * (fx - fy), 200 * (fy - fz)
    return lightness, math.hypot(a, bb), math.degrees(math.atan2(bb, a)) % 360


def _lch_to_rgb(lightness: float, chroma: float, hue: float):
    a = chroma * math.cos(math.radians(hue))
    b = chroma * math.sin(math.radians(hue))
    fy = (lightness + 16) / 116
    x, y, z = (_lab_finv(f) * w for f, w in zip((fy + a / 500, fy, fy - b / 200), _WHITE))
    r = 3.2406 * x - 1.5372 * y - 0.4986 * z
    g = -0.9689 * x + 1.8758 * y + 0.0415 * z
    bl = 0.0557 * x - 0.2040 * y + 1.0570 * z
    return r, g, bl


def tone(hue: float, chroma: float, t: float) -> str:
    """Most chromatic in-gamut sRGB colour at L* = t, up to `chroma`."""
    lo, hi = 0.0, chroma
    for _ in range(30):
        mid = (lo + hi) / 2
        if all(-1e-6 <= c <= 1 + 1e-6 for c in _lch_to_rgb(t, mid, hue)):
            lo = mid
        else:
            hi = mid
    rgb = _lch_to_rgb(t, lo, hue)
    return "#" + "".join(f"{round(min(1, max(0, _gam(min(1, max(0, c))))) * 255):02x}" for c in rgb)


def contrast(a: str, b: str) -> float:
    def lum(hx):
        r, g, bl = (_lin(int(hx[i:i + 2], 16) / 255) for i in (1, 3, 5))
        return 0.2126 * r + 0.7152 * g + 0.0722 * bl
    la, lb = sorted((lum(a), lum(b)), reverse=True)
    return (la + 0.05) / (lb + 0.05)


SEED = "#2f6bff"  # bright blue accent
NEUTRAL_HUE = 265  # cool slate greys
# One hue per section for project tiles, spaced around the LCh wheel.
SECTION_HUES = [280, 200, 140, 75, 35, 330]


def build_tokens() -> str:
    _, seed_c, seed_h = hex_to_lch(SEED)
    pal = {
        "p": (seed_h, max(seed_c, 70)),
        "n": (NEUTRAL_HUE, 6),
        "nv": (NEUTRAL_HUE, 11),
        "ok": (190, 32),   # status: teal, far from the indigo hue
        "warn": (75, 40),  # status: amber
    }
    for i, h in enumerate(SECTION_HUES):
        pal[f"s{i}"] = (h, 40)
    t = lambda k, v: tone(*pal[k], v)  # noqa: E731
    roles = {
        "light": {
            "bg": t("n", 100), "surface": t("n", 97), "surface-2": t("n", 94),
            "text": t("n", 12), "text-2": t("nv", 35), "line": t("nv", 90), "line-strong": t("nv", 70),
            "accent": t("p", 40), "on-accent": t("p", 100),
            "accent-container": t("p", 94), "on-accent-container": t("p", 25),
            "ok-container": t("ok", 92), "on-ok-container": t("ok", 22),
            "warn-container": t("warn", 92), "on-warn-container": t("warn", 25),
            "code-bg": t("n", 15), "code-text": t("n", 92),
        },
        "dark": {
            "bg": t("n", 8), "surface": t("n", 13), "surface-2": t("n", 18),
            "text": t("n", 95), "text-2": t("nv", 76), "line": t("nv", 24), "line-strong": t("nv", 42),
            "accent": t("p", 80), "on-accent": t("p", 20),
            "accent-container": t("p", 22), "on-accent-container": t("p", 90),
            "ok-container": t("ok", 22), "on-ok-container": t("ok", 90),
            "warn-container": t("warn", 22), "on-warn-container": t("warn", 90),
            "code-bg": t("n", 4), "code-text": t("n", 92),
        },
    }
    for i in range(len(SECTION_HUES)):
        roles["light"][f"tile-{i}"], roles["light"][f"on-tile-{i}"] = t(f"s{i}", 90), t(f"s{i}", 25)
        roles["dark"][f"tile-{i}"], roles["dark"][f"on-tile-{i}"] = t(f"s{i}", 28), t(f"s{i}", 90)
    pairs = [("text", "bg"), ("text-2", "bg"), ("text-2", "surface"), ("accent", "bg"), ("accent", "surface"),
             ("on-accent", "accent"), ("on-accent-container", "accent-container"),
             ("on-ok-container", "ok-container"), ("on-warn-container", "warn-container"),
             ("code-text", "code-bg")] + [(f"on-tile-{i}", f"tile-{i}") for i in range(len(SECTION_HUES))]
    report = []
    for mode, r in roles.items():
        for fg, bg in pairs:
            ratio = contrast(r[fg], r[bg])
            report.append(f"  {mode:5} {fg:>20} on {bg:<17} {ratio:5.2f}:1")
            if ratio < 4.5:
                sys.exit(f"contrast below 4.5:1 for {mode} {fg} on {bg}: {ratio:.2f}")
    print(f"contrast checks: {len(report)} pairs, all >= 4.5:1, lowest "
          f"{min(contrast(r[f], r[b]) for r in roles.values() for f, b in pairs):.2f}:1")

    def block(r):
        return "".join(f"  --{k}: {v};\n" for k, v in r.items())
    return (
        "/* Generated by build.py from seed " + SEED + ". Do not edit. */\n"
        ":root {\n  color-scheme: light;\n" + block(roles["light"]) + "}\n"
        "@media (prefers-color-scheme: dark) {\n  :root:not([data-theme=\"light\"]) {\n  color-scheme: dark;\n"
        + block(roles["dark"]) + "  }\n}\n"
        ":root[data-theme=\"dark\"] {\n  color-scheme: dark;\n" + block(roles["dark"]) + "}\n"
    )


# ---------------------------------------------------------------- fetch

def gh(*args: str) -> str:
    return subprocess.run(["gh", *args], check=True, capture_output=True, text=True).stdout


def fetch_repo(owner: str, repo: str) -> str:
    meta = json.loads(gh("api", f"repos/{owner}/{repo}"))
    keep = {k: meta.get(k) for k in ("name", "description", "language", "html_url", "private", "archived",
                                      "fork", "pushed_at", "default_branch", "topics", "stargazers_count")}
    keep["license"] = (meta.get("license") or {}).get("spdx_id")
    keep.update({k: meta.get(k) for k in ("created_at", "homepage", "open_issues_count")})
    parent = meta.get("parent") or {}
    keep["parent"] = {"full_name": parent.get("full_name"), "html_url": parent.get("html_url"),
                      "description": parent.get("description")} if parent else None

    meta_file, readme_file = CACHE / f"{repo}.json", CACHE / f"{repo}.html"
    prev = json.loads(meta_file.read_text()) if meta_file.exists() else {}

    def optional(key: str, shape, *args: str):
        """Fetch one optional resource. 404 (none exists) and 409 (empty repository)
        mean absent; any other failure keeps the cached value or stops the build,
        so a transient error never erases data from a published page."""
        try:
            raw = gh("api", *args)
        except subprocess.CalledProcessError as e:
            if re.search(r"HTTP 40[49]\b", e.stderr or ""):
                return shape(None)
            if key in prev:
                print(f"warning: {repo} {key}: request failed, keeping cached value: {(e.stderr or '').strip()}")
                return prev[key]
            raise RuntimeError(f"{repo} {key}: {(e.stderr or '').strip()}") from e
        return shape(raw)

    def release(raw):
        # releases/latest skips pre-releases, so take the newest published release
        # from the list instead. Drafts are not public and are never shown.
        rels = [r for r in (json.loads(raw) if raw else []) if not r.get("draft") and r.get("published_at")]
        if not rels:
            return None
        rel = max(rels, key=lambda r: r["published_at"])
        return {"tag": rel["tag_name"], "url": rel["html_url"], "date": rel["published_at"],
                "prerelease": bool(rel.get("prerelease"))}

    def doc_list(raw):
        docs = json.loads(raw) if raw else None
        if not isinstance(docs, list):
            return []
        return sorted(({"name": d["name"], "url": d["html_url"]} for d in docs
                       if isinstance(d, dict) and d.get("type") == "file" and d["name"].lower().endswith(".md")),
                      key=lambda d: d["name"].lower())

    def commit_list(raw):
        return [{"msg": c["commit"]["message"].split("\n", 1)[0][:140], "date": c["commit"]["committer"]["date"],
                 "url": c["html_url"]} for c in (json.loads(raw) if raw else [])]

    keep["release"] = optional("release", release, f"repos/{owner}/{repo}/releases?per_page=20")
    keep["docs"] = optional("docs", doc_list, f"repos/{owner}/{repo}/contents/docs")
    # A fork's default branch mostly carries upstream history, so its commits say nothing about this work.
    keep["commits"] = [] if meta.get("fork") else optional("commits", commit_list, f"repos/{owner}/{repo}/commits?per_page=5")
    if readme_file.exists():
        prev["readme"] = readme_file.read_text()
    readme = optional("readme", lambda raw: raw or "",
                      "-H", "Accept: application/vnd.github.html+json", f"repos/{owner}/{repo}/readme")
    meta_file.write_text(json.dumps(keep, indent=1))
    readme_file.write_text(readme)
    return f"{repo}: {'PRIVATE ' if keep['private'] else ''}{len(readme)} bytes"


class _Calendar(HTMLParser):
    def __init__(self):
        super().__init__()
        self.days: list[dict] = []

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if tag == "td" and "ContributionCalendar-day" in (a.get("class") or "") and a.get("data-date"):
            m = re.match(r"contribution-day-component-(\d+)-(\d+)", a.get("id") or "")
            if m:
                self.days.append({"date": a["data-date"], "level": int(a.get("data-level") or 0),
                                  "row": int(m[1]), "week": int(m[2])})


def fetch_contributions(owner: str) -> None:
    # The public profile calendar, unauthenticated, is exactly what any visitor
    # sees. The authenticated API can include private activity, so it is not used.
    req = urllib.request.Request(f"https://github.com/users/{owner}/contributions",
                                 headers={"User-Agent": "static-site-build"})
    with urllib.request.urlopen(req, timeout=30) as res:
        page = res.read().decode()
    cal = _Calendar()
    cal.feed(page)
    total = re.search(r"([\d,]+)\s+contributions?\s+in the last year", page)
    (CACHE / "_contributions.json").write_text(json.dumps(
        {"total": total[1] if total else None, "days": cal.days}))
    print(f"fetched contributions: {len(cal.days)} days")


def fetch_all(site: dict) -> None:
    CACHE.mkdir(exist_ok=True)
    user = json.loads(gh("api", f"users/{site['owner']}"))
    (CACHE / "_user.json").write_text(json.dumps(
        {k: user.get(k) for k in ("login", "avatar_url", "html_url", "created_at", "public_repos")}))
    fetch_contributions(site["owner"])
    repos = [p["repo"] for s in site["sections"] for t in s["topics"] for p in t["pages"] if "repo" in p]
    with ThreadPoolExecutor(max_workers=8) as pool:
        for line in pool.map(lambda r: fetch_repo(site["owner"], r), repos):
            print("fetched", line)
    docs = [p for s in site["sections"] for t in s["topics"] for p in t["pages"] if "doc" in p]
    with ThreadPoolExecutor(max_workers=8) as pool:
        for line in pool.map(lambda p: fetch_doc(site["owner"], p["doc"], p["path"]), docs):
            print("fetched", line)


def doc_cache(repo: str, path: str) -> Path:
    return CACHE / f"{repo}--{path.replace('/', '--')}.html"


def fetch_doc(owner: str, repo: str, path: str) -> str:
    # A listed document is required content: unlike optional repo data, a 404
    # here means the sitemap is out of date, so the build stops either way
    # unless a cached copy exists for a transient failure.
    out = doc_cache(repo, path)
    try:
        raw = gh("api", "-H", "Accept: application/vnd.github.html+json", f"repos/{owner}/{repo}/contents/{path}")
    except subprocess.CalledProcessError as e:
        if out.exists() and not re.search(r"HTTP 404\b", e.stderr or ""):
            print(f"warning: {repo}/{path}: request failed, keeping cached copy")
            return f"{repo}/{path}: cached"
        raise RuntimeError(f"{repo}/{path}: {(e.stderr or '').strip()}") from e
    out.write_text(raw)
    return f"{repo}/{path}: {len(raw)} bytes"


# ---------------------------------------------------------------- Mermaid
# Served from this site so visitors never load a third-party script. The build
# downloads one pinned npm release and refuses it unless the registry's sha512 matches.
MERMAID_VERSION = "12.2.0"
MERMAID_TARBALL = f"https://registry.npmjs.org/mermaid/-/mermaid-{MERMAID_VERSION}.tgz"
MERMAID_INTEGRITY = "sha512-w7nr/SFrLO7BaVTs3dQTvYSV6nYSBj0Yy9DjBhsIJtAcHqRzXSq4Pg32ujHZ/AdWsAMNEvvhbm5dt9E2tOiHzw=="
MERMAID_JS = CACHE / f"mermaid-{MERMAID_VERSION}.min.js"
MERMAID_LICENSE = CACHE / f"mermaid-{MERMAID_VERSION}.LICENSE"


def vendor_mermaid() -> None:
    """Ensure MERMAID_JS and MERMAID_LICENSE are in the cache, downloading them if needed."""
    if MERMAID_JS.exists() and MERMAID_LICENSE.exists():
        return
    import base64, hashlib, io, tarfile
    req = urllib.request.Request(MERMAID_TARBALL, headers={"User-Agent": "static-site-build"})
    with urllib.request.urlopen(req, timeout=60) as res:
        blob = res.read()
    got = "sha512-" + base64.b64encode(hashlib.sha512(blob).digest()).decode()
    if got != MERMAID_INTEGRITY:
        sys.exit(f"mermaid {MERMAID_VERSION}: integrity mismatch, refusing to use it")
    CACHE.mkdir(exist_ok=True)
    with tarfile.open(fileobj=io.BytesIO(blob), mode="r:gz") as tar:
        # Read the two members by name; nothing is extracted to a path from the archive.
        for member, dest in (("package/dist/mermaid.min.js", MERMAID_JS), ("package/LICENSE", MERMAID_LICENSE)):
            data = tar.extractfile(member)
            if data is None:
                sys.exit(f"mermaid {MERMAID_VERSION}: {member} missing from tarball")
            dest.write_bytes(data.read())
    print(f"vendored mermaid {MERMAID_VERSION}")


# ---------------------------------------------------------------- README sanitizer
# README HTML comes from the GitHub API, which sanitizes it, but it is still
# third-party markup entering our pages, so it passes an allowlist here and
# nothing else reaches the output.

ALLOWED = {"p", "h1", "h2", "h3", "h4", "h5", "h6", "a", "ul", "ol", "li", "code", "pre", "blockquote",
           "em", "strong", "b", "i", "table", "thead", "tbody", "tr", "th", "td", "img", "br", "hr",
           "del", "sup", "sub", "dl", "dt", "dd", "details", "summary", "kbd"}
# Void elements never get an end tag, so they must not change the drop depth.
VOID = {"area", "base", "br", "col", "embed", "hr", "img", "input", "link", "meta", "source", "track", "wbr"}
DROP_WITH_CONTENT = {"script", "style", "svg", "iframe", "object", "embed", "template", "noscript", "math", "form"}
ATTRS = {"a": {"href"}, "img": {"src", "alt", "width", "height"}, "th": {"align"}, "td": {"align"}, "ol": {"start"}}


def slugify(text: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-") or "section"


class Sanitizer(HTMLParser):
    def __init__(self, blob_base: str, raw_base: str):
        super().__init__(convert_charrefs=True)
        self.blob_base, self.raw_base = blob_base, raw_base
        self.out: list[str | None] = []
        self.stack: list[str] = []
        self.drop = 0
        self.skip_anchor = 0
        self.heading: list | None = None
        self.headings: list[tuple[int, str, str]] = []
        self.seen_h1 = False
        self.ids: set[str] = set()

    def _url(self, value: str, base: str) -> str | None:
        value = value.strip()
        if value.startswith("#"):
            return "#" + slugify(value[1:].removeprefix("user-content-"))
        scheme = urlsplit(value).scheme.lower()
        if scheme in ("http", "https", "mailto"):
            return value
        if scheme:
            return None  # javascript:, data:, vbscript: and anything else
        return urljoin(base, value)

    def handle_starttag(self, tag, attrs):
        if self.drop or tag in DROP_WITH_CONTENT:
            if tag not in VOID:
                self.drop += 1
            return
        a = dict(attrs)
        if tag == "a" and "anchor" in (a.get("class") or "").split():
            self.skip_anchor += 1
            return
        if tag not in ALLOWED:
            return
        if tag == "pre" and a.get("lang") == "mermaid":
            # Diagram source stays plain text; site.js renders it with Mermaid's strict security level.
            self.out.append('<pre class="mermaid">')
            self.stack.append("pre")
            return
        if tag == "h1":
            if not self.seen_h1:
                self.seen_h1 = True
                self.stack.append("h1-title")
                self.drop += 1
                return
            tag = "h2"
        if tag in {"h2", "h3"}:
            self.heading = [tag, []]
            self.out.append(None)  # placeholder, filled at end tag with the id
            self.stack.append(tag)
            return
        kept = []
        for name, value in attrs:
            if name not in ATTRS.get(tag, ()) or value is None:
                continue
            if name == "href":
                value = self._url(value, self.blob_base)
            elif name == "src":
                value = self._url(value, self.raw_base)
            if value is not None:
                kept.append(f' {name}="{html.escape(value, quote=True)}"')
        if tag == "img":
            kept.append(' loading="lazy"')
        self.out.append(f"<{tag}{''.join(kept)}>")
        if tag not in VOID:
            self.stack.append(tag)

    def handle_endtag(self, tag):
        if tag == "h1" and self.stack and self.stack[-1] == "h1-title":
            self.stack.pop()
            self.drop -= 1
            return
        if self.drop:
            if tag not in VOID:
                self.drop -= 1
            return
        if tag == "a" and self.skip_anchor:
            self.skip_anchor -= 1
            return
        if tag == "h1":
            tag = "h2"
        if tag not in self.stack:
            return
        while self.stack:
            top = self.stack.pop()
            if top in {"h2", "h3"} and self.heading:
                text = "".join(self.heading[1]).strip()
                hid = slugify(text)
                n = 2
                while hid in self.ids:
                    hid, n = f"{slugify(text)}-{n}", n + 1
                self.ids.add(hid)
                self.headings.append((int(top[1]), text, hid))
                idx = self.out.index(None)
                self.out[idx] = f'<{top} id="{hid}">'
                self.heading = None
            self.out.append(f"</{top}>")
            if top == tag:
                break

    def handle_data(self, data):
        if self.drop:
            return
        if self.heading is not None:
            self.heading[1].append(data)
        self.out.append(html.escape(data, quote=False))

    def result(self) -> str:
        while self.stack:
            top = self.stack.pop()
            if top not in {"h1-title"}:
                self.out.append(f"</{top}>")
        return "".join(x for x in self.out if x is not None)


GENERATED_IDS = {"gh-project-details", "gh-upstream", "gh-recent-changes", "gh-repo-docs"}


def sanitize_readme(raw: str, owner: str, repo: str, branch: str, subdir: str = "") -> tuple[str, list]:
    s = Sanitizer(f"https://github.com/{owner}/{repo}/blob/{branch}/{subdir}",
                  f"https://raw.githubusercontent.com/{owner}/{repo}/{branch}/{subdir}")
    # repo_details() appends headings with these IDs after the README, so the
    # README must not claim them; a clash would leave two TOC targets with one ID.
    s.ids.update(GENERATED_IDS)
    s.feed(raw)
    s.close()
    return s.result(), s.headings


# ---------------------------------------------------------------- model

def clean_desc(desc: str | None) -> str:
    return re.sub(r"^\[[a-z]+\]\s*", "", (desc or "").strip())


def status_of(meta: dict) -> tuple[str, str]:
    if meta.get("archived"):
        return "Archived", "muted"
    if meta.get("fork"):
        return "Fork", "muted"
    # A Cacti plugin without a release is still being built; saying "Code
    # available" would suggest something installable.
    if meta.get("name", "").startswith("plugin_"):
        rel = meta.get("release")
        if not rel:
            return "In development", "accent"
        if rel.get("prerelease"):
            return "Pre-release", "accent"
    return "Code available", "ok"


# (repository, file name) -> site URL, so project pages link to documents published here.
DOC_PAGES: dict[tuple[str, str], str] = {}


def load_model(site: dict) -> list[dict]:
    pages = []
    home = {"level": 1, "url": "/", "name": "Home", "crumbs": []}
    pages.append(home)
    for s in site["sections"]:
        s_url = f"/{s['slug']}/"
        sec = {"level": 2, "url": s_url, "name": s["name"], "summary": s["blurb"], "section": s,
               "crumbs": [("Home", "/")]}
        pages.append(sec)
        s["url"] = s_url
        for t in s["topics"]:
            t_url = f"{s_url}{t['slug']}/"
            t["url"] = t_url
            pages.append({"level": 3, "url": t_url, "name": t["name"], "summary": t["blurb"], "section": s,
                          "topic": t, "local": t.get("local"), "crumbs": [("Home", "/"), (s["name"], s_url)]})
            for p in t["pages"]:
                if "repo" in p:
                    meta = json.loads((CACHE / f"{p['repo']}.json").read_text())
                    if meta.get("private"):
                        sys.exit(f"{p['repo']} is private; remove it from content/sitemap.json")
                    summary = p.get("summary") or clean_desc(meta["description"]) or "[Description pending]"
                    p.update(name=meta["name"], summary=summary, kind=p.get("kind", "Reference"),
                             meta=meta, slug=p["repo"].lower())
                elif "doc" in p:
                    repo_meta = json.loads((CACHE / f"{p['doc']}.json").read_text())
                    if repo_meta.get("private"):
                        sys.exit(f"{p['doc']} is private; remove its documents from content/sitemap.json")
                    p.update(repo_meta=repo_meta, kind=p.get("kind", "Reference"),
                             slug=f"{p['doc']}-{Path(p['path']).stem}".lower().replace("_", "-"))
                    DOC_PAGES[(p["doc"], Path(p["path"]).name)] = f"{t_url}{p['slug']}/"
                else:
                    p["slug"] = p["local"]
                p["url"] = f"{t_url}{p['slug']}/"
                pages.append({"level": 4, "url": p["url"], "name": p["name"], "summary": p["summary"],
                              "section": s, "topic": t, "page": p,
                              "crumbs": [("Home", "/"), (s["name"], s_url), (t["name"], t_url)]})
    return pages


# ---------------------------------------------------------------- templates

E = html.escape
FONTS = ("https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700"
         "&amp;family=JetBrains+Mono:wght@400;500&amp;display=swap")


def fmt_date(iso: str | None) -> str:
    if not iso:
        return "unknown"
    d = datetime.fromisoformat(iso.replace("Z", "+00:00"))
    return f"{d.day} {d.strftime('%b %Y')}"


def badge(label: str, tone_: str) -> str:
    return f'<span class="badge badge-{tone_}">{E(label)}</span>'


def status_badge(meta: dict) -> str:
    label, tone_ = status_of(meta)
    return badge(label, {"accent": "warn"}.get(tone_, tone_))


def monogram(name: str) -> str:
    parts = [p for p in re.split(r"[-_.\s]+", re.sub(r"^(plugin|terraform|ansible|macos)[-_]", "", name)) if p]
    letters = (parts[0][0] + (parts[1][0] if len(parts) > 1 else parts[0][1:2])) if parts else name[:2]
    return E(letters.upper())


def header(site: dict, page: dict, docs: bool) -> str:
    cur = page.get("section")
    links = [("/", "Projects", page["level"] == 1),
             (site["sections"][0]["url"], "Docs", docs and cur is not site["sections"][-1]),
             ("/about/", "About", cur is site["sections"][-1]),
             (f"https://github.com/{site['owner']}", "GitHub", False)]
    nav = "".join(f'<a href="{u}"{" aria-current=\"true\"" if on else ""}>{n}</a>' for u, n, on in links)
    return f"""<header class="site-header">
  <div class="header-row">
    <a class="brand" href="/"><span class="brand-mark" aria-hidden="true">swp</span>{E(site["title"])}</a>
    <nav class="primary" aria-label="Main">{nav}</nav>
    <div class="tools">
      <div class="search" data-search hidden>
        <label for="q" class="vh">Search all pages</label>
        <input id="q" type="search" placeholder="Search docs" autocomplete="off" aria-controls="q-results">
        <kbd aria-hidden="true">/</kbd>
        <ul id="q-results" class="results" role="list" hidden></ul>
      </div>
      <button class="icon-btn" type="button" data-theme-toggle aria-label="Switch colour theme">
        <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true"><circle cx="12" cy="12" r="9"></circle><path d="M12 3a9 9 0 0 0 0 18z" fill="currentColor"></path></svg>
      </button>
    </div>
  </div>
</header>"""


def shell(site: dict, page: dict, body: str, built: str, docs: bool) -> str:
    title = site["title"] if page["level"] == 1 else f'{page["name"]} · {site["title"]}'
    desc = page.get("summary") or site["intro"]
    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{E(title)}</title>
<meta name="description" content="{E(desc)}">
<link rel="stylesheet" href="/assets/tokens.css">
<link rel="stylesheet" href="/assets/style.css">
<script src="/assets/theme.js"></script>
<script type="module" src="/assets/site.js"></script>
</head>
<body class="{"docs" if docs else "home"}">
<a class="skip" href="#main">Skip to content</a>
{header(site, page, docs)}
{body}
<footer class="site-footer">
  <div class="footer-row">
    <span>Built {E(built)} from public repositories on <a href="https://github.com/{site["owner"]}">GitHub</a>.</span>
    <span class="footer-links"><a href="/about/security/">Security</a><a href="/about/contributing/">Contributing</a><a href="/">All projects</a></span>
  </div>
</footer>
</body>
</html>
"""


def docs_sidebar(site: dict, page: dict) -> str:
    groups = []
    for s in site["sections"]:
        topics = []
        for t in s["topics"]:
            here = page.get("topic") is t
            t_cur = ' aria-current="page"' if here and page["level"] == 3 else ""
            if not t["pages"]:
                topics.append(f'<li><a class="leaf" href="{t["url"]}"{t_cur}>{E(t["name"])}</a></li>')
                continue
            kids = "".join(
                f'<li><a href="{p["url"]}"{" aria-current=\"page\"" if page.get("page") is p else ""}>{E(p["name"])}</a></li>'
                for p in t["pages"])
            topics.append(f'<li><details{" open" if here else ""}><summary>{E(t["name"])}</summary>'
                          f'<ul><li><a href="{t["url"]}"{t_cur}>Overview</a></li>{kids}</ul></details></li>')
        s_cur = ' aria-current="page"' if page.get("section") is s and page["level"] == 2 else ""
        groups.append(f'<div class="nav-group"><a class="nav-group-title" href="{s["url"]}"{s_cur}>{E(s["name"])}</a>'
                      f'<ul>{"".join(topics)}</ul></div>')
    return ('<details class="side-wrap" open data-side><summary>Browse docs</summary>'
            f'<nav class="side" aria-label="Docs">{"".join(groups)}</nav></details>')


def docs_page(site: dict, page: dict, body: str, toc: str, built: str) -> str:
    crumbs = "".join(f'<li><a href="{u}">{E(n)}</a></li>' for n, u in page["crumbs"][1:])
    crumb_nav = f'<nav class="crumbs" aria-label="Breadcrumb"><ol>{crumbs}</ol></nav>' if crumbs else ""
    toc_html = (f'<aside class="toc" aria-label="On this page"><p class="toc-title">On this page</p>{toc}</aside>'
                if toc else "")
    inner = f"""<div class="docs-grid{" has-toc" if toc else ""}">
  {docs_sidebar(site, page)}
  <main id="main" tabindex="-1" class="docs-main">{crumb_nav}{body}</main>
  {toc_html}
</div>"""
    return shell(site, page, inner, built, docs=True)


# GitHub linguist colours: developers already associate them with each language.
LANG_ACCENT = {
    "PHP": "#4f5d95", "Python": "#3572a5", "Go": "#00add8", "Rust": "#dea584", "TypeScript": "#3178c6",
    "JavaScript": "#f1e05a", "Shell": "#89e051", "HCL": "#844fba", "C": "#555555", "Perl": "#0298c3",
    "Ruby": "#701516", "Swift": "#f05138", "Groovy": "#4298b8", "Jinja": "#a52a22",
}
DEFAULT_ACCENT = "#8b949e"


def project_card(p: dict, heading: str = "h3") -> str:
    meta = p.get("meta") or {}
    lang = meta.get("language")
    accent = LANG_ACCENT.get(lang or "", DEFAULT_ACCENT)
    label, tone_ = status_of(meta) if meta else (p["kind"], "muted")
    note = f'<span class="card-status status-{tone_}">{E(label)}</span>' if label != "Code available" else ""
    lang_html = f'<span class="card-lang">{E(lang or "No language")}</span>'
    return (f'<li><div class="card" style="--accent: {accent}">'
            f'<{heading} class="card-name"><a class="card-link" href="{p["url"]}">{E(p["name"])}</a></{heading}>'
            f'<p class="card-summary">{E(p["summary"])}</p>'
            f'<div class="card-foot">{lang_html}{note}</div></div></li>')


def heatmap() -> str:
    path = CACHE / "_contributions.json"
    if not path.exists():
        return ""
    data = json.loads(path.read_text())
    days = {(d["week"], d["row"]): d for d in data["days"]}
    if not days:
        return ""
    weeks = max(w for w, _ in days) + 1
    cells, last_month = [], None
    for w in range(weeks):
        first = next((days[(w, r)] for r in range(7) if (w, r) in days), None)
        month = datetime.fromisoformat(first["date"]).strftime("%b") if first else None
        cells.append(f'<div class="hm-month">{month if month != last_month else ""}</div>')
        last_month = month
        for r in range(7):
            d = days.get((w, r))
            cells.append(f'<span class="hm-{d["level"]}"></span>' if d else '<span class="hm-none"></span>')
    total = data.get("total")
    caption = (f'<p class="hm-caption">{E(total)} contributions on GitHub in the last year.</p>' if total else "")
    return f'<div class="heatmap" aria-hidden="true"><div class="hm-grid">{"".join(cells)}</div></div>{caption}'


def render_home(site: dict, counts: dict, built: str) -> str:
    user = json.loads((CACHE / "_user.json").read_text())
    groups, chips, n_projects, stars, langs = [], [], 0, 0, set()
    for s in site["sections"]:
        for t in s["topics"]:
            projects = [p for p in t["pages"] if p.get("meta")]
            if not projects:
                continue
            n_projects += len(projects)
            for p in projects:
                stars += p["meta"].get("stargazers_count") or 0
                if p["meta"].get("language"):
                    langs.add(p["meta"]["language"])
            gid = f'{s["slug"]}-{t["slug"]}'
            chips.append(f'<a class="chip" href="#{gid}">{E(t["name"])}</a>')
            groups.append(f'<section class="group"><h2 id="{gid}" class="group-title">{E(t["name"])}</h2>'
                          f'<p class="group-summary">{E(t["blurb"])} <a href="{t["url"]}">Read the docs</a></p>'
                          f'<ul role="list" class="card-grid">{"".join(project_card(p) for p in projects)}</ul></section>')
    years = datetime.now(timezone.utc).year - int(user["created_at"][:4])
    stats = [f"{years} years on GitHub", f"{n_projects} public projects", f"{len(langs)} languages",
             f"{stars} stars", f"{counts['all']} documentation pages"]
    owner = E(site["owner"])
    body = f"""<main id="main" tabindex="-1" class="wrap home-main">
<section class="intro">
  <div class="intro-text">
    <header class="page-header">
      <h1 class="page-title">Open source</h1>
      <p class="page-intro">{E(site["tagline"])} {E(site["intro"])} Most of the work is <a href="#monitoring-cacti-plugins">monitoring for Cacti</a>, from HPC plugins to the RRDtool stack underneath.</p>
    </header>
    <p class="stat-list">{"".join(f'<span>{E(x)}</span>' for x in stats)}</p>
  </div>
  <div class="profile-block">
    <div class="profile">
      <img src="{E(user["avatar_url"])}&amp;s=128" alt="" width="64" height="64" class="avatar">
      <div class="profile-name"><p class="profile-title">{owner}</p><p class="profile-handle" translate="no">github.com/{owner}</p></div>
      <div class="profile-actions">
        <a class="button button-primary" href="https://github.com/{owner}">GitHub profile</a>
        <a class="button button-secondary" href="https://github.com/{owner}?tab=repositories&amp;type=public">All repos</a>
      </div>
    </div>
    {heatmap()}
  </div>
  <nav class="chip-nav" aria-label="Groups of projects">{"".join(chips)}</nav>
</section>
{"".join(groups)}
</main>"""
    return shell(site, {"level": 1, "name": "Home", "summary": site["intro"]}, body, built, docs=False)


def topic_cards(s: dict, si: int) -> str:
    out = []
    for t in s["topics"]:
        kids = "".join(f'<li><a href="{p["url"]}">{E(p["name"])}</a></li>' for p in t["pages"][:6])
        more = f'<li class="more"><a href="{t["url"]}">All {len(t["pages"])} pages</a></li>' if len(t["pages"]) > 6 else ""
        out.append(f'<li class="topic-card"><a class="topic-title" href="{t["url"]}">'
                   f'{E(t["name"])}</a>'
                   f'<p>{E(t["blurb"])}</p>{f"<ul>{kids}{more}</ul>" if kids else ""}</li>')
    return f'<ul class="topic-cards" role="list">{"".join(out)}</ul>'


def safe_url(u: str | None) -> str | None:
    return E(u) if u and urlsplit(u).scheme == "https" else None


def projects_of(topics: list[dict]) -> list[dict]:
    return [p for t in topics for p in t["pages"] if p.get("meta")]


def compare_table(projects: list[dict]) -> str:
    rows = []
    for p in projects:
        m = p["meta"]
        label, tone_ = status_of(m)
        rel = m.get("release")
        rows.append(f'<tr><th scope="row"><a href="{p["url"]}">{E(p["name"])}</a></th>'
                    f'<td><span class="card-status status-{tone_}">{E(label)}</span></td>'
                    f'<td>{E(m.get("language") or "Not set")}</td><td>{E(m.get("license") or "Not set")}</td>'
                    f'<td>{E(rel["tag"]) + (" (pre-release)" if rel.get("prerelease") else "") if rel else "None"}</td><td>{fmt_date(m.get("pushed_at"))}</td></tr>')
    return ('<div class="table-wrap"><table class="compare"><thead><tr><th scope="col">Project</th><th scope="col">Status</th>'
            '<th scope="col">Language</th><th scope="col">License</th><th scope="col">Latest release</th>'
            f'<th scope="col">Updated</th></tr></thead><tbody>{"".join(rows)}</tbody></table></div>')


def activity_list(projects: list[dict], limit: int) -> str:
    items = sorted(((c, p) for p in projects for c in p["meta"].get("commits") or []),
                   key=lambda cp: cp[0]["date"], reverse=True)[:limit]
    if not items:
        return ""
    li = "".join(f'<li><a class="act-msg" href="{safe_url(c["url"]) or p["url"]}">{E(c["msg"])}</a>'
                 f'<span class="act-meta"><a href="{p["url"]}">{E(p["name"])}</a> · {fmt_date(c["date"])}</span></li>'
                 for c, p in items)
    return f'<ul class="activity" role="list">{li}</ul>'


def render_section(site: dict, page: dict, built: str) -> str:
    s = page["section"]
    projects = projects_of(s["topics"])
    n = sum(len(t["pages"]) for t in s["topics"])
    body = (f'<h1>{E(s["name"])}</h1><p class="lede">{E(s["blurb"])}</p>'
            f'<p class="meta-row"><span>{len(s["topics"])} topics</span><span>{n} pages</span></p>')
    if projects:
        langs, statuses = {}, {}
        for p in projects:
            langs[p["meta"].get("language") or "Not set"] = langs.get(p["meta"].get("language") or "Not set", 0) + 1
            label = status_of(p["meta"])[0]
            statuses[label] = statuses.get(label, 0) + 1
        def bar(d):
            return "".join(f'<li><span>{E(k)}</span><b>{v}</b></li>' for k, v in sorted(d.items(), key=lambda kv: (-kv[1], kv[0])))
        recent = sorted(projects, key=lambda p: p["meta"].get("pushed_at") or "", reverse=True)[:6]
        body += (f'<h2 id="at-a-glance" class="docs-h2">At a glance</h2><div class="glance">'
                 f'<div><h3>Languages</h3><ul class="tally" role="list">{bar(langs)}</ul></div>'
                 f'<div><h3>Status</h3><ul class="tally" role="list">{bar(statuses)}</ul></div></div>'
                 f'<h2 id="recently-updated" class="docs-h2">Recently updated</h2>'
                 f'<ul class="card-grid card-grid-docs" role="list">{"".join(project_card(p) for p in recent)}</ul>')
    body += f'<h2 id="topics" class="docs-h2">Topics</h2>{topic_cards(s, 0)}'
    toc = ('<ol><li class="l2"><a href="#at-a-glance">At a glance</a></li><li class="l2"><a href="#recently-updated">Recently updated</a></li>'
           '<li class="l2"><a href="#topics">Topics</a></li></ol>') if projects else ""
    return docs_page(site, page, body, toc, built)


def render_topic(site: dict, page: dict, built: str) -> str:
    t = page["topic"]
    body = f'<h1>{E(t["name"])}</h1><p class="lede">{E(t["blurb"])}</p>'
    if t.get("local"):
        body += f'<div class="prose">{(CONTENT / "pages" / (t["local"] + ".html")).read_text()}</div>'
    projects = projects_of([t])
    toc = []
    if projects:
        body += f'<h2 id="compare" class="docs-h2">Compare</h2>{compare_table(projects)}'
        toc.append(("compare", "Compare"))
    if t["pages"]:
        body += f'<h2 id="pages" class="docs-h2">Pages</h2><ul class="card-grid card-grid-docs" role="list">{"".join(project_card(p, "h3") for p in t["pages"])}</ul>'
        toc.append(("pages", "Pages"))
    act = activity_list(projects, 8)
    if act:
        body += f'<h2 id="recent-activity" class="docs-h2">Recent activity</h2>{act}'
        toc.append(("recent-activity", "Recent activity"))
    toc_html = "<ol>" + "".join(f'<li class="l2"><a href="#{i}">{n}</a></li>' for i, n in toc) + "</ol>" if len(toc) > 1 else ""
    return docs_page(site, page, body, toc_html, built)


def repo_details(p: dict, owner: str) -> tuple[str, list]:
    m = p["meta"]
    out, heads = [], []
    rel = m.get("release")
    rows = [("Created", fmt_date(m.get("created_at"))), ("Last push", fmt_date(m.get("pushed_at"))),
            ("Default branch", E(m.get("default_branch") or "")),
            ("Latest release", f'<a href="{safe_url(rel["url"])}">{E(rel["tag"])}</a>{" pre-release" if rel.get("prerelease") else ""} ({fmt_date(rel["date"])})'
             if rel and safe_url(rel["url"]) else "None yet"),
            ("Open issues and pull requests", str(m.get("open_issues_count") or 0)),
            ("Stars", str(m.get("stargazers_count") or 0))]
    if m.get("topics"):
        rows.append(("Topics", " ".join(f'<span class="card-status status-muted">{E(t)}</span>' for t in m["topics"])))
    if safe_url(m.get("homepage")):
        rows.append(("Homepage", f'<a href="{safe_url(m["homepage"])}">{E(m["homepage"])}</a>'))
    out.append('<h2 id="gh-project-details">Project details</h2><table class="kv"><tbody>'
               + "".join(f'<tr><th scope="row">{k}</th><td>{v}</td></tr>' for k, v in rows) + "</tbody></table>")
    heads.append((2, "Project details", "gh-project-details"))
    par = m.get("parent")
    if par and safe_url(par.get("html_url")):
        out.append(f'<h2 id="gh-upstream">Upstream</h2><p>This is a fork of <a href="{safe_url(par["html_url"])}">{E(par["full_name"])}</a>'
                   f'{": " + E(par["description"]) if par.get("description") else ""}. The README above comes from upstream; '
                   f'changes are prepared here and proposed back there.</p>')
        heads.append((2, "Upstream", "gh-upstream"))
    if m.get("commits"):
        li = "".join(f'<li><a href="{safe_url(c["url"]) or "#"}">{E(c["msg"])}</a> <span class="act-meta">{fmt_date(c["date"])}</span></li>'
                     for c in m["commits"])
        out.append(f'<h2 id="gh-recent-changes">Recent changes</h2><ul>{li}</ul>')
        heads.append((2, "Recent changes", "gh-recent-changes"))
    if m.get("docs"):
        def doc_link(d):
            here = DOC_PAGES.get((p["repo"], d["name"]))
            if here:
                return f'<li><a href="{here}">{E(d["name"])}</a> <span class="act-meta">on this site</span></li>'
            return f'<li><a href="{safe_url(d["url"]) or "#"}">{E(d["name"])}</a></li>'
        li = "".join(doc_link(d) for d in m["docs"])
        out.append(f'<h2 id="gh-repo-docs">Documentation in the repository</h2><ul>{li}</ul>')
        heads.append((2, "Documentation in the repository", "gh-repo-docs"))
    return "".join(out), heads


def render_leaf(site: dict, page: dict, built: str) -> str:
    p = page["page"]
    meta = p.get("meta")
    if meta:
        raw = (CACHE / f"{p['repo']}.html").read_text()
        branch = meta.get("default_branch") or "HEAD"
        prose, heads = sanitize_readme(raw, site["owner"], p["repo"], branch)
        if not prose.strip():
            prose = "<p>[No README yet.]</p>"
        url = E(meta["html_url"])
        chips = [status_badge(meta), badge(p["kind"], "muted")]
        facts = [("Language", meta.get("language") or "Not set"), ("License", meta.get("license") or "Not set"),
                 ("Updated", fmt_date(meta.get("pushed_at")))]
        fact_html = "".join(f'<div><dt>{k}</dt><dd>{E(v)}</dd></div>' for k, v in facts)
        head = (f'<div class="page-head"><div><p class="chips-row">{"".join(chips)}</p>'
                f'<h1 class="code-title">{E(p["name"])}</h1><p class="lede">{E(p["summary"])}</p></div>'
                f'<a class="btn" href="{url}"><svg width="16" height="16" viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M12 2a10 10 0 0 0-3.2 19.5c.5.1.7-.2.7-.5v-1.7c-2.8.6-3.4-1.3-3.4-1.3-.4-1.1-1.1-1.4-1.1-1.4-.9-.6.1-.6.1-.6 1 .1 1.5 1 1.5 1 .9 1.6 2.4 1.1 3 .9.1-.7.4-1.1.6-1.4-2.2-.3-4.6-1.1-4.6-5a3.9 3.9 0 0 1 1-2.7 3.6 3.6 0 0 1 .1-2.7s.8-.3 2.8 1a9.6 9.6 0 0 1 5 0c1.9-1.3 2.8-1 2.8-1 .5 1.4.2 2.4.1 2.7a3.9 3.9 0 0 1 1 2.7c0 3.9-2.4 4.7-4.6 5 .4.3.7.9.7 1.9V21c0 .3.2.6.7.5A10 10 0 0 0 12 2z"></path></svg>View on GitHub</a></div>'
                f'<dl class="facts">{fact_html}</dl>')
        edit = f'<a href="{url}/blob/{E(branch)}/README.md">View this page\'s source</a>'
        extra, extra_heads = repo_details(p, site["owner"])
        prose += extra
        heads = heads + extra_heads
    elif "doc" in p:
        rm = p["repo_meta"]
        branch = rm.get("default_branch") or "HEAD"
        subdir = p["path"].rsplit("/", 1)[0] + "/" if "/" in p["path"] else ""
        prose, heads = sanitize_readme(doc_cache(p["doc"], p["path"]).read_text(), site["owner"], p["doc"], branch, subdir)
        src = f'{rm["html_url"]}/blob/{branch}/{p["path"]}'
        repo_page = next((q for s in site["sections"] for t in s["topics"] for q in t["pages"] if q.get("repo") == p["doc"]), None)
        repo_link = (f'<a href="{repo_page["url"]}">{E(p["doc"])}</a>' if repo_page else E(p["doc"]))
        facts = (f'<div><dt>Project</dt><dd>{repo_link}</dd></div>'
                 f'<div><dt>Source file</dt><dd><a href="{E(src)}">{E(p["path"])}</a></dd></div>'
                 f'<div><dt>Repository updated</dt><dd>{fmt_date(rm.get("pushed_at"))}</dd></div>')
        head = (f'<div class="page-head"><div><p class="chips-row">{status_badge(rm)}{badge(p["kind"], "muted")}</p>'
                f'<h1>{E(p["name"])}</h1><p class="lede">{E(p["summary"])}</p></div></div>'
                f'<dl class="facts">{facts}</dl>')
        edit = f'<a href="{E(src)}">View this page\'s source</a>'
    else:
        prose = (CONTENT / "pages" / f"{p['local']}.html").read_text()
        heads = [(int(m[0]), html.unescape(re.sub("<[^>]+>", "", m[2])), m[1])
                 for m in re.findall(r'<h([23]) id="([^"]+)">(.*?)</h\1>', prose)]
        head = (f'<div class="page-head"><div><p class="chips-row">{badge(p["kind"], "muted")}</p>'
                f'<h1>{E(p["name"])}</h1><p class="lede">{E(p["summary"])}</p></div></div>')
        edit = ""
    sibs = page["topic"]["pages"]
    i = sibs.index(p)
    pager = '<nav class="pager" aria-label="Previous and next">'
    if i > 0:
        pager += f'<a href="{sibs[i-1]["url"]}"><span>Previous</span>{E(sibs[i-1]["name"])}</a>'
    if i < len(sibs) - 1:
        pager += f'<a class="next" href="{sibs[i+1]["url"]}"><span>Next</span>{E(sibs[i+1]["name"])}</a>'
    pager += "</nav>"
    toc = ""
    if len(heads) >= 2:
        toc = "<ol>" + "".join(f'<li class="l{lvl}"><a href="#{hid}">{E(txt)}</a></li>' for lvl, txt, hid in heads) + "</ol>"
    body = f'{head}<div class="prose">{prose}</div>{pager}<p class="page-foot">{edit}</p>'
    return docs_page(site, page, body, toc, built)


# ---------------------------------------------------------------- build

def build(site: dict) -> None:
    pages = load_model(site)
    counts: dict = {lvl: sum(1 for p in pages if p["level"] == lvl) for lvl in (1, 2, 3, 4)}
    counts["all"] = site["page_count"] = len(pages)
    built = datetime.now(timezone.utc).strftime("%-d %b %Y")
    if OUT.exists():
        shutil.rmtree(OUT)
    (OUT / "assets").mkdir(parents=True)
    for f in (ROOT / "assets").iterdir():
        shutil.copy(f, OUT / "assets" / f.name)
    (OUT / "assets" / "tokens.css").write_text(build_tokens())

    index = []
    diagrams = diagram_pages = 0
    for page in pages:
        if page["level"] == 1:
            out = render_home(site, counts, built)
        elif page["level"] == 2:
            out = render_section(site, page, built)
        elif page["level"] == 3:
            out = render_topic(site, page, built)
        else:
            out = render_leaf(site, page, built)
        dest = OUT / page["url"].strip("/") / "index.html"
        dest.parent.mkdir(parents=True, exist_ok=True)
        dest.write_text(out)
        n = out.count('<pre class="mermaid">')
        diagrams, diagram_pages = diagrams + n, diagram_pages + (1 if n else 0)
        trail = " / ".join(n for n, _ in page["crumbs"][1:])
        index.append({"t": page["name"], "u": page["url"], "d": page.get("summary", ""), "p": trail})

    (OUT / "search.json").write_text(json.dumps(index, separators=(",", ":")))
    if diagrams:
        vendor_mermaid()
        (OUT / "assets" / "vendor").mkdir()
        shutil.copy(MERMAID_JS, OUT / "assets" / "vendor" / "mermaid.min.js")
        shutil.copy(MERMAID_LICENSE, OUT / "assets" / "vendor" / "mermaid.LICENSE.txt")
        print(f"diagrams: {diagrams} on {diagram_pages} pages")
    nf = {"level": 0, "url": "/404.html", "name": "Page not found", "crumbs": [("Home", "/")]}
    (OUT / "404.html").write_text(docs_page(site, nf,
        '<h1>Page not found</h1><p class="lede">That address does not exist. <a href="/">Browse all projects.</a></p>',
        "", built))
    (OUT / ".nojekyll").write_text("")
    print(f"built {counts['all']} pages: L1 {counts[1]}, L2 {counts[2]}, L3 {counts[3]}, L4 {counts[4]}")


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--fetch", action="store_true", help="refresh cache/ from GitHub with gh")
    args = ap.parse_args()
    site = json.loads((CONTENT / "sitemap.json").read_text())
    if args.fetch:
        fetch_all(site)
    build(site)


if __name__ == "__main__":
    main()
