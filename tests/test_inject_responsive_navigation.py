from __future__ import annotations

import base64
import json
import re
import subprocess
import unittest
from pathlib import Path
from tempfile import TemporaryDirectory


class ResponsiveNavigationInjectionTests(unittest.TestCase):
    def test_script_runs_directly_from_the_project_root(self):
        script = Path(__file__).resolve().parents[1] / "scripts" / "inject_responsive_navigation.py"
        root = script.parents[1]

        result = subprocess.run(
            ["python", str(script)],
            cwd=root,
            check=False,
            capture_output=True,
            text=True,
        )

        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("Injected responsive navigation", result.stdout)

    def test_home_href_tracks_the_static_route_depth(self):
        from scripts import inject_responsive_navigation as subject

        root = Path("C:/site")

        self.assertEqual(subject.home_href(root / "index.html", root), "./")
        self.assertEqual(subject.home_href(root / "produtos" / "index.html", root), "../")
        self.assertEqual(
            subject.home_href(root / "produto" / "extintor" / "index.html", root),
            "../../",
        )

    def test_normalizes_only_links_inside_theme_logo_widgets(self):
        from scripts import inject_responsive_navigation as subject

        source = """
        <div class="elementor-widget-theme-site-logo elementor-widget-image">
          <div><a href="./"><img alt="Header logo"></a></div>
        </div>
        <nav><a href="/produtos/">Produtos</a></nav>
        <div class="elementor-widget elementor-widget-theme-site-logo">
          <div><a href='https://indafire.com.br/'><img alt="Footer logo"></a></div>
        </div>
        """

        rendered = subject.normalize_logo_links(source, "../")

        self.assertEqual(rendered.count('href="../"'), 2)
        self.assertIn('href="/produtos/"', rendered)
        self.assertNotIn("https://indafire.com.br/", rendered)

    def test_asset_injection_applies_the_route_specific_logo_href_once(self):
        from scripts import inject_responsive_navigation as subject

        with TemporaryDirectory() as directory:
            root = Path(directory)
            page = root / "produtos" / "index.html"
            page.parent.mkdir(parents=True)
            page.write_text(
                '<html><head></head><body><div class="elementor-widget-theme-site-logo">'
                '<a href="./"><img alt="Inda Fire"></a></div></body></html>',
                encoding="utf-8",
            )

            self.assertEqual(subject.inject_assets((page,), root=root), 1)
            self.assertEqual(subject.inject_assets((page,), root=root), 0)
            rendered = page.read_text(encoding="utf-8")

        self.assertIn('href="../"', rendered)

    def test_injects_one_compact_navigation_layer_before_the_document_closes(self):
        from scripts import inject_responsive_navigation as subject

        source = (
            "<html><head></head><body>"
            '<div id="headerInda">'
            '<a class="top-level-link" href="/area-do-cliente/">Area do cliente</a>'
            '<div class="elementor-element-8755157"><a href="#menu">Menu</a></div>'
            "</div></body></html>"
        )

        rendered = subject.inject(source)

        self.assertEqual(rendered.count(f'id="{subject.STYLE_ID}"'), 1)
        self.assertEqual(rendered.count(f'id="{subject.SCRIPT_ID}"'), 1)
        self.assertLess(rendered.index(f'id="{subject.STYLE_ID}"'), rendered.index("</head>"))
        self.assertLess(rendered.index(f'id="{subject.SCRIPT_ID}"'), rendered.index("</body>"))
        self.assertIn("indafire-compact-client", rendered)
        self.assertIn("max-width: 1100px", rendered)
        self.assertIn("elementor-element-20668c0", rendered)
        self.assertIn("elementor-element-8755157", rendered)
        self.assertIn("aria-expanded", rendered)
        self.assertIn(".jet-sub-mega-menu {\n    white-space: normal !important;", rendered)

    def test_replaces_its_managed_layers_without_duplication(self):
        from scripts import inject_responsive_navigation as subject

        with TemporaryDirectory() as directory:
            page = Path(directory) / "index.html"
            page.write_text("<html><head></head><body></body></html>", encoding="utf-8")

            self.assertEqual(subject.inject_assets((page,)), 1)
            self.assertEqual(subject.inject_assets((page,)), 0)
            rendered = page.read_text(encoding="utf-8")

        self.assertEqual(rendered.count(f'id="{subject.STYLE_ID}"'), 1)
        self.assertEqual(rendered.count(f'id="{subject.SCRIPT_ID}"'), 1)

    def test_ignores_incomplete_documents(self):
        from scripts import inject_responsive_navigation as subject

        self.assertEqual(subject.inject("<head></head>"), "<head></head>")

    def test_desktop_mega_menus_recover_auto_height_when_revealed(self):
        """Hidden Swipers must be measured again when their desktop menu opens."""
        from scripts import inject_responsive_navigation as subject

        encoded_script = base64.b64encode(subject.JS.encode("utf-8")).decode("ascii")
        harness = f"""
const source = Buffer.from('{encoded_script}', 'base64').toString('utf8');
function makeMegaMenu(height) {{
  let hoverListener = null;
  const wrapper = {{ style: {{ height: '' }} }};
  const activeSlide = {{ scrollHeight: height, style: {{ height: '' }} }};
  const siblingSlide = {{ scrollHeight: height + 17, style: {{ height: '' }} }};
  return {{
    wrapper,
    addEventListener(type, listener) {{ if (type === 'mouseenter') hoverListener = listener; }},
    querySelector(selector) {{
      if (selector === '.swiper-wrapper') return wrapper;
      if (selector === '.swiper-slide-active') return activeSlide;
      return null;
    }},
    querySelectorAll(selector) {{ return selector === '.swiper-slide' ? [activeSlide, siblingSlide] : []; }},
    siblingSlide,
    reveal() {{ if (hoverListener) hoverListener(); }}
  }};
}}
const products = makeMegaMenu(306);
const services = makeMegaMenu(207);
const header = {{
  querySelectorAll(selector) {{
    if (selector === '#jet-menu-item-29, #jet-menu-item-30') return [products, services];
    return [];
  }},
  querySelector() {{ return null; }}
}};
global.window = {{
  matchMedia(query) {{ return {{ matches: query.indexOf('min-width') !== -1, addEventListener() {{}} }}; }},
  requestAnimationFrame(callback) {{ callback(); }}
}};
global.document = {{
  readyState: 'complete',
  querySelector(selector) {{ return selector === '#headerInda' ? header : null; }},
  addEventListener() {{}}
}};
global.MutationObserver = class {{ observe() {{}} }};
eval(source);
products.reveal();
services.reveal();
console.log(JSON.stringify({{
  products: products.wrapper.style.height,
  productSlide: products.querySelector('.swiper-slide-active').style.height,
  productSibling: products.siblingSlide.style.height,
  services: services.wrapper.style.height,
  serviceSlide: services.querySelector('.swiper-slide-active').style.height,
  serviceSibling: services.siblingSlide.style.height
}}));
"""
        result = subprocess.run(
            ["node", "-e", harness],
            check=False,
            capture_output=True,
            text=True,
        )

        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(
            json.loads(result.stdout),
            {
                "products": "323px",
                "productSlide": "306px",
                "productSibling": "323px",
                "services": "224px",
                "serviceSlide": "207px",
                "serviceSibling": "224px",
            },
        )

    def test_compact_layer_mounts_and_opens_the_static_popup_content(self):
        """The static build must not depend on Elementor rebuilding Popup 2519."""
        from scripts import inject_responsive_navigation as subject

        encoded_script = base64.b64encode(subject.JS.encode("utf-8")).decode("ascii")
        harness = f"""
const source = Buffer.from('{encoded_script}', 'base64').toString('utf8');
let hamburgerClick = null;
const classes = {{ add() {{}}, remove() {{}}, toggle() {{}} }};
class FakeElement {{
  constructor(tag = 'div') {{
    this.tagName = tag.toUpperCase();
    this.children = [];
    this.attributes = {{}};
    this.style = {{ display: '', setProperty(name, value) {{ this[name] = value; }} }};
    this.className = '';
    this.id = '';
    this.parentElement = null;
    this.classList = classes;
  }}
  appendChild(child) {{ child.parentElement = this; this.children.push(child); return child; }}
  insertBefore(child) {{ return this.appendChild(child); }}
  setAttribute(name, value) {{ this.attributes[name] = String(value); }}
  getAttribute(name) {{ return this.attributes[name] ?? null; }}
  addEventListener(type, listener) {{ if (this === hamburgerLink && type === 'click') hamburgerClick = listener; }}
  cloneNode() {{ const clone = new FakeElement(this.tagName); clone.className = this.className; return clone; }}
  matches(selector) {{ return selector === '#' + this.id || selector.split('.').slice(1).every(name => this.className.split(' ').includes(name)); }}
  querySelector(selector) {{
    for (const child of this.children) {{
      if (child.matches(selector)) return child;
      const nested = child.querySelector(selector);
      if (nested) return nested;
    }}
    return null;
  }}
  querySelectorAll() {{ return []; }}
}}
const body = new FakeElement('body');
const popupTemplate = new FakeElement('div');
popupTemplate.className = 'elementor elementor-2519 elementor-location-popup';
const hamburgerLink = {{
  href: '#menu',
  attributes: {{}},
  setAttribute(name, value) {{ this.attributes[name] = String(value); }},
  getAttribute(name) {{ return this.attributes[name] ?? null; }},
  addEventListener(type, listener) {{ if (type === 'click') hamburgerClick = listener; }}
}};
const hamburger = {{
  parentElement: {{ insertBefore() {{}} }},
  querySelector() {{ return hamburgerLink; }}
}};
const header = {{
  style: {{ setProperty() {{}} }},
  querySelector(selector) {{
    if (selector === '.elementor-element-20668c0') return {{}};
    if (selector === '.elementor-element-8755157') return hamburger;
    if (selector === '.indafire-compact-client') return {{}};
    return null;
  }},
  querySelectorAll() {{ return [{{ textContent: 'Área do cliente', href: '/area-do-cliente/' }}]; }}
}};
global.window = {{
  scrollY: 0,
  matchMedia() {{ return {{ matches: true, addEventListener() {{}} }}; }},
  getComputedStyle(element) {{ return {{ display: element.style?.display || 'none', visibility: 'visible' }}; }},
  setTimeout(callback) {{ callback(); }},
  requestAnimationFrame(callback) {{ callback(); }},
  addEventListener() {{}}
}};
global.document = {{
  readyState: 'complete',
  documentElement: {{ classList: classes }},
  body,
  createElement(tag) {{ return new FakeElement(tag); }},
  querySelector(selector) {{
    if (selector === '#headerInda') return header;
    if (selector === '.elementor-2519') return popupTemplate;
    if (selector === '#elementor-popup-modal-2519') return body.querySelector(selector);
    return null;
  }},
  addEventListener() {{}}
}};
global.MutationObserver = class {{ observe() {{}} }};
eval(source);
let prevented = false;
let stopped = false;
hamburgerClick({{ preventDefault() {{ prevented = true; }}, stopPropagation() {{ stopped = true; }} }});
const modal = document.querySelector('#elementor-popup-modal-2519');
console.log(JSON.stringify({{
  prevented,
  stopped,
  mounted: Boolean(modal && modal.querySelector('.elementor-2519')),
  display: modal && modal.style.display,
  expanded: hamburgerLink.attributes['aria-expanded']
}}));
"""
        result = subprocess.run(
            ["node", "-e", harness],
            check=False,
            capture_output=True,
            text=True,
        )

        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(
            json.loads(result.stdout),
            {
                "prevented": True,
                "stopped": True,
                "mounted": True,
                "display": "flex",
                "expanded": "true",
            },
        )

    def test_legacy_drawer_controller_is_not_initialised(self):
        """The static drawer must be the only popup click owner after injection."""
        from scripts import inject_responsive_navigation as subject

        source = (
            "<html><head></head><body><script>"
            "let drawerInitialisations = 0;"
            "function initMenuDrawer() { drawerInitialisations += 1; }"
            "initMenuDrawer();"
            "console.log(JSON.stringify({drawerInitialisations}));"
            "</script></body></html>"
        )
        rendered = subject.inject(source)
        legacy_script = re.search(r"<script>(.*?)</script>", rendered, re.DOTALL)
        self.assertIsNotNone(legacy_script)
        result = subprocess.run(
            ["node", "-e", legacy_script.group(1)],
            check=False,
            capture_output=True,
            text=True,
        )

        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(json.loads(result.stdout), {"drawerInitialisations": 0})

    def test_scroll_direction_moves_the_visible_header_surface(self):
        """Scrolling must transform #headerInda, not its zero-height wrapper."""
        from scripts import inject_responsive_navigation as subject

        encoded_script = base64.b64encode(subject.JS.encode("utf-8")).decode("ascii")
        harness = f"""
const source = Buffer.from('{encoded_script}', 'base64').toString('utf8');
let scrollListener = null;
const classNames = new Set();
const classList = {{
  add(...names) {{ names.forEach(name => classNames.add(name)); }},
  remove(...names) {{ names.forEach(name => classNames.delete(name)); }},
  toggle(name, force) {{ if (force) classNames.add(name); else classNames.delete(name); }},
  contains(name) {{ return classNames.has(name); }}
}};
const headerStyle = {{
  values: {{}},
  setProperty(name, value) {{ this.values[name] = value; }}
}};
const headerHostStyle = {{
  values: {{}},
  setProperty(name, value) {{ this.values[name] = value; }}
}};
const headerHost = {{ style: headerHostStyle }};
const hamburgerLink = {{ setAttribute() {{}}, addEventListener() {{}} }};
const hamburger = {{
  parentElement: {{ insertBefore() {{}} }},
  querySelector() {{ return hamburgerLink; }}
}};
const header = {{
  offsetHeight: 80,
  style: headerStyle,
  querySelector(selector) {{
    if (selector === '.elementor-element-20668c0') return {{}};
    if (selector === '.elementor-element-8755157') return hamburger;
    if (selector === '.indafire-compact-client') return {{}};
    return null;
  }},
  querySelectorAll() {{ return [{{ textContent: 'Área do cliente', href: '/area-do-cliente/' }}]; }}
}};
global.window = {{
  scrollY: 0,
  matchMedia() {{ return {{ matches: true, addEventListener() {{}} }}; }},
  getComputedStyle() {{ return {{ display: 'none', visibility: 'hidden' }}; }},
  requestAnimationFrame(callback) {{ callback(); }},
  addEventListener(type, listener) {{ if (type === 'scroll') scrollListener = listener; }}
}};
global.document = {{
  readyState: 'complete',
  documentElement: {{ classList, style: {{ setProperty() {{}} }} }},
  body: {{ classList }},
  querySelector(selector) {{
    if (selector === '#headerInda') return header;
    if (selector === '.elementor-location-header') return headerHost;
    return null;
  }},
  addEventListener() {{}},
  createElement() {{ return {{ setAttribute() {{}} }}; }}
}};
global.MutationObserver = class {{ observe() {{}} }};
eval(source);
window.scrollY = 320;
if (scrollListener) scrollListener();
const afterDown = headerStyle.values.transform;
window.scrollY = 220;
if (scrollListener) scrollListener();
const afterUp = headerStyle.values.transform;
const hostTransform = headerHostStyle.values.transform;
const headerPosition = headerStyle.values.position;
console.log(JSON.stringify({{ afterDown, afterUp, hostTransform, headerPosition }}));
"""
        result = subprocess.run(
            ["node", "-e", harness],
            check=False,
            capture_output=True,
            text=True,
        )

        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(
            json.loads(result.stdout),
            {
                "afterDown": "translateY(calc(-100% - 12px))",
                "afterUp": "translateY(0)",
                "hostTransform": "none",
                "headerPosition": "fixed",
            },
        )

    def test_css_declares_fixed_header_and_drawer_email_nowrap(self):
        """Header must be fixed and mobile drawer email must not wrap."""
        from scripts import inject_responsive_navigation as subject

        self.assertIn("#headerInda {\n  position: fixed !important;", subject.CSS)
        self.assertIn("z-index: 10000 !important;", subject.CSS)
        self.assertIn(".elementor-2519 a[href*=\"mailto\"]", subject.CSS)
        self.assertIn("white-space: nowrap !important;", subject.CSS)
        self.assertIn("word-break: keep-all !important;", subject.CSS)

    def test_legacy_scroll_styles_are_stripped(self):
        """Older inline location-header scroll rules must be removed."""
        from scripts import inject_responsive_navigation as subject

        legacy_block = (
            "/* Reveal the full navigation whenever the user reverses scroll direction. */\n"
            "html.indafire-scroll-header-ready body {\n"
            "  padding-top: var(--indafire-header-height, 0px) !important;\n"
            "}\n"
            "html.indafire-scroll-header-ready .elementor-location-header {\n"
            "  position: fixed !important;\n"
            "  box-shadow: 0 4px 18px rgba(0, 0, 0, .12) !important;\n"
            "}\n"
        )
        source = f"<html><head><style>{legacy_block}</style></head><body></body></html>"
        rendered = subject.inject(source)
        self.assertNotIn(legacy_block, rendered)
        self.assertNotIn("html.indafire-scroll-header-ready .elementor-location-header", rendered)

    def test_legacy_scroll_controller_is_not_initialised(self):
        """Only the managed navigation layer may react to page scrolling."""
        from scripts import inject_responsive_navigation as subject

        source = (
            "<html><head></head><body>"
            "<script>globalThis.scrollInitialisations = 0;</script>"
            "<script>(function () { 'use strict';"
            "function initIndafireScrollHeader() { scrollInitialisations += 1; }"
            "initIndafireScrollHeader();"
            "})();</script>"
            "<script>console.log(JSON.stringify({scrollInitialisations}));</script>"
            "</body></html>"
        )
        rendered = subject.inject(source)
        scripts = [
            match.group(1)
            for match in re.finditer(r"<script(?: [^>]*)?>(.*?)</script>", rendered, re.DOTALL)
            if subject.SCRIPT_ID not in match.group(0)
        ]
        result = subprocess.run(
            ["node", "-e", "\n".join(scripts)],
            check=False,
            capture_output=True,
            text=True,
        )

        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(json.loads(result.stdout), {"scrollInitialisations": 0})


if __name__ == "__main__":
    unittest.main()
