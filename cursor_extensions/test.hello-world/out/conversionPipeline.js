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
async function convertMarkdownToFinalHtml(md, debugBasePath, templatePath, pandocArgs = [], logDir, timestamp, log) {
    if (log)
        log('convertMarkdownToFinalHtml: called');
    // Save stripped markdown after macro stripping
    let strippedMd = undefined;
    const html = await new Promise((resolve, reject) => {
        (0, pandocUtil_1.runPandoc)(md, (code, html, err, stripped, pandocCmd, pandocStdout, pandocStderr) => {
            if (log) {
                log('Pandoc command: ' + (pandocCmd || 'unknown'));
                log('Pandoc return code: ' + code);
                if (pandocStdout)
                    log('Pandoc stdout: ' + pandocStdout);
                if (pandocStderr)
                    log('Pandoc stderr: ' + pandocStderr);
            }
            if (stripped && logDir && timestamp) {
                const strippedPath = require('path').join(logDir, `stripped_${timestamp}.md`);
                fs.writeFileSync(strippedPath, stripped, 'utf8');
                if (log)
                    log('Saved stripped markdown to ' + strippedPath);
            }
            if (code !== 0) {
                if (log)
                    log('Pandoc failed with code ' + code + ': ' + err);
                reject(new Error('Pandoc failed with code ' + code + ': ' + err));
            }
            else {
                resolve(html);
            }
        }, templatePath, pandocArgs, logDir, timestamp, log);
    });
    if (debugBasePath) {
        fs.writeFileSync(debugBasePath + '.final.html', html, 'utf8');
    }
    if (log)
        log('convertMarkdownToFinalHtml: finished');
    return html;
}
