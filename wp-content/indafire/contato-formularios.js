/*
 * Inda Fire — formulários de /contato/ no site estático (19/11/2026).
 *
 * O site não tem mais o WordPress, que enviava esses formulários por e-mail. Para nenhum contato se perder:
 *  - "Fale Conosco": ao enviar, abre o WhatsApp da Inda Fire com os dados já escritos (a medição conta como
 *    contato_whatsapp, origem "formulario"), e mostra um aviso com o link caso o navegador bloqueie a janela.
 *  - "Trabalhe Conosco": currículo não vai por WhatsApp. O formulário mostra o e-mail certo e abre a mensagem
 *    já preenchida. Esse e-mail NÃO conta como contato comercial na medição (data-if-nao-conta).
 *
 * Arquivo único, sem dependências.
 */
(function () {
  'use strict';

  var WHATSAPP = '551938341741';
  var EMAIL_CURRICULO = 'atendimento@indafire.com.br';

  function limpar(t) {
    return (t || '').replace(/\s+/g, ' ').trim();
  }
  function campo(form, nome) {
    var c = form.querySelector('[name="form_fields[' + nome + ']"]');
    return c ? limpar(c.value) : '';
  }
  function aviso(form, html, classe) {
    var caixa = form.querySelector('.if-form-aviso');
    if (!caixa) {
      caixa = document.createElement('div');
      caixa.className = 'if-form-aviso';
      caixa.setAttribute('role', 'status');
      form.appendChild(caixa);
    }
    caixa.className = 'if-form-aviso ' + (classe || '');
    caixa.innerHTML = html;
  }
  function esc(t) {
    return String(t).replace(/[&<>"]/g, function (c) {
      return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c];
    });
  }

  var estilo = document.createElement('style');
  estilo.textContent =
    '.if-form-aviso{margin:18px 0 0;padding:16px 18px;border-radius:10px;background:#f1f5f9;color:#1e293b;font:600 16px/1.5 "Open Sans",Arial,sans-serif}' +
    '.if-form-aviso a{color:#e30613;text-decoration:underline;word-break:break-all}' +
    '.if-form-aviso--ok{background:#ecfdf3;border:1px solid #86efac}' +
    '.if-form-aviso small{display:block;margin-top:6px;font-weight:400;color:#475569}';
  document.head.appendChild(estilo);

  // Trabalhe Conosco: sem anexo (não há servidor para receber o arquivo); tira a exigência do campo de arquivo
  var trabalhe = document.querySelector('form[name="Trabalhe Conosco"]');
  if (trabalhe) {
    var arquivo = trabalhe.querySelector('input[type="file"]');
    if (arquivo) {
      arquivo.required = false;
      arquivo.removeAttribute('required');
      arquivo.removeAttribute('aria-required');
      var grupo = arquivo.closest('.elementor-field-group');
      if (grupo) grupo.style.display = 'none';
    }
    var grupos = trabalhe.querySelectorAll('.elementor-field-type-html');
    Array.prototype.forEach.call(grupos, function (g) {
      if (/curr[ií]culo/i.test(g.textContent)) {
        g.textContent = 'Ao enviar, abrimos um e-mail pronto para você anexar o currículo em PDF.';
      }
    });
  }

  document.addEventListener(
    'submit',
    function (e) {
      var form = e.target;
      var nomeForm = form && form.getAttribute ? form.getAttribute('name') : '';
      if (nomeForm !== 'Fale Conosco' && nomeForm !== 'Trabalhe Conosco') return;
      e.preventDefault();
      e.stopPropagation();
      e.stopImmediatePropagation();

      var nome = campo(form, 'nome');
      var email = campo(form, 'email');
      var telefone = campo(form, 'telefone');

      if (nomeForm === 'Fale Conosco') {
        var partes = ['Olá! Me chamo ' + nome];
        var empresa = campo(form, 'empresa');
        if (empresa) partes[0] += ', da empresa ' + empresa;
        partes[0] += '.';
        var mensagem = campo(form, 'mensagem');
        if (mensagem) partes.push(mensagem);
        if (telefone) partes.push('Telefone: ' + telefone + '.');
        if (email) partes.push('E-mail: ' + email + '.');
        var url = 'https://wa.me/' + WHATSAPP + '?text=' + encodeURIComponent(partes.join(' '));
        window.open(url, '_blank');
        aviso(
          form,
          'Abrimos o WhatsApp com a sua mensagem. Nossa equipe vai te atender.' +
            '<small>Se a janela não abriu, <a href="' + esc(url) + '" target="_blank" rel="noopener">clique aqui para falar com a gente</a>.</small>',
          'if-form-aviso--ok',
        );
        return;
      }

      // Trabalhe Conosco
      var assunto = 'Currículo - ' + (nome || 'candidato');
      var corpo = 'Olá! Segue meu currículo em anexo (PDF).\n\nNome: ' + nome + '\nTelefone: ' + telefone + '\nE-mail: ' + email;
      var mailto = 'mailto:' + EMAIL_CURRICULO + '?subject=' + encodeURIComponent(assunto) + '&body=' + encodeURIComponent(corpo);
      aviso(
        form,
        'Para enviar o seu currículo, mande um e-mail para <strong>' + EMAIL_CURRICULO + '</strong> com o arquivo em PDF anexado.' +
          '<small><a href="' + esc(mailto) + '" data-if-nao-conta>Abrir o e-mail já preenchido</a></small>',
        'if-form-aviso--ok',
      );
      var link = form.querySelector('.if-form-aviso a');
      if (link) link.click();
    },
    true,
  );
})();
