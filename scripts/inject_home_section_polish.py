"""Inject breakpoint-safe polish for the Indafire home sections.

It corrects the narrow desktop/tablet collision in the experience counters,
keeps the service carousel legible, and leaves the established visual design
and content unchanged.
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

  html body #carrosselServicos {
    padding: 4px 42px !important;
  }

  html body #carrosselServicos > .elementor-widget-container {
    padding: 0 !important;
  }

  html body #carrosselServicos .swiper-slide {
    width: 100% !important;
    padding: 6px !important;
  }

  html body #carrosselServicos .swiper-container {
    width: 100% !important;
    max-width: 100% !important;
    box-sizing: border-box !important;
  }

  html body #carrosselServicos .servico_unidade_carrossel {
    min-height: 142px !important;
    padding: 12px 8px !important;
  }

  html body #carrosselServicos .servico_unidade_carrossel h4 {
    font-size: 0.76rem !important;
    line-height: 1.22 !important;
  }

  html body #carrosselServicos .dce-container-navigation {
    position: absolute !important;
    inset: 0 !important;
    width: auto !important;
    height: auto !important;
    pointer-events: none !important;
  }

  html body #carrosselServicos .swiper-button-prev,
  html body #carrosselServicos .swiper-button-next {
    width: 34px !important;
    height: 34px !important;
    top: 50% !important;
    margin: 0 !important;
    transform: translateY(-50%) !important;
    pointer-events: auto !important;
  }

  html body #carrosselServicos .swiper-button-prev { left: -36px !important; }
  html body #carrosselServicos .swiper-button-next { right: -36px !important; }
}

@media (max-width: 767px) {
  /* Portrait phones need the existing carousel and detail card to flow as
     one readable column; the export keeps these two 50% columns side by
     side and pushes the detail card outside the viewport. */
  html body.home .elementor-element-d88d016 > .elementor-container > .elementor-row {
    flex-direction: column !important;
    flex-wrap: nowrap !important;
    align-items: stretch !important;
    height: auto !important;
  }

  html body .elementor-element-d88d016 > .elementor-container > .elementor-row > .elementor-element-c99c7c0,
  html body .elementor-element-d88d016 > .elementor-container > .elementor-row > .elementor-element-c54c22f {
    flex: 0 0 auto !important;
    width: 100% !important;
    max-width: 100% !important;
    height: auto !important;
    min-height: 0 !important;
  }

  html body.home .elementor-element-c99c7c0,
  html body.home .elementor-element-c54c22f {
    height: auto !important;
    align-self: flex-start !important;
  }

  html body .elementor-element-c54c22f {
    margin-top: 16px !important;
  }

  html body #gridServicos,
  html body #gridServicos .dce-posts-container,
  html body #gridServicos article {
    width: 100% !important;
    max-width: 100% !important;
  }

  html body #carrosselServicos { padding-right: 30px !important; padding-left: 30px !important; }

  html body #carrosselServicos > .elementor-widget-container { padding: 0 !important; }

  html body #carrosselServicos .swiper-container {
    width: 100% !important;
    max-width: 100% !important;
    box-sizing: border-box !important;
  }

  html body #carrosselServicos .swiper-slide { width: 100% !important; }

  html body #carrosselServicos .swiper-button-prev,
  html body #carrosselServicos .swiper-button-next {
    width: 30px !important;
    height: 30px !important;
    top: 50% !important;
    margin: 0 !important;
    transform: translateY(-50%) !important;
  }

  html body #carrosselServicos .swiper-button-prev { left: -30px !important; }
  html body #carrosselServicos .swiper-button-next { right: -30px !important; }
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
