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
exports.runPandoc = runPandoc;
// @ts-ignore
/// <reference types="node" />
const child_process_1 = require("child_process");
const path = __importStar(require("path"));
const fs = __importStar(require("fs"));
const os = __importStar(require("os"));
console.error('LOADED pandocUtil.ts');
function runPandoc(md, callback, templatePath, pandocArgs = []) {
    const logPath = path.resolve(__dirname, 'pandoc_debug.log');
    const timestamp = new Date().toISOString();
    const pandocPath = '/usr/bin/pandoc';
    const inputFormat = 'markdown';
    const outputFormat = 'html5';
    // Write markdown to a temp file
    const tmpDir = os.tmpdir();
    const mdPath = path.join(tmpDir, `pandoc_input_${process.pid}_${Date.now()}.md`);
    const outPath = path.join(tmpDir, `pandoc_output_${process.pid}_${Date.now()}.html`);
    fs.writeFileSync(mdPath, md, 'utf8');
    const args = ['-f', inputFormat, '-t', outputFormat, mdPath, '-o', outPath, '--standalone'];
    if (templatePath) {
        args.push(`--template=${templatePath}`);
    }
    if (pandocArgs && pandocArgs.length > 0) {
        args.push(...pandocArgs);
    }
    fs.appendFileSync(logPath, `[${timestamp}] Invoking: ${pandocPath} ${args.join(' ')}\n`);
    const pandoc = (0, child_process_1.spawn)(pandocPath, args);
    let err = '';
    pandoc.stderr.on('data', (data) => { err += data.toString(); });
    pandoc.on('close', (code) => {
        fs.appendFileSync(logPath, `[${new Date().toISOString()}] Pandoc exited with code ${code}\n`);
        if (err) {
            fs.appendFileSync(logPath, `[${new Date().toISOString()}] Pandoc stderr: ${err}\n`);
        }
        let html = '';
        try {
            html = fs.readFileSync(outPath, 'utf8');
        }
        catch (e) {
            err += `\nFailed to read output file: ${e.stack || e}`;
        }
        // Clean up temp files
        try {
            fs.unlinkSync(mdPath);
        }
        catch { }
        try {
            fs.unlinkSync(outPath);
        }
        catch { }
        callback(code === null ? 1 : code, html, err);
    });
}
