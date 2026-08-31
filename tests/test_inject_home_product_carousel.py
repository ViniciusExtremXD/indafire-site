from __future__ import annotations

import unittest
from pathlib import Path
from tempfile import TemporaryDirectory


class HomeProductCarouselInjectionTests(unittest.TestCase):
    def test_injects_autoplay_with_accessible_progress_without_restyling_products(self) -> None:
        from scripts import inject_home_product_carousel as subject

        with TemporaryDirectory() as directory:
            page = Path(directory) / "index.html"
            page.write_text(
                "<html><head>"
                '<style id="indafire-home-product-carousel-style">old visual layer</style>'
                "</head><body>"
                '<div id="carrosselProdutos"><div class="swiper-wrapper"></div></div>'
                "</body></html>",
                encoding="utf-8",
            )

            changed = subject.inject_assets((page,))
            rendered = page.read_text(encoding="utf-8")

        self.assertEqual(changed, 1)
        self.assertIn(f'id="{subject.SCRIPT_ID}"', rendered)
        self.assertNotIn(f'id="{subject.STYLE_ID}"', rendered)
        self.assertIn("setTimeout", rendered)
        self.assertNotIn("setInterval", rendered)
        self.assertIn("elementor-swiper-button-next", rendered)
        self.assertIn("indafire-carousel-progress", rendered)
        self.assertIn("aria-hidden", rendered)
        self.assertIn("visibilityState", rendered)
        self.assertIn("prefers-reduced-motion", rendered)
        self.assertIn("var AUTOPLAY_DELAY = 2500;", rendered)
        self.assertNotIn("if (reducedMotion) return;", rendered)
        self.assertIn("pointerdown", rendered)
        self.assertNotIn("inda-product-featured", rendered)
        self.assertLess(rendered.index(f'id="{subject.SCRIPT_ID}"'), rendered.index("</body>"))

    def test_replaces_its_managed_layer_instead_of_duplicating_it(self) -> None:
        from scripts import inject_home_product_carousel as subject

        with TemporaryDirectory() as directory:
            page = Path(directory) / "index.html"
            page.write_text("<html><head></head><body></body></html>", encoding="utf-8")

            self.assertEqual(subject.inject_assets((page,)), 1)
            self.assertEqual(subject.inject_assets((page,)), 0)

    def test_keeps_an_unchanged_layer_in_place_when_other_home_layers_follow_it(self) -> None:
        from scripts import inject_home_product_carousel as subject

        source = (
            "<html><head><style id=\"later-home-style\"></style></head><body>"
            f"{subject.script_tag()}<script id=\"later-home-script\"></script>"
            "</body></html>"
        )

        self.assertEqual(subject.inject(source), source)


if __name__ == "__main__":
    unittest.main()
