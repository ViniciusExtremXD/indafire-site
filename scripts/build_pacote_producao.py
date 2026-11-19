"""Gera o pacote para publicar a réplica no domínio oficial (indafire.com.br).

Parte SEMPRE do que está commitado (git archive do HEAD), então o pacote é exatamente o que foi aprovado.
Tira o que só serve para desenvolvimento (testes, scripts, docs, capturas de tela, arquivos do GitHub/Vercel)
e ajusta o que depende do endereço:
  - links do endereço de teste (github.io) passam para https://indafire.com.br;
  - canonical e og:url deixam de ser relativos (viram endereço completo);
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
    for m in tar.getmembers():
        if not m.isfile() or m.name.split("/")[0] in FORA:
            continue
        dados = tar.extractfile(m).read()
        if m.name.endswith(TEXTO):
            dados = dados.replace(TESTE.encode(), DOMINIO.encode())
        if m.name.endswith(".html"):
            stub = STUB in dados[:3000]
            if not stub:
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
    print("commit %s | %d arquivos | %d páginas no sitemap | %s (%.1f MB)"
          % (sha, arquivos, len(paginas), zip_path.name, zip_path.stat().st_size / 1e6))


if __name__ == "__main__":
    main()
