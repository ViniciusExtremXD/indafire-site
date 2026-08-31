from __future__ import annotations

import unittest
from pathlib import Path
from tempfile import TemporaryDirectory

from scripts import update_home_brigada_reference as subject


class HomeBrigadaReferenceInjectionTests(unittest.TestCase):
    def test_injects_reference_brigada_block_into_the_applied_master_style(self) -> None:
        with TemporaryDirectory() as directory:
            page = Path(directory) / "index.html"
            page.write_text(
                '<html><head><style>\n'
                '/* 5. SEÇÃO TREINAMENTOS / BRIGADA DE INCÊNDIO */\n'
                '.elementor-element-3662fd7 { padding: 20px !important; }\n'
                '/* 6. ENQUADRAMENTO DO NEWSLETTER E CATÁLOGO */\n'
                '/* Mobile Brigada: preserve the complete video frame before the firefighter visual. */\n'
                '@media (max-width: 991px) { .elementor-element-3662fd7 { padding: 320px; } }\n'
                '/* Mobile newsletter/catalog cards: keep every form control inside its card. */\n'
                '/* Brigada video: preserve the complete 16:9 frame on every viewport. */\n'
                '.elementor-element-989c3cc video { object-fit: contain; }\n'
                '</style></head><body><style id="indafire-mobile-portrait-landscape-master-override">\n'
                '  /* DESKTOP BRIGADA DE INCÊNDIO & BOMBEIRO */\n'
                '  .elementor-element.elementor-element-3662fd7 {}\n'
                '  .elementor-element.elementor-element-8eed4f7 .elementor-button {\n  }\n'
                '  @media (max-width: 767px) {\n'
                '    /* SERVIÇOS NO MOBILE VERTICAL */\n'
                '    #carrosselServicos .swiper-slide { width: 100% !important; }\n'
                '    /* BRIGADA DE INCÊNDIO NO MOBILE VERTICAL (ZERO ESPAÇO EM BRANCO) */\n'
                '    .elementor-element.elementor-element-44bd2a0 { display: none !important; }\n'
                '    /* PRODUTOS (MOBILE VERTICAL) */\n'
                '  }\n'
                '  @media (max-width: 1024px) and (orientation: landscape) {\n'
                '    /* SERVIÇOS NO MOBILE HORIZONTAL (LADO A LADO) */\n'
                '    .elementor-element.elementor-element-d88d016 { display: flex !important; }\n'
                '  }\n'
                '</style></body></html>',
                encoding="utf-8",
            )

            changed = subject.inject_styles((page,))
            rendered = page.read_text(encoding="utf-8")

        self.assertEqual(changed, 1)
        self.assertIn(subject.MARKER, rendered)
        self.assertIn('id="indafire-mobile-portrait-landscape-master-override"', rendered)
        self.assertNotIn('DESKTOP BRIGADA', rendered)
        self.assertNotIn('@media (min-width: 1025px)', rendered)
        self.assertNotIn('SERVIÇOS NO MOBILE VERTICAL', rendered)
        self.assertNotIn('BRIGADA DE INCÊNDIO NO MOBILE VERTICAL', rendered)
        self.assertNotIn('SERVIÇOS NO MOBILE HORIZONTAL', rendered)
        self.assertNotIn('SEÇÃO TREINAMENTOS / BRIGADA DE INCÊNDIO', rendered)
        self.assertNotIn('Mobile Brigada: preserve', rendered)
        self.assertNotIn('Brigada video: preserve', rendered)
        self.assertNotIn('width: 54%', rendered)

    def test_restores_the_published_brigada_copy(self) -> None:
        source = (
            '<html><head></head><body>'
            '<style id="indafire-mobile-portrait-landscape-master-override">\n'
            '  /* DESKTOP BRIGADA DE INCÊNDIO & BOMBEIRO */\n'
            '  .elementor-element.elementor-element-3662fd7 {}\n'
            '  .elementor-element.elementor-element-8eed4f7 .elementor-button {\n  }\n'
            '</style>'
            '<div class="elementor-element-1c2246b"><p>Capacitação completa com conteúdo teórico e prático, em total conformidade com a NBR 14276 e decretos estaduais do Corpo de Bombeiros.</p></div>'
            '</body></html>'
        )
        with TemporaryDirectory() as directory:
            page = Path(directory) / "index.html"
            page.write_text(source, encoding="utf-8")
            self.assertEqual(subject.inject_styles((page,)), 1)
            rendered = page.read_text(encoding="utf-8")

        self.assertIn(
            'Realizamos o treinamento com todo o conteúdo teórico, conforme NBR-14276/06 e decretos estaduais do corpo de bombeiros.',
            rendered,
        )
        self.assertNotIn('Capacitação completa', rendered)

    def test_injection_is_idempotent(self) -> None:
        with TemporaryDirectory() as directory:
            page = Path(directory) / "index.html"
            page.write_text(
                '<html><head></head><body><style id="indafire-mobile-portrait-landscape-master-override">\n'
                '  /* DESKTOP BRIGADA DE INCÊNDIO & BOMBEIRO */\n'
                '  .elementor-element.elementor-element-3662fd7 {}\n'
                '  .elementor-element.elementor-element-8eed4f7 .elementor-button {\n  }\n'
                '</style></body></html>',
                encoding="utf-8",
            )

            self.assertEqual(subject.inject_styles((page,)), 1)
            self.assertEqual(subject.inject_styles((page,)), 0)


if __name__ == "__main__":
    unittest.main()
