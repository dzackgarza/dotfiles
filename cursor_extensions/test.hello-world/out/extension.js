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
exports.activate = activate;
exports.deactivate = deactivate;
const vscode = __importStar(require("vscode"));
const path = __importStar(require("path"));
const conversionPipeline_1 = require("./conversionPipeline");
function activate(context) {
    // Hello World command
    let disposable = vscode.commands.registerCommand('hello-world.sayHello', function () {
        vscode.window.showInformationMessage('Hello from Hello World extension!');
    });
    context.subscriptions.push(disposable);
    // Markdown webview command
    let webviewDisposable = vscode.commands.registerCommand('hello-world.showMarkdownWebview', async function () {
        const editor = vscode.window.activeTextEditor;
        if (!editor || editor.document.languageId !== 'markdown') {
            vscode.window.showErrorMessage('Please open a Markdown file to preview.');
            return;
        }
        const panel = vscode.window.createWebviewPanel('markdownWebview', 'Markdown Webview', vscode.ViewColumn.Beside, { enableScripts: true });
        const md = editor.document.getText();
        // Use canonical conversion pipeline, output debug files in workspace root
        const debugBasePath = path.resolve(__dirname, '../../webview_debug');
        try {
            const pandocTemplatePath = '/home/dzack/dotfiles/cursor_extensions/test.hello-world/pandoc_webview_template.html';
            const pandocArgs = [
                '--template', pandocTemplatePath,
                '--mathjax',
            ];
            const finalHtml = await (0, conversionPipeline_1.convertMarkdownToFinalHtml)(md, debugBasePath, pandocTemplatePath, pandocArgs);
            panel.webview.html = finalHtml;
        }
        catch (e) {
            panel.webview.html = `<!DOCTYPE html><html><body><pre>Failed to render: ${e.stack || e}</pre></body></html>`;
        }
        return;
    });
    context.subscriptions.push(webviewDisposable);
}
function deactivate() { }
