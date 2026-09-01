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
