const https = require('https');
const fs = require('fs');

https.get('https://indafire.com.br/', (res) => {
  let data = '';
  res.on('data', chunk => data += chunk);
  res.on('end', () => {
    const iconMatch = data.match(/<link[^>]*rel=["'](?:shortcut )?icon["'][^>]*href=["']([^"']+)["']/i);
    console.log('Original favicon link:', iconMatch ? iconMatch[1] : 'Not found');
    if (iconMatch) {
      const url = iconMatch[1];
      const fileStream = fs.createWriteStream('favicon.ico');
      https.get(url, (iconRes) => {
        iconRes.pipe(fileStream);
        fileStream.on('finish', () => {
          fileStream.close();
          console.log('Saved favicon.ico successfully!');
        });
      });
    }
  });
}).on('error', (err) => console.log('Fetch error:', err.message));
