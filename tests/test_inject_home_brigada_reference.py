from __future__ import annotations

import unittest
from pathlib import Path
from tempfile import TemporaryDirectory

from scripts import update_home_brigada_reference as subject


class HomeBrigadaReferenceInjectionTests(unittest.TestCase):
    def test_injects_reference_brigada_block_into_the_applied_master_style(self) -> None:
        with TemporaryDirectory() as directory:
            page = Path(directory) / "index.html"
            page.write_text(
                '<html><head></head><body><style id="indafire-mobile-portrait-landscape-master-override">\n'
                '  /* DESKTOP BRIGADA DE INCÊNDIO & BOMBEIRO */\n'
                '  .elementor-element.elementor-element-3662fd7 {}\n'
                '  .elementor-element.elementor-element-8eed4f7 .elementor-button {\n  }\n'
                '</style></body></html>',
                encoding="utf-8",
            )

            changed = subject.inject_styles((page,))
            rendered = page.read_text(encoding="utf-8")

        self.assertEqual(changed, 1)
        self.assertIn(subject.MARKER, rendered)
        self.assertIn('id="indafire-mobile-portrait-landscape-master-override"', rendered)
        self.assertIn('background-image: url("./wp-content/uploads/2021/10/bombeiro.jpg") !important', rendered)
        self.assertIn('content: none !important', rendered)

    def test_injection_is_idempotent(self) -> None:
        with TemporaryDirectory() as directory:
            page = Path(directory) / "index.html"
            page.write_text(
                '<html><head></head><body><style id="indafire-mobile-portrait-landscape-master-override">\n'
                '  /* DESKTOP BRIGADA DE INCÊNDIO & BOMBEIRO */\n'
                '  .elementor-element.elementor-element-3662fd7 {}\n'
                '  .elementor-element.elementor-element-8eed4f7 .elementor-button {\n  }\n'
                '</style></body></html>',
                encoding="utf-8",
            )

            self.assertEqual(subject.inject_styles((page,)), 1)
            self.assertEqual(subject.inject_styles((page,)), 0)


if __name__ == "__main__":
    unittest.main()
