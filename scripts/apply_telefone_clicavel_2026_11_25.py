"""Deixa o telefone clicável onde ele aparecia só como texto (25/11/2026).

O número (19) 3834-1741 era texto puro no rodapé de todas as páginas e no topo de /contato/: no celular a pessoa
tocava e nada acontecia, então o evento contato_telefone (medicao.js → GTM → GA4 → Google Ads) quase nunca saía.
  - rodapé: o item da lista passa a ter <a href="tel:...">, igual ao item de e-mail logo abaixo;
  - /contato/: o ícone e o número do telefone viram link, igual ao cartão do WhatsApp ao lado;
  - menu lateral: tel:1938341741 vira tel:+551938341741 (sem o +55 nem toda operadora completa a ligação).
Não mexe no texto, no visual, nem nos links do WhatsApp. Pode rodar mais de uma vez.

Uso: python scripts/apply_telefone_clicavel_2026_11_25.py [--dry] [pasta]
     (sem pasta: páginas versionadas deste repositório; com pasta: todos os .html dela, ex.: pacote de produção)
"""
from __future__ import annotations

import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TEL = "tel:+551938341741"
NUMERO = r"\(19\) 3834-1741"

RODAPE = re.compile(
    r'(<li class="elementor-icon-list-item">\s*)'
    r'(<span class="elementor-icon-list-icon">\s*<i aria-hidden="true" class="fas fa-phone-alt"></i>\s*</span>\s*'
    r'<span class="elementor-icon-list-text">' + NUMERO + r"</span>)"
    r"(\s*</li>)"
)
CONTATO = re.compile(
    r'<span class="elementor-icon elementor-animation-" >(\s*<svg\b(?:(?!</svg>).)*</svg>\s*)</span>'
    r'(\s*</div>\s*<div class="elementor-icon-box-content">\s*<h3 class="elementor-icon-box-title">\s*)'
    r"<span\s*>(\s*" + NUMERO + r"\s*)</span>",
    re.S,
)
MENU = 'href="tel:1938341741"'


def aplicar(texto: str) -> tuple[str, int]:
    total = 0
    texto, n = RODAPE.subn(lambda m: f'{m[1]}<a href="{TEL}">{m[2]}</a>{m[3]}', texto)
    total += n
    texto, n = CONTATO.subn(
        lambda m: f'<a class="elementor-icon elementor-animation-" href="{TEL}" aria-label="Ligar para (19) 3834-1741">{m[1]}</a>'
        f'{m[2]}<a href="{TEL}">{m[3]}</a>',
        texto,
    )
    total += n
    n = texto.count(MENU)
    return texto.replace(MENU, f'href="{TEL}"'), total + n


def paginas(pasta: Path | None) -> list[Path]:
    if pasta:
        return sorted(pasta.rglob("*.html"))
    saida = subprocess.check_output(["git", "ls-files", "-z", "*.html"], cwd=ROOT, text=True, encoding="utf-8")
    return [ROOT / f for f in saida.split("\0") if f]


def main(argv: list[str]) -> int:
    dry = "--dry" in argv
    resto = [a for a in argv if not a.startswith("--")]
    pasta = Path(resto[0]) if resto else None
    mudou = trocas = 0
    for p in paginas(pasta):
        bruto = p.read_bytes()
        novo, n = aplicar(bruto.decode("utf-8"))
        if not n:
            continue
        mudou += 1
        trocas += n
        if not dry:
            p.write_bytes(novo.encode("utf-8"))  # bytes: não troca as quebras de linha
    print(f"{'(simulação) ' if dry else ''}páginas alteradas: {mudou} | trocas: {trocas}")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
