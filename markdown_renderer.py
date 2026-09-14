"""Small, escaped Markdown renderer for this publication's authored subset.

Supports headings, paragraphs, quotes, flat lists, tables, fences, links, and
images. Raw HTML is escaped. This intentionally is not a CommonMark parser.
"""

import html
import re


def inline(text):
    tokens = []

    def hold(value):
        tokens.append(value)
        return f"\x00{len(tokens) - 1}\x00"

    text = html.escape(text, quote=True)
    text = re.sub(r"`([^`]+)`", lambda m: hold(f"<code>{m[1]}</code>"), text)

    def link(match):
        label, url = match.group(1), match.group(2)
        if re.match(r"(?:javascript|data|vbscript):", html.unescape(url), re.I):
            return label
        return hold(f'<a href="{url}">{label}</a>')

    text = re.sub(r"\[([^\]]+)\]\(([^\s)]+)\)", link, text)
    text = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", text)
    text = re.sub(r"(?<!\*)\*([^*]+)\*(?!\*)", r"<em>\1</em>", text)
    return re.sub(r"\x00(\d+)\x00", lambda m: tokens[int(m[1])], text)


def render(source):
    lines = source.splitlines()
    result, headings, counts = [], [], {}
    index = 0
    while index < len(lines):
        line = lines[index].strip()
        if not line:
            index += 1
            continue
        if line.startswith("```"):
            code = []
            index += 1
            while index < len(lines) and not lines[index].startswith("```"):
                code.append(lines[index])
                index += 1
            result.append("<pre><code>" + html.escape("\n".join(code)) + "</code></pre>")
        elif match := re.match(r"^(#{1,6}) (.+)$", line):
            level, text = len(match[1]), match[2]
            if level > 1:
                base = re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-") or "section"
                counts[base] = counts.get(base, 0) + 1
                slug = base if counts[base] == 1 else f"{base}-{counts[base]}"
                headings.append((level, slug, text))
                result.append(f'<h{level} id="{slug}">{inline(text)}</h{level}>')
        elif match := re.fullmatch(r"!\[([^\]]*)\]\(([^)]+)\)", line):
            result.append(f'<figure><img src="{html.escape(match[2], quote=True)}" alt="{html.escape(match[1], quote=True)}" loading="lazy"><figcaption>{inline(match[1])}</figcaption></figure>')
        elif line.startswith("> "):
            quote = []
            while index < len(lines) and lines[index].strip().startswith("> "):
                quote.append(lines[index].strip()[2:])
                index += 1
            result.append("<blockquote><p>" + inline(" ".join(quote)) + "</p></blockquote>")
            continue
        elif re.match(r"^(?:- |\d+\. )", line):
            ordered = bool(re.match(r"^\d+\. ", line))
            tag = "ol" if ordered else "ul"
            items = []
            pattern = r"^\d+\. " if ordered else r"^- "
            while index < len(lines) and re.match(pattern, lines[index].strip()):
                items.append("<li>" + inline(re.sub(pattern, "", lines[index].strip())) + "</li>")
                index += 1
            result.append(f"<{tag}>" + "".join(items) + f"</{tag}>")
            continue
        elif line.startswith("|"):
            rows = []
            while index < len(lines) and lines[index].strip().startswith("|"):
                cells = lines[index].strip().strip("|").split("|")
                if not all(re.fullmatch(r"\s*:?-+:?\s*", cell) for cell in cells):
                    tag = 'th scope="col"' if not rows else "td"
                    close = "th" if not rows else "td"
                    rows.append("<tr>" + "".join(f"<{tag}>{inline(c.strip())}</{close}>" for c in cells) + "</tr>")
                index += 1
            result.append('<div class="table-scroll" role="region" aria-label="Comparison table" tabindex="0"><table><thead>' + rows[0] + "</thead><tbody>" + "".join(rows[1:]) + "</tbody></table></div>")
            continue
        elif line == "---":
            result.append("<hr>")
        else:
            paragraph = [line]
            index += 1
            while index < len(lines) and lines[index].strip() and not re.match(r"^(#|>|\||```|!\[|- |\d+\. )", lines[index].strip()):
                paragraph.append(lines[index].strip())
                index += 1
            result.append("<p>" + inline(" ".join(paragraph)) + "</p>")
            continue
        index += 1
    return "\n".join(result), headings
