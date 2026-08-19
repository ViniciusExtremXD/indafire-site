/**
 * INDA FIRE — CATALOG PAGE JAVASCRIPT ENGINE
 * Full Filtering, Live Search, URL Params, Category Tabs, Sidebar & Modals
 */

import { PRODUCT_CATEGORIES, PRODUCTS } from './catalog-data.js';

document.addEventListener('DOMContentLoaded', () => {
  initCatalogPage();
  initDrawerNav();
  initHeaderScroll();
  initMegaMenuNav();
  initClientModal();
});

function initClientModal() {
  const clientBtns = document.querySelectorAll('.btn-client-modal');
  const clientOverlay = document.getElementById('client-modal-overlay');
  if (!clientOverlay) return;

  clientBtns.forEach(btn => {
    btn.addEventListener('click', (e) => {
      e.preventDefault();
      clientOverlay.classList.add('open');
    });
  });

  const closeBtn = clientOverlay.querySelector('.modal-close-btn');
  if (closeBtn) {
    closeBtn.addEventListener('click', () => clientOverlay.classList.remove('open'));
  }

  clientOverlay.addEventListener('click', (e) => {
    if (e.target === clientOverlay) clientOverlay.classList.remove('open');
  });

  document.addEventListener('keydown', (e) => {
    if (e.key === 'Escape' && clientOverlay.classList.contains('open')) {
      clientOverlay.classList.remove('open');
    }
  });
}

function initHeaderScroll() {
  const header = document.getElementById('site-header');
  const progressBar = document.getElementById('scroll-progress');
  if (!header) return;

  function onScroll() {
    const scrollTop = window.scrollY || document.documentElement.scrollTop;
    const scrollHeight = document.documentElement.scrollHeight - document.documentElement.clientHeight;
    
    // Progress Bar
    if (progressBar && scrollHeight > 0) {
      progressBar.style.width = `${(scrollTop / scrollHeight) * 100}%`;
    }

    // Glassmorphism Header state on scroll
    if (scrollTop > 30) {
      header.classList.add('scrolled');
    } else {
      header.classList.remove('scrolled');
    }
  }

  window.addEventListener('scroll', onScroll, { passive: true });
  onScroll();
}

function initMegaMenuNav() {
  const dropdowns = document.querySelectorAll('.nav-item-dropdown');
  const header = document.getElementById('site-header');

  dropdowns.forEach(d => {
    const panel = d.querySelector('.mega-menu-panel');
    if (!panel) return;

    let timeout;

    function openMenu() {
      clearTimeout(timeout);
      dropdowns.forEach(other => {
        if (other !== d) other.querySelector('.mega-menu-panel')?.classList.remove('active');
      });
      panel.classList.add('active');
      if (header) header.classList.add('has-mega-open');
    }

    function closeMenu() {
      timeout = setTimeout(() => {
        panel.classList.remove('active');
        if (header) header.classList.remove('has-mega-open');
      }, 150);
    }

    d.addEventListener('mouseenter', openMenu);
    d.addEventListener('mouseleave', closeMenu);
    panel.addEventListener('mouseenter', openMenu);
    panel.addEventListener('mouseleave', closeMenu);
  });
}

function initDrawerNav() {
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


function initCatalogPage() {
  const tabsBar = document.getElementById('catalog-tabs-bar');
  const sidebarList = document.getElementById('sidebar-category-list');
  const productsGrid = document.getElementById('products-grid-container');
  const searchInput = document.getElementById('live-catalog-search');
  const clearSearchBtn = document.getElementById('clear-search-btn');
  const visibleCountEl = document.getElementById('visible-count');
  const activeCatNameEl = document.getElementById('active-cat-name');
  const activeCatBadgeEl = document.getElementById('active-cat-badge');
  const emptyStateEl = document.getElementById('catalog-empty-state');
  const resetFiltersBtn = document.getElementById('btn-reset-filters');
  
  // Modal Elements
  const modalBackdrop = document.getElementById('product-detail-modal');
  const modalContent = document.getElementById('modal-product-content');
  const modalCloseBtn = document.getElementById('modal-close-btn');

  // Check URL parameters for initial category or search
  const urlParams = new URLSearchParams(window.location.search);
  let activeCategory = urlParams.get('cat') || 'todos';
  let searchTerm = urlParams.get('q') || '';

  if (searchInput && searchTerm) {
    searchInput.value = searchTerm;
    if (clearSearchBtn) clearSearchBtn.style.display = 'block';
  }

  // 1. Render Category Tabs (Top Bar)
  if (tabsBar) {
    tabsBar.innerHTML = PRODUCT_CATEGORIES.map(cat => `
      <button type="button" class="catalog-tab-btn ${cat.id === activeCategory ? 'active' : ''}" data-category="${cat.id}">
        <span>${cat.name}</span>
      </button>
    `).join('');

    tabsBar.addEventListener('click', (e) => {
      const btn = e.target.closest('.catalog-tab-btn');
      if (btn) {
        activeCategory = btn.getAttribute('data-category');
        updateCatalogView();
      }
    });
  }

  // 2. Render Sidebar Categories
  if (sidebarList) {
    sidebarList.innerHTML = PRODUCT_CATEGORIES.map(cat => {
      const isAct = cat.id === activeCategory;
      const count = cat.id === 'todos' ? PRODUCTS.length : PRODUCTS.filter(p => p.category === cat.id).length;
      return `
        <li class="sidebar-cat-item ${isAct ? 'active' : ''}" data-category="${cat.id}">
          <span class="cat-name">${cat.name}</span>
          <span class="cat-count">${count}</span>
        </li>
      `;
    }).join('');

    sidebarList.addEventListener('click', (e) => {
      const item = e.target.closest('.sidebar-cat-item');
      if (item) {
        activeCategory = item.getAttribute('data-category');
        updateCatalogView();
      }
    });
  }

  // 3. Render and Filter Products
  function updateCatalogView() {
    // Update Tab UI
    document.querySelectorAll('.catalog-tab-btn').forEach(btn => {
      btn.classList.toggle('active', btn.getAttribute('data-category') === activeCategory);
    });

    // Update Sidebar UI
    document.querySelectorAll('.sidebar-cat-item').forEach(item => {
      item.classList.toggle('active', item.getAttribute('data-category') === activeCategory);
    });

    // Filter array
    const query = (searchInput ? searchInput.value.toLowerCase().trim() : '');
    
    let filtered = PRODUCTS.filter(prod => {
      const matchCat = (activeCategory === 'todos') || (prod.category === activeCategory);
      const matchQuery = !query || 
        prod.name.toLowerCase().includes(query) ||
        prod.shortDesc.toLowerCase().includes(query) ||
        prod.badge.toLowerCase().includes(query) ||
        (prod.compliance && prod.compliance.some(c => c.toLowerCase().includes(query))) ||
        (prod.specs && Object.values(prod.specs).some(v => String(v).toLowerCase().includes(query)));
      return matchCat && matchQuery;
    });

    // Update stats & category title
    if (visibleCountEl) visibleCountEl.textContent = filtered.length;
    
    const curCatObj = PRODUCT_CATEGORIES.find(c => c.id === activeCategory) || PRODUCT_CATEGORIES[0];
    if (activeCatNameEl) activeCatNameEl.textContent = query ? `Resultados para "${query}"` : curCatObj.name;
    if (activeCatBadgeEl) activeCatBadgeEl.textContent = `${filtered.length} EQUIPAMENTOS`;

    // Render Products Grid
    if (productsGrid) {
      if (filtered.length === 0) {
        productsGrid.innerHTML = '';
        if (emptyStateEl) emptyStateEl.style.display = 'block';
      } else {
        if (emptyStateEl) emptyStateEl.style.display = 'none';
        productsGrid.innerHTML = filtered.map(prod => `
          <div class="product-card" data-product-id="${prod.id}">
            <div class="product-canvas">
              <div class="product-badges-row">
                <span class="product-spec-tag">${prod.badge || 'HOMOLOGADO'}</span>
              </div>
              <div class="product-img-box">
                <img src="${prod.image}" alt="${prod.name}" class="product-img" loading="lazy" />
              </div>
            </div>

            <div class="product-card-body">
              <span class="product-category-tag">${prod.categoryLabel}</span>
              <h3 class="product-card-title">${prod.name}</h3>
              <p class="product-card-summary">${prod.shortDesc}</p>

              <div class="product-specs-chip-row">
                ${prod.compliance && prod.compliance[0] ? `<span class="spec-tech-tag">✓ ${prod.compliance[0]}</span>` : ''}
                <span class="spec-tech-tag">Pronta Entrega</span>
              </div>

              <button type="button" class="btn-product-detail-card btn-open-modal" data-product-id="${prod.id}">
                <span>Especificações Técnicas</span>
                <span class="btn-action-arrow">➔</span>
              </button>
            </div>
          </div>
        `).join('');
      }
    }

    // Update URL history without reload
    const newUrl = new URL(window.location);
    if (activeCategory !== 'todos') newUrl.searchParams.set('cat', activeCategory);
    else newUrl.searchParams.delete('cat');
    if (query) newUrl.searchParams.set('q', query);
    else newUrl.searchParams.delete('q');
    window.history.replaceState({}, '', newUrl);
  }

  // 4. Live Search Input Handlers
  if (searchInput) {
    searchInput.addEventListener('input', () => {
      if (clearSearchBtn) {
        clearSearchBtn.style.display = searchInput.value.length > 0 ? 'block' : 'none';
      }
      updateCatalogView();
    });
  }

  if (clearSearchBtn) {
    clearSearchBtn.addEventListener('click', () => {
      if (searchInput) searchInput.value = '';
      clearSearchBtn.style.display = 'none';
      updateCatalogView();
    });
  }

  if (resetFiltersBtn) {
    resetFiltersBtn.addEventListener('click', () => {
      activeCategory = 'todos';
      if (searchInput) searchInput.value = '';
      if (clearSearchBtn) clearSearchBtn.style.display = 'none';
      updateCatalogView();
    });
  }

  // 5. Open Product Specification Modal
  document.addEventListener('click', (e) => {
    const btn = e.target.closest('.btn-open-modal');
    if (btn) {
      const prodId = btn.getAttribute('data-product-id');
      const prod = PRODUCTS.find(p => p.id === prodId);
      if (prod && modalContent && modalBackdrop) {
        const specsRows = prod.specs ? Object.entries(prod.specs).map(([k, v]) => `
          <div class="modal-spec-row">
            <span class="modal-spec-label">${formatSpecKey(k)}:</span>
            <strong class="modal-spec-value">${v}</strong>
          </div>
        `).join('') : '';

        const complianceBadges = prod.compliance ? prod.compliance.map(c => `
          <span class="modal-compliance-chip">✓ ${c}</span>
        `).join('') : '';

        const whatsappUrl = `https://wa.me/551938341741?text=Ol%C3%A1,%20gostaria%20de%20um%20or%C3%A7amento%20t%C3%A9cnico%20para%20o%20produto:%20${encodeURIComponent(prod.name)}`;

        modalContent.innerHTML = `
          <div class="modal-product-layout">
            <div class="modal-product-visual">
              <span class="modal-badge">${prod.badge}</span>
              <img src="${prod.image}" alt="${prod.name}" class="modal-main-img" />
              <div class="modal-compliance-box">
                ${complianceBadges}
              </div>
            </div>

            <div class="modal-product-info">
              <span class="modal-category">${prod.categoryLabel}</span>
              <h2 class="modal-title">${prod.name}</h2>
              <p class="modal-desc">${prod.shortDesc}</p>

              ${prod.recommendedFor ? `
                <div class="modal-recommendation">
                  <strong>Recomendado para:</strong> ${prod.recommendedFor}
                </div>
              ` : ''}

              <div class="modal-specs-table">
                <h4 class="modal-specs-heading">Ficha Técnica & Normas</h4>
                ${specsRows}
              </div>

              <div class="modal-actions-row">
                <a href="${whatsappUrl}" target="_blank" rel="noopener noreferrer" class="btn-modal-quote">
                  <span>Iniciar Atendimento no WhatsApp</span>
                  <svg width="20" height="20" fill="currentColor" viewBox="0 0 24 24"><path d="M12.031 6.172c-3.181 0-5.767 2.586-5.768 5.766-.001 1.298.38 2.27 1.019 3.287l-.582 2.128 2.182-.573c.978.58 1.911.928 3.145.929 3.178 0 5.767-2.587 5.768-5.766.001-3.187-2.575-5.77-5.764-5.771zm3.392 8.244c-.144.405-.837.774-1.17.824-.312.045-.698.058-2.18-.553-1.894-.778-3.109-2.73-3.204-2.856-.095-.127-.77-1.026-.77-1.956 0-.931.488-1.389.663-1.579.175-.19.382-.238.51-.238.127 0 .254.002.366.007.118.006.275-.045.431.33.16.386.549 1.336.598 1.433.049.098.081.213.016.342-.065.129-.098.21-.194.324-.097.114-.204.256-.292.344-.098.098-.2.204-.086.4.114.195.508.838 1.09 1.356.75.667 1.383.874 1.579.972.196.098.312.082.428-.051.117-.133.501-.584.636-.784.135-.201.27-.168.455-.1.185.068 1.173.553 1.374.654.201.101.335.151.384.235.049.084.049.49-.095.895z"/></svg>
                </a>
              </div>
            </div>
          </div>
        `;

        modalBackdrop.classList.add('active');
        document.body.style.overflow = 'hidden';
      }
    }
  });

  // Modal Close Handlers
  if (modalCloseBtn) {
    modalCloseBtn.addEventListener('click', closeModal);
  }
  if (modalBackdrop) {
    modalBackdrop.addEventListener('click', (e) => {
      if (e.target === modalBackdrop) closeModal();
    });
  }
  document.addEventListener('keydown', (e) => {
    if (e.key === 'Escape') closeModal();
  });

  function closeModal() {
    if (modalBackdrop) modalBackdrop.classList.remove('active');
    document.body.style.overflow = '';
  }

  function formatSpecKey(key) {
    const map = {
      capacidade: 'Capacidade',
      agente: 'Agente Extintor',
      capacidadeExtintora: 'Capacidade Extintora',
      pressurizacao: 'Tipo de Pressurização',
      pesoTotal: 'Peso Bruto Total',
      alcanceJato: 'Alcance do Jato',
      tempoDescarga: 'Tempo de Descarga',
      norma: 'Norma Técnica',
      diametro: 'Diâmetro Nominal',
      comprimento: 'Comprimento',
      pressaoTrabalho: 'Pressão de Trabalho',
      pressaoRuptura: 'Pressão de Ruptura',
      unioes: 'Tipo de Engate',
      material: 'Material de Fabricação',
      dimensoes: 'Dimensões (A x L x P)',
      acabamento: 'Tratamento & Pintura',
      autonomiaBrilho: 'Autonomia de Brilho',
      potenciaSaida: 'Potência em 24VDC',
      bateria: 'Bateria Integrada',
      autonomia: 'Autonomia Contínua',
      fluxoLuminoso: 'Fluxo Luminoso'
    };
    return map[key] || key.replace(/([A-Z])/g, ' $1').replace(/^./, str => str.toUpperCase());
  }

  // Initial Run
  updateCatalogView();
}
