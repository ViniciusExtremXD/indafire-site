import https from 'https';
import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);
const imgDir = path.resolve(__dirname, '../assets/img');

if (!fs.existsSync(imgDir)) {
  fs.mkdirSync(imgDir, { recursive: true });
}

const assets = [
  { name: 'bombeiro_mangueira_original.png', url: 'https://indafire.com.br/site/wp-content/uploads/2021/11/cara.png' },
  { name: 'treinamento_fogo_real.jpg', url: 'https://indafire.com.br/site/wp-content/uploads/2021/11/treinamentos_bombeiros.jpg' },
  { name: 'sede_empresa_banner.png', url: 'https://indafire.com.br/site/wp-content/uploads/2021/11/CONTRA-CAPA-03-2.png' },
  { name: 'timeline_1996.png', url: 'https://indafire.com.br/site/wp-content/uploads/2021/11/1996_Fundacao-1.png' },
  { name: 'timeline_1997_2007.png', url: 'https://indafire.com.br/site/wp-content/uploads/2021/11/1997_2007-1.png' },
  { name: 'timeline_2008_inmetro.png', url: 'https://indafire.com.br/site/wp-content/uploads/2021/11/2018.png' },
  { name: 'timeline_2008_2018.png', url: 'https://indafire.com.br/site/wp-content/uploads/2021/11/2008_2018.png' },
  { name: 'timeline_2018_sede_propria.png', url: 'https://indafire.com.br/site/wp-content/uploads/2021/11/2018-1.png' },
  { name: 'inmetro_cert.svg', url: 'https://indafire.com.br/site/wp-content/uploads/2021/11/inmetro-logo_branco.svg' }
];

async function download(item) {
  const dest = path.join(imgDir, item.name);
  return new Promise((resolve) => {
    https.get(item.url, (res) => {
      if (res.statusCode === 200) {
        const file = fs.createWriteStream(dest);
        res.pipe(file);
        file.on('finish', () => {
          file.close();
          const stats = fs.statSync(dest);
          console.log(`[OK] ${item.name} (${stats.size} bytes)`);
          resolve(true);
        });
      } else {
        console.error(`[FAIL] ${item.name} - Status ${res.statusCode}`);
        resolve(false);
      }
    }).on('error', (err) => {
      console.error(`[ERR] ${item.name}: ${err.message}`);
      resolve(false);
    });
  });
}

async function run() {
  for (const item of assets) {
    await download(item);
  }
  console.log('Done downloading assets!');
}

run();
