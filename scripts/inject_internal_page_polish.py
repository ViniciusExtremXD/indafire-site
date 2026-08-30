"""Inject a light shared polish layer into each static Indafire route.

The export has one full HTML document per route.  This script keeps the
cross-page refinements in one repeatable place while preserving the existing
Elementor visual language and page-specific layout.
"""

from __future__ import annotations

from pathlib import Path
import re


ROOT = Path(__file__).resolve().parents[1]
STYLE_ID = "indafire-internal-page-polish"
TARGETS = (
    ROOT / "index.html",
    ROOT / "produtos" / "index.html",
    ROOT / "categoria-produto" / "extintores" / "index.html",
    ROOT / "produto" / "unidade-central-lux-700-1200-24vdc" / "index.html",
    ROOT / "produto" / "extintor-pqs-bc-4-kg-20bc" / "index.html",
    ROOT / "sobre-nos" / "index.html",
    ROOT / "treinamentos" / "index.html",
    ROOT / "contato" / "index.html",
    ROOT / "area-do-cliente" / "index.html",
    ROOT / "politica-de-privacidade" / "index.html",
)


CSS = r"""
/* INDAFIRE — shared finishing layer; keeps the established visual system. */
:root { --inda-focus-ring: rgba(227, 6, 19, 0.46); }

/* JetMenu keeps the overflow item in the DOM with [hidden]. A legacy flex
   rule can override the browser default and show a stray ellipsis. */
#headerInda .jet-responsive-menu-available-items[hidden] {
  display:none!important;
}

#headerInda a:focus-visible,
main a:focus-visible,
main button:focus-visible,
main input:focus-visible,
main select:focus-visible,
main textarea:focus-visible {
  outline: 3px solid var(--inda-focus-ring) !important;
  outline-offset: 3px !important;
}

/* Preserve page imagery and typography, only making interactive feedback
   consistent at desktop, portrait and landscape sizes. */
main .elementor-button,
main input,
main select,
main textarea {
  transition: border-color 160ms ease, box-shadow 160ms ease,
              transform 160ms ease, background-color 160ms ease;
}

main .elementor-button:hover {
  transform: translateY(-1px);
}

main input:focus,
main select:focus,
main textarea:focus {
  border-color: #e30613 !important;
  box-shadow: 0 0 0 3px rgba(227, 6, 19, 0.12) !important;
}

@media (max-width: 767px) {
  main input:not([type="checkbox"]):not([type="radio"]),
  main select,
  main textarea,
  main .elementor-button {
    min-height: 44px;
  }

  main textarea { min-height: 120px; }
}

@media (max-width: 1024px) and (orientation: landscape),
       (max-height: 620px) and (orientation: landscape) {
  main .elementor-button { min-height: 42px; }
}

@media (prefers-reduced-motion:reduce) {
  *, *::before, *::after {
    scroll-behavior: auto !important;
    animation-duration: 1ms !important;
    animation-iteration-count: 1 !important;
    transition-duration: 1ms !important;
  }
}
""".strip()


def style_tag() -> str:
    return f'<style id="{STYLE_ID}">\n{CSS}\n</style>'


def inject(source: str) -> str:
    pattern = re.compile(rf'<style id="{re.escape(STYLE_ID)}">.*?</style>\s*', re.DOTALL)
    stripped = pattern.sub("", source)
    if "</head>" not in stripped:
        return source
    catalog_style = '<style id="indafire-product-catalog-polish">'
    if catalog_style in stripped:
        return stripped.replace(
            catalog_style, f"{style_tag()}\n{catalog_style}", 1
        )
    return stripped.replace("</head>", f"{style_tag()}\n</head>", 1)


def inject_styles(targets: tuple[Path, ...] | list[Path]) -> int:
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


def main() -> None:
    missing = [path for path in TARGETS if not path.is_file()]
    if missing:
        names = ", ".join(str(path.relative_to(ROOT)) for path in missing)
        raise SystemExit(f"Missing static routes: {names}")
    print(f"Injected internal page polish into {inject_styles(TARGETS)} page(s).")


if __name__ == "__main__":
    main()
