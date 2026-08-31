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
        self.assertIn("max-width: 1100px", rendered)
        self.assertIn(".elementor-element-d88d016", rendered)
        self.assertIn("background-image: none", rendered)
        self.assertIn(".elementor-element-3fbc3d7", rendered)
        self.assertIn(".elementor-element-86cf7df", rendered)
        self.assertIn(".servicos_exibicao", rendered)
        self.assertIn("max-width: 520px", rendered)
        self.assertIn("background: #333333", rendered)
        self.assertIn(".indafire-carousel-progress", rendered)
        self.assertIn("opacity: .55", rendered)
        self.assertIn("transform: scaleX(1)", rendered)
        self.assertNotIn(".indafire-carousel-progress { display: none", rendered)
        self.assertIn(".elementor-element-f195a0e", rendered)
        self.assertRegex(
            rendered,
            r"(?m)^\.elementor-element-7974cb4\s*\{\s*display:\s*none\s*!important",
        )
        self.assertRegex(
            rendered,
            r"\.elementor-element-d88d016\s+\.indafire-carousel-progress\s*\{\s*display:\s*none\s*!important",
        )

    def test_adds_only_portrait_repairs_for_brigada_products_and_services(self):
        module = load_module()

        with tempfile.TemporaryDirectory() as temp_dir:
            page = Path(temp_dir) / "index.html"
            page.write_text("<html><head></head><body></body></html>", encoding="utf-8")
            module.inject_styles((page,))
            rendered = page.read_text(encoding="utf-8")

        self.assertIn("@media (max-width: 1100px) and (orientation: portrait)", rendered)
        self.assertIn(".elementor-element-3662fd7 .elementor-motion-effects-layer", rendered)
        self.assertIn("background-size: auto 44%", rendered)
        self.assertIn("background-position: 65% 100%", rendered)
        self.assertIn(
            "body.home .elementor-2 .elementor-element.elementor-element-9218be1 .elementor-main-swiper",
            rendered,
        )
        self.assertIn("height: 400px", rendered)
        self.assertIn(
            "body.home .elementor-2 .elementor-element.elementor-element-9218be1 .elementor-carousel-image",
            rendered,
        )
        self.assertIn("width: min(320px, calc(100vw - 72px))", rendered)
        self.assertIn("#gridServicos .servicos_exibicao > .elementor-container", rendered)
        self.assertIn("padding-bottom: 24px", rendered)
        self.assertIn("var(--indafire-carousel-duration, 2500ms)", rendered)

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
