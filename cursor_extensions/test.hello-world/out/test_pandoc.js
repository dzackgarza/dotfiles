"use strict";
var __createBinding = (this && this.__createBinding) || (Object.create ? (function(o, m, k, k2) {
    if (k2 === undefined) k2 = k;
    var desc = Object.getOwnPropertyDescriptor(m, k);
    if (!desc || ("get" in desc ? !m.__esModule : desc.writable || desc.configurable)) {
      desc = { enumerable: true, get: function() { return m[k]; } };
    }
    Object.defineProperty(o, k2, desc);
}) : (function(o, m, k, k2) {
    if (k2 === undefined) k2 = k;
    o[k2] = m[k];
}));
var __setModuleDefault = (this && this.__setModuleDefault) || (Object.create ? (function(o, v) {
    Object.defineProperty(o, "default", { enumerable: true, value: v });
}) : function(o, v) {
    o["default"] = v;
});
var __importStar = (this && this.__importStar) || (function () {
    var ownKeys = function(o) {
        ownKeys = Object.getOwnPropertyNames || function (o) {
            var ar = [];
            for (var k in o) if (Object.prototype.hasOwnProperty.call(o, k)) ar[ar.length] = k;
            return ar;
        };
        return ownKeys(o);
    };
    return function (mod) {
        if (mod && mod.__esModule) return mod;
        var result = {};
        if (mod != null) for (var k = ownKeys(mod), i = 0; i < k.length; i++) if (k[i] !== "default") __createBinding(result, mod, k[i]);
        __setModuleDefault(result, mod);
        return result;
    };
})();
Object.defineProperty(exports, "__esModule", { value: true });
const fs = __importStar(require("fs"));
const path = __importStar(require("path"));
const pandocUtil_1 = require("./pandocUtil");
const mdPath = path.resolve(__dirname, '../test_custom_pandoc.md');
const md = fs.readFileSync(mdPath, 'utf8');
(0, pandocUtil_1.runPandoc)(md, (code, html, err) => {
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
    let testResults = [];
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
            }
            else {
                testResults.push(`FAIL: .${cls} block NOT parsed to <div class=\"${cls}\">`);
                allPassed = false;
            }
        }
        testResults.forEach(r => {
            if (r.startsWith('PASS')) {
                console.log(r);
            }
            else {
                console.error(r);
            }
        });
        fs.writeFileSync('pandoc_css_test.testoutput', testResults.join('\n') + '\n');
        if (!allPassed)
            process.exit(1);
    }
    else {
        const failMsg = `FAIL: Pandoc failed with code ${code}`;
        testResults.push(failMsg);
        console.error(failMsg);
        if (err)
            console.error(err);
        fs.writeFileSync('pandoc_css_test.testoutput', testResults.join('\n') + '\n');
        process.exit(1);
    }
});
