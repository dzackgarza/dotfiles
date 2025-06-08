"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
var pandocUtil_1 = require("./pandocUtil");
var md = '# Hello World\n\nThis is a test.';
(0, pandocUtil_1.runPandoc)(md, function (code, html, err) {
    console.log('Pandoc exit code:', code);
    console.log('HTML output:', html.slice(0, 200));
    if (err)
        console.error('Pandoc stderr:', err);
    // Test: fail if 'ZZ' or 'QQ' is found in the output HTML
    if (html.includes('ZZ') || html.includes('QQ')) {
        console.error('TEST FAILED: Output HTML contains forbidden string ZZ or QQ');
        process.exit(1);
    }
    else {
        console.log('TEST PASSED: Output HTML does not contain ZZ or QQ');
    }
}, undefined, []);
