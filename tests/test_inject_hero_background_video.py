from __future__ import annotations

import unittest
from pathlib import Path
from tempfile import TemporaryDirectory


class HeroBackgroundVideoInjectionTests(unittest.TestCase):
    def test_replaces_the_low_resolution_embed_with_the_native_source(self):
        from scripts import inject_hero_background_video as subject

        source = "<html><head></head><body><section class=\"elementor-element-98ce606\"><div class=\"elementor-background-video-container\"></div></section></body></html>"
        rendered = subject.inject(source)

        self.assertIn(f'id="{subject.STYLE_ID}"', rendered)
        self.assertIn(f'id="{subject.SCRIPT_ID}"', rendered)
        self.assertIn(subject.VIDEO_SOURCE, rendered)
        self.assertIn("indafire-hero-background-video", rendered)
        self.assertIn("object-fit: cover", rendered)

    def test_replaces_only_its_own_managed_layers(self):
        from scripts import inject_hero_background_video as subject

        with TemporaryDirectory() as directory:
            page = Path(directory) / "index.html"
            page.write_text("<html><head></head><body></body></html>", encoding="utf-8")

            self.assertEqual(subject.inject_assets((page,)), 1)
            self.assertEqual(subject.inject_assets((page,)), 0)


if __name__ == "__main__":
    unittest.main()
