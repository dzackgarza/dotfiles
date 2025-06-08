import * as fs from 'fs';
import * as path from 'path';
import { runPandoc } from './pandocUtil';

const mdPath = path.resolve(__dirname, '../test_custom_pandoc.md');
const md = fs.readFileSync(mdPath, 'utf8');

runPandoc(
  md,
  (code: number, html: string, err: string) => {
    // Inject custom CSS for theorem environments
    const theoremCSS = `
      <style>
      div.proofenv.theorem,
      div.proofenv.lemma,
      div.proofenv.proposition,
      div.proofenv.remark,
      div.proofenv.corollary {
        border-left: 4px solid #0074d9;
        background: #f8f8ff;
        margin: 1em 0;
        padding: 0.5em 1em;
        position: relative;
      }
      div.proofenv[title]::before {
        content: "(" attr(class) " " attr(title) "): ";
        font-weight: bold;
        display: block;
        margin-bottom: 0.5em;
        color: #222;
        text-transform: capitalize;
      }
      </style>
    `;
    html = theoremCSS + html;
    let testResults: string[] = [];
    if (code === 0) {
      console.log('Pandoc HTML output:');
      console.log(html);
      // Test: Check that each expected block is parsed to a div with the correct class
      const expectedClasses = [
        'remark',
        'definition',
        'lemma',
        'theorem',
        'proof',
        'proposition',
        'corollary',
      ];
      let allPassed = true;
      for (const cls of expectedClasses) {
        const regex = new RegExp(`<div\\s+class=["']${cls}["']`);
        if (regex.test(html)) {
          testResults.push(`PASS: .${cls} block parsed to <div class=\"${cls}\">`);
        } else {
          testResults.push(`FAIL: .${cls} block NOT parsed to <div class=\"${cls}\">`);
          allPassed = false;
        }
      }
      testResults.forEach(r => {
        if (r.startsWith('PASS')) {
          console.log(r);
        } else {
          console.error(r);
        }
      });
      fs.writeFileSync('pandoc_css_test.testoutput', testResults.join('\n') + '\n');
      if (!allPassed) process.exit(1);
    } else {
      const failMsg = `FAIL: Pandoc failed with code ${code}`;
      testResults.push(failMsg);
      console.error(failMsg);
      if (err) console.error(err);
      fs.writeFileSync('pandoc_css_test.testoutput', testResults.join('\n') + '\n');
      process.exit(1);
    }
  }
); 