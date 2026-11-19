#!/usr/bin/env python3
"""Ajustes pedidos na reunião de 17/11/2026 (Wellington e Mayra, Inda Fire).

1. Produtos sem catálogo ("isola isso, depois a gente vê"):
   - cada categoria vira uma página estática: a foto de fundo na tela inteira, o nome
     no meio, "Consulte-nos" e o botão do WhatsApp. Sai a lista de produtos de baixo.
   - /produtos/ mostra as categorias em seções (mosaico) com foto, nome e
     "Consulte-nos" pelo WhatsApp; cada seção abre a página da categoria.
   - o menu "Produtos" do topo fica só com as categorias (sai o carrossel de
     produtos específicos).
2. Fotos certas: EPI vira roupa e capacete de bombeiro, "Iluminações de emergência"
   deixa de usar a foto dos extintores e "Sistema de alarme de incêndio" (Serviços)
   deixa de mostrar um bico de sprinkler.
3. Sai "Resgate em altura" (categoria e produto) e saem "Unidade de treinamento móvel"
   e "Cursos online"; os endereços antigos redirecionam para /produtos/ e /treinamentos/.
4. Carrossel de serviços da home na mesma ordem da página Serviços.

Rodar DEPOIS do apply_client_adjustments_2026_10_15.py e ANTES do
scripts/build_local_preview.py. Idempotente: pode rodar de novo sem duplicar nada.
Uso: python scripts/apply_client_adjustments_2026_11_17.py [--dry]
"""
import html as htmllib
import re
import subprocess
import sys
import urllib.parse
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from scripts.apply_client_adjustments_2026_10_15 import WA_SVG, WHATSAPP, balanced_end, prefix_of  # noqa: E402

IMG_DIR = ROOT / "wp-content" / "indafire" / "img"
MEDIA = ROOT / "media" / "original"

# ── categorias que ficam, na ordem do menu (Resgate em altura saiu) ──
# Descrição só para as siglas: o público (50–70+) não precisa saber o que é "EPR".
SECOES = [
    ("extintores", None),
    ("mangueiras", None),
    ("abrigos", None),
    ("hidrantes", None),
    ("sinalizacoes", None),
    ("alarmes-de-incendio", None),
    ("iluminacoes-de-emergencia", None),
    ("sistema-de-bomba-de-incendio", None),
    ("acessorios", None),
    ("epi", "Equipamentos de proteção individual para combate a incêndio"),
    ("epr", "Equipamentos de proteção respiratória"),
    ("aph", "Atendimento pré-hospitalar"),
    ("epc", "Equipamentos de proteção coletiva"),
    ("incendio-florestal", None),
]

# foto de fundo trocada (o resto continua com a foto original da categoria)
# Melhor original disponível para o banner de cada linha (o banner ocupa a tela inteira).
# Extintores e Mangueiras: as mesmas fotos em PNG sem perda e mais altas (~1930×880) que o site
# usa nas páginas de serviço; EPI: roupa e capacete de bombeiro (banner original); Iluminações:
# a placa de saída (o banner antigo repetia a foto dos extintores). O resto só existe em 1920×616.
ORIGEM_BANNER = {
    "extintores": "wp-content/uploads/2021/10/fire-extinguisher-training-delaware-valley-safety-council-nj-pa-de.png",
    "mangueiras": "wp-content/uploads/2021/10/shutterstock_525389752.png",
    "abrigos": "wp-content/uploads/2021/12/abrigos.jpg",
    "hidrantes": "wp-content/uploads/2021/12/hidrantes.jpg",
    "sinalizacoes": "wp-content/uploads/2021/12/4894_Banners_Produtos_INDAFIRE5_Sinalizacoes.jpg",
    "alarmes-de-incendio": "wp-content/uploads/2021/12/4894_Banners_Produtos_INDAFIRE4_Alarmes.jpg",
    "iluminacoes-de-emergencia": "wp-content/uploads/2021/12/iluminacao.jpg",
    "sistema-de-bomba-de-incendio": "wp-content/uploads/2021/12/sistema-bomba.jpg",
    "acessorios": "wp-content/uploads/2021/12/acessorios.jpg",
    "epi": "media/original/2021/12/4894_Banners_Produtos_INDAFIRE8_EPI.jpg",
    "epr": "wp-content/uploads/2021/12/4894_Banners_Produtos_INDAFIRE9_EPR.jpg",
    "aph": "wp-content/uploads/2021/12/4894_Banners_Produtos_INDAFIRE10_APH.jpg",
    "epc": "wp-content/uploads/2021/12/epc.jpg",
    "incendio-florestal": "wp-content/uploads/2021/12/incendio-florestal.jpg",
}
# o banner publicado: tratado para a tela cheia (ver preparar_imagens)
FOTO_CATEGORIA = {slug: "wp-content/indafire/img/categorias/%s.jpg" % slug for slug in ORIGEM_BANNER}
ALTURA_BANNER = 880  # px: abaixo disso a foto é ampliada com qualidade e ganha nitidez leve

# Onde está o assunto em cada foto (posição horizontal, %). A foto é larga (1920×616) e, na tela
# inteira e no celular em pé, só um pedaço aparece: este é o pedaço que precisa aparecer.
FOCO = {
    "extintores": 35,
    "mangueiras": 50,
    "abrigos": 27,
    "hidrantes": 50,
    "sinalizacoes": 30,
    "alarmes-de-incendio": 27,
    "iluminacoes-de-emergencia": 74,  # no celular em pé: 32 (o corredor com a placa acesa)
    "sistema-de-bomba-de-incendio": 50,
    "acessorios": 48,
    "epi": 55,
    "epr": 50,
    "aph": 40,
    "epc": 45,
    "incendio-florestal": 65,
}

FOCO_CELULAR = {"iluminacoes-de-emergencia": 32}

ALARME_IMG = "wp-content/indafire/img/alarme-acionador.jpg"
ALARME_SPRINKLER = re.compile(r'<img\b[^>]*shutterstock_1044591571[^>]*>')

REDIRECTS = {
    "categoria-produto/resgate-em-altura/index.html": "produtos/",
    "produto/cinturao-de-seguranca-resgate-x-pert-ii/index.html": "produtos/",
    "cursos-online/index.html": "treinamentos/",
    "treinamentos/cursos-online/index.html": "treinamentos/",
    "unidade-de-treinamento-movel/index.html": "treinamentos/",
    "treinamentos/unidade-de-treinamento-movel/index.html": "treinamentos/",
    "cursos/index.html": "treinamentos/",
}
REDIRECT_PREFIX = "<!-- indafire: redirecionamento"
STUB_MARK = "<!-- indafire: redirecionamento (17/11/2026) -->"

# colunas do card "Unidade móvel" e "Cursos online" em /treinamentos/
COLUNAS_TREINAMENTO = ("23d699d", "1302736")
# coluna "Produtos" (produtos específicos) do menu suspenso "Produtos"
COLUNA_MENU_PRODUTOS = "db7b976"

# Carrosséis de serviços (home e menu Serviços): "serviços que vendem mais vêm na frente;
# fabricação de caixa d'água é o último" (Wellington, 17/11). Extintores primeiro, depois
# regularização, manutenção, sistemas e os serviços especiais. Mudar a ordem = mexer só aqui.
ORDEM_SERVICOS = [
    197,  # Recarga de extintores
    194,  # Instalação e venda de extintores
    191,  # AVCB/CLCB – Obtenção ou renovação
    179,  # Projeto Técnico
    200,  # Teste hidrostático em mangueiras
    203,  # Inspeção de equipamentos
    188,  # Processo simplificado (PTS)
    206,  # Sistema de hidrantes
    209,  # Sistema de alarme de incêndio
    212,  # Detecção de fumaça e calor
    216,  # Iluminação de emergência
    219,  # Sprinklers
    222,  # Sinalização de emergência
    228,  # Locação de equipamentos
    231,  # Equipe habilitada para eventos
    234,  # Fabricação de caixa d'água metálica (sempre o último)
]
# Cards do menu Serviços. O WordPress só mostrava 10 serviços (e tirava o da própria página);
# agora o menu mostra todos. id -> (endereço, foto a partir de wp-content/, título como no site original)
MENU_SERVICOS_CARDS = {
    179: ("projeto-tecnico", "uploads/2021/10/serv14.jpg", "Projeto Técnico"),
    188: ("processo-simplificado-pts", "uploads/2021/10/serv15.jpg", "Processo simplificado (PTS)"),
    191: ("obtencao-ou-renovacao-avcb-clcb", "uploads/2021/10/serv16.jpg", "AVCB/CLCB – Obtenção ou renovação"),
    194: ("instalacao-e-venda-de-extintores", "uploads/2021/10/serv2.jpg", "Instalação e venda de extintores"),
    197: ("recarga-de-extintores", "uploads/2021/10/serv3.jpg", "Recarga de Extintores"),
    200: ("teste-hidrostatico-em-mangueiras-de-incendios", "uploads/2021/10/serv4.jpg", "Teste Hidrostático em Mangueiras de Incêndios"),
    203: ("inspecao-de-equipamentos", "uploads/2021/10/serv5.jpg", "Inspeção de Equipamentos"),
    206: ("sistema-de-hidrantes", "uploads/2021/10/hidrantes.jpg", "Sistema de Hidrantes"),
    209: ("sistema-de-alarme-de-incendio", "indafire/img/alarme-acionador.jpg", "Sistema de alarme de incêndio"),
    212: ("sistema-de-deteccao-de-fumaca-e-calor", "uploads/2021/10/serv9.jpg", "Sistema de detecção de fumaça e calor"),
    216: ("sistema-de-iluminacao-de-emergencia", "uploads/2021/10/iluminacao.jpg", "Sistema de iluminação de emergência"),
    219: ("sistemas-de-sprinklers", "uploads/2021/10/Sprinkler.jpg", "Sistemas de Sprinklers"),
    222: ("sinalizacao-de-emergencia", "uploads/2021/10/serv10.jpg", "Sinalização de Emergência"),
    228: ("locacao-de-equipamentos", "uploads/2021/10/PRONTA-5.png", "Locação de equipamentos"),
    231: ("disponibilizacao-de-equipe-habilitada-para-eventos-ou-trabalhos-especificos", "uploads/2021/10/serv12.jpg",
          "Equipe habilitada para eventos ou trabalhos específicos"),
    234: ("fabricacao-de-caixa-dagua-metalica", "uploads/2021/10/serv13.jpg", "Fabricação de caixa d’água metálica"),
}
MENU_SERVICOS_WIDGET = 'data-id="b7b83cb"'


def log(*a):
    print(*a)


# ───────────────────────── utilitários ─────────────────────────
def element_end(text, start):
    """Fim do elemento (qualquer tag) que abre em `start`, contando aninhamento."""
    name = re.match(r"<([a-zA-Z0-9]+)", text[start:]).group(1).lower()
    depth = 0
    for m in re.finditer(r"<(/?)%s\b[^>]*?(/?)>" % name, text[start:], re.I):
        if m.group(2) == "/":
            continue
        depth += -1 if m.group(1) else 1
        if depth == 0:
            return start + m.end()
    raise ValueError("tag <%s> sem fechamento" % name)


ENVOLVENTES = [
    re.compile(r'<option\b[^>]*value="resgate-em-altura"[^>]*>'),
    re.compile(r'<li\b[^>]*class="[^"]*\bcat-item\b[^"]*"[^>]*>'),
    re.compile(r'<div class="swiper-slide[^"]*"[^>]*>'),
    re.compile(r'<div class="elementor-element [^"]*\belementor-widget-image-box\b[^"]*"[^>]*>'),
]


def remove_enclosing(text, link_re, envolventes=ENVOLVENTES):
    """Remove o menor elemento envolvente (da lista) de cada link que casa com link_re."""
    n = 0
    pos = 0
    while True:
        m = link_re.search(text, pos)
        if not m:
            return text, n
        melhor = None
        for pat in envolventes:
            for o in pat.finditer(text, max(0, m.start() - 6000), m.start() + 1):
                try:
                    fim = element_end(text, o.start())
                except ValueError:
                    continue
                if fim >= m.end() and (melhor is None or o.start() > melhor[0]):
                    melhor = (o.start(), fim)
        if melhor is None:
            pos = m.end()  # link solto (ex.: dentro de texto): fica para a conferência final
            continue
        text = text[: melhor[0]] + text[melhor[1]:]
        pos = melhor[0]
        n += 1


def remove_by_data_id(text, data_id, tag="div"):
    n = 0
    while True:
        m = re.search(r'<%s\b[^>]*data-id="%s"[^>]*>' % (tag, data_id), text)
        if not m:
            return text, n
        text = text[: m.start()] + text[element_end(text, m.start()):]
        n += 1


def whatsapp_href(msg):
    return "https://wa.me/%s?text=%s" % (WHATSAPP, urllib.parse.quote(msg))


# ───────────────────────── imagens ─────────────────────────
def preparar_imagens(dry):
    from PIL import Image

    def salvar(origem, destino, largura=None, qualidade=82):
        if destino.exists():
            return
        im = Image.open(origem).convert("RGB")
        if largura and im.width > largura:
            im = im.resize((largura, round(im.height * largura / im.width)), Image.LANCZOS)
        if not dry:
            destino.parent.mkdir(parents=True, exist_ok=True)
            im.save(destino, "JPEG", quality=qualidade, optimize=True, progressive=True)
        log("imagem", destino.relative_to(ROOT))

    from PIL import ImageFilter

    def banner(origem, destino):
        """Banner de tela cheia: sem perda de cor no vermelho (4:4:4) e, se a foto for baixa,
        ampliação Lanczos até ALTURA_BANNER com nitidez leve (não inventa detalhe: só evita que o
        navegador estique a foto pequena e a deixe borrada)."""
        if destino.exists() and destino.stat().st_mtime >= origem.stat().st_mtime:
            return
        im = Image.open(origem).convert("RGB")
        if im.height < ALTURA_BANNER:
            im = im.resize((round(im.width * ALTURA_BANNER / im.height), ALTURA_BANNER), Image.LANCZOS)
            im = im.filter(ImageFilter.UnsharpMask(radius=2, percent=55, threshold=3))
        if not dry:
            destino.parent.mkdir(parents=True, exist_ok=True)
            im.save(destino, "JPEG", quality=86, optimize=True, progressive=True, subsampling=0)
        log("imagem", destino.relative_to(ROOT), im.size)

    salvar(MEDIA / "2021/11/central-alarme-incendio-02.jpg", ROOT / ALARME_IMG)
    for slug, _ in SECOES:
        banner(ROOT / ORIGEM_BANNER[slug], ROOT / FOTO_CATEGORIA[slug])
    for slug, _ in SECOES:
        origem = ROOT / foto_da_categoria(slug)
        destino = IMG_DIR / "secoes" / ("%s.jpg" % slug)
        if dry and not origem.exists():
            continue  # no --dry a foto nova ainda não foi gravada
        if destino.exists() and origem.exists() and destino.stat().st_mtime < origem.stat().st_mtime:
            destino.unlink()  # o banner mudou: refaz a foto do mosaico
        salvar(origem, destino, largura=1440, qualidade=78)

    # fotos recortadas do catálogo (fundo transparente) → WebP leve, no máximo 720 px de altura
    for slug, _ in SECOES:
        origem = RECORTES / ("%s.png" % slug)
        destino = IMG_DIR / "produtos" / ("%s.webp" % slug)
        if not origem.exists() or destino.exists():
            continue
        im = Image.open(origem).convert("RGBA")
        if im.height > 720:
            im = im.resize((round(im.width * 720 / im.height), 720), Image.LANCZOS)
        if not dry:
            destino.parent.mkdir(parents=True, exist_ok=True)
            im.save(destino, "WEBP", quality=84, method=6)
        log("imagem", destino.relative_to(ROOT))


def foto_da_categoria(slug):
    if slug in FOTO_CATEGORIA:
        return FOTO_CATEGORIA[slug]
    s = (ROOT / "categoria-produto" / slug / "index.html").read_text(encoding="utf-8")
    a = s.find('data-elementor-type="product-archive"')
    m = re.search(r'data-dce-background-image-url="(?:\.\./)*([^"]+)"', s[a: a + 4000])
    return m.group(1)


def titulo_da_categoria(text):
    m = re.search(r'id="tituloCategoriaProdutos".*?<h1[^>]*>([^<]+)</h1>', text, re.S)
    return htmllib.unescape(m.group(1)).strip() if m else None


# ───────────────────────── 1. categorias e /produtos/ ─────────────────────────
def archive_bounds(text):
    a = text.find('data-elementor-type="product-archive"')
    if a < 0:
        return None
    wrap = text.find('<div class="elementor-section-wrap">', a)
    hero = text.find("<section", wrap)
    return wrap, hero, balanced_end(text, hero, "section"), balanced_end(text, wrap, "div")


def isolar_catalogo(text):
    """Tira tudo que vem depois da foto (migalhas, filtros, lista de produtos)."""
    b = archive_bounds(text)
    if not b:
        return text, False
    _wrap, _hero, hero_end, wrap_end = b
    miolo = text[hero_end:wrap_end]
    fim_miolo = miolo.rfind("</div>")  # o </div> que fecha o section-wrap
    sobra = miolo[:fim_miolo]
    if "<section" not in sobra:
        return text, False
    text = text[:hero_end] + "\n" + miolo[fim_miolo:] + text[wrap_end:]
    return text, True


def trocar_foto(text, slug):
    nova = FOTO_CATEGORIA.get(slug)
    if not nova:
        return text, False
    a = text.find('data-elementor-type="product-archive"')
    m = re.search(r'data-dce-background-image-url="((?:\.\./)*)([^"]+)"', text[a: a + 4000])
    if not m or m.group(2) == nova:
        return text, False
    antiga = m.group(2)
    return text.replace(antiga, nova), True


def foco_hero(text, slug):
    m = re.search(r'<section\b[^>]*\bid="bannerProdutoINDA"[^>]*>', text)
    if not m or slug not in FOCO:
        return text, False
    tag = re.sub(r'\sstyle="--if-foco:[^"]*"', "", m.group(0))
    estilo = "--if-foco:%d%%" % FOCO[slug]
    if slug in FOCO_CELULAR:
        estilo += ";--if-foco-m:%d%%" % FOCO_CELULAR[slug]
    tag = tag.replace("<section", '<section style="%s"' % estilo, 1)
    new = text[: m.start()] + tag + text[m.end():]
    return new, new != text


CONSULTE_RE = re.compile(r'\n?<p class="if-hero-consulte">.*?</p>', re.S)
HERO_BTN_RE = re.compile(r'\n?<div class="if-hero-whats-wrap">.*?</div>', re.S)
CUE_RE = re.compile(r'\n?<div class="if-hero-cue-wrap">.*?</div>', re.S)
CUE = ('\n<div class="if-hero-cue-wrap"><a class="if-hero-cue" href="#if-linha">'
       "<span>Conheça a linha</span><i aria-hidden=\"true\"></i></a></div>")


def hero_cue(text):
    """Banner da categoria: só a foto e o nome. O WhatsApp desce para depois das especialidades."""
    new = CUE_RE.sub("", CONSULTE_RE.sub("", HERO_BTN_RE.sub("", text)))
    w = re.search(r'<div class="elementor-element [^>]*id="tituloCategoriaProdutos"[^>]*>', new)
    if not w:
        return text, False
    end = balanced_end(new, w.start(), "div")
    new = new[:end] + CUE + new[end:]
    return new, new != text


# ── o que cada linha oferece: itens do catálogo oficial (os mesmos do site-novo/src/data/conteudo.ts) ──
# e os serviços que a própria Inda Fire já descreve no site (links para as páginas de serviço).
OUTROS = "Outros modelos e medidas: consulte-nos"

# Cada item é (título, subtítulo). O subtítulo dá o modelo, a medida ou o uso; o que não está definido
# fica como "consulte-nos", para a lista não limitar o que a Inda Fire vende. As medidas de mangueiras
# e os itens de alarme vêm do retorno do Wellington (reunião de 17/11); o resto, das páginas de produto.
LINHAS = {
    "extintores": (
        [
            ("Pó químico ABC e BC", "Modelo 4 kg, 2-A 20-BC (NBR 15808). Outras capacidades: consulte-nos"),
            ("Gás carbônico (CO₂)", "Para equipamentos elétricos e eletrônicos. Capacidades: consulte-nos"),
            ("Água", "Para papel, madeira e tecido. Capacidades: consulte-nos"),
            ("Espuma", "Para líquidos inflamáveis e sólidos. Capacidades: consulte-nos"),
            ("Classe K e classe D", "K: óleos e gorduras de cozinha. D: metais combustíveis. Capacidades: consulte-nos"),
        ],
        ["instalacao-e-venda-de-extintores", "recarga-de-extintores", "inspecao-de-equipamentos"],
    ),
    "mangueiras": (
        [
            ("Mangueiras de incêndio até o tipo 5", "Do tipo 1 ao tipo 5. Outras especificações: consulte-nos"),
            ("Comprimentos", "De 15 a 30 metros. Para outros comprimentos, consulte-nos"),
            ("Diâmetros", "De 1,5 a 2,5 polegadas. Para diâmetros maiores, consulte-nos"),
        ],
        ["teste-hidrostatico-em-mangueiras-de-incendios"],
    ),
    "abrigos": (
        [
            ("Abrigos para extintor", "De sobrepor, em chapa de aço pintada de vermelho, com porta e visor. Outras medidas: consulte-nos"),
            ("Abrigos para mangueira", OUTROS),
        ],
        [],
    ),
    "hidrantes": (
        [
            ("Esguichos", OUTROS),
            ("Chaves Storz", "Acoplam e desacoplam conexões de engate rápido Storz. Outros modelos: consulte-nos"),
            ("Adaptadores", OUTROS),
            ("Canhões", OUTROS),
        ],
        ["sistema-de-hidrantes"],
    ),
    "sinalizacoes": (
        [
            ("Placas fotoluminescentes de rota de fuga", "Brilham no escuro, em PVC de 2 mm. Outros tamanhos: consulte-nos"),
            ("Placas de identificação de equipamentos", "Como a placa de extintor E5. Outros modelos: consulte-nos"),
        ],
        ["sinalizacao-de-emergencia"],
    ),
    "alarmes-de-incendio": (
        [
            ("Acionadores manuais", "De quebra de vidro, para uso com centrais convencionais. Outros modelos: consulte-nos"),
            ("Detectores", "De fumaça e de calor. Modelos: consulte-nos"),
            ("Centrais de alarme", OUTROS),
            ("Sirenes", OUTROS),
        ],
        ["sistema-de-alarme-de-incendio", "sistema-de-deteccao-de-fumaca-e-calor"],
    ),
    "iluminacoes-de-emergencia": (
        [
            ("Blocos autônomos", OUTROS),
            ("Luminárias de LED", OUTROS),
            ("Centrais de iluminação", "Unidade central Lux 700 e Lux 1200, 24 VDC. Outros modelos: consulte-nos"),
        ],
        ["sistema-de-iluminacao-de-emergencia"],
    ),
    "sistema-de-bomba-de-incendio": (
        [
            ("Bombas jockey", "Mantêm a rede de hidrantes pressurizada. Modelos e vazões: consulte-nos"),
            ("Sistemas de bomba completos", "Conforme a vazão e a pressão do seu projeto: consulte-nos"),
        ],
        ["sistema-de-hidrantes", "sistemas-de-sprinklers"],
    ),
    "acessorios": (
        [
            ("Suportes para extintor", "Suporte de solo em aço carbono, tamanhos grande e pequeno. Outros modelos: consulte-nos"),
            ("Portas corta-fogo", "Medidas e modelos: consulte-nos"),
            ("Barras antipânico", "Para portas de saída de emergência. Modelos: consulte-nos"),
        ],
        [],
    ),
    "epi": (
        [
            ("Capacetes", "Capacete Gallet: casco reforçado, protetor de nuca e viseira refletiva. Outros modelos: consulte-nos"),
            ("Luvas", "Tamanhos e modelos: consulte-nos"),
            ("Botas", "Numerações e modelos: consulte-nos"),
            ("Roupas de combate a incêndio", "Tamanhos e modelos: consulte-nos"),
        ],
        [],
    ),
    "epr": (
        [
            ("Equipamentos de respiração autônoma", OUTROS),
            ("Cilindros de ar", "Cilindro de 6 litros, em aço, com válvula de 300 bar. Outras capacidades: consulte-nos"),
        ],
        [],
    ),
    "aph": (
        [
            ("Pranchas", OUTROS),
            ("Colares cervicais", "Tamanhos: consulte-nos"),
            ("Colete imobilizador (KED)", "Modelo adulto. Outros tamanhos: consulte-nos"),
        ],
        [],
    ),
    "epc": (
        [
            ("Chuveiro lava-olhos", OUTROS),
            ("Armário corta-fogo", "Resiste a 900 °C por 1 hora. Outras medidas: consulte-nos"),
        ],
        [],
    ),
    "incendio-florestal": (
        [
            ("Abafadores", OUTROS),
            ("Rastelos", OUTROS),
            ("Ferramentas de combate", OUTROS),
        ],
        [],
    ),
}

SERVICOS = {
    "instalacao-e-venda-de-extintores": "Instalação e venda de extintores",
    "recarga-de-extintores": "Recarga de extintores",
    "inspecao-de-equipamentos": "Inspeção de equipamentos",
    "teste-hidrostatico-em-mangueiras-de-incendios": "Teste hidrostático em mangueiras",
    "sistema-de-hidrantes": "Sistema de hidrantes",
    "sinalizacao-de-emergencia": "Sinalização de emergência",
    "sistema-de-alarme-de-incendio": "Sistema de alarme de incêndio",
    "sistema-de-deteccao-de-fumaca-e-calor": "Detecção de fumaça e calor",
    "sistema-de-iluminacao-de-emergencia": "Sistema de iluminação de emergência",
    "sistemas-de-sprinklers": "Sistemas de sprinklers",
}

RECORTES = ROOT / "site-novo" / "src" / "assets" / "produtos"  # fotos reais do catálogo, recortadas
LINHA_RE = re.compile(r'\n?<section class="if-linha".*?<!-- /if-linha -->', re.S)


def recorte(slug):
    """(arquivo publicado, pequeno?) da foto recortada do produto, ou None."""
    p = IMG_DIR / "produtos" / ("%s.webp" % slug)
    if not p.exists():
        return None
    from PIL import Image

    with Image.open(p) as im:
        return p, max(im.size) < 320


def bloco_linha(slug, nome):
    itens, servicos = LINHAS[slug]
    lista = "".join(
        '<li><span>%02d</span><div><b>%s</b><small>%s</small></div></li>' % (i + 1, htmllib.escape(t), htmllib.escape(sub))
        for i, (t, sub) in enumerate(itens)
    )
    serv = ""
    if servicos:
        serv = (
            '<div class="if-linha__servicos"><p>Serviços ligados a esta linha</p><ul>%s</ul></div>'
            % "".join('<li><a href="../../servicos_inda_fire/%s/">%s</a></li>' % (s, htmllib.escape(SERVICOS[s])) for s in servicos)
        )
    rec = recorte(slug)
    produto = ""
    if rec:
        produto = '<img class="if-linha__produto%s" src="../../wp-content/indafire/img/produtos/%s.webp" alt="%s" loading="lazy" decoding="async">' % (
            " if-linha__produto--pequeno" if rec[1] else "",
            slug,
            htmllib.escape("Exemplo da linha %s da Inda Fire" % nome, quote=True),
        )
    # com a foto recortada do produto: fundo de estúdio escuro (a foto do banner já está no topo);
    # sem recorte (EPR): a própria foto da linha
    if produto:
        classe_visual, fundo = " if-linha__visual--estudio", ""
    else:
        classe_visual = ""
        fundo = (
            '<img class="if-linha__fundo" src="../../wp-content/indafire/img/secoes/%s.jpg" alt="" loading="lazy" '
            'decoding="async" style="object-position:%d%% 50%%">' % (slug, FOCO.get(slug, 50))
        )
    msg = "Olá! Vim pelo site da Inda Fire e gostaria de atendimento sobre a linha: %s." % nome
    return (
        '\n<section class="if-linha" id="if-linha" aria-labelledby="if-linha-titulo">'
        '<div class="if-linha__grade">'
        '<div class="if-linha__texto" data-if-revelar>'
        '<p class="if-linha__kicker">Linha %s</p>'
        '<h2 class="if-linha__titulo" id="if-linha-titulo">O que a Inda Fire oferece</h2>'
        '<p class="if-linha__intro">Estes são os itens desta linha. Fale com a nossa equipe para saber preço, prazo '
        "e o modelo certo para o seu caso.</p>"
        '<ol class="if-linha__itens">%s</ol>%s</div>'
        '<figure class="if-linha__visual%s" data-if-revelar>%s%s</figure>'
        "</div></section>"
        '<section class="if-linha-cta" aria-labelledby="if-linha-cta-titulo"><div class="if-linha-cta__caixa">'
        '<div><h2 id="if-linha-cta-titulo">Fale com a nossa equipe</h2>'
        "<p>Conte o que você precisa. A gente responde pelo WhatsApp.</p></div>"
        '<div class="if-linha-cta__acoes">'
        '<a class="if-linha-cta__whats" href="%s" target="_blank" rel="noopener" data-if-produto="%s">%s<span>Chamar no WhatsApp</span></a>'
        '<a class="if-linha-cta__tel" href="tel:+551938341741">ou ligue <strong>(19) 3834-1741</strong></a>'
        "</div></div></section>%s<!-- /if-linha -->"
    ) % (
        htmllib.escape(nome),
        lista,
        serv,
        classe_visual,
        fundo,
        produto,
        htmllib.escape(whatsapp_href(msg), quote=True),
        htmllib.escape(nome, quote=True),
        WA_SVG.format(s=22),
        REVELAR_JS,
    )


def pagina_categoria(text, slug, nome):
    new = LINHA_RE.sub("", text)
    # o cartão antigo "Atendimento via WhatsApp" repetiria o convite do fim da página
    m = re.search(r'<section\b[^>]*\bid="indafire-commercial-whatsapp"[^>]*>', new)
    if m:
        new = new[: m.start()] + new[element_end(new, m.start()):]
    new, _ = isolar_catalogo(new)
    new, _ = trocar_foto(new, slug)
    new, _ = hero_cue(new)
    new, _ = foco_hero(new, slug)
    b = archive_bounds(new)
    if b:
        new = new[: b[2]] + bloco_linha(slug, nome) + new[b[2]:]
    return new, new != text


SECOES_RE = re.compile(r'\n?<section class="if-secoes".*?</section><!-- /if-secoes -->', re.S)

REVELAR_JS = (
    "<script>(function(){var d=document.documentElement;if(!('IntersectionObserver' in window)||"
    "window.matchMedia('(prefers-reduced-motion: reduce)').matches)return;d.classList.add('if-movimento');"
    "var ok=false,els=document.querySelectorAll('[data-if-revelar]');"
    "var io=new IntersectionObserver(function(es){ok=true;es.forEach(function(e){if(e.isIntersecting){"
    "e.target.classList.add('is-visivel');io.unobserve(e.target);}});},{rootMargin:'0px 0px -8% 0px'});"
    "els.forEach(function(el){io.observe(el);});"
    "setTimeout(function(){if(!ok){els.forEach(function(el){el.classList.add('is-visivel');});}},3000);})();</script>"
)


# mosaico: duas seções grandes (2×2) e algumas largas (2×1) para quebrar a grade; o resto 1×1
TAMANHO = {
    "extintores": "grande",
    "alarmes-de-incendio": "larga",
    "iluminacoes-de-emergencia": "larga",
    "epi": "grande",
    "epc": "larga",
    "incendio-florestal": "larga",
}


def bloco_secoes(titulos):
    """Mosaico de /produtos/: cada seção é um link para a página da linha (sem botão de WhatsApp aqui)."""
    itens = []
    for i, (slug, desc) in enumerate(SECOES):
        nome = titulos[slug]
        tam = TAMANHO.get(slug)
        itens.append(
            '<li class="if-secao%s" data-if-revelar style="--i:%d">'
            '<a class="if-secao__link" href="../categoria-produto/%s/">'
            '<img class="if-secao__foto" src="../wp-content/indafire/img/secoes/%s.jpg" width="1440" height="462" '
            'loading="lazy" decoding="async" alt="" style="object-position:%d%% 50%%">'
            '<span class="if-secao__num" aria-hidden="true">%02d</span>'
            '<span class="if-secao__texto">'
            '<h3 class="if-secao__titulo">%s</h3>%s'
            '<span class="if-secao__chamada">Consulte-nos<i aria-hidden="true"></i></span>'
            "</span></a></li>"
            % (
                (" if-secao--%s" % tam) if tam else "",
                i % 4,
                slug,
                slug,
                FOCO.get(slug, 50),
                i + 1,
                htmllib.escape(nome),
                ('<span class="if-secao__desc">%s</span>' % htmllib.escape(desc)) if desc else "",
            )
        )
    return (
        '\n<section class="if-secoes" id="if-produtos-secoes" aria-labelledby="if-secoes-titulo">'
        '<div class="if-secoes__topo"><p class="if-secoes__kicker">Produtos</p>'
        '<h2 id="if-secoes-titulo">Escolha a linha</h2>'
        "<p>Toque em uma linha para ver o que a Inda Fire oferece.</p></div>"
        '<ul class="if-secoes__grade">%s</ul>%s</section><!-- /if-secoes -->' % ("".join(itens), REVELAR_JS)
    )


def pagina_produtos(text, titulos):
    changed = False
    new = SECOES_RE.sub("", text)
    new, ch = isolar_catalogo(new)
    b = archive_bounds(new)
    if b:
        hero_end = b[2]
        new = new[:hero_end] + bloco_secoes(titulos) + new[hero_end:]
    # o título do banner estava em inglês
    new = re.sub(r'(<h1 class="elementor-heading-title[^"]*">)\s*Products\s*(</h1>)', r"\1Produtos\2", new)
    new = new.replace(">Products</a>", ">Produtos</a>").replace(">Products</span>", ">Produtos</span>")
    changed = new != text
    return new, changed


# ───────────────────────── 2. fotos certas ─────────────────────────
def alarme_sem_sprinkler(text, path):
    prefix = prefix_of(path)

    def troca(m):
        tag = m.group(0)
        tag = re.sub(r'\s(srcset|sizes|data-srcset|data-sizes|data-lazy-srcset|data-lazy-sizes)="[^"]*"', "", tag)
        tag = re.sub(r'\s(src|data-lazy-src)="[^"]*shutterstock_1044591571[^"]*"', r' \1="%s%s"' % (prefix, ALARME_IMG), tag)
        tag = re.sub(r'\swidth="\d+"', ' width="800"', tag)
        tag = re.sub(r'\sheight="\d+"', ' height="508"', tag)
        if " alt=" in tag:
            tag = re.sub(r'\salt="[^"]*"', ' alt="Acionador manual de alarme de incêndio na parede"', tag)
        return tag

    new = ALARME_SPRINKLER.sub(troca, text)
    # fundos de chamada ("outros serviços"): data-bg e url(...)
    novo = prefix + ALARME_IMG
    new = re.sub(r'(\sdata-(?:lazy-)?bg=")[^"]*shutterstock_1044591571[^"]*(")', lambda m: m.group(1) + novo + m.group(2), new)
    new = re.sub(r'url\(\s*["\']?[^)"\']*shutterstock_1044591571[^)"\']*["\']?\s*\)', lambda m: 'url("%s")' % novo, new)
    # metadados (og:image, JSON-LD) e o title herdado do arquivo antigo
    new = re.sub(r'\stitle="shutterstock_1044591571[^"]*"', "", new)

    def url_meta(m):
        token = m.group(0)
        bs = chr(92)
        if bs in token:  # JSON com barras escapadas
            return "https:" + bs + "/" + bs + "/indafire.com.br" + bs + "/" + ALARME_IMG.replace("/", bs + "/")
        if token.startswith("http"):
            return "https://indafire.com.br/" + ALARME_IMG
        return novo

    new = re.sub(r'[^"\'\s()]*shutterstock_1044591571-scaled-1[^"\'\s()]*?\.png', url_meta, new)
    return new, new != text


# ───────────────────────── 3. remoções ─────────────────────────
RESGATE_LINK = re.compile(r'href="[^"]*categoria-produto/resgate-em-altura/?"')
RESGATE_ARTIGO = re.compile(r'<article\b[^>]*\bproduct_cat-resgate-em-altura\b[^>]*>')
TREINO_LINK = re.compile(r'href="[^"]*(?:cursos-online|unidade-de-treinamento-movel)/?"')


RESGATE_OPCAO = re.compile(r'<option\b[^>]*value="resgate-em-altura"[^>]*>.*?</option>\s*', re.S)


def sem_resgate(text):
    text, n = RESGATE_OPCAO.subn("", text)
    while True:
        m = RESGATE_ARTIGO.search(text)
        if not m:
            break
        text = text[: m.start()] + text[element_end(text, m.start()):]
        n += 1
    text, k = remove_enclosing(text, RESGATE_LINK)
    return text, n + k


def menu_so_categorias(text):
    text, n = remove_by_data_id(text, COLUNA_MENU_PRODUTOS)
    return text, n


def treinamentos(text):
    total = 0
    for did in COLUNAS_TREINAMENTO:
        text, n = remove_by_data_id(text, did)
        total += n
    return text, total


def stub(path, destino):
    prefix = prefix_of(path)
    alvo = prefix + destino
    return (
        "<!DOCTYPE html>\n<html lang=\"pt-BR\">\n<head>\n" + STUB_MARK + "\n"
        '<meta charset="UTF-8">\n<meta name="viewport" content="width=device-width, initial-scale=1">\n'
        '<meta name="robots" content="noindex, follow">\n'
        '<meta http-equiv="refresh" content="0; url=%s">\n'
        '<link rel="canonical" href="https://indafire.com.br/%s">\n'
        "<title>Inda Fire - Equipamentos de Combate a Incêndios</title>\n"
        "</head>\n<body>\n"
        '<p style="font:16px/1.5 \'Open Sans\',Arial,sans-serif;text-align:center;margin:40px 16px">'
        'Esta página mudou. <a href="%s">Continuar no site da Inda Fire</a>.</p>\n'
        "<script>location.replace(%s);</script>\n</body>\n</html>\n"
    ) % (alvo, destino, alvo, repr(alvo))


# ───────────────────────── 4. ordem do carrossel de serviços ─────────────────────────
def ordenar_carrossel_servicos(text):
    w = text.find('id="carrosselServicos"')
    if w < 0:
        return text, False
    start = text.rfind("<div", 0, w)
    end = balanced_end(text, start, "div")
    bloco = text[start:end]
    bloco_novo = ordenar_artigos(bloco)
    return text[:start] + bloco_novo + text[end:], bloco_novo != bloco


ARTIGO_POST = re.compile(r'<article\b[^>]*\bpost-(\d+)\b[^>]*>')


def card_menu_novo(modelo, pid_modelo, pid):
    """Card do menu Serviços para um serviço que faltava, feito a partir de um card que já existe."""
    slug_m = MENU_SERVICOS_CARDS[pid_modelo][0]
    slug, foto, titulo = MENU_SERVICOS_CARDS[pid]
    card = modelo.replace("post-%d" % pid_modelo, "post-%d" % pid)
    card = re.sub(r'(data-(?:dce-post-id|post-id|obj-id))="%d"' % pid_modelo, r'\g<1>="%d"' % pid, card)
    card = card.replace("/" + slug_m + "\\/", "/" + slug + "\\/").replace("/" + slug_m + "/", "/" + slug + "/")
    card = re.sub(r'\btipos-[\w-]+ ', "", card, count=1)
    img = re.search(r'<img\b[^>]*>', card)
    tag = img.group(0)
    base = re.search(r'="([^"]*?)wp-content/', tag).group(1)  # mesmo prefixo de pasta da página
    url = "%swp-content/%s" % (base, foto)

    def trocar(m):  # src/srcset e as versões de carregamento tardio (data-lazy-*); o marcador svg fica
        nome, valor = m.group(1), m.group(2)
        if "wp-content/" not in valor:
            return m.group(0)
        return '%s="%s"' % (nome, url + " 500w" if nome.endswith("srcset") else url)

    nova = re.sub(r'(?<![\w-])((?:data-lazy-)?(?:src|srcset))="([^"]*)"', trocar, tag)
    card = card[: img.start()] + nova + card[img.end():]
    card = re.sub(r'(<noscript><img\b[^>]*>)', lambda m: re.sub(
        r'(?<![\w-])(src|srcset)="([^"]*)"', trocar, m.group(1)), card)
    card, n = re.subn(r'(<h2 class="elementor-heading-title[^"]*">)[^<]*(</h2>)',
                      lambda m: m.group(1) + htmllib.escape(titulo, quote=False) + m.group(2), card, count=1)
    if n != 1 or slug not in card:
        raise SystemExit("menu Serviços: não consegui montar o card %d" % pid)
    return card


def ordenar_artigos(bloco, completar=None):
    arts = list(ARTIGO_POST.finditer(bloco))
    pecas = {int(m.group(1)): bloco[m.start(): element_end(bloco, m.start())] for m in arts}
    if completar:
        pid_modelo = int(arts[0].group(1))
        modelo = pecas[pid_modelo]
        for pid in ORDEM_SERVICOS:
            if pid not in pecas:
                pecas[pid] = completar(modelo, pid_modelo, pid)
    if set(pecas) != set(ORDEM_SERVICOS):
        raise SystemExit("carrossel de serviços: itens inesperados %s" % sorted(set(pecas) ^ set(ORDEM_SERVICOS)))
    a0 = arts[0].start()
    a1 = element_end(bloco, arts[-1].start())
    sep = bloco[element_end(bloco, arts[0].start()): arts[1].start()]
    novos = [re.sub(r'data-dce-post-index="\d+"', 'data-dce-post-index="%d"' % i, pecas[pid], count=1)
             for i, pid in enumerate(ORDEM_SERVICOS)]
    return bloco[:a0] + sep.join(novos) + bloco[a1:]


def ordenar_menu_servicos(text):
    """Menu suspenso Serviços: todos os serviços, na ordem de ORDEM_SERVICOS."""
    w = text.find(MENU_SERVICOS_WIDGET)
    if w < 0:
        return text, False
    start = text.rfind("<div", 0, w)
    end = balanced_end(text, start, "div")
    bloco = text[start:end]
    novo = ordenar_artigos(bloco, card_menu_novo)
    return text[:start] + novo + text[end:], novo != bloco


# ───────────────────────── CSS (bloco gerenciado no ajustes-responsivos.css) ─────────────────────────
CSS_ARQUIVO = ROOT / "wp-content" / "indafire" / "ajustes-responsivos.css"
CSS_INICIO = "/* INDAFIRE 17/11/2026 — início (gerado por scripts/apply_client_adjustments_2026_11_17.py) */"
CSS_FIM = "/* INDAFIRE 17/11/2026 — fim */"
CSS = """
/* categoria = página estática: a foto na tela inteira, o nome no meio, consulte-nos e o WhatsApp */
.tax-product_cat #bannerProdutoINDA,
.tax-product_cat #bannerProdutoINDA > .elementor-container {
  min-height: 100vh !important;
  min-height: 100svh !important;
}
.tax-product_cat #bannerProdutoINDA {
  background-position: var(--if-foco, 50%) center !important;
}
@media (max-width: 767px) and (orientation: portrait) {
  .tax-product_cat #bannerProdutoINDA {
    background-position: var(--if-foco-m, var(--if-foco, 50%)) center !important;
  }
}
.tax-product_cat #bannerProdutoINDA > .elementor-container {
  padding-top: 72px;
  padding-bottom: 40px;
  box-sizing: border-box;
}
.tax-product_cat #tituloCategoriaProdutos .elementor-heading-title {
  color: #fff !important;
  font-size: clamp(30px, 10vw, 104px) !important;
  overflow-wrap: break-word;
  line-height: 1.02 !important;
  text-shadow: 0 4px 30px rgba(0, 0, 0, 0.5);
}
/* sinal discreto no banner: "Conheça a linha" leva às especialidades */
.if-hero-cue-wrap {
  display: flex;
  justify-content: center;
  width: 100%;
}
.if-hero-cue {
  display: inline-flex;
  flex-direction: column;
  align-items: center;
  gap: 12px;
  margin-top: 30px;
  color: #fff !important;
  font-family: "Open Sans", Arial, sans-serif;
  font-size: 13px;
  font-weight: 700;
  letter-spacing: 0.24em;
  text-decoration: none !important;
  text-shadow: 0 2px 12px rgba(0, 0, 0, 0.55);
  text-transform: uppercase;
  animation: if-hero-entrada 0.9s 0.5s cubic-bezier(0.2, 0.8, 0.2, 1) both;
}
.if-hero-cue i {
  display: block;
  width: 2px;
  height: 46px;
  background: linear-gradient(#fff, rgba(255, 255, 255, 0));
  transform-origin: top;
  animation: if-cue 2s cubic-bezier(0.65, 0, 0.35, 1) infinite;
}
.if-hero-cue:hover,
.if-hero-cue:focus-visible {
  color: #fff !important;
  opacity: 0.85;
}
@keyframes if-cue {
  0% { transform: scaleY(0); transform-origin: top; }
  45% { transform: scaleY(1); transform-origin: top; }
  55% { transform: scaleY(1); transform-origin: bottom; }
  100% { transform: scaleY(0); transform-origin: bottom; }
}

/* /produtos/: a base do banner se dissolve em branco, logo abaixo do botão; o mosaico começa no
   mesmo branco. As duas fotos nunca se encontram, então não existe emenda. */
#bannerProdutoINDA:has(+ .if-secoes) > .elementor-container {
  position: relative;
  z-index: 2;
}
#bannerProdutoINDA:has(+ .if-secoes)::after {
  position: absolute;
  right: 0;
  bottom: -1px;
  left: 0;
  z-index: 1;
  height: 30%;
  content: "";
  pointer-events: none;
  background: linear-gradient(180deg, rgba(255, 255, 255, 0) 0%, rgba(255, 255, 255, 0.16) 28%, rgba(255, 255, 255, 0.5) 55%, rgba(255, 255, 255, 0.86) 80%, #fff 100%);
}
@media (max-width: 767px) {
  #bannerProdutoINDA:has(+ .if-secoes) {
    padding-bottom: 104px !important; /* espaço para a transição sem encostar no botão */
  }
  #bannerProdutoINDA:has(+ .if-secoes)::after {
    height: 120px;
  }
}

/* /produtos/: mosaico editorial — cada seção leva à página da linha.
   Fundo: a foto da sala da Inda Fire, clareada, que surge do branco e volta ao branco. */
.if-secoes {
  position: relative;
  padding: clamp(64px, 8vw, 128px) clamp(16px, 4vw, 48px);
  overflow: hidden;
  isolation: isolate;
  background: #fff;
  color: #151517;
}
.if-secoes::before {
  position: absolute;
  top: 0;
  right: 0;
  left: 0;
  z-index: -1;
  height: clamp(620px, 66vw, 880px);
  content: "";
  background:
    linear-gradient(rgba(255, 255, 255, 0.7), rgba(255, 255, 255, 0.7)),
    url("../uploads/2021/11/produtos.jpg") center 40% / cover no-repeat;
  filter: blur(2px) saturate(0.9);
  -webkit-mask-image: linear-gradient(180deg, transparent 0%, #000 26%, #000 50%, transparent 100%);
  mask-image: linear-gradient(180deg, transparent 0%, #000 26%, #000 50%, transparent 100%);
}
.if-secoes__topo {
  display: grid;
  gap: 12px;
  max-width: 1280px;
  margin: 0 auto clamp(32px, 4vw, 60px);
}
.if-secoes__kicker,
.if-linha__kicker {
  display: flex;
  align-items: center;
  gap: 14px;
  margin: 0 !important;
  color: #e30613;
  font-family: "Open Sans", Arial, sans-serif;
  font-size: 13px;
  font-weight: 700;
  letter-spacing: 0.24em;
  text-transform: uppercase;
}
.if-secoes__kicker::before,
.if-linha__kicker::before {
  width: 38px;
  height: 2px;
  content: "";
  background: #e30613;
}
.if-secoes__topo h2 {
  margin: 0 !important;
  color: #151517 !important;
  font-family: "Open Sans", Arial, sans-serif;
  font-size: clamp(36px, 5.4vw, 72px) !important;
  font-weight: 800 !important;
  letter-spacing: -0.025em;
  line-height: 1 !important;
}
.if-secoes__topo p {
  margin: 0 !important;
  color: #3f3f45;
  font-size: clamp(16px, 1.5vw, 19px);
}
.if-secoes__grade {
  display: grid;
  grid-template-columns: repeat(4, minmax(0, 1fr));
  grid-auto-rows: clamp(200px, 17vw, 250px);
  gap: clamp(10px, 1.2vw, 16px);
  max-width: 1280px;
  margin: 0 auto !important;
  padding: 0 !important;
  list-style: none !important;
}
.if-secao {
  position: relative;
  margin: 0 !important;
  overflow: hidden;
  border-radius: 6px;
  background: #1a1a1d;
  box-shadow: 0 18px 40px rgba(20, 20, 24, 0.16);
}
.if-secao--grande {
  grid-column: span 2;
  grid-row: span 2;
}
.if-secao--larga {
  grid-column: span 2;
}
.if-secao__link {
  position: absolute;
  inset: 0;
  display: flex;
  align-items: flex-end;
  padding: clamp(18px, 2vw, 30px);
  isolation: isolate;
  color: #fff !important;
  text-decoration: none !important;
}
.if-secao__foto {
  position: absolute;
  inset: 0;
  z-index: -2;
  width: 100% !important;
  height: 100% !important;
  max-width: none !important;
  object-fit: cover;
  filter: saturate(0.85) brightness(0.92);
  transform: scale(1.02);
  transition: transform 1.4s cubic-bezier(0.16, 1, 0.3, 1), scale 1.4s cubic-bezier(0.16, 1, 0.3, 1), filter 0.6s ease;
}
.if-secao__link::before {
  position: absolute;
  inset: 0;
  z-index: -1;
  content: "";
  background: linear-gradient(180deg, rgba(10, 10, 12, 0) 25%, rgba(10, 10, 12, 0.55) 62%, rgba(10, 10, 12, 0.92));
}
.if-secao__link::after {
  position: absolute;
  left: 0;
  bottom: 0;
  width: 100%;
  height: 3px;
  content: "";
  background: #e30613;
  transform: scaleX(0);
  transform-origin: left;
  transition: transform 0.7s cubic-bezier(0.16, 1, 0.3, 1);
}
.if-secao__num {
  position: absolute;
  top: clamp(16px, 1.8vw, 26px);
  left: clamp(18px, 2vw, 30px);
  color: rgba(255, 255, 255, 0.75);
  font-size: 13px;
  font-weight: 700;
  letter-spacing: 0.2em;
}
.if-secao__texto {
  display: grid;
  gap: 6px;
}
.if-secao__titulo {
  margin: 0 !important;
  color: #fff !important;
  font-family: "Open Sans", Arial, sans-serif;
  font-size: clamp(20px, 1.9vw, 28px) !important;
  font-weight: 800 !important;
  letter-spacing: -0.01em;
  line-height: 1.05 !important;
  text-transform: uppercase;
}
.if-secao--grande .if-secao__titulo {
  font-size: clamp(30px, 3.6vw, 54px) !important;
}
.if-secao__desc {
  max-width: 34ch;
  color: rgba(255, 255, 255, 0.8);
  font-size: 14px;
  line-height: 1.4;
}
.if-secao__chamada {
  display: inline-flex;
  align-items: center;
  gap: 12px;
  margin-top: 8px;
  color: #fff;
  font-size: 13px;
  font-weight: 700;
  letter-spacing: 0.18em;
  text-transform: uppercase;
}
.if-secao__chamada i {
  position: relative;
  display: block;
  width: 24px;
  height: 2px;
  background: #e30613;
  transition: width 0.6s cubic-bezier(0.16, 1, 0.3, 1);
}
.if-secao__chamada i::after {
  position: absolute;
  top: -4px;
  right: 0;
  width: 8px;
  height: 8px;
  content: "";
  border-top: 2px solid #e30613;
  border-right: 2px solid #e30613;
  transform: rotate(45deg);
}
.if-secao__link:hover .if-secao__foto,
.if-secao__link:focus-visible .if-secao__foto {
  filter: saturate(1.05) brightness(1);
  transform: scale(1.09);
}
.if-secao__link:hover::after,
.if-secao__link:focus-visible::after {
  transform: scaleX(1);
}
.if-secao__link:hover .if-secao__chamada i,
.if-secao__link:focus-visible .if-secao__chamada i {
  width: 48px;
}
.if-secao__link:focus-visible {
  outline: 3px solid #fff;
  outline-offset: -3px;
}
/* entrada: a seção abre como cortina, de baixo para cima, e a foto assenta */
html.if-movimento .if-secao[data-if-revelar] {
  clip-path: inset(100% 0 0 0);
  transition: clip-path 1.1s cubic-bezier(0.16, 1, 0.3, 1);
  transition-delay: calc(var(--i, 0) * 90ms);
}
html.if-movimento .if-secao[data-if-revelar] .if-secao__foto {
  scale: 1.22;
}
html.if-movimento .if-secao[data-if-revelar].is-visivel {
  clip-path: inset(0 0 0 0);
}
html.if-movimento .if-secao[data-if-revelar].is-visivel .if-secao__foto {
  scale: 1;
}
@media (max-width: 1024px) {
  .if-secoes__grade {
    grid-template-columns: repeat(2, minmax(0, 1fr));
    grid-auto-rows: 230px;
  }
  .if-secao--grande {
    grid-row: span 1;
  }
}
@media (max-width: 600px) {
  .if-secoes__grade {
    grid-template-columns: 1fr;
    grid-auto-rows: 210px;
  }
  .if-secao--grande,
  .if-secao--larga {
    grid-column: span 1;
  }
}

/* página da linha: o que a Inda Fire oferece + um único convite para o WhatsApp */
.if-linha {
  padding: clamp(64px, 9vw, 140px) clamp(16px, 4vw, 48px);
  scroll-margin-top: 60px;
  background: #fff;
}
.if-linha__grade {
  display: grid;
  grid-template-columns: minmax(0, 1.05fr) minmax(0, 0.95fr);
  align-items: center;
  gap: clamp(40px, 6vw, 100px);
  max-width: 1240px;
  margin: 0 auto;
}
.if-linha__kicker {
  margin-bottom: 16px !important;
}
.if-linha__titulo {
  margin: 0 0 18px !important;
  color: #151517 !important;
  font-family: "Open Sans", Arial, sans-serif;
  font-size: clamp(32px, 4.2vw, 56px) !important;
  font-weight: 800 !important;
  letter-spacing: -0.025em;
  line-height: 1.02 !important;
}
.if-linha__intro {
  max-width: 52ch;
  margin: 0 0 30px !important;
  color: #4a4a50;
  font-size: clamp(17px, 1.45vw, 19px);
  line-height: 1.6;
}
.if-linha__itens {
  margin: 0 0 32px !important;
  padding: 0 !important;
  border-top: 1px solid #e4e4e7;
  list-style: none !important;
}
.if-linha__itens li {
  display: grid;
  grid-template-columns: 52px 1fr;
  align-items: baseline;
  margin: 0 !important;
  padding: 17px 0;
  border-bottom: 1px solid #e4e4e7;
  color: #1c1c1f;
  font-size: clamp(17px, 1.45vw, 20px);
  font-weight: 600;
  line-height: 1.35;
}
.if-linha__itens li span {
  color: #e30613;
  font-size: 13px;
  font-weight: 700;
  letter-spacing: 0.14em;
}
.if-linha__itens li b {
  display: block;
  font-weight: 600;
}
.if-linha__itens li small {
  display: block;
  margin-top: 4px;
  color: #6a6a72;
  font-size: clamp(14px, 1.15vw, 16px);
  font-weight: 400;
  line-height: 1.45;
}
.if-linha__servicos p {
  margin: 0 0 12px !important;
  color: #6a6a72;
  font-size: 13px;
  font-weight: 700;
  letter-spacing: 0.16em;
  text-transform: uppercase;
}
.if-linha__servicos ul {
  display: flex;
  flex-wrap: wrap;
  gap: 10px;
  margin: 0 !important;
  padding: 0 !important;
  list-style: none !important;
}
.if-linha__servicos li {
  margin: 0 !important;
}
.if-linha__servicos a {
  display: inline-flex;
  align-items: center;
  gap: 10px;
  min-height: 44px;
  padding: 10px 18px;
  border: 1px solid #d6d6db;
  border-radius: 999px;
  color: #1c1c1f !important;
  font-size: 15px;
  font-weight: 600;
  text-decoration: none !important;
  transition: border-color 0.3s, color 0.3s;
}
.if-linha__servicos a::after {
  content: "→";
  color: #e30613;
  transition: transform 0.3s;
}
.if-linha__servicos a:hover,
.if-linha__servicos a:focus-visible {
  border-color: #e30613;
  color: #e30613 !important;
}
.if-linha__servicos a:hover::after {
  transform: translateX(4px);
}
.if-linha__visual {
  position: relative;
  width: 100%;
  margin: 0 !important;
  aspect-ratio: 4 / 5;
}
.if-linha__visual::after {
  position: absolute;
  right: -16px;
  bottom: -16px;
  width: 44%;
  height: 44%;
  content: "";
  border-right: 3px solid #e30613;
  border-bottom: 3px solid #e30613;
  pointer-events: none;
}
.if-linha__fundo {
  position: absolute;
  inset: 0;
  width: 100% !important;
  height: 100% !important;
  max-width: none !important;
  border-radius: 6px;
  object-fit: cover;
  filter: brightness(0.5) saturate(0.85);
}
.if-linha__produto {
  position: absolute;
  bottom: 7%;
  left: 50%;
  width: auto !important;
  max-width: 76% !important;
  height: auto !important;
  max-height: 80%;
  filter: drop-shadow(0 32px 40px rgba(0, 0, 0, 0.55));
  transform: translateX(-50%);
}
.if-linha__produto--pequeno {
  max-height: 46%;
}
/* vitrine: o produto real sobre um fundo de estúdio escuro, com o brilho vermelho da marca no chão */
.if-linha__visual--estudio {
  border-radius: 6px;
  background: radial-gradient(120% 90% at 50% 32%, #3c3c43 0%, #1c1c20 55%, #0e0e10 100%);
}
.if-linha__visual--estudio::before {
  position: absolute;
  right: 14%;
  bottom: 5%;
  left: 14%;
  height: 12%;
  content: "";
  border-radius: 50%;
  background: radial-gradient(closest-side, rgba(227, 6, 19, 0.5), transparent);
  filter: blur(10px);
}
html.if-movimento .if-linha__visual--estudio[data-if-revelar] {
  clip-path: inset(0 0 100% 0);
  transition: clip-path 1.2s cubic-bezier(0.16, 1, 0.3, 1);
}
html.if-movimento .if-linha__visual--estudio[data-if-revelar].is-visivel {
  clip-path: inset(0 -24px -24px 0);
}
html.if-movimento .if-linha__texto[data-if-revelar] > * {
  opacity: 0;
  translate: 0 26px;
  transition: opacity 0.8s ease, translate 1s cubic-bezier(0.16, 1, 0.3, 1);
}
html.if-movimento .if-linha__texto[data-if-revelar] > :nth-child(2) { transition-delay: 0.08s; }
html.if-movimento .if-linha__texto[data-if-revelar] > :nth-child(3) { transition-delay: 0.16s; }
html.if-movimento .if-linha__texto[data-if-revelar] > :nth-child(4) { transition-delay: 0.24s; }
html.if-movimento .if-linha__texto[data-if-revelar] > :nth-child(5) { transition-delay: 0.32s; }
html.if-movimento .if-linha__texto[data-if-revelar].is-visivel > * {
  opacity: 1;
  translate: 0 0;
}
html.if-movimento .if-linha__visual[data-if-revelar] .if-linha__fundo {
  clip-path: inset(0 0 100% 0);
  transition: clip-path 1.2s cubic-bezier(0.16, 1, 0.3, 1);
}
html.if-movimento .if-linha__visual[data-if-revelar] .if-linha__produto {
  opacity: 0;
  translate: 0 70px;
  transition: opacity 0.9s ease 0.35s, translate 1.2s cubic-bezier(0.16, 1, 0.3, 1) 0.35s;
}
html.if-movimento .if-linha__visual[data-if-revelar].is-visivel .if-linha__fundo {
  clip-path: inset(0 0 0 0);
}
html.if-movimento .if-linha__visual[data-if-revelar].is-visivel .if-linha__produto {
  opacity: 1;
  translate: 0 0;
}
.if-linha-cta {
  position: relative;
  padding: clamp(56px, 7vw, 104px) clamp(16px, 4vw, 48px);
  overflow: hidden;
  isolation: isolate;
  background: #0e0e10;
  color: #fff;
}
.if-linha-cta::before {
  position: absolute;
  inset: 0;
  z-index: -1;
  content: "";
  background: radial-gradient(50% 90% at 100% 100%, rgba(227, 6, 19, 0.3), transparent 70%);
}
.if-linha-cta__caixa {
  display: grid;
  grid-template-columns: minmax(0, 1fr) auto;
  align-items: center;
  gap: 24px 56px;
  max-width: 1240px;
  margin: 0 auto;
}
.if-linha-cta h2 {
  margin: 0 0 10px !important;
  color: #fff !important;
  font-family: "Open Sans", Arial, sans-serif;
  font-size: clamp(30px, 3.6vw, 48px) !important;
  font-weight: 800 !important;
  letter-spacing: -0.02em;
  line-height: 1.05 !important;
}
.if-linha-cta p {
  margin: 0 !important;
  color: rgba(255, 255, 255, 0.75);
  font-size: clamp(16px, 1.45vw, 19px);
}
.if-linha-cta__acoes {
  display: grid;
  justify-items: center;
  gap: 14px;
}
.if-linha-cta__whats {
  display: inline-flex;
  align-items: center;
  gap: 12px;
  min-height: 60px;
  padding: 14px 32px;
  border-radius: 999px;
  background: #128a45;
  box-shadow: 0 16px 36px rgba(18, 138, 69, 0.35);
  color: #fff !important;
  font-family: "Open Sans", Arial, sans-serif;
  font-size: 16px;
  font-weight: 700;
  letter-spacing: 0.04em;
  text-decoration: none !important;
  text-transform: uppercase;
  transition: transform 0.25s ease, background-color 0.25s ease;
}
.if-linha-cta__whats svg {
  flex: 0 0 auto;
  fill: #fff;
}
.if-linha-cta__whats:hover,
.if-linha-cta__whats:focus-visible {
  background: #0e7439;
  transform: translateY(-3px);
}
.if-linha-cta__tel {
  color: rgba(255, 255, 255, 0.78) !important;
  font-size: 15px;
  text-decoration: none !important;
}
.if-linha-cta__tel strong {
  color: #fff;
}
@media (max-width: 900px) {
  .if-linha__grade {
    grid-template-columns: 1fr;
  }
  .if-linha__visual {
    order: -1;
    max-width: 560px;
    margin: 0 auto !important;
    aspect-ratio: 4 / 3;
  }
  .if-linha__visual::after {
    right: -10px;
    bottom: -10px;
  }
  .if-linha-cta__caixa {
    grid-template-columns: 1fr;
    text-align: center;
  }
}
@media (prefers-reduced-motion: reduce) {
  .if-hero-cue,
  .if-hero-cue i {
    animation: none;
  }
  .if-secao__foto,
  .if-secao__link::after,
  .if-secao__chamada i {
    transition: none;
  }
}


/* menu "Produtos": só as categorias (saiu o carrossel de produtos específicos) */
.elementor-element.elementor-element-7ed0e60 {
  width: 100% !important;
}
/* menu "Produtos": nomes e ícones bem visíveis em todas as páginas (o estilo da antiga lista
   lateral do catálogo, que usa a mesma classe, deixava tudo cinza-escuro nas páginas de produto) */
.jet-sub-mega-menu .elementor-2456 .elementor-widget-image-box {
  border-bottom: 1px solid rgba(255, 255, 255, 0.14) !important;
  background: transparent !important;
  transition: background-color 0.25s ease;
}
.jet-sub-mega-menu .elementor-2456 .elementor-widget-image-box:hover {
  background: rgba(255, 255, 255, 0.07) !important;
}
.jet-sub-mega-menu .elementor-2456 .elementor-image-box-title,
.jet-sub-mega-menu .elementor-2456 .elementor-image-box-title a {
  color: #fff !important;
  font-size: 15px !important;
  font-weight: 600 !important;
  letter-spacing: 0.05em;
  opacity: 1 !important;
  text-transform: uppercase;
}
.jet-sub-mega-menu .elementor-2456 .elementor-widget-image-box:hover .elementor-image-box-title a {
  color: #ff4a52 !important;
}
.jet-sub-mega-menu .elementor-2456 .elementor-image-box-img img {
  width: 24px !important;
  height: 24px !important;
  object-fit: contain;
  filter: invert(1) !important;
  opacity: 1 !important;
}

/* /treinamentos/: ficou só o card da Brigada de Incêndio, centralizado */
.elementor-element-f2c61a3 > .elementor-container > .elementor-row,
.elementor-element-f2c61a3 > .elementor-container {
  justify-content: center;
}
""".strip("\n")


def atualizar_css(dry):
    atual = CSS_ARQUIVO.read_text(encoding="utf-8")
    bloco = CSS_INICIO + "\n" + CSS + "\n" + CSS_FIM + "\n"
    i, j = atual.find(CSS_INICIO), atual.find(CSS_FIM)
    if i >= 0 and j > i:
        novo = atual[:i] + bloco + atual[j + len(CSS_FIM):].lstrip("\n")
    else:
        novo = atual.rstrip("\n") + "\n\n" + bloco
    if novo != atual:
        log("css atualizado")
        if not dry:
            with CSS_ARQUIVO.open("w", encoding="utf-8", newline="\r\n") as fh:
                fh.write(novo)


# versão nos links dos arquivos da Inda Fire (o navegador não fica com o CSS velho em cache)
ASSET_VERSION = "16"
VERSAO_RE = re.compile(r"(wp-content/indafire/(?:ajustes-responsivos\.css|medicao\.js|aviso-whatsapp-produtos\.js|carrossel-relacionados\.js))\?v=\d+")


def versao_assets(text):
    new = VERSAO_RE.sub(r"\1?v=" + ASSET_VERSION, text)
    return new, new != text


# ───────────────────────── execução ─────────────────────────
def main(argv):
    dry = "--dry" in argv
    files = [f for f in subprocess.check_output(["git", "ls-files", "*.html"], cwd=ROOT, text=True).split("\n") if f]
    files += [f for f in REDIRECTS if f not in files]
    preparar_imagens(dry)
    atualizar_css(dry)

    titulos = {}
    for slug, _ in SECOES:
        titulos[slug] = titulo_da_categoria((ROOT / "categoria-produto" / slug / "index.html").read_text(encoding="utf-8"))
        if not titulos[slug]:
            sys.exit("sem título: %s" % slug)

    stats = {}

    def conta(nome, n):
        stats[nome] = stats.get(nome, 0) + int(n)

    for f in files:
        p = ROOT / f
        if not p.is_file():
            continue
        text = p.read_text(encoding="utf-8")
        orig = text
        if f in REDIRECTS:
            text = stub(f, REDIRECTS[f])
            conta("redirecionamento", text != orig)
        elif REDIRECT_PREFIX in text[:3000]:
            if "cursos-online/" in text:  # cursos/lorem-ipsum-*: iam para /cursos-online/, que saiu
                text = stub(f, "treinamentos/")
                conta("redirecionamento", text != orig)
        else:
            text, n = sem_resgate(text)
            conta("resgate", n)
            text, n = menu_so_categorias(text)
            conta("menu_produtos", n)
            text, ch = alarme_sem_sprinkler(text, f)
            conta("alarme", ch)
            text, ch = versao_assets(text)
            conta("versao_assets", ch)
            text, ch = ordenar_menu_servicos(text)
            conta("menu_servicos", ch)
            if f == "treinamentos/index.html":
                text, n = treinamentos(text)
                conta("treinamentos", n)
            if f == "index.html":
                text, ch = ordenar_carrossel_servicos(text)
                conta("carrossel_servicos", ch)
            if f == "produtos/index.html":
                text, ch = pagina_produtos(text, titulos)
                conta("produtos_secoes", ch)
            if f.startswith("categoria-produto/"):
                slug = f.split("/")[1]
                text, ch = pagina_categoria(text, slug, titulos[slug])
                conta("categoria", ch)
        if text != orig:
            conta("arquivos", 1)
            if not dry:
                with p.open("w", encoding="utf-8", newline="\r\n") as fh:  # working tree do projeto é CRLF
                    fh.write(text)
    log(stats)

    # conferência: nada pode continuar apontando para o que saiu
    sobras = []
    for f in files:
        p = ROOT / f
        if not p.is_file() or f in REDIRECTS:
            continue
        t = p.read_text(encoding="utf-8")
        if REDIRECT_PREFIX in t[:3000]:
            continue
        for rx in (RESGATE_LINK, TREINO_LINK, re.compile(r"shutterstock_1044591571")):
            if rx.search(t):
                sobras.append((f, rx.pattern[:40]))
    if sobras and not dry:
        for s in sobras[:20]:
            log("SOBRA", *s)
        sys.exit("%d página(s) ainda apontam para itens removidos" % len(sobras))


if __name__ == "__main__":
    main(sys.argv[1:])
