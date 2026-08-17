const https = require('https');
const fs = require('fs');

const fullUrl = 'https://indafire.com.br/site/wp-content/uploads/2021/10/cropped-inda-512-192x192.png';
const fileStream = fs.createWriteStream('favicon.png');
https.get(fullUrl, (res) => {
  res.pipe(fileStream);
  fileStream.on('finish', () => {
    fileStream.close();
    fs.copyFileSync('favicon.png', 'brand/favicon.png');
    console.log('Saved high-res original favicon.png!');
  });
});
