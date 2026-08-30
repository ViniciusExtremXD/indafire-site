from __future__ import annotations

import importlib.util
from pathlib import Path
import sys
import tempfile
import unittest


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "inject_product_catalog_polish.py"


def load_module():
    spec = importlib.util.spec_from_file_location("product_catalog_polish", SCRIPT)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


class ProductCatalogPolishTests(unittest.TestCase):
    def test_injects_one_style_block_and_replaces_an_older_version(self):
        module = load_module()
        stale = '<style id="indafire-product-catalog-polish">old</style>'

        with tempfile.TemporaryDirectory() as temp_dir:
            page = Path(temp_dir) / "produtos" / "index.html"
            page.parent.mkdir(parents=True)
            page.write_text(
                f"<!doctype html><html><head>{stale}</head><body>Catalog</body></html>",
                encoding="utf-8",
            )

            changed = module.inject_styles((page,))
            rendered = page.read_text(encoding="utf-8")

        self.assertEqual(changed, 1)
        self.assertEqual(rendered.count('id="indafire-product-catalog-polish"'), 1)
        self.assertNotIn(">old</style>", rendered)
        self.assertIn("#bannerProdutoINDA", rendered)
        self.assertIn("wp-content/uploads/2021/11/produtos.jpg", rendered)
        self.assertIn("#bannerProdutoINDA > .elementor-container", rendered)
        self.assertLess(
            rendered.index('id="indafire-product-catalog-polish"'),
            rendered.index("</head>"),
        )

    def test_leaves_a_document_without_head_unchanged(self):
        module = load_module()

        with tempfile.TemporaryDirectory() as temp_dir:
            page = Path(temp_dir) / "index.html"
            original = "<!doctype html><html><body>Catalog</body></html>"
            page.write_text(original, encoding="utf-8")

            changed = module.inject_styles((page,))

            self.assertEqual(changed, 0)
            self.assertEqual(page.read_text(encoding="utf-8"), original)


if __name__ == "__main__":
    unittest.main()
