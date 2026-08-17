const fs = require('fs');
const path = require('path');

function search(dir) {
  const list = fs.readdirSync(dir);
  for (const f of list) {
    const p = path.join(dir, f);
    if (f === 'node_modules' || f === '.git' || f === 'brain') continue;
    const stat = fs.statSync(p);
    if (stat.isDirectory()) search(p);
    else if (f.endsWith('.html') || f.endsWith('.js') || f.endsWith('.json') || f.endsWith('.md')) {
      const content = fs.readFileSync(p, 'utf8');
      const matches = content.match(/https?:\/\/[^\s"'<>]+/g);
      if (matches) {
        matches.filter(m => m.includes('indafire') || m.includes('fire')).forEach(m => console.log(p, '->', m));
      }
    }
  }
}
search('.');
