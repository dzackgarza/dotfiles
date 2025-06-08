import * as vscode from 'vscode';
import * as path from 'path';
import { convertMarkdownToFinalHtml } from './conversionPipeline';

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
    const panel = vscode.window.createWebviewPanel(
      'markdownWebview',
      'Markdown Webview',
      vscode.ViewColumn.Beside,
      { enableScripts: true }
    );
    const md = editor.document.getText();
    // Use canonical conversion pipeline, output debug files in workspace root
    const debugBasePath = path.resolve(__dirname, '../../webview_debug');
    try {
      const pandocTemplatePath = '/home/dzack/dotfiles/cursor_extensions/test.hello-world/pandoc_webview_template.html';
      const pandocArgs = [
        '--template', pandocTemplatePath,
      ];
      const finalHtml = await convertMarkdownToFinalHtml(md, debugBasePath, pandocTemplatePath, pandocArgs);
      panel.webview.html = finalHtml;
    } catch (e: any) {
      panel.webview.html = `<!DOCTYPE html><html><body><pre>Failed to render: ${e.stack || e}</pre></body></html>`;
    }
    return;
  });
  context.subscriptions.push(webviewDisposable);
}

export function deactivate() {} 