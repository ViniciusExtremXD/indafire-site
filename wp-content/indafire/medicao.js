/*
 * Inda Fire — medição de contatos para o Google Tag Manager (GTM-WTKSN3VL), 15/10/2026.
 *
 * Envia para o dataLayer um evento a cada contato real:
 *   contato_whatsapp  — abriu o WhatsApp (link, botão flutuante, formulário ou aviso)
 *   contato_telefone  — tocou num telefone (tel:)
 *   contato_email     — clicou num e-mail (mailto:)
 * com { origem, produto, link_url }. O GTM transforma isso em eventos do GA4
 * (e depois em conversões do Google Ads).
 *
 * Botões que só abrem o aviso "Fale com a nossa equipe" NÃO contam: o contato
 * só é registrado quando a pessoa clica em "Chamar no WhatsApp".
 */
(function () {
  'use strict';

  window.dataLayer = window.dataLayer || [];
  var ultimo = { chave: '', quando: 0 };

  function enviar(evento, dados) {
    // o mesmo contato não conta duas vezes em menos de 1,5 s (ex.: clique + window.open)
    var chave = evento + '|' + (dados.link_url || '');
    var agora = Date.now();
    if (chave === ultimo.chave && agora - ultimo.quando < 1500) return;
    ultimo = { chave: chave, quando: agora };
    window.dataLayer.push({
      event: evento,
      origem: dados.origem || 'outro',
      produto: dados.produto || '',
      link_url: dados.link_url || '',
    });
  }

  function tipoDoLink(url) {
    if (!url) return '';
    if (/^tel:/i.test(url)) return 'contato_telefone';
    if (/^mailto:/i.test(url)) return 'contato_email';
    if (/(^|\/\/)(wa\.me|api\.whatsapp\.com|web\.whatsapp\.com|chat\.whatsapp\.com)\b/i.test(url)) return 'contato_whatsapp';
    return '';
  }

  function origemDo(el) {
    if (!el || !el.closest) return 'outro';
    if (el.closest('.if-aviso')) return 'aviso';
    if (el.closest('.if-hero-whats-wrap, #bannerProdutoINDA')) return 'banner';
    if (el.closest('.if-menu-whats-wrap, .jet-menu, .jet-sub-mega-menu')) return 'menu_produtos';
    if (el.closest('#ht-ctc-chat, .ht-ctc')) return 'botao_flutuante';
    if (el.closest('#indafire-commercial-whatsapp, .indafire-whatsapp-card')) return 'formulario_whatsapp';
    if (el.closest('form')) return 'formulario';
    if (el.closest('.elementor-location-footer, footer')) return 'rodape';
    if (el.closest('.elementor-location-header, header')) return 'cabecalho';
    return 'pagina';
  }

  function produtoDo(el) {
    var alvo = el && el.closest && el.closest('[data-if-produto]');
    if (alvo) return alvo.getAttribute('data-if-produto') || '';
    var aviso = el && el.closest && el.closest('.if-aviso');
    var linha = aviso && aviso.querySelector('[data-if-produto] strong');
    return linha ? linha.textContent.trim() : '';
  }

  // Cliques em links. Fase de "bolha" no window: roda depois dos outros scripts,
  // então dá para saber se o clique só abriu o aviso (defaultPrevented) ou se abriu o link.
  window.addEventListener('click', function (e) {
    var link = e.target && e.target.closest ? e.target.closest('a[href]') : null;
    if (!link) return;
    var tipo = tipoDoLink(link.getAttribute('href'));
    if (!tipo) return;
    if (e.defaultPrevented) return; // abriu o aviso, ainda não é contato
    enviar(tipo, { origem: origemDo(link), produto: produtoDo(link), link_url: link.href });
  });

  // último elemento tocado/clicado: o botão flutuante é uma <div>, não recebe foco
  var toque = { el: null, quando: 0 };
  document.addEventListener(
    'pointerdown',
    function (e) {
      toque = { el: e.target, quando: Date.now() };
    },
    true,
  );

  // WhatsApp aberto por script (botão flutuante e formulários que montam a mensagem)
  var abrirOriginal = window.open;
  window.open = function (url) {
    try {
      var texto = String(url || '');
      if (tipoDoLink(texto) === 'contato_whatsapp') {
        var ativo = Date.now() - toque.quando < 3000 && toque.el ? toque.el : document.activeElement;
        enviar('contato_whatsapp', { origem: origemDo(ativo), produto: produtoDo(ativo), link_url: texto });
      }
    } catch (err) {
      /* medição nunca atrapalha o clique */
    }
    return abrirOriginal.apply(window, arguments);
  };
})();
