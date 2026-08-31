"""Inject breakpoint-safe polish for the Indafire home sections.

It corrects the narrow desktop/tablet collision in the experience counters
and leaves the published Services layout and content unchanged.
"""

from __future__ import annotations

from pathlib import Path
import re


ROOT = Path(__file__).resolve().parents[1]
STYLE_ID = "indafire-home-section-polish"
TARGETS = (ROOT / "index.html",)


CSS = r"""
/* INDAFIRE — Home sectional polish: preserve the existing visual language. */

/* At intermediate desktop widths the original 50/50 counter internals were
   narrower than their figures. Stack each card internally to keep every
   value inside its own dark panel. */
@media (min-width: 768px) and (max-width: 1024px) {
  .elementor-element.elementor-element-bbbbf1b > .elementor-column-wrap > .elementor-widget-wrap {
    display: flex !important;
    flex-direction: row !important;
    align-items: stretch !important;
    justify-content: center !important;
    gap: 8px !important;
    width: 100% !important;
  }

  .elementor-element.elementor-element-f195a0e,
  .elementor-element.elementor-element-c8f1cd7,
  .elementor-element.elementor-element-8da6b11 {
    flex: 1 1 0 !important;
    width: auto !important;
    min-width: 0 !important;
    max-width: none !important;
    min-height: 164px !important;
    margin: 0 !important;
    padding: 12px 6px !important;
  }

  .elementor-element.elementor-element-f195a0e > .elementor-container > .elementor-row,
  .elementor-element.elementor-element-c8f1cd7 > .elementor-container > .elementor-row,
  .elementor-element.elementor-element-8da6b11 > .elementor-container > .elementor-row {
    flex-direction: column !important;
    align-items: center !important;
    justify-content: center !important;
    gap: 5px !important;
  }

  .elementor-element.elementor-element-a3dab2c,
  .elementor-element.elementor-element-b2860d9,
  .elementor-element.elementor-element-03ad2f7,
  .elementor-element.elementor-element-0bb67cf,
  .elementor-element.elementor-element-d21256a,
  .elementor-element.elementor-element-06d9a11 {
    flex: 0 0 auto !important;
    width: 100% !important;
    max-width: 100% !important;
    min-width: 0 !important;
    text-align: center !important;
    align-items: center !important;
  }

  .elementor-element.elementor-element-166d00a img,
  .elementor-element.elementor-element-312be29 img,
  .elementor-element.elementor-element-3bbd276 img {
    width: 34px !important;
    height: 34px !important;
    max-width: 34px !important;
    max-height: 34px !important;
  }

  .elementor-counter-number-wrapper {
    justify-content: center !important;
    width: 100% !important;
    max-width: 100% !important;
    min-width: 0 !important;
    font-size: 1.32rem !important;
  }

  .elementor-element.elementor-element-0bb67cf .elementor-widget-container,
  .elementor-element.elementor-element-d21256a .elementor-widget-container,
  .elementor-element.elementor-element-06d9a11 .elementor-widget-container,
  .elementor-element.elementor-element-0bb67cf .elementor-counter,
  .elementor-element.elementor-element-d21256a .elementor-counter,
  .elementor-element.elementor-element-06d9a11 .elementor-counter {
    width: 100% !important;
    max-width: 100% !important;
    min-width: 0 !important;
  }

  .elementor-element.elementor-element-0bb67cf .elementor-widget-counter .elementor-widget-container,
  .elementor-element.elementor-element-d21256a .elementor-widget-counter .elementor-widget-container,
  .elementor-element.elementor-element-06d9a11 .elementor-widget-counter .elementor-widget-container {
    margin: 0 !important;
  }

  .elementor-counter-number-prefix,
  .elementor-counter-number {
    font-size: 1.32rem !important;
  }

  .elementor-element.elementor-element-d2fc79d .elementor-heading-title,
  .elementor-element.elementor-element-e676369 .elementor-heading-title,
  .elementor-element.elementor-element-04ea4f9 .elementor-heading-title {
    max-width: 86px !important;
    margin: 0 auto !important;
    font-size: 0.66rem !important;
    line-height: 1.2 !important;
    text-align: center !important;
    overflow-wrap: anywhere;
  }

}
""".strip()


def style_tag() -> str:
    return f'<style id="{STYLE_ID}">\n{CSS}\n</style>'


def inject_styles(targets: tuple[Path, ...] | list[Path]) -> int:
    changed = 0
    pattern = re.compile(rf'<style id="{re.escape(STYLE_ID)}">.*?</style>\s*', re.DOTALL)
    replacement = style_tag() + "\n"
    for page in targets:
        with page.open("r", encoding="utf-8", newline="") as handle:
            source = handle.read()
        stripped = pattern.sub("", source)
        if "</head>" not in stripped:
            continue
        rendered = stripped.replace("</head>", f"{replacement}</head>", 1)
        if rendered != source:
            with page.open("w", encoding="utf-8", newline="") as handle:
                handle.write(rendered)
            changed += 1
    return changed


if __name__ == "__main__":
    print(f"Injected home section polish into {inject_styles(TARGETS)} page(s).")
