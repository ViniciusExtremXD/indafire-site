"""Gera o pacote para publicar a réplica no domínio oficial (indafire.com.br).

Parte SEMPRE do que está commitado (git archive do HEAD), então o pacote é exatamente o que foi aprovado.
Tira o que só serve para desenvolvimento (testes, scripts, docs, capturas de tela, arquivos do GitHub/Vercel)
e ajusta o que depende do endereço:
  - links do endereço de teste (github.io) passam para https://indafire.com.br;
  - canonical e og:url deixam de ser relativos (viram endereço completo);
  - tira a lupa de busca do cabeçalho e a janela de busca (dependem do WordPress, que sai do ar);
  - gera robots.txt e sitemap.xml.
NÃO leva .htaccess (a hospedagem já tem o seu); veja docs/operacional/runbook-publicacao-replica.md.

Uso: python scripts/build_pacote_producao.py   → deploy/indafire-producao-<sha>/ e .zip
"""
from __future__ import annotations

import datetime
import io
import re
import shutil
import subprocess
import sys
import tarfile
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DOMINIO = "https://indafire.com.br"
TESTE = "https://viniciusextremxd.github.io/indafire-site"
FORA = {"tests", "scripts", "docs", "screenshots", ".github", "README.md", "design-qa.md", "vercel.json",
        ".vercelignore", ".gitignore", ".nojekyll"}
# páginas que existem na réplica mas não são conteúdo para buscador
FORA_DO_SITEMAP = {"404.html", "carrinho", "finalizar-compra", "minha-conta", "area-do-cliente"}
TEXTO = (".html", ".js", ".css", ".json", ".xml", ".txt", ".svg")
CANONICAL = re.compile(rb'(<link rel="canonical" href=")[^"]*(")')
OG_URL = re.compile(rb'(<meta property="og:url" content=")[^"]*(")')
STUB = b"<!-- indafire: redirecionamento"
# a busca do cabeçalho (lupa + janela 2434) usa o WordPress para procurar; sem ele não funcionaria
BUSCA_ID = b"eyJpZCI6IjI0MzQi"  # base64 de {"id":"2434"...}, que está no link da lupa
TAG_DIV = re.compile(rb"<(/?)div\b[^>]*?(/?)>", re.I)


def fim_do_div(dados: bytes, inicio: int) -> int:
    nivel = 0
    for m in TAG_DIV.finditer(dados, inicio):
        if m.group(2):  # <div ... />
            continue
        nivel += -1 if m.group(1) else 1
        if nivel == 0:
            return m.end()
    raise ValueError("div sem fechamento")


def tirar_busca(dados: bytes) -> tuple[bytes, int]:
    removidos = 0
    # 1) o widget da lupa: o <div class="elementor-element ... elementor-widget-icon"> logo antes do link da janela 2434
    pos = 0
    while True:
        i = dados.find(BUSCA_ID, pos)
        if i < 0:
            break
        pos = i + 1
        ini = dados.rfind(b'<div class="elementor-element ', 0, i)
        tag_fim = dados.find(b">", ini)
        if ini < 0 or i - ini > 900 or b"elementor-widget-icon" not in dados[ini:tag_fim]:
            continue  # o mesmo texto aparece em outros lugares (ex.: configuração da janela): não é a lupa
        dados = dados[:ini] + dados[fim_do_div(dados, ini):]
        removidos += 1
        pos = ini
    # 2) a janela de busca em si
    j = dados.find(b'<div data-elementor-type="popup" data-elementor-id="2434"')
    if j >= 0:
        dados = dados[:j] + dados[fim_do_div(dados, j):]
        removidos += 1
    return dados, removidos


def git(*args: str) -> bytes:
    return subprocess.check_output(["git", *args], cwd=ROOT)


def url_da_pagina(rel: str) -> str:
    pasta = rel[: -len("index.html")] if rel.endswith("index.html") else rel
    # os duplicados antigos servicos/<serviço>/ apontam para a página oficial do serviço
    m = re.fullmatch(r"servicos/([^/]+)/", pasta)
    if m and (ROOT / "servicos_inda_fire" / m.group(1) / "index.html").is_file():
        pasta = "servicos_inda_fire/%s/" % m.group(1)
    return "%s/%s" % (DOMINIO, pasta)


def main() -> None:
    sujo = git("status", "--porcelain", "--untracked-files=no").decode().strip()
    if sujo:
        sys.exit("há mudanças não commitadas; commite antes de gerar o pacote:\n" + sujo)
    sha = git("rev-parse", "--short", "HEAD").decode().strip()
    saida = ROOT / "deploy" / ("indafire-producao-" + sha)
    if saida.exists():
        shutil.rmtree(saida)
    saida.mkdir(parents=True)

    tar = tarfile.open(fileobj=io.BytesIO(git("archive", "--format=tar", "HEAD")))
    paginas = []
    sem_busca = 0
    for m in tar.getmembers():
        if not m.isfile() or m.name.split("/")[0] in FORA:
            continue
        dados = tar.extractfile(m).read()
        if m.name.endswith(TEXTO):
            dados = dados.replace(TESTE.encode(), DOMINIO.encode())
        if m.name.endswith(".html"):
            stub = STUB in dados[:3000]
            if not stub:
                dados, n = tirar_busca(dados)
                sem_busca += bool(n)
                alvo = url_da_pagina(m.name).encode()
                dados = CANONICAL.sub(lambda x: x.group(1) + alvo + x.group(2), dados)
                dados = OG_URL.sub(lambda x: x.group(1) + alvo + x.group(2), dados)
                noindex = b"noindex" in dados[:6000].lower()
                topo = m.name.split("/")[0]
                if not noindex and m.name != "404.html" and topo not in FORA_DO_SITEMAP \
                        and url_da_pagina(m.name).split(DOMINIO)[1] == "/" + m.name[: -len("index.html")]:
                    paginas.append(m.name)
        destino = saida / m.name
        destino.parent.mkdir(parents=True, exist_ok=True)
        destino.write_bytes(dados)

    hoje = datetime.date.today().isoformat()
    urls = "".join(
        "  <url><loc>%s/%s</loc><lastmod>%s</lastmod></url>\n"
        % (DOMINIO, p[: -len("index.html")], hoje) for p in sorted(paginas)
    )
    (saida / "sitemap.xml").write_text(
        '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
        + urls + "</urlset>\n", encoding="utf-8")
    (saida / "robots.txt").write_text(
        "User-agent: *\nAllow: /\nDisallow: /carrinho/\nDisallow: /finalizar-compra/\nDisallow: /minha-conta/\n\n"
        "Sitemap: %s/sitemap.xml\n" % DOMINIO, encoding="utf-8")

    zip_path = saida.with_suffix(".zip")
    if zip_path.exists():
        zip_path.unlink()
    with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as z:
        for f in sorted(saida.rglob("*")):
            if f.is_file():
                z.write(f, f.relative_to(saida).as_posix())
    arquivos = sum(1 for f in saida.rglob("*") if f.is_file())
    print("commit %s | %d arquivos | %d páginas no sitemap | busca retirada de %d páginas | %s (%.1f MB)"
          % (sha, arquivos, len(paginas), sem_busca, zip_path.name, zip_path.stat().st_size / 1e6))


if __name__ == "__main__":
    main()
