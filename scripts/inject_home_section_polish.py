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

/* Remove the legacy red connector artwork between the Services cards and
   detail panel. It is decorative and collides with the modernized spacing. */
.elementor-element-7974cb4 {
  display: none !important;
}

/* The Services carousel already communicates state through the active card.
   Keep the Products progress indicator, but remove this redundant red rule. */
.elementor-element-d88d016 .indafire-carousel-progress {
  display: none !important;
}

/* At intermediate desktop widths the original 50/50 counter internals were
   narrower than their figures. Stack each card internally to keep every
   value inside its own dark panel. */
@media (min-width: 768px) and (max-width: 1100px) {
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

/* Keep Services stacked until both columns have enough room for the original
   image treatment. This extends Elementor's tablet behavior without changing
   the desktop composition or any source asset. */
@media (min-width: 768px) and (max-width: 1100px) {
  .elementor-element.elementor-element-d88d016 > .elementor-container > .elementor-row {
    display: flex !important;
    flex-flow: row wrap !important;
  }

  .elementor-element.elementor-element-c99c7c0,
  .elementor-element.elementor-element-c54c22f {
    flex: 0 0 100% !important;
    width: 100% !important;
    max-width: 100% !important;
  }

  .elementor-element.elementor-element-c54c22f > .elementor-element-populated {
    margin: 0 0 30px !important;
  }

  .elementor-319 .elementor-element.elementor-element-ef36f3b {
    margin-top: 0 !important;
  }

  #gridServicos {
    height: auto !important;
  }
}

@media (max-width: 1100px) {
  .elementor-element.elementor-element-3fbc3d7,
  .elementor-element.elementor-element-d88d016 {
    background-image: none !important;
  }

  .elementor-element.elementor-element-3fbc3d7 > .elementor-container > .elementor-row {
    display: flex !important;
    flex-flow: row nowrap !important;
  }

  .elementor-element.elementor-element-23a9c77 {
    flex: 1 1 100% !important;
    width: 100% !important;
    max-width: 100% !important;
  }

  .elementor-element.elementor-element-86cf7df {
    display: none !important;
  }

  .elementor-element.elementor-element-c54c22f > .elementor-element-populated {
    background-image: none !important;
  }

  #gridServicos .dce-posts-wrapper {
    display: flex !important;
    flex-direction: column !important;
    align-items: center !important;
  }

  #gridServicos article {
    width: 100% !important;
    max-width: 550px !important;
    margin: 0 auto !important;
    padding: 0 15px 35px !important;
  }

  #gridServicos .servicos_exibicao {
    width: 100% !important;
    max-width: 520px !important;
    margin: 0 auto !important;
    overflow: hidden !important;
    border-radius: 14px !important;
    background: #333333 !important;
    box-shadow: 0 12px 28px rgba(0, 0, 0, .16) !important;
  }

  #gridServicos .servicos_exibicao > .elementor-container {
    width: 100% !important;
    max-width: 520px !important;
  }
}

/* Portrait-only repairs. Keep the current design intact while giving the
   firefighter, detail CTA and product artwork the room they need. */
@media (max-width: 1100px) and (orientation: portrait) {
  .elementor-element.elementor-element-3662fd7 {
    min-height: 980px !important;
    overflow: hidden !important;
  }

  .elementor-element.elementor-element-3662fd7 .elementor-motion-effects-layer {
    width: 100% !important;
    left: 0 !important;
    transform: none !important;
    background-size: auto 44% !important;
    background-position: 65% 100% !important;
    background-repeat: no-repeat !important;
  }

  #gridServicos .servicos_exibicao > .elementor-container {
    box-sizing: border-box !important;
    padding-bottom: 24px !important;
  }
}

@media (max-width: 767px) and (orientation: portrait) {
  body.home .elementor-2 .elementor-element.elementor-element-9218be1 .elementor-main-swiper {
    width: 100% !important;
    max-width: 400px !important;
    height: 400px !important;
  }

  body.home .elementor-2 .elementor-element.elementor-element-9218be1 .elementor-carousel-image {
    width: min(320px, calc(100vw - 72px)) !important;
    max-width: 320px !important;
    height: 350px !important;
    min-height: 350px !important;
  }
}

.indafire-carousel-progress {
  position: relative;
  width: min(220px, 58%);
  height: 3px;
  margin: 14px auto 0;
  overflow: hidden;
  border-radius: 999px;
  background: rgba(30, 30, 30, .16);
}

.indafire-carousel-progress__fill {
  display: block;
  width: 100%;
  height: 100%;
  border-radius: inherit;
  background: #e30613;
  transform: scaleX(0);
  transform-origin: left center;
}

.indafire-carousel-progress.is-running .indafire-carousel-progress__fill {
  animation: indafire-carousel-progress var(--indafire-carousel-duration, 2500ms) linear forwards;
}

.indafire-carousel-progress.is-paused .indafire-carousel-progress__fill {
  animation-play-state: paused;
}

@keyframes indafire-carousel-progress {
  from { transform: scaleX(0); }
  to { transform: scaleX(1); }
}

@media (prefers-reduced-motion: reduce) {
  .indafire-carousel-progress { opacity: .55; }
  .indafire-carousel-progress .indafire-carousel-progress__fill {
    animation: none !important;
    transform: scaleX(1) !important;
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
        source = page.read_text(encoding="utf-8")
        stripped = pattern.sub("", source)
        if "</head>" not in stripped:
            continue
        rendered = stripped.replace("</head>", f"{replacement}</head>", 1)
        if rendered != source:
            page.write_text(rendered, encoding="utf-8")
            changed += 1
    return changed


if __name__ == "__main__":
    print(f"Injected home section polish into {inject_styles(TARGETS)} page(s).")
