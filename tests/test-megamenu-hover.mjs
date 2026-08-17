import puppeteer from 'puppeteer';

async function testMegaMenu() {
  const browser = await puppeteer.launch({ headless: 'new', args: ['--no-sandbox'] });
  const page = await browser.newPage();
  await page.setViewport({ width: 1440, height: 900 });

  await page.goto('http://localhost:3000', { waitUntil: 'networkidle0' });

  console.log('1. Hovering over #nav-produtos-btn...');
  await page.hover('#nav-produtos-btn');
  await new Promise(r => setTimeout(r, 200));

  const isMenuVisible = await page.$eval('#mega-menu-produtos', el => {
    const style = window.getComputedStyle(el);
    return style.opacity === '1' && style.visibility === 'visible';
  });
  console.log('Mega menu visible on hover:', isMenuVisible);

  console.log('2. Moving mouse slowly inside mega menu to category link...');
  await page.mouse.move(300, 150);
  await new Promise(r => setTimeout(r, 100));
  await page.mouse.move(300, 220);
  await new Promise(r => setTimeout(r, 100));

  const isStillVisible = await page.$eval('#mega-menu-produtos', el => {
    const style = window.getComputedStyle(el);
    return style.opacity === '1' && style.visibility === 'visible';
  });
  console.log('Mega menu still visible inside content:', isStillVisible);

  await page.screenshot({ path: 'screenshots/megamenu-hover-test.png' });
  console.log('Saved screenshot to screenshots/megamenu-hover-test.png');

  await browser.close();
}

testMegaMenu().catch(err => {
  console.error('Test error:', err);
  process.exit(1);
});
