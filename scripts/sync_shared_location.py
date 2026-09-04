"""Keep internal-page location sections identical to the Home component."""

from __future__ import annotations

from pathlib import Path
import re


ROOT = Path(__file__).resolve().parents[1]
STYLE_ID = "indafire-shared-location-style"
LOCATION_CSS_START = "/* Location section aligned with the site's light cards and red accents. */"
LOCATION_CSS_END = "/* Reveal the full navigation whenever the user reverses scroll direction. */"
LOCATION_CSS_END_MARKERS = (
    LOCATION_CSS_END,
    "/* Mobile newsletter/catalog cards: keep every form control inside its card. */",
    "</style>",
)
TARGETS = (
    ROOT / "produtos" / "index.html",
    ROOT / "servicos" / "index.html",
    ROOT / "treinamentos" / "index.html",
    ROOT / "sobre-nos" / "index.html",
    ROOT / "blog" / "index.html",
    ROOT / "contato" / "index.html",
    ROOT / "area-do-cliente" / "index.html",
    ROOT / "politica-de-privacidade" / "index.html",
    ROOT / "categoria-produto" / "extintores" / "index.html",
    ROOT / "produto" / "extintor-pqs-bc-4-kg-20bc" / "index.html",
    ROOT / "produto" / "unidade-central-lux-700-1200-24vdc" / "index.html",
)


def _location_bounds(source: str) -> tuple[int, int]:
    opening = re.search(
        r'<section\b(?=[^>]*\bid=["\']localizacao_mapa["\'])[^>]*>',
        source,
        flags=re.IGNORECASE | re.DOTALL,
    )
    if opening is None:
        raise ValueError("Missing section #localizacao_mapa")

    depth = 0
    token_pattern = re.compile(r"<section\b[^>]*>|</section\s*>", re.IGNORECASE | re.DOTALL)
    for token in token_pattern.finditer(source, opening.start()):
        if token.group(0).lower().startswith("</section"):
            depth -= 1
            if depth == 0:
                return opening.start(), token.end()
        else:
            depth += 1

    raise ValueError("Unclosed section #localizacao_mapa")


def extract_location(source: str) -> str:
    """Return the complete Home location section, including nested sections."""
    start, end = _location_bounds(source)
    return source[start:end]


def extract_location_css(source: str) -> str:
    """Return only the location rules from the Home managed style layer."""
    start = source.find(LOCATION_CSS_START)
    if start < 0:
        raise ValueError("Missing Home location CSS start marker")
    end = -1
    for marker in LOCATION_CSS_END_MARKERS:
        pos = source.find(marker, start + len(LOCATION_CSS_START))
        if pos != -1 and (end == -1 or pos < end):
            end = pos
    if end < 0:
        raise ValueError("Missing Home location CSS markers")
    return source[start:end].rstrip()


def style_tag(home_source: str) -> str:
    return f'<style id="{STYLE_ID}">\n{extract_location_css(home_source)}\n</style>'


def render_target(target_source: str, home_source: str) -> str:
    """Replace or insert the shared location section and its managed style layer."""
    style_pattern = re.compile(
        rf'<style id="{re.escape(STYLE_ID)}">.*?</style>\s*',
        re.DOTALL,
    )
    stripped = style_pattern.sub("", target_source)
    loc_markup = extract_location(home_source)

    has_loc = re.search(
        r'<section\b(?=[^>]*\bid=["\']localizacao_mapa["\'])[^>]*>',
        stripped,
        flags=re.IGNORECASE | re.DOTALL,
    )
    if has_loc:
        target_start, target_end = _location_bounds(stripped)
        rendered = (
            stripped[:target_start]
            + loc_markup
            + stripped[target_end:]
        )
    else:
        form_match = re.search(
            r'<section\b(?=[^>]*\bid=["\']formulariosRodape["\'])[^>]*>',
            stripped,
            flags=re.IGNORECASE | re.DOTALL,
        )
        if form_match:
            insert_pos = form_match.start()
        else:
            footer_match = re.search(r'<footer\b', stripped, flags=re.IGNORECASE)
            if footer_match:
                insert_pos = footer_match.start()
            else:
                body_match = re.search(r'</body\b', stripped, flags=re.IGNORECASE)
                if body_match:
                    insert_pos = body_match.start()
                else:
                    raise ValueError("Cannot find insertion point for location section")
        rendered = (
            stripped[:insert_pos]
            + loc_markup
            + "\n"
            + stripped[insert_pos:]
        )

    if "</head>" not in rendered:
        raise ValueError("Target document is missing </head>")
    shared_style = style_tag(home_source) + "\n"
    for marker in (
        '<style id="indafire-responsive-navigation-style">',
        '<style id="indafire-internal-page-polish">',
    ):
        if marker in rendered:
            return rendered.replace(marker, shared_style + marker, 1)
    return rendered.replace("</head>", f"{shared_style}</head>", 1)


def sync_location(home_page: Path, targets: tuple[Path, ...] | list[Path]) -> int:
    """Synchronize location markup and CSS, returning the changed-file count."""
    with home_page.open("r", encoding="utf-8", newline="") as handle:
        home_source = handle.read()

    changed = 0
    for target in targets:
        with target.open("r", encoding="utf-8", newline="") as handle:
            source = handle.read()
        rendered = render_target(source, home_source)
        if rendered != source:
            with target.open("w", encoding="utf-8", newline="") as handle:
                handle.write(rendered)
            changed += 1
    return changed


def main() -> None:
    missing = [path for path in TARGETS if not path.is_file()]
    if missing:
        names = ", ".join(str(path.relative_to(ROOT)) for path in missing)
        raise SystemExit(f"Missing location target routes: {names}")
    print(f"Synchronized Home location into {sync_location(ROOT / 'index.html', TARGETS)} page(s).")


if __name__ == "__main__":
    main()
