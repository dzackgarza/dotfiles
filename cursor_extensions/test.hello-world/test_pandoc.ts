import * as fs from 'fs';
import * as path from 'path';
import { runPandoc } from './pandocUtil';

const mdPath = path.resolve(__dirname, '../../test_custom_pandoc.md');
const md = fs.readFileSync(mdPath, 'utf8');

runPandoc(
  md,
  (code: number, html: string, err: string) => {
    if (code === 0) {
      console.log('Pandoc HTML output:');
      console.log(html);
      // Test: Check that ':::{.remark}' is parsed to a div with class "remark"
      const hasRemarkDiv = /<div\s+class=["']remark["']/.test(html);
      if (hasRemarkDiv) {
        console.log('PASS: .remark block parsed to <div class="remark">');
      } else {
        console.error('FAIL: .remark block NOT parsed to <div class="remark">');
        process.exit(1);
      }
    } else {
      console.error(`Pandoc failed with code ${code}`);
      if (err) console.error(err);
      process.exit(1);
    }
  }
); 