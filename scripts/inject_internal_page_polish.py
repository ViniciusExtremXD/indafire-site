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
    ROOT / "servicos" / "index.html",
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

/* The exported footer lets the brand asset grow to its intrinsic width on
   some routes. Keep its familiar treatment while giving it a dependable,
   proportional cap at every breakpoint. */
.elementor-element.elementor-element-95a2442 .elementor-image {
  display: flex !important;
  align-items: center !important;
  justify-content: flex-end !important;
}

.elementor-element.elementor-element-95a2442 img {
  display: block !important;
  width: min(100%, 260px) !important;
  max-width: 260px !important;
  height: auto !important;
}

@media (min-width: 768px) and (max-width: 1024px) {
  .elementor-element.elementor-element-95a2442 img {
    width: min(100%, 210px) !important;
    max-width: 210px !important;
  }
}

@media (max-width: 767px) {
  main input:not([type="checkbox"]):not([type="radio"]),
  main select,
  main textarea,
  main .elementor-button {
    min-height: 44px;
  }

  main textarea { min-height: 120px; }

  .elementor-element.elementor-element-95a2442 {
    width: 100% !important;
    margin: 20px auto 0 !important;
  }

  .elementor-element.elementor-element-95a2442 .elementor-image {
    justify-content: center !important;
  }

  .elementor-element.elementor-element-95a2442 img {
    width: min(72vw, 230px) !important;
    max-width: 230px !important;
  }
}

@media (max-width: 1024px) and (orientation: landscape),
       (max-height: 620px) and (orientation: landscape) {
  main .elementor-button { min-height: 42px; }

  /* The archive sliders already animate inside their viewport.  Contain
     off-screen slides so a landscape phone never gains a page-wide rail. */
  main .elementor-widget-dce-dynamicposts-v2 .dce-posts-container {
    max-width: 100% !important;
    overflow: hidden !important;
  }

  /* Elementor marks this as hidden on tablet; the exported responsive
     stylesheet misses the compact landscape range on some routes. */
  #headerInda .elementor-hidden-tablet { display: none !important; }
}

/* Standardized responsive styling for newsletter and catalog forms (#formulariosRodape) */
#formulariosRodape {
  padding: 60px 20px !important;
  box-sizing: border-box !important;
}

#formulariosRodape .elementor-container {
  max-width: 1140px !important;
  margin: 0 auto !important;
  width: 100% !important;
}

#formulariosRodape .elementor-row {
  display: flex !important;
  flex-wrap: wrap !important;
  gap: 32px !important;
  justify-content: center !important;
  align-items: stretch !important;
}

#formulariosRodape .elementor-column.elementor-col-50 {
  flex: 1 1 calc(50% - 16px) !important;
  max-width: 530px !important;
  min-width: 290px !important;
  width: auto !important;
  display: flex !important;
}

#formulariosRodape .elementor-element-21b9e52 > .elementor-column-wrap,
#formulariosRodape .elementor-element-f3b6b56 > .elementor-column-wrap {
  background: rgba(22, 27, 34, 0.95) !important;
  border: 1px solid rgba(255, 255, 255, 0.12) !important;
  border-radius: 20px !important;
  padding: 36px 30px !important;
  box-shadow: 0 16px 40px rgba(0, 0, 0, 0.45) !important;
  display: flex !important;
  flex-direction: column !important;
  justify-content: space-between !important;
  box-sizing: border-box !important;
  transition: transform 0.3s ease, border-color 0.3s ease, box-shadow 0.3s ease !important;
}

#formulariosRodape .elementor-element-21b9e52 > .elementor-column-wrap:hover,
#formulariosRodape .elementor-element-f3b6b56 > .elementor-column-wrap:hover {
  border-color: rgba(227, 6, 19, 0.5) !important;
  transform: translateY(-4px) !important;
  box-shadow: 0 20px 45px rgba(227, 6, 19, 0.15) !important;
}

#formulariosRodape .elementor-widget-wrap {
  display: flex !important;
  flex-direction: column !important;
  height: 100% !important;
  padding: 0 !important;
}

#formulariosRodape .elementor-element-faab318,
#formulariosRodape .elementor-element-ba015bc {
  margin-bottom: 20px !important;
  text-align: center !important;
}

#formulariosRodape .elementor-element-faab318 img,
#formulariosRodape .elementor-element-ba015bc img {
  height: 120px !important;
  width: auto !important;
  margin: 0 auto !important;
  display: block !important;
  object-fit: contain !important;
  filter: drop-shadow(0 8px 18px rgba(0, 0, 0, 0.5)) !important;
}

#formulariosRodape .elementor-widget-heading .elementor-heading-title {
  color: #ffffff !important;
  font-size: 1.45rem !important;
  font-weight: 700 !important;
  text-align: center !important;
  margin-bottom: 10px !important;
  letter-spacing: 0.3px !important;
}

#formulariosRodape .elementor-widget-text-editor {
  color: #c0c6cc !important;
  font-size: 0.95rem !important;
  line-height: 1.5 !important;
  text-align: center !important;
  margin-bottom: 24px !important;
}

#formulariosRodape .elementor-field-textual {
  background: rgba(255, 255, 255, 0.07) !important;
  border: 1px solid rgba(255, 255, 255, 0.18) !important;
  border-radius: 8px !important;
  color: #ffffff !important;
  padding: 12px 16px !important;
  font-size: 14px !important;
  width: 100% !important;
  box-sizing: border-box !important;
  transition: all 0.2s ease !important;
}

#formulariosRodape .elementor-field-textual:focus {
  border-color: #e30613 !important;
  background: rgba(255, 255, 255, 0.12) !important;
  outline: none !important;
  box-shadow: 0 0 0 2px rgba(227, 6, 19, 0.25) !important;
}

#formulariosRodape .elementor-field-textual::placeholder {
  color: #88939e !important;
}

#formulariosRodape .elementor-field-group {
  margin-bottom: 12px !important;
  padding: 0 !important;
  width: 100% !important;
}

#formulariosRodape .elementor-field-type-radio,
#formulariosRodape .elementor-field-type-checkbox {
  margin-top: 6px !important;
  margin-bottom: 10px !important;
}

#formulariosRodape .elementor-field-subgroup {
  display: flex !important;
  flex-direction: column !important;
  align-items: flex-start !important;
  text-align: left !important;
  gap: 8px !important;
  width: 100% !important;
}

#formulariosRodape .elementor-field-option {
  display: flex !important;
  align-items: flex-start !important;
  gap: 10px !important;
  width: 100% !important;
  cursor: pointer !important;
}

#formulariosRodape .elementor-field-option input[type="radio"],
#formulariosRodape .elementor-field-option input[type="checkbox"] {
  margin-top: 3px !important;
  accent-color: #e30613 !important;
  flex-shrink: 0 !important;
  width: 16px !important;
  height: 16px !important;
  cursor: pointer !important;
}

#formulariosRodape .elementor-field-option label {
  color: #b0b8c1 !important;
  font-size: 13px !important;
  line-height: 1.45 !important;
  cursor: pointer !important;
  overflow-wrap: anywhere !important;
  word-break: normal !important;
}

#formulariosRodape .elementor-field-option label a {
  color: #e30613 !important;
  text-decoration: underline !important;
}

#formulariosRodape .elementor-button {
  background-color: #e30613 !important;
  color: #ffffff !important;
  border: none !important;
  border-radius: 8px !important;
  padding: 14px 28px !important;
  font-size: 15px !important;
  font-weight: 700 !important;
  letter-spacing: 0.5px !important;
  width: 100% !important;
  text-align: center !important;
  display: block !important;
  box-shadow: 0 4px 16px rgba(227, 6, 19, 0.4) !important;
  cursor: pointer !important;
  transition: all 0.25s ease !important;
}

#formulariosRodape .elementor-button:hover {
  background-color: #c40410 !important;
  transform: translateY(-2px) !important;
  box-shadow: 0 6px 22px rgba(227, 6, 19, 0.55) !important;
}

@media (max-width: 991px) {
  #formulariosRodape {
    width: 100% !important;
    padding: 40px 16px !important;
    overflow: hidden !important;
  }

  #formulariosRodape .elementor-container,
  #formulariosRodape .elementor-row,
  #formulariosRodape .elementor-column,
  #formulariosRodape .elementor-column-wrap,
  #formulariosRodape .elementor-widget-wrap,
  #formulariosRodape .elementor-widget-form,
  #formulariosRodape .elementor-widget-form .elementor-widget-container,
  #formulariosRodape .elementor-form,
  #formulariosRodape .elementor-form-fields-wrapper {
    width: 100% !important;
    max-width: 100% !important;
    min-width: 0 !important;
    box-sizing: border-box !important;
  }

  #formulariosRodape .elementor-container {
    display: block !important;
  }

  #formulariosRodape .elementor-row {
    display: flex !important;
    flex-direction: column !important;
    align-items: center !important;
    gap: 28px !important;
  }

  #formulariosRodape .elementor-column.elementor-col-50 {
    width: 100% !important;
    max-width: 520px !important;
    min-width: 0 !important;
    display: block !important;
  }

  #formulariosRodape .elementor-element-21b9e52 > .elementor-column-wrap,
  #formulariosRodape .elementor-element-f3b6b56 > .elementor-column-wrap {
    height: auto !important;
    min-height: 0 !important;
    padding: 28px 20px !important;
    border-radius: 16px !important;
    overflow: hidden !important;
    justify-content: flex-start !important;
  }

  #formulariosRodape .elementor-element-faab318 img,
  #formulariosRodape .elementor-element-ba015bc img {
    height: 100px !important;
  }

  #formulariosRodape .elementor-widget-heading .elementor-heading-title {
    font-size: 1.25rem !important;
  }

  #formulariosRodape .elementor-widget-text-editor {
    font-size: 0.88rem !important;
    margin-bottom: 18px !important;
  }

  #formulariosRodape .elementor-widget-wrap {
    height: auto !important;
    overflow: visible !important;
  }

  #formulariosRodape .elementor-form-fields-wrapper {
    display: flex !important;
    flex-wrap: wrap !important;
    margin-left: 0 !important;
    margin-right: 0 !important;
  }

  #formulariosRodape .elementor-field-group,
  #formulariosRodape .elementor-field-type-text,
  #formulariosRodape .elementor-field-type-email,
  #formulariosRodape .elementor-field-type-radio,
  #formulariosRodape .elementor-field-type-checkbox,
  #formulariosRodape .e-form__buttons {
    flex: 0 0 100% !important;
    width: 100% !important;
    max-width: 100% !important;
    min-width: 0 !important;
    box-sizing: border-box !important;
  }

  #formulariosRodape .elementor-field-subgroup,
  #formulariosRodape .elementor-field-option {
    width: 100% !important;
    max-width: 100% !important;
    min-width: 0 !important;
    box-sizing: border-box !important;
  }

  #formulariosRodape .elementor-field-option label {
    font-size: 12px !important;
    overflow-wrap: anywhere !important;
    word-break: normal !important;
  }
}

@media (max-width: 900px) and (orientation: landscape),
       (max-height: 500px) and (orientation: landscape) {
  #formulariosRodape {
    padding: 24px 16px !important;
  }
  #formulariosRodape .elementor-row {
    flex-direction: row !important;
    gap: 16px !important;
    align-items: stretch !important;
  }
  #formulariosRodape .elementor-column.elementor-col-50 {
    flex: 1 1 0 !important;
    width: 0 !important;
    max-width: none !important;
  }
  #formulariosRodape .elementor-element-21b9e52 > .elementor-column-wrap,
  #formulariosRodape .elementor-element-f3b6b56 > .elementor-column-wrap {
    padding: 20px 16px !important;
  }
  #formulariosRodape .elementor-element-faab318 img,
  #formulariosRodape .elementor-element-ba015bc img {
    height: 72px !important;
  }
  #formulariosRodape .elementor-widget-heading .elementor-heading-title {
    font-size: 1.1rem !important;
  }
  #formulariosRodape .elementor-widget-text-editor {
    font-size: 0.8rem !important;
    margin-bottom: 12px !important;
  }
  #formulariosRodape .elementor-field-textual {
    padding: 9px 11px !important;
    font-size: 12px !important;
  }
  #formulariosRodape .elementor-field-option label {
    font-size: 11px !important;
  }
  #formulariosRodape .elementor-button {
    padding: 10px 16px !important;
    font-size: 12px !important;
    margin-top: 6px !important;
  }
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


def normalize_footer_forms(source: str) -> str:
    """Standardize newsletter and catalog footer forms across routes."""
    if "formulariosRodape" not in source:
        return source
    rendered = source.replace('placeholder="Name"', 'placeholder="Nome"')
    rendered = rendered.replace(
        '<span class="elementor-button-text">RECEBER MATERIAL</span>',
        '<span class="elementor-button-text">Receber material</span>',
    )
    rendered = rendered.replace(
        '<input type="radio" value="Concordo em receber conteúdos da Inda Fire"',
        '<input type="checkbox" value="Concordo em receber conteúdos da Inda Fire"',
    )
    rendered = rendered.replace(
        '<input type="radio" value="Concordo com os termos de uso',
        '<input type="checkbox" value="Concordo com os termos de uso',
    )
    return rendered


def style_tag() -> str:
    return f'<style id="{STYLE_ID}">\n{CSS}\n</style>'


def inject(source: str) -> str:
    pattern = re.compile(rf'<style id="{re.escape(STYLE_ID)}">.*?</style>\s*', re.DOTALL)
    stripped = pattern.sub("", source)
    if "</head>" not in stripped:
        return normalize_footer_forms(source)
    stripped = normalize_footer_forms(stripped)
    catalog_style = '<style id="indafire-product-catalog-polish">'
    home_style = '<style id="indafire-home-section-polish">'
    if catalog_style in stripped:
        return stripped.replace(
            catalog_style, f"{style_tag()}\n{catalog_style}", 1
        )
    if home_style in stripped:
        return stripped.replace(home_style, f"{style_tag()}\n{home_style}", 1)
    return stripped.replace("</head>", f"{style_tag()}\n</head>", 1)


def inject_styles(targets: tuple[Path, ...] | list[Path]) -> int:
    changed = 0
    for page in targets:
        source = page.read_text(encoding="utf-8")
        rendered = inject(source)
        if rendered != source:
            page.write_text(rendered, encoding="utf-8")
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
