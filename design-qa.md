# Indafire — QA responsivo dos ajustes verticais (2026-08-31)

## Alvo da comparação

- Verdade visual: capturas fornecidas pelo usuário:
  - `C:/Users/Vini_/AppData/Local/Temp/codex-clipboard-4f9fc076-2895-47f8-a014-34df8aca807f.png`
  - `C:/Users/Vini_/AppData/Local/Temp/codex-clipboard-60f79fc4-1c23-40f1-a8c1-3c9c6bf97d5f.png`
  - `C:/Users/Vini_/AppData/Local/Temp/codex-clipboard-5b87ab59-6247-4dfa-95af-948e2f7656dc.png`
  - `C:/Users/Vini_/AppData/Local/Temp/codex-clipboard-c1fe6cad-292b-4971-8cdf-9cd3a56a353a.png`
- Implementação: prévia local `http://127.0.0.1:4174/`.
- Escopo: bombeiro da Brigada no retrato, escala do produto central no celular vertical, respiro do CTA de Serviços e autoplay/progresso de Serviços e Produtos.
- Restrições preservadas: sem redesign, sem troca de imagens, sem alteração do menu, do desktop ou do landscape.

## Viewports, estado e normalização

- Celular compacto: viewport CSS `375 × 812`, DPR `1`.
- Celular vertical ampliado: `683 × 830`, `691 × 768` e `700 × 900`, DPR `1`.
- Vertical intermediário: `831 × 903` e `840 × 900`, DPR `1`.
- Celular horizontal: `812 × 375`, DPR `1`.
- Desktop: `1280 × 900`, DPR `1`.
- As comparações dedicadas usam o mesmo tamanho CSS da captura de referência. O estado de conteúdo de Serviços pode variar porque o carrossel está ativo; estrutura, espaçamento e proporções foram comparados no mesmo breakpoint.

## Evidências visuais

Comparações combinadas inspecionadas:

- `audit/responsive-qa/comparison-brigada.png`
- `audit/responsive-qa/comparison-products.png`
- `audit/responsive-qa/comparison-services.png`

Capturas adicionais:

- `audit/responsive-qa/brigada-portrait-375-after.png`
- `audit/responsive-qa/products-portrait-375-after.png`
- `audit/responsive-qa/services-portrait-375-after.png`
- `audit/responsive-qa/brigada-portrait-700-after.png`
- `audit/responsive-qa/products-portrait-700-after.png`
- `audit/responsive-qa/services-portrait-700-after.png`
- `audit/responsive-qa/brigada-portrait-840-after.png`
- `audit/responsive-qa/services-portrait-840-after.png`
- `audit/responsive-qa/brigada-landscape-812-after.png`
- `audit/responsive-qa/brigada-desktop-1280-after.png`

Os recortes focados foram necessários porque os três problemas estavam em seções diferentes e os detalhes de escala, sobreposição e respiro não seriam legíveis em uma captura da página inteira.

## Superfícies de fidelidade obrigatórias

- Tipografia: família, pesos, caixa, cores, hierarquia e quebras existentes foram preservados. Não há texto cortado nos breakpoints testados.
- Espaçamento e ritmo: a Brigada vertical ganhou área inferior para separar o bombeiro do vídeo; o CTA de Serviços agora mantém `24px` livres até o limite do card; o produto central ocupa `320 × 350px` em `700px` e `282 × 350px` no telefone de `375px`, sem overflow horizontal.
- Cores e tokens: nenhum token foi alterado. As barras continuam no vermelho Indafire e os cards mantêm branco/grafite originais.
- Imagens e ativos: foram mantidos `bombeiro.jpg`, `Video-10-1.mp4`, as imagens originais de Serviços e os PNGs originais de Produtos. Nenhum ativo foi recriado ou substituído.
- Conteúdo: textos, links, ordem dos slides e destinos permanecem os mesmos.

## Responsividade e interações

- Retrato até `1100px`: o bombeiro fica ancorado embaixo, com a cabeça e o corpo visíveis abaixo do vídeo; a camada horizontal de movimento é neutralizada somente nessa orientação.
- Retrato até `767px`: a arte central de Produtos é ampliada sem alterar o carrossel ou os cards.
- Serviços: o card ativo mantém `24px` entre o fim do botão e a borda inferior, inclusive em `840 × 900`.
- Autoplay: Serviços e Produtos avançaram após `3s` com intervalo configurado em `2500ms`, mesmo com `prefers-reduced-motion: reduce`; nesse modo, a troca continua e a animação visual é reduzida.
- Navegação manual: os dois botões “próximo” mudaram o slide; Serviços também atualizou o detalhe correspondente. Apenas um detalhe permaneceu visível.
- Imagens de Serviços: `0` imagens quebradas após navegação manual e automática.
- Documento: nenhum overflow horizontal foi detectado em `375 × 812`, `700 × 900`, `840 × 900`, `812 × 375` ou `1280 × 900`.
- Console: somente o erro legado da configuração Adopt foi registrado. Nenhum novo erro dos carrosséis ou dos ajustes responsivos apareceu.

## Histórico de comparação

1. P1 — o bombeiro ficava encoberto pelo vídeo em layouts altos e estreitos.
   - Correção: altura vertical de `980px`, imagem em `44%`, posição inferior em `65% 100%` e neutralização do deslocamento horizontal somente no retrato.
   - Evidência pós-correção: `comparison-brigada.png`, `brigada-portrait-375-after.png` e `brigada-portrait-840-after.png`.
2. P2 — o produto central havia voltado a ficar pequeno no celular vertical.
   - Correção: área visual ampliada e responsiva, mantendo o PNG, setas, bullets e botão existentes.
   - Evidência pós-correção: `comparison-products.png` e `products-portrait-375-after.png`.
3. P2 — o CTA de Serviços encostava no limite inferior do card.
   - Correção: `24px` de respiro inferior no container de detalhe em retrato.
   - Evidência pós-correção: `comparison-services.png` e `services-portrait-840-after.png`.
4. P1 — os carrosséis não avançavam quando o navegador sinalizava redução de movimento.
   - Correção: o agendamento deixou de ser cancelado; Serviços e Produtos agora avançam a cada `2,5s`, enquanto a preferência continua reduzindo a animação.
   - Evidência pós-correção: ambos mudaram de item após `3s` e a sincronização de Serviços permaneceu correta.

## Achados finais

- Não restam diferenças P0, P1 ou P2 acionáveis dentro do escopo aprovado.
- P3 conhecido: o script legado Adopt ainda registra erro de configuração; ele não interfere nos componentes ajustados.

## Verificação técnica

- Regressões Python focadas: `32/32` passaram.
- Regressões JavaScript: `2/2` passaram.
- Build local executado duas vezes sem alterações na segunda execução.

final result: passed

---

# Indafire — QA de fidelidade da página Serviços (2026-09-01, revisão final)

Esta seção substitui, para `/servicos/`, as observações da rodada anterior que descreviam uma grade de cards, formulário comercial e mapa. Esses elementos não pertencem ao conteúdo principal da página original e foram removidos desta rota.

## Verdade visual e implementação

- Fonte desktop: `audit/services-origin-2026-09-01/source-services-desktop-full-1366x900.png` (`1351 × 3815` px; viewport CSS `1366 × 900`; DPR `1`; os `15px` restantes são a barra de rolagem).
- Implementação desktop: `audit/services-qa-2026-09-01/implementation-services-desktop-full-1366x900.png` (`1366 × 3944` px; viewport CSS `1366 × 900`; DPR `1`).
- Fonte celular vertical: `audit/services-origin-2026-09-01/source-services-mobile-full-390x844.png` (`375 × 5959` px; viewport CSS `390 × 844`; DPR `1`).
- Implementação celular vertical: `audit/services-qa-2026-09-01/implementation-services-mobile-full-390x844.png` (`375 × 6085` px; viewport CSS `390 × 844`; DPR `1`).
- Fonte celular horizontal: `audit/services-qa-2026-09-01/source-services-landscape-full-844x390.png` (`829 × 3898` px; viewport CSS `844 × 390`; DPR `1`).
- Implementação celular horizontal: `audit/services-qa-2026-09-01/implementation-services-landscape-full-844x390.png` (`829 × 3144` px; viewport CSS `844 × 390`; DPR `1`).
- Estado comparado: topo da rota, conteúdo completo e painéis de categoria após a ativação das animações de entrada do site de origem.
- Normalização: fonte e implementação foram capturadas no mesmo viewport e DPR; a largura útil de `15px` a menos corresponde à barra de rolagem do navegador.

## Evidência de comparação

- Vista completa desktop: `audit/services-qa-2026-09-01/comparison-services-desktop.png`.
- Vista completa celular vertical: `audit/services-qa-2026-09-01/comparison-services-mobile.png`.
- Vista completa celular horizontal: `audit/services-qa-2026-09-01/comparison-services-landscape.png`.
- Comparação focada de fotografia, ícone, painel, tipografia e lista: `audit/services-qa-2026-09-01/comparison-services-desktop-focus.png`.

O recorte focado foi necessário porque as listas e a tipografia dos painéis ficam pequenas na composição da página completa. O site de origem usa animações de entrada que deixam alguns painéis vazios em capturas full-page; as capturas em etapas foram usadas para confirmar o conteúdo visível desses painéis.

## Superfícies de fidelidade obrigatórias

- Fontes e tipografia: Open Sans, caixa alta, pesos, vermelho dos títulos, itálico do texto auxiliar e hierarquia das listas acompanham a referência.
- Espaçamento e ritmo: hero de `500px`, cinco faixas 50/50, painéis de `500px` máximos, ícones destacados, raios de `10px` e sombras equivalentes à fonte no desktop. Retrato empilha fotografia e conteúdo; horizontal preserva a composição 50/50 em escala compacta já aprovada.
- Cores e tokens: branco, cinza-claro, grafite, gradiente escuro e vermelho Indafire foram preservados; não há novos tokens decorativos no conteúdo de Serviços.
- Qualidade e fidelidade de imagens: hero, cinco fotografias e cinco ícones são ativos locais copiados do site de origem; nenhuma imagem foi recriada, esticada ou substituída por desenho em CSS/SVG artesanal.
- Conteúdo: cinco categorias e 16 destinos do conteúdo visual de referência aparecem na ordem original. Não há grade moderna, mapa, formulário comercial ou “Projeto Técnico” extra no corpo gerenciado.

## Responsividade e interações

- Desktop `1366 × 900`, vertical `390 × 844` e horizontal `844 × 390`: cinco categorias, 16 links, zero imagem quebrada e zero overflow horizontal.
- Cabeçalho, newsletter e rodapé compartilhados permanecem no acabamento moderno previamente aprovado; somente o conteúdo principal foi reconduzido à estrutura visual original.
- O logotipo continua apontando para a Home.
- O menu compacto foi aberto no horizontal, permaneceu visível por `3,2s` e manteve `aria-expanded="true"`, modal `display:flex` e estado de corpo aberto, sem fechamento espontâneo.

## Histórico de comparação e correções

1. P1 — a primeira implementação usava uma grade moderna de cards, diferente das cinco faixas alternadas do original.
   - Correção: reconstrução do conteúdo principal com hero e cinco linhas 50/50, fotografias, ícones, textos e links originais.
   - Evidência pós-correção: as três comparações completas e o recorte focado listados acima.
2. P1 — o build geral reinjetava o mapa e exigia o formulário comercial de Produtos na rota de Serviços.
   - Correção: `/servicos/` foi removido dos alvos de sincronização do mapa e o gerador passou a remover integralmente a seção legada de localização.
   - Evidência pós-correção: DOM renderizado com `5` linhas, `16` links, `0` mapas e `0` formulários; segundo build sem alterações.

## Achados finais

- Não restam diferenças P0, P1 ou P2 acionáveis no conteúdo principal de Serviços.
- P3/aceito: o cabeçalho, newsletter e rodapé têm o polimento moderno já aprovado e, por decisão anterior do projeto, não reproduzem literalmente os estilos legados da referência.

## Verificação técnica

- Suíte rastreada completa do site: `68/68` testes passaram na rodada final.
- Build local executado duas vezes; a segunda execução foi no-op.

final result: passed

---

# Indafire — QA visual de Produtos e Serviços (2026-09-01)

## Escopo validado

- Nova rota estática `/servicos/`, seguindo o acabamento aprovado em `/produtos/` e preservando a identidade do site original.
- Mapa de `/produtos/` sincronizado com a seção completa da Home.
- Logos do cabeçalho e rodapé retornando para a Home conforme a profundidade da rota.
- Catálogos e ordem dos produtos preservados.

## Comparação visual

- Referência e implementação no mesmo viewport desktop: `screenshots/services-comparison-desktop-1366x900.png`.
- Referência original isolada: `screenshots/source-servicos-desktop-1366x900.png`.
- Implementação desktop: `screenshots/services-desktop-1366x900.png`.
- Implementação celular vertical: `screenshots/services-mobile-portrait-390x844.png`.
- Implementação celular horizontal: `screenshots/services-mobile-landscape-844x390.png`.
- Mapa de Produtos carregado no celular vertical: `screenshots/products-map-mobile-portrait-390x844.png`.

## Resultados por viewport

- Desktop `1366 × 900`: hero, header pill, introdução, cards e primeira dobra sem recortes ou overflow horizontal.
- Celular vertical `390 × 844`: 17 cards em coluna única, formulário e mapa presentes, menu gaveta abre e permanece aberto, sem imagens quebradas e sem overflow horizontal.
- Celular horizontal `844 × 390`: introdução em duas colunas e cards em três colunas compactas, sem sobreposição ou overflow horizontal.
- Cabeçalho responsivo: some ao rolar para baixo e reaparece ao rolar para cima nos breakpoints compactos.
- Mapa de Produtos: iframe, endereço e CTA são o mesmo fragmento gerenciado usado pela Home.

## Ativos, conteúdo e interações

- As quatro fotografias de Serviços são cópias binárias dos ativos publicados no site original; os hashes são verificados por teste.
- Todos os 17 serviços mantêm destinos reais do site original; Brigada de Incêndio aponta para Treinamentos.
- O formulário comercial gera a mensagem do WhatsApp localmente e não foi submetido durante o QA.
- O menu móvel foi mantido aberto por 3,5 segundos durante o teste, sem o fechamento espontâneo relatado anteriormente.
- O único erro de console observado é o legado da configuração Adopt; nenhum erro novo de Serviços, mapa ou navegação foi registrado.

## Verificação técnica

- Testes rastreados do site: `67/67` passaram.
- Build local executado duas vezes: ambas com código `0`; a segunda execução foi no-op.
- A descoberta global também executou testes operacionais não rastreados e encontrou 2 erros por ausência de `scripts.build_baseline_factual_1`, igualmente não rastreado e fora do escopo do site estático.

final result: passed

---

# Indafire — QA de Localização Móvel e Formulários de Rodapé (2026-09-04)

## Escopo validado (Ajuste Focado e Estrito)

- **Localização Mobile**: Remoção definitiva da seção duplicada de localização em `/servicos/` (gerada anteriormente por resquício da casca herdada e injeção redundante), garantindo que Serviços exiba 0 seções duplicadas e Produtos exiba exatamente 1 seção sincronizada com a Home.
- **Formulários de Rodapé (`#formulariosRodape`)**:
  - Padronização do placeholder do campo de nome (`placeholder="Nome"` em português).
  - Padronização do botão de envio do catálogo ("Receber material").
  - Substituição dos seletores de consentimento de privacidade de `type="radio"` (que não podiam ser desselecionados) por `type="checkbox"` acessíveis e nativos.
  - Estilos responsivos aplicados universalmente em `inject_internal_page_polish.py` para visualização mobile vertical (`390 × 844`), mobile horizontal (`844 × 390`) e desktop (`1440 × 900`), garantindo alinhamento e consistência sem tocar no cabeçalho ou demais blocos da página.

## Resultados
- Celular vertical (`390 × 844`): Cards de newsletter e catálogo com margens equilibradas, inputs padronizados, checkboxes funcionais e sem overflow horizontal.
- Celular horizontal (`844 × 390`): Cards lado a lado compactos e alinhados.
- Desktop (`1440 × 900`): Layout de duas colunas perfeitamente simétrico com alturas padronizadas e elevação suave.
- Zero impacto regressivo no cabeçalho, menu móvel ou cards de conteúdo.

final result: passed

