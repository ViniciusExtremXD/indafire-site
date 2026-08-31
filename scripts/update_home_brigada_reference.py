"""Restore the effective desktop Brigada block to the published reference."""

from __future__ import annotations

from pathlib import Path
import re


ROOT = Path(__file__).resolve().parents[1]
MASTER_STYLE_ID = "indafire-mobile-portrait-landscape-master-override"
MARKER = "INDAFIRE HOME BRIGADA REFERENCE"
TARGETS = (ROOT / "index.html",)


REFERENCE_BLOCK = r'''
  /* DESKTOP BRIGADA REFERENCE */
  .elementor-element.elementor-element-3662fd7 {
    min-height: 585px !important;
    padding: 0 !important;
    position: relative !important;
    background-color: transparent !important;
    background-image: url("./wp-content/uploads/2021/10/bombeiro.jpg") !important;
    background-position: bottom center !important;
    background-repeat: no-repeat !important;
    background-size: contain !important;
  }
  .elementor-element.elementor-element-3662fd7 > .elementor-container {
    max-width: 1140px !important;
    min-height: 585px !important;
    margin: 0 auto !important;
    padding: 0 !important;
  }
  .elementor-element.elementor-element-3662fd7 .elementor-container > .elementor-row {
    display: flex !important;
    flex-direction: row !important;
    flex-wrap: nowrap !important;
    align-items: stretch !important;
    justify-content: normal !important;
    gap: 0 !important;
    width: 100% !important;
  }
  .elementor-element.elementor-element-169964b {
    flex: 1 1 50% !important;
    width: 50% !important;
    max-width: 50% !important;
    display: flex !important;
    flex-direction: column !important;
    align-items: flex-end !important;
    text-align: left !important;
    padding: 0 !important;
    z-index: 3 !important;
  }
  .elementor-element.elementor-element-42aaacd .elementor-heading-title {
    font-size: 1em !important;
    letter-spacing: normal !important;
    text-transform: uppercase !important;
    color: #333333 !important;
    font-weight: 700 !important;
    text-align: left !important;
    margin: 0 !important;
  }
  .elementor-element.elementor-element-9d7bf30 .elementor-heading-title {
    font-size: 2.5em !important;
    line-height: normal !important;
    font-weight: 700 !important;
    text-transform: none !important;
    color: #e30613 !important;
    text-align: left !important;
    margin: 0 !important;
  }
  .elementor-element.elementor-element-9d7bf30 > .elementor-widget-container { margin: -15px 0 0 !important; }
  .elementor-element.elementor-element-1c2246b,
  .elementor-element.elementor-element-1c2246b p {
    font-size: 1rem !important;
    line-height: 1.5 !important;
    color: #555555 !important;
    text-align: left !important;
    max-width: none !important;
    margin: 0 !important;
  }
  .elementor-element.elementor-element-989c3cc {
    width: 100% !important;
    max-width: 550px !important;
    border-radius: 0 !important;
    box-shadow: none !important;
    overflow: visible !important;
    margin: 0 !important;
  }
  .elementor-element.elementor-element-989c3cc > .elementor-widget-container {
    margin: 0 0 -100px !important;
    padding: 0 !important;
    box-shadow: 7px 6px 10px rgba(0, 0, 0, .5) !important;
  }
  .elementor-element.elementor-element-989c3cc video { display: block !important; width: 100% !important; border-radius: 0 !important; }
  .elementor-element.elementor-element-44bd2a0 {
    flex: 1 1 50% !important;
    width: 50% !important;
    max-width: 50% !important;
    min-height: 0 !important;
    height: auto !important;
    display: block !important;
    position: relative !important;
    border-radius: 0 !important;
    background: transparent !important;
    box-shadow: none !important;
    overflow: visible !important;
  }
  .elementor-element.elementor-element-44bd2a0::before,
  .elementor-element.elementor-element-44bd2a0::after { content: none !important; }
  .elementor-element.elementor-element-08f0d01,
  .elementor-element.elementor-element-d3d2086 { display: none !important; height: 0 !important; margin: 0 !important; padding: 0 !important; }
  .elementor-element.elementor-element-207ff2b { padding: 110px 0 30px !important; margin: 0 auto !important; display: flex !important; justify-content: center !important; }
  .elementor-element.elementor-element-8eed4f7 .elementor-button {
    padding: 15px 40px !important;
    font-size: 1em !important;
    font-weight: 600 !important;
    text-transform: uppercase !important;
    border-radius: 50px !important;
    background-color: #e30613 !important;
    color: #ffffff !important;
    box-shadow: none !important;
  }
'''.strip().replace("\n  .elementor", "\n  body.home .elementor-2 .elementor")


def inject_styles(targets: tuple[Path, ...] | list[Path]) -> int:
    changed = 0
    marker_pattern = re.compile(rf'\s*/\* {MARKER} START \*/.*?/\* {MARKER} END \*/\s*', re.DOTALL)
    desktop_pattern = re.compile(
        r'  /\* DESKTOP BRIGADA DE INCÊNDIO & BOMBEIRO \*/.*?'
        r'  \.elementor-element\.elementor-element-8eed4f7 \.elementor-button \{.*?\n  \}\n',
        re.DOTALL,
    )
    reference_pattern = re.compile(
        r'/\* DESKTOP BRIGADA[^*]*\*/.*?'
        r'  (?:body\.home \.elementor-2 )?\.elementor-element\.elementor-element-8eed4f7 \.elementor-button \{.*?\n  \}\n',
        re.DOTALL,
    )
    master_pattern = re.compile(rf'(<style id="{MASTER_STYLE_ID}">)(.*?)(</style>)', re.DOTALL)
    marker = f"/* {MARKER} START */\n/* {MARKER} END */"
    for page in targets:
        source = page.read_text(encoding="utf-8")
        match = master_pattern.search(source)
        if match is None:
            continue
        master_css = marker_pattern.sub("\n", match.group(2))
        if "DESKTOP BRIGADA" in master_css:
            master_css, count = reference_pattern.subn(
                f"{REFERENCE_BLOCK}\n", master_css, count=1
            )
            if count != 1:
                continue
        else:
            master_css, count = desktop_pattern.subn(f"{REFERENCE_BLOCK}\n", master_css, count=1)
            if count != 1:
                continue
        master_css = master_css.rstrip() + f"\n\n{marker}\n"
        rendered = source[:match.start()] + match.group(1) + master_css + match.group(3) + source[match.end():]
        if rendered != source:
            page.write_text(rendered, encoding="utf-8")
            changed += 1
    return changed
