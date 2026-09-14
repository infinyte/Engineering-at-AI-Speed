"""Release and rendering acceptance tests for the static publication."""

import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest
import xml.etree.ElementTree as ET


ROOT = Path(__file__).resolve().parents[1]


class PublicationTests(unittest.TestCase):
    def setUp(self):
        self.assertTrue((ROOT / "build.py").exists(), "The publication builder must exist")
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.site = Path(self.temp.name) / "site"
        shutil.copytree(ROOT, self.site, ignore=shutil.ignore_patterns(".git", "__pycache__"))
        # Test release transitions against a fixed launch fixture, independent
        # of how many episodes the real publication has subsequently released.
        manifest = json.loads((self.site / "series.json").read_text(encoding="utf-8"))
        for episode in manifest["episodes"][2:]:
            episode.update(status="draft", date="")
        (self.site / "series.json").write_text(json.dumps(manifest), encoding="utf-8")

    def build(self):
        result = subprocess.run([sys.executable, "build.py"], cwd=self.site,
                                capture_output=True, text=True, encoding="utf-8")
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def test_launch_contains_only_released_episodes(self):
        self.build()
        home = (self.site / "index.html").read_text(encoding="utf-8")
        self.assertIn('href="ep0.html"', home)
        self.assertIn('href="ep1.html"', home)
        self.assertIn("Building a World Around a Terrible API", home)
        self.assertNotIn('href="ep2.html"', home)
        self.assertFalse((self.site / "ep2.html").exists())

    def test_draft_transition_removes_stale_page_and_feed_entry(self):
        self.build()
        manifest = json.loads((self.site / "series.json").read_text(encoding="utf-8"))
        manifest["episodes"][1]["status"] = "draft"
        (self.site / "series.json").write_text(json.dumps(manifest), encoding="utf-8")
        self.build()
        self.assertFalse((self.site / "ep1.html").exists())
        self.assertNotIn("ep1.html", (self.site / "feed.xml").read_text(encoding="utf-8"))
        self.assertNotIn('href="ep1.html"', (self.site / "index.html").read_text(encoding="utf-8"))

    def test_publishing_next_episode_updates_navigation_and_feed(self):
        manifest = json.loads((self.site / "series.json").read_text(encoding="utf-8"))
        manifest["episodes"][2].update(status="published", date="2026-09-28")
        # Unreleased manuscripts stay outside the public repository. Supply a
        # synthetic manuscript in the isolated test copy to exercise release.
        manuscript = "# Release fixture\n\n## A complete test article\n\n" + " ".join(
            ["This synthetic paragraph exercises publication with known content."] * 45)
        (self.site / manifest["episodes"][2]["file"]).write_text(manuscript, encoding="utf-8")
        (self.site / "series.json").write_text(json.dumps(manifest), encoding="utf-8")
        self.build()
        self.assertTrue((self.site / "ep2.html").exists())
        self.assertIn('href="ep2.html"', (self.site / "ep1.html").read_text(encoding="utf-8"))
        self.assertIn("ep2.html", (self.site / "feed.xml").read_text(encoding="utf-8"))

    def test_article_has_navigation_accessible_content_and_metadata(self):
        self.build()
        page = (self.site / "ep1.html").read_text(encoding="utf-8")
        for expected in ['lang="en"', 'id="main"', 'class="toc"', 'rel="canonical"',
                         'property="og:image"', '<h1>', '<blockquote>', '<table>',
                         'href="ep0.html"', 'href="index.html#episodes"']:
            self.assertIn(expected, page)
        self.assertNotIn('href="ep2.html"', page)

    def test_feed_and_sitemap_have_only_published_articles(self):
        self.build()
        feed = ET.parse(self.site / "feed.xml")
        self.assertEqual(len(feed.findall("./channel/item")), 2)
        ET.parse(self.site / "sitemap.xml")
        self.assertNotIn("ep2.html", (self.site / "sitemap.xml").read_text(encoding="utf-8"))

    def test_bad_release_metadata_fails_before_modifying_output(self):
        self.build()
        before = (self.site / "index.html").read_bytes()
        manifest = json.loads((self.site / "series.json").read_text(encoding="utf-8"))
        manifest["episodes"][2].update(status="published", date="")
        (self.site / "series.json").write_text(json.dumps(manifest), encoding="utf-8")
        result = subprocess.run([sys.executable, "build.py"], cwd=self.site, capture_output=True)
        self.assertNotEqual(result.returncode, 0)
        self.assertEqual(before, (self.site / "index.html").read_bytes())

    def test_verifier_checks_links_and_detects_missing_assets(self):
        self.build()
        result = subprocess.run([sys.executable, "verify.py"], cwd=self.site, capture_output=True)
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        (self.site / "assets/style.css").unlink()
        result = subprocess.run([sys.executable, "verify.py"], cwd=self.site, capture_output=True)
        self.assertNotEqual(result.returncode, 0)

    def test_build_is_repeatable(self):
        self.build()
        first = {p.name: p.read_bytes() for p in self.site.glob("*.html")}
        self.build()
        self.assertEqual(first, {p.name: p.read_bytes() for p in self.site.glob("*.html")})

    def test_error_page_links_work_from_a_nested_missing_url(self):
        self.build()
        error_page = (self.site / "404.html").read_text(encoding="utf-8")
        self.assertNotIn('href="index.html', error_page)
        self.assertNotIn('href="reference.html', error_page)
        self.assertNotIn('href="feed.xml', error_page)


if __name__ == "__main__":
    unittest.main()
