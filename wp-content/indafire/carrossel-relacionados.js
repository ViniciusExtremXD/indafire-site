/*
 * Inda Fire — carrossel de "Produtos relacionados" na página do produto (15/10/2026).
 *
 * O trilho é rolagem horizontal nativa (arrasta com o dedo, desliza com o trackpad);
 * aqui só entram as setas, que andam um card por vez e somem nas pontas.
 */
(function () {
  'use strict';

  var trilho = document.querySelector('[data-if-carrossel]');
  if (!trilho) return;

  var SETA =
    '<svg width="22" height="22" viewBox="0 0 24 24" aria-hidden="true" focusable="false">' +
    '<path d="M15 5l-7 7 7 7" fill="none" stroke="currentColor" stroke-width="2.6" stroke-linecap="round" stroke-linejoin="round"/></svg>';

  var moldura = document.createElement('div');
  moldura.className = 'if-rel-carrossel';
  trilho.parentNode.insertBefore(moldura, trilho);
  moldura.appendChild(trilho);

  function seta(lado, rotulo) {
    var b = document.createElement('button');
    b.type = 'button';
    b.className = 'if-rel-seta if-rel-seta--' + lado;
    b.setAttribute('aria-label', rotulo);
    b.innerHTML = SETA;
    moldura.appendChild(b);
    return b;
  }
  var anterior = seta('anterior', 'Produtos anteriores');
  var proximo = seta('proximo', 'Próximos produtos');

  function passo() {
    var card = trilho.querySelector('article');
    if (!card) return trilho.clientWidth;
    var gap = parseFloat(getComputedStyle(trilho).columnGap) || 0;
    return card.getBoundingClientRect().width + gap;
  }

  function atualizar() {
    var max = trilho.scrollWidth - trilho.clientWidth - 2;
    anterior.disabled = trilho.scrollLeft <= 8;
    proximo.disabled = trilho.scrollLeft >= max - 6;
    moldura.classList.toggle('if-rel-sem-setas', max <= 0);
  }

  anterior.addEventListener('click', function () {
    trilho.scrollBy({ left: -passo(), behavior: 'smooth' });
  });
  proximo.addEventListener('click', function () {
    trilho.scrollBy({ left: passo(), behavior: 'smooth' });
  });
  trilho.addEventListener('scroll', atualizar, { passive: true });
  window.addEventListener('resize', atualizar);
  // teclado: com o trilho em foco, setas do teclado andam um card
  trilho.addEventListener('keydown', function (e) {
    if (e.key === 'ArrowRight') {
      e.preventDefault();
      proximo.click();
    } else if (e.key === 'ArrowLeft') {
      e.preventDefault();
      anterior.click();
    }
  });
  atualizar();
  window.setTimeout(atualizar, 600); // depois das imagens
})();
