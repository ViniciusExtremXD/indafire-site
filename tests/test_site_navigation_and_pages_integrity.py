import os
import re
import pytest

REPO_DIR = r"c:\Users\Vini_\OneDrive - Instituto Presbiteriano Mackenzie\Área de Trabalho\Vesta\Projeto\Freelance\Sites Grupo Alvo\Indafire"

IGNORE_DIRS = {
    '.git', 'node_modules', 'audit', 'baseline', 'baseline-factual-1', 
    'baseline-pristine', 'tests', '.gemini', 'dist_gh_pages', 'screenshots',
    'wp-content', 'wp-includes', 'staging-local', '.worktrees'
}

def get_site_html_files():
    html_files = []
    for root, dirs, files in os.walk(REPO_DIR):
        dirs[:] = [d for d in dirs if d not in IGNORE_DIRS]
        for f in files:
            if f.endswith('.html'):
                html_files.append(os.path.join(root, f))
    return html_files

def test_site_pages_count_and_core_routes():
    pages = get_site_html_files()
    rel_pages = [os.path.relpath(p, REPO_DIR).replace('\\', '/') for p in pages]
    
    assert len(rel_pages) >= 60, f"Expected at least 60 pages, found {len(rel_pages)}"
    
    expected_core = [
        "index.html",
        "404.html",
        "servicos/index.html",
        "produtos/index.html",
        "sobre-nos/index.html",
        "treinamentos/index.html",
        "blog/index.html",
        "contato/index.html",
        "area-do-cliente/index.html",
        "politica-de-privacidade/index.html",
        "treinamentos/brigada-de-incendio/index.html",
        "treinamentos/unidade-de-treinamento-movel/index.html",
        "treinamentos/cursos-online/index.html",
        "blog/beneficios-extintores-espuma-incendios/index.html",
        "blog/como-inspecionar-e-manter-seus-extintores-em-condicoes-ideais-passo-a-passo/index.html",
        "blog/os-diferentes-tipos-de-extintores-como-escolher-o-certo-para-cada-situacao/index.html",
        "blog/seguranca-contra-incendios-em-eventos-ao-vivo-o-que-voce-deve-saber/index.html",
        "blog/sistemas-de-seguranca/index.html"
    ]
    for page in expected_core:
        assert page in rel_pages, f"Missing required core page: {page}"

def test_no_broken_internal_links():
    pages = get_site_html_files()
    broken = []
    
    for filepath in pages:
        rel_file = os.path.relpath(filepath, REPO_DIR).replace('\\', '/')
        file_dir = os.path.dirname(filepath)
        with open(filepath, 'r', encoding='utf-8', errors='ignore') as fp:
            c = fp.read()
        
        for m in re.finditer(r'href=["\']([^"\'#][^"\']*)["\']', c):
            href = m.group(1).strip()
            if any(href.startswith(p) for p in ['http://', 'https://', 'mailto:', 'tel:', 'javascript:', '#', 'data:', '//']):
                continue
            if href in ('itemDataObject.url', '{{{data.link}}}'):
                continue
            clean = href.split('?')[0]
            target = os.path.normpath(os.path.join(file_dir, clean))
            exists = (
                os.path.isfile(target) or 
                (os.path.isdir(target) and os.path.exists(os.path.join(target, 'index.html'))) or
                os.path.exists(target + '.html') or
                os.path.exists(os.path.join(target, 'index.html'))
            )
            if not exists:
                broken.append((rel_file, href, target))
    
    assert len(broken) == 0, f"Found {len(broken)} broken links: {broken[:10]}"

def test_mandatory_elements_in_all_pages():
    pages = get_site_html_files()
    elements = {
        "map": ['id="localizacao_mapa"', "inda-location-section", "google.com/maps", "maps.google"],
        "whatsapp": ["indafire-whatsapp-section", "indafire-commercial-whatsapp", "sendIndafireWhatsApp", "api.whatsapp.com"],
        "newsletter": ["formulario_newsletter", "Assine nossa newsletter", "newsletter"],
        "catalogo": ["formulario_catalogo", "Baixe nosso catálogo", "catalogo-inda-fire", "modal_catalogo"]
    }
    
    for filepath in pages:
        rel_file = os.path.relpath(filepath, REPO_DIR).replace('\\', '/')
        with open(filepath, 'r', encoding='utf-8', errors='ignore') as fp:
            content = fp.read()
        
        for el_name, patterns in elements.items():
            found = any(k in content for k in patterns)
            assert found, f"Page '{rel_file}' is missing mandatory element '{el_name}'"

def test_smart_404_reconciliation_script():
    fpath = os.path.join(REPO_DIR, "404.html")
    assert os.path.exists(fpath), "404.html does not exist"
    with open(fpath, 'r', encoding='utf-8') as fp:
        c = fp.read()
    assert "window.location.replace" in c, "404.html must contain auto-redirect logic"
    assert "/servicos/" in c and "/produtos/" in c, "404.html must contain section recovery mappings"

def test_no_external_indafire_links_in_content():
    pages = get_site_html_files()
    external_links = []
    
    for filepath in pages:
        rel_file = os.path.relpath(filepath, REPO_DIR).replace('\\', '/')
        with open(filepath, 'r', encoding='utf-8', errors='ignore') as fp:
            c = fp.read()
            
        for m in re.finditer(r'href=["\']([^"\'#][^"\']*)["\']', c):
            href = m.group(1).strip()
            if href.startswith('mailto:') or 'login2.php' in href:
                continue
            if 'indafire.com.br' in href or 'indafire.ind.br' in href:
                external_links.append((rel_file, href))
                
    assert len(external_links) == 0, f"Found unwanted external indafire links: {external_links}"

def test_responsive_navigation_injected_in_all_pages():
    pages = get_site_html_files()
    missing_script = []
    missing_style = []
    missing_modal = []
    
    for filepath in pages:
        rel_file = os.path.relpath(filepath, REPO_DIR).replace('\\', '/')
        with open(filepath, 'r', encoding='utf-8', errors='ignore') as fp:
            c = fp.read()
            
        if 'id="indafire-responsive-navigation"' not in c:
            missing_script.append(rel_file)
        if 'id="indafire-responsive-navigation-style"' not in c:
            missing_style.append(rel_file)
        if 'elementor-2519' not in c:
            missing_modal.append(rel_file)
            
    assert len(missing_script) == 0, f"Pages missing responsive script: {missing_script}"
    assert len(missing_style) == 0, f"Pages missing responsive style: {missing_style}"
    assert len(missing_modal) == 0, f"Pages missing popup modal 2519: {missing_modal}"

