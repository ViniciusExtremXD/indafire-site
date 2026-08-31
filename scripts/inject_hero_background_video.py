"""Use the original high-resolution video in the homepage hero background."""

from __future__ import annotations

from pathlib import Path
import re


ROOT = Path(__file__).resolve().parents[1]
TARGETS = (ROOT / "index.html",)
STYLE_ID = "indafire-hero-background-video-style"
SCRIPT_ID = "indafire-hero-background-video"
VIDEO_SOURCE = "https://indafire.com.br/wp-content/uploads/2021/10/banner-indafire.mp4"


CSS = r"""
/* INDAFIRE — native 1920px hero source, replacing the 640px YouTube embed. */
.elementor-element-98ce606 .elementor-background-video-container {
  overflow: hidden !important;
  background: #151515 !important;
}

.elementor-element-98ce606 .indafire-hero-background-video {
  position: absolute !important;
  inset: 0 !important;
  display: block !important;
  width: 100% !important;
  height: 100% !important;
  min-width: 100% !important;
  min-height: 100% !important;
  object-fit: cover !important;
  object-position: center center !important;
}

@media (max-width: 767px) and (orientation: portrait) {
  .elementor-element-98ce606 .indafire-hero-background-video {
    object-position: 56% center !important;
  }
}
""".strip()


JS = rf"""
(function () {{
  var HERO_SELECTOR = '.elementor-element-98ce606';
  var VIDEO_SOURCE = '{VIDEO_SOURCE}';

  function mountHighResolutionHeroVideo() {{
    var hero = document.querySelector(HERO_SELECTOR);
    var container = hero && hero.querySelector('.elementor-background-video-container');
    if (!container || container.querySelector('.indafire-hero-background-video')) return;

    var video = document.createElement('video');
    video.className = 'indafire-hero-background-video';
    video.src = VIDEO_SOURCE;
    video.autoplay = true;
    video.muted = true;
    video.loop = true;
    video.playsInline = true;
    video.preload = 'auto';
    video.setAttribute('aria-hidden', 'true');
    video.setAttribute('playsinline', '');
    container.replaceChildren(video);
    var playback = video.play();
    if (playback && typeof playback.catch === 'function') playback.catch(function () {{}});
  }}

  function initialise() {{
    mountHighResolutionHeroVideo();
    window.setTimeout(mountHighResolutionHeroVideo, 250);
    window.setTimeout(mountHighResolutionHeroVideo, 1200);
  }}

  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', initialise);
  else initialise();
}})();
""".strip()


def style_tag() -> str:
    return f'<style id="{STYLE_ID}">\n{CSS}\n</style>'


def script_tag() -> str:
    return f'<script id="{SCRIPT_ID}">\n{JS}\n</script>'


def inject(source: str) -> str:
    style_pattern = re.compile(rf'<style id="{re.escape(STYLE_ID)}">.*?</style>\s*', re.DOTALL)
    script_pattern = re.compile(rf'<script id="{re.escape(SCRIPT_ID)}">.*?</script>\s*', re.DOTALL)
    stripped = script_pattern.sub("", style_pattern.sub("", source))
    if "</head>" not in stripped or "</body>" not in stripped:
        return source
    internal_style_marker = '<style id="indafire-internal-page-polish">'
    home_style_marker = '<style id="indafire-home-section-polish">'
    if internal_style_marker in stripped:
        rendered = stripped.replace(internal_style_marker, f"{style_tag()}\n{internal_style_marker}", 1)
    elif home_style_marker in stripped:
        rendered = stripped.replace(home_style_marker, f"{style_tag()}\n{home_style_marker}", 1)
    else:
        rendered = stripped.replace("</head>", f"{style_tag()}\n</head>", 1)
    marker = '<script id="indafire-responsive-navigation">'
    if marker in rendered:
        return rendered.replace(marker, f"{script_tag()}\n{marker}", 1)
    return rendered.replace("</body>", f"{script_tag()}\n</body>", 1)


def inject_assets(targets: tuple[Path, ...] | list[Path]) -> int:
    changed = 0
    for page in targets:
        source = page.read_text(encoding="utf-8")
        rendered = inject(source)
        if rendered != source:
            page.write_text(rendered, encoding="utf-8")
            changed += 1
    return changed


if __name__ == "__main__":
    print(f"Injected high-resolution hero video into {inject_assets(TARGETS)} page(s).")
