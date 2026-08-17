import fs from 'fs';

const prodHtml = fs.readFileSync('scripts/produtos_raw.html', 'utf8');
const servHtml = fs.readFileSync('scripts/servicos_raw.html', 'utf8');

// 1. Parse Products Categories from sidebar or menu
const catRegex = /<li[^>]*class="[^"]*cat-item[^"]*"[^>]*><a[^>]*href="([^"]*)"[^>]*>([^<]+)<\/a>(?:\s*<span[^>]*class="count"[^>]*>\(([0-9]+)\)<\/span>)?/gi;
let catMatch;
const categories = [];
while ((catMatch = catRegex.exec(prodHtml)) !== null) {
  categories.push({
    url: catMatch[1],
    slug: catMatch[1].replace(/.*\/categoria-produto\/([^\/]+)\/?/, '$1'),
    name: catMatch[2].trim(),
    count: parseInt(catMatch[3] || '0', 10)
  });
}

// Extract products from the grid
// WooCommerce product list regex
const prodRegex = /<li[^>]*class="[^"]*product[^"]*"[^>]*>([\s\S]*?)<\/li>/gi;
let pMatch;
const products = [];

while ((pMatch = prodRegex.exec(prodHtml)) !== null) {
  const block = pMatch[1];
  
  // Title
  const titleMatch = block.match(/<h2[^>]*class="[^"]*woocommerce-loop-product__title[^"]*"[^>]*>([^<]+)<\/h2>/i)
    || block.match(/<h3[^>]*class="[^"]*product[^"]*title[^"]*"[^>]*>([^<]+)<\/h3>/i)
    || block.match(/<h2[^>]*>([^<]+)<\/h2>/i);
  const name = titleMatch ? titleMatch[1].trim() : '';

  // Link
  const linkMatch = block.match(/href="([^"]*\/produto\/[^"]*)"/i);
  const link = linkMatch ? linkMatch[1] : '';

  // Image
  const imgMatch = block.match(/data-lazy-src="([^"]+)"/i) 
    || block.match(/data-src="([^"]+)"/i)
    || block.match(/src="([^"]+\.(?:jpg|png|jpeg|webp))"/i);
  const img = imgMatch ? imgMatch[1] : '';

  // Classes / Categories
  const catClasses = (block.match(/product_cat-([a-zA-Z0-9_-]+)/g) || []).map(c => c.replace('product_cat-', ''));

  if (name && link) {
    products.push({
      id: link.replace(/.*\/produto\/([^\/]+)\/?/, '$1'),
      name,
      link,
      image: img,
      categories: catClasses
    });
  }
}

// 2. Parse Services from Servicos HTML
const servPostRegex = /<article[^>]*class="[^"]*servicos_inda_fire[^"]*"[^>]*>([\s\S]*?)<\/article>/gi;
let sMatch;
const services = [];

while ((sMatch = servPostRegex.exec(servHtml)) !== null) {
  const block = sMatch[1];
  
  const titleMatch = block.match(/<h2[^>]*class="[^"]*elementor-heading-title[^"]*"[^>]*>([^<]+)<\/h2>/i)
    || block.match(/<h3[^>]*>([^<]+)<\/h3>/i);
  const name = titleMatch ? titleMatch[1].trim() : '';

  const linkMatch = block.match(/href="([^"]*\/servicos_inda_fire\/[^"]*)"/i)
    || block.match(/data-ha-element-link="\{&quot;url&quot;:&quot;([^&]+)&quot;/i);
  let link = linkMatch ? linkMatch[1].replace(/\\\//g, '/') : '';

  const imgMatch = block.match(/data-lazy-src="([^"]+)"/i)
    || block.match(/src="([^"]+\.(?:jpg|png|jpeg|webp))"/i);
  const img = imgMatch ? imgMatch[1] : '';

  const catMatch = block.match(/tipos-[a-zA-Z0-9_-]+/g) || [];

  if (name) {
    services.push({
      id: link ? link.replace(/.*\/servicos_inda_fire\/([^\/]+)\/?/, '$1') : name.toLowerCase().replace(/\s+/g, '-'),
      name,
      link,
      image: img,
      categories: catMatch
    });
  }
}

console.log('Categories found:', categories.length, categories);
console.log('Products found on page:', products.length);
console.log('Services found on page:', services.length, services.map(s => s.name));

fs.writeFileSync('scripts/parsed_data.json', JSON.stringify({ categories, products, services }, null, 2));
