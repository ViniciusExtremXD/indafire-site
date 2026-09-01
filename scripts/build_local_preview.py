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
from scripts import inject_responsive_navigation as responsive_navigation
from scripts import inject_hero_background_video as hero_video
from scripts import restore_static_hero_assets as hero_assets
from scripts import build_services_page as services_page
from scripts import sync_shared_location as shared_location


ROOT = Path(__file__).resolve().parents[1]
INTERNAL_MARKER = 'id="indafire-internal-page-polish"'
CATALOG_MARKER = 'id="indafire-product-catalog-polish"'
COMMERCIAL_FORM_MARKER = 'id="indafire-commercial-whatsapp"'
HOME_MARKER = 'id="indafire-home-section-polish"'
HOME_BRIGADA_MARKER = "INDAFIRE HOME BRIGADA REFERENCE"
HOME_SERVICE_MARKER = 'id="indafire-home-service-sync"'
HOME_PRODUCTS_MARKER = 'id="indafire-home-product-carousel"'
RESPONSIVE_NAV_STYLE_MARKER = 'id="indafire-responsive-navigation-style"'
RESPONSIVE_NAV_SCRIPT_MARKER = 'id="indafire-responsive-navigation"'
HERO_VIDEO_MARKER = 'id="indafire-hero-background-video"'
SERVICES_PAGE_MARKER = 'id="indafire-services-page"'
SHARED_LOCATION_MARKER = 'id="indafire-shared-location-style"'


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
        if RESPONSIVE_NAV_STYLE_MARKER not in source or RESPONSIVE_NAV_SCRIPT_MARKER not in source:
            raise ValueError(f"Missing responsive navigation in {route}")
        if route == "index.html" and HOME_MARKER not in source:
            raise ValueError(f"Missing home section polish in {route}")
        if route == "index.html" and HOME_BRIGADA_MARKER not in source:
            raise ValueError(f"Missing home Brigada reference polish in {route}")
        if route == "index.html" and HOME_SERVICE_MARKER not in source:
            raise ValueError(f"Missing home service sync in {route}")
        if route == "index.html" and HOME_PRODUCTS_MARKER not in source:
            raise ValueError(f"Missing home Products carousel in {route}")
        if route == "index.html" and HERO_VIDEO_MARKER not in source:
            raise ValueError(f"Missing high-resolution hero video in {route}")
        if route in {
            str(path.relative_to(ROOT)).replace("\\", "/")
            for path in catalog.TARGETS
        } and CATALOG_MARKER not in source:
            raise ValueError(f"Missing catalog polish in {route}")
        if route == "produtos/index.html" and COMMERCIAL_FORM_MARKER not in source:
            raise ValueError(f"Missing commercial WhatsApp form in {route}")
        if route in {"produtos/index.html", "servicos/index.html"} and SHARED_LOCATION_MARKER not in source:
            raise ValueError(f"Missing shared Home location in {route}")
        if route == "servicos/index.html" and SERVICES_PAGE_MARKER not in source:
            raise ValueError(f"Missing managed Services page in {route}")
        if route == "servicos/index.html" and COMMERCIAL_FORM_MARKER not in source:
            raise ValueError(f"Missing commercial WhatsApp form in {route}")


def main() -> None:
    restored = hero_assets.restore_assets()
    services_changed = services_page.build_services_page(
        ROOT / "sobre-nos" / "index.html",
        ROOT / "index.html",
        ROOT / "servicos" / "index.html",
    )
    location_changed = shared_location.sync_location(
        ROOT / "index.html",
        shared_location.TARGETS,
    )
    catalog_changed = catalog.inject_styles(catalog.TARGETS)
    commercial_form_changed = catalog.inject_commercial_form(catalog.PRODUCTS_PAGE)
    internal_changed = internal.inject_styles(internal.TARGETS)
    navigation_changed = responsive_navigation.inject_assets(responsive_navigation.TARGETS)
    hero_video_changed = hero_video.inject_assets(hero_video.TARGETS)
    home_changed = home_sections.inject_styles(home_sections.TARGETS)
    brigada_changed = home_brigada.inject_styles(home_brigada.TARGETS)
    products_changed = home_products.inject_assets(home_products.TARGETS)
    service_sync_changed = home_service_sync.inject_scripts(home_service_sync.TARGETS)
    validate_documents(documents())
    print(
        "Local static preview ready: "
        f"{restored} asset(s) restored, {services_changed} Services page(s), "
        f"{location_changed} shared location page(s), "
        f"{catalog_changed} catalog page(s) and "
        f"{commercial_form_changed} commercial form page(s), "
        f"{internal_changed} internal page(s), {home_changed} home page(s), "
        f"{navigation_changed} responsive navigation page(s), "
        f"{hero_video_changed} high-resolution hero video page(s), "
        f"{brigada_changed} Brigada page(s), "
        f"{service_sync_changed} service sync script(s), "
        f"{products_changed} Products carousel page(s) refreshed."
    )


if __name__ == "__main__":
    main()
