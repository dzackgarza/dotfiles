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
const conversionPipeline_1 = require("./conversionPipeline");
const mdPath = path.resolve(__dirname, '../test_custom_pandoc.md');
const md = fs.readFileSync(mdPath, 'utf8');
const debugBasePath = path.resolve(__dirname, '../webview_test_output');
const templatePath = path.resolve(__dirname, 'pandoc_webview_template.html');
(async () => {
    // Use canonical conversion pipeline
    let finalHtml;
    try {
        finalHtml = await (0, conversionPipeline_1.convertMarkdownToFinalHtml)(md, debugBasePath, templatePath, ['--mathjax']);
        console.log('Webview HTML output saved to webview_test_output.final.html');
    }
    catch (e) {
        console.error('FAIL: Conversion pipeline failed:', e);
        process.exit(1);
    }
    // Simple check: does the output look like a full HTML document?
    if (!finalHtml.trim().startsWith('<!DOCTYPE html>')) {
        console.error('FAIL: Output is not a full HTML document');
        process.exit(1);
    }
    console.log('PASS: Output is a full HTML document');
    // Additional test: simulate missing template file
    const missingTemplatePath = '/tmp/this_template_does_not_exist.html';
    let errorCaught = false;
    try {
        await (0, conversionPipeline_1.convertMarkdownToFinalHtml)(md, debugBasePath, missingTemplatePath, []);
        console.error('FAIL: Expected error for missing template, but none was thrown');
        process.exit(1);
    }
    catch (e) {
        if (e.message && e.message.includes('Could not find data file')) {
            console.log('PASS: Detected missing template error from Pandoc');
            errorCaught = true;
        }
        else {
            console.error('FAIL: Unexpected error for missing template:', e);
            process.exit(1);
        }
    }
    if (!errorCaught) {
        console.error('FAIL: Missing template error was not detected');
        process.exit(1);
    }
})();
