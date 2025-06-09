import { macroStrip, runPandocOnStripped, Raw_Markdown } from '../src/pandocUtil';

console.error('[DEBUG] START minimal_pandoc_test');

const md = '# Hello World\n\nThis is a test.' as Raw_Markdown;

console.error('[DEBUG] About to call macroStrip and runPandocOnStripped');
(async () => {
  const stripped = await macroStrip(md);
  const html = await runPandocOnStripped(stripped, 'html');
  if (!html || (html as string).trim().length === 0) {
    console.error('TEST FAILED: Output HTML is missing or empty!');
    process.exit(1);
  }
  console.log('HTML output:', (html as string).slice(0, 200));
  // Test: fail if 'ZZ' or 'QQ' is found in the output HTML
  if ((html as string).includes('ZZ') || (html as string).includes('QQ')) {
    console.error('TEST FAILED: Output HTML contains forbidden string ZZ or QQ');
    process.exit(1);
  } else {
    console.log('TEST PASSED: Output HTML is valid.');
  }
})();
console.error('[DEBUG] After runPandoc call'); 