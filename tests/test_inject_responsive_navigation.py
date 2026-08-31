from __future__ import annotations

import unittest
from pathlib import Path
from tempfile import TemporaryDirectory


class ResponsiveNavigationInjectionTests(unittest.TestCase):
    def test_injects_one_compact_navigation_layer_before_the_document_closes(self):
        from scripts import inject_responsive_navigation as subject

        source = (
            "<html><head></head><body>"
            '<div id="headerInda">'
            '<a class="top-level-link" href="/area-do-cliente/">Area do cliente</a>'
            '<div class="elementor-element-8755157"><a href="#menu">Menu</a></div>'
            "</div></body></html>"
        )

        rendered = subject.inject(source)

        self.assertEqual(rendered.count(f'id="{subject.STYLE_ID}"'), 1)
        self.assertEqual(rendered.count(f'id="{subject.SCRIPT_ID}"'), 1)
        self.assertLess(rendered.index(f'id="{subject.STYLE_ID}"'), rendered.index("</head>"))
        self.assertLess(rendered.index(f'id="{subject.SCRIPT_ID}"'), rendered.index("</body>"))
        self.assertIn("indafire-compact-client", rendered)
        self.assertIn("max-width: 1100px", rendered)
        self.assertIn("elementor-element-20668c0", rendered)
        self.assertIn("elementor-element-8755157", rendered)
        self.assertIn("aria-expanded", rendered)

    def test_replaces_its_managed_layers_without_duplication(self):
        from scripts import inject_responsive_navigation as subject

        with TemporaryDirectory() as directory:
            page = Path(directory) / "index.html"
            page.write_text("<html><head></head><body></body></html>", encoding="utf-8")

            self.assertEqual(subject.inject_assets((page,)), 1)
            self.assertEqual(subject.inject_assets((page,)), 0)
            rendered = page.read_text(encoding="utf-8")

        self.assertEqual(rendered.count(f'id="{subject.STYLE_ID}"'), 1)
        self.assertEqual(rendered.count(f'id="{subject.SCRIPT_ID}"'), 1)

    def test_ignores_incomplete_documents(self):
        from scripts import inject_responsive_navigation as subject

        self.assertEqual(subject.inject("<head></head>"), "<head></head>")


if __name__ == "__main__":
    unittest.main()
