"""Build the static Blog page for Indafire."""

from __future__ import annotations

from pathlib import Path
import re
import sys

ROOT = Path(r"c:\Users\Vini_\OneDrive - Instituto Presbiteriano Mackenzie\Área de Trabalho\Vesta\Projeto\Freelance\Sites Grupo Alvo\Indafire")
BLOG_HTML = ROOT / "blog" / "index.html"
SCRATCH_CONTENT = ROOT / "scratch_blog_content.html"

INSTAGRAM_SECTION = """<!-- SEÇÃO INSTAGRAM SHOWCASE -->
<section class="inda-instagram-section">
  <div class="inda-insta-container">
    <div class="inda-insta-header">
      <div class="inda-insta-badge">
        <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="currentColor"><path d="M12 2.163c3.204 0 3.584.012 4.85.07 3.252.148 4.771 1.691 4.919 4.919.058 1.265.069 1.645.069 4.849 0 3.205-.012 3.584-.069 4.849-.149 3.225-1.664 4.771-4.919 4.919-1.266.058-1.644.07-4.85.07-3.204 0-3.584-.012-4.849-.07-3.26-.149-4.771-1.699-4.919-4.92-.058-1.265-.07-1.644-.07-4.849 0-3.204.013-3.583.07-4.849.149-3.227 1.664-4.771 4.919-4.919 1.266-.057 1.645-.069 4.849-.069zm0-2.163c-3.259 0-3.667.014-4.947.072-4.358.2-6.78 2.618-6.98 6.98-.059 1.281-.073 1.689-.073 4.948 0 3.259.014 3.668.072 4.948.2 4.358 2.618 6.78 6.98 6.98 1.281.058 1.689.072 4.948.072 3.259 0 3.668-.014 4.948-.072 4.354-.2 6.782-2.618 6.979-6.98.059-1.28.073-1.689.073-4.948 0-3.259-.014-3.667-.072-4.947-.196-4.354-2.617-6.78-6.979-6.98-1.281-.059-1.69-.073-4.949-.073zm0 5.838c-3.403 0-6.162 2.759-6.162 6.162s2.759 6.163 6.162 6.163 6.162-2.759 6.162-6.163c0-3.403-2.759-6.162-6.162-6.162zm0 10.162c-2.209 0-4-1.79-4-4 0-2.209 1.791-4 4-4s4 1.791 4 4c0 2.21-1.791 4-4 4zm6.406-11.845c-.796 0-1.441.645-1.441 1.44s.645 1.44 1.441 1.44c.795 0 1.439-.645 1.439-1.44s-.644-1.44-1.439-1.44z"/></svg>
        <span>Instagram Oficial</span>
      </div>
      <h2 class="inda-insta-title">Acompanhe Nosso Trabalho em Tempo Real</h2>
      <p class="inda-insta-subtitle">Treinamentos, vistorias técnicas, testes de hidrantes e bastidores das nossas operações diárias diretamente no Instagram da Inda Fire.</p>
      <a href="https://www.instagram.com/inda.fire/" target="_blank" rel="noopener noreferrer" class="inda-insta-profile-btn">
        <svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="currentColor"><path d="M12 2.163c3.204 0 3.584.012 4.85.07 3.252.148 4.771 1.691 4.919 4.919.058 1.265.069 1.645.069 4.849 0 3.205-.012 3.584-.069 4.849-.149 3.225-1.664 4.771-4.919 4.919-1.266.058-1.644.07-4.85.07-3.204 0-3.584-.012-4.849-.07-3.26-.149-4.771-1.699-4.919-4.92-.058-1.265-.07-1.644-.07-4.849 0-3.204.013-3.583.07-4.849.149-3.227 1.664-4.771 4.919-4.919 1.266-.057 1.645-.069 4.849-.069zm0-2.163c-3.259 0-3.667.014-4.947.072-4.358.2-6.78 2.618-6.98 6.98-.059 1.281-.073 1.689-.073 4.948 0 3.259.014 3.668.072 4.948.2 4.358 2.618 6.78 6.98 6.98 1.281.058 1.689.072 4.948.072 3.259 0 3.668-.014 4.948-.072 4.354-.2 6.782-2.618 6.979-6.98.059-1.28.073-1.689.073-4.948 0-3.259-.014-3.667-.072-4.947-.196-4.354-2.617-6.78-6.979-6.98-1.281-.059-1.69-.073-4.949-.073zm0 5.838c-3.403 0-6.162 2.759-6.162 6.162s2.759 6.163 6.162 6.163 6.162-2.759 6.162-6.163c0-3.403-2.759-6.162-6.162-6.162zm0 10.162c-2.209 0-4-1.79-4-4 0-2.209 1.791-4 4-4s4 1.791 4 4c0 2.21-1.791 4-4 4zm6.406-11.845c-.796 0-1.441.645-1.441 1.44s.645 1.44 1.441 1.44c.795 0 1.439-.645 1.439-1.44s-.644-1.44-1.439-1.44z"/></svg>
        <span>Seguir @inda.fire</span>
      </a>
    </div>

    <div class="inda-insta-grid">
      <a href="https://www.instagram.com/inda.fire/" target="_blank" rel="noopener noreferrer" class="inda-insta-card">
        <div class="inda-insta-img-wrap">
          <img src="../wp-content/uploads/2021/10/bombeiro.jpg" alt="Treinamento de Brigada de Incêndio" loading="lazy">
          <div class="inda-insta-overlay">
            <span class="inda-insta-tag">Treinamentos</span>
            <p class="inda-insta-desc">Formação prática de Brigada de Incêndio com simulação real e certificação.</p>
            <span class="inda-insta-view">Ver no Instagram &rarr;</span>
          </div>
        </div>
      </a>

      <a href="https://www.instagram.com/inda.fire/" target="_blank" rel="noopener noreferrer" class="inda-insta-card">
        <div class="inda-insta-img-wrap">
          <img src="../wp-content/uploads/2023/11/prevencao-a-incendio-em-grandes-eventos.jpg" alt="Prevenção em Eventos e AVCB" loading="lazy">
          <div class="inda-insta-overlay">
            <span class="inda-insta-tag">AVCB &amp; Projetos</span>
            <p class="inda-insta-desc">Segurança contra incêndio em eventos e consultoria para emissão do AVCB.</p>
            <span class="inda-insta-view">Ver no Instagram &rarr;</span>
          </div>
        </div>
      </a>

      <a href="https://www.instagram.com/inda.fire/" target="_blank" rel="noopener noreferrer" class="inda-insta-card">
        <div class="inda-insta-img-wrap">
          <img src="../wp-content/uploads/2021/10/hidrantes.jpg" alt="Manutenção de Hidrantes" loading="lazy">
          <div class="inda-insta-overlay">
            <span class="inda-insta-tag">Manutenção Técnica</span>
            <p class="inda-insta-desc">Testes hidrostáticos em mangueiras e manutenção completa de hidrantes.</p>
            <span class="inda-insta-view">Ver no Instagram &rarr;</span>
          </div>
        </div>
      </a>

      <a href="https://www.instagram.com/inda.fire/" target="_blank" rel="noopener noreferrer" class="inda-insta-card">
        <div class="inda-insta-img-wrap">
          <img src="../wp-content/uploads/2021/10/iluminacao.jpg" alt="Sistemas de Emergência" loading="lazy">
          <div class="inda-insta-overlay">
            <span class="inda-insta-tag">Sistemas de Alarme</span>
            <p class="inda-insta-desc">Instalação de blocos de iluminação de emergência e rotas de fuga seguras.</p>
            <span class="inda-insta-view">Ver no Instagram &rarr;</span>
          </div>
        </div>
      </a>
    </div>

    <div class="inda-insta-footer">
      <p class="inda-insta-footer-text">
        Fique por dentro das normas do Corpo de Bombeiros, dicas de segurança e cases reais.
      </p>
      <a href="https://www.instagram.com/inda.fire/" target="_blank" rel="noopener noreferrer" class="inda-insta-cta-link">
        Conheça nosso perfil oficial @inda.fire &rarr;
      </a>
    </div>
  </div>
</section>
"""

WHATSAPP_SECTION = """<!-- SEÇÃO WHATSAPP -->
<section class="indafire-whatsapp-section" style="padding: 60px 20px; background: #f8fafc; border-top: 1px solid #e2e8f0; border-bottom: 1px solid #e2e8f0;">
  <div style="max-width: 620px; width: 100%; margin: 0 auto; box-sizing: border-box; font-family: 'Open Sans', sans-serif;">
    <div class="indafire-whatsapp-card" style="width: 100%; background: #ffffff; border-radius: 16px; padding: 32px 28px; box-shadow: 0 10px 25px -5px rgba(0,0,0,0.06), 0 8px 10px -6px rgba(0,0,0,0.04); border: 1px solid #e2e8f0; box-sizing: border-box;">
      <div style="text-align: center; margin-bottom: 22px;">
        <div style="display: inline-flex; align-items: center; justify-content: center; width: 52px; height: 52px; background-color: #25D366; border-radius: 50%; color: #fff; font-size: 26px; margin-bottom: 12px; box-shadow: 0 4px 14px rgba(37,211,102,0.35);">
          <svg xmlns="http://www.w3.org/2000/svg" width="28" height="28" viewBox="0 0 24 24" fill="#ffffff"><path d="M.057 24l1.687-6.163c-1.041-1.804-1.588-3.849-1.587-5.946.003-6.556 5.338-11.891 11.893-11.891 3.181.001 6.167 1.24 8.413 3.488 2.245 2.248 3.481 5.236 3.48 8.414-.003 6.557-5.338 11.892-11.893 11.892-1.99-.001-3.951-.5-5.688-1.448l-6.305 1.654zm6.597-3.807c1.676.995 3.276 1.591 5.392 1.592 5.448 0 9.886-4.434 9.889-9.885.002-5.462-4.415-9.89-9.881-9.892-5.452 0-9.887 4.434-9.889 9.884-.001 2.225.651 3.891 1.746 5.634l-.999 3.648 3.742-.981zm11.387-5.464c-.074-.124-.272-.198-.57-.347-.297-.149-1.758-.868-2.031-.967-.272-.099-.47-.149-.669.149-.198.297-.768.967-.941 1.165-.173.198-.347.223-.644.074-.297-.149-1.255-.462-2.39-1.475-.883-.788-1.48-1.761-1.653-2.059-.173-.297-.018-.458.13-.606.134-.133.297-.347.446-.521.151-.172.2-.296.3-.495.099-.198.05-.372-.025-.521-.075-.148-.669-1.611-.916-2.206-.242-.579-.487-.501-.669-.51l-.57-.01c-.198 0-.52.074-.792.372s-1.04 1.016-1.04 2.479 1.065 2.876 1.213 3.074c.149.198 2.095 3.2 5.076 4.487.709.306 1.263.489 1.694.626.712.226 1.36.194 1.872.118.571-.085 1.758-.719 2.006-1.413.248-.695.248-1.29.173-1.414z"/></svg>
        </div>
        <h3 style="margin: 0 0 6px 0; color: #1e293b; font-size: 22px; font-weight: 700; text-transform: uppercase; letter-spacing: 0.5px;">Atendimento via WhatsApp</h3>
        <p style="margin: 0; color: #475569; font-size: 15px; font-weight: 600;">Ficou com alguma dúvida? Entre em contato com o WhatsApp</p>
      </div>
      <form onsubmit="sendIndafireWhatsApp(event)" style="display: flex; flex-direction: column; gap: 14px;">
        <div style="width: 100%; box-sizing: border-box;">
          <label style="display: block; font-size: 13px; font-weight: 600; color: #334155; margin-bottom: 6px;">Seu Nome / Empresa *</label>
          <input type="text" class="wa_nome_input" required placeholder="Nome ou empresa" style="width: 100%; height: 44px; padding: 0 14px; border: 1.5px solid #cbd5e1; border-radius: 8px; font-size: 14px; box-sizing: border-box; outline: none; transition: border-color 0.2s;" onfocus="this.style.borderColor='#25D366'" onblur="this.style.borderColor='#cbd5e1'">
        </div>
        <div style="width: 100%; box-sizing: border-box;">
          <label style="display: block; font-size: 13px; font-weight: 600; color: #334155; margin-bottom: 6px;">Mensagem / Dúvida *</label>
          <textarea class="wa_msg_input" required rows="3" placeholder="Como podemos ajudar você hoje?" style="width: 100%; padding: 12px 14px; border: 1.5px solid #cbd5e1; border-radius: 8px; font-size: 14px; box-sizing: border-box; outline: none; resize: vertical; min-height: 80px; transition: border-color 0.2s; font-family: inherit;" onfocus="this.style.borderColor='#25D366'" onblur="this.style.borderColor='#cbd5e1'"></textarea>
        </div>
        <button type="submit" style="background-color: #25D366; color: #ffffff; border: none; border-radius: 50px; height: 48px; padding: 0 24px; font-size: 15px; font-weight: 700; text-transform: uppercase; letter-spacing: 0.5px; cursor: pointer; display: flex; align-items: center; justify-content: center; gap: 10px; transition: background-color 0.2s, transform 0.1s; margin-top: 6px; box-shadow: 0 4px 14px rgba(37,211,102,0.35); width: 100%; box-sizing: border-box;" onmouseover="this.style.backgroundColor='#1ebe5d'; this.style.transform='translateY(-1px)';" onmouseout="this.style.backgroundColor='#25D366'; this.style.transform='none';">
          <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="#ffffff"><path d="M.057 24l1.687-6.163c-1.041-1.804-1.588-3.849-1.587-5.946.003-6.556 5.338-11.891 11.893-11.891 3.181.001 6.167 1.24 8.413 3.488 2.245 2.248 3.481 5.236 3.48 8.414-.003 6.557-5.338 11.892-11.893 11.892-1.99-.001-3.951-.5-5.688-1.448l-6.305 1.654zm6.597-3.807c1.676.995 3.276 1.591 5.392 1.592 5.448 0 9.886-4.434 9.889-9.885.002-5.462-4.415-9.89-9.881-9.892-5.452 0-9.887 4.434-9.889 9.884-.001 2.225.651 3.891 1.746 5.634l-.999 3.648 3.742-.981zm11.387-5.464c-.074-.124-.272-.198-.57-.347-.297-.149-1.758-.868-2.031-.967-.272-.099-.47-.149-.669.149-.198.297-.768.967-.941 1.165-.173.198-.347.223-.644.074-.297-.149-1.255-.462-2.39-1.475-.883-.788-1.48-1.761-1.653-2.059-.173-.297-.018-.458.13-.606.134-.133.297-.347.446-.521.151-.172.2-.296.3-.495.099-.198.05-.372-.025-.521-.075-.148-.669-1.611-.916-2.206-.242-.579-.487-.501-.669-.51l-.57-.01c-.198 0-.52.074-.792.372s-1.04 1.016-1.04 2.479 1.065 2.876 1.213 3.074c.149.198 2.095 3.2 5.076 4.487.709.306 1.263.489 1.694.626.712.226 1.36.194 1.872.118.571-.085 1.758-.719 2.006-1.413.248-.695.248-1.29.173-1.414z"/></svg>
          Enviar Mensagem
        </button>
      </form>
    </div>
  </div>
</section>
<script>
  function sendIndafireWhatsApp(e) {
    e.preventDefault();
    var form = e.target;
    var nome = form.querySelector('.wa_nome_input').value.trim();
    var msg = form.querySelector('.wa_msg_input').value.trim();
    var text = "Olá! Me chamo " + nome + ". " + msg;
    var url = "https://wa.me/551938341741?text=" + encodeURIComponent(text);
    window.open(url, "_blank");
  }
</script>
"""

BLOG_ENHANCED_CSS = """
<style id="indafire-blog-custom-style">
/* Custom polished styling for Indafire Blog */

/* Hero banner */
.elementor-element-6dcc59d {
  background: radial-gradient(circle at 50% 20%, #e30613 0%, #b3040e 55%, #180305 100%) !important;
  padding: 85px 20px 145px 20px !important;
  margin-top: 0 !important;
  margin-bottom: 0 !important;
  text-align: center !important;
  position: relative !important;
  overflow: hidden !important;
}
.elementor-element-6dcc59d::before {
  content: "" !important;
  position: absolute !important;
  top: 0; left: 0; right: 0; bottom: 0 !important;
  background-image: radial-gradient(rgba(255, 255, 255, 0.08) 1px, transparent 1px) !important;
  background-size: 24px 24px !important;
  pointer-events: none !important;
  opacity: 0.6 !important;
}
.elementor-element-6dcc59d .elementor-container {
  position: relative !important;
  z-index: 2 !important;
}
.elementor-element-92e22f0 {
  visibility: visible !important;
  opacity: 1 !important;
}
.inda-blog-hero-content {
  display: flex !important;
  flex-direction: column !important;
  align-items: center !important;
  text-align: center !important;
}
.inda-blog-eyebrow {
  display: inline-flex !important;
  align-items: center !important;
  gap: 8px !important;
  background: rgba(255, 255, 255, 0.16) !important;
  border: 1px solid rgba(255, 255, 255, 0.3) !important;
  color: #ffffff !important;
  padding: 6px 18px !important;
  border-radius: 50px !important;
  font-size: 13px !important;
  font-weight: 700 !important;
  letter-spacing: 1px !important;
  text-transform: uppercase !important;
  margin-bottom: 16px !important;
  backdrop-filter: blur(4px) !important;
}
.inda-blog-eyebrow svg {
  fill: #ffffff !important;
}
.elementor-element-6dcc59d .elementor-heading-title {
  color: #ffffff !important;
  font-size: clamp(30px, 5vw, 44px) !important;
  font-weight: 900 !important;
  letter-spacing: 0.5px !important;
  text-transform: uppercase !important;
  margin: 0 0 14px 0 !important;
  text-shadow: 0 4px 16px rgba(0, 0, 0, 0.35) !important;
}
.inda-blog-lead {
  max-width: 680px !important;
  margin: 0 auto !important;
  color: rgba(255, 255, 255, 0.92) !important;
  font-size: clamp(15px, 2vw, 17px) !important;
  line-height: 1.6 !important;
  font-weight: 400 !important;
}

/* Overlapping Blog Cards Section */
.elementor-element-b1cf804 {
  margin-top: -85px !important;
  position: relative !important;
  z-index: 10 !important;
  max-width: 1200px !important;
  margin-left: auto !important;
  margin-right: auto !important;
  padding: 0 20px 60px 20px !important;
}
@media (max-width: 767px) {
  .elementor-element-b1cf804 {
    margin-top: -55px !important;
    padding: 0 16px 40px 16px !important;
  }
}
.ha-pg-grid-wrap {
  display: grid !important;
  grid-template-columns: repeat(3, 1fr) !important;
  gap: 30px !important;
  padding: 10px 0 20px 0 !important;
}
@media (max-width: 1024px) {
  .ha-pg-grid-wrap {
    grid-template-columns: repeat(2, 1fr) !important;
    gap: 24px !important;
  }
}
@media (max-width: 767px) {
  .ha-pg-grid-wrap {
    grid-template-columns: 1fr !important;
    gap: 24px !important;
    padding: 10px 0 !important;
  }
}
.ha-pg-item {
  background: #ffffff !important;
  border-radius: 14px !important;
  overflow: hidden !important;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.12) !important;
  transition: transform 0.25s ease, box-shadow 0.25s ease !important;
  display: flex !important;
  flex-direction: column !important;
  justify-content: space-between !important;
  border: 1px solid rgba(0, 0, 0, 0.06) !important;
}
.ha-pg-item:hover {
  transform: translateY(-6px) !important;
  box-shadow: 0 18px 40px rgba(0, 0, 0, 0.18) !important;
}
.ha-pg-thumb-area {
  position: relative !important;
  width: 100% !important;
  height: 220px !important;
  overflow: hidden !important;
  background-color: #f1f5f9 !important;
}
.ha-pg-thumb {
  width: 100% !important;
  height: 100% !important;
  display: block !important;
}
.ha-pg-thumb img {
  width: 100% !important;
  height: 100% !important;
  object-fit: cover !important;
  transition: transform 0.4s ease !important;
}
.ha-pg-item:hover .ha-pg-thumb img {
  transform: scale(1.06) !important;
}
.ha-pg-content-area {
  padding: 24px 22px 18px 22px !important;
  flex-grow: 1 !important;
  display: flex !important;
  flex-direction: column !important;
}
.ha-pg-badge {
  margin-bottom: 12px !important;
}
.ha-pg-badge a {
  display: inline-block !important;
  background-color: #e30613 !important;
  color: #ffffff !important;
  font-size: 11px !important;
  font-weight: 700 !important;
  text-transform: uppercase !important;
  letter-spacing: 0.5px !important;
  padding: 4px 10px !important;
  border-radius: 4px !important;
  text-decoration: none !important;
}
.ha-pg-title {
  font-size: 18px !important;
  font-weight: 700 !important;
  line-height: 1.35 !important;
  margin: 0 0 12px 0 !important;
}
.ha-pg-title a {
  color: #1a202c !important;
  text-decoration: none !important;
  transition: color 0.2s ease !important;
}
.ha-pg-title a:hover {
  color: #e30613 !important;
}
.ha-pg-excerpt {
  color: #64748b !important;
  font-size: 14px !important;
  line-height: 1.55 !important;
  margin-bottom: 16px !important;
  flex-grow: 1 !important;
}
.ha-pg-meta-wrap {
  padding: 14px 22px !important;
  background-color: #f8fafc !important;
  border-top: 1px solid #f1f5f9 !important;
}
.ha-pg-meta-wrap ul {
  list-style: none !important;
  padding: 0 !important;
  margin: 0 !important;
  display: flex !important;
  align-items: center !important;
  justify-content: space-between !important;
  font-size: 12px !important;
  color: #94a3b8 !important;
}
.ha-pg-meta-wrap ul li {
  display: inline-flex !important;
  align-items: center !important;
  gap: 5px !important;
}
.ha-pg-meta-wrap a {
  color: #64748b !important;
  text-decoration: none !important;
  display: inline-flex !important;
  align-items: center !important;
  gap: 5px !important;
}
.ha-pg-meta-wrap svg {
  width: 14px !important;
  height: 14px !important;
  fill: #94a3b8 !important;
}

/* Instagram Showcase Section */
.inda-instagram-section {
  padding: 70px 20px 80px 20px;
  background: linear-gradient(180deg, #f8fafc 0%, #ffffff 100%);
  border-top: 1px solid #e2e8f0;
  border-bottom: 1px solid #e2e8f0;
  font-family: 'Open Sans', sans-serif;
}
.inda-insta-container {
  max-width: 1200px;
  margin: 0 auto;
}
.inda-insta-header {
  text-align: center;
  margin-bottom: 40px;
}
.inda-insta-badge {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  background: linear-gradient(45deg, #f09433, #e6683c, #dc2743, #cc2366, #bc1888);
  color: #ffffff;
  padding: 6px 16px;
  border-radius: 50px;
  font-size: 13px;
  font-weight: 700;
  letter-spacing: 0.5px;
  text-transform: uppercase;
  margin-bottom: 14px;
  box-shadow: 0 4px 14px rgba(220, 39, 67, 0.3);
}
.inda-insta-title {
  font-size: clamp(24px, 3.5vw, 34px);
  font-weight: 800;
  color: #0f172a;
  margin: 0 0 10px 0;
  letter-spacing: -0.5px;
}
.inda-insta-subtitle {
  font-size: 16px;
  color: #64748b;
  max-width: 620px;
  margin: 0 auto 22px auto;
  line-height: 1.55;
}
.inda-insta-profile-btn {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  background: linear-gradient(45deg, #f09433, #e6683c, #dc2743, #cc2366, #bc1888);
  color: #ffffff !important;
  padding: 12px 26px;
  border-radius: 50px;
  font-size: 14px;
  font-weight: 700;
  text-decoration: none;
  box-shadow: 0 4px 16px rgba(220, 39, 67, 0.35);
  transition: transform 0.2s ease, box-shadow 0.2s ease;
}
.inda-insta-profile-btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 8px 22px rgba(220, 39, 67, 0.45);
}
.inda-insta-grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 20px;
  margin-bottom: 30px;
}
@media (max-width: 1024px) {
  .inda-insta-grid {
    grid-template-columns: repeat(2, 1fr);
    gap: 18px;
  }
}
@media (max-width: 560px) {
  .inda-insta-grid {
    grid-template-columns: 1fr;
    gap: 16px;
  }
}
.inda-insta-card {
  display: block;
  text-decoration: none;
  border-radius: 14px;
  overflow: hidden;
  box-shadow: 0 6px 18px rgba(0, 0, 0, 0.07);
  background: #ffffff;
  border: 1px solid #e2e8f0;
  transition: transform 0.25s ease, box-shadow 0.25s ease;
}
.inda-insta-card:hover {
  transform: translateY(-6px);
  box-shadow: 0 16px 32px rgba(0, 0, 0, 0.12);
}
.inda-insta-img-wrap {
  position: relative;
  width: 100%;
  aspect-ratio: 4 / 3;
  overflow: hidden;
  background: #0f172a;
}
.inda-insta-img-wrap img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  display: block;
  transition: transform 0.4s ease;
}
.inda-insta-card:hover .inda-insta-img-wrap img {
  transform: scale(1.08);
}
.inda-insta-overlay {
  position: absolute;
  inset: 0;
  background: linear-gradient(to top, rgba(15, 23, 42, 0.9) 0%, rgba(15, 23, 42, 0.35) 60%, transparent 100%);
  display: flex;
  flex-direction: column;
  justify-content: flex-end;
  padding: 16px;
  color: #ffffff;
}
.inda-insta-tag {
  display: inline-block;
  align-self: flex-start;
  background: #e30613;
  color: #ffffff;
  font-size: 11px;
  font-weight: 700;
  text-transform: uppercase;
  padding: 3px 8px;
  border-radius: 4px;
  margin-bottom: 8px;
  letter-spacing: 0.5px;
}
.inda-insta-desc {
  font-size: 13px;
  font-weight: 500;
  color: #ffffff;
  margin: 0 0 10px 0;
  line-height: 1.4;
}
.inda-insta-view {
  font-size: 12px;
  font-weight: 700;
  color: #fca5a5;
  display: inline-flex;
  align-items: center;
  gap: 5px;
  transition: color 0.2s ease;
}
.inda-insta-card:hover .inda-insta-view {
  color: #ffffff;
}
.inda-insta-footer {
  text-align: center;
  padding-top: 10px;
}
.inda-insta-footer-text {
  font-size: 14px;
  color: #64748b;
  margin: 0 0 8px 0;
}
.inda-insta-cta-link {
  color: #e30613 !important;
  font-weight: 700;
  font-size: 14px;
  text-decoration: none;
  transition: color 0.2s ease, text-decoration 0.2s ease;
}
.inda-insta-cta-link:hover {
  color: #b3040e !important;
  text-decoration: underline;
}
</style>
"""


def _wp_page_bounds(source: str) -> tuple[int, int]:
    opening = re.search(
        r'<div\b(?=[^>]*\bdata-elementor-type=["\']wp-page["\'])[^>]*>',
        source,
        re.I | re.S,
    )
    if opening is None:
        raise ValueError("Missing Elementor wp-page")

    depth = 0
    token_pattern = re.compile(r"<div\b[^>]*>|</div>", re.I | re.S)
    for token in token_pattern.finditer(source, opening.start()):
        if token.group(0).lower().startswith("</div"):
            depth -= 1
            if depth == 0:
                return opening.start(), token.end()
        else:
            depth += 1
    raise ValueError("Unclosed Elementor wp-page shell")


def clean_blog_content(raw_html: str) -> str:
    html = raw_html
    # Replace absolute domain URLs
    html = re.sub(r"https?://indafire\.com\.br/(?:site/)?wp-content/", "../wp-content/", html)
    
    # Fix the 3 article image sources
    html = html.replace(
        "src=\"data:image/svg+xml,%3Csvg%20xmlns='http://www.w3.org/2000/svg'%20viewBox='0%200%20800%20450'%3E%3C/svg%3E\"",
        "src=\"../wp-content/uploads/2023/12/CAPA-ARTIGO-BLOG-INDA-FIRE-3-1024x576.png\""
    )
    html = html.replace(
        "src=\"data:image/svg+xml,%3Csvg%20xmlns='http://www.w3.org/2000/svg'%20viewBox='0%200%20768%20434'%3E%3C/svg%3E\"",
        "src=\"../wp-content/uploads/2023/11/prevencao-a-incendio-em-grandes-eventos.jpg\""
    )
    html = html.replace(
        "src=\"data:image/svg+xml,%3Csvg%20xmlns='http://www.w3.org/2000/svg'%20viewBox='0%200%20800%20366'%3E%3C/svg%3E\"",
        "src=\"../wp-content/uploads/2023/11/1b6bc6f47565f13b197f9c7b60c6c91e-1024x469.jpg\""
    )
    # Remove noscript tags
    html = re.sub(r"<noscript>.*?</noscript>", "", html, flags=re.S)

    # Enhance hero with eyebrow and descriptive lead
    old_heading = '<h1 class="elementor-heading-title elementor-size-default">Blog da inda fire 🔥</h1>'
    new_hero_html = """<div class="inda-blog-hero-content">
  <div class="inda-blog-eyebrow">
    <svg xmlns="http://www.w3.org/2000/svg" width="14" height="14" viewBox="0 0 24 24" fill="currentColor"><path d="M19.484 15.244c-.752 2.766-3.197 4.756-6.147 4.756-3.535 0-6.398-2.864-6.398-6.399 0-2.31 1.229-4.331 3.072-5.462-.12.439-.187.903-.187 1.382 0 2.871 2.219 5.216 5.044 5.394-.131-.482-.204-.988-.204-1.515 0-2.81 1.83-5.201 4.382-6.04-.658 2.502.438 5.485.438 7.884zm-6.147-15.244c-2.484 2.88-5.337 6.438-5.337 10.399 0 4.636 3.763 8.399 8.398 8.399 4.637 0 8.4-3.763 8.4-8.399 0-3.961-2.853-7.519-5.338-10.399-1.258 2.05-2.923 3.639-3.062 5.518-1.026-1.583-1.89-3.376-3.061-5.518z"/></svg>
    <span>Conteúdo Técnico &amp; Prevenção</span>
  </div>
  <h1 class="elementor-heading-title">BLOG DA INDA FIRE 🔥</h1>
  <p class="inda-blog-lead">Artigos técnicos, normas de segurança contra incêndio, exigências do Corpo de Bombeiros e inovações para proteger seu patrimônio e salvar vidas.</p>
</div>"""
    html = html.replace(old_heading, new_hero_html)

    # Insert Instagram and WhatsApp sections right before the end of wp-page
    last_closing_divs = html.rfind("</div>\n\t\t\t</div>\n\t\t\t\t\t</div>")
    if last_closing_divs != -1:
        html = html[:last_closing_divs] + "\n" + INSTAGRAM_SECTION + "\n" + WHATSAPP_SECTION + "\n" + html[last_closing_divs:]
    else:
        last_div = html.rfind("</div>")
        html = html[:last_div] + "\n" + INSTAGRAM_SECTION + "\n" + WHATSAPP_SECTION + "\n" + html[last_div:]

    return html


def build_blog_page() -> None:
    shell = (ROOT / "sobre-nos" / "index.html").read_text(encoding="utf-8")
    scratch = SCRATCH_CONTENT.read_text(encoding="utf-8")

    blog_main = clean_blog_content(scratch)
    start, end = _wp_page_bounds(shell)
    rendered = shell[:start] + blog_main + shell[end:]

    # Metadata
    rendered = re.sub(r"<title>.*?</title>", "<title>Blog - Inda Fire - Equipamentos de Combate a Incêndios</title>", rendered, count=1, flags=re.S)
    rendered = re.sub(r'<link rel="canonical" href="[^"]*"\s*/?>', '<link rel="canonical" href="../blog/" />', rendered, count=1)
    rendered = re.sub(r'(<meta property="og:title" content=")[^"]*("\s*/?>)', r'\1Blog - Inda Fire - Equipamentos de Combate a Incêndios\2', rendered, count=1)
    rendered = re.sub(r'(<meta property="og:url" content=")[^"]*("\s*/?>)', r'\1https://indafire.com.br/blog/\2', rendered, count=1)
    rendered = rendered.replace('referer_title" value="Sobre nós - Inda Fire - Equipamentos de Combate a Incêndios"', 'referer_title" value="Blog - Inda Fire - Equipamentos de Combate a Incêndios"')

    # Replace post-19.css with post-6.css and add ha-6.css and custom styles
    rendered = rendered.replace(
        "../wp-content/uploads/elementor/css/post-19.css",
        "../wp-content/uploads/elementor/css/post-6.css"
    )
    css_injection = (
        "<link rel='stylesheet' id='happy-elementor-addons-6-css' href='../wp-content/uploads/happyaddons/css/ha-6.css' media='all' />\n"
        + BLOG_ENHANCED_CSS
    )
    rendered = rendered.replace("</head>", f"{css_injection}\n</head>", 1)

    BLOG_HTML.parent.mkdir(parents=True, exist_ok=True)
    BLOG_HTML.write_text(rendered, encoding="utf-8")
    print("blog/index.html created successfully!")


if __name__ == "__main__":
    build_blog_page()
