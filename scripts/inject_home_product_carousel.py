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
  var AUTOPLAY_DELAY = 2500;

  function createProgress(root) {
    var existing = root.parentElement && root.parentElement.querySelector(':scope > .indafire-carousel-progress[data-carousel="products"]');
    if (existing) return existing;
    var progress = document.createElement('div');
    progress.className = 'indafire-carousel-progress';
    progress.dataset.carousel = 'products';
    progress.setAttribute('aria-hidden', 'true');
    progress.style.setProperty('--indafire-carousel-duration', AUTOPLAY_DELAY + 'ms');
    progress.innerHTML = '<span class="indafire-carousel-progress__fill"></span>';
    root.insertAdjacentElement('afterend', progress);
    return progress;
  }

  function wireProductsAutoplay() {
    var root = document.querySelector('#carrosselProdutos');
    var next = root && root.querySelector('.elementor-swiper-button-next');
    if (!root || !next) return;

    var progress = createProgress(root);
    var reducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
    progress.dataset.reducedMotion = reducedMotion ? 'true' : 'false';
    var timer = 0;
    var hovering = false;
    var focusing = false;
    var pointerActive = false;
    var advancing = false;

    function isPaused() {
      return hovering || focusing || pointerActive || document.visibilityState !== 'visible';
    }

    function resetProgress() {
      var fill = progress.querySelector('.indafire-carousel-progress__fill');
      progress.classList.remove('is-running', 'is-paused');
      fill.style.animation = 'none';
      void fill.offsetWidth;
      fill.style.animation = '';
      progress.classList.add('is-running');
    }

    function schedule() {
      window.clearTimeout(timer);
      resetProgress();
      if (isPaused()) {
        progress.classList.add('is-paused');
        return;
      }
      timer = window.setTimeout(function () {
        advancing = true;
        next.click();
        advancing = false;
        schedule();
      }, AUTOPLAY_DELAY);
    }

    root.addEventListener('mouseenter', function () { hovering = true; schedule(); });
    root.addEventListener('mouseleave', function () { hovering = false; schedule(); });
    root.addEventListener('focusin', function () { focusing = true; schedule(); });
    root.addEventListener('focusout', function () {
      window.setTimeout(function () { focusing = root.contains(document.activeElement); schedule(); }, 0);
    });
    root.addEventListener('pointerdown', function () { pointerActive = true; schedule(); });
    root.addEventListener('pointerup', function () { pointerActive = false; schedule(); });
    root.addEventListener('pointercancel', function () { pointerActive = false; schedule(); });
    root.addEventListener('click', function (event) {
      if (!advancing && event.target.closest('.elementor-swiper-button, .swiper-pagination-bullet')) schedule();
    });
    document.addEventListener('visibilitychange', schedule);
    schedule();
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
