# Image sources

Download date: 2026-08-12.

## Third-party photography

All selected source files have at least 2400 pixels on their longest edge. The committed WebP files are resized and compressed adaptations.

| Used for | Title | Creator | Source page | Original dimensions | License |
| --- | --- | --- | --- | --- | --- |
| `hero.webp`, `hero-960.webp`, `hero-1440.webp`, `sprinklers.webp`, `hydrants.webp`, `facility.webp` | SprinkleranschluesseSF (external fire sprinkler and standpipe connections) | Túrelio | [Wikimedia Commons](https://commons.wikimedia.org/wiki/File:SprinkleranschluesseSF.jpg) | 3007 × 1238 | [CC BY-SA 2.5](https://creativecommons.org/licenses/by-sa/2.5/) — resized and compressed; credit retained here; adaptations use the same license |
| `inspection.webp` | Christian Jacobs, fire inspector, demonstrating grease-fire extinguishing techniques | Airman Areca T. Wilson, U.S. Air Force | [Wikimedia Commons](https://commons.wikimedia.org/wiki/File:Christian_Jacobs,_a_fire_inspector_with_the_633rd_Civil_Engineer_Squadron,_demonstrates_techniques_for_extinguishing_a_grease_fire_during_Fire_Prevention_Week_at_Joint_Base_Langley-Eustis,_Va_131011-F-IT851-014.jpg) | 2588 × 1910 | [Public domain — U.S. federal government work](https://commons.wikimedia.org/wiki/Template:PD-USGov-Military-Air_Force) — resized and compressed |
| `training.webp` | RAF Firefighter During a Training Exercise | Corporal Jennie Blunden / MOD | [Wikimedia Commons](https://commons.wikimedia.org/wiki/File:RAF_Firefighter_During_a_Training_Exercise_MOD_45152012.jpg) | 3032 × 4800 | [Open Government Licence v1.0](https://www.nationalarchives.gov.uk/doc/open-government-licence/version/1/) — commercial reuse and adaptation permitted; resized and compressed; required credit retained here |

## Inda Fire-owned media

The brand vectors and product/category artwork below come from the official Inda Fire website. They are reused for this commissioned redesign of the same company.

- Brand vectors: [logo](https://indafire.com.br/site/wp-content/uploads/2021/10/logo.svg), [white logo](https://indafire.com.br/site/wp-content/uploads/2021/11/logo-branco.svg), [favicon](https://indafire.com.br/site/wp-content/uploads/2021/10/ico-1.svg).
- Product artwork: [Placa E5](https://indafire.com.br/site/wp-content/uploads/2022/01/52-2.png), [Capacete Gallet](https://indafire.com.br/site/wp-content/uploads/2021/11/EPI.png), [Armário corta-fogo](https://indafire.com.br/site/wp-content/uploads/2021/11/EPC.png), [Botoeira](https://indafire.com.br/site/wp-content/uploads/2021/11/Alarmes_Incendio.png), [Cinturão X-PERT II](https://indafire.com.br/site/wp-content/uploads/2022/01/1650.png), [Colete KED](https://indafire.com.br/site/wp-content/uploads/2021/11/APH.png), [Suporte de solo](https://indafire.com.br/site/wp-content/uploads/2021/11/Acessorios.png), [Mangueira tipo I](https://indafire.com.br/site/wp-content/uploads/2021/11/103-1000x1000-1.png).
- `unidade-central-lux.webp`: exact LUX 700/1200 unit shown on printed page 34 of the [official Inda Fire product catalog](https://indafire.com.br/site/wp-content/uploads/2021/11/catalogo-inda-fire.pdf). The commissioned-redesign authorization applies to this Inda Fire-owned catalog. The page was rendered at 1272 × 1800, the product-only region was cropped and padded to 310 × 260 outside `public/`, then resized to width 640 and encoded as WebP quality 82.
- `cilindro-6l.webp`: exact "Cilindro aço leve — Pressão 300 Bar", volume 6 L, shown on printed page 44 of the same [official Inda Fire product catalog](https://indafire.com.br/site/wp-content/uploads/2021/11/catalogo-inda-fire.pdf). The page was rendered at 1272 × 1800, the product-only region was cropped and padded to 210 × 405 outside `public/`, then resized to width 640 and encoded as WebP quality 82.

No file whose name contains `shutterstock` is used.

## Complete original Inda Fire archive

The deterministic source-of-truth inventory is `content/original-media.json`. It was imported from the official public WordPress REST collection and the six public content endpoints on 2026-08-13. The archive preserves every retrievable unique public image/video byte in `public/media/original/`; generated WordPress thumbnail renditions are deliberately excluded and selected web derivatives live in `public/media/optimized/`.

The public REST collection declares 351 slots and exposes 241 records: 236 images, three MP4 videos, one PDF and one administrative PPTX. The PDF remains a document at its official source URL and the PPTX is excluded from deploy. SHA-256 verification found 229 unique visual binaries across 239 visual source records, with all ten byte-identical source pairs retained as aliases in the manifest. Filename signals such as `shutterstock` are preserved as provenance warnings; this archive does not assert authorship.

Self-hosted fonts in `public/fonts/` use official Google Fonts Latin WOFF2 files: Barlow Condensed 600/700/800 and Inter Variable 400–700. Their exact source URLs, SHA-256 hashes and upstream OFL license files are recorded in the manifest.
