/**
 * INDA FIRE — CATALOG & SERVICES DATA REPOSITORY
 * Base de Dados Completa e Homologada de Produtos e Serviços
 */

export const PRODUCT_CATEGORIES = [
  { id: 'todos', name: 'Todos os Produtos', icon: 'grid', count: 48 },
  { id: 'extintores', name: 'Extintores', icon: 'fire-extinguisher', count: 8 },
  { id: 'mangueiras', name: 'Mangueiras', icon: 'circle-dot', count: 6 },
  { id: 'abrigos', name: 'Abrigos e Caixas', icon: 'box', count: 4 },
  { id: 'hidrantes', name: 'Hidrantes e Válvulas', icon: 'faucet', count: 5 },
  { id: 'sinalizacoes', name: 'Sinalizações', icon: 'triangle-alert', count: 5 },
  { id: 'alarmes-de-incendio', name: 'Alarmes e Detecção', icon: 'bell', count: 5 },
  { id: 'iluminacoes-de-emergencia', name: 'Iluminação de Emergência', icon: 'sun', count: 4 },
  { id: 'acessorios', name: 'Acessórios e Suportes', icon: 'wrench', count: 4 },
  { id: 'epi', name: 'EPI (Proteção Individual)', icon: 'hard-hat', count: 4 },
  { id: 'epr', name: 'EPR (Proteção Respiratória)', icon: 'shield', count: 2 },
  { id: 'aph', name: 'APH (Primeiros Socorros)', icon: 'heart-pulse', count: 3 },
  { id: 'epc', name: 'EPC (Proteção Coletiva)', icon: 'building-shield', count: 2 },
  { id: 'resgate-em-altura', name: 'Resgate em Altura', icon: 'link', count: 2 },
  { id: 'incendio-florestal', name: 'Incêndio Florestal', icon: 'tree-pine', count: 2 }
];

export const PRODUCTS = [
  // EXTINTORES
  {
    id: 'extintor-po-abc-6kg',
    name: 'Extintor Pó Químico ABC 6kg',
    category: 'extintores',
    categoryLabel: 'Extintores',
    badge: 'HOMOLOGADO INMETRO',
    shortDesc: 'Extintor portátil de pressurização direta para classes A (sólidos), B (líquidos inflamáveis) e C (equipamentos elétricos).',
    image: 'images/products_original/extintor-pqs-bc-4-kg-20bc.png',
    specs: {
      capacidade: '6 kg',
      agente: 'Fosfato Monoamônico 55%',
      capacidadeExtintora: '3-A:40-B:C',
      pressurizacao: 'Direta (Nitrogênio N2)',
      pesoTotal: '9,8 kg',
      alcanceJato: '4 a 6 metros',
      tempoDescarga: '15 a 20 segundos',
      norma: 'NBR 15808 / Portaria Inmetro nº 002874'
    },
    compliance: ['NBR 15808', 'Inmetro 002874', 'Garantia 1 Ano'],
    recommendedFor: 'Indústrias, comércios, galpões logísticos e edifícios corporativos.'
  },
  {
    id: 'extintor-co2-6kg',
    name: 'Extintor Gás Carbônico CO₂ 6kg',
    category: 'extintores',
    categoryLabel: 'Extintores',
    badge: 'ALTA EFICIÊNCIA ELÉTRICA',
    shortDesc: 'Extintor de CO₂ com difusor dielétrico para combate a incêndios classe B e C sem deixar resíduos.',
    image: 'images/products_original/extintores-linha-completa.jpg',
    specs: {
      capacidade: '6 kg',
      agente: 'Dióxido de Carbono (CO₂ puro)',
      capacidadeExtintora: '5-B:C',
      pressurizacao: 'Auto-pressurizado',
      cilindro: 'Aço sem costura SAE 4130',
      pesoTotal: '17,5 kg',
      norma: 'NBR 15808 / Certificação Inmetro'
    },
    compliance: ['NBR 15808', 'Sem Resíduos', 'Não Conduz Eletricidade'],
    recommendedFor: 'Salas de CPD, servidores, painéis elétricos e laboratórios.'
  },
  {
    id: 'extintor-agua-pressurizada-10l',
    name: 'Extintor Água Pressurizada 10 Litros',
    category: 'extintores',
    categoryLabel: 'Extintores',
    badge: 'MÁXIMO RESFRIAMENTO',
    shortDesc: 'Extintor de água pressurizada com bico esguicho para materiais sólidos combustíveis Classe A.',
    image: 'images/products_original/extintor-pqs-bc-4-kg-20bc.png',
    specs: {
      capacidade: '10 Litros',
      agente: 'Água Potável + Inibidor de Corrosão',
      capacidadeExtintora: '2-A',
      pressurizacao: 'Direta (Nitrogênio N2)',
      pesoTotal: '13,5 kg',
      norma: 'NBR 15808'
    },
    compliance: ['NBR 15808', 'Classe A Especial', 'Inmetro Compulsório'],
    recommendedFor: 'Madeireiras, indústrias de papel e celulose, estoques e tecelagens.'
  },
  {
    id: 'extintor-po-bc-4kg',
    name: 'Extintor Pó Químico BC 4kg',
    category: 'extintores',
    categoryLabel: 'Extintores',
    badge: 'HOMOLOGADO ABNT',
    shortDesc: 'Extintor pressurizado de Bicarbonato de Sódio para líquidos combustíveis e sistemas elétricos.',
    image: 'images/products_original/extintor-pqs-bc-4-kg-20bc.png',
    specs: {
      capacidade: '4 kg',
      agente: 'Bicarbonato de Sódio 95%',
      capacidadeExtintora: '20-B:C',
      pressurizacao: 'Direta',
      norma: 'NBR 15808'
    },
    compliance: ['NBR 15808', 'Classe BC', 'Inmetro'],
    recommendedFor: 'Oficinas, postos de combustíveis e depósitos de tintas.'
  },
  {
    id: 'carreta-po-abc-50kg',
    name: 'Carreta Sobre Rodas Pó ABC 50kg',
    category: 'extintores',
    categoryLabel: 'Extintores',
    badge: 'CAPACIDADE INDUSTRIAL',
    shortDesc: 'Unidade móvel sobre rodas para combate intensivo em grandes plantas industriais e refinarias.',
    image: 'images/products_original/extintor-pqs-bc-4-kg-20bc.png',
    specs: {
      capacidade: '50 kg',
      agente: 'Fosfato Monoamônico 55%',
      capacidadeExtintora: '10-A:80-B:C',
      pressurizacao: 'Ampola Externa de N2',
      mangueira: '5 metros com pistola dosadora',
      norma: 'NBR 15809'
    },
    compliance: ['NBR 15809', 'Grande Porte', 'Alta Vazão'],
    recommendedFor: 'Subestações elétricas, pátios de tanques e hangares.'
  },
  {
    id: 'carreta-co2-25kg',
    name: 'Carreta Sobre Rodas CO₂ 25kg',
    category: 'extintores',
    categoryLabel: 'Extintores',
    badge: 'SISTEMA PESADO CO₂',
    shortDesc: 'Carreta sobre rodas com cilindro de CO₂ e mangueira de alta pressão para grandes áreas elétricas.',
    image: 'images/products_original/extintores-linha-completa.jpg',
    specs: {
      capacidade: '25 kg',
      agente: 'Dióxido de Carbono (CO₂)',
      capacidadeExtintora: '10-B:C',
      norma: 'NBR 15809'
    },
    compliance: ['NBR 15809', 'Zero Resíduos', 'Uso Industrial'],
    recommendedFor: 'Grandes indústrias petroquímicas e centros de distribuição de energia.'
  },
  {
    id: 'extintor-espuma-mecanica-10l',
    name: 'Extintor Espuma Mecânica 10 Litros',
    category: 'extintores',
    categoryLabel: 'Extintores',
    badge: 'ABAFAMENTO E RESFRIAMENTO',
    shortDesc: 'Extintor com líquido gerador de espuma (LGE) de alta eficácia para solventes e hidrocarbonetos.',
    image: 'images/products_original/extintor-pqs-bc-4-kg-20bc.png',
    specs: {
      capacidade: '10 Litros',
      agente: 'Água + LGE 6%',
      capacidadeExtintora: '2-A:10-B',
      norma: 'NBR 15808'
    },
    compliance: ['NBR 15808', 'Formador de Filme', 'Inmetro'],
    recommendedFor: 'Armazéns de combustíveis, indústrias químicas e oficinas mecânicas.'
  },
  {
    id: 'extintor-k-kitchen-6l',
    name: 'Extintor Classe K Cozinhas Industriais 6L',
    category: 'extintores',
    categoryLabel: 'Extintores',
    badge: 'CLASSE K ESPECIAL',
    shortDesc: 'Extintor com acetato de potássio para combate a incêndios em óleos vegetais e gorduras em alta temperatura.',
    image: 'images/products_original/extintor-pqs-bc-4-kg-20bc.png',
    specs: {
      capacidade: '6 Litros',
      agente: 'Solução Aquosa de Acetato de Potássio',
      capacidadeExtintora: '1-A:K',
      norma: 'NBR 15808 / NFPA 10'
    },
    compliance: ['NBR 15808', 'NFPA 10', 'Específico para Cozinhas'],
    recommendedFor: 'Cozinhas industriais, restaurantes corporativos e redes hoteleiras.'
  },

  // MANGUEIRAS
  {
    id: 'mangueira-tipo-1-predial',
    name: 'Mangueira de Incêndio Tipo 1 Predial 15m/30m',
    category: 'mangueiras',
    categoryLabel: 'Mangueiras',
    badge: 'HOMOLOGADA NBR 11861',
    shortDesc: 'Mangueira com reforço têxtil em fio de poliéster e tubo interno de borracha sintética para edifícios residenciais.',
    image: 'images/products_original/mangueira-tipo-i-predial.png',
    specs: {
      diametro: '1.1/2" (38mm)',
      comprimento: '15m ou 30m',
      pressaoTrabalho: '10 kgf/cm² (980 kPa)',
      pressaoRuptura: 'Acima de 35 kgf/cm²',
      unioes: 'Engate Rápido Storz em Latão NBR 14349',
      norma: 'NBR 11861 Tipo 1'
    },
    compliance: ['NBR 11861', 'Certificado ABNT', 'União Storz'],
    recommendedFor: 'Prédios residenciais e condomínios.'
  },
  {
    id: 'mangueira-tipo-2-comercial-industrial',
    name: 'Mangueira de Incêndio Tipo 2 Comercial 15m/30m',
    category: 'mangueiras',
    categoryLabel: 'Mangueiras',
    badge: 'ALTA RESISTÊNCIA',
    shortDesc: 'Mangueira reforçada para edifícios comerciais, indústrias médias e depósitos de mercadorias.',
    image: 'images/products_original/mangueira-tipo-i-predial.png',
    specs: {
      diametro: '1.1/2" (38mm) ou 2.1/2" (65mm)',
      pressaoTrabalho: '14 kgf/cm² (1.370 kPa)',
      pressaoRuptura: 'Acima de 42 kgf/cm²',
      norma: 'NBR 11861 Tipo 2'
    },
    compliance: ['NBR 11861 Tipo 2', 'ABNT', 'Alta Abrasão'],
    recommendedFor: 'Shopping centers, galpões logísticos e indústrias.'
  },
  {
    id: 'mangueira-tipo-3-naval-florestal',
    name: 'Mangueira de Incêndio Tipo 3 Capa Dupla',
    category: 'mangueiras',
    categoryLabel: 'Mangueiras',
    badge: 'CAPA DUPLA REFORÇADA',
    shortDesc: 'Mangueira com dupla capa têxtil para máxima durabilidade contra abrasão extrema e superfícies pontiagudas.',
    image: 'images/products_original/mangueira-tipo-i-predial.png',
    specs: {
      diametro: '1.1/2" e 2.1/2"',
      pressaoTrabalho: '15 kgf/cm²',
      norma: 'NBR 11861 Tipo 3'
    },
    compliance: ['NBR 11861 Tipo 3', 'Dupla Capa', 'Naval / Bombeiros'],
    recommendedFor: 'Corpo de bombeiros, estaleiros, portos e combate florestal.'
  },
  {
    id: 'mangueira-tipo-4-plastificada',
    name: 'Mangueira Tipo 4 Revestida de Borracha Nitrílica',
    category: 'mangueiras',
    categoryLabel: 'Mangueiras',
    badge: 'RESISTÊNCIA QUÍMICA',
    shortDesc: 'Mangueira plastificada em vermelho com altíssima resistência a óleos, derivados de petróleo e ácidos.',
    image: 'images/products_original/mangueira-tipo-i-predial.png',
    specs: {
      revestimento: 'Polímero Nitrílico Especial',
      pressaoTrabalho: '14 kgf/cm²',
      norma: 'NBR 11861 Tipo 4'
    },
    compliance: ['NBR 11861 Tipo 4', 'Resistente a Óleos', 'Lavável'],
    recommendedFor: 'Refinarias, usinas de açúcar/álcool e indústrias químicas.'
  },
  {
    id: 'esguicho-regulavel-neblina',
    name: 'Esguicho Regulável Tipo Neblina Storz',
    category: 'mangueiras',
    categoryLabel: 'Mangueiras',
    badge: 'LATÃO FORJADO',
    shortDesc: 'Esguicho com regulagem contínua para jato sólido, neblina e fechamento estanque rápido.',
    image: 'images/products_original/valvula-globo-angular-hidrante.png',
    specs: {
      diametro: '1.1/2" e 2.1/2"',
      material: 'Latão Forjado com Anel de Proteção em Borracha',
      norma: 'NBR 14349'
    },
    compliance: ['NBR 14349', 'Jato Regulável', 'Engate Storz'],
    recommendedFor: 'Uso conjunto em caixas de hidrante e linhas de mangueira.'
  },
  {
    id: 'chave-storz-dupla',
    name: 'Chave Storz Dupla para Conexões de Incêndio',
    category: 'mangueiras',
    categoryLabel: 'Mangueiras',
    badge: 'FERRAMENTA PADRÃO',
    shortDesc: 'Chave dupla forjada em latão ou alumínio fundido para acoplamento e desacoplamento de uniões Storz.',
    image: 'images/products_original/valvula-globo-angular-hidrante.png',
    specs: {
      compatibilidade: 'Uniões Storz 1.1/2" e 2.1/2"',
      material: 'Latão / Alumínio',
      norma: 'NBR 14349'
    },
    compliance: ['NBR 14349', 'Alta Resistência'],
    recommendedFor: 'Obrigatória em todos os abrigos de hidrante.'
  },

  // ABRIGOS E CAIXAS
  {
    id: 'abrigo-hidrante-embutir',
    name: 'Abrigo para Hidrante de Embutir 90x60x17cm',
    category: 'abrigos',
    categoryLabel: 'Abrigos e Caixas',
    badge: 'AÇO CARBONO / PINTURA EPÓXI',
    shortDesc: 'Caixa de hidrante para embutir em alvenaria com porta veneziana, visor de acrílico e pintura vermelho fogo.',
    image: 'images/products_original/abrigo-para-extintor-fibra.png',
    specs: {
      dimensoes: '90 x 60 x 17 cm (ou 120 x 90 x 17 cm)',
      material: 'Chapa de Aço Carbono #20',
      acabamento: 'Pintura Eletrostática a Pó Epóxi UV',
      capacidade: '2 mangueiras de 15m + esguicho + chave',
      norma: 'NBR 13714'
    },
    compliance: ['NBR 13714', 'Pintura Eletrostática', 'Visor Acrílico'],
    recommendedFor: 'Edificações comerciais, condomínios e hospitais.'
  },
  {
    id: 'abrigo-hidrante-sobrepor-inox',
    name: 'Abrigo para Hidrante Sobrepor Aço Inox 304',
    category: 'abrigos',
    categoryLabel: 'Abrigos e Caixas',
    badge: 'INOX ESCOVADO',
    shortDesc: 'Abrigo em aço inoxidável para instalação externa ou ambientes de alto padrão arquitetônico e maresia.',
    image: 'images/products_original/abrigo-para-extintor-fibra.png',
    specs: {
      material: 'Aço Inoxidável AISI 304 Escovado',
      dimensoes: '90 x 60 x 17 cm',
      norma: 'NBR 13714'
    },
    compliance: ['AISI 304', 'Anti-corrosão', 'Design Premium'],
    recommendedFor: 'Hotéis, sedes corporativas, indústrias farmacêuticas e áreas litorâneas.'
  },
  {
    id: 'abrigo-extintor-fibra-vidro',
    name: 'Abrigo para Extintor em Fibra de Vidro (PRFV)',
    category: 'abrigos',
    categoryLabel: 'Abrigos e Caixas',
    badge: '100% IMPERMEÁVEL',
    shortDesc: 'Caixa protetora em plástico reforçado com fibra de vidro com fecho de engate rápido e proteção contra raios solares.',
    image: 'images/products_original/abrigo-para-extintor-fibra.png',
    specs: {
      material: 'Compósito PRFV com Resina Isoftálica',
      protecao: 'IP66 contra poeira e intempéries',
      capacidade: '1 extintor portátil até 12kg'
    },
    compliance: ['Imune à Corrosão', 'Proteção UV', 'Grau Industrial'],
    recommendedFor: 'Pátios externos, plataformas offshore e indústrias químicas.'
  },
  {
    id: 'armario-corta-fogo',
    name: 'Armário Corta-Fogo para Inflamáveis',
    category: 'abrigos',
    categoryLabel: 'Abrigos e Caixas',
    badge: 'PROTEÇÃO TÉRMICA CONTÍNUA',
    shortDesc: 'Armário técnico para armazenamento seguro de solventes, combustíveis e tintas com isolamento duplo.',
    image: 'images/products_original/abrigo-para-extintor-fibra.png',
    specs: {
      construcao: 'Chapas de aço carbono duplas com isolamento térmico mineral',
      resistenciaFogo: 'Resistente a chamas diretas conforme NFPA 30',
      fechamento: 'Trancamento em 3 pontos com chave',
      norma: 'NFPA 30 / ABNT NBR 17505'
    },
    compliance: ['NFPA 30', 'NBR 17505', 'Dique de Contenção'],
    recommendedFor: 'Laboratórios, oficinas mecânicas e almoxarifados de produtos químicos.'
  },

  // HIDRANTES E VÁLVULAS
  {
    id: 'valvula-globo-angular-45',
    name: 'Válvula Globo Angular 45° Latão 2.1/2"',
    category: 'hidrantes',
    categoryLabel: 'Hidrantes e Válvulas',
    badge: 'LATÃO PESADO',
    shortDesc: 'Registro de hidrante para bloqueio e liberação de fluxo de água com conexão de entrada rosca BSP e saída Storz.',
    image: 'images/products_original/valvula-globo-angular-hidrante.png',
    specs: {
      diametroEntrada: '2.1/2" Rosca Fêmea BSP (11 FPP)',
      diametroSaida: '2.1/2" Macho ou Storz',
      pressaoTrabalho: 'PN 16 (16 bar)',
      material: 'Bronze / Latão Fundido de Alta Resistência',
      norma: 'NBR 13714 / NBR 16021'
    },
    compliance: ['NBR 13714', 'NBR 16021', 'Pressão PN16'],
    recommendedFor: 'Pontos de hidrante prediais e industriais.'
  },
  {
    id: 'adaptador-storz-latão',
    name: 'Adaptador Storz em Latão com Rosca Macho/Fêmea',
    category: 'hidrantes',
    categoryLabel: 'Hidrantes e Válvulas',
    badge: 'CONEXÃO INSTANTÂNEA',
    shortDesc: 'Adaptador com engate rápido tipo Storz para acoplamento das mangueiras nos registros de hidrante.',
    image: 'images/products_original/valvula-globo-angular-hidrante.png',
    specs: {
      bitolas: '1.1/2" x 1.1/2", 2.1/2" x 1.1/2" e 2.1/2" x 2.1/2"',
      material: 'Latão Forjado',
      norma: 'NBR 14349'
    },
    compliance: ['NBR 14349', 'Latão Forjado'],
    recommendedFor: 'Conexão em válvulas de hidrante e colunas de recalque.'
  },
  {
    id: 'tampao-storz-com-corrente',
    name: 'Tampão Cego Storz com Corrente de Retenção',
    category: 'hidrantes',
    categoryLabel: 'Hidrantes e Válvulas',
    badge: 'PROTEÇÃO DE LINHA',
    shortDesc: 'Tampão de vedação para proteger as saídas de hidrante e registros de recalque contra sujeira e vandalismo.',
    image: 'images/products_original/valvula-globo-angular-hidrante.png',
    specs: {
      bitolas: '1.1/2" e 2.1/2"',
      guarnicao: 'Borracha de Vedação NBR',
      corrente: 'Aço Galvanizado 30cm',
      norma: 'NBR 14349'
    },
    compliance: ['NBR 14349', 'Vedação Estanque'],
    recommendedFor: 'Hidrantes de parede e registros de recalque de calçada.'
  },
  {
    id: 'registro-recalque-passeio',
    name: 'Registro de Recalque de Passeio / Calçada',
    category: 'hidrantes',
    categoryLabel: 'Hidrantes e Válvulas',
    badge: 'PADRÃO CORPO DE BOMBEIROS',
    shortDesc: 'Válvula de recalque para conexão dos caminhões do Corpo de Bombeiros na calçada para pressurização da rede predial.',
    image: 'images/products_original/valvula-globo-angular-hidrante.png',
    specs: {
      diametro: '2.1/2"',
      material: 'Bronze Naval',
      tampa: 'Em ferro fundido com gravação "INCÊNDIO"',
      norma: 'NBR 13714 / IT-22'
    },
    compliance: ['IT-22 Bombeiros', 'NBR 13714', 'Uso Externo'],
    recommendedFor: 'Entrada de condomínios residenciais e centros comerciais.'
  },
  {
    id: 'coluna-hidrante-industrial',
    name: 'Coluna de Hidrante Duplo Industrial em Aço',
    category: 'hidrantes',
    categoryLabel: 'Hidrantes e Válvulas',
    badge: 'DUPLA EXPEDIÇÃO',
    shortDesc: 'Coluna de hidrante para pátios externos com duas saídas de 2.1/2" com válvulas independentes.',
    image: 'images/products_original/valvula-globo-angular-hidrante.png',
    specs: {
      diametroTubo: '4" (100mm)',
      saidas: '2 x 2.1/2" com adaptadores Storz',
      pressaoTrabalho: '20 kgf/cm²',
      norma: 'NBR 13714'
    },
    compliance: ['NBR 13714', 'Pátio Fabril', 'Alta Resistência'],
    recommendedFor: 'Pátios de manobra, depósitos a céu aberto e indústrias pesadas.'
  },

  // SINALIZAÇÕES
  {
    id: 'placa-extintor-e5',
    name: 'Placa Fotoluminescente Extintor E5',
    category: 'sinalizacoes',
    categoryLabel: 'Sinalizações',
    badge: 'NBR 13434 FOTOLUMINESCENTE',
    shortDesc: 'Placa sinalizadora de extintor de incêndio com alta luminescência residual em conformidade com as normas estaduais.',
    image: 'images/products_original/placa-extintor-e5-nbr.png',
    specs: {
      dimensoes: '15 x 15 cm ou 20 x 20 cm',
      material: 'PVC Anti-chamas com pigmento fotoluminescente',
      autonomiaBrilho: 'Até 30 horas no escuro total',
      norma: 'NBR 13434 / IT-20'
    },
    compliance: ['NBR 13434', 'IT-20 Bombeiros', 'Auto-extinguível'],
    recommendedFor: 'Obrigatória em todos os pontos de extintor.'
  },
  {
    id: 'placa-saida-emergencia',
    name: 'Placa Saída de Emergência com Seta Fotoluminescente',
    category: 'sinalizacoes',
    categoryLabel: 'Sinalizações',
    badge: 'ROTA DE FUGA CERTIFICADA',
    shortDesc: 'Placa de orientação de rota de fuga verde e branca com indicação de direção e porta de saída.',
    image: 'images/products_original/placa-extintor-e5-nbr.png',
    specs: {
      dimensoes: '30 x 15 cm ou 24 x 12 cm',
      material: 'PVC Rígido 2mm',
      norma: 'NBR 13434-2'
    },
    compliance: ['NBR 13434', 'Sinalização de Rota', 'Alta Visibilidade'],
    recommendedFor: 'Corredores, escadarias e portas corta-fogo.'
  },
  {
    id: 'demarcacao-piso-extintor',
    name: 'Demarcação de Piso para Extintor Vermelho/Amarelo',
    category: 'sinalizacoes',
    categoryLabel: 'Sinalizações',
    badge: 'ADESIVO INDUSTRIAL ALTA ADERÊNCIA',
    shortDesc: 'Pintura e adesivo antiderrapante de 1m x 1m para garantir que a área em frente ao extintor não seja obstruída.',
    image: 'images/products_original/placa-extintor-e5-nbr.png',
    specs: {
      dimensoes: '100 x 100 cm com borda amarela de 15 cm',
      material: 'Vinil adesivo de tráfego pesado com laminação UV',
      norma: 'IT-20 Corpo de Bombeiros'
    },
    compliance: ['IT-20 Bombeiros', 'Anti-obstrução', 'Antiderrapante'],
    recommendedFor: 'Chão de fábrica, galpões logísticos e garagens.'
  },
  {
    id: 'placa-alarme-botoeira',
    name: 'Placa de Identificação de Botoeira de Alarme',
    category: 'sinalizacoes',
    categoryLabel: 'Sinalizações',
    badge: 'NBR 13434',
    shortDesc: 'Sinalização fotoluminescente indicativa de acionador manual de alarme de incêndio e bomba.',
    image: 'images/products_original/placa-extintor-e5-nbr.png',
    specs: {
      dimensoes: '15 x 15 cm',
      material: 'PVC Fotoluminescente 2mm'
    },
    compliance: ['NBR 13434', 'Brilho > 140 mcd/m²'],
    recommendedFor: 'Instalação acima dos acionadores manuais de alarme.'
  },
  {
    id: 'placa-proibido-fumar',
    name: 'Placa de Proibição "Proibido Fumar / Inflamável"',
    category: 'sinalizacoes',
    categoryLabel: 'Sinalizações',
    badge: 'AVISO DE PERIGO',
    shortDesc: 'Placa de advertência e proibição em áreas de risco de explosão e armazenamento de inflamáveis.',
    image: 'images/products_original/placa-extintor-e5-nbr.png',
    specs: {
      dimensoes: '20 x 20 cm ou 30 x 20 cm',
      material: 'PVC Anti-chama'
    },
    compliance: ['NBR 13434', 'Prevenção de Sinistro'],
    recommendedFor: 'Depósitos de GLP, tintas e cabines de pintura.'
  },

  // ALARMES E DETECÇÃO
  {
    id: 'central-alarme-incendio-enderecavel',
    name: 'Central de Alarme de Incêndio Endereçável 250 Pontos',
    category: 'alarmes-de-incendio',
    categoryLabel: 'Alarmes e Detecção',
    badge: 'SISTEMA INTELIGENTE',
    shortDesc: 'Central microprocessada com identificação ponto a ponto de acionadores, detectores e sirenes em tempo real.',
    image: 'images/products_original/unidade-central-lux-emergencia.png',
    specs: {
      capacidadePontos: '250 endereços por laço',
      bateriaAutonomia: 'Até 24 horas em standby',
      display: 'LCD retroiluminado com histórico de eventos',
      norma: 'NBR ISO 7240 / NBR 17240'
    },
    compliance: ['NBR 17240', 'ISO 7240', 'Supervisão de Linha'],
    recommendedFor: 'Indústrias, edifícios comerciais e hospitais.'
  },
  {
    id: 'detector-optico-fumaca',
    name: 'Detector Óptico de Fumaça Endereçável',
    category: 'alarmes-de-incendio',
    categoryLabel: 'Alarmes e Detecção',
    badge: 'ALTA SENSIBILIDADE',
    shortDesc: 'Detector de fumaça por câmara fotoelétrica com algoritmo de compensação de poeira e LED indicador.',
    image: 'images/products_original/unidade-central-lux-emergencia.png',
    specs: {
      areaCobertura: 'Até 81 m² por detector',
      tensaoOperacao: '24 VDC',
      norma: 'NBR 17240'
    },
    compliance: ['NBR 17240', 'Filtro Anti-insetos', 'Compensação Automática'],
    recommendedFor: 'Escritórios, quartos de hotel e forros rebaixados.'
  },
  {
    id: 'botoeira-de-bomba',
    name: 'Botoeira de Partida de Bomba de Incêndio',
    category: 'alarmes-de-incendio',
    categoryLabel: 'Alarmes e Detecção',
    badge: 'ACIONAMENTO DIRETO',
    shortDesc: 'Dispositivo em caixa blindada de alumínio ou policarbonato destinado a ligar e desligar a bomba d’água.',
    image: 'images/products_original/unidade-central-lux-emergencia.png',
    specs: {
      tipoContato: '1 NA + 1 NF (10A 250VAC)',
      tipoProtecao: 'IP65',
      marteloQuebraVidro: 'Incluso com corrente',
      norma: 'NBR 13714 / NBR 17240'
    },
    compliance: ['NBR 13714', 'NBR 17240', 'Alta Durabilidade'],
    recommendedFor: 'Próximo aos abrigos de hidrantes e casa de bombas.'
  },
  {
    id: 'sirene-audiovisual-led',
    name: 'Sirene Audiovisual com Flash LED 24V',
    category: 'alarmes-de-incendio',
    categoryLabel: 'Alarmes e Detecção',
    badge: 'ALERTA VISUAL E SONORO',
    shortDesc: 'Sirene eletrônica bitonal de alta intensidade acústica combinada com estroboscópio LED de alerta visual.',
    image: 'images/products_original/unidade-central-lux-emergencia.png',
    specs: {
      pressaoSonora: '105 dB a 1 metro',
      frequenciaFlash: '1 Hz a 2 Hz (LED Vermelho)',
      consumo: 'Baixo consumo (35 mA)',
      norma: 'NBR 17240'
    },
    compliance: ['NBR 17240', 'Acessibilidade NBR 9050', '105 dB'],
    recommendedFor: 'Áreas com ruído industrial e ambientes corporativos.'
  },
  {
    id: 'acionador-manual-rearmavel',
    name: 'Acionador Manual de Alarme Tipo Quebra-Vidro / Rearmável',
    category: 'alarmes-de-incendio',
    categoryLabel: 'Alarmes e Detecção',
    badge: 'FÁCIL OPERAÇÃO',
    shortDesc: 'Botoeira de acionamento manual de emergência com chave de rearme rápido e LED de supervisão.',
    image: 'images/products_original/unidade-central-lux-emergencia.png',
    specs: {
      tipo: 'Rearmável com chave de teste',
      norma: 'NBR 17240'
    },
    compliance: ['NBR 17240', 'Rearme Mecânico'],
    recommendedFor: 'Rotas de fuga e saídas de emergência.'
  },

  // ILUMINAÇÃO DE EMERGÊNCIA
  {
    id: 'unidade-central-lux-700-1200-24vdc',
    name: 'Unidade Central Lux 700 / 1200 24VDC',
    category: 'iluminacoes-de-emergencia',
    categoryLabel: 'Iluminação de Emergência',
    badge: 'SISTEMA CENTRALIZADO INTELIGENTE',
    shortDesc: 'Central inteligente para alimentação e controle contínuo de luminárias de emergência em grandes edificações.',
    image: 'images/products_original/unidade-central-lux-emergencia.png',
    specs: {
      potenciaSaida: '700W a 1200W em 24VDC',
      bateria: 'Banco de baterias estacionárias seladas VRLA',
      autonomia: '3 a 6 horas ininterruptas',
      carregador: 'Flutuação automática com corte térmico',
      norma: 'NBR 10898'
    },
    compliance: ['NBR 10898', 'Bateria Estacionária', 'Supervisão Inteligente'],
    recommendedFor: 'Grandes indústrias, hipermercados e torres corporativas.'
  },
  {
    id: 'bloco-autonomo-led-2200-lumens',
    name: 'Bloco Autônomo de Iluminação LED 2200 Lúmens',
    category: 'iluminacoes-de-emergencia',
    categoryLabel: 'Iluminação de Emergência',
    badge: 'FARÓIS DIRECIONÁVEIS',
    shortDesc: 'Equipamento autônomo com faróis duplos de LED de alta potência e bateria recarregável de lítio integrada.',
    image: 'images/products_original/unidade-central-lux-emergencia.png',
    specs: {
      fluxoLuminoso: '2200 Lúmens',
      autonomia: '2 a 4 horas',
      anguloFarois: 'Ajuste 360° horizontal e 90° vertical',
      norma: 'NBR 10898'
    },
    compliance: ['NBR 10898', 'Bateria de Lítio', 'Faróis Articulados'],
    recommendedFor: 'Galpões de pé-direito duplo e plantas fabris.'
  },
  {
    id: 'luminaria-balizamento-led',
    name: 'Luminária de Balizamento LED Slim Face Única / Dupla',
    category: 'iluminacoes-de-emergencia',
    categoryLabel: 'Iluminação de Emergência',
    badge: 'ACRÍLICO ILUMINADO',
    shortDesc: 'Luminária de saída autônoma em acrílico gravado a laser com indicação luminosa contínua e de emergência.',
    image: 'images/products_original/unidade-central-lux-emergencia.png',
    specs: {
      autonomia: '3 horas',
      instalacao: 'Sobrepor / Parede / Teto',
      norma: 'NBR 10898'
    },
    compliance: ['NBR 10898', 'Design Slim', 'LED de Alta Durabilidade'],
    recommendedFor: 'Portas corta-fogo, teatros, cinemas e hotéis.'
  },
  {
    id: 'bloco-emergencia-led-industrial-ip65',
    name: 'Bloco de Emergência LED Industrial Blindado IP65',
    category: 'iluminacoes-de-emergencia',
    categoryLabel: 'Iluminação de Emergência',
    badge: 'BLINDAGEM IP65',
    shortDesc: 'Luminária hermética à prova d’água e gases com vedação em silicone e difusor em policarbonato anti-impacto.',
    image: 'images/products_original/unidade-central-lux-emergencia.png',
    specs: {
      protecao: 'Grau IP65 contra poeira e jatos de água',
      autonomia: '3 horas',
      norma: 'NBR 10898'
    },
    compliance: ['IP65', 'NBR 10898', 'Anti-impacto IK08'],
    recommendedFor: 'Câmaras frigoríficas, indústrias alimentícias e pátios externos.'
  },

  // EPI, EPR, APH, RESGATE
  {
    id: 'capacete-gallet',
    name: 'Capacete de Combate a Incêndio Gallet MSA',
    category: 'epi',
    categoryLabel: 'EPI (Proteção Individual)',
    badge: 'PROTEÇÃO ESTRUTURAL MÁXIMA',
    shortDesc: 'Capacete de alta proteção térmica e mecânica com protetor facial dourado refletivo e protetor de nuca em Nomex.',
    image: 'images/products_original/valvula-globo-angular-hidrante.png',
    specs: {
      casco: 'Termoplástico de engenharia de alta resistência térmica (> 1000°C flashover)',
      visor: 'Policarbonato com revestimento em ouro antirreflexo e antirrisco',
      norma: 'EN 443 / NFPA 1971'
    },
    compliance: ['EN 443', 'NFPA 1971', 'Reflexão Térmica'],
    recommendedFor: 'Bombeiros militares, brigadistas e equipes de resgate profissional.'
  },
  {
    id: 'roupa-aproximacao-bombeiro',
    name: 'Capa e Calça de Combate a Incêndio Nomex / Kevlar',
    category: 'epi',
    categoryLabel: 'EPI (Proteção Individual)',
    badge: 'TRIPLA CAMADA TÉRMICA',
    shortDesc: 'Conjunto de proteção contra calor radiante, chamas diretas e penetração de líquidos com faixas refletivas.',
    image: 'images/products_original/valvula-globo-angular-hidrante.png',
    specs: {
      composicao: 'Camada Externa em Nomex/Kevlar + Barreira de Umidade + Barreira Térmica',
      norma: 'NFPA 1971 / EN 469'
    },
    compliance: ['NFPA 1971', 'EN 469', 'Ignífugo'],
    recommendedFor: 'Brigadas industriais de alto risco e combate a fogo direto.'
  },
  {
    id: 'mascara-autonoma-respiracao-scba',
    name: 'Máscara Autônoma de Ar Comprimido (EPR) 300 Bar',
    category: 'epr',
    categoryLabel: 'EPR (Proteção Respiratória)',
    badge: 'AR RESPIRÁVEL AUTÔNOMO',
    shortDesc: 'Equipamento autônomo com cilindro de ar comprimido em fibra de carbono 300 bar e máscara panorâmica com pressão positiva.',
    image: 'images/products_original/valvula-globo-angular-hidrante.png',
    specs: {
      cilindro: '6,8 Litros em Fibra de Carbono 300 bar (45 minutos de autonomia)',
      mascara: 'Silicone hipoalergênico com comunicação de voz integrada',
      norma: 'NBR 13716 / EN 137'
    },
    compliance: ['NBR 13716', 'EN 137', 'Pressão Positiva'],
    recommendedFor: 'Ambientes com fumaça densa, gases tóxicos e espaços confinados.'
  },
  {
    id: 'prancha-resgate-polietileno-aph',
    name: 'Prancha Rígida de Resgate em Polietileno com Cintos',
    category: 'aph',
    categoryLabel: 'APH (Primeiros Socorros)',
    badge: '100% TRANSLÚCIDA A RAIO-X',
    shortDesc: 'Prancha para imobilização e transporte de vítimas com 3 jogos de cintos de engate rápido e pegadores anatômicos.',
    image: 'images/products_original/valvula-globo-angular-hidrante.png',
    specs: {
      capacidadeCarga: 'Até 250 kg',
      flutuabilidade: 'Flutuante em água',
      norma: 'ABNT / Portaria MS'
    },
    compliance: ['Translúcida Raio-X', 'Carga 250kg', 'Resgate Rápido'],
    recommendedFor: 'Brigadas de emergência, ambulatórios industriais e piscinas.'
  }
];

export const SERVICES = [
  {
    id: 'projeto-tecnico',
    name: 'Projeto Técnico de Prevenção e Combate a Incêndio (PPCI)',
    category: 'projetos',
    tag: 'PROJETO EXECUTIVO COMPLETO',
    image: 'images/services/projeto-tecnico-ppci.jpg',
    summary: 'Elaboração de plantas baixas executivas, memoriais descritivos, cálculos hidráulicos de hidrantes/sprinklers e aprovação oficial junto ao Corpo de Bombeiros.',
    normas: ['Decreto Estadual nº 63.911', 'IT-01 a IT-44 CBPMESP', 'ART de Engenharia'],
    benefits: [
      'Dimensionamento técnico exato para evitar desperdício e superdimensionamento',
      'Acompanhamento integral até a emissão do parecer favorável dos Bombeiros',
      'Engenheiros registrados no CREA com vasta experiência em indústrias e edifícios'
    ]
  },
  {
    id: 'pts',
    name: 'Processo Técnico Simplificado (PTS)',
    category: 'projetos',
    tag: 'APROVAÇÃO RÁPIDA DE IMÓVEIS',
    image: 'images/services/processo-simplificado-pts.jpg',
    summary: 'Regularização rápida e digital para edificações com área construída de até 750 m² e até 3 pavimentos, garantindo emissão ágil da licença de funcionamento.',
    normas: ['IT-42/18 Corpo de Bombeiros', 'Licenciamento Digital Via Fácil'],
    benefits: [
      'Regularização ágil para abertura e renovação de alvarás comerciais',
      'Vistoria prévia in loco para checagem minuciosa de extintores e sinalizações',
      'Emissão de laudos de conformidade técnica e ARTs necessárias'
    ]
  },
  {
    id: 'avcb-clcb',
    name: 'AVCB e CLCB — Obtenção e Renovação',
    category: 'projetos',
    tag: 'REGULARIZAÇÃO COMPLETA',
    image: 'images/services/avcb-clcb-regularizacao.jpg',
    summary: 'Assessoria completa para obtenção e renovação do Auto de Vistoria (AVCB) e Certificado de Licença (CLCB) do Corpo de Bombeiros em todo o Estado de SP.',
    normas: ['Decreto Estadual SP', 'FAT e Formulários de Vistoria', 'Via Fácil Bombeiros'],
    benefits: [
      'Gestão rigorosa de prazos e vistorias sem risco de multas ou interdição',
      'Testes prévios de pressurização de hidrantes, alarmes e iluminação',
      'Acompanhamento presencial no dia da vistoria oficial dos Bombeiros'
    ]
  },
  {
    id: 'laudos-vistorias',
    name: 'Laudos Técnicos, Vistorias e Inspeções Digitais',
    category: 'projetos',
    tag: 'DIAGNÓSTICO E CONFORMIDADE',
    image: 'images/services/laudos-vistorias-tecnicas.jpg',
    summary: 'Auditorias preventivas in loco com emissão de relatórios fotográficos, laudos de estanqueidade, laudos elétricos (NR-10) e atestados de conformidade.',
    normas: ['Normas ABNT NBR', 'Instruções Técnicas CBPMESP', 'ART / RRT'],
    benefits: [
      'Inspeção detalhada de todos os itens de segurança patrimonial',
      'Relatório preventivo apontando inconformidades antes da fiscalização',
      'Laudos aceitos por seguradoras, prefeituras e órgãos reguladores'
    ]
  },
  {
    id: 'recarga-inmetro',
    name: 'Recarga e Manutenção de Extintores de Incêndio',
    category: 'manutencao',
    tag: 'CERTIFICAÇÃO INMETRO Nº 002874',
    image: 'images/services/recarga-inmetro-extintores.jpg',
    summary: 'Serviço credenciado pelo Inmetro (Nível 1, 2 e 3) para recarga periódica, substituição de agentes extintores, teste de pressão e selagem oficial.',
    normas: ['Portaria Inmetro nº 002874', 'NBR 12962', 'NBR 13485'],
    benefits: [
      'Primeira empresa da região certificada pelo Inmetro com mais de 30 anos',
      'Frota própria para coleta e entrega com extintores de reserva provisórios',
      'Laboratório próprio com maquinário de pressurização e balanças aferidas'
    ]
  },
  {
    id: 'teste-hidrostatico',
    name: 'Teste Hidrostático de Mangueiras e Cilindros',
    category: 'manutencao',
    tag: 'SEGURANÇA CONTRA RUPTURA',
    image: 'images/services/teste-hidrostatico-mangueiras.jpg',
    summary: 'Ensaio hidrostático anual de mangueiras de incêndio e teste quinquenal em cilindros de alta pressão para certificar a resistência sob pressão extrema.',
    normas: ['NBR 12779 (Mangueiras)', 'NBR 12274 (Cilindros CO2)', 'NBR 15808'],
    benefits: [
      'Bancada hidrostática computadorizada com emissão de laudo técnico individual',
      'Secagem em estufa e re-empate com anéis de cobre novos conforme norma',
      'Identificação de microfissuras e desgastes invisíveis a olho nu'
    ]
  },
  {
    id: 'sistemas-hidrantes',
    name: 'Instalação e Manutenção de Redes de Hidrantes',
    category: 'hidraulica',
    tag: 'ENGENHARIA HIDRÁULICA',
    image: 'images/services/redes-hidrantes-bombas.jpg',
    summary: 'Montagem de tubulações em aço carbono ranhurado (Grooved) ou roscado, instalação de bombas de incêndio principais e jockey, e testes de vazão.',
    normas: ['NBR 13714', 'IT-22 Bombeiros', 'Válvulas & Conexões Ranhuradas'],
    benefits: [
      'Equipe de montagem, soldadores e instaladores certificados',
      'Cálculo exato de perda de carga e dimensionamento de reservatório técnico',
      'Painéis de comando automático com acionamento por pressostato'
    ]
  },
  {
    id: 'sprinklers',
    name: 'Sistemas de Sprinklers (Chuveiros Automáticos)',
    category: 'hidraulica',
    tag: 'COMBATE AUTOMÁTICO 24H',
    image: 'images/services/sistemas-sprinklers.jpg',
    summary: 'Engenharia, instalação e manutenção de sistemas de chuveiros automáticos (Sprinklers) para controle e extinção instantânea de princípios de incêndio.',
    normas: ['NBR 10897', 'NFPA 13', 'IT-23 CBPMESP'],
    benefits: [
      'Proteção patrimonial máxima para indústrias e galpões de alto valor agregado',
      'Válvulas de Governo e Alarme (VGA) com monitoramento eletrônico de fluxo',
      'Manutenções preventivas com limpeza de bicos e testes de estanqueidade'
    ]
  },
  {
    id: 'caixa-dagua',
    name: 'Fabricação e Manutenção de Caixa d’Água / RTI',
    category: 'hidraulica',
    tag: 'RESERVATÓRIO DEDICADO',
    image: 'images/services/caixa-dagua-reservatorio-rti.jpg',
    summary: 'Construção e reforma de caixas d’água metálicas tipo taça e cilíndricas com reserva técnica exclusiva de incêndio (RTI) conforme cálculo dos Bombeiros.',
    normas: ['NBR 13714', 'NBR 7821', 'Reserva Técnica Exclusiva'],
    benefits: [
      'Pintura interna epóxi atóxica e pintura externa automotiva anticorrosiva',
      'Garantia de vazão e reserva técnica ininterrupta para a rede de hidrantes',
      'Inspeção interna por ultrassom e reparos estruturais especializados'
    ]
  },
  {
    id: 'alarmes-deteccao',
    name: 'Sistemas de Alarme e Detecção Automática de Incêndio',
    category: 'eletrica',
    tag: 'RESPOSTA PRECOCE A SINISTROS',
    image: 'images/services/alarmes-deteccao-incendio.jpg',
    summary: 'Implantação de redes endereçáveis e convencionais com detectores ópticos de fumaça, termo-velocimétricos, acionadores manuais e integração predial.',
    normas: ['NBR 17240', 'ISO 7240', 'IT-19 CBPMESP'],
    benefits: [
      'Identificação milimétrica do foco de fumaça antes da propagação do fogo',
      'Integração com portas corta-fogo, pressurização de escadas e elevadores',
      'Painéis repetidores na portaria/segurança para ação rápida da brigada'
    ]
  },
  {
    id: 'iluminacao-emergencia',
    name: 'Sistemas de Iluminação e Balizamento de Emergência',
    category: 'eletrica',
    tag: 'ROTAS SEGURAS ILUMINADAS',
    image: 'images/services/iluminacao-emergencia.jpg',
    summary: 'Projeto e implementação de redes de iluminação centralizadas ou autônomas em conformidade rigorosa com a NBR 10898 e Instrução Técnica nº 18.',
    normas: ['NBR 10898', 'IT-18 Corpo de Bombeiros', 'Blocos Autônomos LED'],
    benefits: [
      'Mapeamento de iluminância mínima em lux para todos os pontos da rota de fuga',
      'Centrais inteligentes com comutação instantânea na queda de energia elétrica',
      'Baterias de ciclo profundo com vida útil prolongada'
    ]
  },
  {
    id: 'sinalizacao-fotoluminescente',
    name: 'Sinalização de Emergência Fotoluminescente',
    category: 'eletrica',
    tag: 'ORIENTAÇÃO & ROTAS DE FUGA',
    image: 'images/services/sinalizacao-fotoluminescente.jpg',
    summary: 'Fornecimento e instalação de placas fotoluminescentes normatizadas de rota de fuga, indicação de extintores, hidrantes e saídas de emergência.',
    normas: ['NBR 13434', 'IT-20 Corpo de Bombeiros'],
    benefits: [
      'Placas com certificação de pigmento fotoluminescente de alta intensidade',
      'Layout e instalação nas alturas e distâncias exatas exigidas pela norma',
      'Resistência a intempéries e produtos de limpeza industriais'
    ]
  },
  {
    id: 'treinamento-brigada',
    name: 'Treinamento de Brigada de Incêndio e Primeiros Socorros',
    category: 'brigada',
    tag: 'CAPACITAÇÃO PRÁTICA HOMOLOGADA',
    image: 'images/services/treinamento-brigada-incendio.jpg',
    summary: 'Curso teórico e prático de formação e reciclagem de brigadistas em conformidade com a NBR 14276 e IT-17, com simulações reais de combate ao fogo.',
    normas: ['NBR 14276', 'IT-17 CBPMESP', 'Certificado Oficial'],
    benefits: [
      'Instrutores credenciados pelo Corpo de Bombeiros e médicos/socorristas',
      'Campo de treinamento prático com simuladores de fogo real e primeiros socorros',
      'Emissão de certificados individuais e atestado de formação de brigada'
    ]
  },
  {
    id: 'locacao-equipamentos',
    name: 'Locação de Equipamentos, Extintores e Carretas',
    category: 'brigada',
    tag: 'FLEXIBILIDADE OPERACIONAL',
    image: 'images/services/locacao-equipamentos-extintores.jpg',
    summary: 'Disponibilização temporária de extintores, carretas de grande porte, mangueiras e rádios para feiras, eventos, paradas industriais e obras.',
    normas: ['NBR 15808', 'IT-12 CBPMESP', 'Equipamentos Certificados'],
    benefits: [
      'Equipamentos com carga 100% nova e certificada Inmetro',
      'Entrega, suporte de posicionamento e retirada sem dor de cabeça',
      'Opções de curto, médio e longo prazo para construtoras e indústrias'
    ]
  },
  {
    id: 'equipe-eventos',
    name: 'Disponibilização de Bombeiros Civis e Plantão Técnico',
    category: 'brigada',
    tag: 'BRIGADA PROFISSIONAL DEDICADA',
    image: 'images/services/bombeiros-civis-eventos.jpg',
    summary: 'Equipe de bombeiros civis credenciados e uniformizados para plantão em eventos corporativos, feiras industriais, shows e intervenções de risco elevado.',
    normas: ['NBR 14608', 'IT-17 CBPMESP', 'APH & Desfibrilador (DEA)'],
    benefits: [
      'Profissionais treinados em primeiros socorros, resgate e combate a incêndio',
      'Kits completos de APH com prancha, desfibrilador (DEA) e extintores dedicados',
      'Tranquilidade jurídica e conformidade com as exigências dos órgãos públicos'
    ]
  }
];

