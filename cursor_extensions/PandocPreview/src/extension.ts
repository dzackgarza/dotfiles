import * as vscode from 'vscode';
import * as path from 'path';
import { convertMarkdownToFinalHtml } from './conversionPipeline';
import * as fs from 'fs';
import * as yaml from 'js-yaml';
import { Raw_Markdown } from './pandocUtil';

export function activate(context: vscode.ExtensionContext) {
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
    if (!fs.existsSync(logDir)) fs.mkdirSync(logDir);
    const logFile = path.join(logDir, 'logs.log');
    function log(msg: string) {
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
      const config = yaml.load(fs.readFileSync(configPath, 'utf8')) as any;
      const pandocArgs = [
        ...(config.pandoc.args || [])
      ];
      log('Calling convertMarkdownToFinalHtml...');
      const finalHtml = await convertMarkdownToFinalHtml(md as Raw_Markdown, debugBasePath, pandocArgs, logDir, timestamp, log);
      const htmlPath = path.join(logDir, `output_${timestamp}.html`);
      fs.writeFileSync(htmlPath, finalHtml, 'utf8');
      log('Saved output HTML to ' + htmlPath);
      log('Setting webview HTML. First 200 chars: ' + finalHtml.slice(0, 200));
      const panel = vscode.window.createWebviewPanel(
        'markdownWebview',
        'Markdown Webview',
        vscode.ViewColumn.Beside,
        { enableScripts: true }
      );
      panel.webview.html = finalHtml;
    } catch (e: any) {
      log('Pandoc failed: ' + (e && e.message ? e.message : e));
      vscode.window.showErrorMessage('Pandoc failed: ' + (e && e.message ? e.message : e));
      throw e;
    }
    log('--- Webview command finished ---');
    return;
  });
  context.subscriptions.push(webviewDisposable);
}

export function deactivate() {} 