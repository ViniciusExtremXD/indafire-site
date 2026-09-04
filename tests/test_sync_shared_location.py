from __future__ import annotations

import unittest
from pathlib import Path
from tempfile import TemporaryDirectory


HOME = """<html><head>
<style id="indafire-home-section-polish">
.before { color: black; }
/* Location section aligned with the site's light cards and red accents. */
#localizacao_mapa.inda-location-section { background: #f4f4f4 !important; }
.inda-location-container { display: grid; }
@media (max-width: 767px) {
  .inda-location-container { grid-template-columns: 1fr; }
}
/* Reveal the full navigation whenever the user reverses scroll direction. */
.after { color: red; }
</style>
</head><body>
<section class="inda-location-section" id="localizacao_mapa">
  <div class="inda-location-container">
    <section class="nested"><p>Nossa Localização</p></section>
    <div class="inda-location-map"><iframe title="Localização Inda Fire no Google Maps"></iframe></div>
  </div>
</section>
</body></html>"""

TARGET = """<html><head><style id="existing">body{margin:0}</style></head><body>
<main><p>Catálogo preservado</p></main>
<section id="localizacao_mapa" style="background:#12171c"><p>Mapa legado</p></section>
<footer><p>Newsletter preservada</p></footer>
</body></html>"""

TARGET_NO_LOC = """<html><head><style id="existing">body{margin:0}</style></head><body>
<main><p>Serviços preservados</p></main>
<section id="formulariosRodape"><p>Newsletter preservada</p></section>
</body></html>"""


class SharedLocationTests(unittest.TestCase):
    def test_all_internal_routes_are_managed_targets(self):
        from scripts import sync_shared_location as subject

        expected = (
            subject.ROOT / "produtos" / "index.html",
            subject.ROOT / "servicos" / "index.html",
            subject.ROOT / "treinamentos" / "index.html",
            subject.ROOT / "sobre-nos" / "index.html",
            subject.ROOT / "blog" / "index.html",
            subject.ROOT / "contato" / "index.html",
            subject.ROOT / "area-do-cliente" / "index.html",
            subject.ROOT / "politica-de-privacidade" / "index.html",
            subject.ROOT / "categoria-produto" / "extintores" / "index.html",
            subject.ROOT / "produto" / "extintor-pqs-bc-4-kg-20bc" / "index.html",
            subject.ROOT / "produto" / "unidade-central-lux-700-1200-24vdc" / "index.html",
        )
        for route in expected:
            self.assertIn(route, subject.TARGETS)

    def test_extracts_the_complete_location_section_with_nested_sections(self):
        from scripts import sync_shared_location as subject

        section = subject.extract_location(HOME)

        self.assertTrue(section.startswith('<section class="inda-location-section"'))
        self.assertIn('<section class="nested">', section)
        self.assertTrue(section.rstrip().endswith("</section>"))
        self.assertEqual(section.count("<section"), section.count("</section>"))

    def test_extracts_only_the_location_css_from_the_home_layer(self):
        from scripts import sync_shared_location as subject

        css = subject.extract_location_css(HOME)

        self.assertIn("#localizacao_mapa.inda-location-section", css)
        self.assertIn("@media (max-width: 767px)", css)
        self.assertNotIn(".before", css)
        self.assertNotIn(".after", css)

    def test_replaces_legacy_location_and_preserves_surrounding_content(self):
        from scripts import sync_shared_location as subject

        rendered = subject.render_target(TARGET, HOME)

        self.assertIn("Catálogo preservado", rendered)
        self.assertIn("Newsletter preservada", rendered)
        self.assertNotIn("Mapa legado", rendered)
        self.assertIn('class="inda-location-section"', rendered)
        self.assertIn('class="inda-location-map"', rendered)
        self.assertEqual(rendered.count('id="localizacao_mapa"'), 1)
        self.assertEqual(rendered.count(f'id="{subject.STYLE_ID}"'), 1)

    def test_inserts_location_when_missing_before_footer_forms(self):
        from scripts import sync_shared_location as subject

        rendered = subject.render_target(TARGET_NO_LOC, HOME)

        self.assertIn("Serviços preservados", rendered)
        self.assertIn("Newsletter preservada", rendered)
        self.assertIn('class="inda-location-section"', rendered)
        self.assertIn('id="localizacao_mapa"', rendered)
        self.assertIn(f'id="{subject.STYLE_ID}"', rendered)
        self.assertLess(
            rendered.index('id="localizacao_mapa"'),
            rendered.index('id="formulariosRodape"'),
        )

    def test_sync_is_idempotent(self):
        from scripts import sync_shared_location as subject

        with TemporaryDirectory() as directory:
            root = Path(directory)
            home = root / "index.html"
            target = root / "produtos" / "index.html"
            target.parent.mkdir(parents=True)
            home.write_text(HOME, encoding="utf-8")
            target.write_text(TARGET, encoding="utf-8")

            self.assertEqual(subject.sync_location(home, (target,)), 1)
            self.assertEqual(subject.sync_location(home, (target,)), 0)

    def test_shared_location_style_stays_before_the_responsive_navigation_layer(self):
        from scripts import sync_shared_location as subject

        target = TARGET.replace(
            "</head>",
            '<style id="indafire-responsive-navigation-style"></style></head>',
        )

        rendered = subject.render_target(target, HOME)

        self.assertLess(
            rendered.index(f'id="{subject.STYLE_ID}"'),
            rendered.index('id="indafire-responsive-navigation-style"'),
        )

    def test_missing_location_fails_loudly(self):
        from scripts import sync_shared_location as subject

        with self.assertRaisesRegex(ValueError, "localizacao_mapa"):
            subject.extract_location("<html><body></body></html>")


if __name__ == "__main__":
    unittest.main()
