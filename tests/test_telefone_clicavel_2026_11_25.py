import importlib.util
import re
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("tel", ROOT / "scripts" / "apply_telefone_clicavel_2026_11_25.py")
tel = importlib.util.module_from_spec(spec)
spec.loader.exec_module(tel)

SEM_LINK_RODAPE = re.compile(
    r'<li class="elementor-icon-list-item">\s*<span class="elementor-icon-list-icon">\s*<i aria-hidden="true" class="fas fa-phone-alt">'
)


def paginas():
    saida = subprocess.check_output(["git", "ls-files", "-z", "*.html"], cwd=ROOT, text=True, encoding="utf-8")
    return [f for f in saida.split("\0") if f]


def ler(f):
    return (ROOT / f).read_text(encoding="utf-8")


def test_rodape_de_toda_pagina_tem_link_de_ligacao():
    com_rodape = [f for f in paginas() if '<span class="elementor-icon-list-text">(19) 3834-1741</span>' in ler(f)]
    assert len(com_rodape) == 78
    for f in com_rodape:
        texto = ler(f)
        assert not SEM_LINK_RODAPE.search(texto), f
        assert 'href="tel:+551938341741"' in texto, f


def test_contato_tem_icone_e_numero_com_link():
    texto = ler("contato/index.html")
    bloco = texto[texto.index('data-id="7e7939e"'):]
    bloco = bloco[: bloco.index("elementor-column ")]
    assert bloco.count('href="tel:+551938341741"') == 2
    assert "api.whatsapp.com" not in bloco


def test_nenhum_link_sem_codigo_do_pais():
    for f in paginas():
        assert 'href="tel:1938341741"' not in ler(f), f


def test_links_do_whatsapp_nao_mudaram():
    antes = subprocess.check_output(["git", "show", "b1de4ad65:contato/index.html"], cwd=ROOT).decode("utf-8")
    agora = ler("contato/index.html")
    assert agora.count("api.whatsapp.com") == antes.count("api.whatsapp.com")
    assert agora.count("mailto:") == antes.count("mailto:")


def test_rodar_de_novo_nao_muda_nada():
    for f in paginas():
        _, n = tel.aplicar(ler(f))
        assert n == 0, f
