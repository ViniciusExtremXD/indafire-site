import fs from 'fs';
import path from 'path';

const filesToTest = ['index.html', 'produtos.html', 'servicos.html'];
let totalFound = 0;
const missing = [];

for (const f of filesToTest) {
  const html = fs.readFileSync(f, 'utf8');
  const assetRegex = /(?:src|href)=["']([^"']+)["']/g;
  let match;

  while ((match = assetRegex.exec(html)) !== null) {
    const rawPath = match[1];
    if (rawPath.startsWith('#') || 
        rawPath.startsWith('http://') || 
        rawPath.startsWith('https://') || 
        rawPath.startsWith('tel:') || 
        rawPath.startsWith('mailto:') || 
        rawPath.startsWith('data:')) {
      continue;
    }
    
    const cleanPath = rawPath.split('?')[0].split('#')[0];
    if (!cleanPath) continue;

    if (!fs.existsSync(cleanPath)) {
      missing.push(`${f} -> ${rawPath} (${cleanPath})`);
    } else {
      totalFound++;
    }
  }
}

console.log('Total referenced local assets across all pages:', totalFound);
if (missing.length > 0) {
  console.error('MISSING ASSETS:', missing);
  process.exit(1);
} else {
  console.log('ALL REFERENCED ASSETS AND PAGES EXIST SUCCESSFULLY! 100% VALIDATED.');
}
