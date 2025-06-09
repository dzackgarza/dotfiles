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
const pandocUtil_1 = require("../src/pandocUtil");
const fs = __importStar(require("fs"));
const path = __importStar(require("path"));
const child_process_1 = require("child_process");
const inputPath = path.resolve(__dirname, 'inputs/simple_test.md');
const outputHtmlPath = path.resolve(__dirname, 'outputs/simple_test_webview.html');
describe('simple_test.md integration', () => {
    let rawMd;
    beforeAll(() => {
        rawMd = (0, pandocUtil_1.fileToRawMarkdown)(inputPath);
    });
    it('strips all macros except default MathJax', async () => {
        const stripped = await (0, pandocUtil_1.macroStrip)(rawMd);
        // Check for forbidden macros (e.g., \\ZZ, \\QQ, custom macros)
        expect(stripped).not.toMatch(/\\ZZ|\\QQ|\\tensor|\\Quad|\\Sym|\\dual/);
        // Should still contain standard math
        expect(stripped).toMatch(/\\mathbf\{Q\}/);
    });
    it('renders HTML with correct prooenv lemma div and title', async () => {
        const stripped = await (0, pandocUtil_1.macroStrip)(rawMd);
        const html = await (0, pandocUtil_1.runPandocOnStripped)(stripped, 'html');
        // Check for lemma div and title
        expect(html).toMatch(/<div[^>]*class="lemma"[^>]*>/);
        expect(html).toMatch(/Correspondence between bilinear and quadratic forms/);
        // Save for webview test
        fs.writeFileSync(outputHtmlPath, html, 'utf8');
    });
    it('renders (not necessarily symmetric) as text, not math', async () => {
        const stripped = await (0, pandocUtil_1.macroStrip)(rawMd);
        // Should not wrap (not necessarily symmetric) in math delimiters
        expect(stripped).toContain('(not necessarily symmetric)');
        // Should not be inside $...$ or \(...\)
        expect(stripped).not.toMatch(/\$\(not necessarily symmetric\)\$/);
        expect(stripped).not.toMatch(/\\\(not necessarily symmetric\\\)/);
        const html = await (0, pandocUtil_1.runPandocOnStripped)(stripped, 'html');
        // Should appear as plain text in HTML
        expect(html).toContain('not necessarily symmetric');
    });
    it('produces a webview-compatible HTML file and opens it in the browser', async () => {
        // Use the HTML file saved above
        expect(fs.existsSync(outputHtmlPath)).toBe(true);
        // Open in browser (xdg-open)
        (0, child_process_1.execSync)(`xdg-open ${outputHtmlPath}`);
    });
});
