# Engineering at AI Speed

**Implementation became cheap before alignment did.**

A series by Kurt Mitchell about terminology, requirements, integration, architecture, and evidence in AI-driven development.

- Website: https://infinyte.github.io/Engineering-at-AI-Speed/
- Start here: https://infinyte.github.io/Engineering-at-AI-Speed/ep0.html
- Feed: https://infinyte.github.io/Engineering-at-AI-Speed/feed.xml

## Publication model

This repository follows the small static publication model used by [Pattern Mirror](https://github.com/infinyte/Pattern-Mirror). Python generates the root HTML pages from Markdown manuscripts; GitHub Pages serves `main` from `/`. No server, database, JavaScript framework, or Python packages are required.

The prologue and Episodes 1–6 are published. Future manuscripts and editorial plans are maintained outside this public repository until release. A `draft` or `planned` episode appears as Coming soon without an article link. Dates are editorial metadata, not a scheduler.

**This repository is public.** Keep unreleased manuscripts and editorial notes outside it. A draft status hides an article from site navigation; it is not an access control.

## Build and verify

Requires Python 3.11 or newer.

```sh
python -m unittest discover -s tests -v
python build.py
python verify.py
python -m http.server 8000
```

Visit http://localhost:8000/. Test files exercise publication transitions in temporary copies. The verifier checks generated-page links, anchors, image alt text, headings, and XML. It does not perform live external-link or visual checks.

The Markdown renderer intentionally supports this publication’s authored subset: headings, paragraphs, emphasis, flat lists, tables, blockquotes, code fences, links, and images. Raw HTML is escaped. Use root-relative-to-page asset paths such as `assets/world.svg` in manuscripts; generated episode pages live at repository root. Nested lists and full CommonMark compatibility are not supported.

## Release an episode

1. Finish and review its manuscript outside this public repository. Confirm factual claims, examples, sources, and project-local definitions. Copy the approved manuscript into the path named in `series.json` when ready to release.
2. In `series.json`, set the episode’s `status` to `published` and its `date` to the intended publication date (`YYYY-MM-DD`).
3. Run the tests, build, and verifier. Preview the article on desktop and mobile. Check tables, diagrams, next/previous navigation, and social metadata.
4. Commit the manuscript, manifest, and regenerated output together. Push to `main` after review.
5. Confirm the GitHub Pages build and the live article. Share the release copy after verifying the URL.

The builder updates article navigation, homepage cards, RSS, and sitemap. Returning an episode to `draft` removes its generated HTML on the next build. It does not remove public Git history or copies already fetched by readers.

## Repository map

- `series.json`: titles, manuscript paths, publication statuses, and dates.
- `articles/`: canonical manuscripts for released articles.
- `content/`: About and terminology reference manuscripts.
- `assets/`: shared presentation, diagrams, favicon, and social cover.
- `build.py`, `markdown_renderer.py`: static publication builder.
- `verify.py`, `tests/`: structural and release checks.
- `PUBLISHING.md`: release checklist and season boundaries.
- `.github/workflows/verify.yml`: validation and generated-output drift check.

## Editorial conventions

Start with a concrete engineering problem. Explain the hidden assumption before introducing abstractions. End with a practical behavior the reader can adopt. Distinguish hypothetical examples from observed incidents. Do not present local meanings as universal definitions.

All rights reserved unless otherwise stated. The repository’s public availability does not grant a separate reuse license.
