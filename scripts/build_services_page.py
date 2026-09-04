"""Generate a faithful static copy of the original Indafire Services page."""

from __future__ import annotations

from dataclasses import dataclass
from html import escape
from pathlib import Path
import re
import sys

if __package__ in {None, ""}:
    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

ROOT = Path(__file__).resolve().parents[1]
STYLE_ID = "indafire-services-style"
PAGE_ID = "indafire-services-page"
OUTPUT_PAGE = ROOT / "servicos" / "index.html"


@dataclass(frozen=True)
class Service:
    title: str
    href: str


@dataclass(frozen=True)
class ServiceGroup:
    slug: str
    title: str
    feature_image: str
    image_alt: str
    icon: str
    tone: str
    services: tuple[Service, ...]


SERVICE_GROUPS = (
    ServiceGroup(
        "engenharia", "Engenharia e Consultoria",
        "../wp-content/uploads/2021/12/Projeto-Simplificado.jpg",
        "Equipe de engenharia analisando um projeto de segurança contra incêndio",
        "../wp-content/uploads/2021/11/ico-1.svg", "engineering",
        (
            Service("AVCB/CLCB – Obtenção ou renovação", "https://indafire.com.br/servicos_inda_fire/obtencao-ou-renovacao-avcb-clcb/"),
            Service("Processo simplificado (PTS)", "https://indafire.com.br/servicos_inda_fire/processo-simplificado-pts/"),
        ),
    ),
    ServiceGroup(
        "manutencoes", "Manutenções e Inspeções",
        "../wp-content/uploads/2022/01/2.jpg",
        "Profissional realizando inspeção em um extintor",
        "../wp-content/uploads/2021/11/ico-2.svg", "muted",
        (
            Service("Inspeção de Equipamentos", "https://indafire.com.br/servicos_inda_fire/inspecao-de-equipamentos/"),
            Service("Instalação e venda de extintores", "https://indafire.com.br/servicos_inda_fire/instalacao-e-venda-de-extintores/"),
            Service("Recarga de Extintores", "https://indafire.com.br/servicos_inda_fire/recarga-de-extintores/"),
            Service("Teste Hidrostático em Mangueiras de Incêndios", "https://indafire.com.br/servicos_inda_fire/teste-hidrostatico-em-mangueiras-de-incendios/"),
        ),
    ),
    ServiceGroup(
        "sistemas", "Sistemas de Prevenção e Combate a Incêndio",
        "../wp-content/uploads/2022/01/3.jpg",
        "Sistema de sprinklers e sinalização de saída de emergência",
        "../wp-content/uploads/2021/11/ico-3.svg", "plain",
        (
            Service("Sinalização de Emergência", "https://indafire.com.br/servicos_inda_fire/sinalizacao-de-emergencia/"),
            Service("Sistema de alarme de incêndio", "https://indafire.com.br/servicos_inda_fire/sistema-de-alarme-de-incendio/"),
            Service("Sistema de detecção de fumaça e calor", "https://indafire.com.br/servicos_inda_fire/sistema-de-deteccao-de-fumaca-e-calor/"),
            Service("Sistema de Hidrantes", "https://indafire.com.br/servicos_inda_fire/sistema-de-hidrantes/"),
            Service("Sistema de iluminação de emergência", "https://indafire.com.br/servicos_inda_fire/sistema-de-iluminacao-de-emergencia/"),
            Service("Sistemas de Sprinklers", "https://indafire.com.br/servicos_inda_fire/sistemas-de-sprinklers/"),
        ),
    ),
    ServiceGroup(
        "treinamentos", "Treinamentos", "../wp-content/uploads/2022/01/4.jpg",
        "Treinamento de brigada de incêndio em campo",
        "../wp-content/uploads/2021/11/ico-4.svg", "muted",
        (Service("Brigada de Incêndio", "https://indafire.com.br/treinamentos/brigada-de-incendio/"),),
    ),
    ServiceGroup(
        "especiais", "Serviços Especiais",
        "../wp-content/uploads/2021/11/10639604_1538289183049362_3959369163680743290_n.jpg",
        "Fabricação e transporte de caixa d'água metálica",
        "../wp-content/uploads/2021/11/ico-4-1.svg", "plain",
        (
            Service("Equipe habilitada para eventos ou trabalhos específicos", "https://indafire.com.br/servicos_inda_fire/disponibilizacao-de-equipe-habilitada-para-eventos-ou-trabalhos-especificos/"),
            Service("Fabricação de caixa d’água metálica", "https://indafire.com.br/servicos_inda_fire/fabricacao-de-caixa-dagua-metalica/"),
            Service("Locação de equipamentos", "https://indafire.com.br/servicos_inda_fire/locacao-de-equipamentos/"),
        ),
    ),
)


CSS = r"""
#indafire-services-page{--inda-red:#e30613;color:#333;overflow:clip;background:#fff;font-family:"Open Sans",Arial,sans-serif}
#indafire-services-page *,#indafire-services-page *::before,#indafire-services-page *::after{box-sizing:border-box}
#indafire-services-page .indafire-services-hero{position:relative;display:grid;min-height:500px;place-items:center;isolation:isolate;background:url("../wp-content/uploads/2021/11/servicos.jpg") center 48%/cover no-repeat}
#indafire-services-page .indafire-services-hero::before{position:absolute;inset:0;z-index:-1;content:"";background:rgba(0,0,0,.62)}
#indafire-services-page .indafire-services-hero h1{margin:0;color:rgba(255,255,255,.33);font-size:clamp(72px,8.3vw,112px);font-weight:700;letter-spacing:-.025em;line-height:1;text-align:center}
#indafire-services-page .indafire-source-service-row{--row-height:450px;display:grid;grid-template-columns:repeat(2,minmax(0,1fr));min-height:var(--row-height);background:#fff}
#indafire-services-page .indafire-source-service-row--sistemas{--row-height:490px}
#indafire-services-page .indafire-source-service-row--especiais{--row-height:420px}
#indafire-services-page .indafire-source-service-visual,#indafire-services-page .indafire-source-service-content{min-width:0;min-height:var(--row-height)}
#indafire-services-page .indafire-source-service-visual{overflow:hidden}
#indafire-services-page .indafire-source-service-image{display:block;width:100%;height:100%;object-fit:cover}
#indafire-services-page .indafire-source-service-content{position:relative;display:flex;align-items:center;justify-content:center;padding:104px 32px 42px;background:#fff}
#indafire-services-page .indafire-source-service-row--muted .indafire-source-service-content{background:#f1f1f1}
#indafire-services-page .indafire-source-service-row--engineering .indafire-source-service-content{isolation:isolate;background:linear-gradient(180deg,#050505 0%,#3d414a 100%)}
#indafire-services-page .indafire-source-service-row--engineering .indafire-source-service-content::before{position:absolute;inset:0;z-index:-1;content:"";opacity:.1;background:url("../wp-content/uploads/2021/11/foguim.svg") center 56%/230px auto no-repeat}
#indafire-services-page .indafire-source-service-stack{position:relative;width:min(500px,100%)}
#indafire-services-page .indafire-source-service-icon-wrap{position:absolute;top:-104px;left:0;z-index:2;display:grid;width:76px;height:76px;place-items:center;background:#fff;box-shadow:0 0 10px rgba(0,0,0,.5)}
#indafire-services-page .indafire-source-service-icon{display:block;width:46px;height:46px;object-fit:contain}
#indafire-services-page .indafire-source-service-panel{min-height:162px;padding:30px 35px;border-radius:10px;color:#f3f3f3;background:#333;box-shadow:0 0 10px rgba(0,0,0,.5)}
#indafire-services-page .indafire-source-service-row--engineering .indafire-source-service-panel{min-height:230px;color:#737373;background:#fff}
#indafire-services-page .indafire-source-service-row--manutencoes .indafire-source-service-panel{min-height:254px}
#indafire-services-page .indafire-source-service-row--sistemas .indafire-source-service-panel{min-height:326px}
#indafire-services-page .indafire-source-service-row--especiais .indafire-source-service-panel{min-height:230px}
#indafire-services-page .indafire-source-service-panel h2{margin:0 0 18px;color:var(--inda-red);font-size:24px;font-weight:600;line-height:1;text-transform:uppercase}
#indafire-services-page .indafire-source-service-hint{margin:0 0 18px;color:inherit;font-family:"Open Sans Condensed","Open Sans",sans-serif;font-size:14px;font-style:italic;line-height:1.5}
#indafire-services-page .indafire-source-service-list{display:grid;gap:3px;margin:0;padding:0;list-style:none}
#indafire-services-page .indafire-source-service-link{display:grid;grid-template-columns:14px minmax(0,1fr);gap:8px;align-items:start;color:inherit!important;font-size:16px;line-height:1.45;text-decoration:none!important}
#indafire-services-page .indafire-source-service-link::before{content:"›";color:var(--inda-red);font-size:24px;font-weight:800;line-height:.9}
#indafire-services-page .indafire-source-service-link:hover,#indafire-services-page .indafire-source-service-link:focus-visible{color:var(--inda-red)!important}
@keyframes indafire-source-enter-left{from{opacity:0;transform:translateX(-24px)}to{opacity:1;transform:translateX(0)}}
@keyframes indafire-source-enter-right{from{opacity:0;transform:translateX(24px)}to{opacity:1;transform:translateX(0)}}
@media (min-width: 1025px){#indafire-services-page .indafire-source-service-row:nth-child(even) .indafire-source-service-panel{animation:indafire-source-enter-left 520ms ease both}#indafire-services-page .indafire-source-service-row:nth-child(odd) .indafire-source-service-panel{animation:indafire-source-enter-right 520ms ease both}}
@media (min-width:768px) and (max-width:1024px){#indafire-services-page .indafire-services-hero{min-height:430px}#indafire-services-page .indafire-services-hero h1{font-size:clamp(70px,10vw,96px)}#indafire-services-page .indafire-source-service-row{--row-height:420px}#indafire-services-page .indafire-source-service-row--sistemas{--row-height:470px}#indafire-services-page .indafire-source-service-stack{width:min(430px,100%)}#indafire-services-page .indafire-source-service-content{padding-inline:24px}#indafire-services-page .indafire-source-service-panel{padding-inline:28px}}
@media (max-width: 767px){
  #indafire-services-page .indafire-services-hero{min-height:448px;background-position:53% center}
  #indafire-services-page .indafire-services-hero h1{color:rgba(255,255,255,.4);font-size:clamp(42px,13vw,58px)}
  #indafire-services-page .indafire-source-service-row{--row-height:auto;grid-template-columns:1fr}
  #indafire-services-page .indafire-source-service-visual{min-height:240px}
  #indafire-services-page .indafire-source-service-content{min-height:430px;padding:132px 10px 32px}
  #indafire-services-page .indafire-source-service-row--manutencoes .indafire-source-service-content{min-height:437px}
  #indafire-services-page .indafire-source-service-row--sistemas .indafire-source-service-content{min-height:628px}
  #indafire-services-page .indafire-source-service-row--treinamentos .indafire-source-service-content{min-height:297px}
  #indafire-services-page .indafire-source-service-row--especiais .indafire-source-service-content{min-height:443px}
  #indafire-services-page .indafire-source-service-stack{width:min(341px,100%)}
  #indafire-services-page .indafire-source-service-icon-wrap{top:-104px;left:50%;transform:translateX(-50%)}
  #indafire-services-page .indafire-source-service-panel,#indafire-services-page .indafire-source-service-row--engineering .indafire-source-service-panel,#indafire-services-page .indafire-source-service-row--manutencoes .indafire-source-service-panel,#indafire-services-page .indafire-source-service-row--sistemas .indafire-source-service-panel,#indafire-services-page .indafire-source-service-row--especiais .indafire-source-service-panel{min-height:0;padding:32px 34px}
  #indafire-services-page .indafire-source-service-panel h2{margin-bottom:24px;font-size:21px;line-height:1.05}
  #indafire-services-page .indafire-source-service-hint{margin-bottom:22px}
  #indafire-services-page .indafire-source-service-link{font-size:15px}
}
@media (orientation: landscape) and (max-height:600px) and (min-width:568px){
  #indafire-services-page .indafire-services-hero{min-height:300px}#indafire-services-page .indafire-services-hero h1{font-size:68px}
  #indafire-services-page .indafire-source-service-row,#indafire-services-page .indafire-source-service-row--sistemas,#indafire-services-page .indafire-source-service-row--especiais{--row-height:340px}
  #indafire-services-page .indafire-source-service-content{padding:78px 22px 24px}#indafire-services-page .indafire-source-service-stack{width:min(390px,100%)}
  #indafire-services-page .indafire-source-service-icon-wrap{top:-66px;width:58px;height:58px}#indafire-services-page .indafire-source-service-icon{width:36px;height:36px}
  #indafire-services-page .indafire-source-service-panel,#indafire-services-page .indafire-source-service-row--engineering .indafire-source-service-panel,#indafire-services-page .indafire-source-service-row--manutencoes .indafire-source-service-panel,#indafire-services-page .indafire-source-service-row--sistemas .indafire-source-service-panel,#indafire-services-page .indafire-source-service-row--especiais .indafire-source-service-panel{min-height:0;padding:20px 24px}
  #indafire-services-page .indafire-source-service-panel h2{margin-bottom:12px;font-size:18px}#indafire-services-page .indafire-source-service-hint{margin-bottom:10px;font-size:12px}#indafire-services-page .indafire-source-service-list{gap:1px}#indafire-services-page .indafire-source-service-link{font-size:12px;line-height:1.3}
}
@media (prefers-reduced-motion:reduce){#indafire-services-page .indafire-source-service-panel{animation:none!important}}
""".strip()


def _render_service(service: Service) -> str:
    return ('<li><a class="indafire-source-service-link" '
            f'href="{escape(service.href, quote=True)}">{escape(service.title)}</a></li>')


def _render_group(group: ServiceGroup, index: int) -> str:
    links = "\n".join(_render_service(service) for service in group.services)
    loading = "eager" if index == 0 else "lazy"
    return f"""<section class="indafire-source-service-row indafire-source-service-row--{group.slug} indafire-source-service-row--{group.tone}" id="servicos-{group.slug}" aria-labelledby="servicos-{group.slug}-title">
  <div class="indafire-source-service-visual">
    <img class="indafire-source-service-image" src="{escape(group.feature_image, quote=True)}" width="960" height="640" loading="{loading}" decoding="async" alt="{escape(group.image_alt, quote=True)}">
  </div>
  <div class="indafire-source-service-content">
    <div class="indafire-source-service-stack">
      <div class="indafire-source-service-icon-wrap" aria-hidden="true"><img class="indafire-source-service-icon" src="{escape(group.icon, quote=True)}" width="72" height="72" alt=""></div>
      <article class="indafire-source-service-panel">
        <h2 id="servicos-{group.slug}-title">{escape(group.title)}</h2>
        <p class="indafire-source-service-hint">Clique nas opções abaixo</p>
        <ul class="indafire-source-service-list">{links}</ul>
      </article>
    </div>
  </div>
</section>"""


def render_services_main(_location_section: str = "") -> str:
    """Render only the content present on the original Services page."""
    rows = "\n".join(_render_group(group, index) for index, group in enumerate(SERVICE_GROUPS))
    return f"""<main id="{PAGE_ID}">
<style id="{STYLE_ID}">{CSS}</style>
<section class="indafire-services-hero" aria-labelledby="indafire-services-title"><h1 id="indafire-services-title">SERVIÇOS</h1></section>
<div class="indafire-source-services" aria-label="Categorias de serviços">{rows}</div>
</main>"""


def _wp_page_bounds(source: str) -> tuple[int, int]:
    opening = re.search(r'<div\b(?=[^>]*\bdata-elementor-type=["\']wp-page["\'])[^>]*>', source, re.I | re.S)
    if opening is None:
        raise ValueError("Missing Elementor wp-page shell")
    depth = 0
    for token in re.finditer(r"<div\b[^>]*>|</div\s*>", source[opening.start():], re.I | re.S):
        if token.group(0).lower().startswith("</div"):
            depth -= 1
            if depth == 0:
                return opening.start(), opening.start() + token.end()
        else:
            depth += 1
    raise ValueError("Unclosed Elementor wp-page shell")


def _remove_section_by_id(source: str, section_id: str) -> str:
    """Remove one complete section, including any nested sections."""
    opening = re.search(
        rf'<section\b(?=[^>]*\bid=["\']{re.escape(section_id)}["\'])[^>]*>',
        source,
        re.I | re.S,
    )
    if opening is None:
        return source

    depth = 0
    for token in re.finditer(r"<section\b[^>]*>|</section\s*>", source[opening.start():], re.I | re.S):
        if token.group(0).lower().startswith("</section"):
            depth -= 1
            if depth == 0:
                end = opening.start() + token.end()
                return source[:opening.start()] + source[end:]
        else:
            depth += 1
    raise ValueError(f"Unclosed section #{section_id}")


def build_page(shell: str, _home: str) -> str:
    """Return the Services document while preserving the approved shared shell."""
    start, end = _wp_page_bounds(shell)
    rendered = shell[:start] + render_services_main() + shell[end:]
    rendered = re.sub(r"<title>.*?</title>", "<title>Serviços - Inda Fire - Equipamentos de Combate a Incêndios</title>", rendered, count=1, flags=re.S)
    rendered = re.sub(r'<link rel="canonical" href="[^"]*"\s*/?>', '<link rel="canonical" href="../servicos/" />', rendered, count=1)
    rendered = re.sub(r'(<meta property="og:title" content=")[^"]*("\s*/?>)', r'\1Serviços - Inda Fire - Equipamentos de Combate a Incêndios\2', rendered, count=1)
    rendered = re.sub(r'(<meta property="og:url" content=")[^"]*("\s*/?>)', r'\1https://indafire.com.br/servicos/\2', rendered, count=1)
    rendered = rendered.replace('<body class="', '<body class="indafire-services-static ', 1)
    rendered = rendered.replace('referer_title" value="Sobre nós - Inda Fire - Equipamentos de Combate a Incêndios"', 'referer_title" value="Serviços - Inda Fire - Equipamentos de Combate a Incêndios"')
    rendered = _remove_section_by_id(rendered, "localizacao_mapa")
    return re.sub(r'<style id="indafire-shared-location-style">.*?</style>\s*', "", rendered, flags=re.S)


def build_services_page(shell_page: Path, home_page: Path, output_page: Path) -> int:
    """Write the generated route and return one only when bytes changed."""
    from scripts import inject_internal_page_polish as internal
    from scripts import inject_responsive_navigation as navigation

    with shell_page.open("r", encoding="utf-8", newline="") as handle:
        shell = handle.read()
    with home_page.open("r", encoding="utf-8", newline="") as handle:
        home = handle.read()
    rendered = navigation.normalize_logo_links(navigation.inject(internal.inject(build_page(shell, home))), "../")
    current = None
    if output_page.is_file():
        with output_page.open("r", encoding="utf-8", newline="") as handle:
            current = handle.read()
    if current == rendered:
        return 0
    output_page.parent.mkdir(parents=True, exist_ok=True)
    with output_page.open("w", encoding="utf-8", newline="") as handle:
        handle.write(rendered)
    return 1


def main() -> None:
    changed = build_services_page(ROOT / "sobre-nos" / "index.html", ROOT / "index.html", OUTPUT_PAGE)
    print(f"Generated Services route: {changed} page(s) changed.")


if __name__ == "__main__":
    main()
