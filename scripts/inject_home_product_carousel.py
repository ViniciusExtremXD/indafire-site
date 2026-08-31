"""Keep the existing Home Products carousel visual treatment and add autoplay."""

from __future__ import annotations

from pathlib import Path
import re


ROOT = Path(__file__).resolve().parents[1]
# Kept as a cleanup identifier for the visual layer that was added in error.
STYLE_ID = "indafire-home-product-carousel-style"
SCRIPT_ID = "indafire-home-product-carousel"
TARGETS = (ROOT / "index.html",)


JS = r"""
(function () {
  function wireProductsAutoplay() {
    var root = document.querySelector('#carrosselProdutos');
    var next = root && root.querySelector('.elementor-swiper-button-next');
    if (!root || !next) return;

    var paused = false;
    var pause = function () { paused = true; };
    var resume = function () { paused = false; };

    root.addEventListener('mouseenter', pause);
    root.addEventListener('mouseleave', resume);
    root.addEventListener('focusin', pause);
    root.addEventListener('focusout', resume);

    window.setInterval(function () {
      if (!paused && document.visibilityState === 'visible') next.click();
    }, 5000);
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', wireProductsAutoplay);
  } else {
    wireProductsAutoplay();
  }
})();
""".strip()


def script_tag() -> str:
    return f'<script id="{SCRIPT_ID}">\n{JS}\n</script>'


def inject(source: str) -> str:
    style_pattern = re.compile(
        rf'<style id="{re.escape(STYLE_ID)}">.*?</style>\s*', re.DOTALL
    )
    script_pattern = re.compile(
        rf'<script id="{re.escape(SCRIPT_ID)}">.*?</script>\s*', re.DOTALL
    )
    if STYLE_ID not in source and script_tag() in source:
        return source

    stripped = script_pattern.sub("", style_pattern.sub("", source))
    if "</body>" not in stripped:
        return source
    return stripped.replace("</body>", f"{script_tag()}\n</body>", 1)


def inject_assets(targets: tuple[Path, ...] | list[Path]) -> int:
    changed = 0
    for page in targets:
        with page.open("r", encoding="utf-8", newline="") as handle:
            source = handle.read()
        rendered = inject(source)
        if rendered != source:
            with page.open("w", encoding="utf-8", newline="") as handle:
                handle.write(rendered)
            changed += 1
    return changed


if __name__ == "__main__":
    print(f"Injected Home Products autoplay into {inject_assets(TARGETS)} page(s).")
