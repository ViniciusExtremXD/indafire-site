from __future__ import annotations

import re
import unittest
from pathlib import Path
from tempfile import TemporaryDirectory


ROOT = Path(__file__).resolve().parents[1]
SHELL = ROOT / "sobre-nos" / "index.html"
HOME = ROOT / "index.html"
LOCATION = """<section class="inda-location-section" id="localizacao_mapa">
<div class="inda-location-container"><div class="inda-location-map">
<iframe title="Localização Inda Fire no Google Maps"></iframe>
</div></div></section>"""

EXPECTED_GROUPS = (
    "Engenharia e Consultoria",
    "Manutenções e Inspeções",
    "Sistemas de Prevenção e Combate a Incêndio",
    "Treinamentos",
    "Serviços Especiais",
)

EXPECTED_SERVICES = (
    "AVCB/CLCB – Obtenção ou renovação",
    "Processo simplificado (PTS)",
    "Projeto Técnico",
    "Inspeção de Equipamentos",
    "Instalação e venda de extintores",
    "Recarga de Extintores",
    "Teste Hidrostático em Mangueiras de Incêndios",
    "Sinalização de Emergência",
    "Sistema de alarme de incêndio",
    "Sistema de detecção de fumaça e calor",
    "Sistema de Hidrantes",
    "Sistema de iluminação de emergência",
    "Sistemas de Sprinklers",
    "Brigada de Incêndio",
    "Equipe habilitada para eventos ou trabalhos específicos",
    "Fabricação de caixa d’água metálica",
    "Locação de equipamentos",
)


class BuildServicesPageTests(unittest.TestCase):
    def test_renders_all_original_service_groups_and_cards_in_order(self):
        from scripts import build_services_page as subject

        rendered = subject.render_services_main(LOCATION)

        positions = [rendered.index(title) for title in EXPECTED_GROUPS]
        self.assertEqual(positions, sorted(positions))
        service_positions = [rendered.index(title) for title in EXPECTED_SERVICES]
        self.assertEqual(service_positions, sorted(service_positions))
        self.assertEqual(rendered.count('class="indafire-service-card"'), 17)
        self.assertEqual(rendered.count('loading="lazy"'), 17)

    def test_uses_original_local_photography_and_real_service_destinations(self):
        from scripts import build_services_page as subject

        rendered = subject.render_services_main(LOCATION)
        sources = re.findall(r'<img[^>]+src="([^"]+)"', rendered)

        self.assertIn("../wp-content/uploads/2021/11/servicos.jpg", rendered)
        self.assertIn("../wp-content/uploads/2021/10/shutterstock_1044591571-scaled-1-1024x467.png", rendered)
        self.assertTrue(sources)
        for source in sources:
            with self.subTest(source=source):
                self.assertTrue(source.startswith("../wp-content/uploads/"))
                self.assertTrue((ROOT / source.removeprefix("../")).is_file(), source)
        self.assertIn("https://indafire.com.br/servicos_inda_fire/projeto-tecnico/", rendered)
        self.assertIn('href="../treinamentos/"', rendered)
        self.assertNotIn("example.com", rendered)

    def test_includes_services_form_and_the_exact_supplied_location_fragment(self):
        from scripts import build_services_page as subject

        rendered = subject.render_services_main(LOCATION)

        self.assertIn('id="indafire-commercial-whatsapp"', rendered)
        self.assertIn('<option value="Serviço" selected>', rendered)
        self.assertIn("https://wa.me/551938341741?text=", rendered)
        self.assertEqual(rendered.count('id="localizacao_mapa"'), 1)
        self.assertIn(LOCATION, rendered)

    def test_css_contract_covers_desktop_portrait_and_landscape_without_global_leaks(self):
        from scripts import build_services_page as subject

        rendered = subject.render_services_main(LOCATION)

        self.assertIn('id="indafire-services-style"', rendered)
        self.assertIn("@media (min-width: 1025px)", rendered)
        self.assertIn("@media (max-width: 767px)", rendered)
        self.assertIn("orientation: landscape", rendered)
        self.assertIn("#indafire-services-page", rendered)

    def test_build_page_replaces_only_the_page_body_and_preserves_shared_shell(self):
        from scripts import build_services_page as subject

        shell = SHELL.read_text(encoding="utf-8")
        home = HOME.read_text(encoding="utf-8")
        rendered = subject.build_page(shell, home)

        self.assertIn("<title>Serviços - Inda Fire - Equipamentos de Combate a Incêndios</title>", rendered)
        self.assertIn('<link rel="canonical" href="../servicos/"', rendered)
        self.assertIn('id="headerInda"', rendered)
        self.assertEqual(rendered.count('data-elementor-type="footer"'), 1)
        self.assertEqual(rendered.count('id="indafire-services-page"'), 1)
        self.assertNotIn('data-elementor-type="wp-page" data-elementor-id="19"', rendered)

    def test_page_build_is_idempotent(self):
        from scripts import build_services_page as subject

        with TemporaryDirectory() as directory:
            output = Path(directory) / "servicos" / "index.html"

            self.assertEqual(subject.build_services_page(SHELL, HOME, output), 1)
            self.assertEqual(subject.build_services_page(SHELL, HOME, output), 0)
            rendered = output.read_text(encoding="utf-8")

        self.assertEqual(rendered.count('id="indafire-services-page"'), 1)

    def test_services_route_is_managed_by_the_shared_internal_layer(self):
        from scripts import inject_internal_page_polish as internal

        self.assertIn(ROOT / "servicos" / "index.html", internal.TARGETS)


if __name__ == "__main__":
    unittest.main()
