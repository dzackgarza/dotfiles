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
exports.TMP_DIR = exports.DEFAULT_TEMPLATE_PATH = exports.STRIP_MACROS_PATH = exports.CONFIG_PATH = void 0;
exports.loadPandocConfig = loadPandocConfig;
exports.fileToRawMarkdown = fileToRawMarkdown;
exports.fileToStrippedMarkdown = fileToStrippedMarkdown;
exports.rawMarkdownToFile = rawMarkdownToFile;
exports.strippedMarkdownToFile = strippedMarkdownToFile;
exports.macroStrip = macroStrip;
exports.runPandocOnStripped = runPandocOnStripped;
exports.rawMarkdownToStrippedMarkdownAndConvert = rawMarkdownToStrippedMarkdownAndConvert;
exports.injectMathJaxConfig = injectMathJaxConfig;
// @ts-ignore
/// <reference types="node" />
const child_process_1 = require("child_process");
const path = __importStar(require("path"));
const fs = __importStar(require("fs"));
const os = __importStar(require("os"));
const yaml = __importStar(require("js-yaml"));
console.error('LOADED pandocUtil.ts');
// ---- CONSTANTS ----
exports.CONFIG_PATH = path.resolve(__dirname, 'pandoc_global.yaml');
exports.STRIP_MACROS_PATH = '/home/dzack/.pandoc/bin/pandoc_stripmacros.sh';
exports.DEFAULT_TEMPLATE_PATH = path.resolve(__dirname, '../templates/pandoc_webview_template.html');
exports.TMP_DIR = os.tmpdir();
// Load config from YAML
function loadPandocConfig() {
    if (!fs.existsSync(exports.CONFIG_PATH))
        throw new Error('Config file not found: ' + exports.CONFIG_PATH);
    return yaml.load(fs.readFileSync(exports.CONFIG_PATH, 'utf8'));
}
// ---- FILE UTILITIES ----
/**
 * PURE
 * FILE -> RAW_MARKDOWN
 */
function fileToRawMarkdown(file) {
    if (!fs.existsSync(file))
        throw new Error('File not found: ' + file);
    return fs.readFileSync(file, 'utf8');
}
/**
 * PURE
 * FILE -> STRIPPED_MARKDOWN
 */
function fileToStrippedMarkdown(file) {
    if (!fs.existsSync(file))
        throw new Error('File not found: ' + file);
    return fs.readFileSync(file, 'utf8');
}
/**
 * SIDE-EFFECTING (writes to disk)
 * RAW_MARKDOWN -> FILE
 */
function rawMarkdownToFile(md, file) {
    if (typeof md !== 'string')
        throw new Error('Not a Raw_Markdown string');
    fs.writeFileSync(file, md, 'utf8');
}
/**
 * SIDE-EFFECTING (writes to disk)
 * STRIPPED_MARKDOWN -> FILE
 */
function strippedMarkdownToFile(md, file) {
    if (typeof md !== 'string')
        throw new Error('Not a Stripped_Markdown string');
    fs.writeFileSync(file, md, 'utf8');
}
// ---- MACRO STRIPPING ----
/**
 * SIDE-EFFECTING (spawns process)
 * RAW_MARKDOWN -> STRIPPED_MARKDOWN
 */
function macroStrip(md) {
    if (typeof md !== 'string')
        throw new Error('Input is not Raw_Markdown');
    return new Promise((resolve, reject) => {
        const proc = (0, child_process_1.spawn)(exports.STRIP_MACROS_PATH, [], { stdio: ['pipe', 'pipe', 'pipe'] });
        let out = '';
        let err = '';
        proc.stdout.on('data', (data) => { out += data.toString(); });
        proc.stderr.on('data', (data) => { err += data.toString(); });
        proc.on('close', (code) => {
            if (code === 0)
                resolve(out);
            else
                reject(new Error('macroStrip failed: ' + err));
        });
        proc.stdin.write(md);
        proc.stdin.end();
    });
}
// ---- PANDOC CONVERSION ----
/**
 * SIDE-EFFECTING (spawns process)
 * STRIPPED_MARKDOWN -> (PANDOC_HTML_OUTPUT | PANDOC_MARKDOWN_OUTPUT)
 */
function runPandocOnStripped(md, to, extraArgs = [], templatePath) {
    if (typeof md !== 'string')
        throw new Error('Input is not Stripped_Markdown');
    const config = loadPandocConfig();
    const pandocPath = config.pandoc.path;
    const from = config.pandoc.from;
    const args = [
        '--from=' + from,
        '--to=' + to,
        ...(templatePath ? ['--template=' + templatePath] : []),
        ...(config.pandoc.args || []),
        ...extraArgs
    ];
    return new Promise((resolve, reject) => {
        const proc = (0, child_process_1.spawn)(pandocPath, args, { stdio: ['pipe', 'pipe', 'pipe'] });
        let out = '';
        let err = '';
        proc.stdout.on('data', (data) => { out += data.toString(); });
        proc.stderr.on('data', (data) => { err += data.toString(); });
        proc.on('close', (code) => {
            if (code === 0) {
                if (to === 'html')
                    resolve(out);
                else
                    resolve(out);
            }
            else {
                reject(new Error('runPandocOnStripped failed: ' + err));
            }
        });
        proc.stdin.write(md);
        proc.stdin.end();
    });
}
// =============================
// PIPELINE / COMPOSED FUNCTIONS
// =============================
/**
 * SIDE-EFFECTING (spawns process)
 * RAW_MARKDOWN -> { output: PANDOC_HTML_OUTPUT | PANDOC_MARKDOWN_OUTPUT, stripped: STRIPPED_MARKDOWN }
 * Pipeline: macroStrip -> runPandocOnStripped
 */
async function rawMarkdownToStrippedMarkdownAndConvert(md, to, extraArgs = [], templatePath) {
    if (typeof md !== 'string')
        throw new Error('Input is not Raw_Markdown');
    const stripped = await macroStrip(md);
    const output = await runPandocOnStripped(stripped, to, extraArgs, templatePath);
    return { output, stripped };
}
// ---- TESTABLE PIECES ----
// Export all above for individual testing
// ---- INJECT MATHJAX ----
/**
 * PURE
 * PANDOC_HTML_OUTPUT -> PANDOC_HTML_OUTPUT
 */
function injectMathJaxConfig(html) {
    if (typeof html !== 'string')
        throw new Error('Input is not Pandoc_HTML_Output');
    const MATHJAX_V3_CONFIG = `<script>\nwindow.MathJax = {\n  tex: {\n    inlineMath: [['\\(','\\)']],\n    displayMath: [['\\[','\\]']],\n    tags: 'ams'\n  },\n  options: {\n    skipHtmlTags: ['script', 'noscript', 'style', 'textarea', 'pre', 'code']\n  }\n};\n</script>\n<script src=\"https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-mml-chtml.js\"></script>`;
    return html.replace(/<\/head>/i, `${MATHJAX_V3_CONFIG}\n</head>`);
}
