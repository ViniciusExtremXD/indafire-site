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


# 17/11/2026: páginas que saíram do site viraram redirecionamentos (resgate em altura, cursos online,
# unidade móvel, páginas de teste) — não têm cabeçalho, rodapé nem medição.
def is_redirect(text):
    return "<!-- indafire: redirecionamento" in text[:3000]


REMOVIDOS = {adj.CINTURAO}  # produto de resgate em altura, removido na reunião de 17/11


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
        if slug in REMOVIDOS:
            continue
        text = read("produto/%s/index.html" % slug)
        # WhatsApp na página do produto: só banner, formulário e botão flutuante
        assert "if-cta-whats" not in text and 'href="#orcamento"' not in text, slug
        assert text.count('class="if-hero-whats"') == 1, slug
        assert 'id="ht-ctc-chat"' in text, slug
        assert "Solicite seu orçamento via WhatsApp" in text, slug
        start, end = adj.grid_bounds(text)
        grid = text[start:end]
        assert "if-card-whats" not in grid, slug  # botão fica no menu Produtos, não nos cards
        shown = []
        for art in adj.ARTICLE.finditer(grid):
            shown.append(adj.article_slug(art.group(0)))
        esperado = [s for s in adj.related_order(slug) if s not in REMOVIDOS]
        assert shown == esperado, (slug, shown)
        primeiros = [s for s in related if s not in REMOVIDOS]
        assert len(shown) >= 9 and shown[: len(primeiros)] == primeiros, (slug, shown)
        assert 'data-if-carrossel' in text and "carrossel-relacionados.js?v=" in text, slug
        assert slug not in shown
        assert '>Mais opções</h3>' in text and 'Produtos relacionados' not in text, slug
        assert 'if-rel-destaque' not in text, slug


def test_cylinder_related_are_not_the_whole_rescue_family():
    assert adj.RELATED[adj.CILINDRO][0] == "capacete-gallet"
    assert adj.COLETE not in adj.RELATED[adj.CILINDRO]


def test_products_page_shows_the_lines_not_the_catalog():
    # 17/11: /produtos/ mostra as linhas em seções (cada uma leva à página da linha), sem catálogo
    text = read("produtos/index.html")
    if "<!-- if-produtos-faixas -->" in text:
        # variante da prévia na Vercel (scripts/variante_produtos_estilo_servicos.py): faixas como em Serviços
        assert 'id="if-produtos-secoes"' not in text
        assert text.count('href="../categoria-produto/') >= 14
    else:
        assert 'id="if-produtos-secoes"' in text
        assert text.count("if-secao__link") >= 12
    assert "if-card-whats" not in text
    for slug in adj.CATEGORIES:
        assert "produto/%s/" % slug not in text, slug


def test_script_is_idempotent():
    out = subprocess.check_output(
        [sys.executable, str(ROOT / "scripts" / "apply_client_adjustments_2026_10_15.py"), "--dry"], text=True
    )
    assert "'files'" not in out, out
    assert "catálogo isolado em 17/11" in out, out


def test_products_menu_shows_only_the_lines():
    # 17/11: a coluna de produtos específicos saiu do menu Produtos (só as linhas ficam)
    for rel in PAGES:
        text = read(rel)
        if is_redirect(text) or "jet-sub-mega-menu" not in text:
            continue
        assert 'class="if-menu-whats"' not in text, rel
        assert 'data-id="db7b976"' not in text, rel


def test_whatsapp_button_on_banner_or_after_the_line():
    for rel in PAGES:
        if not rel.startswith(("produto/", "categoria-produto/", "produtos/")):
            continue
        text = read(rel)
        if is_redirect(text):
            continue
        if rel.startswith("categoria-produto/"):
            # 17/11: a página da linha mostra as especialidades e só depois o botão do WhatsApp
            assert 'class="if-hero-whats"' not in text, rel
            assert text.count('class="if-linha-cta"') == 1, rel
            continue
        assert text.count('class="if-hero-whats"') == 1, rel
        assert text.index('id="tituloCategoriaProdutos"') < text.index('class="if-hero-whats"'), rel


def test_every_product_tab_is_filled():
    pat = re.compile(r'<div id="elementor-tab-content-\d+" class="elementor-tab-content[^"]*"[^>]*>(.*?)</div>', re.S)
    for slug in set(adj.RELATED) - REMOVIDOS:
        tabs = pat.findall(read("produto/%s/index.html" % slug))
        assert len(tabs) == 3, slug
        for i, tab in enumerate(tabs):
            assert tab.strip(), (slug, ["Informações Técnicas", "Quando usar", "Garantia"][i])


def test_no_outdated_manufacturing_year_in_product_info():
    for slug in set(adj.RELATED) - REMOVIDOS:
        text = read("produto/%s/index.html" % slug)
        assert "Fab 2020" not in text, slug
    cil = read("produto/%s/index.html" % adj.CILINDRO)
    assert "Validade: 5 anos a partir da data de fabricação" in cil


def test_gtm_replaces_hardcoded_gtag_on_every_page():
    for rel in PAGES:
        text = read(rel)
        assert "gtag/js?id=G-RBGKBY9PJR" not in text, rel
        if is_redirect(text):
            continue
        assert text.count("GTM-WTKSN3VL") == 2, rel  # <head> + <noscript> no <body>
        assert text.index("GTM-WTKSN3VL") < text.index("<body"), rel
        assert "wp-content/indafire/medicao.js?v=" in text, rel


def test_responsividade_2026_11_12():
    for rel in PAGES:
        text = read(rel)
        # número que não existe no site original
        assert "5519999015942" not in text and "99901-5942" not in text, rel
        # catálogo fora também dos posts do blog
        assert "Catalogue Widget Box" not in text and "btn-abrir-catalogo" not in text, rel
        # textos do WooCommerce em português
        assert "Select a category" not in text and '"View cart"' not in text, rel
        if rel.startswith("cursos/lorem-ipsum"):
            # 17/11: os cursos online saíram; as páginas de teste levam a /treinamentos/
            assert is_redirect(text) and "treinamentos/" in text and "cursos-online" not in text, rel
    css = (ROOT / "wp-content/indafire/ajustes-responsivos.css").read_text(encoding="utf-8")
    assert "Menu aberto no celular e no tablet" in css
    assert "#ht-ctc-chat" in css  # botão flutuante some com o menu aberto
