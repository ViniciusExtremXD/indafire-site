"""Keep the Home service detail card in sync with the visible carousel item."""

from __future__ import annotations

from pathlib import Path
import re


ROOT = Path(__file__).resolve().parents[1]
SCRIPT_ID = "indafire-home-service-sync"
TARGETS = (ROOT / "index.html",)


JS = r"""
(function () {
  var servicePreloads = [];

  function preloadServiceImages() {
    document.querySelectorAll('#gridServicos img').forEach(function (image) {
      image.loading = 'eager';
      image.decoding = 'async';
      image.fetchPriority = 'high';

      var source = image.currentSrc || image.src;
      if (!source) return;

      var preload = new Image();
      preload.src = source;
      servicePreloads.push(preload);

      if (typeof image.decode === 'function') image.decode().catch(function () {});
      if (typeof preload.decode === 'function') preload.decode().catch(function () {});
    });
  }

  function syncServiceDetail() {
    var carousel = document.querySelector('#carrosselServicos .swiper-container');
    var selected = carousel && (carousel.querySelector('.swiper-slide-next') || carousel.querySelector('.swiper-slide-active'));
    var section = selected && selected.querySelector('section[id^="servico_"]');
    if (!section) return;

    var targetId = section.getAttribute('id');
    var number = targetId.replace('servico_', '');
    var articles = document.querySelectorAll('#gridServicos article');
    articles.forEach(function (article) {
      var matchingDetail = article.querySelector('.' + targetId + ', #visualizacao_' + number);
      article.style.setProperty('display', matchingDetail ? 'block' : 'none', 'important');
    });
  }

  function wireServiceCarousel() {
    var carousel = document.querySelector('#carrosselServicos .swiper-container');
    var wrapper = carousel && carousel.querySelector('.swiper-wrapper');
    if (!carousel || !wrapper) return;

    preloadServiceImages();

    new MutationObserver(syncServiceDetail).observe(wrapper, {
      attributes: true,
      subtree: true,
      attributeFilter: ['class']
    });

    if (carousel.swiper && typeof carousel.swiper.on === 'function') {
      ['slideChange', 'transitionStart', 'slideChangeTransitionEnd', 'transitionEnd'].forEach(function (eventName) {
        carousel.swiper.on(eventName, syncServiceDetail);
      });
    }

    carousel.addEventListener('transitionend', syncServiceDetail);
    syncServiceDetail();
    setTimeout(syncServiceDetail, 500);
    setTimeout(syncServiceDetail, 1500);
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
    legacy_pattern = re.compile(
        r'\s*function\s+apagaServicos\s*\(\)\s*\{.*?'
        r'(?=\s*jQuery\s*\(\s*["\']#carrosselServicos \.dce-container-navigation["\'])',
        re.DOTALL,
    )
    stripped = pattern.sub("", source)
    stripped = legacy_pattern.sub("\n", stripped, count=1)
    stripped = re.sub(
        r'^\s*jQuery\s*\(\s*["\']#carrosselServicos \.dce-container-navigation["\']\s*\)'
        r'\.click[^\r\n]*\r?\n?',
        '',
        stripped,
        count=1,
        flags=re.MULTILINE,
    )
    stripped = re.sub(
        r'^\s*}\s*\);\s*\r?\n\s*mudaServicos_home\(\);\s*$',
        '',
        stripped,
        count=1,
        flags=re.MULTILINE,
    )
    stripped = re.sub(r'^\s*mudaServicos_home\(\);\s*$', '', stripped, count=1, flags=re.MULTILINE)
    stripped = re.sub(r'^\s*initServicesInteractive\(\);\s*$', '', stripped, flags=re.MULTILINE)
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
