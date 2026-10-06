/*
 * Inda Fire — aviso de WhatsApp nos produtos (pedido do Wellington, 06/10/2026).
 *
 * Na área de produtos, o clique não leva mais à página do produto nem envia
 * formulário: a tela fica fosca e aparece o aviso "Entre em contato pelo
 * nosso WhatsApp. Nossa equipe vai te atender.", com o botão que abre o
 * WhatsApp já com o nome do produto (e, no formulário, com os dados que a
 * pessoa digitou).
 *
 * Vale para:
 *  - listas (produtos/ e categoria-produto/*): cartão do produto, "Veja +" e "Conheça";
 *  - página do produto (produto/*): "Solicite orçamento", formulário de
 *    orçamento e produtos relacionados.
 *
 * Arquivo único, sem dependências: injeta o próprio CSS e o HTML do aviso.
 */
(function () {
  'use strict';

  var WHATSAPP = '551938341741';
  var caminho = location.pathname;
  var naLista = /\/(produtos|categoria-produto)\//.test(caminho);
  var naPagina = /\/produto\//.test(caminho);
  if (!naLista && !naPagina) return;

  /* ── Estilo (mesma linha visual do site: Open Sans, vermelho #e30613,
        cartão branco arredondado e botão verde do WhatsApp) ── */
  var css =
    '.if-aviso{position:fixed;inset:0;z-index:2147483646;display:flex;align-items:center;justify-content:center;padding:20px;' +
    'background:rgba(15,15,18,.55);-webkit-backdrop-filter:blur(6px);backdrop-filter:blur(6px);opacity:0;visibility:hidden;' +
    'transition:opacity .25s ease,visibility 0s linear .25s}' +
    '.if-aviso.if-aberto{opacity:1;visibility:visible;transition:opacity .25s ease,visibility 0s}' +
    '.if-aviso__caixa{position:relative;width:100%;max-width:440px;max-height:calc(100vh - 40px);overflow-y:auto;background:#fff;' +
    'border-radius:16px;padding:36px 28px 28px;text-align:center;font-family:"Open Sans",Arial,sans-serif;color:#1e293b;' +
    'box-shadow:0 24px 60px rgba(0,0,0,.28);border-top:5px solid #e30613;transform:translateY(16px) scale(.97);transition:transform .3s ease}' +
    '.if-aviso.if-aberto .if-aviso__caixa{transform:none}.if-aviso__caixa:focus,.if-aviso__caixa:focus-visible{outline:none !important;box-shadow:0 24px 60px rgba(0,0,0,.28) !important}' +
    '.if-aviso__icone{display:inline-flex;align-items:center;justify-content:center;width:64px;height:64px;margin-bottom:14px;' +
    'border-radius:50%;background:#25D366}' +
    '.if-aviso__titulo{margin:0 0 10px;font-size:22px;font-weight:700;line-height:1.25;text-transform:uppercase;letter-spacing:.3px;color:#1e293b}' +
    '.if-aviso__texto{margin:0 0 6px;font-size:17px;line-height:1.5;color:#334155}' +
    '.if-aviso__produto{margin:14px 0 0;padding:10px 14px;border-radius:10px;background:#f1f5f9;font-size:15px;line-height:1.4;color:#334155}' +
    '.if-aviso__produto strong{color:#1e293b}' +
    '.if-aviso__botao{display:flex;align-items:center;justify-content:center;gap:10px;width:100%;min-height:54px;margin-top:22px;' +
    'padding:12px 20px;border:0;border-radius:50px;background:#25D366;color:#fff !important;font-size:16px;font-weight:700;' +
    'text-transform:uppercase;text-decoration:none !important;cursor:pointer;box-shadow:0 8px 20px rgba(37,211,102,.35);transition:background-color .2s}' +
    '.if-aviso__botao:hover{background:#1ebe5a}' +
    '.if-aviso__fechar-texto{display:inline-block;margin-top:14px;padding:8px 14px;border:0;background:none;color:#64748b;' +
    'font:600 15px "Open Sans",Arial,sans-serif;text-decoration:underline;cursor:pointer}' +
    '.if-aviso__x{position:absolute;top:10px;right:10px;width:40px;height:40px;border:0;border-radius:50%;background:none;' +
    'color:#64748b;font-size:26px;line-height:40px;cursor:pointer}' +
    '.if-aviso__x:hover,.if-aviso__fechar-texto:hover{color:#e30613}' +
    '.if-aviso :focus-visible{outline:3px solid #1e293b;outline-offset:2px}' +
    'html.if-aviso-trava,html.if-aviso-trava body{overflow:hidden}' +
    '@media (max-width:420px){.if-aviso__caixa{padding:32px 20px 22px}.if-aviso__titulo{font-size:19px}.if-aviso__texto{font-size:16px}}' +
    '@media (max-height:480px){.if-aviso__caixa{padding:22px 22px 16px}.if-aviso__icone{width:48px;height:48px;margin-bottom:8px}' +
    '.if-aviso__botao{margin-top:14px;min-height:48px}.if-aviso__fechar-texto{margin-top:6px}}';

  var estilo = document.createElement('style');
  estilo.id = 'if-aviso-css';
  estilo.textContent = css;
  document.head.appendChild(estilo);

  var ICONE_WHATS =
    '<svg width="34" height="34" viewBox="0 0 24 24" fill="#fff" aria-hidden="true"><path d="M.057 24l1.687-6.163a11.867 11.867 0 01-1.587-5.946C.16 5.335 5.495 0 12.05 0a11.817 11.817 0 018.413 3.488 11.824 11.824 0 013.48 8.414c-.003 6.557-5.338 11.892-11.893 11.892a11.9 11.9 0 01-5.688-1.448L.057 24zm6.597-3.807c1.676.995 3.276 1.591 5.392 1.592 5.448 0 9.886-4.434 9.889-9.885.002-5.462-4.415-9.89-9.881-9.892-5.452 0-9.887 4.434-9.889 9.884-.001 2.225.651 3.891 1.746 5.634l-.999 3.648 3.742-.981zm11.387-5.464c-.074-.124-.272-.198-.57-.347-.297-.149-1.758-.868-2.031-.967-.272-.099-.47-.149-.669.149-.198.297-.768.967-.941 1.165-.173.198-.347.223-.644.074-.297-.149-1.255-.462-2.39-1.475-.883-.788-1.48-1.761-1.653-2.059-.173-.297-.018-.458.13-.606.134-.133.297-.347.446-.521.151-.172.2-.296.3-.495.099-.198.05-.372-.025-.521-.075-.148-.669-1.611-.916-2.206-.242-.579-.487-.501-.669-.51l-.57-.01c-.198 0-.52.074-.792.372s-1.04 1.016-1.04 2.479 1.065 2.876 1.213 3.074c.149.198 2.095 3.2 5.076 4.487.709.306 1.263.489 1.694.626.712.226 1.36.194 1.872.118.571-.085 1.758-.719 2.006-1.413.248-.695.248-1.29.173-1.414z"/></svg>';

  /* ── Aviso (criado uma vez) ── */
  var aviso = document.createElement('div');
  aviso.className = 'if-aviso';
  aviso.setAttribute('role', 'dialog');
  aviso.setAttribute('aria-modal', 'true');
  aviso.setAttribute('aria-labelledby', 'if-aviso-titulo');
  aviso.setAttribute('aria-hidden', 'true');
  aviso.innerHTML =
    '<div class="if-aviso__caixa" tabindex="-1">' +
    '<button type="button" class="if-aviso__x" data-if-fechar aria-label="Fechar">&times;</button>' +
    '<div class="if-aviso__icone">' + ICONE_WHATS + '</div>' +
    '<h2 class="if-aviso__titulo" id="if-aviso-titulo">Fale com a nossa equipe</h2>' +
    '<p class="if-aviso__texto">Entre em contato pelo nosso WhatsApp.<br>Nossa equipe vai te atender.</p>' +
    '<p class="if-aviso__produto" data-if-produto hidden></p>' +
    '<a class="if-aviso__botao" data-if-whats href="https://wa.me/' + WHATSAPP + '" target="_blank" rel="noopener">' +
    ICONE_WHATS.replace('width="34" height="34"', 'width="22" height="22"') +
    '<span>Chamar no WhatsApp</span></a>' +
    '<button type="button" class="if-aviso__fechar-texto" data-if-fechar>Fechar</button>' +
    '</div>';

  var linhaProduto = aviso.querySelector('[data-if-produto]');
  var botaoWhats = aviso.querySelector('[data-if-whats]');
  var focoAnterior = null;

  function montarAviso() {
    if (!aviso.isConnected) document.body.appendChild(aviso);
  }

  function abrir(produto, mensagem) {
    montarAviso();
    var texto =
      mensagem ||
      (produto
        ? 'Olá! Vim pelo site da Inda Fire e gostaria de saber mais sobre: ' + produto + '.'
        : 'Olá! Vim pelo site da Inda Fire e gostaria de atendimento.');
    botaoWhats.href = 'https://wa.me/' + WHATSAPP + '?text=' + encodeURIComponent(texto);
    if (produto) {
      linhaProduto.innerHTML = '';
      var rotulo = document.createTextNode('Produto: ');
      var nome = document.createElement('strong');
      nome.textContent = produto;
      linhaProduto.appendChild(rotulo);
      linhaProduto.appendChild(nome);
      linhaProduto.hidden = false;
    } else {
      linhaProduto.hidden = true;
    }
    focoAnterior = document.activeElement;
    aviso.setAttribute('aria-hidden', 'false');
    aviso.classList.add('if-aberto');
    document.documentElement.classList.add('if-aviso-trava');
    window.setTimeout(function () {
      aviso.querySelector('.if-aviso__caixa').focus();
    }, 60);
  }

  function fechar() {
    aviso.classList.remove('if-aberto');
    aviso.setAttribute('aria-hidden', 'true');
    document.documentElement.classList.remove('if-aviso-trava');
    if (focoAnterior && typeof focoAnterior.focus === 'function') focoAnterior.focus();
  }

  aviso.addEventListener('click', function (e) {
    if (e.target === aviso || e.target.closest('[data-if-fechar]')) fechar();
  });
  // depois de abrir o WhatsApp, o aviso fecha (a pessoa volta e o site está normal)
  botaoWhats.addEventListener('click', function () {
    window.setTimeout(fechar, 400);
  });
  document.addEventListener('keydown', function (e) {
    if (!aviso.classList.contains('if-aberto')) return;
    if (e.key === 'Escape') fechar();
    if (e.key === 'Tab') {
      // foco preso dentro do aviso
      var focaveis = aviso.querySelectorAll('a[href],button');
      var primeiro = focaveis[0];
      var ultimo = focaveis[focaveis.length - 1];
      if (e.shiftKey && document.activeElement === primeiro) {
        e.preventDefault();
        ultimo.focus();
      } else if (!e.shiftKey && document.activeElement === ultimo) {
        e.preventDefault();
        primeiro.focus();
      }
    }
  });

  /* ── Nome do produto ── */
  function limpar(t) {
    return (t || '').replace(/\s+/g, ' ').trim();
  }

  function nomeDoCartao(el) {
    var cartao = el.closest('article.product, .product, .dce-post, .areaProduto');
    if (cartao) {
      var titulo = cartao.querySelector('.tituloProduto .elementor-heading-title, .woocommerce-loop-product__title, h2, h3, h4');
      if (titulo) return limpar(titulo.textContent);
    }
    return '';
  }

  function nomeDaPagina() {
    var h1 = document.querySelector('.product_title, h1.elementor-heading-title, h1');
    var nome = h1 ? limpar(h1.textContent) : '';
    if (!nome) nome = limpar(document.title.split(' - ')[0]);
    // títulos em caixa alta no layout: o texto original vem do <title>
    var doTitulo = limpar(document.title.split(' - ')[0]);
    if (doTitulo && doTitulo.toUpperCase() === nome.toUpperCase()) nome = doTitulo;
    return nome;
  }

  function nomeDoLink(a) {
    var m = (a.getAttribute('href') || '').match(/produto\/([a-z0-9-]+)\/?/i);
    if (!m) return '';
    var s = m[1].replace(/-/g, ' ');
    return s.charAt(0).toUpperCase() + s.slice(1);
  }

  /* ── Cliques: tudo que levaria a um produto abre o aviso ── */
  function ehLinkDeProduto(a) {
    var href = a.getAttribute('href') || '';
    return /(^|\/)produto\/[a-z0-9-]+\/?(#.*)?$/i.test(href) && !/categoria-produto/i.test(href);
  }

  document.addEventListener(
    'click',
    function (e) {
      if (e.defaultPrevented || e.button > 0 || e.metaKey || e.ctrlKey || e.shiftKey || e.altKey) return;
      var alvo = e.target;
      if (!alvo || !alvo.closest || alvo.closest('.if-aviso')) return;

      var a = alvo.closest('a[href]');
      var produto = '';

      if (naPagina) {
        // "Solicite orçamento" (âncora #orcamento) e botões de orçamento
        if (a && /#orcamento\b/i.test(a.getAttribute('href') || '')) {
          produto = nomeDaPagina();
        } else if (a && ehLinkDeProduto(a)) {
          // produtos relacionados
          produto = nomeDoCartao(a) || nomeDoLink(a);
        } else if (!a && alvo.closest('article.product [data-ha-element-link]')) {
          produto = nomeDoCartao(alvo);
        } else {
          return;
        }
      } else {
        // listas: cartão inteiro (o cartão é clicável pelo Happy Addons), "Veja +" e "Conheça"
        if (a && ehLinkDeProduto(a)) {
          produto = nomeDoCartao(a) || nomeDoLink(a);
        } else if (!a && alvo.closest('article.product')) {
          produto = nomeDoCartao(alvo);
        } else if (!a) {
          var link = alvo.closest('[data-ha-element-link]');
          if (!link || !/produto\\?\/[a-z0-9-]+/i.test(link.getAttribute('data-ha-element-link') || '') ||
              /categoria-produto/i.test(link.getAttribute('data-ha-element-link') || '')) return;
          produto = nomeDoCartao(alvo);
        } else {
          return;
        }
      }

      e.preventDefault();
      e.stopPropagation();
      e.stopImmediatePropagation();
      abrir(produto);
    },
    true,
  );

  /* ── Formulário "Solicite seu orçamento": vai pelo WhatsApp com os dados ── */
  document.addEventListener(
    'submit',
    function (e) {
      var form = e.target;
      if (!form || form.getAttribute('name') !== 'Produto') return;
      e.preventDefault();
      e.stopPropagation();
      e.stopImmediatePropagation();

      function valor(nome) {
        var campo = form.querySelector('[name="form_fields[' + nome + ']"]');
        return campo ? limpar(campo.value) : '';
      }

      var nome = valor('nome');
      var telefone = valor('telefone');
      if (!nome) {
        var campoNome = form.querySelector('[name="form_fields[nome]"]');
        if (campoNome) campoNome.focus();
        return;
      }

      var produto = valor('produto') || nomeDaPagina();
      var partes = ['Olá! Meu nome é ' + nome + '.'];
      if (produto) partes.push('Gostaria de um orçamento de: ' + produto + '.');
      if (telefone) partes.push('Telefone: ' + telefone + '.');
      var email = valor('email');
      if (email) partes.push('E-mail: ' + email + '.');
      var obs = valor('observacoes');
      if (obs) partes.push('Observações: ' + obs);
      abrir(produto, partes.join(' '));
    },
    true,
  );
})();
