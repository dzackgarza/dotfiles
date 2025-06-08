const fs = require('fs');
const path = require('path');
const assert = require('assert');
const { runPandoc } = require('./out/pandocUtil.js');

function normalizeHtml(html) {
  return html.replace(/\s+/g, ' ').trim();
}

function testCheckboxes(done) {
  const mdPath = path.resolve(__dirname, '../test_checkboxes.md');
  const md = fs.readFileSync(mdPath, 'utf8');
  runPandoc(md, (code, html, err) => {
    try {
      assert.strictEqual(code, 0, 'Pandoc should exit with code 0');
      const norm = normalizeHtml(html);
      assert(norm.includes('<input type="checkbox" />'), 'Should contain unchecked checkbox');
      assert(norm.includes('<input type="checkbox" checked="" />'), 'Should contain checked checkbox');
      assert(norm.includes('Regular item'), 'Should contain regular item');
      done();
    } catch (e) {
      console.error('testCheckboxes failed:', e);
      process.exit(1);
    }
  });
}

testCheckboxes(() => {
  console.log('All tests passed.');
}); 