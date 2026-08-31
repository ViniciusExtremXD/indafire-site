from __future__ import annotations

import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
HOME_CSS = ROOT / "wp-content" / "uploads" / "elementor" / "css" / "post-2.css"


class HomeReferenceCssTests(unittest.TestCase):
    def test_uses_the_published_services_and_brigada_responsive_rules(self) -> None:
        css = HOME_CSS.read_text(encoding="utf-8")

        self.assertNotIn("MODELO 1: CELULAR NA VERTICAL", css)
        self.assertNotIn("MODELO 2: CELULAR NA HORIZONTAL", css)
        self.assertNotIn("Brigada de Incêndio (.elementor-element-3662fd7)", css)
        self.assertIn(
            ".elementor-2 .elementor-element.elementor-element-3662fd7{padding:0px 0px 200px 0px;}",
            css,
        )
        self.assertIn(
            ".elementor-2 .elementor-element.elementor-element-9a752a9 > .elementor-widget-container{padding:2px 35px 2px 35px;}",
            css,
        )


if __name__ == "__main__":
    unittest.main()
