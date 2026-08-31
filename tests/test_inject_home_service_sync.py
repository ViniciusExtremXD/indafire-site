from __future__ import annotations

import importlib.util
from pathlib import Path
import sys
import tempfile
import unittest


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "inject_home_service_sync.py"


def load_module():
    spec = importlib.util.spec_from_file_location("home_service_sync", SCRIPT)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


class HomeServiceSyncTests(unittest.TestCase):
    def test_injects_one_idempotent_sync_script(self):
        module = load_module()
        stale = '<script id="indafire-home-service-sync">old</script>'
        legacy = """<script>
function apagaServicos(){
  jQuery("#gridServicos article").each(function(){ jQuery(this).css("display","none"); });
}
function mudaServicos_home(){
  apagaServicos();
  setTimeout(function(){
    var idSlider_meio = jQuery("#carrosselServicos .swiper-slide-next section").attr("id");
  }, 100);
}
jQuery("#carrosselServicos .dce-container-navigation").click(function(){ mudaServicos_home(); });
</script>"""

        with tempfile.TemporaryDirectory() as temp_dir:
            page = Path(temp_dir) / "index.html"
            page.write_text(f"<html><body>{legacy}{stale}</body></html>", encoding="utf-8")
            self.assertEqual(module.inject_scripts((page,)), 1)
            rendered = page.read_text(encoding="utf-8")
            self.assertEqual(module.inject_scripts((page,)), 0)

        self.assertEqual(rendered.count('id="indafire-home-service-sync"'), 1)
        self.assertNotIn(">old</script>", rendered)
        self.assertIn("swiper-slide-next", rendered)
        self.assertIn("MutationObserver", rendered)
        self.assertIn("visualizacao_", rendered)
        self.assertIn("preloadServiceImages", rendered)
        self.assertIn("loading = 'eager'", rendered)
        self.assertIn("image.decode()", rendered)
        self.assertIn("new MutationObserver(syncServiceDetail)", rendered)
        self.assertNotIn("function apagaServicos", rendered)
        self.assertNotIn("mudaServicos_home", rendered)
        self.assertNotIn("setTimeout(syncServiceDetail, 80)", rendered)

    def test_ignores_documents_without_a_body(self):
        module = load_module()
        with tempfile.TemporaryDirectory() as temp_dir:
            page = Path(temp_dir) / "index.html"
            original = "<head></head>"
            page.write_text(original, encoding="utf-8")
            self.assertEqual(module.inject_scripts((page,)), 0)
            self.assertEqual(page.read_text(encoding="utf-8"), original)


if __name__ == "__main__":
    unittest.main()
