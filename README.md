# Indafire — prévia estática

Esta cópia de trabalho é uma réplica estática do site Indafire. O polimento
visual preserva o sistema existente e é aplicado diretamente aos documentos
HTML exportados.

## Build e prévia local

```powershell
python scripts/build_local_preview.py
python -m http.server 4173 --directory .
```

Abra `http://127.0.0.1:4173/`. O build é idempotente e valida as camadas de
polimento compartilhada e do catálogo; ele também repõe apenas os assets de
hero originais que as páginas estáticas já referenciam.

As páginas principais a validar são:

- `/`
- `/produtos/`
- `/servicos/`
- `/categoria-produto/extintores/`
- `/produto/unidade-central-lux-700-1200-24vdc/`
- `/produto/extintor-pqs-bc-4-kg-20bc/`
- `/sobre-nos/`
- `/treinamentos/`
- `/contato/`
- `/area-do-cliente/`
- `/politica-de-privacidade/`

## Validação

```powershell
python -m unittest tests/test_build_local_preview.py tests/test_build_services_page.py tests/test_sync_shared_location.py tests/test_services_assets.py tests/test_inject_product_catalog_polish.py tests/test_inject_internal_page_polish.py tests/test_static_hero_assets.py
```

## Publicação

`dist_gh_pages/` é um artefato legado e o exportador histórico depende de um
WordPress local em `localhost:8080`. A prévia acima não altera essa pasta. O
workflow `.github/workflows/static.yml` publica diretamente a raiz da branch
`main`; o push deve acontecer somente após a validação visual da versão
estática.
