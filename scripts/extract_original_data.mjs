import https from 'https';
import fs from 'fs';

function fetchUrl(url) {
  return new Promise((resolve) => {
    https.get(url, (res) => {
      let data = '';
      res.on('data', chunk => data += chunk);
      res.on('end', () => resolve(data));
    }).on('error', err => {
      console.error('Fetch error:', err.message);
      resolve('');
    });
  });
}

async function scrape() {
  console.log('Fetching produtos...');
  const produtosHtml = await fetchUrl('https://indafire.com.br/produtos/');
  console.log('Produtos HTML length:', produtosHtml.length);
  fs.writeFileSync('scripts/produtos_raw.html', produtosHtml);

  console.log('Fetching servicos...');
  const servicosHtml = await fetchUrl('https://indafire.com.br/servicos/');
  console.log('Servicos HTML length:', servicosHtml.length);
  fs.writeFileSync('scripts/servicos_raw.html', servicosHtml);

  console.log('Saved raw files for parsing.');
}

scrape();
