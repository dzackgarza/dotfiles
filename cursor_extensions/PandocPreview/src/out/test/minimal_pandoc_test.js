"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
const pandocUtil_1 = require("../src/pandocUtil");
console.error('[DEBUG] START minimal_pandoc_test');
const md = '# Hello World\n\nThis is a test.';
console.error('[DEBUG] About to call macroStrip and runPandocOnStripped');
(async () => {
    const stripped = await (0, pandocUtil_1.macroStrip)(md);
    const html = await (0, pandocUtil_1.runPandocOnStripped)(stripped, 'html');
    if (!html || html.trim().length === 0) {
        console.error('TEST FAILED: Output HTML is missing or empty!');
        process.exit(1);
    }
    console.log('HTML output:', html.slice(0, 200));
    // Test: fail if 'ZZ' or 'QQ' is found in the output HTML
    if (html.includes('ZZ') || html.includes('QQ')) {
        console.error('TEST FAILED: Output HTML contains forbidden string ZZ or QQ');
        process.exit(1);
    }
    else {
        console.log('TEST PASSED: Output HTML is valid.');
    }
})();
console.error('[DEBUG] After runPandoc call');
