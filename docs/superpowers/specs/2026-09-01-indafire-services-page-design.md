# Indafire — Página de Serviços e consistência das páginas internas

## Objetivo

Criar a rota estática `/servicos/` com a linguagem visual modernizada já aprovada na Home e em `/produtos/`, mantendo fidelidade ao conteúdo e aos ativos do site original. O mesmo pacote corrige o mapa da página de Produtos para usar exatamente o componente da Home e garante que a logo do cabeçalho sempre leve à página inicial.

## Escopo

### Página de Produtos

- Preservar integralmente catálogo, ordem dos produtos, busca, filtros, formulário comercial, newsletter e rodapé.
- Substituir somente a seção `#localizacao_mapa` pelo mesmo markup e pelas mesmas classes usadas na Home: texto e CTA à esquerda, mapa em card à direita.
- Reutilizar a camada de CSS já existente da Home para que os três breakpoints tenham o mesmo comportamento.

### Navegação pela logo

- Normalizar o link da logo principal e da logo do rodapé em todas as rotas estáticas.
- A página inicial usa `./`; páginas de primeiro nível usam `../`; páginas de segundo nível usam `../../`.
- A correção será aplicada pelo script mestre de navegação, evitando edições manuais divergentes.

### Nova página `/servicos/`

A página terá esta sequência:

1. Cabeçalho responsivo existente, incluindo ocultação ao rolar para baixo e reaparecimento ao rolar para cima.
2. Hero com a fotografia original `servicos.jpg`, overlay escuro e título “SERVIÇOS”.
3. Introdução de Engenharia e Consultoria com a fotografia original de projeto/consultoria e a composição grafite, branca e vermelha observada no site original.
4. Grupos e serviços confirmados no HTML original, mesmo quando o carregamento legado deixa os cards visualmente vazios:
   - Engenharia e Consultoria: AVCB/CLCB — Obtenção ou renovação; Processo simplificado (PTS); Projeto Técnico.
   - Manutenções e Inspeções: Inspeção de Equipamentos; Instalação e venda de extintores; Recarga de Extintores; Teste Hidrostático em Mangueiras de Incêndios.
   - Sistemas de Prevenção e Combate a Incêndio: Sinalização de Emergência; Sistema de alarme de incêndio; Sistema de detecção de fumaça e calor; Sistema de Hidrantes; Sistema de iluminação de emergência; Sistemas de Sprinklers.
   - Treinamentos: Brigada de Incêndio.
   - Serviços Especiais: Equipe habilitada para eventos ou trabalhos específicos; Fabricação de caixa d’água metálica; Locação de equipamentos.
5. Cada card usará fotografia original, título e link para a rota original correspondente. Links sem export estático local poderão continuar apontando para a rota real do domínio original; não serão criadas páginas fictícias.
6. Formulário comercial de WhatsApp no mesmo padrão de `/produtos/`, com assunto previamente orientado a Serviços.
7. Mapa idêntico ao da Home.
8. Newsletter, catálogo e rodapé já existentes, sem mudanças de conteúdo.

## Responsividade

- Desktop: introdução em duas colunas e cada grupo de serviços em até três cards por linha.
- Celular vertical: fluxo em uma coluna, cards com imagens sem corte e formulário empilhado.
- Celular horizontal: introdução e formulário em duas colunas compactas; cards em três colunas quando houver espaço útil e duas colunas quando necessário.
- Nenhum breakpoint poderá gerar overflow horizontal, sobreposição do cabeçalho ou corte dos CTAs.

## Arquitetura e pipeline

- A nova rota será gerada por um script mestre dedicado e idempotente, sem edição manual permanente do HTML gerado.
- `scripts/build_local_preview.py` passará a gerar e validar `/servicos/index.html`.
- O injetor de navegação continuará sendo a fonte da normalização dos links da logo.
- O componente de localização será mantido como fragmento compartilhado entre Home, Produtos e Serviços para evitar divergência visual futura.
- A exportação/deploy incluirá explicitamente `/servicos/` e somente ativos locais já pertencentes ao site original.

## Interações e falhas

- O formulário usa validação HTML nativa e abre uma mensagem pré-preenchida para o WhatsApp comercial existente.
- Links de serviço serão preservados apenas quando houver destino real; não haverá rotas ou respostas simuladas.
- Imagens usarão `object-fit: contain` ou `cover` conforme a composição original, com fallback visual neutro caso um ativo não carregue.
- O mapa manterá o link externo “Traçar rota no Google Maps” e o iframe existente.

## Testes e validação

- Testes unitários primeiro para geração idempotente da página, ordem das seções, mapa compartilhado e normalização da logo.
- Build executado duas vezes; a segunda execução deve informar zero alterações.
- Validação visual comparativa nos viewports desktop, 390×844 e 844×390.
- Verificação dos links principais, formulário, mapa, ausência de overflow e erros novos no console.
- Deploy para `main`/GitHub Pages somente após testes e design QA aprovados.

## Fora de escopo

- Alterar produtos, categorias, descrições ou ordem do catálogo.
- Criar páginas detalhadas novas para serviços que não existem no export.
- Redesenhar Home, Produtos, newsletter, rodapé ou menu.
- Trocar fotografias originais por imagens geradas ou de terceiros.
