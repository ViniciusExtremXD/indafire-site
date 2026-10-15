#!/usr/bin/env python3
"""Ajustes pedidos pelo cliente em 15/10/2026 (Wellington / Inda Fire).

1. Remove "Assine nossa newsletter" + "Baixe nosso catálogo" (e o popup do catálogo).
2. Remove a assinatura Bee Creative do rodapé.
3. Deixa um único bloco "Atendimento via WhatsApp" na home e tira o card
   genérico das páginas de produto (o orçamento do produto já é pelo WhatsApp).
4. Botão "Atendimento via WhatsApp" abaixo de cada produto do menu "Produtos" (cabeçalho).
4b. Botão "Atendimento via WhatsApp" no banner de produtos, categorias e produto.
5. Página de produto: sai o botão ao lado da foto (repetia o do banner); o formulário vira
   "Solicite seu orçamento via WhatsApp".
6. "Produtos relacionados" em carrossel (10 produtos, por afinidade).
7. Abas Informações Técnicas / Quando usar / Garantia preenchidas onde o original está vazio.

Idempotente: pode rodar de novo sem duplicar nada.
"""
import html as htmllib
import re
import subprocess
import sys
import urllib.parse
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
WHATSAPP = "551938341741"
ASSET_VERSION = "8"

WA_SVG = (
    '<svg xmlns="http://www.w3.org/2000/svg" width="{s}" height="{s}" viewBox="0 0 24 24" fill="#fff" aria-hidden="true" focusable="false">'
    '<path d="M.057 24l1.687-6.163a11.867 11.867 0 01-1.587-5.946C.16 5.335 5.495 0 12.05 0a11.817 11.817 0 018.413 3.488 '
    '11.824 11.824 0 013.48 8.414c-.003 6.557-5.338 11.892-11.893 11.892a11.9 11.9 0 01-5.688-1.448L.057 24zm6.597-3.807c1.676.995 '
    '3.276 1.591 5.392 1.592 5.448 0 9.886-4.434 9.889-9.885.002-5.462-4.415-9.89-9.881-9.892-5.452 0-9.887 4.434-9.889 9.884-.001 '
    '2.225.651 3.891 1.746 5.634l-.999 3.648 3.742-.981zm11.387-5.464c-.074-.124-.272-.198-.57-.347-.297-.149-1.758-.868-2.031-.967-.272-.099-.47-.149-.669.149-.198.297-.768.967-.941 '
    '1.165-.173.198-.347.223-.644.074-.297-.149-1.255-.462-2.39-1.475-.883-.788-1.48-1.761-1.653-2.059-.173-.297-.018-.458.13-.606.134-.133.297-.347.446-.521.151-.172.2-.296.3-.495.099-.198.05-.372-.025-.521-.075-.148-.669-1.611-.916-2.206-.242-.579-.487-.501-.669-.51l-.57-.01c-.198 '
    '0-.52.074-.792.372s-1.04 1.016-1.04 2.479 1.065 2.876 1.213 3.074c.149.198 2.095 3.2 5.076 4.487.709.306 1.263.489 1.694.626.712.226 1.36.194 1.872.118.571-.085 1.758-.719 2.006-1.413.248-.695.248-1.29.173-1.414z"/></svg>'
)

# ── Produtos: categoria real de cada um (vem dos cards do catálogo) e afinidade ──
# Cada produto lista os 3 mais próximos, do mais para o menos parecido. O critério
# é o uso: quem compra um item costuma precisar dos vizinhos do grupo.
#   extintores  : extintor, abrigo, suporte de solo, placa de sinalização
#   proteção    : capacete (EPI), cilindro (EPR), cinturão (resgate em altura), colete KED (APH)
#   hidrantes   : mangueira, chaves Storz, botoeira da bomba
#   emergência  : unidade central de iluminação, botoeira de alarme, armário corta-fogo
CATEGORIES = {
    "extintor-pqs-bc-4-kg-20bc": ["extintores"],
    "abrigo-para-extintor": ["abrigos"],
    "suporte-de-solo-para-extintor": ["acessorios"],
    "placa-extintor-e5": ["sinalizacoes"],
    "armario-corta-fogo": ["epc"],
    "capacete-gallet": ["epi"],
    "cilindro-p-aparelho-de-respiracao-autonoma-6l-aco-c-valvula-300-bar": ["epr"],
    "cinturao-de-seguranca-resgate-x-pert-ii": ["resgate-em-altura"],
    "colete-imobilizador-dorsal-ked-adulto": ["aph"],
    "mangueira-tipo-i": ["mangueiras"],
    "chaves-para-engate-rapido-storz": ["hidrantes"],
    "botoeira-de-bomba": ["alarmes-de-incendio", "sistema-de-bomba-de-incendio"],
    "unidade-central-lux-700-1200-24vdc": ["iluminacoes-de-emergencia"],
}
CILINDRO = "cilindro-p-aparelho-de-respiracao-autonoma-6l-aco-c-valvula-300-bar"
CINTURAO = "cinturao-de-seguranca-resgate-x-pert-ii"
COLETE = "colete-imobilizador-dorsal-ked-adulto"
UNIDADE = "unidade-central-lux-700-1200-24vdc"
CHAVES = "chaves-para-engate-rapido-storz"
RELATED = {
    "extintor-pqs-bc-4-kg-20bc": ["abrigo-para-extintor", "suporte-de-solo-para-extintor", "placa-extintor-e5"],
    "abrigo-para-extintor": ["extintor-pqs-bc-4-kg-20bc", "suporte-de-solo-para-extintor", "placa-extintor-e5"],
    "suporte-de-solo-para-extintor": ["extintor-pqs-bc-4-kg-20bc", "abrigo-para-extintor", "placa-extintor-e5"],
    "placa-extintor-e5": ["extintor-pqs-bc-4-kg-20bc", "abrigo-para-extintor", "suporte-de-solo-para-extintor"],
    "armario-corta-fogo": ["extintor-pqs-bc-4-kg-20bc", "abrigo-para-extintor", "placa-extintor-e5"],
    "capacete-gallet": [CILINDRO, CINTURAO, COLETE],
    CILINDRO: ["capacete-gallet", "mangueira-tipo-i", CINTURAO],
    CINTURAO: ["capacete-gallet", COLETE, CILINDRO],
    COLETE: [CINTURAO, "capacete-gallet", CILINDRO],
    "mangueira-tipo-i": [CHAVES, "botoeira-de-bomba", "extintor-pqs-bc-4-kg-20bc"],
    CHAVES: ["mangueira-tipo-i", "botoeira-de-bomba", "extintor-pqs-bc-4-kg-20bc"],
    "botoeira-de-bomba": [CHAVES, "mangueira-tipo-i", UNIDADE],
    UNIDADE: ["botoeira-de-bomba", "placa-extintor-e5", "extintor-pqs-bc-4-kg-20bc"],
}
# Categoria sem produto cadastrado ainda
EMPTY_CATEGORIES = {"incendio-florestal"}
# produtos que a lista /produtos/ não mostrava (ordem do catálogo: mais novos primeiro)
LISTING_TAIL = ["extintor-pqs-bc-4-kg-20bc", "chaves-para-engate-rapido-storz", "abrigo-para-extintor"]


# ───────────────────────── utilitários de HTML ─────────────────────────
TAG = re.compile(r"<(/?)(div|section)\b[^>]*?(/?)>", re.I)


def balanced_end(text, start, name):
    """Índice logo depois do </name> que fecha a tag aberta em `start`."""
    depth = 0
    for m in TAG.finditer(text, start):
        if m.group(2).lower() != name:
            continue
        if m.group(3) == "/":
            continue
        depth += -1 if m.group(1) else 1
        if depth == 0:
            return m.end()
    raise ValueError("tag sem fechamento")


def remove_block(text, start, name):
    end = balanced_end(text, start, name)
    # leva junto a quebra de linha/indentação que sobraria
    return text[:start].rstrip(" \t") + text[end:].lstrip(" \t") if False else text[:start] + text[end:]


def log(*a):
    print(*a)


# ───────────────────────── 1. catálogo + newsletter ─────────────────────────
def remove_forms_rodape(text):
    i = text.find('id="formulariosRodape"')
    if i < 0:
        return text, False
    start = text.rfind("<section", 0, i)
    return remove_block(text, start, "section"), True


def remove_catalog_popup(text):
    m = re.search(r'<div data-elementor-type="popup" data-elementor-id="701"[^>]*>', text)
    if not m:
        return text, False
    return remove_block(text, m.start(), "div"), True


UNIVERSAL_FORMS_TAIL = re.compile(
    r"\n  document\.addEventListener\('submit', function\(e\) \{\n    var form = e\.target;\n    if \(!form\) return;\n\n"
    r"    // Intercept Cat.logo Form.*?\n  \}, true\);\n(?=\}\)\(\);\n</script>)",
    re.S,
)


def strip_forms_js(text):
    new, n = UNIVERSAL_FORMS_TAIL.subn("\n", text)
    return new, n > 0


# ───────────────────────── 2. Bee Creative ─────────────────────────
def remove_bee(text):
    i = text.find("beecreative.com.br")
    if i < 0:
        return text, False
    start = text.rfind('<div class="elementor-column ', 0, i)
    end = balanced_end(text, start, "div")
    text = text[:start] + text[end:]
    # a coluna da esquerda passa a ocupar a barra inteira
    sec = text.rfind('data-element_type="section"', 0, start)
    sec_start = text.rfind("<section", 0, sec)
    seg_end = balanced_end(text, sec_start, "section")
    seg = text[sec_start:seg_end]
    seg2 = seg.replace("elementor-col-50 elementor-top-column", "elementor-col-100 elementor-top-column", 1)
    text = text[:sec_start] + seg2 + text[seg_end:]
    return text, True


# ───────────────────────── 3. WhatsApp duplicado ─────────────────────────
def dedupe_whatsapp(text, is_product_page):
    changed = False
    i = text.find('class="indafire-video-wa-wrapper"')
    if i >= 0:  # home: segundo card dentro da seção do vídeo
        # sobe até a seção de topo que contém o card
        j = text.rfind('<section ', 0, i)
        while j >= 0:
            end = balanced_end(text, j, "section")
            seg = text[j:end]
            if "elementor-top-section" in seg[:400] and "indafire-video-wa-wrapper" in seg:
                text = text[:j] + text[end:]
                changed = True
                break
            j = text.rfind("<section ", 0, j)
    if is_product_page:
        k = text.find('id="indafire-commercial-whatsapp"')
        if k >= 0:
            start = text.rfind("<section", 0, k)
            comment = text.rfind("<!-- SE", 0, start)
            if comment >= 0 and text[comment:start].strip().endswith("-->"):
                start = comment
            text = remove_block(text, start, "section")
            changed = True
    return text, changed


# ───────────────────────── 4. botão nos cards ─────────────────────────
# só os cards da grade (o carrossel do menu "Produtos" também usa <article class="product ...">)
ARTICLE = re.compile(r'<article class="[^"]*\bproduct\b[^"]*\bdce-item-grid\b[^"]*"[^>]*>.*?</article>', re.S)
BTN_RE = re.compile(r'\n\t\t\t\t<div class="if-card-whats-wrap">.*?</div>\n\t\t\t', re.S)  # exatamente o que add_card_button insere


def card_title(article):
    m = re.search(r'<h4 class="elementor-heading-title elementor-size-default">([^<]+)</h4>', article)
    return htmllib.unescape(m.group(1)).strip() if m else ""


def card_button(title):
    msg = "Olá! Vim pelo site da Inda Fire e gostaria de atendimento sobre: %s." % title
    href = "https://wa.me/%s?text=%s" % (WHATSAPP, urllib.parse.quote(msg))
    t = htmllib.escape(title, quote=True)
    return (
        '<div class="if-card-whats-wrap">'
        '<a class="if-card-whats" href="%s" target="_blank" rel="noopener" data-if-produto="%s" '
        'aria-label="Atendimento via WhatsApp: %s">%s<span>Atendimento via WhatsApp</span></a></div>'
        % (href, t, t, WA_SVG.format(s=20))
    )


def add_card_button(article):
    """O cliente quer o botão no menu "Produtos", não embaixo dos cards da lista:
    esta função só remove o botão que a 1ª versão (15/10) tinha colocado nos cards."""
    return BTN_RE.sub("", article)


# ── botão "Atendimento via WhatsApp" no menu Produtos (carrossel do cabeçalho) ──
MENU_ARTICLE = re.compile(r'<article class="[^"]*\bproduct\b[^"]*\bswiper-slide\b[^"]*"[^>]*>.*?</article>', re.S)
MENU_BTN_RE = re.compile(r'\n<div class="if-menu-whats-wrap">.*?</div>', re.S)


def menu_button(title):
    msg = "Olá! Vim pelo site da Inda Fire e gostaria de atendimento sobre: %s." % title
    href = "https://wa.me/%s?text=%s" % (WHATSAPP, urllib.parse.quote(msg))
    t = htmllib.escape(title, quote=True)
    return (
        '\n<div class="if-menu-whats-wrap">'
        '<a class="if-menu-whats" href="%s" target="_blank" rel="noopener" data-if-produto="%s" '
        'aria-label="Atendimento via WhatsApp: %s">%s<span>Atendimento via WhatsApp</span></a></div>'
        % (href, t, t, WA_SVG.format(s=18))
    )


def add_menu_button(article):
    article = MENU_BTN_RE.sub("", article)
    m = re.search(r'<h2 class="elementor-heading-title elementor-size-default">([^<]+)</h2>', article)
    w = re.search(r'<div class="elementor-element [^"]*elementor-widget-button"[^>]*>', article)
    if not m or not w:
        return article
    end = balanced_end(article, w.start(), "div")
    return article[:end] + menu_button(htmllib.unescape(m.group(1)).strip()) + article[end:]


# ── botão "Atendimento via WhatsApp" na imagem (banner) de produtos/categorias/produto ──
HERO_BTN_RE = re.compile(r'\n<div class="if-hero-whats-wrap">.*?</div>', re.S)


def hero_button(path, text):
    parts = Path(path).parts
    produto = ""
    if parts[0] == "produto":
        produto = product_name(text)
        msg = "Olá! Vim pelo site da Inda Fire e gostaria de atendimento sobre: %s." % produto
    elif parts[0] == "categoria-produto":
        h1 = re.search(r'id="tituloCategoriaProdutos".*?<h1[^>]*>([^<]+)</h1>', text, re.S)
        cat = htmllib.unescape(h1.group(1)).strip() if h1 else parts[1]
        msg = "Olá! Vim pelo site da Inda Fire e gostaria de atendimento sobre a categoria: %s." % cat
    else:
        msg = "Olá! Vim pelo site da Inda Fire e gostaria de atendimento sobre os produtos."
    href = "https://wa.me/%s?text=%s" % (WHATSAPP, urllib.parse.quote(msg))
    attr = ' data-if-produto="%s"' % htmllib.escape(produto, quote=True) if produto else ""
    return (
        '\n<div class="if-hero-whats-wrap">'
        '<a class="if-hero-whats" href="%s" target="_blank" rel="noopener"%s>%s<span>Atendimento via WhatsApp</span></a></div>'
        % (href, attr, WA_SVG.format(s=24))
    )


def apply_hero_button(text, path):
    text = HERO_BTN_RE.sub("", text)
    w = re.search(r'<div class="elementor-element [^>]*id="tituloCategoriaProdutos"[^>]*>', text)
    if not w:
        return text, False
    end = balanced_end(text, w.start(), "div")
    return text[:end] + hero_button(path, text) + text[end:], True


def apply_menu_buttons(text):
    new = MENU_ARTICLE.sub(lambda m: add_menu_button(m.group(0)), text)
    return new, new != text


def article_slug(article):
    m = re.search(r'produto\\?/([a-z0-9-]+)\\?/', article)
    return m.group(1) if m else None


def with_prefix(article, src_prefix, dst_prefix):
    """Reaponta os caminhos relativos de um card para a profundidade da página de destino."""
    if src_prefix == dst_prefix:
        return article
    pat = re.compile(r'(?<=["\s,])' + re.escape(src_prefix) + r'(?=(?:wp-content|produto|categoria-produto)/)')
    article = pat.sub(dst_prefix, article)
    # data-ha-element-link guarda a URL escapada: ..\/produto\/x\/
    esc_src = src_prefix.replace("/", r'\/')
    esc_dst = dst_prefix.replace("/", r'\/')
    return article.replace("&quot;" + esc_src + "produto", "&quot;" + esc_dst + "produto")


def prefix_of(path):
    depth = len(Path(path).parent.parts)
    return "../" * depth if depth else "./"


# ───────────────────────── 5. CTA do produto ─────────────────────────
CTA_RE = re.compile(
    r'<a href="#orcamento" class="elementor-button-link elementor-button elementor-size-md" role="button">\s*'
    r'<span class="elementor-button-content-wrapper">\s*<span class="elementor-button-text">Solicite or.amento</span>\s*</span>\s*</a>'
)


def product_name(text):
    m = re.search(r'<h1 class="product_title[^>]*>([^<]*)</h1>', text)
    return htmllib.unescape(m.group(1)).strip() if m else ""


def remove_product_cta(text):
    """Página de produto: o WhatsApp fica só no banner, no formulário e no botão flutuante.
    O botão ao lado da foto ("Solicite orçamento via WhatsApp") repetia o do banner."""
    m = re.search(r'<div class="elementor-element elementor-element-6f4fdbb [^>]*>', text)
    if not m:
        return text, False
    end = balanced_end(text, m.start(), "div")
    if "if-cta-whats" not in text[m.start() : end] and 'href="#orcamento"' not in text[m.start() : end]:
        return text, False
    return text[: m.start()] + text[end:], True


def apply_cta(text):
    name = product_name(text)
    if not name:
        return text, False
    msg = "Olá! Vim pelo site da Inda Fire e gostaria de um orçamento de: %s." % name
    href = "https://wa.me/%s?text=%s" % (WHATSAPP, urllib.parse.quote(msg))
    new = (
        '<a href="%s" class="elementor-button-link elementor-button elementor-size-md if-cta-whats" role="button" '
        'target="_blank" rel="noopener" data-if-produto="%s">'
        '<span class="elementor-button-content-wrapper">'
        '<span class="elementor-button-icon elementor-align-icon-left">%s</span>'
        '<span class="elementor-button-text">Solicite orçamento via WhatsApp</span></span></a>'
        % (href, htmllib.escape(name, quote=True), WA_SVG.format(s=22))
    )
    out, n = CTA_RE.subn(lambda _m: new, text, count=1)
    if n == 0 and "if-cta-whats" in text:
        return text, False
    # formulário de orçamento (dados da pessoa -> WhatsApp)
    out = out.replace(
        '<h3 class="elementor-heading-title elementor-size-default">Solicite seu orçamento</h3>',
        '<h3 class="elementor-heading-title elementor-size-default">Solicite seu orçamento via WhatsApp</h3>',
    )
    out = re.sub(
        r'(id="botao_enviar_orcamento">.*?<span class="elementor-button-text">)(?:Enviar)(</span>)',
        r"\1Enviar pelo WhatsApp\2",
        out,
        count=1,
        flags=re.S,
    )
    return out, n > 0


# ───────────────────────── 6. relacionados e lista de produtos ─────────────────────────
def grid_bounds(text):
    """(início do miolo, fim do miolo) da primeira grade DCE que tem cards de produto."""
    for m in re.finditer(r'<div class="(?:dce-posts-wrapper dce-wrapper-grid|if-rel-track)"[^>]*>', text):
        end = balanced_end(text, m.start(), "div")
        inner = text[m.end() : end - len("</div>")]
        if ARTICLE.search(inner):
            return m.end(), end - len("</div>")
    return None


RELATED_COUNT = 10
RELATED_TITLE = "Produtos relacionados e mais opções"
TRACK_OPEN = '<div class="if-rel-track" data-if-carrossel tabindex="0" aria-label="Produtos relacionados">'


def related_order(slug):
    """Os 3 mais próximos (RELATED) e depois os vizinhos deles, em ondas, até 10 produtos."""
    order, fila = [], list(RELATED[slug])
    while fila and len(order) < RELATED_COUNT:
        s = fila.pop(0)
        if s == slug or s in order:
            continue
        order.append(s)
        fila.extend(RELATED.get(s, []))
    for s in CATEGORIES:  # completa com o resto do catálogo, se faltar
        if len(order) >= RELATED_COUNT:
            break
        if s != slug and s not in order:
            order.append(s)
    return order


def collect_cards(files):
    """slug -> (card sem botão, prefixo). A lista /produtos/ vem primeiro: tem o título comercial."""
    cards = {}
    ordered = [f for f in files if f == "produtos/index.html"] + [
        f for f in files if f.startswith(("categoria-produto/", "produto/"))
    ]
    for f in ordered:
        text = (ROOT / f).read_text(encoding="utf-8")
        for m in ARTICLE.finditer(text):
            art = BTN_RE.sub("", m.group(0))
            slug = article_slug(art)
            if slug and slug not in cards:
                cards[slug] = (art, prefix_of(f))
    return cards


def build_cards(slugs, cards, dst_prefix):
    out = []
    for s in slugs:
        art, pre = cards[s]
        art = with_prefix(art, pre, dst_prefix)
        out.append(art)
    return "\n".join(out) + "\n"


EMPTY_STATE = (
    '<div class="if-categoria-vazia"><p><strong>Estamos organizando os produtos desta categoria.</strong></p>'
    "<p>Fale com a nossa equipe e receba a indicação certa para a sua necessidade.</p>"
    '<a class="if-cta-whats if-cta-whats--bloco" href="https://wa.me/%s?text=%s" target="_blank" rel="noopener">%s'
    "<span>Atendimento via WhatsApp</span></a></div>\n"
)


def apply_related(text, path, cards):
    parts = Path(path).parts
    prefix = prefix_of(path)
    if parts[0] == "produto":
        # relacionados: carrossel com 10, na ordem de afinidade (tabela RELATED)
        b = grid_bounds(text)
        slug = parts[1]
        if not b or slug not in RELATED:
            return text, False
        new_inner = build_cards(related_order(slug), cards, prefix)
        # os 3 primeiros combinam de verdade com o produto: ganham o selo "Combina com este produto"
        new_inner = re.sub(r'<article class="', '<article class="if-rel-destaque ', new_inner, count=len(RELATED[slug]))
        new = text[: b[0]] + new_inner + text[b[1] :]
        new = new.replace(
            '<h3 class="elementor-heading-title elementor-size-default">Produtos relacionados</h3>',
            '<h3 class="elementor-heading-title elementor-size-default">%s</h3>' % RELATED_TITLE,
        )
        # a grade vira trilho do carrossel (fora do layout automático do plugin, que posiciona os cards sozinho)
        new = new.replace('<div class="dce-posts-wrapper dce-wrapper-grid">', TRACK_OPEN, 1) if TRACK_OPEN not in new else new
    elif parts[0] == "categoria-produto":
        # a categoria mostra os produtos dela (já estavam certos); só ganham o botão
        new = ARTICLE.sub(lambda m: add_card_button(m.group(0)), text)
        if parts[1] in EMPTY_CATEGORIES and "if-categoria-vazia" not in new:
            m = re.search(r'<div class="dce-posts-wrapper dce-wrapper-grid">', new)
            if m:
                msg = "Olá! Vim pelo site da Inda Fire e gostaria de atendimento sobre a categoria: Incêndio florestal."
                new = new[: m.end()] + EMPTY_STATE % (WHATSAPP, urllib.parse.quote(msg), WA_SVG.format(s=20)) + new[m.end() :]
    elif parts[0] == "produtos":
        # a lista parava em 10 produtos (a 2ª página do catálogo não existe no site): entram os 3 que faltavam
        b = grid_bounds(text)
        if not b:
            return text, False
        inner = text[b[0] : b[1]]
        present = {article_slug(m.group(0)) for m in ARTICLE.finditer(inner)}
        missing = [s for s in LISTING_TAIL if s not in present]
        inner = ARTICLE.sub(lambda m: add_card_button(m.group(0)), inner)
        if missing:
            inner = inner.rstrip("\n") + "\n" + build_cards(missing, cards, prefix)
        new = text[: b[0]] + inner + text[b[1] :]
    else:
        return text, False
    return new, new != text


# ───────────────────────── assets compartilhados ─────────────────────────
# ───────────────────────── 7. abas do produto (Informações Técnicas / Quando usar / Garantia) ─────────────────────────
# No site original (indafire.com.br) a maioria destas abas está vazia. O que existe lá foi mantido.
# Os textos abaixo só entram nas abas VAZIAS e foram escritos a partir da descrição do próprio
# produto no site original (nada de especificação inventada). Garantia: só o extintor tem prazo
# informado pelo fabricante; nos demais o texto manda confirmar com a equipe.
GARANTIA_PADRAO = (
    "<p>Produto com garantia contra defeitos de fabricação, conforme as condições do fabricante.</p>"
    "<p>Para saber o prazo e as condições deste item, fale com a nossa equipe pelo WhatsApp.</p>"
)
ABAS = {
    "extintor-pqs-bc-4-kg-20bc": {
        "uso": "<p>Para apagar o começo de incêndio em <strong>líquidos e gases inflamáveis</strong> (gasolina, óleo, gás) "
        "e em <strong>equipamentos elétricos ligados</strong> (classes B e C).</p>"
        "<p>Indicado para garagens, casas de máquinas e locais com quadros de energia.</p>",
    },
    "abrigo-para-extintor": {
        "uso": "<p>Quando o extintor fica preso na parede e precisa ficar protegido de batidas, poeira e uso indevido.</p>"
        "<p>O visor na porta deixa o extintor sempre à vista e a placa “INCÊNDIO” ajuda a encontrá-lo rápido.</p>",
        "gar": GARANTIA_PADRAO,
    },
    "suporte-de-solo-para-extintor": {
        "uso": "<p>Quando o extintor deve ficar no chão, sem furar ou danificar a parede.</p>"
        "<p>Serve para extintores portáteis de pó químico, água e CO2 e evita que o equipamento caia.</p>",
        "gar": GARANTIA_PADRAO,
    },
    "placa-extintor-e5": {
        "tec": "<ul><li>Material: PVC fotoluminescente (brilha no escuro)</li><li>Espessura: 2 mm</li>"
        "<li>Superfície antiestática</li><li>Não propaga chamas: classificada como “Retardador” (IEC 60092-01:2002)</li></ul>",
        "gar": GARANTIA_PADRAO,
    },
    "armario-corta-fogo": {
        "tec": "<ul><li>Chapas de aço carbono por dentro e por fora, com isolante resistente entre elas</li>"
        "<li>Resiste a 900 °C por 1 hora</li>"
        "<li>Respiros com duplo sistema corta-chama, certificado pela FM Global Technologies LLC</li>"
        "<li>Duas portas com trinco Cremona antifaiscante e 2 chaves</li>"
        "<li>Prateleiras móveis e reguláveis, com 4 réguas de 15 em 15 cm</li>"
        "<li>Base reforçada com 4 pés niveladores</li></ul>",
        "uso": "<p>Para guardar <strong>produtos inflamáveis</strong> (tintas, solventes, combustíveis e produtos químicos) "
        "com segurança, longe de faíscas e do fogo.</p>",
        "gar": GARANTIA_PADRAO,
    },
    "capacete-gallet": {
        "tec": "<ul><li>Casco em termoplástico injetado, totalmente reforçado</li>"
        "<li>Acabamento com camada brilhante de poliuretano</li>"
        "<li>Crista no topo que ajuda a absorver impactos</li><li>Protetor de nuca aluminizado</li>"
        "<li>Viseira refletiva que protege rosto e olhos do calor</li>"
        "<li>Normas: EN 443, EN 166, EN 14458, EN 170 e EN 171</li></ul>",
        "uso": "<p>Combate a incêndios em edificações, atendimento em estradas, operações de resgate e demais atividades de bombeiros.</p>"
        "<p>Protege a cabeça contra calor, chama, frio, eletricidade, água e objetos pesados ou pontiagudos.</p>",
        "gar": GARANTIA_PADRAO,
    },
    CILINDRO: {
        "uso": "<p>Como cilindro de ar para <strong>aparelho de respiração autônoma</strong> de 300 bar, usado no combate a incêndio, "
        "no resgate e em locais com fumaça ou pouco oxigênio.</p>"
        "<p>Atenção: o cilindro é vendido <strong>vazio</strong> e precisa ser carregado antes do uso.</p>",
        "gar": GARANTIA_PADRAO,
    },
    CINTURAO: {
        "uso": "<p>Trabalhos em altura, espaços confinados, resgate técnico, acesso por cordas, evacuação e posicionamento.</p>",
        "gar": GARANTIA_PADRAO,
    },
    COLETE: {
        "uso": "<p>No atendimento pré-hospitalar, para imobilizar a coluna e o pescoço do paciente adulto com segurança e conforto, "
        "por exemplo na retirada de vítimas que estão sentadas em veículos.</p>"
        "<p>Não tem pregos nem parafusos: pode ficar no paciente durante o raio X.</p>",
        "gar": GARANTIA_PADRAO,
    },
    "mangueira-tipo-i": {"gar": GARANTIA_PADRAO},
    CHAVES: {
        "tec": "<ul><li>Para conexões com engate rápido tipo Storz</li>"
        "<li>Faz o acoplamento e o desacoplamento de duas ou mais conexões</li></ul>",
        "uso": "<p>Para conectar e soltar mangueiras, esguichos e outras conexões Storz nos hidrantes, com rapidez e sem esforço.</p>",
        "gar": GARANTIA_PADRAO,
    },
    "botoeira-de-bomba": {
        "uso": "<p>Para acionar o alarme de incêndio na mão: basta quebrar o vidro.</p>"
        "<p>Funciona com todas as centrais de alarme convencionais, em ambientes internos ou externos protegidos.</p>",
        "gar": GARANTIA_PADRAO,
    },
    UNIDADE: {
        "uso": "<p>Para manter a iluminação de emergência acesa quando falta energia, em edifícios, supermercados, boates, "
        "restaurantes, salões, hospitais e farmácias.</p>",
        "gar": GARANTIA_PADRAO,
    },
}
TAB_CONTENT = re.compile(r'(<div id="elementor-tab-content-\d+" class="elementor-tab-content[^"]*"[^>]*>)(.*?)(</div>)', re.S)


# Informação que envelhece (ano de fabricação de um lote antigo): vira regra que vale sempre.
TEXT_FIXES = {
    "&#8211; Fab 2020 &#8211; 5 anos de validade<br />": "&#8211; Validade: 5 anos a partir da data de fabricação<br />",
}


def fill_tabs(text, path):
    for antigo, novo in TEXT_FIXES.items():
        text = text.replace(antigo, novo)
    parts = Path(path).parts
    extra = ABAS.get(parts[1]) if parts[0] == "produto" else None
    if not extra:
        return text, False
    keys = iter(["tec", "uso", "gar"])

    def fill(m):
        key = next(keys, None)
        if key and not m.group(2).strip() and extra.get(key):
            return m.group(1) + extra[key] + m.group(3)
        return m.group(0)

    new = TAB_CONTENT.sub(fill, text)
    return new, new != text


def link_assets(text, path):
    prefix = prefix_of(path)
    text = re.sub(
        r'(wp-content/indafire/ajustes-responsivos\.css)\?v=\d+',
        r"\1?v=" + ASSET_VERSION,
        text,
    )
    needs_js = ("if-menu-whats" in text) or ("if-hero-whats" in text) or ("if-cta-whats" in text) or ('name="Produto"' in text)
    js_tag = '<script src="%swp-content/indafire/aviso-whatsapp-produtos.js?v=%s" defer></script>' % (prefix, ASSET_VERSION)
    if needs_js:
        if "aviso-whatsapp-produtos.js" in text:
            text = re.sub(r"(aviso-whatsapp-produtos\.js)\?v=\d+", r"\1?v=" + ASSET_VERSION, text)
        else:
            css_tag = re.search(r'<link rel="stylesheet" id="indafire-ajustes-responsivos"[^>]*>', text)
            if css_tag:
                text = text[: css_tag.start()] + js_tag + "\n" + text[css_tag.start() :]
    if "data-if-carrossel" in text:
        if "carrossel-relacionados.js" in text:
            text = re.sub(r"(carrossel-relacionados\.js)\?v=\d+", r"\1?v=" + ASSET_VERSION, text)
        else:
            css_tag = re.search(r'<link rel="stylesheet" id="indafire-ajustes-responsivos"[^>]*>', text)
            if css_tag:
                tag = '<script src="%swp-content/indafire/carrossel-relacionados.js?v=%s" defer></script>' % (prefix, ASSET_VERSION)
                text = text[: css_tag.start()] + tag + "\n" + text[css_tag.start() :]
    return text


def main(argv):
    dry = "--dry" in argv
    files = [f for f in subprocess.check_output(["git", "ls-files", "*.html"], cwd=ROOT, text=True).split("\n") if f]
    cards = collect_cards(files)
    missing = set(CATEGORIES) - set(cards)
    if missing:
        sys.exit("cards-fonte ausentes: %s" % sorted(missing))
    stats = {}
    for f in files:
        p = ROOT / f
        text = p.read_text(encoding="utf-8")
        orig = text
        is_prod = f.startswith("produto/")
        for name, fn in (
            ("rodape", remove_forms_rodape),
            ("popup", remove_catalog_popup),
            ("formsjs", strip_forms_js),
            ("bee", remove_bee),
        ):
            text, ch = fn(text)
            stats[name] = stats.get(name, 0) + ch
        text, ch = apply_menu_buttons(text)
        stats["menu"] = stats.get("menu", 0) + ch
        text, ch = dedupe_whatsapp(text, is_prod)
        stats["wa"] = stats.get("wa", 0) + ch
        if f.startswith(("produto/", "categoria-produto/", "produtos/")):
            text, ch = apply_hero_button(text, f)
            stats["hero"] = stats.get("hero", 0) + ch
        if is_prod:
            text, ch = apply_cta(text)
            stats["cta"] = stats.get("cta", 0) + ch
            text, ch = remove_product_cta(text)
            stats["cta_removido"] = stats.get("cta_removido", 0) + ch
            text, ch = fill_tabs(text, f)
            stats["abas"] = stats.get("abas", 0) + ch
        if f.startswith(("produto/", "categoria-produto/", "produtos/")):
            text, ch = apply_related(text, f, cards)
            stats["cards"] = stats.get("cards", 0) + ch
        text = link_assets(text, f)
        if text != orig:
            stats["files"] = stats.get("files", 0) + 1
            if not dry:
                with p.open("w", encoding="utf-8", newline="\r\n") as fh:  # working tree do projeto é CRLF
                    fh.write(text)
    log(stats)


if __name__ == "__main__":
    main(sys.argv[1:])
