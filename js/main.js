/**
 * INDA FIRE — MAIN KINETIC INDUSTRIAL JAVASCRIPT ENGINE
 * Features: Translucent Sticky Nav, Smooth Logo Scroll & Animation Replay,
 * Viewport Counters, Connected Overlapping Certificate Carousel & Product Engine
 */

document.addEventListener('DOMContentLoaded', () => {
  initScrollEffects();
  initNavigation();
  initMegaMenus();
  initMotionReveal();
  initAnimatedCounters();
  initServicesCarousel();
  initTimelineCarousel();
  initExpertiseCarousel();
  initMVVCarousel();
  initProductCatalog();
  initQuoteForm();
  initWhatsAppWidget();
  initModals();
  initLogoScrollToTop();
  initTrainingVideoControls();
});

/* ==========================================================================
   1. SCROLL EFFECTS & SCROLLSPY
   ========================================================================== */
function initScrollEffects() {
  const progressBar = document.getElementById('scroll-progress');
  const header = document.getElementById('site-header');

  window.addEventListener('scroll', () => {
    const scrollTop = window.scrollY || document.documentElement.scrollTop;
    const scrollHeight = document.documentElement.scrollHeight - document.documentElement.clientHeight;
    
    // Progress Bar
    if (progressBar && scrollHeight > 0) {
      progressBar.style.width = `${(scrollTop / scrollHeight) * 100}%`;
    }

    // Glassmorphism Header state
    if (header) {
      if (scrollTop > 40) {
        header.classList.add('scrolled');
      } else {
        header.classList.remove('scrolled');
      }
    }
  }, { passive: true });

  // Scrollspy
  const sections = document.querySelectorAll('section[id]');
  const navLinks = document.querySelectorAll('.nav-link, .mobile-nav-link');

  const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        const id = entry.target.getAttribute('id');
        navLinks.forEach(link => {
          if (link.getAttribute('href') === `#${id}`) {
            link.classList.add('active');
          } else if (link.getAttribute('href')?.startsWith('#')) {
            link.classList.remove('active');
          }
        });
      }
    });
  }, { rootMargin: '-20% 0px -70% 0px' });

  sections.forEach(s => observer.observe(s));
}

/* ==========================================================================
   2. LOGO SMOOTH SCROLL TO TOP & REPLAY MOTION ANIMATIONS
   ========================================================================== */
function initLogoScrollToTop() {
  const logoBtn = document.getElementById('brand-logo-btn');
  if (!logoBtn) return;

  logoBtn.addEventListener('click', (e) => {
    e.preventDefault();
    
    window.scrollTo({
      top: 0,
      behavior: 'smooth'
    });

    // Reset and replay animations
    const revealElements = document.querySelectorAll('.reveal, .reveal-up, .reveal-fade, .reveal-left, .reveal-right, .reveal-scale');
    revealElements.forEach(el => {
      el.classList.remove('active');
    });

    setTimeout(() => {
      // Re-trigger hero animation immediately
      const heroContent = document.querySelector('.hero-content');
      if (heroContent) heroContent.classList.add('active');
      
      // Re-initialize intersection observers for the rest
      initMotionReveal();
    }, 400);
  });
}

/* ==========================================================================
   3. MOBILE NAVIGATION DRAWER & OVERLAY CONTROLLER
   ========================================================================== */
function initNavigation() {
  const toggleBtn = document.getElementById('mobile-menu-toggle');
  const drawer = document.getElementById('mobile-drawer');
  const overlay = document.getElementById('mobile-drawer-overlay');
  const closeBtn = document.getElementById('mobile-drawer-close');
  const links = document.querySelectorAll('.mobile-nav-link, .btn-drawer-quote');

  if (!toggleBtn || !drawer) return;

  function toggleDrawer(open) {
    const shouldOpen = open !== undefined ? open : !drawer.classList.contains('open');
    drawer.classList.toggle('open', shouldOpen);
    if (overlay) overlay.classList.toggle('open', shouldOpen);
    toggleBtn.classList.toggle('open', shouldOpen);
    toggleBtn.setAttribute('aria-expanded', shouldOpen);
    document.body.style.overflow = shouldOpen ? 'hidden' : '';
  }

  toggleBtn.addEventListener('click', () => toggleDrawer());
  if (closeBtn) closeBtn.addEventListener('click', () => toggleDrawer(false));
  if (overlay) overlay.addEventListener('click', () => toggleDrawer(false));
  links.forEach(l => l.addEventListener('click', () => toggleDrawer(false)));

  document.addEventListener('keydown', (e) => {
    if (e.key === 'Escape' && drawer.classList.contains('open')) {
      toggleDrawer(false);
    }
  });
}


/* ==========================================================================
   3.1. EXPANDED MEGA-MENUS (PRODUTOS & SERVIÇOS)
   ========================================================================== */
function initMegaMenus() {
  const header = document.querySelector('.site-header');
  const dropdowns = document.querySelectorAll('.nav-item-dropdown');
  const megaLinks = document.querySelectorAll('.mega-category-link');
  const vignetteLinks = document.querySelectorAll('.mega-servico-vignette');
  
  dropdowns.forEach(d => {
    const panel = d.querySelector('.mega-menu-panel');
    let closeTimeout = null;

    const openMenu = () => {
      if (closeTimeout) clearTimeout(closeTimeout);
      dropdowns.forEach(other => {
        if (other !== d) other.classList.remove('open');
      });
      d.classList.add('open');
      if (header) header.classList.add('has-mega-open');
    };

    const closeMenu = () => {
      if (closeTimeout) clearTimeout(closeTimeout);
      closeTimeout = setTimeout(() => {
        d.classList.remove('open');
        const anyOpen = Array.from(dropdowns).some(item => item.classList.contains('open'));
        if (!anyOpen && header) {
          header.classList.remove('has-mega-open');
        }
      }, 280); // Tolerância suave de 280ms para transição sem interrupção
    };

    d.addEventListener('mouseenter', openMenu);
    d.addEventListener('mouseleave', closeMenu);

    if (panel) {
      panel.addEventListener('mouseenter', openMenu);
      panel.addEventListener('mouseleave', closeMenu);
    }
  });

  // Close mega menus on click outside
  document.addEventListener('click', (e) => {
    if (!e.target.closest('.nav-item-dropdown')) {
      dropdowns.forEach(d => d.classList.remove('open'));
      if (header) header.classList.remove('has-mega-open');
    }
  });

  // Mega Products Carousel
  const prodImg = document.getElementById('mega-prod-img');
  const prodTitle = document.getElementById('mega-prod-title');
  const prodDesc = document.getElementById('mega-prod-desc');
  const prodBtn = document.getElementById('mega-prod-btn');
  const prevBtn = document.getElementById('mega-prod-prev');
  const nextBtn = document.getElementById('mega-prod-next');

  if (typeof INDAFIRE_PRODUCTS !== 'undefined' && INDAFIRE_PRODUCTS.length && prodImg) {
    let currentIdx = 0;

    function updateMegaProduct(idx) {
      currentIdx = (idx + INDAFIRE_PRODUCTS.length) % INDAFIRE_PRODUCTS.length;
      const p = INDAFIRE_PRODUCTS[currentIdx];
      prodImg.src = p.image;
      prodImg.alt = p.name;
      prodTitle.textContent = p.name;
      prodDesc.textContent = p.shortDesc;
      if (prodBtn) {
        prodBtn.onclick = (e) => {
          e.preventDefault();
          openProductModal(p.id);
        };
      }
    }

    if (prevBtn) {
      prevBtn.addEventListener('click', (e) => {
        e.preventDefault();
        e.stopPropagation();
        updateMegaProduct(currentIdx - 1);
      });
    }

    if (nextBtn) {
      nextBtn.addEventListener('click', (e) => {
        e.preventDefault();
        e.stopPropagation();
        updateMegaProduct(currentIdx + 1);
      });
    }

    updateMegaProduct(0);
  }

  // Category links in Mega Menu
  megaLinks.forEach(link => {
    link.addEventListener('click', (e) => {
      const filter = link.getAttribute('data-filter');
      dropdowns.forEach(d => d.classList.remove('open'));
      const pill = document.querySelector(`.category-pill[data-category="${filter}"]`);
      if (pill) pill.click();
    });
  });

  // Vignette links in Serviços Mega Menu
  vignetteLinks.forEach(vignette => {
    vignette.addEventListener('click', () => {
      const anchor = vignette.getAttribute('data-service-anchor');
      dropdowns.forEach(d => d.classList.remove('open'));
      const tab = document.querySelector(`.service-card-item[data-service-key="${anchor}"]`);
      if (tab) tab.click();
      const servSection = document.getElementById('servicos');
      if (servSection) {
        servSection.scrollIntoView({ behavior: 'smooth' });
      }
    });
  });
}

/* ==========================================================================
   4. MOTION DESIGN & SCROLL REVEAL (WITH STAGGER)
   ========================================================================== */
function initMotionReveal() {
  const revealElements = document.querySelectorAll('.reveal, .reveal-up, .reveal-fade, .reveal-left, .reveal-right, .reveal-scale');
  
  if (!('IntersectionObserver' in window)) {
    revealElements.forEach(el => el.classList.add('active'));
    return;
  }

  const isMobile = window.innerWidth <= 768;
  const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        entry.target.classList.add('active');
        observer.unobserve(entry.target);
      }
    });
  }, { 
    threshold: isMobile ? 0.01 : 0.08, 
    rootMargin: isMobile ? '0px 0px 100px 0px' : '0px 0px -20px 0px' 
  });

  revealElements.forEach(el => {
    // If element is already in viewport or in hero on initial load, activate immediately
    const rect = el.getBoundingClientRect();
    if (rect.top < window.innerHeight && rect.bottom > 0) {
      el.classList.add('active');
    } else {
      observer.observe(el);
    }
  });
}

/* ==========================================================================
   5. LIVE ANIMATED VIEWPORT COUNTERS
   ========================================================================== */
function initAnimatedCounters() {
  const counterElements = document.querySelectorAll('[data-counter-target]');
  if (!counterElements.length || !('IntersectionObserver' in window)) return;

  const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        const el = entry.target;
        const target = parseFloat(el.getAttribute('data-counter-target') || '0');
        const duration = parseInt(el.getAttribute('data-counter-duration') || '2400', 10);
        const prefix = el.getAttribute('data-counter-prefix') || '+';
        const suffix = el.getAttribute('data-counter-suffix') || '';
        
        let startTimestamp = null;
        const step = (timestamp) => {
          if (!startTimestamp) startTimestamp = timestamp;
          const progress = Math.min((timestamp - startTimestamp) / duration, 1);
          // Ultra-smooth ease-out quart
          const easeOut = 1 - Math.pow(1 - progress, 4);
          const currentVal = Math.floor(easeOut * target);
          
          el.innerHTML = `${prefix}${currentVal.toLocaleString('pt-BR')}${suffix}`;
          
          if (progress < 1) {
            window.requestAnimationFrame(step);
          } else {
            el.innerHTML = `${prefix}${target.toLocaleString('pt-BR')}${suffix}`;
          }
        };
        
        window.requestAnimationFrame(step);
        observer.unobserve(el);
      }
    });
  }, { threshold: 0.2 });

  counterElements.forEach(el => observer.observe(el));
}

/* ==========================================================================
   6. SERVICES CAROUSEL & CONNECTED OVERLAPPING CERTIFICATE PANEL
   ========================================================================== */
const SERVICES_DATA = {
  "pts": {
    id: "pts",
    title: "Processo Simplificado (PTS)",
    image: "images/serv15-500.webp",
    alt: "Certificado de Licença do Corpo de Bombeiros CLCB - Processo Simplificado",
    desc: "Elaborado para edificações com área construída abaixo de 750 m² e com altura de até 3 pavimentos, nos termos e exceções previstas na Instrução Técnica IT 42/18.",
    specs: [
      "Vistoria prévia no imóvel com check-list técnico",
      "Emissão de laudo e recolhimento de ART junto ao CREA-SP",
      "Protocolo e acompanhamento ágil no sistema Via Fácil Bombeiros"
    ]
  },
  "pt": {
    id: "pt",
    title: "Projeto Técnico (PT)",
    image: "images/serv14-500.webp",
    alt: "Projeto Técnico de Prevenção e Combate a Incêndio",
    desc: "Desenvolvimento de projetos técnicos completos para indústrias, centros logísticos e comércios de grande porte, com cálculo hidráulico de bombas, hidrantes e sprinklers.",
    specs: [
      "Plantas executivas em DWG com detalhamento rigoroso",
      "Cálculo de carga de incêndio e compartimentação",
      "Aprovação e expedição de AVCB pelo Corpo de Bombeiros"
    ]
  },
  "avcb": {
    id: "avcb",
    title: "AVCB / CLCB — Obtenção ou Renovação",
    image: "images/serv16-500.webp",
    alt: "Auto de Vistoria do Corpo de Bombeiros AVCB",
    desc: "Consultoria e assessoria técnica integral para regularização predial, renovação de licenças vencidas e adequação imediata para vistorias oficiais dos bombeiros.",
    specs: [
      "Adequação de rotas de fuga, iluminação e sinalização",
      "Acompanhamento presencial no dia da vistoria oficial",
      "Garantia de conformidade técnica e jurídica do imóvel"
    ]
  },
  "recarga": {
    id: "recarga",
    title: "Manutenção e Recarga Inmetro",
    image: "images/serv17-500.webp",
    alt: "Selo Inmetro e Laudo de Recarga de Extintores",
    desc: "Oficina própria homologada pelo Inmetro com registro compulsório desde 2008. Realizamos inspeção dos níveis 1, 2 e 3 em extintores de Pó Químico, Água e CO2.",
    specs: [
      "Selo de conformidade Inmetro e anel de garantia inviolável",
      "Empréstimo de extintores de backup durante a manutenção",
      "Frota própria para coleta e entrega programada"
    ]
  },
  "hidrostatico": {
    id: "hidrostatico",
    title: "Teste Hidrostático de Mangueiras",
    image: "images/serv18-500.webp",
    alt: "Laudo de Teste Hidrostático de Mangueiras de Incêndio",
    desc: "Ensaio periódico obrigatório de pressão hidrostática em mangueiras de incêndio conforme norma NBR 11861, com secagem em estufa e laudo técnico individual.",
    specs: [
      "Bancada de teste de alta pressão com manômetros aferidos",
      "Reempatação de uniões Storz de latão e teste de estanqueidade",
      "Etiqueta técnica com validade do ensaio para vistoria"
    ]
  },
  "brigada": {
    id: "brigada",
    title: "Treinamento de Brigada (IT-17)",
    image: "images/training.webp",
    alt: "Treinamento de Brigada de Incêndio Inda Fire",
    desc: "Capacitação prática e teórica in-company com Unidade Móvel de Treinamento e simuladores de fogo real, conforme Instrução Técnica IT-17 e NR-23.",
    specs: [
      "Instrutores credenciados com ampla experiência operacional",
      "Simulações práticas de extinção e primeiros socorros (APH)",
      "Emissão imediata de Certificados e Atestado de Brigada"
    ]
  }
};

function initServicesCarousel() {
  const tabs = document.querySelectorAll('.service-card-item, .service-tab-card');
  const track = document.getElementById('carousel-cards-track');
  const prevBtn = document.getElementById('carousel-prev-btn');
  const nextBtn = document.getElementById('carousel-next-btn');
  const dotsContainer = document.getElementById('services-dots-nav');
  const dots = document.querySelectorAll('.service-dot');

  const panel = document.getElementById('service-detail-panel');
  const certBox = document.querySelector('.cert-document-card') || document.querySelector('.out-of-frame-cert-box');
  const certImg = document.getElementById('detail-cert-img');
  const titleEl = document.getElementById('detail-title');
  const descEl = document.getElementById('detail-desc');
  const specsEl = document.getElementById('detail-specs-list');

  if (!tabs.length || !certImg) return;

  // Extract valid ordered keys
  const serviceKeys = Array.from(tabs)
    .map(t => t.getAttribute('data-service-key'))
    .filter((k, idx, arr) => k && arr.indexOf(k) === idx);

  let currentIndex = serviceKeys.indexOf('pts');
  if (currentIndex === -1) currentIndex = 0;

  let autoplayTimer = null;
  const AUTOPLAY_DELAY_MS = 5200; // 5.2 seconds for a calm, editorial pace

  function centerActiveCard(tabEl) {
    if (!track || !tabEl) return;
    const trackWidth = track.clientWidth;
    const tabLeft = tabEl.offsetLeft;
    const tabWidth = tabEl.clientWidth;
    const targetScrollLeft = tabLeft - (trackWidth / 2) + (tabWidth / 2);
    track.scrollTo({
      left: Math.max(0, targetScrollLeft),
      behavior: 'smooth'
    });
  }

  function updateDots(activeIdx) {
    const allDots = document.querySelectorAll('.service-dot');
    allDots.forEach((dot, idx) => {
      if (idx === activeIdx) {
        dot.classList.add('active');
      } else {
        dot.classList.remove('active');
      }
    });
  }

  function selectTab(key, updateIndex = true) {
    const data = SERVICES_DATA[key];
    if (!data) return;

    if (updateIndex) {
      const idx = serviceKeys.indexOf(key);
      if (idx !== -1) currentIndex = idx;
    }

    let activeTabEl = null;
    tabs.forEach(t => {
      if (t.getAttribute('data-service-key') === key) {
        t.classList.add('active');
        activeTabEl = t;
      } else {
        t.classList.remove('active');
      }
    });

    if (activeTabEl) {
      centerActiveCard(activeTabEl);
    }

    updateDots(currentIndex);

    if (certBox) {
      certBox.style.opacity = '0.3';
      certBox.style.transform = 'scale(0.96)';
    }

    setTimeout(() => {
      certImg.src = data.image;
      certImg.alt = data.alt;
      if (titleEl) titleEl.textContent = data.title;
      if (descEl) descEl.textContent = data.desc;
      if (specsEl) specsEl.innerHTML = data.specs.map(s => `<li>✓ ${s}</li>`).join('');

      if (certBox) {
        certBox.style.opacity = '1';
        certBox.style.transform = 'scale(1)';
      }
    }, 120);
  }

  function nextSlide() {
    if (!serviceKeys.length) return;
    currentIndex = (currentIndex + 1) % serviceKeys.length;
    selectTab(serviceKeys[currentIndex], false);
  }

  function prevSlide() {
    if (!serviceKeys.length) return;
    currentIndex = (currentIndex - 1 + serviceKeys.length) % serviceKeys.length;
    selectTab(serviceKeys[currentIndex], false);
  }

  function startAutoplay() {
    stopAutoplay();
    autoplayTimer = setInterval(nextSlide, AUTOPLAY_DELAY_MS);
  }

  function stopAutoplay() {
    if (autoplayTimer) {
      clearInterval(autoplayTimer);
      autoplayTimer = null;
    }
  }

  // Click listeners for tabs
  tabs.forEach(tab => {
    tab.addEventListener('click', () => {
      const key = tab.getAttribute('data-service-key');
      if (key) {
        selectTab(key);
        startAutoplay(); // Reset timer after manual selection
      }
    });
  });

  // Navigation Arrows
  if (prevBtn) {
    prevBtn.addEventListener('click', () => {
      prevSlide();
      startAutoplay();
    });
  }

  if (nextBtn) {
    nextBtn.addEventListener('click', () => {
      nextSlide();
      startAutoplay();
    });
  }

  // Click listeners for position indicator dots
  dots.forEach(dot => {
    dot.addEventListener('click', () => {
      const idx = parseInt(dot.getAttribute('data-index'), 10);
      if (!isNaN(idx) && serviceKeys[idx]) {
        currentIndex = idx;
        selectTab(serviceKeys[currentIndex], false);
        startAutoplay();
      }
    });
  });

  // Pause on hover over carousel track, dots or details panel
  const interactiveZones = [track, panel, prevBtn, nextBtn, dotsContainer].filter(Boolean);
  interactiveZones.forEach(zone => {
    zone.addEventListener('mouseenter', stopAutoplay);
    zone.addEventListener('mouseleave', startAutoplay);
    zone.addEventListener('touchstart', stopAutoplay, { passive: true });
    zone.addEventListener('touchend', startAutoplay, { passive: true });
  });

  // Default selection and start autoplay
  selectTab('pts');
  startAutoplay();
}

/* ==========================================================================
   7. PRODUCTS CATALOG & SEARCH
   ========================================================================== */
function initProductCatalog() {
  const grid = document.getElementById('products-grid');
  const searchInput = document.getElementById('catalog-search-input');
  const pillsContainer = document.getElementById('category-pills-wrap');

  if (!grid || typeof INDAFIRE_PRODUCTS === 'undefined') return;

  let currentCategory = 'all';
  let searchQuery = '';

  if (pillsContainer && typeof PRODUCT_CATEGORIES !== 'undefined') {
    pillsContainer.innerHTML = PRODUCT_CATEGORIES.map(cat => `
      <button type="button" class="category-pill ${cat.id === 'all' ? 'active' : ''}" data-category="${cat.id}">
        ${cat.label}
      </button>
    `).join('');

    const pills = pillsContainer.querySelectorAll('.category-pill');
    pills.forEach(pill => {
      pill.addEventListener('click', () => {
        pills.forEach(p => p.classList.remove('active'));
        pill.classList.add('active');
        currentCategory = pill.getAttribute('data-category') || 'all';
        renderCatalog();
      });
    });
  }

  if (searchInput) {
    searchInput.addEventListener('input', (e) => {
      searchQuery = e.target.value.toLowerCase().trim();
      renderCatalog();
    });
  }

  function renderCatalog() {
    const filtered = INDAFIRE_PRODUCTS.filter(prod => {
      const matchCat = currentCategory === 'all' || prod.category === currentCategory;
      const matchSearch = searchQuery === '' || 
        prod.name.toLowerCase().includes(searchQuery) ||
        prod.shortDesc.toLowerCase().includes(searchQuery) ||
        prod.categoryLabel.toLowerCase().includes(searchQuery);
      return matchCat && matchSearch;
    });

    if (!filtered.length) {
      grid.innerHTML = `
        <div style="grid-column: 1 / -1; text-align: center; padding: 3rem 1rem;">
          <p style="font-size: 1.2rem; color: var(--text-dark-muted); margin-bottom: 1rem;">Nenhum produto encontrado para sua busca.</p>
          <button type="button" class="btn btn-secondary btn-sm" id="btn-clear-search">Limpar Filtros</button>
        </div>
      `;
      const clearBtn = document.getElementById('btn-clear-search');
      if (clearBtn) {
        clearBtn.addEventListener('click', () => {
          if (searchInput) searchInput.value = '';
          searchQuery = '';
          currentCategory = 'all';
          const pills = pillsContainer?.querySelectorAll('.category-pill');
          pills?.forEach(p => p.classList.toggle('active', p.getAttribute('data-category') === 'all'));
          renderCatalog();
        });
      }
      return;
    }

    grid.innerHTML = filtered.map(prod => `
      <div class="product-card reveal">
        <!-- Canvas Showcase -->
        <div class="product-canvas">
          <div class="product-badges-row">
            <span class="product-spec-tag">${prod.badge || 'HOMOLOGADO'}</span>
          </div>
          <div class="product-img-box">
            <img src="${prod.image}" alt="${prod.name}" class="product-img" loading="lazy" />
          </div>
        </div>

        <!-- Content Body -->
        <div class="product-card-body">
          <span class="product-category-tag">${prod.categoryLabel}</span>
          <h3 class="product-card-title">${prod.name}</h3>
          <p class="product-card-summary">${prod.shortDesc}</p>
          
          <div class="product-specs-chip-row">
            ${prod.compliance && prod.compliance[0] ? `<span class="spec-tech-tag">✓ ${prod.compliance[0]}</span>` : ''}
            <span class="spec-tech-tag">Pronta Entrega</span>
          </div>

          <button type="button" class="btn-product-detail-card btn-product-modal" data-product-id="${prod.id}">
            <span>Especificações Técnicas</span>
            <span class="btn-action-arrow">➔</span>
          </button>
        </div>
      </div>
    `).join('');

    // Re-bind modal clicks
    grid.querySelectorAll('.btn-product-modal').forEach(btn => {
      btn.addEventListener('click', () => {
        openProductModal(btn.getAttribute('data-product-id'));
      });
    });

    // Reveal items
    grid.querySelectorAll('.product-card').forEach((c, idx) => {
      setTimeout(() => c.classList.add('active'), idx * 40);
    });
  }

  renderCatalog();
}

/* ==========================================================================
   8. PRODUCT DETAIL MODAL
   ========================================================================== */
function openProductModal(productId) {
  if (typeof INDAFIRE_PRODUCTS === 'undefined') return;
  const product = INDAFIRE_PRODUCTS.find(p => p.id === productId);
  if (!product) return;

  const overlay = document.getElementById('product-modal-overlay');
  const body = document.getElementById('product-modal-body');
  if (!overlay || !body) return;

  body.innerHTML = `
    <div style="display: flex; flex-direction: column; gap: 1.25rem;">
      <div style="display: flex; gap: 1.5rem; align-items: center; flex-wrap: wrap;">
        <div style="width: 150px; height: 150px; background: var(--bg-light); border-radius: var(--radius-sm); display: flex; align-items: center; justify-content: center; padding: 1rem; flex-shrink: 0;">
          <img src="${product.image}" alt="${product.name}" style="max-width: 100%; max-height: 100%; object-fit: contain;" />
        </div>
        <div style="flex: 1; min-width: 220px;">
          <span style="font-family: var(--font-heading); font-size: 0.95rem; font-weight: 800; color: var(--fire-red); text-transform: uppercase;">${product.categoryLabel}</span>
          <h2 style="font-family: var(--font-heading); font-size: 1.9rem; font-weight: 900; text-transform: uppercase; margin: 0.2rem 0;">${product.name}</h2>
          <p style="font-size: 0.95rem; color: var(--text-dark-muted);">${product.shortDesc}</p>
        </div>
      </div>

      <div>
        <h4 style="font-family: var(--font-heading); font-size: 1.2rem; font-weight: 800; text-transform: uppercase; margin-bottom: 0.4rem;">Especificações do Equipamento</h4>
        <p style="font-size: 0.95rem; color: var(--text-dark); line-height: 1.6; margin-bottom: 1rem;">${product.fullDesc}</p>
        <table style="width: 100%; border-collapse: collapse; font-size: 0.9rem;">
          <tbody>
            ${product.specs.map(s => `
              <tr style="border-bottom: 1px solid var(--border-light);">
                <td style="padding: 0.55rem 0; font-weight: 600; color: var(--text-dark);">${s.label}</td>
                <td style="padding: 0.55rem 0; text-align: right; color: var(--text-dark-muted);">${s.value}</td>
              </tr>
            `).join('')}
          </tbody>
        </table>
      </div>

      <div style="padding-top: 1.25rem; border-top: 1px solid var(--border-light); display: flex; gap: 1rem;">
        <a href="https://wa.me/551938341741?text=Ol%C3%A1,%20gostaria%20de%20solicitar%20uma%20cota%C3%A7%C3%A3o%20técnica%20do%20produto:%20${encodeURIComponent(product.name)}" target="_blank" rel="noopener noreferrer" class="btn btn-whatsapp btn-block">
          Solicitar Cotação no WhatsApp
        </a>
      </div>
    </div>
  `;

  overlay.classList.add('open');
}

/* ==========================================================================
   9. MODALS & GENERAL OVERLAYS
   ========================================================================== */
function initModals() {
  document.addEventListener('click', (e) => {
    if (e.target.classList.contains('modal-overlay') || e.target.closest('.modal-close-btn')) {
      document.querySelectorAll('.modal-overlay').forEach(m => m.classList.remove('open'));
    }
  });

  document.addEventListener('keydown', (e) => {
    if (e.key === 'Escape') {
      document.querySelectorAll('.modal-overlay').forEach(m => m.classList.remove('open'));
    }
  });

  // Client Area Button
  const clientBtns = document.querySelectorAll('.btn-client-modal');
  const clientOverlay = document.getElementById('client-modal-overlay');
  clientBtns.forEach(b => {
    b.addEventListener('click', (e) => {
      e.preventDefault();
      if (clientOverlay) clientOverlay.classList.add('open');
    });
  });
}

/* ==========================================================================
   10. QUOTE FORM & WHATSAPP
   ========================================================================== */
function initQuoteForm() {
  const form = document.getElementById('quote-form');
  
  // CTA: Header "Solicitar Orçamento"
  document.querySelectorAll('.btn-header-quote').forEach(btn => {
    btn.addEventListener('click', (e) => {
      const href = btn.getAttribute('href');
      if (href && href.includes('#contato')) {
        const contactSection = document.getElementById('contato');
        if (contactSection) {
          e.preventDefault();
          contactSection.scrollIntoView({ behavior: 'smooth' });
          const nameInput = document.getElementById('form-name');
          if (nameInput) setTimeout(() => nameInput.focus(), 500);
        }
      }
    });
  });

  // CTA: "Agendar Agora Mesmo" Treinamento
  document.querySelectorAll('.btn-training-schedule').forEach(btn => {
    btn.addEventListener('click', (e) => {
      const contactSection = document.getElementById('contato');
      if (contactSection) {
        e.preventDefault();
        contactSection.scrollIntoView({ behavior: 'smooth' });
        const select = document.getElementById('form-service');
        if (select) {
          select.value = 'Treinamento de Brigada de Incêndio';
        }
        const nameInput = document.getElementById('form-name');
        if (nameInput) setTimeout(() => nameInput.focus(), 500);
      }
    });
  });

  if (!form) return;

  form.addEventListener('submit', (e) => {
    e.preventDefault();
    const name = form.querySelector('#form-name')?.value.trim();
    const company = form.querySelector('#form-company')?.value.trim();
    const phone = form.querySelector('#form-phone')?.value.trim();
    const email = form.querySelector('#form-email')?.value.trim();
    const service = form.querySelector('#form-service')?.value;
    const msg = form.querySelector('#form-message')?.value.trim();

    if (!name || !phone || !email || !service) {
      alert('Por favor, preencha os campos obrigatórios (Nome, Telefone, E-mail e Serviço).');
      return;
    }

    let text = `*SOLICITAÇÃO DE ATENDIMENTO - INDA FIRE*\n\n` +
      `*Nome:* ${name}\n` +
      (company ? `*Empresa:* ${company}\n` : '') +
      `*Telefone:* ${phone}\n` +
      `*E-mail:* ${email}\n` +
      `*Assunto / Serviço:* ${service}\n` +
      (msg ? `*Mensagem:* ${msg}` : '');

    window.open(`https://wa.me/551938341741?text=${encodeURIComponent(text)}`, '_blank');
    form.reset();
  });
}

/* ==========================================================================
   11. FLOATING WHATSAPP WIDGET
   ========================================================================== */
function initWhatsAppWidget() {
  const btn = document.getElementById('floating-whatsapp-btn');
  if (!btn) return;
  btn.addEventListener('click', () => {
    window.open('https://wa.me/551938341741?text=Ol%C3%A1,%20gostaria%20de%20informa%C3%A7%C3%B5es%20sobre%20os%20servi%C3%A7os%20da%20Inda%20Fire', '_blank');
  });
}

/* ==========================================================================
   12. EXPERTISE MATRIX & INTERACTIVE SEQUENTIAL ANIMATION
   ========================================================================== */
function initExpertiseCarousel() {
  const items = document.querySelectorAll('.expertise-matrix-item');
  if (!items.length) return;

  let currentIndex = 0;
  let isHovered = false;
  let cycleTimer = null;
  const cycleDuration = 4800; // 4.8s per capability (smooth & calm)

  function setActive(index) {
    currentIndex = index;
    items.forEach((item, idx) => {
      item.classList.toggle('active-highlight', idx === currentIndex);
    });
  }

  function nextStep() {
    if (isHovered) return;
    currentIndex = (currentIndex + 1) % items.length;
    setActive(currentIndex);
  }

  function startCycle() {
    if (cycleTimer) clearInterval(cycleTimer);
    cycleTimer = setInterval(nextStep, cycleDuration);
  }

  function stopCycle() {
    if (cycleTimer) {
      clearInterval(cycleTimer);
      cycleTimer = null;
    }
  }

  // Hover & Click events
  items.forEach((item, idx) => {
    item.addEventListener('mouseenter', () => {
      isHovered = true;
      setActive(idx);
    });

    item.addEventListener('mouseleave', () => {
      isHovered = false;
    });

    item.addEventListener('click', () => {
      isHovered = true;
      setActive(idx);
      setTimeout(() => { isHovered = false; }, 3000);
    });

    // Touch support for mobile/tablets
    item.addEventListener('touchstart', () => {
      isHovered = true;
      setActive(idx);
    }, { passive: true });
  });

  // IntersectionObserver: only cycle when section is visible
  const section = document.getElementById('diferenciais') || document.querySelector('.expertise-section');
  if (section && 'IntersectionObserver' in window) {
    const observer = new IntersectionObserver((entries) => {
      entries.forEach(entry => {
        if (entry.isIntersecting) {
          startCycle();
        } else {
          stopCycle();
        }
      });
    }, { threshold: 0.15 });
    observer.observe(section);
  } else {
    startCycle();
  }

  // Set initial active state on first item
  setActive(0);
}

/* ==========================================================================
   13. MISSÃO, VISÃO E VALORES (MVV) INTERACTIVE SEQUENTIAL ANIMATION
   ========================================================================== */
function initMVVCarousel() {
  const cards = document.querySelectorAll('.mvv-card');
  if (!cards.length) return;

  let currentIndex = 0;
  let isHovered = false;
  let cycleTimer = null;
  const cycleDuration = 5200; // 5.2s per card (calm, noble pace)

  function setActive(index) {
    currentIndex = index;
    cards.forEach((card, idx) => {
      card.classList.toggle('active-highlight', idx === currentIndex);
    });
  }

  function nextStep() {
    if (isHovered) return;
    currentIndex = (currentIndex + 1) % cards.length;
    setActive(currentIndex);
  }

  function startCycle() {
    if (cycleTimer) clearInterval(cycleTimer);
    cycleTimer = setInterval(nextStep, cycleDuration);
  }

  function stopCycle() {
    if (cycleTimer) {
      clearInterval(cycleTimer);
      cycleTimer = null;
    }
  }

  cards.forEach((card, idx) => {
    card.addEventListener('mouseenter', () => {
      isHovered = true;
      setActive(idx);
    });

    card.addEventListener('mouseleave', () => {
      isHovered = false;
    });

    card.addEventListener('click', () => {
      isHovered = true;
      setActive(idx);
      setTimeout(() => { isHovered = false; }, 2500);
    });

    card.addEventListener('touchstart', () => {
      isHovered = true;
      setActive(idx);
    }, { passive: true });
  });

  const section = document.getElementById('missao-visao-valores') || document.querySelector('.mvv-section');
  if (section && 'IntersectionObserver' in window) {
    const observer = new IntersectionObserver((entries) => {
      entries.forEach(entry => {
        if (entry.isIntersecting) {
          startCycle();
        } else {
          stopCycle();
        }
      });
    }, { threshold: 0.15 });
    observer.observe(section);
  } else {
    startCycle();
  }

  setActive(0);
}

/* ==========================================================================
   14. INDA FIRE TIMELINE DATA & PROGRESSIVE STEPPER ENGINE
   ========================================================================== */
const INDAFIRE_TIMELINE_DATA = [
  {
    id: 0,
    year: "1996",
    tag: "FUNDAÇÃO & PIONEIRISMO",
    title: "Fundação da Inda Fire em Indaiatuba",
    location: "Avenida Presidente Kennedy — Indaiatuba/SP",
    shortDesc: "Início das atividades com veículo próprio e foco em assessoria e manutenção preventiva contra incêndios.",
    fullDesc: "A Inda Fire nasceu em 1996 impulsionada pelo compromisso inegociável de proteger vidas e patrimônios. Com seu primeiro veículo utilitário e atendimento técnico dedicado, a empresa iniciou suas operações na Av. Presidente Kennedy, prestando serviços especializados de manutenção de extintores e assessoria preventiva para indústrias e comércios de Indaiatuba e região.",
    image: "assets/img/timeline_1996.png",
    highlights: [
      "Início das operações em Indaiatuba/SP",
      "Frota inicial de coleta e entrega rápida",
      "Assessoria técnica especializada",
      "Pioneirismo em segurança patrimonial"
    ]
  },
  {
    id: 1,
    year: "1997–2007",
    tag: "EXPANSÃO COMERCIAL & CONSOLIDAÇÃO",
    title: "Loja & Oficina na Rua Barão de Taunay",
    location: "Rua Barão de Taunay — Indaiatuba/SP",
    shortDesc: "Sede da empresa durante uma década de consolidação técnica, abertura de balcão e ampliação da linha de equipamentos.",
    fullDesc: "Durante dez anos decisivos, a Inda Fire consolidou sua reputação técnica operando na Rua Barão de Taunay. O período foi marcado pela inauguração do primeiro balcão de atendimento direto ao cliente, expansão do portfólio para comercialização de mangueiras, hidrantes, sinalização fotoluminescente e equipamentos de proteção (EPI/EPC).",
    image: "assets/img/timeline_1997_2007.png",
    highlights: [
      "Primeiro showroom e balcão técnico aberto ao público",
      "Ampliação do catálogo de EPIs e sinalização",
      "Oficina própria de manutenção e recarga",
      "Parcerias industriais consolidadas no interior de SP"
    ]
  },
  {
    id: 2,
    year: "2008",
    tag: "HOMOLOGAÇÃO & CONFORMIDADE RTB",
    title: "1º Registro Oficial Inmetro da Região",
    location: "Registro Oficial Inmetro nº 002874 (Portaria nº 173)",
    shortDesc: "Conquista do registro pioneiro do Inmetro nº 002874 para manutenção de extintores de Pó, Água, CO2 e Espuma.",
    fullDesc: "Em 2008, a Inda Fire alcançou um marco histórico: tornou-se a primeira empresa de Indaiatuba e região a conquistar o Registro de Declaração de Conformidade do Inmetro (nº 002874 / RTB) para manutenção de 1º, 2º e 3º níveis em extintores de Pó Químico, Água Pressurizada, Dióxido de Carbono (CO2) e Espuma Mecânica, garantindo máxima rastreabilidade e segurança normativa.",
    image: "assets/img/timeline_2008_inmetro.png",
    highlights: [
      "1ª empresa da região certificada pelo Inmetro",
      "Registro compulsório oficial nº 002874",
      "Bancada técnica aferida e selos invioláveis",
      "Conformidade total com a Portaria Inmetro nº 173"
    ]
  },
  {
    id: 3,
    year: "2008–2018",
    tag: "EXPANSÃO INDUSTRIAL & INFRAESTRUTURA",
    title: "Parque Fabril na Av. Francisco de Paula Leite",
    location: "Av. Francisco de Paula Leite, 1034 — Indaiatuba/SP",
    shortDesc: "Estrutura fabril expandida para mais de 800 m², bancada de teste hidrostático e triplicação da capacidade produtiva.",
    fullDesc: "Para atender à crescente demanda de grandes polos industriais, a Inda Fire transferiu seu parque operacional para a Av. Francisco de Paula Leite. A nova planta fabril contou com maquinário de pressurização de alta velocidade, estufas térmicas para ensaio hidrostático de mangueiras conforme NBR 11861 e ampliação substancial da frota logística.",
    image: "assets/img/timeline_2008_2018.png",
    highlights: [
      "Área industrial ampla com mais de 800 m²",
      "Ensaio hidrostático de mangueiras (NBR 11861)",
      "Capacidade de recarga triplicada em escala seriada",
      "Frota própria para rotas corporativas expressas"
    ]
  },
  {
    id: 4,
    year: "2018",
    tag: "SEDE PRÓPRIA & CENTRO TECNOLÓGICO",
    title: "Inauguração do Complexo Sede Própria",
    location: "Rua Emílio Lopes Cruz, 420 — Jd. Belo Horizonte, Indaiatuba/SP",
    shortDesc: "Inauguração do moderno complexo corporativo com centro de treinamentos práticos de brigada e docas de carga rápida.",
    fullDesc: "Em 2018, a Inda Fire inaugurou sua imponente sede própria construída especificamente para engenharia contra incêndios no Jardim Belo Horizonte. Projetada com docas de logística rápida, oficina automatizada de recargas de alta pressão e centro de formação de brigadistas com simuladores reais de combate a incêndio.",
    image: "assets/img/timeline_2018_sede_propria.png",
    highlights: [
      "Complexo próprio com infraestrutura de ponta",
      "Centro de Treinamento e simulador de fogo real",
      "Oficina de alta pressão com tecnologia limpa",
      "Localização estratégica com acesso direto às rodovias"
    ]
  },
  {
    id: 5,
    year: "2024 — Hoje",
    tag: "LIDERANÇA & SOLUÇÕES INTEGRADAS 360°",
    title: "Liderança Nacional & Ecossistema de Proteção",
    location: "Atendimento Estadual e Nacional — +30 Anos",
    shortDesc: "Mais de 12.000 clientes corporativos ativos e mais de 18.500 brigadistas capacitados em mais de 30 anos de história.",
    fullDesc: "Hoje, com mais de 30 anos de história sólida, a Inda Fire é referência absoluta em soluções 360° de proteção contra incêndios: elaboração de projetos técnicos AVCB/CLCB, inspeções periciais, assessoria contínua, manutenção Inmetro e formação de mais de 18.500 brigadistas para as maiores empresas do Brasil.",
    image: "assets/img/sede_empresa_banner.png",
    highlights: [
      "+30 Anos de história e credibilidade",
      "+12.000 Clientes corporativos atendidos",
      "+18.500 Brigadistas capacitados",
      "Soluções completas: AVCB, Manutenção e Treinamento"
    ]
  }
];

let activeTimelineModalIndex = 0;

function initTimelineCarousel() {
  const scrollBox = document.getElementById('timeline-scroll-container');
  const cells = document.querySelectorAll('.timeline-node-cell:not(.empty-cell)');
  const segments = document.querySelectorAll('.rail-segment');
  const total = cells.length;
  
  if (!cells.length || !segments.length) return;

  let currentIndex = 0;
  let isPaused = false;
  let progress = 0; // 0 to 100
  const stepDurationMs = 5800; // 5.8 seconds per step (smooth, dignified pace)
  let lastTimestamp = null;
  let animFrameId = null;

  function updateVisualState(index, fillPercent = 0) {
    currentIndex = index;

    // Update node cells
    cells.forEach(cell => {
      const cellIdx = parseInt(cell.getAttribute('data-index'), 10);
      cell.classList.toggle('active', cellIdx === currentIndex);
    });

    // Update central rail segments
    segments.forEach((seg) => {
      const segIdx = parseInt(seg.getAttribute('data-index'), 10);
      const fill = seg.querySelector('.rail-segment-fill');
      
      if (segIdx < currentIndex) {
        seg.classList.remove('active');
        seg.classList.add('completed');
        if (fill) fill.style.width = '100%';
      } else if (segIdx === currentIndex) {
        seg.classList.add('active');
        seg.classList.remove('completed');
        if (fill) fill.style.width = `${Math.min(100, Math.max(0, fillPercent))}%`;
      } else {
        seg.classList.remove('active', 'completed');
        if (fill) fill.style.width = '0%';
      }
    });

    // Smoothly keep active cell in view if container is scrollable
    const activeCell = Array.from(cells).find(c => parseInt(c.getAttribute('data-index'), 10) === currentIndex);
    if (activeCell && scrollBox) {
      const containerLeft = scrollBox.getBoundingClientRect().left;
      const cellLeft = activeCell.getBoundingClientRect().left;
      const offset = cellLeft - containerLeft - (scrollBox.clientWidth / 2) + (activeCell.clientWidth / 2);
      if (Math.abs(offset) > 40) {
        scrollBox.scrollBy({ left: offset, behavior: 'smooth' });
      }
    }
  }

  function step(timestamp) {
    if (!lastTimestamp) lastTimestamp = timestamp;
    const delta = timestamp - lastTimestamp;
    lastTimestamp = timestamp;

    const modalEl = document.getElementById('timeline-history-modal');
    const isModalOpen = modalEl && modalEl.classList.contains('open');

    if (!isPaused && !isModalOpen) {
      progress += (delta / stepDurationMs) * 100;
      if (progress >= 100) {
        progress = 0;
        currentIndex = (currentIndex + 1) % total;
        updateVisualState(currentIndex, 0);
      } else {
        const activeSeg = Array.from(segments).find(s => parseInt(s.getAttribute('data-index'), 10) === currentIndex);
        const activeFill = activeSeg ? activeSeg.querySelector('.rail-segment-fill') : null;
        if (activeFill) {
          activeFill.style.width = `${progress}%`;
        }
      }
    }

    animFrameId = requestAnimationFrame(step);
  }

  function goToStep(index) {
    if (index < 0) index = total - 1;
    if (index >= total) index = 0;
    currentIndex = index;
    progress = 0;
    lastTimestamp = performance.now();
    updateVisualState(currentIndex, 0);
  }

  window.goToTimelineStep = goToStep;

  // Click on cell or card
  cells.forEach(cell => {
    cell.addEventListener('click', (e) => {
      const idx = parseInt(cell.getAttribute('data-index'), 10);
      goToStep(idx);
      // Open modal when clicking anywhere on the info card or cell
      if (e.target.closest('.timeline-info-card') || e.target.closest('.timeline-card-link-cta') || e.target.closest('.timeline-card-zoom-badge')) {
        openTimelineModal(idx);
      }
    });
  });

  // Click on rail segment
  segments.forEach(seg => {
    seg.addEventListener('click', () => {
      const idx = parseInt(seg.getAttribute('data-index'), 10);
      goToStep(idx);
    });
  });

  // Continuous playback: timeline never stops on mouse hover
  // (Pausado apenas quando o modal de detalhes estiver aberto)

  // Start engine
  updateVisualState(0, 0);
  animFrameId = requestAnimationFrame(step);

  // Initialize Timeline Modal listeners
  initTimelineModal();
}

let isTimelineModalAnimating = false;

function buildTimelineModalHTML(data) {
  return `
    <div class="thm-visual-col">
      <span class="thm-year-pill-overlay">${data.year}</span>
      <img src="${data.image}" alt="${data.title}" />
    </div>

    <div class="thm-content-col">
      <span class="thm-tag-label">
        <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><path d="M12 2L2 7l10 5 10-5-10-5zM2 17l10 5 10-5M2 12l10 5 10-5"/></svg>
        ${data.tag}
      </span>
      <h2 class="thm-title" id="thm-title">${data.title}</h2>
      
      <div class="thm-location-badge">
        <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M21 10c0 7-9 13-9 13s-9-6-9-13a9 9 0 0 1 18 0z"/><circle cx="12" cy="10" r="3"/></svg>
        <span>${data.location}</span>
      </div>

      <p class="thm-narrative">${data.fullDesc}</p>

      <div class="thm-highlights-list">
        ${data.highlights.map(h => `
          <div class="thm-highlight-chip">
            <span>✓ ${h}</span>
          </div>
        `).join('')}
      </div>
    </div>
  `;
}

function updateTimelineModalDots(index) {
  const dotsContainer = document.getElementById('timeline-modal-dots');
  if (!dotsContainer || typeof INDAFIRE_TIMELINE_DATA === 'undefined') return;

  dotsContainer.innerHTML = INDAFIRE_TIMELINE_DATA.map((_, dIdx) => `
    <span class="thm-dot ${dIdx === index ? 'active' : ''}" data-dot-idx="${dIdx}"></span>
  `).join('');

  dotsContainer.querySelectorAll('.thm-dot').forEach(dot => {
    dot.addEventListener('click', () => {
      const targetIdx = parseInt(dot.getAttribute('data-dot-idx'), 10);
      slideTimelineModal(targetIdx);
    });
  });
}

function openTimelineModal(index) {
  const overlay = document.getElementById('timeline-history-modal');
  const content = document.getElementById('timeline-modal-content');
  if (!overlay || !content || typeof INDAFIRE_TIMELINE_DATA === 'undefined') return;

  const total = INDAFIRE_TIMELINE_DATA.length;
  if (index < 0) index = total - 1;
  if (index >= total) index = 0;
  activeTimelineModalIndex = index;

  const data = INDAFIRE_TIMELINE_DATA[activeTimelineModalIndex];
  if (!data) return;

  content.className = 'timeline-modal-inner thm-slide-active';
  content.innerHTML = buildTimelineModalHTML(data);
  updateTimelineModalDots(activeTimelineModalIndex);

  overlay.classList.add('open');
  document.body.style.overflow = 'hidden';
}

function slideTimelineModal(targetIndex, direction) {
  const overlay = document.getElementById('timeline-history-modal');
  const content = document.getElementById('timeline-modal-content');
  if (!overlay || !content || typeof INDAFIRE_TIMELINE_DATA === 'undefined') return;

  if (!overlay.classList.contains('open')) {
    openTimelineModal(targetIndex);
    return;
  }

  if (isTimelineModalAnimating) return;

  const total = INDAFIRE_TIMELINE_DATA.length;
  if (targetIndex < 0) targetIndex = total - 1;
  if (targetIndex >= total) targetIndex = 0;
  if (targetIndex === activeTimelineModalIndex) return;

  if (!direction) {
    direction = (targetIndex > activeTimelineModalIndex || (activeTimelineModalIndex === total - 1 && targetIndex === 0)) ? 'next' : 'prev';
  }

  isTimelineModalAnimating = true;
  const outClass = direction === 'next' ? 'thm-slide-out-left' : 'thm-slide-out-right';
  const inClass = direction === 'next' ? 'thm-slide-in-right' : 'thm-slide-in-left';

  content.className = `timeline-modal-inner ${outClass}`;

  setTimeout(() => {
    activeTimelineModalIndex = targetIndex;
    const nextData = INDAFIRE_TIMELINE_DATA[activeTimelineModalIndex];
    content.innerHTML = buildTimelineModalHTML(nextData);
    updateTimelineModalDots(activeTimelineModalIndex);

    content.className = `timeline-modal-inner ${inClass}`;
    void content.offsetWidth;

    requestAnimationFrame(() => {
      content.className = 'timeline-modal-inner thm-slide-active';
    });

    setTimeout(() => {
      isTimelineModalAnimating = false;
    }, 380);
  }, 160);
}

function closeTimelineModal() {
  const overlay = document.getElementById('timeline-history-modal');
  if (overlay) {
    overlay.classList.remove('open');
    document.body.style.overflow = '';
  }
}

function initTimelineModal() {
  const btnClose = document.getElementById('btn-close-timeline-modal');
  const btnPrev = document.getElementById('btn-timeline-modal-prev');
  const btnNext = document.getElementById('btn-timeline-modal-next');
  const overlay = document.getElementById('timeline-history-modal');
  const content = document.getElementById('timeline-modal-content');

  if (btnClose) btnClose.addEventListener('click', closeTimelineModal);

  if (btnPrev) {
    btnPrev.addEventListener('click', (e) => {
      e.stopPropagation();
      slideTimelineModal(activeTimelineModalIndex - 1, 'prev');
    });
  }

  if (btnNext) {
    btnNext.addEventListener('click', (e) => {
      e.stopPropagation();
      slideTimelineModal(activeTimelineModalIndex + 1, 'next');
    });
  }

  if (overlay) {
    overlay.addEventListener('click', (e) => {
      if (e.target === overlay) closeTimelineModal();
    });
  }

  if (content) {
    let touchStartX = 0;
    let touchEndX = 0;

    content.addEventListener('touchstart', (e) => {
      touchStartX = e.changedTouches[0].screenX;
    }, { passive: true });

    content.addEventListener('touchend', (e) => {
      touchEndX = e.changedTouches[0].screenX;
      const diffX = touchStartX - touchEndX;
      if (Math.abs(diffX) > 45) {
        if (diffX > 0) {
          slideTimelineModal(activeTimelineModalIndex + 1, 'next');
        } else {
          slideTimelineModal(activeTimelineModalIndex - 1, 'prev');
        }
      }
    }, { passive: true });
  }

  document.addEventListener('keydown', (e) => {
    if (overlay && overlay.classList.contains('open')) {
      if (e.key === 'Escape') closeTimelineModal();
      if (e.key === 'ArrowLeft') slideTimelineModal(activeTimelineModalIndex - 1, 'prev');
      if (e.key === 'ArrowRight') slideTimelineModal(activeTimelineModalIndex + 1, 'next');
    }
  });
}

/* ==========================================================================
   TRAINING VIDEO CONTROLS (AUTOPLAY LOOP + UNMUTE & PLAY/PAUSE)
   ========================================================================== */
function initTrainingVideoControls() {
  const video = document.getElementById('trainingVideo');
  const btnSound = document.getElementById('btnToggleSound');
  const btnPlay = document.getElementById('btnTogglePlay');

  if (!video) return;

  if (btnSound) {
    btnSound.addEventListener('click', (e) => {
      e.stopPropagation();
      video.muted = !video.muted;
      const mutedIcon = btnSound.querySelector('.sound-icon-muted');
      const unmutedIcon = btnSound.querySelector('.sound-icon-unmuted');
      if (video.muted) {
        if (mutedIcon) mutedIcon.style.display = 'block';
        if (unmutedIcon) unmutedIcon.style.display = 'none';
        btnSound.setAttribute('aria-label', 'Ativar Som');
      } else {
        if (mutedIcon) mutedIcon.style.display = 'none';
        if (unmutedIcon) unmutedIcon.style.display = 'block';
        btnSound.setAttribute('aria-label', 'Desativar Som');
      }
    });
  }

  if (btnPlay) {
    btnPlay.addEventListener('click', (e) => {
      e.stopPropagation();
      const pauseIcon = btnPlay.querySelector('.play-icon-pause');
      const playIcon = btnPlay.querySelector('.play-icon-play');
      if (video.paused) {
        video.play();
        if (pauseIcon) pauseIcon.style.display = 'block';
        if (playIcon) playIcon.style.display = 'none';
        btnPlay.setAttribute('aria-label', 'Pausar Vídeo');
      } else {
        video.pause();
        if (pauseIcon) pauseIcon.style.display = 'none';
        if (playIcon) playIcon.style.display = 'block';
        btnPlay.setAttribute('aria-label', 'Reproduzir Vídeo');
      }
    });
  }
}

