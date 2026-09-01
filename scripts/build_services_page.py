"""Generate the static Services route from the existing Indafire shell."""

from __future__ import annotations

from dataclasses import dataclass
from html import escape
from pathlib import Path
import re
import sys


if __package__ in {None, ""}:
    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from scripts import sync_shared_location as shared_location


ROOT = Path(__file__).resolve().parents[1]
STYLE_ID = "indafire-services-style"
PAGE_ID = "indafire-services-page"
OUTPUT_PAGE = ROOT / "servicos" / "index.html"


@dataclass(frozen=True)
class Service:
    title: str
    image: str
    href: str


@dataclass(frozen=True)
class ServiceGroup:
    slug: str
    eyebrow: str
    title: str
    description: str
    feature_image: str
    services: tuple[Service, ...]


SERVICE_GROUPS = (
    ServiceGroup(
        "engenharia",
        "Projetos e regularização",
        "Engenharia e Consultoria",
        "Soluções técnicas para adequação, licenciamento e segurança contra incêndios.",
        "../wp-content/uploads/2021/12/Projeto-Simplificado.jpg",
        (
            Service(
                "AVCB/CLCB – Obtenção ou renovação",
                "../wp-content/uploads/elementor/thumbs/serv16-pf8x4kbkpnj15xn4m10x25iorm7qr32raj37hdfyjs.jpg",
                "https://indafire.com.br/servicos_inda_fire/obtencao-ou-renovacao-avcb-clcb/",
            ),
            Service(
                "Processo simplificado (PTS)",
                "../wp-content/uploads/elementor/thumbs/serv15-pf8wz5qzey4oenhr66x580m9suurhqmbjs1p53ggbs.jpg",
                "https://indafire.com.br/servicos_inda_fire/processo-simplificado-pts/",
            ),
            Service(
                "Projeto Técnico",
                "../wp-content/uploads/elementor/thumbs/serv14-pf8wm00bqg45v6lw0i56bc5yenprqadlqn8z9myvfs.jpg",
                "https://indafire.com.br/servicos_inda_fire/projeto-tecnico/",
            ),
        ),
    ),
    ServiceGroup(
        "manutencoes",
        "Confiabilidade operacional",
        "Manutenções e Inspeções",
        "Equipe especializada para manter equipamentos e instalações em conformidade e prontos para uso.",
        "../wp-content/uploads/2022/01/2.jpg",
        (
            Service(
                "Inspeção de Equipamentos",
                "../wp-content/uploads/elementor/thumbs/serv5-pf8yb4gi5lseubtm3fasyew11og19q18h6gnqec8tk.jpg",
                "https://indafire.com.br/servicos_inda_fire/inspecao-de-equipamentos/",
            ),
            Service(
                "Instalação e venda de extintores",
                "../wp-content/uploads/elementor/thumbs/serv2-pf8xwh51njqjx33kmld3llyfsin4bivtgoh9i623s8.jpg",
                "https://indafire.com.br/servicos_inda_fire/instalacao-e-venda-de-extintores/",
            ),
            Service(
                "Recarga de Extintores",
                "../wp-content/uploads/elementor/thumbs/serv3-pf8y1a3cl2bb9c4cko4gceb93eynntyfggilt2xnzc.jpg",
                "https://indafire.com.br/servicos_inda_fire/recarga-de-extintores/",
            ),
            Service(
                "Teste Hidrostático em Mangueiras de Incêndios",
                "../wp-content/uploads/elementor/thumbs/serv4-pf8y4inc4iqv8zf1o2i6xkwer7066at58hetbe4ujs.jpg",
                "https://indafire.com.br/servicos_inda_fire/teste-hidrostatico-em-mangueiras-de-incendios/",
            ),
        ),
    ),
    ServiceGroup(
        "sistemas",
        "Proteção integrada",
        "Sistemas de Prevenção e Combate a Incêndio",
        "Projeto, instalação e manutenção dos sistemas que protegem pessoas e patrimônios.",
        "../wp-content/uploads/2022/01/3.jpg",
        (
            Service(
                "Sinalização de Emergência",
                "../wp-content/uploads/2021/10/serv10.jpg",
                "https://indafire.com.br/servicos_inda_fire/sinalizacao-de-emergencia/",
            ),
            Service(
                "Sistema de alarme de incêndio",
                "../wp-content/uploads/2021/10/shutterstock_1044591571-scaled-1-1024x467.png",
                "https://indafire.com.br/servicos_inda_fire/sistema-de-alarme-de-incendio/",
            ),
            Service(
                "Sistema de detecção de fumaça e calor",
                "../wp-content/uploads/2021/10/serv9.jpg",
                "https://indafire.com.br/servicos_inda_fire/sistema-de-deteccao-de-fumaca-e-calor/",
            ),
            Service(
                "Sistema de Hidrantes",
                "../wp-content/uploads/2021/10/hidrantes.jpg",
                "https://indafire.com.br/servicos_inda_fire/sistema-de-hidrantes/",
            ),
            Service(
                "Sistema de iluminação de emergência",
                "../wp-content/uploads/2021/10/iluminacao.jpg",
                "https://indafire.com.br/servicos_inda_fire/sistema-de-iluminacao-de-emergencia/",
            ),
            Service(
                "Sistemas de Sprinklers",
                "../wp-content/uploads/2021/10/Sprinkler.jpg",
                "https://indafire.com.br/servicos_inda_fire/sistemas-de-sprinklers/",
            ),
        ),
    ),
    ServiceGroup(
        "treinamentos",
        "Preparo para agir",
        "Treinamentos",
        "Capacitação teórica e prática para resposta segura e eficiente em emergências.",
        "../wp-content/uploads/2022/01/4.jpg",
        (
            Service(
                "Brigada de Incêndio",
                "../wp-content/uploads/2022/01/4.jpg",
                "../treinamentos/",
            ),
        ),
    ),
    ServiceGroup(
        "especiais",
        "Atendimento sob medida",
        "Serviços Especiais",
        "Estrutura e suporte especializado para necessidades específicas de segurança e operação.",
        "../wp-content/uploads/2021/10/PRONTA-5.png",
        (
            Service(
                "Equipe habilitada para eventos ou trabalhos específicos",
                "../wp-content/uploads/2021/10/serv12.jpg",
                "https://indafire.com.br/servicos_inda_fire/disponibilizacao-de-equipe-habilitada-para-eventos-ou-trabalhos-especificos/",
            ),
            Service(
                "Fabricação de caixa d’água metálica",
                "../wp-content/uploads/2021/10/serv13.jpg",
                "https://indafire.com.br/servicos_inda_fire/fabricacao-de-caixa-dagua-metalica/",
            ),
            Service(
                "Locação de equipamentos",
                "../wp-content/uploads/2021/10/PRONTA-5.png",
                "https://indafire.com.br/servicos_inda_fire/locacao-de-equipamentos/",
            ),
        ),
    ),
)


CSS = r"""
#indafire-services-page {
  --inda-red: #e30613;
  --inda-ink: #202124;
  --inda-muted: #626a73;
  --inda-surface: #f4f4f4;
  --inda-shadow: 0 14px 34px rgba(24, 26, 29, .12);
  color: var(--inda-ink);
  overflow: clip;
  background: #fff;
}

#indafire-services-page *,
#indafire-services-page *::before,
#indafire-services-page *::after { box-sizing: border-box; }

#indafire-services-page .indafire-services-hero {
  position: relative;
  display: grid;
  min-height: clamp(330px, 44vw, 590px);
  place-items: center;
  padding: 100px 24px 64px;
  isolation: isolate;
  background: url("../wp-content/uploads/2021/11/servicos.jpg") center 48% / cover no-repeat;
}

#indafire-services-page .indafire-services-hero::before {
  position: absolute;
  inset: 0;
  z-index: -1;
  content: "";
  background: linear-gradient(90deg, rgba(12, 13, 15, .74), rgba(12, 13, 15, .38));
}

#indafire-services-page .indafire-services-hero h1 {
  margin: 0;
  color: #fff;
  font-size: clamp(42px, 7vw, 88px);
  font-weight: 800;
  letter-spacing: .035em;
  line-height: .96;
  text-align: center;
  text-shadow: 0 5px 24px rgba(0, 0, 0, .3);
}

#indafire-services-page .indafire-services-intro,
#indafire-services-page .indafire-services-group-inner,
#indafire-services-page .indafire-commercial-inner {
  width: min(1140px, calc(100% - 40px));
  margin-inline: auto;
}

#indafire-services-page .indafire-services-intro {
  display: grid;
  grid-template-columns: minmax(0, 1.1fr) minmax(320px, .9fr);
  align-items: stretch;
  margin-top: -58px;
  padding-bottom: 72px;
  position: relative;
  z-index: 2;
}

#indafire-services-page .indafire-services-intro-media {
  min-height: 390px;
  overflow: hidden;
  border-radius: 16px 0 0 16px;
  background: #ececec;
  box-shadow: var(--inda-shadow);
}

#indafire-services-page .indafire-services-intro-media img {
  display: block;
  width: 100%;
  height: 100%;
  object-fit: cover;
}

#indafire-services-page .indafire-services-intro-copy {
  display: flex;
  flex-direction: column;
  justify-content: center;
  padding: clamp(38px, 5vw, 68px);
  border-radius: 0 16px 16px 0;
  color: #fff;
  background: #2f3032;
  box-shadow: var(--inda-shadow);
}

#indafire-services-page .indafire-services-eyebrow,
#indafire-services-page .indafire-services-group-eyebrow,
#indafire-services-page .indafire-commercial-eyebrow {
  display: block;
  margin-bottom: 10px;
  color: var(--inda-red);
  font-size: 12px;
  font-weight: 800;
  letter-spacing: .16em;
  text-transform: uppercase;
}

#indafire-services-page .indafire-services-intro h2,
#indafire-services-page .indafire-services-group h2,
#indafire-services-page .indafire-commercial-copy h2 {
  margin: 0;
  font-weight: 800;
  letter-spacing: .015em;
  line-height: 1.08;
}

#indafire-services-page .indafire-services-intro h2 {
  color: #fff;
  font-size: clamp(30px, 4vw, 50px);
}

#indafire-services-page .indafire-services-intro p,
#indafire-services-page .indafire-services-group-heading p,
#indafire-services-page .indafire-commercial-copy p {
  margin: 18px 0 0;
  font-size: 16px;
  line-height: 1.65;
}

#indafire-services-page .indafire-services-intro p { color: #d6d8da; }

#indafire-services-page .indafire-services-group {
  padding: 76px 20px;
  background: #fff;
}

#indafire-services-page .indafire-services-group:nth-child(even) { background: var(--inda-surface); }

#indafire-services-page .indafire-services-group-heading {
  display: grid;
  grid-template-columns: minmax(0, 1fr) minmax(240px, 380px);
  gap: 44px;
  align-items: end;
  margin-bottom: 34px;
}

#indafire-services-page .indafire-services-group-heading h2 {
  max-width: 800px;
  color: #333;
  font-size: clamp(28px, 4vw, 46px);
}

#indafire-services-page .indafire-services-group-heading p {
  color: var(--inda-muted);
}

#indafire-services-page .indafire-service-grid {
  display: grid;
  grid-template-columns: repeat(3, minmax(0, 1fr));
  gap: 24px;
}

#indafire-services-page .indafire-service-card {
  min-width: 0;
  overflow: hidden;
  border: 1px solid #e5e6e8;
  border-radius: 14px;
  background: #fff;
  box-shadow: 0 8px 22px rgba(24, 26, 29, .08);
  transition: transform 180ms ease, box-shadow 180ms ease, border-color 180ms ease;
}

#indafire-services-page .indafire-service-card:hover,
#indafire-services-page .indafire-service-card:focus-within {
  transform: translateY(-4px);
  border-color: rgba(227, 6, 19, .32);
  box-shadow: 0 15px 34px rgba(24, 26, 29, .14);
}

#indafire-services-page .indafire-service-card-image {
  display: block;
  aspect-ratio: 16 / 10;
  overflow: hidden;
  background: #eceeef;
}

#indafire-services-page .indafire-service-card-image img {
  display: block;
  width: 100%;
  height: 100%;
  object-fit: cover;
  transition: transform 320ms ease;
}

#indafire-services-page .indafire-service-card:hover img { transform: scale(1.025); }

#indafire-services-page .indafire-service-card-body {
  display: flex;
  min-height: 150px;
  flex-direction: column;
  align-items: flex-start;
  padding: 22px;
}

#indafire-services-page .indafire-service-card h3 {
  margin: 0 0 22px;
  color: #303236;
  font-size: clamp(18px, 2vw, 23px);
  font-weight: 800;
  line-height: 1.22;
}

#indafire-services-page .indafire-service-card-link {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  margin-top: auto;
  color: var(--inda-red) !important;
  font-size: 12px;
  font-weight: 800;
  letter-spacing: .08em;
  text-decoration: none !important;
  text-transform: uppercase;
}

#indafire-services-page .indafire-commercial-section {
  padding: 76px 20px;
  color: #fff;
  background: #202124;
}

#indafire-services-page .indafire-commercial-inner {
  display: grid;
  grid-template-columns: minmax(260px, .75fr) minmax(0, 1.25fr);
  gap: 48px;
  align-items: center;
}

#indafire-services-page .indafire-commercial-copy h2 {
  color: #fff;
  font-size: clamp(28px, 3.6vw, 44px);
}

#indafire-services-page .indafire-commercial-copy p { color: #c9cbd0; }

#indafire-services-page #indafire-commercial-form {
  display: grid;
  grid-template-columns: repeat(2, minmax(0, 1fr));
  gap: 18px;
  padding: 28px;
  border: 1px solid rgba(255, 255, 255, .12);
  border-radius: 14px;
  background: #2f3032;
  box-shadow: 0 16px 36px rgba(0, 0, 0, .22);
}

#indafire-services-page .indafire-commercial-field { min-width: 0; }
#indafire-services-page .indafire-commercial-field--wide { grid-column: 1 / -1; }

#indafire-services-page .indafire-commercial-field label {
  display: block;
  margin-bottom: 7px;
  color: #fff;
  font-size: 12px;
  font-weight: 700;
}

#indafire-services-page .indafire-commercial-field input,
#indafire-services-page .indafire-commercial-field select,
#indafire-services-page .indafire-commercial-field textarea {
  width: 100%;
  min-height: 48px;
  padding: 12px 14px;
  border: 1px solid #595b60;
  border-radius: 8px;
  color: #202124;
  background: #fff;
}

#indafire-services-page .indafire-commercial-field textarea {
  min-height: 116px;
  resize: vertical;
}

#indafire-services-page #indafire-commercial-form button {
  grid-column: 1 / -1;
  justify-self: start;
  min-height: 46px;
  padding: 12px 24px;
  border: 0;
  border-radius: 24px;
  color: #fff;
  background: var(--inda-red);
  font-weight: 800;
  cursor: pointer;
}

@media (min-width: 1025px) {
  #indafire-services-page .indafire-service-grid { grid-template-columns: repeat(3, minmax(0, 1fr)); }
}

@media (min-width: 768px) and (max-width: 1024px) {
  #indafire-services-page .indafire-services-intro { grid-template-columns: 1fr 1fr; }
  #indafire-services-page .indafire-service-grid { grid-template-columns: repeat(2, minmax(0, 1fr)); }
  #indafire-services-page .indafire-services-group-heading { grid-template-columns: 1fr; gap: 12px; }
}

@media (max-width: 767px) {
  #indafire-services-page .indafire-services-hero {
    min-height: 310px;
    padding-top: 86px;
    background-position: 58% center;
  }
  #indafire-services-page .indafire-services-intro {
    grid-template-columns: 1fr;
    width: min(100% - 28px, 620px);
    margin-top: -34px;
    padding-bottom: 48px;
  }
  #indafire-services-page .indafire-services-intro-media {
    min-height: 230px;
    border-radius: 14px 14px 0 0;
  }
  #indafire-services-page .indafire-services-intro-copy {
    padding: 30px 24px;
    border-radius: 0 0 14px 14px;
  }
  #indafire-services-page .indafire-services-group { padding: 52px 14px; }
  #indafire-services-page .indafire-services-group-inner { width: min(100%, 620px); }
  #indafire-services-page .indafire-services-group-heading { grid-template-columns: 1fr; gap: 10px; }
  #indafire-services-page .indafire-service-grid { grid-template-columns: 1fr; gap: 18px; }
  #indafire-services-page .indafire-service-card-body { min-height: 132px; padding: 20px; }
  #indafire-services-page .indafire-commercial-section { padding: 52px 14px; }
  #indafire-services-page .indafire-commercial-inner { grid-template-columns: 1fr; gap: 28px; width: min(100%, 620px); }
  #indafire-services-page #indafire-commercial-form { grid-template-columns: 1fr; padding: 22px 18px; }
  #indafire-services-page .indafire-commercial-field--wide,
  #indafire-services-page #indafire-commercial-form button { grid-column: auto; }
  #indafire-services-page #indafire-commercial-form button { width: 100%; justify-self: stretch; }
}

@media (orientation: landscape) and (max-height: 600px) and (min-width: 568px) {
  #indafire-services-page .indafire-services-hero { min-height: 300px; padding-block: 82px 38px; }
  #indafire-services-page .indafire-services-intro { width: min(100% - 32px, 1040px); margin-top: -34px; padding-bottom: 42px; }
  #indafire-services-page .indafire-services-intro-media { min-height: 260px; }
  #indafire-services-page .indafire-services-intro-copy { padding: 28px; }
  #indafire-services-page .indafire-services-group { padding: 46px 16px; }
  #indafire-services-page .indafire-services-group-inner { width: min(100% - 8px, 1040px); }
  #indafire-services-page .indafire-services-group-heading { grid-template-columns: minmax(0, 1fr) minmax(220px, 340px); gap: 28px; margin-bottom: 24px; }
  #indafire-services-page .indafire-service-grid { grid-template-columns: repeat(3, minmax(0, 1fr)); gap: 16px; }
  #indafire-services-page .indafire-service-card-body { min-height: 116px; padding: 16px; }
  #indafire-services-page .indafire-service-card h3 { margin-bottom: 14px; font-size: 17px; }
  #indafire-services-page .indafire-commercial-section { padding: 48px 16px; }
  #indafire-services-page .indafire-commercial-inner { grid-template-columns: minmax(220px, .7fr) minmax(0, 1.3fr); gap: 28px; }
  #indafire-services-page #indafire-commercial-form { padding: 20px; }
}

@media (prefers-reduced-motion: reduce) {
  #indafire-services-page .indafire-service-card,
  #indafire-services-page .indafire-service-card img { transition: none; }
}
""".strip()


COMMERCIAL_SCRIPT = r"""
<script id="indafire-services-commercial-whatsapp-script">
(() => {
  const form = document.getElementById('indafire-commercial-form');
  if (!form || form.dataset.ready === 'true') return;
  form.dataset.ready = 'true';
  form.addEventListener('submit', (event) => {
    event.preventDefault();
    const name = document.getElementById('indafire-commercial-name').value.trim();
    const message = document.getElementById('indafire-commercial-message').value.trim();
    const text = `Olá! Meu nome/empresa é ${name}. Tenho interesse em serviço. ${message}`;
    window.open(`https://wa.me/551938341741?text=${encodeURIComponent(text)}`, '_blank', 'noopener,noreferrer');
  });
})();
</script>
""".strip()


def _render_card(service: Service) -> str:
    title = escape(service.title)
    return f"""<article class="indafire-service-card">
  <a class="indafire-service-card-image" href="{escape(service.href, quote=True)}" aria-label="Conhecer {title}">
    <img src="{escape(service.image, quote=True)}" width="720" height="450" loading="lazy" decoding="async" alt="{title}">
  </a>
  <div class="indafire-service-card-body">
    <h3>{title}</h3>
    <a class="indafire-service-card-link" href="{escape(service.href, quote=True)}">Veja em detalhes <i class="fas fa-arrow-right" aria-hidden="true"></i></a>
  </div>
</article>"""


def _render_group(group: ServiceGroup) -> str:
    cards = "\n".join(_render_card(service) for service in group.services)
    return f"""<section class="indafire-services-group" id="servicos-{group.slug}" aria-labelledby="servicos-{group.slug}-title">
  <div class="indafire-services-group-inner">
    <header class="indafire-services-group-heading">
      <div>
        <span class="indafire-services-group-eyebrow">{escape(group.eyebrow)}</span>
        <h2 id="servicos-{group.slug}-title">{escape(group.title)}</h2>
      </div>
      <p>{escape(group.description)}</p>
    </header>
    <div class="indafire-service-grid">
{cards}
    </div>
  </div>
</section>"""


def render_services_main(location_section: str) -> str:
    """Render the complete managed Services main element."""
    groups = "\n".join(_render_group(group) for group in SERVICE_GROUPS)
    return f"""<main id="{PAGE_ID}">
<style id="{STYLE_ID}">
{CSS}
</style>
<section class="indafire-services-hero" aria-labelledby="indafire-services-title">
  <h1 id="indafire-services-title">SERVIÇOS</h1>
</section>
<section class="indafire-services-intro" aria-labelledby="indafire-services-intro-title">
  <div class="indafire-services-intro-media">
    <img src="../wp-content/uploads/2021/10/shutterstock_1044591571-scaled-1-1024x467.png" width="1024" height="467" decoding="async" alt="Equipe de engenharia analisando projeto de segurança contra incêndio">
  </div>
  <div class="indafire-services-intro-copy">
    <span class="indafire-services-eyebrow">Soluções completas</span>
    <h2 id="indafire-services-intro-title">ENGENHARIA E CONSULTORIA</h2>
    <p>Atuamos no mercado de equipamentos de combate a incêndios, realizando uma ampla gama de serviços para proteger pessoas e patrimônios.</p>
  </div>
</section>
<div class="indafire-services-groups">
{groups}
</div>
<section class="indafire-commercial-section" id="indafire-commercial-whatsapp" data-context="services" aria-labelledby="indafire-commercial-title">
  <div class="indafire-commercial-inner">
    <div class="indafire-commercial-copy">
      <span class="indafire-commercial-eyebrow">Atendimento comercial</span>
      <h2 id="indafire-commercial-title">Ficou com dúvida sobre algum serviço?</h2>
      <p>Envie uma mensagem para nossa equipe. Ajudamos você a encontrar a solução adequada para sua necessidade.</p>
    </div>
    <form id="indafire-commercial-form">
      <div class="indafire-commercial-field">
        <label for="indafire-commercial-name">Nome ou empresa *</label>
        <input id="indafire-commercial-name" name="name" type="text" autocomplete="organization" required placeholder="Como podemos chamar você?">
      </div>
      <div class="indafire-commercial-field">
        <label for="indafire-commercial-interest">Assunto *</label>
        <select id="indafire-commercial-interest" name="interest" required>
          <option value="Serviço" selected>Serviço</option>
        </select>
      </div>
      <div class="indafire-commercial-field indafire-commercial-field--wide">
        <label for="indafire-commercial-message">Mensagem *</label>
        <textarea id="indafire-commercial-message" name="message" required placeholder="Conte brevemente o que você precisa"></textarea>
      </div>
      <button type="submit">Enviar mensagem pelo WhatsApp</button>
    </form>
  </div>
</section>
{location_section}
{COMMERCIAL_SCRIPT}
</main>"""


def _wp_page_bounds(source: str) -> tuple[int, int]:
    opening = re.search(
        r'<div\b(?=[^>]*\bdata-elementor-type=["\']wp-page["\'])[^>]*>',
        source,
        re.IGNORECASE | re.DOTALL,
    )
    if opening is None:
        raise ValueError("Missing Elementor wp-page shell")
    depth = 0
    for token in re.finditer(r"<div\b[^>]*>|</div\s*>", source[opening.start() :], re.I | re.S):
        if token.group(0).lower().startswith("</div"):
            depth -= 1
            if depth == 0:
                return opening.start(), opening.start() + token.end()
        else:
            depth += 1
    raise ValueError("Unclosed Elementor wp-page shell")


def build_page(shell: str, home: str) -> str:
    """Return the Services document while preserving the shared shell."""
    start, end = _wp_page_bounds(shell)
    rendered = shell[:start] + render_services_main(shared_location.extract_location(home)) + shell[end:]
    rendered = re.sub(
        r"<title>.*?</title>",
        "<title>Serviços - Inda Fire - Equipamentos de Combate a Incêndios</title>",
        rendered,
        count=1,
        flags=re.DOTALL,
    )
    rendered = re.sub(
        r'<link rel="canonical" href="[^"]*"\s*/?>',
        '<link rel="canonical" href="../servicos/" />',
        rendered,
        count=1,
    )
    rendered = re.sub(
        r'(<meta property="og:title" content=")[^"]*("\s*/?>)',
        r'\1Serviços - Inda Fire - Equipamentos de Combate a Incêndios\2',
        rendered,
        count=1,
    )
    rendered = re.sub(
        r'(<meta property="og:url" content=")[^"]*("\s*/?>)',
        r'\1https://indafire.com.br/servicos/\2',
        rendered,
        count=1,
    )
    rendered = rendered.replace(
        '<body class="',
        '<body class="indafire-services-static ',
        1,
    )
    rendered = rendered.replace(
        'referer_title" value="Sobre nós - Inda Fire - Equipamentos de Combate a Incêndios"',
        'referer_title" value="Serviços - Inda Fire - Equipamentos de Combate a Incêndios"',
    )
    shared_style = re.compile(
        rf'<style id="{re.escape(shared_location.STYLE_ID)}">.*?</style>\s*',
        re.DOTALL,
    )
    rendered = shared_style.sub("", rendered)
    rendered = rendered.replace(
        "</head>",
        f"{shared_location.style_tag(home)}\n</head>",
        1,
    )
    return rendered


def build_services_page(shell_page: Path, home_page: Path, output_page: Path) -> int:
    """Write the generated route and return one only when bytes changed."""
    from scripts import inject_internal_page_polish as internal
    from scripts import inject_responsive_navigation as navigation

    with shell_page.open("r", encoding="utf-8", newline="") as handle:
        shell = handle.read()
    with home_page.open("r", encoding="utf-8", newline="") as handle:
        home = handle.read()
    rendered = build_page(shell, home)
    rendered = internal.inject(rendered)
    rendered = navigation.normalize_logo_links(navigation.inject(rendered), "../")
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
    changed = build_services_page(
        ROOT / "sobre-nos" / "index.html",
        ROOT / "index.html",
        OUTPUT_PAGE,
    )
    print(f"Generated Services route: {changed} page(s) changed.")


if __name__ == "__main__":
    main()
