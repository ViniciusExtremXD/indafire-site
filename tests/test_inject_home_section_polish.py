from __future__ import annotations

import importlib.util
from pathlib import Path
import sys
import tempfile
import unittest


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "inject_home_section_polish.py"


def load_module():
    spec = importlib.util.spec_from_file_location("home_section_polish", SCRIPT)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


class HomeSectionPolishTests(unittest.TestCase):
    def test_replaces_the_home_layer_without_duplicates(self):
        module = load_module()
        stale = '<style id="indafire-home-section-polish">old</style>'

        with tempfile.TemporaryDirectory() as temp_dir:
            page = Path(temp_dir) / "index.html"
            page.write_text(f"<html><head>{stale}</head><body></body></html>", encoding="utf-8")
            changed = module.inject_styles((page,))
            rendered = page.read_text(encoding="utf-8")

        self.assertEqual(changed, 1)
        self.assertEqual(rendered.count('id="indafire-home-section-polish"'), 1)
        self.assertNotIn(">old</style>", rendered)
        self.assertIn("#carrosselServicos .swiper-slide", rendered)
        self.assertIn("#carrosselServicos .swiper-container", rendered)
        self.assertIn("#carrosselServicos > .elementor-widget-container", rendered)
        self.assertIn(".elementor-element-d88d016 > .elementor-container > .elementor-row", rendered)
        self.assertIn("flex-wrap: nowrap", rendered)
        self.assertIn(".elementor-element-f195a0e", rendered)

    def test_ignores_documents_without_a_head(self):
        module = load_module()
        with tempfile.TemporaryDirectory() as temp_dir:
            page = Path(temp_dir) / "index.html"
            original = "<body>Indafire</body>"
            page.write_text(original, encoding="utf-8")
            self.assertEqual(module.inject_styles((page,)), 0)
            self.assertEqual(page.read_text(encoding="utf-8"), original)


if __name__ == "__main__":
    unittest.main()
