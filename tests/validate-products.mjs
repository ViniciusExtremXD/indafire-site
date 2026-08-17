import fs from 'fs';

let allValid = true;

// 1. Check js/products-data.js
const productsContent = fs.readFileSync('js/products-data.js', 'utf8');
const imgRegex1 = /image:\s*["']([^"']+)["']/g;
let match;
let count1 = 0;
const missing1 = [];

while ((match = imgRegex1.exec(productsContent)) !== null) {
  const imgPath = match[1];
  count1++;
  if (!fs.existsSync(imgPath)) {
    missing1.push(imgPath);
    allValid = false;
  }
}
console.log(`js/products-data.js images checked: ${count1} (Missing: ${missing1.length})`);

// 2. Check js/catalog-data.js
const catalogContent = fs.readFileSync('js/catalog-data.js', 'utf8');
const imgRegex2 = /image:\s*["']([^"']+)["']/g;
let count2 = 0;
const missing2 = [];

while ((match = imgRegex2.exec(catalogContent)) !== null) {
  const imgPath = match[1];
  count2++;
  if (!fs.existsSync(imgPath)) {
    missing2.push(imgPath);
    allValid = false;
  }
}
console.log(`js/catalog-data.js images checked: ${count2} (Missing: ${missing2.length})`);

if (!allValid) {
  console.error('MISSING IMAGES FOUND:', { missing1, missing2 });
  process.exit(1);
} else {
  console.log('ALL PRODUCT IMAGES FROM BOTH DATASETS EXIST 100% ON DISK!');
}
