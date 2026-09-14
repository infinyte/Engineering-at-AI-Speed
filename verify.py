"""Validate generated pages, local links, anchors, image descriptions and XML."""

from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlsplit
import sys
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parent


class Document(HTMLParser):
    def __init__(self, content):
        super().__init__()
        self.links, self.ids, self.errors = [], set(), []
        self.headings = 0
        self.feed(content)

    def handle_starttag(self, tag, attrs):
        values = dict(attrs)
        if "id" in values:
            if values["id"] in self.ids:
                self.errors.append("Duplicate id: " + values["id"])
            self.ids.add(values["id"])
        if tag == "h1":
            self.headings += 1
        if tag == "img" and not values.get("alt"):
            self.errors.append("Image is missing descriptive alt text")
        for attribute in ("href", "src"):
            if attribute in values:
                self.links.append(values[attribute])


def verify():
    documents = {p.resolve(): Document(p.read_text(encoding="utf-8")) for p in ROOT.glob("*.html")}
    errors = []
    if not documents:
        errors.append("No generated pages. Run build.py first.")
    for path, document in documents.items():
        errors.extend(f"{path.name}: {error}" for error in document.errors)
        if document.headings != 1:
            errors.append(f"{path.name}: expected exactly one h1")
        for link in document.links:
            parsed = urlsplit(link)
            if parsed.scheme or parsed.netloc:
                continue
            target = (path.parent / unquote(parsed.path)).resolve() if parsed.path else path
            if not target.exists():
                errors.append(f"{path.name}: missing {link}")
            elif parsed.fragment and target in documents and unquote(parsed.fragment) not in documents[target].ids:
                errors.append(f"{path.name}: missing anchor {link}")
    for name in ["feed.xml", "sitemap.xml"]:
        try:
            ET.parse(ROOT / name)
        except (OSError, ET.ParseError) as error:
            errors.append(str(error))
    for path in (ROOT / "assets").glob("*.svg"):
        tree = ET.parse(path)
        if tree.find("{http://www.w3.org/2000/svg}title") is None:
            errors.append(f"{path.name}: SVG requires a title")
    for error in errors:
        print(error)
    print(f"Checked {len(documents)} pages: {len(errors)} errors.")
    return bool(errors)


if __name__ == "__main__":
    sys.exit(verify())
