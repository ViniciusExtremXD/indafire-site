"""Build the static Blog page for Indafire."""

from __future__ import annotations

from pathlib import Path
import re
import sys

ROOT = Path(r"c:\Users\Vini_\OneDrive - Instituto Presbiteriano Mackenzie\Área de Trabalho\Vesta\Projeto\Freelance\Sites Grupo Alvo\Indafire")
BLOG_HTML = ROOT / "blog" / "index.html"
SCRATCH_CONTENT = ROOT / "scratch_blog_content.html"

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
.elementor-element-b1cf804 {
  padding: 50px 20px 70px 20px !important;
  max-width: 1200px !important;
  margin: 0 auto !important;
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
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.07) !important;
  transition: transform 0.25s ease, box-shadow 0.25s ease !important;
  display: flex !important;
  flex-direction: column !important;
  justify-content: space-between !important;
  border: 1px solid #eef0f4 !important;
}
.ha-pg-item:hover {
  transform: translateY(-5px) !important;
  box-shadow: 0 14px 32px rgba(0, 0, 0, 0.12) !important;
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
  transform: scale(1.05) !important;
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
/* Hero banner */
.elementor-element-6dcc59d {
  background: linear-gradient(135deg, #12171c 0%, #1d252c 100%) !important;
  padding: 70px 20px 50px 20px !important;
  margin-top: 0 !important;
  margin-bottom: 0 !important;
  text-align: center !important;
}
.elementor-element-6dcc59d .elementor-heading-title {
  color: #ffffff !important;
  font-size: clamp(28px, 5vw, 42px) !important;
  font-weight: 800 !important;
  letter-spacing: 1px !important;
  text-transform: uppercase !important;
  margin: 0 !important;
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

    # Insert WhatsApp section right before the end of wp-page
    last_closing_divs = html.rfind("</div>\n\t\t\t</div>\n\t\t\t\t\t</div>")
    if last_closing_divs != -1:
        html = html[:last_closing_divs] + "\n" + WHATSAPP_SECTION + "\n" + html[last_closing_divs:]
    else:
        last_div = html.rfind("</div>")
        html = html[:last_div] + "\n" + WHATSAPP_SECTION + "\n" + html[last_div:]

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
