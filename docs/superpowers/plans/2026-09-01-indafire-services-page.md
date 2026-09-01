# Indafire Services Page Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Entregar `/servicos/` com o mesmo sistema visual aprovado em Home e Produtos, tornar o mapa de Produtos uma cópia exata do mapa da Home e fazer todas as logos internas voltarem para a página inicial, preservando integralmente os catálogos existentes.

**Architecture:** A nova página será gerada de forma idempotente a partir do shell estático já existente, por um script dedicado. Um segundo módulo manterá a seção de localização como fragmento compartilhado extraído da Home. A normalização dos links das logos continuará sob responsabilidade do injetor mestre de navegação. O build local executará esses passos antes das camadas visuais existentes e validará os marcadores gerenciados.

**Tech Stack:** Python 3 (`pathlib`, `re`, `html` e `unittest`), HTML/CSS/JavaScript estático, pipeline atual de injeção idempotente, GitHub Actions Pages na branch `main`.

---

## Restrições de escopo

- Não alterar produtos, categorias, ordem, busca, filtros ou descrições do catálogo.
- Não redesenhar Home, newsletter, rodapé ou menu.
- Não criar rotas fictícias para detalhes de serviços.
- Não usar imagens geradas, hotlinks ou fotografias externas; copiar somente os binários originais já arquivados no workspace.
- Não adicionar `dist_gh_pages/` ao commit: o workflow atual publica diretamente a raiz de `main`.
- Não usar `git add .`; o workspace contém muitos arquivos não rastreados e evidências de auditoria fora deste escopo.

### Task 0: Preservar e versionar o trabalho de Produtos já aprovado

**Files:**
- Verify/commit: `produtos/index.html`
- Verify/commit: `categoria-produto/extintores/index.html`
- Verify/commit: `produto/extintor-pqs-bc-4-kg-20bc/index.html`
- Verify/commit: `produto/unidade-central-lux-700-1200-24vdc/index.html`
- Verify/commit: `scripts/build_local_preview.py`
- Verify/commit: `scripts/inject_product_catalog_polish.py`
- Verify/commit: `tests/test_build_local_preview.py`
- Verify/commit: `tests/test_inject_product_catalog_polish.py`

- [ ] **Step 1: Confirmar que o diff atual corresponde somente ao trabalho aprovado**

Run:

```powershell
git diff -- produtos/index.html categoria-produto/extintores/index.html produto/extintor-pqs-bc-4-kg-20bc/index.html produto/unidade-central-lux-700-1200-24vdc/index.html scripts/build_local_preview.py scripts/inject_product_catalog_polish.py tests/test_build_local_preview.py tests/test_inject_product_catalog_polish.py
```

Expected: somente o polimento visual previamente aprovado das imagens originais de produtos, o formulário comercial antes do mapa e os testes correspondentes; nenhuma mudança em nomes, categorias, ordem, filtros ou descrições.

- [ ] **Step 2: Reexecutar os testes focais existentes**

Run:

```powershell
python -m unittest tests/test_build_local_preview.py tests/test_inject_product_catalog_polish.py tests/test_inject_internal_page_polish.py tests/test_static_hero_assets.py -v
```

Expected: 34 testes relevantes passam.

- [ ] **Step 3: Criar um checkpoint limpo antes das novas mudanças**

```powershell
git add produtos/index.html categoria-produto/extintores/index.html produto/extintor-pqs-bc-4-kg-20bc/index.html produto/unidade-central-lux-700-1200-24vdc/index.html scripts/build_local_preview.py scripts/inject_product_catalog_polish.py tests/test_build_local_preview.py tests/test_inject_product_catalog_polish.py
git commit -m "feat: polish product catalog and commercial contact"
```

### Task 1: Sincronizar o mapa exato da Home

**Files:**
- Create: `scripts/sync_shared_location.py`
- Create: `tests/test_sync_shared_location.py`
- Modify: `produtos/index.html`

- [ ] **Step 1: Escrever os testes que falham**

Cobrir as funções públicas:

```python
def extract_location(source: str) -> str:
    """Return the complete section whose id is localizacao_mapa."""

def extract_location_css(source: str) -> str:
    """Return the managed inda-location CSS block from the Home document."""

def sync_location(home_page: Path, targets: tuple[Path, ...]) -> int:
    """Replace each target location section and CSS layer idempotently."""
```

Os testes devem provar:

```python
self.assertIn('class="inda-location-section"', rendered)
self.assertIn('class="inda-location-container"', rendered)
self.assertIn('class="inda-location-map"', rendered)
self.assertEqual(rendered.count('id="localizacao_mapa"'), 1)
self.assertEqual(rendered.count('id="indafire-shared-location-style"'), 1)
self.assertEqual(sync_location(home, (products,)), 0)  # segunda execução
```

- [ ] **Step 2: Executar o teste RED**

Run: `python -m unittest tests/test_sync_shared_location.py -v`

Expected: `ModuleNotFoundError` para `scripts.sync_shared_location`.

- [ ] **Step 3: Implementar a extração e sincronização mínimas**

Usar um scanner de tags `<section>` com profundidade, em vez de uma regex que pare no primeiro `</section>`. O fragmento fonte é `index.html#localizacao_mapa`. Extrair também as regras `.inda-location-*` da camada da Home e instalá-las como:

```html
<style id="indafire-shared-location-style">
/* cópia gerenciada das regras de localização da Home */
</style>
```

O alvo inicial é `produtos/index.html`; `servicos/index.html` será adicionado depois que existir. Preservar o restante do arquivo byte a byte e retornar o número de documentos realmente alterados.

- [ ] **Step 4: Executar os testes GREEN e verificar o diff restrito**

Run: `python -m unittest tests/test_sync_shared_location.py -v`

Expected: todos os testes passam.

Run: `git diff -- produtos/index.html scripts/sync_shared_location.py tests/test_sync_shared_location.py`

Expected: em Produtos, apenas a seção de localização e a camada CSS gerenciada mudam; catálogo, formulário e newsletter permanecem intactos.

- [ ] **Step 5: Commit**

```powershell
git add scripts/sync_shared_location.py tests/test_sync_shared_location.py produtos/index.html
git commit -m "fix: share home location with product page"
```

### Task 2: Fazer todas as logos voltarem para a Home

**Files:**
- Modify: `scripts/inject_responsive_navigation.py`
- Modify: `tests/test_inject_responsive_navigation.py`
- Modify: managed HTML pages listed by `scripts/inject_internal_page_polish.py`

- [ ] **Step 1: Adicionar testes de profundidade de rota**

Adicionar uma função pura e testes para cabeçalho e rodapé:

```python
def home_href(page: Path, root: Path = ROOT) -> str:
    depth = len(page.relative_to(root).parent.parts)
    return "./" if depth == 0 else "../" * depth

def normalize_logo_links(source: str, href: str) -> str:
    """Rewrite only anchors inside theme-site-logo widgets."""
```

Asserções obrigatórias:

```python
self.assertEqual(home_href(ROOT / "index.html"), "./")
self.assertEqual(home_href(ROOT / "produtos/index.html"), "../")
self.assertEqual(home_href(ROOT / "produto/item/index.html"), "../../")
self.assertEqual(rendered.count('href="../"'), 2)  # header + footer fixture
```

Confirmar que links fora de `.elementor-widget-theme-site-logo` não mudam.

- [ ] **Step 2: Executar o teste RED**

Run: `python -m unittest tests/test_inject_responsive_navigation.py -v`

Expected: falha porque as funções ainda não existem ou os `href` continuam incorretos.

- [ ] **Step 3: Implementar no injetor mestre**

No laço de `inject_assets`, calcular `href = home_href(page)` e chamar `normalize_logo_links` antes de gravar o HTML. Restringir a busca aos dois widgets de logo do tema (`elementor-widget-theme-site-logo`) para não tocar links de produto, menu, formulário ou redes sociais.

- [ ] **Step 4: Executar testes e build idempotente**

Run: `python -m unittest tests/test_inject_responsive_navigation.py -v`

Expected: todos os testes passam.

Run: `python scripts/inject_responsive_navigation.py; python scripts/inject_responsive_navigation.py`

Expected: a segunda execução informa `0 page(s)` alteradas.

- [ ] **Step 5: Verificar amostras reais**

Run:

```powershell
rg -n -U 'elementor-widget-theme-site-logo[\s\S]{0,500}<a href="(\./|\.\./|\.\./\.\./)"' index.html produtos/index.html produto/extintor-pqs-bc-4-kg-20bc/index.html
```

Expected: Home usa `./`, Produtos usa `../` e detalhe usa `../../`.

- [ ] **Step 6: Commit somente os arquivos gerenciados alterados**

```powershell
git add scripts/inject_responsive_navigation.py tests/test_inject_responsive_navigation.py index.html produtos/index.html categoria-produto/extintores/index.html produto/extintor-pqs-bc-4-kg-20bc/index.html produto/unidade-central-lux-700-1200-24vdc/index.html sobre-nos/index.html treinamentos/index.html contato/index.html area-do-cliente/index.html politica-de-privacidade/index.html
git commit -m "fix: route site logos back to home"
```

### Task 3: Adicionar somente os ativos originais necessários a Serviços

**Files:**
- Create/copy: `wp-content/uploads/2021/11/servicos.jpg`
- Create/copy, if absent: `wp-content/uploads/2021/12/Projeto-Simplificado.jpg`
- Create/copy, if absent: `wp-content/uploads/2022/01/2.jpg`
- Create/copy, if absent: `wp-content/uploads/2022/01/3.jpg`
- Create/copy, if absent: `wp-content/uploads/2022/01/4.jpg`
- Create: `tests/test_services_assets.py`

- [ ] **Step 1: Testar existência e integridade antes da cópia**

O teste deve comparar SHA-256 do destino com os valores originais já medidos e validar a assinatura JPEG/PNG:

```python
EXPECTED_SHA256 = {
    "wp-content/uploads/2021/11/servicos.jpg": "076DC8B0F8F69955C94DC400B334BC1E6E926AEEE6E600D7A3845CC352CFF4A0",
    "wp-content/uploads/2021/12/Projeto-Simplificado.jpg": "2F34D458D345A1CFB5E298E2FA2142D966247432BDEF737E53E788FCD31651C0",
    "wp-content/uploads/2022/01/2.jpg": "39286A4FD9E84C1A3251CE784790A850AD0113A04BF77F4D4BFD7B38D57E7E1C",
    "wp-content/uploads/2022/01/3.jpg": "4A56B9EAF968FC4FB86AAD9CB2ACE2B5093722639FC16E31068BF6C02CF497FC",
    "wp-content/uploads/2022/01/4.jpg": "D106942E553303B7A270940EEA63033773D5718E6EE02A006751B93AB4B8222D",
}
```

- [ ] **Step 2: Executar o teste RED**

Run: `python -m unittest tests/test_services_assets.py -v`

Expected: falha para os destinos ausentes.

- [ ] **Step 3: Copiar os binários exatos**

Usar `Copy-Item -LiteralPath` somente para os arquivos ausentes. Não converter, recomprimir, recortar ou renomear conteúdo. Antes de copiar, resolver e imprimir origem e destino para confirmar que ambos estão dentro do workspace.

- [ ] **Step 4: Executar o teste GREEN**

Run: `python -m unittest tests/test_services_assets.py -v`

Expected: hashes e assinaturas passam.

- [ ] **Step 5: Commit**

```powershell
git add tests/test_services_assets.py wp-content/uploads/2021/11/servicos.jpg wp-content/uploads/2021/12/Projeto-Simplificado.jpg wp-content/uploads/2022/01/2.jpg wp-content/uploads/2022/01/3.jpg wp-content/uploads/2022/01/4.jpg
git commit -m "assets: restore original services photography"
```

### Task 4: Gerar a nova rota `/servicos/`

**Files:**
- Create: `scripts/build_services_page.py`
- Create: `tests/test_build_services_page.py`
- Create/generated: `servicos/index.html`
- Modify: `scripts/inject_internal_page_polish.py`
- Modify: `scripts/inject_responsive_navigation.py` indirectly through shared `TARGETS`

- [ ] **Step 1: Criar fixtures e testes de contrato da página**

Definir as estruturas tipadas e API pública:

```python
@dataclass(frozen=True)
class Service:
    title: str
    image: str
    href: str
    description: str

@dataclass(frozen=True)
class ServiceGroup:
    title: str
    eyebrow: str
    image: str
    services: tuple[Service, ...]

def render_services_main(location_section: str) -> str:
    """Render the complete managed Services main element."""

def build_page(shell: str, home: str) -> str:
    """Return the Services document while preserving the shared shell."""

def build_services_page(shell_page: Path, home_page: Path, output_page: Path) -> int:
    """Write the generated route and return one only when bytes changed."""
```

Os testes devem validar, nesta ordem:

1. Hero `SERVIÇOS` com `../wp-content/uploads/2021/11/servicos.jpg`.
2. Introdução `ENGENHARIA E CONSULTORIA` com fotografia original.
3. Cinco grupos e os 17 cards listados na especificação aprovada.
4. Até três cards por linha no desktop, uma coluna em 390 px e duas/três colunas compactas em 844×390.
5. Links apenas para rotas originais existentes; `Brigada de Incêndio` aponta para `../treinamentos/`.
6. Formulário comercial com `Serviço` pré-selecionado e WhatsApp `551938341741`.
7. Exatamente um `#localizacao_mapa`, idêntico ao fragmento da Home.
8. Newsletter e footer preservados do shell.
9. `build_services_page(...)` retorna `1` na primeira gravação e `0` na segunda.

- [ ] **Step 2: Executar o teste RED**

Run: `python -m unittest tests/test_build_services_page.py -v`

Expected: `ModuleNotFoundError` ou falta de `servicos/index.html`.

- [ ] **Step 3: Implementar o gerador idempotente**

Usar `sobre-nos/index.html` como shell estrutural para manter `<head>`, cabeçalho, newsletter, rodapé, WhatsApp flutuante e scripts já compatíveis. Substituir apenas o `<main>` da página, atualizar `<title>`, canonical e metadados específicos de Sobre Nós para Serviços e inserir um bloco gerenciado:

```html
<main id="indafire-services-page">
  <section class="indafire-services-hero" aria-labelledby="indafire-services-title">
    <h1 id="indafire-services-title">SERVIÇOS</h1>
  </section>
  <section class="indafire-services-intro" aria-labelledby="indafire-services-intro-title">
    <h2 id="indafire-services-intro-title">ENGENHARIA E CONSULTORIA</h2>
  </section>
  <section class="indafire-services-groups" aria-label="Serviços Inda Fire"></section>
  <section id="indafire-commercial-whatsapp" data-context="services" aria-labelledby="indafire-commercial-title"></section>
  <!-- exact Home location fragment -->
</main>
```

Manter o sistema visual aprovado: fundo claro, grafite `#202124`, vermelho `#e30613`, bordas arredondadas discretas e sombras moderadas. Imagens de hero usam `cover`; imagens de card usam `cover` com `aspect-ratio` estável e `object-position` específico somente quando necessário para preservar o assunto original. Adicionar `loading="lazy"`, dimensões e `alt` descritivo nos cards; o hero deve carregar imediatamente.

Aplicar os breakpoints sem afetar outras rotas:

```css
@media (min-width: 1025px) { .indafire-service-grid { grid-template-columns: repeat(3, minmax(0, 1fr)); } }
@media (min-width: 768px) and (max-width: 1024px) { .indafire-service-grid { grid-template-columns: repeat(2, minmax(0, 1fr)); } }
@media (max-width: 767px) { .indafire-service-grid { grid-template-columns: 1fr; } }
@media (orientation: landscape) and (max-height: 600px) and (min-width: 568px) { .indafire-service-grid { grid-template-columns: repeat(3, minmax(0, 1fr)); } }
```

As descrições e links devem vir do HTML original já capturado. Quando não houver detalhe estático local, usar somente estas URLs reais confirmadas:

```text
AVCB/CLCB -> https://indafire.com.br/servicos_inda_fire/obtencao-ou-renovacao-avcb-clcb/
Processo simplificado (PTS) -> https://indafire.com.br/servicos_inda_fire/processo-simplificado-pts/
Projeto Técnico -> https://indafire.com.br/servicos_inda_fire/projeto-tecnico/
Inspeção de Equipamentos -> https://indafire.com.br/servicos_inda_fire/inspecao-de-equipamentos/
Instalação e venda de extintores -> https://indafire.com.br/servicos_inda_fire/instalacao-e-venda-de-extintores/
Recarga de Extintores -> https://indafire.com.br/servicos_inda_fire/recarga-de-extintores/
Teste Hidrostático em Mangueiras de Incêndios -> https://indafire.com.br/servicos_inda_fire/teste-hidrostatico-em-mangueiras-de-incendios/
Sinalização de Emergência -> https://indafire.com.br/servicos_inda_fire/sinalizacao-de-emergencia/
Sistema de alarme de incêndio -> https://indafire.com.br/servicos_inda_fire/sistema-de-alarme-de-incendio/
Sistema de detecção de fumaça e calor -> https://indafire.com.br/servicos_inda_fire/sistema-de-deteccao-de-fumaca-e-calor/
Sistema de Hidrantes -> https://indafire.com.br/servicos_inda_fire/sistema-de-hidrantes/
Sistema de iluminação de emergência -> https://indafire.com.br/servicos_inda_fire/sistema-de-iluminacao-de-emergencia/
Sistemas de Sprinklers -> https://indafire.com.br/servicos_inda_fire/sistemas-de-sprinklers/
Brigada de Incêndio -> ../treinamentos/
Equipe habilitada -> https://indafire.com.br/servicos_inda_fire/disponibilizacao-de-equipe-habilitada-para-eventos-ou-trabalhos-especificos/
Fabricação de caixa d’água metálica -> https://indafire.com.br/servicos_inda_fire/fabricacao-de-caixa-dagua-metalica/
Locação de equipamentos -> https://indafire.com.br/servicos_inda_fire/locacao-de-equipamentos/
```

- [ ] **Step 4: Registrar a rota nas camadas compartilhadas**

Adicionar `ROOT / "servicos" / "index.html"` a `scripts/inject_internal_page_polish.py::TARGETS`. Como `inject_responsive_navigation.py::TARGETS` importa essa tupla, a navegação e o comportamento de scroll serão aplicados automaticamente.

- [ ] **Step 5: Executar testes e inspecionar a saída**

Run:

```powershell
python -m unittest tests/test_build_services_page.py tests/test_services_assets.py -v
python scripts/build_services_page.py
python scripts/build_services_page.py
```

Expected: testes passam; segunda geração informa zero alterações.

- [ ] **Step 6: Commit**

```powershell
git add scripts/build_services_page.py tests/test_build_services_page.py scripts/inject_internal_page_polish.py servicos/index.html
git commit -m "feat: add modernized services page"
```

### Task 5: Integrar a nova rota ao build local e à validação

**Files:**
- Modify: `scripts/build_local_preview.py`
- Modify: `tests/test_build_local_preview.py`
- Modify: `README.md`

- [ ] **Step 1: Escrever os testes de integração que falham**

Adicionar marcadores:

```python
SERVICES_PAGE_MARKER = 'id="indafire-services-page"'
SHARED_LOCATION_MARKER = 'id="indafire-shared-location-style"'
```

Validar que:

- `servicos/index.html` existe e contém as camadas interna, navegação, Serviços, formulário e mapa compartilhado.
- `produtos/index.html` contém o mapa compartilhado.
- a segunda execução completa é no-op.
- as rotas de catálogo continuam contendo exatamente os marcadores anteriores.

- [ ] **Step 2: Executar o teste RED**

Run: `python -m unittest tests/test_build_local_preview.py -v`

Expected: falha porque o build ainda não chama o gerador e o sincronizador.

- [ ] **Step 3: Atualizar a ordem do pipeline**

Em `main()` executar nesta ordem:

```python
services_changed = services_page.build_services_page(
    ROOT / "sobre-nos/index.html", ROOT / "index.html", ROOT / "servicos/index.html"
)
location_changed = shared_location.sync_location(
    ROOT / "index.html",
    (ROOT / "produtos/index.html", ROOT / "servicos/index.html"),
)
```

Depois executar os injetores existentes, pois a rota de Serviços já existirá quando `internal.TARGETS` e `responsive_navigation.TARGETS` forem percorridos. Atualizar a mensagem final para incluir os dois contadores.

- [ ] **Step 4: Atualizar o README**

Adicionar `/servicos/` à matriz de rotas e os novos testes ao comando de validação. Documentar que Pages publica a raiz de `main` pelo workflow `.github/workflows/static.yml`; manter `dist_gh_pages/` identificado como legado.

- [ ] **Step 5: Rodar o conjunto focal e o build duas vezes**

Run:

```powershell
python -m unittest tests/test_sync_shared_location.py tests/test_services_assets.py tests/test_build_services_page.py tests/test_inject_responsive_navigation.py tests/test_build_local_preview.py -v
python scripts/build_local_preview.py
python scripts/build_local_preview.py
```

Expected: tudo passa e o segundo build informa zero alterações em todas as camadas.

- [ ] **Step 6: Confirmar que o catálogo não mudou fora do diff já aprovado**

Run:

```powershell
git diff --stat
git diff -- produtos/index.html categoria-produto/extintores/index.html produto/extintor-pqs-bc-4-kg-20bc/index.html produto/unidade-central-lux-700-1200-24vdc/index.html
```

Expected: em Produtos, somente mapa/logo/camadas gerenciadas do build aparecem além das alterações comerciais previamente aprovadas; nenhum card, produto, filtro ou ordem de catálogo novo.

- [ ] **Step 7: Commit**

```powershell
git add scripts/build_local_preview.py tests/test_build_local_preview.py README.md
git commit -m "build: include services and shared location"
```

### Task 6: Design QA nos três cenários

**Files:**
- Create: `screenshots/services-desktop-1366x900.png`
- Create: `screenshots/services-mobile-portrait-390x844.png`
- Create: `screenshots/services-mobile-landscape-844x390.png`
- Create: `screenshots/products-map-mobile-portrait-390x844.png`
- Create: `docs/audits/2026-09-01-services-design-qa.md`

- [ ] **Step 1: Iniciar a prévia local**

Run: `python -m http.server 4174 --directory .`

Expected: servidor local acessível em `http://127.0.0.1:4174/`.

- [ ] **Step 2: Executar a skill obrigatória de Design QA**

Ler e seguir `product-design:design-qa` antes de capturar resultados. Comparar a fonte original já capturada (`https://indafire.com.br/servicos/`) com `http://127.0.0.1:4174/servicos/`, preservando conteúdo e fotografias, mas aceitando a modernização aprovada para corrigir o lazy loading quebrado.

- [ ] **Step 3: Capturar desktop, celular vertical e celular horizontal**

Capturar a página inteira nos viewports 1366×900, 390×844 e 844×390. Em cada viewport verificar:

- hero legível e sem pixelização;
- header sem sobreposição, menu compacto funcional e scroll motion preservado;
- nenhuma barra de rolagem horizontal;
- todos os 17 cards visíveis, sem recorte ruim ou imagens trocadas;
- formulário sem campos fora do container;
- mapa igual ao da Home e sem bloco escuro legado;
- newsletter e rodapé sem alteração visual;
- Produtos continua com o mesmo catálogo e usa somente o novo mapa compartilhado.

- [ ] **Step 4: Testar interações e console**

Testar cliques na logo em Home, Produtos, Serviços e uma rota de segundo nível; todos devem resolver para `/indafire-site/` na prévia do GitHub ou `/` localmente. Testar o envio do formulário sem concluir conversa externa: confirmar somente que a URL gerada começa com `https://wa.me/551938341741?text=` e contém assunto de Serviço. Verificar console sem erros JavaScript novos e todos os assets locais com HTTP 200.

- [ ] **Step 5: Registrar a auditoria**

Em `docs/audits/2026-09-01-services-design-qa.md`, registrar viewport, rota, resultado, screenshots e qualquer diferença intencional em relação ao site original. Não incluir arquivos temporários de captura ou caches.

- [ ] **Step 6: Commit da evidência final**

```powershell
git add docs/audits/2026-09-01-services-design-qa.md screenshots/services-desktop-1366x900.png screenshots/services-mobile-portrait-390x844.png screenshots/services-mobile-landscape-844x390.png screenshots/products-map-mobile-portrait-390x844.png
git commit -m "test: document services responsive QA"
```

### Task 7: Verificação final e deploy em GitHub Pages

**Files:**
- Verify only: `.github/workflows/static.yml`
- Verify only: all files staged by previous tasks

- [ ] **Step 1: Executar a skill de verificação antes de concluir**

Ler e seguir `superpowers:verification-before-completion`. Não afirmar que está pronto antes de executar novamente todos os comandos abaixo.

- [ ] **Step 2: Rodar testes completos relevantes**

Run:

```powershell
python -m unittest discover -s tests -p "test_*.py" -v
python scripts/build_local_preview.py
python scripts/build_local_preview.py
```

Expected: testes passam; segunda execução é no-op.

- [ ] **Step 3: Fazer auditoria do diff e do status**

Run:

```powershell
git diff --check
git status --short
git diff --stat origin/main...HEAD
git log --oneline origin/main..HEAD
```

Expected: sem whitespace errors; somente arquivos do escopo e alterações previamente aprovadas; nenhum diretório de auditoria legado, backup, `.worktrees/`, cache ou `dist_gh_pages/` rastreado por engano.

- [ ] **Step 4: Enviar a branch validada para `main`**

Como o workflow publica diretamente a raiz de `main`, executar:

```powershell
git fetch origin main
git rebase origin/main
python -m unittest discover -s tests -p "test_*.py" -v
git push origin HEAD:main
```

Se o rebase encontrar conflito ou o push não for fast-forward, parar e reportar; não usar force push.

- [ ] **Step 5: Acompanhar o deploy e validar a URL pública**

Verificar a execução `Deploy static content to Pages` até sucesso. Depois abrir:

- `https://viniciusextremxd.github.io/indafire-site/servicos/`
- `https://viniciusextremxd.github.io/indafire-site/produtos/`

Confirmar HTTP 200, assets visíveis, logo voltando à Home, mapa compartilhado, formulário comercial e os três layouts responsivos. Se o CDN ainda servir a versão anterior, aguardar a propagação e recarregar sem cache antes de concluir.

- [ ] **Step 6: Entrega ao usuário**

Informar o commit publicado, status do workflow, links públicos e caminhos dos quatro screenshots. Destacar explicitamente que catálogos, filtros e ordem de produtos não foram alterados.
