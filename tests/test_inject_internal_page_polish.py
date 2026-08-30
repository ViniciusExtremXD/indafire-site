import unittest

from scripts.inject_internal_page_polish import STYLE_ID, inject


class InternalPagePolishTests(unittest.TestCase):
    def test_inserts_master_once_before_head(self):
        source = "<html><head><title>Indafire</title></head><body></body></html>"

        rendered = inject(source)
        repeated = inject(rendered)

        self.assertIn(f'<style id="{STYLE_ID}">', rendered)
        self.assertLess(rendered.index(STYLE_ID), rendered.index("</head>"))
        self.assertEqual(repeated.count(f'id="{STYLE_ID}"'), 1)

    def test_master_preserves_header_menu_and_accessibility_guards(self):
        rendered = inject("<head></head>")

        self.assertIn(".jet-responsive-menu-available-items[hidden]", rendered)
        self.assertIn("display:none!important", rendered)
        self.assertIn(":focus-visible", rendered)
        self.assertIn("prefers-reduced-motion:reduce", rendered)

    def test_document_without_head_is_unchanged(self):
        source = "<html><body>Sem cabeçalho</body></html>"
        self.assertEqual(inject(source), source)


if __name__ == "__main__":
    unittest.main()
