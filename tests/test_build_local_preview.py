from __future__ import annotations

import unittest
from pathlib import Path
import subprocess
import sys

from scripts.build_local_preview import validate_documents


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "build_local_preview.py"
NAV_STYLE = '<style id="indafire-responsive-navigation-style"></style>'
NAV_SCRIPT = '<script id="indafire-responsive-navigation"></script>'
HERO_VIDEO_SCRIPT = '<script id="indafire-hero-background-video"></script>'
SHARED_LOCATION_STYLE = '<style id="indafire-shared-location-style"></style>'
SERVICES_PAGE = '<main id="indafire-services-page"></main>'


class BuildLocalPreviewTests(unittest.TestCase):
    def test_accepts_every_expected_polish_marker(self):
        documents = {
            "index.html": (
                '<head><style id="indafire-internal-page-polish"></style>'
                '<style id="indafire-responsive-navigation-style"></style>'
                '<style id="indafire-home-section-polish"></style></head>'
                '<body><script id="indafire-home-service-sync"></script>'
                '<script id="indafire-home-product-carousel"></script>'
                f'{HERO_VIDEO_SCRIPT}'
                '<script id="indafire-responsive-navigation"></script>'
                'INDAFIRE HOME BRIGADA REFERENCE</body>'
            ),
            "produtos/index.html": (
                '<head><style id="indafire-internal-page-polish"></style>'
                '<style id="indafire-responsive-navigation-style"></style>'
                '<style id="indafire-product-catalog-polish"></style>'
                f'{SHARED_LOCATION_STYLE}</head>'
                '<body><section id="indafire-commercial-whatsapp"></section>'
                '<script id="indafire-responsive-navigation"></script></body>'
            ),
            "servicos/index.html": (
                '<head><style id="indafire-internal-page-polish"></style>'
                '<style id="indafire-responsive-navigation-style"></style>'
                f'{SHARED_LOCATION_STYLE}</head><body>{SERVICES_PAGE}'
                '<section id="indafire-commercial-whatsapp"></section>'
                '<script id="indafire-responsive-navigation"></script></body>'
            ),
        }

        validate_documents(documents)

    def test_rejects_an_internal_route_without_the_shared_layer(self):
        with self.assertRaisesRegex(ValueError, "internal polish"):
            validate_documents({"contato/index.html": "<head></head>"})

    def test_rejects_a_route_without_responsive_navigation(self):
        source = '<head><style id="indafire-internal-page-polish"></style></head>'
        with self.assertRaisesRegex(ValueError, "responsive navigation"):
            validate_documents({"contato/index.html": source})

    def test_rejects_home_without_its_section_polish(self):
        source = (
            '<head><style id="indafire-internal-page-polish"></style>'
            f'{NAV_STYLE}</head><body>{NAV_SCRIPT}</body>'
        )
        with self.assertRaisesRegex(ValueError, "home section polish"):
            validate_documents({"index.html": source})

    def test_rejects_home_without_service_sync(self):
        source = (
            '<head><style id="indafire-internal-page-polish"></style>'
            f'{NAV_STYLE}<style id="indafire-home-section-polish"></style></head>'
            '<body><script id="indafire-home-product-carousel"></script>'
            f'{HERO_VIDEO_SCRIPT}'
            f'{NAV_SCRIPT}'
            'INDAFIRE HOME BRIGADA REFERENCE</body>'
        )
        with self.assertRaisesRegex(ValueError, "home service sync"):
            validate_documents({"index.html": source})

    def test_rejects_home_without_brigada_reference_polish(self):
        source = (
            '<head><style id="indafire-internal-page-polish"></style>'
            f'{NAV_STYLE}<style id="indafire-home-section-polish"></style></head>'
            '<body><script id="indafire-home-service-sync"></script>'
            '<script id="indafire-home-product-carousel"></script>'
            f'{HERO_VIDEO_SCRIPT}'
            f'{NAV_SCRIPT}</body>'
        )
        with self.assertRaisesRegex(ValueError, "Brigada reference"):
            validate_documents({"index.html": source})

    def test_rejects_home_without_the_products_carousel_layer(self):
        source = (
            '<head><style id="indafire-internal-page-polish"></style>'
            f'{NAV_STYLE}<style id="indafire-home-section-polish"></style></head>'
            '<body><script id="indafire-home-service-sync"></script>'
            f'{HERO_VIDEO_SCRIPT}'
            f'{NAV_SCRIPT}INDAFIRE HOME BRIGADA REFERENCE</body>'
        )
        with self.assertRaisesRegex(ValueError, "Products carousel"):
            validate_documents({"index.html": source})

    def test_rejects_home_without_the_high_resolution_hero_video(self):
        source = (
            '<head><style id="indafire-internal-page-polish"></style>'
            f'{NAV_STYLE}<style id="indafire-home-section-polish"></style></head>'
            '<body><script id="indafire-home-service-sync"></script>'
            '<script id="indafire-home-product-carousel"></script>'
            f'{NAV_SCRIPT}INDAFIRE HOME BRIGADA REFERENCE</body>'
        )
        with self.assertRaisesRegex(ValueError, "high-resolution hero video"):
            validate_documents({"index.html": source})

    def test_rejects_a_product_route_without_the_catalog_layer(self):
        source = (
            '<head><style id="indafire-internal-page-polish"></style>'
            f'{NAV_STYLE}</head><body>{NAV_SCRIPT}</body>'
        )
        with self.assertRaisesRegex(ValueError, "catalog polish"):
            validate_documents({"produtos/index.html": source})

    def test_rejects_products_page_without_the_commercial_whatsapp_form(self):
        source = (
            '<head><style id="indafire-internal-page-polish"></style>'
            '<style id="indafire-product-catalog-polish"></style>'
            f'{NAV_STYLE}</head><body>{NAV_SCRIPT}</body>'
        )
        with self.assertRaisesRegex(ValueError, "commercial WhatsApp form"):
            validate_documents({"produtos/index.html": source})

    def test_rejects_products_page_without_the_shared_home_location(self):
        source = (
            '<head><style id="indafire-internal-page-polish"></style>'
            '<style id="indafire-product-catalog-polish"></style>'
            f'{NAV_STYLE}</head><body><section id="indafire-commercial-whatsapp"></section>'
            f'{NAV_SCRIPT}</body>'
        )
        with self.assertRaisesRegex(ValueError, "shared Home location"):
            validate_documents({"produtos/index.html": source})

    def test_rejects_services_page_without_the_managed_services_content(self):
        source = (
            '<head><style id="indafire-internal-page-polish"></style>'
            f'{NAV_STYLE}{SHARED_LOCATION_STYLE}</head><body>'
            '<section id="indafire-commercial-whatsapp"></section>'
            f'{NAV_SCRIPT}</body>'
        )
        with self.assertRaisesRegex(ValueError, "Services page"):
            validate_documents({"servicos/index.html": source})

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
        self.assertIn(
            "0 Services page(s), 0 shared location page(s), "
            "0 catalog page(s) and 0 commercial form page(s), "
            "0 internal page(s), 0 home page(s), "
            "0 responsive navigation page(s), 0 high-resolution hero video page(s), 0 Brigada page(s), "
            "0 service sync script(s), 0 Products carousel page(s) refreshed",
            result.stdout,
        )


if __name__ == "__main__":
    unittest.main()
