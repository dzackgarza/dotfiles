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
const fs = __importStar(require("fs"));
const yaml = __importStar(require("js-yaml"));
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
        const timestamp = new Date().toISOString().replace(/[:.]/g, '-');
        const logDir = path.resolve(__dirname, '../../logs');
        if (!fs.existsSync(logDir))
            fs.mkdirSync(logDir);
        const logFile = path.join(logDir, 'logs.log');
        function log(msg) {
            const entry = `[${new Date().toISOString()}] ${msg}\n`;
            fs.appendFileSync(logFile, entry);
            console.log(entry);
        }
        log('--- Webview command started ---');
        const md = editor.document.getText();
        const mdPath = path.join(logDir, `input_${timestamp}.md`);
        fs.writeFileSync(mdPath, md, 'utf8');
        log('Saved input markdown to ' + mdPath);
        // Use canonical conversion pipeline, output debug files in workspace root
        const debugBasePath = path.resolve(__dirname, '../../webview_debug');
        try {
            const configPath = path.resolve(__dirname, 'pandoc_global.yaml');
            const config = yaml.load(fs.readFileSync(configPath, 'utf8'));
            const pandocArgs = [
                ...(config.pandoc.args || [])
            ];
            log('Calling convertMarkdownToFinalHtml...');
            const finalHtml = await (0, conversionPipeline_1.convertMarkdownToFinalHtml)(md, debugBasePath, pandocArgs, logDir, timestamp, log);
            const htmlPath = path.join(logDir, `output_${timestamp}.html`);
            fs.writeFileSync(htmlPath, finalHtml, 'utf8');
            log('Saved output HTML to ' + htmlPath);
            log('Setting webview HTML. First 200 chars: ' + finalHtml.slice(0, 200));
            const panel = vscode.window.createWebviewPanel('markdownWebview', 'Markdown Webview', vscode.ViewColumn.Beside, { enableScripts: true });
            panel.webview.html = finalHtml;
        }
        catch (e) {
            log('Pandoc failed: ' + (e && e.message ? e.message : e));
            vscode.window.showErrorMessage('Pandoc failed: ' + (e && e.message ? e.message : e));
            throw e;
        }
        log('--- Webview command finished ---');
        return;
    });
    context.subscriptions.push(webviewDisposable);
}
function deactivate() { }
