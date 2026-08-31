from __future__ import annotations

import unittest
from pathlib import Path
import subprocess
import sys

from scripts.build_local_preview import validate_documents


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "build_local_preview.py"


class BuildLocalPreviewTests(unittest.TestCase):
    def test_accepts_every_expected_polish_marker(self):
        documents = {
            "index.html": (
                '<head><style id="indafire-internal-page-polish"></style>'
                '<style id="indafire-home-section-polish"></style></head>'
                '<body><script id="indafire-home-service-sync"></script>'
                '<script id="indafire-home-product-carousel"></script>'
                'INDAFIRE HOME BRIGADA REFERENCE</body>'
            ),
            "produtos/index.html": (
                '<head><style id="indafire-internal-page-polish"></style>'
                '<style id="indafire-product-catalog-polish"></style></head>'
            ),
        }

        validate_documents(documents)

    def test_rejects_an_internal_route_without_the_shared_layer(self):
        with self.assertRaisesRegex(ValueError, "internal polish"):
            validate_documents({"contato/index.html": "<head></head>"})

    def test_rejects_home_without_its_section_polish(self):
        source = '<head><style id="indafire-internal-page-polish"></style></head>'
        with self.assertRaisesRegex(ValueError, "home section polish"):
            validate_documents({"index.html": source})

    def test_rejects_home_without_service_sync(self):
        source = (
            '<head><style id="indafire-internal-page-polish"></style>'
            '<style id="indafire-home-section-polish"></style></head>'
            '<body><script id="indafire-home-product-carousel"></script>'
            'INDAFIRE HOME BRIGADA REFERENCE</body>'
        )
        with self.assertRaisesRegex(ValueError, "home service sync"):
            validate_documents({"index.html": source})

    def test_rejects_home_without_brigada_reference_polish(self):
        source = (
            '<head><style id="indafire-internal-page-polish"></style>'
            '<style id="indafire-home-section-polish"></style></head>'
            '<body><script id="indafire-home-service-sync"></script>'
            '<script id="indafire-home-product-carousel"></script></body>'
        )
        with self.assertRaisesRegex(ValueError, "Brigada reference"):
            validate_documents({"index.html": source})

    def test_rejects_home_without_the_products_carousel_layer(self):
        source = (
            '<head><style id="indafire-internal-page-polish"></style>'
            '<style id="indafire-home-section-polish"></style></head>'
            '<body><script id="indafire-home-service-sync"></script>'
            'INDAFIRE HOME BRIGADA REFERENCE</body>'
        )
        with self.assertRaisesRegex(ValueError, "Products carousel"):
            validate_documents({"index.html": source})

    def test_rejects_a_product_route_without_the_catalog_layer(self):
        source = '<head><style id="indafire-internal-page-polish"></style></head>'
        with self.assertRaisesRegex(ValueError, "catalog polish"):
            validate_documents({"produtos/index.html": source})

    def test_script_runs_directly_from_the_project_root(self):
        result = subprocess.run(
            [sys.executable, str(SCRIPT)],
            cwd=ROOT,
            check=False,
            capture_output=True,
            text=True,
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("Local static preview ready", result.stdout)

    def test_second_build_is_a_no_op(self):
        subprocess.run(
            [sys.executable, str(SCRIPT)],
            cwd=ROOT,
            check=True,
            capture_output=True,
            text=True,
        )
        result = subprocess.run(
            [sys.executable, str(SCRIPT)],
            cwd=ROOT,
            check=False,
            capture_output=True,
            text=True,
        )

        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("0 catalog page(s) and 0 internal page(s), 0 home page(s), 0 Brigada page(s), 0 service sync script(s), 0 Products carousel page(s) refreshed", result.stdout)


if __name__ == "__main__":
    unittest.main()
