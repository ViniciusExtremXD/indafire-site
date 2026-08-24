const assert = require('node:assert/strict');
const fs = require('node:fs');

const homePage = fs.readFileSync('index.html', 'utf8');

assert.match(
  homePage,
  /Brigada video: preserve the complete 16:9 frame on every viewport\.[\s\S]*?\.elementor-widget-container\s*\{[\s\S]*?margin-bottom:\s*0\s*!important/,
  'the Brigada video container must override Elementor’s negative bottom margin so overflow cannot crop the frame'
);

console.log('Brigada video frame regression test passed.');
