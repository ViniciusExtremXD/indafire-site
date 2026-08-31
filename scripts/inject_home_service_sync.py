"""Keep the Home service detail card in sync with the visible carousel item."""

from __future__ import annotations

from pathlib import Path
import re


ROOT = Path(__file__).resolve().parents[1]
SCRIPT_ID = "indafire-home-service-sync"
TARGETS = (ROOT / "index.html",)


JS = r"""
(function () {
  function preloadServiceImages() {
    document.querySelectorAll('#gridServicos img').forEach(function (image) {
      image.loading = 'eager';
      image.decoding = 'async';
      if (!image.complete || !image.naturalWidth) {
        var preload = new Image();
        preload.src = image.currentSrc || image.src;
      }
    });
  }

  function syncServiceDetail() {
    var carousel = document.querySelector('#carrosselServicos .swiper-container');
    var selected = carousel && (carousel.querySelector('.swiper-slide-next') || carousel.querySelector('.swiper-slide-active'));
    var section = selected && selected.querySelector('section[id^="servico_"]');
    if (!section) return;

    var targetId = section.getAttribute('id');
    var number = targetId.replace('servico_', '');
    document.querySelectorAll('#gridServicos article').forEach(function (article) {
      var matchingDetail = article.querySelector('.' + targetId + ', #visualizacao_' + number);
      article.style.setProperty('display', matchingDetail ? 'block' : 'none', 'important');
    });
  }

  function wireServiceCarousel() {
    var carousel = document.querySelector('#carrosselServicos .swiper-container');
    var wrapper = carousel && carousel.querySelector('.swiper-wrapper');
    if (!carousel || !wrapper) return;

    preloadServiceImages();

    var timer;
    var scheduleSync = function () {
      clearTimeout(timer);
      timer = setTimeout(syncServiceDetail, 80);
    };

    new MutationObserver(scheduleSync).observe(wrapper, {
      attributes: true,
      subtree: true,
      attributeFilter: ['class']
    });

    if (carousel.swiper && typeof carousel.swiper.on === 'function') {
      ['slideChange', 'slideChangeTransitionEnd', 'transitionEnd'].forEach(function (eventName) {
        carousel.swiper.on(eventName, scheduleSync);
      });
    }

    carousel.addEventListener('transitionend', scheduleSync);
    scheduleSync();
    setTimeout(scheduleSync, 500);
    setTimeout(scheduleSync, 1500);
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', wireServiceCarousel);
  } else {
    wireServiceCarousel();
  }
})();
""".strip()


def script_tag() -> str:
    return f'<script id="{SCRIPT_ID}">\n{JS}\n</script>'


def inject(source: str) -> str:
    pattern = re.compile(rf'<script id="{re.escape(SCRIPT_ID)}">.*?</script>\s*', re.DOTALL)
    stripped = pattern.sub("", source)
    if "</body>" not in stripped:
        return source
    return stripped.replace("</body>", f"{script_tag()}\n</body>", 1)


def inject_scripts(targets: tuple[Path, ...] | list[Path]) -> int:
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
    print(f"Injected Home service synchronization into {inject_scripts(TARGETS)} page(s).")
