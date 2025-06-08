"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
const pandocUtil_1 = require("./pandocUtil");
const md = '# Hello World\n\nThis is a test.';
(0, pandocUtil_1.runPandoc)(md, (code, html, err) => {
    console.log('Pandoc exit code:', code);
    console.log('HTML output:', html.slice(0, 200));
    if (err)
        console.error('Pandoc stderr:', err);
}, undefined, []);
