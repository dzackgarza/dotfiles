const vscode = require('vscode');
const { spawn } = require('child_process');
const path = require('path');
const fs = require('fs');
const { runPandoc } = require('./pandocUtil.js');

function activate(context) {
  let disposable = vscode.commands.registerCommand('hello-world.sayHello', function () {
    vscode.window.showInformationMessage('Hello from Hello World extension!');
  });
  context.subscriptions.push(disposable);

  // Minimal Pandoc-based Markdown webview
  let webviewDisposable = vscode.commands.registerCommand('hello-world.showMarkdownWebview', function () {
    const editor = vscode.window.activeTextEditor;
    if (!editor || editor.document.languageId !== 'markdown') {
      vscode.window.showErrorMessage('Please open a Markdown file to preview.');
      return;
    }
    const panel = vscode.window.createWebviewPanel(
      'markdownWebview',
      'Markdown Webview',
      vscode.ViewColumn.Beside,
      {}
    );
    const md = editor.document.getText();
    runPandoc(md, (code, html, err) => {
      if (code !== 0) {
        let logTail = '';
        const logPath = require('path').resolve(__dirname, 'pandoc_debug.log');
        try {
          const logContent = require('fs').readFileSync(logPath, 'utf8').split('\n');
          logTail = logContent.slice(-20).join('\n');
        } catch (e) {
          logTail = 'Could not read pandoc_debug.log: ' + (e.stack || e);
        }
        panel.webview.html = `<pre>Pandoc failed with code ${code}\n\n--- pandoc_debug.log (last 20 lines) ---\n${logTail}</pre>`;
      } else {
        panel.webview.html = html;
      }
    });
    return;
  });
  context.subscriptions.push(webviewDisposable);
}
exports.activate = activate;

function deactivate() {}
exports.deactivate = deactivate; 