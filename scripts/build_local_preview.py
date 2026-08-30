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
from scripts import restore_static_hero_assets as hero_assets


ROOT = Path(__file__).resolve().parents[1]
INTERNAL_MARKER = 'id="indafire-internal-page-polish"'
CATALOG_MARKER = 'id="indafire-product-catalog-polish"'


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
        if route in {
            str(path.relative_to(ROOT)).replace("\\", "/")
            for path in catalog.TARGETS
        } and CATALOG_MARKER not in source:
            raise ValueError(f"Missing catalog polish in {route}")


def main() -> None:
    restored = hero_assets.restore_assets()
    catalog_changed = catalog.inject_styles(catalog.TARGETS)
    internal_changed = internal.inject_styles(internal.TARGETS)
    validate_documents(documents())
    print(
        "Local static preview ready: "
        f"{restored} asset(s) restored, {catalog_changed} catalog page(s) and "
        f"{internal_changed} internal page(s) refreshed."
    )


if __name__ == "__main__":
    main()
