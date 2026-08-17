/**
 * INDA FIRE — SERVICES PAGE INTERACTIVE ENGINE
 * Real-time Search, Category Filtering, Deep-linking & Scope Details Modal
 */

import { SERVICES } from './catalog-data.js';

document.addEventListener('DOMContentLoaded', () => {
  initServicesPage();
  initDrawerNav();
});

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


function initServicesPage() {
  const tabsBar = document.getElementById('services-filter-tabs');
  const cardsGrid = document.getElementById('services-cards-grid');
  const searchInput = document.getElementById('services-search-input');
  const searchClear = document.getElementById('services-search-clear');
  const resultsCount = document.getElementById('services-results-count');
  const emptyState = document.getElementById('services-empty-state');
  const resetSearchBtn = document.getElementById('btn-reset-search');
  
  // Modal Elements
  const modalBackdrop = document.getElementById('service-detail-modal');
  const modalContent = document.getElementById('modal-service-content');
  const modalCloseBtn = document.getElementById('service-modal-close-btn');

  // URL State
  const urlParams = new URLSearchParams(window.location.search);
  let activeCategory = urlParams.get('cat') || 'todos';
  let searchQuery = urlParams.get('q') || '';
  const initialServId = urlParams.get('serv') || '';

  // Update Category Count Badges
  function updateCountBadges() {
    const counts = {
      todos: SERVICES.length,
      projetos: SERVICES.filter(s => s.category === 'projetos').length,
      manutencao: SERVICES.filter(s => s.category === 'manutencao').length,
      hidraulica: SERVICES.filter(s => s.category === 'hidraulica').length,
      eletrica: SERVICES.filter(s => s.category === 'eletrica').length,
      brigada: SERVICES.filter(s => s.category === 'brigada').length
    };

    Object.keys(counts).forEach(cat => {
      const badge = document.getElementById(`count-${cat}`);
      if (badge) badge.textContent = counts[cat];
    });
  }
  updateCountBadges();

  // Set initial category tab state
  if (tabsBar) {
    const targetTab = tabsBar.querySelector(`.service-tab-btn[data-cat="${activeCategory}"]`);
    if (targetTab) {
      tabsBar.querySelectorAll('.service-tab-btn').forEach(b => b.classList.remove('active'));
      targetTab.classList.add('active');
    }
  }

  // Set initial search input
  if (searchInput && searchQuery) {
    searchInput.value = searchQuery;
    if (searchClear) searchClear.style.display = 'block';
  }

  // 1. Search Input Event
  if (searchInput) {
    searchInput.addEventListener('input', (e) => {
      searchQuery = e.target.value.trim().toLowerCase();
      if (searchClear) {
        searchClear.style.display = searchQuery ? 'block' : 'none';
      }
      renderServicesGrid();
    });
  }

  if (searchClear) {
    searchClear.addEventListener('click', () => {
      if (searchInput) searchInput.value = '';
      searchQuery = '';
      searchClear.style.display = 'none';
      renderServicesGrid();
      if (searchInput) searchInput.focus();
    });
  }

  if (resetSearchBtn) {
    resetSearchBtn.addEventListener('click', () => {
      if (searchInput) searchInput.value = '';
      searchQuery = '';
      if (searchClear) searchClear.style.display = 'none';
      activeCategory = 'todos';
      if (tabsBar) {
        tabsBar.querySelectorAll('.service-tab-btn').forEach(b => {
          b.classList.toggle('active', b.getAttribute('data-cat') === 'todos');
        });
      }
      renderServicesGrid();
    });
  }

  // 2. Category Tabs Event
  if (tabsBar) {
    tabsBar.addEventListener('click', (e) => {
      const btn = e.target.closest('.service-tab-btn');
      if (btn) {
        activeCategory = btn.getAttribute('data-cat');
        tabsBar.querySelectorAll('.service-tab-btn').forEach(b => {
          b.classList.toggle('active', b === btn);
        });
        renderServicesGrid();
      }
    });
  }

  // 3. Render Services Cards Grid
  function renderServicesGrid() {
    if (!cardsGrid) return;

    let filtered = SERVICES;

    // Filter by Category
    if (activeCategory !== 'todos') {
      filtered = filtered.filter(s => s.category === activeCategory);
    }

    // Filter by Search Query
    if (searchQuery) {
      filtered = filtered.filter(s => {
        const textToSearch = [
          s.name,
          s.summary,
          s.tag,
          ...(s.normas || []),
          ...(s.benefits || [])
        ].join(' ').toLowerCase();
        return textToSearch.includes(searchQuery);
      });
    }

    // Update Results Count & Empty State
    if (resultsCount) {
      resultsCount.innerHTML = `Exibindo <strong>${filtered.length} serviço${filtered.length === 1 ? '' : 's'} especializado${filtered.length === 1 ? '' : 's'}</strong>`;
    }

    if (emptyState) {
      emptyState.style.display = filtered.length === 0 ? 'block' : 'none';
    }

    cardsGrid.style.display = filtered.length === 0 ? 'none' : 'grid';

    cardsGrid.innerHTML = filtered.map(serv => {
      const normasList = serv.normas ? serv.normas.map(n => `<span class="service-norm-chip">✓ ${n}</span>`).join('') : '';

      return `
        <div class="service-card" data-service-id="${serv.id}">
          <div class="service-card-canvas">
            <span class="service-card-tag">${serv.tag}</span>
            <img src="${serv.image}" alt="${serv.name}" class="service-card-img" loading="lazy" />
          </div>

          <div class="service-card-body">
            <h3 class="service-card-title">${serv.name}</h3>
            <p class="service-card-summary">${serv.summary}</p>

            <div class="service-norms-row">
              ${normasList}
            </div>

            <div class="service-card-footer" style="margin-top: auto;">
              <button type="button" class="btn-service-detail btn-open-service-modal" data-service-id="${serv.id}">
                <span>Ver Detalhes do Escopo</span>
                <span class="btn-arrow">➔</span>
              </button>
            </div>
          </div>
        </div>
      `;
    }).join('');
  }

  // Initial render
  renderServicesGrid();

  // 4. Open Service Details Modal
  document.addEventListener('click', (e) => {
    const btn = e.target.closest('.btn-open-service-modal');
    if (btn) {
      const servId = btn.getAttribute('data-service-id');
      openServiceModal(servId);
    }
  });

  function openServiceModal(servId) {
    const serv = SERVICES.find(s => s.id === servId);
    if (!serv || !modalContent || !modalBackdrop) return;

    const benefitsList = serv.benefits ? serv.benefits.map(b => `
      <li class="modal-benefit-item">
        <span class="benefit-check">✓</span>
        <span>${b}</span>
      </li>
    `).join('') : '';

    const normasChips = serv.normas ? serv.normas.map(n => `
      <span class="modal-norm-chip">${n}</span>
    `).join('') : '';

    const whatsappUrl = `https://wa.me/551938341741?text=Ol%C3%A1,%20gostaria%20de%20solicitar%20uma%20proposta%20t%C3%A9cnica%20para%20o%20servi%C3%A7o:%20${encodeURIComponent(serv.name)}`;

    modalContent.innerHTML = `
      <div class="modal-service-layout">
        <div class="modal-service-visual">
          <span class="modal-service-tag">${serv.tag}</span>
          <img src="${serv.image}" alt="${serv.name}" class="modal-service-img" />
          <div class="modal-service-norms-box">
            <h4>Normas & Regulamentos:</h4>
            <div class="norms-flex">${normasChips}</div>
          </div>
        </div>

        <div class="modal-service-info">
          <h2 class="modal-service-title">${serv.name}</h2>
          <p class="modal-service-desc">${serv.summary}</p>

          <div class="modal-benefits-box">
            <h4 class="modal-section-heading">O Que Está Incluso no Escopo:</h4>
            <ul class="modal-benefits-list">
              ${benefitsList}
            </ul>
          </div>

          <div class="modal-service-actions">
            <a href="${whatsappUrl}" target="_blank" rel="noopener noreferrer" class="btn-service-quote-wa">
              <svg width="20" height="20" fill="currentColor" viewBox="0 0 24 24"><path d="M12.031 6.172c-3.181 0-5.767 2.586-5.768 5.766-.001 1.298.38 2.27 1.019 3.287l-.582 2.128 2.182-.573c.978.58 1.911.928 3.145.929 3.178 0 5.767-2.587 5.768-5.766.001-3.187-2.575-5.77-5.764-5.771zm3.392 8.244c-.144.405-.837.774-1.17.824-.312.045-.698.058-2.18-.553-1.894-.778-3.109-2.73-3.204-2.856-.095-.127-.77-1.026-.77-1.956 0-.931.488-1.389.663-1.579.175-.19.382-.238.51-.238.127 0 .254.002.366.007.118.006.275-.045.431.33.16.386.549 1.336.598 1.433.049.098.081.213.016.342-.065.129-.098.21-.194.324-.097.114-.204.256-.292.344-.098.098-.2.204-.086.4.114.195.508.838 1.09 1.356.75.667 1.383.874 1.579.972.196.098.312.082.428-.051.117-.133.501-.584.636-.784.135-.201.27-.168.455-.1.185.068 1.173.553 1.374.654.201.101.335.151.384.235.049.084.049.49-.095.895z"/></svg>
              <span>Solicitar no WhatsApp</span>
            </a>
            <a href="index.html#contato" class="btn-service-quote-form">
              <span>Formulário de Orçamento</span>
            </a>
          </div>
        </div>
      </div>
    `;

    modalBackdrop.classList.add('active');
    document.body.style.overflow = 'hidden';
  }

  // Modal Close Handlers
  if (modalCloseBtn) modalCloseBtn.addEventListener('click', closeServiceModal);
  if (modalBackdrop) {
    modalBackdrop.addEventListener('click', (e) => {
      if (e.target === modalBackdrop) closeServiceModal();
    });
  }
  document.addEventListener('keydown', (e) => {
    if (e.key === 'Escape') closeServiceModal();
  });

  function closeServiceModal() {
    if (modalBackdrop) modalBackdrop.classList.remove('active');
    document.body.style.overflow = '';
  }

  // Check if initial service was requested in URL
  if (initialServId) {
    setTimeout(() => {
      openServiceModal(initialServId);
    }, 300);
  }
}
