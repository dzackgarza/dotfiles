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
const conversionPipeline_1 = require("../src/conversionPipeline");
const os = __importStar(require("os"));
const yaml = __importStar(require("js-yaml"));
const pandocUtil_1 = require("../src/pandocUtil");
const configPath = path.resolve(__dirname, '../pandoc_global.yaml');
const config = yaml.load(fs.readFileSync(configPath, 'utf8'));
const mdPath = config.pandoc.test_inputs.test_custom_pandoc;
const strippedPath = config.pandoc.test_inputs.test_custom_pandoc_stripped;
const outputHtmlPath = config.pandoc.test_outputs.test_custom_pandoc_html;
const outputMdPath = config.pandoc.test_outputs.stripmacros_test_output;
const debugBasePath = path.resolve(__dirname, '../webview_test_output');
const templatePath = config.pandoc.template;
const tmpDir = os.tmpdir();
const inputPath = path.join(tmpDir, 'pandoc_input_debug.md');
const strippedTmpPath = path.join(tmpDir, 'pandoc_stripped_debug.md');
const md = fs.readFileSync(mdPath, 'utf8');
const pandocArgs = [
    ...(config.pandoc.args || [])
];
console.error('[DEBUG] Template path:', templatePath);
console.error('[DEBUG] Markdown input path:', mdPath);
console.error('[DEBUG] Markdown input (first 500 chars):', md.slice(0, 500));
(async () => {
    // Use canonical conversion pipeline
    let finalHtml;
    try {
        console.error('[DEBUG] Calling convertMarkdownToFinalHtml...');
        finalHtml = await (0, conversionPipeline_1.convertMarkdownToFinalHtml)(md, debugBasePath, [], undefined, undefined, console.error);
        console.error('[DEBUG] Final HTML for Cursor webview (first 500 chars):', finalHtml.slice(0, 500));
    }
    catch (e) {
        console.error('[DEBUG] Error during convertMarkdownToFinalHtml:', e);
        throw e;
    }
    // Show the text after pandoc_stripmacros
    try {
        const stripped = fs.readFileSync(strippedPath, 'utf8');
        console.error('[DEBUG] Text after pandoc_stripmacros (first 500 chars):', stripped.slice(0, 500));
    }
    catch (e) {
        console.error('[DEBUG] Could not read stripped markdown:', e);
    }
    // Show the text after the pandoc command (markdown)
    try {
        const outMd = fs.readFileSync(outputMdPath, 'utf8');
        console.error('[DEBUG] Text after pandoc command (markdown, first 500 chars):', outMd.slice(0, 500));
    }
    catch (e) {
        console.error('[DEBUG] Could not read output markdown:', e);
    }
    // Show the text after the pandoc command (HTML, if available)
    try {
        const outHtml = fs.readFileSync(outputHtmlPath, 'utf8');
        console.error('[DEBUG] Text after pandoc command (HTML, first 500 chars):', outHtml.slice(0, 500));
    }
    catch (e) {
        console.error('[DEBUG] Could not read output HTML:', e);
    }
    // Simple check: does the output look like a full HTML document?
    if (!finalHtml.trim().startsWith('<!DOCTYPE html>')) {
        console.error('FAIL: Output is not a full HTML document');
        process.exit(1);
    }
    else {
        console.error('PASS: Output is a full HTML document');
    }
    // Additional test: simulate missing template file
    const missingTemplatePath = '/tmp/this_template_does_not_exist.html';
    try {
        await (0, conversionPipeline_1.convertMarkdownToFinalHtml)(md, debugBasePath, [], missingTemplatePath, undefined, console.error);
        console.error('WARN: No error was thrown for missing template. This may be expected if Pandoc does not error on missing template.');
    }
    catch (e) {
        if (e.message && e.message.includes('Could not find data file')) {
            console.error('PASS: Detected missing template error from Pandoc');
        }
        else {
            console.error('WARN: Unexpected error for missing template:', e);
        }
    }
    fs.writeFileSync(outputHtmlPath, finalHtml, 'utf8');
    // Test 1: macroStrip
    console.error('--- TEST 1: macroStrip ---');
    const rawMd = (0, pandocUtil_1.fileToRawMarkdown)(mdPath);
    try {
        const stripped = await (0, pandocUtil_1.macroStrip)(rawMd);
        console.error('[TEST 1] Stripped markdown (first 500 chars):', stripped.slice(0, 500));
    }
    catch (e) {
        console.error('[TEST 1] Error:', e);
    }
    // Test 2: runPandocOnStripped
    console.error('--- TEST 2: runPandocOnStripped ---');
    const strippedMd = (0, pandocUtil_1.fileToStrippedMarkdown)(strippedPath);
    try {
        const html = await (0, pandocUtil_1.runPandocOnStripped)(strippedMd, 'html');
        console.error('[TEST 2] HTML output (first 500 chars):', html.slice(0, 500));
    }
    catch (e) {
        console.error('[TEST 2] Error:', e);
    }
})();
