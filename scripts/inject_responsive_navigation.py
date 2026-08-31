"""Inject the shared adaptive header behavior into every managed static route."""

from __future__ import annotations

from pathlib import Path
import re

from scripts import inject_internal_page_polish as internal


ROOT = Path(__file__).resolve().parents[1]
STYLE_ID = "indafire-responsive-navigation-style"
SCRIPT_ID = "indafire-responsive-navigation"
TARGETS = internal.TARGETS


CSS = r"""
/* INDAFIRE — adaptive header; full navigation is shown only when it fits. */
.indafire-compact-client {
  display: none !important;
}

@media (max-width: 1100px) {
  #headerInda .elementor-element.elementor-element-46583ef > .elementor-container > .elementor-row {
    display: flex !important;
    flex-flow: row nowrap !important;
    align-items: center !important;
    justify-content: space-between !important;
  }

  #headerInda .elementor-element.elementor-element-20668c0,
  #headerInda .jet-menu-container,
  #headerInda .elementor-element.elementor-element-3de852d {
    display: none !important;
  }

  #headerInda .elementor-element.elementor-element-2e5c5af {
    order: 1 !important;
    flex: 1 1 auto !important;
    width: auto !important;
    min-width: 0 !important;
    max-width: none !important;
  }

  #headerInda .elementor-element.elementor-element-0d060a6 {
    order: 2 !important;
    display: flex !important;
    flex: 0 0 auto !important;
    width: auto !important;
    min-width: 0 !important;
    max-width: none !important;
    margin: 0 0 0 auto !important;
    padding: 0 !important;
  }

  #headerInda .elementor-element.elementor-element-0d060a6 > .elementor-column-wrap,
  #headerInda .elementor-element.elementor-element-0d060a6 > .elementor-column-wrap > .elementor-widget-wrap {
    display: flex !important;
    flex-flow: row nowrap !important;
    align-items: center !important;
    justify-content: flex-end !important;
    gap: 10px !important;
    width: auto !important;
    margin: 0 !important;
    padding: 0 !important;
  }

  #headerInda .elementor-element.elementor-element-8755157.elementor-hidden-desktop,
  #headerInda .elementor-element.elementor-element-8755157 {
    display: flex !important;
    flex: 0 0 auto !important;
    align-items: center !important;
    justify-content: center !important;
    width: auto !important;
    margin: 0 !important;
    padding: 0 !important;
  }

  #headerInda .elementor-element.elementor-element-8755157 .elementor-icon {
    position: relative !important;
    display: inline-flex !important;
    align-items: center !important;
    justify-content: center !important;
    width: 40px !important;
    min-width: 40px !important;
    height: 40px !important;
    padding: 0 !important;
    border: 1px solid rgba(227, 6, 19, .3) !important;
    border-radius: 11px !important;
    background: #ffffff !important;
    color: #e30613 !important;
    box-shadow: 0 4px 12px rgba(24, 24, 24, .08) !important;
    text-decoration: none !important;
    transition: transform 180ms ease, border-color 180ms ease,
                box-shadow 180ms ease, background-color 180ms ease !important;
  }

  #headerInda .elementor-element.elementor-element-8755157 .elementor-icon i {
    display: none !important;
  }

  #headerInda .elementor-element.elementor-element-8755157 .elementor-icon::before {
    content: "" !important;
    display: block !important;
    width: 19px !important;
    height: 14px !important;
    background: linear-gradient(
      to bottom,
      #e30613 0 2px,
      transparent 2px 6px,
      #e30613 6px 8px,
      transparent 8px 12px,
      #e30613 12px 14px
    ) !important;
  }

  #headerInda .elementor-element.elementor-element-8755157 .elementor-icon:hover,
  #headerInda .elementor-element.elementor-element-8755157 .elementor-icon:focus-visible {
    border-color: #e30613 !important;
    background: #fff7f8 !important;
    box-shadow: 0 6px 16px rgba(227, 6, 19, .15) !important;
    transform: translateY(-1px) !important;
    outline: none !important;
  }

  #headerInda .indafire-compact-client {
    display: inline-flex !important;
    align-items: center !important;
    justify-content: center !important;
    min-height: 36px !important;
    padding: 8px 14px !important;
    border: 1px solid #e30613 !important;
    border-radius: 999px !important;
    background: #e30613 !important;
    color: #ffffff !important;
    font-size: 11px !important;
    font-weight: 700 !important;
    line-height: 1 !important;
    letter-spacing: .02em !important;
    text-decoration: none !important;
    white-space: nowrap !important;
    box-shadow: 0 4px 12px rgba(227, 6, 19, .2) !important;
    transition: transform 260ms ease, box-shadow 260ms ease, background-color 260ms ease !important;
  }

  #headerInda .indafire-compact-client:hover,
  #headerInda .indafire-compact-client:focus-visible {
    background: #c9000c !important;
    transform: translateY(-1px) !important;
    box-shadow: 0 6px 16px rgba(227, 6, 19, .28) !important;
  }
}

@media (min-width: 768px) and (max-width: 1100px) {
  #headerInda .elementor-element.elementor-element-46583ef {
    width: calc(100% - 24px) !important;
    min-height: 56px !important;
    margin: 8px auto !important;
    padding: 4px 16px !important;
  }

  #headerInda .elementor-element.elementor-element-e171195 img {
    height: 34px !important;
    max-height: 34px !important;
    max-width: 150px !important;
  }
}

@media (max-width: 430px) {
  #headerInda .elementor-element.elementor-element-e171195 img {
    max-width: 112px !important;
  }

  #headerInda .elementor-element.elementor-element-0d060a6 > .elementor-column-wrap > .elementor-widget-wrap {
    gap: 7px !important;
  }

  #headerInda .indafire-compact-client {
    min-height: 34px !important;
    padding: 7px 10px !important;
    font-size: 10px !important;
  }
}

@media (min-width: 1101px) {
  #headerInda .elementor-element.elementor-element-20668c0,
  #headerInda .jet-menu-container {
    display: block !important;
  }

  #headerInda .elementor-element.elementor-element-8755157,
  #headerInda .indafire-compact-client {
    display: none !important;
  }
}

@keyframes indafire-soft-icon-enter {
  from { opacity: 0; transform: translateY(7px); }
  to { opacity: 1; transform: translateY(0); }
}

#headerInda .elementor-social-icon,
#headerInda .elementor-element-8755157 .elementor-icon,
#headerInda .indafire-compact-client {
  animation: indafire-soft-icon-enter 560ms cubic-bezier(.22, .61, .36, 1) both;
}

#headerInda .elementor-social-icons-wrapper .elementor-grid-item:nth-child(2) .elementor-social-icon { animation-delay: 70ms; }
#headerInda .elementor-social-icons-wrapper .elementor-grid-item:nth-child(3) .elementor-social-icon { animation-delay: 140ms; }
#headerInda .elementor-social-icons-wrapper .elementor-grid-item:nth-child(4) .elementor-social-icon { animation-delay: 210ms; }

@media (prefers-reduced-motion: reduce) {
  #headerInda .elementor-social-icon,
  #headerInda .elementor-element-8755157 .elementor-icon,
  #headerInda .indafire-compact-client {
    animation: none !important;
    transition-duration: 1ms !important;
  }
}
""".strip()


JS = r"""
(function () {
  var compactQuery = window.matchMedia('(max-width: 1100px)');
  var staticDrawerSource = document.querySelector('.elementor-2519');
  var staticDrawerTemplate = staticDrawerSource && staticDrawerSource.cloneNode(true);

  function normalized(value) {
    return (value || '').normalize('NFD').replace(/[\u0300-\u036f]/g, '').toLowerCase();
  }

  function modalIsOpen(modal) {
    if (!modal) return false;
    var style = window.getComputedStyle(modal);
    return style.display !== 'none' && style.visibility !== 'hidden' && modal.getAttribute('aria-hidden') !== 'true';
  }

  function hydrateDrawerImages(root) {
    Array.prototype.forEach.call(root.querySelectorAll('img'), function (image) {
      var lazySource = image.getAttribute('data-lazy-src') || image.getAttribute('data-src');
      if (lazySource && !image.getAttribute('src')) image.setAttribute('src', lazySource);
    });
  }

  function ensureStaticDrawer() {
    var existing = document.querySelector('#elementor-popup-modal-2519');
    if (existing && existing.querySelector('.elementor-2519')) return existing;
    if (!staticDrawerTemplate) return existing;

    if (existing && existing.parentElement) existing.parentElement.removeChild(existing);

    var modal = document.createElement('div');
    modal.id = 'elementor-popup-modal-2519';
    modal.className = 'dialog-widget dialog-lightbox-widget dialog-type-buttons dialog-type-lightbox elementor-popup-modal indafire-static-drawer';
    modal.setAttribute('role', 'dialog');
    modal.setAttribute('aria-modal', 'true');
    modal.setAttribute('aria-label', 'Menu principal');
    modal.setAttribute('aria-hidden', 'true');

    var panel = document.createElement('div');
    panel.className = 'dialog-widget-content dialog-lightbox-widget-content animated slideInRight';
    var header = document.createElement('div');
    header.className = 'dialog-header dialog-lightbox-header';
    var closeButton = document.createElement('button');
    closeButton.className = 'dialog-close-button dialog-close-button-default';
    closeButton.type = 'button';
    closeButton.setAttribute('aria-label', 'Fechar menu');
    var message = document.createElement('div');
    message.className = 'dialog-message dialog-lightbox-message';
    var drawerContent = staticDrawerTemplate.cloneNode(true);
    hydrateDrawerImages(drawerContent);
    message.appendChild(drawerContent);
    panel.appendChild(header);
    panel.appendChild(closeButton);
    panel.appendChild(message);
    modal.appendChild(panel);
    document.body.appendChild(modal);
    return modal;
  }

  function setupResponsiveNavigation() {
    var header = document.querySelector('#headerInda');
    var headerHost = document.querySelector('.elementor-location-header');
    var menuWidget = header && header.querySelector('.elementor-element-20668c0');
    var hamburger = header && header.querySelector('.elementor-element-8755157');
    var hamburgerLink = hamburger && hamburger.querySelector('a');
    var actionWrap = hamburger && hamburger.parentElement;
    if (!header || !menuWidget || !hamburger || !hamburgerLink || !actionWrap) return;

    var clientSource = Array.prototype.find.call(header.querySelectorAll('a'), function (link) {
      return normalized(link.textContent).indexOf('area do cliente') !== -1;
    });

    if (clientSource && !header.querySelector('.indafire-compact-client')) {
      var clientLink = document.createElement('a');
      clientLink.className = 'indafire-compact-client';
      clientLink.href = clientSource.href;
      clientLink.textContent = 'Área do cliente';
      clientLink.setAttribute('aria-label', 'Acessar a Área do cliente');
      if (clientSource.target) clientLink.target = clientSource.target;
      if (clientSource.rel) clientLink.rel = clientSource.rel;
      actionWrap.insertBefore(clientLink, hamburger);
    }

    var root = document.documentElement;
    var lastScrollY = Math.max(window.scrollY || 0, 0);
    var scrollFramePending = false;

    function revealHeader() {
      header.style.setProperty('transform', 'translateY(0)', 'important');
      root.classList.add('indafire-scroll-header-ready', 'indafire-header-visible');
      root.classList.remove('indafire-header-hidden');
    }

    function hideHeader() {
      header.style.setProperty('transform', 'translateY(calc(-100% - 12px))', 'important');
      root.classList.add('indafire-scroll-header-ready', 'indafire-header-hidden');
      root.classList.remove('indafire-header-visible');
    }

    function updateHeaderFromScroll() {
      var currentScrollY = Math.max(window.scrollY || 0, 0);
      var delta = currentScrollY - lastScrollY;
      var drawerOpen = document.body.classList.contains('elementor-popup-modal-active');

      if (currentScrollY <= 8 || delta < -4 || drawerOpen) revealHeader();
      else if (delta > 4) hideHeader();

      lastScrollY = currentScrollY;
      scrollFramePending = false;
    }

    function onPageScroll() {
      if (scrollFramePending) return;
      scrollFramePending = true;
      window.requestAnimationFrame(updateHeaderFromScroll);
    }

    header.style.setProperty(
      'transition',
      'transform 280ms cubic-bezier(.22, .61, .36, 1), box-shadow 240ms ease',
      'important'
    );
    header.style.setProperty('will-change', 'transform');
    if (headerHost && headerHost !== header) {
      headerHost.style.setProperty('transform', 'none', 'important');
      headerHost.style.setProperty('transition', 'none', 'important');
    }
    revealHeader();
    window.addEventListener('scroll', onPageScroll, { passive: true });

    function syncState() {
      var compact = compactQuery.matches;
      var modal = document.querySelector('#elementor-popup-modal-2519');
      document.documentElement.classList.toggle('indafire-compact-nav', compact);

      if (!compact && modalIsOpen(modal)) {
        modal.style.display = 'none';
        modal.setAttribute('aria-hidden', 'true');
        document.body.classList.remove('elementor-popup-modal-active');
      }

      hamburgerLink.setAttribute('aria-expanded', String(compact && modalIsOpen(modal)));
    }

    function closeDrawer() {
      var modal = document.querySelector('#elementor-popup-modal-2519');
      if (!modal) return;
      modal.style.setProperty('display', 'none', 'important');
      modal.setAttribute('aria-hidden', 'true');
      document.body.classList.remove('elementor-popup-modal-active');
      hamburgerLink.setAttribute('aria-expanded', 'false');
    }

    function openDrawer(event) {
      if (!compactQuery.matches) return;
      event.preventDefault();
      event.stopPropagation();
      var modal = ensureStaticDrawer();
      if (!modal || !modal.querySelector('.elementor-2519')) return;
      modal.style.setProperty('display', 'flex', 'important');
      modal.setAttribute('aria-hidden', 'false');
      document.body.classList.add('elementor-popup-modal-active');
      hamburgerLink.setAttribute('aria-expanded', 'true');
      revealHeader();
    }

    hamburgerLink.setAttribute('aria-controls', 'elementor-popup-modal-2519');
    hamburgerLink.setAttribute('aria-haspopup', 'dialog');
    hamburgerLink.setAttribute('aria-expanded', 'false');
    hamburgerLink.addEventListener('click', openDrawer);

    document.addEventListener('click', function (event) {
      var modal = document.querySelector('#elementor-popup-modal-2519');
      if (!modal || !modalIsOpen(modal)) return;
      var closeTarget = event.target.closest && event.target.closest('.dialog-close-button');
      var navigationTarget = event.target.closest && event.target.closest('.elementor-2519 a');
      if (event.target === modal || closeTarget || navigationTarget) closeDrawer();
    });

    document.addEventListener('keydown', function (event) {
      if (event.key === 'Escape') closeDrawer();
    });

    new MutationObserver(syncState).observe(document.body, {
      attributes: true,
      childList: true,
      subtree: true,
      attributeFilter: ['class', 'style', 'aria-hidden']
    });

    if (typeof compactQuery.addEventListener === 'function') compactQuery.addEventListener('change', syncState);
    else compactQuery.addListener(syncState);
    syncState();
  }

  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', setupResponsiveNavigation);
  else setupResponsiveNavigation();
})();
""".strip()


def style_tag() -> str:
    return f'<style id="{STYLE_ID}">\n{CSS}\n</style>'


def script_tag() -> str:
    return f'<script id="{SCRIPT_ID}">\n{JS}\n</script>'


def disable_legacy_drawer_controller(source: str) -> str:
    """Remove the older click owner before installing the static drawer controller."""
    return source.replace("initMenuDrawer();", "")


def disable_legacy_scroll_controller(source: str) -> str:
    """Remove the zero-height wrapper scroll controller from static pages."""
    pattern = re.compile(
        r"<script>\s*\(function \(\) \{\s*['\"]use strict['\"];.*?"
        r"function initIndafireScrollHeader\(\).*?</script>\s*",
        re.DOTALL,
    )
    return pattern.sub("", source)


def inject(source: str) -> str:
    style_pattern = re.compile(rf'<style id="{re.escape(STYLE_ID)}">.*?</style>\s*', re.DOTALL)
    script_pattern = re.compile(rf'<script id="{re.escape(SCRIPT_ID)}">.*?</script>\s*', re.DOTALL)
    stripped = disable_legacy_scroll_controller(
        disable_legacy_drawer_controller(
            script_pattern.sub("", style_pattern.sub("", source))
        )
    )
    if "</head>" not in stripped or "</body>" not in stripped:
        return source
    hero_video_marker = '<style id="indafire-hero-background-video-style">'
    internal_marker = '<style id="indafire-internal-page-polish">'
    if hero_video_marker in stripped:
        rendered = stripped.replace(hero_video_marker, f"{style_tag()}\n{hero_video_marker}", 1)
    elif internal_marker in stripped:
        rendered = stripped.replace(internal_marker, f"{style_tag()}\n{internal_marker}", 1)
    else:
        rendered = stripped.replace("</head>", f"{style_tag()}\n</head>", 1)

    products_marker = '<script id="indafire-home-product-carousel">'
    service_marker = '<script id="indafire-home-service-sync">'
    script_markers = [marker for marker in (products_marker, service_marker) if marker in rendered]
    if script_markers:
        first_marker = min(script_markers, key=rendered.index)
        return rendered.replace(first_marker, f"{script_tag()}\n{first_marker}", 1)
    return rendered.replace("</body>", f"{script_tag()}\n</body>", 1)


def inject_assets(targets: tuple[Path, ...] | list[Path]) -> int:
    changed = 0
    for page in targets:
        source = page.read_text(encoding="utf-8")
        rendered = inject(source)
        if rendered != source:
            page.write_text(rendered, encoding="utf-8")
            changed += 1
    return changed


if __name__ == "__main__":
    print(f"Injected responsive navigation into {inject_assets(TARGETS)} page(s).")
