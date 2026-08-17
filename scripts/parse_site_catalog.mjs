import fs from 'fs';

const html = fs.readFileSync('scripts/produtos_raw.html', 'utf8');

// 1. All Category Links
const catRegex = /href="https:\/\/indafire\.com\.br\/categoria-produto\/([^\/"]+)\/?"[^>]*>([^<]+)<\/a>/gi;
let m;
const catMap = new Map();
while ((m = catRegex.exec(html)) !== null) {
  const slug = m[1].toLowerCase().trim();
  const name = m[2].trim();
  if (name && !catMap.has(slug)) {
    catMap.set(slug, name);
  }
}
console.log('Categories from links:', Object.fromEntries(catMap));

// 2. All Product Links & Names
const prodRegex = /href="(https:\/\/indafire\.com\.br\/produto\/([^\/"]+)\/?)"[^>]*>([\s\S]*?)<\/a>/gi;
const prodMap = new Map();
while ((m = prodRegex.exec(html)) !== null) {
  const url = m[1];
  const slug = m[2];
  const inner = m[3];
  
  // Try to find image
  const imgMatch = inner.match(/src="([^"]+\.(?:png|jpg|jpeg|webp))"/i) || inner.match(/data-lazy-src="([^"]+)"/i);
  const img = imgMatch ? imgMatch[1] : '';

  // Try to find title
  const titleMatch = inner.match(/<h2[^>]*>([^<]+)<\/h2>/i) || inner.match(/<h3[^>]*>([^<]+)<\/h3>/i) || inner.match(/class="[^"]*title[^"]*"[^>]*>([^<]+)</i);
  const title = titleMatch ? titleMatch[1].trim() : slug.replace(/-/g, ' ').toUpperCase();

  if (!prodMap.has(slug)) {
    prodMap.set(slug, {
      slug,
      url,
      title,
      image: img
    });
  }
}

console.log('Total products found:', prodMap.size);
console.log('Products:', Array.from(prodMap.values()).slice(0, 15));
