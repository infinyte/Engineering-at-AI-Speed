"""Build the GitHub Pages publication with Python 3.11+; no dependencies."""

from datetime import date, datetime, timezone
from email.utils import format_datetime
from html import escape
import json
import math
from pathlib import Path
import re
import xml.etree.ElementTree as ET

from markdown_renderer import render

ROOT = Path(__file__).resolve().parent


def page(config, title, description, filename, content, accent="#60a5fa"):
    canonical = config["url"] + filename
    social = config["url"] + "assets/social-cover.png"
    document_title = title if title == config["title"] else title + " | " + config["title"]
    return f'''<!DOCTYPE html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>{escape(document_title)}</title><meta name="description" content="{escape(description, quote=True)}">
<link rel="canonical" href="{canonical}"><meta property="og:title" content="{escape(title, quote=True)}">
<meta property="og:description" content="{escape(description, quote=True)}"><meta property="og:type" content="{'article' if filename.startswith('ep') else 'website'}">
<meta property="og:url" content="{canonical}"><meta property="og:image" content="{social}"><meta property="og:image:width" content="1200"><meta property="og:image:height" content="630">
<meta name="twitter:card" content="summary_large_image"><meta property="og:image:alt" content="Engineering at AI Speed. Implementation became cheap before alignment did.">
<meta name="theme-color" content="#111827"><link rel="icon" href="assets/favicon.svg" type="image/svg+xml">
<link rel="alternate" type="application/rss+xml" title="Engineering at AI Speed" href="feed.xml"><link rel="stylesheet" href="assets/style.css">
</head><body style="--episode-accent:{accent}"><a class="skip" href="#main">Skip to content</a>
<header class="site-header"><a class="brand" href="index.html">Engineering at AI Speed<span>by Kurt Mitchell</span></a>
<nav aria-label="Main navigation"><a href="index.html#episodes">The series</a><a href="reference.html">Field guide</a><a href="about.html">About</a><a href="feed.xml">RSS</a></nav></header>
{content}
<footer class="site-footer"><p><strong>Engineering at AI Speed</strong><br>Better decisions before more code.</p><div><a href="index.html#episodes">Engineering at AI Speed — All episodes</a><a href="https://github.com/infinyte/Engineering-at-AI-Speed">GitHub repository</a><a href="https://infinyte.github.io/Pattern-Mirror/">Also by Kurt: The Pattern Mirror</a><span>© {date.fromisoformat(config['episodes'][0]['date']).year} Kurt Mitchell</span></div></footer>
</body></html>'''


def label(episode):
    return "Prologue" if episode["number"] == 0 else f"Episode {episode['number']:02}"


def article(config, episode, source, published):
    body, headings = render(source)
    minutes = max(1, math.ceil(len(source.split()) / 220))
    toc = "".join(f'<a href="#{slug}">{escape(title)}</a>' for level, slug, title in headings if level == 2)
    position = published.index(episode)
    neighbors = []
    for offset, text in [(-1, "Previous"), (1, "Next")]:
        adjacent = position + offset
        if 0 <= adjacent < len(published):
            target = published[adjacent]
            neighbors.append(f'<a href="ep{target["number"]}.html"><span>{text} · {label(target)}</span>{escape(target["title"])}</a>')
    if position == len(published) - 1:
        neighbors.append('<a href="index.html#episodes"><span>Explore the series</span>Return to all episodes</a>')
    return f'''<main id="main"><section class="article-hero"><a class="back" href="index.html#episodes">All episodes</a><p class="episode-label">{label(episode)}</p><h1>{escape(episode['title'])}</h1><p class="dek">{escape(episode['description'])}</p><p class="byline">Kurt Mitchell <span>·</span> <time datetime="{episode['date']}">{date.fromisoformat(episode['date']).strftime('%B %d, %Y')}</time> <span>·</span> {minutes} min read</p></section><div class="article-layout"><aside class="toc" aria-label="On this page"><p>In this article</p>{toc}</aside><article class="prose">{body}<nav class="episode-navigation" aria-label="Episode navigation">{''.join(neighbors)}</nav></article></div></main>'''


def home(config, published):
    latest = published[-1]
    latest_link = (f'<a class="text-link" href="ep{latest["number"]}.html">Read Episode {latest["number"]}</a>' if latest["number"] else '<a class="text-link" href="#episodes">Explore the season</a>')
    cards = []
    for ep in config["episodes"]:
        if ep["number"] == 0:
            continue
        available = ep["status"] == "published"
        title = escape(ep["title"])
        heading = f'<a href="ep{ep["number"]}.html">{title}</a>' if available else title
        cards.append(f'<article class="episode-card {"available" if available else "upcoming"}" style="--card-accent:{ep["color"]}"><div class="card-top"><span class="episode-number">{ep["number"]:02}</span><span class="status">{"Read now" if available else "Coming soon"}</span></div><h3>{heading}</h3><p>{escape(ep["description"])}</p></article>')
    return f'''<main id="main"><section class="hero"><div class="hero-copy"><p class="series-note">A series by Kurt Mitchell</p><h1>Engineering<br>at AI Speed</h1><p class="hero-thesis">Implementation became cheap<br>before alignment did.</p><p class="hero-description">AI compresses the distance between an idea and its implementation. This series explores the engineering discipline that makes that speed useful.</p><div class="hero-actions"><a class="button" href="ep0.html">Start with the prologue</a>{latest_link}</div><p class="release-note">A prologue and eight focused episodes. Released one at a time.</p></div><figure class="hero-figure"><img src="assets/interpretation.svg" alt="One ambiguous request branches into two internally reasonable implementations: a searchable catalog and an authoritative registry."><figcaption>The disagreement existed before the code.</figcaption></figure></section>
<section class="premise"><p>Some friction was carrying information.</p><div>Clarification. Failure analysis. Architectural decisions. As implementation gets faster, we need to make that work more deliberate—and bring it forward.</div></section>
<section id="episodes" class="episodes"><div class="section-heading"><h2>The first season</h2><p>One engineering problem at a time.</p></div><div class="episode-grid">{''.join(cards)}</div></section>
<section class="field-note"><div><h2>Keep the language close.</h2><p>A companion field guide distinguishes established terminology from the vocabulary we use inside a project.</p></div><a class="button secondary" href="reference.html">Open the field guide</a></section></main>'''


def build():
    config = json.loads((ROOT / "series.json").read_text(encoding="utf-8"))
    numbers = [ep["number"] for ep in config["episodes"]]
    if numbers != list(range(9)):
        raise ValueError("Episodes must be numbered 0 through 8 in order")
    published = [ep for ep in config["episodes"] if ep["status"] == "published"]
    sources = {}
    # Validate the complete release before touching generated output.
    for ep in config["episodes"]:
        if ep["status"] not in {"published", "draft", "planned"}:
            raise ValueError("Unknown publication status")
        if ep in published:
            date.fromisoformat(ep["date"])
            sources[ep["number"]] = (ROOT / ep["file"]).read_text(encoding="utf-8")
            if len(sources[ep["number"]].split()) < 300:
                raise ValueError("A published article must contain a complete manuscript")
    if not published or published[0]["number"] != 0:
        raise ValueError("The prologue must be published")
    pages = {"index.html": page(config, config["title"], config["description"], "index.html", home(config, published))}
    for ep in published:
        name = f"ep{ep['number']}.html"
        pages[name] = page(config, ep["title"], ep["description"], name, article(config, ep, sources[ep["number"]], published), ep["color"])
    for stem, title, desc in [("about", "About the series", config["description"]), ("reference", "The integration field guide", "Definitions, distinctions, and project-local vocabulary for integration work.")]:
        body, _ = render((ROOT / f"content/{stem}.md").read_text(encoding="utf-8"))
        pages[f"{stem}.html"] = page(config, title, desc, f"{stem}.html", f'<main id="main" class="standalone"><h1>{title}</h1><article class="prose">{body}</article></main>')
    pages["404.html"] = page(config, "Page not found", "Return to the series.", "404.html", f'<main id="main" class="standalone"><h1>This page isn’t here.</h1><p>The episode may not have been released yet.</p><a class="button" href="{config["url"]}">Return to the series</a></main>').replace('href="assets/', f'href="{config["url"]}assets/')
    # A Pages 404 can be served at any nested URL, so its links must be absolute.
    pages["404.html"] = re.sub(r'href="(?!https?://|#)([^\"]+)"', lambda m: 'href="' + config["url"] + m[1] + '"', pages["404.html"])
    for filename, content in pages.items():
        (ROOT / filename).write_text(content, encoding="utf-8", newline="\n")
    # Only delete known generated article files, never source manuscripts.
    for path in ROOT.glob("ep[0-9]*.html"):
        if re.fullmatch(r"ep\d+\.html", path.name) and path.name not in pages:
            path.unlink()
    rss = ET.Element("rss", version="2.0")
    channel = ET.SubElement(rss, "channel")
    for key, value in [("title", config["title"]), ("link", config["url"]), ("description", config["description"]), ("language", "en-us")]:
        ET.SubElement(channel, key).text = value
    for ep in reversed(published):
        item = ET.SubElement(channel, "item")
        url = config["url"] + f"ep{ep['number']}.html"
        for key, value in [("title", ep["title"]), ("link", url), ("guid", url), ("description", ep["description"]), ("pubDate", format_datetime(datetime.fromisoformat(ep["date"]).replace(tzinfo=timezone.utc)))]:
            ET.SubElement(item, key).text = value
    ET.ElementTree(rss).write(ROOT / "feed.xml", encoding="utf-8", xml_declaration=True)
    sitemap = ET.Element("urlset", xmlns="http://www.sitemaps.org/schemas/sitemap/0.9")
    for name in pages:
        if name != "404.html":
            ET.SubElement(ET.SubElement(sitemap, "url"), "loc").text = config["url"] + name
    ET.ElementTree(sitemap).write(ROOT / "sitemap.xml", encoding="utf-8", xml_declaration=True)
    (ROOT / ".nojekyll").touch()
    (ROOT / "robots.txt").write_text(f"User-agent: *\nAllow: /\nSitemap: {config['url']}sitemap.xml\n", encoding="utf-8")
    print(f"Built {len(pages)} pages; {len(published)} released articles.")


if __name__ == "__main__":
    build()
