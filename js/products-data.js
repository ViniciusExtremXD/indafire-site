/**
 * Inda Fire - Base de Dados de Produtos Oficiais
 * Classificação, especificações técnicas e conformidade com normas ABNT / Inmetro
 */

const INDAFIRE_PRODUCTS = [
  {
    id: "unidade-central-lux-700-1200",
    name: "Unidade Central LUX 700/1200",
    category: "iluminacao",
    categoryLabel: "Iluminação de Emergência",
    image: "images/products_original/unidade-central-lux-emergencia.png",
    featured: true,
    badge: "Alta Autonomia",
    shortDesc: "Sistema centralizado inteligente para alimentação e controle de luminárias de emergência.",
    fullDesc: "A Unidade Central LUX 700/1200 foi desenvolvida para garantir iluminação contínua e segura em rotas de fuga e ambientes industriais em caso de queda de energia. Possui carregador flutuante automático, baterias seladas isentas de manutenção e proteção contra sobrecarga e descarga profunda.",
    specs: [
      { label: "Autonomia", value: "Até 3 horas contínuas" },
      { label: "Tensão de Entrada", value: "Bivolt Automático 110V / 220V" },
      { label: "Capacidade de Carga", value: "700W a 1200W" },
      { label: "Tipo de Bateria", value: "Chumbo-ácida selada VRLA" },
      { label: "Gabinete", value: "Aço carbono com pintura eletrostática a pó" }
    ],
    compliance: ["NBR 10898", "Instrução Técnica Corpo de Bombeiros"]
  },
  {
    id: "placa-extintor-e5",
    name: "Placa Extintor Fotoluminescente E5",
    category: "sinalizacao",
    categoryLabel: "Sinalização de Emergência",
    image: "images/products_original/placa-extintor-e5-nbr.png",
    featured: true,
    badge: "Norma NBR 13434",
    shortDesc: "Sinalização de orientação e salvamento com pigmento fotoluminescente de alta intensidade.",
    fullDesc: "Placa de sinalização básica e complementar com pictograma e código E5 para identificação rápida de extintores de incêndio. Fabricada em PVC antichama com pigmentação fotoluminescente que garante visibilidade no escuro por até 30 horas após a interrupção da luz.",
    specs: [
      { label: "Material", value: "PVC rígido 2mm autoextinguível" },
      { label: "Fotoluminescência", value: "140 mcd/m² a 10 min | 20 mcd/m² a 60 min" },
      { label: "Dimensões", value: "150 x 150 mm ou 200 x 200 mm" },
      { label: "Fixação", value: "Fita dupla face industrial ou furação" }
    ],
    compliance: ["NBR 13434", "IT-20 Corpo de Bombeiros"]
  },
  {
    id: "capacete-gallet-f1-sf",
    name: "Capacete de Combate a Incêndio Gallet F1 SF",
    category: "epi-epc",
    categoryLabel: "EPI / Proteção Individual",
    image: "images/products_original/capacete-gallet-f1.png",
    featured: true,
    badge: "Padrão Internacional",
    shortDesc: "Capacete de alta proteção térmica e mecânica para combate a incêndios estruturais e resgates.",
    fullDesc: "O Capacete Gallet F1 SF é a referência mundial em proteção para brigadistas e bombeiros profissionais. Oferece resistência a impactos extremos, radiação térmica e penetração de objetos, com viseira dourada integrada para reflexão de calor radiante e protetor facial retrátil.",
    specs: [
      { label: "Resistência Térmica", value: "Até 1.000°C por flashover térmico curto" },
      { label: "Viseiras", value: "Protetor ocular retrátil + Viseira facial dourada" },
      { label: "Carcaça", value: "Termoplástico injetado de altíssima densidade" },
      { label: "Ajuste", value: "Catraca ergonômica ajustável para luvas" }
    ],
    compliance: ["EN 443:2008", "NFPA 1971", "Certificado de Aprovação (CA)"]
  },
  {
    id: "armario-corta-fogo",
    name: "Armário Corta-Fogo para Inflamáveis",
    category: "epi-epc",
    categoryLabel: "EPC / Armazenamento Seguro",
    image: "images/products_original/armario-corta-fogo-seguranca.png",
    featured: true,
    badge: "Segurança Industrial",
    shortDesc: "Gabinete blindado de contenção para líquidos inflamáveis, combustíveis e químicos.",
    fullDesc: "Armário de segurança construído em parede dupla de chapa de aço com isolamento térmico e sistema de fechamento automático em caso de incêndio. Projetado para conter e isolar vapores perigosos, retardando a propagação do fogo e protegendo as instalações.",
    specs: [
      { label: "Construção", value: "Parede dupla com câmara de ar isolante de 38mm" },
      { label: "Pintura", value: "Epóxi amarelo de alta resistência química" },
      { label: "Fechamento", value: "Fechadura tipo cremona de 3 pontos com chave" },
      { label: "Dreno e Respiro", value: "Válvulas corta-chama com rosca NPT nas laterais" }
    ],
    compliance: ["NFPA 30", "OSHA 29 CFR 1910.106", "NBR 17505"]
  },
  {
    id: "botoeira-bomba",
    name: "Botoeira de Alarme / Acionador Manual",
    category: "alarmes",
    categoryLabel: "Sistemas de Alarme e Detecção",
    image: "images/products_original/botoeira-de-bomba-alarme.png",
    featured: true,
    badge: "Disparo Rápido",
    shortDesc: "Acionador manual tipo 'quebre o vidro' ou rearmável com LED indicador de estado.",
    fullDesc: "Dispositivo para disparo manual do alarme de emergência em casos de sinistro ou princípio de incêndio. Disponível nas versões convencional e endereçável, com proteção frontal acrílica e chave de teste para manutenção preventiva sem quebra de componente.",
    specs: [
      { label: "Tipo de Acionamento", value: "Pressão mecânica rearmável com chave" },
      { label: "Sinalização", value: "LED bicolor de supervisão e alarme" },
      { label: "Tensão de Operação", value: "24 VDC nominal" },
      { label: "Grau de Proteção", value: "IP40 interno / IP66 externo sob consulta" }
    ],
    compliance: ["NBR 17240", "Certificação CE"]
  },
  {
    id: "mangueira-tipo-i",
    name: "Mangueira de Combate a Incêndio Tipo I e II",
    category: "mangueiras",
    categoryLabel: "Mangueiras de Incêndio",
    image: "images/products_original/mangueira-tipo-i-predial.png",
    featured: true,
    badge: "Certificada ABNT",
    shortDesc: "Mangueira flexível com reforço têxtil em poliéster e tubo interno de borracha vulcanizada.",
    fullDesc: "Mangueiras fabricadas rigorosamente sob normas técnicas, com engates rápidos tipo Storz em latão forjado. Disponíveis em comprimentos de 15m, 20m, 25m e 30m, nos diâmetros de 1.1/2\" (Tipo I - Residencial/Edifícios) e 2.1/2\" (Tipo II - Comercial e Industrial).",
    specs: [
      { label: "Pressão de Trabalho", value: "Tipo 1: 10 kgf/cm² | Tipo 2: 14 kgf/cm²" },
      { label: "Pressão de Ruptura", value: "Tipo 1: 42 kgf/cm² | Tipo 2: 55 kgf/cm²" },
      { label: "União", value: "Engate rápido tipo Storz em latão forjado" },
      { label: "Revestimento", value: "Trama 100% poliéster de alta tenacidade" }
    ],
    compliance: ["NBR 11861", "Selo de Conformidade Inmetro / ABNT"]
  },
  {
    id: "suporte-solo-extintor",
    name: "Suporte de Solo para Extintor (Inox e Cromado)",
    category: "extintores",
    categoryLabel: "Extintores e Acessórios",
    image: "images/products_original/suporte-solo-extintor-inox.png",
    featured: false,
    badge: "Acabamento Premium",
    shortDesc: "Suporte tubular de piso para acomodação segura e elegante de extintores portáteis.",
    fullDesc: "Suporte de chão tipo tripé ou pedestal em aço inoxidável ou cromado, ideal para escritórios, halls de entrada, shoppings e indústrias onde não é permitida ou desejada a furação de paredes de alvenaria ou divisórias de drywall.",
    specs: [
      { label: "Material", value: "Aço Inox AISI 304 polido ou Aço Carbono Cromado" },
      { label: "Compatibilidade", value: "Extintores de 4kg a 12kg (Água, PQS, CO2)" },
      { label: "Proteção", value: "Pés com borrachas antiderrapantes e anti-risco" },
      { label: "Altura", value: "Aproximadamente 60 cm a 75 cm" }
    ],
    compliance: ["NBR 12693", "NBR 15808"]
  },
  {
    id: "colete-ked",
    name: "Colete de Imobilização KED (Kendrick Extrication Device)",
    category: "resgate-aph",
    categoryLabel: "Resgate e Primeiros Socorros (APH)",
    image: "images/products_original/colete-ked-adulto.png",
    featured: false,
    badge: "Imobilização Espinhal",
    shortDesc: "Dispositivo de imobilização espinhal para resgate veicular e locais de difícil acesso.",
    fullDesc: "O KED permite a estabilização completa da coluna cervical e espinhal de vítimas presas em ferragens ou espaços confinados antes da remoção, minimizando riscos de agravamento de lesões na medula. Confeccionado em nylon de alta resistência com tiras coloridas codificadas.",
    specs: [
      { label: "Acessórios Inclusos", value: "Colete, almofada de cabeça, tiras de queixo e testa, bolsa" },
      { label: "Material", value: "Nylon 600D lavável e impermeável" },
      { label: "Carga Máxima", value: "150 kg" },
      { label: "Radiotransparência", value: "100% radiotransparente para Raio-X" }
    ],
    compliance: ["Normas Internacionais de Resgate e Trauma", "ANVISA"]
  },
  {
    id: "cinturao-xpert-ii",
    name: "Cinturão Paraquedista X-PERT II",
    category: "epi-epc",
    categoryLabel: "EPI / Proteção Individual",
    image: "images/products_original/cinturao-xpert-ii.png",
    featured: false,
    badge: "NR-35 Certificado",
    shortDesc: "Cinturão de segurança tipo paraquedista com pontos de ancoragem dorsal e peitoral.",
    fullDesc: "Desenvolvido para retenção de quedas, posicionamento e acesso por corda em serviços de manutenção predial, brigada e espaços industriais. Fitas de poliéster de alta tenacidade com almofadas respiráveis nas pernas e cintura.",
    specs: [
      { label: "Pontos de Ancoragem", value: "Dorsal, Peitoral e Laterais para Posicionamento" },
      { label: "Fivelas", value: "Aço estampado de engate rápido com travamento" },
      { label: "Acolchoamento", value: "Espuma termoformada e tecido transpirável" },
      { label: "Capacidade", value: "Usuários de até 140 kg (com ferramentas)" }
    ],
    compliance: ["NR-35", "NBR 15835", "NBR 15836", "Certificado de Aprovação (CA)"]
  },
  {
    id: "cilindro-6l-300-bar",
    name: "Cilindro de Proteção Respiratória 6L / 300 BAR",
    category: "resgate-aph",
    categoryLabel: "Proteção Respiratória",
    image: "images/products_original/cilindro-ar-respiravel-6l.png",
    featured: false,
    badge: "Ar Respirável",
    shortDesc: "Cilindro de ar comprimido respirável em fibra de carbono ou aço para máscara autônoma.",
    fullDesc: "Cilindro para equipamento autônomo de proteção respiratória (EAPR). Fornece ar respirável de grau médico e alta pureza para brigadistas e equipes de resgate em atmosferas imediatamente perigosas à vida e à saúde (IPVS), com fumaça tóxica ou deficiência de oxigênio.",
    specs: [
      { label: "Volume / Pressão", value: "6 Litros / 300 BAR (Volume expandido 1.800L)" },
      { label: "Autonomia", value: "Aproximadamente 45 a 60 minutos" },
      { label: "Válvula", value: "Válvula com manômetro integrado e trava de segurança" },
      { label: "Composição", value: "Linha de fibra de carbono ultra-leve ou aço tratado" }
    ],
    compliance: ["NBR 13716", "EN 12245", "DOT-SP"]
  }
];

const PRODUCT_CATEGORIES = [
  { id: "all", label: "Todos os Produtos" },
  { id: "extintores", label: "Extintores & Suportes" },
  { id: "mangueiras", label: "Mangueiras de Incêndio" },
  { id: "sinalizacao", label: "Sinalização Fotoluminescente" },
  { id: "iluminacao", label: "Iluminação de Emergência" },
  { id: "alarmes", label: "Alarmes & Detecção" },
  { id: "epi-epc", label: "EPIs & EPCs" },
  { id: "resgate-aph", label: "Resgate & APH" }
];
