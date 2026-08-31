const assert = require('node:assert/strict');
const fs = require('node:fs');

const homePage = fs.readFileSync('index.html', 'utf8');

assert.match(
  homePage,
  /elementor-element-989c3cc[^>]*elementor-aspect-ratio-169[^>]*data-settings="[^"]*&quot;aspect_ratio&quot;:&quot;169&quot;[^"]*"[\s\S]*?<video[^>]*data-src="\.\/wp-content\/uploads\/2021\/10\/Video-10-1\.mp4"[^>]*playsinline/,
  'the Brigada block must keep the original hosted video in its native 16:9 Elementor frame'
);

console.log('Brigada video frame regression test passed.');
