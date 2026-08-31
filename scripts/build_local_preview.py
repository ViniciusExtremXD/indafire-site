"""Reproduce the local static Indafire preview from the checked-out sources.

This is intentionally non-destructive: it refreshes only the two managed
style layers and the original hero assets that the static HTML already uses.
It does not touch the GitHub Pages export directory.
"""

from __future__ import annotations

from pathlib import Path
import sys


if __package__ in {None, ""}:
    # Direct execution places ``scripts/`` on sys.path, while the managed
    # helpers live in the project-root namespace.
    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from scripts import inject_internal_page_polish as internal
from scripts import inject_product_catalog_polish as catalog
from scripts import inject_home_section_polish as home_sections
from scripts import update_home_brigada_reference as home_brigada
from scripts import inject_home_service_sync as home_service_sync
from scripts import inject_home_product_carousel as home_products
from scripts import restore_static_hero_assets as hero_assets


ROOT = Path(__file__).resolve().parents[1]
INTERNAL_MARKER = 'id="indafire-internal-page-polish"'
CATALOG_MARKER = 'id="indafire-product-catalog-polish"'
HOME_MARKER = 'id="indafire-home-section-polish"'
HOME_BRIGADA_MARKER = "INDAFIRE HOME BRIGADA REFERENCE"
HOME_SERVICE_MARKER = 'id="indafire-home-service-sync"'
HOME_PRODUCTS_MARKER = 'id="indafire-home-product-carousel"'


def documents() -> dict[str, str]:
    return {
        str(path.relative_to(ROOT)).replace("\\", "/"): path.read_text(
            encoding="utf-8"
        )
        for path in internal.TARGETS
    }


def validate_documents(pages: dict[str, str]) -> None:
    for route, source in pages.items():
        if INTERNAL_MARKER not in source:
            raise ValueError(f"Missing internal polish in {route}")
        if route == "index.html" and HOME_MARKER not in source:
            raise ValueError(f"Missing home section polish in {route}")
        if route == "index.html" and HOME_BRIGADA_MARKER not in source:
            raise ValueError(f"Missing home Brigada reference polish in {route}")
        if route == "index.html" and HOME_SERVICE_MARKER not in source:
            raise ValueError(f"Missing home service sync in {route}")
        if route == "index.html" and HOME_PRODUCTS_MARKER not in source:
            raise ValueError(f"Missing home Products carousel in {route}")
        if route in {
            str(path.relative_to(ROOT)).replace("\\", "/")
            for path in catalog.TARGETS
        } and CATALOG_MARKER not in source:
            raise ValueError(f"Missing catalog polish in {route}")


def main() -> None:
    restored = hero_assets.restore_assets()
    catalog_changed = catalog.inject_styles(catalog.TARGETS)
    internal_changed = internal.inject_styles(internal.TARGETS)
    home_changed = home_sections.inject_styles(home_sections.TARGETS)
    brigada_changed = home_brigada.inject_styles(home_brigada.TARGETS)
    service_sync_changed = home_service_sync.inject_scripts(home_service_sync.TARGETS)
    products_changed = home_products.inject_assets(home_products.TARGETS)
    validate_documents(documents())
    print(
        "Local static preview ready: "
        f"{restored} asset(s) restored, {catalog_changed} catalog page(s) and "
        f"{internal_changed} internal page(s), {home_changed} home page(s), "
        f"{brigada_changed} Brigada page(s), "
        f"{service_sync_changed} service sync script(s), "
        f"{products_changed} Products carousel page(s) refreshed."
    )


if __name__ == "__main__":
    main()
