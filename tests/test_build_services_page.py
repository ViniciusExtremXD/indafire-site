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
    def test_renders_the_five_original_split_rows_and_service_lists_in_order(self):
        from scripts import build_services_page as subject

        rendered = subject.render_services_main(LOCATION)

        positions = [rendered.index(title) for title in EXPECTED_GROUPS]
        self.assertEqual(positions, sorted(positions))
        service_positions = [rendered.index(title) for title in EXPECTED_SERVICES]
        self.assertEqual(service_positions, sorted(service_positions))
        self.assertEqual(rendered.count('class="indafire-source-service-row'), 5)
        self.assertEqual(rendered.count('class="indafire-source-service-link"'), 16)
        self.assertNotIn('class="indafire-service-grid"', rendered)
        self.assertNotIn('class="indafire-service-card"', rendered)

        feature_images = re.findall(
            r'<img class="indafire-source-service-image"[^>]+src="([^"]+)"',
            rendered,
        )
        self.assertEqual(
            feature_images,
            [
                "../wp-content/uploads/2021/12/Projeto-Simplificado.jpg",
                "../wp-content/uploads/2022/01/2.jpg",
                "../wp-content/uploads/2022/01/3.jpg",
                "../wp-content/uploads/2022/01/4.jpg",
                "../wp-content/uploads/2021/11/10639604_1538289183049362_3959369163680743290_n.jpg",
            ],
        )

    def test_uses_original_local_photography_and_real_service_destinations(self):
        from scripts import build_services_page as subject

        rendered = subject.render_services_main(LOCATION)
        sources = re.findall(r'<img[^>]+src="([^"]+)"', rendered)

        self.assertIn("../wp-content/uploads/2021/11/servicos.jpg", rendered)
        self.assertIn("../wp-content/uploads/2021/11/foguim.svg", rendered)
        self.assertIn("../wp-content/uploads/2021/11/ico-1.svg", rendered)
        self.assertIn("../wp-content/uploads/2021/11/ico-4-1.svg", rendered)
        self.assertTrue(sources)
        for source in sources:
            with self.subTest(source=source):
                self.assertTrue(source.startswith("../wp-content/uploads/"))
                self.assertTrue((ROOT / source.removeprefix("../")).is_file(), source)
        self.assertNotIn("https://indafire.com.br/servicos_inda_fire/projeto-tecnico/", rendered)
        self.assertIn('href="https://indafire.com.br/treinamentos/brigada-de-incendio/"', rendered)
        self.assertNotIn("example.com", rendered)

    def test_does_not_add_sections_that_are_absent_from_the_original_services_page(self):
        from scripts import build_services_page as subject

        rendered = subject.render_services_main(LOCATION)

        self.assertNotIn('id="indafire-commercial-whatsapp"', rendered)
        self.assertNotIn("https://wa.me/551938341741?text=", rendered)
        self.assertNotIn('id="localizacao_mapa"', rendered)
        self.assertNotIn(LOCATION, rendered)

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
        self.assertEqual(rendered.count('id="indafire-shared-location-style"'), 0)
        self.assertNotIn('id="localizacao_mapa"', rendered)
        self.assertNotIn("Nossa Localização", rendered)
        self.assertNotIn('data-elementor-type="wp-page" data-elementor-id="19"', rendered)

    def test_page_build_is_idempotent(self):
        from scripts import build_services_page as subject

        with TemporaryDirectory() as directory:
            output = Path(directory) / "servicos" / "index.html"

            self.assertEqual(subject.build_services_page(SHELL, HOME, output), 1)
            self.assertEqual(subject.build_services_page(SHELL, HOME, output), 0)
            rendered = output.read_text(encoding="utf-8")

        self.assertEqual(rendered.count('id="indafire-services-page"'), 1)

    def test_generated_page_is_already_final_for_shared_injectors(self):
        from scripts import build_services_page as subject
        from scripts import inject_internal_page_polish as internal
        from scripts import inject_responsive_navigation as navigation

        with TemporaryDirectory() as directory:
            root = Path(directory)
            output = root / "servicos" / "index.html"
            subject.build_services_page(SHELL, HOME, output)

            self.assertEqual(internal.inject_styles((output,)), 0)
            self.assertEqual(navigation.inject_assets((output,), root=root), 0)

    def test_services_route_is_managed_by_the_shared_internal_layer(self):
        from scripts import inject_internal_page_polish as internal

        self.assertIn(ROOT / "servicos" / "index.html", internal.TARGETS)


if __name__ == "__main__":
    unittest.main()
