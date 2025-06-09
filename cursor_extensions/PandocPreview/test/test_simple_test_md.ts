import { macroStrip, runPandocOnStripped, fileToRawMarkdown, Raw_Markdown } from '../src/pandocUtil';
import * as fs from 'fs';
import * as path from 'path';
import { execSync } from 'child_process';

const inputPath = path.resolve(__dirname, 'inputs/simple_test.md');
const outputHtmlPath = path.resolve(__dirname, 'outputs/simple_test_webview.html');

describe('simple_test.md integration', () => {
  let rawMd: Raw_Markdown;
  beforeAll(() => {
    rawMd = fileToRawMarkdown(inputPath);
  });

  it('strips all macros except default MathJax', async () => {
    const stripped = await macroStrip(rawMd);
    // Check for forbidden macros (e.g., \\ZZ, \\QQ, custom macros)
    expect(stripped).not.toMatch(/\\ZZ|\\QQ|\\tensor|\\Quad|\\Sym|\\dual/);
    // Should still contain standard math
    expect(stripped).toMatch(/\\mathbf\{Q\}/);
  });

  it('renders HTML with correct prooenv lemma div and title', async () => {
    const stripped = await macroStrip(rawMd);
    const html = await runPandocOnStripped(stripped, 'html');
    // Check for lemma div and title
    expect(html).toMatch(/<div[^>]*class="lemma"[^>]*>/);
    expect(html).toMatch(/Correspondence between bilinear and quadratic forms/);
    // Save for webview test
    fs.writeFileSync(outputHtmlPath, html, 'utf8');
  });

  it('renders (not necessarily symmetric) as text, not math', async () => {
    const stripped = await macroStrip(rawMd);
    // Should not wrap (not necessarily symmetric) in math delimiters
    expect(stripped).toContain('(not necessarily symmetric)');
    // Should not be inside $...$ or \(...\)
    expect(stripped).not.toMatch(/\$\(not necessarily symmetric\)\$/);
    expect(stripped).not.toMatch(/\\\(not necessarily symmetric\\\)/);
    const html = await runPandocOnStripped(stripped, 'html');
    // Should appear as plain text in HTML
    expect(html).toContain('not necessarily symmetric');
  });

  it('produces a webview-compatible HTML file and opens it in the browser', async () => {
    // Use the HTML file saved above
    expect(fs.existsSync(outputHtmlPath)).toBe(true);
    // Open in browser (xdg-open)
    execSync(`xdg-open ${outputHtmlPath}`);
  });
}); 