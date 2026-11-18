"""Variante de /produtos/ só para a prévia da Vercel (ramo previa/produtos-estilo-servicos).

Troca o mosaico de /produtos/ pelo mesmo desenho da página Serviços: faixas que alternam foto e
conteúdo, com o ícone num quadrado branco, a caixa com o título em vermelho, "Clique nas opções
abaixo" e a lista de linhas, e a mesma animação de entrada (foto de um lado, conteúdo do outro).
Cada item da lista leva à página da linha (especialidades e, por último, o WhatsApp).

O GitHub Pages (ramo main) continua com o mosaico. Rodar depois de
apply_client_adjustments_2026_11_17.py. Idempotente.
"""
from __future__ import annotations

import re
import sys
from dataclasses import dataclass
from html import escape
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from scripts import build_services_page as servicos  # noqa: E402

PAGINA = ROOT / "produtos" / "index.html"
MOSAICO_RE = re.compile(r'\n?<section class="if-secoes".*?</section><!-- /if-secoes -->', re.S)
VARIANTE_RE = re.compile(r'\n?<!-- if-produtos-faixas -->.*?<!-- /if-produtos-faixas -->', re.S)


@dataclass(frozen=True)
class Grupo:
    slug: str          # id da faixa
    tamanho: str       # classe de altura emprestada da página Serviços
    tom: str           # engineering (escuro), muted (cinza) ou plain (branco), como em Serviços
    titulo: str
    foto: str          # banner da linha, em wp-content/indafire/img/categorias/
    foco: int          # ponto horizontal da foto (%)
    alt: str
    icone: str
    linhas: tuple[tuple[str, str], ...]  # (categoria, rótulo)


GRUPOS = (
    Grupo("extintores", "engenharia", "engineering", "Extintores e Abrigos", "extintores", 35,
          "Extintores de incêndio vermelhos lado a lado", "02-icone-extintores.svg",
          (("extintores", "Extintores"), ("abrigos", "Abrigos"), ("acessorios", "Acessórios"))),
    Grupo("hidrantes", "manutencoes", "muted", "Hidrantes e Mangueiras", "hidrantes", 50,
          "Registros de hidrante vermelhos", "05-icone-hidrantes.svg",
          (("hidrantes", "Hidrantes"), ("mangueiras", "Mangueiras"),
           ("sistema-de-bomba-de-incendio", "Sistema de bomba de incêndio"))),
    Grupo("sinalizacao", "manutencoes", "plain", "Sinalização, Alarme e Iluminação", "sinalizacoes", 30,
          "Placa de sinalização de extintor", "06-icone-sinalizacoes.svg",
          (("sinalizacoes", "Sinalizações"), ("alarmes-de-incendio", "Alarmes de incêndio"),
           ("iluminacoes-de-emergencia", "Iluminações de emergência"))),
    Grupo("protecao", "sistemas", "muted", "Proteção e Atendimento", "epi", 55,
          "Roupa e capacete de bombeiro", "10-icone-epi.svg",
          (("epi", "EPI – Equipamentos de proteção individual"),
           ("epr", "EPR – Equipamentos de proteção respiratória"),
           ("epc", "EPC – Equipamentos de proteção coletiva"),
           ("aph", "APH – Atendimento pré-hospitalar"))),
    Grupo("florestal", "especiais", "plain", "Incêndio Florestal", "incendio-florestal", 65,
          "Combate a incêndio em vegetação", "15-icone-incendio-florestal.svg",
          (("incendio-florestal", "Incêndio florestal"),)),
)

# Ajustes de encaixe: as fotos das linhas são panorâmicas (o recorte segue o ponto de cada linha) e
# a faixa de Proteção tem quatro itens, como a de Sistemas em Serviços.
CSS_EXTRA = (
    "#indafire-services-page.if-produtos-faixas .indafire-source-service-image{object-position:var(--foco,50%) center}"
    # ícones das linhas são traço preto; ficam no vermelho dos ícones de Serviços (#e30613)
    "#indafire-services-page.if-produtos-faixas .indafire-source-service-icon{filter:invert(11%) sepia(96%) saturate(6800%) hue-rotate(354deg) brightness(92%) contrast(110%)}"
)


def _faixa(g: Grupo, i: int) -> str:
    itens = "\n".join(
        f'<li style="--n:{n}"><a class="indafire-source-service-link" href="../categoria-produto/{slug}/">'
        f"{escape(rotulo)}</a></li>"
        for n, (slug, rotulo) in enumerate(g.linhas)
    )
    loading = "eager" if i == 0 else "lazy"
    return f"""<section class="indafire-source-service-row indafire-source-service-row--{g.tamanho} indafire-source-service-row--{g.tom}" id="produtos-{g.slug}" aria-labelledby="produtos-{g.slug}-title" data-if-revelar>
  <div class="indafire-source-service-visual">
    <img class="indafire-source-service-image" style="--foco:{g.foco}%" src="../wp-content/indafire/img/categorias/{g.foto}.jpg" width="960" height="640" loading="{loading}" decoding="async" alt="{escape(g.alt, quote=True)}">
  </div>
  <div class="indafire-source-service-content">
    <div class="indafire-source-service-stack">
      <div class="indafire-source-service-icon-wrap" aria-hidden="true"><img class="indafire-source-service-icon" src="../wp-content/uploads/2021/11/{g.icone}" width="72" height="72" alt=""></div>
      <article class="indafire-source-service-panel">
        <h2 id="produtos-{g.slug}-title">{escape(g.titulo)}</h2>
        <p class="indafire-source-service-hint">Clique nas opções abaixo</p>
        <ul class="indafire-source-service-list">{itens}</ul>
      </article>
    </div>
  </div>
</section>"""


def bloco() -> str:
    faixas = "\n".join(_faixa(g, i) for i, g in enumerate(GRUPOS))
    return (
        "\n<!-- if-produtos-faixas -->\n"
        '<div id="indafire-services-page" class="if-produtos-faixas">\n'
        f'<style id="indafire-services-style">{servicos.CSS}{CSS_EXTRA}</style>\n'
        f'<div class="indafire-source-services" aria-label="Linhas de produtos">{faixas}</div>\n'
        f'<script id="indafire-services-reveal">{servicos.REVEAL_JS}</script>\n'
        "</div>\n<!-- /if-produtos-faixas -->"
    )


def aplicar(texto: str) -> str:
    novo = bloco()
    if VARIANTE_RE.search(texto):
        return VARIANTE_RE.sub(lambda _m: novo, texto, count=1)
    if not MOSAICO_RE.search(texto):
        raise SystemExit("produtos/index.html: não achei o mosaico nem a variante")
    return MOSAICO_RE.sub(lambda _m: novo, texto, count=1)


def main() -> None:
    for g in GRUPOS:
        for caminho in (ROOT / "wp-content/indafire/img/categorias" / f"{g.foto}.jpg",
                        ROOT / "wp-content/uploads/2021/11" / g.icone):
            if not caminho.is_file():
                raise SystemExit("arquivo ausente: %s" % caminho)
        for slug, _ in g.linhas:
            if not (ROOT / "categoria-produto" / slug / "index.html").is_file():
                raise SystemExit("linha sem página: %s" % slug)
    texto = PAGINA.read_text(encoding="utf-8")
    novo = aplicar(texto)
    if novo != texto:
        with PAGINA.open("w", encoding="utf-8", newline="\r\n") as fh:
            fh.write(novo)
    print("produtos/index.html:", "atualizada" if novo != texto else "sem mudança")


if __name__ == "__main__":
    main()
