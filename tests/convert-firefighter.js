const sharp = require('sharp');
const fs = require('fs');

async function processCutout() {
  const input = 'media/original/2021/10/shutterstock_668147359.png';
  if (fs.existsSync(input)) {
    await sharp(input)
      .resize({ width: 900 })
      .webp({ quality: 88 })
      .toFile('images/firefighter-cutout.webp');
    console.log('Saved images/firefighter-cutout.webp successfully!');
  }
}

processCutout().catch(console.error);
