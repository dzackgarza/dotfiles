const fs = require('fs');
const path = require('path');
const { runPandoc } = require('./pandocUtil.js');
const mdPath = path.resolve(__dirname, '../../test_checkboxes.md');
const md = fs.readFileSync(mdPath, 'utf8');
const { spawn } = require('child_process');
const pandoc = spawn('pandoc', ['-f', 'markdown', '-t', 'html']);
let html = '';
pandoc.stdout.on('data', (data) => { html += data.toString(); });
pandoc.on('close', (code) => {
  if (code === 0) {
    console.log(html);
  } else {
    console.error(`Pandoc failed with code ${code}`);
  }
});
pandoc.stdin.write(md);
pandoc.stdin.end();

runPandoc(md, (code, html, err) => {
  if (code === 0) {
    console.log(html);
  } else {
    console.error(`Pandoc failed with code ${code}`);
    if (err) console.error(err);
  }
}); 