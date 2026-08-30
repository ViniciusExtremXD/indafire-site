"""Inject the shared product-catalog polish into the static site sources.

The static export contains standalone HTML pages, so this keeps the product
archive, category archive, and available product detail pages on one visual
layer without duplicating hand-edited CSS across routes.
"""

from __future__ import annotations

from pathlib import Path
import re


ROOT = Path(__file__).resolve().parents[1]
STYLE_ID = "indafire-product-catalog-polish"
TARGETS = (
    ROOT / "produtos" / "index.html",
    ROOT / "categoria-produto" / "extintores" / "index.html",
    ROOT / "produto" / "unidade-central-lux-700-1200-24vdc" / "index.html",
    ROOT / "produto" / "extintor-pqs-bc-4-kg-20bc" / "index.html",
)


CSS = r"""
/* INDAFIRE — product catalog polish: preserves the existing visual system. */
.woocommerce-shop,
.tax-product_cat,
.single-product {
  --inda-red: #e30613;
  --inda-ink: #202124;
  --inda-line: #e8eaed;
  --inda-shadow: 0 12px 30px rgba(26, 28, 31, 0.10);
}

.woocommerce-shop :focus-visible,
.tax-product_cat :focus-visible,
.single-product :focus-visible {
  outline: 3px solid rgba(227, 6, 19, 0.42) !important;
  outline-offset: 3px !important;
}

/* Archive and category landing: keep the original photographic hero, but
   make its hierarchy stable from wide desktop down to mobile. */
.woocommerce-shop #bannerProdutoINDA,
.tax-product_cat #bannerProdutoINDA {
  min-height: clamp(260px, 37vw, 600px) !important;
}

/* The legacy archive script points to a WordPress-only relative URL. Keep
   the original product workshop image bundled and addressable in the static
   export. */
.woocommerce-shop #bannerProdutoINDA {
  background-image: url("../wp-content/uploads/2021/11/produtos.jpg") !important;
  background-position: center center !important;
  background-repeat: no-repeat !important;
  background-size: cover !important;
}

.woocommerce-shop #tituloCategoriaProdutos .elementor-heading-title,
.tax-product_cat #tituloCategoriaProdutos .elementor-heading-title {
  font-size: clamp(2.35rem, 5.2vw, 5rem) !important;
  line-height: 0.98 !important;
  letter-spacing: 0.025em !important;
  text-wrap: balance;
  text-shadow: 0 3px 18px rgba(0, 0, 0, 0.18);
}

.woocommerce-shop .elementor-element-a7ca6f9,
.tax-product_cat .elementor-element-a7ca6f9 {
  padding-top: 24px !important;
  padding-bottom: 12px !important;
}

.woocommerce-shop .ha-breadcrumbs,
.tax-product_cat .ha-breadcrumbs {
  gap: 9px !important;
  color: #65686d !important;
  font-size: 0.88rem !important;
}

/* The desktop filter stays a filter, gaining clearer grouping and states. */
.woocommerce-shop .elementor-element-c4abd9d > .elementor-column-wrap,
.tax-product_cat .elementor-element-c4abd9d > .elementor-column-wrap {
  border: 1px solid var(--inda-line) !important;
  border-radius: 14px !important;
  overflow: hidden !important;
  background: #fff !important;
  box-shadow: 0 6px 18px rgba(26, 28, 31, 0.055) !important;
}

.woocommerce-shop .elementor-element-b75d9a7,
.tax-product_cat .elementor-element-b75d9a7 {
  margin: 0 !important;
  padding: 20px 22px 16px !important;
  border-bottom: 1px solid var(--inda-line) !important;
}

.woocommerce-shop .elementor-element-b75d9a7 .elementor-heading-title,
.tax-product_cat .elementor-element-b75d9a7 .elementor-heading-title {
  color: var(--inda-red) !important;
  font-size: 1.18rem !important;
  font-weight: 800 !important;
  letter-spacing: 0.03em !important;
}

.woocommerce-shop .filtrolateral,
.tax-product_cat .filtrolateral {
  margin: 0 !important;
  border-bottom: 1px solid #f0f1f2 !important;
  transition: background-color 160ms ease, box-shadow 160ms ease !important;
}

.woocommerce-shop .filtrolateral:last-child,
.tax-product_cat .filtrolateral:last-child {
  border-bottom: 0 !important;
}

.woocommerce-shop .filtrolateral .elementor-image-box-wrapper,
.tax-product_cat .filtrolateral .elementor-image-box-wrapper {
  min-height: 44px !important;
  padding: 10px 18px !important;
  align-items: center !important;
}

.woocommerce-shop .filtrolateral:hover,
.tax-product_cat .filtrolateral:hover {
  background: rgba(227, 6, 19, 0.045) !important;
  box-shadow: inset 3px 0 0 var(--inda-red) !important;
}

.woocommerce-shop .filtrolateral a,
.tax-product_cat .filtrolateral a {
  color: #3d4045 !important;
  font-size: 0.9rem !important;
  font-weight: 650 !important;
  text-decoration: none !important;
}

/* Search controls share a single vertical rhythm with the product grid. */
.woocommerce-shop .jet-ajax-search__form,
.tax-product_cat .jet-ajax-search__form {
  display: grid !important;
  grid-template-columns: minmax(0, 1fr) minmax(190px, 0.42fr) 52px !important;
  gap: 10px !important;
  align-items: stretch !important;
}

.woocommerce-shop .jet-ajax-search__fields-holder,
.tax-product_cat .jet-ajax-search__fields-holder {
  display: contents !important;
}

.woocommerce-shop .jet-ajax-search__field,
.woocommerce-shop .jet-ajax-search__categories-select,
.tax-product_cat .jet-ajax-search__field,
.tax-product_cat .jet-ajax-search__categories-select,
.woocommerce-shop .dropdown_product_cat,
.tax-product_cat .dropdown_product_cat {
  min-height: 48px !important;
  border: 1px solid #dfe2e5 !important;
  border-radius: 9px !important;
  background: #fff !important;
  color: #3c4045 !important;
  font-size: 0.93rem !important;
  box-shadow: 0 1px 0 rgba(20, 20, 20, 0.02) !important;
  transition: border-color 160ms ease, box-shadow 160ms ease !important;
}

.woocommerce-shop .jet-ajax-search__field,
.tax-product_cat .jet-ajax-search__field {
  padding: 0 15px !important;
}

.woocommerce-shop .jet-ajax-search__field:focus,
.woocommerce-shop .jet-ajax-search__categories-select:focus,
.woocommerce-shop .dropdown_product_cat:focus,
.tax-product_cat .jet-ajax-search__field:focus,
.tax-product_cat .jet-ajax-search__categories-select:focus,
.tax-product_cat .dropdown_product_cat:focus {
  border-color: var(--inda-red) !important;
  box-shadow: 0 0 0 3px rgba(227, 6, 19, 0.12) !important;
  outline: 0 !important;
}

.woocommerce-shop .jet-ajax-search__submit,
.tax-product_cat .jet-ajax-search__submit {
  width: 52px !important;
  min-height: 48px !important;
  border-radius: 9px !important;
  background: var(--inda-red) !important;
  box-shadow: 0 6px 14px rgba(227, 6, 19, 0.2) !important;
  transition: transform 160ms ease, box-shadow 160ms ease, background-color 160ms ease !important;
}

.woocommerce-shop .jet-ajax-search__submit:hover,
.tax-product_cat .jet-ajax-search__submit:hover {
  background: #c90813 !important;
  box-shadow: 0 9px 18px rgba(227, 6, 19, 0.28) !important;
  transform: translateY(-1px) !important;
}

/* Product cards retain their original neutral imagery and red CTA, while
   their edges, image area and hover feedback become more deliberate. */
.woocommerce-shop .dce-post-item .areaProduto > .elementor-column-wrap,
.tax-product_cat .dce-post-item .areaProduto > .elementor-column-wrap {
  height: 100% !important;
  overflow: hidden !important;
  border: 1px solid var(--inda-line) !important;
  border-radius: 14px !important;
  background: #fff !important;
  box-shadow: 0 3px 12px rgba(24, 26, 28, 0.055) !important;
  transition: transform 180ms ease, box-shadow 180ms ease, border-color 180ms ease !important;
}

.woocommerce-shop .dce-post-item:hover .areaProduto > .elementor-column-wrap,
.tax-product_cat .dce-post-item:hover .areaProduto > .elementor-column-wrap {
  border-color: rgba(227, 6, 19, 0.34) !important;
  box-shadow: var(--inda-shadow) !important;
  transform: translateY(-4px) !important;
}

.woocommerce-shop .dce-post-item .areaImagem,
.tax-product_cat .dce-post-item .areaImagem {
  min-height: 205px !important;
  background: #f5f6f7 !important;
}

.woocommerce-shop .dce-post-item .areaImagem img,
.tax-product_cat .dce-post-item .areaImagem img {
  width: 100% !important;
  height: 205px !important;
  object-fit: contain !important;
  padding: 18px !important;
  transition: transform 220ms ease !important;
}

.woocommerce-shop .dce-post-item:hover .areaImagem img,
.tax-product_cat .dce-post-item:hover .areaImagem img {
  transform: scale(1.035) !important;
}

.woocommerce-shop .dce-post-item .areaConteudo,
.tax-product_cat .dce-post-item .areaConteudo {
  min-height: 174px !important;
  padding: 18px 18px 17px !important;
  background: #fff !important;
}

.woocommerce-shop .dce-post-item .tituloProduto:first-child .elementor-heading-title,
.tax-product_cat .dce-post-item .tituloProduto:first-child .elementor-heading-title {
  color: var(--inda-ink) !important;
  font-size: 1rem !important;
  font-weight: 750 !important;
  line-height: 1.3 !important;
}

.woocommerce-shop .dce-post-item .tituloProduto + .tituloProduto .elementor-heading-title,
.tax-product_cat .dce-post-item .tituloProduto + .tituloProduto .elementor-heading-title {
  color: #676b70 !important;
  font-size: 0.83rem !important;
  font-weight: 400 !important;
  line-height: 1.45 !important;
}

.woocommerce-shop .dce-post-item .botaoProduto .elementor-heading-title,
.tax-product_cat .dce-post-item .botaoProduto .elementor-heading-title {
  display: inline-flex !important;
  align-items: center !important;
  gap: 6px !important;
  color: var(--inda-red) !important;
  font-size: 0.78rem !important;
  font-weight: 800 !important;
  letter-spacing: 0.06em !important;
  text-transform: uppercase !important;
}

.woocommerce-shop .dce-post-item .botaoProduto .elementor-heading-title::after,
.tax-product_cat .dce-post-item .botaoProduto .elementor-heading-title::after {
  content: "→";
  font-size: 1rem;
  line-height: 1;
  transition: transform 160ms ease;
}

.woocommerce-shop .dce-post-item:hover .botaoProduto .elementor-heading-title::after,
.tax-product_cat .dce-post-item:hover .botaoProduto .elementor-heading-title::after {
  transform: translateX(3px);
}

/* Product details: use the same quiet hierarchy without changing copy,
   images, form fields or call-to-action destinations. */
.single-product .product_title {
  color: var(--inda-ink) !important;
  line-height: 1.12 !important;
  letter-spacing: -0.018em !important;
  text-wrap: balance;
}

.single-product .elementor-button {
  min-height: 46px !important;
  border-radius: 8px !important;
  transition: transform 160ms ease, box-shadow 160ms ease, background-color 160ms ease !important;
}

.single-product .elementor-button:hover {
  box-shadow: 0 8px 18px rgba(227, 6, 19, 0.25) !important;
  transform: translateY(-1px) !important;
}

@media (max-width: 767px) {
  .woocommerce-shop #bannerProdutoINDA,
  .tax-product_cat #bannerProdutoINDA {
    min-height: 264px !important;
    padding: 104px 18px 54px !important;
  }

  .woocommerce-shop .elementor-element-a7ca6f9,
  .tax-product_cat .elementor-element-a7ca6f9 {
    padding: 18px 16px 8px !important;
  }

  .woocommerce-shop .elementor-element-c07e745,
  .tax-product_cat .elementor-element-c07e745 {
    padding: 0 16px 28px !important;
  }

  .woocommerce-shop .elementor-element-15e9629,
  .tax-product_cat .elementor-element-15e9629 {
    margin: 0 0 12px !important;
  }

  .woocommerce-shop .dropdown_product_cat,
  .tax-product_cat .dropdown_product_cat {
    width: 100% !important;
    padding: 0 13px !important;
  }

  .woocommerce-shop .jet-ajax-search__form,
  .tax-product_cat .jet-ajax-search__form {
    grid-template-columns: minmax(0, 1fr) 48px !important;
    gap: 8px !important;
  }

  .woocommerce-shop .jet-ajax-search__categories,
  .tax-product_cat .jet-ajax-search__categories {
    grid-column: 1 / -1 !important;
    grid-row: 2 !important;
  }

  .woocommerce-shop .jet-ajax-search__categories-select,
  .tax-product_cat .jet-ajax-search__categories-select {
    width: 100% !important;
  }

  .woocommerce-shop .jet-ajax-search__submit,
  .tax-product_cat .jet-ajax-search__submit {
    width: 48px !important;
    min-height: 48px !important;
  }

  .woocommerce-shop .dce-posts-wrapper,
  .tax-product_cat .dce-posts-wrapper {
    row-gap: 16px !important;
  }

  .woocommerce-shop .dce-post-item .areaImagem,
  .tax-product_cat .dce-post-item .areaImagem {
    min-height: 188px !important;
  }

  .woocommerce-shop .dce-post-item .areaImagem img,
  .tax-product_cat .dce-post-item .areaImagem img {
    height: 188px !important;
    padding: 14px !important;
  }

  .woocommerce-shop .dce-post-item .areaConteudo,
  .tax-product_cat .dce-post-item .areaConteudo {
    min-height: 0 !important;
    padding: 16px !important;
  }

  .woocommerce-shop .dce-post-item:hover .areaProduto > .elementor-column-wrap,
  .tax-product_cat .dce-post-item:hover .areaProduto > .elementor-column-wrap {
    transform: none !important;
  }
}

@media (max-width: 1024px) and (orientation: landscape),
       (max-height: 620px) and (orientation: landscape) {
  .woocommerce-shop #bannerProdutoINDA,
  .tax-product_cat #bannerProdutoINDA {
    min-height: 210px !important;
    padding-top: 76px !important;
    padding-bottom: 38px !important;
  }

  .woocommerce-shop #bannerProdutoINDA > .elementor-container,
  .tax-product_cat #bannerProdutoINDA > .elementor-container {
    min-height: 210px !important;
    height: auto !important;
  }

  .woocommerce-shop .elementor-element-c07e745,
  .tax-product_cat .elementor-element-c07e745 {
    padding-bottom: 20px !important;
  }

  .woocommerce-shop .dce-posts-wrapper,
  .tax-product_cat .dce-posts-wrapper {
    row-gap: 14px !important;
  }

  .woocommerce-shop .dce-post-item .areaImagem,
  .tax-product_cat .dce-post-item .areaImagem,
  .woocommerce-shop .dce-post-item .areaImagem img,
  .tax-product_cat .dce-post-item .areaImagem img {
    min-height: 150px !important;
    height: 150px !important;
  }
}

@media (prefers-reduced-motion: reduce) {
  .woocommerce-shop *,
  .tax-product_cat *,
  .single-product * {
    scroll-behavior: auto !important;
    transition-duration: 1ms !important;
    animation-duration: 1ms !important;
    animation-iteration-count: 1 !important;
  }
}
""".strip()


def style_tag() -> str:
    return f'<style id="{STYLE_ID}">\n{CSS}\n</style>'


def inject_styles(targets: tuple[Path, ...] | list[Path]) -> int:
    """Replace this style layer in each supplied static HTML document."""
    changed = 0
    pattern = re.compile(
        rf'<style id="{re.escape(STYLE_ID)}">.*?</style>\s*', re.DOTALL
    )
    replacement = style_tag() + "\n"
    internal_pattern = re.compile(
        r'<style id="indafire-internal-page-polish">.*?</style>\s*',
        re.DOTALL,
    )

    for page in targets:
        # Some exported HTML files carry mixed legacy newline sequences.
        # Keep them byte-for-byte intact outside this one inserted style tag.
        with page.open("r", encoding="utf-8", newline="") as handle:
            source = handle.read()
        stripped = pattern.sub("", source)
        if "</head>" not in stripped:
            continue
        internal_match = internal_pattern.search(stripped)
        if internal_match:
            rendered = (
                stripped[: internal_match.end()]
                + replacement
                + stripped[internal_match.end() :]
            )
        else:
            rendered = stripped.replace("</head>", f"{replacement}</head>", 1)
        if rendered != source:
            with page.open("w", encoding="utf-8", newline="") as handle:
                handle.write(rendered)
            changed += 1
    return changed


def main() -> None:
    missing = [path for path in TARGETS if not path.is_file()]
    if missing:
        names = ", ".join(str(path.relative_to(ROOT)) for path in missing)
        raise SystemExit(f"Missing static product routes: {names}")
    print(f"Injected product catalog polish into {inject_styles(TARGETS)} page(s).")


if __name__ == "__main__":
    main()
