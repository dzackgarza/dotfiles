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
exports.convertMarkdownToFinalHtml = convertMarkdownToFinalHtml;
const pandocUtil_1 = require("./pandocUtil");
const fs = __importStar(require("fs"));
const MATHJAX_V3_CONFIG = `<script>
window.MathJax = {
  tex: {
    inlineMath: [['\\(','\\)']],
    displayMath: [['\\[','\\]']],
    tags: 'ams'
  },
  options: {
    skipHtmlTags: ['script', 'noscript', 'style', 'textarea', 'pre', 'code']
  }
};
</script>\n<script src="https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-mml-chtml.js"></script>`;
async function convertMarkdownToFinalHtml(md, debugBasePath, pandocArgs = [], logDir, timestamp, log) {
    if (log)
        log('convertMarkdownToFinalHtml: called (NOT STALE)');
    // Save stripped markdown after macro stripping
    let strippedMd = undefined;
    if (log)
        log('convertMarkdownToFinalHtml: md (first 200 chars): ' + md.slice(0, 200));
    if (log)
        log('convertMarkdownToFinalHtml: pandocArgs: ' + JSON.stringify(pandocArgs));
    if (log)
        log('convertMarkdownToFinalHtml: debugBasePath: ' + debugBasePath);
    if (log)
        log('convertMarkdownToFinalHtml: logDir: ' + logDir);
    if (log)
        log('convertMarkdownToFinalHtml: timestamp: ' + timestamp);
    if (log)
        log('convertMarkdownToFinalHtml: log: ' + typeof log);
    // Use the new pipeline: convert md (Raw_Markdown) to stripped, then to HTML
    const stripped = await (0, pandocUtil_1.macroStrip)(md);
    const html = await (0, pandocUtil_1.runPandocOnStripped)(stripped, 'html', pandocArgs);
    // Inject MathJax config
    const injectedHtml = html.replace(/<\/head>/i, `${MATHJAX_V3_CONFIG}\n</head>`);
    if (debugBasePath) {
        fs.writeFileSync(debugBasePath + '.final.html', injectedHtml, 'utf8');
    }
    if (log)
        log('convertMarkdownToFinalHtml: finished');
    return injectedHtml;
}
