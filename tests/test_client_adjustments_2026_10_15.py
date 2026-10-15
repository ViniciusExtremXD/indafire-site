"""Ajustes do cliente (15/10/2026): catálogo/newsletter/Bee Creative fora, WhatsApp único,
botão de atendimento no menu Produtos e relacionados por afinidade."""
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))
import apply_client_adjustments_2026_10_15 as adj  # noqa: E402

PAGES = [f for f in subprocess.check_output(["git", "ls-files", "*.html"], cwd=ROOT, text=True).split("\n") if f]


def read(rel):
    return (ROOT / rel).read_text(encoding="utf-8")


def test_catalog_newsletter_and_bee_creative_are_gone():
    for rel in PAGES:
        text = read(rel)
        for needle in ('id="formulariosRodape"', "formulario_newsletter", "formulario_catalogo", "beecreative.com.br", "catalogo-inda-fire.pdf"):
            assert needle not in text, (rel, needle)


def test_single_whatsapp_card_per_page():
    for rel in PAGES:
        assert read(rel).count('class="indafire-whatsapp-card"') <= 1, rel


def test_product_pages_cta_and_related():
    for slug, related in adj.RELATED.items():
        text = read("produto/%s/index.html" % slug)
        assert "Solicite orçamento via WhatsApp" in text, slug
        assert "Solicite seu orçamento via WhatsApp" in text, slug
        start, end = adj.grid_bounds(text)
        grid = text[start:end]
        assert "if-card-whats" not in grid, slug  # botão fica no menu Produtos, não nos cards
        shown = []
        for art in adj.ARTICLE.finditer(grid):
            shown.append(adj.article_slug(art.group(0)))
        assert shown == related, (slug, shown)
        assert slug not in shown


def test_cylinder_related_are_not_the_whole_rescue_family():
    assert adj.RELATED[adj.CILINDRO][0] == "capacete-gallet"
    assert adj.COLETE not in adj.RELATED[adj.CILINDRO]


def test_product_list_shows_every_product_with_button():
    text = read("produtos/index.html")
    start, end = adj.grid_bounds(text)
    slugs = [adj.article_slug(m.group(0)) for m in adj.ARTICLE.finditer(text[start:end])]
    assert set(slugs) == set(adj.CATEGORIES)
    assert "if-card-whats" not in text


def test_script_is_idempotent():
    out = subprocess.check_output(
        [sys.executable, str(ROOT / "scripts" / "apply_client_adjustments_2026_10_15.py"), "--dry"], text=True
    )
    assert "'files'" not in out, out


def test_products_menu_has_whatsapp_button_under_each_product():
    for rel in PAGES:
        text = read(rel)
        if "swiper-slide dce-item-carousel" not in text:
            continue
        assert text.count('class="if-menu-whats"') == 5, rel
        assert "aviso-whatsapp-produtos.js?v=" in text, rel


def test_banner_has_whatsapp_button_on_products_categories_and_product_pages():
    for rel in PAGES:
        if not rel.startswith(("produto/", "categoria-produto/", "produtos/")):
            continue
        text = read(rel)
        assert text.count('class="if-hero-whats"') == 1, rel
        assert text.index('id="tituloCategoriaProdutos"') < text.index('class="if-hero-whats"'), rel
